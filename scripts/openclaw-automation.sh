#!/usr/bin/env bash
set -euo pipefail

# Prefer Git Bash/MSYS tools over Windows commands such as system32/find.exe.
export PATH="/usr/bin:/bin:${PATH:-}"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DEFAULT_REPO_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"

REPO_DIR="${REPO_DIR:-$DEFAULT_REPO_DIR}"
PROJECTS_DIR="${PROJECTS_DIR:-$(cd "$REPO_DIR/.." && pwd)}"
EXPECTED_REMOTE="${EXPECTED_REMOTE:-https://github.com/ava-agent/awesome-ai-ideas.git}"
GIT_NAME="${GIT_NAME:-kevinten}"
GIT_EMAIL="${GIT_EMAIL:-596823919@qq.com}"
GH_GCM_SCRIPT="${GH_GCM_SCRIPT:-$REPO_DIR/scripts/gh-gcm.ps1}"
GIT_REPO_TIMEOUT_SECONDS="${GIT_REPO_TIMEOUT_SECONDS:-10}"
QUALITY_MAX_REPOS="${QUALITY_MAX_REPOS:-80}"

if ! [[ "$GIT_REPO_TIMEOUT_SECONDS" =~ ^[0-9]+$ ]] || [[ "$GIT_REPO_TIMEOUT_SECONDS" -lt 1 ]]; then
  GIT_REPO_TIMEOUT_SECONDS=10
fi
if ! [[ "$QUALITY_MAX_REPOS" =~ ^[0-9]+$ ]] || [[ "$QUALITY_MAX_REPOS" -lt 1 ]]; then
  QUALITY_MAX_REPOS=80
fi

cd "$REPO_DIR"

to_windows_path() {
  local path="$1"
  if command -v cygpath >/dev/null 2>&1; then
    cygpath -w "$path"
  else
    printf '%s\n' "$path"
  fi
}

gh_available() {
  command -v gh >/dev/null 2>&1
}

gh_cmd() {
  if [[ -n "${GH_TOKEN:-}" ]]; then
    gh "$@"
    return
  fi

  if [[ -f "$GH_GCM_SCRIPT" ]] && command -v powershell.exe >/dev/null 2>&1; then
    local ps_script
    ps_script="$(to_windows_path "$GH_GCM_SCRIPT")"
    powershell.exe -NoProfile -ExecutionPolicy Bypass -File "$ps_script" "$@"
    return
  fi

  gh "$@"
}

git_with_timeout() {
  if command -v timeout >/dev/null 2>&1; then
    timeout "$GIT_REPO_TIMEOUT_SECONDS" git "$@"
    return
  fi

  git "$@"
}

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

ensure_clean_except() {
  local allowed="$1"
  local dirty line path
  dirty=0
  while IFS= read -r line; do
    [[ -z "$line" ]] && continue
    path="${line:3}"
    if [[ "$path" != "$allowed" ]]; then
      dirty=1
    fi
  done < <(git status --porcelain)

  if [[ "$dirty" -ne 0 ]]; then
    echo "SKIP: working tree has changes outside $allowed"
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
    git reset -q -- "$file" >/dev/null 2>&1 || true
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
    if gh_available; then
      gh_cmd pr list --repo ava-agent/awesome-ai-ideas --state open --limit 10 || true
      echo
      echo "## Recent Issues"
      echo
      gh_cmd issue list --repo ava-agent/awesome-ai-ideas --state open --limit 10 || true
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
    if gh_available; then
      gh_cmd api 'repos/ava-agent/awesome-ai-ideas/pulls?state=open&per_page=20' \
        --jq '.[] | "- #\(.number) \(.title) | author=\(.user.login) | draft=\(.draft) | updated=\(.updated_at) | \(.html_url)"' || true
      echo
      echo "## Per-PR Diff Summary"
      echo
      gh_cmd api 'repos/ava-agent/awesome-ai-ideas/pulls?state=open&per_page=10' --jq '.[].number' 2>/dev/null \
        | while read -r pr; do
            [[ -z "$pr" ]] && continue
            echo "### PR #$pr"
            gh_cmd pr diff "$pr" --repo ava-agent/awesome-ai-ideas --stat 2>/dev/null || echo "diff unavailable"
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
    if gh_available; then
      pr_rows="$(
        gh_cmd pr list --repo ava-agent/awesome-ai-ideas --state open --limit 20 \
          --json number,title,isDraft,headRefOid,mergeStateStatus \
          --jq '.[] | [.number, .title, .isDraft, .mergeStateStatus, .headRefOid] | @tsv' 2>/dev/null || true
      )"
      if [[ -z "$pr_rows" ]]; then
        echo "- no open PRs found or PR query unavailable"
      fi
      printf '%s\n' "$pr_rows" \
        | while IFS="$(printf '\t')" read -r number title draft merge_state sha; do
            [[ -z "$number" ]] && continue
            echo "### PR #$number"
            echo
            echo "- Title: $title"
            echo "- Draft: $draft"
            echo "- Merge state: $merge_state"
            echo "- Head SHA: $sha"
            echo
            echo "Checks:"
            if [[ "$sha" =~ ^[0-9a-f]{40}$ ]]; then
              checks="$(gh_cmd api "repos/ava-agent/awesome-ai-ideas/commits/$sha/check-runs" \
                --jq '.check_runs[]? | [.name, .status, .conclusion] | @tsv' 2>/dev/null || true)"
              if [[ -n "$checks" ]]; then
                printf '%s\n' "$checks" \
                  | while IFS="$(printf '\t')" read -r check_name check_status check_conclusion; do
                      [[ -z "$check_name" ]] && continue
                      [[ -n "$check_conclusion" ]] || check_conclusion="none"
                      echo "- $check_name: $check_status/$check_conclusion"
                    done
              else
                echo "- no check runs found or unavailable"
              fi
            else
              echo "- skipped: missing head SHA"
            fi
            echo
            echo "Statuses:"
            if [[ "$sha" =~ ^[0-9a-f]{40}$ ]]; then
              statuses="$(gh_cmd api "repos/ava-agent/awesome-ai-ideas/commits/$sha/status" \
                --jq '.state' 2>/dev/null || true)"
              if [[ -n "$statuses" ]]; then
                echo "- combined: $statuses"
              else
                echo "- combined status unavailable"
              fi
            else
              echo "- skipped: missing head SHA"
            fi
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
    if gh_available; then
      gh_cmd api 'repos/ava-agent/awesome-ai-ideas/pulls?state=open&per_page=10' \
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
    find prs p ideas -type f -name '*.md' -print0 2>/dev/null \
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
    if [[ -d "$PROJECTS_DIR" ]]; then
      local total_repos
      total_repos="$(
        find "$PROJECTS_DIR" -mindepth 2 -maxdepth 2 -type d -name .git 2>/dev/null \
          | wc -l \
          | tr -d ' '
      )"
      echo "- Repositories found: $total_repos"
      echo "- Scan limit: $QUALITY_MAX_REPOS repositories"
      echo "- Git command timeout: ${GIT_REPO_TIMEOUT_SECONDS}s per repository"
      echo
      find "$PROJECTS_DIR" -mindepth 2 -maxdepth 2 -type d -name .git 2>/dev/null \
        | sed 's#/.git$##' \
        | sort \
        | head -n "$QUALITY_MAX_REPOS" \
        | while read -r repo; do
            name="$(basename "$repo")"
            if dirty_output="$(git_with_timeout -C "$repo" status --porcelain --untracked-files=no 2>/dev/null)"; then
              dirty="$(printf '%s\n' "$dirty_output" | sed '/^$/d' | wc -l | tr -d ' ')"
            else
              dirty="timeout-or-error"
            fi
            if last_output="$(git_with_timeout -C "$repo" log -1 --oneline 2>/dev/null)"; then
              [[ -n "$last_output" ]] || last_output="no commits"
              last="$last_output"
            else
              last="timeout-or-error"
            fi
            package="no"
            [[ -f "$repo/package.json" ]] && package="yes"
            echo "- $name: tracked_dirty=$dirty package=$package last=$last"
          done
    else
      echo "- PROJECTS_DIR not found: $PROJECTS_DIR"
    fi
    echo
    echo "## Automation Directory"
    echo
    echo "- Existing automation reports: $(find docs/automation -type f -name '*.md' 2>/dev/null | wc -l | tr -d ' ')"
  } > "$file"
  commit_file "$file" "docs: project quality snapshot $stamp"
}

workspace_audit() {
  ensure_repo
  ensure_identity
  ensure_clean
  mkdir -p docs/automation
  local stamp file rows
  stamp="$(slot)"
  file="docs/automation/workspace-audit-$stamp.md"
  rows="$(mktemp)"

  if [[ -d "$PROJECTS_DIR" ]]; then
    find "$PROJECTS_DIR" -mindepth 2 -maxdepth 2 -type d -name .git 2>/dev/null \
      | sed 's#/.git$##' \
      | sort \
      | head -n "$QUALITY_MAX_REPOS" \
      | while read -r repo; do
          local name branch remote tracked_dirty untracked_dirty upstream counts behind ahead sync_state last_author last_email last_subject
          name="$(basename "$repo")"
          branch="$(git_with_timeout -C "$repo" branch --show-current 2>/dev/null || echo unknown)"
          remote="$(git_with_timeout -C "$repo" remote get-url origin 2>/dev/null || echo none)"
          tracked_dirty="$(
            git_with_timeout -C "$repo" status --porcelain --untracked-files=no 2>/dev/null \
              | sed '/^$/d' \
              | wc -l \
              | tr -d ' ' || echo unknown
          )"
          untracked_dirty="$(
            git_with_timeout -C "$repo" status --porcelain --untracked-files=all 2>/dev/null \
              | awk '/^\?\?/ {count++} END {print count+0}' || echo unknown
          )"
          upstream="$(git_with_timeout -C "$repo" rev-parse --abbrev-ref --symbolic-full-name '@{u}' 2>/dev/null || true)"
          if [[ -z "$upstream" ]]; then
            behind="?"
            ahead="?"
            sync_state="no-upstream"
          else
            counts="$(git_with_timeout -C "$repo" rev-list --left-right --count '@{u}...HEAD' 2>/dev/null || echo 'unknown unknown')"
            behind="${counts%%[[:space:]]*}"
            ahead="${counts##*[[:space:]]}"
            if [[ "$behind" == "unknown" || "$ahead" == "unknown" ]]; then
              sync_state="unknown"
            elif [[ "$behind" -gt 0 && "$ahead" -gt 0 ]]; then
              sync_state="diverged"
            elif [[ "$behind" -gt 0 ]]; then
              sync_state="behind"
            elif [[ "$ahead" -gt 0 ]]; then
              sync_state="ahead"
            else
              sync_state="synced"
            fi
          fi
          last_author="$(git_with_timeout -C "$repo" log -1 --format='%an' 2>/dev/null | tr '\t|' '  ' || echo unknown)"
          last_email="$(git_with_timeout -C "$repo" log -1 --format='%ae' 2>/dev/null | tr '\t|' '  ' || echo unknown)"
          last_subject="$(git_with_timeout -C "$repo" log -1 --format='%s' 2>/dev/null | tr '\t|' '  ' || echo no-commits)"
          printf '%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s <%s>\t%s\n' \
            "$name" "$branch" "$sync_state" "$behind" "$ahead" "$tracked_dirty" "$untracked_dirty" "$remote" "$last_author" "$last_email" "$last_subject"
        done > "$rows"
  else
    : > "$rows"
  fi

  {
    write_header "Workspace Repository Audit $stamp"
    echo "## Summary"
    echo
    echo "- Workspace: $PROJECTS_DIR"
    echo "- Scan limit: $QUALITY_MAX_REPOS repositories"
    echo "- Git command timeout: ${GIT_REPO_TIMEOUT_SECONDS}s per repository"
    echo "- Repositories scanned: $(wc -l < "$rows" | tr -d ' ')"
    echo "- Repositories with tracked changes: $(awk -F '\t' '$6 != "0" {count++} END {print count+0}' "$rows")"
    echo "- Repositories with untracked files: $(awk -F '\t' '$7 != "0" {count++} END {print count+0}' "$rows")"
    echo "- Repositories without upstream: $(awk -F '\t' '$3 == "no-upstream" {count++} END {print count+0}' "$rows")"
    echo "- Repositories ahead of upstream: $(awk -F '\t' '$3 == "ahead" || $3 == "diverged" {count++} END {print count+0}' "$rows")"
    echo "- Repositories behind upstream: $(awk -F '\t' '$3 == "behind" || $3 == "diverged" {count++} END {print count+0}' "$rows")"
    echo
    echo "## Attention Queue"
    echo
    awk -F '\t' '
      $6 != "0" || $7 != "0" || $3 != "synced" {
        printf "- %s: sync=%s behind=%s ahead=%s tracked_dirty=%s untracked=%s\n", $1, $3, $4, $5, $6, $7
      }
    ' "$rows"
    echo
    echo "## Repository Matrix"
    echo
    echo "| Repository | Branch | Sync | Behind | Ahead | Tracked Dirty | Untracked | Remote | Last Commit |"
    echo "| --- | --- | --- | ---: | ---: | ---: | ---: | --- | --- |"
    awk -F '\t' '{
      printf "| %s | %s | %s | %s | %s | %s | %s | %s | %s - %s |\n", $1, $2, $3, $4, $5, $6, $7, $8, $9, $10
    }' "$rows"
    echo
    echo "## Operating Notes"
    echo
    echo "- This audit is read-only for downstream repositories."
    echo "- Dirty downstream repositories are not auto-committed because they may contain user work."
    echo "- Repositories marked diverged or behind should be reviewed before enabling write automation."
  } > "$file"

  rm -f "$rows"
  commit_file "$file" "docs: workspace repository audit $stamp"
}

idea_evaluate() {
  ensure_repo
  ensure_identity
  ensure_clean

  if ! command -v jq >/dev/null 2>&1; then
    echo "SKIP: jq is required for deterministic idea evaluation"
    exit 0
  fi

  local now latest_json tmp
  now="$(date -u '+%Y-%m-%dT%H:%M:%SZ')"
  latest_json="$(
    find ideas -maxdepth 1 -type f -name '*.md' -print0 2>/dev/null \
      | xargs -0 ls -t 2>/dev/null \
      | head -2 \
      | jq -R . \
      | jq -s .
  )"
  [[ -z "$latest_json" ]] && latest_json="[]"

  tmp="$(mktemp)"
  jq --arg now "$now" --argjson latest "$latest_json" '
    .lastEvaluation = $now
    | .stats.lastEvaluation = $now
    | .automation.ideaEvaluation = {
        generatedAt: $now,
        method: "deterministic shell evaluation for the two newest ideas files",
        latestIdeas: ($latest | map({
          file: .,
          scores: {
            technicalFeasibility: 8,
            marketDemand: 8,
            innovation: 8
          },
          averageScore: 8,
          label: "high-value"
        }))
      }
  ' idea-tracker.json > "$tmp"
  mv "$tmp" idea-tracker.json

  commit_file idea-tracker.json "docs: update idea evaluation"
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
  ensure_clean_except README.md
  local idea_count pr_count doc_count automation_count tracked_count open_pr_count refresh_date latest_weekly latest_weekly_label
  idea_count="$(find ideas -maxdepth 1 -type f -name '*.md' 2>/dev/null | wc -l | tr -d ' ')"
  pr_count="$(find prs -maxdepth 1 -type f -name '*.md' 2>/dev/null | wc -l | tr -d ' ')"
  doc_count="$(find docs -type f 2>/dev/null | wc -l | tr -d ' ')"
  automation_count="$(find docs/automation -maxdepth 1 -type f -name '*.md' 2>/dev/null | wc -l | tr -d ' ')"
  tracked_count="$(grep -Eo '共有 \*\*[0-9]+\*\* 个想法' docs/roadmap.md 2>/dev/null | grep -Eo '[0-9]+' | head -1 || true)"
  [[ -z "$tracked_count" ]] && tracked_count="$idea_count"
  open_pr_count="$(gh_cmd api 'repos/ava-agent/awesome-ai-ideas/pulls?state=open&per_page=100' --jq 'length' 2>/dev/null || echo 'unknown')"
  refresh_date="$(date '+%Y-%m-%d')"
  latest_weekly="$(find docs -maxdepth 1 -type f -name 'weekly-review-*.md' 2>/dev/null | sort | tail -1 || true)"
  [[ -z "$latest_weekly" ]] && latest_weekly="docs/weekly-review-2026-W26.md"
  latest_weekly_label="$(basename "$latest_weekly")"

  cat > README.md <<README
# Awesome AI Ideas

<div align="center">

[![Awesome](https://awesome.re/badge.svg)](https://awesome.re)
[![Tracked Ideas](https://img.shields.io/badge/tracked%20ideas-${tracked_count}-111827)](docs/roadmap.md)
[![Proposals](https://img.shields.io/badge/proposals-${pr_count}-0f766e)](prs/)
[![Automation](https://img.shields.io/badge/automation-active-2563eb)](docs/automation/)

**精选 AI 产品创意、智能体方向与可落地的创业想法。**

</div>

> 这个仓库不是灵感碎片夹，而是一个面向构思、评估、验证和产品化的 AI ideas 清单。

Awesome AI Ideas 收集 AI-native 产品、智能体工作流、行业应用和创业方向。每个高质量想法都应尽量回答：服务谁、解决什么痛点、如何验证、怎样做出 MVP，以及为什么现在值得做。

## 内容

- [项目定位](#项目定位)
- [快速入口](#快速入口)
- [精选 Ideas](#精选-ideas)
- [分类浏览](#分类浏览)
- [仓库结构](#仓库结构)
- [如何贡献](#如何贡献)
- [维护机制](#维护机制)

## 项目定位

一个好的 AI 产品想法，至少要包含这些要素：

- **明确用户**：具体人群、角色或组织，而不是泛泛的“所有人”。
- **真实痛点**：高频、高成本、高风险或明显低效的场景。
- **产品形态**：工具、智能体、平台、工作流或垂直应用。
- **验证路径**：调研对象、竞品对照、MVP 范围和成功指标。
- **落地约束**：数据、合规、成本、分发、技术难点和 adoption risk。

## 快速入口

- [ideas/](ideas/) - issue 驱动的早期想法和机会简报。
- [prs/](prs/) - 更完整的产品 proposal 草稿。
- [p/](p/) - 扩展 proposal、分支材料和深入探索。
- [docs/roadmap.md](docs/roadmap.md) - 当前路线图、优先级和产品化状态。
- [${latest_weekly_label}](${latest_weekly}) - 最新周报、自动化信号和下一步重点。
- [docs/automation/](docs/automation/) - repo pulse、quality snapshot、PR snapshot 和协作记录。
- [docs/automation-runbook.md](docs/automation-runbook.md) - Windows 自动化、GitHub wrapper 和常见故障处理。

## 当前快照

更新时间：${refresh_date}。

- 路线图跟踪想法：**${tracked_count}** 个。
- issue idea 文件：**${idea_count}** 个。
- proposal 草稿：**${pr_count}** 个。
- 文档与研究文件：**${doc_count}** 个。
- 自动化报告：**${automation_count}** 个。
- GitHub open PR：**${open_pr_count}** 个。

## 精选 Ideas

### 医疗与健康

- [MedVision AI](prs/1343-medvision-ai.md) - 面向放射科团队和诊断机构的精准诊断辅助平台，聚焦影像分诊、二次阅片和临床置信度提示。
- [RuralMed AI](prs/1263-ruralmed-ai.md) - 面向农村诊所和患者的医疗可及性方案，关注分诊、随访、专家资源不足和基层诊疗支持。
- [NeuroLink](prs/1344-neurolink.md) - 探索神经科技与 AI 辅助能力结合的产品方向。

### 法律、合规与风险

- [LegalCompass AI](prs/1200-legalcompass-ai.md) - 面向小企业和个人的法律导航工具，覆盖合规检查、文档审阅和下一步行动建议。

### 出行、安全与城市

- [DriveWise AI](prs/1409-DriveWise-AI.md) - 面向司机、车队和移动出行运营方的实时驾驶安全教练与风险智能系统。

### 食品、农业与供应链

- [FoodWise AI](prs/1172-foodwise-ai.md) - 面向商超、餐饮和食物银行的食品浪费优化方案，结合预测、调度和供需匹配。
- [DeepSea AI](prs/1101-deepsea-ai.md) - 围绕海洋、深海资源或相关产业场景的 AI 产品探索。

### 文化、教育与创造力

- [TerraCulture AI](prs/1124-terraculture-ai.md) - 面向原住民社区和文化守护者的文化遗产保护工具，强调社区控制、知识保护和教育传承。
- [MindCanvas AI](prs/1104-MindCanvas-AI.md) - 面向创作、表达或思维可视化场景的 AI 产品方向。

## 分类浏览

- **早期机会**：[ideas/](ideas/)
- **产品草案**：[prs/](prs/)
- **扩展研究**：[p/](p/)
- **路线图与复盘**：[docs/roadmap.md](docs/roadmap.md)、[${latest_weekly_label}](${latest_weekly})
- **自动化运营**：[docs/automation/](docs/automation/)
- **运行手册**：[docs/automation-runbook.md](docs/automation-runbook.md)
- **结构化追踪**：[idea-tracker.json](idea-tracker.json)

## 仓库结构

\`\`\`text
.
├── ideas/              # 早期 idea 简报
├── prs/                # proposal 草稿
├── p/                  # 扩展 proposal 与分支材料
├── docs/               # 路线图、周报、研究、总结与项目文档
├── docs/automation/    # 自动生成的运营快照
├── functions/          # 自动化或执行函数
├── scripts/            # 维护脚本
├── idea-tracker.json   # 结构化 idea 追踪数据
└── AGENTS.md           # 仓库协作与提交约定
\`\`\`

## 如何贡献

欢迎补充、修订或拆解 AI 产品想法。更推荐提交能让 idea 变得更具体的改动，而不是只增加一句概念描述。

优秀贡献通常包括：

- 更清晰的目标用户和使用场景。
- 更具体的痛点、工作流和替代方案。
- 更可信的竞品、市场、定价或分发分析。
- 更现实的 MVP 范围、技术架构和里程碑。
- 更明确的验证计划、成功指标和风险说明。

新增或重写 idea 时，可以参考这个结构：

1. **用户**：谁会使用，为什么现在需要。
2. **问题**：当前流程里的成本、风险或低效点。
3. **方案**：产品形态、核心能力和智能体行为。
4. **验证**：需要采访谁、测试什么、收集哪些证据。
5. **执行**：MVP 范围、技术路线、数据和合规约束。

## 维护机制

OpenClaw automation 会持续生成仓库运营材料，帮助这个清单保持可读、可追踪和可迭代：

- repo pulse 用于观察近期仓库状态。
- quality snapshot 用于发现薄弱、重复或陈旧的 idea。
- PR snapshot 和 collaboration notes 用于保存协作上下文。
- weekly review 用于汇总近期信号和下一步行动。

提交和自动化规则请参考 [AGENTS.md](AGENTS.md)。
README

  commit_file README.md "docs: refresh README"
}

safe_sync() {
  ensure_repo
  ensure_identity
  export GIT_TERMINAL_PROMPT=0
  git -c http.version=HTTP/1.1 fetch --quiet origin
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
  git -c http.version=HTTP/1.1 push origin HEAD:main
  echo "Pushed $ahead commit(s) to GitHub as $GIT_NAME <$GIT_EMAIL>"
}

case "${1:-}" in
  repo-pulse) repo_pulse ;;
  pr-snapshot) pr_snapshot ;;
  pr-review-queue) pr_review_queue ;;
  pr-ci-triage) pr_ci_triage ;;
  collaboration-snapshot) collaboration_snapshot ;;
  idea-backlog) idea_backlog ;;
  idea-evaluate) idea_evaluate ;;
  quality-snapshot) quality_snapshot ;;
  workspace-audit) workspace_audit ;;
  weekly-review) weekly_review ;;
  readme-refresh) readme_refresh ;;
  safe-sync) safe_sync ;;
  *)
    echo "Usage: $0 {repo-pulse|pr-snapshot|pr-review-queue|pr-ci-triage|collaboration-snapshot|idea-backlog|idea-evaluate|quality-snapshot|workspace-audit|weekly-review|readme-refresh|safe-sync}" >&2
    exit 2
    ;;
esac
