# RG2-D5R — Resource-Construction Query Scheduling, Selection and Determinism

**Project:** `starfield-outpost-research` (`D:\Projects\starfield-outpost-research\`)  
**Assignment:** Bounded offline research into request scheduling, query selection, effective input determinism and within-invocation source lifetime; conditional, read-only save investigation only if an indispensable input is not derivable from executable/static game data.  
**Status:** Implementation/research brief; freeze D5R-AC1–AC9 before starting.  
**D5P observer:** Unchanged; retail engineering **NO-GO**. **B6/publication:** ON HOLD.

## 1. Purpose and changed research emphasis

**Primary question:** For a specified outpost location and the pinned game's static procedural data, can we determine the construction queries that Starfield will issue, identify the query (or equivalent inputs) that determines the generated resource population, and reproduce that population without requiring a historical live trace?

D5Q mapped the provider, spatial-cell contributor selection, coordinate conversion, low-nibble rarity control, geometry-generation path and the source-pointer-keyed retained map. The remaining priority is **how the game schedules requests, chooses effective queries and makes results stable**, not proving the historical identity of a specific cached allocation. Do not reintroduce a requirement to witness full construction–retention–later-hit continuity.

Investigate whether stability follows from deterministic query generation and ordering, canonicalized or equivalent query inputs, serialization or persisted state, synchronization/arbitration, order-independent generation, or some other supported mechanism. **Do not assume that results are invariant or that a unique winning query exists.** D5H/D5I established variable sampled values (including 0/3 for the second Feynman V source). Explicitly seek counterexamples and conditions under which normal execution could produce different outcomes.

The deliverable is an **evidence-linked behavioural model and, where justified, a bounded reproducible offline evaluator** of query derivation/selection. It need not recreate Bethesda's C++ types or names, nor generate a full planet resource map. A precise negative finding or missing-input contract is valid; do not substitute a presumed deterministic rule.

## 2. Research baseline and fixed references

Read the current repository `AGENTS.md`, `WORKFLOW.md`, `docs/RESEARCH_EXECUTION_PROTOCOL.md`, `docs/EVIDENCE_STANDARD.md`, `docs/SAVE_PROTECTION.md`, `docs/EDITORIAL_STANDARD.md` and active research/navigation records. In particular, inspect D5D's request dependencies and scheduling gates, D5G–D5I's query variability/reachability and geometry controls, D5P/R1–R3's instrumentation findings, and **D5Q's** `docs/experiments/resource-retained-population/d5q-call-dataflow-map.md`, report and source ledger. Recheck original evidence and competing interpretations where material. The D5P capture failures are not evidence against deterministic scheduling.

Verify pinned binary identities before relying on addresses: **Starfield 1.16.244.0**, `Starfield.exe` SHA-256 `7e9adb1414a8e1b325e5e1f097b9b17b78deb7eebeda37a333351a43a60f9d28`. Verify installed ESM/PlanetData and Ghidra state against durable local records. Addresses here are preferred static VAs at image base `0x140000000`, not runtime addresses. Work in existing Ghidra state **read-only** (prefer established `-readOnly -noanalysis` export flow); no destructive reanalysis or database rewrite. Stop and report an identity mismatch rather than silently porting addresses.

Relevant D5Q anchors (verify, do not presume complete):

| Boundary | Static VA | Established role or open question |
|---|---|---|
| Coordinate dependency request | `0x1403625e0` | Receives cell/rectangular dependency demand; upstream initiating conditions remain bounded |
| Rectangular request | `0x1407a1580` | Cell min/max, owner/discriminator, dependency gates |
| Layer worker | `0x1407b5160` | Provider call `0x1407b526a`, neighbor preparation beforehand |
| Density-level builder | `0x1407a1940` | Provider call `0x1407a1a3c`, aggregate-reuse skip |
| Source provider | `0x14079f860` | RCX=ProcGen, RDX=original Int2 pointer, R8=aggregate holder |
| Cell selection | `0x140985870`; `0x14079fa90..0x14079fa93` | Spatial lookup then current source selection from cell contributors |
| Geographic conversion / sampling | `0x14078d660`; `0x142339340` | Query-dependent converted coordinates, low-nibble sample |
| Source map and construction | D5Q Q07–Q15 | Visit guard, hit/miss and generation; cache is a boundary condition, not active continuity target |

**Terminology:** Source object = native geographically defined resource contributor, not an extractor or individual deposit. Sampled ordinary “mask” = raster byte low nibble, used numerically in rarity selection; do **not** interpret bits as individual resource membership. Distinguish source identity, geographic descriptors, original query, converted geographic coordinates, sampled nibble, effective resource definitions and generated geometry.

## 3. Required backward trace: from provider to request initiation

Follow the two known provider callers backwards through worker dispatch, dependencies, neighbour preparation, rectangular/cell requests and the closest defensible gameplay or location-derived initiating boundaries. For each branch determine:

1. **Exact request creation:** The data from which original Int2 query coordinates are computed; region/rectangle bounds; indexing, strides, rounding, cell/chart transformations, level/layer and any offsets. Distinguish mathematically derived inputs from state-derived inputs.
2. **Candidate enumeration:** Which cells/coordinates can produce a provider invocation for a specified location/source; order of construction or iteration; deduplication, queue insertion and task/result dependencies; triggers and early exits.
3. **Scheduling and arbitration:** Work queue ordering, dispatch, thread workers, locks, result reuse, dependency completion, pending/visited guards and source-map insertion. Identify whether “first” means first enqueued, started, map miss, successfully sampled, successfully copied region or first retained populated result; do not collapse those milestones.
4. **Competitors:** Whether two different original Int2 requests may target the same source, with different converted geographic samples, and whether their ordering or first-writer behaviour can influence geometry. Explicitly examine simultaneous requests, neighbour work, canceled/restarted requests and initialization/reset boundaries where relevant.
5. **Boundaries:** If global scheduling cannot be uniquely resolved statically, isolate the smallest unresolved operation or state, the exact evidence needed, and the consequences for determinism. Do not claim the first historical Save52 invocation was observed.

For every consequential call/field, record static VA/RVA, call site, register/stack argument locations or field offset, width, producer, consumer, control predicates, side effects and precise evidence provenance. Treat work queues, task state, thread-local state and manager fields as **implicit** inputs when applicable. The objective is a comprehensible execution/data-flow model, not a purported Bethesda declaration.

## 4. Determinism analysis and discriminating controls

Build an explicit dependency and variability matrix classifying every effective input as: **static game data**, **derived from location**, **runtime but reproducible**, **runtime order-/state-dependent**, **save-persisted (verified)**, or **unresolved**. Include the earliest known stage, causal consumers and whether its value can affect selected source, ordinary sampled nibble, resource weights or geometry. Validate the actual raster/descriptor and component ordering assumptions inherited from D5Q and earlier native controls.

Evaluate competing mechanisms, with evidence both for and against:

- Deterministic request coordinates and dispatch order.
- Distinct but equivalent or canonicalized requests.
- Requests that sample different nibble values yet produce equivalent **effective output** because rarity/resource definitions make the difference immaterial.
- Synchronization or winner-selection rules that make a specific request authoritative.
- First-writer/race-sensitive outcomes or other non-invariant behavior.
- Persisted input/state that selects one result on loading.

Do not infer invariant geometry from invariant sampled nibble, or the converse. Analyse resource eligibility, successful geometry and complete population separately. Where representative offline execution is practical, construct **focused comparisons** from independently chosen input cases (including known D5H/D5I mask 0/3 conditions and the second Feynman V source `0:37536:20928:0029d20e`). Test alternate valid request orders, interleavings **as models only unless native ordering semantics are proven**, and boundaries that could falsify invariance. Preserve negative or contradictory results; never choose query coordinates retrospectively because they match saved geometry.

If formal ordering cannot be established, provide a bounded set of permissible query candidates and outcomes, with a clear statement about whether the available inputs uniquely select one. A deterministic enumeration of possibilities is not proof of deterministic engine scheduling. Avoid reconstructing an entire geometry simulator unless essential to distinguish documented alternatives; reuse qualified native/fixture algorithms and earlier controls.

## 5. Within-invocation source lifetime — proportionate offline check

Investigate only the lifetime and synchronization necessary to conclude that a native source selected by a cell contributor remains the **same valid object during its current provider/generator invocation**. Examine Grid reference retention, contributor-cell ownership, allocation/acquire, Grid clear, standalone retirement, ProcGen reset/destruction, lock ordering and possible concurrent mutation/writers. Identify relevant guarded intervals and whether retirement can overlap the provider's use of a raw source pointer.

Separate **proved non-overlap under an identified lock/owner contract**, **inferred intended engine safety**, and **unresolved interference**. A source address being reused in some later session does not by itself threaten one properly guarded invocation. Do not undertake exhaustive allocator-ABA or later cache-hit provenance testing. If static analysis shows an unprotected window, document precise conditions and consequences rather than inventing a live hazard. No native locks/functions may be called in the live game under this brief.

## 6. Conditional save-file investigation — evidence-triggered, not automatic

**First exhaust the executable, static game data and reproducibly derived location inputs.** Save inspection is permitted **only after** the dependency matrix identifies a **specific indispensable input/state** for query derivation, selection or determinism that cannot be located in those sources, and documents the search undertaken and why serialized state is a plausible origin. Do not investigate save serialization merely to find geometry or historical cache contents.

For each triggered input, perform a focused, **read-only** check of existing save research, schemas and approved local copies (including Save52 if permitted by repository protection rules). Determine whether the input is serialized, derivable from saved outpost location/identity, regenerated on load, or unresolved. Distinguish a field's presence from proof that it drives query selection. Never modify, resave, load in Starfield, convert in place, replace or upload protected saves. If required material is inaccessible or format cannot be decoded safely, record a specific gap and follow-up proposal instead of broad speculative save archaeology. No full-save reverse-engineering programme or invented requirement to prove a saved geometry cache.

## 7. Method, evidence, verification and scope limits

Use read-only static analysis and task-owned offline scripts/fixtures; rely on existing qualified native tests where possible. Any executable test must be an isolated/disposable process, not a Starfield/SFSE session. Prioritize cross-checking the two independent provider caller routes, coordinate/value definitions at producer and consumer, ordering/synchronization edges and boundary cases. Revalidate changed interpretations against D5Q Q01–Q19, D5D and D5I. Record source binary hash, original native instruction windows, Ghidra/export receipts and necessary test identities. Keep proprietary bulk disassembly and raw saved data local-only under ignored scratch; tracked documents contain only short defensible evidence references.

Use confidence labels **ESTABLISHED (static)**, **ESTABLISHED (executed)** with its actual fixture or historical evidence envelope, **INFERRED**, and **UNRESOLVED**. A proven native branch is not an observed Save52 historical event. State separately: (a) determinism of *candidate query generation*, (b) dispatch/winner determinism, (c) mask/eligibility determinism for a specified query, and (d) output-equivalence or invariance across admissible queries. A claim of reproducibility must name all required inputs and the tested scope, with a falsifier or qualification boundary. Independent technical/scientific and editorial reviews must inspect evidence strength and unresolved alternatives; don't allow a superficially complete diagram to replace discriminating proofs.

**Excluded:** Full cache-hit/retained-population continuity or historical first-cache-writer tracing; further D5P SFSE repair; any retail launch, debugger attach, plugin installation or Vortex operation; live regeneration, save mutation, unrelated outpost systems; broad save archaeology or release/publication work. If cache lookup/miss affects request scheduling, record its *control-flow role* only, without making cache correctness a target.

## 8. Deliverables and completion outcomes

Use established project conventions, minimizing redundant artifacts:

- `docs/experiments/resource-retained-population/d5r-query-scheduling-map.md` — navigable initiating-call graph, request/coordinate derivations, candidate enumeration, dispatch/winner ordering, lifetime guards, and source/claim evidence labels.
- `docs/experiments/resource-retained-population/d5r-determinism-matrix.csv` — input origins, derived values, dependency edges, stable versus variable classifications, impact on sampled value/output, and missing-input trigger for save inspection.
- `docs/experiments/resource-retained-population/d5r-report.md` — methodology, bounded findings, counterexamples, conclusions on deterministic query/geometry reproduction, residual uncertainty and precise next discriminator. State whether save investigation was triggered, and why.
- `docs/experiments/resource-retained-population/d5r-sources.csv` — auditable claim-to-evidence provenance and static/fixture distinctions; `d5r-review.md` — frozen acceptance criteria and independent technical/scientific and editorial decisions.
- Optional compact task-owned derivation/verification scripts, test receipts and focused read-only save findings if triggered; source/binary provenance and reproduction commands. Focused updates to durable research navigation only where justified.
- Final exact-hash manifest, complete and task-only diffs, HEAD/index/status, preservation/exclusion statement. **Do not stage, commit or push.** No retail package/run card.

**Permissible conclusions:** (A) Inputs and scheduling proven sufficient for a reproducible offline calculation within bounded conditions; (B) candidate set or effective outputs equivalent despite unknown ordering; (C) material order dependence or non-invariance established under qualified conditions; or (D) a specific unresolved input, scheduler guarantee or state boundary prevents a conclusive result. Do not turn D into A by assumption or claim that C necessarily occurs in ordinary retail operation based only on a constructed interleaving.

## 9. Frozen acceptance criteria

| ID | Required outcome |
|---|---|
| **D5R-AC1 — Authority/provenance** | Verify repository/executable/data/Ghidra pins and protection; no live game, observer, Vortex, protected save changes or publication activity; explicit scope and exclusions. |
| **D5R-AC2 — Upstream query map** | Trace both provider caller routes, request/dependency/worker producers, relevant initiation and coordinate origins with exact ABI/control-flow evidence; honestly bound unmapped upstream edges. |
| **D5R-AC3 — Candidate generation and winner selection** | Identify candidate query enumeration, ordering, barriers, deduplication, misses/skips and competing requests; distinguish first scheduled, first miss, first completed copy and first retained output; qualify rather than assume any winner rule. |
| **D5R-AC4 — Effective inputs and mask/output effects** | Trace query coordinates, descriptor/BIOM, sampled ordinary nibble, ordered resource definitions and geometry dependencies; matrix classifies static, derived, runtime, persisted and unresolved inputs without bitmask misinterpretation. |
| **D5R-AC5 — Determinism discrimination** | Test or rigorously reason through competing stable/variable mechanisms, alternative query orders and known mask 0/3 cases; provide falsifiers/counterexamples and a bounded verdict on reproducibility, not mere plausible invariance. |
| **D5R-AC6 — Source lifetime** | Examine within-invocation selected-source ownership and synchronization against retirement/clear; classify protected and unresolved intervals; no requirement to prove later cache-hit identity. |
| **D5R-AC7 — Conditional save discipline** | Save examination only for an identified indispensable unavailable input after static-data search; if triggered, read-only focused results with protection and causal caveats; otherwise explicit not-triggered justification. |
| **D5R-AC8 — Verification and durable outputs** | Traceable graph and dependency matrix, precise provenance, focused controls and counterexamples, truthful report and compact necessary scripts/receipts; preserve historical evidence and local-only proprietary material. |
| **D5R-AC9 — Independent delivery** | Separate technical/scientific and editorial reviews, correction of substantive defects, frozen source and diff hashes, complete/task-only patch verification and unchanged HEAD/index. No automatic follow-on authority. |

## 10. Operational protections and handoff

All research is offline/read-only with respect to Starfield, saves, Ghidra database and prior accepted primary evidence. Do not launch `Starfield.exe`, `sfse_loader.exe` or Steam; do not attach a debugger to the game; do not alter/enable/deploy any plugin; do not load/resave games, alter Vortex, or initiate an observational retail trial. Offline tests may alter disposable copies only. Retain established C: and D: free-space floors of **40,000,000,000 bytes** where meaningful local acquisitions occur. Protect original saves and backups using current `SAVE_PROTECTION.md` policy; don't imply a full audit was performed if it was not. Preserve accepted evidence; disposable task-owned ignored scratch can be cleaned per workflow.

The next engineering decision, if any, must follow the actual D5R findings. **D5P retail remains NO-GO; B6 remains on hold.** The brief is authorization for bounded research, not for an implementation of a new observer or a live experiment.
