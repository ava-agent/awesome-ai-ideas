# Idea 质量巡检缺口报告 - 2026-11-18

## 巡检基线与范围

- 来源仓库：`https://github.com/ava-agent/awesome-ai-ideas.git`
- 远端 `main` 基线：`9c4e305800a45d5f7ef0a8fc6b4519dcb9f23fa3`
- 已读：`AGENTS.md`、`docs/automation-runbook.md`、`idea-tracker.json`、`ideas/`、`prs/`、`p/` 的目录清单，以及既有报告 `docs/automation/idea-quality-gaps-2026-07-01.md`。
- tracker 的 7 个 `priority: 1` 条目文件路径均无法在当前仓库根目录解析；本轮不猜测其对应内容。抽查了 `ideas/` 中 5 个未在既有报告中列出的条目（#1431、两个 #1432、#1433、#1434）。
- 本报告不修改 idea、proposal 或 tracker 正文；仅记录新增巡检结论。

## 新增或恶化的可执行缺口

### 1. TokenWeave AI 与 SolScale AI 的首个产品切口重叠，缺少归属与可比较验证

- 证据：`ideas/issue-1431--for-AI-Developers--Product-Builders--TokenWeave-AI--From-token-bloat-and-wasted-costs-to-intentional-minimal-token-design-and-LLM-efficiency-ecosystem.md:10-24` 覆盖 token 成本、提示压缩、上下文/缓存和效率监控；其 MVP 同时列出监控、压缩、评估、Web 和 CLI（`:89-101`）。`ideas/issue-1433--for-Enterprise-IT-Teams--SolScale-AI--From-LLM-cost-and-latency-pain-to-intelligent-GPT-5-6-Sol-powered-inference-optimization-platform.md:10-24` 覆盖同一组成本、提示工程、缓存与监控需求，MVP 又包含模型路由、语义缓存、成本/性能仪表板（`:98-109`）。两者都面向企业/开发者并采用 SaaS、企业授权/API/咨询路径（#1431 `:144-162`；#1433 `:148-174`）。
- 缺口：两条目都声称 LLM 成本与延迟优化，但没有明确哪一个拥有压缩/评估、哪一个拥有网关路由，也没有共用的基线任务、质量损失阈值或成本归因方式。并行推进会重复建设并使“节省”无法比较。
- 最小补齐动作：增加一张共享定位卡，指定 TokenWeave 仅负责离线提示/上下文压缩评测，或将其并入 SolScale；为保留的条目定义同一 3 个真实请求集、质量基线、每千次请求成本和 p95 延迟的测量方法。
- 验收条件：每项能力只归属一个主条目；在固定请求集上可复跑“压缩前后质量变化、成本、p95 延迟”，并预先写明继续/停止阈值。

### 2. 两个无关条目共用 Issue #1432，破坏引用、去重与后续验证追溯

- 证据：`ideas/issue-1432--for-Anxiety-Sufferers-Loneliness-Individuals-Mental-Health-Supporters-EmoSoul-BCI--From-emotional-isolation-and-ineffective-therapy-to-AI-powered-brain-emotion-digital-twin-ecosystem.md:1-3` 将心理健康 BCI 条目标为 `Issue #1432`；`ideas/issue-1432--for-Content-Creators--Video-Producers-MontageFlow-AI--From-manual-video-editing-chaos-to-AI-powered-agentic-video-production-ecosystem.md:1-3` 也将视频制作条目标为 `Issue #1432`。两者的 MVP 分别是情感识别/音频干预（EmoSoul `:103-115`）和视频规划、脚本、拼接、字幕（MontageFlow `:95-107`），不是同一产品。
- 缺口：文件名、标题内编号和任何外部 issue 链接无法一一对应；后续 tracker、用户访谈或实验结果会被错误归并。
- 最小补齐动作：在 GitHub issue 与对应 Markdown 之间做一次编号核对，给其中一个条目恢复其真实 issue 编号，并在两个文件中补充显式的 issue URL。
- 验收条件：目录内每个 `issue-<n>` 前缀、正文 `## Issue #<n>` 和链接三者一致，且同一编号只映射到一个 idea。

### 3. EmoSoul BCI 的危机处置、医疗声明和数据删除边界不足以支撑“预警—干预”闭环

- 证据：该条目以焦虑、孤独和低效心理干预为目标，提出“干预方案生成”和“情绪危机预警系统”（`ideas/issue-1432--for-Anxiety-Sufferers-Loneliness-Individuals-Mental-Health-Supporters-EmoSoul-BCI--From-emotional-isolation-and-ineffective-therapy-to-AI-powered-brain-emotion-digital-twin-ecosystem.md:74-80`），MVP 即用消费级设备识别焦虑/放松/专注并播放干预音频（`:103-110`）。风险段只列设备信号、准确率和认证不确定性（`:198-220`），以及泛化的加密存储（`:222-230`）；没有误报/漏报后的人工升级路径、紧急资源呈现、非诊断声明、未成年人/高风险用户排除规则、保留期限或可验证删除机制。
- 缺口：对可能处于危机中的用户，模型预测与自动干预的失败后果未被限制；“先健康管理、后认证”的路径也没有把医疗建议与健康提示的输出边界落到产品行为。
- 最小补齐动作：为首个 MVP 增加安全协议：只提供非诊断的自我调节提示；定义危机关键词/高风险信号时的本地紧急资源和人工支持提示；明确不自动诊断、不替代专业治疗；规定目标地区、最小采集字段、保留期、导出/删除测试和人工审查责任人。
- 验收条件：用包含高风险、误报和普通情绪三类脚本的测试集演练，所有高风险路径在规定时间内展示正确地区的紧急资源且不输出诊断；隐私测试能证明账户删除后原始 EEG 与派生画像均不可检索。

## 后续处置

优先修复重复编号，再决定 TokenWeave/SolScale 的边界；EmoSoul 在有可审计安全协议前不应把危机预警或临床效果作为 MVP 成功主张。tracker 路径解析问题仍需由维护者提供正确映射后再复核。
