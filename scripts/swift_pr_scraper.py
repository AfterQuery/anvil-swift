#!/usr/bin/env python3
"""
Swift PR Scraper for iOS-Bench Task Extraction

Scrapes merged PRs from Swift repositories that:
- Are linked to issues (have problem statements)
- Modify test files (have verifiable solutions)
- Can be reversed to create fail-to-pass tasks

This follows the SWE-bench / SWE-gen methodology.
"""

import subprocess
import json
import time
import argparse
import re
from dataclasses import dataclass, asdict, field
from pathlib import Path
from typing import Optional
from datetime import datetime, timezone


@dataclass
class PRCandidate:
    """A candidate PR for iOS-Bench task extraction."""
    repo: str
    pr_number: int
    title: str
    body: str
    url: str
    merged_at: str
    base_sha: str
    merge_sha: str

    # Issue linkage
    linked_issues: list[int] = field(default_factory=list)
    issue_titles: list[str] = field(default_factory=list)
    issue_bodies: list[str] = field(default_factory=list)

    # File changes
    files_changed: int = 0
    additions: int = 0
    deletions: int = 0
    changed_files: list[str] = field(default_factory=list)

    # Test info
    test_files_modified: list[str] = field(default_factory=list)
    has_test_changes: bool = False

    # Metadata
    author: str = ""
    labels: list[str] = field(default_factory=list)

    @property
    def problem_statement(self) -> str:
        """Construct problem statement from issue(s) or PR body."""
        if self.issue_bodies:
            return "\n\n---\n\n".join(self.issue_bodies)
        return self.body or self.title

    @property
    def is_valid_task(self) -> bool:
        """Check if this PR can be converted to a valid task."""
        return (
            bool(self.linked_issues) and  # Has issue linkage
            self.has_test_changes and      # Has test modifications
            self.files_changed > 0 and     # Actually changes code
            bool(self.base_sha)            # Has base commit
        )

    @property
    def task_quality_score(self) -> float:
        """Score the quality of this PR as a benchmark task."""
        score = 0.0

        # Problem statement quality (30 points)
        if self.linked_issues:
            score += 20
            if any(len(b) > 100 for b in self.issue_bodies):
                score += 10  # Good issue description
        elif len(self.body or "") > 100:
            # No linked issue, but good PR description
            score += 15
            if len(self.body or "") > 300:
                score += 5  # Really detailed PR body

        # Test changes (30 points)
        if self.has_test_changes:
            score += 20
            score += min(10, len(self.test_files_modified) * 3)

        # Reasonable size (20 points)
        total_changes = self.additions + self.deletions
        if 10 <= total_changes <= 500:
            score += 20
        elif total_changes < 10:
            score += 5  # Too small
        elif total_changes <= 1000:
            score += 10  # Getting large

        # Multi-file but not too many (20 points)
        if 2 <= self.files_changed <= 10:
            score += 20
        elif self.files_changed == 1:
            score += 10
        elif self.files_changed <= 20:
            score += 5

        return round(score, 2)


def run_gh(args: list[str], max_retries: int = 3) -> dict | list | None:
    """Run a GitHub CLI command and return JSON output."""
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
                print(f"    Rate limited. Waiting {wait_time}s...")
                time.sleep(wait_time)
                continue

            if "Not Found" in result.stderr:
                return None

            if attempt == max_retries - 1:
                print(f"    Error: {result.stderr[:200]}")
                return None

        except subprocess.TimeoutExpired:
            print(f"    Timeout on attempt {attempt + 1}")
            continue
        except json.JSONDecodeError:
            return None

    return None


def extract_issue_numbers(text: str) -> list[int]:
    """Extract issue numbers from PR title/body."""
    if not text:
        return []

    patterns = [
        r'(?:fix|fixes|fixed|close|closes|closed|resolve|resolves|resolved)\s*#(\d+)',
        r'(?:issue|issues|ref|refs)\s*#(\d+)',
        r'#(\d+)',
    ]

    issues = set()
    text_lower = text.lower()

    for pattern in patterns:
        matches = re.findall(pattern, text_lower)
        issues.update(int(m) for m in matches)

    return sorted(issues)


def get_issue_details(repo: str, issue_number: int) -> tuple[str, str]:
    """Get issue title and body."""
    result = run_gh([f"/repos/{repo}/issues/{issue_number}"])
    if result:
        return result.get("title", ""), result.get("body", "")
    return "", ""


def get_pr_files(repo: str, pr_number: int) -> list[dict]:
    """Get list of files changed in PR."""
    files = []
    page = 1

    while True:
        result = run_gh([
            f"/repos/{repo}/pulls/{pr_number}/files?per_page=100&page={page}"
        ])

        if not result:
            break

        files.extend(result)

        if len(result) < 100:
            break
        page += 1

    return files


def is_test_file(filename: str) -> bool:
    """Check if a file is a test file."""
    name_lower = filename.lower()

    # Swift test patterns
    patterns = [
        "test", "tests", "spec", "specs",
        "xctest", "xctestcase",
        "mock", "stub", "fake",
    ]

    # Check path components
    parts = name_lower.replace("\\", "/").split("/")
    for part in parts:
        if any(p in part for p in patterns):
            return True

    # Check filename
    basename = parts[-1] if parts else ""
    if basename.endswith("test.swift") or basename.endswith("tests.swift"):
        return True
    if basename.endswith("spec.swift") or basename.endswith("specs.swift"):
        return True
    if basename.startswith("test") and basename.endswith(".swift"):
        return True

    return False


def get_merged_prs(
    repo: str,
    since: Optional[str] = None,
    max_prs: int = 100
) -> list[dict]:
    """Get merged PRs from a repository."""
    prs = []
    page = 1

    while len(prs) < max_prs:
        # Use query string params (not -f flags which make it a POST)
        endpoint = f"/repos/{repo}/pulls?state=closed&sort=updated&direction=desc&per_page=100&page={page}"
        params = [endpoint
        ]

        result = run_gh(params)

        if not result:
            break

        for pr in result:
            if pr.get("merged_at"):
                # Filter by date if specified
                if since:
                    merged = pr["merged_at"]
                    if merged < since:
                        continue
                prs.append(pr)

        if len(result) < 100:
            break

        page += 1
        time.sleep(0.5)

    return prs[:max_prs]


def analyze_pr(repo: str, pr: dict) -> Optional[PRCandidate]:
    """Analyze a PR for task extraction suitability."""
    pr_number = pr["number"]

    # Extract basic info
    candidate = PRCandidate(
        repo=repo,
        pr_number=pr_number,
        title=pr.get("title", ""),
        body=pr.get("body") or "",
        url=pr.get("html_url", ""),
        merged_at=pr.get("merged_at", ""),
        base_sha=pr.get("base", {}).get("sha", ""),
        merge_sha=pr.get("merge_commit_sha", ""),
        author=pr.get("user", {}).get("login", ""),
        labels=[l.get("name", "") for l in pr.get("labels", [])]
    )

    # Extract linked issues
    all_text = f"{candidate.title} {candidate.body}"
    candidate.linked_issues = extract_issue_numbers(all_text)

    # Get issue details
    for issue_num in candidate.linked_issues[:3]:  # Limit to 3 issues
        title, body = get_issue_details(repo, issue_num)
        if title:
            candidate.issue_titles.append(title)
        if body:
            candidate.issue_bodies.append(body)
        time.sleep(0.3)

    # Get changed files
    files = get_pr_files(repo, pr_number)
    candidate.files_changed = len(files)

    for f in files:
        filename = f.get("filename", "")
        candidate.changed_files.append(filename)
        candidate.additions += f.get("additions", 0)
        candidate.deletions += f.get("deletions", 0)

        if is_test_file(filename):
            candidate.test_files_modified.append(filename)

    candidate.has_test_changes = len(candidate.test_files_modified) > 0

    return candidate


def scrape_repo_prs(
    repo: str,
    max_prs: int = 100,
    since: Optional[str] = None,
    require_tests: bool = True,
    require_issues: bool = True,
) -> list[PRCandidate]:
    """Scrape PRs from a single repository."""
    print(f"\nScraping {repo}...")

    # Get merged PRs
    prs = get_merged_prs(repo, since=since, max_prs=max_prs * 2)
    print(f"  Found {len(prs)} merged PRs")

    candidates = []

    for i, pr in enumerate(prs):
        if len(candidates) >= max_prs:
            break

        print(f"  [{i+1}/{len(prs)}] PR #{pr['number']}: {pr['title'][:50]}...")

        candidate = analyze_pr(repo, pr)
        if not candidate:
            continue

        # Apply filters
        if require_issues and not candidate.linked_issues:
            print(f"    Skipping: no linked issues")
            continue

        if require_tests and not candidate.has_test_changes:
            print(f"    Skipping: no test changes")
            continue

        candidates.append(candidate)
        print(f"    ✓ Valid task (score: {candidate.task_quality_score})")

        time.sleep(0.5)  # Rate limiting

    return candidates


def main():
    parser = argparse.ArgumentParser(
        description="Scrape Swift PRs for iOS-Bench task extraction"
    )
    parser.add_argument(
        "repos", nargs="*",
        help="Repositories to scrape (owner/repo format)"
    )
    parser.add_argument(
        "--repos-file", type=str,
        help="JSON file with repository list (from swift_repo_scraper.py)"
    )
    parser.add_argument(
        "--max-prs", type=int, default=50,
        help="Max PRs to analyze per repo (default: 50)"
    )
    parser.add_argument(
        "--since", type=str,
        help="Only PRs merged after this date (YYYY-MM-DD)"
    )
    parser.add_argument(
        "--output", type=str, default="swift_pr_candidates.json",
        help="Output JSON file"
    )
    parser.add_argument(
        "--no-require-tests", action="store_true",
        help="Include PRs without test changes"
    )
    parser.add_argument(
        "--no-require-issues", action="store_true",
        help="Include PRs without linked issues (use PR body as problem statement)"
    )
    parser.add_argument(
        "--min-score", type=float, default=0,
        help="Minimum task quality score"
    )

    args = parser.parse_args()

    # Get repo list
    repos = list(args.repos) if args.repos else []

    if args.repos_file:
        with open(args.repos_file) as f:
            data = json.load(f)
            for r in data.get("repositories", []):
                repos.append(r["full_name"])

    if not repos:
        # Default repos for testing
        repos = [
            "Alamofire/Alamofire",
            "vapor/vapor",
            "onevcat/Kingfisher",
            "SnapKit/SnapKit",
            "apple/swift-collections",
        ]
        print("No repos specified. Using defaults:", repos)

    # Scrape each repo
    all_candidates = []

    for repo in repos:
        candidates = scrape_repo_prs(
            repo,
            max_prs=args.max_prs,
            since=args.since,
            require_tests=not args.no_require_tests,
            require_issues=not args.no_require_issues,
        )

        # Filter by score
        candidates = [c for c in candidates if c.task_quality_score >= args.min_score]

        all_candidates.extend(candidates)
        print(f"  → {len(candidates)} valid candidates from {repo}")

    # Sort by score
    all_candidates.sort(key=lambda x: x.task_quality_score, reverse=True)

    # Save results
    output_path = Path(args.output)
    output_data = {
        "metadata": {
            "scraped_at": datetime.now(timezone.utc).isoformat(),
            "repos_scraped": repos,
            "total_candidates": len(all_candidates),
            "filters": {
                "require_tests": not args.no_require_tests,
                "require_issues": not args.no_require_issues,
                "min_score": args.min_score,
                "since": args.since,
            }
        },
        "candidates": [asdict(c) for c in all_candidates]
    }

    with open(output_path, "w") as f:
        json.dump(output_data, f, indent=2)

    # Summary
    print(f"\n{'='*60}")
    print(f"SCRAPING COMPLETE")
    print(f"{'='*60}")
    print(f"Total candidates: {len(all_candidates)}")
    print(f"Output: {output_path}")

    if all_candidates:
        valid = [c for c in all_candidates if c.is_valid_task]
        print(f"Valid tasks: {len(valid)}")
        print(f"\nTop 10 candidates:")
        print("-" * 60)

        for c in all_candidates[:10]:
            issues = f"#{', #'.join(map(str, c.linked_issues))}" if c.linked_issues else "none"
            tests = f"{len(c.test_files_modified)} test files" if c.has_test_changes else "no tests"
            print(f"  {c.repo} PR #{c.pr_number}")
            print(f"    {c.title[:60]}")
            print(f"    Issues: {issues} | {tests} | {c.files_changed} files")
            print(f"    Score: {c.task_quality_score}")
            print()


if __name__ == "__main__":
    main()
