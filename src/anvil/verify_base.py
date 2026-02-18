"""Verify that tests fail against base (unpatched) images.

Runs each task's test suite against its Docker image WITHOUT applying the gold
patch.  All fail_to_pass tests should FAIL, confirming the harness is correct
and the tests actually detect the missing feature / bug fix.
"""

from __future__ import annotations

import os
import re
import subprocess
from pathlib import Path

import typer
from ruamel.yaml import YAML


def _load_instances(tasks_dir: Path) -> list[dict]:
    """Load instances from instances.yaml."""
    instances_path = tasks_dir / "instances.yaml"
    if not instances_path.exists():
        typer.secho(f"Error: {instances_path} not found. Run convert-dataset first.", fg=typer.colors.RED)
        raise typer.Exit(1)

    yaml = YAML()
    with instances_path.open() as f:
        return yaml.load(f) or []


def _parse_instance_info(info_path: Path) -> tuple[list[str], list[str]]:
    """Parse instance_info.txt to extract fail_to_pass and pass_to_pass test names."""
    fail_to_pass: list[str] = []
    pass_to_pass: list[str] = []

    if not info_path.exists():
        return fail_to_pass, pass_to_pass

    content = info_path.read_text()
    for line in content.strip().splitlines():
        if line.startswith("FAIL_TO_PASS:"):
            value = line.split(":", 1)[1].strip()
            try:
                fail_to_pass = eval(value)  # noqa: S307
            except Exception:
                pass
        elif line.startswith("PASS_TO_PASS:"):
            value = line.split(":", 1)[1].strip()
            try:
                pass_to_pass = eval(value)  # noqa: S307
            except Exception:
                pass

    return fail_to_pass, pass_to_pass


def _parse_pytest_results(output: str) -> dict[str, str]:
    """Parse pytest verbose output into {test_name: status} map."""
    results: dict[str, str] = {}
    pattern = re.compile(
        r"^([\w/.-]+\.py::(?:[\w]+::)?[\w]+)\s+(PASSED|FAILED|SKIPPED|ERROR|XFAIL)",
        re.MULTILINE,
    )
    for match in pattern.finditer(output):
        full_name = match.group(1)
        status = match.group(2)
        parts = full_name.split("::")
        if len(parts) == 3:
            test_name = f"{parts[1]}::{parts[2]}"
        elif len(parts) == 2:
            test_name = parts[1]
        else:
            test_name = full_name
        results[test_name] = status

    return results


def _run_tests_on_image(
    image_name: str,
    run_script_path: Path,
) -> tuple[int, str]:
    """Run tests inside a Docker container against the base image.

    Returns (return_code, combined_output).
    """
    result = subprocess.run(
        [
            "docker", "run", "--rm",
            "-v", f"{run_script_path}:/tmp/run_script.sh:ro",
            image_name,
            "bash", "/tmp/run_script.sh",
        ],
        capture_output=True,
        text=True,
    )
    combined = result.stdout + "\n" + result.stderr
    return result.returncode, combined


def verify_base(
    dataset_id: str = typer.Option(..., "--dataset", "-d", help="Dataset path"),
    dockerhub_username: str = typer.Option("", "--dockerhub-username", "-u", help="Docker Hub username (defaults to REGISTRY_USERNAME from .env)"),
    dockerhub_repo: str = typer.Option("", "--dockerhub-repo", help="Docker Hub repository name"),
) -> None:
    """Run tests against base (unpatched) images to verify fail_to_pass tests fail.

    For each task in the dataset, runs the test suite against the Docker image
    WITHOUT the gold patch applied.  All fail_to_pass tests must FAIL for the
    harness to be considered valid.
    """
    dockerhub_username = dockerhub_username or os.environ.get("REGISTRY_USERNAME", "")
    dockerhub_repo = dockerhub_repo or os.environ.get("REGISTRY_REPO", "anvil-images")

    dataset_path = Path(dataset_id)
    if not dataset_path.is_absolute():
        dataset_path = Path.cwd() / dataset_id

    tasks_dir = dataset_path / "tasks"
    if not tasks_dir.exists():
        typer.secho(
            f"Error: {tasks_dir} not found. Run convert-dataset first.",
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)

    instances = _load_instances(tasks_dir)
    if not instances:
        typer.secho("Error: No instances found in instances.yaml", fg=typer.colors.RED)
        raise typer.Exit(1)

    run_scripts_dir = tasks_dir / "run_scripts"

    total = len(instances)
    passed_tasks: list[str] = []
    failed_tasks: list[str] = []
    error_tasks: list[str] = []

    typer.echo(f"Verifying {total} task(s) against base images...\n")

    for idx, instance in enumerate(instances, 1):
        instance_id = instance.get("instance_id", "unknown")
        image_name = instance.get("image_name", "")

        if not image_name:
            image_name = f"{dockerhub_username}/{dockerhub_repo}:{instance_id}"

        # Locate run_script and instance_info
        instance_scripts_dir = run_scripts_dir / instance_id
        run_script_path = instance_scripts_dir / "run_script.sh"
        instance_info_path = instance_scripts_dir / "instance_info.txt"

        if not run_script_path.exists():
            typer.secho(
                f"[{idx}/{total}] {instance_id} - SKIP (run_script.sh not found)",
                fg=typer.colors.YELLOW,
            )
            error_tasks.append(instance_id)
            continue

        # Load expected test classifications
        fail_to_pass, pass_to_pass = _parse_instance_info(instance_info_path)

        typer.echo(f"[{idx}/{total}] {instance_id} - running tests against base image...")

        # Run tests
        returncode, output = _run_tests_on_image(image_name, run_script_path)

        # Parse pytest results
        test_results = _parse_pytest_results(output)

        if not test_results:
            typer.secho(
                f"  WARNING: No test results parsed from output",
                fg=typer.colors.YELLOW,
            )
            typer.echo(f"  Docker exit code: {returncode}")
            typer.echo(f"  Output (last 500 chars): {output[-500:]}")
            error_tasks.append(instance_id)
            continue

        # Check that fail_to_pass tests actually FAILED
        task_ok = True
        for test_name in fail_to_pass:
            status = test_results.get(test_name)
            if status is None:
                # Try partial match (test name without class prefix)
                for full_name, s in test_results.items():
                    if full_name.endswith(test_name) or test_name.endswith(full_name):
                        status = s
                        break

            if status == "FAILED" or status == "ERROR":
                typer.secho(f"  FAIL_TO_PASS {test_name}: {status} (expected)", fg=typer.colors.GREEN)
            elif status == "PASSED":
                typer.secho(
                    f"  FAIL_TO_PASS {test_name}: PASSED (UNEXPECTED - test should fail on base!)",
                    fg=typer.colors.RED,
                )
                task_ok = False
            elif status is None:
                typer.secho(
                    f"  FAIL_TO_PASS {test_name}: NOT FOUND in output",
                    fg=typer.colors.YELLOW,
                )
                task_ok = False
            else:
                typer.secho(f"  FAIL_TO_PASS {test_name}: {status}", fg=typer.colors.YELLOW)

        # Optionally check pass_to_pass tests still pass
        for test_name in pass_to_pass:
            status = test_results.get(test_name)
            if status is None:
                for full_name, s in test_results.items():
                    if full_name.endswith(test_name) or test_name.endswith(full_name):
                        status = s
                        break

            if status == "PASSED":
                typer.secho(f"  PASS_TO_PASS {test_name}: {status} (expected)", fg=typer.colors.GREEN)
            elif status is not None:
                typer.secho(
                    f"  PASS_TO_PASS {test_name}: {status} (UNEXPECTED - regression test should pass!)",
                    fg=typer.colors.RED,
                )
                task_ok = False

        if task_ok:
            typer.secho(f"  Result: VALID", fg=typer.colors.GREEN)
            passed_tasks.append(instance_id)
        else:
            typer.secho(f"  Result: INVALID", fg=typer.colors.RED)
            failed_tasks.append(instance_id)

        typer.echo("")

    # Summary
    typer.secho("=" * 60, fg=typer.colors.CYAN)
    typer.secho("VERIFICATION SUMMARY", fg=typer.colors.CYAN, bold=True)
    typer.secho("=" * 60, fg=typer.colors.CYAN)
    typer.echo(f"  Total tasks:  {total}")
    typer.secho(f"  Valid:        {len(passed_tasks)}", fg=typer.colors.GREEN)
    if failed_tasks:
        typer.secho(f"  Invalid:      {len(failed_tasks)}", fg=typer.colors.RED)
        for tid in failed_tasks:
            typer.echo(f"    - {tid}")
    if error_tasks:
        typer.secho(f"  Errors/Skips: {len(error_tasks)}", fg=typer.colors.YELLOW)
        for tid in error_tasks:
            typer.echo(f"    - {tid}")

    if failed_tasks:
        typer.echo("")
        typer.secho(
            "Some tasks have tests that PASS on the base image. "
            "These tests do not properly detect the missing feature/fix.",
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)
    elif not error_tasks:
        typer.echo("")
        typer.secho(
            "All fail_to_pass tests correctly fail on the base image!",
            fg=typer.colors.GREEN,
        )
