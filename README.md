# Awesome AI Ideas

<div align="center">

[![Awesome](https://awesome.re/badge.svg)](https://awesome.re)
[![Tracked Ideas](https://img.shields.io/badge/tracked%20ideas-60-111827)](docs/roadmap.md)
[![Proposals](https://img.shields.io/badge/proposals-10-0f766e)](prs/)
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
- [weekly-review-2026-W26.md](docs/weekly-review-2026-W26.md) - 最新周报、自动化信号和下一步重点。
- [docs/automation/](docs/automation/) - repo pulse、quality snapshot、PR snapshot 和协作记录。
- [docs/automation-runbook.md](docs/automation-runbook.md) - Windows 自动化、GitHub wrapper 和常见故障处理。

## 当前快照

更新时间：2026-06-29。

- 结构化追踪想法：**60** 个。
- issue idea 文件：**27** 个。
- proposal 草稿：**10** 个。
- 文档与研究文件：**222** 个。
- 自动化报告：**108** 个。
- GitHub open PR：**2** 个。

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
- **路线图与复盘**：[docs/roadmap.md](docs/roadmap.md)、[weekly-review-2026-W26.md](docs/weekly-review-2026-W26.md)
- **自动化运营**：[docs/automation/](docs/automation/)
- **运行手册**：[docs/automation-runbook.md](docs/automation-runbook.md)
- **结构化追踪**：[idea-tracker.json](idea-tracker.json)

## 仓库结构

```text
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
```

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
