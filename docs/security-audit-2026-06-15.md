# 安全审计报告（只读）- 2026-06-15

- 执行时间：2026-06-15 14:00 Asia/Shanghai
- 审计范围：`/Users/wangshihao/projects/openclaws` 下真实 Git 仓库
- 筛选条件：目录名不含 `-bak`、工作区干净、同时存在 `package.json` 与 `package-lock.json`
- 审计命令：`npm audit --omit=dev --json`
- 约束：只读审计；未运行 `npm audit fix`；未升级或修改依赖；未 push。

## 仓库筛选结果

纳入审计的仓库：

- `ai-appointment-manager`
- `ai-workspace-orchestrator`
- `ai-family-health-guardian`
- `ai-voice-notes-organizer`

因工作区不干净而跳过的仓库：

- `ai-gardening-designer`
- `ai-rental-detective`
- `ai-error-diagnostician`
- `ai-interview-coach`
- `romance-of-three-claws`
- `ai-carbon-footprint-tracker`

## 总览

| 仓库 | Critical | High | Moderate | Low | Total | `npm audit` exit code |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `ai-appointment-manager` | 0 | 1 | 8 | 0 | 9 | 1 |
| `ai-workspace-orchestrator` | 0 | 0 | 5 | 0 | 5 | 1 |
| `ai-family-health-guardian` | 0 | 1 | 8 | 0 | 9 | 1 |
| `ai-voice-notes-organizer` | 0 | 1 | 4 | 0 | 5 | 1 |
| **合计** | **0** | **3** | **25** | **0** | **28** |  |

> 说明：`npm audit` 因发现漏洞返回非零属于预期结果，本次未因此中断审计。

## 详细结果与建议

### `ai-appointment-manager`

漏洞数量：Critical 0 / High 1 / Moderate 8 / Low 0，总计 9。

主要问题：

- `nodemailer`：High，影响范围 `<=8.0.4`；修复可用但需要升级到 `nodemailer@9.0.0`，属于 semver major。
- `googleapis` / `googleapis-common`：Moderate，修复建议升级到 `googleapis@173.0.0`，属于 semver major。
- `node-cron` / `uuid`：Moderate，修复建议升级到 `node-cron@4.2.1`，属于 semver major。
- `express` / `body-parser` / `qs`：Moderate，存在可用修复。

建议：

1. 优先评估 `nodemailer` 升级到 9.x 的兼容性，并补充邮件发送相关回归测试。
2. 对 `googleapis` major 升级单独开分支验证 OAuth、日历/接口调用等集成路径。
3. `express`、`body-parser`、`qs` 可作为较低风险依赖修复组处理，但仍需运行服务启动和 API 冒烟测试。
4. `node-cron` major 升级需要验证定时任务表达式、时区和任务调度行为。

### `ai-workspace-orchestrator`

漏洞数量：Critical 0 / High 0 / Moderate 5 / Low 0，总计 5。

主要问题：

- `express` / `body-parser` / `qs`：Moderate，存在可用修复。
- `joi`：Moderate，影响范围 `<17.13.4`，存在可用修复。
- `uuid`：Moderate，修复建议升级到 `uuid@14.0.0`，属于 semver major。

建议：

1. 优先处理 `express`、`body-parser`、`qs` 与 `joi` 的非重大版本修复，并运行 API 参数校验相关测试。
2. `uuid` 升级到 14.x 可能涉及 ESM/API 兼容性变化，建议单独验证导入方式和 ID 生成调用点。
3. 修复后重新执行 `npm audit --omit=dev --json` 确认生产依赖漏洞清零或降级。

### `ai-family-health-guardian`

漏洞数量：Critical 0 / High 1 / Moderate 8 / Low 0，总计 9。

主要问题：

- `nodemailer`：High，影响范围 `<=8.0.4`；修复可用但需要升级到 `nodemailer@9.0.0`，属于 semver major。
- `express` / `body-parser` / `qs`：Moderate，存在可用修复。
- `socket.io-adapter` / `engine.io` / `ws`：Moderate，存在可用修复，影响实时通信链路。
- `joi`：Moderate，影响范围 `<17.13.4`，存在可用修复。
- `ip-address`：Moderate，影响范围 `<=10.1.0`，存在可用修复。

建议：

1. 该项目涉及健康数据场景，应将 `nodemailer` High 漏洞作为最高优先级处理，并验证通知邮件链路。
2. 实时通信相关依赖（`socket.io-adapter`、`engine.io`、`ws`）建议成组升级，重点测试连接建立、消息广播、断线重连和鉴权边界。
3. 参数校验和地址解析相关依赖（`joi`、`ip-address`）修复后需补充输入校验回归。
4. 在修复前避免扩大公网暴露面；修复后重新运行生产依赖 audit。

### `ai-voice-notes-organizer`

漏洞数量：Critical 0 / High 1 / Moderate 4 / Low 0，总计 5。

主要问题：

- `lodash`：High，影响范围 `<=4.17.23`；存在可用修复。
- `express` / `body-parser` / `qs`：Moderate，存在可用修复。
- `uuid`：Moderate，修复建议升级到 `uuid@14.0.0`，属于 semver major。

建议：

1. 优先修复 `lodash` High 漏洞，检查锁文件中是否可通过补丁版本提升解决。
2. `express`、`body-parser`、`qs` 可作为 Web 框架依赖修复组处理，修复后运行上传/转写/API 冒烟测试。
3. `uuid` major 升级需验证 CommonJS/ESM 导入兼容性。

## 总体建议

1. 本次未发现 Critical；High 集中在 `nodemailer` 与 `lodash`，建议优先处理。
2. 多个仓库共享 `express` / `body-parser` / `qs` Moderate 链路，可统一制定修复模板并逐仓库验证。
3. 涉及 semver major 的修复（`nodemailer`、`googleapis`、`node-cron`、`uuid`）不要直接自动升级，应建立独立 PR 并补充兼容性测试。
4. 修复顺序建议：
   - 第一优先级：`ai-family-health-guardian` 的 High 漏洞与实时通信链路。
   - 第二优先级：`ai-appointment-manager` 的 `nodemailer` / `googleapis` / `node-cron`。
   - 第三优先级：`ai-voice-notes-organizer` 的 `lodash`。
   - 第四优先级：`ai-workspace-orchestrator` 的 Moderate 漏洞清理。
5. 每个仓库修复后均应重新运行 `npm audit --omit=dev --json`，并执行项目现有测试或至少服务启动/API 冒烟验证。
