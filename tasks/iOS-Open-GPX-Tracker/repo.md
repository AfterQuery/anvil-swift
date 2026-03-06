Mobile GPS Logger: https://github.com/merlos/iOS-Open-GPX-Tracker

## Tasks

1. Fix Scale Bar Color: https://github.com/merlos/iOS-Open-GPX-Tracker/pull/296

- Patch: curl -L https://github.com/merlos/iOS-Open-GPX-Tracker/pull/296.diff -o solution.diff
- Patch Commit: 972b742
- Base Commit: 3d3ae151d854187f5e0090dc08faf4246473df7d

2. Add localization support: https://github.com/merlos/iOS-Open-GPX-Tracker/pull/118

- Patch: curl -L https://github.com/merlos/iOS-Open-GPX-Tracker/pull/118.diff -o solution.diff
- Patch Commit: ac0e67a
- Base Commit: 9ca33065e6a0d56f4a5db17ae20e9d143aa86e2f

3. Add Scale View on Map: https://github.com/merlos/iOS-Open-GPX-Tracker/pull/285

- Patch: curl -L https://github.com/merlos/iOS-Open-GPX-Tracker/pull/285.diff -o solution.diff
- Patch Commit: 93e20d4
- Base Commit: 72c1e361d4ab27c71e46d1384dcaa29dea667f3c

4. Fix Width Height IPad Orientation: https://github.com/merlos/iOS-Open-GPX-Tracker/pull/111

- Patch: curl -L https://github.com/merlos/iOS-Open-GPX-Tracker/pull/111.diff -o solution.diff
- Patch Commit: 1d3f1b7
- Base Commit: fa320f1cc5cfe1e58ac538c22e5165a08dc34b8a

5. Custom Default Names: https://github.com/merlos/iOS-Open-GPX-Tracker/pull/157

- Patch: curl -L https://github.com/merlos/iOS-Open-GPX-Tracker/pull/157.diff -o solution.diff
- Patch Commit: 887bef7
- Base Commit: 8e87edced43cb8292475510587b8dc82cb6e9e5c

6. Auto Reload Table When File Received: https://github.com/merlos/iOS-Open-GPX-Tracker/pull/99

- Patch: curl -L https://github.com/merlos/iOS-Open-GPX-Tracker/pull/99.diff -o solution.diff
- Patch Commit: 4dbc1aa
- Base Commit: df8dd1e25fbd28bd5496f3bc23d06922474396e3

7. Screen Always on and Loading Toast: https://github.com/merlos/iOS-Open-GPX-Tracker/pull/275

- Patch: curl -L https://github.com/merlos/iOS-Open-GPX-Tracker/pull/275.diff -o solution.diff
- Patch Commit: 971954b
- Base Commit: fbd582ed6af1ca637097ede12078c8ef2be88c60

8. Auto Recover Last Track: https://github.com/merlos/iOS-Open-GPX-Tracker/pull/249

- Patch: curl -L https://github.com/merlos/iOS-Open-GPX-Tracker/pull/249.diff -o solution.diff
- Patch Commit: 548e8ff
- Base Commit: b63c5109ee5a3a6c6e93703d26e5b5255b68205f

9. Trial Activity Type: https://github.com/merlos/iOS-Open-GPX-Tracker/pull/113

- Patch: curl -L https://github.com/merlos/iOS-Open-GPX-Tracker/pull/113.diff -o solution.diff
- Patch Commit: 6aa30ba
- Base Commit: 1d3f1b7199639ceaee5491d696f27dc7c22e44e8

10. Custom Output File: https://github.com/merlos/iOS-Open-GPX-Tracker/pull/239

- Patch: curl -L https://github.com/merlos/iOS-Open-GPX-Tracker/pull/239.diff -o solution.diff
- Patch Commit: 398ab75
- Base Commit: a9aa34ff04091f0111d978f5b206f682a8a92566

## Existing Unit Tests

- `OpenGpxTrackerTests/OpenGpxTrackerTests.swift` — placeholder tests only (testExample, testPerformanceExample)
- Test target `OpenGpxTrackerTests` is configured in the Xcode project but has no real test cases

> Note: The repo's own tests are placeholders. Evaluation uses per-task `tests.swift` files (see below).

**Test class convention** — `validate-tests` categorizes by class name:

- Classes containing `F2P` (e.g. `AnvilTask1F2PTests`) — **fail-to-pass** (must fail on base)
- All other classes (repo tests, P2P classes, etc.) — **pass-to-pass** (must pass on base)

## Scraping PRs

```bash
python3 scripts/fetch_merged_prs.py merlos/iOS-Open-GPX-Tracker --scan-limit 20

python3 scripts/fetch_merged_prs.py merlos/iOS-Open-GPX-Tracker --min-changes 200 --max-changes 700 --scan-limit 20
```

## Commands

```bash
source .venv/bin/activate

# Step 1: Convert dataset (reads tasks/, writes to datasets/)
anvil convert-dataset --dataset tasks/iOS-Open-GPX-Tracker

# Step 2: (Run only once) Warm Xcode build cache (~5 min per unique base commit)
anvil warm-xcode-cache --dataset datasets/iOS-Open-GPX-Tracker

# Step 3: Validate task tests fail on unpatched base commits
anvil validate-tests --dataset datasets/iOS-Open-GPX-Tracker

# Step 4: Verify gold patches compile and pass unit tests
anvil run-evals --dataset datasets/iOS-Open-GPX-Tracker --agent oracle --no-continue

# Step 5: Publish Docker images (required for LLM agent runs — agents run in Modal)
anvil publish-images --dataset datasets/iOS-Open-GPX-Tracker

# Step 6: Run against models (agent rollout via Modal, eval via local Xcode)
anvil run-evals --dataset datasets/iOS-Open-GPX-Tracker --agent mini-swe-agent --model openrouter/anthropic/claude-opus-4.6 --n-attempts 4 --no-continue

anvil run-evals --dataset datasets/iOS-Open-GPX-Tracker --agent mini-swe-agent --model openrouter/anthropic/claude-sonnet-4.5 --n-attempts 4 --no-continue

anvil run-evals --dataset datasets/iOS-Open-GPX-Tracker --agent mini-swe-agent --model openrouter/anthropic/claude-sonnet-4.6 --n-attempts 4 --no-continue

anvil run-evals --dataset datasets/iOS-Open-GPX-Tracker --agent mini-swe-agent --model openrouter/openai/gpt-5.4 --n-attempts 4 --no-continue

anvil run-evals --dataset datasets/iOS-Open-GPX-Tracker --agent mini-swe-agent --model openrouter/openai/gpt-5.2 --n-attempts 4 --no-continue

anvil run-evals --dataset datasets/iOS-Open-GPX-Tracker --agent mini-swe-agent --model openrouter/openai/gpt-5.2-codex --n-attempts 4 --no-continue

anvil run-evals --dataset datasets/iOS-Open-GPX-Tracker --agent mini-swe-agent --model openrouter/google/gemini-3.1-pro-preview --n-attempts 4 --no-continue

anvil run-evals --dataset datasets/iOS-Open-GPX-Tracker --agent mini-swe-agent --model openrouter/google/gemini-3-pro-preview --n-attempts 4 --no-continue

anvil run-evals --dataset datasets/iOS-Open-GPX-Tracker --agent mini-swe-agent --model openrouter/qwen/qwen3-coder-next --n-attempts 4 --no-continue

anvil run-evals --dataset datasets/iOS-Open-GPX-Tracker --agent mini-swe-agent --model openrouter/deepseek/deepseek-v3.2 --n-attempts 4 --no-continue
```
