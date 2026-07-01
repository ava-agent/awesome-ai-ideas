# GitHub PR/CI Monitor - 2026-06-30

Run time: 2026-06-30 11:30 Asia/Shanghai

## Scope

- Repository: `ava-agent/awesome-ai-ideas`
- Remote: `https://github.com/ava-agent/awesome-ai-ideas.git`
- Branch checked locally: `main`
- GitHub access: OK via `scripts/gh-gcm.ps1`
- Network: `github.com:443` reachable
- Local workspace before report: clean

## Summary

- Open PRs: 2
- Open issues: 684
- PR branches with recent workflow runs: none found for the 2 open PR branches
- Latest 20 workflow runs: all completed with `failure`, latest run from 2026-04-28
- Latest default branch push: 2026-06-30T02:02:00Z

## Open PRs

| PR | State | Review | Checks | Updated | Notes |
| --- | --- | --- | --- | --- | --- |
| [#1437](https://github.com/ava-agent/awesome-ai-ideas/pull/1437) Add idea document #1426: MfgKnowledge AI | `CLEAN` | none | no check rollup | 2026-06-28T14:02:57Z | Adds `docs/ideas/issue-1426.md`; no reviews or comments yet. |
| [#1368](https://github.com/ava-agent/awesome-ai-ideas/pull/1368) ChainVision AI | `CLEAN` | `APPROVED` | no check rollup | 2026-05-05T05:22:55Z | Long-lived approved PR; current file list is one added file under `p/pr-1368/1268-chainvision-ai.md`. |

## CI Status

- Recent Actions runs are stale: the latest listed run is [25058559809](https://github.com/ava-agent/awesome-ai-ideas/actions/runs/25058559809), created 2026-04-28T14:23:06Z, conclusion `failure`.
- The latest run failed both matrix test jobs:
  - `test (18.x)`: `failure`
  - `test (20.x)`: `failure`
  - `deploy`: `skipped`
  - `quality-check`: `skipped`
- No workflow runs were found for `feature/add-issue-1426-mfgknowledge-ai` or `fix/issue-1268`.

## Issue Backlog

- Open issues: 684.
- Issues not updated since 2026-05-31: 673.
- Issues not updated since 2026-05-01: 595.
- Oldest stale examples:
  - [#12](https://github.com/ava-agent/awesome-ai-ideas/issues/12) updated 2026-03-21T02:15:35Z
  - [#13](https://github.com/ava-agent/awesome-ai-ideas/issues/13) updated 2026-03-21T02:15:36Z
  - [#8](https://github.com/ava-agent/awesome-ai-ideas/issues/8) updated 2026-03-21T03:15:39Z
- Duplicate-looking current issues:
  - [#1444](https://github.com/ava-agent/awesome-ai-ideas/issues/1444), [#1445](https://github.com/ava-agent/awesome-ai-ideas/issues/1445), and [#1446](https://github.com/ava-agent/awesome-ai-ideas/issues/1446) all use the same `.self` title.

## Action List

### P0

- Fix or intentionally retire the stale CI pipeline. The most recent 20 workflow runs all failed, and the newest run is from 2026-04-28, so current PR quality gates are not providing a reliable signal.

### P1

- Review [#1368](https://github.com/ava-agent/awesome-ai-ideas/pull/1368) manually for merge readiness. It is approved and `CLEAN`, but it has been idle since 2026-05-05 and has no current check run.
- Review [#1437](https://github.com/ava-agent/awesome-ai-ideas/pull/1437) manually. It is `CLEAN` but has no review and no check run.
- Triage the three duplicate-looking `.self` issues ([#1444](https://github.com/ava-agent/awesome-ai-ideas/issues/1444), [#1445](https://github.com/ava-agent/awesome-ai-ideas/issues/1445), [#1446](https://github.com/ava-agent/awesome-ai-ideas/issues/1446)) before converting more issue content into PRs.

### P2

- Start a backlog aging pass for issues older than 2026-05-31. The open backlog is 684 issues, with 673 not updated since that date.
- Add a lightweight PR monitor check that flags open PRs with empty `statusCheckRollup`, so review decisions are not mistaken for CI coverage.
