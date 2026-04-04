# AI Ideas Issue Evaluator

一个用于评估 ava-agent/awesome-ai-ideas 仓库中创意的自动化工具，能够从不同专业角度为Issue提供评估评论。

## 功能特点

- 🎯 **多角色评估**：产品经理、技术专家、商业分析师、增长黑客四种视角
- 🔄 **自动轮换**：按照预设角色循环为Issue添加评估
- ⏱️ **错误重试**：遇到API错误时自动重试（最多2次）
- 📊 **进度追踪**：实时记录评估进度和结果
- 💡 **智能分析**：根据Issue内容生成针对性的评估建议

## 使用方法

### 1. 设置GitHub Token（可选但推荐）

```bash
# 设置GitHub个人访问令牌（提高API调用限制）
export GH_TOKEN='your_github_personal_access_token_here'
```

### 2. 运行评估

```bash
# 直接运行评估
/Users/zhengmin/.openclaw/workspace/memory/awesome-ai-ideas/evaluate.sh

# 或者进入脚本目录运行
cd /Users/zhengmin/.openclaw/workspace/memory/awesome-ai-ideas
./evaluate.sh
```

### 3. 查看结果

评估完成后，结果会保存在以下文件中：

- `progress.json` - 评估进度和详细记录
- `evaluation.log` - 操作日志和评估过程

## 角色说明

### 🎯 产品经理
- **关注点**：用户价值、市场规模、产品定位
- **评估重点**：市场需求、用户痛点、商业价值
- **典型建议**：落地场景、用户群体验证、功能优先级

### 👨‍💻 技术专家  
- **关注点**：实现难度、技术风险、架构设计
- **评估重点**：技术可行性、复杂度评估、可维护性
- **典型建议**：技术验证方案、架构优化、风险评估

### 💰 商业分析师
- **关注点**：变现可能、竞品分析、商业模式
- **评估重点**：盈利模式、市场定位、竞争格局
- **典型建议**：差异化策略、定价策略、合作机会

### 🚀 增长黑客
- **关注点**：推广策略、增长点、用户增长
- **评估重点**：获客成本、传播机制、用户粘性
- **典型建议**：病毒式传播、社区运营、内容营销

## 工作流程

1. **获取Issue列表**：从 ava-agent/awesome-ai-ideas 仓库获取未评估的Issue
2. **筛选Issue**：选择评论最少的2个Issue
3. **角色分配**：按顺序为每个Issue分配评估角色
4. **生成评估**：根据Issue内容和角色定位生成针对性评估
5. **添加评论**：在GitHub Issue中添加评估评论
6. **更新进度**：记录评估结果和状态

## 错误处理

- **API限流**：自动等待5秒后重试，最多重试2次
- **网络错误**：记录错误并跳过当前Issue
- **认证失败**：提示设置GitHub Token
- **内容解析错误**：跳过格式异常的Issue

## 配置说明

### 环境变量
- `GH_TOKEN`: GitHub个人访问令牌（可选）

### 输出文件
- `progress.json`: 评估进度JSON文件
- `evaluation.log`: 详细操作日志

### 评价标准
- **最少评论优先**：选择评论数最少的Issue进行评估
- **角色轮换**：按照产品经理→技术专家→商业分析师→增长黑客的顺序循环
- **内容适配**：根据Issue标题和内容生成个性化评估

## 示例输出

```
🎯 **产品经理评估**

从用户价值角度看，这个创意关注核心需求，具有不错的市场潜力。建议关注落地场景和用户群体验证。

💡 **具体建议**：AI-powered code review using LLMs to help developers write better code...
```

## 故障排除

### 常见问题

1. **Rate limit exceeded**
   - 解决方案：设置GitHub Token提高API调用限制
   - 命令：`export GH_TOKEN='your_token'`

2. **No issues found**
   - 解决方案：检查网络连接和仓库名称
   - 确认：`ava-agent/awesome-ai-ideas` 仓库是否可访问

3. **JQ parse error**
   - 解决方案：确保jq已正确安装
   - 安装：`brew install jq` 或 `sudo apt-get install jq`

## 开发说明

### 扩展角色

如需添加新的评估角色，修改以下部分：

```bash
# 在 evaluate_issue() 函数中添加新角色
case $role in
    "new_role")
        evaluation="🔍 **新角色评估**\n\n评估内容..."
        ;;
esac
```

### 自定义评估逻辑

在 `evaluate_issue()` 函数中，可以添加更复杂的评估逻辑：

```bash
# 根据Issue标签调整评估重点
if echo "$title" | grep -q "AI"; then
    evaluation+="\n\n特别关注AI技术的应用场景..."
fi
```

## 贡献指南

欢迎提交Issue和Pull Request来改进这个工具！

### 开发环境设置

```bash
# 1. 克隆仓库
git clone <repository-url>

# 2. 安装依赖
chmod +x evaluate.sh

# 3. 测试运行
./evaluate.sh
```

### 测试方法

```bash
# 设置测试Token
export GH_TOKEN='test_token'

# 运行测试模式
./evaluate.sh
```

---

**注意**：要使用完整的GitHub API功能，需要设置有效的GitHub个人访问令牌。