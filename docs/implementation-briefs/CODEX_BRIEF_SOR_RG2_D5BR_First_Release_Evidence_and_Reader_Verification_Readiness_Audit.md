# D5BR — First-Release Evidence and Reader Verification Readiness Audit

**Project:** `starfield-outpost-research`  
**Assignment type:** documentation / evidence-readiness audit, **read-only investigation with narrowly permitted authored documentation**  
**Baseline:** pinned Starfield 1.16.244.0; use current repository HEAD and authoritative claim/asset/source ledgers, recording their actual identities at intake  
**Authority:** this brief defines a proposed bounded Codex assignment. Do not infer authorization for execution, release or Git integration beyond the maintainer's instruction to carry it out.

## 1. Purpose and controlling questions

The maintainer has settled first-release scientific and original-evidence tier choices in D5BO, D5BP and D5BQ. **The next roadmap step is item 5A: identify, without prematurely executing, everything required to verify the selected original saves, standalone evidence derivatives and readers.** This is not item 5B (real-data qualification), item 6 (D5BD generator modernization), item 7 (asset clearance/archival) or item 8 (candidate freeze/B6/release).

Complete all four questions at the **selected first-release tier**:

- **D5BR-Q1 — Coverage.** Can every selected first-release claim and indispensable evidence route be traced to an exact asset/member (if any), reviewed reader/method, prerequisites, source identity, expected assertion, negative controls, existing qualification and outstanding release gate? Identify both the 12 `ACTION REQUIRED` rows and READY/READY—QUALIFIED routes whose external prerequisites would otherwise be overlooked.
- **D5BR-Q2 — Existing qualification.** Which selected routes are already supported by sufficient reviewed evidence at their chosen tier, which need a bounded execution, and which are genuinely blocked? Distinguish integrity-only checks, synthetic qualifications, local derivative verification, historical original-byte execution, native/conditional readers and the future clean-checkout B6 gate.
- **D5BR-Q3 — Minimal execution plan.** What is the smallest complete, safely staged set of *subsequently authorized* tests to close the outstanding first-release prerequisites, grouped by shared original saves and independent derivative readers? Identify exact inputs, outputs, preflight gates, adverse controls, safe side effects, review points, blocker responses and public-reader instructions.
- **D5BR-Q4 — Governance and handoff.** Does the audited graph preserve original claim confidence, status and historical exceptions, all held rights/hosting/B6 gates, authorizations and deferred options? Produce a reviewed, actionable handoff without claiming to have completed evidence execution or cleared publication.

**Success:** no selected claim, necessary evidence edge, reader dependency, missing original or negative control is silently treated as available, reproduced or approved. An accurate, specifically evidenced `BLOCKED` route is an audit finding, not permission to invent a substitute or falsely close the parent question.

## 2. Controlling references and scope

Read and substantively apply `AGENTS.md`, `WORKFLOW.md`, `THIRD_PARTY_POLICY.md`, `docs/CHARTER.md`, `docs/EVIDENCE_STANDARD.md`, `docs/RESEARCH_EXECUTION_PROTOCOL.md`, `docs/EDITORIAL_STANDARD.md`, `docs/PUBLICATION.md`, `docs/PUBLICATION_RUN_CARD.md`, `docs/templates/completion-contract.md`, the current relevant `docs/RESEARCH_STATE.md` sections and this brief. **Read full relevant content, including continuation after truncated tool output; reading order is not an acceptance criterion.** Record consequential application, not a filename checklist.

Primary authority sources:

- `docs/audits/publication-claims-d5bg/{README.md,claims.json,actions.json,evidence-edges.json,crosswalk.md,exceptions.md,handoff.md,verify.py}`; inspect all 71 current claim rows and the actual action/edge graph, without assuming that inherited row statuses encode the narrower selected first-release decisions.
- `docs/audits/publication-decisions-d5bp/README.md` and `docs/audits/publication-decisions-d5bq/README.md`; `docs/audits/public-evidence-d5bo/README.md`; related D5BH/D5BI/D5BO and D5BN audits and `docs/DECISIONS.md`.
- `docs/audits/release-assets-d5bf/{README.md,release-assets.json}`; B4/F1 `coverage.md`, `file-dispositions.csv`, `coverage.csv` and privacy policy; B3 method contracts, source manifests and reproduction guidance; B0/B1/B4/B5 release requirements.
- Existing owned readers and contracts under `research/`, `save-analysis/`, `docs/experiments/` and evidence-access audits; the D5AG reader and D5BJ previously qualified component are **not** a mandate to restart the deferred D5BJ/D5BM work.

Use exact current paths and hashes from the checked-out repository and the ledgers; the paths in this brief are pointers, not assertions that private binaries or original saves exist in this execution environment.

### Mandatory candidate coverage

Treat these **seven asset groups** as a complete minimum inventory, not as seven already cleared uploads:

| Group | Relevant selected scope |
| --- | --- |
| D5BF CORE | 25 original first-party saves; selected position, power Save29, cargo Save52, fabrication HIST-0036, Shared Storage and other original witness routes |
| D5BF ADDENDUM | 14 original saves and 13 JPEGs; selected output-link L-series controls, displayed-item case, construction/placement and other selected controls |
| D5BF D5AS ZIP | Two canonical references and 30 qualified Feynman V complete geometry bodies; verify exact class comparison, exclusion/replacement, not unobserved generating masks |
| D5BF C19 JSON | 346 complete Kreet native UI callback-to-row comparisons and adverse controls; *not* the complete 35,573 upstream evaluation series |
| D5BH episode derivative | Qualified D5AK/D5AL fixed-geometry comparisons across source-lifetime/process episodes, conditional exact public candidate |
| D5BI N2 projected derivative | Selected original N2 construction/competition evidence, conditional exact public candidate |
| D5BO B2 projected derivative | Selected D5AC earlier-unvisited/later-constructor sequence, context and standalone negative controls, conditional exact public candidate |

Also separately inventory **D5AG fixed-geometry reproduction**: a reader/method route reusing the accepted D5BJ native component, exact D5AS ZIP, and reader-supplied lawful Starfield files. Do **not** count it as an eighth independent asset or promote D5AG's original blocked Q2/Q3/AC01.

### The twelve existing `ACTION REQUIRED` claims

The primary agent must resolve the current list from `claims.json`, then include all of these IDs (or flag an authoritative ledger change rather than silently omitting one):

`C02-ORIGINALS`; `C03-FRAME-CONTROL`; `C06-0036`; `B4-C22-L-SERIES-ORIGINAL`; `B4-C23-SAVE52-ORIGINAL`; `C25-ORIGINALS`; `B4-C13-H21-DISPLAY-ORIGINAL`; `C14-ORIGINALS`; `B4-C17`; `C19-CALLBACK`; `B4-C21-SAVE29-ORIGINAL`; `D5AS-BODY`.

The audit must explicitly cross-check, among others: coordinate CORE B4-F001/F002/F003/F047/F053; HIST-0036 CORE B4-F064 (E3 17 fabricators/14 groups and SD2 17 owner joins, checked separately); SD2 census controls CORE B4-F051/HIST-0255 (16) and B4-F040/Save52/HIST-0267 (17), **not** replacements for HIST-0018/HIST-0257 fresh-owner joins; Save29 CORE B4-F054 and its four ordered CB rows; Save52 CORE B4-F040 with shared hold, unknown inventories and four fuel-source joins; L0/S4C CORE B4-F032 plus L0C–L2C ADDENDUM B4-F055–F059 (failed original literal, 19/12/19 selected relationship and same-session controls); display HIST-0021 B4-F067; selected construction/placement controls and photos; Save52's qualified 848-root census; D5AS and C19 standalone exact-data routes. Verify the precise selectors and expected results against source records rather than treating this paragraph as a replacement for them.

Survey other selected READY/READY—QUALIFIED routes, proposed D5BO/D5BH/D5BI exact reader routes and the chosen D5AT tracked-table arithmetic. Assign a justified entry even when *no* new original-data execution is needed. Include selected underlying source/installed-game dependencies where indispensable. Do not turn historical-only, unselected stronger or optional evidence into required first-release assets.

## 3. Authority, exclusions and protections

**Allowed:** inspect tracked project documentation and owned source; inspect existing historical receipts/manifests and separately lawful evidence metadata; trace exact claim-to-edge-to-method dependencies; inspect script entrypoints/imports/CLI/help text **without running real-data processing**; run bounded text/JSON/schema/link/hash/static checks against existing authored materials; make only the necessary documentation/audit files; and perform reversible checks in caller-owned isolated scratch. Inspect source and receipt provenance before relying on a previous PASS. No new package acquisition is authorized.

**Prohibited:** new original-save decoding or original-byte qualification; execution of native fixtures, Ghidra/Pybag, Starfield, SFSE, game/PEX code, observer/hooks or unknown scripts; modifying game files, saves or protected evidence; building new scientific derivatives; publishing/uploading/transferring evidence; asset rights clearance by assertion; D5BD generator modernization; repository archive restructuring; staging, committing, pushing, tagging, releases, visibility changes or destructive cleanup. Do not run apparently harmless scripts before reading side effects, imports, hard-coded local paths and output policy. External installed game files remain user-supplied lawful prerequisites, not something to copy into tracked or public artifacts.

Preserve the relevant C:/D: free-space guard and protected-input identity safeguards wherever an authorized operation could create substantive scratch. Existing receipts may be inspected without retroactively demanding impossible rehashes of unavailable inputs. Never overwrite original receipts or misdescribe an unavailable input as a failed scientific control.

**Publication remains `NOT READY / NOT CLEARED`**; `APPROVED FOR PROPOSED RELEASE` is not distribution authorization. Final file-specific rights/privacy review, archive-member permission, approved transfer/retention, isolated B6, exact hosted bytes and public Git-history exposure all remain separate. The first-release D5AQ Option C, D5BJ/D5BM restart and optional post-publication Feynman VII-b series are excluded.

### Sub-agents

For **D5BR only**, the maintainer approves a **narrow exception to the normal one-active-sub-agent rule**: up to two **concurrent read-only specialists**, with disjoint scopes:

- **Specialist A — original-save routes:** CORE and ADDENDUM, their methods and historical read-only qualification, selected saved-state claims and visual evidence limits.
- **Specialist B — derivative/native-reader routes:** D5AS, C19, D5BH, D5BI, D5BO B2, D5AG reusable native reader and their exact source/host prerequisites.

The primary agent owns every edited file and the global graph, checks overlap/omissions and integrates the results. Specialists do not write shared or final authored files; retain their returns as local read-only inputs. Confirm **both specialist sessions have terminated before launching the fresh independent reviewer**. The reviewer cannot be either specialist and must independently challenge the source inventory, selected tier, negative controls and proposed next actions. Record any concurrency overage and actual consequences; the exception does not transfer to later briefs.

## 4. Required deliverables

Create `docs/audits/evidence-readiness-d5br/` containing at least:

1. **`README.md` — answer-first readiness report:** verdict per D5BR-Q1–Q4, clearly labelled first-release scope, quantified ready/needs-check/blocked/deferred findings, remaining release gates and direct links. Explain technical subjects in plain language before displaying internal claim IDs.
2. **`readiness.csv` or `readiness.json` — authoritative crosswalk:** one traceable entry per selected claim × indispensable method/evidence route (multiple rows when needed); stable claim ID, tier/wording, edge ID/state, asset ID/name/member and exact ledger identity, method/reader path and revision/hash, reader type, input/dependency/rights/host requirements, expected assertion, required negative/counterexample controls, historical reviewed receipts and their *actual* coverage, prospective verification step, owner/group and audit disposition. Include no-asset authored/static cases explicitly. Do not copy secret paths or raw personal identifiers into publication files.
3. **`execution-plan.md` — minimal later-authorization plan:** grouped batches to avoid redundant CORE/ADDENDUM hashing/decoding; separate selected original-save qualification, standalone derivative checks and D5AG lawful native-reader route; prerequisites, ordered stages, expected independently reviewable receipts, side effects, safety and negative tests, fallback/narrow-scope alternatives, stop/escalation and links to the exact source contracts. This plan is not an execution authorization.
4. **`exceptions.md` — route-level gaps and deferred scope:** missing originals, unavailable historical inputs, unqualified reader/version domains, static-only or synthetic-only routes, rights/privacy/hosting holds, unselected exact replay and historical-only exceptions. For each blocker give evidence, smallest reasonable corrective action and affected claim; do not propose large new research by default.
5. **`investigation-ledger.md` — active question and branch record:** record discovery paths, source controls, independent leads, counterexamples, inspection outcomes, exclusions and question-level dispositions during the assignment (not a post hoc box-ticking narrative).
6. **`review.md` — completion/review:** AC/Q matrix, source and receipt identities, actual static checks, editorial screen, any failures/deviations/corrections, specialist scope and termination receipts, independent reviewer verdict and scope limits.

If a smaller or alternate file layout materially improves integration with the existing audits, justify it and provide equivalent machine-readable coverage. Do not mutate `claims.json`, `actions.json`, `evidence-edges.json` or scientific research dispositions merely to make readiness counts more attractive. Correct objective inconsistencies only when necessary to perform the audit, documenting before/after and obtaining authorization for any material claim/tier change.

### Disposition vocabulary

Use these **audit-only** classifications; they do **not** overwrite D5BG status or edge states:

- `READY FOR B6`: existing identified, independently reviewed qualification suffices at the **selected tier**; only normal candidate, rights, transfer, host and B6 checks remain. Name which were actually performed historically and which are B6-only.
- `READY FOR VERIFICATION`: exact needed input and documented method are available or specifically obtainable under approved staging, but a bounded original-byte/derivative/native-reader qualification is outstanding. Do not assume a local file is present merely because a ledger names it.
- `BLOCKED`: a specifically evidenced missing indispensable input, unsafe/unavailable method, unsupported header or additional permission prevents the selected verification. Name barrier class, proof, fallback and minimal resolution.
- `NOT REQUIRED`: stronger historical replay, optional future research or unselected claim tier is out of first-release scope. Record the retained source and rationale.

Separately record whether an asset is `PENDING RELEASE`, rights/policy is unapproved, and a scientific claim is historically attributed. `READY FOR B6` **never** means public distribution cleared, hosted asset available or B6 completed. If evidence cannot justify either ready classification, use `BLOCKED` or a clearly flagged unresolved audit finding; do not guess.

## 5. Mandatory acceptance criteria

- **AC01 — Reading and authority:** complete relevant required reading by final substantive acceptance; recorded applied understanding; no tool, permission or source-scope confusion.
- **AC02 — Claim completeness:** all 71 D5BG claim rows classified for selected-tier relevance; every one of the 12 `ACTION REQUIRED` rows included; actual graph/action counts and indispensable edge inventory reproduced without dropped or invented IDs.
- **AC03 — Decision preservation:** D5BO/D5BP/D5BQ selections, D5AT narrower tier, D1 historical attribution, all four historical-only rows, deferred D5AQ/D5BJ/D5BM and optional VII-b study correctly respected; no scientific/status promotion.
- **AC04 — Seven asset groups:** exact four D5BF plus three later derivative candidates inventoried, with container/member identity, known existing receipts, access and safety boundaries; D5AG treated as an additional reader route rather than another asset.
- **AC05 — Original saves:** every selected CORE/ADDENDUM original-witness route maps to exact member IDs, reader/version/domain, expected positive/negative results and missing prerequisites; key Save29, Save52, HIST-0036, SD2 census, L-series, position, placement and display distinctions preserved.
- **AC06 — Derivative readers:** D5AS/C19/D5BH/D5BI/D5BO/D5AG candidates assigned correct source fidelity, standalone verification, adverse controls, legal external-input requirements and remaining holds. No native execution in this assignment.
- **AC07 — Qualification discipline:** no unsupported upgrade from SOURCE AVAILABLE, SYNTHETICALLY QUALIFIED, historical local receipt or asset checksum to original-byte/reader reproduction; each `READY FOR B6` finding cites the exact accepted basis.
- **AC08 — Executable later plan:** scoped, prioritized and grouped verification batches specify prerequisites, actual tested oracle, error/failure response, receipts, review and separate execution permission; identify genuine missing reader capability versus simple staging.
- **AC09 — Governance and safety:** no protected material mutation, unauthorized execution or external disclosure; repository HEAD/index and excluded content accounted for, exceptions and stop conditions preserved.
- **AC10 — Editorial completeness:** clear newcomer-readable labels, consistent technical terms and status distinctions; complete relevant links/UTF-8/LF/structural screen and manual read per `EDITORIAL_STANDARD.md`, with documented exceptions rather than bulk rewriting.
- **AC11 — Delivery integrity:** exact final changed/untracked authored-file inventory, file hashes, complete and task-only patches; verified byte-exact forward and reverse reconstruction in disposable directories and actual-tree reverse applicability; no staging/commit/push.
- **AC12 — Independent disposition:** two bounded specialist returns, confirmed termination before a distinct read-only independent reviewer, explicit review of every controlling question and AC, challenge to omissions and adverse cases, `ACCEPT`/`REWORK`/`ESCALATE` applied under the completion protocol; no material post-review edit inherits an earlier acceptance without exact-delta review.

## 6. Completion contract and escalation

**Task category:** audit / documentation. **Question parent:** roadmap item 5, readiness substage 5A only; item 5B original-data execution remains OPEN until its own reviewed authorized work. Maintain the active `investigation-ledger.md` near the beginning. For Q1–Q4, record `COMPLETE`, `INCOMPLETE` or evidenced terminal `BLOCKED`, with source evidence and remaining action. A `BLOCKED` individual reader is a documented output of Q2/Q3; it does not automatically prevent the audit question from being COMPLETE if its full boundary and consequence are established.

Within the narrow authorized documentary scope, investigate, correct, retest and resubmit ordinary failures without another brief. Do not invent operational or evidence-volume stopping criteria for healthy authorized static analysis. Stop an unsafe/unauthorized action and preserve the failing receipt; continue unaffected read-only work. For an indispensable audit source not recoverable under current permissions, document its identifier, access attempt, impact, alternatives and minimal authorization needed rather than silently substituting another source. A material new claim-tier decision, live operation, proprietary-input transfer, raw evidence decoding or repository change outside this brief requires separate maintainer approval.

The independent reviewer must receive the frozen brief, amendments (if any), ledger, full proposed crosswalk, underlying selected-source and negative-control references, exact changed tree, source/receipts and both specialists' results. They must independently challenge a representative sample of each source class **and** every consequential exception, assess any omitted viable dependency route, and verify the final snapshot's actual review artifacts.

Report **scientific claims unchanged**, **audit/engineering evidence readiness** (including honest blockers), **protected-input/target effects**, **editorial quality** and **publication authority** separately. D5BR completion is not B6 acceptance or asset release authorization.

**Expected handoff:** the complete audit directory, named next execution batches and a short maintainer-facing summary with exact unresolved permissions and dependencies. Suggest, but do not perform, a commit after independent `ACCEPT` and user diff review.
