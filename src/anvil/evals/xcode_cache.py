from __future__ import annotations

import logging
import os
import shutil
import subprocess
from pathlib import Path

import typer

logger = logging.getLogger(__name__)

DEFAULT_CACHE_ROOT = Path.home() / ".anvil" / "xcode-cache"


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


def _build_xcodebuild_cmd(
    xcode_config: dict,
    work_dir: Path,
    derived_data_dir: Path,
    clean: bool = False,
    compile_only: bool = False,
) -> list[str]:
    """Build the xcodebuild command from config.

    If both workspace and project are specified, prefers the workspace when it
    exists at the worktree path, otherwise falls back to the project.
    """
    project = xcode_config.get("project", "")
    workspace = xcode_config.get("workspace", "")
    scheme = xcode_config["scheme"]
    destination = xcode_config.get(
        "destination",
        "generic/platform=iOS Simulator",
    )

    cmd = ["xcodebuild"]

    if clean:
        cmd.append("clean")
    cmd.append("build")

    workspace_path = work_dir / workspace if workspace else None
    project_path = work_dir / project if project else None

    if workspace_path and workspace_path.exists():
        cmd.extend(["-workspace", str(workspace_path)])
    elif project_path and project_path.exists():
        cmd.extend(["-project", str(project_path)])
    elif workspace:
        cmd.extend(["-workspace", str(workspace_path)])
    elif project:
        cmd.extend(["-project", str(project_path)])

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
        cmd.extend([
            "COMPILER_INDEX_STORE_ENABLE=NO",
        ])

    return cmd


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
