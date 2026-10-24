# Codex research and implementation brief — RG2-D5

**Title:** Feynman Construction-Mask and Component-Selection Reconciliation  
**Project:** `D:\Projects\starfield-outpost-research` / `gooberpede/starfield-outpost-research`  
**Authority:** Offline research, read-only examination of existing saves/native evidence/installed definitions, local corpus building, analytical implementation and synthetic tests. **No Starfield launch, retail debugger attachment, live acquisition, new gameplay saves, staging, commit, push, release or publication.**  
**Status:** Proposed for execution. Freeze AC1–AC8 below before implementation; do not expand authority by interpreting this brief as approval for a later run card.

## 1. Scientific objective and baseline

RG2-D4E recovered the general component resource-slot initializer and predictive owner-root construction, independently reproduced Archimedes' `Water, Water, Tungsten, Chlorine` candidate sequence, and preserved ten exact native geometry controls: four Feynman V, three Carinae III-a and three Archimedes III. RG2-D2/D3 preserve the independent Save52 blind predictions and subsequent coverage results. Following D4E, **nine resource associations remain indeterminate**: seven primarily affected by nonuniform **first source-construction-query** resource masks, and two by effective alternate component/descriptor precedence at Feynman III. These are known research gaps, not demonstrated negative resources.

This assignment addresses two separate mechanisms, in priority order:

- **Track A — nonuniform construction-query resource masks.** Determine the exact initial source-construction query and native mask sampling. The initial mask can differ from the masks sampled by later resource-cell queries. Do not substitute a beacon-point query or choose a mask because it agrees with gameplay.
- **Track B — effective component traversal and descriptor selection.** Establish which ordered component/BIOM/RSGD context wins at Feynman III, including visitation, alternate handling, failure and selection semantics. Do not select a descriptor simply because it admits Uranium or Vanadium.

A successful result must reconstruct independently supported inputs for the standalone predictor, test their generality against the **entire qualified Save52 cohort**, and account individually for all nine indeterminate associations. Partial resolution is acceptable only with precisely localized missing operands and a concrete acquisition route; do not relabel unsupported cases as absent.

### Governing workflow and research references

Read and obey current `AGENTS.md`, `WORKFLOW.md`, `docs/PERMISSIONS.md`, `docs/RESEARCH_EXECUTION_PROTOCOL.md`, `docs/EVIDENCE_STANDARD.md`, `docs/EDITORIAL_STANDARD.md`, `docs/templates/completion-contract.md`, `docs/reviewers/research-completion-reviewer.md`, and `docs/SAVE_PROTECTION.md` where relevant. Treat these live repository files as authoritative over any illustrative workflow phrasing here.

Inspect at minimum `docs/experiments/resource-save52/`, `docs/experiments/resource-save52-d3/`, `docs/experiments/resource-slot-provenance/`, `docs/experiments/resource-owner-root/`, `docs/experiments/resource-selection-context/`, `docs/experiments/resource-standalone/`, `docs/experiments/resource-geometry/`, and current related native source registers. Verify actual filenames/paths rather than assuming this list is exhaustive. Reuse prior C1G/D4 native selection work, D4E owner-root/slot initialization and D4C SFPT layout correction rather than restarting general reverse engineering. Pin exact supported executable/installed definition identities; previous results were scoped to `Starfield.exe` 1.16.244.0, not arbitrary builds.

## 2. New first-party gameplay evidence: 24 Feynman screenshots

The maintainer supplied `screengrabs-feynman.zip` in the conversation, containing **24 original JPEG screenshots**. The archive covers these three Save52 outposts (classification from the preceding inspection; verify actual visible outpost labels in every image):

| Outpost | Images | Relevance |
|---|---:|---|
| Second **Feynman V Cu IL F** | 8 | Nonuniform resource-mask case; **active**, not deleted |
| **Feynman VIII-b Au Sb** | 7 | Nonuniform masks; historical deposit-instability lead remains unproven |
| **Feynman III V U** | 9 | Alternate-component/RSGD ordering and Uranium/Vanadium |

The archive's filenames, in their original order, are `20261025093456_1.jpg`, `20261025093502_1.jpg`, `20261025093514_1.jpg`, `20261025093526_1.jpg`, `20261025093535_1.jpg`, `20261025093547_1.jpg`, `20261025093556_1.jpg`, `20261025093603_1.jpg`, `20261025093709_1.jpg`, `20261025093746_1.jpg`, `20261025093753_1.jpg`, `20261025093806_1.jpg`, `20261025093826_1.jpg`, `20261025093847_1.jpg`, `20261025093907_1.jpg`, `20261025094006_1.jpg`, `20261025094010_1.jpg`, `20261025094015_1.jpg`, `20261025094026_1.jpg`, `20261025094036_1.jpg`, `20261025094045_1.jpg`, `20261025094052_1.jpg`, `20261025094056_1.jpg`, `20261025094115_1.jpg`.

**Intake and evidence handling:** Locate the supplied original ZIP using the session attachment or established user-provided local evidence location; do not infer a Windows pathname from this brief. Hash the ZIP and all extracted images; preserve originals and immutable per-image identity locally under an ignored evidence path. Do not commit the ZIP, image payloads or derivative annotated image bytes without a separate rights/publication decision. Record a tracked, authored evidence index with original filenames, hash references, observed outpost label, selected extractor/resource, actual visible deposit where supported, any placement error, ambiguity and an evidence qualifier. Maintain a robust link between screenshot and saved Workshop identity; a displayed name alone is not proof of a unique native handle. If originals are inaccessible to Codex, explicitly state the access blocker and preserve the intended mapping rather than inventing observations.

**Permitted conclusions:** A displayed extractor item provides catalogue membership at the observed moment; a highlighted area is gameplay evidence of an apparent region; neither proves native path count, exact coordinates, selection mask or successful construction. A contiguous highlighted patch can be the union of several paths. An existing extractor is historical positive evidence only, not an exhaustive resource inventory or guaranteed current vein state. An error caused by overlap, foundation height or boundary placement is not automatically a resource-absence finding. Screenshots are held-out **comparison evidence**; do not use their visible resources to choose source masks, component ordering, RSGDs or chance settings. Preserve D2/D3 frozen comparisons and record when these screenshots were already known to the implementer; do not call this exercise fully blinded to their contents.

## 3. Required work — Track A: first construction-query resource masks

1. Enumerate **all currently unresolved nonuniform-mask source/case associations**, including the four affected Feynman outposts, using D2/D3 case IDs and qualified Save52 Workshop/site joins. Do not limit the investigation to the three photographed sites and do not count the previously mistaken Feynman V deletion claim as fact. Build a per-case matrix of currently known source, component, spatial and mask operands, with evidence basis and precise unknowns.
2. Trace native source-construction initiation, query-coordinate preparation, frame transforms, surface/raster mask lookup and subsequent generator admission. Establish exact field/offset domains, integer/floating arithmetic and operation order: geographic coordinates, source local anchor, construction query, source-map/mask lookup, selected ordinary low-nibble mask and later per-cell evaluation are **distinct domains**. Pin disassembly/decompiler claims to source exports and instructions, not a post-hoc geometric fit.
3. Reconstruct the actual first query from installed data and saved geographic inputs **where supported**. Preserve intermediate query values and the final sampled mask. Show why any mask is selected, including cases where neighbouring cells have different masks. Test synthetic opposite-mask/boundary examples so that accidentally sampling the outpost beacon or a later cell cannot pass.
4. Implement a **general** correction to corpus builder/predictor only if the native source and derivation are established. Do not insert case-specific masks, guess the first query to recover known resources or broaden support by treating the whole source as uniform. When a runtime-only operand remains, classify that source as indeterminate and specify the exact native observation required.

## 4. Required work — Track B: component and descriptor precedence

Investigate the two outstanding Feynman III Uranium/Vanadium associations. Existing D3 candidates include BIOM `0x0008ae7b` / RSGD `0x000083ea` and BIOM `0x00095092` / RSGD `0x000083dd`; reverify their role and identifier domains from the current research. Trace actual component population/order, first-success and failed-prerequisite paths, alternate-descriptor handling, owner-root maps, and effective per-biome data. D4E's component slot and owner-root mechanisms may help, but must not be presumed to settle descriptor precedence.

Implement a native-supported deterministic rule if recoverable from installed records. Preserve visited candidate order and explicit reasons for rejection, bypass, selection or unresolved choice. No choosing an RSGD because the saved outpost name says `V U` or because a screenshot depicts the associated extractor. If an effective runtime component selection cannot be determined offline, specify the smallest missing operand, its upstream producer, and a qualified capture contract.

## 5. Prediction freeze, generalization and geometric controls

1. Preserve immutable original RG2-D1/D2/D3/D4E predictions, validation ledgers, installed corpus hashes and historic conclusions. Produce **versioned new predictions** and machine-readable per-case inputs before opening the held-out extractor/screenshot comparison in the dedicated comparison step. Clearly disclose the limits of blindness given the already-known issues.
2. If selection input changes, derive all ordinary resource paths with the **unchanged qualified geometry algorithm**, preserving native resource order, inactive settings, owner-root/slot semantics and competing-path geometry. Extend minimal corpus only by independently justified source fields and report precise canonical uncompressed byte delta; do not optimize performance or compression in this task.
3. Verify all **ten exact native-region controls**: four Feynman V, three Carinae III-a, three Archimedes III. Check exact identity, ordered binary32 XYZ/widths and native bounds. Reassess the complete recognized Save52 cohort, distinguishing saved-active, disabled and membership-unknown cases, supported/full versus partial predictions, positives, additional unverified resources, potential false negatives, and indeterminate pairs.
4. For **all nine D4E indeterminate resource associations**, provide before/after classification, underlying mechanism, independent evidence and consequence. Report counts and case identities; no unsupported accuracy percentage based on installed extractors as complete ground truth. Compare observed gameplay screenshots only **after** candidate selection/prediction is frozen. Preserve first-party observations and any conflict with the saved associations without rewriting earlier evidence.
5. Preserve the boundaries among ordinary finite veins, Special resources, terrestrial biome Water and ATMO-derived atmospheric resources. Do not mistake the presence of extractor types for discrete vein polygons or two Water mechanisms for two generated Water deposits.

## 6. Constructive offline-first escalation

If either track remains unresolved, Codex must not finish with a generic `UNKNOWN`. Identify the *earliest* not-reconstructible native value or branch and demonstrate why current installed/static/captured evidence cannot settle it. Prefer a small reusable extension to the already qualified D4 selection/context collector, with synthetic qualification if implementation is needed, and provide a **completed, reviewable live run card** only where a natural observation can discriminate the remaining hypotheses. Define identity joins to the correct Workshop/source, non-hit or cache-hit treatment, scientifically meaningful stopping predicates and realistic fallbacks. Do not accept an unrelated body-owned event as scientific success.

This brief **does not authorize** launch, attachment, forced regeneration, new game saves, changing Starfield files, publication, repository integration into the Outpost Tracker, or automatic attempts. A future live run requires separate explicit maintainer approval after inspection of its finalized card. All protected manual/research/quicksaves and historical backups remain subject to hash-based pre/postflight checks; ordinary autosave/exitsave churn is diagnostic-only under the current policy.

## 7. Frozen acceptance criteria — AC1–AC8

**AC1 — Authority and preservation.** All existing saves, protected backups, native captures, installed definitions, historical frozen predictions, and Git HEAD/index unchanged. Screenshot originals securely retained as local first-party evidence; no unauthorized live action or staged/committed work.

**AC2 — Construction-mask lineage.** Derive the first source-construction query and native resource mask for nonuniform cases using established operands and transformations where possible. Show intermediate values and distinguish construction-query from subsequent resource-cell masks. Unresolved values receive a precise source-backed dependency and acquisition path.

**AC3 — Component precedence.** Determine Feynman III's effective component/descriptor traversal or localize the exact missing native decision. Preserve native ordering, alternate/failed paths and separation of root-map construction from descriptor selection.

**AC4 — General native-supported implementation.** Any predictor/builder changes implement general rules with evidence, no Feynman-specific fitting; preserve published algorithm and corpus specification fidelity and quantify additional portable bytes.

**AC5 — Full Save52 regression.** Reassess entire qualified Save52 outpost population and all nine prior indeterminate pairs, preserving original frozen results and all ten native geometry controls. Report coverage, corroborated positives, potential false negatives and indeterminate status separately.

**AC6 — Independent gameplay evidence and scientific discrimination.** Properly intake all 24 supplied screenshots with hashed provenance and qualified per-image observations; use only as validation controls, not generation inputs. Resolve or materially narrow both tracks, with specific runnable acquisition proposals when necessary. Mere screenshot/catalogue repetition is insufficient.

**AC7 — Durable records and editorial finalization.** Deliver traceable native source/operand ledgers, per-case input/output tables, script/test receipts, changed corpus cost, failures and uncertainty, with mandatory automated screening and manual reading of **all changed prose** per `docs/EDITORIAL_STANDARD.md`. Avoid run-together words/numbers, garbled Unicode and ambiguous hexadecimal offsets/identity notation; no redundant decimal annotations.

**AC8 — Independent review and exact package.** Independent reviewer challenges all criteria, reads primary evidence/code and test failures, checks screenshot interpretation and prediction/validation separation, regression and rights limits; returns `ACCEPT`, `REWORK` or `ESCALATE` with justified scientific and editorial dispositions. Verify final complete and task-only patches, exact changed/untracked/ignored/excluded inventory, hashes, forward/reverse reconstruction and unmodified Git index/HEAD. Any final post-review edit requires independent delta acceptance.

An implementer test PASS is not a scientific acceptance certificate. Preserve valid partial results even if a missing runtime operand requires ESCALATE; do not overclaim closure of all nine associations.

## 8. Expected delivery and stopping boundary

Provide a concise direct research report, complete source/mask derivation trace, Feynman III component-order analysis, held-out screenshot evidence index, original versus revised nine-pair disposition matrix, Save52-wide results, exact geometry regression evidence, minimal corpus field/byte report, versioned algorithm/specification updates where justified, and independently reviewed completion matrix.

Include exact commands and input identities for reproducibility. Raw game-derived datasets, images, native dumps and original save files remain ignored and local-only, with first-party source hashes and authored interpretation tracked as permitted. Track reference research code, tests and specifications as usual, subject to publication review. **No Starfield live action, Git staging/commit/push or B6 release work.** Return an exact review package and suggested commit message for maintainer review.
