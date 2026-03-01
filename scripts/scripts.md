# Scripts

## swift_repo_scraper.py

Scrapes GitHub for Swift repositories suitable for SWE-bench style benchmarks. Scores and filters repos by stars, test coverage, SPM support, and PR-issue linkage.

```bash
cd scripts

# Basic search (default: ≥100 stars, up to 100 repos)
python3 scripts/swift_repo_scraper.py

# Higher bar: more stars, tests required, SPM required
python3 scripts/swift_repo_scraper.py --min-stars 500 --require-tests --require-spm

# iOS apps only (searches by topic)
python3 scripts/swift_repo_scraper.py --apps-only --max-repos 50

# Filter by specific topic
python3 scripts/swift_repo_scraper.py --topic swiftui --min-stars 200

# Only repos with at least 5 PRs linked to issues
python3 scripts/swift_repo_scraper.py --min-prs-with-issues 5

# Custom output file
python3 scripts/swift_repo_scraper.py --output my_repos.json
```

**Output:** JSON file with scored repository candidates (`swift_repos.json` by default).

---

## swift_pr_scraper.py

Scrapes merged PRs from Swift repositories for benchmark task extraction. Finds PRs linked to issues that also modify test files (fail-to-pass tasks).

```bash
# Scrape specific repos
python3 scripts/swift_pr_scraper.py Alamofire/Alamofire vapor/vapor

# Load repo list from swift_repo_scraper.py output
python3 scripts/swift_pr_scraper.py --repos-file swift_repos.json

# Include PRs without linked issues (use PR body as problem statement)
python3 scripts/swift_pr_scraper.py Alamofire/Alamofire --no-require-issues

# Include PRs without test changes
python3 scripts/swift_pr_scraper.py Alamofire/Alamofire --no-require-tests

# Only PRs merged after a date, minimum quality score
python3 scripts/swift_pr_scraper.py Alamofire/Alamofire --since 2023-01-01 --min-score 40

# Limit PRs analyzed per repo, custom output
python3 scripts/swift_pr_scraper.py Alamofire/Alamofire --max-prs 25 --output my_prs.json
```

**Output:** JSON file with scored PR candidates (`swift_pr_candidates.json` by default).

---

## fetch_merged_prs.py

Fetches merged PRs for a single repo filtered by change size (total lines changed and/or number of files touched).

```bash
# PRs with 50–500 total line changes
python3 scripts/fetch_merged_prs.py merlos/iOS-Open-GPX-Tracker --min-changes 200 --max-changes 700

# PRs touching 2–10 files
python3 scripts/fetch_merged_prs.py merlos/iOS-Open-GPX-Tracker --min-files 2 --max-files 10

# Combine line and file filters with a date range
python3 scripts/fetch_merged_prs.py vapor/vapor \
  --min-changes 10 --max-changes 300 --max-files 15 --since 2023-01-01

# Cap results and write to a custom file
python3 scripts/fetch_merged_prs.py onevcat/Kingfisher \
  --min-changes 20 --max-prs 50 --output kingfisher_prs.json
```

**Flags:**

| Flag                              | Description                                             |
| --------------------------------- | ------------------------------------------------------- |
| `--min-changes` / `--max-changes` | Total line changes (additions + deletions)              |
| `--min-files` / `--max-files`     | Number of files touched                                 |
| `--since` / `--until`             | Merge date range (`YYYY-MM-DD`)                         |
| `--max-prs`                       | Cap on matching results (default: 200)                  |
| `--output`                        | Output path (default: `<owner>_<repo>_merged_prs.json`) |

**Output:** JSON file with matching merged PRs and their change stats.
