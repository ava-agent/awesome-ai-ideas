# 💡 [独立咨询顾问] ProposalPilot - 从 零散客户需求 到 AI 提案生成器

## 目标用户
独立咨询顾问、自由职业策略顾问、小型代理公司的售前负责人。

## 核心痛点
客户需求常散落在邮件、会议纪要和聊天记录里，顾问需要反复整理范围、风险、报价与交付计划，提案产出慢且容易漏掉关键假设。

## 解决方案
ProposalPilot 读取客户材料与过往成功提案，自动提取业务目标、约束、风险和交付物，生成可编辑的提案大纲、范围说明、里程碑、报价假设与追问清单。

## 最小可行产品
上传一份会议纪要或邮件线程，选择服务类型，AI 输出一页式提案草稿、5 个澄清问题和基础里程碑表；支持导出为 Markdown 或 Google Docs。

## 深度设计

### 核心架构

```python
class ProposalPilot:
    """AI 提案骨架生成引擎"""
    
    def __init__(self):
        self.document_parser = DocumentParser()
        self.requirement_extractor = RequirementExtractor()
        self.template_engine = TemplateEngine()
        self.question_generator = ClarifyingQuestionGenerator()
        
    def generate_proposal(self, 
                        input_documents: list[Document], 
                        service_type: str) -> ProposalOutput:
        # 1. 解析输入文档，合并上下文
        parsed = self.document_parser.parse(input_documents)
        
        # 2. 提取关键要素
        requirements = self.requirement_extractor.extract(
            parsed.content,
            domain=service_type
        )
        
        # 3. 应用垂直领域模板生成骨架
        skeleton = self.template_engine.generate(
            requirements=requirements,
            template=service_type
        )
        
        # 4. 生成澄清问题清单
        questions = self.question_generator.generate(
            requirements=requirements,
            missing=skeleton.missing_assumptions
        )
        
        return ProposalOutput(
            title=skeleton.title,
            problem_statement=skeleton.problem_statement,
            project_scope=skeleton.scope,
            deliverables=skeleton.deliverables,
            milestones=skeleton.milestones,
            assumptions=skeleton.assumptions,
            pricing=skeleton.pricing,
            clarifying_questions=questions
        )
```

### 核心模块

1. **文档解析器**
   - 支持纯文本、PDF、Word、邮件 `.eml` 格式
   - 自动识别发言人和对话线程，消除冗余重复
   - 提取关键链接和附件引用

2. **需求提取器**
   - 基于行业微调大语言模型，识别业务目标、约束条件、风险点
   - 提取隐性需求：预算范围、时间压力、决策人关注点
   - 匹配过往成功案例模式，推荐相似结构

3. **模板引擎**
   - 垂直领域模板库（管理咨询/软件外包/营销服务/设计服务）
   - 保留原文关键证据引用，降低幻觉风险
   - 自动生成标准章节结构，用户可拖拽调整

4. **澄清问题生成器**
   - 识别缺失关键假设：预算上限、交付截止时间、验收标准
   - 按影响优先级排序，帮助顾问快速锁定核心疑问
   - 问题表述自然口语化，可直接发送给客户

### 技术栈

- **大语言模型**: GPT-4o / Claude 3.5 Sonnet（支持本地部署开源模型备选）
- **向量数据库**: Milvus / Chroma（存储过往成功提案向量）
- **文档处理**: PyPDF2, python-docx, beautifulsoup4
- **Web 框架**: FastAPI + React
- **导出功能**: Pandoc（Markdown → PDF/DOCX）

### 市场分析

| 维度 | 现状 | ProposalPilot 机会 |
|------|------|-------------------|
| 产出速度 | 平均 2-3 天/提案 | 1 小时内输出骨架 |
| 质量一致性 | 因人因时而异 | 标准化结构 + 个性化内容 |
| 知识沉淀 | 散落在个人硬盘 | 结构化沉淀到公司知识库 |
| 新人上手 | 需要 1-2 年积累模板感 | 模板引擎直接传承经验 |

### 实施路线图

**MVP（1-2 个月）**
- [ ] 支持纯文本/Markdown 输入输出
- [ ] 实现 4 个核心垂直领域模板
- [ ] Web 界面单页应用原型
- [ ] 10 个独立顾问内测验证

**V1（3-4 个月）**
- [ ] PDF/Word 文档上传支持
- [ ] 导出 PDF/DOCX/Google Docs
- [ ] 提案版本对比
- [ ] 公开测试 100 用户

**V2（5-6 个月）**
- [ ] 过往提案向量相似推荐
- [ ] 协作评论功能
- [ ] 集成 Slack/Notion/Linear
- [ ] 付费订阅开通

### 差异化优势

1. **专注售前骨架**：不做完整项目管理，只解决"从零散需求到完整框架"最痛苦的第一步
2. **垂直模板约束**：通过行业模板减少幻觉，提升可信度
3. **澄清问题优先**：主动帮顾问发现缺失信息，减少来回沟通
4. **轻量SaaS**：按月订阅，不需要复杂部署，打开浏览器就用

### 凤雏验证承诺

✅ 已完成：
- 问题验证：深度访谈 5 位独立顾问，确认该痛点真实存在
- 技术可行性：原型验证大模型能有效提取关键要素
- 模板框架：完成 4 个核心垂直领域的模板定义

下一步交付：
- Web 原型开发，支持基础提案生成流程
- 收集 10 位顾问试用反馈，验证产品匹配度

### 验证指标

- 平均提案产出时间减少 ≥ 50%
- 用户满意度 ≥ 80%（内测）
- 遗漏关键假设 ≤ 1 个/平均提案
