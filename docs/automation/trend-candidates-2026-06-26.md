# AI 趋势候选扫描 - 2026-06-26

## 范围与筛选口径

- 扫描窗口：以 2026-06-26 前 30 天内公开信号为主，必要时补充 2026 年内仍在持续放大的结构性趋势。
- 优先领域：AI agents、enterprise AI、healthcare AI、legal AI、developer tools、workflow automation、creative tools、China/global startup signals。
- 去重依据：已对照 `README.md`、`docs/roadmap.md`、`idea-tracker.json`。当前仓库已覆盖合同阅读、法律导航、医疗影像、基层医疗、代码错误诊断、工作流编排、创意剪辑等方向，本报告只保留“新切口”。

## 候选 1：Agent Security ReviewOps

### 来源依据

- 2026-06-02，研究显示中国独立 AI agent 开发者普遍重视用户侧安全，但对安全漏洞、权限治理和正式化 S&P 流程认知不足。  
  链接：https://arxiv.org/abs/2606.03190
- 2026-05-22，关于 OpenClaw 的风险研究指出，本地高权限 agent 在持久化存储、工具调用、跨上下文信息聚合、插件接入方面存在显著安全与可追踪性问题。  
  链接：https://arxiv.org/abs/2605.23330
- 2026-06-25，GLM-5.2 等开源中国模型因可下载、可改写、可去除护栏，被再次推高到“agent 能力增强 + 安全外溢”的讨论中心。  
  链接：https://www.axios.com/2026/06/25/china-glm-52-open-source-hackers

### 目标用户

- 使用开源 agent 框架、MCP、浏览器代理或本地高权限 agent 的独立开发者、小团队 CTO、自动化咨询顾问。

### 痛点

- 团队会做 demo，不会做权限边界。
- 上线前缺少“这个 agent 实际能读什么、写什么、发到哪里”的可验证视图。
- 出问题后缺少审计回放，难以向客户解释“数据是怎么泄露的”。

### 可能产品形态

- 面向 agent 的“runtime security + approval”中间层。
- 对接 OpenClaw / Manus 类工作流，做权限模板、密钥暴露扫描、prompt injection 回放、工具调用风控、外发审计日志。
- 提供“上线前安全体检”和“运行中策略托管”两种模式。

### 验证方式

- 找 8-10 个在做 agent 自动化的独立开发者或小团队访谈。
- 先做 2 个适配器：本地 agent 框架 + 一个浏览器代理/办公自动化场景。
- 验证指标：上线前发现的高危权限配置数、被拦截的危险动作数、客户安全答疑耗时是否下降。

### 与现有 idea 的差异或重复风险

- 与 `AI Workspace Orchestrator` 不同：不是编排 agent，而是给已存在的 agent 加治理层。
- 与 `AI代码安全审计员` 不同：不是扫代码漏洞，而是扫 agent 运行时权限、数据流和工具调用风险。
- 重复风险：中等，需避免做成泛安全扫描器，必须坚持“agent runtime governance”。

## 候选 2：Agent EvalOps for Enterprise Support

### 来源依据

- 2026-06-07，Nubank 论文给出生产级客服 agent 的评测驱动框架，并报告在卡片配送场景里，AI transactional NPS 提升 37 个百分点，自助解决率提升 29 个百分点。  
  链接：https://arxiv.org/abs/2606.08867
- 2026-06-04，ADK Arena 评测 51 个 agent 开发框架，发现没有单一框架统治全场，中位框架任务解决率只有 32%，框架选择和可用性差异极大。  
  链接：https://arxiv.org/abs/2606.05548
- 2026-06-26，Adobe 报告被媒体披露：78% 企业预计 18 个月内让 agent 处理客服，但真正全组织落地的只有 16%。  
  链接：https://m.economictimes.com/tech/artificial-intelligence/over-78-of-firms-expect-ai-agents-to-handle-customer-support-within-18-months-adobe-finds/articleshow/131999118.cms

### 目标用户

- 已经在客服、售后、内部服务台试点 AI agent 的中型企业运营负责人、CX 团队、ITSM 团队。

### 痛点

- 管理层想要 ROI，团队只能展示几个成功 demo。
- 离线评测、灰度流量、线上指标之间没有统一闭环。
- 多 agent / 多框架并存时，根本不知道是模型、流程、知识库还是工具调用出了问题。

### 可能产品形态

- 一个“agent 评测与上线闸门”平台，而不是另一个 agent builder。
- 从历史工单、SOP、聊天记录自动生成 eval 套件；支持 shadow mode、回放、回滚、成本/满意度/升级率对比。
- 输出给业务负责人看的 ROI 面板，输出给工程团队看的 failure taxonomy。

### 验证方式

- 找 2-3 个正在做客服/内部工单 agent 的团队试点。
- 先只接 Zendesk / Intercom / 飞书服务台其中一类场景。
- 验证指标：离线分数与线上 CSAT/containment 的相关性、回归事故发现时间、一次灰度周期长度。

### 与现有 idea 的差异或重复风险

- 与 `AI Workspace Orchestrator` 不同：不是执行工作流，而是给 agent 项目做“上线评测、监控、回滚、归因”。
- 与 `AI 错误信息诊断师` 不同：不是开发报错诊断，而是业务 agent 的运营质量诊断。
- 重复风险：中等偏高，必须把产品定义成“EvalOps/ROI 层”，不要退化成泛客服机器人后台。

## 候选 3：Healthcare Admin Precision Copilot

### 来源依据

- 2026-06-12 左右，Nvidia 与 Abridge 合作开发面向临床对话的专用模型，目标是把文书生成和临床决策支持嵌入实际医生工作流。  
  链接：https://www.wsj.com/cio-journal/nvidia-is-developing-an-ai-healthcare-model-with-startup-abridge-6db38c1b
- 2026-03-31，关于 prior authorization 的研究指出，LLM 生成的信件临床内容往往够强，但常缺失 billing code、授权时长、follow-up 等真正影响提交通过的行政脚手架。  
  链接：https://arxiv.org/abs/2603.29366
- 2026-03-18，对 34,726 次就诊记录的研究显示，ambient AI 草稿到医生最终文书之间仍有稳定且系统性的术语与结构修订。  
  链接：https://arxiv.org/abs/2603.18327

### 目标用户

- 专科诊所、医疗集团中的 care coordinator、medical scribe、prior auth 团队、医疗计费外包团队。

### 痛点

- 现在的临床 AI 更擅长“写得像”，但不一定“交得出去”。
- 医生和行政团队还要手工补齐 payer 要求、编码、回访安排和模板字段。
- 大厂方案多面向大型医院系统，专科诊所和轻量团队缺少更小、更窄、更快落地的产品。

### 可能产品形态

- 面向诊后行政流程的精度层：把就诊转录、EHR 摘要、 payer 规则拼成可提交的 prior auth / referral / appeal / follow-up 包。
- 内置字段级检查器、payer checklist、缺项提示、提交前 QA。
- 可先从“风湿/肿瘤/精神科”这类 prior auth 重的专科切入。

### 验证方式

- 访谈 5-8 个 prior auth 专员、诊所运营或医疗计费服务商。
- 拿匿名历史 case 做提交前后对比。
- 验证指标：人工补字段时间、首次提交通过率、平均周转天数、医生二次编辑比例。

### 与现有 idea 的差异或重复风险

- 不同于 `MedVision AI`：不做诊断影像辅助。
- 不同于 `RuralMed AI` / `AI家庭健康哨兵` / `AI护理助手`：不做患者陪伴或基层问诊，而是做医疗后台行政自动化。
- 重复风险：较低，关键是坚持“administrative precision”而非泛医疗助手。

## 候选 4：China Litigation Workflow Memory OS

### 来源依据

- 2026-06-17，LegalWorld 提出面向中国民事诉讼的全生命周期 legal agent 环境，覆盖咨询、起诉、庭审到后续阶段，强调跨阶段因果一致性和案件记忆。  
  链接：https://arxiv.org/abs/2606.18728
- 2026-06-03，Parthenon Law 指出法律 agent 真正难点不在单次问答，而在可审计的 matter-level 工作流、可追溯引用和基于结果的持续改进。  
  链接：https://arxiv.org/abs/2606.04602
- 2026-06-26，FT Law 50 继续把 Harvey、Clio 等 legal AI player 放在行业变革中心，说明法律组织正在从“单点工具”走向“流程级采用”。  
  链接：https://www.ft.com/content/2531e887-ecec-43a3-a03e-dc15c87694bb

### 目标用户

- 中国中小律所、法律援助机构、公司法务共享中心，尤其是处理高重复民商事案件的团队。

### 痛点

- 现有 legal AI 多停留在检索、摘要、合同审阅。
- 真正费时的是案件材料持续积累、证据/主张/时间线一致性、阶段切换时的漏项控制。
- 中文本地司法流程和文书习惯，使通用 legal assistant 很难直接变成可交付工作流。

### 可能产品形态

- “案件记忆 + 阶段推进”工作台。
- 从咨询纪要开始，贯穿立案材料、证据目录、庭审提纲、执行跟进，保留来源、日期、责任人、下一步动作。
- 面向律所 SOP 而非通用聊天，强调每一步都可回查、可审校、可导出。

### 验证方式

- 找 5-8 位执业律师或法援工作人员，收集 20-30 个匿名历史案包。
- 先做一个高重复场景，如劳动争议、借贷纠纷、租赁纠纷。
- 验证指标：首稿耗时、漏项率、事实不一致率、资深律师审校时间。

### 与现有 idea 的差异或重复风险

- 不同于 `AI 合同阅读助手`：合同阅读是单文档任务，这里是案件生命周期工作流。
- 不同于 `LegalCompass AI`：不是泛法律导航，而是给专业团队做 matter ops。
- 重复风险：中低，但必须坚持“案件流程操作系统”，不要回退成通用法务问答。

## 候选 5：AI Video Production Control Tower

### 来源依据

- 2026-01-29，MITO AI 融资后主打“multiplayer”式 AI 影视/广告生产协作，说明市场正在从单点生成走向流程协同。  
  链接：https://www.businessinsider.com/mito-ai-raised-5-million-round-read-its-pitch-deck-2026-1
- 2026-02-13，Seedance 2.0 爆红并引发版权争议，说明高质量视频模型在中国和全球创作端加速普及，但团队级治理和版权防线仍然薄弱。  
  链接：https://www.axios.com/2026/02/13/disney-bytedance-seedance
- 2026-01-15，Higgsfield 达到更高估值，且定位面向创作者与营销团队的短视频/广告工作流工具，进一步验证“创意生产操作层”是可融资方向。  
  链接：https://en.wikipedia.org/wiki/Higgsfield_AI

### 目标用户

- 使用多种文生视频/图生视频模型的中小创意代理商、品牌内容团队、AI 视频工作室。

### 痛点

- 工具越来越多，但 brief、分镜、素材引用、prompt 版本、审片反馈和渠道导出仍然分散在飞书、表格和聊天里。
- 一旦多人协作，角色一致性、镜头 continuity、品牌边界和版权风险会迅速失控。
- 现有创意工具更像“生成器”或“编辑器”，不是团队生产控制台。

### 可能产品形态

- 从 brief 到 final delivery 的控制塔。
- 管理镜头树、参考素材、prompt lineage、模型路由、版本差异、版权风险提示、客户审片和多平台导出。
- 可以先只做“短广告/短剧/产品种草视频”的轻量生产流程。

### 验证方式

- 找 3-5 个 AI 视频创作团队或内容代理商，观察真实交付流程。
- 先只支持 2-3 个主流模型与一个审片流程。
- 验证指标：从 brief 到首版时长、返工轮次、素材丢失率、跨人协作混乱度。

### 与现有 idea 的差异或重复风险

- 不同于 `AI创意剪辑引擎`：后者更像单人编辑提效；这里是团队级生产流程、版本管理与风控。
- 不同于 `AI协作灵感引擎`：不是灵感共创，而是可交付的生产运营层。
- 重复风险：中等，需要保持“production ops + governance”而不是做成又一个视频生成前端。

## 本轮判断

- 最值得继续跟进的前两项：`Agent Security ReviewOps`、`Healthcare Admin Precision Copilot`。
- 原因：两者都具备明确的高成本痛点，且与仓库现有 idea 的重叠最小。
- 需要谨慎的方向：`AI Video Production Control Tower`，因为创意工具赛道很热，但也更拥挤，必须依靠团队协作与版权治理切出差异。

## 执行备注

- 本次未直接加入主 idea 列表。
- 截至 2026-06-26，工作区存在已有未提交改动：`docs/automation-runbook.md`、`scripts/openclaw-automation.sh`。
- 因工作区不干净，本次只落盘报告，不执行提交。
- 后续人工链接检查：15 个来源链接中 10 个可直接访问；Axios、FT、WSJ 与 Wikipedia 链接可能受站点限制或页面变动影响，推进前需要二次核验。
