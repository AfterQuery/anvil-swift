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

- Type: Refactor
- Patch: curl -L https://github.com/mozilla-mobile/firefox-ios/pull/31920.diff -o solution.diff
- Patch Commit: 9864541
- Base Commit: 9d4d3d5508a5c758c6c8c42f34b81e400b8a2a74

4. Per Tab Persistence: https://github.com/mozilla-mobile/firefox-ios/pull/32090

- Type: Feature
- Patch: curl -L https://github.com/mozilla-mobile/firefox-ios/pull/32090.diff -o solution.diff
- Patch Commit: 1da9193
- Base Commit: 30c75403d6b6680f3e4215f44351c7bb226484ec

5. Fix Homepage Appearance Lifecycle Events: https://github.com/mozilla-mobile/firefox-ios/pull/31825

- Type: Fix
- Patch: curl -L https://github.com/mozilla-mobile/firefox-ios/pull/31825.diff -o solution.diff
- Patch Commit: 8077234
- Base Commit: 1a4def9884b9f23be656511286e446e7eb978cd1

6. Improve Skeleton Bars Performance: https://github.com/mozilla-mobile/firefox-ios/pull/32102

- Type: Refactor
- Patch: curl -L https://github.com/mozilla-mobile/firefox-ios/pull/32102.diff -o solution.diff
- Patch Commit: 9d39377
- Base Commit: 103a7b0fafb7c3b08146b6e15babd16bc6d18453

7. Voice Search Speech Recognizer: https://github.com/mozilla-mobile/firefox-ios/pull/32088

- Type: Feature
- Patch: curl -L https://github.com/mozilla-mobile/firefox-ios/pull/32088.diff -o solution.diff
- Patch Commit: 242f69e
- Base Commit: f63033f2f1d31814d9f41b87a939a23847de123a

8. Per Tab Persistence Vertical Scroll: https://github.com/mozilla-mobile/firefox-ios/pull/32090

- Type: Feature
- Patch: curl -L https://github.com/mozilla-mobile/firefox-ios/pull/32090.diff -o solution.diff
- Patch Commit: 1da9193
- Base Commit: 30c75403d6b6680f3e4215f44351c7bb226484ec

9. Open Mask Management New Tab: https://github.com/mozilla-mobile/firefox-ios/pull/32021

- Type: Fix
- Patch: curl -L https://github.com/mozilla-mobile/firefox-ios/pull/32021.diff -o solution.diff
- Patch Commit: 11ab43e
- Base Commit: 34d4d846810c903d88007c1f1f5e2c4e8563e9bb

10. Fix Animation on Use Saved Cards: https://github.com/mozilla-mobile/firefox-ios/pull/31888

- Type: Fix
- Patch: curl -L https://github.com/mozilla-mobile/firefox-ios/pull/31888.diff -o solution.diff
- Patch Commit: 77b3f2d
- Base Commit: 1f59a5f538dc38cbbb3798325ae8778f75621367

## Existing Unit Tests

- `firefox-ios/firefox-ios-tests/Tests/ClientTests/` — unit tests for client functionality
- `firefox-ios/firefox-ios-tests/Tests/XCUITests/` — UI tests
- `BrowserKit/Tests/` — tests for BrowserKit module (CommonTests, ComponentLibraryTests, WebEngineTests, etc.)
- `focus-ios/focus-ios-tests/` — Focus-specific tests
- ~692 Swift files importing XCTest across the repo

**Test class convention** — `validate-tests` categorizes by class name:
- Classes containing `F2P` (e.g. `AnvilTask1F2PTests`) — **fail-to-pass** (must fail on base)
- All other classes (repo tests, P2P classes, etc.) — **pass-to-pass** (must pass on base)

## Commands

```bash

# Step 1: (Run only once) Warm Xcode build cache (~5 min per unique base commit)
anvil warm-xcode-cache --dataset datasets/firefox-ios

# Step 2: Convert dataset (reads tasks/, writes to datasets/)
anvil convert-dataset --dataset tasks/firefox-ios

# Step 3: Validate task tests fail on unpatched base commits
anvil validate-tests --dataset datasets/firefox-ios

# Step 4: Verify gold patches compile (no Modal/Docker needed)
anvil run-evals --dataset datasets/firefox-ios --agent oracle --compile-only --no-continue

# Step 5: Publish Docker images (required for LLM agent runs — agents run in Modal)
anvil publish-images --dataset datasets/firefox-ios

# Step 6: Run against models (agent rollout via Modal, eval via local Xcode)
anvil run-evals --dataset datasets/firefox-ios --agent mini-swe-agent --model openrouter/anthropic/claude-opus-4.6 --n-attempts 4 --no-continue

anvil run-evals --dataset datasets/firefox-ios --agent mini-swe-agent --model openrouter/anthropic/claude-sonnet-4.5 --n-attempts 4 --no-continue

anvil run-evals --dataset datasets/firefox-ios --agent mini-swe-agent --model openrouter/openai/gpt-5.2 --n-attempts 4 --no-continue

anvil run-evals --dataset datasets/firefox-ios --agent mini-swe-agent --model openrouter/openai/gpt-5.2-codex --n-attempts 4 --no-continue

anvil run-evals --dataset datasets/firefox-ios --agent mini-swe-agent --model openrouter/google/gemini-3-pro-preview --n-attempts 4 --no-continue

anvil run-evals --dataset datasets/firefox-ios --agent mini-swe-agent --model openrouter/qwen/qwen3-coder-next --n-attempts 4 --no-continue

anvil run-evals --dataset datasets/firefox-ios --agent mini-swe-agent --model openrouter/deepseek/deepseek-v3.2 --n-attempts 4 --no-continue
```
