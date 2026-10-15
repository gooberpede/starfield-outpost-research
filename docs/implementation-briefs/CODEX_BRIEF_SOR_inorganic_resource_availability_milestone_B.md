# Codex Research Brief — SOR Inorganic Resource Availability Milestone B
## Native Algorithm Reconstruction and Input Provenance

**Project:** `D:\Projects\starfield-outpost-research`  
**Assignment type:** offline research, deterministic implementation, scientific verification  
**Starting state:** latest committed and synced research, including successful SorNativePositionOracle 0.7.0 preview capture and shared session infrastructure  
**Authority:** no game launch, SFSE deployment, new hooks, save writes, staging, commit, or push  
**Agents:** primary Codex implementer; independent reviewer mandatory; one optional specialist researcher, maximum **two active sub-agents** at any time.

## 1. Scientific purpose and controlling definition

Recover and explain **how Starfield determines the inorganic resources displayed in the Available Resources panel for a proposed outpost beacon position**. The game's displayed set is our authoritative gameplay oracle. The position is that of the **unplaced prospective beacon**, not necessarily the player character. Resource presence is not active extraction, and this assignment does **not** require demonstration that an extractor footprint can be placed. Do not introduce extractor collision, placement feasibility, minimum vein area, or construction-cost requirements as additional acceptance criteria.

The mechanism must be described for use by independent game-engine researchers and mod authors, not tailored exclusively to Outpost Tracker or a speculative Planner. A correct runtime model is scientifically valuable even if the information cannot be reconstructed from save files.

**Known baseline:** previous offline work identified `WorkshopAreaResourcesDataModel`, producer `0x1421E07D0`, UI-row builder `0x141578500`, native spatial resource-region contribution, atmosphere contribution, and a biome-derived/water contribution. The 0.7.0 live run recorded **35,574 complete resource evaluations, 346 reconciled native UI updates and 611,926 verified records**. The observed resource sets at Kreet included Iron + Helium-3, and Iron + Alkanes + Helium-3, with a return to Iron + Helium-3. These are established observations, not an invitation to assume the underlying algorithm. Consult canonical committed reports and sealed local evidence for precise identities, provenance and qualifications; don't rely on these summary values as primary evidence.

## 2. Two technical levels

### B1 — Native resource-availability evaluation (mandatory)

Reconstruct the actual decision rules that, given **qualified native inputs**, determine which inorganic resource identities are included for a prospective Workshop area. This includes:

1. Query-region representation, coordinate/frame interpretation and prospective beacon position at the **evaluation boundary**.
2. Resource-region candidate retrieval and spatial membership/intersection logic, including relevant point-count branches, radii, boundaries, floating-point behavior and other native predicates actually used.
3. Resolving candidate region/definition identities to stable inorganic resource identities, without confusing IRES definitions, actor values, production recipes and displayed names.
4. Atmosphere-associated resources, including Helium-3 on Kreet.
5. Biome-derived contribution, including the previously identified water-specific path where applicable.
6. Union, filtering, deduplication and any presentation-order semantics; distinguish a *set* from UI row ordering and asynchronous model updates.
7. Special cases (including X-Tech) clearly isolated from ordinary inorganic resource presence. Do not infer site presence from a place-anywhere construction exemption.

Deliver a **documented executable evaluator** with an explicit, versioned input/output contract, typed unknowns and diagnostic provenance. An implementation that merely unions already-finalized sets supplied by the game is **not** enough to satisfy B1: trace and implement the native *spatial membership* logic to the maximum extent supported by the capture and static code. Exact agreement must use qualified actual operands and independent native results, not predictions made by the evaluator itself.

### B2 — Input provenance and independent reconstruction (substantive investigation required)

Trace how each B1 input is produced, selected, cached or retrieved in the live game:

- Procedural resource-region geometry, indexing and identity; selected landscape/terrain frame and relevant world/body/biome context.
- Atmosphere and biome resource-definition relationships, including installed ESM/record dependencies.
- Cached resource state, invalidation and evaluation-to-UI queue boundaries where they affect interpretation.
- Whether required state or sufficiently deterministic upstream parameters appear in saves; distinguish saved construction/producer registries from site availability. Existing extractors provide only a positive, incomplete proxy and cannot define the full availability set.

Follow concrete native producer dependencies to a defensible boundary. **Do not let B2 silently expand into complete planetary terrain/ore-vein generation** if a narrower qualified region representation suffices for B1. Equally, do not declare B2 finished simply upon finding a terrain function or a missing pointer; investigate reachable offline dependencies and identify precisely which producing quantities remain absent.

## 3. Evidence-first execution plan

1. Inventory the committed scientific reports, `0.7.0` native capture and decoding/inspection tools, prior partial resource evaluator, installed resource definition exports, controlled and mature saves and existing test harnesses. Establish exact source, capture and tool identities. Preserve all existing inputs, historical findings and frozen position predictions.
2. Analyze **all relevant 0.7.0 evaluation populations** with streaming/bounded-memory readers; quantify unique native input geometries and region identities, meaningful branch coverage, candidate-set transitions and repetition. The 35,574 records are **not** 35,574 independent test geometries. Separate genuine operands, inferred values, UI-model rows and manual screenshot/operator reports.
3. Independently reconstruct the resource-region evaluation native control flow and floating-point behavior; confirm the actual ABI, condition order, boundary and special-case rules in the pinned retail executable. Use prior source ledgers and direct native evidence rather than assuming names imply semantics.
4. Build/extend the executable B1 evaluator, frozen reference controls and adversarial tests. Preserve counterexamples and report mismatches; do not tune original evidence or silently change expected data.
5. Pursue B2 producer dependencies, static definitions and save representations in parallel where useful. Record which input values can be sourced offline and which are available only from live runtime state.
6. Produce a clear technical specification, validation corpus/receipts, coverage matrix and a *decision-ready* recommendation about whether another live acquisition is indispensable. Avoid speculative hook lists.

Suggested division: primary agent owns capture archaeology, evaluator and integrated scientific claims. Optional specialist independently follows native spatial-resource generation / index and producer provenance, with explicit source-supported findings. Independent reviewer evaluates original contract and primary evidence, checks circular validation, requires REWORK on correctable failures and challenges premature evidence-bound claims. Do not spawn more than two sub-agents concurrently.

## 4. Scientific validation and exclusions

- Test exact set agreement at qualified A/B/C Kreet contexts, including the atmospheric control, Iron/Alkanes transitions and UI-model updates, **without claiming exact render-frame timing** or fabricating unique asynchronous ancestry.
- Exercise native point-count alternatives, empty regions, geometry boundaries, reflected/translated coordinate inputs where applicable, float32 rounding, duplicate resources, cache repeats, malformed/unavailable operands and special resource classes.
- Treat independently captured actual native outputs as oracle evidence; a rerun of the same algorithm or native inputs computed by the model is not an independent validation.
- Do not conflate planet-wide resource populations, local prospective-beacon availability, active extraction, unlocked build-menu items and valid harvester footprints.
- Treat X-Tech as a separately documented exception; do not force it into ordinary vein rules.
- Never infer a resource's **absence** from an absent extractor in a save.
- No terrain geometry generation, new live capture or native instrumentation is required by default; any future proposal must identify exact missing operands, competing predictions and why existing evidence cannot discriminate them.

## 5. Completion contract (Research Execution and Completion Protocol)

The assignment must end with independent reviewer evaluation of **the original criteria**, not a narrowed self-selected scope. Correct in-scope test failures, trace promising native dependencies, requalify and resubmit under the **same assignment** rather than handing off an unfinished problem.

**Outcome A — validated B1:** Executable native-style availability evaluator agrees with independent captured native data over a clearly characterized set of geometries and branches; B2 gives a credible input-production model with explicit coverage and remaining dependencies. Full site-to-set generation for arbitrary planet locations need not be claimed without its inputs.

**Outcome B — completed evidence-bounded result:** Deliver the deepest defensible executable evaluator and native dependency reconstruction; explicitly demonstrate which indispensable operands/branches are absent from authorized offline evidence, which hypotheses remain distinguishable, and what *specific* acquisition would be needed. A set union, static record catalog or generic “terrain procgen unknown” is insufficient. The independent reviewer must challenge exhaustion of available evidence.

In both cases distinguish scientific confidence, branch coverage, identity confidence, practical usability and native-equivalence scope. Do not convert an untested branch into an assumed rule. If genuine permission or machine-safety authority is needed, escalate with an exact proposed action; do not attempt it.

## 6. Outputs and durable record

Deliver all of the following together:

1. **Milestone B technical specification:** readable data flow, native inputs, algorithms/conditionals, coordinate frames, provenance, output schema, cache/UI behavior and evidence citations or stable local references. Keep suitable for later external research publication, without publishing private game assets.
2. **Executable B1 evaluator:** deterministic CLI or importable library, focused tests, sample inputs/outputs, clear `UNKNOWN` semantics and input validation. Reuse existing code where appropriate; avoid overlapping competing implementations.
3. **B2 provenance/dependency ledger:** resource-region, atmosphere, biome, UI and serialization sources with qualified native instructions and uncertainty annotations.
4. **Capture coverage and validation report:** unique-vs-repeated cases, branch matrix, native comparisons, counterexamples, preserved raw evidence identity and reproducible command/receipt.
5. **Decision and acquisition assessment:** Outcome A/B, precise scientific limitations and the minimal justified next action if needed.
6. **Independent review and rework evidence**, specialist contribution assessment where used, complete/task-only diffs under `.local-work/diffs/`, file manifest, status, preservation checks and conventional commit proposal (do **not** commit).

Keep raw records, proprietary data, executable binaries and large private receipts local/ignored. Update existing indexes, scientific-state ledger and durable backlog accurately without reopening the deferred native Z, continuous geographic coordinates, historical Hab ownership or other unrelated work.

## 7. Constraints and operations

**Offline only.** No Starfield execution, SFSE plugin implementation/deployment, UI automation, save creation/modification, external debugger revival, staging, commit, push or public disclosure. Consult source and installed game records only under existing permissions and provenance rules; record third-party authors/licenses/revisions and do not copy outside code without permission.

Preserve all 0.7.0 raw capture, protected saves, prior verification receipts, native exports, game files and **23 frozen position predictions**. Run required protected-input and preservation checks. Maintain the 40,000,000,000-byte free-space guard on both C: and D: for substantial evidence operations. Stream large datasets, avoid redundant  multi-gigabyte materialization, and do not create arbitrary elapsed-time, event-count or file-size cutoffs as scientific stop conditions. Existing shared `runtime/session-tools/` is available but **not** to be reworked in this task.

Codex should return a completed scientific package for critical review; the maintainer will decide on commit or any subsequent live observation.
