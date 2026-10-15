# Codex Research Brief — SOR: Resource-Region Generation, Native Dependencies, and Minimum Runtime Requirements

**Repository:** `D:\Projects\starfield-outpost-research` (`gooberpede/starfield-outpost-research`)  
**Assignment type:** Offline native-code research, evidence synthesis, and documentation  
**Authorization:** Research and bounded offline tests only. **Do not** launch Starfield, operate the game/debugger against a live process, construct or deploy an observer, modify saves, stage, commit, or push.  
**Status:** Implementation/research brief for Codex; requires subsequent user/ChatGPT review.

## 1. Purpose and governing question

Establish, as precisely as existing evidence permits, **what information and native runtime state Starfield requires to determine the inorganic resources available within a specified area on a planetary surface**, especially when the queried area is not where the player character currently stands.

This is a question about **how Starfield works**, not a challenge to demonstrate remote querying. An evidence-supported finding that resource availability can only be evaluated after the player travels to and loads the location is a legitimate complete finding. So is an evidence-supported finding that the engine can prepare and evaluate a separate planetary context without player travel. If evidence establishes neither, report the precise unresolved boundary rather than asserting either outcome.

Do not orient the research toward hypothetical mods, prescribe future mod features, perform modder-specific gap analysis, or devise workarounds to defeat native prerequisites. The native functionality, dependencies, and evidence are the research objects.

## 2. Starting evidence and current boundaries

Read the project's current `WORKFLOW.md`, native-availability mapping documents, Milestone B findings, relevant static native exports, and provenance/validation registers before expanding analysis. Treat repository findings as version-specific unless independently demonstrated otherwise.

Established research includes:

- The common availability updater at **Starfield.exe RVA `0x021E07D0`** (pinned researched executable, reported version **1.16.244.0**). At its call boundary it receives an initialized query-state object, an indexed position descriptor (XYZ, frame index, domain/reference context), a horizontal radius, and a distinct upper-coordinate scalar. It consumes available loaded ProcGen resource maps and maintains cached collections. Do **not** describe that scalar generically as a symmetric height.
- Prospective-beacon preview and established-Workshop paths statically converge on that updater, but **established-versus-preview runtime equality has not been independently established**. Preview position helper: RVA `0x00B4CEE0`; established Workshop area-descriptor builder: RVA `0x00F4A140`.
- Resource-region provider/cache path **RVA `0x0079F860`** and identified construction path **RVA `0x0079B520`** are the initial research leads. Their full caller graph, context ownership, and cache-miss prerequisites have not yet been established. **Do not assume the common updater itself calls the provider**; the mapped updater consumes existing ProcGen maps.
- Milestone B recovered spatial predicates and an offline evaluator for qualified supplied region geometry, but original 0.7.0 captures lack the complete region maps, ordered points/widths, translation operands, and independent native accept/reject decisions needed to validate spatial equivalence.
- The 0.7.0 evidence includes **35,574 completed evaluations**, **11,128 distinct indexed descriptors**, and **346/346 validated UI resource-set folds**; these validate captured aggregation, **not** full upstream geometry or remote-query sufficiency.
- Atmosphere contributions, biome-specific water additions, stateful cache retention, X-Tech exceptional behavior, and generation completeness must be explicitly delimited. Do not collapse them into generic spatial-region logic.
- Prior saved-location, beacon positioning, and Workshop membership research may ground identities/coordinates, but saved extractor lists are **not** a complete measure of available resources.

Confirm these identities against the local pinned evidence; correct any discrepancy with citations to native offsets and clear provenance, not conjecture.

## 3. Research questions — pursue the dependency chain

### A. Resource-region provider and generation lifecycle

1. Trace callers and callees of `0x0079F860` and `0x0079B520` through cache lookup, miss, generation, insertion, invalidation, and any background/async scheduling paths. Distinguish a routine that **requests** generation from one that **guarantees completed, usable** geometry.
2. Identify the concrete source of each required operand: world/body, landed area or cell, source-map selection, ProcGen context, biome/resource definitions, RNG/seed where supported, region descriptor, coordinate frames/translations, and cache owner.
3. Describe which objects own resource/source maps, when those objects are populated, and what native lifecycle events create, refresh, discard, or replace them. Trace enough upstream callers to understand why the availability updater can read those maps.
4. Note whether retrieval is per-world, per-landing-area, per-cell, or otherwise scoped; do not infer scope from a field name alone.

### B. Minimum inputs and state for resource availability

Separate **(i) explicit function arguments**, **(ii) indirectly resolved native inputs**, **(iii) required initialized state**, **(iv) lifecycle or freshness conditions**, and **(v) evidence of sufficiency**.

For each investigated boundary (provider, generation path, loaded-map consumption, common availability updater, and established/preview area setup), ask:

- What is required to form a query for a specified indexed center and radius? What role does the upper-coordinate scalar play?
- Which prerequisites are fixed by world identity, coordinate context, terrain generation, loaded cells, existing reference/Workshop state, cached geometry, or prior query history?
- Can the query execute with **loaded geometry but no player presence**? With a **separately initialized planetary context**? With **persistent save/world data alone**? Which cases are demonstrated, statically plausible, contradicted, or unknown?
- Is the **player's presence** required by code or merely correlated with normal terrain loading? Explicitly distinguish presence, active world, loaded terrain, resident ProcGen maps, region-generation completion, and availability-cache freshness.
- What does an empty result mean relative to an unavailable, incomplete, stale, or retained result? Identify initialization/refresh semantics and failure handling.

Do not assume an address and apparent calling convention constitute a safe standalone callable contract. Conversely, do not infer that no alternative entry point exists merely because one has not yet been mapped.

### C. Native function relationships

Extend the existing native function register **in place**, recording substantive newly identified functions and improving current entries where supported. For each material function include: executable version and VA/RVA; descriptive label versus proven symbol; caller/callee evidence; inputs and object/layout provenance; outputs and mutated state; caches and ownership; preconditions/lifetime/thread requirements where established; observed or inferred side effects; evidence locations; validation status; uncertainties.

Maintain a readable call/dataflow map tying **provider → resource-map construction/population → availability consumption**, including branches for atmosphere and biome water contributions when relevant. Clearly mark indirect or hypothesized edges; do not draw speculative edges as observed calls.

## 4. Evidence, tests, and research standard

1. Start with **existing offline materials** and pinned native exports. Reuse existing disassembly analysis, resource-map findings, frozen evidence, and existing deterministic test harnesses; avoid broad rescans or rebuilding solved infrastructure.
2. Use instruction- and dataflow-backed claims with specific native evidence: VA/RVA, function block, calling site, field offsets, relevant predicates, version pin, and provenance. Distinguish direct instruction observations, reasoned inference, runtime observation, and open hypotheses.
3. Where justified, add **small deterministic offline probes/tests** for decoded layouts, cache-state logic, or call/dataflow assertions. Do not implement new ProcGen or resource-generation machinery merely to manufacture a success case; do not use synthetic tests as proof of native runtime equivalence.
4. Do not infer independent agreement from repeated events, self-derived inputs, or the 346 UI folds where the question concerns upstream generation, region geometry, or lifecycle.
5. Follow concrete in-scope leads to a defensible boundary rather than stopping at the first missing operand. An **Outcome B/evidence-bound** conclusion requires detailed proof of what was traced, what cannot be established with current evidence, and what exact missing evidence would discriminate alternatives.
6. Preserve all existing research evidence, saves, installed binaries, native exports, frozen predictions, and protected hashes. No hidden modification of evidence artifacts.

## 5. Outcomes and acceptance criteria

The assignment has **no preferred outcome about remote feasibility**.

- **Outcome A — Supported minimum-requirements account:** Grounded evidence identifies the minimum native input/state and lifecycle conditions sufficient for local and/or nonlocal determination, with clearly delineated scope and validation level. It may establish player travel/load as a requirement or establish independence from player presence. Do not claim runtime sufficiency from static tracing alone.
- **Outcome B — Completed evidence-bound account:** Native dependencies and known contracts are mapped as deeply as current offline evidence allows, with an explicit account of what is necessary, what is sufficient, what is merely normal game behavior, and what remains unproven. Any proposed further experiment must name the exact missing operand/state or competing hypotheses, what the experiment would discriminate, and why archived evidence cannot answer it. No experiment is authorized by this assignment.

Both require a coherent, neutral technical reference; function maps and provenance; and a reviewer-supported completion assessment. Do not treat inability to demonstrate remote querying as failure, and do not overstate a requirement that travel is necessary without evidence.

## 6. Deliverables

Create or extend documentation within the project's established research-document organization; follow existing naming and workflow conventions instead of inventing a parallel structure. Expected durable artifacts:

1. **Technical report:** methods, traced native behavior, evidence, positive and negative findings, qualified conclusions, and scope/build constraints.
2. **Provider/generation lifecycle map:** specific producer/provider/consumer native functions, cache miss and hit paths, state ownership, creation/completion/invalidation paths, and clearly qualified open edges.
3. **Minimum-requirements matrix:** explicit arguments versus implicit state, separate rows for prospective preview, established Workshop, arbitrary location in the loaded area, separate terrain/world context, and unloaded remote area. Mark each as *demonstrated / statically supported / hypothesis / unknown / contradicted* with citations and avoid equating player presence with data residency.
4. **Updated existing native function register and dataflow documentation**, with cross-references to prior Milestone B and native mapping work.
5. **Evidence/uncertainty register:** sharply formulated unknowns and, only if necessary, discriminating future observations for later user approval.
6. **Offline test and preservation receipts**, including clear coverage limitations.
7. **Review package:** changed-file inventory, evidence locations, qualification notes, results, reviewer findings/rework, and ready-to-inspect task-only and complete diffs under `.local-work/diffs/`; ensure complete diff includes newly added untracked text files as appropriate and does not include private raw traces, binaries, saves or large evidence.

Summarize conclusions concisely in the Codex final response, pointing to the report, review package, and diffs. Provide a suggested Conventional Commit subject; do not stage, commit or push.

## 7. Execution discipline and review

- Consult and follow `WORKFLOW.md` and the repository's research-execution/completion protocol.
- One primary agent; independent reviewer **required** for substantive scientific claims. One specialist researcher may be used where beneficial. **No more than two active sub-agents at once.** Resolve reviewer objections and provide the final reviewer disposition; do not claim acceptance merely because tests pass.
- Prefer existing research paths and established verification workflows. Maintain source/version traceability and clean boundaries between static and runtime support.
- This is **strictly offline**: no Starfield launch, live attach, observer/DLL/hook development, Vortex installation, live terrain activation, mutable save access, staging/commit/push, or historical evidence archival/deletion. If live validation would help, document a targeted proposal for separate authorization rather than doing it.
- Do not expand into the Outpost Tracker/Planner, external modder requirements, hypothetical API designs, general terrain-generation reconstruction, or speculative non-native bypasses.

## 8. Final research question

**For a specified planetary area, which native Starfield functions and states supply the resource-region data consumed by inorganic resource availability, and what is the smallest *evidence-supported* set of inputs and runtime conditions under which that determination is valid?**

A precise, well-supported limit is a satisfactory result. Do not optimize for proving that remote evaluation works.
