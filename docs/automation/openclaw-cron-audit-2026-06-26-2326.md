# OpenClaw Cron Audit 2026-06-26-2326

- Generated at: 2026-06-26 23:26:10 +0800
- Commit identity: kevinten <596823919@qq.com>
- Remote: https://github.com/ava-agent/awesome-ai-ideas.git

## Summary

- Total jobs: 24
- Enabled jobs: 24
- Disabled jobs: 0
- Status error: 0
- Last run error: 0
- Command jobs: 16
- Agent jobs: 8
- Jobs with stale SKIP summary: 0

## Error Or Attention Jobs


## Command Payload Duplicates


## Schedule Matrix

| Job | Enabled | Status | Kind | Schedule | Next Run Ms | Last Run |
| --- | --- | --- | --- | --- | ---: | --- |
| Workspace Git状态巡检 每4小时（只读） | true | ok | command | every 14400000ms | 1782487780390 | ok |
| MEMORY整理 23:30 | true | ok | agentTurn | cron 30 23 * * * Asia/Shanghai | 1782487800000 | ok |
| AI Ideas PR只读巡检 每6小时 | true | ok | command | every 21600000ms | 1782487845954 | ok |
| AI Ideas quality快照 每日4次 | true | ok | command | cron 50 11,15,19,23 * * * Asia/Shanghai | 1782489000000 | ok |
| OpenClaw Workspace仓库审计 每日07:45 | true | ok | command | cron 45 7 * * * Asia/Shanghai | 1782517500000 | ok |
| 项目健康巡检 08:00 | true | ok | agentTurn | cron 0 8 * * * Asia/Shanghai | 1782518400000 | ok |
| AI Ideas 安全同步 GitHub 每2小时 | true | ok | command | cron 15 8-23/2 * * * Asia/Shanghai | 1782519300000 | ok |
| AI Ideas repo pulse 每2小时 | true | ok | command | cron 20 8-22/2 * * * Asia/Shanghai | 1782519600000 | ok |
| 系统巡检+workspace状态 08:30（只读） | true | ok | command | cron 30 8 * * * Asia/Shanghai | 1782520200000 | ok |
| AI Ideas README维护 每日09:10 | true | ok | command | cron 10 9 * * * Asia/Shanghai | 1782522600000 | ok |
| AI Ideas PR Review Queue 每4小时 | true | ok | command | cron 25 9-21/4 * * * Asia/Shanghai | 1782523500000 | ok |
| 三虾协作健康检查 09:30 | true | ok | agentTurn | cron 30 9 * * * Asia/Shanghai | 1782523800000 | ok |
| AI Ideas PR快照 每3小时 | true | ok | command | cron 40 9-21/3 * * * Asia/Shanghai | 1782524400000 | ok |
| AI Ideas 三爪协作快照 每日10:05 | true | ok | command | cron 5 10 * * * Asia/Shanghai | 1782525900000 | ok |
| AI Ideas backlog索引 每日4次 | true | ok | command | cron 10 10,14,18,22 * * * Asia/Shanghai | 1782526200000 | ok |
| AI Ideas - 想法评估（shell） | true | ok | command | cron 30 10 * * * Asia/Shanghai | 1782527400000 | ok |
| AI Ideas PR CI Triage 每6小时 | true | ok | command | cron 55 10,16,22 * * * Asia/Shanghai | 1782528900000 | ok |
| 🔬 调研：技术趋势+论文+开源+竞品（合并） | true | ok | agentTurn | cron 0 11 * * * Asia/Shanghai | 1782529200000 | ok |
| 功能候选扫描 13:30（只读 shell） | true | ok | command | cron 30 13 * * * Asia/Shanghai | 1782538200000 | ok |
| 进度阻塞+指标追踪 18:30 | true | ok | agentTurn | cron 30 18 * * * Asia/Shanghai | 1782556200000 | ok |
| 📋 每日内容生成：博客+社交媒体+反思（合并） | true | ok | agentTurn | cron 0 22 * * * Asia/Shanghai | 1782568800000 | ok |
| 周度复盘 20:00（shell） | true | ok | command | cron 0 20 * * 0 Asia/Shanghai | 1782648000000 | ok |
| 安全审计 周一14:00（只读） | true | ok | agentTurn | cron 0 14 * * 1 Asia/Shanghai | 1782712800000 | ok |
| 架构设计+路线图 周三12:30 | true | ok | agentTurn | cron 30 12 * * 3 Asia/Shanghai | 1782880200000 | ok |

## Operating Notes

- Error jobs should be fixed or intentionally disabled.
- Stale SKIP summaries are not current failures, but they hide the real latest state until the job runs again.
- Command jobs are preferred for deterministic maintenance; agent jobs should stay narrow and file-scoped.
