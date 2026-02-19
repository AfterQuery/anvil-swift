#!/usr/bin/env python3
"""
Compute comprehensive metrics for iOS-Open-GPX-Tracker eval runs.
"""

import json
import os
from collections import defaultdict

BASE_DIR = "/Users/marvindeng/VS_Code_Projects/anvil/datasets/iOS-Open-GPX-Tracker/runs"
TASKS = ["iOS-Open-GPX-Tracker.task-1",
         "iOS-Open-GPX-Tracker.task-2",
         "iOS-Open-GPX-Tracker.task-3",
         "iOS-Open-GPX-Tracker.task-4"]
TASK_SHORT = ["task-1", "task-2", "task-3", "task-4"]
N_ATTEMPTS = 4
SKIP_COST_MODELS = {"oracle"}

# ── helpers ──────────────────────────────────────────────────────────────────

def load_json(path):
    if not os.path.exists(path):
        return None
    with open(path) as f:
        return json.load(f)

def count_assistant_steps(messages):
    return sum(1 for m in messages if m.get("role") == "assistant")

# ── data collection ──────────────────────────────────────────────────────────

# Structure:
#   data[model][task_id][attempt_n] = {
#       "passed": bool,
#       "diff_bytes": int,
#       "cost": float|None,
#       "steps": int|None,
#   }

data = {}

models = sorted(os.listdir(BASE_DIR))

for model in models:
    model_path = os.path.join(BASE_DIR, model)
    if not os.path.isdir(model_path):
        continue
    data[model] = {}
    skip_cost = (model in SKIP_COST_MODELS)

    for task_id in TASKS:
        task_path = os.path.join(model_path, task_id)
        if not os.path.isdir(task_path):
            continue
        data[model][task_id] = {}

        for n in range(1, N_ATTEMPTS + 1):
            attempt_dir = os.path.join(task_path, f"attempt_{n}")
            if not os.path.isdir(attempt_dir):
                continue

            # ── eval result ──
            er_path = os.path.join(attempt_dir, "eval_results", "eval_results.json")
            er = load_json(er_path)
            if er is None:
                passed = None
            else:
                # value may be bool or 0/1
                val = er.get(task_id)
                passed = bool(val) if val is not None else None

            # ── model patch / diff size ──
            pred_path = os.path.join(attempt_dir, "rollout", f"{task_id}.pred")
            pred = load_json(pred_path)
            if pred is not None:
                patch = pred.get("model_patch", "")
                diff_bytes = len(patch.encode("utf-8"))
            else:
                patch = None
                diff_bytes = None

            # ── trajectory: cost and steps ──
            traj_path = os.path.join(attempt_dir, "rollout", "trajectory.json")
            traj = load_json(traj_path)
            if traj is not None and not skip_cost:
                cost = traj.get("info", {}).get("model_stats", {}).get("instance_cost")
                steps = count_assistant_steps(traj.get("messages", []))
            else:
                cost = None
                steps = None

            data[model][task_id][n] = {
                "passed": passed,
                "diff_bytes": diff_bytes,
                "patch": patch,
                "cost": cost,
                "steps": steps,
            }

# ── metric computation ────────────────────────────────────────────────────────

def avg(lst):
    lst = [x for x in lst if x is not None]
    return sum(lst) / len(lst) if lst else None

def fmt_float(v, decimals=4):
    if v is None:
        return "N/A"
    return f"{v:.{decimals}f}"

def fmt_cost(v):
    if v is None:
        return "N/A"
    return f"${v:.4f}"

def fmt_bytes(v):
    if v is None:
        return "N/A"
    return f"{v:,.0f}"

# ── per-model, per-task table ─────────────────────────────────────────────────

print("=" * 100)
print("iOS-Open-GPX-Tracker  —  Eval Metrics")
print("=" * 100)

MODEL_COL = 34

for model in models:
    if model not in data:
        continue

    model_data = data[model]
    skip_cost = (model in SKIP_COST_MODELS)

    # collect per-task stats
    task_rows = []
    all_passed = []
    all_costs = []
    all_steps = []
    all_diff_bytes = []
    empty_diffs = 0
    tasks_with_pass = 0

    for task_id, short in zip(TASKS, TASK_SHORT):
        if task_id not in model_data:
            task_rows.append((short, None, None, None, None, None))
            continue

        attempts = model_data[task_id]

        passed_list = [a["passed"] for a in attempts.values() if a["passed"] is not None]
        task_pass1 = sum(passed_list) / len(passed_list) if passed_list else None
        task_pass4 = 1 if any(passed_list) else 0

        diff_sizes = [a["diff_bytes"] for a in attempts.values() if a["diff_bytes"] is not None]
        avg_diff = avg(diff_sizes)

        costs = [a["cost"] for a in attempts.values() if a["cost"] is not None]
        avg_cost = avg(costs)

        steps_list = [a["steps"] for a in attempts.values() if a["steps"] is not None]
        avg_steps_val = avg(steps_list)

        for a in attempts.values():
            if a["patch"] is not None and a["patch"] == "":
                empty_diffs += 1

        all_passed.extend(passed_list)
        all_costs.extend(costs)
        all_steps.extend(steps_list)
        all_diff_bytes.extend(diff_sizes)
        if any(passed_list):
            tasks_with_pass += 1

        task_rows.append((short, task_pass1, task_pass4, avg_diff, avg_cost, avg_steps_val))

    # model totals
    total_pass1 = sum(all_passed) / len(all_passed) if all_passed else None
    total_pass4 = tasks_with_pass  # out of 4
    total_cost = sum(all_costs) if all_costs else None
    global_avg_cost = avg(all_costs)
    global_avg_steps = avg(all_steps)

    # ── print model header ──
    print()
    print(f"  Model: {model}")
    print(f"  {'─' * 96}")

    # per-task header
    header = f"  {'Task':<10} {'pass@1':>8} {'pass@4':>8} {'avg diff (B)':>14} {'avg cost':>12} {'avg steps':>11}"
    print(header)
    print(f"  {'─' * 96}")

    for short, p1, p4, diff, cost, steps in task_rows:
        p1_s  = f"{p1:.2f}" if p1 is not None else "N/A"
        p4_s  = str(p4)     if p4 is not None else "N/A"
        d_s   = fmt_bytes(diff)
        c_s   = fmt_cost(cost) if not skip_cost else "N/A"
        st_s  = f"{steps:.1f}" if steps is not None else "N/A"
        print(f"  {short:<10} {p1_s:>8} {p4_s:>8} {d_s:>14} {c_s:>12} {st_s:>11}")

    print(f"  {'─' * 96}")

    # totals line
    p1_s  = f"{total_pass1:.4f}" if total_pass1 is not None else "N/A"
    p4_s  = f"{total_pass4}/4"
    tc_s  = fmt_cost(total_cost) if not skip_cost else "N/A"
    ac_s  = fmt_cost(global_avg_cost) if not skip_cost else "N/A"
    as_s  = f"{global_avg_steps:.1f}" if global_avg_steps is not None else "N/A"
    ed_s  = str(empty_diffs) if not skip_cost else "N/A"

    print(f"  {'TOTAL':<10} {p1_s:>8} {p4_s:>8}   total_cost={tc_s}  avg_cost={ac_s}  avg_steps={as_s}  empty_diffs={ed_s}")

# ── summary table across all models ──────────────────────────────────────────

print()
print("=" * 100)
print("Summary Table — All Models")
print("=" * 100)

col_widths = {
    "model":        34,
    "pass@1":        8,
    "pass@4":        8,
    "total_cost":   12,
    "avg_cost":     12,
    "avg_steps":    11,
    "empty_diffs":  13,
}

header = (
    f"  {'Model':<{col_widths['model']}} "
    f"{'pass@1':>{col_widths['pass@1']}} "
    f"{'pass@4':>{col_widths['pass@4']}} "
    f"{'total_cost':>{col_widths['total_cost']}} "
    f"{'avg_cost':>{col_widths['avg_cost']}} "
    f"{'avg_steps':>{col_widths['avg_steps']}} "
    f"{'empty_diffs':>{col_widths['empty_diffs']}}"
)
print(header)
print("  " + "─" * 100)

for model in models:
    if model not in data:
        continue

    model_data = data[model]
    skip_cost = (model in SKIP_COST_MODELS)

    all_passed = []
    all_costs = []
    all_steps = []
    empty_diffs = 0
    tasks_with_pass = 0

    for task_id in TASKS:
        if task_id not in model_data:
            continue
        attempts = model_data[task_id]
        passed_list = [a["passed"] for a in attempts.values() if a["passed"] is not None]
        all_passed.extend(passed_list)
        if any(passed_list):
            tasks_with_pass += 1
        for a in attempts.values():
            cost = a["cost"]
            steps = a["steps"]
            if cost is not None:
                all_costs.append(cost)
            if steps is not None:
                all_steps.append(steps)
            if a["patch"] is not None and a["patch"] == "":
                empty_diffs += 1

    total_pass1   = sum(all_passed) / len(all_passed) if all_passed else None
    total_pass4   = tasks_with_pass
    total_cost    = sum(all_costs) if all_costs else None
    avg_cost_val  = avg(all_costs)
    avg_steps_val = avg(all_steps)

    p1_s  = f"{total_pass1:.4f}" if total_pass1 is not None else "N/A"
    p4_s  = f"{total_pass4}/4"
    tc_s  = fmt_cost(total_cost) if not skip_cost else "N/A"
    ac_s  = fmt_cost(avg_cost_val) if not skip_cost else "N/A"
    as_s  = f"{avg_steps_val:.1f}" if avg_steps_val is not None else "N/A"
    ed_s  = str(empty_diffs)

    print(
        f"  {model:<{col_widths['model']}} "
        f"{p1_s:>{col_widths['pass@1']}} "
        f"{p4_s:>{col_widths['pass@4']}} "
        f"{tc_s:>{col_widths['total_cost']}} "
        f"{ac_s:>{col_widths['avg_cost']}} "
        f"{as_s:>{col_widths['avg_steps']}} "
        f"{ed_s:>{col_widths['empty_diffs']}}"
    )

print()
print("Notes:")
print("  pass@1  = fraction of all individual attempts that passed  (total: 16 attempts per model)")
print("  pass@4  = number of tasks (out of 4) where at least 1 of 4 attempts passed")
print("  cost/steps: 'N/A' for oracle (no trajectory) and models with 0.0 reported cost (may be free-tier/local)")
print("  empty_diffs: attempts where model_patch == '' (no code change submitted)")
