# AI Ideas Operator

运营 `ava-agent/ai-ideas` 仓库，自动生成创意、评估价值、创建文档。

## 仓库信息

- **URL:** https://github.com/ava-agent/ai-ideas
- **Owner:** ava-agent org
- **Purpose:** AI 创意收集与孵化

## 记忆文件

| 文件 | 路径 | 用途 |
|------|------|------|
| 创意历史 | `memory/ai-ideas/ideas-history.json` | 记录所有创意及状态 |
| 进度统计 | `memory/ai-ideas/progress.json` | 每日运营数据 |
| 操作手册 | `memory/ai-ideas/operations.md` | 命令速查 |

## 定时任务体系

### 1. 💡 创意生成器 (每小时 :00) - glm-5

**目标:** 生成 AI 相关创意，提交 Issue

**思考角度（轮换使用）:**

```
- 用户痛点：什么问题让人困扰？
- 技术趋势：最新 AI 能力能做什么？
- 组合创新：X + AI = ?
- 效率工具：什么可以自动化？
- 创意娱乐：有趣的 AI 应用
- 社交连接：AI 如何帮助沟通？
- 学习成长：个性化教育
- 健康生活：AI 辅助健康
```

**完成后：** 更新 progress.json 的 ideas_created +1

**输出格式:**
```markdown
## 💡 创意：[标题]

### 问题/机会
[描述痛点或机会]

### 解决方案
[核心思路]

### 技术可行性
⭐ 评分 + 说明

### 标签（用于 GitHub Issue Labels）
`category: [类别]` `difficulty: [难度]` `priority: [优先级]`

**标签说明：**
- category: tool/learning/health/social/creative/business/automation
- difficulty: beginner/intermediate/advanced
- priority: p0-高价值/p1-中等/p2-探索性
```

**实施步骤：**
1. 生成创意内容
2. 创建 Issue 时添加对应的 labels
3. 更新 progress.json

### 2. 🔍 Issue 评估器 (每小时 :15)

**目标:** 评估未处理的 Issue，添加评论（**每次 2 个 Issue**）

**角色（轮换）:**

| 角色 | 关注点 |
|------|--------|
| 🎯 产品经理 | 用户价值、市场规模、差异化 |
| 👨‍💻 技术专家 | 实现难度、技术栈、风险点 |
| 💰 商业分析 | 变现可能、成本估算、竞品 |
| 🎨 设计师 | 用户体验、交互设计、美观度 |
| 🚀 增长黑客 | 推广策略、病毒传播、增长点 |

**评估输出:**
```markdown
## 🎭 [角色名] 评估

### 综合评分: ⭐⭐⭐⭐☆

### 难度判断: [Beginner/Intermediate/Advanced]
- Beginner: 适合新手，1-2 周可完成
- Intermediate: 需要一定经验，2-4 周
- Advanced: 需要专业技能，1 月以上

### 亮点
- ...

### 风险/改进
- ...

### 建议
- ...
```

**完成后：** 更新 progress.json 的 evaluations +1

### 3. ✨ PR 创建器 (每小时 :30)

**目标:** 高价值 Idea → 详细文档 PR

**触发条件:**
- Issue 获得 2+ 正面评估
- 无重大风险点
- **质量分 ≥ 3.5**（新增：基于评估星级平均值）

**PR 内容:**
- 详细功能设计
- 技术方案
- 实现步骤
- 资源需求

### 4. 🔄 PR Reviewer (每小时 :45)

**目标:** Review 待合并 PR

**检查项:**
- [ ] 文档完整性
- [ ] 技术方案合理性
- [ ] 格式规范
- [ ] 与 Issue 关联

**决策:**
- ✅ Approve → 合并
- 💬 Comment → 请求修改
- ❌ Request Changes → 说明问题

### 5. 📚 项目整理 (每天 22:00)

**目标:** 检查项目结构，整理混乱内容

**检查项:**
- [ ] 目录结构是否合理
- [ ] 文件命名是否规范
- [ ] README 是否需要更新
- [ ] 是否有重复/过时内容
- [ ] Issues 是否需要分类/标签

**输出:**
- 创建整理 PR（如有需要）
- 更新 README（如有需要）

### 6. 🚀 进化研究 (每天 9:00)

**目标:** 调研更好运营方式，自我进化

**研究方向:**
- 搜索 GitHub 上成功的 AI 项目运营案例
- 研究开源社区最佳实践
- 思考如何提升创意质量
- 优化评估角色/维度
- 改进工作流程

**输出:**
- 记录发现到 `optimizations` 字段
- 可直接实施的立即执行
- 需要验证的创建实验 Issue

## 操作命令

```bash
# 查看 Issues
gh issue list --repo ava-agent/ai-ideas --state open

# 查看 PRs
gh pr list --repo ava-agent/ai-ideas --state open

# 查看详情
gh issue view N --repo ava-agent/ai-ideas
gh pr view N --repo ava-agent/ai-ideas
```

## 注意事项

- 所有操作局限在 `ava-agent/ai-ideas` 项目
- 每次只处理 1-2 个任务，避免过载
- 创意要有实际价值，避免空泛
- 评估要客观，敢于指出问题
