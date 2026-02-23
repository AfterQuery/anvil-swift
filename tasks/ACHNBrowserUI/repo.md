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

5. Add Custom Chores and To-Dos: https://github.com/Dimillian/ACHNBrowserUI/pull/210

- Type: Feature
- Patch: curl -L https://github.com/Dimillian/ACHNBrowserUI/pull/210.diff -o solution.diff
- Patch Commit: fae875a
- Base Commit: 848a1589eb08f89f6badfde10d3b10ea592157a5

## Unit Tests

### Existing repo tests (BackendTests)

- `Packages/Backend/Tests/BackendTests/ItemsTests.swift` — JSON decoding for ItemResponse
- `Packages/Backend/Tests/BackendTests/CrittersTests.swift` — critter/fish decoding, active months, categories
- `Packages/Backend/Tests/BackendTests/CollectionTest.swift` — UserCollection toggle functionality

### Per-task evaluation tests

Task-specific unit tests live in `tasks/ACHNBrowserUI/task-N/tests.swift`. During
evaluation they are routed to the SPM backend or app test target based on their
`@testable import` (see `_detect_test_type` in `xcode_eval.py`).

**Test class convention** — `validate-tests` categorizes by class name:
- Classes containing `F2P` (e.g. `AnvilTask1F2PTests`) — **fail-to-pass** (must fail on base)
- All other classes (repo tests, P2P classes, etc.) — **pass-to-pass** (must pass on base)

**Design principle** — tests target *integration points* (ViewModel structs, view
components the rest of the app binds to) and *behavioral outcomes* rather than
internal API names. Compilation already enforces that the model's internal naming
is consistent across the codebase.

| Task | Tests | Route | What they validate |
|------|-------|-------|--------------------|
| task-1 | `AnvilTask1F2PTests` | app | Backend: `isActiveAtThisHour()` exists and returns false without data. App: `CritterInfo` struct has `toCatchNow`/`toCatchLater` |
| task-2 | `AnvilTask2F2PTests` | app | `GridStack` view existence, `rows`/`columns`/`spacing` properties |
| task-3 | `AnvilTask3F2PTests` | spm | `hasSomeVariations`, `VariantsCompletionStatus` enum, `completionStatus(for:)`. Behavioral: `toggleVariant` auto-manages parent item |
| task-4 | `AnvilTask4F2PTests` | app | `VillagersViewModel.Sort` enum with `.name`/`.species`, `sortedVillagers` empty with no data, clearing sort empties results |
| task-5 | `AnvilTask5F2PTests` | app | `Chore` model, `UserCollection` chore operations, `ChoreFormViewModel`, `ChoreListViewModel`, `TodayChoresSectionViewModel`, `TodaySection.chores` default |

## Commands

```bash
source .venv/bin/activate

# Step 1: Convert dataset (reads tasks/, writes to datasets/)
anvil convert-dataset --dataset tasks/ACHNBrowserUI

# Step 2: Warm Xcode build cache (~5 min per unique base commit)
anvil warm-xcode-cache --dataset datasets/ACHNBrowserUI

# Step 3: Validate task tests fail on unpatched base commits
anvil validate-tests --dataset datasets/ACHNBrowserUI

# Step 4: Verify gold patches compile and pass unit tests
anvil run-evals --dataset datasets/ACHNBrowserUI --agent oracle --no-continue

# Step 5: Publish Docker images (required for LLM agent runs — agents run in Modal)
anvil publish-images --dataset datasets/ACHNBrowserUI

# Step 6: Run against models (agent rollout via Modal, eval via local Xcode)
anvil run-evals --dataset datasets/ACHNBrowserUI --agent mini-swe-agent --model openrouter/anthropic/claude-opus-4.6 --n-attempts 4 --no-continue

anvil run-evals --dataset datasets/ACHNBrowserUI --agent mini-swe-agent --model openrouter/anthropic/claude-sonnet-4.5 --n-attempts 4 --no-continue

anvil run-evals --dataset datasets/ACHNBrowserUI --agent mini-swe-agent --model openrouter/openai/gpt-5.2 --n-attempts 4 --no-continue

anvil run-evals --dataset datasets/ACHNBrowserUI --agent mini-swe-agent --model openrouter/openai/gpt-5.2-codex --n-attempts 4 --no-continue

anvil run-evals --dataset datasets/ACHNBrowserUI --agent mini-swe-agent --model openrouter/google/gemini-3-pro-preview --n-attempts 4 --no-continue

anvil run-evals --dataset datasets/ACHNBrowserUI --agent mini-swe-agent --model openrouter/qwen/qwen3-coder-next --n-attempts 4 --no-continue

anvil run-evals --dataset datasets/ACHNBrowserUI --agent mini-swe-agent --model openrouter/deepseek/deepseek-v3.2 --n-attempts 4 --no-continue
```
