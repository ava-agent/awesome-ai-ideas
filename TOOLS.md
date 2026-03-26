# TOOLS.md - Local Environment Notes

## Network

- **System Proxy:** http://127.0.0.1:7897 (Clash/V2Ray)
- **Note:** 海外服务 (Telegram, GitHub, npm) 需要通过代理访问
- **Gateway Proxy:** 已在 LaunchAgent plist 中配置 HTTP_PROXY/HTTPS_PROXY

## Gateway

- **Port:** 18789
- **Bind:** loopback (127.0.0.1)
- **Auth:** token
- **Dashboard:** http://127.0.0.1:18789/
- **Service:** LaunchAgent (ai.openclaw.gateway)
- **Plist:** ~/Library/LaunchAgents/ai.openclaw.gateway.plist

## Paths

- **OpenClaw Config:** ~/.openclaw/openclaw.json
- **Credentials:** ~/.openclaw/credentials/ (chmod 700)
- **Workspace:** ~/.openclaw/workspace/
- **Skills:** ~/.openclaw/workspace/skills/
- **Logs:** ~/.openclaw/logs/
- **Node.js:** /usr/local/bin/node
- **npm Global:** ~/.npm-global/lib/node_modules/

## AI Model

- **Provider:** Z.AI (智谱 AI)
- **Base URL:** https://open.bigmodel.cn/api/coding/paas/v4
- **Primary Model:** zai/glm-5
- **Available Models:** glm-5, glm-4.7, glm-4.7-flash, glm-4.7-flashx

## Agents

| Agent | Workspace | Purpose |
|-------|-----------|---------|
| main | ~/.openclaw/workspace | 主 Agent (咕噜) |
| ai-news | ~/.openclaw/workspace-ai-news | AI 资讯助手 (每日新闻) |
| coder | ~/.openclaw/workspace-coder | Coding Agent |

## Known Issues

- `openclaw gateway install --force` 会覆盖 plist，丢失手动添加的代理配置和 PATH
- 每次重装 Gateway 后需重新在 plist 中添加 HTTP_PROXY/HTTPS_PROXY 和 ~/homebrew/bin
- LaunchAgent 环境变量修改后需 `launchctl unload/load`，普通 restart 不生效
- /usr/local/bin/brew 是 Intel 版 (不可用)，用 ~/homebrew/bin/brew 代替
- peekaboo 需要 macOS 15.0+，当前 14.7.7 不兼容

## Installed System Tools

- **Node.js:** v24.4.1
- **npm:** global
- **Homebrew (ARM):** ~/homebrew/bin/brew (用户空间安装，非标准路径)
- **Homebrew (Intel):** /usr/local/bin/brew (不可用，无 bottles)
- **OpenClaw:** 2026.3.13

## Skill CLI Tools

| Tool | Version | Install Method | Path |
|------|---------|----------------|------|
| himalaya | v1.2.0 | GitHub binary | /usr/local/bin/himalaya |
| tmux | 3.6a | ~/homebrew | ~/homebrew/bin/tmux → /usr/local/bin/tmux |
| summarize | 0.12.0 | ~/homebrew (steipete/tap) | ~/homebrew/bin/summarize → /usr/local/bin/summarize |
| codexbar | 0.18.0 | ~/homebrew cask (steipete/tap) | /Applications/CodexBar.app |
| memo | 0.5.1 | ~/homebrew (antoniorodr/memo) | ~/homebrew/bin/memo → /usr/local/bin/memo |
| remindctl | 0.1.1 | ~/homebrew (steipete/tap) | ~/homebrew/bin/remindctl → /usr/local/bin/remindctl |
| mcporter | npm | npm i -g mcporter | ~/.npm-global/bin/mcporter |
| yt-dlp | 2025.10.14 | pip3 | /usr/local/bin/yt-dlp |

## Missing (可选安装)

- **gh** - GitHub CLI
- **jq** - JSON processor
- **ffmpeg** - Media processing
- **go** - Go language (needed for blogwatcher skill)
- **nano-pdf** - Python ≥ 3.10 needed (use ~/homebrew/bin/python3.13)
