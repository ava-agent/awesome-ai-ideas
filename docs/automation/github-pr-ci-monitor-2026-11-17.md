# GitHub PR / CI 监控（2026-11-17）

> 归属：`awesome-ai-ideas-github-pr-ci + docs/automation/github-pr-ci-monitor-2026-11-17.md + 2026-11-17`

## 取证范围

- 仓库：`ava-agent/awesome-ai-ideas`
- 基线：远端 `main` `9c4e305800a45d5f7ef0a8fc6b4519dcb9f23fa3`
- 查询时间：2026-11-17（Asia/Shanghai）
- 访问身份：`kevinten10`（通过 `scripts/gh-gcm.ps1` 验证）

## 实时摘要

| 项目 | 本次 | 上次成功快照（2026-11-16） | 变化 |
| --- | ---: | ---: | --- |
| 开放 PR | 18 | 17 | +1 |
| 开放 Issue | 755 | 755 | 无变化 |

## 新增或状态变化

- 新增 [PR #1601：docs: weekly review 2026-W46](https://github.com/ava-agent/awesome-ai-ideas/pull/1601)，于 2026-11-15 更新。该 PR 目标分支为 `main`，当前 `mergeStateStatus` 为 `CLEAN`；没有审批记录，`statusCheckRollup` 为空。`CLEAN` 只表示当前可合并，不能视为 CI 已通过。
- 上次快照中的 17 个开放 PR 仍在列表中，未观察到合并状态变化；开放 Issue 总数未变化。

## 每周最旧项目抽查

首次成功的 ISO 第 47 周运行抽查了最旧的三个开放 Issue；它们仍为开放状态，均无标签，最近更新时间未变：

- [Issue #1](https://github.com/ava-agent/awesome-ai-ideas/issues/1)：2026-03-21T13:16:22Z
- [Issue #4](https://github.com/ava-agent/awesome-ai-ideas/issues/4)：2026-03-21T12:15:41Z
- [Issue #8](https://github.com/ava-agent/awesome-ai-ideas/issues/8)：2026-03-21T03:15:39Z

## 建议动作

1. P1：为 [PR #1601](https://github.com/ava-agent/awesome-ai-ideas/pull/1601) 安排维护者审阅；当前没有审批。
2. P1：确认 [PR #1601](https://github.com/ava-agent/awesome-ai-ideas/pull/1601) 的仓库 CI 是否应触发；当前没有任何 check-run/status，不能据此判断通过。
