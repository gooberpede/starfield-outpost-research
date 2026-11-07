# Codex implementation brief — RG2-D5AX: Publication-tree inventory and reader architecture

**Project:** `D:\Projects\starfield-outpost-research` (`gooberpede/starfield-outpost-research`)  
**Assignment:** D5AX — read-only publication inventory, indispensable-evidence dependency audit, and proposed repository architecture  
**Date:** 2026-11-07 (Australia/Sydney)  
**Type:** Documentation / research-infrastructure audit and design; **not** release execution  
**Authority:** This brief authorizes bounded read-only investigation of the repository, its relevant local metadata/evidence indexes, and existing prior audits; creation of **new tracked audit deliverables and ignored task-local receipts only**. It does **not** authorize moving, archiving, deleting, replacing, or rewriting existing research material; changing Git history; staging/committing/pushing; publishing; uploading Release assets; or operating Starfield. Publication remains **NOT READY / NOT CLEARED**.

## 1. Purpose and controlling decisions

The private repository has accumulated substantial valuable but fragmented research, hundreds of historical briefs/audits, administrative artifacts, and links/locators referencing approximately 70 GB of `.local-work/` outputs. Before restructuring, provide a **complete, reconciled inventory and a decision-ready design** for a navigable public research library that retains scientific history, supports selected release claims, and does not depend on ongoing availability of `.local-work/`.

Implement the prospective D5AW publication plan and the 2026-11-07 maintainer retention amendment. **`.local-work/` is disposable**, not permanent protected evidence. The maintainer may remove it all after publication; operational guards for active experiments and protected saves are different and remain applicable during this assignment. No public claim may depend exclusively on irreplaceable `.local-work/` content after release. Do not demand or attempt a byte-by-byte census of the entire 70 GB. Trace from **proposed release claims and tracked links/dependencies**, inspecting a particular local artifact only where needed to resolve an indispensable edge.

**History policy:** Preserve existing Git history by default. Historical broken links, old conclusions, prior file names, old local paths, and superseded instructions are normal historical records, **not themselves cleanup obligations**. Earlier repository/history publication audits already examined this issue; **locate, assess scope and freshness, and reuse those results**. Perform a bounded delta/risk recheck against the current refs and tracked content, rather than repeating an exhaustive audit without evidence of a gap. A clean/limited-history publication strategy may be recommended **only** upon a *specific evidenced privacy, rights, credentials, proprietary-content, or size/exposure problem*, never merely to tidy historical links. No history modification is authorized.

**Prior evidence decisions:** Reuse B4-F1's provisional **25 CORE first-party saves** and **27 ADDENDUM originals (14 saves, 13 screenshots)**, with 15 local-only and 4 excluded. Save52 is HIST-0267, not HIST-0255. Those packages and decisions are **provisional**, not release permission; do not rebuild or reselect the original 71-file population. Conduct a focused claim-led *delta* review for evidence generated or made indispensable since the 2026-10-21 selection (notably D5AK–D5AV). First-party originals retain unchanged bytes and original names inside any future approved package. Raw saves stay out of Git; eligible selected originals may be separate GitHub Release assets after specific approval. No distribution or asset creation now.

**Presentation objective:** Make coherent subsystem guides and technical references the primary reading path. Keep original investigations, corrected/negative results, and review history accessible but secondary. The result of D5AX is an architecture and execution plan, **not the actual guides or relocation**.

## 2. Frozen controlling questions

**D5AX-Q1 — What exactly is in the candidate public repository, and what currently breaks or obscures access?**

At a frozen Git HEAD/index/working-tree boundary, census all tracked paths and relevant current untracked modifications (do not incorporate unrelated modifications as though approved). Classify file type, size, substantive role, current authority/age, reader significance, administrative residue, and proposed disposition. Build a reference inventory covering Markdown relative links and anchors, links within tables and CSV/manifest values, code/example references, and **plain-text** references to `.local-work/`, absolute machine paths, or unpublished evidence. Distinguish actual broken links from private provenance, deliberately historical locators, and proposed future assets. Identify inbound dependencies before suggesting that any file move or compression is safe. Reuse B0/B1/B2/RR1 prior link and repository-history audits, with bounded delta checks and explicit coverage limits.

**Success:** Reconciled path/role and link/reference inventories with representative independently checked detection controls; decision-ready exceptions and precise inbound-reference consequences. No claim of having exhaustively opened every private evidence file.

**D5AX-Q2 — Which selected-publication claims would fail if `.local-work/` disappeared?**

Use the existing B1 claim/build matrix and D5AW pre-publication disposition register as **proposed scope**, not presumed final maintainer selection. Include recent resource-generation claims as clearly labelled proposed additions or deltas. Follow each selected/proposed claim through its decisive source report, methods, intermediate artifacts, original inputs and software/tool dependencies. Classify each artifact/edge as indispensable, independently reproducible, supporting but nonessential, or disposable; give actual evidence, not just local filename/hash. Every indispensable dependency must have a **credible proposed durable route**: tracked public material, approved candidate Release asset, or independent reconstruction from publicly obtainable lawful inputs and documented steps. A private path or hash is not a route. Identify blocked claims and a specific proposed remedy (promote bounded derived data/source, Release asset candidate, verify method, narrow/exclude claim). Distinguish historical runtime events that cannot be replayed exactly from computations that can be independently reproduced; do not mislabel a narrative report as primary runtime evidence.

**Success:** Claim-led transitive dependency ledger with explicit public-route candidates, remaining verification/rights gates and unresolved indispensable paths. Do not silently downgrade the publication-independence rule to “disclose missing evidence and proceed” for indispensable evidence; seek explicit maintainer disposition on affected claims.

**D5AX-Q3 — What reader-facing documentation structure and archival layout should we adopt?**

Propose a concrete directory tree and navigation model with (i) accessible subsystem overviews/guides, (ii) evidence-backed technical references, and (iii) retained research history. For each subsystem, identify existing source documents, current authoritative findings, unresolved qualifications, required synthesis, and links back to primary reports and historical reviews. Give at least one worked **resource-generation** reader journey, incorporating the settled nondeterminism and GC-35–37 conditional caching findings without promoting conditional mask surveys to actual winner probabilities. Also show two other representative subsystems and three reader paths: understand, reproduce within advertised tier, and challenge/recover the historical interpretation. Avoid writing final guides or moving documents now.

Design in-directory compressed archives for historical implementation briefs and administrative audits. Use local `README.md` indexes plus machine-readable membership manifests; propose archive groups, filenames, loose exceptions and link-migration rules. Preserve original source filenames/bytes within proposed archives. Declare the accounting universe before counting:

- `ARCHIVED_SOURCE_DOCUMENTS`: eligible source documents proposed inside archives;
- `REMAINING_LOOSE_SOURCE_DOCUMENTS`: eligible source documents intentionally left loose;
- `GUIDING_READMES_AND_INDEXES`: separately enumerated directory guide/index documents;
- `MANIFESTS_OR_OTHER_GENERATED_METADATA`: generated inventories, receipts, archive containers, etc.;
- `EXCLUDED_NON_SOURCE_FILES`: placeholders, controlling administrative files and any other explicit exclusions.

Require the disjoint whole-universe reconciliation and `TOTAL_ELIGIBLE_SOURCE_DOCUMENTS = ARCHIVED_SOURCE_DOCUMENTS + REMAINING_LOOSE_SOURCE_DOCUMENTS`. **Guiding briefs are not silently lost from the denominator**: explicitly classify each controlling/source brief and record why it is counted or excluded. README and generated-manifest counts are separate; never count archive containers as source members. Document case-folded filename collisions, safe archive paths, exact original path/size/SHA-256 plan, archive-member lookup, and prospective extraction/byte-verification procedure. A ZIP member is *not* a working GitHub Markdown hyperlink; plan reader-visible replacement links or archive citations without inventing individually browsable member URLs. Historical commits need not be rewritten to fix links.

**Success:** Concrete architecture diagram/tree, proposed archive membership strategy with reconciled counts, per-subsystem guide foundations, file-migration/link strategy and measurable reader-journey tests. The recommended structure must be useful for a public reader rather than just a file sorting plan.

**D5AX-Q4 — What is the smallest ordered, independently reviewable migration and final clearance plan?**

Produce bounded subsequent assignments and acceptance gates: synthesis first, migration/archive only after approved inventories and verified guides, evidence packaging/link updates, pre-release isolated clean-checkout verification without the existing `.local-work/`, then exact tree/history/asset/rights review and maintainer release authorization. Account for B0–B6 responsibility, B4-F1, D5AW, explicit author/contributor/rights decisions, Git history/release-surface approval, and the distinction between prior review, current delta audit, and final B6 candidate review. Propose a decision table for the maintainer: exact structure, archive groups/count conventions, claim inclusion/exclusion, selected evidence routes, actual disclosure issues and proposed publication-history boundary. Preserve the default full Git history when no material exposure issue is found.

**Success:** Ordered plan with dependencies, risk controls and crisp decisions; no implementation that requires unapproved moves, deletions, public exposure or experiments.

## 3. Mandatory material to read and reconcile

Read all relevant content (including truncated continuations) by final substantive review, and show its use; chronology of reading is not an acceptance criterion:

- `AGENTS.md`, `WORKFLOW.md`, `docs/CHARTER.md`, `docs/RESEARCH_EXECUTION_PROTOCOL.md`, `docs/EVIDENCE_STANDARD.md`, `docs/EDITORIAL_STANDARD.md`, `docs/templates/completion-contract.md`, `docs/THIRD_PARTY_NOTICES.md` if present, `docs/PERMISSIONS.md`.
- `docs/PUBLICATION.md`; `docs/DECISIONS.md` (D5AW local-working evidence decision); `docs/audits/deferred-work-d5aw/` (review, dispositions, crosswalk, decision ledger, publication-plan-amendment v2); `docs/research-roadmap.md` and proposed first-release claim matrix.
- Publication-readiness B0–B5 and RR1 records, especially **prior Git history/secret/private-payload reviews**, B1 navigation/claims, B2 link/prose rework, B3 methods and 1.16.244.0 baseline, B4 rights/privacy, B4-F1 `README.md`, `coverage.md`, `file-dispositions.csv`, `members.csv` and `assets.csv`; B5 creator/housekeeping decisions.
- D5AU and D5AV settled gameplay-gap decisions, D5AS closeout, D5AT active-outpost survey, and other recent accepted findings relevant to first-release claims.
- Existing `README.md`, directory-level navigation, `docs/experiments/README.md`, `docs/implementation-briefs/README.md`, `docs/audits/README.md` and relevant archive precedent where accessible. **Do not assume the sibling `starfield-resource-research` repository or its files are available or authorized; the counting/indexing lesson is specified in this brief.**

Keep original scientific scope and old verdicts intact. A current navigation or proposed release matrix can supersede an older recommendation without rewriting the historical source report.

## 4. Method and evidence standards

1. **Freeze inventory boundary**: record HEAD, index and worktree status, refs considered, file inventory basis, existing provenance/hashes and source date. This is a planning audit, not an authorization to change any of those objects. Use read-only Git operations. Describe prior history-audit reuse and current delta; flag a genuinely unreviewed ref or suspicious committed material specifically. Historical broken links/obsolete text are expected, not a history defect.
2. **Census exactly, classify consistently**: Use machine-readable CSV/JSON datasets for tracked roles, references, candidate moving/archiving, claim-to-artifact edges, blockers and their owner. Count disjoint sets, verify foreign keys and preserve raw unresolved examples; avoid regex-only claim of complete semantic detection. Spot-check link types (relative/absolute/anchors/images/CSV/code/plain text), encoded characters, case and duplicate paths on both Windows and GitHub case-sensitive resolution. Do not modify existing links.
3. **Claim-led, not terabyte-led**: First determine candidate claims and their primary supporting reports. Trace only their indispensable input paths; record why nonessential material need not be opened. Keep `.local-work/` entirely disposable in the proposed final state. If an indispensable historical runtime trace is nonreplayable and cannot be publicly carried by a rights-cleared bounded derivative, mark a **claim-specific publication blocker**, not an indefinite preservation duty.
4. **B4-F1 is existing work**: Reuse the 25/27 selection, archive/member hashes and actual local packages when supported by current evidence. Do not assert that provisional packages are approved or hosted. For newer material, recommend **minimal** evidence derivatives or claim-specific asset candidates rather than bulk 70-GB uploads. Content from installed EXE/ESM/BA2, proprietary dumps, bulk disassembly and private/donor saves does not become distributable by moving it into a “public” directory.
5. **Historical archives are design-only**: No ZIP creation now, no original deletions, no moves. Include lossless exact-byte verification and source/loose accounting in the future implementation plan. Identify old inbound links whose current-facing use would break after archiving; propose indexes/stubs or archive references. Distinguish intended public working links from historical citations.
6. **Current-facing prose and navigation**: Propose summaries faithful to native-versus-runtime, source-versus-outpost, static-versus-conditional, observed-versus-inferred distinctions. Avoid mass automatic rewrites of technical symbols, identities, masks, code or addresses.
7. **Independent reviewer**: Challenge completeness of census, residual dependencies, access tiers, architecture usefulness, historical audit reuse, missing third-party/privacy risks, and whether any pre-publication science is actually indispensable. Editorial screen and substantive review are separate. Reviewer must not accept its own edits.

## 5. Boundaries and safeguards

**Allowed:** Read-only inspection of tracked tree, existing repo metadata, reports, methodological source, documented reference registers and approved existing local indexes; creation of new D5AX documentation and bounded ignored receipts without overwriting existing outputs; read-only Git ref/history **delta** analysis; independent review. Use dedicated new names/roots and follow normal free-space/input guards when writing outputs. Preserve any active named protected save/evidence immutability under existing rules.

**Not allowed:** Game launch, save modification, native execution, debugger/Ghidra opening for new analysis, broad archive extraction or unpacking 70 GB, crawler over every `.local-work` file, building or distributing release archives, changing `.gitignore` or Git configuration, relocation, compression, deletion, staging/commit/push, history rewrite, GitHub repo creation, release/tag/visibility changes, or uploading anything. Do not alter prior publication policy or claim selection under this architecture brief; propose required decisions.

**Agent concurrency:** Existing project default **maximum one concurrently active sub-agent**. A specialist or independent reviewer may be used sequentially, not concurrently. Any minor overrun must be promptly disclosed and evaluated by consequence under current project governance; it is not automatically an acceptance failure. The two-agent D5AV exception has expired.

No automatic stop for an editorial checkpoint. Codex must pursue material in-scope corrections through substantive COMPLETE, or a genuinely evidenced terminal BLOCKED/ESCALATE, and preserve review failures and corrections.

## 6. Deliverables and proposed tracked locations

Create a new, self-contained set of D5AX reports, preferably under `docs/audits/publication-architecture-d5ax/` (the exact path may be adjusted to match established conventions), with a local README that introduces the documents and distinguishes current proposals from history. Minimum contents:

1. **`report.md`** — answers to Q1–Q4, compact actual metrics, major design findings, decisions, and unresolved release blockers.
2. **`tracked-inventory.csv`** — one row per tracked path (plus separately classified non-tracked current exceptions where material), its role/size, reader/publication significance and proposed destination.
3. **`reference-inventory.csv`** and **`link-analysis.md`** — scanned reference occurrences, resolved/unresolved targets, private provenance or true dependency, inbound impacts and bounded detection limitations.
4. **`claim-evidence-dependencies.csv`** and **`evidence-access.md`** — claim-to-artifact graph, indispensable classification, transitive prerequisites, proposed public access/reproduction route, rights/permission status and blockers; B4-F1 continuity and later deltas.
5. **`architecture.md`** and **`archive-plan.md`** — proposed public directory tree, subsystem guide foundations and reader journeys, archive families/member counts and classification universe, README/index/member lookup strategy, migration and link treatment. Where a fully enumerated archive proposal is tractable from tracked files, include an exact member inventory (CSV) rather than only sample groups.
6. **`migration-plan.md`** — incremental implementation briefs/work packages, safety and test gates, B0–B6 responsibilities, history-risk decision, exact post-implementation clean-checkout validation requirement.
7. **`ledger.md`**, **`review.md`**, appropriate exact-file manifests, verified complete/task-only patches and disposition/acceptance matrix. Preserve reviewer REWORK and correction history. Place task-local receipts and scratch under ignored `.local-work/d5ax/`; these outputs themselves are disposable and **not** substitutes for the new tracked findings.

Avoid generating enormous redundant prose or CSV duplicates without evidentiary value; each artifact should serve a distinct question. Existing source documents remain unmoved.

## 7. Mandatory acceptance criteria (AC01–AC09)

**AC01 — Governance and preservation.** Applicable required material read and substantively used. Frozen current tree/ref/rights boundary recorded. No prohibited operations or protected-input changes. One-sub-agent default applied, with proportionate overage reporting. No fabricated final release/claim approval.

**AC02 — Complete tracked-file census.** Every frozen tracked path accounted for once, with stable counts by role and proposed disposition; pre-existing untracked/user changes distinguished. Actual source-path and archive denominators reconcile; missing files and known detection limits disclosed.

**AC03 — Link and reference coverage.** Every tracked source file is searched using the declared bounded techniques for links and text/private paths; current-facing broken/unavailable links and provenance-only historical links distinguished. Incoming references and future archive moves assessed; spot-checked false-positive and false-negative controls reported. Historical Git links need no repair.

**AC04 — Claim dependency and independence.** Each proposed first-release claim and new relevant resource-generation delta has an evidence-dependency path, availability and indispensability classification, and explicit durable public/reproduction route or a named unresolved release blocker. Selected save assets remain B4-F1 provisional; no claim treats a private hash/locator as sufficient. No dependence on permanent `.local-work/`.

**AC05 — Evidence rights/access and history delta.** Reuse and qualify earlier history-review findings. Identify actual current/ref delta or specific exposures; do not invent a problem because of old links. B4-F1 and later evidence assessed for *proposed* routes with rights/privacy gates unwaived. No unauthorized history rewrite or asset distribution.

**AC06 — Usable reader architecture.** Concrete proposed directories, guide/technical/history tiers, per-subsystem foundation mapping, the three reader journeys and a worked resource-generation example. Independent reader-centered critique identifies navigation failures and proposes corrections.

**AC07 — Historical archive design and accounting.** In-directory ZIP/index plan with proposed membership (or explicit unresolved categories), safe member naming, original-path preservation, SHA-256/byte verification method, guiding README classification and reconciled five-category counts. No missing governing briefs, no double-counting source documents, no fictitious clickable ZIP-member links.

**AC08 — Ordered implementation/release gates.** Clear reviewable post-D5AX sequence, no unapproved restructuring, planned clean-checkout test without private `.local-work/`, claim-specific blocker resolution, B0–B6 integration and separate maintainer approval for final tree/history/assets/visibility/timing.

**AC09 — Independent substantive, editorial and delivery verification.** Reviewer checks Q1–Q4 against their original questions and current tree, explores material omitted source/dependency possibilities, verifies output dataset integrity and acceptance matrix, challenges history-audit assumptions, documents corrections and exact final snapshot. Complete/task-only patch byte consistency and current status/HEAD/index recorded. ACCEPT only if all mandatory questions/criteria are met; otherwise REWORK or evidenced ESCALATE.

## 8. Closure and handoff

The answer must specify **which choices the maintainer now needs to make** to authorize subsequent restructuring, which decisions are already settled and which release gates remain independent. Separate **scientific adequacy**, **public evidence accessibility**, **publication rights/privacy**, and **repo usability** rather than blending them into a generic readiness score. A negative finding (no new history hazard; no additional indispensable asset) is a valid result when supported by the audit's actual coverage.

Provide question dispositions, AC matrix, all datasets/reports, independent review, source and hash accounting, unresolved cases and proposed commit message. Do **not** stage, commit, push or publish. D5AX authorizes planning only; it neither selects final first-release claims nor grants permission to delete `.local-work/` during active work.
