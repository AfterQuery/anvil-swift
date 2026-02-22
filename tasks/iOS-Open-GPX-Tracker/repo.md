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

## Existing Unit Tests

- `OpenGpxTrackerTests/OpenGpxTrackerTests.swift` — placeholder tests only (testExample, testPerformanceExample)
- Test target `OpenGpxTrackerTests` is configured in the Xcode project but has no real test cases

> Note: This repo has no meaningful unit tests. Evaluation relies on compilation checks via Xcode.

## Commands

```bash

# Step 1: (Run only once) Warm Xcode build cache (~5 min per unique base commit)
anvil warm-xcode-cache --dataset datasets/iOS-Open-GPX-Tracker

# Step 2: Convert dataset (reads tasks/, writes to datasets/)
anvil convert-dataset --dataset tasks/iOS-Open-GPX-Tracker

# Step 3: Verify gold patches compile (no Modal/Docker needed)
anvil run-evals --dataset datasets/iOS-Open-GPX-Tracker --agent oracle --compile-only --no-continue

# Step 4: Publish Docker images (required for LLM agent runs — agents run in Modal)
anvil publish-images --dataset datasets/iOS-Open-GPX-Tracker

# Step 5: Run against models (agent rollout via Modal, eval via local Xcode)
anvil run-evals --dataset datasets/iOS-Open-GPX-Tracker --agent mini-swe-agent --model openrouter/anthropic/claude-opus-4.6 --compile-only --n-attempts 4 --no-continue

anvil run-evals --dataset datasets/iOS-Open-GPX-Tracker --agent mini-swe-agent --model openrouter/anthropic/claude-sonnet-4.5 --compile-only --n-attempts 4 --no-continue

anvil run-evals --dataset datasets/iOS-Open-GPX-Tracker --agent mini-swe-agent --model openrouter/openai/gpt-5.2 --compile-only --n-attempts 4 --no-continue

anvil run-evals --dataset datasets/iOS-Open-GPX-Tracker --agent mini-swe-agent --model openrouter/openai/gpt-5.2-codex --compile-only --n-attempts 4 --no-continue

anvil run-evals --dataset datasets/iOS-Open-GPX-Tracker --agent mini-swe-agent --model openrouter/google/gemini-3-pro-preview --compile-only --n-attempts 4 --no-continue

anvil run-evals --dataset datasets/iOS-Open-GPX-Tracker --agent mini-swe-agent --model openrouter/qwen/qwen3-coder-next --compile-only --n-attempts 4 --no-continue

anvil run-evals --dataset datasets/iOS-Open-GPX-Tracker --agent mini-swe-agent --model openrouter/deepseek/deepseek-v3.2 --compile-only --n-attempts 4 --no-continue
```
