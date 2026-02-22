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

## Unit Tests

### Existing repo tests (BackendTests)

- `Packages/Backend/Tests/BackendTests/ItemsTests.swift` — JSON decoding for ItemResponse
- `Packages/Backend/Tests/BackendTests/CrittersTests.swift` — critter/fish decoding, active months, categories
- `Packages/Backend/Tests/BackendTests/CollectionTest.swift` — UserCollection toggle functionality

### Per-task evaluation tests

Task-specific unit tests live in `tasks/ACHNBrowserUI/task-N/tests.swift`. During
evaluation they are copied into the BackendTests SPM test target and run via
`xcodebuild test -scheme Backend`.

| Task | Tests | What they validate |
|------|-------|--------------------|
| task-1 | `AnvilTask1Tests.swift` | `isActiveThisMonth()`, `isActiveAtThisHour()`, `filterActiveThisMonth()`, `formattedTimes()` |
| task-2 | *(compile-only)* | App-layer changes (GridStack, TurnipsView) — no Backend code modified |
| task-3 | `AnvilTask3Tests.swift` | `hasSomeVariations`, `VariantsCompletionStatus`, `completionStatus(for:)`, variant toggle auto-manages parent |
| task-4 | *(compile-only)* | App-layer changes (VillagersSortView, VillagersViewModel) — no Backend code modified |

## Commands

```bash
source .venv/bin/activate

# Step 1: Convert dataset (reads tasks/, writes to datasets/)
anvil convert-dataset --dataset tasks/ACHNBrowserUI

# Step 2: (Run only once) Warm Xcode build cache (~5 min per unique base commit)
anvil warm-xcode-cache --dataset datasets/ACHNBrowserUI

# Step 3: Verify gold patches compile and pass unit tests
anvil run-evals --dataset datasets/ACHNBrowserUI --agent oracle --no-continue

# Step 4: Publish Docker images (required for LLM agent runs — agents run in Modal)
anvil publish-images --dataset datasets/ACHNBrowserUI

# Step 5: Run against models (agent rollout via Modal, eval via local Xcode)
anvil run-evals --dataset datasets/ACHNBrowserUI --agent mini-swe-agent --model openrouter/anthropic/claude-opus-4.6 --n-attempts 4 --no-continue

anvil run-evals --dataset datasets/ACHNBrowserUI --agent mini-swe-agent --model openrouter/anthropic/claude-sonnet-4.5 --n-attempts 4 --no-continue

anvil run-evals --dataset datasets/ACHNBrowserUI --agent mini-swe-agent --model openrouter/openai/gpt-5.2 --n-attempts 4 --no-continue

anvil run-evals --dataset datasets/ACHNBrowserUI --agent mini-swe-agent --model openrouter/openai/gpt-5.2-codex --n-attempts 4 --no-continue

anvil run-evals --dataset datasets/ACHNBrowserUI --agent mini-swe-agent --model openrouter/google/gemini-3-pro-preview --n-attempts 4 --no-continue

anvil run-evals --dataset datasets/ACHNBrowserUI --agent mini-swe-agent --model openrouter/qwen/qwen3-coder-next --n-attempts 4 --no-continue

anvil run-evals --dataset datasets/ACHNBrowserUI --agent mini-swe-agent --model openrouter/deepseek/deepseek-v3.2 --n-attempts 4 --no-continue
```
