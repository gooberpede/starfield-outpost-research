# CODEX BRIEF — SOR RG2 D5AG: Terrain-to-Resource Consistency and Lifecycle

**Date:** 2026-11-02  
**Project:** `D:\Projects\starfield-outpost-research` / `gooberpede/starfield-outpost-research`  
**Type:** Offline native research, causal reconstruction and bounded native controls  
**Parent scientific objective:** D5R remains OPEN. Preserve B1, B2, D5S–D5AF conclusions and their evidence classifications.  
**Authority:** This brief authorizes offline research and documentation, not a retail run or production observer changes.

## Purpose and non-goal

**Controlling question D5AG-CQ:** *What concrete terrain-to-resource data, scheduling, ownership or lifecycle mechanisms constrain the construction and continued identity of ordinary resource populations, and what do these mechanisms actually establish about reproducibility of complete resource types and geometry during ordinary gameplay?*

Investigate the hypothesis that Starfield has a stabilizing or authoritative mechanism upstream of, or shared with, resource construction that helps reconcile competing requests with persistent-looking deposit geometry. **Do not assume the hypothesis is true.** A supported alternative must have a specific native or empirical evidentiary basis; hypothetical possibilities alone cannot justify dismissing the hypothesis or closing the research. A particular failed candidate is not completion while material, authorized alternatives remain.

**Explicitly deferred:** physical overlap, intersection and mutual exclusion *between different resource deposits/types*. Record any directly relevant finding incidentally, but do not investigate general non-overlap rules, introduce a non-overlap acceptance criterion, or add physical-overlap tasks to this assignment. That is a separate future investigative line. Distinguish source-footprint overlap (which allows multiple geographic requests to reach one source) from the deferred deposit-overlap question.

Consistency means **identical resource identities and complete geometry for equivalent effective world inputs**, not merely the same available resource list or approximately similar shapes. A displaced deposit beneath an extractor is a material difference. Do not assume existing gameplay stability proves independent cold reconstruction is identical, and do not confuse cached reuse with regeneration reproducibility.

## Frozen controlling questions

| ID | Original question and completion/falsification obligation |
|---|---|
| **D5AG-Q1 — Terrain-to-resource authority** | Identify the terrain producer(s) of every consequential resource-generation coordinate, frame, source ownership/context, content/seed and raster-ready operand; establish whether any authoritative terrain cell, region or stable request identity constrains the source population. Prove joins through actual native data/control flow, including negative controls for attractive but irrelevant paths. Do not replace request-specific operands with source anchors without proof. |
| **D5AG-Q2 — Construction consistency** | Determine whether real terrain preparation, scheduling, task dependencies, source ownership or synchronization imposes a stable winner or equivalent canonical input despite multiple eligible provider requests. Explain B2 `[4,-1]` versus `[5,0]` at the strongest supportable causal level, explicitly separating actual observations from compiled possible schedules and missing lock-admission times. If a candidate fails, follow other positively supported mechanisms and document counterexamples. |
| **D5AG-Q3 — Lifecycle consistency** | Establish what happens to the same resource source and its *complete* population across streaming shifts, source retirement, world/context changes, broad ProcGen reset, save-load reconstruction and a subsequent return/reconstruction. Distinguish retention, visited bypass with missing cache, restored persistent data, and genuinely new geometry. Identify when consumer/extractor stability is guaranteed, conditional, or not established; no assertion of an actual gameplay bug without evidence. |
| **D5AG-Q4 — Geometric reproducibility and discriminating evidence** | Determine which stable/variable inputs can change *complete* ordinary resource geometry across otherwise comparable generations; test or rigorously delimit any claimed equivalence of differing requests/masks. Produce an evidence-backed explanatory model and falsifiable predictions for any surviving stabilizing mechanism. If retail observations become indispensable, specify exact minimally sufficient measured operands and test contrasts **without running them**. |

**Original scope is not silently narrowed to:** first protected-map miss; replay of two allowed native schedules; identical resource labels; same-session cached reuse; the presence of a constant seed; or merely locating a terrain caller. These are intermediate findings, not substitutes for D5AG-CQ.

## Starting evidence and dependency discipline

Read repository `AGENTS.md`, `WORKFLOW.md`, `docs/PERMISSIONS.md`, `docs/SAVE_PROTECTION.md`, `docs/EVIDENCE_STANDARD.md`, `docs/EDITORIAL_STANDARD.md`, `docs/RESEARCH_EXECUTION_PROTOCOL.md`, `docs/reviewers/research-completion-reviewer.md`, and `docs/templates/completion-contract.md` **before actions**. Also read current `docs/RESEARCH_STATE.md`, D5R history, and the current checklist.

Begin with the **existing exact native and live evidence**, notably:

- `docs/experiments/resource-retained-population/d5s-report.md`, `d5w-normal-path-model.md`, `d5v-lifecycle-consumer-map.md`, D5T/D5U complete-geometry controls and maps;
- D5AD input-provenance, save-state and load chronology; D5AE scheduling; D5AF pre-lock/lock-admission results and candidate ledger;
- D5AB B2 authenticated direct target query `[5,0]`, mask `0x3`, successful visited-token store and later bypass; D5AC's earlier `[4,-1]` unvisited decision, later cache hit, and reset/Grid-clear reconciliation;
- the canonical `docs/experiments/resource-retained-population/resource-generation-gameplay-checklist.md` with stable GC IDs.

The **first substantive deliverable** is an evidence-backed **terrain→resource dependency map**, listing each producer, receiver, consequential operand, lifecycle owner, native location, ordering/synchronization condition, evidence status and relevant GC item. Trace only material dependencies, but **cross terrain subsystems where a real data/control/ownership/scheduling edge makes them relevant**. Do not stop because the next dependency is called TerrainDB, LOD, worldspace, cell streaming or content management. Nor should the brief become a general survey of unrelated rendering, grass, materials, visual effects or the complete terrain engine without such an edge.

## Research procedure

1. **Inventory hypotheses and distinguish guarantees.** Freeze competing, evidenced candidates: upstream canonicalization/priority; terrain task dependency/locality; lock admission and pre-lock delay; world/context persistence; exact output equivalence despite differing requests; other mechanisms only when source evidence justifies. Label each as established, plausible-with-evidence, falsified, or still open. Record why candidate evidence matters to *full geometry*.
2. **Trace authoritative inputs upstream.** For the exact target source and representative controls, follow effective original Int2, transformed geographic frame, owner/component, source identity/extent, BIOM, raster sample, seeds, definitions and any preparation state through actual producer/caller chains. Check both demand-driven density/layer and cell/terrain routes, and relevant source publication/retirement paths. Distinguish object/reference ownership from grid retention. Document exact native reader/writer and memory lifecycle constraints; do not infer the missing physical landing-zone tile size from unrelated grid parameters.
3. **Test construction authority against terrain scheduling.** Explain which terrain tasks can produce competing target requests, eligibility/ready/claim stages, and the protected-map miss; identify any mechanism restricting the *eligible request set*, canonicalizing coordinates or causing stable pre-lock/lock admission. Compare to B2 without inventing unobserved lock waits or scheduling timestamps. Challenge prioritization with rival runnable continuations and actual upstream dependencies.
4. **Trace cross-episode lifecycle.** Build a transition table for (a) first cold construction, (b) repeated same-session demand, (c) movement/shift and partial retirement, (d) world/context switch and broad reset, (e) save/load and return to an existing outpost. State exactly what survives as native geometry, what is recomputed, and which saved fields influence reconstruction. If an outpost/extractor-specific protection is asserted, prove its native consumer/producer relationship; otherwise mark it unknown.
5. **Compare *complete geometry*.** Reuse and, if materially necessary, extend bounded original-native geometric controls with independently verified source, frame, seed, mask and complete output serialization/normalization. Compare resources **and every retained region/point** under a documented coordinate frame; no list-only equivalence, image-only similarity or hash without a cross-checked canonical byte contract. Preserve the known mask-0 versus mask-3 difference and test proposed alternative equalities with controls.
6. **Resolve or characterize remaining gaps.** For each credible unresolved mechanism, identify the exact native producer/writer, lost historical operand or future runtime event needed. Provide specific falsifiable predictions and a discriminator table; a future retail trial must test a *candidate mechanism*, not merely sample more masks. Do not modify the observer or launch a live experiment.

Use fresh read-only/disposable Ghidra **project copies**, verifying original-project baseline and post-run unchanged hashes; do not open the original project for an operation that may write project housekeeping. Inspect original executable/data files read-only. Native fixtures operate only in owned disposable processes. Preserve protected Save52, backups and all original evidence; save examination is read-only on approved copies and only when it materially supplies a provenance dependency. All raw proprietary material remains LOCAL-ONLY. Follow both-drive 40,000,000,000-byte caller-available guard and existing preservation controls.

## Mandatory deliverables

Create in `docs/experiments/resource-retained-population/` (use consistent `d5ag-` names):

- **`d5ag-report.md`** — answers Q1–Q4 separately, then provides one coherent architecture/consistency explanation, what remains unknown and why, and implications for the checklist and D5R.
- **`d5ag-investigation-ledger.md`** — maintained during research, not invented retrospectively; hypothesis/branch, path checked, evidence, counterexample, disposition and next action.
- **`d5ag-terrain-resource-map.md`** — native producer/consumer/authority map with exact primary provenance and conditional/historical ordering distinctions.
- **`d5ag-lifecycle-consistency.md`** — transition and persistence model, explicitly distinguishing retained versus independently regenerated geometry and outpost consumer implications.
- **`d5ag-geometry-controls.md`** (plus reproducible local-only scripts/receipts as necessary) — complete geometry comparison methods, actual outcomes and counterexamples.
- **`d5ag-discriminators.md`** — mechanistic hypotheses, testable predictions and the smallest future runtime measurement plan *only if indispensable*; no unapproved trial.
- **Checklist update** to canonical stable-GC file plus an evidence/justification matrix. Change a tick only when original scope is met. Add material new tasks without renumbering or silently revising old ones. Keep GC-06/10/25/30/31 OPEN unless independently supported to their original standards. No overlap/non-overlap investigative item is introduced here.
- **`d5ag-review.md`** — original-contract criterion/question dispositions, independent engineering/scientific and editorial challenge, preservation/identity record, and complete/task-only diff inventory.

Diagrams are optional where they clarify a verified relationship. Do not create speculative images or use conceptual artwork as a substitute for primary native evidence.

## Mandatory acceptance criteria (frozen)

| ID | Pass condition |
|---|---|
| **D5AG-AC01 — Authority and baseline** | Required guidance read before actions; exact sources/build/snapshots pinned; original Ghidra project, protected saves and B1/B2 raw inputs unchanged; permitted operations only. Two concurrent sub-agents maximum, independently recorded. Deviations honestly reported and separately classified; never silently converted into PASS. |
| **D5AG-AC02 — Integrated dependency map** | Actual terrain→resource paths account for all consequential inputs/owners and active demand branches relevant to Q1, with causal evidence and an explicit treatment of unresolved material upstream links. Partial unrelated terrain mapping does not satisfy this. |
| **D5AG-AC03 — Construction consistency** | Tests evidenced candidates for authoritative request restriction/order and covers real source-map arbitration, competing schedules, B2 context, counterexamples and relevant alternative demands. Does not substitute mere non-FIFO or first-miss rule for the explanation. |
| **D5AG-AC04 — Lifecycle and persistence** | Traces retention, removal, reset and saved/reconstructed state through return/reconstruction, challenging whether any mechanism preserves exact geometry and any relevant extractor/outpost association. One-session caching does not satisfy cross-episode reproducibility. |
| **D5AG-AC05 — Geometry evidence** | Complete resource/region/point geometry or an independently defensible equivalent oracle tests relevant repeated and differing effective inputs; material differences and failures retained. No same-resource-list shortcut and no expansion into physical deposit overlap. |
| **D5AG-AC06 — Discrimination and question sufficiency** | Gives supported conclusions or carefully tested negative evidence for each frozen question, examines all material in-scope leads and produces falsifiable predictions. If indispensable historical/live data are absent, supplies terminal BLOCKED proof per protocol and precise smallest future measurement; no generic 'timing-dependent' closure. |
| **D5AG-AC07 — Checklist and parent continuity** | Preserves original GC meanings/IDs, updates evidence/ticks transparently, adds only relevant new dependencies, and keeps D5R/open parent scientific requirements explicit. No physical-overlap scope creep. |
| **D5AG-AC08 — Independent review and delivery** | Independent reviewer challenges exact original questions, evidence, alternative mechanisms and geometry counterexamples; optional specialist is not its own reviewer. Full source/editorial manual review, verified exact-final complete/task-only diffs and manifests, separate SCIENCE / ENGINEERING / EDITORIAL / PERMISSION dispositions. |

## Execution, delegation and completion contract

**Task type:** Original offline investigation with bounded native controls and authored findings. **Question-level outcome:** `COMPLETE` only with original question answered at required generality (including adequately controlled scoped negative); `INCOMPLETE / REWORK` if viable authorized investigation remains; `BLOCKED / ESCALATE` only with exact missing indispensable edge/evidence, attempts, alternative routes, barrier class and smallest required action. Independent `ACCEPT` cannot upgrade an open original question, and one method's failure does not close the parent. Separate scientific finding from integration and publication decisions.

Codex owns scope, integration and documentation. Optional specialist sub-agent for a bounded terrain/dependency or geometry/lifecycle task. **At most two active sub-agents concurrently**; count before invoking the independent reviewer. Reviewer must not implement the work it reviews, must receive the original brief, complete ledger, original primary evidence, methods, failures and exact tree/snapshot. Use `docs/reviewers/research-completion-reviewer.md` and `docs/EDITORIAL_STANDARD.md`. On REWORK, correct/retest/re-review under the same brief; no new brief for ordinary in-scope failed tests. Record cybersecurity interruptions as observed (suspected false positives only where appropriate), neither conceal/refashion work to bypass a refusal nor pre-emptively abandon legitimate authorized research.

**Not authorized:** production SFSE observer, bridge, hook, reducer or operational controller modifications; Starfield launch/deployment/attachment; save or Ghidra original-project mutation; publication, raw-data disclosure, Git stage/commit/push; live B2/B3 or any new retail attempt. Retain existing safety and evidence requirements. A future run requires distinct maintainer approval after a concrete evidenced candidate and discriminator are reviewed.

**Handoff:** stable question/criterion matrix; primary native/source/save/fixture references; completed and counterexample tests; authoritative explanatory model versus hypotheses; exact unresolved dependencies/next actions; checklist diff; independently reviewed report; task-only and complete Git diffs (including untracked authored files), snapshot/manifest; no falsely reported completion. Any authority escalation is a narrow request, not a science PASS.
