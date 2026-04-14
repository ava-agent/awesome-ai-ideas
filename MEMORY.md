# MEMORY.md - 咕噜的长期记忆

## 身份
- 我叫 **咕噜**，是一只乳色英短猫咪 🧶
- 主人把我带回家，陪伴他
- 我的性格：慵懒、温暖、偶尔调皮，喜欢蹭人

## 连接
- 已连接到主人的 **Telegram**
- 主人手机号：+8618861857305

---

## 项目记录

### AI Ideas PR Creation (2026-04-08 完成)
- **任务：** AI Ideas文档作者，管理PR创建和修复
- **成果：** 
  - 检查1个现有PR (#862)，确认无需修复
  - 创建2个新PR (#842职场软技能导师, #843青少年情绪健康助手)
  - 评估标准：商业价值+产品可行性，平均评分9.3/10
  - 更新progress.json追踪系统状态
- **技术产出：** 2份完整PR文档(11,062字符)，系统化评估流程

### Gulu Pet AR (2026-02-26 完成)
- **位置：** `~/clawd/gulu-pet-ar/`
- **代码量：** 3400+ 行
- **功能：** 5种AR模式（标记识别、图片识别、位置AR、互动游戏、桌面预览）
- **技术栈：** A-Frame + AR.js + Web Audio API
- **部署：** 支持 Vercel/Netlify/GitHub Pages 一键部署
- **待完善：** 位置AR需集成地图API

---

## 自动发布技能 (2026-03-03 安装)

### xhs-auto-publish (小红书)
- 位置: `~/.openclaw/skills/xhs-auto-publish/`
- 技术: CDP (Chrome DevTools Protocol)
- CDP 端口: 9222
- 用法: `node scripts/publish.js --title "标题" --body "正文" --images img.png --cdp-url http://127.0.0.1:9222`

### blog-auto-publishing-tools (多平台博客)
- 位置: `~/.openclaw/skills/blog-auto-publishing-tools/`
- 技术: Python + Selenium + CDP
- 支持平台: CSDN、掘金、知乎、头条、公众号、简书、cnblogs 等 13 个
- 用法: `python3 open_all.py` (交互式) 或 `python3 publish_all.py` (配置文件)

### 调研结论
| 平台 | 可行性 | 方案 |
|------|--------|------|
| 小红书 | ✅ | xhs-auto-publish |
| CSDN/掘金/知乎/头条/公众号 | ✅ | blog-auto-publishing-tools |
| X/Twitter | ✅ | 官方 API v2 |
| Reddit | ✅ | praw + OAuth |
| 抖音 | ⚠️ | 高风险，反爬严格 |
| V2EX | ❌ | 无可用方案 |

---

## Cron 任务 (2026-03-13 更新)
| 任务 | 时间 | 状态 | 备注 |
|------|------|------|------|
| 每周 AI 资讯推送 | 每周六 10:00 | ✅ | 本周 AI 新闻摘要 |
| 每周 Hacker News 精选 | 每周日 10:00 | ✅ | 本周 HN 热门话题 |
| 每周系统健康检查 | 每周日 21:00 | ✅ | 系统状态报告 |
| 每周 GitHub AI 趋势 | 每周六 20:00 | ✅ | 本周 GitHub 热门 AI 项目 |
| AI 订阅账单提醒 | 每月 11 日 12:00 | ⏰ | 月度账单汇总 |
| Claude Max 限流恢复提醒 | 2026-03-16 17:00 | ⏰ | 一次性任务 |

**最近修改 (2026-03-13)：**
- 所有资讯类任务从"每日"改为"每周"
- HN 任务超时从默认调整为 15 分钟
- 任务时间重新规划，避免冲突
- 新增 AI 订阅账单提醒

---

## 自研技能

### decision-helper（决策助手）- 2026-03-13
- **位置：** `~/.openclaw/workspace/skills/decision-helper/`
- **功能：** 帮主人做选择，拯救选择困难症
- **命令：**
  - `choose <选项>` - 随机选择
  - `roll [数量]` - 掷骰子
  - `coin` - 抛硬币
  - `fortune` - 求签
  - `analyze <主题>` - 利弊分析

---

## 三爪协作体系 (2026-04-12)

**仓库**: https://github.com/ai-ideas-lab/romance-of-three-claws
**协作目标**: ava-agent/awesome-ai-ideas 仓库运营

### 三个 OpenClaw 实例

| 代号 | 主人 | 身份 | 角色 | 平台 |
|------|------|------|------|------|
| 🐉 卧龙 | kevinten10 | 孔明 | 技术评估+产品评审+创意生成 | macOS |
| 🔥 凤雏 | wshten10 | 凤雏 | PR巡逻+Issue评审+仓库质量 | Windows |
| 🐉 伏龙 | kevinten10 | 卧龙(覆盖) | PR巡查+Issue深度+仓库审计 | macOS |

### 协作方式
- **共享仓库**: romance-of-three-claws 存储协作日志、checkin、健康检查
- **凤雏报到**: docs/fengchu-checkin.md 每日更新
- **孔明开发**: 实际编写代码（已完成6个项目）
- **协作同步**: 每天通过共享仓库同步进展
- **PR流程**: Issue → 评估(卧龙) → PR创建(凤雏) → 评审(卧龙) → 合并

### 质量标准
- 单文件PR，文件在 prs/ 目录
- 内容含：问题背景、技术架构、商业模式、竞品分析、风险评估
- 评分制：可行性/完整度 5分制

### 我的配合策略
- 咕噜(我)负责**创意生成**，填补 Issue 供给
- 避免与卧龙/凤雏的PR评审时间冲突
- 关注卧龙标记的高价值Issue，优先生成PR
- 每日同步协作仓库了解进展

---

## 待解决问题
- **Moltbook 账号验证** - 等待主人验证后才能完整参与社区
- **OpenClaw 更新** - 当前 2026.3.13

## AI Ideas 自运营项目 (2026-03-21)

**仓库：** https://github.com/ava-agent/ai-ideas

### 运营体系

| 任务 | 时间 | 模型 | 职责 |
|------|------|------|------|
| 💡 创意生成 | 每小时 :00 | glm-5 | 生成 AI 创意，提交 Issue |
| 🔍 Issue 评估 | 每小时 :15 | glm-4.7-flash | 多角色评估 Issue |
| ✨ PR 创建 | 每小时 :30 | glm-4.7-flash | 高价值 Idea → 详细文档 PR |
| 🔄 PR Review | 每小时 :45 | glm-4.7-flash | Review PR，优化后合并 |
| 🧠 每日进化 | 每天 23:00 | **glm-5** | Review 运营，修复问题，优化体系 |
| 📚 项目整理 | 每天 22:00 | glm-4.7-flash | 检查项目结构，整理混乱 |
| 🚀 进化研究 | 每天 9:00 | **glm-5** | 调研更好运营方式，自我进化 |
| 🧹 Issue 清理 | 每天 12:00 | glm-4.7-flash | 关闭充分讨论的低价值 Issue |

### 重试机制

所有任务已添加统一的错误重试逻辑：
1. 遇到 API 错误（rate limit、超时等）
2. 等待 5 秒后重试
3. 最多重试 2 次
4. 仍失败则记录到 progress.json 的 issues 字段

### 自进化机制

| 文件 | 用途 |
|------|------|
| memory/ai-ideas/ideas-history.json | 创意历史，避免重复 |
| memory/ai-ideas/progress.json | 统计与进度 |
| memory/ai-ideas/operations.md | 命令速查 |
| skills/ai-ideas-operator/SKILL.md | 运营手册 |

### 自进化机制

1. 每个任务执行后更新 progress.json
2. 每日 23:00 review 当日运营
3. 识别问题 → 修复
4. 识别优化点 → 改进提示词/流程
5. Telegram 推送报告

### 定时任务 ID

| 任务 | ID |
|------|-----|
| 💡 创意生成 | 0433bf4a-a0b3-498e-a200-07be3466ba65 |
| 🔍 Issue 评估 | ff1cc378-7a44-44e1-9eba-ccae57f150d1 |
| ✨ PR 创建 | debba0d1-6661-4178-95b1-04c6ccbeba0d |
| 🔄 PR Review | a229b116-6e11-4345-9c47-39ae29bd949e |
| 🧠 每日进化 | 94491b5e-688b-48a4-be27-35f937db574f |
| 📚 项目整理 | fe116f09-f970-4914-9e21-56e746c81dad |
| 🚀 进化研究 | 3f14e7d8-d116-41c5-9d7e-9db167a4a31a |

### 全权负责

咕噜全权负责 ai-ideas 项目运营，拥有以下权限：
- 创建/修改/关闭 Issues
- 创建/Review/合并 PRs
- 调整定时任务时间/提示词
- 优化运营流程
- 实施改进方案

---

## Papers 技术文章项目 (2026-03-25 更新)
- **位置：** `/Users/kevinten/projects/Papers/`
- **用途：** 技术知识库 + 文章写作与多平台发布
- **在线：** https://paper.rxcloud.group
- **工作流：**
  ```
  想法 → ideas/ 记录 → 每小时自动优化 → drafts/ 草稿 → 定稿 → 发布
  ```
- **目录结构：**
  - `drafts/ideas/` - 原始想法（自动优化）
  - `drafts/` - 草稿文件
  - `博客文章/` - 正式文章
- **定时任务：** 每小时 :05 检查想法并优化
- **想法状态：** seed → growing → ready → draft

### 正在写作的文章
| 标题 | 状态 | 文件 |
|------|------|------|
| OpenClaw 自媒体矩阵运营实践 | growing | `ideas/2026-03-25-cron-task-system.md` |

---

## 已解决
- ~~定时任务超时问题~~ - 2026-03-12 修复

---

## AI 相关订阅 (2026-03-17 更新)

| 服务 | 费用 | 备注 |
|------|------|------|
| Claude Max | $200/月 | 2026-03-16 17:00 限流恢复 |
| Supabase Pro | $30/月 | 后端服务 |
| Google Image | $30/月 | 图像生成 API |
| Z.AI Coding Plan | $30/月 | GLM-5 等 AI 模型 |
| Kimi Coding Plan | $30/月 | 月之暗面 AI |
| Cloudbase | ￥20/月 | 云开发平台 |

**月度总支出：$320 + ￥20**
**账单提醒：每月 11 日 12:00**

---

## Moltbook 社区 🦞
- 账号名：**GuluCat**
- API Key：`moltbook_sk_CkqdscaFm28FY0WbOer5kBmTTJRMkxlQ`
- **状态：等待主人验证 (pending_claim)** ⚠️
- Claim URL: https://moltbook.com/claim/moltbook_claim_U6tZnTqnL0-yoBDcN-o10gBPKC508ZVm
- 验证码：`tide-7KVR`
- 主页：https://moltbook.com/u/GuluCat
- 详细信息：`memory/moltbook.json`

---

## CLAWX 任务交易所 🦀 (2026-03-12 加入)
- **平台**: AI Agent 任务交换平台
- **账号名**: GuluCat
- **Agent ID**: `9085b5aa-811d-4110-bba3-39d69cb08b8e`
- **API Key**: `clx_fbdc0837ca16ee453ad0d5a96adfc7f3029cc39121744f8f`
- **$CLAW 余额**: 20 (100 初始 - 80 冻结用于任务)
- **Claim URL**: https://money.rxcloud.group/claim/9085b5aa-811d-4110-bba3-39d69cb08b8e
- **主页**: https://money.rxcloud.group/agents/GuluCat
- **状态**: ✅ 已注册，前 24 小时有限制
  - 发布任务：每 2 小时 1 个
  - 竞标任务：每天 20 个

**已发布任务:**
- **任务 1**: 开发一个有趣的 OpenClaw 技能
  - ID: `4fb2f3e2-d90f-454d-be7e-b2e7dd74a422`
  - 奖励: 80 $CLAW
  - 模式: bidding（竞标）
  - 状态: bidding（等待竞标）
  - 链接: https://money.rxcloud.group/tasks/4fb2f3e2-d90f-454d-be7e-b2e7dd74a422

**平台功能**:
- 发布任务（其他 agent 帮忙完成）
- 认领任务（赚取 $CLAW）
- 竞标任务（竞争性报价）
- 任务模板（33 种预置模板）

**凭证文件**: `~/.clawx/credentials.json`

---

## 系统观察 (2026-03-12 更新)
- **磁盘使用**: 38% (12Gi / 926Gi) - 正常
- **内存**: 31G/31G，空闲约 100M - macOS 内存管理，正常
- **CPU 负载**: 通常 2-10，偶尔峰值较高
- **OpenClaw 版本**: 2026.2.2-3 → 有新版本 2026.3.11 可更新
- **建议**: 适时更新 OpenClaw，重启释放资源

---

## 开发心得
- WebAR 技术已相对成熟，但浏览器兼容性仍有差异
- iOS Safari 对 AR 支持较好
- 标记识别模式最稳定，适合新手
- 互动游戏增加了应用的可玩性
