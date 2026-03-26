---
name: dev-loop
description: "持续开发循环 - 启动 Claude Code 后台运行，自动监控、恢复、继续。适用于：通宵开发、批量任务、长期项目。需要 claude 或 codex CLI。"
metadata:
  {
    "openclaw": { "emoji": "🔄", "requires": { "anyBins": ["claude", "codex"] } },
  }
---

# Dev Loop - 持续开发循环（最佳实践版）

基于 OpenClaw 官方文档和社区最佳实践整理。

---

## 核心架构

```
┌─────────────────────────────────────────────────────┐
│              Dev Loop 工作流程                       │
├─────────────────────────────────────────────────────┤
│                                                     │
│  1. 启动 Claude Code (background + PTY)             │
│     └─→ 返回 sessionId                              │
│                                                     │
│  2. HEARTBEAT 定期检查 (本地模型)                   │
│     ├─→ process action:list                         │
│     ├─→ process action:log                          │
│     └─→ 检测卡住/等待输入                           │
│                                                     │
│  3. 自动恢复机制                                    │
│     ├─→ 卡住 → submit "continue"                   │
│     ├─→ 等待确认 → submit "yes"                    │
│     ├─→ 崩溃 → 读取日志 → 重启                     │
│     └─→ 连续失败3次 → 通知主人                     │
│                                                     │
│  4. 任务完成                                        │
│     ├─→ 更新 MEMORY.md                              │
│     ├─→ 提交 git                                    │
│     └─→ 发送 Telegram 通知                         │
│                                                     │
└─────────────────────────────────────────────────────┘
```

---

## 启动方式

### 方式一：单次长任务

```bash
# 在目标目录启动 Claude Code
bash pty:true \
  workdir:~/projects/myapp \
  background:true \
  command:"claude '实现用户认证系统，包括注册、登录、JWT。完成后运行测试。'"
```

### 方式二：任务队列模式

创建 `~/clawd/dev-tasks.md`：

```markdown
# Dev Tasks

## Current
- [ ] 实现用户认证系统

## Next
- [ ] 添加 API 速率限制
- [ ] 实现缓存层

## Rules
- 每完成一个任务，标记为 [x]
- 自动开始下一个任务
- 遇到阻塞发 Telegram 询问
```

启动命令：

```bash
bash pty:true \
  workdir:~/clawd \
  background:true \
  command:"claude '读取 dev-tasks.md，按顺序完成任务。完成后更新文件状态。'"
```

### 方式三：GitHub Issue 驱动

```bash
bash pty:true \
  workdir:~/projects/myapp \
  background:true \
  command:"claude '获取 GitHub Issues 列表，按优先级修复。每个修复创建独立 PR。'"
```

---

## 监控命令

| 操作 | 命令 |
|------|------|
| 查看活跃会话 | `process action:list` |
| 检查是否运行 | `process action:poll sessionId:XXX` |
| 获取最新输出 | `process action:log sessionId:XXX limit:50` |
| 发送继续信号 | `process action:submit sessionId:XXX data:"continue"` |
| 自动确认 | `process action:submit sessionId:XXX data:"yes"` |
| 发送任意输入 | `process action:submit sessionId:XXX data:"你的回答"` |
| 终止进程 | `process action:kill sessionId:XXX` |

---

## 自动恢复配置

### 崩溃恢复

如果 Claude Code 崩溃：

1. **自动检测**：HEARTBEAT 发现进程消失
2. **日志分析**：读取 `~/.openclaw/logs/gateway.log`
3. **断点恢复**：读取 `memory/dev-progress.md`
4. **重启任务**：从上次停止点继续

### 进度保存

让 Claude Code 定期保存进度：

```
"每完成一个功能模块后：
1. git commit
2. 更新 memory/dev-progress.md
3. 发送 openclaw system event --text 'Done: 模块名'"
```

---

## 最佳实践

### ✅ DO

1. **使用 workdir 隔离**
   ```bash
   workdir:~/projects/auth-system  # 每个项目独立
   ```

2. **设置超时保护**
   ```bash
   timeout:3600000  # 1 小时
   ```

3. **明确定义停止条件**
   ```
   "遇到以下情况停止并通知我：
   - 需要数据库迁移
   - 需要修改 API 接口
   - 连续 3 次测试失败"
   ```

4. **使用本地模型处理心跳**（节省成本）
   ```json
   {
     "heartbeat": {
       "model": "ollama://qwen2.5:7b",
       "interval": 3600
     }
   }
   ```

### ❌ DON'T

1. **不要在 ~/.openclaw/ 目录启动 Claude Code**
   - 它会读取你的 SOUL.md 并产生奇怪的想法

2. **不要让 Claude Code 无限运行**
   - 设置明确的时间限制或任务数量

3. **不要忽略错误日志**
   - 连续失败 3 次应该人工介入

---

## 实战案例

### 通宵开发

```
用户："今晚帮我完成 auth-system：
- 读取项目里的 TODO.md
- 按优先级依次完成
- 遇到无法决定的问题发 Telegram
- 明早 8 点给我完成报告"
```

结果：
- 夜间自动运行 8 小时
- 完成 12 个任务
- 生成 47 次 commit
- 早 8 点收到完整报告

### 批量 PR 修复

```bash
# 启动多个并行任务
bash pty:true workdir:/tmp/issue-78 background:true \
  command:"codex --yolo 'Fix issue #78. Commit and push.'"

bash pty:true workdir:/tmp/issue-99 background:true \
  command:"codex --yolo 'Fix issue #99. Commit and push.'"

# HEARTBEAT 自动监控所有会话
```

---

## 成本优化

| 场景 | 推荐模型 | 成本 |
|------|---------|------|
| 心跳检查 | Qwen 7B (本地) | $0 |
| 简单任务 | GLM-4.7-flash | 极低 |
| 复杂开发 | Claude Code | 标准 |
| 代码审查 | Claude Sonnet | 中等 |

---

## 安全配置

```json
{
  "security": {
    "sandbox": {
      "allowedPaths": ["~/projects", "~/clawd"],
      "blockedCommands": ["rm -rf", "dd", "mkfs"]
    }
  }
}
```

---

## 故障排除

| 问题 | 解决方案 |
|------|---------|
| Agent 无响应 | `process action:submit data:"continue"` |
| 等待确认超时 | `process action:submit data:"yes"` |
| 进程崩溃 | 检查日志，从断点重启 |
| Token 超限 | 执行 `/compact` 压缩上下文 |
| 权限错误 | 检查 allowedPaths 配置 |
