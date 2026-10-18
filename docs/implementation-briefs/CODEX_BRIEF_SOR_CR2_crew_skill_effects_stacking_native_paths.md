# Codex research brief — CR2: Crew skill effects, eligibility, stacking and modifier application

**Project:** `starfield-outpost-research`  
**Type:** Bounded offline native/definition/save research with independent review  
**Status:** New CR2 investigation following committed CR1 and current-assignment rework  
**Authority:** Offline/read-only investigation and authored research documents/helpers only. No Starfield launch, debugger attachment or live observer, save editing, game/mod changes, plugin engineering, network acquisition, staging, commit or push. Preserve protected originals, analysis databases, existing evidence and Git state.

## 1. Research question and objective

**Which skills actually affect outpost processes when possessed by assigned crew, why do those skills qualify while others do not, and exactly how are their effects selected, applied, combined and removed?**

Produce an **explanatory reference for the existing game**, not a guide or prototype for adding/modifying perks. Map the relevant definition, actor/perk admission, assignment, native/script dispatch, contribution selection, process-specific consumer and final effective-value paths. An answer consisting only of a table of skill descriptions, perk entry points or attractive candidate effects does **not** satisfy the assignment.

For each materially distinct effect family, explain in ordinary language the full causal chain from crew possessing a skill to an outpost process actually using (or declining to use) its modifier. Distinguish displayed skill, rank, eligible contributing entry, active assigned actor, and calculated gameplay effect. Preserve competing pathways and negative findings without assuming one universal perk policy.

## 2. Prior work and evidence

Read `AGENTS.md`, `WORKFLOW.md`, `docs/EVIDENCE_STANDARD.md`, `docs/RESEARCH_EXECUTION_PROTOCOL.md`, `docs/templates/completion-contract.md`, CR1's `docs/experiments/crew/` findings (especially `report.md`, `screen.md`, `current-assignments.md` and their reviews), E1 stacking/production contracts (`docs/experiments/inorganic-extractors/stacking-report.md`, `stacking-native.md`, `stacking-matrix.md`, arithmetic), E2/E3 production, P1 power, S1 capacity, S2 local logistics and C2/C3 cargo timing/fuel evidence. Verify existing pin paths, game build, hashes, native image base and actual data before reuse; reuse established readers and source-permission grants rather than rebuilding an engine framework.

In particular, E1's scoped result indicates that **distinct assigned actor timer contributions can multiply**, rank changes replace the corresponding rank entry, and player contributions compose later. Do not re-prove those findings for their established paths; determine their applicability and exceptions for CR2's broader crew/perk population and other effect mechanisms.

## 3. A — Crew population and complete observed skill census

Identify the practical recruitable crew population represented in installed definitions: named companions/recruits, named hirelings and ordinary generic specialist archetypes (including inheritance, template/perk/script grants and rank variants). Record which skills/ranks are positively established at definition level, which are granted conditionally, which can be changed at runtime, and which remain unknown for particular historical actors. Do not assume all named NPC perks are crew-visible; reproduce the Crew screen's actual crew-flag admission as a separate field. Do not infer actual possessed rank from a base NPC template when runtime grants can differ.

Provide a searchable table of **every distinct skill found in the qualifying crew population**: skill/perk identity, known ranks, representative crew, UI-display eligibility, native/PEX/record effect mechanism, applicable context (outpost / ship / individual / player-only / none demonstrated), and evidence. Explicitly test **Payloads, Aneutronic Fusion, Geology, Pistols, Outpost Engineering and Outpost Management**. A skill with no outpost-wide effect is a valid result **only after tracing the positive effect definitions and relevant context/consumer gates sufficiently to justify that negative scope**. Keep ship-system effects only to the extent required to distinguish them from outpost effects; no full ship perk audit.

## 4. B — Why a perk does or does not affect an outpost

Identify the **admission and applicability machinery**, not just skill names. For each relevant effect family, trace and distinguish:

- Perk definitions, ranks, entry point(s), operations, conditions, actor-value or keyword selectors, owner/target/context predicates, and scripts where used.
- How crew ownership and outpost assignment are found: registered crew lists/ExtraE2, `CrewAssignment` links, actor handles, eligibility/status and any effective perk application records.
- The exact consumer on the outpost side: how it supplies actor, Workshop, facility, resource, ship or inventory context; where applicable ranks are selected; where evaluation is rejected; what field/value is actually changed.
- Whether a skill's mere presence, its Crew screen flag, or assignment to an outpost is *insufficient* absent another gate. Classify UI-only, actor-local, ship-only, outpost-wide, producer-specific and mixed effects.
- Whether the relevant operation is a direct formula at use time, a cached AV modification, a registered contributor, an event-driven refresh, or a persistent change of object state.

Deliver at least one **instruction/record-backed end-to-end example** of an outpost-affecting crew perk and one contrasting crew skill without an outpost contribution, with exact locus of the decisive difference. Where multiple mechanisms exist, supply an example per consequential family. Do not divert into hypothetical plugin APIs, new skill registration design, or Creation Kit tutorials.

## 5. C — Stacking, rank precedence and player interaction

Trace the actual aggregation path for each outpost-relevant effect family, separating: different actors with the same skill, different ranks of one skill, multiple distinct skills, player-owned perks, duplicate grants and reassignment/removal. Establish which mechanisms multiply, add, maximize, replace, override, or apply per actor/facility. Resolve ordering only where it changes outputs. Give concrete **worked numeric or symbolic examples** for two crew members with overlapping entries and for crew plus player bonuses, using installed effect definitions and exact operations—not assumed percentages.

Avoid equating selected rank with summed lower ranks. Explain whether and how the game removes old entries and updates effective values when actors, ranks or destinations change. If a mechanism is dynamic per call, say so rather than inventing a cache. Distinguish a mathematically calculated modifier from a measured historical running-outpost output.

## 6. D — Process-specific impact, including unintended effects

Use the already-mapped consumers to check crew contribution to the following, recording supported positives and bounded negatives:

| Process | Required investigation |
|---|---|
| Inorganic extraction | Effective production interval/rate, gates, current producer eligibility |
| Organic production | Greenhouse/husbandry timing and product/input differences |
| Fabricators | Production interval and recipe/input/output stages |
| Inter-system cargo fuel marker | Whether crew effects can shorten the **5 He-3 / base 108-s** fuel cycle; actual applicability and rank conditions rather than generic shared-scheduler speculation |
| Outpost power | Whether skills such as Aneutronic Fusion actually change generator or reactor output, or have a ship-only consumer |
| Dedicated storage and cargo holds | Whether Payloads alters outpost container capacity, cargo-ship capacity or only ship inventory capacity; distinguish actors/perk contexts |
| Cargo schedule and local logistics | Any actual crew effect on timers, freight quantity or movement; don't infer from a generic production label |
| Defenses / combat | Whether combat skills affect turrets, outpost-wide combat, or only the NPC's own actor; defer comprehensive turret/attack mechanics |

Where an effect has multiple possible targets, identify the exact context required by the native consumer. Preserve ordinary vs exceptional or modded-state limits. No blanket claim that every A1 producer receives every producer-type perk.

## 7. E — Assignment-to-effect lifecycle and save/runtime correspondence

Trace the sequence from initial assignment, rank grant or change, transfer, unassignment and dismissal to **actual modifier availability**. Distinguish assignment-list mutation, event/queue dispatch, contributor registration/removal, next modifier evaluation, and first observable production consequence. Determine whether a delay is required by native ordering or merely possible from asynchronous work. Do not conflate actor travel/arrival with effect activation; CR3 retains physical presence and remote residency as its primary topic.

Examine actual saved skill/perk/assignment/actor references in a **purposefully selected** corpus; take CR1's lesson seriously. Begin with earlier mature positive-assignment witnesses such as HIST-0255/Save41 and HIST-0021/22/24, then widen according to required perk overlap, rank and control states. Save52 may be a comparison but **must not be the default negative oracle**. Positively decode saved ranks/identities where supported; mark missing/unsupported fields `UNKNOWN`, not zero/unassigned. Connect native serialization/restoration to runtime effect registration and identify whether effective modifier values themselves persist or are rebuilt. A derived hypothetical numeric example must not be represented as a directly observed save value.

Do not commission a controlled live save pair merely because historical examples are inconvenient. Where a decisive witness is absent, first use installed definitions and native causality, search the existing qualified corpus purposefully and state the precise remaining gap. A future live experiment, if genuinely needed for an application-relevant contradiction, is a **proposal requiring new authorization**, not part of this task.

## 8. Output and acceptance contract (freeze before execution)

**Task type:** Bounded offline semantic/native/save investigation and documentation, not production engineering.

**Mandatory acceptance criteria — all eight:**

1. **Answer-first report:** Plain-English findings explaining *why* some crew skills affect outposts and others do not; distinguish displayed rank, contributed rank and effective outcome, with concrete coverage and evidence confidence.
2. **Crew/perk catalogue:** Qualified named/generic population and every distinct identified skill, conditional grants, role/context classification, and explicit Payloads/Aneutronic Fusion/Geology/Pistols cases; unknowns and exclusions disclosed.
3. **Causal admission map:** Exact definition-to-consumer paths for relevant effect families, including selectors/gates and at least one outpost-positive and one properly bounded outpost-negative example. Mere entry-point listings fail.
4. **Stacking/precedence:** Per-mechanism combination and rank semantics, player interactions, duplicate contributor/reassignment effects and reproducible worked examples; retain E1's accepted narrower result without contradiction.
5. **Actual outpost impact:** Process matrix covering extraction, organic, fabricators, power, storage/cargo capacity, local/cargo timing, fuel marker and bounded defense implications. Every consequential positive/negative cites relevant consumers.
6. **Assignment and persistence:** Effect-registration/refresh/removal sequencing and supported save-to-runtime perk/rank/assignment joins using intentionally chosen positive and negative corpus examples; no invented complete loaded census.
7. **Durable evidence and integrity:** Report plus focused tables, source/function/provenance evidence, supported tests, status notes and CR3 boundaries; frozen criteria, failed attempts and corrective actions preserved. No new live/tooling, protected-input, Git or third-party-permission violations. Apply established both-drive free-space and evidence safeguards.
8. **Independent review and package:** Per-criterion PASS/FAIL/NOT TESTED with scientific confidence, semantic coverage and application readiness separately stated; independent reviewer inspects primary evidence and corrections; verified task-only and complete diffs, changed/untracked text inventories, exclusions, hashes, exact forward/reverse reconstruction and local review/manifest receipts per `WORKFLOW.md`. No commit or push.

**Optional:** Additional crew variants, advanced ship comparisons and modded load-order effects only if discovered economically within the established scope. No new skill/mod/observer development.

**Negative-result closure:** A bounded negative is acceptable when definition effects, dispatch gates and the relevant native consumers exclude an outpost contribution within explicitly declared context. An untested skill, absent save witness or missing search hit alone is not negative proof. Evaluate the strongest evidenced explanation at reasonable engineering confidence; hypothetical undiscovered paths do not receive equal weight without concrete evidence. Do not demand exhaustive engine-global absence proof.

**Continuation authority:** Diagnose, correct, expand relevant native/definition searches, rerun tests and repair reviewer issues within these eight frozen criteria under this brief; retain evidence and earlier failures. Do not stop merely because an initial witness/sample is unhelpful.

**Escalation:** Stop only the affected operation for a genuine protected-input/integrity/permission/safety/resource dependency, or indispensable live-only evidence. State the exact missing input, attempted bounded alternatives and a narrow separately approvable next action. No open-ended scope creep or unconditional observer recommendation.

**Completion means:** The existing crew-perk system is understandable end-to-end across its materially distinct outpost effect mechanisms, with usable rules and limits. `COMPLETE` is a bounded assignment judgment, not a claim every conceivable crew state was observed live. Retain CR3 for remote actor presence, load/arrival/death behavior and full post-load modifier coherence.
