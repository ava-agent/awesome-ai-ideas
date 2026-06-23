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
  idea-backlog) idea_backlog ;;
  quality-snapshot) quality_snapshot ;;
  weekly-review) weekly_review ;;
  safe-sync) safe_sync ;;
  *)
    echo "Usage: $0 {repo-pulse|pr-snapshot|idea-backlog|quality-snapshot|weekly-review|safe-sync}" >&2
    exit 2
    ;;
esac
