# 💡 [for Hardware Engineers & Chip Designers] HORIZON AI - From Manual Hardware Design to AI-Powered Repository-Level Chip Evolution Ecosystem

## Issue #1466

---

## 🎯 问题

**痛点背景：**
- 硬件设计（芯片、FPGA、ASIC）周期漫长，通常需要数月甚至数年
- 设计迭代依赖人工经验，重复工作多，自动化程度低
- 验证成本高，覆盖率难以保证，错误发现晚导致代价高昂
- 最新的 arXiv 论文（HORIZON）展示了 Agentic AI 在硬件设计领域的巨大潜力

**具体问题：**
- 硬件描述语言（Verilog/VHDL）编写和调试效率低
- 缺乏智能的设计空间探索和优化工具
- 验证用例生成和覆盖率分析需要大量人工
- 设计知识难以复用和传承，新手上手慢
- 跨设计项目的最佳实践传播困难

---

## 🤖 功能

**核心功能：**
- 基于 HORIZON 论文的仓库级硬件设计自进化框架
- Markdown 需求编译为项目包（领域知识、评估器、验收谓词、Git 策略）
- 免手动 Agent 循环，通过仓库操作进行状态管理、追踪和回放
- 支持 ChipBench、RTLLM、Verilog-Eval 等标准硬件设计基准测试
- 完整的硬件设计 AI 辅助工作台

**特色功能：**
- 需求驱动的硬件设计生成（自然语言 → Verilog）
- 智能设计空间探索和自动优化
- 形式化验证和覆盖率分析自动化
- 设计知识库和最佳实践推荐引擎
- 多模态设计评审（原理图、仿真波形、功耗分析）
- 人类专家反馈闭环和持续学习

---

## 🏗️ 方案

**技术架构：**
- 模型层：LLM 代码生成 + 硬件设计专用适配器
- 处理层：需求编译、评估执行、验收谓词判断、Git 策略
- 应用层：Agent 循环引擎、设计工作台、知识库管理
- 集成层：EDA 工具集成、Git 仓库、CI/CD 管道

**实现路线：**
- MVP：基础需求编译 + 单模块设计生成 + 标准基准测试支持
- V1：设计空间探索 + 形式化验证集成 + 知识库构建
- V2：多模块协同设计 + 专家反馈闭环 + 企业级部署方案

**技术栈：**
- Python backend (FastAPI)
- 硬件设计工具集成（Verilator、Yosys、OpenLANE）
- Git 操作自动化
- React 设计工作台
- 向量数据库用于设计知识检索

---

*生成时间：2026-06-30*
*基于 arXiv:2606.28279 - "Agentic Hardware Design as Repository-Level Code Evolution"*
