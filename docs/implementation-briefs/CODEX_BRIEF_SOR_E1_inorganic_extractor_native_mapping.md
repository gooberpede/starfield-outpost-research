# Codex Research Brief — SOR E1: Inorganic Extractors, Native Contracts and Operating State

**Assignment type:** Offline native-code and save-evidence research; documentation and narrowly justified offline verification only.  
**Repository:** `starfield-outpost-research` (use existing repository workflow and conventions).  
**Decision authority:** User reviews the complete diff before staging, committing or syncing.  
**Scope:** E1 inorganic extractors only. Organic greenhouse and animal-husbandry systems are reserved for E2.

## 1. Purpose and research standard

Map Starfield's existing machinery sufficiently that a technically capable researcher can locate and understand how inorganic extractors are identified, classified, associated with a resource, powered/activated/operated, linked for output, and scheduled for production. This is a **neutral native technical reference**, not an extractor-management tool, implementation recipe, complete simulator, or request to duplicate the engine's functionality.

The aim is to reach the same kind of **conditionally complete, useful native-function mapping** achieved in the prior resource-availability work. Record actual native addresses, data layouts, call relationships, state provenance and limits of evidence. Do not pursue comprehensive reverse engineering merely to resolve incidental unknowns. Distinguish native behavior demonstrated at runtime, static disassembly inferences, save-derived findings, and hypotheses.

Use the pinned build and identities established in repository records; do not assume RVAs or structures are stable across builds. Reuse the existing native function register, provenance references, save-analysis tools and existing evidence. Avoid parallel, incompatible documentation or speculative names presented as verified symbols.

## 2. Required questions and completion contract

For each identifiable **inorganic extractor** or relevant family of extractor definitions, establish the best supported native path for determining:

| Requirement | Required result |
| --- | --- |
| Identity and inventory | How individual installed extractors are enumerated and associated with their Workshop, where such membership can be established; how references and base definitions are identified. |
| Type and size | Native classification of ordinary solid, liquid and gas extractors; model/type, size or tier and exceptional variants (including X-Tech if distinct). Do not rely exclusively on EditorID naming heuristics. |
| Resource association | Which inorganic resource a given extractor is assigned to extract; distinction between resource definitions, cached/generated deposit geometry, and persistent association. |
| Current power state | Native *current* powered/unpowered status, rather than whether a power network could theoretically supply it. Identify the output contract or native state; distinguish inferred state if direct status is unavailable. |
| Current activation state | Whether extractor activation/deactivation is represented separately from power and how to retrieve that state, if established. Do not presume the distinction exists. |
| Current operating state | Native operational/production status and how it relates to power and activation, if distinct. |
| Output links | Existing **outgoing** links and their actual target references/destinations, not merely a Boolean “linked” status; distinguish durable/save data from runtime link state. |
| Production rate and quantity | How per-cycle output quantity, cycle frequency/timing, and effective modifiers or conditions are determined. Where a value is dynamic, identify the producer/consumer functions and minimum state needed to observe or derive it; do not fabricate a general formula when native evidence is insufficient. |

**Out of scope:** extractor stored inventory or item counts; aggregate outpost power generation, network sufficiency or topology; tracing switch placement, configuration, on/off logic or distribution; cargo-network modeling; remote operation; writing an extractor; in-game instrumentation or runtime test; general ore-vein generation; greenhouse and husbandry systems except necessary classification boundaries.

Power-switch effects may be mentioned as an external dependency. Do **not** investigate switch state or power-flow logic: document only the extractor's present observed/native state and any directly encountered external calls.

For production calculations, distinguish native base definitions from realized/effective behavior, and note conditions such as power, activation, temporal scheduling or skills **only when supported by evidence**. Do not attempt a complete economic or timing simulation.

## 3. Research sequence

### E1-A. Inventory and identity

Start with the existing saved extractor inventory and known Workshop membership analysis, including Save52 and any more directly relevant already-qualified samples. Identify which representations are ordinary extractors versus variant equipment, builder/fabricator machines, and organic facilities; mark uncertain cases. Extend extraction scripts only where indispensable and protect original saves. Establish the bridge from saved reference/base/resource association to the relevant runtime native objects, where static evidence permits.

### E1-B. Trace native states and output links

Trace native functions and data structures that maintain or expose current power, enabled/activated, operational status and outgoing links. Specifically test whether these are separate fields/states, computed results, or aliases/derived views. Record whether each can be known from a save, a live object, or only from runtime evaluation; **do not confuse persisted flags with confirmed current runtime status**.

For links, document source and destination reference identities, directionality, relevant link keywords/types and lifecycle if supported. Avoid silently treating any connection as an output link.

### E1-C. Trace production

Identify the native scheduling, tick/update or event and resource-production functions, resource selection/association, base and effective quantity, production interval and relevant modifiers. Identify what can be read directly versus reconstructed from definitions, and record any unresolved causal dependencies. Separate production of new units from storage/transfer of already produced units.

### E1-D. Opportunistic D1 cross-checks

Read and cite the durable disappearing-deposit reconnaissance, preserving stable **D1-H1 through D1-H4** hypothesis identifiers, original predictions, falsifiers, and their scoped dispositions. Where E1 naturally discovers decisive native evidence about extractor placement versus continuing operation, persistent resource association, geometry consultation or stale state, apply existing falsifiers and append evidence and updated *scoped* dispositions. **Do not** rewrite original predictions to fit findings, require bug reproduction, or enlarge E1 into a separate bug investigation. If no new discriminating evidence appears, leave hypotheses open and say so.

Additionally preserve the user's historical context: Decaran II Helium-3 production was established after Decaran VII-b could no longer supply Helium-3. This is eyewitness chronology, not proof of an incident timestamp or save-state mismatch.

## 4. Native technical reference and evidence standards

Add findings to the existing native function registry and documentary architecture. For relevant native functions, include pinned executable version, VA/RVA, inferred or verified role, callers/callees, argument and output representations, object offsets/layouts, state ownership, lifecycle and conditions, side effects, confidence level and precise evidence pointers. Avoid naming an unidentified function as an established public API.

Document a navigable conceptual dataflow: **installed extractor reference → base/type/resource association → current states → output links → production cycle and effective output**. This is descriptive, not a prescription for external developers.

For each question in §2, distinguish:
- **Mapped:** specific native contract and supporting evidence.
- **Qualified inference:** plausible semantics with exact limits.
- **Unresolved:** missing contract, missing runtime observation, or evidence not present.

A static finding can satisfy the research endpoint if the contract is adequately grounded; don't demand a live experiment simply to fill every validation gap. Conversely, do not promote synthetic tests or historic save relationships to proof of actual current operating state.

Use falsifiable hypotheses to guide unresolved *research-relevant* mechanisms; a negative result is valuable when its tested scope is explicit. No open-ended investigation or invented requirement to reproduce the system independently.

## 5. Completion and stopping rule

Return one of:

- **COMPLETE:** Native functions, structures and relationships sufficiently mapped for each agreed E1 capability, with appropriately supported confidence.
- **CONDITIONALLY COMPLETE:** A substantive usable map covering the E1 capabilities, with explicit limitations where direct/current status or effective rates are not yet established.
- **INCOMPLETE / evidence-bounded:** Name each consequential missing contract preventing the agreed endpoint and specify the smallest achievable further evidence that could settle it. Do not merely list unrelated unknowns.

If further investigation is not meaningfully likely to settle an in-scope question within the authorized offline evidence, stop and document the boundary. **No live observer or experiment should be developed, and none should be requested merely because an uncertain fact exists.** If an additional experiment is genuinely necessary, only propose it with a falsifiable comparison and concrete payoff for separate approval.

Do not silently reclassify an unfinished agreed requirement as optional; distinguish not established from does not exist.

## 6. Scope control and workflow

- **Offline only.** No Starfield launch, debugger attachment to a live game, plugin/DLL instrumentation, Vortex deployment, save modification, or native invocation within Starfield.
- Do not reopen the completed native availability mapping, the Experiment A spatial-equivalence NO-GO, or the discontinued 0.8.0 observer except as reference evidence.
- No changes to protected historical captures, frozen predictions, executable/Ghidra inputs, native binary evidence or original saves.
- Follow the repository's current `WORKFLOW.md` / `AGENTS.md` research execution and independent-review protocol. One primary agent; optional focused specialist and mandatory independent reviewer as permitted by existing project policy (maximum two active sub-agents concurrently).
- Make the independent reviewer challenge classification, power-versus-activation semantics, link direction, production-rate claims, completion classification and any unsupported inference from saved data.
- Conduct a **task-wide prose-quality audit** for fused words, missing spaces around numeric tokens/RVAs/versions and unreadable automatically generated text. Fix issues before packaging. Do not reformat historical unrelated documents.
- Verify preservation, relevant tests and documentary links. Record exactly what was run and what was *not* independently verified.
- Do not stage, commit or push. Provide suggested Conventional Commit subject only after the work is reviewed.

## 7. Deliverables

1. A readable E1 technical report answering each requirement in §2, with a compact status/evidence matrix and clear scope boundaries.
2. Updated native-function register and supporting code/dataflow diagrams or layouts, integrated with the current documentation structure.
3. Reproducible offline evidence inventory: native export pins, saved-extractor examples, qualification checks and any narrowly justified scripts/tests.
4. An explicitly separate short section on D1 hypotheses: newly tested, unchanged or deferred, with evidence and no overclaiming.
5. Independent review record, remediation history, preservation and test receipts, plus prose-audit results.
6. **Task-only and complete diffs** (including newly created textual files), output manifest and relevant hashes, with locations clearly stated. Do not bundle private raw evidence or executable binaries into review diffs.
7. Final completion classification and suggested Conventional Commit message. Summarize any important evidence-bound follow-up question, but do not automatically create a new research mandate.

**Backlog note (not part of E1):** Determine whether native runtime and/or save information can establish outpost creation/deletion ordering, including deleted outposts; exact, relative and partially bounded chronology should be distinguished. Do not restrict this question to save parsing or pursue it under E1.

**Scientific emphasis:** Learn which functionality Starfield already possesses, how it is represented and reached, and where our evidence ends. E1 succeeds by producing a useful native reference, not by implementing extractor management or exhaustively describing every related system.
