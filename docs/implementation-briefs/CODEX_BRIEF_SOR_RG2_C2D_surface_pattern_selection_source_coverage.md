# Codex research and implementation brief — RG2-C2D

## Native surface-pattern selection and source-coverage reconstruction

**Project:** `D:\Projects\starfield-outpost-research` / `gooberpede/starfield-outpost-research`  
**Authority:** Phase A, **offline only**. No Starfield launch, debugger attachment, live data acquisition, forced regeneration, save modification, staging, commit, push, release or publication.  
**Build scope:** pinned `Starfield.exe` 1.16.244.0 and corresponding installed, hash-verified definitions. No unqualified transfer of static VAs or results across executable builds.  
**Scientific status:** prospective investigation; do not amend established findings or frozen predictions in place.  
**Publication:** B6 remains on hold.

## 1. Question and rationale

RG2-C2C showed that Carinae III-a's accepted Iron, Alkanes and Rothicite regions can be generated exactly from the existing geometry algorithm **when supplied with the surface-pattern identity retained in a native source**. That observation yielded SFPT `0x00212e16`, while the frozen ordinary-initialization model selected `0x00212e19` at the relevant coarse cell. Under the witnessed pattern, source enumeration discovers anchor `(-12, -12)` without that anchor being supplied, and a whole-source replay matches the three native regions exactly. Feynman's four native region matches remain intact.

**Open question:** What *upstream, independently recoverable* inputs and native decision sequence select the effective SFPT for a coarse terrain cell? Can the offline model select Carinae's `0x00212e16` **without consulting the observed SFPT identity or downstream observed source anchor**?

Treat the observed Carinae pattern and three matching paths as **held-out validation witnesses**, not selectable input parameters. Do not infer universal source or region completeness from seven exact accepted-region matches across the two planets.

## 2. Required source review and preserved baselines

Read and follow `AGENTS.md`, `WORKFLOW.md`, `docs/PERMISSIONS.md`, `docs/EVIDENCE_STANDARD.md`, `docs/RESEARCH_EXECUTION_PROTOCOL.md`, `docs/EDITORIAL_STANDARD.md`, `docs/templates/completion-contract.md` and `docs/reviewers/research-completion-reviewer.md`. Freeze AC1–AC8 below before implementing.

At minimum, consult:

- `docs/experiments/resource-source-enumeration/{report.md,inventories.md}` and corresponding before/after/candidate inventories, code and reviewer evidence.
- `docs/experiments/resource-geometry/{report.md,native.md,evaluator.md}` and the surface-pattern/CRC/registration-source evidence they cite.
- `docs/experiments/resource-geometry-mature-context/` and `docs/experiments/resource-installed-settings/` for Feynman/Carinae frozen and corrected predictions.
- `docs/experiments/resource-carinae-source-context/{phase-b.md,phase-b-results.json}` and `docs/experiments/resource-carinae/{phase-b.md,phase-b-review.md}` for *held-out* native observations and evidence limits.
- Relevant native-availability and source/seed lineage records. Use existing hash-pinned native exports and installed definitions rather than generating broad new dumps without an evidenced need.

Existing results to preserve: Carinae source `(-12, -12)` and observed SFPT `0x00212e16`; previously frozen candidate `0x00212e19`; 48 unresolved fine cells of the 272-cell Carinae halo under the witnessed pattern; four exact Feynman and three exact Carinae native-region correspondences. Keep observed, derived, static and predicted classifications distinct.

## 3. Scientific workstream A — native pattern-selector lineage

Trace, in bounded native code and data, the chain from requested planetary/coarse-cell context to selected SFPT. Specifically establish or delimit:

1. Runtime SFPT registration and actual candidate order. Distinguish registration order, installed record order, lookup/hash iteration order and style-filter result order; do not silently substitute one for another.
2. Effective BIOM/surface style and candidate eligibility, including absent and invalid candidate handling.
3. Surface seed and planetary identity inputs; exact CRC/PRNG operands, draw sequence, candidate indexing or weighted selection, where supported. Verify how these relate to the previously reconstructed surface CRC and default seed without assuming the default is the observed runtime value.
4. Orientation, rotation, reflection, source/block selection, cache state and initialization mode **only insofar as they can change SFPT identity or applicable lookup**.
5. The distinction between selecting a coarse SFPT and resolving its constituent SFBK/source anchors.

Produce a **selection trace** per tested coarse cell recording candidate identities and order, supported seed/identity operands, intermediate numeric decisions, selection outcome and evidence/provenance. Include explicit `UNKNOWN` at unsupported steps, rather than inventing a complete trace.

## 4. Scientific workstream B — blind predictive validation

Implement or extend an offline selector driven only by independently supported *upstream* inputs. Keep the selected pattern witness inaccessible to the selector's decision logic: design a clear predictor/validator separation (for example, input manifest versus read-only expected-result check). The expected SFPT must not be used to rank candidates, tune a seed, choose an order or select a conditional branch.

- **Primary held-out case:** Carinae III-a coarse cell previously predicted as `0x00212e19`; after calculating the result, verify whether independent prediction yields `0x00212e16`.
- **Cross-site check:** Apply the same documented selection semantics to Feynman V, including both relevant coarse cells and its conditional pattern/source population. Do not claim unobserved Feynman SFPTs are runtime-proven.
- Produce before/after source inventories, with an **inclusion/exclusion reason** for every tested source/cell, including source identity, pattern identity, eligibility/coverage rule and uncertainty.
- If the selector can be resolved, rerun installed-settings resource geometry without modifying underlying mathematical generation logic. Test all seven established native accepted-region matches; preserve Feynman's four exact controls.

A predictor that is handed `0x00212e16`, the retained source's anchor or a downstream geometry-matching score is **not independent predictive validation**. A candidate envelope containing the right answer but not selecting it is **not a successful prediction**.

## 5. Scientific workstream C — invalid-block fallback / coverage

Independently investigate the 48 unresolved Carinae fine cells under the witnessed pattern. Determine whether each class arises from valid native empty/invalid blocks, neighbour delegation, indexing/orientation/translation error, cache-dependent fallback or unsupported source selection.

- Trace the bounded native lookup and fallback instructions, with explicit coverage and counterexamples.
- Record before/after cell-level classification and any source identities thereby added, removed or still indeterminate.
- Keep **SFPT selection correctness** separate from **complete source coverage**. Do not infer a complete planetary source census from successful reproduction of the three observed paths.
- Do not force an artificial resolution to every cell if the evidence is insufficient. A bounded, evidenced `UNKNOWN` with a precise missing dependency is acceptable for this secondary workstream.

## 6. Methodology, limits and escalation

Favor the existing native-source evidence, installed Starfield definitions, exact offline algorithms and small independent fixtures. Permit read-only bounded additional static native exports if necessary and source-pin them. Avoid broad genome-like scans, brute-force seed search, Carinae-specific anchor patches, or fitted parameters chosen to match the held-out pattern or region geometry.

If runtime registration, initialization state, cache epoch or another effective input is genuinely unavailable offline, identify its **exact producer/consumer boundary**, data type/domain, likely natural trigger, and scientific discrimination value. Prepare a specific collector extension, safety qualification plan and approval-ready run card **only if needed**. Do not execute any live operation under this brief. Do not reuse past NO-GO instrumentation unchanged.

A concrete missing native operand, with a testable acquisition route and evidence that existing offline sources cannot settle it, is acceptable scientific progress. Merely restating the five compatible Carinae SFPTs and repeating `UNKNOWN` is not.

## 7. Verification and deliverables

Deliver durable, project-conventional artifacts: scientific report, exact native/definition source ledger, predictive-selection contract/trace, source and cell before/after inventories, scripts and tests where useful, held-out validation results, precise coverage limits, and a concrete next discriminator if unresolved. Link through experiment navigation and update research state consistently without changing accepted historical reports or frozen predictions.

Required checks include: determinism under repeat runs, meaningful negative/counterexample tests for registration order, candidate eligibility, seed/draw and invalid-block fallbacks; hash/protection checks; Feynman and Carinae exact-geometry regressions where their qualified inputs exist; and clear separation of tested from derived claims. Never replace missed observations with a predicted empty list.

**Mandatory editorial finalization:** Screen *all changed authored text* under `docs/EDITORIAL_STANDARD.md`, including prose, Markdown tables, captions, CSV descriptions, headings, summaries and changed code comments. Manually check run-together words/numbers, encoding, conventional `0x` notation for addresses/FormIDs/member offsets, numeric domains, source/slot/epoch distinctions and claim-strength consistency. Avoid redundant `(decimal)` labels and gratuitous conversions. Independent reviewer must review exact final changed text; any post-review change requires scoped delta review. Record screening commands, diagnostics, resolutions and reviewer disposition.

**Review/delivery:** Invoke a genuinely independent reviewer against the original frozen criteria, evidence, actual changed tree and source scripts. Preserve REWORK cycles and failures. Provide original/specific AC matrix, primary evidence references, protected-before/after results, exact complete and task-only diffs plus changed/new/excluded manifest, SHA-256 hashes and verified forward/reverse applicability. No staging/commit/push. Return a concise summary and suggested commit message.

## 8. Frozen acceptance criteria

| Criterion | Mandatory requirement |
|---|---|
| **AC1 — Authority and preservation** | Offline only; exact pinned inputs; existing saves, captures, installed definitions, frozen predictions, HEAD and index protected and checked. |
| **AC2 — Native selector lineage** | Evidence-bound trace of SFPT registry, order, eligibility, seed and native decision route, with unknowns and provenance identified. |
| **AC3 — Independent Carinae prediction** | Run witness-blind selection from qualified upstream inputs; explicitly classify exact prediction of `0x00212e16` versus unresolved missing inputs or falsification. No answer leakage or fitting. |
| **AC4 — Fallback and coverage** | Examine and classify the 48 unresolved Carinae cells through a bounded native lookup/fallback investigation, without unsupported completeness claims. |
| **AC5 — Cross-site validation** | Before/after source inventories with inclusion reasons; Feynman checks and preservation of seven exact captured-region matches where applicable. |
| **AC6 — Scientific discrimination** | Deliver a predictive selector or materially narrow the missing selector operand/rule with a concrete, qualified next acquisition route; repeating a candidate list is insufficient. |
| **AC7 — Durable technical and editorial record** | Reproducible code/traces/tests, scientific limitations, zero unresolved material editorial defects and manual finalization record. |
| **AC8 — Independent review and exact delivery** | Independent science/editorial review of final snapshot, PASS/FAIL/NOT TESTED matrix, preservation and verified complete/task-only patches; no unauthorized integration. |

**Completion policy:** AC1–AC8 are frozen. A supported negative/bounded result can pass if its mandated discrimination and evidence requirements are met; a preferred positive prediction is not guaranteed. An unexamined actionable lead, missing tests, or reviewer REWORK is unfinished. If another live experiment is proposed, user approval after run-card review remains a separate gate.

## 9. Requested completion response

Report (a) Carinae selected SFPT outcome and whether it was truly predicted, (b) exact source/enumeration/fallback status and remaining unknowns, (c) seven native-region regression state and Feynman implications, (d) editorial finalization/reviewer disposition, and (e) the exact locally generated diff/manifest paths and commit suggestion. Explicitly state **no live test was performed** and **B6 remains on hold**.
