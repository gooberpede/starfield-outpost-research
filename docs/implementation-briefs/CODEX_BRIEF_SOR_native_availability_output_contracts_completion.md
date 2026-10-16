# Codex Research Brief — SOR: Native Resource Availability Output Contracts and Research Completion Assessment

**Assignment type:** bounded, offline research and documentation assessment  
**Repository:** `starfield-outpost-research`  
**Authority:** This brief supersedes no standing repository workflow or preservation requirements. Do not stage, commit, push, launch Starfield, deploy plugins, modify saves, or make native calls.  
**Purpose:** Decide whether the existing Starfield native resource-availability research has reached a useful, well-supported endpoint, and consolidate the evidence necessary for others to understand the native output contract.

## 1. Central research question

> Have we mapped Starfield's native inorganic resource-availability machinery sufficiently that another researcher can identify the relevant native functions, understand their execution and data contracts, and determine where and under what conditions the game's calculated resource identities can be observed or obtained?

**This is not** a request to implement an extractor or a mod, design hypothetical developer workflows, independently reproduce planetary resource generation, or prove all possible calls into the game safe. The objective is an accurate, reusable native technical reference—not exhaustive decompilation or a complete functional facsimile.

A finding can be complete despite unresolved questions about arbitrary remote sites, independent invocation, exact spatial predicate equivalence, or exceptional planets. Those limitations must be visible and accurately scoped, not silently treated as resolved.

## 2. Research baseline and sources

Start from the repository's currently committed work and inspect the actual artifacts; do not treat this brief's summary as a substitute for source evidence. In particular:

- Existing native function register, resource-availability dataflow and minimum-inputs records under `docs/experiments/native-availability-map/`.
- Resource-region lifecycle and minimum-runtime-requirements research (`region-dependencies.md`, `region-lifecycle.md`, `region-requirements.md`, and associated registers and evidence).
- Milestone B spatial predicate research and qualified limitations.
- The completed 0.7.0 natural beacon-preview experiment and its original captured/derived evidence, including 346 matched native UI folds; distinguish observed data from interpretations.
- The unadopted 0.8.0 observer and the subsequent NO-GO reassessment; neither its engineering qualification nor its run card demonstrates retail results.
- Experiment A feasibility, synthetic qualification, x87 preservation and final geometry-lifetime NO-GO; do not reopen or repeat those tasks.
- Repository `WORKFLOW.md`, `AGENTS.md`, source/provenance pin requirements, and current documentation indexes.

Relevant starting RVAs on the pinned **Starfield 1.16.244.0** executable are the common updater `0x021E07D0`, UI consumption `0x01578500`, established Workshop descriptor builder `0x00F4A140`, and resource-region provider `0x0079F860`. Confirm identity/version and existing citations before repeating them in durable documentation. Do not infer signatures or safe invocation solely from RVAs.

## 3. Workstream A — output population contract

Trace and document the output *as it exists in native execution*, not merely the UI rows:

1. Identify the native producer, updater, storage locations and consumer(s) of the final inorganic resource populations.
2. Describe their relevant data structures: identity type, collection layout, membership semantics, deduplication, ordering, spatial/atmospheric/biome-water contributions, and state retention or invalidation behavior **only to the extent supported**.
3. Locate the point or points where a complete population is available in ordinary execution. Distinguish a complete snapshot at a given event from a guarantee that it is fresh for all possible contexts.
4. Establish the native object's ownership, lifetime and mutation rules relevant to reading or copying *resource identities* into independently owned storage. Do not conflate this comparatively small result collection with the separately unresolved ownership of full generated region-point geometry.
5. Document any constraints on thread, native callback lifetime, source reference or frame, synchronization and object state that materially affect an observation; explicitly mark inferred versus demonstrated guarantees.
6. Explain what the successful 0.7.0 trace directly demonstrates, what static analysis additionally supports, and what remains unverified. In particular, do not present the natural preview path as proof of arbitrary direct invocation.

If an exact safe read/copy contract cannot be supported without live experiments, report the bounded contract and missing evidence. Do not claim safety by analogy alone.

## 4. Workstream B — prospective versus established path

Map each path separately, and identify their convergence:

- **Prospective beacon:** origin of reference, indexed position descriptor, radius, upper-coordinate scalar, query-state initialization and final population consumption as supported by the source and 0.7.0 runtime record.
- **Established Workshop:** Workshop reference resolution and descriptor construction, relevant state setup, downstream availability updater and any native consumer/output collection. Record the actual call chain and any differences in area construction, cached state or lifetime.
- Clearly distinguish **statically established convergence on the common updater** from **unperformed runtime equality tests**; similar centers need not imply identical radius, vertical bounds or state.
- Determine whether missing established-path runtime observation is consequential to the research endpoint. If yes, specify the exact unresolved output/association contract and why it prevents completion; if not, state why a qualified static mapping suffices.

Do not require or design another live experiment simply to obtain symmetry between the paths.

## 5. Workstream C — provenance, function map and navigable reference

Extend the existing native function register rather than building a competing inventory. Produce a neutral technical reference that connects:

- RVA, pinned executable version, analyst-assigned/known function name, and source/evidence reference.
- Verified call edges and dataflow relationships, noting indirect dispatch or inferred scheduling separately.
- Inputs, outputs, relevant object and field layouts, ownership/lifetime, side effects, and context prerequisites.
- Observed versus static-only versus hypothesized properties with explicit confidence and unresolved questions.
- The path from area descriptor through resource-population assembly to the point at which resource identities can be read.

Expose a concise entry point in the repository's existing documentation navigation. Avoid describing untested code paths as publicly supported APIs, and do not give hypothetical mod-specific implementation instructions or gap analyses.

## 6. Workstream D — explicit completion assessment

Apply this research-level standard:

> Would a technically capable reader, using the documented executable version and native references, understand where Starfield determines the available inorganic resources of a naturally evaluated area and where its resource identities become accessible, including material lifetime/context caveats, without repeating the central reverse-engineering work?

Produce one of the following judgments, with reasons:

- **COMPLETE:** The native output contract and normal execution relationships are sufficiently established for the stated research endpoint.
- **CONDITIONALLY COMPLETE:** The native machinery is sufficiently mapped to be useful, but clearly identified limitations constrain the contexts or guarantees; those limitations do not justify continuing this research line solely to obtain completeness.
- **INCOMPLETE:** A specific missing *consequential* function, data contract, output association or ownership condition prevents the stated endpoint. Identify that exact blocker and the smallest evidence that could settle it. Do not turn every unvalidated branch into a blocker.

The assessor must be willing to conclude COMPLETE or CONDITIONALLY COMPLETE. Do not create additional work to avoid closure. A reviewer must challenge any claim that an unsolved spatial geometry capture, remote world query, or full planetary generation is necessary for this limited endpoint.

Explicitly separate **what the engine computes**, **where the calculated result resides**, and **whether an independently authored caller can invoke the engine operation at will**. The last is not required for completion, but its limitations must not be obscured.

## 7. Scope constraints

**Authorized:** offline inspection of existing native exports, pinned disassembly/decompiler artifacts, past captures, local research tools and project documentation; minimal focused documentation/index/source-assertion corrections directly necessary to substantiate the output contract.

**Not authorized:** Starfield launch or gameplay, debugger attachment, DLL/SFSE observer or Vortex work, direct native calls, new save manipulation, resource extractor or mod code, more spatial-equivalence instrumentation, remote-resource generation research, speculative caching experiments, broad reverse engineering, or an independent replacement resource algorithm. Do not delete or modify sealed historical evidence or protected research inputs.

Do not expand scope to the separately deferred disappearing-deposit investigation (including ongoing extractor production versus placement geometry). It can be noted as future research, not investigated under this task.

## 8. Evidence, preservation and verification

- Follow repository workflow and provenance requirements, including protection of native exports, binaries, Ghidra projects, historical captures and saves.
- Verify changed assertions against pinned sources; do not fabricate source observations or infer runtime behavior from compiler-style pseudocode without qualification.
- Run appropriate existing tests and links/index/document checks. Preserve test results, exact commands, relevant hashes and source pin scope. Do not portray selected pin checks as complete repository-wide checks.
- Review all newly authored or changed prose for malformed spacing/fused tokens, including version numbers, RVAs, file names and code/text boundaries. Correct defects in task scope and include a concise prose audit.
- An **independent reviewer** is mandatory for source-contract accuracy, evidence taxonomy, completion outcome and prose quality. One optional specialist may assist, with no more than two active sub-agents at once, subject to repository workflow. The reviewer should challenge unsupported claims, inflated completeness requirements, and unnecessary new research.
- If consequential issues emerge in review, correct and re-review within scope. Do not silently weaken the completion standard.

## 9. Deliverables and handoff

1. A clearly named **native output contract** reference, linked into the existing native function register and documentation navigation, with source-level evidence and confidence qualifications.
2. A concise **prospective versus established Workshop** dataflow and output-association assessment, distinguishing observed versus static-only claims.
3. A **research-completion report** with COMPLETE / CONDITIONALLY COMPLETE / INCOMPLETE verdict, evidence supporting it, exact remaining limits and whether anything genuinely blocks research closure.
4. A **review record**, verification/preservation summary and prose-quality audit.
5. Both **task-only** and **complete** review diffs under `.local-work/diffs/`, including relevant untracked text in the complete diff; identify artifacts and their hashes in the review package. Do not include proprietary binaries, saved games or raw captures inside the diffs.
6. Suggested Conventional Commit subject for later maintainer approval. **Do not stage, commit, push or sync.**

## 10. Final reporting

Report the completion verdict at the top. State in ordinary language what another researcher can learn from the map and what is not established, avoiding promises of a working extractor or general native invocation API. Where confidence depends on static analysis alone, say so. Do not recommend a live experiment unless the completion verdict is INCOMPLETE and the missing *essential* evidence can be stated and justified; even then, make it a separate proposal only, not an authorization.

**Success is a reliable and reusable account of the game's native resource-availability output machinery, with a defensible research stopping point—not a maximal reverse-engineering effort.**
