# Codex research brief — SOR: Local Inorganic Resource Availability — Native Function Mapping, Dataflow and Minimum Inputs

**Status:** Implementation/research assignment for Codex; offline only; maintainer review required.  
**Supersedes:** `CODEX_BRIEF_SOR_local_inorganic_resource_query_native_contracts.md` in full. Do **not** combine its modder-oriented gap-analysis requirements with this brief.  
**Repository:** `D:\Projects\starfield-outpost-research` (continue from current committed/synced research state).

## 1. Scientific purpose

Investigate **how Starfield itself determines the set of inorganic resources present within a proposed or established local Workshop area**. Map the actual native functions, state, inputs, outputs, interactions and provenance; determine the minimum sufficient inputs and runtime prerequisites for that calculation. Produce a neutral technical account that another investigator can use for their own purposes.

The subject is **engine behavior**, not implementing a particular mod, an API for mod authors, an Outpost Tracker import feature, or a hypothetical developer's gap analysis. Do not recommend what a prospective mod author *should* implement to accomplish an unspecified goal.

The authoritative resource set for the supported preview conditions is the game's **Available Resources** panel. Our existing 0.7.0 observations confirmed agreement of native resource identities, native UI rows and the player-visible A/B/C sets. The goal here is to explain the calculation and its **minimum inputs**, not to reopen whether the panel's resources can fit extractor footprints.

## 2. Existing research to carry forward

Read the current durable record before beginning. In particular:

- `docs/experiments/resource-availability/` and `docs/experiments/resource-availability-milestone-b/` reports, ledgers and review documents.
- `docs/experiments/continuous-beacon-preview/` live scientific report and the 0.7.0 capture/decoder evidence, including the 35,574 completed evaluations, 11,128 distinct query descriptors and 346 validated native UI updates (retain their precise scope).
- Existing executable partial resource/spatial models and their tests; installed ESM definitions, prior native-code exports and relevant function registers.
- The project's `WORKFLOW.md`, provenance/permission instructions, experiment conventions and frozen research records.

Treat earlier hypotheses as hypotheses. Preserve all frozen predictions and primary evidence. The prior reconstructed functions and RVAs are leads subject to verification against the pinned executable, not free-standing guarantees of contract or general applicability.

## 3. Research questions and required deliverables

### A. Native function register — mandatory

Create or extend a structured, source-linked register covering the function chain involved in local inorganic resource availability. For each relevant function, record where supportable:

- Pin to executable/module build and RVA; any actual symbols versus analyst-assigned descriptive names.
- Native purpose, role in the calculation and observed call sites/consumers.
- Inputs and calling convention, object/layout types, pointers, coordinate domains and units; distinguish known from inferred.
- Return values, out-parameters, mutated containers and other observable outputs.
- Preconditions (loaded world, terrain/ProcGen resource caches, candidate-area descriptor, biome/atmosphere state, initialization and thread/lifecycle state).
- Side effects, caching, lazy generation, scheduling/queue behavior and invalidation where established.
- Relationships and call/ownership edges to upstream state producers and downstream resource/UI consumers.
- Actual exposed interfaces (including Papyrus or SFSE when demonstrably present), stated **only as facts about engine functionality**, not mod-building recommendations.
- Evidence references, confidence, coverage limits and unresolved semantics.

Include already identified resource producer, region/geometry-query, spatial eligibility, atmosphere/biome contributions, aggregation and UI-model paths. Don't assume there is one all-in-one availability function.

### B. Native dataflow specification — mandatory

Reconstruct the actual dependency chain from a **candidate area** through local resource-region retrieval, native inclusion predicates, identity resolution, atmospheric and biome contributions, deduplication and the displayed set. Distinguish:

1. Data supplied by the caller.
2. Data obtained from the currently loaded or cached world.
3. Data computed or generated on demand.
4. Data passed between synchronous functions versus asynchronously queued UI updates.
5. Data that is merely read from the native output, not an input to deciding availability.

Represent branching, missing state and failed lookups faithfully. Separate *available-resource identity evaluation* from resource-generation geometry construction and from unrelated harvester placement validation. Include coordinates/frame and radius/height semantics where justified by source evidence.

### C. Minimum sufficient input analysis — mandatory

Establish, as precisely as the evidence allows, the least information required by **the engine's own calculation** to determine a resource set for a local area. Examine both:

- A prospective beacon location in loaded terrain (as in the 0.7.0 preview).
- An already established Workshop within loaded terrain, insofar as its data/state can supply the same calculation.

Determine which apparently required parameters can actually be resolved from native context. Distinguish an input to an inner geometric predicate from the input an upstream native operation requires; **do not mistake a supplied region array for a necessary external argument if the engine can itself retrieve or construct it**.

For each proposed minimal contract, declare its context, sufficient inputs, hidden prerequisites, output/failure/UNKNOWN behavior, and the evidence demonstrating sufficiency. If sufficiency is not established, state the exact missing dependency and do not present a hypothetical signature as an implemented callable contract. It is acceptable to identify several native boundaries with different minimum-input sets.

Remote/unloaded planetary queries are **out of scope** except to identify facts about dependencies that naturally emerge from the local investigation. Do not produce a modder's feature or implementation gap analysis.

### D. Executable verification and evidence ledger — mandatory

Reuse the established partial spatial evaluator and 0.7.0 capture, rather than replacing them. Add deterministic tests and/or analysis code where it tests a recovered native contract or a distinct dependency. The reader must be able to distinguish:

- independently observed input/output pairs;
- static instruction-derived arithmetic verified by synthetic test vectors;
- reuse of captured resource sets or final UI rows (which is **not** independent validation of upstream geometry);
- repeated observations versus independent geometries;
- unavailable operands or source-frame/region context.

Preserve native resource identities and the atmospheric Helium-3 versus spatial Iron/Alkanes provenance in the captured Kreet conditions. X-Tech remains an explicitly scoped exception; do not conflate place-anywhere extractor rules with naturally present resource identities. No need to prove the fit of a physical extractor footprint.

### E. Neutral technical reference and research disposition — mandatory

Deliver readable documentation, a maintained native-function map and a concise evidence/uncertainty register. State what is established, conditional, and unresolved, and which specific observation or native dependency would settle each residual question. A later investigator should be able to perform their *own* gap analysis; **Codex must not perform that analysis for imagined mod requirements**.

If further live evidence would be decisive, formulate a **discriminating scientific acquisition question** with exact missing operands and distinguishable outcomes, not an observer implementation assignment. Reuse of the shared session infrastructure is a future possibility, not part of this offline task.

## 4. Completion contract

Adhere to the repository Research Execution and Completion Protocol: in-scope obstacles and failed tests belong to this assignment, not another automatic handoff. Deliver one of:

- **A — Supported native function/dataflow and minimum-input reconstruction:** all mandatory artifacts delivered, with supported contracts and independently defensible evidence inside the explicitly established domain; or
- **B — Completed evidence-bounded investigation:** exhaustive **relevant authorized** dependency tracing, runnable recoverable components, and precise demonstration of which input/state or native result cannot be established offline. B must not be a superficial list of missing inputs or an application-oriented workaround.

Both outcomes must include the function register, dataflow, minimum-input assessment, tests, provenance, uncertainty and a decision-ready technical conclusion. Do not claim arbitrary local query feasibility, full terrain-generation equivalence or universal resource reconstruction without the required evidence.

Have an **independent reviewer** assess the original contract, primary evidence and claims. Permit up to **one optional specialist researcher** on an independently useful workstream (e.g. loaded ProcGen resource-region provider/caching dependencies). Maximum **two concurrently active sub-agents**, excluding the primary agent. The reviewer must return REWORK for unmet in-scope requirements and require correction within this assignment. Report the specialist's concrete contribution briefly, without renewed routine evaluation of reviewer value.

## 5. Limits, permissions and preservation

- **Offline only:** no Starfield launch or process access, SFSE deployment, new native hooks or debugger attachment, native call injection, controlled-save creation or original-save modification.
- Respect owner/third-party intellectual-property, licensing, provenance and attribution policies. Public third-party code may be consulted subject to the standing rules; do not copy implementations without permission.
- Preserve raw captures, sealed evidence, executable/ESM inputs, save archives, frozen outputs and existing scientific conclusions; do not silently rewrite historical reports.
- Retain the established **40,000,000,000 free bytes** guard on C: and D: where local bulk processing requires it; do not invent arbitrary time or data-volume cutoffs.
- Do not stage, commit or push. New local raw/derived evidence stays in ignored work directories; no proprietary data in patches.
- No broad UI rework, Tracker/Planner implementation, X-Tech construction feature, general ore-vein geometry generation or remote resource-query project is authorized.

## 6. Review handoff

Provide:

1. Technical report and actual native function register, with pinned RVAs and source/evidence links.
2. Native dataflow/dependency map and minimum sufficient input assessment for local prospective and established Workshop contexts.
3. Deterministic tools/tests and reproducible receipts, explicitly reporting what was **not** independently validated.
4. Evidence/uncertainty register, any bounded future acquisition recommendation, and independent reviewer verdict/REWORK record.
5. `git status --short`, changed/excluded file manifest and **task-only** and **complete** review diffs under `.local-work/diffs/`, including untracked authored text, with forward/reverse and completeness checks.
6. Suggested **Conventional Commit** subject only; do not commit.

**Acceptance principle:** Document Starfield's native functionality neutrally and accurately enough to be useful to future researchers with unpredictable goals. Do not orient conclusions around hypothetical mod features or prescribe missing mod implementation work.
