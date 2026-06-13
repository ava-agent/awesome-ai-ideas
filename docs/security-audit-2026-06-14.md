# npm 生产依赖安全审计报告 - 2026-06-14

- 审计范围：`/Users/wangshihao/projects/openclaws`
- 执行时间：2026/6/14 GMT+8 0:10:47
- 模式：只读（未运行 `npm audit fix`，未升级或修改依赖）
- 筛选条件：目录名不含 `-bak`、真实 Git 仓库、工作区干净、同时存在 `package.json` 和 `package-lock.json`

## 总览

符合条件并完成审计的仓库数：4

| Severity | Count |
| --- | ---: |
| critical | 0 |
| high | 3 |
| moderate | 25 |
| low | 0 |

## 建议

- 优先处理 critical/high 漏洞：查看下方受影响包与 npm audit 建议，在独立修复分支中评估升级或替换依赖。
- 对生产路径上的漏洞先做影响面确认，再运行测试；本次报告未执行自动修复。
- 不建议在自动审计任务中直接运行 `npm audit fix`；修复应通过单独 PR 审查。

## 仓库明细

### ai-appointment-manager

- 路径：`/Users/wangshihao/projects/openclaws/ai-appointment-manager`
- npm audit exit code：1（发现漏洞导致非零退出码属正常）
- 漏洞计数：critical 0, high 1, moderate 8, low 0

| Package | Severity | Range | Via | Fix available |
| --- | --- | --- | --- | --- |
| nodemailer | high | <=8.0.4 | Nodemailer: Email to an unintended domain can occur due to Interpretation Conflict; Nodemailer’s addressparser is vulnerable to DoS caused by recursive calls; Nodemailer has SMTP command injection due to unsanitized `envelope.size` parameter | {"name":"nodemailer","version":"8.0.11","isSemVerMajor":true} |
| body-parser | moderate | 1.20.3 - 1.20.4 \|\| 2.0.0-beta.1 - 2.0.2 | qs | true |
| express | moderate | 4.21.0 - 4.22.1 \|\| 5.0.0-alpha.1 - 5.0.1 | qs | true |
| gaxios | moderate | 6.4.0 - 6.7.1 | uuid | true |
| googleapis | moderate | 33.0.0 - 149.0.0 | googleapis-common | {"name":"googleapis","version":"173.0.0","isSemVerMajor":true} |
| googleapis-common | moderate | <=7.2.0 | uuid | {"name":"googleapis","version":"173.0.0","isSemVerMajor":true} |
| node-cron | moderate | 3.0.2 - 3.0.3 | uuid | {"name":"node-cron","version":"4.2.1","isSemVerMajor":true} |
| qs | moderate | 6.11.1 - 6.15.1 | qs has a remotely triggerable DoS: qs.stringify crashes with TypeError on null/undefined entries in comma-format arrays when encodeValuesOnly is set | true |
| uuid | moderate | <11.1.1 | uuid: Missing buffer bounds check in v3/v5/v6 when buf is provided | {"name":"node-cron","version":"4.2.1","isSemVerMajor":true} |

### ai-family-health-guardian

- 路径：`/Users/wangshihao/projects/openclaws/ai-family-health-guardian`
- npm audit exit code：1（发现漏洞导致非零退出码属正常）
- 漏洞计数：critical 0, high 1, moderate 8, low 0

| Package | Severity | Range | Via | Fix available |
| --- | --- | --- | --- | --- |
| nodemailer | high | <=8.0.4 | Nodemailer: Email to an unintended domain can occur due to Interpretation Conflict; Nodemailer’s addressparser is vulnerable to DoS caused by recursive calls; Nodemailer has SMTP command injection due to unsanitized `envelope.size` parameter | {"name":"nodemailer","version":"8.0.11","isSemVerMajor":true} |
| body-parser | moderate | 1.20.3 - 1.20.4 \|\| 2.0.0-beta.1 - 2.0.2 | qs | true |
| engine.io | moderate | 0.7.8 - 0.7.9 \|\| 6.0.0 - 6.6.7 | ws | true |
| express | moderate | 4.21.0 - 4.22.1 \|\| 5.0.0-alpha.1 - 5.0.1 | qs | true |
| ip-address | moderate | <=10.1.0 | ip-address has XSS in Address6 HTML-emitting methods | true |
| joi | moderate | <17.13.4 | joi has an uncaught RangeError on deeply nested input through recursive `link()` schemas | true |
| qs | moderate | 6.11.1 - 6.15.1 | qs has a remotely triggerable DoS: qs.stringify crashes with TypeError on null/undefined entries in comma-format arrays when encodeValuesOnly is set | true |
| socket.io-adapter | moderate | 2.5.2 - 2.5.6 | ws | true |
| ws | moderate | 8.0.0 - 8.20.0 | ws: Uninitialized memory disclosure | true |

### ai-voice-notes-organizer

- 路径：`/Users/wangshihao/projects/openclaws/ai-voice-notes-organizer`
- npm audit exit code：1（发现漏洞导致非零退出码属正常）
- 漏洞计数：critical 0, high 1, moderate 4, low 0

| Package | Severity | Range | Via | Fix available |
| --- | --- | --- | --- | --- |
| lodash | high | <=4.17.23 | lodash vulnerable to Code Injection via `_.template` imports key names; lodash vulnerable to Prototype Pollution via array path bypass in `_.unset` and `_.omit` | true |
| body-parser | moderate | 1.20.3 - 1.20.4 \|\| 2.0.0-beta.1 - 2.0.2 | qs | true |
| express | moderate | 4.21.0 - 4.22.1 \|\| 5.0.0-alpha.1 - 5.0.1 | qs | true |
| qs | moderate | 6.11.1 - 6.15.1 | qs has a remotely triggerable DoS: qs.stringify crashes with TypeError on null/undefined entries in comma-format arrays when encodeValuesOnly is set | true |
| uuid | moderate | <11.1.1 | uuid: Missing buffer bounds check in v3/v5/v6 when buf is provided | {"name":"uuid","version":"14.0.0","isSemVerMajor":true} |

### ai-workspace-orchestrator

- 路径：`/Users/wangshihao/projects/openclaws/ai-workspace-orchestrator`
- npm audit exit code：1（发现漏洞导致非零退出码属正常）
- 漏洞计数：critical 0, high 0, moderate 5, low 0

| Package | Severity | Range | Via | Fix available |
| --- | --- | --- | --- | --- |
| body-parser | moderate | 1.20.3 - 1.20.4 \|\| 2.0.0-beta.1 - 2.0.2 | qs | true |
| express | moderate | 4.21.0 - 4.22.1 \|\| 5.0.0-alpha.1 - 5.0.1 | qs | true |
| joi | moderate | <17.13.4 | joi has an uncaught RangeError on deeply nested input through recursive `link()` schemas | true |
| qs | moderate | 6.11.1 - 6.15.1 | qs has a remotely triggerable DoS: qs.stringify crashes with TypeError on null/undefined entries in comma-format arrays when encodeValuesOnly is set | true |
| uuid | moderate | <11.1.1 | uuid: Missing buffer bounds check in v3/v5/v6 when buf is provided | {"name":"uuid","version":"14.0.0","isSemVerMajor":true} |

## 排除项

| Directory | Reason |
| --- | --- |
| .git | 不是真实 Git 仓库（缺少 .git 目录） |
| .tmp | 不是真实 Git 仓库（缺少 .git 目录） |
| ai-carbon-footprint-tracker | 工作区不干净 |
| ai-career-soft-skills-coach-bak | 目录名包含 -bak |
| ai-contract-reader | 缺少 package.json 或 package-lock.json |
| ai-email-manager | 缺少 package.json 或 package-lock.json |
| ai-error-diagnostician | 工作区不干净 |
| ai-gardening-designer | 工作区不干净 |
| ai-interview-coach | 工作区不干净 |
| ai-rental-detective | 工作区不干净 |
| appointment-manager | 缺少 package.json 或 package-lock.json |
| awesome-ai-idea | 不是真实 Git 仓库（缺少 .git 目录） |
| awesome-ai-ideas | 缺少 package.json 或 package-lock.json |
| career-soft-skills-coach | 缺少 package.json 或 package-lock.json |
| code-knowledge-map-generator | 缺少 package.json 或 package-lock.json |
| docs | 不是真实 Git 仓库（缺少 .git 目录） |
| error-diagnostician | 缺少 package.json 或 package-lock.json |
| logs | 不是真实 Git 仓库（缺少 .git 目录） |
| memory | 不是真实 Git 仓库（缺少 .git 目录） |
| romance-of-three-claws | 工作区不干净 |
| src | 不是真实 Git 仓库（缺少 .git 目录） |
| utils | 不是真实 Git 仓库（缺少 .git 目录） |
| workspace | 不是真实 Git 仓库（缺少 .git 目录） |
