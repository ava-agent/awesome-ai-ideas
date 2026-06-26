# TherapyFlow AI - 心理治疗工作流优化与来访者洞察增强生态

> 解决治疗师文档 burnout 和治疗计划复杂性痛点，通过 AI 驱动提升临床工作流效率，增强来访者长期洞察。

## 用户

- **核心用户**：心理健康从业者、心理咨询师、临床心理学家、治疗师
- **场景**：私人执业、中小诊所、心理健康机构

## 痛点

1. **文档负担过重**：每次 session 后需要花费 1-2 小时撰写 SOAP 格式临床笔记，挤占实际咨询时间
2. **治疗计划复杂度高**：跨疗程进度追踪、主题演变分析、效果量化全靠手动，难以发现长期趋势
3. **危机识别滞后**：自伤、自杀等风险信号分散在多疗程对话中，容易遗漏
4. **继续教育零散**：缺乏个性化的临床技能提升建议，与实际案例脱节

## 方案

**AI 驱动的治疗工作流辅助平台**，核心能力分层落地：

### MVP 阶段：AI 辅助 Session Note 生成

```python
class TherapyNoteEngine:
    def __init__(self):
        self.asr = WhisperMedical()           # 医疗领域微调语音识别
        self.context_analyzer = TherapyNLP()  # 治疗对话上下文理解
        self.note_formatter = SOAPGenerator() # SOAP格式报告生成
        
    def generate_session_note(self, audio_recording, session_context):
        # 1. 医疗级语音转文字（支持方言+低音量+说话人分离）
        transcript = self.asr.transcribe(
            audio_recording,
            domain='mental_health',
            speaker_diarization=True
        )
        
        # 2. 治疗对话语义分析（识别主题、情绪变化、风险信号）
        analysis = self.context_analyzer.analyze(
            transcript=transcript,
            therapy_type=session_context.therapy_type,  # CBT/DBT/精神分析等
            session_number=session_context.session_count,
            treatment_goals=session_context.goals
        )
        
        # 3. 生成结构化SOAP Note（治疗师审核后保存）
        soap_note = self.note_formatter.generate(
            subjective=analysis.client_reported,
            objective=analysis.therapist_observed,
            assessment=analysis.clinical_assessment,
            plan=analysis.treatment_recommendations
        )
        
        return {
            'transcript': transcript,
            'soap_note': soap_note,
            'risk_alerts': analysis.crisis_flags,  # 🔴 自杀/自伤/危机信号高亮
            'progress_indicators': analysis.session_progress,
            'themes': analysis.emerging_themes,
            'confidence_score': analysis.overall_confidence
        }
```

### 产品进化路径：

1. **阶段一**：核心笔记生成 + 实时危机预警
2. **阶段二**：跨疗程进度纵向分析 — 识别情绪轨迹、主题演变、治疗效果量化
3. **阶段三**：个性化继续教育推荐 + EHR 系统集成插件

### 差异化关键

| 维度 | 竞品现状 | TherapyFlow AI 优势 |
|------|---------|-------------------|
| Note 生成 | 通用模板 | 流派特定的 AI 生成（CBT/DBT/精神分析适配） |
| 进度追踪 | 手动量表 | AI 自动识别变化趋势 |
| 危机预警 | 无 | 实时风险信号检测 |
| 继续教育 | 外部资源 | 内嵌个性化学习推荐 |

## 技术关键与解决方案

### 1. 幻觉控制（临床场景核心要求）

- 基于 DSM-5/ICD-11 术语库做 constrained generation，严格限制生成范围
- 所有 AI 输出必须标注置信度，治疗师**强制审核**后才能保存
- 建立临床专家盲评验证流程，目标准确率 >90%

### 2. HIPAA 合规与隐私

- 端到端加密 + 本地处理优先，敏感数据不上公共云
- 可选部署模式：on-premise / HIPAA 合规云（AWS GovCloud/Azure Healthcare）
- 支持数据去标识化用于模型训练，严格获得用户授权

### 3. 流派适配

- MVP 先支持 CBT（占美国心理治疗市场最大份额，结构化程度最高）
- 不同流派定制 prompt 工程和笔记模板
- 开放模板贡献机制，社区扩展支持更多流派

## 商业模式

### 定价策略：Freemium

- **基础版**：每月 10 次 session note 生成免费
- **专业版**：$29-$49/月/治疗师，无限生成 + 进度追踪 + 危机预警
- **机构版**：按 seat 订阅，提供团队管理 + 自定义集成

### 更好的 GTM 路径：

不要一开始做独立平台，优先与现有 EHR 厂商（TherapyNotes/SimplePractice）合作做插件，借渠道获客，验证 PMF 再考虑独立产品。

## 验证指标

- Session Note 生成准确率：>90%（临床专家盲评）
- 文档时间减少：>50%（从 2 小时/session → <1 小时）
- 危机信号识别召回率：>95%（零漏报是底线）
- 治疗师 7 日留存：>60%

## 市场分析

### 有利因素

- 疫情后心理健康需求激增，全美治疗师平均 waitlist 3 个月
- APA 2025 新指南明确鼓励使用 AI 辅助工具
- Telehealth 常态化使音频数据获取更容易

### 风险因素

- 各州 Licensing Board 对 AI 使用的政策不统一
- 治疗师群体对新技术接受度保守，平均采用周期 18-24 个月

## 交付物与边界

本次 PR 交付完整产品 proposal，包含：
- 用户画像与痛点定义
- 分层产品架构
- 核心技术方案与合规策略
- 验证指标与市场分析

不包含实现代码，仅完成 idea 固化和评审。

## 相关讨论

- GitHub Issue: [#1403](https://github.com/ava-agent/awesome-ai-ideas/issues/1403)
