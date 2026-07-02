# 运营改进建议 - 2026-W29

## 识别的改进点

### 1. 统一脚本目录管理
- 问题：根目录和 scripts/ 目录都存放脚本，造成混乱
  - 根目录：fetch_huggingface_trends.py, predict_trends.py, search_arxiv.py, update_idea_tracker.py, update_stats.py
  - scripts/：已有多个 fetch_* 脚本
- 建议：将所有脚本统一移动到 scripts/ 目录

### 2. 整理 untracked 文件
- 问题：有 20+ 个 untracked 文件（临时脚本、idea 文件、配置等）
- 建议：要么提交到 git，要么清理掉

### 3. 统一 idea 生成/命名流程
- 问题：发现 ideas/ 目录下 issue-*.md 文件没有通过 issue → PR 流程直接生成
- 建议：统一通过 GitHub issue → PR 流程管理所有 idea 文件

---
**记录时间**：2026-07-02
