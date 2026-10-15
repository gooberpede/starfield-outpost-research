# Codex Research and Implementation Brief — SOR Local Availability Readiness: Native-Execution Observation

**Status:** Implementation/research brief; **not authorization to deploy or launch**.  
**Repository:** `starfield-outpost-research`  
**Proposed working title:** *Local inorganic availability: ProcGen readiness, native evaluation and cache-state observation*  
**Execution mode:** Prepare and qualify a single focused, passive native observer and an integrated experiment package; stop for user/ChatGPT review before live execution.

## 1. Scientific purpose

Establish, through observation of **natural Starfield native execution**, the relationships among (a) readiness of local ProcGen resource-region data, (b) the common native area-resource availability updater, (c) cache history and freshness, and (d) the inorganic resources the game reports for a specified area in the currently loaded planetary environment.

Primary questions:

1. Under what observed initialization/generation/cache conditions is a queried local area backed by sufficient resource-region data for the availability result to be complete and current?
2. Which concrete native inputs, intermediate resource populations and decisions lead from the local area descriptor to the resource set consumed by the UI?
3. How do prospective-beacon and, where naturally observable, established-Workshop call paths obtain and maintain their query state? Is their convergence on the same updater observable, and what must be held equal before comparing results?

Secondary question, **only if naturally observable**: Is a local area's availability evaluation observed when the player is at another position within the same loaded planetary environment, and what does that observation actually establish about player-position independence?

**Do not make remote querying, player-position independence, an arbitrary-call interface or equivalence between preview and established Workshop mandatory outcomes.** A well-qualified negative or bounded inconclusive result is acceptable. This research describes how Starfield works, rather than designing an application or a mod-specific workaround.

## 2. Existing evidence and foundations — examine before implementation

Read the current durable research, source-pinned exports, existing disposable observer implementations, previous run cards, and `WORKFLOW.md`. In particular inspect:

- Milestone A: SorNativePositionOracle 0.7.0 Kreet unplaced-beacon capture; 35,574 complete evaluations, 346 UI updates and observed A/B/C changes among Iron, Alkanes and atmospheric Helium-3. Do not treat these as proof of spatial native equivalence.
- Milestone B resource spatial predicates and B2 input provenance; the missing native region points, widths, source/resource maps and translation operands prevented independent spatial replay.
- Native availability mapping: `docs/experiments/native-availability-map/` — function register, minimum inputs, native dataflow and outstanding uncertainties.
- Resource lifecycle mapping: `region-dependencies.md`, `region-lifecycle.md`, `region-requirements.md`, `region-uncertainty.md`, associated native pins and review.
- Native function anchors (verify exact build, hashes, signatures, call edges and RVA spelling against pinned evidence, **do not blindly trust this prose**): common availability updater `Starfield.exe` RVA `0x021E07D0`; UI consumer `0x01578500`; region provider `0x0079F860`; geometry constructor `0x0079B520`; established-Workshop descriptor builder `0x00F4A140`; preview position helper `0x00B4CEE0`.
- Shared operational tooling `runtime/session-tools/` and its README, prelaunch/live/ACK/STOP/postflight/sealing/archive interfaces, and qualifications. Reuse rather than recreate.

The native updater receives initialized query state, indexed area position/context, horizontal radius and a separate upper-coordinate scalar. The latter **is not necessarily a symmetric height**. It consumes resident ProcGen maps and internally resolves atmosphere/biome contributions, with state retention across updates. The resource-region provider has cache-miss generation and lifecycle dependencies; a cached entry is not necessarily evidence that generation succeeded. The updater must not be assumed to invoke the provider or automatically generate missing resource regions.

## 3. Observation-only authority boundary

**Authorized:** offline static investigation sufficient to design a small scientific observer; build and disposable/offline-qualify native instrumentation; assemble an auditable Vortex-only deployment package and complete operator run card; produce a written assessment of whether a *future* controlled-invocation experiment would be useful.

**Not authorized in this assignment:** any direct/independent call to the native availability updater, provider, constructor or other target function; fabricated preview or Workshop evaluation; alteration of engine behavior, forced generation, prefetch, cache mutations or synthetic query-state submission; running Starfield, deploying observer DLLs, in-game testing, or changing actual saves; staging, committing or pushing repository changes. Natural calls may be observed; observers must not change the decisions being studied.

If a proposed hook risks changing native behavior or a reliable observation-only strategy cannot be qualified, stop that instrumentation strand and document the blocker. Never silently escalate into controlled invocation.

## 4. Experiment design and discriminating evidence

### 4.1 Select a minimal, justified capture surface

Before writing hooks, produce a **question → native operation → exact operands/outputs → event identity → validation** matrix. Every hook or emitted field must address a stated hypothesis. Prefer a narrowly targeted native observation over broad event flooding. Reuse qualified 0.7.0 mechanisms where compatible, while verifying they still preserve instructions, registers, stack, calling convention, memory ownership and host behavior for this build. Native RVA and version identity must be pinned. No multi-breakpoint debugger workflow.

Capture the following *where accessible safely*, with explicit fields for **not observed**, **unavailable**, and **unqualified**, rather than silently defaulting values:

- Natural caller path and invocation ancestry: preview, Workshop or other; call/evaluation identity; thread and sequencing information adequate to prevent false cross-event joins.
- Area descriptor: source reference or context (without assuming a FormID-only interface), indexed XYZ/frame/domain, radius, upper-coordinate scalar, actual coordinate translations where needed, relevant descriptor-builder outputs.
- Availability state before and after update: initialization provenance, cached spatial/atmosphere/biome collections, refresh or retention indication, resource identity outputs, and errors/failures. Distinguish a return/refresh flag from a changed resource set.
- Region provider and lifecycle, if reachable in a bounded safe capture: source keys, selection/index mapping, cache hit/miss, visited-state changes, construction attempt and early-exit categories, publication/invalidation/epoch evidence, generation and readiness markers **only when actually defined and supported by code**.
- Native spatial evaluation: candidate region identity and **both accepted and rejected** decisions; complete ordered region geometry (point positions, widths, centers/radii and transforms) and effective query operands wherever practical. If full geometry is too invasive to capture safely, record the deficiency precisely and do not claim native spatial validation.
- Relevant atmospheric and biome/water contributions, native resource IDs and eventual UI-model rows, with correlation that respects asynchronous dispatch and retained collections.

Avoid treating worker/task completion, provider return, cache insertion, cache hit or an empty list as independently sufficient proof of complete, fresh region coverage. Specify which completeness claims can actually be tested versus merely inferred.

### 4.2 Controlled observational scenarios

Prefer Kreet and the established, already evidenced A/B/C unplaced-beacon resource transitions for an initial natural-preview control (Iron + He-3; Iron + Alkanes + He-3; Iron + He-3), subject to verifying available save identities with the existing save-menu utility. The user moves the beacon normally. Exact numeric A/B/A return is **not** required, and no constructed outpost or extractor is necessary.

If an existing Workshop in an accessible loaded area can naturally trigger its established initialization or refresh path **without modifying the save** and without enlarging the scope disproportionally, add a separately labeled observational scenario. Record the *actual* preview versus established area descriptors, including differing vertical bounds, and avoid unsupported equality claims.

Player displacement in the same loaded area may be included only if it is operationally straightforward and improves interpretation. A passive observation cannot by itself demonstrate an independent native invocation contract, and lack of such an event does not prove travel is mandatory.

Codex must select the smallest meaningful scenario set after inspecting real available saves and current hooks. The run card must describe *which in-game user actions* correspond to each desired native event and when the user should signal STOP. **Do not invent a mandatory event count, capture volume, elapsed-time quota or ACK-response cutoff.** Genuine machine/instrument failures remain hard stops, and partial observations must be preserved.

### 4.3 Scientific controls and verdict categories

Predeclare comparisons and their legitimate conclusions:

- Agreement of observed native model populations with UI rows is validation of that final aggregation only, not automatically validation of candidate geometry or cache completeness.
- Independent spatial replay requires real captured region/query operands paired with actual native accept/reject outcomes, including rejections. Do not validate an implementation against its own synthetic inputs and call that native equivalence.
- Freshness claims require evidence for initialized state, relevant coverage and prior retained cache/invalidation history, or must be marked **unknown**.
- Prospective-versus-established comparison requires matching **actual native descriptors, world context and material cache state**, not merely visual proximity.
- Report **observed**, **statically established**, **inferred**, **contradicted** and **unknown** separately. The absence of a natural call cannot establish a universal runtime impossibility.

A successful Outcome A would be one or more independently controlled, native-observed relations sufficient to substantiate a particular readiness/evaluation claim. Outcome B is acceptable when a complete, reviewed, safe experiment design and available evidence establish a precise, irreducible measurement limit and what evidence would resolve it. Do not conflate merely building a DLL with obtaining a scientific finding: this brief ends at **pre-live package review**; any later live results require a separate postflight analysis and verdict.

## 5. Controlled-invocation feasibility assessment — assessment only

Deliver a short, **separate** evidence-backed recommendation concerning a possible later controlled-invocation experiment. Do not implement or run it.

For each plausible invocation boundary (for example the common updater, natural descriptor builder or region provider), address:

- What particular scientific question controlled invocation would answer that natural observation cannot;
- Exact known/unknown ABI, argument types, ownership, initialization, global/context state, thread affinity, lifecycle, side effects and cache prerequisites;
- Whether a meaningful independent oracle and failure/unknown categories could be established;
- Expected risks, smallest discriminating test, preconditions for authorization, and whether the expected gain warrants the intervention;
- Explicit recommendation **worth proposing**, **premature**, or **not useful**, with evidence.

Do not treat the existence of a function, a decompiler signature or a feasible indirect call as proof of safe standalone invocation. An honest recommendation of *not yet* is a successful result.

## 6. Packaging, deployment and safety qualification

Assemble and offline-qualify the instrumentation and run card in one integrated review package, with no premature live execution:

1. Pin target executable, SFSE, observer version, signatures, instruction bytes, DLL SHA-256 and dependency inventory; check all guarded hook surfaces for the exact binary version.
2. Ensure bounded, nonblocking, observation-only callbacks. Include thread-safe event identity, explicit event/schema versions, reliable worker health and ACK/STOP and idempotent retirement. Verify failure paths: no partial patch left applied, no unsafe dangling callbacks, and no mutation of original target results.
3. Generate disposable offline tests/fixtures for record serialization, joins, source identities, loss/overflow diagnostics, worker errors, STOP/ACK freshness, failed writer, archive integrity and other concrete hazards. Classify what these tests do **not** establish about in-game behavior.
4. Prepare a **Vortex-only** package; only the necessary DLL and actual runtime dependencies belong in the installed plugin location. Exclude research documents, run traces, raw evidence, build trees and other nonruntime files. No deployment by Codex at this stage.
5. Use shared `runtime/session-tools` for phase-aware preflight, lightweight live health checks, STOP, postflight, evidence sealing and **verified lossless ZIP archival**. Current adapter is 0.7.0-only unless extended in a narrowly justified, tested way for this observer. Do not assume the adapter will work unchanged.
6. Verify before launch and after exit (not repeatedly during player-controlled gameplay) the protected manifest, save/executable integrity and observer removal. Preserve **40 GB free on each C: and D:** where the established tool contract applies. Accept known Steam/NVIDIA overlays; pin the actual deployed DLL. Do not rerun multi-minute corpus hashing while the user stands idle in-game unless a specific integrity incident requires it.
7. Preserve original raw captures and sealed evidence. Archive must verify complete member hashes and ZIP hash; no automatic deletion, overwrite or retroactive bulk archival of previous runs. Handle partial captures and failed compression explicitly.
8. Avoid unnecessary permission prompts. After **one integrated user/ChatGPT approval** of the actual observer, package and run card, Codex may execute the approved preflight/launch workflow; the user conducts in-game actions. **That approval has not yet occurred.**

Codex may make small, justified updates to common operational adapters for the new observer, but must not create a parallel preflight/postflight harness or conduct a general infrastructure refactor.

## 7. Research process and review

Follow `WORKFLOW.md`, including its research execution/completion protocol. Use a primary agent, an independent reviewer, and optionally one relevant specialist (at most two active sub-agents). Reviewer must examine scientific discrimination, hook safety, counterexamples, provenance joins, capture completeness, data retention and whether the invocation prohibition is respected. Address substantive review findings before labeling the pre-live package accepted.

No unnecessary subagent or repeated review rounds if evidence can be settled directly. Prefer narrow, verifiable actions to a speculative rewrite of Starfield's ProcGen engine.

## 8. Required deliverables

Produce in the durable research tree, with discoverable indices and links:

1. **Experiment rationale and falsifiable hypothesis matrix**, including exactly what observational outcomes can and cannot establish.
2. **Native observation map**: pinned RVAs/VA, actual caller/callee edges, hook sites, input/output memory layouts, thread/concurrency considerations, confidence and provenance references.
3. **Observer implementation and disposable qualification tests**; event schema and loss/correlation policy; qualification evidence and limitations.
4. **Integrated Vortex installation package**: exact contents, version and hashes, no deployment; operational preflight and postflight instructions.
5. **Single clear operator run card**: save-menu-backed load selection, actions, expected UI controls, ACK/STOP and abort procedures, expected artifacts, no hard quotas, no unapproved live calls.
6. **Evidence-processing plan**: how native/ProcGen/UI event populations will be joined, checks for missing/ambiguous relations, and exact tests against existing 0.7.0 reference cases and reconstructed spatial evaluator.
7. **Controlled-invocation assessment**, explicitly separate from the approved observation-only experiment.
8. **Independent review report**, open issues, revised evidence limits, and explicit **ready/not-ready for user approval** conclusion.
9. **Review diffs**: `.local-work/diffs/<task>-task-only.diff` and `<task>-complete.diff` including untracked text, plus a review package manifest and checksums (exclude raw proprietary binary content and huge evidence).
10. Suggested conventional commit subject; do **not** stage, commit, push or sync.

Ensure documentation does not claim that a DLL's disposable qualification is equivalent to actual live observation. Future postflight findings belong to the later, separately authorized live phase.

## 9. Explicit stopping condition

Stop after delivering a fully reviewable **pre-live** research/instrumentation package. Do **not** launch Starfield, deploy via Vortex, alter saves, initiate native calls or perform the live experiment on the strength of this brief alone. Await user/ChatGPT review and explicit approval of the concrete observer and run card.

**Primary scientific principle:** establish what existing Starfield execution demonstrates; neither remote availability nor player-travel necessity is a desired outcome.
