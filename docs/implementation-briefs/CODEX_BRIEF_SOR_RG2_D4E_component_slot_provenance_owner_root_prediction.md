# Codex research and implementation brief — RG2-D4E

**Title:** Native Component Resource-Slot Provenance and Predictive Owner-Root Reconstruction  
**Project:** `D:\Projects\starfield-outpost-research` / `gooberpede/starfield-outpost-research`  
**Authority:** Offline native analysis, read-only installed-data extraction, original analytical implementation, synthetic tests, independent review. **No Starfield launch, retail debugger attachment, live sampling, staging, commit, push, release or publication.**  
**Status:** Assignment proposed for implementation; freeze the acceptance criteria below before execution.

## 1. Scientific question and baseline

RG2-D4D Phase B captured an ordered Archimedes III owner-root component-map construction. Its witnessed generator-resource sequence was **Water, Water, Tungsten, Chlorine**. The traced origins include Tungsten in component 2 slot 0, one Water in component 2 slot 5, another Water in component 7 slot 5, and the selected Chlorine family root. The map-builder's append/exchange operations transfer the earlier Lead-associated array into the selected Chlorine-root entry. The two identical Water operands cannot be assigned a unique order of origin after sorting.

The prior offline model reproduces most component fields but projected **zero at slot 5** for seven of eight ordered components (components 0–5 and 7); component 6's six slots match. The first mismatch is **component 0, slot 5**, component-relative byte offset `0x88` (payload-relative `0x68`). This is a discrepancy in **component-slot population**, not an invitation to hard-code Water, Tungsten or a repaired final candidate list. The previous D4C result remains **ESCALATE**; preserve that judgment and its original conditional reconstruction.

Separate established facts: terrestrial Water passes a biome-resource admission route; atmospheric resources are read from effective `ATMO` definitions. The two ordinary-loop Water calls used zero effective weights and do **not** represent two finite Water deposits or a terrestrial-plus-atmospheric pair. Do not conflate those systems.

Read the current project instructions and evidence before changing code: `AGENTS.md`, `WORKFLOW.md`, `docs/RESEARCH_EXECUTION_PROTOCOL.md`, `docs/EVIDENCE_STANDARD.md`, `docs/EDITORIAL_STANDARD.md`, `docs/PERMISSIONS.md`, `docs/templates/completion-contract.md`, and `docs/reviewers/research-completion-reviewer.md`. Relevant research includes `docs/experiments/resource-owner-acquisition/` (especially `phase-b.md`, native/review records), `docs/experiments/resource-owner-root/`, `docs/experiments/resource-tungsten-repair/`, `docs/experiments/resource-tungsten-acquisition/`, `docs/experiments/resource-save52-d3/`, `docs/experiments/resource-standalone/` and `docs/experiments/resource-pattern-selection/`. Verify exact current filenames and local evidence references instead of assuming this list is exhaustive.

## 2. Required work

### A. Establish the producer of resource slot 5

Trace component initialization, deserialization, copy/transformation and slot-writing dataflow backward from the known runtime `+0x88` slot and associated owner/component structures. Use pinned native instructions, existing hashed exports and installed definitions. Determine whether the resource is serialized directly, inherited/derived, initialized by a default, or inserted via another owner/component transformation. Record the exact writer, field widths, offsets, ordering, and provenance with separate **STATIC**, **INSTALLED**, **DERIVED** and **RUNTIME-WITNESS** labels. A source/record identification guessed from Water's expected value is not proof.

Investigate all six slot producers sufficiently to verify their relationship to slot 5, including zero and duplicate entries. Distinguish the record's raw serialized representation from its initialized runtime form; the portable corpus should contain only the real inputs needed to reproduce initialization.

### B. Independently reconstruct the eight ordered components

Using only independently extracted installed definitions and supported initialization rules, produce an ordered, versioned eight-row Archimedes component reconstruction: identities, family/root keys, all six resource slots (including zeros and duplicates), and relevant selection/ownership context. **Do not inject captured runtime slots, expected Water/Tungsten labels or the known final candidate sequence into the builder.** Freeze and hash the result **before** the comparator opens the D4D held-out component and map receipts. Show bit/identity comparisons for each slot, with exact mismatch reasons.

### C. Replay the actual owner-root map algorithm

Implement or extend the general native-equivalent append, staging-array, exchange, displaced-array and root-keyed map logic. Preserve traversal order, duplicates and intermediate arrays; do not automatically deduplicate or alphabetize. Compare **each witnessed intermediate state** and final selected-root candidate list against existing captures only after freezing the independent reconstruction. Explain the derivation of `Water → Water → Tungsten → Chlorine` if established; otherwise pinpoint the first unsupported producer/transition and preserve all mismatches.

### D. Integrate only verified general rules

If the evidence establishes the correct slot and map mechanisms, version the standalone corpus builder/predictor and update the authored algorithm/corpus specifications. Do not install an Archimedes-specific Water fix or select component order to fit the witness. Identify every added field and its upstream dependency; measure incremental **local** corpus bytes without reopening general compression or performance work. Extracted ESM payloads, corpora, native exports and raw receipts remain ignored/local-only; authored algorithm/specification and original research code may remain tracked subject to rights review.

Run a complete cross-site regression: all **seven Feynman/Carinae native regions**, all **three Archimedes native-region controls** (Tungsten plus two Chlorine), preserved historic D1/D2/D3 predictions and the Save52-wide classification inventory. Do not silently reclassify unresolved positive associations. A new supported prediction must be versioned separately from frozen earlier outputs.

### E. Discriminate and escalate constructively if incomplete

If the actual producer or effective component order cannot be inferred offline, identify the **first missing native operand** and why existing static/installed evidence cannot supply it. Propose a tightly bounded extension of the working acquisition machinery with an exact observation contract, identity/coherence join and completed draft run card. This work **does not** authorize implementation against the retail game or a live attempt. Do not present another generic 'context unknown' conclusion without a specific falsifiable next step.

## 3. Mandatory acceptance criteria (frozen AC1–AC8)

**AC1 — Authority and preservation.** All original saves, protected historical evidence, installed data, frozen predictions, Git HEAD and index remain unchanged. No live game or other unauthorized actions. Retain local raw inputs under approved ignored paths and preserve failed attempts.

**AC2 — Sixth-slot provenance.** Provide native source-backed evidence of the component slot-5 producer/initialization semantics, including exact offset domains, or a precise, demonstrably missing producer and observation path. Distinguish raw serialized values from runtime initialized fields.

**AC3 — Independent component reconstruction.** Reconstruct and freeze eight ordered six-slot component records from authorized installed inputs before opening the held-out D4D witness for comparison. Report every slot including zeros and duplicate resources.

**AC4 — Predictive owner-root map.** Reproduce the intermediate map/staging/exchange history and final `Water, Water, Tungsten, Chlorine` sequence using general logic, or identify the earliest specifically evidenced divergence. Matching a final list while intermediate states disagree is insufficient.

**AC5 — Generalization and regression.** Preserve seven Feynman/Carinae and three Archimedes exact native geometry controls, evaluate the complete Save52 cohort, preserve frozen historic baselines and independently account for any new corpus field/byte cost. No site-specific fitting.

**AC6 — Substantive scientific progress.** Either independently close the slot/map discrepancy or materially narrow it to a specific unavailable operand with a qualified concrete acquisition route. A speculative replay built from observed answers does not satisfy this criterion.

**AC7 — Durable evidence and editorial finalization.** Deliver reviewed algorithm and corpus revisions where justified, provenance/operand ledgers, frozen hashes, commands, tests, mismatch tables and a complete compliance record. Run the established automated editorial screen, manually read **all changed prose**, and resolve malformed word/number joins, encoding faults, ambiguous address/offset/identity domains and inflated scientific claims. Use conventional `0x` notation without redundant decimal annotations.

**AC8 — Independent exact-snapshot review and delivery.** An independent critic must challenge AC1–AC7 against actual primary bytes/code/tests, validate blind-prediction separation and negative conclusions, and return `ACCEPT`, `REWORK` or `ESCALATE`. Preserve review defects and corrections. Deliver verified **complete and task-only unified diffs**, changed/untracked/exclusion manifest, SHA-256 values, exact forward/reverse applicability, protected hashes and unchanged index/HEAD. Final post-review changes require independent delta approval; no automatic commit/push.

ACCEPT must not be inferred solely from test success. If the necessary scientific input cannot be recovered under the authorized scope, preserve a candid ESCALATE assessment while delivering the strongest verified partial result.

## 4. Deliverables and stopping rules

Tracked research documents should provide: a concise direct answer; an exact slot-producer dataflow ledger; ordered eight-component comparison; before/after owner-root map-state table; frozen independent candidate prediction and native comparison; standalone corpus changes and byte deltas (if established); regression/accounting matrix; explicit unknowns; next acquisition contract if needed; independent science/engineering/editorial review. Implementation and original synthetic tests may be tracked within the research boundary. Primary proprietary content must not enter diffs.

No Starfield launch, runtime debugger attachment, new save production, forced generation, cache modification, application integration, publishing, cleanup or release verification. **B6 remains on hold.** Return the verified patch package and completion report for maintainer review; do not stage or commit.
