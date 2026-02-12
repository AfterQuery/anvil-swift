#!/usr/bin/env python3
"""
Swift Repository Scraper for iOS-Bench

Scrapes GitHub for Swift repositories suitable for SWE-bench Pro style benchmarks.
Filters for:
- Active maintenance
- Good test coverage
- PRs linked to issues
- SPM support (preferred)
"""

import subprocess
import json
import time
import argparse
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Optional


@dataclass
class RepoCandidate:
    """A candidate Swift repository for iOS-Bench."""
    full_name: str
    description: str
    stars: int
    forks: int
    open_issues: int
    language: str
    updated_at: str
    has_tests: bool
    test_framework: Optional[str]
    has_spm: bool
    has_xcodeproj: bool
    pr_count: int
    prs_with_issues: int
    license: Optional[str]
    url: str

    @property
    def score(self) -> float:
        """Calculate a suitability score for benchmarking."""
        score = 0.0

        # Stars (log scale, max 30 points)
        if self.stars > 0:
            import math
            score += min(30, math.log10(self.stars) * 10)

        # Has tests (25 points)
        if self.has_tests:
            score += 25

        # SPM support (15 points) - easier to containerize
        if self.has_spm:
            score += 15

        # PRs linked to issues (up to 20 points)
        if self.pr_count > 0:
            ratio = self.prs_with_issues / self.pr_count
            score += ratio * 20

        # Recent activity (10 points if updated in last 6 months)
        from datetime import datetime, timezone
        try:
            updated = datetime.fromisoformat(self.updated_at.replace('Z', '+00:00'))
            now = datetime.now(timezone.utc)
            days_old = (now - updated).days
            if days_old < 180:
                score += 10
            elif days_old < 365:
                score += 5
        except:
            pass

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
                timeout=60
            )

            if result.returncode == 0:
                return json.loads(result.stdout) if result.stdout.strip() else None

            # Rate limit handling
            if "rate limit" in result.stderr.lower():
                wait_time = 60 * (attempt + 1)
                print(f"Rate limited. Waiting {wait_time}s...")
                time.sleep(wait_time)
                continue

            # 404 is expected for missing files - silent return
            if "Not Found" in result.stderr:
                return None

            # Other unexpected error - only print on last attempt
            if attempt == max_retries - 1:
                print(f"    API Error: {result.stderr[:100]}")
                return None

        except subprocess.TimeoutExpired:
            print(f"Timeout on attempt {attempt + 1}")
            continue
        except json.JSONDecodeError:
            return None

    return None


def search_swift_repos(
    min_stars: int = 100,
    min_size_kb: int = 500,
    max_results: int = 500,
    sort: str = "stars",
    apps_only: bool = False,
    topic: str = None,
) -> list[dict]:
    """Search for Swift repositories matching criteria."""
    repos = []

    mode = "iOS apps" if apps_only else "Swift repos"
    print(f"Searching for {mode} (min {min_stars} stars)...")

    # For apps/topics, use gh search repos command (better topic support)
    if apps_only or topic:
        topics_to_search = [topic] if topic else ["ios-app", "macos-app", "swiftui-app"]

        for t in topics_to_search:
            if len(repos) >= max_results:
                break

            cmd = [
                "gh", "search", "repos",
                "--language=Swift",
                f"--topic={t}",
                f"--stars=>{min_stars}",
                f"--limit={min(100, max_results - len(repos))}",
                "--json", "fullName,description,stargazersCount,forksCount,updatedAt,license,url"
            ]

            try:
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
                if result.returncode == 0 and result.stdout.strip():
                    items = json.loads(result.stdout)
                    for item in items:
                        # Convert to standard format
                        item["full_name"] = item.pop("fullName", "")
                        item["stargazers_count"] = item.pop("stargazersCount", 0)
                        item["forks_count"] = item.pop("forksCount", 0)
                        item["updated_at"] = item.pop("updatedAt", "")
                        item["html_url"] = item.pop("url", "")
                        item["language"] = "Swift"
                        item["open_issues_count"] = 0

                        # Dedupe
                        if not any(r.get("full_name") == item["full_name"] for r in repos):
                            repos.append(item)

                    print(f"  Found {len(items)} repos with topic '{t}'")
            except Exception as e:
                print(f"  Error searching topic {t}: {e}")

            time.sleep(1)

        return repos[:max_results]

    # Standard search for libraries
    per_page = 100
    page = 1

    while len(repos) < max_results:
        query = f"language:Swift stars:>={min_stars} size:>={min_size_kb} archived:false NOT awesome in:name NOT awesome in:description"

        result = run_gh([
            f"/search/repositories",
            "-X", "GET",
            "-f", f"q={query}",
            "-f", f"sort={sort}",
            "-f", "order=desc",
            "-f", f"per_page={per_page}",
            "-f", f"page={page}"
        ])

        if not result or "items" not in result:
            break

        items = result["items"]
        if not items:
            break

        repos.extend(items)
        print(f"  Found {len(repos)} repos so far...")

        if len(items) < per_page:
            break

        page += 1
        time.sleep(1)  # Rate limit courtesy

    return repos[:max_results]


def check_has_tests(repo_full_name: str) -> tuple[bool, Optional[str]]:
    """Check if repo has test files and identify test framework."""

    # Check for Tests directory via tree (avoids code search API rate limits)
    tree = run_gh([f"/repos/{repo_full_name}/git/trees/HEAD?recursive=1"])
    if not tree or "tree" not in tree:
        return False, None

    for item in tree["tree"]:
        path = item.get("path", "")
        path_lower = path.lower()

        # Skip non-directories for directory checks
        is_dir = item.get("type") == "tree"

        # Check for test directories (at any level)
        if is_dir:
            dir_name = path_lower.split("/")[-1]
            if dir_name in ["tests", "test", "specs", "unittests", "uitests"]:
                if "spec" in dir_name:
                    return True, "Quick/Nimble"
                return True, "XCTest"
            # iOS app pattern: *Tests, *-tests
            if dir_name.endswith("tests") or dir_name.endswith("-tests"):
                return True, "XCTest"

        # Check for test files
        if path_lower.endswith("tests.swift") or path_lower.endswith("test.swift"):
            return True, "XCTest"
        if path_lower.endswith("spec.swift") or path_lower.endswith("specs.swift"):
            return True, "Quick/Nimble"

    # Check for Package.swift with test targets
    pkg = run_gh([f"/repos/{repo_full_name}/contents/Package.swift"])
    if pkg and "content" in pkg:
        import base64
        try:
            content = base64.b64decode(pkg["content"]).decode("utf-8").lower()
            if ".testtarget" in content or "testtarget(" in content:
                return True, "XCTest/SPM"
        except:
            pass

    return False, None


def check_has_spm(repo_full_name: str) -> bool:
    """Check if repo has Package.swift (SPM support)."""
    result = run_gh([f"/repos/{repo_full_name}/contents/Package.swift"])
    return result is not None and "name" in result


def check_has_xcodeproj(repo_full_name: str) -> bool:
    """Check if repo has .xcodeproj or .xcworkspace."""
    tree = run_gh([f"/repos/{repo_full_name}/git/trees/HEAD"])
    if tree and "tree" in tree:
        for item in tree["tree"]:
            path = item.get("path", "")
            if path.endswith(".xcodeproj") or path.endswith(".xcworkspace"):
                return True
    return False


def get_pr_stats(repo_full_name: str, limit: int = 100) -> tuple[int, int]:
    """Get PR count and count of PRs linked to issues."""
    # Get recent merged PRs
    result = run_gh([
        f"/repos/{repo_full_name}/pulls",
        "-X", "GET",
        "-f", "state=closed",
        "-f", f"per_page={limit}",
        "-f", "sort=updated",
        "-f", "direction=desc"
    ])

    if not result:
        return 0, 0

    total = 0
    with_issues = 0

    for pr in result:
        if not pr.get("merged_at"):
            continue
        total += 1

        # Check if PR body references an issue
        body = pr.get("body") or ""
        title = pr.get("title") or ""

        # Common patterns for issue linking
        issue_patterns = [
            "fixes #", "closes #", "resolves #",
            "fix #", "close #", "resolve #",
            "fixed #", "closed #", "resolved #",
            "issue #", "issues #",
            "refs #", "ref #",
        ]

        text = (body + " " + title).lower()
        if any(pattern in text for pattern in issue_patterns):
            with_issues += 1

    return total, with_issues


def analyze_repo(repo: dict) -> Optional[RepoCandidate]:
    """Analyze a single repository for benchmark suitability."""
    full_name = repo["full_name"]

    # Skip obvious non-code repos
    name_lower = full_name.lower()
    if any(skip in name_lower for skip in ["awesome", "interview", "guide", "tutorial", "cheatsheet", "learning"]):
        print(f"  Skipping {full_name} (likely not a code repo)")
        return None

    print(f"  Analyzing {full_name}...")

    # Check for tests
    has_tests, test_framework = check_has_tests(full_name)
    time.sleep(1)  # Rate limit - be conservative

    # Check for SPM
    has_spm = check_has_spm(full_name)
    time.sleep(0.5)

    # Check for Xcode project
    has_xcodeproj = check_has_xcodeproj(full_name)
    time.sleep(0.5)

    # Get PR stats
    pr_count, prs_with_issues = get_pr_stats(full_name)
    time.sleep(1)  # Rate limit - be conservative

    return RepoCandidate(
        full_name=full_name,
        description=repo.get("description") or "",
        stars=repo.get("stargazers_count", 0),
        forks=repo.get("forks_count", 0),
        open_issues=repo.get("open_issues_count", 0),
        language=repo.get("language") or "Swift",
        updated_at=repo.get("updated_at") or "",
        has_tests=has_tests,
        test_framework=test_framework,
        has_spm=has_spm,
        has_xcodeproj=has_xcodeproj,
        pr_count=pr_count,
        prs_with_issues=prs_with_issues,
        license=repo.get("license", {}).get("spdx_id") if repo.get("license") else None,
        url=repo.get("html_url") or f"https://github.com/{full_name}"
    )


def main():
    parser = argparse.ArgumentParser(
        description="Scrape GitHub for Swift repos suitable for iOS-Bench"
    )
    parser.add_argument(
        "--min-stars", type=int, default=100,
        help="Minimum star count (default: 100)"
    )
    parser.add_argument(
        "--max-repos", type=int, default=100,
        help="Maximum repos to analyze (default: 100)"
    )
    parser.add_argument(
        "--output", type=str, default="swift_repos.json",
        help="Output JSON file (default: swift_repos.json)"
    )
    parser.add_argument(
        "--require-tests", action="store_true",
        help="Only include repos with tests"
    )
    parser.add_argument(
        "--require-spm", action="store_true",
        help="Only include repos with Package.swift"
    )
    parser.add_argument(
        "--min-prs-with-issues", type=int, default=0,
        help="Minimum PRs linked to issues (default: 0)"
    )
    parser.add_argument(
        "--apps-only", action="store_true",
        help="Only search for iOS/macOS apps (not libraries)"
    )
    parser.add_argument(
        "--topic", type=str, default=None,
        help="Filter by GitHub topic (e.g., 'ios-app', 'swiftui')"
    )

    args = parser.parse_args()

    # Search for repos
    repos = search_swift_repos(
        min_stars=args.min_stars,
        max_results=args.max_repos * 2,  # Get extra in case some are filtered
        apps_only=args.apps_only,
        topic=args.topic,
    )

    print(f"\nFound {len(repos)} Swift repos. Analyzing...")

    # Analyze each repo
    candidates = []
    for i, repo in enumerate(repos):
        if len(candidates) >= args.max_repos:
            break

        print(f"[{i+1}/{len(repos)}]", end="")
        candidate = analyze_repo(repo)

        if not candidate:
            continue

        # Apply filters
        if args.require_tests and not candidate.has_tests:
            print(f"    Skipping {candidate.full_name}: no tests")
            continue

        if args.require_spm and not candidate.has_spm:
            print(f"    Skipping {candidate.full_name}: no SPM")
            continue

        if candidate.prs_with_issues < args.min_prs_with_issues:
            print(f"    Skipping {candidate.full_name}: insufficient PR-issue links")
            continue

        candidates.append(candidate)
        print(f"    Added {candidate.full_name} (score: {candidate.score})")

    # Sort by score
    candidates.sort(key=lambda x: x.score, reverse=True)

    # Output results
    output_path = Path(args.output)
    output_data = {
        "metadata": {
            "total_found": len(candidates),
            "filters": {
                "min_stars": args.min_stars,
                "require_tests": args.require_tests,
                "require_spm": args.require_spm,
                "min_prs_with_issues": args.min_prs_with_issues,
            }
        },
        "repositories": [asdict(c) for c in candidates]
    }

    with open(output_path, "w") as f:
        json.dump(output_data, f, indent=2)

    print(f"\n{'='*60}")
    print(f"Results saved to {output_path}")
    print(f"Total candidates: {len(candidates)}")
    print(f"\nTop 10 by score:")
    print("-" * 60)

    for c in candidates[:10]:
        tests = f"✓ {c.test_framework}" if c.has_tests else "✗"
        spm = "✓ SPM" if c.has_spm else ""
        prs = f"{c.prs_with_issues}/{c.pr_count} PRs"
        print(f"  {c.full_name}")
        print(f"    ★ {c.stars:,} | {tests} | {spm} | {prs} | Score: {c.score}")
        print()


if __name__ == "__main__":
    main()
