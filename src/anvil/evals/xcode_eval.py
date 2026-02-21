from __future__ import annotations

import json
import logging
import os
import shutil
import subprocess
import tempfile
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path

import typer
from tqdm import tqdm

from .xcode_cache import XcodeBuildCache, _build_xcodebuild_cmd, _build_xcodebuild_test_cmd, load_xcode_config, resolve_test_package_path
from .xcode_parser import merge_test_results, parse_build_result, parse_xcodebuild_output

logger = logging.getLogger(__name__)


def _copy_task_tests(
    instance_id: str,
    source_tasks_dir: Path | None,
    xcode_config: dict,
    worktree_dir: Path,
) -> bool:
    """Copy the task's ``tests.swift`` into the worktree's test target directory.

    Each task can define a single ``tests.swift`` file at
    ``tasks/<repo>/task-N/tests.swift``.  It is copied into the directory
    given by ``test_files_dest`` in xcode_config.

    For SPM-based test targets (``test_package_path`` set), the file is
    auto-discovered.  For Xcode-project test targets (``test_target`` set),
    the file is also added to the target's compile sources via pbxproj.

    Returns True if the test file was copied.
    """
    if not source_tasks_dir:
        return False

    test_files_dest = xcode_config.get("test_files_dest", "")
    if not test_files_dest:
        return False

    parts = instance_id.split(".")
    task_name = parts[-1] if len(parts) > 1 else instance_id
    tests_file = source_tasks_dir / task_name / "tests.swift"

    if not tests_file.is_file():
        return False

    # Resolve which test_package_path candidate exists at this worktree.
    resolved_pkg = resolve_test_package_path(xcode_config, worktree_dir)
    has_pkg_config = bool(xcode_config.get("test_package_path"))

    if has_pkg_config and not resolved_pkg:
        logger.warning(
            "No test_package_path candidate found at worktree — skipping test copy for %s",
            instance_id,
        )
        return False

    # test_files_dest is relative to the resolved package path when one exists.
    if resolved_pkg:
        dest_dir = worktree_dir / resolved_pkg / test_files_dest
    else:
        dest_dir = worktree_dir / test_files_dest
    dest_dir.mkdir(parents=True, exist_ok=True)

    dst = dest_dir / tests_file.name
    shutil.copy2(str(tests_file), str(dst))
    logger.info("Copied test file %s → %s", tests_file.name, dest_dir)

    # For non-SPM projects, add the file to the Xcode test target via pbxproj.
    test_target = xcode_config.get("test_target", "")
    if test_target and not xcode_config.get("test_package_path"):
        project_rel = xcode_config.get("project", "")
        if project_rel:
            pbxproj_path = worktree_dir / project_rel / "project.pbxproj"
            if pbxproj_path.exists():
                try:
                    from pbxproj import XcodeProject

                    project = XcodeProject.load(str(pbxproj_path))
                    rel_path = str(dst.relative_to(worktree_dir))
                    project.add_file(rel_path, target_name=test_target)
                    project.save()
                    logger.info("Added %s to target %s in pbxproj", rel_path, test_target)
                except Exception as exc:
                    logger.warning("pbxproj injection failed for %s: %s", test_target, exc)

    return True


def eval_single_patch(
    patch: str,
    instance_id: str,
    base_commit: str,
    repo_name: str,
    xcode_config: dict,
    cache: XcodeBuildCache,
    output_dir: Path,
    eval_id: str,
    attempt: int | None = None,
    compile_only: bool = False,
    source_tasks_dir: Path | None = None,
) -> dict | None:
    """Evaluate a single patch using local xcodebuild.

    When *source_tasks_dir* is provided, looks for a ``tests.swift`` file at
    ``<source_tasks_dir>/<task_name>/tests.swift`` and copies it into the
    test target directory configured by ``test_files_dest`` in xcode_config.
    If task tests are present they are **always** run, even when
    *compile_only* is ``True``.

    Returns {"tests": [{"name": ..., "status": ...}, ...]} or None on error.
    """
    tag = f"{instance_id}:{attempt}" if attempt else instance_id
    worktree_dir = None

    try:
        worktree_dir = Path(tempfile.mkdtemp(prefix=f"anvil-eval-{instance_id}-{attempt or 0}-"))

        cache.checkout(repo_name, base_commit, worktree_dir)

        if patch and patch.strip():
            patch_file = worktree_dir / "_anvil_patch.diff"
            patch_file.write_text(patch)
            apply_result = subprocess.run(
                ["git", "apply", "--allow-empty", str(patch_file)],
                cwd=str(worktree_dir),
                capture_output=True,
                text=True,
            )
            if apply_result.returncode != 0:
                fallback = subprocess.run(
                    ["patch", "-p1", "-i", str(patch_file)],
                    cwd=str(worktree_dir),
                    capture_output=True,
                    text=True,
                )
                if fallback.returncode != 0:
                    logger.warning("Patch apply failed for %s: %s", tag, fallback.stderr[:200])
                    return {"tests": [{"name": "patch_apply", "status": "FAILED",
                                       "message": fallback.stderr[:200]}]}
            patch_file.unlink(missing_ok=True)

        has_task_tests = _copy_task_tests(
            instance_id, source_tasks_dir, xcode_config, worktree_dir,
        )

        dd_dir = worktree_dir / "DerivedData"
        build_cmd = _build_xcodebuild_cmd(
            xcode_config, worktree_dir, dd_dir, clean=False, compile_only=compile_only,
        )

        build_result = subprocess.run(
            build_cmd,
            cwd=str(worktree_dir),
            capture_output=True,
            text=True,
            timeout=600,
        )

        build_output = parse_build_result(build_result.returncode, build_result.stdout, build_result.stderr)
        all_stdout = build_result.stdout
        all_stderr = build_result.stderr

        if build_result.returncode != 0:
            _save_eval_output(output_dir, instance_id, attempt, eval_id, build_output,
                              patch, all_stdout, all_stderr)
            return build_output

        run_tests = has_task_tests or not compile_only

        xctest_output = None
        if run_tests:
            # Use a separate DerivedData for the test step when targeting an
            # SPM package.  The main build resolves the package as a project
            # dependency (library only); reusing the same DerivedData causes
            # xcodebuild to miss the auto-generated test scheme.
            test_dd = dd_dir
            if resolve_test_package_path(xcode_config, worktree_dir):
                test_dd = worktree_dir / "DerivedData-tests"
            test_info = _build_xcodebuild_test_cmd(xcode_config, worktree_dir, test_dd)
            if test_info:
                test_cmd, test_cwd = test_info
                test_result = subprocess.run(
                    test_cmd,
                    cwd=str(test_cwd),
                    capture_output=True,
                    text=True,
                    timeout=600,
                )
                all_stdout += "\n" + test_result.stdout
                all_stderr += "\n" + test_result.stderr
                xctest_output = parse_xcodebuild_output(test_result.stdout, test_result.stderr)
                if test_result.returncode != 0 and not xctest_output["tests"]:
                    xctest_output = {"tests": [{"name": "xctest_run", "status": "FAILED",
                                                "message": "xcodebuild test exited with non-zero"}]}
            elif has_task_tests:
                xctest_output = {"tests": [{"name": "unit_test_setup", "status": "FAILED",
                                            "message": "Task tests found but test_scheme/test_destination "
                                                       "not configured in xcode_config.yaml"}]}

        if xctest_output:
            combined = merge_test_results(build_output, xctest_output)
        else:
            combined = build_output

        _save_eval_output(output_dir, instance_id, attempt, eval_id, combined,
                          patch, all_stdout, all_stderr)
        return combined

    except subprocess.TimeoutExpired:
        logger.error("Build timed out for %s", tag)
        result = {"tests": [{"name": "compilation", "status": "FAILED",
                              "message": "Build timed out (600s)"}]}
        _save_eval_output(output_dir, instance_id, attempt, eval_id, result, patch, "", "")
        return result
    except Exception as e:
        logger.error("Error evaluating %s: %s", tag, e)
        return None
    finally:
        if worktree_dir and worktree_dir.exists():
            try:
                cache.cleanup(repo_name, worktree_dir)
            except Exception:
                pass


def _save_eval_output(
    output_dir: Path,
    instance_id: str,
    attempt: int | None,
    eval_id: str,
    output: dict,
    patch: str,
    stdout: str,
    stderr: str,
) -> None:
    """Save eval outputs in the same directory structure as the Modal eval."""
    if attempt is not None:
        eval_dir = output_dir / instance_id / f"attempt_{attempt}" / "eval_results"
    else:
        eval_dir = output_dir / instance_id / "eval_results"

    eval_dir.mkdir(parents=True, exist_ok=True)

    prefix = eval_id
    (eval_dir / f"{prefix}_output.json").write_text(json.dumps(output, indent=2))
    (eval_dir / f"{prefix}_patch.diff").write_text(patch or "")
    (eval_dir / f"{prefix}_stdout.log").write_text(stdout or "")
    if stderr:
        (eval_dir / f"{prefix}_stderr.log").write_text(stderr)


def run_xcode_evals(
    patches: list[dict],
    instances: list[dict],
    dataset_tasks_dir: Path,
    output_dir: Path,
    eval_id: str,
    max_workers: int | None = None,
    compile_only: bool = False,
    dataset_id: str | None = None,
) -> dict[str, bool]:
    """Run Xcode-based evaluation for a batch of patches.

    Args:
        patches: List of dicts with instance_id, patch, attempt keys.
        instances: Instance definitions from instances.yaml.
        dataset_tasks_dir: Path to dataset's tasks/ directory.
        output_dir: Base output directory for results.
        eval_id: Evaluation identifier prefix.
        max_workers: Max concurrent xcodebuild processes.
        compile_only: If True, only check compilation (skip repo-wide tests).
            Per-task unit tests are still run when present.
        dataset_id: Dataset identifier for config lookup.

    Returns:
        Dict mapping "instance_id:attempt_N" to bool pass/fail.
    """
    xcode_config = load_xcode_config(dataset_tasks_dir, dataset_id=dataset_id)
    cache = XcodeBuildCache()

    instance_map = {inst["instance_id"]: inst for inst in instances}

    src_tasks: Path | None = None
    if dataset_id:
        from ..config import source_tasks_dir as _src_tasks_dir
        candidate = _src_tasks_dir(dataset_id)
        if candidate.is_dir():
            src_tasks = candidate

    if max_workers is None:
        cpu_count = os.cpu_count() or 4
        max_workers = max(1, min(cpu_count // 4, 3))

    eval_results: dict[str, bool] = {}

    def _has_tests(iid: str) -> bool:
        if src_tasks is None:
            return False
        task_name = iid.split(".")[-1]
        return (src_tasks / task_name / "tests.swift").is_file()

    n_with_tests = sum(1 for p in patches if _has_tests(p["instance_id"]))
    typer.echo(
        f"Running Xcode evals ({len(patches)} patches, {max_workers} workers, "
        f"compile_only={compile_only}, {n_with_tests} with unit tests)"
    )

    with ProcessPoolExecutor(max_workers=max_workers) as pool:
        future_to_patch = {}
        for patch_sample in patches:
            iid = patch_sample["instance_id"]
            attempt = patch_sample.get("attempt")
            inst = instance_map.get(iid)
            if not inst:
                continue

            future = pool.submit(
                eval_single_patch,
                patch=patch_sample.get("patch", patch_sample.get("model_patch", "")),
                instance_id=iid,
                base_commit=inst["base_commit"],
                repo_name=inst["repo_name"],
                xcode_config=xcode_config,
                cache=cache,
                output_dir=output_dir,
                eval_id=eval_id,
                attempt=attempt,
                compile_only=compile_only,
                source_tasks_dir=src_tasks,
            )
            future_to_patch[future] = patch_sample

        pbar = tqdm(as_completed(future_to_patch), total=len(future_to_patch), desc="Xcode evals", unit="eval")
        for future in pbar:
            patch_sample = future_to_patch[future]
            iid = patch_sample["instance_id"]
            attempt = patch_sample.get("attempt")
            result_key = f"{iid}:attempt_{attempt}" if attempt else iid

            try:
                output = future.result()
            except Exception as e:
                logger.error("Eval failed for %s: %s", result_key, e)
                output = None

            if output is None:
                eval_results[result_key] = False
            else:
                tests = output.get("tests", [])
                failed = [t for t in tests if t["status"] == "FAILED"]
                eval_results[result_key] = len(tests) > 0 and len(failed) == 0

                if attempt is not None:
                    task_results_dir = output_dir / iid / f"attempt_{attempt}" / "eval_results"
                    task_results_dir.mkdir(parents=True, exist_ok=True)
                    (task_results_dir / "eval_results.json").write_text(
                        json.dumps({iid: eval_results[result_key]})
                    )

            passed = sum(eval_results.values())
            total = len(eval_results)
            tag = f"{iid}:{attempt}" if attempt else iid
            status = "pass" if eval_results.get(result_key) else "fail"
            pbar.set_postfix_str(f"{passed}/{total} passed, {tag} {status}")

    (output_dir / "eval_results.json").write_text(json.dumps(eval_results))
    typer.echo(f"Xcode eval complete: {sum(eval_results.values())}/{len(eval_results)} passed")

    return eval_results
