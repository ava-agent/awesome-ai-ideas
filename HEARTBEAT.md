# HEARTBEAT.md - 持续开发循环

## 核心原则
- 保持简洁以减少 Token 消耗
- 定义清晰优先级避免过度打扰
- 仅在"异常"条件触发动作

---

## P0 - 阻塞问题（立即处理）

- [ ] 检查是否有失败的 CI 构建 → 停止开发，优先修复
- [ ] 检查是否有紧急 Bug 报告 → 立即通知主人
- [ ] 检查 Claude Code 进程是否卡住（5分钟无输出）→ 发送 "continue"

---

## P1 - Dev Loop 监控（每 5 分钟）

如果有活跃的 Claude Code 开发会话：

```bash
# 1. 检查活跃会话
process action:list

# 2. 获取最新输出（检查是否卡住）
process action:log sessionId:XXX limit:20

# 3. 如果卡住，发送继续信号
process action:submit sessionId:XXX data:"continue"

# 4. 如果等待确认，自动批准
process action:submit sessionId:XXX data:"yes"
```

**停止条件：**
- 连续 3 次尝试失败 → 暂停并通知主人
- 遇到需要人工决策的问题 → 发 Telegram 询问
- 收到 `/stop` 指令 → 保存进度并停止

---

## P2 - 系统健康（每 2 小时）

- [ ] 检查磁盘使用（> 85% 报警）
- [ ] 检查内存压力（压缩内存 > 16G 报警）
- [ ] 检查 Gateway 状态（不可达则自动重启）

---

## P3 - 开发进度（每天 1 次）

- [ ] 读取项目 TODO.md，更新任务状态
- [ ] 将完成的任务写入 MEMORY.md
- [ ] 生成当日开发简报

---

## 静默规则

以下情况回复 `HEARTBEAT_OK`：
- 23:00 - 08:00 之间（夜间模式）
- 最近 30 分钟内刚检查过
- 所有检查项都正常
- 没有活跃的开发任务

---

## 恢复机制

如果 Claude Code 崩溃：
1. 读取最近日志：`tail -50 ~/.openclaw/logs/gateway.log`
2. 分析崩溃原因
3. 从断点恢复：读取 `memory/dev-progress.md`
4. 重启任务并通知主人
