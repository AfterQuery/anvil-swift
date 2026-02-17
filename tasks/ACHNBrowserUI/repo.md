Animal Crossing Helper: https://github.com/Dimillian/ACHNBrowserUI

## Tasks

1. Catch Now: https://github.com/Dimillian/ACHNBrowserUI/pull/263

- Type: Feature
- Patch: curl -L https://github.com/Dimillian/ACHNBrowserUI/pull/263.diff -o solution.diff
- Patch Commit: 154e105
- Base Commit: 3eba9512b0fb430d2507e27df3f8311d3bd67706

2. Adjust Grid View: https://github.com/Dimillian/ACHNBrowserUI/pull/191

- Type: Fix
- Patch: curl -L https://github.com/Dimillian/ACHNBrowserUI/pull/191.diff -o solution.diff
- Patch Commit: c05456f
- Base Commit: 31b3185f7435e9f1c208ad7c0c726a54652ca791

3. Add Partial Like: https://github.com/Dimillian/ACHNBrowserUI/pull/338

- Type: Feature
- Patch: curl -L https://github.com/Dimillian/ACHNBrowserUI/pull/338.diff -o solution.diff
- Patch Commit: c452f40
- Base Commit: 3d11674846dd9ad905de616782134b0a76a4e148

4. Add Sorting Villagers: https://github.com/Dimillian/ACHNBrowserUI/pull/190

- Type: Feature
- Patch: curl -L https://github.com/Dimillian/ACHNBrowserUI/pull/190.diff -o solution.diff
- Patch Commit: 0bfd982
- Base Commit: 89ac53bfe6d0769411f4005060e8974fa8fd35d4

## Commands

```bash
# 1. Clone repo
git clone https://github.com/Dimillian/ACHNBrowserUI.git repos/ACHNBrowserUI

# 2. Initialize dataset
source .venv/bin/activate

anvil init-dataset -d datasets/ACHNBrowserUI --repo-path repos/ACHNBrowserUI --base-image swift:5.9

# 3. Add all tasks
anvil add-task -d datasets/ACHNBrowserUI -n 1 --base-commit 3eba9512b0fb430d2507e27df3f8311d3bd67706
anvil add-task -d datasets/ACHNBrowserUI -n 2 --base-commit 31b3185f7435e9f1c208ad7c0c726a54652ca791
anvil add-task -d datasets/ACHNBrowserUI -n 3 --base-commit 3d11674846dd9ad905de616782134b0a76a4e148
anvil add-task -d datasets/ACHNBrowserUI -n 4 --base-commit 89ac53bfe6d0769411f4005060e8974fa8fd35d4

# 4. Convert to Anvil evaluation format
anvil convert-dataset -d datasets/ACHNBrowserUI -u marvindeng

# 5. Publish images
anvil publish-images --dataset datasets/ACHNBrowserUI -u marvindeng --repo anvil-images

# Remove cached builds
docker builder prune -f

# 6. Verify base (all fail_to_pass tests should fail)
anvil verify-base -d datasets/ACHNBrowserUI -u marvindeng --dockerhub-repo anvil-images

# 7. Run oracle (all tests should pass with gold patch)
anvil run-evals --dataset datasets/ACHNBrowserUI --agent oracle --dockerhub-username marvindeng --dockerhub-repo anvil-images --no-continue

# 8. Run against models

# Claude Sonnet 4.5
anvil run-evals --dataset datasets/ACHNBrowserUI --agent mini-swe-agent --dockerhub-username marvindeng --dockerhub-repo anvil-images --model openrouter/anthropic/claude-sonnet-4.5 --no-continue --n-attempts 4

# Claude Opus 4.6
anvil run-evals --dataset datasets/ACHNBrowserUI --agent mini-swe-agent --dockerhub-username marvindeng --dockerhub-repo anvil-images --model openrouter/anthropic/claude-opus-4.6 --no-continue --n-attempts 4

# GPT 5.2
anvil run-evals --dataset datasets/ACHNBrowserUI --agent mini-swe-agent --dockerhub-username marvindeng --dockerhub-repo anvil-images --model openrouter/openai/gpt-5.2 --no-continue --n-attempts 4

# GPT 5.2 Codex
anvil run-evals --dataset datasets/ACHNBrowserUI --agent mini-swe-agent --dockerhub-username marvindeng --dockerhub-repo anvil-images --model openrouter/openai/gpt-5.2-codex --no-continue --n-attempts 4

# Gemini 3 Pro
anvil run-evals --dataset datasets/ACHNBrowserUI --agent mini-swe-agent --dockerhub-username marvindeng --dockerhub-repo anvil-images --model openrouter/google/gemini-3-pro-preview --no-continue --n-attempts 4

# Llama 4 Maverick
anvil run-evals --dataset datasets/ACHNBrowserUI --agent mini-swe-agent --dockerhub-username marvindeng --dockerhub-repo anvil-images --model openrouter/meta-llama/llama-4-maverick --no-continue --n-attempts 4

# Qwen 3 Coder Next
anvil run-evals --dataset datasets/ACHNBrowserUI --agent mini-swe-agent --dockerhub-username marvindeng --dockerhub-repo anvil-images --model openrouter/qwen/qwen3-coder-next --no-continue --n-attempts 4

# Deepseek V3.2
anvil run-evals --dataset datasets/ACHNBrowserUI --agent mini-swe-agent --dockerhub-username marvindeng --dockerhub-repo anvil-images --model openrouter/deepseek/deepseek-v3.2 --no-continue --n-attempts 4
```
