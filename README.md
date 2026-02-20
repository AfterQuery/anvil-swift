# Anvil Swift

- [IOS Bench Planning](https://docs.google.com/document/d/1Z4GBUpmrXLeStbd7piRd--3_QEBh5qOoUvYEyTonEww/edit?usp=sharing)
- [IOS SWE Bench Run Results](https://docs.google.com/spreadsheets/d/1Nakl-DBZibBaoPCxJI6aNfICPZPnfrgeM5ZTV-NkF9s/edit?usp=sharing)

## Setup

**1. Install dependencies**

```bash
uv venv
source .venv/bin/activate
uv sync
```

**2. Configure environment**

Copy `.env.example` to `.env` and fill in:

- `OPENROUTER_API_KEY` (or whichever provider you're using)
- `REGISTRY_USERNAME` - your Docker Hub username
- `REGISTRY_PASSWORD` - a Docker Hub [access token](https://hub.docker.com/settings/security)

**3. Authenticate services**

Make sure Docker is running locally, then:

```bash
modal setup          # Modal account for sandboxed execution
docker login         # Docker Hub for image pulls
```

**4. Create a private Docker Hub repository**

Go to [hub.docker.com](https://hub.docker.com) and create a new **private** repository (e.g., `anvil-images`).

> ⚠️ Public repos will not work—Anvil refuses to push task images to public repositories to prevent data leakage.

## Usage

### Publish task images

Build and push Docker images for a dataset to your private repo:

```bash
anvil publish-images --dataset datasets/file-utilization
```

The username and repo are read from `REGISTRY_USERNAME` and `REGISTRY_REPO` in `.env` (or pass `-u <username>` / `--repo <name>` to override).

Modal sandboxes pull images from Docker Hub, so task images need to be pushed there first.

To remove local anvil images: `docker rmi $(docker images $(grep REGISTRY_USERNAME .env | cut -d= -f2)/anvil-images -q) --force`

### Run evaluations

Run an agent on all tasks and evaluate the patches:

```bash
anvil run-evals \
  --model openrouter/google/gemini-2.5-flash \
  --dataset datasets/file-utilization \
  --agent mini-swe-agent \
  --n-attempts 3
```

Use `--n-attempts` to control how many runs per task (useful for pass@k metrics). Results are saved to `<dataset>/runs/<agent>_<model>/`.

> 💡 **Progress is saved automatically** to minimize costs. If you re-run the same command, completed tasks are skipped—nothing runs on Modal for those tasks. Use `--no-continue` to start fresh.

### Oracle Agent

Use the `oracle` agent to validate your task harnesses before running LLM agents:

```bash
# Oracle: applies gold patches - all tests should PASS
anvil run-evals \
  --dataset datasets/my-dataset \
  --agent oracle
```

The oracle agent skips LLM rollouts and applies gold patches from `gold_patches.json` directly. All tests should pass if your harness is correct.

**Prerequisites**: Requires Modal and Docker Hub setup (see [Setup](#setup)).

### Local Xcode evaluation (macOS)

Instead of running evals in Docker containers via Modal, you can compile and test patches locally with Xcode. This is faster for iOS/Swift datasets and doesn't require Docker Hub or Modal.

**Prerequisites**

- macOS with Xcode installed (`xcode-select --install` if needed)
- iOS platform component downloaded: `xcodebuild -downloadPlatform iOS`
- Source repos cloned into `repos/` (e.g. `repos/ACHNBrowserUI/`)

**Step 1: Warm the build cache (one-time)**

Pre-builds every base commit so subsequent evals only do fast incremental builds:

```bash
anvil warm-xcode-cache --dataset datasets/ACHNBrowserUI
```

Cached DerivedData is stored in `~/.anvil/xcode-cache/`. This takes a few minutes per unique base commit but only needs to run once.

**Step 2: Run evals with the Xcode backend**

```bash
# Compile-only check (fastest — just verifies the patch compiles)
anvil run-evals \
  --dataset datasets/ACHNBrowserUI \
  --agent oracle \
  --eval-backend xcode \
  --compile-only

# Full eval (compile + existing pytest structural tests)
anvil run-evals \
  --dataset datasets/ACHNBrowserUI \
  --model openrouter/anthropic/claude-sonnet-4.5 \
  --agent mini-swe-agent \
  --eval-backend xcode \
  --n-attempts 4
```

Each dataset needs a `xcode_config.yaml` in its source tasks directory (e.g. `tasks/ACHNBrowserUI/xcode_config.yaml`) specifying the Xcode project/workspace, scheme, and build destination.

### Options

| Flag                   | Default                 | Description                                         |
| ---------------------- | ----------------------- | --------------------------------------------------- |
| `--model`              | —                       | Model ID (required for agents, optional for oracle) |
| `--dataset`            | —                       | Dataset ID or path                                  |
| `--dockerhub-username` | `REGISTRY_USERNAME` env | Docker Hub username                                 |
| `--dockerhub-repo`     | `anvil-images`          | Docker Hub repo name                                |
| `--agent`              | mini-swe-agent          | Agent to use (`mini-swe-agent` or `oracle`)         |
| `--n-attempts`         | 1                       | Attempts per task (for pass@k)                      |
| `--max-parallel`       | 30                      | Concurrent agent runs                               |
| `--no-continue`        | false                   | Start fresh, ignore previous results                |
| `--max-wait`           | auto                    | Minutes to wait for Modal rate limits               |
| `--eval-backend`       | `modal`                 | `modal` (Docker/Modal) or `xcode` (local macOS)    |
| `--compile-only`       | false                   | Xcode backend: only check compilation, skip tests   |

## Creating Custom Tasks

Anvil includes a task creation wizard to help you build your own evaluation datasets.

Swift Repos

- [PullToDismiss](https://github.com/sgr-ksmt/PullToDismiss)
  - [EdgeShadow Feature](https://github.com/sgr-ksmt/PullToDismiss/pull/10)

### Quick Start

```bash
# Clone Repo and setup tasks
git clone https://github.com/sgr-ksmt/PullToDismiss.git

# Pull golden patch for an issue
curl -L https://github.com/mssun/passforios/pull/496.diff -o solution.diff

# 1. Initialize dataset with your repository
source .venv/bin/activate

anvil init-dataset -d my-dataset --repo-path ./my-repo --base-image golang:1.22

anvil init-dataset -d iOS-Open-GPX-Tracker --repo-path /Users/marvindeng/VS_Code_Projects/anvil/repos/iOS-Open-GPX-Tracker --base-image swift:5.9

# 2. Add tasks (problem statement + solution patch + tests)
anvil add-task -d my-dataset \
  --problem-file problem.md \
  --patch-file solution.diff \
  --tests-file tests.py \
  --fail-to-pass "test_feature_works,test_edge_case"

anvil add-task -d datasets/GPX-Tracker -n 4 --base-commit fa320f1cc5cfe1e58ac538c22e5165a08dc34b8a

# 3. Convert to Anvil evaluation format
[Dockerhub](https://hub.docker.com/repositories/marvindeng)

anvil convert-dataset -d my-dataset

anvil convert-dataset -d datasets/GPX-Tracker

# 4. Publish image
anvil publish-images -d my-dataset

anvil publish-images --dataset datasets/GPX-Tracker

# Remove cached builds
docker builder prune -f

# 5. Run base and Oracle
anvil run-evals -d my-dataset --agent oracle --no-continue

# All tests pass with gold patch (oracle)
anvil run-evals --dataset datasets/GPX-Tracker --agent oracle --no-continue

# 6. Run against models

# Claude Sonnet 4.5
anvil run-evals \
  --dataset datasets/GPX-Tracker \
  --agent mini-swe-agent \
  --model openrouter/anthropic/claude-sonnet-4.5 \
  --no-continue \
  --n-attempts 4

# Claude Opus 4.6
anvil run-evals \
  --dataset datasets/GPX-Tracker \
  --agent mini-swe-agent \
  --model openrouter/anthropic/claude-opus-4.6 \
  --no-continue \
  --n-attempts 4

# GPT 5.2
anvil run-evals \
  --dataset datasets/GPX-Tracker \
  --agent mini-swe-agent \
  --model openrouter/openai/gpt-5.2 \
  --no-continue \
  --n-attempts 4

# GPT 5.2 Codex
anvil run-evals \
  --dataset datasets/GPX-Tracker \
  --agent mini-swe-agent \
  --model openrouter/openai/gpt-5.2-codex \
  --no-continue \
  --n-attempts 4

# Gemini 3 Pro
anvil run-evals \
  --dataset datasets/GPX-Tracker \
  --agent mini-swe-agent \
  --model openrouter/google/gemini-3-pro-preview \
  --no-continue \
  --n-attempts 4

# Llama 4 Maverick
anvil run-evals \
  --dataset datasets/GPX-Tracker \
  --agent mini-swe-agent \
  --model openrouter/meta-llama/llama-4-maverick \
  --no-continue \
  --n-attempts 4

# Qwen 3 Coder Next
anvil run-evals \
  --dataset datasets/GPX-Tracker \
  --agent mini-swe-agent \
  --model openrouter/qwen/qwen3-coder-next \
  --no-continue \
  --n-attempts 4

# Deepseek V3.2
anvil run-evals \
  --dataset datasets/GPX-Tracker \
  --agent mini-swe-agent \
  --model openrouter/deepseek/deepseek-v3.2 \
  --no-continue \
  --n-attempts 4


See **[docs/TASK_CREATION_GUIDE.md](docs/TASK_CREATION_GUIDE.md)** for the complete guide including:

- Writing effective structural tests
- Task file format reference
- Troubleshooting tips
- Full workflow example

## How it works

1. **Agent phase**: Each task runs in a Modal sandbox using the pre-built Docker image. The agent (mini-swe-agent) receives the problem statement and generates a patch.

2. **Eval phase**: Patches are applied and test harnesses run inside containers. Results are aggregated into pass/fail per task.

3. **Output**: Trajectories, patches, stdout/stderr, and eval results are saved per-task. A summary with pass@k metrics is printed at the end.
```
