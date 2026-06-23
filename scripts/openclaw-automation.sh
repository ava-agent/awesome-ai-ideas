#!/usr/bin/env bash
set -euo pipefail

REPO_DIR="/Users/wangshihao/projects/openclaws/awesome-ai-ideas"
PROJECTS_DIR="/Users/wangshihao/projects/openclaws"
EXPECTED_REMOTE="https://github.com/ava-agent/awesome-ai-ideas.git"
GIT_NAME="kevinten"
GIT_EMAIL="596823919@qq.com"

cd "$REPO_DIR"

ensure_repo() {
  local actual branch
  actual="$(git remote get-url origin)"
  branch="$(git branch --show-current)"
  if [[ "$actual" != "$EXPECTED_REMOTE" ]]; then
    echo "SKIP: unexpected remote $actual"
    exit 0
  fi
  if [[ "$branch" != "main" ]]; then
    echo "SKIP: branch is $branch, expected main"
    exit 0
  fi
}

ensure_identity() {
  git config user.name "$GIT_NAME"
  git config user.email "$GIT_EMAIL"
}

ensure_clean() {
  if [[ -n "$(git status --porcelain)" ]]; then
    echo "SKIP: working tree is dirty"
    git status --short
    exit 0
  fi
}

write_header() {
  local title="$1"
  {
    echo "# $title"
    echo
    echo "- Generated at: $(date '+%Y-%m-%d %H:%M:%S %z')"
    echo "- Commit identity: $(git config user.name) <$(git config user.email)>"
    echo "- Remote: $(git remote get-url origin)"
    echo
  }
}

commit_file() {
  local file="$1"
  local message="$2"
  git add -- "$file"
  if git diff --cached --quiet -- "$file"; then
    echo "No changes for $file"
    exit 0
  fi
  GIT_COMMITTER_NAME="$GIT_NAME" GIT_COMMITTER_EMAIL="$GIT_EMAIL" \
    git commit --author="$GIT_NAME <$GIT_EMAIL>" -m "$message"
}

slot() {
  date '+%Y-%m-%d-%H%M'
}

repo_pulse() {
  ensure_repo
  ensure_identity
  ensure_clean
  mkdir -p docs/automation
  local stamp file
  stamp="$(slot)"
  file="docs/automation/repo-pulse-$stamp.md"
  {
    write_header "Repository Activity Pulse $stamp"
    echo "## Git"
    echo
    echo "- Latest commit: $(git log -1 --oneline)"
    echo "- Tracked files: $(git ls-files | wc -l | tr -d ' ')"
    echo "- Docs files: $(find docs -type f | wc -l | tr -d ' ')"
    echo "- Idea files: $(find ideas -type f -name '*.md' 2>/dev/null | wc -l | tr -d ' ')"
    echo
    echo "## Recent Commits"
    echo
    git log --oneline -8 | sed 's/^/- /'
  } > "$file"
  commit_file "$file" "docs: repo activity pulse $stamp"
}

pr_snapshot() {
  ensure_repo
  ensure_identity
  ensure_clean
  mkdir -p docs/automation
  local stamp file
  stamp="$(slot)"
  file="docs/automation/pr-snapshot-$stamp.md"
  {
    write_header "GitHub PR Snapshot $stamp"
    echo "## Open Pull Requests"
    echo
    if command -v gh >/dev/null 2>&1; then
      gh pr list --repo ava-agent/awesome-ai-ideas --state open --limit 10 || true
      echo
      echo "## Recent Issues"
      echo
      gh issue list --repo ava-agent/awesome-ai-ideas --state open --limit 10 || true
    else
      echo "gh is not installed."
    fi
  } > "$file"
  commit_file "$file" "docs: GitHub PR snapshot $stamp"
}

pr_review_queue() {
  ensure_repo
  ensure_identity
  ensure_clean
  mkdir -p docs/automation
  local stamp file
  stamp="$(slot)"
  file="docs/automation/pr-review-queue-$stamp.md"
  {
    write_header "PR Review Queue $stamp"
    echo "## Open PR Review Queue"
    echo
    if command -v gh >/dev/null 2>&1; then
      gh api 'repos/ava-agent/awesome-ai-ideas/pulls?state=open&per_page=20' \
        --jq '.[] | "- #\(.number) \(.title) | author=\(.user.login) | draft=\(.draft) | updated=\(.updated_at) | \(.html_url)"' || true
      echo
      echo "## Per-PR Diff Summary"
      echo
      gh api 'repos/ava-agent/awesome-ai-ideas/pulls?state=open&per_page=10' --jq '.[].number' 2>/dev/null \
        | while read -r pr; do
            [[ -z "$pr" ]] && continue
            echo "### PR #$pr"
            gh pr diff "$pr" --repo ava-agent/awesome-ai-ideas --stat 2>/dev/null || echo "diff unavailable"
            echo
          done || true
    else
      echo "gh is not installed."
    fi
  } > "$file"
  commit_file "$file" "docs: PR review queue $stamp"
}

pr_ci_triage() {
  ensure_repo
  ensure_identity
  ensure_clean
  mkdir -p docs/automation
  local stamp file
  stamp="$(slot)"
  file="docs/automation/pr-ci-triage-$stamp.md"
  {
    write_header "PR CI Triage $stamp"
    echo "## Open PR Merge State"
    echo
    if command -v gh >/dev/null 2>&1; then
      gh api 'repos/ava-agent/awesome-ai-ideas/pulls?state=open&per_page=20' \
        --jq '.[] | [.number, .title, .mergeable, .mergeable_state, .draft, .head.sha] | @tsv' 2>/dev/null \
        | while IFS="$(printf '\t')" read -r number title mergeable merge_state draft sha; do
            echo "### PR #$number"
            echo
            echo "- Title: $title"
            echo "- Draft: $draft"
            echo "- Mergeable: $mergeable"
            echo "- Merge state: $merge_state"
            echo "- Head SHA: $sha"
            echo
            echo "Checks:"
            gh api "repos/ava-agent/awesome-ai-ideas/commits/$sha/check-runs" \
              --jq '.check_runs[]? | "- \(.name): \(.status)/\(.conclusion)"' 2>/dev/null || echo "- check runs unavailable"
            echo
            echo "Statuses:"
            gh api "repos/ava-agent/awesome-ai-ideas/commits/$sha/status" \
              --jq '"- combined: \(.state)"' 2>/dev/null || echo "- combined status unavailable"
            echo
          done || true
    else
      echo "gh is not installed."
    fi
  } > "$file"
  commit_file "$file" "docs: PR CI triage $stamp"
}

collaboration_snapshot() {
  ensure_repo
  ensure_identity
  ensure_clean
  mkdir -p docs/automation
  local stamp file
  stamp="$(slot)"
  file="docs/automation/three-claws-collaboration-$stamp.md"
  {
    write_header "Three-Claws Collaboration Snapshot $stamp"
    echo "## Roles"
    echo
    echo "- 孔明/main: coordination, acceptance, final external actions."
    echo "- 卧龙/github: read-only GitHub review, PR/issue risk analysis."
    echo "- 凤雏/coding-agent: implementation proposals, local verification, no push."
    echo
    echo "## Current PR Queue"
    echo
    if command -v gh >/dev/null 2>&1; then
      gh api 'repos/ava-agent/awesome-ai-ideas/pulls?state=open&per_page=10' \
        --jq '.[] | "- #\(.number) \(.title) | \(.html_url)"' || true
    else
      echo "gh is not installed."
    fi
    echo
    echo "## Recent Automation Evidence"
    echo
    find docs/automation -maxdepth 1 -type f -name '*.md' -print0 2>/dev/null \
      | xargs -0 ls -t 2>/dev/null \
      | head -12 \
      | sed 's#^#- #' || true
    echo
    echo "## Operating Rules"
    echo
    echo "- Do not auto-merge PRs."
    echo "- Review reports are evidence for humans and agents, not approvals."
    echo "- All commits must remain attributed to kevinten <596823919@qq.com>."
  } > "$file"
  commit_file "$file" "docs: three-claws collaboration snapshot $stamp"
}

idea_backlog() {
  ensure_repo
  ensure_identity
  ensure_clean
  mkdir -p docs/automation
  local stamp file
  stamp="$(slot)"
  file="docs/automation/idea-backlog-$stamp.md"
  {
    write_header "Idea Backlog Index $stamp"
    echo "## Counts"
    echo
    echo "- ideas/*.md: $(find ideas -maxdepth 1 -type f -name '*.md' 2>/dev/null | wc -l | tr -d ' ')"
    echo "- prs/*.md: $(find prs -maxdepth 1 -type f -name '*.md' 2>/dev/null | wc -l | tr -d ' ')"
    echo "- p/* directories: $(find p -maxdepth 1 -mindepth 1 -type d 2>/dev/null | wc -l | tr -d ' ')"
    echo
    echo "## Newest Ideas"
    echo
    find ideas -maxdepth 1 -type f -name '*.md' -print0 2>/dev/null \
      | xargs -0 ls -t 2>/dev/null \
      | head -10 \
      | sed 's#^#- #' || true
    echo
    echo "## Largest Proposal Files"
    echo
    find prs pr ideas -type f -name '*.md' -print0 2>/dev/null \
      | xargs -0 wc -l 2>/dev/null \
      | sort -nr \
      | head -10 \
      | sed 's/^/- /' || true
  } > "$file"
  commit_file "$file" "docs: idea backlog index $stamp"
}

quality_snapshot() {
  ensure_repo
  ensure_identity
  ensure_clean
  mkdir -p docs/automation
  local stamp file
  stamp="$(slot)"
  file="docs/automation/quality-snapshot-$stamp.md"
  {
    write_header "Project Quality Snapshot $stamp"
    echo "## Local Git Repositories"
    echo
    find "$PROJECTS_DIR" -mindepth 2 -maxdepth 2 -type d -name .git \
      | sed 's#/.git$##' \
      | sort \
      | while read -r repo; do
          name="$(basename "$repo")"
          dirty="$(git -C "$repo" status --porcelain 2>/dev/null | wc -l | tr -d ' ')"
          last="$(git -C "$repo" log -1 --oneline 2>/dev/null || echo 'no commits')"
          package="no"
          [[ -f "$repo/package.json" ]] && package="yes"
          echo "- $name: dirty=$dirty package=$package last=$last"
        done
    echo
    echo "## Automation Directory"
    echo
    echo "- Existing automation reports: $(find docs/automation -type f -name '*.md' 2>/dev/null | wc -l | tr -d ' ')"
  } > "$file"
  commit_file "$file" "docs: project quality snapshot $stamp"
}

weekly_review() {
  ensure_repo
  ensure_identity
  ensure_clean
  mkdir -p docs
  local week file
  week="$(date '+%Y-W%V')"
  file="docs/weekly-review-$week.md"
  {
    write_header "Weekly Review $week"
    echo "## Recent Daily Summaries"
    echo
    find docs -maxdepth 1 -type f -name 'daily-summary-*.md' -print0 2>/dev/null \
      | xargs -0 ls -t 2>/dev/null \
      | head -5 \
      | while read -r f; do
          echo "- $(basename "$f")"
          sed -n '1,8p' "$f" | sed 's/^/  /'
        done || true
    echo
    echo "## Recent Automation Signals"
    echo
    find docs/automation -maxdepth 1 -type f -name '*.md' -print0 2>/dev/null \
      | xargs -0 ls -t 2>/dev/null \
      | head -8 \
      | sed 's#^#- #' || true
    echo
    echo "## Repository Snapshot"
    echo
    echo "- Latest commit: $(git log -1 --oneline)"
    echo "- Automation reports: $(find docs/automation -type f -name '*.md' 2>/dev/null | wc -l | tr -d ' ')"
    echo "- Idea files: $(find ideas -type f -name '*.md' 2>/dev/null | wc -l | tr -d ' ')"
    echo
    echo "## Next Focus"
    echo
    echo "- Keep commits attributed to kevinten10."
    echo "- Continue frequent small operational snapshots."
    echo "- Investigate dirty downstream project repositories before enabling automated code changes."
  } > "$file"
  commit_file "$file" "docs: weekly review $week"
}

readme_refresh() {
  ensure_repo
  ensure_identity
  ensure_clean
  local idea_count pr_count doc_count automation_count open_pr_count refresh_date
  idea_count="$(find ideas -maxdepth 1 -type f -name '*.md' 2>/dev/null | wc -l | tr -d ' ')"
  pr_count="$(find prs -maxdepth 1 -type f -name '*.md' 2>/dev/null | wc -l | tr -d ' ')"
  doc_count="$(find docs -type f 2>/dev/null | wc -l | tr -d ' ')"
  automation_count="$(find docs/automation -maxdepth 1 -type f -name '*.md' 2>/dev/null | wc -l | tr -d ' ')"
  open_pr_count="$(gh api 'repos/ava-agent/awesome-ai-ideas/pulls?state=open&per_page=100' --jq 'length' 2>/dev/null || echo 'unknown')"
  refresh_date="$(date '+%Y-%m-%d')"

  cat > README.md <<README
# Awesome AI Ideas

<div align="center">

**AI product ideas that are ready to evaluate, build, and ship.**

[![Ideas](https://img.shields.io/badge/ideas-$idea_count-2f6f6f)](ideas/)
[![Proposal Drafts](https://img.shields.io/badge/proposals-$pr_count-0f766e)](prs/)
[![Automation](https://img.shields.io/badge/automation-active-2563eb)](docs/automation/)
[![Maintained](https://img.shields.io/badge/maintained-by%20OpenClaw-111827)](scripts/openclaw-automation.sh)

</div>

This repository is a product lab for AI-native startup and agent ideas. It is designed for builders, investors, researchers, and operators who want more than a prompt list: each proposal aims to connect a real audience, a painful workflow, a product surface, and an execution path.

## Why Follow This Repository

- Discover AI product directions with clear users, scenarios, and market framing.
- Reuse proposal drafts as starting points for prototypes, pitch decks, specs, or research.
- Track automated repository health, PR review queues, and collaboration snapshots.
- Watch the idea library evolve through scheduled OpenClaw maintenance.

## Current Snapshot

| Area | Count |
| --- | ---: |
| Idea files | $idea_count |
| Proposal drafts | $pr_count |
| Documentation files | $doc_count |
| Automation reports | $automation_count |
| Open pull requests | $open_pr_count |

Last refreshed: $refresh_date.

## Featured Ideas

| Idea | Audience | Why It Matters |
| --- | --- | --- |
| [MedVision AI](prs/1343-medvision-ai.md) | Radiology teams and diagnostic clinics | Precision diagnostic workflows need faster triage, better second reads, and clearer clinical confidence signals. |
| [DriveWise AI](prs/1409-DriveWise-AI.md) | Drivers, fleets, and mobility operators | Safer driving can become a real-time coaching and risk intelligence product instead of a post-incident report. |
| [LegalCompass AI](prs/1200-legalcompass-ai.md) | Small businesses and individuals | Legal access remains expensive and fragmented; AI can guide compliance, document review, and next actions. |
| [FoodWise AI](prs/1172-foodwise-ai.md) | Grocers, restaurants, food banks | Food waste is an operational and social problem that benefits from forecasting, routing, and demand matching. |
| [RuralMed AI](prs/1263-ruralmed-ai.md) | Rural clinics and patients | Rural healthcare needs practical AI support for triage, access, follow-up, and specialist scarcity. |
| [TerraCulture AI](prs/1124-terraculture-ai.md) | Indigenous communities and cultural stewards | Heritage preservation needs tools that respect community control while making knowledge easier to protect and teach. |

## Explore

- [Newest issue-driven ideas](ideas/)
- [Proposal-ready drafts](prs/)
- [Expanded proposal branches](p/)
- [Automation and operations reports](docs/automation/)
- [Roadmap](docs/roadmap.md)
- [Latest weekly review](docs/weekly-review-2026-W26.md)

## For Builders

Use each proposal as a launchpad:

1. Pick a user group with urgent pain.
2. Validate the workflow and existing alternatives.
3. Turn the proposal into a prototype or agent workflow.
4. Open an issue or PR with evidence, scope, and next steps.

Good contributions make ideas more concrete: sharper user segments, clearer workflows, better GTM assumptions, stronger technical architecture, or updated competitive research.

## Maintenance Promise

OpenClaw automation keeps this repository from drifting:

- README refresh runs on a schedule so the public landing page is not lost again.
- PR review and CI triage snapshots track open collaboration work.
- Three-claws collaboration snapshots preserve coordination context.
- Local hooks enforce the \`kevinten <596823919@qq.com>\` commit identity before commits and pushes.

If the README disappears or gets stale, the scheduled maintenance task can regenerate it from the current repository state.
README

  commit_file README.md "docs: refresh README"
}

safe_sync() {
  ensure_repo
  ensure_identity
  export GIT_TERMINAL_PROMPT=0
  git fetch --quiet origin
  if [[ -n "$(git status --porcelain)" ]]; then
    echo "SKIP: working tree is dirty"
    git status --short
    exit 0
  fi
  set -- $(git rev-list --left-right --count origin/main...HEAD)
  local behind="$1"
  local ahead="$2"
  if [[ "$behind" -ne 0 ]]; then
    echo "SKIP: local branch is behind/diverged (behind=$behind ahead=$ahead)"
    exit 0
  fi
  if [[ "$ahead" -eq 0 ]]; then
    echo "Already synced with GitHub"
    exit 0
  fi
  git push origin HEAD:main
  echo "Pushed $ahead commit(s) to GitHub as $GIT_NAME <$GIT_EMAIL>"
}

case "${1:-}" in
  repo-pulse) repo_pulse ;;
  pr-snapshot) pr_snapshot ;;
  pr-review-queue) pr_review_queue ;;
  pr-ci-triage) pr_ci_triage ;;
  collaboration-snapshot) collaboration_snapshot ;;
  idea-backlog) idea_backlog ;;
  quality-snapshot) quality_snapshot ;;
  weekly-review) weekly_review ;;
  readme-refresh) readme_refresh ;;
  safe-sync) safe_sync ;;
  *)
    echo "Usage: $0 {repo-pulse|pr-snapshot|pr-review-queue|pr-ci-triage|collaboration-snapshot|idea-backlog|quality-snapshot|weekly-review|readme-refresh|safe-sync}" >&2
    exit 2
    ;;
esac
