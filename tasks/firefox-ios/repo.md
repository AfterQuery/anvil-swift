Firefox for iOS: https://github.com/mozilla-mobile/firefox-ios

## Tasks

1. Vertical Scrolling Homepage Stories: https://github.com/mozilla-mobile/firefox-ios/pull/31925

- Type: Feature
- Patch: curl -L https://github.com/mozilla-mobile/firefox-ios/pull/31925.diff -o solution.diff
- Patch Commit: d508a61
- Base Commit: b54d1c5b89b142bb7e6135fa090484c4385ef2d1

2. Open Mask Management New Tab: https://github.com/mozilla-mobile/firefox-ios/pull/32021

- Type: Fix
- Patch: curl -L https://github.com/mozilla-mobile/firefox-ios/pull/32021.diff -o solution.diff
- Patch Commit: 11ab43e
- Base Commit: 34d4d846810c903d88007c1f1f5e2c4e8563e9bb

3. Replace Constraints: https://github.com/mozilla-mobile/firefox-ios/pull/31920

- Type: Fix
- Patch: curl -L https://github.com/mozilla-mobile/firefox-ios/pull/31920.diff -o solution.diff
- Patch Commit: 9864541
- Base Commit: 9d4d3d5508a5c758c6c8c42f34b81e400b8a2a74

4. Per Tab Persistence: https://github.com/mozilla-mobile/firefox-ios/pull/32090

- Type: Feature
- Patch: curl -L https://github.com/mozilla-mobile/firefox-ios/pull/32090.diff -o solution.diff
- Patch Commit: 1da9193
- Base Commit: 30c75403d6b6680f3e4215f44351c7bb226484ec

## Existing Unit Tests

- `firefox-ios/firefox-ios-tests/Tests/ClientTests/` — unit tests for client functionality
- `firefox-ios/firefox-ios-tests/Tests/XCUITests/` — UI tests
- `BrowserKit/Tests/` — tests for BrowserKit module (CommonTests, ComponentLibraryTests, WebEngineTests, etc.)
- `focus-ios/focus-ios-tests/` — Focus-specific tests
- ~692 Swift files importing XCTest across the repo

## Commands

```bash

# Step 1: (Run only once) Warm Xcode build cache (~5 min per unique base commit)
anvil warm-xcode-cache --dataset datasets/firefox-ios

# Step 2: Convert dataset (reads tasks/, writes to datasets/)
anvil convert-dataset --dataset tasks/firefox-ios

# Step 3: Verify gold patches compile (no Modal/Docker needed)
anvil run-evals --dataset datasets/firefox-ios --agent oracle --eval-backend xcode --compile-only

# Step 4: Publish Docker images (required for LLM agent runs — agents run in Modal)
anvil publish-images --dataset datasets/firefox-ios

# Step 5: Run against models (agent rollout via Modal, eval via local Xcode)
anvil run-evals --dataset datasets/firefox-ios --agent mini-swe-agent --model openrouter/anthropic/claude-sonnet-4.5 --eval-backend xcode --n-attempts 4

anvil run-evals --dataset datasets/firefox-ios --agent mini-swe-agent --model openrouter/openai/gpt-5.2-codex --eval-backend xcode --n-attempts 4

anvil run-evals --dataset datasets/firefox-ios --agent mini-swe-agent --model openrouter/google/gemini-3-pro-preview --eval-backend xcode --n-attempts 4

anvil run-evals --dataset datasets/firefox-ios --agent mini-swe-agent --model openrouter/deepseek/deepseek-v3.2 --eval-backend xcode --n-attempts 4
```
