from __future__ import annotations

import logging
import os
import shutil
import subprocess
from pathlib import Path

import typer

logger = logging.getLogger(__name__)

DEFAULT_CACHE_ROOT = Path.home() / ".anvil" / "xcode-cache"


def resolve_test_package_path(xcode_config: dict, work_dir: Path) -> str:
    """Resolve ``test_package_path`` to the first candidate that exists.

    ``test_package_path`` may be a single string or a list of candidate paths.
    Returns the first path where ``Package.swift`` exists under *work_dir*,
    or an empty string if none match.
    """
    raw = xcode_config.get("test_package_path", "")
    if not raw:
        return ""
    candidates = raw if isinstance(raw, list) else [raw]
    for candidate in candidates:
        if (work_dir / candidate / "Package.swift").exists():
            return candidate
    return ""


class XcodeBuildCache:
    """Manages pre-built DerivedData caches per (repo, base_commit) pair."""

    def __init__(self, cache_root: Path = DEFAULT_CACHE_ROOT):
        self.cache_root = cache_root
        self.cache_root.mkdir(parents=True, exist_ok=True)

    def _repo_cache_dir(self, repo_name: str) -> Path:
        return self.cache_root / repo_name

    def _commit_cache_dir(self, repo_name: str, base_commit: str) -> Path:
        short = base_commit[:12]
        return self._repo_cache_dir(repo_name) / short

    def _repo_clone_dir(self, repo_name: str) -> Path:
        return self._repo_cache_dir(repo_name) / "_repo"

    def _derived_data_dir(self, repo_name: str, base_commit: str) -> Path:
        return self._commit_cache_dir(repo_name, base_commit) / "DerivedData"

    def is_warm(self, repo_name: str, base_commit: str) -> bool:
        dd = self._derived_data_dir(repo_name, base_commit)
        return dd.exists() and any(dd.iterdir())

    def warm(
        self,
        repo_path: Path,
        repo_name: str,
        base_commit: str,
        xcode_config: dict,
    ) -> Path:
        """Pre-build a base commit and cache DerivedData.

        Returns the path to the cached DerivedData directory.
        """
        dd_dir = self._derived_data_dir(repo_name, base_commit)
        if self.is_warm(repo_name, base_commit):
            logger.info("Cache hit for %s@%s", repo_name, base_commit[:8])
            return dd_dir

        commit_dir = self._commit_cache_dir(repo_name, base_commit)
        commit_dir.mkdir(parents=True, exist_ok=True)

        clone_dir = self._repo_clone_dir(repo_name)
        if not clone_dir.exists():
            typer.echo(f"  Cloning {repo_name} into cache...")
            _run_cmd(["git", "clone", str(repo_path.resolve()), str(clone_dir)])

        work_dir = commit_dir / "worktree"
        if work_dir.exists():
            _run_cmd(["git", "-C", str(clone_dir), "worktree", "remove", "--force", str(work_dir)],
                     check=False)
            if work_dir.exists():
                shutil.rmtree(work_dir)

        typer.echo(f"  Creating worktree at {base_commit[:8]}...")
        _run_cmd(["git", "-C", str(clone_dir), "fetch", "--all"], check=False)
        _run_cmd(["git", "-C", str(clone_dir), "worktree", "add", "--detach", str(work_dir), base_commit])

        typer.echo(f"  Building {repo_name} (full clean build)...")
        dd_dir.mkdir(parents=True, exist_ok=True)

        build_cmd = _build_xcodebuild_cmd(xcode_config, work_dir, dd_dir, clean=True)
        result = subprocess.run(
            build_cmd,
            cwd=str(work_dir),
            capture_output=True,
            text=True,
            timeout=600,
        )

        if result.returncode != 0:
            error_lines = [
                line for line in result.stderr.splitlines()
                if "error:" in line.lower()
            ]
            summary = "\n".join(error_lines[:10]) if error_lines else result.stderr[-500:]
            typer.echo(f"  Build failed for {repo_name}@{base_commit[:8]}:\n{summary}", err=True)
            shutil.rmtree(dd_dir, ignore_errors=True)
            raise RuntimeError(f"xcodebuild failed for {repo_name}@{base_commit[:8]}")

        _run_cmd(["git", "-C", str(clone_dir), "worktree", "remove", "--force", str(work_dir)],
                 check=False)
        if work_dir.exists():
            shutil.rmtree(work_dir, ignore_errors=True)

        typer.echo(f"  Cached DerivedData for {repo_name}@{base_commit[:8]}")
        return dd_dir

    def checkout(
        self,
        repo_name: str,
        base_commit: str,
        target_dir: Path,
    ) -> Path:
        """Create an isolated worktree with pre-built DerivedData.

        Returns target_dir (the worktree root).
        """
        clone_dir = self._repo_clone_dir(repo_name)
        if not clone_dir.exists():
            raise RuntimeError(
                f"No cached repo for {repo_name}. Run 'anvil warm-xcode-cache' first."
            )

        if target_dir.exists():
            self.cleanup(repo_name, target_dir)

        _run_cmd([
            "git", "-C", str(clone_dir),
            "worktree", "add", "--detach", str(target_dir), base_commit,
        ])

        dd_src = self._derived_data_dir(repo_name, base_commit)
        dd_dst = target_dir / "DerivedData"
        if dd_src.exists() and any(dd_src.iterdir()):
            shutil.copytree(str(dd_src), str(dd_dst), symlinks=True)

        return target_dir

    def cleanup(self, repo_name: str, target_dir: Path) -> None:
        """Remove a worktree created by checkout()."""
        clone_dir = self._repo_clone_dir(repo_name)
        if clone_dir.exists():
            _run_cmd(
                ["git", "-C", str(clone_dir), "worktree", "remove", "--force", str(target_dir)],
                check=False,
            )
        if target_dir.exists():
            shutil.rmtree(target_dir, ignore_errors=True)


def _resolve_project_args(xcode_config: dict, work_dir: Path) -> list[str]:
    """Resolve -workspace/-project args, preferring workspace when it exists."""
    workspace = xcode_config.get("workspace", "")
    project = xcode_config.get("project", "")

    workspace_path = work_dir / workspace if workspace else None
    project_path = work_dir / project if project else None

    if workspace_path and workspace_path.exists():
        return ["-workspace", str(workspace_path)]
    elif project_path and project_path.exists():
        return ["-project", str(project_path)]
    elif workspace:
        return ["-workspace", str(workspace_path)]
    elif project:
        return ["-project", str(project_path)]
    return []


def _build_xcodebuild_cmd(
    xcode_config: dict,
    work_dir: Path,
    derived_data_dir: Path,
    clean: bool = False,
    compile_only: bool = False,
) -> list[str]:
    """Build the xcodebuild compile command from config."""
    scheme = xcode_config["scheme"]
    destination = xcode_config.get(
        "destination",
        "generic/platform=iOS Simulator",
    )

    cmd = ["xcodebuild"]
    if clean:
        cmd.append("clean")
    cmd.append("build")

    cmd.extend(_resolve_project_args(xcode_config, work_dir))
    cmd.extend([
        "-scheme", scheme,
        "-destination", destination,
        "-derivedDataPath", str(derived_data_dir),
        "-quiet",
        "ONLY_ACTIVE_ARCH=YES",
        "CODE_SIGNING_ALLOWED=NO",
        "CODE_SIGN_IDENTITY=",
    ])

    if compile_only:
        cmd.append("COMPILER_INDEX_STORE_ENABLE=NO")

    return cmd


def _build_xcodebuild_test_cmd(
    xcode_config: dict,
    work_dir: Path,
    derived_data_dir: Path,
    test_only: list[str] | None = None,
) -> tuple[list[str], Path] | None:
    """Build the xcodebuild test command.

    Returns (cmd, cwd) or None if no test config.

    When ``test_package_path`` is set in the config, the test command targets
    the standalone SPM package (no -project/-workspace flags) and ``cwd`` is
    set to the package directory.  Otherwise the main project is used and
    ``cwd`` is the worktree root.

    Args:
        test_only: Optional list of test identifiers to run, e.g.
            ["BackendTests/ItemsTests", "BackendTests/CrittersTests/testFishDecoding"]
            Uses xcodebuild's -only-testing: flag.
    """
    test_scheme = xcode_config.get("test_scheme", "")
    if not test_scheme:
        return None

    test_destination = xcode_config.get(
        "test_destination",
        xcode_config.get("destination", ""),
    )
    if not test_destination or "generic/" in test_destination:
        return None

    test_package_path = resolve_test_package_path(xcode_config, work_dir)

    cmd = ["xcodebuild", "test"]

    if test_package_path:
        cwd = work_dir / test_package_path
    elif xcode_config.get("test_package_path"):
        logger.warning(
            "No test_package_path candidate has Package.swift at %s — skipping tests",
            work_dir,
        )
        return None
    else:
        cwd = work_dir
        cmd.extend(_resolve_project_args(xcode_config, work_dir))

    cmd.extend([
        "-scheme", test_scheme,
        "-destination", test_destination,
        "-derivedDataPath", str(derived_data_dir),
        "ONLY_ACTIVE_ARCH=YES",
        "CODE_SIGNING_ALLOWED=NO",
        "CODE_SIGN_IDENTITY=",
    ])

    only = test_only or xcode_config.get("test_only", [])
    for target in only:
        cmd.extend(["-only-testing:" + target])

    return cmd, cwd


def _run_cmd(cmd: list[str], check: bool = True, **kwargs) -> subprocess.CompletedProcess:
    logger.debug("Running: %s", " ".join(cmd))
    return subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        check=check,
        **kwargs,
    )


def load_xcode_config(dataset_tasks_dir: Path, dataset_id: str | None = None) -> dict:
    """Load xcode_config.yaml, searching generated and source task dirs."""
    candidates = [dataset_tasks_dir / "xcode_config.yaml"]

    if dataset_id:
        from ..config import source_tasks_dir
        candidates.append(source_tasks_dir(dataset_id) / "xcode_config.yaml")

    for path in candidates:
        if path.exists():
            from ruamel.yaml import YAML
            yaml = YAML()
            return yaml.load(path)

    searched = ", ".join(str(c) for c in candidates)
    raise FileNotFoundError(
        f"No xcode_config.yaml found. Searched: {searched}. "
        "Create one with project/scheme/destination settings."
    )
