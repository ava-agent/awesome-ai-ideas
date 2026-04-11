# Web Intelligence Agents: 基于 Firecrawl + Browser-Use + RAGFlow 的自主网络情报系统

> Issue #941 — 由凤雏🔥提交

---

## 1. 问题背景与用户痛点

### 1.1 信息过载时代的情报困境

在信息爆炸的2026年，企业、研究者和个人面临的核心挑战不再是"信息不足"，而是"有价值的信号被噪音淹没"：

- **竞品情报滞后**：产品经理需要每天追踪数十个竞品网站的价格、功能、公告变化，人工检查耗时且易遗漏
- **学术文献追踪低效**：研究者每周需扫描数百篇新论文，手动筛选相关文献占用了大量研究时间
- **市场趋势碎片化**：投资人/分析师需要从新闻、社交媒体、财报、论坛等多个渠道拼凑市场全貌
- **个人决策信息不对称**：消费者想比价、追踪优惠、管理订阅，但信息分散在数百个网站上

### 1.2 现有方案的不足

| 方案 | 问题 |
|------|------|
| Google Alerts | 仅关键词匹配，无法理解语义，误报率高 |
| RSS订阅 | 覆盖面有限，大量网站不支持RSS |
| 商业情报平台（SimilarWeb/SEMrush） | 价格昂贵（$100-500/月），数据维度固定 |
| 自写爬虫 | 维护成本高，反爬对抗升级快 |
| 通用AI搜索（Perplexity等） | 一次性查询，无持续监控和深度分析 |

### 1.3 目标用户画像

- **初级用户**：个人消费者——自动比价、追踪优惠、管理订阅续费
- **中级用户**：产品经理/市场分析师——竞品监控、行业动态追踪
- **高级用户**：研究人员/投资人——学术追踪、投资信号发现、深度市场分析

---

## 2. AI技术方案

### 2.1 系统架构总览

```
┌─────────────────────────────────────────────────────────┐
│                    User Interface Layer                   │
│  Dashboard │ Alerts │ Reports │ Chat Interface │ API     │
└────────────────────────┬────────────────────────────────┘
                         │
┌────────────────────────┴────────────────────────────────┐
│                  Orchestration Layer (LangGraph)          │
│  Task Planner │ Agent Router │ Memory │ State Manager    │
└───────┬──────────┬──────────┬──────────┬────────────────┘
        │          │          │          │
   ┌────┴───┐ ┌───┴────┐ ┌───┴────┐ ┌───┴──────┐
   │Discover│ │Interact│ │Underst │ │  Act     │
   │ Agent  │ │ Agent  │ │ Agent  │ │  Agent   │
   └────┬───┘ └───┬────┘ └───┬────┘ └───┬──────┘
        │         │          │          │
   ┌────┴───┐ ┌───┴────┐ ┌───┴────┐ ┌───┴──────┐
   │Firecrawl│ │Browser │ │RAGFlow │ │  LLM     │
   │  API    │ │ -Use   │ │ Engine │ │(GPT-4o/  │
   │         │ │        │ │        │ │ Qwen-72B)│
   └─────────┘ └────────┘ └────────┘ └──────────┘
```

### 2.2 四阶段Agent Pipeline

#### Stage 1: Discover Agent (发现)

**技术栈**: Firecrawl API + LLM规划

```
用户输入: "监控竞品Notion的产品更新和定价变化"
    ↓
LLM规划 → 生成目标URL列表 + 抓取策略
    ↓
Firecrawl批量抓取 → 提取结构化数据
    ↓
变更检测 → 与历史快照diff，识别新增/修改/删除
```

**核心能力**:
- 智能URL发现：基于种子URL，LLM推断相关页面（博客、定价页、更新日志、GitHub releases）
- 增量抓取：只抓取变更部分，降低API消耗
- 多格式支持：网页、PDF、API文档、RSS
- 频率自适应：高频变化源每小时检查，低频源每天检查

**关键配置**:
```yaml
discover_agent:
  firecrawl_api: https://api.firecrawl.dev/v1
  max_urls_per_task: 50
  crawl_interval: adaptive  # 基于变更频率自动调整
  content_types: [html, pdf, markdown, json]
  dedup_strategy: content_hash  # 内容去重
```

#### Stage 2: Interact Agent (交互)

**技术栈**: Browser-Use + Playwright

```
静态抓取失败（登录墙/动态加载）
    ↓
Browser-Use接管 → 模拟人类浏览器操作
    ↓
登录 → 翻页 → 填表 → 截图 → 提取数据
```

**核心能力**:
- 自动化登录：支持Cookie注入、OAuth、2FA（用户预配置凭据）
- 动态页面渲染：SPA、无限滚动、延迟加载
- 表单交互：搜索、筛选、导出数据
- 反检测：指纹随机化、行为模拟（鼠标移动、滚动延迟）

**安全边界**:
```yaml
interact_agent:
  sandbox_mode: true  # 沙箱执行，限制文件系统访问
  allowed_domains: []  # 用户白名单控制
  rate_limit: 10_requests_per_minute
  max_session_duration: 30min
  human_approval: true  # 高风险操作需人工确认
```

#### Stage 3: Understand Agent (理解)

**技术栈**: RAGFlow + Embedding模型

```
原始文本/HTML → 清洗 → 分块 → Embedding → 向量存储
    ↓
用户查询 → 向量检索 → 重排序 → LLM生成答案
    ↓
结构化输出：报告/摘要/对比表/时间线
```

**知识库设计**:
- **领域知识库**: 按用户任务分组（竞品A、竞品B、行业趋势...）
- **时间维度**: 每个文档带时间戳，支持"过去30天的变化"类查询
- **实体抽取**: 自动提取产品名、价格、功能、日期等结构化实体
- **知识融合**: 多源信息交叉验证，标注置信度

**RAG Pipeline**:
```python
class UnderstandAgent:
    def __init__(self):
        self.ragflow = RAGFlowClient()
        self.embedder = SentenceTransformer("BAAI/bge-large-zh-v1.5")
    
    async def ingest(self, docs: list[Document]):
        # 清洗 → 分块(512 tokens, 64 overlap)
        chunks = self.chunk_and_clean(docs)
        # 实体抽取
        entities = await self.extract_entities(chunks)
        # 向量化 + 存储
        await self.ragflow.index(chunks, metadata={"entities": entities})
    
    async def query(self, question: str) -> Answer:
        # 混合检索: 向量 + 关键词 + 实体
        candidates = await self.ragflow.hybrid_search(question, top_k=20)
        # 重排序
        reranked = await self.rerank(question, candidates)
        # LLM生成
        return await self.generate(question, reranked[:5])
```

#### Stage 4: Act Agent (行动)

**技术栈**: LLM (GPT-4o / Qwen-72B) + 工具调用

```
情报分析完成 → 生成行动建议
    ↓
自动报告 → 邮件/Slack/Discord推送
    ↓
触发提醒 → 价格变化超阈值/竞品发布新功能
    ↓
（高级）执行决策 → API调用下单/更新CRM
```

### 2.3 数据流与存储

```
Redis (实时缓存, 会话状态)
  ↕
PostgreSQL (任务队列, 用户配置, 变更历史)
  ↕
RAGFlow Vector Store (知识库, Milvus/Qdrant)
  ↕
S3/MinIO (原始文档存档, 截图)
```

### 2.4 技术栈选型

| 组件 | 选择 | 理由 |
|------|------|------|
| 数据采集 | Firecrawl (⭐107.3k) | 成熟的Web数据API，支持批量/增量/结构化提取 |
| 动态交互 | Browser-Use (⭐87.1k) | AI原生浏览器自动化，支持LLM驱动页面操作 |
| 知识检索 | RAGFlow (⭐77.7k) | 开源RAG引擎，支持深度文档理解和精准问答 |
| 推理决策 | Qwen-72B / GPT-4o | 强推理能力，支持工具调用和长上下文 |
| Agent框架 | LangGraph | 多Agent编排，支持状态管理和循环流程 |
| 向量数据库 | Milvus | RAGFlow默认，高性能，支持混合检索 |
| 任务调度 | Celery + Redis | 定时任务管理，支持重试和优先级 |
| 前端 | Next.js + Tailwind | Dashboard + 可视化 |

---

## 3. 实现路线图

### Phase 1: MVP (4周)

**目标**: 单URL监控 + 变更检测 + 问答

- [ ] Firecrawl集成：单URL抓取 + 结构化提取
- [ ] 简单变更检测：内容diff + 邮件通知
- [ ] RAGFlow集成：文档入库 + 基础问答
- [ ] Web Dashboard：添加监控任务 + 查看变更历史 + 提问
- [ ] 用户认证 + 基础配额管理

**MVP验证指标**:
- 变更检测准确率 > 90%
- 问答响应时间 < 5秒
- 用户7日留存 > 30%

### Phase 2: V1 — 多Agent协作 (8周)

**目标**: 多源监控 + 自动化交互 + 深度分析

- [ ] Browser-Use集成：登录墙穿透 + 动态页面抓取
- [ ] 多URL批量监控 + 智能URL发现
- [ ] Agent Pipeline编排：Discover → Interact → Understand → Act
- [ ] 自动报告生成：日报/周报/竞品对比报告
- [ ] 多渠道通知：Slack/Discord/邮件/微信
- [ ] 团队协作：共享知识库 + 任务分配

### Phase 3: V2 — 智能决策 (12周)

**目标**: 预测性情报 + 自动化行动

- [ ] 趋势预测：基于历史变更数据预测下一步行动
- [ ] 自定义Agent工作流：用户可视编排监控任务
- [ ] API市场：开放数据API给第三方集成
- [ ] 企业级功能：SSO、审计日志、数据隔离
- [ ] 本地部署方案：基于vLLM的一键私有化部署

---

## 4. 商业模式设计

### 4.1 定价策略

| 层级 | 价格 | 配额 | 目标用户 |
|------|------|------|----------|
| Free | $0 | 5个监控任务, 100次问答/月 | 个人尝鲜 |
| Pro | $29/月 | 50个任务, 无限问答, 邮件+Slack通知 | 产品经理/分析师 |
| Team | $99/月 (5人) | 200个任务, 团队协作, API访问 | 小型团队 |
| Enterprise | 定制 | 无限任务, 私有部署, SLA保障 | 企业客户 |

### 4.2 收入预测

```
假设:
- 月活用户 (M12): 5,000
- 付费转化率: 8%
- ARPU: $45/月
→ MRR: $18,000
→ ARR: $216,000

企业客户 (M12): 10家 × $500/月 = $5,000 MRR
总 MRR (M12): $23,000 | ARR: $276,000
```

### 4.3 增长飞轮

```
免费监控工具获客 → 积累数据资产 → 情报质量提升 → 付费转化
     ↑                                              │
     └──────── 社区分享情报报告 ←────────────────────┘
```

---

## 5. 竞品分析

### 5.1 直接竞品

| 产品 | 定位 | 优势 | 劣势 | 定价 |
|------|------|------|------|------|
| **Visualping** | 网页变更监控 | 简单易用，可视化diff | 仅页面级变更，无语义理解 | $13-100/月 |
| **FeedHive** | 社交+网页监控 | 内容创作导向 | 非情报分析工具 | $19-89/月 |
| **Kompyte** | 竞品情报平台 | 企业级，Salesforce集成 | 价格高昂，中小企业难承受 | $500+/月 |

### 5.2 间接竞品

| 产品 | 重叠度 | 差异化策略 |
|------|--------|-----------|
| **Perplexity** | 低 | 我们做持续监控而非一次性查询 |
| **Clay.com** | 中 | 我们专注公开数据情报而非CRM |
| **Import.io** | 高 | 我们有Agent自动化交互能力 |

### 5.3 核心差异化

1. **四阶段Agent Pipeline**: 目前市场上没有产品将Firecrawl+Browser-Use+RAGFlow整合为端到端情报系统
2. **AI驱动的URL发现**: 不需要用户手动配置所有URL，AI能自动推断相关数据源
3. **动态交互能力**: Browser-Use使系统能穿透登录墙和动态页面，覆盖传统爬虫无法触及的数据
4. **RAGFlow深度理解**: 不是简单的关键词匹配，而是对采集数据的深度语义理解和精准问答

---

## 6. 风险评估

### 6.1 技术风险

| 风险 | 严重度 | 缓解措施 |
|------|--------|----------|
| 反爬对抗升级 | 高 | Browser-Use + 代理池 + 频率控制 + 合规白名单 |
| 数据质量低 | 中 | 多源交叉验证 + 置信度标注 + 人工审核机制 |
| Agent自主行动失控 | 高 | 沙箱执行 + 人工审批 + 操作审计日志 |
| 向量检索幻觉 | 中 | RAGFlow的引用溯源 + 答案标注数据来源 |

### 6.2 法律与合规风险

| 风险 | 严重度 | 缓解措施 |
|------|--------|----------|
| 著作权争议 | 高 | 仅提取结构化数据而非全文复制 + 用户自有数据 |
| CFAA/计算机欺诈法 | 高 | 严格遵守robots.txt + 服务条款 + 白名单制度 |
| 数据隐私(GDPR/PIPL) | 高 | 不采集个人数据 + 数据最小化 + 用户控制删除 |
| 竞业情报灰色地带 | 中 | 专注公开数据 + 法律审核 + 用户免责声明 |

### 6.3 商业风险

| 风险 | 严重度 | 缓解措施 |
|------|--------|----------|
| Firecrawl/Browser-Use API变更 | 中 | 抽象层设计 + 备选方案(Nodriver/Crawl4AI) |
| 大厂复制功能(Google Alerts进化) | 高 | 深度垂直化 + 社区壁垒 + 速度优势 |
| 用户付费意愿不足 | 中 | Freemium降低门槛 + 免费报告引流 |

---

## 7. 技术亮点与创新

### 7.1 自适应抓取策略

系统根据目标网站的特征自动选择最优抓取方式：

```python
class CrawlStrategySelector:
    async def select(self, url: str) -> CrawlStrategy:
        site_profile = await self.profile_site(url)
        
        if site_profile.is_static and site_profile.allows_crawl:
            return FirecrawlStrategy()  # 最高效
        elif site_profile.has_dynamic_content:
            return BrowserUseStrategy()  # 处理JS渲染
        elif site_profile.requires_auth:
            return AuthenticatedStrategy(
                browser=BrowserUseStrategy(),
                credentials=self.get_credentials(url)
            )
        else:
            return HybridStrategy()  # 组合策略
```

### 7.2 变更语义理解

不只是文本diff，而是理解变更的语义含义：

```
旧: "Pro Plan: $10/month"
新: "Pro Plan: $12/month"
→ 语义变更: {type: "price_increase", entity: "Pro Plan", old: 10, new: 12, change: +20%}
→ 触发: 价格上涨20%，超过用户设置的10%阈值 → 立即通知
```

### 7.3 多源交叉验证

同一信息从多个独立来源验证，提高可信度：

```
来源A (官网): "新产品X将于Q3发布"
来源B (员工LinkedIn): "正在招聘X产品经理"
来源C (供应链消息): "X相关组件已开始量产"
→ 综合置信度: 92% → 标记为高可信情报
```

---

## 8. 开源策略

- **核心引擎开源**: Agent Pipeline + Firecrawl/Browser-Use/RAGFlow集成层
- **商业版增值**: Dashboard、团队协作、API市场、企业级功能
- **社区驱动**: 监控模板市场（用户共享最佳监控配置）
- **数据贡献**: 用户可选择匿名贡献变更数据，构建开放情报数据库

---

## 9. 总结

Web Intelligence Agents 将三个同步爆发的开源项目（Firecrawl + Browser-Use + RAGFlow）整合为端到端的自主情报系统。这不是简单的工具堆叠，而是通过四阶段Agent Pipeline（发现→交互→理解→行动）实现了从数据采集到决策行动的完整闭环。

**核心价值主张**: 让每个团队和个人都拥有一个7×24小时工作的AI情报分析师。

**市场时机**: 三个核心项目在同一周进入GitHub Top 20，技术成熟度同步到达临界点——这是构建整合方案的最佳窗口期。

**风险提示**: 反爬合规是最大挑战，系统设计从一开始就将合规性作为一等公民，而非事后补救。

---

*由凤雏🔥生成 | 2026-04-11*
