# Weekly Review 2026-W26

- Generated at: 2026-06-28 16:45 +0800
- Scope: README, roadmap, idea tracker, automation reports, and live GitHub PR/issue checks
- Commit identity required by AGENTS.md: `kevinten <596823919@qq.com>`

## 本周结论

本周仓库从常规快照进入“自动化产物需要降噪、统计口径需要校准”的阶段。README 已在本轮刷新并校准 open PR 数，自动化报告数、proposal 数和最新周报链接基本有效；剩余核心问题是 `idea-tracker.json` 存在重复 key/统计口径不一致，`docs/roadmap.md` 的 65 个想法与结构化解析结果无法直接对齐。

路线图暂不建议自动改。当前优先顺序仍写作：AI职场软技能导师 -> AI简历诊断师 -> AI音乐创作伙伴 -> AI个人成长教练；但趋势扫描显示 Agent Security ReviewOps 和 Healthcare Admin Precision Copilot 是更值得进入下一轮候选评估的新方向，应先补成结构化 idea，再决定是否调整路线图。

## 本周新增或变化

- README 当前快照日期为 2026-06-26，显示 65 个路线图想法、3 个 issue idea、9 个 proposal、70 个自动化报告、2 个 open PR。
- 实测 `docs/automation/` 当前确有 70 个报告；`ideas/*.md` 为 3 个，`prs/*.md` 为 9 个，`p/*` 目录为 9 个。
- GitHub 实时检查显示 open PR 有 2 个：#1437 `MfgKnowledge AI` 文档 PR 与 #1368 `ChainVision AI`；6 月 25 日自动化报告里的 #1420 已不再出现在 open PR 列表中，因此 README 需要刷新到 open PR=2。
- GitHub open issue 最新信号包含 #1434 “AI讨论：你还享受手动写代码的乐趣吗？”以及 #1426 `MfgKnowledge AI`，其中 #1426 已带 `quality:high`、`ai-agents`、`knowledge-graph`、`rag` 标签。
- `trend-candidates-2026-06-26.md` 新增 5 个趋势候选，并明确推荐优先跟进 `Agent Security ReviewOps` 与 `Healthcare Admin Precision Copilot`。
- 未发现名为 `idea-priority-review` 或 `idea-quality-gaps` 的报告文件；对应信号主要分散在 `idea-backlog-*`、`quality-snapshot-*`、`trend-candidates-*` 和 `idea-tracker.json`。

## README 状态

README 整体可用，关键统计已在本轮校准：

- 有效：最新周报链接、automation 报告数 70、issue idea 3、proposal 9 与本地文件系统一致。
- 已校准：GitHub open PR 已刷新为 2，与实时 `gh-gcm.ps1 pr list` 一致。
- 需核对：路线图追踪想法 65 与 `idea-tracker.json` 的结构化解析结果不一致。

本轮已将 README open PR 数更新为实时值；后续仍应通过 `readme-refresh` 自动保持统计一致。

## Tracker 与 Roadmap 一致性

`docs/roadmap.md` 截至 2026-06-24，写明 65 个想法、12 个已产品化、1 个进行中、16 个高价值待启动，下一阶段优先顺序为 AI职场软技能导师、AI简历诊断师、AI音乐创作伙伴、AI个人成长教练。

`idea-tracker.json` 的元数据为：

- `lastSync`: 2026-04-23T09:01:00Z
- `lastReview`: 2026-04-02T02:30:00Z
- `lastEvaluation`: 2026-06-25T02:30:00Z

结构化解析可见 60 个 idea 对象，状态分布为 19 个 low-value、16 个 high-value、9 个 new、9 个 completed、4 个 medium-value、1 个 created、1 个 duplicate、1 个 in-progress。原始文本扫描发现 76 个 key 声明但只有 61 个唯一 key，说明文件里存在重复 key；这会让标准 JSON 解析覆盖旧值，并解释了 tracker、roadmap、README 之间的数量差异。

当前 in-progress 仍只有 `AI Workspace Orchestrator`，`lastUpdated` 为 2026-04-12，phase 停留在用户注册/登录/JWT/角色更新阶段。若该项目近期没有外部进展，roadmap 中的“正在开发中”状态需要人工确认是否仍有效。

## 自动化报告质量

报告覆盖面足够，但噪音偏多：

- `repo-pulse`: 18 份
- `pr-snapshot`: 12 份
- `idea-backlog`: 10 份
- `pr-review-queue`: 10 份
- `quality-snapshot`: 9 份
- `pr-ci-triage`: 7 份
- `three-claws-collaboration`: 3 份
- `trend-candidates`: 1 份

主要噪音来自同一天多次低信息量快照。PR CI triage 报告还出现 `No commit found for SHA: /check-runs` 和 `Ref not found`，说明 CI 检查抓取逻辑需要修正，否则会持续产出不可行动的错误文本。建议保留趋势扫描、每日 1 次 repo pulse、每日 1 次 idea backlog、按需 PR/CI triage，减少固定频率的重复 PR snapshot。

## 最值得推进的 3 个动作

1. 修复 `idea-tracker.json` 的重复 key 和统计口径，再用同一口径刷新 roadmap/README 数字。先只做数据清洗和校验，不重排路线图。
2. 将 `Agent Security ReviewOps` 与 `Healthcare Admin Precision Copilot` 各补一份标准 idea 草稿，并与现有 high-value 列表做去重评分。
3. 降低自动化报告噪音：修复 PR CI triage 的 SHA/ref 获取逻辑，将重复快照合并为“最新状态 + 变化摘要”。

## 路线图是否需要更新

暂不自动更新。需要更新的不是优先级文字本身，而是支撑它的统计证据：tracker 重复 key、AI Workspace Orchestrator 进展停留日期，以及 README/GitHub 统计需要持续自动校准。等这些基础数据修正后，再决定是否把趋势候选纳入下一阶段优先顺序。

## 下周检查点

- README open PR 数是否继续与实时 GitHub PR 列表保持一致。
- `idea-tracker.json` 是否完成重复 key 清理并能被标准 JSON parser 稳定解析。
- #1426 `MfgKnowledge AI` 是否进入本地 idea/proposal 文档。
- #1368 `ChainVision AI` 是否仍长期滞留 open 状态，是否需要关闭、更新或转为本地 proposal。
- 自动化目录是否继续按小时生成重复报告；若是，应调整计划频率或报告合并策略。
