# Codex research / implementation brief — RG2-D3

## Save52 Predictor Discrepancy and Coverage Investigation

**Status:** Issued for offline execution only. **Branch/repository:** current `starfield-outpost-research` checkout, working tree as found. **Research baseline:** committed RG2-D1 and RG2-D2, plus all accepted RG1/RG2-C1/C2 evidence. **Publication:** B6 remains on hold.

### 1. Research question and mandated outcome

Investigate **all** unresolved RG2-D2 Save52 discrepancies and coverage classes, beginning with the Archimedes III Tungsten potential false negative, and extend the standalone geometry predictor only where installed-data and native evidence support the missing mechanism. Distinguish source/resource **selection**, generation, geometric intersection, and non-spatial extractor admission. Preserve the original blind D2 results intact.

The aim is a **versioned, evidence-backed expansion in scientific coverage**, not maximizing a success percentage or optimizing speed. An acceptable unresolved result identifies the exact missing operand/branch and a constructive, actionable acquisition route; it must not stop at a generic `UNKNOWN` or an enlarged backlog.

### 2. Authoritative inputs and scope

Read the governing instructions first: `AGENTS.md`, `WORKFLOW.md`, `docs/RESEARCH_EXECUTION_PROTOCOL.md`, `docs/EVIDENCE_STANDARD.md`, `docs/EDITORIAL_STANDARD.md`, `docs/PERMISSIONS.md`, `docs/templates/completion-contract.md`, and the independent-reviewer procedure. Freeze the original AC1–AC8 from **this brief** before doing substantive work.

Prior findings to reuse (check current repository paths and indices, do not assume these are exhaustive):

- `docs/experiments/resource-standalone/` — validated standalone geometry pipeline, algorithm, corpus, native controls, local-only corpus policy.
- `docs/experiments/resource-save52/` — D2 frozen roster, predictions, comparison, 17 saved-active qualified outposts, two disabled, eight fully predicted held-out sites, one partial-positive site, six unsupported sites, 16 corroborated ordinary extractor pairs, one potential false negative, 18 indeterminate associations, and four separately assessed Water associations. Reconcile individual row accounting from D2 primary tables rather than inferring totals from this summary.
- `docs/experiments/resource-geometry/`, `docs/experiments/resource-source-enumeration/`, `docs/experiments/resource-pattern-selection/`, `docs/experiments/resource-selection-operands/`, and the native availability / Water admission research.
- Save52 protected corpus and installed definitions, within established read-only/source-hash controls. Existing native captures are reference evidence, never inputs used to select a desired new prediction.

**New first-party Archimedes III observation** (user screenshot set dated 24 October 2026): outpost labelled `ARCH III W H2O LUB` visibly offers **Tungsten**, **Chlorine**, terrestrial **Water** and atmospheric **Water Vapor** extraction. One contiguous highlighted Tungsten deposit was seen; multiple spatially separated Chlorine patches were seen. The screenshots **do not** identify individual native paths, prove component/generator inputs, or establish that each contiguous patch consists of one region. Distinguish screenshot-visible facts from the maintainer's report and from model inferences. Retain original files as protected/local evidence, with authored references and screenshot provenance in tracked records where appropriate; no proprietary image publication is authorized by this brief.

**In-scope tracks (all mandatory for accounting):**

A. **Archimedes III Tungsten:** Offline predictor omitted Tungsten while a saved extractor and new in-game highlighted vein corroborate its presence. Test effective BIOM/component/family selection first; then eligible source identities, masks, generation operands and finally spatial predicates if selection occurred. Keep Chlorine as a positive control. Treat atmospheric/terrestrial Water separately from ordinary finite veins.

B. **Nonuniform masks:** All D2 affected Feynman cases, including the correctly identified active second Feynman V outpost and Feynman VIII-b. Revisit existing native mask/selection semantics. Implement a faithfully reconstructed mechanism when qualified; no uniform-mask shortcut masquerading as equivalence.

C. **Other unsupported branches:** Special Helium-3, no-selected-family configurations, and any other distinct D2 unsupported reason. Identify whether they belong in ordinary geometry or a separate availability/admission path. Implement only supported behaviour.

D. **Complete D2 dispositions:** Preserve and account for every held-out case and each of the 18 indeterminate associations, grouping shared root causes without asserting that missing installed extractors imply missing deposits. Disabled/deleted outposts remain excluded from ordinary predictions but still count according to existing documented selection accounting; do not add them because residual records survive.

### 3. Ordered execution method

**A — Freeze and audit.** Snapshot and hash the committed D1/D2 model, corpora, original blind predictions, native controls, eligible case roster, current installed-data hashes, and protected inputs. Establish one immutable **baseline-to-revision comparison**. Do not retroactively alter D2's blind results or its holdout definitions.

**B — Diagnostic hypothesis ledger.** For each affected case/class, record the expected resource(s), actual positive evidence, predictor output/state (`PRESENT`, `ABSENT`, `UNSUPPORTED`, `INDETERMINATE` as appropriate), exact failing stage, candidate explanations, necessary discriminators and evidence provenance. Distinguish unsupported computation from computed absence. Prioritize Archimedes but investigate all classes.

**C — Targeted static/offline reconstruction.** Reuse native export windows and installed record consumers to reconstruct missing BIOM/component, nonuniform mask, Special, and no-family branches. Identify the precise upstream caller, selected definition/field, default/override, branch decision and numeric domain. If a field or branch cannot be established, say so rather than inventing a value. Do not choose a biome, source anchor, seed, setting or resource family because it yields desired output.

**D — Versioned implementation where justified.** Extend corpus extraction/schema and reproducer only for supported semantics, with tests for field necessity and correctly missing data. Keep extracted corpus, full generated payloads, raw native evidence, and installed files **local-only/ignored**; authored algorithm/specification amendments, source references, code and bounded result summaries may be tracked subject to established release gates. Do not integrate with the Outpost Tracker. Do not optimize performance in this task.

**E — Reproduce and cross-validate.** Rerun **all** original Save52 held-out cases and D1/D2 supported requests on the revised model, documenting changes in case classification and resource membership. Preserve all **seven exact native region controls** (four Feynman, three Carinae) including ordered binary32 points/widths and native bounds; do not silently degrade the earlier exact correspondence. Compare newly supported positive witnesses and record unverified predicted additions neutrally. No retrospective fitting or comparison-led parameter tuning.

**F — Constructive escalation where needed.** For each unresolved common dependency, identify the smallest native/serialized observation that would distinguish the remaining hypotheses; reuse available controllers and prepare a technically qualified capture design and **complete prospective run card** if and only if further live evidence is needed. Include exact target, relevant runtime identities, expected distinguishing values, first useful sample, evidence/durability, stop/no-hit/abort logic, preflight and postflight hash-protection, and bounded fallback. Ordinary exitsave/autosave rotation is **diagnostic only**; designated research/manual/quicksaves and protected archival backups remain protected. **Do not execute the live card in D3.**

### 4. Scientific and reporting discipline

- Do not equate saved extractor resources to a complete ground-truth availability list. Positive corroboration is useful; absence of equipment is not an absence result.
- Do not equate contiguous visible overlays with one generated vein/path, or different patches with a fixed number of paths.
- Keep **geometry correctness**, **predictor coverage**, **validation coverage** and **observed resource agreement** as separate measures; do not calculate a misleading global accuracy percentage.
- Separate loaded/retained historical geometry from freshly generated geometry; distinguish runtime source slot, source identity, manager context and generation epoch.
- Use only independently grounded input alternatives in replay; preserve comparison-failing attempts and negative results.
- Protect immutable frozen predictions and previous raw receipt files. Changes to production or publication eligibility are out of scope; B6 remains on hold.

### 5. Required durable deliverables

Under a new `docs/experiments/` folder appropriate to D3, produce:

1. **Research report** answering each track, including positive results first, evidence grades, remaining limits and a concise scientific disposition.
2. **Complete D2-to-D3 case matrix** keyed by prior stable case/outpost IDs, with all eligible, excluded, partially supported and indeterminate cases accounted for, initial versus revised predictions, independent witnesses, and per-class reason codes.
3. **Archimedes case record** recording the new screenshot observations and separating Tungsten/Chlorine finite veins from the two Water-admission routes.
4. **Native operand/definition provenance ledger** with exact source hashes/addresses, field domains, source selection and new corpus requirements.
5. **Versioned predictor/corpus amendments and test results** where justified, never rewriting the frozen baseline; local-only generated data under ignored storage.
6. **Coverage and comparison summary** that distinguishes new corroborated positives, remaining genuine potential false negatives, unsupported cases and indeterminate comparisons.
7. **Acquisition proposals and prospective run cards** only for unresolved dependencies requiring live evidence.
8. **Review/evidence/delivery package**, including failures and corrections, full commands, test results, local/trackable exclusions, independently verified hashes and exact complete/task-only diffs.

### 6. Frozen acceptance contract (AC1–AC8)

- **AC1 — Authority and preservation:** Offline-only authority honored; installed EXE/ESM, original saves/backups, raw captures, frozen D1/D2 predictions, controls, HEAD/index and protected inputs unchanged. Correct transient-save policy applied in any prospective card.
- **AC2 — Full D2 accounting:** Every held-out outpost, every D2 unsupported class, the Archimedes discrepancy and 18 indeterminate associations receive explicit, traceable dispositions; no convenient exclusions.
- **AC3 — Archimedes discriminator:** An evidence-based attempt localizes Tungsten's first selection/generation/query disagreement, correctly classifies Chlorine and treats terrestrial/atmospheric Water independently; user screenshots recorded with correct evidentiary limits.
- **AC4 — Mechanism reconstruction:** Nonuniform-mask, Special and no-family branches are investigated against exact native/installed evidence; supported mechanisms are implemented and tested where possible, with no speculative substitutes.
- **AC5 — Generalization and regressions:** Baseline/revision comparison covers the entire D2 population and all seven exact native controls; no case-specific fitting; unsupported and negative results reported accurately.
- **AC6 — Material scientific progress:** Each gap class is resolved, precisely localized or provided with an actionable, falsifiable acquisition route. Merely re-listing unsupported cases or proposing repetition of known gameplay observations fails.
- **AC7 — Durable specification and editorial quality:** Data/schema/algorithm changes, versioned outputs, reproducible checks and all changed prose finalized under `docs/EDITORIAL_STANDARD.md` with automated screening, manual reading, conventional numeric notation, scientific-claim fidelity and zero unexplained material defects.
- **AC8 — Independent review and exact delivery:** Independent reviewer critiques original contract, primary tests, saved evidence and exact final changed-tree snapshot; reviewer may demand REWORK. Complete/task-only patches and manifest reconstructed/apply/reverse exactly; final delta gets reviewer approval; nothing staged, committed or pushed.

### 7. Stop/return and permissions

Do the substantive offline work and authorized tests now; do not return early with a feasibility-only report if implementable native-supported mechanisms remain. Report genuine blockers with bounded evidence and actionable next experiments rather than guessing. No Starfield launch, new save production, process attachment, debugger instrumentation, installed game mutation, cleanup, publication, Git staging, commit, push or PR is authorized by this brief. Any live trial needs **a new, reviewed run card and explicit maintainer approval**. Final response should include the exact changed/new-file manifest, AC matrix, independent verdict and links to local complete/task-only diffs, noting proprietary/ignored exclusions.
