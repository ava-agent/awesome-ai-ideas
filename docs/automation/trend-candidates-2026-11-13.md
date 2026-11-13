# AI 趋势候选扫描 · 2026-11-13

基线为 [ava-agent/awesome-ai-ideas 的 main 快照](https://github.com/ava-agent/awesome-ai-ideas/tree/9c4e305800a45d5f7ef0a8fc6b4519dcb9f23fa3)。对照 README、路线图、追踪器、在库的 6 月 26 日趋势报告及历史扫描记忆，保留 1 项候选。主扫描窗口为 11 月 6–13 日，法律方向补查 10 月 27 日和 11 月 4 日的产品变更。

## 并购尽调备忘录的变更复核

**证据。** Harvey 于 11 月 4 日发布 Review Tables Sync，11 月 9 日公开介绍该功能。新文件或新版文件进入 Vault 后会触发过期提示，编辑者同步后，新版以新行加入，已核验的旧行保留。Litera 则于 10 月 27 日发布从 Kira 或 Lito 的审阅表导出生成风险报告初稿的能力。两家厂商分别展示了上游文件持续更新和下游报告基于一次导出的工作方式。现有证据来自产品说明，实际返工频率和购买意愿仍待验证。[Harvey 发布记录](https://help.harvey.ai/release-notes/category/review-tables) · [Harvey 11 月 9 日公告](https://www.harvey.ai/blog/review-table-sync) · [Harvey 审阅表操作说明](https://help-harvey.vercel.app/articles/using-review-tables) · [Litera 10 月 27 日公告](https://www.litera.com/blog/review-report-introducing-first-draft-red-flags-report)

**用户和痛点假设。** 面向负责签发买方并购尽调备忘录的主办律师和项目助理。若签核后收到新版合同，助理要核查备忘录里哪些结论仍引用旧条款，例如变更控制条款的第三方同意要求，并请原审阅人复核受影响段落。

**产品假设。** 在本地读取前后两批审阅表导出和一份 Word 备忘录，用数据室文档编号、版本号和条款引用定位可能失效的段落。输出包含旧版、新版和引用依据的复核清单。版本映射缺失时标记待人工确认，段落更新由律师签核。

**重复风险中等。** [AI 合同阅读助手](../../idea-tracker.json)覆盖单份合同的条款分析，[LegalCompass AI](../../prs/1200-legalcompass-ai.md)涵盖合规与法律文档工作。6 月 26 日的诉讼候选已有跨阶段一致性概念，历史扫描也曾提出法务连接器完整性核对。本轮只验证已签核的并购交付物在合同换版后是否需要重审。如果客户的文档比较或审阅表原生功能已能直接指出受影响的备忘录段落，独立工具的空间有限。[6 月 26 日趋势报告](trend-candidates-2026-06-26.md)

**低成本验证。** 请 3 位并购律师用脱敏历史样本或律师编写的模拟样本，回放 10 处修订，先标出应重审的段落，再比较现有流程与脚本生成的复核清单。假设验收门槛为预先标为关键的受影响段落零遗漏、人工复核耗时中位数下降至少 30%，且至少 2 位律师确认近三个月遇到过类似返工。若出现关键遗漏、导出缺少可稳定匹配的版本标识，或现有工具已达到同等结果，则放弃独立产品假设。

## 本轮其余信号

- 开发工具方面，GitHub 11 月 6 日公开了 Copilot 审阅归属和配置 API 的扩展。通用审阅归因与已有 PR 变更影响分析、历史 Coding Agent Validation Queue 重叠，本轮没有获得独立流程需求的证据。[GitHub Changelog](https://github.blog/changelog/2026-11-06-copilot-code-review-api-management-and-review-overview-updates/)
- 医疗方面，Abridge 11 月 12 日公告称其助手可以引用院内临床路径。公开资料确认了产品功能，本轮尚未找到足够证据证明医院需要独立的路径维护或审计工具。[Abridge 公告](https://www.abridge.com/press-release/local-pathways-abridge-assistant)
