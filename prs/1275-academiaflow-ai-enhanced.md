# AcademiaFlow AI Draft Proposal

This proposal develops [Issue 1275](https://github.com/ava-agent/awesome-ai-ideas/issues/1275) into a focused literature evidence workflow for small research groups. It is a product hypothesis, not an implemented platform or a report of productivity gains. The first question is whether researchers can verify a source grounded evidence table with less effort than their current reference manager and spreadsheet workflow.

## Intended users and problem

The proposed initial users are graduate researchers and supervisors preparing a literature review within one defined research question. They already collect references but must manually reconcile notes, source passages and citations. The prevalence, severity and willingness to pay for this problem require interviews; no industry wide productivity or burnout statistics are asserted.

The proposed product complements a reference manager rather than replacing all research, teaching and administrative software. It does not perform autonomous research, make funding decisions, grade students, or promise more publications.

## Proposed minimum viable workflow

1. A researcher imports a reference export or authorizes read only access to a selected reference collection.
2. The researcher adds documents they are entitled to process and defines the question and inclusion criteria.
3. The system proposes an evidence table with each statement linked to a source identifier and an inspectable passage location.
4. The researcher accepts, edits or rejects each statement. Unsupported statements remain visibly unresolved and cannot silently enter the approved table.
5. The researcher exports reviewed evidence and a bibliography, preserving source references and review decisions.

Generated summaries must distinguish a source's claim, an inference and the absence of evidence. A citation resolving to a real document is necessary but does not show that the cited passage supports the generated statement.

## Proposed data and integration scope

Start with user supplied reference exports and documents. A later read only Zotero connector should request only the permissions needed for the selected library. Public libraries can be read without authentication; private libraries need appropriate credentials. Credentials must be kept out of exports, URLs and logs. The [Zotero API documentation](https://www.zotero.org/support/dev/web_api/v3/basics) describes the relevant access and versioning behavior.

Use Crossref for bibliographic metadata and identifier checks where applicable. Its API exposes deposited scholarly metadata; it does not grant access to publisher full text or establish that a generated claim is true. See the [Crossref REST API documentation](https://www.crossref.org/documentation/retrieve-metadata/rest-api/).

Do not scrape restricted publisher sites or claim integrations with services whose access terms have not been reviewed. Document processing must respect licenses, institutional rules and the permissions of the uploader. Missing documents, inaccessible passages and ambiguous identifiers should produce explicit limitations rather than invented citations.

## Proposed architecture

Use a small web interface, an ingestion worker, document storage and a relational database for source records and review events. A retrieval layer locates evidence passages before a language model proposes summaries. Save the document version, passage locator, extraction method and generated statement together so reviewers can inspect provenance.

Treat extracted text as untrusted content. Instructions inside a paper must not control tools or change project permissions. The first version needs no autonomous browsing, tool execution or institutional system writes.

Keep projects isolated. Any external model processing of uploaded documents must be disclosed and enabled only under an appropriate policy. Private manuscripts and sensitive research data are outside the initial public document pilot. Export and deletion behavior should be tested, including caches and derived artifacts.

## Evaluation plan

Use a fixed set of appropriately licensed papers and a predefined research question. Human reviewers prepare a reference evidence table before examining generated outputs. Include contradictory findings, missing metadata and questions with no supporting source.

The following are proposed measurements, not achieved performance:

| Question | Measurement | Decision rule |
| --- | --- | --- |
| Are the statements supported | Independent review of statement and passage pairs | Report unsupported, contradicted and unresolved statements separately |
| Are references and locations usable | Identifier resolution and ability to open the cited passage | No fabricated identifier or unmarked missing source may enter an approved export |
| Does verification save time | Time to a reviewed table against the reference manager and spreadsheet baseline | Include correction time and review effort, not just generation latency |
| Is the workflow useful | Interviews and observed completion of a defined literature task | Continue only if participants prefer the reviewed workflow for a stated reason |
| Does it handle failure safely | Missing file, revoked access, failed retrieval and conflicting evidence tests | Preserve limitations and require review instead of asserting unsupported conclusions |

Predefine the sampling method, reviewer instructions, primary metric and acceptance thresholds before the pilot. Report disagreement between reviewers, sample size and uncertainty. This study cannot establish publication increases or long term teaching outcomes.

## Validation and milestones

First conduct interviews and observe the current workflow. The next milestone is a small demonstrator using public or explicitly permitted documents, followed by a comparison against existing tools. Collaboration features are a later option only if the pilot supports them.

Pricing, institutional procurement, research grants and customer acquisition remain open questions. Do not base a business case on unsourced market projections or assumed university partnerships. There is no committed delivery date, funding round, customer count or revenue forecast.

## Boundaries and discussion

Teaching personalization, automated assessment, paper generation, grant submission, institution wide analytics and a research metaverse are not part of this MVP. Human review remains necessary, and the software does not guarantee academic integrity or regulatory compliance.

The unresolved choices are which research discipline to begin with, what evidence fields reviewers need, whether documents may be processed outside the institution, and whether the workflow improves on the existing reference manager. Earlier numerical productivity, market and policy claims have not been carried into this draft because supporting evidence was not established.
