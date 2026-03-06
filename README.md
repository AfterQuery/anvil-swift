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

**2. Install Xcode prerequisites**

```bash
xcode-select --install
xcodebuild -downloadPlatform iOS

# Only required for repos with embedded Watch apps (e.g. iOS-Open-GPX-Tracker)
xcodebuild -downloadPlatform watchOS
```

**3. Configure environment**

Copy `.env.example` to `.env` and fill in:

- `OPENROUTER_API_KEY` (or whichever provider you're using)
- `REGISTRY_USERNAME` - your Docker Hub username
- `REGISTRY_PASSWORD` - a Docker Hub [access token](https://hub.docker.com/settings/security)

**4. Clone source repositories**

Clone the repos you want to evaluate into the `repos/` directory:

```bash
git clone https://github.com/Dimillian/ACHNBrowserUI repos/ACHNBrowserUI
git clone https://github.com/mozilla-mobile/firefox-ios repos/firefox-ios
git clone https://github.com/merlos/iOS-Open-GPX-Tracker repos/iOS-Open-GPX-Tracker
```

**5. Authenticate services**

Make sure Docker is running locally, then:

```bash
modal setup          # Modal account for sandboxed agent execution
docker login         # Docker Hub for image pulls
```

**6. Create a private Docker Hub repository**

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

### Warm the build cache (one-time)

Pre-builds every base commit so subsequent evals only do fast incremental builds:

```bash
anvil warm-xcode-cache --dataset datasets/ACHNBrowserUI
```

Cached DerivedData is stored in `.xcode-cache/` in the project root. This takes a few minutes per unique base commit but only needs to run once.

### Run evaluations

**Via GitHub Actions (recommended):**

Use the [Anvil Eval workflow](https://github.com/AfterQuery/anvil-swift/actions/workflows/eval.yml) to run evaluations in CI. Click **Run workflow**, pick a dataset, model, and agent from the dropdowns, then set the number of attempts. Results are uploaded as artifacts on the workflow run.

**Locally:**

```bash
anvil run-evals \
  --dataset datasets/ACHNBrowserUI \
  --model openrouter/anthropic/claude-sonnet-4.5 \
  --agent mini-swe-agent \
  --n-attempts 4
```

Use `--n-attempts` to control how many runs per task (useful for pass@k metrics). Results are saved to `<dataset>/runs/<agent>_<model>/`.

> 💡 **Progress is saved automatically** to minimize costs. If you re-run the same command, completed tasks are skipped. Use `--no-continue` to start fresh.

### Validate task tests

Check that your `tests.swift` files behave correctly on the unpatched base commit:

```bash
anvil validate-tests --dataset datasets/ACHNBrowserUI
```

Tests are categorized by **class name**:

- Classes containing `F2P` (e.g. `AnvilTask1F2PTests`) — **fail-to-pass**; must fail on base
- All other classes (repo's own tests, `AnvilTask2P2PTests`, etc.) — **pass-to-pass**; must pass on base

The command reports inconsistencies (f2p tests that pass, or p2p tests that fail on the unpatched commit).

### Oracle Agent

Use the `oracle` agent to validate your task harnesses before running LLM agents:

```bash
anvil run-evals --dataset datasets/ACHNBrowserUI --agent oracle
```

The oracle agent skips LLM rollouts and applies gold patches from `gold_patches.json` directly. All tests should pass if your harness is correct.

Each dataset needs a `xcode_config.yaml` in its source tasks directory (e.g. `tasks/ACHNBrowserUI/xcode_config.yaml`) specifying the Xcode project/workspace, scheme, and build destination.

### Options

| Flag                   | Default                 | Description                                         |
| ---------------------- | ----------------------- | --------------------------------------------------- |
| `--model`              | —                       | Model ID (required for agents, optional for oracle) |
| `--dataset`            | —                       | Dataset ID or path                                  |
| `--agent`              | mini-swe-agent          | Agent to use (`mini-swe-agent` or `oracle`)         |
| `--n-attempts`         | 1                       | Attempts per task (for pass@k)                      |
| `--compile-only`       | false                   | Only check compilation, skip unit tests             |
| `--no-continue`        | false                   | Start fresh, ignore previous results                |
| `--max-parallel`       | 30                      | Concurrent agent runs                               |
| `--max-wait`           | auto                    | Minutes to wait for Modal rate limits               |
| `--eval-backend`       | `xcode`                 | `xcode` (local macOS) or `modal` (Docker/Modal)     |
| `--dockerhub-username` | `REGISTRY_USERNAME` env | Docker Hub username (modal backend)                 |
| `--dockerhub-repo`     | `anvil-images`          | Docker Hub repo name (modal backend)                |

## Creating Custom Tasks

Anvil includes a task creation wizard to help you build your own evaluation datasets.

### Quick Start

````bash
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

# 5. Validate task tests on unpatched base commits
anvil validate-tests -d my-dataset

anvil validate-tests --dataset datasets/GPX-Tracker

# 6. Run oracle to verify gold patches pass all tests
anvil run-evals -d my-dataset --agent oracle --no-continue

anvil run-evals --dataset datasets/GPX-Tracker --agent oracle --no-continue

# 7. Run against models

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

## How it works

1. **Agent phase**: Each task runs in a Modal sandbox using a pre-built Docker image. The agent (mini-swe-agent) receives the problem statement and generates a patch.

2. **Eval phase**: Patches are applied to a local worktree with cached DerivedData. `xcodebuild` compiles the patched project and runs per-task unit tests (from `tests.swift`). Each worker gets its own simulator clone to avoid boot conflicts during parallel evaluation.

3. **Output**: Trajectories, patches, stdout/stderr, and eval results are saved per-task. A summary with pass@k metrics is printed at the end.

## Writing task tests

Each task's `tests.swift` is copied into the test target during evaluation. Use XCTest class names to indicate test category:

```swift
// Fail-to-pass: tests new functionality introduced by the gold patch.
// Must FAIL on the unpatched base commit, PASS after the patch.
final class AnvilTask1F2PTests: XCTestCase {
    func testNewFeature() { ... }
}

// Pass-to-pass: regression tests for existing functionality.
// Must PASS on both the base commit and after the patch.
final class AnvilTask1P2PTests: XCTestCase {
    func testExistingBehavior() { ... }
}
````

The repo's own pre-existing tests are automatically treated as pass-to-pass. Run `anvil validate-tests` to verify consistency before running model evaluations.
