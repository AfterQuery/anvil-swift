from __future__ import annotations

import json
import logging
import os
import subprocess
import tempfile
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path

import typer
from tqdm import tqdm

from .xcode_cache import XcodeBuildCache, _build_xcodebuild_cmd, load_xcode_config
from .xcode_parser import merge_test_results, parse_build_result

logger = logging.getLogger(__name__)


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
    run_script_path: Path | None = None,
    parser_path: Path | None = None,
) -> dict | None:
    """Evaluate a single patch using local xcodebuild.

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

        dd_dir = worktree_dir / "DerivedData"
        build_cmd = _build_xcodebuild_cmd(
            xcode_config, worktree_dir, dd_dir, clean=False, compile_only=compile_only,
        )

        build_result = subprocess.run(
            build_cmd,
            cwd=str(worktree_dir),
            capture_output=True,
            text=True,
            timeout=300,
        )

        build_output = parse_build_result(build_result.returncode, build_result.stdout, build_result.stderr)

        if build_result.returncode != 0:
            _save_eval_output(output_dir, instance_id, attempt, eval_id, build_output,
                              patch, build_result.stdout, build_result.stderr)
            return build_output

        pytest_output = None
        if run_script_path and run_script_path.exists() and not compile_only:
            pytest_output = _run_pytest_tests(worktree_dir, run_script_path, parser_path)

        if pytest_output:
            combined = merge_test_results(build_output, pytest_output)
        else:
            combined = build_output

        _save_eval_output(output_dir, instance_id, attempt, eval_id, combined,
                          patch, build_result.stdout, build_result.stderr)
        return combined

    except subprocess.TimeoutExpired:
        logger.error("Build timed out for %s", tag)
        result = {"tests": [{"name": "compilation", "status": "FAILED",
                              "message": "Build timed out (300s)"}]}
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


def _run_pytest_tests(
    worktree_dir: Path,
    run_script_path: Path,
    parser_path: Path | None,
) -> dict | None:
    """Run the existing pytest structural tests against the worktree."""
    try:
        test_dir = worktree_dir / "_anvil_tests"
        test_dir.mkdir(exist_ok=True)

        run_script_content = run_script_path.read_text()
        modified_script = run_script_content.replace("/app", str(worktree_dir))

        script_file = test_dir / "run_script.sh"
        script_file.write_text(modified_script)
        script_file.chmod(0o755)

        result = subprocess.run(
            ["bash", str(script_file)],
            cwd=str(worktree_dir),
            capture_output=True,
            text=True,
            timeout=60,
            env={**os.environ, "PATH": os.environ.get("PATH", "/usr/bin:/usr/local/bin")},
        )

        stdout = result.stdout
        stderr = result.stderr

        if parser_path and parser_path.exists():
            stdout_file = test_dir / "stdout.log"
            stderr_file = test_dir / "stderr.log"
            output_file = test_dir / "output.json"
            stdout_file.write_text(stdout)
            stderr_file.write_text(stderr)

            subprocess.run(
                ["python3", str(parser_path), str(stdout_file), str(stderr_file), str(output_file)],
                cwd=str(worktree_dir),
                capture_output=True,
                text=True,
                timeout=30,
            )

            if output_file.exists():
                return json.loads(output_file.read_text())

        return _parse_pytest_fallback(stdout + "\n" + stderr)

    except Exception as e:
        logger.warning("pytest run failed: %s", e)
        return None


def _parse_pytest_fallback(output: str) -> dict:
    """Fallback parser for pytest verbose output."""
    import re
    tests = []
    pattern = re.compile(
        r"^([\w/.-]+\.py::(?:[\w]+::)?[\w]+)\s+(PASSED|FAILED|SKIPPED|ERROR)",
        re.MULTILINE,
    )
    for match in pattern.finditer(output):
        name = match.group(1).split("::")[-1]
        tests.append({"name": name, "status": match.group(2)})
    return {"tests": tests}


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
) -> dict[str, bool]:
    """Run Xcode-based evaluation for a batch of patches.

    Args:
        patches: List of dicts with instance_id, patch, attempt keys.
        instances: Instance definitions from instances.yaml.
        dataset_tasks_dir: Path to dataset's tasks/ directory.
        output_dir: Base output directory for results.
        eval_id: Evaluation identifier prefix.
        max_workers: Max concurrent xcodebuild processes.
        compile_only: If True, only check compilation (skip tests).

    Returns:
        Dict mapping "instance_id:attempt_N" to bool pass/fail.
    """
    import pandas as pd

    xcode_config = load_xcode_config(dataset_tasks_dir)
    cache = XcodeBuildCache()

    instance_map = {inst["instance_id"]: inst for inst in instances}

    tasks_csv = dataset_tasks_dir / "tasks.csv"
    raw_sample_df = pd.read_csv(tasks_csv).fillna("").set_index("instance_id", drop=False)

    if max_workers is None:
        cpu_count = os.cpu_count() or 4
        max_workers = max(1, min(cpu_count // 4, 3))

    eval_results: dict[str, bool] = {}

    typer.echo(f"Running Xcode evals ({len(patches)} patches, {max_workers} workers, compile_only={compile_only})")

    with ProcessPoolExecutor(max_workers=max_workers) as pool:
        future_to_patch = {}
        for patch_sample in patches:
            iid = patch_sample["instance_id"]
            attempt = patch_sample.get("attempt")
            inst = instance_map.get(iid)
            if not inst:
                continue

            run_script = dataset_tasks_dir / "run_scripts" / iid / "run_script.sh"
            parser = dataset_tasks_dir / "run_scripts" / iid / "parser.py"

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
                run_script_path=run_script,
                parser_path=parser,
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
                if iid in raw_sample_df.index:
                    raw_sample = raw_sample_df.loc[iid]
                    passed_tests = {t["name"] for t in output.get("tests", []) if t["status"] == "PASSED"}
                    f2p = set(eval(raw_sample["fail_to_pass"])) if raw_sample["fail_to_pass"] else set()
                    p2p = set(eval(raw_sample["pass_to_pass"])) if raw_sample["pass_to_pass"] else set()
                    result = (f2p | p2p) <= passed_tests
                    eval_results[result_key] = result
                else:
                    eval_results[result_key] = False

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
