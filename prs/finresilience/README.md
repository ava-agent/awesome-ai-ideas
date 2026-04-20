# FinResilience AI 💰🛡️

> AI驱动的财务韧性平台 — 为面临经济困难的人群提供个性化危机规划、债务管理、资源匹配和教育支持。

## 🌟 项目愿景

帮助每个人从财务危机中恢复并获得长期稳定，无论其收入水平或财务知识如何。

## 🏗️ 架构概览

```
backend/
├── app.py                      # FastAPI 主入口
├── requirements.txt
├── database/                   # 数据层 (SQLAlchemy + PostgreSQL)
├── crisis_analyzer/            # 智能危机分析器
├── debt_optimizer/             # 债务优化引擎
├── resource_matcher/           # 资源智能匹配
├── financial_education/        # 个性化财务教育
└── emotional_support/          # 情感支持系统
```

## 🔑 核心模块

### 1. 智能危机分析器 (Crisis Analyzer)
- 输入用户财务状况（收入、支出、资产、负债）
- AI 分析紧急程度（低/中/高/危机）
- 生成 3/6/9 个月个性化行动计划
- 风险预警与趋势分析

### 2. 债务优化引擎 (Debt Optimizer)
- 多维度债务结构分析
- 雪崩法 vs 雪球法策略推荐
- 自动生成债权人谈判模板
- 还款时间线模拟与优化

### 3. 资源智能匹配 (Resource Matcher)
- 整合政府、非营利、社区资源数据库
- 基于地理位置、收入、家庭状况精准匹配
- 申请流程指引与材料清单
- 资源使用状态跟踪

### 4. 个性化财务教育 (Financial Education)
- 自适应知识水平评估
- 模块化学习路径（基础→进阶→高级）
- 日常语言解释复杂金融概念
- 互动式学习与测验

### 5. 情感支持系统 (Emotional Support)
- 压力水平评估与跟踪
- 认知行为疗法(CBT)练习
- 冥想与呼吸练习引导
- 支持群体匹配与社区连接

## 🚀 快速开始

```bash
# 安装依赖
pip install -r backend/requirements.txt

# 配置环境变量
cp .env.example .env

# 启动服务
uvicorn backend.app:app --reload --port 8000
```

## 📡 API 文档

启动服务后访问：
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 🛡️ 安全与隐私

- 所有财务数据端到端加密
- GDPR 合规设计
- 用户数据本地化存储选项
- 定期安全审计

## 📄 许可证

MIT License
