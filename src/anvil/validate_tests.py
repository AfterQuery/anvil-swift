"""CLI command for validating task tests against the unpatched base commit."""

from __future__ import annotations

from typing import Annotated

import typer


def validate_tests(
    dataset: Annotated[
        str,
        typer.Option("--dataset", "-d", help="Dataset ID or path (e.g. datasets/ACHNBrowserUI)"),
    ],
) -> None:
    """Validate that task tests fail on the unpatched base commit.

    For each task with a tests.swift file, runs tests with no patch applied.
    Tests must FAIL — if they pass, they don't actually detect the bug and the
    task is invalid.

    To verify gold patches make tests pass, use: anvil run-evals --agent oracle
    """
    from .evals.xcode_eval import validate_task_tests

    rc = validate_task_tests(dataset_id=dataset)
    raise typer.Exit(rc)
