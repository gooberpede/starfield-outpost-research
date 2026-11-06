# CODEX BRIEF — SOR-RG2-D5AT
## Save52 Outpost Resource-Mask Inventory and Distribution Survey

**Status:** Offline implementation/research only; no live or deployment authority.  
**Repository:** `D:\Projects\starfield-outpost-research\`  
**Build and input:** Pinned Starfield 1.16.244.0 and protected Save52.  
**Parent questions:** GC-10, GC-31, D5R remain governed by their existing wording and statuses.  
**Decision:** Survey Save52 outposts and their candidate geographic resource sources, derive and independently verify source-specific conditional request-mask distributions, and rank worthwhile future sampling locations—especially balanced sources. **Cache semantics are explicitly deferred to a separate brief.**

## 1. Authority and governance

Read and apply the complete relevant versions of `AGENTS.md`, `README.md`, `WORKFLOW.md`, `docs/RESEARCH_EXECUTION_PROTOCOL.md`, `docs/EVIDENCE_STANDARD.md`, `docs/EDITORIAL_STANDARD.md`, `docs/PERMISSIONS.md`, `docs/SAVE_PROTECTION.md`, `docs/RESEARCH_STATE.md`, `docs/reviewers/research-completion-reviewer.md`, `docs/templates/completion-contract.md`, and source/save/native documents relevant to this survey. Recover truncated readings before final substantive acceptance. Required *understanding* matters; chronological reading order is not an acceptance criterion. Record how the readings governed implementation; an independent reviewer verifies that understanding.

**New prospective sub-agent policy, explicitly approved by the maintainer:** a maximum of **one simultaneously active sub-agent**. That one may be a specialist **or** an independent reviewer, never both concurrently. Both may be used sequentially, after the preceding one is confirmed terminated. The primary agent retains responsibility and can work without sub-agents. Codex must disclose any limit breach and its duration, operations and effects. **A minor, promptly corrected breach with no material consequences does not by itself constitute an AC01 or contract failure.** Material interference with evidence, review independence, safety, authorization or budget must be evaluated and can fail the relevant criterion. Update prospective governance documents (`AGENTS.md`, `WORKFLOW.md`, and relevant reviewer/protocol/decision text), without rewriting prior failures.

Authorized: offline read-only Save52/resource-data analysis, verified disposable-copy Ghidra inspection where needed, native simulations on owned disposable hosts, read-only use of earlier authenticated evidence, new offline tools/oracles and authored documentation. Prohibited: game launch, live observation, process attachment, SFSE changes/deployment, original Ghidra database edits, save modification/restoration, publication of proprietary raw material, Git stage/commit/push, extractor/physical-overlap or cache-semantics investigations. Use SOR-P-0002 for owned-method reuse, retaining source attribution. Maintain at least **40,000,000,000 caller-available bytes on both C: and D:** before material writes. Preserve Save52/backups, source inputs, prior captures and archives; timestamp-only changes may be accepted only after verified content equivalence. Use pinned Python with `-E -B`; entrypoints must reject optimization using ordinary conditionals, not assertions.

## 2. Starting evidence and essential distinctions

- D5AQ: `d5aq-report.md`, `d5aq-mask-method.md`, `d5aq-request-mask-map.csv`, `d5aq-reachability.md`, `d5aq-native-dependency-inventory.md` and original sampling/oracle controls. **D5AQ-C1 is specific to one Feynman source:** 196 requests, 28 yielding mask `0x0`, 168 yielding mask `0x3`. Do **not** assume 196 requests, the same raster or two masks at another source.
- D5AG/D5AF/D5T: original-input coordinate conversion, ordinary raster sampling, effective geometry inputs, Special/Everywhere applicability and independently verified full-content comparisons. A mask alone is not a universal certificate of identical geometry.
- D5AI/D5AJ: distinct outpost, body, Grid, geographic source, transient source allocation, resource-map holder, descriptor/frame and owner identities. A resident ProcGen map is **not** automatically a census of sources physically intersecting an outpost.
- D5AS: the completed 30-cold-start Feynman geometry study recorded 2 mask-0-reference and 28 mask-3-reference outcomes. This is retail evidence of geometry classes, **not** evidence that candidate-coordinate frequencies equal winning probabilities. Do not reclassify its historical indirect mask observations as direct mask samples.
- Save52 outpost/state reconstruction and existing project reference exports. Save52 is the roster authority, not the outpost tracker, labels, recollection, or a later game save. Cite the exact save and installed definition identities.

**Central rule:** report the conditional fraction of *request coordinates* mapping to each mask. Never call that fraction the probability of that mask winning. Unknown fields must remain explicitly unknown; no convenient guessed descriptors/atlas data.

## 3. Frozen controlling research questions

### D5AT-Q1 — Complete Save52 outpost-to-source inventory

Which outposts exist in protected Save52, and which geographic sources may contribute resource geometry to each?

Recover and reconcile **every** saved outpost, including inactive/abandoned but still constructed ones, with stable record identity, body/planet, position, reference and descriptive label where available. Establish source associations using actual verified spatial coverage, owner/descriptor/Grid and data provenance; source allocations themselves are transient and may not be stored in Save52. One outpost can intersect multiple sources and a source can contribute to multiple outposts. Distinguish **verified area intersection**, **plausible source candidate**, **resident-only**, **unresolved**, and **not applicable**. Account for every outpost and likely source with explicit denominators and a reconciliation table. Do not silently exclude sources because association is difficult or names are missing.

### D5AT-Q2 — Actual conditional mask census

For each qualified source, derive and verify the applicable complete original-request cohort, starting context/descriptor, terrain/BIOM/raster and conversion parameters. Do not generalize Feynman's `[-2,11]^2` without proof. Calculate the raster atlas address/byte and low-nibble mask for **each request**, using generalized D5AQ methods. Include both relevant FMA/non-FMA paths and an independently implemented oracle; resolve discrepancies. Allow any number of mask classes, not just 0 and 3. Separate actual observed requests, conditional sampled requests and ambiguous/unavailable input cases. If full effective inputs cannot be authenticated, use a named, evidence-qualified conditional contract and disclose what changes it; never invent one. Pursue viable offline data and native paths before labeling essential inputs blocked.

### D5AT-Q3 — Full distribution survey and ranking

Produce a real ranked census of Save52 source/outpost candidates, not only a proposed methodology or three convenient examples. For each source show number of requests, counts and shares per mask, all masks, qualification and unresolved counts. Prioritize genuine two-class splits near **50:50**, but preserve other classes, single-mask sources and incomplete cases in the full dataset. For 3+ masks use a distribution-aware measure such as entropy/effective number of classes, alongside the largest class share, and explicitly distinguish overall balance from a top-two-only conditional balance. A 50:50 split of just the top two is misleading when a substantial third class exists. Rank *source-at-outpost* combinations, keeping separate source percentages rather than averaging them into an imaginary outpost-level probability. Include mask grids and a full source-indexed CSV/JSON.

### D5AT-Q4 — Identify promising future empirical locations

Evaluate top sources for practical visits from Save52, positive source identity and resident-map attribution, available effective data/frames, reproducible starting conditions, and whether the existing generic `SORSnapshot` tool can discriminate results. For the strongest candidates where qualified inputs permit, execute offline full-geometry native/independent controls for alternate masks; establish whether **complete geometry differs**, not merely the low nibble. List candidates with evidence-supported trade-offs and exact further permissions/inputs needed. Avoid live cards, deployment or new forecast freezing. Keep GC-10/GC-31/D5R statuses and other research tracks truthful.

## 4. Required scientific method

1. Inventory Save52 and evidence first; do not shortlist by convenience before establishing the denominator.
2. Reproduce D5AQ-C1 Feynman’s **196 rows and 28/168 counts** exactly as a regression, including independently checked atlas samples.
3. Demonstrate the generic calculation on **at least two genuinely different verified body/source contexts**, not relabeled Feynman data. Challenge chart/face boundaries, different request-cohort sizes, missing raster, ambiguous body and outpost mapping, all mask classes and input changes.
4. For each source, preserve explicit sampling inputs and evidence confidence. Request existence is not proof of first-miss reachability. A source’s geographic relationship to an outpost is not established merely by being in the current manager.
5. Build an independent auditor that checks roster completeness, one row per qualified request, identity joins and mask counts, including negative/corrupted cases. Test that distributions with 3+ classes remain intact and missing sources cannot vanish from rankings.
6. Where essential source inputs are missing, trace reasonable Save52/native/data alternatives to completion. An unresolved mandatory original question is **INCOMPLETE/REWORK** unless a genuine terminal blocker meets the research protocol’s precise proof, in which case report **BLOCKED/ESCALATE**. Neither a partial shortlist nor an algorithm alone constitutes completion.
7. The source-code/native investigation is limited to obtaining accurate outpost-associated request-to-mask maps. **Do not reopen cache semantics or construction scheduling** in this brief; probabilities of construction winners remain unknown.

## 5. Required durable deliverables

- `docs/experiments/resource-retained-population/d5at-report.md`: answer-first full coverage, conclusions, ranked candidates, confidence and remaining uncertainties.
- `d5at-outpost-source-inventory.md`: complete Save52 roster/association method, reconciliation and missing cases.
- `d5at-mask-distributions.md`: complete source-level mask summaries and readable ranking/mask grids.
- `d5at-candidate-assessment.md`: top candidate feasibility, geometry-discrimination evidence, follow-up recommendation.
- `d5at-investigation-ledger.md`: original questions, acceptance matrix, attempted branches, failures, evidence locators and remaining constraints.
- Machine-readable `d5at/` tables (`outposts`, `outpost-source-joins`, `request-masks`, `source-distributions`, `candidate-ranking`, `unresolved`) with explicit schema, unique IDs, provenance, qualifying input contracts and unqualified rows. Never omit a record simply because it cannot be classified.
- Reproducible offline source- and geometry-checking methods and independent test/oracle under `research/resource-retained-population/`, with proprietary raw results remaining in ignored local storage.
- Independent substantive and editorial review record, relevant checklist/research-state updates, proposed governance updates for one sub-agent, exact source lock, complete/task-only verified diffs and a handoff manifest.

Final Codex summary must link to the actual report, ranking tables, candidate assessment, independent review and patches. No invented local artifact or claim that screenshots of a report prove the underlying input corpus.

## 6. Frozen acceptance criteria

| ID | Mandatory pass condition |
|---|---|
| AC01 | Complete relevant required reading and applied understanding; lawful offline scope/provenance and protected-input/disk preservation. One-active-sub-agent policy adopted prospectively. Minor reported brief overages with no material harm are **not automatic failures**; material effects judged substantively. |
| AC02 | Exhaustive and reconciled Save52 outpost roster, complete accounting for all relevant potential sources, qualification/uncertainty and evidence-backed geographic associations. |
| AC03 | Source-specific effective input and request-cohort qualification; no blanket Feynman rectangle/atlas/mask assumption. |
| AC04 | Per-request source-level mask results for all recoverably qualified sources, complete counts/classes and rigorous unknown rows, with independent numeric/native checks. |
| AC05 | Exact 196-row Feynman 28/168 regression, two genuinely different contexts and adverse attribution/sampler checks passing. |
| AC06 | Full readable and machine-readable Save52 distributions and meaningful ranked near-balanced candidates, including 3+ masks, single-mask and missing/unqualified cases; no invented win probabilities. |
| AC07 | Evidence-supported future sampling candidate assessment including source accessibility, snapshot compatibility and where possible genuinely different full geometry. |
| AC08 | Accurate state/checklist updates, historical findings preserved, cache investigation deferred, reproducible ledgers and no unauthorized action. |
| AC09 | Independent substantive and editorial acceptance against the **exact final snapshot**; complete/task-only diff verified, review limits and evidence pins recorded; no staging/commit/push or live operation. |

Q1–Q4 each require explicit COMPLETE/INCOMPLETE/BLOCKED dispositions. A documented partial result is useful but **cannot** close an unanswered original mandatory question. A true blocker needs concrete missing evidence, attempted alternatives, scope impact and the smallest next authorization/input. Reviewers cannot grant new gameplay authority or manufacture positive controls from missing files.

## 7. Handoff and next boundary

Record starting HEAD/index, preexisting changes and every task-authored path. Preserve errors and failed/superseded controls. Use at most one active sub-agent; if a specialist is used, end its session before initiating the independent reviewer. Do not self-accept. Give the reviewer the frozen brief, primary input identities, complete corpus, negative cases and the actual runnable method. Return question/AC matrix, precise confidence and coverage, full review and byte-verified patches. **Codex must not stage, commit or push.**

**Cache semantics will be a separate future brief after D5AT.** This work is a distribution inventory and candidate-discovery assignment, not a general re-investigation of winner scheduling, retention or extractor behaviour.
