# 生产依赖安全审计报告（只读）

- 审计日期：2026-06-14（Asia/Shanghai）
- 审计对象：`/Users/wangshihao/projects/openclaws/ai-contract-reader`
- 仓库分支：`main`
- 仓库提交：`3b1bb5b`
- 选择规则：枚举 `/Users/wangshihao/projects/openclaws` 下真实 Git 仓库；选择第一个包含 `package.json`、目录名不含 `-bak`、且工作区干净的仓库。
- 执行命令：`npm audit --omit=dev --json`
- 只读原则：未执行 `npm audit fix`，未升级或修改依赖。

## 结果摘要

本次审计未能得到漏洞统计结果，因为 `npm audit` 要求项目存在 lockfile，而目标仓库当前没有 `package-lock.json` / `npm-shrinkwrap.json`。

| 等级 | 数量 |
| --- | ---: |
| critical | 未统计 |
| high | 未统计 |
| moderate | 未统计 |
| low | 未统计 |

## npm audit 输出

```text
npm ERR! code ENOLOCK
npm ERR! audit This command requires an existing lockfile.
npm ERR! audit Try creating one first with: npm i --package-lock-only
npm ERR! audit Original error: loadVirtual requires existing shrinkwrap file
{
  "error": {
    "code": "ENOLOCK",
    "summary": "This command requires an existing lockfile.",
    "detail": "Try creating one first with: npm i --package-lock-only\nOriginal error: loadVirtual requires existing shrinkwrap file"
  }
}
```

## 建议

1. 为 `ai-contract-reader` 生成并提交 lockfile（例如在后续维护窗口中执行 `npm install --package-lock-only` 或标准 `npm install`，经人工确认后提交）。本次任务要求只读，因此没有生成 lockfile。
2. lockfile 提交后重新运行：`npm audit --omit=dev --json`，再统计 `critical/high/moderate/low`。
3. 若后续审计发现漏洞，优先处理 `critical` 和 `high`；修复前先查看 `npm audit` 的 `fixAvailable` 信息和破坏性升级风险，不要直接在自动任务中运行 `npm audit fix`。
4. 将 lockfile 纳入 CI 检查，避免生产依赖审计因缺少 lockfile 而失效。
