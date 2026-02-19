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

## Commands

```bash
# 1. Clone repo
git clone https://github.com/mozilla-mobile/firefox-ios.git repos/firefox-ios

# 2. Initialize dataset
source .venv/bin/activate

anvil init-dataset -d datasets/firefox-ios --repo-path repos/firefox-ios --base-image swift:5.9

# 3. Add all tasks
anvil add-task -d datasets/firefox-ios -n 1 --base-commit b54d1c5b89b142bb7e6135fa090484c4385ef2d1
anvil add-task -d datasets/firefox-ios -n 2 --base-commit 34d4d846810c903d88007c1f1f5e2c4e8563e9bb
anvil add-task -d datasets/firefox-ios -n 3 --base-commit 9d4d3d5508a5c758c6c8c42f34b81e400b8a2a74
anvil add-task -d datasets/firefox-ios -n 4 --base-commit 30c75403d6b6680f3e4215f44351c7bb226484ec

# 4. Convert to Anvil evaluation format
anvil convert-dataset -d datasets/firefox-ios

# Remove cached builds
docker builder prune -f

# 5. Publish images
anvil publish-images --dataset datasets/firefox-ios

# 6. Verify base (all fail_to_pass tests should fail)
anvil verify-base -d datasets/firefox-ios

# 7. Run oracle (all tests should pass with gold patch)
anvil run-evals --dataset datasets/firefox-ios --agent oracle --no-continue

# 8. Run against models

# Claude Sonnet 4.5
anvil run-evals --dataset datasets/firefox-ios --agent mini-swe-agent --model openrouter/anthropic/claude-sonnet-4.5 --no-continue --n-attempts 4

# Claude Opus 4.6
anvil run-evals --dataset datasets/firefox-ios --agent mini-swe-agent --model openrouter/anthropic/claude-opus-4.6 --no-continue --n-attempts 4

# GPT 5.2
anvil run-evals --dataset datasets/firefox-ios --agent mini-swe-agent --model openrouter/openai/gpt-5.2 --no-continue --n-attempts 4

# GPT 5.2 Codex
anvil run-evals --dataset datasets/firefox-ios --agent mini-swe-agent --model openrouter/openai/gpt-5.2-codex --no-continue --n-attempts 4

# Gemini 3 Pro
anvil run-evals --dataset datasets/firefox-ios --agent mini-swe-agent --model openrouter/google/gemini-3-pro-preview --no-continue --n-attempts 4

# Llama 4 Maverick
anvil run-evals --dataset datasets/firefox-ios --agent mini-swe-agent --model openrouter/meta-llama/llama-4-maverick --no-continue --n-attempts 4

# Qwen 3 Coder Next
anvil run-evals --dataset datasets/firefox-ios --agent mini-swe-agent --model openrouter/qwen/qwen3-coder-next --no-continue --n-attempts 4

# Deepseek V3.2
anvil run-evals --dataset datasets/firefox-ios --agent mini-swe-agent --model openrouter/deepseek/deepseek-v3.2 --no-continue --n-attempts 4
```
