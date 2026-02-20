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

## Existing Unit Tests

- `Packages/Backend/Tests/BackendTests/ItemsTests.swift` — JSON decoding for ItemResponse
- `Packages/Backend/Tests/BackendTests/CrittersTests.swift` — critter/fish decoding, active months, categories
- `Packages/Backend/Tests/BackendTests/CollectionTest.swift` — UserCollection toggle functionality
- `Packages/UI/Tests/UITests/UITests.swift` — placeholder

Test targets configured in Package.swift: `BackendTests`, `UITests`

## Commands

```bash
# Compile-only check (fastest — just verifies agent patches compile)
anvil run-evals --dataset datasets/ACHNBrowserUI --agent oracle --eval-backend xcode --compile-only

# Run against models
anvil run-evals --dataset datasets/ACHNBrowserUI --agent mini-swe-agent --model openrouter/anthropic/claude-sonnet-4.5 --eval-backend xcode --n-attempts 4
anvil run-evals --dataset datasets/ACHNBrowserUI --agent mini-swe-agent --model openrouter/openai/gpt-5.2-codex --eval-backend xcode --n-attempts 4
anvil run-evals --dataset datasets/ACHNBrowserUI --agent mini-swe-agent --model openrouter/google/gemini-3-pro-preview --eval-backend xcode --n-attempts 4
anvil run-evals --dataset datasets/ACHNBrowserUI --agent mini-swe-agent --model openrouter/deepseek/deepseek-v3.2 --eval-backend xcode --n-attempts 4
```
