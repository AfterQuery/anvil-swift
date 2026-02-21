"""CLI command to pre-warm Xcode build caches for a dataset."""

from __future__ import annotations

from pathlib import Path

import typer
from ruamel.yaml import YAML

from .config import source_tasks_dir, tasks_dir, repo_root
from .evals.xcode_cache import XcodeBuildCache, load_xcode_config


def warm_xcode_cache(
    dataset: str = typer.Option(..., "--dataset", "-d", help="Dataset ID or path"),
) -> None:
    """Pre-build all base commits for a dataset and cache DerivedData.

    This is a one-time setup step. Subsequent evals with --eval-backend xcode
    will use the cached builds for fast incremental compilation.
    """
    dataset_tasks_dir = tasks_dir(dataset)
    src_tasks_dir = source_tasks_dir(dataset)

    yaml = YAML()
    instances = None
    for candidate in [dataset_tasks_dir / "instances.yaml", src_tasks_dir / "instances.yaml"]:
        if candidate.exists():
            instances = yaml.load(candidate)
            typer.echo(f"Loaded instances from {candidate}")
            break

    if not instances:
        typer.echo(
            f"Error: instances.yaml not found.\n"
            f"  Searched: {dataset_tasks_dir / 'instances.yaml'}\n"
            f"           {src_tasks_dir / 'instances.yaml'}",
            err=True,
        )
        raise typer.Exit(1)

    try:
        xcode_config = load_xcode_config(dataset_tasks_dir, dataset_id=dataset)
    except FileNotFoundError as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(1)

    seen_commits: dict[str, str] = {}
    for inst in instances:
        repo_name = inst["repo_name"]
        base_commit = inst["base_commit"]
        key = f"{repo_name}:{base_commit}"
        if key not in seen_commits:
            seen_commits[key] = inst["instance_id"]

    typer.echo(f"Warming Xcode build cache for {dataset}")
    typer.echo(f"  Unique (repo, commit) pairs: {len(seen_commits)}")

    cache = XcodeBuildCache()

    repos_root = repo_root() / "repos"
    for key, example_iid in seen_commits.items():
        repo_name, base_commit = key.split(":", 1)
        repo_path = repos_root / repo_name

        if not repo_path.exists():
            typer.echo(f"  Skipping {repo_name}@{base_commit[:8]}: repo not found at {repo_path}", err=True)
            continue

        try:
            cache.warm(repo_path, repo_name, base_commit, xcode_config)
            typer.echo(f"  {repo_name}@{base_commit[:8]}: cached")
        except Exception as e:
            typer.echo(f"  {repo_name}@{base_commit[:8]}: FAILED - {e}", err=True)

    typer.echo("Cache warming complete.")
