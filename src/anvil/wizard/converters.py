"""Converters for Anvil evaluation format.

Converts task directories to Anvil's evaluation format which includes:
- instances.yaml - List of instances for run-evals
- gold_patches.json - Reference patches for oracle evaluation
- tasks.csv - Combined CSV of all tasks
- dockerfiles/ - Docker image definitions (Modal backend only)
- run_scripts/ - Test execution scripts (Modal backend only)

Supports two task directory layouts:

Docker/Modal layout (instance_info.txt + tasks.csv + task_tests.py):
    task-N/instance_info.txt, task-N/tasks.csv, task-N/task_tests.py

Xcode layout (problem.md + solution.diff, base commits in repo.md):
    repo.md, task-N/problem.md, task-N/solution.diff
"""

from __future__ import annotations

import csv
import io
import os
import json
import re
import shutil
from pathlib import Path
from typing import Annotated

import typer
import yaml

from .models import Task, TestSpec


def _parse_instance_info(instance_info_path: Path) -> dict:
    """Parse instance_info.txt file."""
    content = instance_info_path.read_text()
    result = {}

    for line in content.strip().split("\n"):
        if ": " in line:
            key, value = line.split(": ", 1)
            key = key.strip().lower().replace(" ", "_")
            result[key] = value.strip()

    return result


def _parse_tasks_csv(csv_path: Path) -> dict:
    """Parse tasks.csv file and return the first data row as dict."""
    csv.field_size_limit(1_000_000)
    content = csv_path.read_text()
    reader = csv.DictReader(io.StringIO(content))
    for row in reader:
        return dict(row)
    return {}


def load_task_from_directory(task_dir: Path) -> Task | None:
    """Load a Task from a task directory.

    Expected files:
    - instance_info.txt
    - tasks.csv
    - task_tests.py
    """
    instance_info_path = task_dir / "instance_info.txt"
    tasks_csv_path = task_dir / "tasks.csv"
    tests_path = task_dir / "task_tests.py"

    if not all(p.exists() for p in [instance_info_path, tasks_csv_path, tests_path]):
        return None

    instance_info = _parse_instance_info(instance_info_path)
    csv_data = _parse_tasks_csv(tasks_csv_path)

    # Parse fail_to_pass and pass_to_pass from instance_info
    fail_to_pass = []
    pass_to_pass = []

    fail_str = instance_info.get("fail_to_pass", "[]")
    pass_str = instance_info.get("pass_to_pass", "[]")

    try:
        fail_to_pass = eval(fail_str) if fail_str else []
    except Exception as e:
        import sys

        print(
            f"Warning: Failed to parse fail_to_pass in {task_dir.name}: {e}",
            file=sys.stderr,
        )
        fail_to_pass = []

    try:
        pass_to_pass = eval(pass_str) if pass_str else []
    except Exception as e:
        import sys

        print(
            f"Warning: Failed to parse pass_to_pass in {task_dir.name}: {e}",
            file=sys.stderr,
        )
        pass_to_pass = []

    return Task(
        task_id=task_dir.name,
        instance_id=instance_info.get(
            "instance_id", f"{task_dir.parent.name}.{task_dir.name}"
        ),
        problem_statement=csv_data.get("problem_statement", ""),
        patch=csv_data.get("patch", ""),
        test_code=tests_path.read_text(),
        test_spec=TestSpec(fail_to_pass=fail_to_pass, pass_to_pass=pass_to_pass),
        base_commit=csv_data.get("base_commit", ""),
        repo=csv_data.get("repo", ""),
        language=csv_data.get("repo_language", "Python"),
        before_repo_set_cmd=csv_data.get("before_repo_set_cmd", ""),
        requirements=csv_data.get("requirements", ""),
        interface=csv_data.get("interface", ""),
        issue_specificity=csv_data.get("issue_specificity", ""),
        issue_categories=csv_data.get("issue_categories", ""),
    )


def _parse_repo_md(repo_md_path: Path) -> dict[str, dict]:
    """Parse repo.md to extract per-task metadata (base_commit, type, etc.).

    Returns a dict keyed by task number string,
    e.g. {"1": {"base_commit": "abc...", "type": "Bug Fix"}, ...}
    """
    text = repo_md_path.read_text()
    tasks: dict[str, dict] = {}
    current_task_num: str | None = None

    for line in text.splitlines():
        header_match = re.match(r"^(\d+)\.\s+", line)
        if header_match:
            current_task_num = header_match.group(1)
            tasks[current_task_num] = {}
            continue

        if current_task_num is None:
            continue

        meta_match = re.match(r"^-\s+(.+?):\s+(.+)$", line)
        if meta_match:
            key = meta_match.group(1).strip().lower().replace(" ", "_")
            value = meta_match.group(2).strip()
            tasks[current_task_num][key] = value

    return tasks


def _load_xcode_task(task_dir: Path, repo_name: str, base_commit: str) -> Task | None:
    """Load a Task from an Xcode-style task directory (problem.md + solution.diff)."""
    problem_path = task_dir / "problem.md"
    solution_path = task_dir / "solution.diff"

    if not problem_path.exists() or not solution_path.exists():
        return None

    return Task(
        task_id=task_dir.name,
        instance_id=f"{repo_name}.{task_dir.name}",
        problem_statement=problem_path.read_text(),
        patch=solution_path.read_text(),
        test_code="",
        test_spec=TestSpec(),
        base_commit=base_commit,
        repo=repo_name,
        language="Swift",
    )


def load_all_tasks(dataset_path: Path) -> list[Task]:
    """Load all tasks from a dataset directory.

    Tries the Docker/Modal format first (instance_info.txt + tasks.csv +
    task_tests.py).  Falls back to the Xcode format (problem.md +
    solution.diff) using repo.md for base commits.
    """
    tasks = []

    task_dirs = sorted(
        [d for d in dataset_path.iterdir() if d.is_dir() and d.name.startswith("task-")],
        key=lambda d: d.name,
    )

    # Try Docker/Modal format first
    for item in task_dirs:
        task = load_task_from_directory(item)
        if task:
            tasks.append(task)

    if tasks:
        return tasks

    # Fall back to Xcode format (problem.md + solution.diff + repo.md)
    repo_md = dataset_path / "repo.md"
    if not repo_md.exists():
        return []

    repo_name = dataset_path.name
    task_meta = _parse_repo_md(repo_md)

    for item in task_dirs:
        task_num = item.name.split("-")[1]
        meta = task_meta.get(task_num, {})
        base_commit = meta.get("base_commit", "")
        if not base_commit:
            import sys
            print(f"Warning: {item.name}: no base_commit in repo.md for task {task_num}", file=sys.stderr)
            continue

        task = _load_xcode_task(item, repo_name, base_commit)
        if task:
            tasks.append(task)

    return tasks


def generate_instances_yaml(
    tasks: list[Task],
    dockerhub_username: str,
    dockerhub_repo: str,
    dataset_id: str,
) -> str:
    """Generate instances.yaml content for Anvil's run-evals."""
    instances = []

    for task in tasks:
        repo_name = task.instance_id.partition(".")[0]

        instance: dict = {
            "instance_id": task.instance_id,
            "repo_name": repo_name,
            "base_commit": task.base_commit,
            "problem_statement": task.problem_statement,
        }

        if dockerhub_username:
            instance["image_name"] = f"{dockerhub_username}/{dockerhub_repo}:{task.instance_id}"
        if task.before_repo_set_cmd:
            instance["before_repo_set_cmd"] = task.before_repo_set_cmd

        instances.append(instance)

    return yaml.dump(instances, default_flow_style=False, sort_keys=False)


def generate_gold_patches_json(tasks: list[Task]) -> str:
    """Generate gold_patches.json for oracle evaluation."""
    patches = []

    for task in tasks:
        patch_entry = {
            "instance_id": task.instance_id,
            "patch": task.patch,
            "prefix": "gold",
        }
        patches.append(patch_entry)

    return json.dumps(patches, indent=2)


def generate_combined_tasks_csv(tasks: list[Task]) -> str:
    """Generate combined tasks.csv with all tasks."""
    output = io.StringIO()
    writer = csv.writer(output, quoting=csv.QUOTE_MINIMAL)

    # Header
    header = [
        "repo",
        "instance_id",
        "base_commit",
        "patch",
        "test_patch",
        "problem_statement",
        "requirements",
        "interface",
        "repo_language",
        "fail_to_pass",
        "pass_to_pass",
        "issue_specificity",
        "issue_categories",
        "before_repo_set_cmd",
        "selected_test_files_to_run",
    ]
    writer.writerow(header)

    # Data rows
    for task in tasks:
        row = [
            task.repo,
            task.instance_id,
            task.base_commit,
            task.patch,
            "",  # test_patch
            task.problem_statement,
            task.requirements,
            task.interface,
            task.language,
            str(task.test_spec.fail_to_pass),
            str(task.test_spec.pass_to_pass),
            task.issue_specificity,
            task.issue_categories,
            task.before_repo_set_cmd,
            str([f"tasks/{task.task_id}/task_tests.py"]),
        ]
        writer.writerow(row)

    return output.getvalue()


def convert_to_anvil_structure(
    dataset_path: Path,
    output_path: Path,
    dockerhub_username: str,
    dockerhub_repo: str,
) -> dict[str, list[Path]]:
    """Convert a task directory to Anvil evaluation format.

    Handles both Docker/Modal datasets and Xcode datasets.
    Returns dict of created file paths by category.
    """
    dataset_id = dataset_path.name
    tasks = load_all_tasks(dataset_path)

    if not tasks:
        raise ValueError(f"No tasks found in {dataset_path}")

    project_name = tasks[0].instance_id.partition(".")[0]
    has_docker = (dataset_path / "Dockerfile").exists()

    created_files: dict[str, list[Path]] = {
        "config": [],
        "dockerfiles": [],
        "run_scripts": [],
    }

    output_path.mkdir(parents=True, exist_ok=True)

    # --- Docker/Modal artifacts (only when a Dockerfile is present) ---
    if has_docker:
        dockerfiles_base_dir = (
            output_path / "dockerfiles" / "docker_image_creation" / project_name
        )
        dockerfiles_base_dockerfile_dir = (
            output_path / "dockerfiles" / "base_dockerfile" / project_name
        )
        dockerfiles_instance_dir = output_path / "dockerfiles" / "instance_dockerfile"
        run_scripts_dir = output_path / "run_scripts"

        dockerfiles_base_dir.mkdir(parents=True, exist_ok=True)
        dockerfiles_base_dockerfile_dir.mkdir(parents=True, exist_ok=True)
        dockerfiles_instance_dir.mkdir(parents=True, exist_ok=True)
        run_scripts_dir.mkdir(parents=True, exist_ok=True)

        base_dockerfile = dataset_path / "Dockerfile"
        dest = dockerfiles_base_dir / "Dockerfile"
        shutil.copy(base_dockerfile, dest)
        created_files["dockerfiles"].append(dest)

        dest_base = dockerfiles_base_dockerfile_dir / "Dockerfile"
        shutil.copy(base_dockerfile, dest_base)
        created_files["dockerfiles"].append(dest_base)

        requirements_txt = dataset_path / "requirements.txt"
        if requirements_txt.exists():
            dest_req = dockerfiles_base_dir / "requirements.txt"
            shutil.copy(requirements_txt, dest_req)
            created_files["dockerfiles"].append(dest_req)

        repo_dir = dataset_path / project_name
        if repo_dir.is_dir():
            shutil.copytree(repo_dir, dockerfiles_base_dir, dirs_exist_ok=True)

    # --- Docker artifacts for Xcode datasets (auto-generated from repos/) ---
    if not has_docker:
        from ..config import repo_root as _repo_root
        repo_source = _repo_root() / "repos" / project_name

        if repo_source.is_dir():
            # Get the remote URL so the Dockerfile can clone the repo
            import subprocess
            remote_url = ""
            try:
                result = subprocess.run(
                    ["git", "remote", "get-url", "origin"],
                    cwd=str(repo_source), capture_output=True, text=True,
                )
                if result.returncode == 0:
                    remote_url = result.stdout.strip()
            except FileNotFoundError:
                pass

            dockerfiles_base_dir = (
                output_path / "dockerfiles" / "docker_image_creation" / project_name
            )
            dockerfiles_base_dockerfile_dir = (
                output_path / "dockerfiles" / "base_dockerfile" / project_name
            )
            dockerfiles_instance_dir = output_path / "dockerfiles" / "instance_dockerfile"

            dockerfiles_base_dir.mkdir(parents=True, exist_ok=True)
            dockerfiles_base_dockerfile_dir.mkdir(parents=True, exist_ok=True)
            dockerfiles_instance_dir.mkdir(parents=True, exist_ok=True)

            if remote_url:
                base_dockerfile_content = (
                    "FROM ubuntu:24.04\n"
                    "RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*\n"
                    f"RUN git clone {remote_url} /app\n"
                    "WORKDIR /app\n"
                )
            else:
                base_dockerfile_content = (
                    "FROM ubuntu:24.04\n"
                    "RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*\n"
                    "WORKDIR /app\n"
                    "COPY . .\n"
                    "RUN git init\n"
                )

            for dest_dir in [dockerfiles_base_dir, dockerfiles_base_dockerfile_dir]:
                dest = dest_dir / "Dockerfile"
                dest.write_text(base_dockerfile_content)
                created_files["dockerfiles"].append(dest)

            # If no remote URL, copy repo source into build context (minus .git)
            if not remote_url:
                shutil.copytree(
                    repo_source, dockerfiles_base_dir,
                    dirs_exist_ok=True,
                    ignore=shutil.ignore_patterns(".git"),
                )

            # Per-instance Dockerfiles
            for task in tasks:
                instance_docker_dir = dockerfiles_instance_dir / task.instance_id
                instance_docker_dir.mkdir(parents=True, exist_ok=True)
                content = (
                    f"FROM {dockerhub_username}/{dockerhub_repo}:{project_name}.base\n"
                    "WORKDIR /app\n"
                )
                if task.base_commit:
                    content += f"RUN git reset --hard {task.base_commit}\n"
                dest = instance_docker_dir / "Dockerfile"
                dest.write_text(content)
                created_files["dockerfiles"].append(dest)

    # --- Config files (always generated) ---
    instances_yaml = generate_instances_yaml(
        tasks, dockerhub_username, dockerhub_repo, dataset_id
    )
    instances_path = output_path / "instances.yaml"
    instances_path.write_text(instances_yaml)
    created_files["config"].append(instances_path)

    gold_patches = generate_gold_patches_json(tasks)
    gold_patches_path = output_path / "gold_patches.json"
    gold_patches_path.write_text(gold_patches)
    created_files["config"].append(gold_patches_path)

    tasks_csv = generate_combined_tasks_csv(tasks)
    tasks_csv_path = output_path / "tasks.csv"
    tasks_csv_path.write_text(tasks_csv)
    created_files["config"].append(tasks_csv_path)

    # --- Per-task Docker artifacts (only when Dockerfile is present) ---
    if has_docker:
        for task in tasks:
            instance_docker_dir = dockerfiles_instance_dir / task.instance_id
            instance_docker_dir.mkdir(parents=True, exist_ok=True)

            dest = instance_docker_dir / "Dockerfile"
            task_dockerfile = dataset_path / task.task_id / "Dockerfile"
            if task_dockerfile.exists():
                content = task_dockerfile.read_text()
            else:
                content = (
                    f"FROM {dockerhub_username}/{dockerhub_repo}:{project_name}.base\n"
                    "WORKDIR /app\n"
                )
            if task.base_commit:
                content += f"RUN git reset --hard {task.base_commit}\n"
            dest.write_text(content)
            created_files["dockerfiles"].append(dest)

            instance_scripts_dir = run_scripts_dir / task.instance_id
            instance_scripts_dir.mkdir(parents=True, exist_ok=True)

            run_script = dataset_path / task.task_id / "run_script.sh"
            if run_script.exists():
                dest = instance_scripts_dir / "run_script.sh"
                shutil.copy(run_script, dest)
                dest.chmod(0o755)
                created_files["run_scripts"].append(dest)

            parser_py = dataset_path / task.task_id / "parser.py"
            if parser_py.exists():
                dest = instance_scripts_dir / "parser.py"
                shutil.copy(parser_py, dest)
                created_files["run_scripts"].append(dest)

            instance_info = dataset_path / task.task_id / "instance_info.txt"
            if instance_info.exists():
                dest = instance_scripts_dir / "instance_info.txt"
                shutil.copy(instance_info, dest)
                created_files["run_scripts"].append(dest)

    return created_files


def convert_dataset(
    dataset: Annotated[str, typer.Option("--dataset", "-d", help="Dataset path")],
    dockerhub_username: Annotated[
        str, typer.Option("--dockerhub-username", "-u", help="Docker Hub username (defaults to REGISTRY_USERNAME from .env)")
    ] = "",
    dockerhub_repo: Annotated[
        str, typer.Option("--dockerhub-repo", help="Docker Hub repository name")
    ] = "",
    output_dir: Annotated[
        Path | None, typer.Option("--output-dir", "-o", help="Output directory")
    ] = None,
) -> None:
    """Convert dataset to Anvil evaluation format.

    Generates instances.yaml, gold_patches.json, and the directory structure
    required for Anvil's publish-images and run-evals commands.
    """
    dockerhub_username = dockerhub_username or os.environ.get("REGISTRY_USERNAME", "")
    dockerhub_repo = dockerhub_repo or os.environ.get("REGISTRY_REPO", "anvil-images")

    # Resolve dataset path
    dataset_path = Path(dataset)
    if not dataset_path.is_absolute():
        dataset_path = Path.cwd() / dataset

    if not dataset_path.exists():
        typer.secho(
            f"Error: Dataset directory does not exist: {dataset_path}",
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)

    # Determine output directory.
    # Default: datasets/<name>/tasks/ so downstream commands use
    # --dataset datasets/<name> and tasks_dir() finds instances.yaml.
    if output_dir:
        output_path = output_dir
    else:
        from ..config import repo_root
        output_path = repo_root() / "datasets" / dataset_path.name / "tasks"

    typer.echo(f"Converting dataset {dataset_path.name} to Anvil format...")
    typer.echo(f"Output directory: {output_path}")

    try:
        created_files = convert_to_anvil_structure(
            dataset_path=dataset_path,
            output_path=output_path,
            dockerhub_username=dockerhub_username,
            dockerhub_repo=dockerhub_repo,
        )
    except ValueError as e:
        typer.secho(f"Error: {e}", fg=typer.colors.RED)
        raise typer.Exit(1)

    # Summary
    typer.secho("\nConversion completed successfully!", fg=typer.colors.GREEN)

    typer.echo("\nCreated files:")
    typer.echo("  Config:")
    for f in created_files["config"]:
        typer.echo(f"    - {f.relative_to(output_path)}")

    if created_files["dockerfiles"]:
        typer.echo(f"  Dockerfiles: {len(created_files['dockerfiles'])} files")
    if created_files["run_scripts"]:
        typer.echo(f"  Run scripts: {len(created_files['run_scripts'])} files")

    dataset_name = dataset_path.name
    ds_path = f"datasets/{dataset_name}"
    has_xcode_config = (dataset_path / "xcode_config.yaml").exists()
    typer.echo("\nNext steps:")
    if has_xcode_config:
        typer.echo(f"  1. Warm cache:      anvil warm-xcode-cache --dataset {ds_path}")
        typer.echo(f"  2. Oracle eval:     anvil run-evals --dataset {ds_path} --agent oracle --compile-only")
        typer.echo(f"  3. Publish images:  anvil publish-images --dataset {ds_path}")
        typer.echo(f"  4. Agent eval:      anvil run-evals --dataset {ds_path} --agent mini-swe-agent --model <model> --compile-only")
    else:
        typer.echo(f"  1. Publish images:  anvil publish-images --dataset {ds_path}")
        typer.echo(f"  2. Run evaluation:  anvil run-evals --dataset {ds_path} --agent oracle")
