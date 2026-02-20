# Implementation Plan: Local Xcode Evaluation Pipeline

## Overview

Replace the Modal-based Linux Docker eval step with a local macOS evaluation pipeline that compiles Swift projects with `xcodebuild` and runs XCTests. The agent rollout phase (Modal + LLM APIs) stays unchanged.

### Current Pipeline

```
Agent Rollout (Modal Linux)  →  Eval (Modal Linux Docker)  →  Aggregation
         ↓                              ↓
  Generates patches            Python regex tests via pytest
```

### Target Pipeline

```
Agent Rollout (Modal Linux)  →  Eval (Local macOS)  →  Aggregation (unchanged)
         ↓                           ↓
  Generates patches           xcodebuild build + test
                              (with cached incremental builds)
```

Only the eval phase changes. Rollout, patch format, result aggregation, and pass@k computation remain identical.

---

## Architecture

### New Component: `src/anvil/evals/xcode_eval.py`

A new eval backend that sits alongside `swe_bench_pro_eval.py`. The runner (`runner.py`) calls it instead of (or in addition to) the Modal-based eval when `--eval-backend xcode-local` is passed.

```
runner.py
├── Phase 1: Agent Rollout (unchanged, Modal)
├── Phase 2: Patch Evaluation
│   ├── --eval-backend modal    → swe_bench_pro_eval.py (existing)
│   └── --eval-backend xcode    → xcode_eval.py (new)
└── Phase 3: Aggregation (unchanged)
```

### New Component: `src/anvil/evals/xcode_cache.py`

Manages pre-built DerivedData caches per base commit. This is the key optimization — turns 3-5 minute clean builds into 10-30 second incremental builds.

### New Dataset Artifact: Xcode Build Metadata

Each dataset gains an `xcode_config.yaml`:

```yaml
# datasets/ACHNBrowserUI/tasks/xcode_config.yaml
project: ACHNBrowserUI/ACHNBrowserUI.xcodeproj
scheme: ACHNBrowserUI
destination: "platform=iOS Simulator,name=iPhone 16,OS=latest"
test_target: ACHNBrowserUITests  # optional, for tasks with XCTests
```

---

## Implementation Steps

### Step 1: Xcode Build Cache System (`xcode_cache.py`)

**What it does:** Pre-builds each base commit once, saves the DerivedData directory as a reusable cache. Subsequent eval runs copy the cache and do incremental builds (only recompiling files touched by the agent's patch).

**Why it matters:** This is the single biggest optimization. A clean Xcode build takes 2-5 minutes. An incremental build after a 3-10 file patch takes 10-30 seconds. For 32 evals, this is the difference between 55 minutes and 4 minutes.

**How it works:**

```
~/.anvil/xcode-cache/
├── ACHNBrowserUI/
│   ├── 31b3185f/          # base commit hash
│   │   ├── repo/          # clean checkout at this commit
│   │   └── DerivedData/   # pre-built DerivedData
│   ├── 3eba9512/
│   │   ├── repo/
│   │   └── DerivedData/
│   └── ...
```

**Interface:**

```python
class XcodeBuildCache:
    def __init__(self, cache_root: Path = Path.home() / ".anvil" / "xcode-cache"):
        ...

    def warm(self, repo_path: Path, base_commit: str, xcode_config: dict) -> Path:
        """Pre-build a base commit. Returns path to cached DerivedData.

        1. If cache exists and is valid, return immediately.
        2. Clone/checkout repo at base_commit into cache dir.
        3. Run full xcodebuild build.
        4. Save DerivedData.
        """

    def checkout(self, repo_name: str, base_commit: str, target_dir: Path) -> Path:
        """Create an isolated working copy with cached DerivedData.

        1. git worktree add target_dir from cached repo at base_commit.
        2. cp -r cached DerivedData to target_dir's DerivedData.
        3. Return target_dir.
        """

    def cleanup(self, target_dir: Path):
        """Remove a worktree created by checkout()."""
```

**CLI command:**

```bash
# Pre-warm caches for a dataset (run once, or after adding tasks)
anvil warm-xcode-cache --dataset datasets/ACHNBrowserUI
```

This iterates over `instances.yaml`, clones the repo if needed, checks out each unique `base_commit`, and runs a full `xcodebuild build`. Takes ~5-15 min per unique base commit (one-time cost).

### Step 2: Local Xcode Eval Runner (`xcode_eval.py`)

**What it does:** For each (instance_id, attempt) pair, applies the agent's patch to an isolated worktree, runs `xcodebuild build` (and optionally `xcodebuild test`), parses results, and writes the same output format as the Modal eval.

**How it works (per eval):**

```
1. cache.checkout(repo, base_commit, /tmp/eval-{iid}-{attempt})
   → Isolated worktree with pre-built DerivedData

2. git apply /path/to/agent_patch.diff
   → Patch applied to worktree

3. xcodebuild build (incremental, 10-30s)
   → Compilation check: does the patched code compile?

4. [If task has XCTests] xcodebuild test
   → Run unit tests

5. [If task has pytest structural tests] python -m pytest tests.py
   → Run existing regex tests (backward compat)

6. Parse results → output.json (same format as today)

7. cache.cleanup(worktree)
```

**Key: Steps 4 and 5 can coexist.** A task can have both XCTests (for logic) and Python regex tests (for structural checks like "did you delete the old files"). The eval runner merges results from both.

**Interface:**

```python
def eval_with_xcode(
    patch: str,
    sample: dict,           # from tasks.csv row
    output_dir: str,
    xcode_config: dict,     # from xcode_config.yaml
    cache: XcodeBuildCache,
    prefix: str = "",
    attempt: int | None = None,
    compile_only: bool = False,
) -> dict | None:
    """Evaluate a single patch using local xcodebuild.

    Returns: {"tests": [{"name": ..., "status": "PASSED"|"FAILED"}, ...]}
    """
```

**Parallelism:**

```python
# In xcode_eval.py main()
with ProcessPoolExecutor(max_workers=max_workers) as pool:
    futures = {
        pool.submit(eval_with_xcode, patch, sample, ...): patch_sample
        for patch_sample in valid_patches
    }
    for future in as_completed(futures):
        ...
```

`max_workers` defaults to `min(os.cpu_count() // 4, 3)` — each xcodebuild process uses ~4 cores for incremental builds, so on an 8-core Mac you run 2 concurrent, on a 12-core Mac you run 3.

### Step 3: xcodebuild Output Parser (`xcode_parser.py`)

**What it does:** Parses `xcodebuild` output and/or `.xcresult` bundles into the standardized `{"tests": [{"name": ..., "status": ...}]}` format that the aggregation phase expects.

**Why a separate parser:** `xcodebuild test` output is verbose and format varies across Xcode versions. The parser handles:

```
# xcodebuild test stdout patterns:
Test Case '-[ACHNBrowserUITests.TurnipsGridTests testUsesGridLayout]' passed (0.003 seconds).
Test Case '-[ACHNBrowserUITests.TurnipsGridTests testOldRowsRemoved]' failed (0.001 seconds).

# Or xcresult bundle (more reliable):
xcrun xcresulttool get --format json --path results.xcresult
```

**For compilation-only checks** (no test target), the parser produces a synthetic test result:

```json
{
  "tests": [
    {"name": "compilation", "status": "PASSED"}
  ]
}
```

If compilation fails, it extracts the first error:

```json
{
  "tests": [
    {"name": "compilation", "status": "FAILED",
     "message": "TurnipsView.swift:42: error: cannot find 'GridStack' in scope"}
  ]
}
```

### Step 4: CLI Integration

**Changes to `runner.py`:**

Add an `--eval-backend` flag:

```python
eval_backend: Literal["modal", "xcode"] = typer.Option(
    "modal", "--eval-backend",
    help="Evaluation backend: 'modal' (Linux Docker via Modal) or 'xcode' (local macOS xcodebuild)"
)
```

When `eval_backend == "xcode"`:
- Skip the `swe_bench_pro_eval.py` subprocess call
- Instead, import and call `xcode_eval.run_xcode_evals()`
- Result format is identical, so the aggregation phase is unchanged

**New CLI commands:**

```bash
# Pre-warm xcode build caches
anvil warm-xcode-cache --dataset datasets/ACHNBrowserUI

# Run evals with xcode backend
anvil run-evals --dataset datasets/ACHNBrowserUI \
    --agent mini-swe-agent \
    --model openrouter/anthropic/claude-sonnet-4.5 \
    --eval-backend xcode \
    --n-attempts 4

# Compile-only mode (no tests, just verify compilation)
anvil run-evals --dataset datasets/ACHNBrowserUI \
    --eval-backend xcode \
    --compile-only
```

### Step 5: XCTest Authoring (Per Task)

Convert testable logic from Python regex tests to real XCTests. Not all tests should be converted — structural checks stay as Python.

**What converts well → XCTest:**
- Data model behavior (UserCollection.completionStatus, toggleVariant)
- ViewModel state (LikeButtonViewModel.variantsCompletionStatus)
- Computed properties (Item.hasSomeVariations)
- Business logic (color computation, price calculations)

**What stays as Python regex:**
- File existence/deletion checks ("old row files removed")
- Naming convention checks ("uses GridStack keyword")
- Code structure checks ("eraseToAnyViewForRow removed")
- Reference removal checks ("no longer imports X")

**Per-task setup:**

Each task that wants XCTests needs a test file added to the Xcode project. This gets baked into the Docker image at the base commit via a `before_test_cmd` in `xcode_config.yaml`:

```yaml
# datasets/ACHNBrowserUI/tasks/xcode_config.yaml
tasks:
  ACHNBrowserUI.task-3:
    xctest_file: tasks/ACHNBrowserUI/task-3/xctest/VariantCollectionTests.swift
    test_class: VariantCollectionTests
```

The eval runner copies the test file into the worktree before building:

```bash
cp xctest/VariantCollectionTests.swift \
   ACHNBrowserUI/ACHNBrowserUITests/VariantCollectionTests.swift
```

**Example XCTest for task-3:**

```swift
import XCTest
@testable import Backend

class VariantCollectionTests: XCTestCase {

    func testCompletionStatusNone() {
        let collection = UserCollection()
        let item = static_item  // has 3 variants
        let status = collection.variants.completionStatus(for: item)
        XCTAssertEqual(status, .unstarted)
    }

    func testCompletionStatusPartial() {
        let collection = UserCollection()
        let item = static_item
        let variant = item.variations!.first!
        _ = collection.toggleVariant(item: item, variant: variant)
        let status = collection.variants.completionStatus(for: item)
        XCTAssertEqual(status, .partial)
    }

    func testCompletionStatusComplete() {
        let collection = UserCollection()
        let item = static_item
        for variant in item.variations! {
            _ = collection.toggleVariant(item: item, variant: variant)
        }
        let status = collection.variants.completionStatus(for: item)
        XCTAssertEqual(status, .complete)
    }

    func testParentAutoAddedOnFirstVariant() {
        let collection = UserCollection()
        let item = static_item
        let variant = item.variations!.first!
        XCTAssertFalse(collection.items.contains(item))
        _ = collection.toggleVariant(item: item, variant: variant)
        XCTAssertTrue(collection.items.contains(item))
    }

    func testParentAutoRemovedOnLastVariant() {
        let collection = UserCollection()
        let item = static_item
        let variant = item.variations!.first!
        _ = collection.toggleVariant(item: item, variant: variant)
        _ = collection.toggleVariant(item: item, variant: variant)  // un-toggle
        XCTAssertFalse(collection.items.contains(item))
    }
}
```

These test actual behavior, not naming conventions. An agent that implements the feature correctly passes regardless of what it names its variables.

### Step 6: Hybrid Test Merging

**What it does:** Combines results from XCTests and Python regex tests into a single `output.json`.

For a task with both test types, the eval produces:

```json
{
  "tests": [
    {"name": "compilation", "status": "PASSED"},
    {"name": "testCompletionStatusPartial", "status": "PASSED"},
    {"name": "testParentAutoAddedOnFirstVariant", "status": "PASSED"},
    {"name": "test_old_row_views_removed", "status": "PASSED"},
    {"name": "test_erase_to_any_view_for_row_removed", "status": "FAILED"}
  ]
}
```

The `tasks.csv` `fail_to_pass` field lists all test names (both XCTest and pytest) that must pass. The existing aggregation logic handles this unchanged since it just checks `(f2p | p2p) <= passed_tests`.

---

## Optimizations Explained

### Optimization 1: DerivedData Caching (10-15x speedup)

**The problem:** A clean `xcodebuild build` compiles every Swift file from scratch. For a project with 100+ Swift files, this takes 2-5 minutes even on a fast Mac.

**The fix:** Build once per base commit, save the DerivedData directory (contains compiled `.o` files, module maps, framework caches). For each eval, copy the cached DerivedData and run `xcodebuild build` again — Xcode's incremental build system sees that only the patched files changed and recompiles just those (typically 3-10 files). This takes 10-30 seconds.

**Why it works:** Xcode's build system uses file modification timestamps and a dependency graph stored in DerivedData. When you copy DerivedData and then `git apply` a patch, only the touched files have newer timestamps. Xcode recompiles those files and their dependents, then re-links.

**One-time cost:** ~5 minutes per unique base commit (amortized across all evals forever).

### Optimization 2: git worktree Isolation (zero-copy checkouts)

**The problem:** Each eval needs an isolated repo checkout at a specific commit with a specific patch applied. Naively, this means N full `git clone` operations.

**The fix:** `git worktree add` creates a new working directory that shares the git object store with the main clone. Creating a worktree is instant (~100ms) and uses minimal disk space (just the working tree files, not the full .git history). Each eval gets its own worktree, applies its patch, builds independently, then the worktree is removed.

**Disk savings:** ~50MB per worktree vs ~200MB+ per full clone.

### Optimization 3: Parallel Builds with Core Affinity

**The problem:** Running N concurrent `xcodebuild` processes on the same machine means they all compete for the same CPU cores. With 8 cores and 4 concurrent builds, each build gets ~2 effective cores, slowing each one down.

**The fix:** Limit concurrency to `cpu_count // 4` (since incremental builds are fast and don't need all cores). On a typical Mac:

| Machine | Cores | Concurrent builds | Per-build time | 32 evals total |
|---|---|---|---|---|
| M1 MacBook | 8 | 2 | ~20s | ~5 min |
| M3 Pro | 12 | 3 | ~15s | ~3 min |
| M2 Ultra | 24 | 6 | ~12s | ~1.5 min |

### Optimization 4: Compile-Only Mode (skip linking + testing)

**The problem:** Even incremental builds spend time linking the final binary and (if testing) booting a simulator. For tasks where you only need compilation verification, this is wasted time.

**The fix:** Pass `--compile-only` to skip `xcodebuild test` and only check that `xcodebuild build` succeeds. Optionally use `ONLY_ACTIVE_ARCH=YES` and skip code signing to further reduce build time. This brings per-eval time down to ~5-15 seconds.

**When to use:** As an additional gate alongside Python regex tests. "Does the agent's patch compile?" catches a class of bugs that regex tests miss entirely (type errors, missing imports, protocol conformance violations).

### Optimization 5: Shared Simulator Pool

**The problem:** `xcodebuild test` boots an iOS Simulator for each test run. Booting a simulator takes 10-30 seconds, and each consumes ~1-2GB RAM.

**The fix:** Pre-boot a pool of simulators and reuse them across evals. Use `xcrun simctl` to create and manage simulator instances:

```bash
# Pre-boot N simulators before eval run
for i in $(seq 1 $MAX_WORKERS); do
    xcrun simctl create "anvil-eval-$i" "iPhone 16"
    xcrun simctl boot "anvil-eval-$i"
done

# Each eval targets a specific pre-booted simulator
xcodebuild test -destination "platform=iOS Simulator,id=$SIM_UDID" ...
```

Saves 10-30 seconds per eval that requires test execution. Not needed for compile-only mode.

---

## Migration Strategy

### Phase 1: Compile Gate (1-2 days)

Add compilation checking alongside existing Python regex tests. No test conversion needed.

- Implement `XcodeBuildCache` (warm + checkout)
- Implement `eval_with_xcode()` in compile-only mode
- Wire into `runner.py` via `--eval-backend xcode --compile-only`
- Add `xcode_config.yaml` for both datasets
- Add `anvil warm-xcode-cache` CLI command

**Result:** Every eval now verifies the patch compiles. Regex tests still handle pass/fail logic. Patches that don't compile auto-fail.

### Phase 2: Hybrid Tests (3-5 days)

Add XCTests for tasks with testable business logic, keeping Python regex tests for structural checks.

- Write XCTests for task-3 (variant collection — best candidate, lots of testable logic)
- Write XCTests for task-1 and task-4 if their logic is testable
- Implement hybrid result merging
- Update `tasks.csv` `fail_to_pass` to include XCTest names
- Implement `xcode_parser.py` for xcresult/stdout parsing

**Result:** Tasks with XCTests are evaluated by actual behavior, not naming conventions. False negatives from brittle regex drop significantly.

### Phase 3: Full Test Suite (ongoing, per task)

As new tasks are added, write XCTests for testable logic from the start. Structural checks remain as Python regex where appropriate.

---

## File Changes Summary

```
New files:
  src/anvil/evals/xcode_eval.py      # Local xcodebuild eval runner
  src/anvil/evals/xcode_cache.py     # DerivedData cache manager
  src/anvil/evals/xcode_parser.py    # xcodebuild output parser

Modified files:
  src/anvil/evals/runner.py           # Add --eval-backend flag, xcode path
  src/anvil/cli.py                    # Add warm-xcode-cache command
  src/anvil/run_evals.py              # Pass eval_backend option through

New per-dataset:
  datasets/*/tasks/xcode_config.yaml  # Xcode project/scheme/destination

New per-task (optional):
  tasks/*/task-N/xctest/*.swift       # XCTest files for testable logic
```

## Estimated Timeline

| Phase | Effort | Scope |
|---|---|---|
| Phase 1: Compile gate | 1-2 days | xcode_cache.py, xcode_eval.py (compile-only), CLI |
| Phase 2: Hybrid tests | 3-5 days | xcode_parser.py, XCTest authoring, result merging |
| Phase 3: Per-task tests | ~0.5 days/task | Ongoing as tasks are added |
| **Total for Phase 1+2** | **~1 week** | |
