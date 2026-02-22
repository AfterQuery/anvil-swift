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
    """Run task tests on the unpatched base commit and check consistency.

    Tests are categorized by class name:
      - Classes containing "P2P" (e.g. AnvilTask1P2PTests) — pass-to-pass; must pass on base.
      - All other classes — fail-to-pass; must fail on base.

    Reports inconsistencies (p2p tests that fail, or f2p tests that pass).

    To verify gold patches make all tests pass, use: anvil run-evals --agent oracle
    """
    from .evals.xcode_eval import validate_task_tests

    rc = validate_task_tests(dataset_id=dataset)
    raise typer.Exit(rc)
