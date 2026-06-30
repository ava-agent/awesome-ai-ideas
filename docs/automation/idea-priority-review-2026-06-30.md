# High-Value Idea Priority Review - 2026-06-30

- Run time: 2026-06-30 10:04 +08:00
- Repository: `ava-agent/awesome-ai-ideas`
- Scope: `docs/automation-runbook.md`, `AGENTS.md`, `idea-tracker.json`, `docs/roadmap.md`, `ideas/`, `prs/`, recent `docs/automation/` reports, and live GitHub issue/PR checks through `scripts/gh-gcm.ps1`
- Decision rule: favor high-scoring ideas with near-term MVP evidence, clear buyer/user pain, and a concrete validation path; downgrade ideas with missing source docs, stale downstream repos, or over-broad first releases.

## Executive Decision

| Rank | Idea | Decision | Why now | Suggested owner | Next artifact |
| ---: | --- | --- | --- | --- | --- |
| 1 | DocAI Studio | Start MVP spec immediately | Highest structured score tied with LogiChain, source proposal is complete, and MVP scope is already constrained to document parsing + AI understanding + library/search/export | Product + full-stack builder | `docs/mvp/docai-studio-mvp-spec.md` |
| 2 | MfgKnowledge AI | Merge/accept idea document, then run discovery sprint | Live GitHub labels mark it `quality:high`; PR #1437 is clean and closes #1426; MVP can start from knowledge/RAG + report automation before harder vision/predictive modules | Manufacturing domain owner + data/RAG engineer | `docs/ideas/issue-1426.md`, then `docs/mvp/mfgknowledge-ai-discovery.md` |
| 3 | SupplyGuard AI | Advance as the supply-chain MVP path, not the broader SupplyChain OS | Strong vertical B2B pain and 1-2 month MVP exists; narrower than SupplyChain OS and better evidenced than missing LogiChain source file | B2B supply-chain/compliance owner | `docs/mvp/supplyguard-ai-validation-plan.md` |

Not selected for immediate MVP:

- `LogiChain AI` has `totalScore=8.6` and `priority=1`, but `idea-tracker.json` points to `供应链智能-LogiChain-AI.md`, which is not present in the current tree. It should be reconciled before using it as the execution source.
- `AI Workspace Orchestrator` remains high score (`8.2`) and in progress, but the 2026-06-27 workspace audit reports the downstream repo as diverged (`behind=15`, `ahead=208`). This is a repo reconciliation task before a new MVP push.
- `AI Resume Doctor` is high score (`8.4`) and roadmap-aligned, but the tracker points to `prs/0140-ai-resume-doctor.md`, which is not present in the current tree. It needs source recovery before prioritization.
- `SupplyChain OS AI` is promising but too broad for first MVP because it combines supply chain, compliance, security, customer support, analytics, and workflow automation.

## Evidence Base

### Repository and Automation Evidence

- `idea-tracker.json` last evaluation is `2026-06-27T02:30:00Z`; `docs/roadmap.md` says the tracker has 60 ideas, 16 high-value ideas waiting, and one in-progress project.
- `docs/roadmap.md` next priority is older B2C/prosumer sequence: AI职场软技能导师 -> AI简历诊断师 -> AI音乐创作伙伴 -> AI个人成长教练. This should be updated because recent B2B proposals now have clearer MVP and monetization evidence.
- `docs/automation/github-pr-ci-monitor-2026-06-29.md` shows GitHub access was OK, but current `main` has no `.github/workflows`, so PRs have no CI signal.
- Live GitHub check on 2026-06-30 shows open PR #1437 for `MfgKnowledge AI` is `CLEAN`, adds `docs/ideas/issue-1426.md`, and closes #1426.
- Live GitHub issue #1426 has labels `quality:high`, `idea`, `ai-agents`, `knowledge-graph`, and `rag`.
- Live GitHub issue queue has newer issues #1447-#1443, but none in the sampled newest queue had quality labels comparable to #1426.

### Candidate Evidence

#### 1. DocAI Studio

- Source: `prs/1444-docai-studio.md`
- Tracker status: `high-value`
- Score: `8.6`
- Category: Research & Content Creation
- Strengths in source doc:
  - Unified multi-format support across PDF, DOCX, scanned images, handwritten notes, tables, formulas, Markdown, and LaTeX.
  - Explicit MVP plan for months 1-2: upload, document type detection, OCR, table/formula extraction, summarization, key phrase/topic extraction, citation/reference identification, entity recognition, basic search, export, and user auth.
  - Clear pricing tiers: Free, Professional, Team, Enterprise, plus API usage add-on.
  - Validation metrics are concrete: 500 beta users, 30% weekly active, NPS 40+, OCR accuracy targets, processing speed target, MRR targets.

Why now:

- The proposal already contains enough detail to move from idea to MVP spec without another ideation pass.
- Document intelligence is a reusable wedge for this repository's own workflow: PR/idea docs, automation reports, PDFs, and research notes can become internal dogfood.
- The MVP can be built without needing proprietary enterprise integrations on day one.

Gaps:

- Needs source-of-truth decision on parser stack and hosting cost ceiling.
- MinerU/OpenAI/Claude references need licensing, deployment, and privacy checks before committing architecture.
- Knowledge graph should be phase 2; including it in MVP risks expanding scope.

Next validation actions:

1. Build a 20-document benchmark set: PDFs, DOCX, scanned images, tables, formulas, bilingual docs.
2. Prototype parser pipeline and compare parse quality, latency, and cost per document.
3. Interview 5 target users: researcher, archivist/librarian, content creator, enterprise knowledge worker, and internal repo maintainer.
4. Define MVP acceptance: upload -> parse -> summary/entities/topics -> search/export in one web workflow.

Recommended owner/product:

- Owner: product + full-stack builder with document parsing experience.
- First product artifact: `docs/mvp/docai-studio-mvp-spec.md`.
- First build artifact: parser benchmark harness plus a minimal document library web app.

#### 2. MfgKnowledge AI

- Source: live GitHub issue #1426 and PR #1437
- GitHub status: issue #1426 is `quality:high`; PR #1437 is clean and adds the formal document.
- Core pain: manufacturing expertise loss, ERP/MES/SCADA data silos, manual quality inspection, delayed equipment fault detection.
- MVP wedge in issue body:
  - Start with process knowledge digitization and cross-system production report automation.
  - Defer harder visual quality inspection and predictive maintenance until after knowledge/data workflows prove value.

Why now:

- It has stronger live triage signal than many local high-value ideas because GitHub labels already classify it as high quality.
- It fits B2B willingness-to-pay better than many consumer wellness/learning ideas.
- It can be validated incrementally with low-risk artifacts: RAG knowledge base, production daily/weekly report automation, and a factory Q&A assistant.

Gaps:

- The PR is not merged into local `main`, so the source doc is not yet in the local tree.
- Needs a narrow pilot persona: factory manager, process engineer, or manufacturing digital transformation owner.
- Needs sample domain data. Without anonymized SOPs, production reports, or machine logs, the MVP will remain a generic RAG demo.

Next validation actions:

1. Merge or manually accept PR #1437 after human review, since current repo has no CI workflow signal.
2. Create an interview script for 5 manufacturing operators/managers focused on daily report pain and process knowledge loss.
3. Build a small demo corpus from public/manual manufacturing SOP examples and simulate Q&A + daily report generation.
4. Define phase boundary: phase 1 is knowledge/RAG and reporting; phase 2 is vision quality inspection; phase 3 is predictive maintenance.

Recommended owner/product:

- Owner: manufacturing domain owner + data/RAG engineer.
- First product artifact: accepted `docs/ideas/issue-1426.md`, then `docs/mvp/mfgknowledge-ai-discovery.md`.
- First build artifact: local-only RAG prototype with citations and generated production report.

#### 3. SupplyGuard AI

- Source: `ideas/issue-1359--for-Supply-Chain-Managers-Compliance-Officers-Risk-Managers-SupplyGuard-AI---From-fragmented-supply-chain-risk-and-compliance-chaos-to-intelligent-real-time-governance-ecosystem.md`
- Score evidence: local tracker has two SupplyGuard/BuildSafe-style June entries in the high-value range; the supply-chain cluster also contains `LogiChain AI` at `8.6`, but the LogiChain source file is missing.
- Core pain: supplier risk, ESG/CSRD/UFLPA-style compliance, fragmented supply-chain systems, and reactive disruption response.
- MVP in source doc:
  - Risk monitoring engine foundation.
  - Basic compliance rule configuration.
  - Supplier data ingestion and visualization.
  - Simple risk warning.
  - Web dashboard and API design.

Why now:

- Supply-chain risk/compliance is a clearer B2B buyer problem than broad personal productivity ideas.
- The repo has multiple supply-chain documents (`SupplyGuard AI`, `SupplyChain OS AI`, `SupplyChain AI Pro`, `ChainShield AI`, and stale PR #1368 `ChainVision AI`), so consolidation can unlock one stronger direction instead of more duplicate proposals.
- SupplyGuard is narrower than SupplyChain OS and has a cleaner 1-2 month MVP path.

Gaps:

- Need to reconcile duplication across `LogiChain`, `SupplyGuard`, `SupplyChain OS`, `SupplyChain AI Pro`, `ChainShield`, and `ChainVision`.
- Need real or representative supplier/risk/compliance data sources.
- Need a first vertical, such as electronics manufacturing, retail importers, or procurement teams managing ESG/UFLPA risk.

Next validation actions:

1. Create a supply-chain idea consolidation note mapping duplicated features and naming one canonical MVP.
2. Prototype a supplier-risk dashboard with synthetic supplier records, event feed, compliance checklist, and alert scoring.
3. Interview 3 supply-chain/procurement/compliance users to rank risk visibility, compliance reporting, and supplier scoring pain.
4. Decide whether stale PR #1368 should be merged, closed, or mined for requirements.

Recommended owner/product:

- Owner: B2B supply-chain/compliance owner.
- First product artifact: `docs/mvp/supplyguard-ai-validation-plan.md`.
- First build artifact: supplier risk scoring demo with explainable alerts.

## Recommended 7-Day Plan

1. Day 1: Create MVP spec for DocAI Studio and freeze phase-1 scope.
2. Day 2: Run parser benchmark on 20 representative documents and record quality/cost/latency.
3. Day 3: Review and merge or reject PR #1437 for MfgKnowledge AI; if accepted, add it to tracker/roadmap.
4. Day 4: Draft MfgKnowledge discovery note and collect sample corpus requirements.
5. Day 5: Create supply-chain consolidation note and identify canonical naming.
6. Day 6: Build one clickable or CLI demo for the highest-confidence path, preferably DocAI parser/library MVP.
7. Day 7: Update `docs/roadmap.md` with the revised priority order after user review.

## Final Ranking Rationale

DocAI Studio is the best immediate MVP because it combines high score, complete local source, narrow first release, and dogfood value. MfgKnowledge AI is second because GitHub already marks it high quality and it has a practical low-risk entry point, but it needs PR acceptance first. SupplyGuard AI is third because supply-chain risk/compliance has strong B2B value, but the repo must consolidate duplicate supply-chain proposals before implementation.
