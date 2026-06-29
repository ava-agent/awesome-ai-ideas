# 💡 [for Enterprise CX & ITSM] Agent EvalOps - From Demo-Only to AI-Powered Agent Evaluation & ROI Platform

## Issue #1464

---

## 🎯 问题

**痛点背景：**
- 78% 企业预计18个月内让 agent 处理客服，但真正全组织落地的只有16%
- 管理层想要 ROI，团队只能展示几个成功 demo
- 离线评测、灰度流量、线上指标之间没有统一闭环
- 多 agent / 多框架并存时，根本不知道是模型、流程、知识库还是工具调用出了问题

**具体问题：**
- 离线分数与线上 CSAT/containment 相关性低
- 回归事故发现时间长
- 一次灰度周期长
- 缺少 failure taxonomy 指导改进

---

## 🤖 功能

**核心功能：**
- 从历史工单、SOP、聊天记录自动生成 eval 套件
- 支持 shadow mode、回放、回滚
- 成本/满意度/升级率对比
- ROI 面板给业务负责人看
- failure taxonomy 给工程团队看

**特色功能：**
- Zendesk / Intercom / 飞书服务台适配器
- 离线评测 → 灰度 → 线上的完整闭环
- 多框架评测对比 (51个框架中位任务解决率只有32%)
- 可解释的 failure 归因

---

## 🏗️ 方案

**技术架构：**
- 数据层：工单历史、聊天记录、知识库、SOP
- 评测层：自动生成 eval 套件、shadow mode 运行、指标计算
- 分析层：failure taxonomy、归因分析、ROI 计算
- 集成层：Zendesk/Intercom/飞书服务台/主流 agent 框架

**实现路线：**
- MVP：Zendesk 适配器 + 自动生成 eval 套件 + 基础指标
- V1：shadow mode + 回滚 + failure taxonomy
- V2：多框架对比 + 完整 ROI 面板

**技术栈：**
- Python/Node.js backend
- React dashboard
- 集成 OpenAI/Anthropic API 做评测
- 支持主流 agent 框架 (LangChain, AutoGPT, 等)

---

*生成时间：2026-06-30*
