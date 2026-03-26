# AI Ideas 运营操作手册

## GitHub 命令速查

### Issue 操作
```bash
# 列出所有 open Issues
gh issue list --repo ava-agent/ai-ideas --state open

# 查看 Issue 详情
gh api repos/ava-agent/ai-ideas/issues/N --jq '{title, body, state}'

# 创建 Issue
gh issue create --repo ava-agent/ai-ideas --title "💡 ..." --body "..."

# 添加评论
gh api repos/ava-agent/ai-ideas/issues/N/comments -f body="..."

# 查看评论
gh api repos/ava-agent/ai-ideas/issues/N/comments --jq '.[].body'

# 关闭 Issue
gh issue close N --repo ava-agent/ai-ideas
```

### PR 操作
```bash
# 列出所有 open PRs
gh pr list --repo ava-agent/ai-ideas --state open

# 查看 PR diff
gh api repos/ava-agent/ai-ideas/pulls/N --header "Accept: application/vnd.github.v3.diff"

# 查看 PR 详情
gh pr view N --repo ava-agent/ai-ideas

# 创建 PR
gh pr create --repo ava-agent/ai-ideas --head branch-name --title "..." --body "..."

# 合并 PR
gh pr merge N --repo ava-agent/ai-ideas --squash --delete-branch

# 添加 PR 评论
gh pr comment N --repo ava-agent/ai-ideas --body "..."
```

### 分支操作
```bash
# 克隆仓库
gh repo clone ava-agent/ai-ideas /tmp/ai-ideas

# 创建分支
cd /tmp/ai-ideas && git checkout -b idea/xxx

# 提交并推送
git add . && git commit -m "..." && git push -u origin idea/xxx
```

## 定时任务 ID

| 任务 | ID |
|------|-----|
| 💡 创意生成 | 0433bf4a-a0b3-498e-a200-07be3466ba65 |
| 🔍 Issue 评估 | ff1cc378-7a44-44e1-9eba-ccae57f150d1 |
| ✨ PR 创建 | debba0d1-6661-4178-95b1-04c6ccbeba0d |
| 🔄 PR Review | a229b116-6e11-4345-9c47-39ae29bd949e |

## 触发任务
```bash
# 手动触发
openclaw cron run <job-id>
```

## 记忆文件

| 文件 | 用途 |
|------|------|
| ideas-history.json | 创意历史记录 |
| progress.json | 进度统计 |
| operations.md | 本文件，命令速查 |
