# AI 代码库知识地图生成器

> 自动分析代码库，生成交互式知识地图，让新成员快速理解架构

## 功能设计

### 核心功能
- **架构可视化** - 自动识别核心模块、依赖关系、调用链路，生成 Mermaid/Graphviz 图
- **关键节点标注** - 标记入口文件、配置中心、核心业务逻辑、高频修改区域
- **问答式探索** - "这个模块做什么？" "数据流怎么走？" 直接向地图提问
- **版本对比** - PR 合并后自动更新地图，高亮变更影响范围

### 辅助功能
- 支持多语言（通过 Tree-sitter）
- GitHub Actions 集成，push 触发更新
- 导出为 PNG/SVG/PDF

## 技术方案

### 数据层
```
代码仓库 → Git Clone
    ↓
AST 解析器 (Tree-sitter)
    ↓
依赖图提取 (imports/exports 分析)
    ↓
图数据库 (Neo4j / 内存图)
```

### 逻辑层
```
graph-service/
├── parser.ts        # AST 解析，提取节点
├── analyzer.ts      # 依赖分析，构建图
├── ranker.ts        # PageRank 找核心节点
└── diff.ts          # 版本对比，增量更新

ai-service/
├── embedder.ts      # 代码片段向量化
├── qna.ts           # 问答接口 (RAG)
└── summarizer.ts    # 模块摘要生成
```

### 展示层
```
Web 前端 (React + D3.js / Cytoscape.js)
├── 交互式图谱视图
├── 节点详情面板
├── 问答对话框
└── 版本对比视图
```

## 实现步骤

### Phase 1: MVP (2-3 周)
1. 实现单语言支持（JS/TS）
2. 基础依赖图生成（import 语句解析）
3. 简单 Web UI 展示图谱
4. GitHub Action 触发更新

### Phase 2: 智能化 (2 周)
1. 代码向量化 + 相似度检索
2. 模块自动摘要生成
3. PageRank 识别核心节点
4. 问答功能集成

### Phase 3: 增强功能 (2 周)
1. 多语言支持（Python, Go, Java, Rust）
2. 版本对比功能
3. 导出功能（PNG/SVG/PDF）
4. 团队协作功能（评论、标注）

## 资源需求

### API & 服务
- **LLM API** - OpenAI / Claude / GLM（摘要生成、问答）
- **向量数据库** - Pinecone / Milvus / Chroma（可选，小项目可用内存）
- **图数据库** - Neo4j（可选，小项目可用内存图）

### 开源依赖
- `tree-sitter` - 多语言 AST 解析
- `@babel/parser` - JS/TS 深度解析
- `cytoscape.js` 或 `react-force-graph` - 图可视化
- `langchain` - RAG 问答链

### 部署
- GitHub App 或 GitHub Action
- 可选：Vercel / Cloudflare Pages 托管前端

## 风险与缓解

| 风险 | 缓解措施 |
|------|----------|
| 大型仓库解析性能 | 增量更新 + 懒加载 |
| Token 消耗大 | 只向量化关键节点 |
| 企业代码隐私 | 支持自托管 + 私有 LLM |

## 变现建议

- **开源版** - 公开仓库免费使用，建立社区
- **Pro 版** - 私有仓库支持，$9.9/月
- **Team 版** - 团队协作功能，$29/月/团队
- **Enterprise** - 自托管 + SSO + SLA，定制报价

## 参考 Issue

Closes #15

---

**Created by:** AI Ideas Bot
**Date:** 2026-03-22
