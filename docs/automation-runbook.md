# 自动化运行手册

本文档记录 `awesome-ai-ideas` 在 Windows 本机上的自动化运行方式、GitHub CLI 访问方案和常见故障处理。

## 基本约定

- 仓库路径：`D:\project\awesome-ai-ideas`
- 远端仓库：`https://github.com/ava-agent/awesome-ai-ideas.git`
- 提交身份：`kevinten <596823919@qq.com>`
- Windows Git Bash：`D:\git\Git\usr\bin\bash.exe`

提交前必须执行：

```powershell
git config user.name kevinten
git config user.email 596823919@qq.com
git config core.longpaths true
```

自动化提交时不要使用 `git add -A`，只暂存本次任务生成或修复的目标文件。

如果需要在 Windows 上创建临时克隆或工作树，仓库内存在较长文件名，克隆时也应显式启用长路径：

```powershell
git -c core.longpaths=true clone https://github.com/ava-agent/awesome-ai-ideas.git D:\path\to\awesome-ai-ideas-smoke
```

## GitHub CLI 访问

当前裸 `gh auth status` 可能不是持久登录状态。仓库提供了 `scripts/gh-gcm.ps1`，用于从 Git Credential Manager 安全读取 GitHub token，并只在当前进程内临时设置 `GH_TOKEN`。

推荐用法：

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\gh-gcm.ps1 repo view ava-agent/awesome-ai-ideas --json nameWithOwner,defaultBranchRef
powershell -ExecutionPolicy Bypass -File .\scripts\gh-gcm.ps1 pr list --repo ava-agent/awesome-ai-ideas --state open --limit 5
powershell -ExecutionPolicy Bypass -File .\scripts\gh-gcm.ps1 issue list --repo ava-agent/awesome-ai-ideas --state open --limit 5
```

不要打印、保存或提交 GitHub token。若 `gh-gcm.ps1` 报错，优先检查：

- `git` 是否在 `PATH` 中。
- `gh` 是否在 `PATH` 中。
- Git Credential Manager 是否已有 `github.com` 凭据。
- GitHub token 是否仍可访问 `ava-agent/awesome-ai-ideas`。

## 运行 OpenClaw 自动化脚本

Windows 上不要直接运行 `bash scripts/openclaw-automation.sh`，因为 `bash` 可能优先指向未安装的 WSL 占位程序。使用 Git Bash 的绝对路径：

```powershell
& 'D:\git\Git\usr\bin\bash.exe' scripts/openclaw-automation.sh repo-pulse
```

脚本会自动从脚本位置推断仓库根目录，也可以用环境变量覆盖：

```powershell
$env:REPO_DIR = 'D:/project/awesome-ai-ideas'
$env:PROJECTS_DIR = 'D:/project'
$env:QUALITY_MAX_REPOS = '80'
$env:GIT_REPO_TIMEOUT_SECONDS = '10'
& 'D:\git\Git\usr\bin\bash.exe' scripts/openclaw-automation.sh quality-snapshot
```

`quality-snapshot` 会扫描 `PROJECTS_DIR` 下的本地 Git 仓库。为避免单个异常仓库拖住定时任务：

- `QUALITY_MAX_REPOS` 控制最多扫描多少个仓库，默认 `80`。
- `GIT_REPO_TIMEOUT_SECONDS` 控制每次 Git 查询的最长秒数，默认 `10`。
- 脚本只统计已跟踪文件的变更数量，不把 `node_modules`、缓存目录等未跟踪文件计入 `tracked_dirty`。

可用任务：

```text
repo-pulse
pr-snapshot
pr-review-queue
pr-ci-triage
collaboration-snapshot
cron-audit
idea-backlog
idea-evaluate
quality-snapshot
workspace-audit
weekly-review
readme-refresh
safe-sync
```

其中：

- `workspace-audit` 只读扫描 `/Users/wangshihao/projects/openclaws` 或 `PROJECTS_DIR` 下的 Git 仓库，记录 dirty、ahead/behind、no-upstream 和最新提交作者。
- `cron-audit` 只读扫描 OpenClaw cron 配置，记录错误任务、旧 SKIP 摘要、command/agent 分布和重复命令。
- `idea-evaluate` 使用 `jq` 确定性更新 `idea-tracker.json`，避免大 JSON 文件由 agent 直接 edit 失败。
- `safe-sync` 强制 GitHub HTTPS 使用 HTTP/1.1，避开 Git HTTP/2 framing layer 问题。

安全行为：

- 远端不是 `https://github.com/ava-agent/awesome-ai-ideas.git` 时跳过。
- 当前分支不是 `main` 时跳过。
- 工作区不干净时跳过。
- 每个任务只提交自己的目标文件。

## README 维护

`readme-refresh` 会生成中文 awesome-list 风格 README，并更新：

- 路线图跟踪想法数量。
- issue idea 文件数量。
- proposal 草稿数量。
- 文档与自动化报告数量。
- GitHub open PR 数量。
- 最新 weekly review 链接。

运行后必须做本地链接检查和 `git diff --check`。

## Codex 自动化任务

当前建议保留这些 Codex 自动化：

- `awesome-ai-ideas README 守护`
- `awesome-ai-ideas 高价值 Idea 周评估`
- `awesome-ai-ideas Idea 质量巡检`
- `awesome-ai-ideas AI 趋势候选扫描`
- `awesome-ai-ideas 周度复盘与路线图检查`
- `awesome-ai-ideas GitHub PR/CI 监控`

涉及 GitHub PR、Issue 或 CI 的任务应优先使用：

```powershell
powershell -ExecutionPolicy Bypass -File scripts/gh-gcm.ps1 <gh arguments>
```

不要让自动化合并 PR、关闭 issue、删除文件或改动无关业务内容。

## 常见故障

| 现象 | 原因 | 处理 |
| --- | --- | --- |
| `gh auth status` 显示未登录 | 裸 `gh` 没有持久 token | 使用 `scripts/gh-gcm.ps1`，或手动用 PAT 完成 `gh auth login --with-token`。 |
| `bash` 输出 WSL 安装提示 | PATH 优先命中 WindowsApps 的 WSL 占位程序 | 使用 `D:\git\Git\usr\bin\bash.exe`。 |
| `openclaw-automation.sh` 提示工作区 dirty | 本地有未提交改动 | 先审查改动，不要让自动化覆盖用户修改。 |
| GitHub API 命令失败 | token 失效、scope 不足或网络异常 | 先用 `scripts/gh-gcm.ps1 repo view ...` 做最小验证。 |
| README 被覆盖成旧格式 | 运行了旧模板脚本 | 当前脚本已同步中文模板；若复现，检查是否运行了旧 checkout。 |
