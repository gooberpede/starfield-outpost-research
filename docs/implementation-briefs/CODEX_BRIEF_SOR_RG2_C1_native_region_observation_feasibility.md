# Codex research brief — RG2-C1: Coherent native resource-region observation feasibility and capture design

**Project:** `D:\Projects\starfield-outpost-research`  
**Task type:** Bounded **offline-only** native-evidence reconnaissance, acquisition-feasibility assessment, experimental design and durable documentation.  
**Status:** New assignment; **does not authorize RG2-C2 live capture**. B6 publication verification remains on hold.  
**Research baseline:** Starfield `1.16.244.0`, preserving exact installed-source and save provenance.  
**Deliverable:** An independently reviewed, executable-in-principle **capture contract and prospective operator run cards** that can discriminate why frozen resource geometry differs from observed mature-outpost evidence, and whether unstable inputs/lifecycle can account for unexpected changes.

## 1. Scientific question and boundaries

RG1 reconstructed an offline, qualified inorganic vein-path generator; RG2-A, RG2-A1 and RG2-A1-F1 established frozen predictions and real contradictions at active mature outposts. In Save52, **Feynman V Cu Co Ni IL** contains a supported Ionic Liquids extractor/visible region where the conditional evaluator predicts absence; **Carinae III-a Rc Fe** contains saved Iron extraction/visible patches where the conditional model also predicts absence. The Feynman Copper singleton disk contains the saved extractor and provides a **positive control**, without yet establishing native/current geometric equivalence.

**Fourth diagnostic case:** **Feynman VIII-b Au Sb**, previously investigated in D1 for the user's report that a Gold or Antimony deposit appeared to be replaced by Copper. D1 establishes an exact site join between Save51/HIST-0266 and Save52/HIST-0267, with unchanged saved beacon/site position; it **does not prove the substitution event**, its timing or a changed resource region. Copper, Gold and Antimony extractor representations were already present in Save51. Treat it as a **potential input/cache/lifecycle-instability diagnostic**, not as a bug-reproduction target or a confirmed incident. No mandatory requirement to trigger or identify the bug's root cause.

**Central question:** What minimal trustworthy observation of the **same actual game evaluation** binds (a) outpost/extractor and coordinate frame, (b) source/owner/biome/resource-selection inputs and effective RNG/settings, (c) generated and **consumed** resource regions/cache epoch and (d) native availability/admission outcome, such that exact offline replay can determine the **first material disagreement**?

The diagnostic hypotheses to distinguish are:

- **Different effective inputs or source selection:** offline model was supplied a wrong owner/key, region source, frame, BIOM/RSGD, weight, setting, or prior-state operand.
- **Same inputs, different generated paths:** generator/PRNG/competition reconstruction is wrong or input/order was omitted.
- **Same generated paths, different consumed population or epoch:** stale, replaced, partially built, rebased or differently selected cache/region state.
- **Same consumed regions, different classification/admission:** spatial consumer, extractor footprint, special resource properties or native predicate differs.

The possibility of **runtime-dependent instability** must be considered concretely: inspect which mutable inputs, caches, seeds, ordering, readiness or lifecycle events could change outcomes between otherwise comparable evaluations. **Do not assume the native machinery is bug-free, but do not presume a bug exists.** A coherent stable result is useful evidence. No speculative expansion into generalized bug hunting, arbitrary travel loops or an indefinite attempt to reproduce the historic incident.

## 2. Required existing inputs and authority

Read and reuse before new reconnaissance:

1. RG1: `docs/experiments/resource-geometry/` (native mechanism, evaluator, point/region geometry, tests, reviewer counterexamples and source pins).
2. RG2-A: `docs/experiments/resource-geometry-live-prep/` (frozen Kreet v1 controls, save/Workshop identities, observation limitations, run cards).
3. RG2-A1/F1: `docs/experiments/resource-geometry-mature-context/` (planetary seed/owner provenance, conditional mature v1/v2 predictions, eleven Save52 screenshots, seven saved extractor joins, Copper, Water, and unresolved IL/Iron comparisons).
4. D1: `docs/experiments/disappearing-deposits/` (`report.md`, `native.md`, `hypotheses.md`, `saves.csv`, `sites.csv`, `extractors.csv`, reviews). Preserve source-reported versus observed state.
5. Earlier resource-availability/provider/region-lifecycle and NO-GO observer/disposition reports, including resource-region owner/cache, `source +0x68` visited state, selected source index, synchronous on-miss producer and separately consumed area/raster products.
6. Relevant WORKFLOW, PERMISSIONS, EVIDENCE_STANDARD, RESEARCH_EXECUTION_PROTOCOL, publication and third-party rules; B3 historical source/version pins. Use an existing pinned executable/source record. Prior accepted conclusions are not automatically promoted to current live equivalence.

**Allowed:** Read-only inspection of tracked project records, project-owned private historical receipts, installed *locally held* definitions and disassembly already covered by project permissions; narrowly scoped additional offline static analysis where essential; original documentation and minimal **synthetic** contract/checking code using nonproprietary inputs; qualified identity/hash checks; independent reviewer and diff packaging. Keep installed Ghidra/database/tool/game files outside the repository and unchanged. If consulting external prior art or sibling `starfield-resource-research`, apply source-specific permission/provenance/attribution gates before incorporation; do not treat external claims as measured project validation.

**Prohibited:** Starfield or Creation Kit launch/load, live process attachment, debugger execution, SFSE build/deploy/use, memory modification, target code execution, console gameplay, new game saves, original save mutation, proprietary/raw native dump promotion, third-party evidence disclosure, changes to installed game/tool files, unauthorized source changes, staging/committing/pushing, uploading or publication. **Earlier observer NO-GO remains binding**. This brief authorizes no revival or operational trial of that observer.

A historical receipt check must be **short and exact-match-led**: look for the required same-case identity/source/frame/region/epoch operands in named existing receipts. State inspected families and exact missing fields; stop once absence of a coherent full record is established. Do not reopen a broad archive search to avoid designing the acquisition.

## 3. Capture design: minimal coherent observation

Trace and propose the most appropriate **naturally executing consumer** and, only where needed, its upstream generator. Prefer observation of the actual region/query or extractor-admission consumer over capturing every region-construction operation merely because it is earlier in the pipeline. Provide stable semantic names, pinned baseline function locators, callsites, expected argument/result types, runtime ownership/lifetime, and dataflow for:

- **Identity:** source save hash/display identity; active Workshop and beacon relationship; named extractor's saved and runtime reference IDs, base form and effective properties. Do not substitute a same-planet or same-name object. Identify actor/world/cell/workshop epochs when actually available.
- **Position:** beacon and extractor XY/Z, parent frame/source translation, chart, generator-local coordinates, query point versus extractor footprint, nominal 150-unit boundary and any actual admission radius/upper scalar. State rounding and coordinate-domain transformations.
- **Generation context:** selected source / SFBK / SFPT / BIOM / RSGD / IRES; manager owner key/suffix; packed cell key; per-biome chance/weights, effective atmosphere and family selection, installed defaults versus overrides, PRNG seed/consumption order and prior different-resource competition if required.
- **Geometry:** complete relevant ordered XYZ/width paths (including paths originating outside the footprint), generated bounded disks/rectangles and availability strips where consumed, resource identity, valid source/window boundaries, winning or rejected region state. Distinguish a region collection from scanner raster or UI summary.
- **Lifecycle:** source/cache pointer plus durable identity, creation/selection/invalidation/eviction or reuse state, source generation/region population epoch, visited/queued/work state, readiness and load/return order. Address pointer reuse; pointers alone are not stable identities across loads.
- **Result:** the actual game-side resource or availability decision and the **specific collection and epoch consumed**; extractor-specific admission branch (ordinary vein, biome/skip-vein, atmosphere or bypass) as relevant, plus a negative or rejected classification if available.

Define an **atomic/coherent capture criterion**: fields must refer to one logical evaluation or be bound by stable identities and source/epoch values that demonstrate equivalence; a sequential grab across mutating frames is not sufficient. Explain how to detect incoherence, dropped records, unloaded references, stale region pointers, reentrant/multithreaded producers, and observer interference. Acquire only the smallest necessary data slice, not memory dumps of the whole ProcGen manager. Give the expected maximum captured scope/size from bounded structures, or state what must be measured before live approval.

State whether the chosen observation can be obtained at **consumption of existing cached geometry**. If upstream generation is indispensable, specify exactly which missing producer operands require a second point of observation and how the two observations are correlated without guessing that they belong to the same cache epoch.

## 4. Cases and discriminators

Prepare four **separate named scientific cases**, with associated read-only save identity and exact existing witness links:

| Case | Role | Specific discriminator |
|---|---|---|
| Feynman V Cu Co Ni IL — Ionic Liquids | Primary contradiction | Saved IL extractor/visible region vs frozen conditional absence |
| Carinae III-a Rc Fe — Iron | Independent contradiction | Saved Iron extractor/visible regions vs frozen conditional absence |
| Feynman V Cu Co Ni IL — Copper | Positive/geometry control | Predicted singleton disk contains saved Copper extractor; circular appearance remains observational clue, not exact polygon match |
| Feynman VIII-b Au Sb — Gold/Antimony/Copper | Optional lifecycle/instability diagnostic | Compare effective generation and consumed-source inputs across controlled evaluations; historical substitution remains unverified |

If Feynman VIII-b introduces too much live acquisition complexity, provide a **self-contained optional stability card** rather than silently expanding mandatory IL/Iron acquisition. Design the comparison so **same inputs/same consumed epoch**, **different inputs**, **different cache selection**, **partial readiness** and **different extractor/UI result** are separable outcomes. The test does **not** require repeated visits until a rare change occurs.

Keep existing frozen Kreet predictions and mature v1/v2 files byte-identical. Specify a pre-observation freeze and a replay algorithm: compare actual captured generation operands with frozen inputs, replay with the accepted RG1 evaluator **without fitting**, compare complete region/path identity and numeric tolerances, then compare the exact consumed region decision. Preserve discrepancies and counterexamples; any corrected evaluator/prediction must be new, separately versioned and tested against held-out IL, Iron, Copper and relevant Kreet controls.

A capture of only the displayed resource list, a screenshot, a guessed generator owner from PNDT or an unbound source pointer **does not pass** the native-spatial validation requirement. Likewise, the existence of saved extractors does not certify current live vein geometry. Clearly identify manual scanner/placement fallback evidence and what it can and cannot falsify.

## 5. Acquisition feasibility and safety assessment

Evaluate concrete acquisition architectures with an information-gain versus interference/risk comparison, including at least:

- Observation of already consumed native region/query state using minimally invasive read-only capture.
- Bounded event-associated record capture if a trustworthy low-interference route exists.
- Manual scanner/extractor-placement observation as a lower-resolution fallback.
- Reasons prior debugger/observer designs are unsuitable under their recorded NO-GO outcomes.

**Do not implement a live observer in C1.** A native observer, injection, live attachment or instrumentation needs a separately reviewed engineering contract and explicit maintainer approval. If no safe acquisition route can be specified with existing evidence, return a narrow evidenced blocker, feasible alternatives tested, minimal missing qualification and a proposed separate next step; do not claim a live run is ready.

For the proposed RG2-C2 cards specify version/hash and identity preflight, selected Save52 load-menu identification, outpost/actor positive verification, exact trigger/event, minimal collected fields, expected control outcomes, preservation/rollback and STOP actions, worker/target integrity safeguards, no save writes, both-drive disk guards where applicable, teardown and output manifests, coherent-epoch verification, numeric comparison policy and review gates. Do not invent available runtime tools or authorization. No irreversible or private-source exposure.

## 6. Durable deliverables

Place bounded authored material under an appropriate `docs/experiments/` continuation directory, cross-linking—not rewriting—the established research history:

1. **Answer-first report:** Preferred capture point, concrete reason, unresolved feasibility, scientific tests and exact next authorization step.
2. **Native/consumer and producer contract:** Pinned function/address/domain locators, owner/epoch and dataflow, minimal schema with type/units/identity/time semantics.
3. **Stability/lifecycle assessment:** Actual mutable inputs and cache events that could produce unexpected outcomes; supported causal branches and stated unknowns. *Not* a bug-root-cause investigation.
4. **Case matrix and prospective operator cards:** IL/Iron/Copper, plus optional Au/Sb/Cu; frozen prediction references, controls, discriminators and identity checks.
5. **Exact archived-receipt availability check** and acquisition-method comparison with explicit NO-GO constraints.
6. **Independent review, receipt and package:** all acceptance statuses, scientific/engineering/authority outcome dimensions, source/evidence hashes, status and inclusion/exclusion inventory, verified complete and task-only diffs. No raw proprietary payloads in authored tracked deliverables.

Document a current research interpretation and separately list inherited STATIC findings, user-observed screenshots, inferred conditional predictions and still-unmeasured runtime behaviour. Keep changes proportionate and do not modify prior accepted reports merely to reflect a newer hypothesis; new notes and backlinks suffice.

## 7. Frozen completion contract — RG2-C1 (AC1–AC8)

**Task type:** Offline design/research feasibility; not live engineering qualification or geometry validation. All eight criteria are mandatory and frozen unless the maintainer explicitly approves amendment.

| Criterion | Observable acceptance / primary evidence |
|---|---|
| **AC1 — Identity, safety and authority** | Exact starting Git/installed/source/evidence identities and protected-input/hash receipts; read-only scope, NO-GO observer and no Git/publication mutation respected. |
| **AC2 — Existing evidence and provenance** | Bounded search of exact existing receipts, RG1/RG2/D1 dependencies and any relevant prior art with permission/attribution; no unsupported claim that a coherent receipt exists or is universally absent. |
| **AC3 — Native observation contract** | Identified actual producer/consumer call chain and all material fields/owners/types/frame conversions, with verified locators or explicit named gaps; distinguish generated from consumed geometry. |
| **AC4 — Coherence and lifecycle** | Same-evaluation or positively joined source/cache epoch contract; concrete mutable-input and lifecycle failure modes, with controls; no mandate to reproduce an intermittent bug. |
| **AC5 — Four-case discrimination** | IL and Iron disagreements, Copper positive control, optional Feynman VIII-b instability case, all positively identified; compare input/generator/cache/consumer failure branches without fitting. |
| **AC6 — Feasible, bounded acquisition and prospective cards** | Alternative capture methods evaluated against NO-GO/interference; actionable-in-principle run design, qualification gates, STOP/recovery and replay comparison; if unsupported, precise blocker and next test rather than invented readiness. |
| **AC7 — Durable technical clarity** | Answer-first report, minimal capture schema, cases/stability/receipt records, versioned frozen-prediction handling, clear provenance/limits, proper notation and links. |
| **AC8 — Critical review and exact delivery** | Independent reviewer of entire final snapshot using primary evidence; ACCEPT/REWORK/ESCALATE with per-criterion PASS/FAIL/NOT TESTED and retained failed attempts; exact complete/task-only forward/reverse patches, protected status and exclusions. |

**Negative-result closure:** A bounded, independently accepted conclusion that no *currently qualified* safe coherent capture path exists may complete the **C1 feasibility assessment** if it identifies actual explored paths, concrete missing evidence or safety controls, and a discriminating next engineering step. It **does not** count as runtime geometry validation or establish that observation is impossible. Merely listing hypothetical hazards or declaring an undefined capture method sufficient does not satisfy C1.

**Continuation authority:** Diagnose and correct in-scope evidence, schema, tests and review defects within authorized offline operations; no new brief for ordinary REWORK. Scientific claims must be evidence-bounded, not blocked by unsupported hypothetical alternatives. Preserve prior failed attempts and actual counterexamples. Reviewer acceptance is not user permission to run live.

**Exit/escalation:** Stop affected operations on source-identity/hash mismatch, protected-input change, insufficient disk/worker safeguards, required prohibited live operation, missing indispensable source authority or genuine session/resource exhaustion. Retain exact checkpoint and request the narrow missing approval; continue independent authorized tasks. Apply standing both-drive free-space and protected evidence rules where applicable; do not invent fixed time/output caps on healthy offline research.

**Independent reviewer:** Review original criteria, primary call/receipt/source pins, actual changed tree and complete/task-only package; challenge unsupported live-readiness, false owner/epoch joins, omitted cache/lifecycle alternatives, retrofitted predictions, permission defects and speculative bug claims. If reviewer edits, use a different reviewer for the changed snapshot. Return only after actual reviewer disposition and verified hashes/patches; no staging, commit or push.

## 8. Required final Codex response

Provide concise: scientific answer; chosen or blocked capture method; what existing evidence was reused; actual native identity/epoch contract; predicted discriminators for all cases; confidence and remaining missing inputs; test/check counts honestly categorized; reviewer decision and AC matrix; authored file list; complete/task-only patch paths and manifest; protected-input/HEAD/index status; next **separately authorized** action. **Do not claim RG2-B/C2 was executed.**
