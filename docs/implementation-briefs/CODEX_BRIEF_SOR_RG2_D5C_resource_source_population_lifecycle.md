# Codex research brief — RG2-D5C
## Resource-source population lifecycle and cache semantics

**Project:** `D:\Projects\starfield-outpost-research\` (`gooberpede/starfield-outpost-research`)  
**Authority:** Bounded **offline** native/static investigation, examination of previously acquired read-only evidence, and disposable synthetic tests only. **No launch or attachment to Starfield, live debugging, save loading in the game, mutation of saves/installed content, regeneration, publication, staging, commit, or push.**  
**Scientific disposition:** Do not assume that the source-keyed native collection is a cache. Determine its actual semantics, or precisely delimit what remains unknown.  
**Review:** Independent scientific/engineering and editorial assessment of the final evidence-backed snapshot; AC1–AC8 frozen.

## 1. Motivation and established observations

RG2-D5 and D5A isolated 13 sources whose ordinary resource masks vary across plausible source-construction queries. The initial construction query, not necessarily the beacon position or a later resource-cell query, determines the effective ordinary resource mask. D5A selected the active second Feynman V source **`0:37536:20928:0029d20e`**, mask alternatives **0** and **3**, as the strongest first discriminator; VI-b remains fallback, and the historical Feynman VIII-b resource substitution is deferred.

RG2-D5B Phase A built and synthetically qualified a combined construction/consumer observer. The subsequently approved Phase B retail observation positively bound the correct Feynman V Workshop, selected source, and consumed geometry. **Ionic Liquids, Fluorine and Copper each matched the independently frozen mask-3 geometry exactly and differed from mask 0**, using the native ordered binary32 region comparison. **No qualified source-construction query or sampled mask was captured.** D5B recorded 36 generation entries, 108 resource calls, 36 provider returns, three Workshop-bound accepted regions and one spatial transfer, but **zero qualified target-source construction chains**; instrumentation scheduling gaps prevent ruling out a missed construction. The evidence cannot establish historical mask selection or generation-to-consumption ancestry.

We have native indications of a source-keyed structure and retrievable region-bearing wrappers. This supports the *possibility* of retention/reuse; it is not proof that the structure is a persistent population cache, that the chosen source was cached when Save52 loaded, or that geometry is serialized. Avoid converting these hypotheses into premises.

**Main question:** What are the ownership, keying, construction, reuse, invalidation and save/load semantics of the *generated resource population* read by the outpost resource consumer? Specifically, what does this imply—and not imply—about D5B's consumer-only observation?

## 2. Source discipline, boundaries and operational safeguards

Before work, read the current repository versions of `AGENTS.md`, `WORKFLOW.md`, `docs/PERMISSIONS.md`, `docs/SAVE_PROTECTION.md`, `docs/RESEARCH_EXECUTION_PROTOCOL.md`, `docs/EVIDENCE_STANDARD.md`, `docs/EDITORIAL_STANDARD.md`, `docs/templates/completion-contract.md`, and `docs/reviewers/research-completion-reviewer.md`. Consult source registers, native contracts and the D2–D5B reports, especially:

- `docs/experiments/resource-combined-acquisition/report.md`, `phase-b.md`, `phase-b-review.md` and relevant source register;
- `docs/experiments/resource-construction-mask-selection/report.md` and the D5 source-selection evidence;
- native collection/source construction, owner/root traversal, save/Workshop and region-consumer investigations already indexed in `docs/RESEARCH_STATE.md` and `docs/SOURCES.md`.

Follow actual repository references when paths vary; do not manufacture a named function or data layout. Target pinned Starfield.exe version **1.16.244.0**, SHA-256 **`7e9adb1414a8e1b325e5e1f097b9b17b78deb7eebeda37a333351a43a60f9d28`**, and verify source hash/pins before relying on offsets. Distinguish static VA, RVA, runtime pointer, serialized FormID, source geographic key, descriptor, Workshop reference and save-local token. Annotate certainty for every native field, edge and inference. `FUN_` names are decompiler conveniences, not interfaces.

Protect all prior original captures, sealed D5B receipts, saves/backups, installed ESM, executable, screenshots, frozen D2–D5 alternatives and ten exact native geometry controls. No edits to the standalone predictor to impose a cache rule or guess mask 3; no reclassification of the seven indeterminate Save52 associations. Keep proprietary binary bytes, dumps, raw receipts and saves local-only; tracked research must be reproducible using authored descriptions, hashes and lawful local-input instructions. Run bounded, read-only offline analysis and isolated synthetic tests, not a broad Starfield save-format rewrite.

## 3. Investigation workstreams

### A. Population object, ownership and identity

Trace backwards **from the actual native consumer** observed in D5B to the region-bearing object, its backing arrays/wrappers and the collection responsible for providing it. Reconcile any seemingly different native entry points used by producer and consumer. Establish to the extent possible:

1. Allocation sites, constructor/initializer path, population materialization and array ownership, including deep vs shallow references and any copy-on-write or forwarding.
2. Exact lookup key construction and equality/hash/comparator semantics. Identify every discriminating dimension (body, map cell/source key, context, seed, biome, generation version, owner or other actual native field); do not equate source ordinal or display name with complete identity without proof.
3. Reference-count/handle/lock semantics, holder relationships, ephemeral/local storage versus retained manager storage, and destruction/freeing. Include pointer-reuse hazards.
4. The structural difference between **source definition**, **generated resource region population**, and **Workshop area/resource result**. Diagram the data path and distinguish observed layout from conjectured roles.

Deliver a source-cited object/key/ownership map with exact function addresses or stable native pins, branch conditions and per-claim evidence grade. Record alternate interpretations where code or fields remain ambiguous.

### B. Lookup, reuse and construction chronology

Trace representative entry paths from a consumer/query to **lookup**, **hit/miss decision**, **construction**, **insert/replace** and **return**, showing conditions for skipping region generation. Determine whether generated region data is retained beyond the initiating native call and, if so, by what object and for what demonstrated scope.

Specifically examine whether two distinct initial queries that map to one source identity could lead to different generated populations, and whether the **first request** can determine the population observed on subsequent requests. Treat it as a testable hypothesis, not a conclusion. Determine whether duplicate concurrent constructions are possible, whether winners are deterministic, how synchronization works and whether masked construction context is included in the cache key. A static possibility of differing masks is **not** evidence that the game has ever served two different populations at the same outpost.

Describe lookup miss vs invalid/expired/missing entry, and distinguish an actual reuse fast path from generic object lifetime. Capture exact branch predicates and critical native evidence; if indirect or dynamically resolved, record that limitation.

### C. Invalidation, mutation and lifetime boundaries

Map supported destruction, clearing, eviction, replacement, refresh, and source-owner teardown paths. Follow the effects of terrain/cell/worldspace change, source-manager recreation, outpost placement/movement and resource/biome context changes **only where code shows a relevant linkage**. State which events can modify the population versus merely recompute a consumer overlay.

For each lifecycle boundary, specify: owning structure, triggering operation, predicate, old/new lifetime identity, retained/invalidated state and known race or uncertainty. Preserve potentially contradictory branches rather than selecting one that explains Feynman VIII-b.

### D. Save serialization and Save52 load timing — strictly bounded

Search for serialization or restoration paths that **actually read/write generated region-population fields or owning collection entries**. Check save-form records and loading call chains only to the extent they bear on the population object. Distinguish:

- persisted **geometry** (full region members) versus persisted **recipe/seed/source identity**;
- native **load-time construction/reconstruction** versus later lazy/on-demand construction;
- reuse within a single process versus survival across process boundaries;
- a Feynman V Workshop being restored versus the Feynman V source population being materialized.

Trace load/init sequencing as far as offline evidence supports, including whether outpost/worldspace initialization can demand resources before the player arrives. **Absence of an obvious serialization call is not proof that geometry is not saved**, and the existence of a save record referencing a source is not proof that generated regions are saved. Avoid a complete save-format archaeology diversion. If direct Save52 load timing cannot be established statically, explicitly say so and identify the narrowest runtime event needed to demonstrate it.

### E. D5B evidence reconciliation and implications

Produce an evidence classification matrix for at least these propositions: collection retains region populations; existing population can be reused without re-running generator; collection key fully identifies population; population is present as Save52 load completes; construction occurs during Save52 load; geometry is serialized; D5B consumed a previously retained source; D5B's historical construction sampled mask 3; two initial queries can yield different retained geometry; cache/retention could explain Feynman VIII-b mutation.

Use **DEMONSTRATED / CONTRADICTED / PLAUSIBLE-BUT-UNPROVEN / UNRESOLVED** (or equivalent explicitly defined categories), with links to exact evidence and falsification conditions. Keep the distinction between D5B's **three exact mask-3 geometry matches** and **unknown constructor query, sampled mask, cache state and epoch**. Do not turn an instrumentation non-hit into a native negative event. Separate model prediction, native code proof, synthetic demonstration and retail observation.

If a missing observation is essential, specify the event boundary, identity and timing discriminators, minimal fields, alternative outcomes and why existing D5B capture cannot resolve it. Return a **proposed, not authorized** acquisition or synthetic qualification design; do not build or execute a new retail collector unless separately authorized.

## 4. Deliverables and working method

1. A durable, concise main report (under a logical `docs/experiments/` subdirectory) with executive findings, source/object diagrams, chronological control-flow, identity/key table, provenance and evidence grades, limitations, D5B interpretation, and next-step recommendation.
2. Auditable source register: native address/RVA, module/build pin, corresponding decompiler/export or existing receipt, decisive read/branch evidence, proposed role, certainty and reviewer cross-reference. Small quoted byte/field excerpts only if allowed by repository rules; no copyrighted binaries or raw protected data committed.
3. A lifecycle matrix including lookup, first construction, reuse, replacement, teardown, serialization, load-time initialization, and unknown boundaries; distinguish **proved call graph** from **demonstrated runtime frequency**.
4. Read-only, narrowly scoped helper scripts or synthetic fixtures *only if they materially test a specific claim*. Prefer existing tools. Include exact commands, inputs, hashes, actual execution status, failure cases and output checks. No obligation to write production code for a purely static result.
5. A case-specific reconciliation of Feynman V D5B with the complete range of cache/no-cache explanations, plus controlled discussion of potential implications for VIII-b (not bug reproduction).
6. If unresolved, an explicitly bounded follow-on experiment proposal/run-card **draft** with decision outcomes, trigger/observation timing relative to Save52 load, event association and anti-confounding criteria. **No live GO.**
7. Final review package, protection verification, machine-readable complete/task-only manifests, SHA-256 for final files and patches, and exact verified complete/task-only diffs; identify pre-existing changes rather than silently including unrelated work. No staging/commit/push.

Keep scope finite. After tracing the principal source construction/lookup/consumer and their direct ownership and save/load edges, stop expanding unrelated engine subsystems when another hop cannot discriminate the defined hypotheses. Record the concrete blocker rather than inventing a universal negative result.

## 5. Frozen acceptance criteria AC1–AC8

| Criterion | Required evidence |
|---|---|
| **AC1 — Scope and preservation** | No retail launch/attach/game modifications; pinned executable/data, protected saves and evidence unchanged; original D2–D5B findings and local-only materials preserved; no staging, commit, push or publication. |
| **AC2 — Population ownership** | Native-backed allocation/representation/holder/destruction account for the generated resource population, including distinction from static source definitions and Workshop results; uncertainty explicit. |
| **AC3 — Lookup/reuse semantics** | Exact collection key and lookup decision traced as far as evidence permits, with supported hit/miss/reuse claims and alternative source-context handling; missing key dimensions identified rather than guessed. |
| **AC4 — Lifecycle/invalidation** | Trace relevant construction, insert, replace/evict/invalidate and teardown paths; assess same-source different-initial-query hypothesis without presupposing a cache or observed history dependence. |
| **AC5 — Save/load boundary** | Targeted examination of population serialization, restoration and initialization/load triggers; distinguish demonstrated paths, negative searches and unresolved timing, specifically for Save52/Feynman V. |
| **AC6 — D5B scientific reconciliation** | Proposition-by-proposition evidence status, preserving exact mask-3 consumer geometry but unknown construction mask, historical cache state and population epoch; no unapproved Save52 reclassification. |
| **AC7 — Reproducibility/editorial quality** | Native/source pins, durable report, lifecycle diagrams/matrices, exact actual tests and protected-input check; all ten geometry controls/frozen outputs unchanged (rerun when touched, otherwise hash/integrity-check and accurately qualify). Final prose follows `docs/EDITORIAL_STANDARD.md`. |
| **AC8 — Independent review and deliverable** | Independent reviewer validates scientific inference, native/engineering claims, negative evidence, unchanged inputs, final editorial state and final complete/task-only diff/manifests/hashes. Provide ACCEPT or precise ESCALATE against each AC; fix and re-review substantive defects. |

These criteria are binding and must not be relaxed to manufacture success. **An honest finding that save-load population timing cannot be resolved offline can satisfy AC5 if the specific inspected paths, missing link and discriminating next observation are demonstrated.** Do not claim an unsupported negative conclusion. A valid partial result can close the bounded investigation with an explicit research uncertainty; a broken or unreviewable method cannot.

## 6. Completion and handoff

The completion summary must state: HEAD/branch and baseline cleanliness, paths added/changed, actual native inputs accessed and verification pins, source/key/ownership/lifetime findings, which caching and Save52-loading claims remain unsupported, D5B implication, tests and control integrity, evidence/protection hashes, independent-review disposition per AC, exact final diff/manifests and any unapproved next-run proposal. Explicitly state **no retail session authorized or performed**.

Suggested commit message **only if subsequently approved by maintainer**: `docs(research): trace resource-source population lifecycle`.

**Research priority:** establish what the native implementation does before explaining historical anomalies. **B6 publication verification stays on hold.**
