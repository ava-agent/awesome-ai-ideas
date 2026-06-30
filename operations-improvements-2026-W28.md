# 运营改进建议 - 2026-W28

## 识别的改进点

### 1. 同步 idea-tracker.json 与最新文件
- 问题：idea-tracker.json 最后同步时间是 2026-04-23，很多新 idea 文件未被追踪
- 建议：运行 idea-evaluate 任务同步所有新 idea 文件

### 2. 定期清理临时验证脚本
- 问题：仓库根目录有多个 hermes-verify-*.py 临时脚本，未被 git 跟踪
- 建议：制定临时脚本清理规则，每周定期清理

### 3. 精选 Ideas 区域更新
- 问题：README 的精选 Ideas 部分已有一段时间未更新
- 建议：每周从 idea-tracker.json 中挑选 top 3 high-value idea 更新到 README

---
**记录时间**：2026-06-30
