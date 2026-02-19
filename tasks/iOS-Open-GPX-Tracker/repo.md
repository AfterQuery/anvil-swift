Mobile GPS Logger: https://github.com/merlos/iOS-Open-GPX-Tracker

## Tasks

1. Fix Scale Bar Color: https://github.com/merlos/iOS-Open-GPX-Tracker/pull/296

- Type: Bug Fix
- Patch: curl -L https://github.com/merlos/iOS-Open-GPX-Tracker/pull/296.diff -o solution.diff
- Patch Commit: 972b742
- Base Commit: 3d3ae151d854187f5e0090dc08faf4246473df7d

2. Migrate to UIAlertController: https://github.com/merlos/iOS-Open-GPX-Tracker/pull/86

- Type: Refactor
- Patch: curl -L https://github.com/merlos/iOS-Open-GPX-Tracker/pull/86.diff -o solution.diff
- Patch Commit: 7072e70
- Base Commit: 19f7c55db93c8526649b783c7bd8a3e480bf5628

3. Add ScaleView on map: https://github.com/merlos/iOS-Open-GPX-Tracker/pull/285

- Type: Feature + Fix
- Patch: curl -L https://github.com/merlos/iOS-Open-GPX-Tracker/pull/285.diff -o solution.diff
- Patch Commit: 93e20d4
- Base Commit: 72c1e361d4ab27c71e46d1384dcaa29dea667f3c

4. Fix IPad Orientation: https://github.com/merlos/iOS-Open-GPX-Tracker/pull/111

- Type: Fix
- Patch: curl -L https://github.com/merlos/iOS-Open-GPX-Tracker/pull/111.diff -o solution.diff
- Patch Commit: 1d3f1b7
- Base Commit: fa320f1cc5cfe1e58ac538c22e5165a08dc34b8a

## Commands

```bash
# 1. Clone repo
git clone https://github.com/merlos/iOS-Open-GPX-Tracker.git repos/iOS-Open-GPX-Tracker

# 2. Initialize dataset
source .venv/bin/activate

anvil init-dataset -d datasets/iOS-Open-GPX-Tracker --repo-path repos/iOS-Open-GPX-Tracker --base-image swift:5.9

# 3. Add all tasks
anvil add-task -d datasets/iOS-Open-GPX-Tracker -n 1 --base-commit 3d3ae151d854187f5e0090dc08faf4246473df7d
anvil add-task -d datasets/iOS-Open-GPX-Tracker -n 2 --base-commit 19f7c55db93c8526649b783c7bd8a3e480bf5628
anvil add-task -d datasets/iOS-Open-GPX-Tracker -n 3 --base-commit 72c1e361d4ab27c71e46d1384dcaa29dea667f3c
anvil add-task -d datasets/iOS-Open-GPX-Tracker -n 4 --base-commit fa320f1cc5cfe1e58ac538c22e5165a08dc34b8a

# 4. Convert to Anvil evaluation format
anvil convert-dataset -d datasets/iOS-Open-GPX-Tracker

# Remove cached builds
docker builder prune -f

# 5. Publish images
anvil publish-images --dataset datasets/iOS-Open-GPX-Tracker

# 6. Verify base (all fail_to_pass tests should fail)
anvil verify-base -d datasets/iOS-Open-GPX-Tracker

# 7. Run oracle (all tests should pass with gold patch)
anvil run-evals --dataset datasets/iOS-Open-GPX-Tracker --agent oracle --no-continue

# 8. Run against models

# Claude Sonnet 4.5
anvil run-evals --dataset datasets/iOS-Open-GPX-Tracker --agent mini-swe-agent --model openrouter/anthropic/claude-sonnet-4.5 --no-continue --n-attempts 4

# Claude Opus 4.6
anvil run-evals --dataset datasets/iOS-Open-GPX-Tracker --agent mini-swe-agent --model openrouter/anthropic/claude-opus-4.6 --no-continue --n-attempts 4

# GPT 5.2
anvil run-evals --dataset datasets/iOS-Open-GPX-Tracker --agent mini-swe-agent --model openrouter/openai/gpt-5.2 --no-continue --n-attempts 4

# GPT 5.2 Codex
anvil run-evals --dataset datasets/iOS-Open-GPX-Tracker --agent mini-swe-agent --model openrouter/openai/gpt-5.2-codex --no-continue --n-attempts 4

# Gemini 3 Pro
anvil run-evals --dataset datasets/iOS-Open-GPX-Tracker --agent mini-swe-agent --model openrouter/google/gemini-3-pro-preview --no-continue --n-attempts 4

# Llama 4 Maverick
anvil run-evals --dataset datasets/iOS-Open-GPX-Tracker --agent mini-swe-agent --model openrouter/meta-llama/llama-4-maverick --no-continue --n-attempts 4

# Qwen 3 Coder Next
anvil run-evals --dataset datasets/iOS-Open-GPX-Tracker --agent mini-swe-agent --model openrouter/qwen/qwen3-coder-next --no-continue --n-attempts 4

# Deepseek V3.2
anvil run-evals --dataset datasets/iOS-Open-GPX-Tracker --agent mini-swe-agent --model openrouter/deepseek/deepseek-v3.2 --no-continue --n-attempts 4
```
