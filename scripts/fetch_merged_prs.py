#!/usr/bin/env python3
"""
Fetch merged PRs for a specific repo filtered by change size.

Pulls merged PRs and filters by:
- Min/max total line changes (additions + deletions)
- Min/max number of files changed
"""

import subprocess
import json
import time
import argparse
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Optional
from datetime import datetime, timezone


@dataclass
class MergedPR:
    repo: str
    number: int
    title: str
    url: str
    author: str
    merged_at: str
    base_sha: str
    merge_sha: str
    files_changed: int
    additions: int
    deletions: int
    total_changes: int
    changed_files: list[str]
    body: str
    labels: list[str]


def run_gh(args: list[str], max_retries: int = 3) -> dict | list | None:
    cmd = ["gh", "api"] + args

    for attempt in range(max_retries):
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=120
            )

            if result.returncode == 0:
                return json.loads(result.stdout) if result.stdout.strip() else None

            if "rate limit" in result.stderr.lower():
                wait_time = 60 * (attempt + 1)
                print(f"  Rate limited. Waiting {wait_time}s...")
                time.sleep(wait_time)
                continue

            if "Not Found" in result.stderr:
                print(f"  Not found: {' '.join(args)[:120]}")
                return None

            if attempt == max_retries - 1:
                print(f"  API error: {result.stderr[:200]}")
                return None

        except subprocess.TimeoutExpired:
            print(f"  Timeout on attempt {attempt + 1}")
            continue
        except json.JSONDecodeError:
            return None

    return None


def get_pr_files(repo: str, pr_number: int) -> list[dict]:
    files = []
    page = 1

    while True:
        result = run_gh([f"/repos/{repo}/pulls/{pr_number}/files?per_page=100&page={page}"])
        if not result:
            break
        files.extend(result)
        if len(result) < 100:
            break
        page += 1

    return files


def validate_repo(repo: str) -> bool:
    """Check the repo exists and print a clear error if not."""
    if "/" not in repo:
        print(f"Error: repo must be in owner/repo format (got: '{repo}')")
        print(f"  e.g. python3 scripts/fetch_merged_prs.py merlos/iOS-Open-GPX-Tracker")
        return False
    result = run_gh([f"/repos/{repo}"])
    if result is None:
        print(f"Error: repo '{repo}' not found on GitHub. Check the owner/repo spelling.")
        return False
    return True


def fetch_merged_prs(
    repo: str,
    since: Optional[str] = None,
    until: Optional[str] = None,
    scan_limit: int = 20,
    max_prs: int = 200,
    min_changes: Optional[int] = None,
    max_changes: Optional[int] = None,
    min_files: Optional[int] = None,
    max_files: Optional[int] = None,
) -> list[MergedPR]:
    """Fetch and filter merged PRs from a repo by change size."""
    print(f"Fetching merged PRs from {repo}...")

    results = []
    page = 1
    fetched = 0
    stop_early = False

    while not stop_early:
        endpoint = (
            f"/repos/{repo}/pulls"
            f"?state=closed&sort=updated&direction=desc&per_page=100&page={page}"
        )
        batch = run_gh([endpoint])

        if not batch:
            break

        for pr in batch:
            if not pr.get("merged_at"):
                continue

            merged_at = pr["merged_at"]

            # Date range filtering
            if since and merged_at < since:
                # PRs are sorted by updated desc; once we go past `since` we can stop
                stop_early = True
                break
            if until and merged_at > until:
                continue

            fetched += 1
            if fetched > scan_limit:
                stop_early = True
                break

            pr_number = pr["number"]

            # Fetch per-file stats (required for additions/deletions)
            files = get_pr_files(repo, pr_number)
            additions = sum(f.get("additions", 0) for f in files)
            deletions = sum(f.get("deletions", 0) for f in files)
            total_changes = additions + deletions
            files_changed = len(files)

            # Apply filters
            if min_changes is not None and total_changes < min_changes:
                continue
            if max_changes is not None and total_changes > max_changes:
                continue
            if min_files is not None and files_changed < min_files:
                continue
            if max_files is not None and files_changed > max_files:
                continue

            results.append(MergedPR(
                repo=repo,
                number=pr_number,
                title=pr.get("title", ""),
                url=pr.get("html_url", ""),
                author=pr.get("user", {}).get("login", ""),
                merged_at=merged_at,
                base_sha=pr.get("base", {}).get("sha", ""),
                merge_sha=pr.get("merge_commit_sha", ""),
                files_changed=files_changed,
                additions=additions,
                deletions=deletions,
                total_changes=total_changes,
                changed_files=[f.get("filename", "") for f in files],
                body=pr.get("body") or "",
                labels=[l.get("name", "") for l in pr.get("labels", [])],
            ))
            print(f"  #{pr_number} +{additions}/-{deletions} ({files_changed} files) {pr.get('title', '')[:60]}")

            if len(results) >= max_prs:
                stop_early = True
                break

            time.sleep(0.3)

        if len(batch) < 100:
            break

        page += 1
        time.sleep(0.5)

    return results


def main():
    parser = argparse.ArgumentParser(
        description="Fetch merged PRs for a repo filtered by change size"
    )
    parser.add_argument(
        "repo",
        help="Repository in owner/repo format (e.g. Alamofire/Alamofire)"
    )
    parser.add_argument(
        "--min-changes", type=int, default=None,
        help="Minimum total line changes (additions + deletions)"
    )
    parser.add_argument(
        "--max-changes", type=int, default=None,
        help="Maximum total line changes (additions + deletions)"
    )
    parser.add_argument(
        "--min-files", type=int, default=None,
        help="Minimum number of files changed"
    )
    parser.add_argument(
        "--max-files", type=int, default=None,
        help="Maximum number of files changed"
    )
    parser.add_argument(
        "--since", type=str, default=None,
        help="Only PRs merged on or after this date (YYYY-MM-DD)"
    )
    parser.add_argument(
        "--until", type=str, default=None,
        help="Only PRs merged on or before this date (YYYY-MM-DD)"
    )
    parser.add_argument(
        "--scan-limit", type=int, default=20,
        help="Maximum number of merged PRs to pull from the API before filtering (default: 20)"
    )
    parser.add_argument(
        "--max-prs", type=int, default=200,
        help="Maximum number of matching PRs to return (default: 200)"
    )
    parser.add_argument(
        "--output", type=str, default=None,
        help="Output JSON file (default: <repo_name>_merged_prs.json)"
    )

    args = parser.parse_args()

    if not validate_repo(args.repo):
        raise SystemExit(1)

    prs = fetch_merged_prs(
        repo=args.repo,
        since=args.since,
        until=args.until,
        scan_limit=args.scan_limit,
        max_prs=args.max_prs,
        min_changes=args.min_changes,
        max_changes=args.max_changes,
        min_files=args.min_files,
        max_files=args.max_files,
    )

    # Output
    repo_name = args.repo.split("/")[-1]
    output_path = Path(args.output or f"tasks/{repo_name}/merged_prs.json")
    output_path.parent.mkdir(parents=True, exist_ok=True)

    output_data = {
        "metadata": {
            "repo": args.repo,
            "scraped_at": datetime.now(timezone.utc).isoformat(),
            "total_found": len(prs),
            "filters": {
                "scan_limit": args.scan_limit,
                "min_changes": args.min_changes,
                "max_changes": args.max_changes,
                "min_files": args.min_files,
                "max_files": args.max_files,
                "since": args.since,
                "until": args.until,
            },
        },
        "pull_requests": [asdict(p) for p in prs],
    }

    with open(output_path, "w") as f:
        json.dump(output_data, f, indent=2)

    print(f"\n{'='*60}")
    print(f"Done. Found {len(prs)} matching PRs.")
    print(f"Output: {output_path}")

    if prs:
        total_lines = [p.total_changes for p in prs]
        print(f"Change range: {min(total_lines)}–{max(total_lines)} lines")
        print(f"\nSample (first 5):")
        for p in prs[:5]:
            print(f"  #{p.number}  +{p.additions}/-{p.deletions} ({p.files_changed} files)  {p.title[:55]}")


if __name__ == "__main__":
    main()
