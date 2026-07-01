# Idea 质量巡检缺口报告 - 2026-07-01

## 巡检范围

- 已读规则：`docs/automation-runbook.md`、`AGENTS.md`
- 已读目录/索引：`ideas/`、`prs/`、`p/`、`idea-tracker.json`
- 抽查策略：优先抽查最近修改条目、`idea-tracker.json` 中最高优先级/高分条目，以及 `p/` 下 PR 草稿样本。
- 本次不改动任何 idea/proposal 正文。

## 总体判断

最近新增的 issue idea 普遍具备“目标用户 + 痛点 + 功能 + 技术方案”骨架，但质量不均衡。最常见缺口不是“没有想法”，而是缺少能指导下一步行动的商业和验证约束：

- 替代方案/竞品对照不足，容易把趋势热点误判成产品机会。
- MVP 范围偏大，很多条目直接跳到生态系统/平台，没有 2-4 周可验证切口。
- 验证计划多停留在指标名，没有明确样本、访谈对象、成功阈值和失败判据。
- 医疗、合规、安全、金融、硬件等高风险方向缺少合规边界和责任边界。
- 重复主题未合并，导致同一方向分散在多个 issue/proposal 中。
- `p/` 下存在中文内容编码损坏样本，降低后续评审和自动化分析可靠性。

## P0 - 必须优先补齐

### 1. Healthcare Admin Precision Copilot 重复且缺合规落地边界

- 文件：
  - `ideas/issue-1460--for-Care-Coordinators-Medical-Scribes-Healthcare-Admin-Precision-Copilot--From-Manual-Administrative-Drudge-to-AI-Powered-Clinical-Administrative-Workflow-Ecosystem.md`
  - `ideas/issue-1455--for-Care-Coordinators-Scribes-Prior-Auth-Teams-Healthcare-Admin-Precision-Copilot--From-Manual-Administrative-Drudge-to-AI-Powered-Clinical-Administrative-Workflow-Ecosystem.md`
- 缺口：两个条目高度重合。目标用户和真实痛点较清楚，但缺少 HIPAA/PHI、EHR 集成权限、payer 规则来源、人工复核责任、错误提交责任边界。替代方案未列明，如现有 prior auth 工具、EHR 内置模块、RCM/BPO 服务。
- 最小改进：合并为一个主条目，新增“合规与责任边界”小节：只做提交前 checklist 和字段缺失检测，不自动提交；列出 3 个替代方案；MVP 限定为 1 个专科、2 个 payer、20 份历史 prior auth 包回放，成功阈值为人工补字段时间下降 30% 且首次提交缺项率下降 20%。

### 2. UnlimitedOCR Pro 重复且产品切口不清

- 文件：
  - `ideas/issue-1456--for-Content-Creators-Researchers-Enterprises-UnlimitedOCR-Pro--From-Generic-OCR-Limitations-to-AI-Powered-Unlimited-Document-Intelligence-Ecosystem.md`
  - `ideas/issue-1452--for-Developers-Product-Teams-Enterprises-UnlimitedOCR-Pro--From-Generic-OCR-Limitations-to-AI-Powered-Unlimited-Document-Intelligence-Ecosystem.md`
- 缺口：同名方向重复。`1452` 有 MVP 和商业模式，`1456` 更像论文摘要。缺少与 MinerU、PaddleOCR、Azure/AWS/GCP Document AI、开源 OCR pipeline 的替代方案对照。技术约束也不足，包括 GPU 成本、长文档评测集、隐私隔离、表格/公式准确率指标。
- 最小改进：保留 `1452` 作为主版本，把 `1456` 作为论文来源补充；新增 1 页竞品矩阵；MVP 限定为“长 PDF 批量转 Markdown + 表格保真评测”，用 50 份真实长文档测试，指标为页级准确率、表格结构 F1、每 100 页推理成本和处理时延。

### 3. p/pr-1397 CashFlow Copilot 内容编码损坏，无法可靠审查

- 文件：`p/pr-1397/prs/1266-CashFlow-Copilot.md`
- 缺口：正文中文出现明显 mojibake，目标用户、痛点、合规风险和商业化路径虽然可能存在，但当前文件不可可靠阅读和自动化抽取。金融/税务方向本身还需要更严格的隐私、税务建议免责声明和数据授权边界。
- 最小改进：先从原始来源或 Git 历史恢复 UTF-8 正文；恢复后补充“非持牌税务/投资建议边界”“银行/支付平台数据授权方式”“本地加密和删除策略”。MVP 只做现金流预测与发票/税务提醒，不给投资或税务结论。

## P1 - 高价值条目需要补齐验证和约束

### 4. OpenClaw Pro 范围过大，替代方案不充分

- 文件：`ideas/issue-1467--for-Developers-Power-Users-OpenClaw-Pro--From-Basic-AI-Assistants-to-Agentic-Workflow-Automation-Ecosystem.md`
- 缺口：目标用户和痛点明确，但直接定位“Agentic Workflow Automation Ecosystem”，MVP 仍偏宽。缺少与 n8n、Zapier、Dify、LangGraph、OpenHands、Claude Code/Codex 工作流的替代方案对照，也缺少权限安全、失败恢复和用户数据隔离约束。
- 最小改进：MVP 收缩为“本地 repo 自动化 runbook 执行器”，只支持 3 类任务：读 runbook、生成计划、执行带审批命令。验证 10 个真实仓库任务，指标为人工步骤减少、失败可恢复率、越权命令拦截率。

### 5. Agent EvalOps 需要明确买方和验证样本

- 文件：`ideas/issue-1464--for-Enterprise-CX-ITSM-Agent-EvalOps--From-Demo-Only-to-AI-Powered-Agent-Evaluation-ROI-Platform.md`
- 缺口：痛点强，方向质量较高，但买方画像仍泛化在 CX/ITSM。缺少替代方案，如 LangSmith/evals、Humanloop、Galileo、客服平台内置 analytics、人工 QA 团队。验证计划未说明需要多少历史工单、如何处理 PII、如何证明离线 eval 与线上指标相关。
- 最小改进：限定首个 ICP 为“100-1000 人客服团队、已上线 agent 但 containment 不稳定”。MVP 只做 Zendesk 历史工单 eval 生成 + shadow replay；用 500 条脱敏工单验证，目标是找出前 5 类失败原因并让人工 QA 时间下降 30%。

### 6. Agent Security ReviewOps 需要威胁模型和责任分层

- 文件：`ideas/issue-1459--for-Agent-Developers-Small-Teams-Agent-Security-ReviewOps--From-Agent-Runtime-Chaos-to-AI-Powered-Agent-Security-Governance-Ecosystem.md`
- 缺口：痛点聚焦，但内容较短。缺少明确替代方案，如 promptfoo、Lakera、Lasso、Protect AI、LangSmith tracing、云厂商 guardrails。缺少 threat model、默认策略、误报处理和对高权限工具的技术约束。
- 最小改进：新增 STRIDE/agent runtime 威胁表；MVP 限定为“工具调用审计 + secret scan + prompt injection replay”；验证 5 个开源 agent 项目，指标为高危权限配置发现数、误报率、阻断危险命令的覆盖率。

### 7. HORIZON AI 技术深但商业落点不足

- 文件：`ideas/issue-1466--for-Hardware-Engineers-Chip-Designers-HORIZON-AI--From-Manual-Hardware-Design-to-AI-Powered-Repository-Level-Chip-Evolution-Ecosystem.md`
- 缺口：技术来源和硬件痛点清楚，但缺少商业化路径、采购方、EDA 生态替代方案和 IP/许可风险。MVP 仍包含需求编译、设计生成、标准基准、工作台，范围偏大。
- 最小改进：首个 MVP 改成“Verilog 小模块生成 + Verilator/Yosys 自动验收 + benchmark replay”。明确不碰 proprietary PDK；列出与 Synopsys/Cadence/Siemens EDA、GitHub Copilot、开源 HDL 工具链的差异。

### 8. ComplySecure AI 风险边界和 ICP 过宽

- 文件：`ideas/issue-1441--for-Compliance-Officers-Security-Teams-Data-Analysts-ComplySecure-AI---From-manual-compliance-and-security-burden-to-AI-powered-automated-governance-ecosystem.md`
- 缺口：内容完整，有商业模式和竞品，但把合规、安全、数据审计、威胁响应同时纳入，MVP 仍过宽。合规误判、审计证据链、数据跨境、法律责任边界需要更明确。
- 最小改进：MVP 收缩为“单一合规框架证据收集与差距检查”，例如 SOC 2 或 PIPL 数据资产盘点。验证 3 家小型 SaaS 的真实审计资料，输出证据缺口清单，不自动给法律结论。

### 9. DocAI Studio 高分但需要更严的差异化和隐私约束

- 文件：`prs/1444-docai-studio.md`
- 缺口：内容非常完整，但平台愿景较大。核心风险是与现有文档 AI、知识库、OCR 和研究工具重叠。医疗/法律/企业文档场景会引入隐私、数据保留和模型训练边界。
- 最小改进：新增“为何不是 NotebookLM/Zotero/Notion/MinerU/PaddleOCR 组合”的替代方案段落；MVP 只选研究者 PDF 文献库，验证 20 位研究者完成文献提取任务的时间节省，并默认关闭用户文档训练。

## P2 - 可在下轮维护中补齐

### 10. issue-1445 hot autonomous coding/self-hosting 需要从热点摘要转成具体产品假设

- 文件：`ideas/issue-1445-hot-AI-driven-autonomous-coding-and-self-hosting.md`
- 缺口：目标用户和痛点较泛，替代方案、MVP、商业化路径都不足。与 OpenClaw Pro、AI Workspace Orchestrator、现有 DevOps/自托管面板存在重叠。
- 最小改进：拆成一个具体场景，例如“把 Docker Compose 服务安全迁移到个人 VPS”。列出 Coolify、Dokploy、CapRover、Portainer、GitHub Actions 的替代方案；MVP 只支持 5 个常见开源应用模板。

### 11. AgentHarness Pro 需要与 Agent Security ReviewOps/OpenClaw Pro 分工

- 文件：`ideas/issue-1441--for-Agent-Developers-Engineers-AgentHarness-Pro--From-agent-performance-friction-to-intelligent-agent-harness-optimization-ecosystem.md`
- 缺口：目标用户明确，但与 agent 安全、工作流自动化、性能监控多个方向重叠。缺少替代方案和验证计划。
- 最小改进：定位成“agent harness benchmark + regression dashboard”，不要同时做 security/memory/skills 全量优化。验证 3 个 agent CLI 在同一任务集上的成功率、耗时、token 成本。

### 12. p/ 下历史 PR 草稿普遍偏技术方案，缺少 go-to-market 校验

- 样本：
  - `p/pr-1380/1087-OptiTranslate-Natural-Language-to-Optimization.md`
  - `p/pr-1381/1088-Self-Supervised-Search-Agents.md`
  - `p/pr-1382/1089-Smart-EV-Fleet-Management.md`
  - `p/pr-1383/1090-AI-Powered-Privacy-Auditing.md`
- 缺口：这些草稿技术架构和痛点描述很充分，但普遍缺少最小销售路径、真实首批用户、替代采购方案和失败判据。
- 最小改进：每个 PR 草稿补一个 8 行“验证卡”：ICP、替代方案、单句价值主张、MVP 输入/输出、首批 10 个访谈对象、成功阈值、合规红线、放弃条件。

## 建议的下轮补齐顺序

1. 先处理 P0：合并重复 Healthcare Admin、合并 UnlimitedOCR、恢复 CashFlow Copilot 编码。
2. 再处理 P1 中最可能转化为产品的三项：Agent EvalOps、Agent Security ReviewOps、DocAI Studio。
3. 最后对 `p/` 历史草稿批量加“验证卡”，用统一模板提升自动化可评估性。

## 建议模板

后续每个 idea/proposal 至少补齐以下字段：

```markdown
## 质量补齐卡

- ICP：
- 高频真实痛点：
- 当前替代方案：
- 为什么现在：
- MVP 范围：
- 非目标范围：
- 2 周验证计划：
- 成功阈值：
- 技术约束：
- 合规/隐私/责任边界：
- 商业化路径：
- 放弃条件：
```
