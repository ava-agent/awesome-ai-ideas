# 安全审计报告 - 2026-06-22

本次审计范围：`/Users/wangshihao/projects/openclaws` 下，目录名不含 `-bak`、工作区干净、同时存在 `package.json` 和 `package-lock.json` 的 Git 仓库。

## 符合条件的仓库

1. `/Users/wangshihao/projects/openclaws/ai-appointment-manager`
2. `/Users/wangshihao/projects/openclaws/ai-family-health-guardian`
3. `/Users/wangshihao/projects/openclaws/ai-voice-notes-organizer`
4. `/Users/wangshihao/projects/openclaws/ai-workspace-orchestrator`

## 漏洞汇总

按 severity 统计：

| 级别     | 数量 |
|----------|------|
| critical | 0    |
| high     | 7    |
| moderate | 24   |
| low      | 0    |
| **总计** | **31** |

## 各仓库详情

### 1. ai-appointment-manager

| 级别     | 数量 |
|----------|------|
| critical | 0    |
| high     | 2    |
| moderate | 8    |
| low      | 0    |

主要漏洞：
- form-data: CRLF injection (high)
- nodemailer: 多个漏洞包括 DoS 和 SMTP 命令注入 (high + 多个 moderate)
- express/body-parser: qs DoS (moderate)
- uuid: 缓冲区边界检查缺失 (moderate)

### 2. ai-family-health-guardian

| 级别     | 数量 |
|----------|------|
| critical | 0    |
| high     | 3    |
| moderate | 7    |
| low      | 0    |

主要漏洞：
- form-data: CRLF injection (high)
- nodemailer: 多个漏洞包括 DoS 和 任意文件读取 (high + 多个 moderate)
- ws: 内存耗尽 DoS (high)
- express/body-parser: qs DoS (moderate)
- joi: 未捕获 RangeError (moderate)

### 3. ai-voice-notes-organizer

| 级别     | 数量 |
|----------|------|
| critical | 0    |
| high     | 2    |
| moderate | 4    |
| low      | 0    |

主要漏洞：
- form-data: CRLF injection (high)
- lodash: 代码注入和原型污染 (high + moderate)
- express/body-parser: qs DoS (moderate)
- uuid: 缓冲区边界检查缺失 (moderate)

### 4. ai-workspace-orchestrator

| 级别     | 数量 |
|----------|------|
| critical | 0    |
| high     | 0    |
| moderate | 5    |
| low      | 0    |

主要漏洞：
- express/body-parser: qs DoS (moderate)
- joi: 未捕获 RangeError (moderate)
- uuid: 缓冲区边界检查缺失 (moderate)

## 建议

所有发现的漏洞都有可用修复版本，但本次审计**未执行** `npm audit fix`，建议：

1. 按严重性顺序评估修复：优先处理 7 个 high 级别的漏洞
2. 注意大多数修复涉及主版本变更，可能存在不兼容性
3. 修复后需要重新测试功能
4. 定期重复审计
