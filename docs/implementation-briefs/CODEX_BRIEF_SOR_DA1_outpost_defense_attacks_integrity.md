# Codex research brief — DA1: Outpost defense, attacks, Integrity, damage and repair

**Project:** `starfield-outpost-research`  
**Type:** Single bounded offline research assignment; native/script/definition/save correspondence and independent review  
**Proposed file in repository:** `docs/implementation-briefs/CODEX_BRIEF_SOR_DA1_outpost_defense_attacks_integrity.md`  
**Authority:** Read-only investigation and authored research documentation/checking only. No game launch, gameplay, live observation, new instrumentation or deployment, save modification, original binary/database changes, staging, commit or push. Local ignored scratch and text evidence helpers are allowed under project policy.

## 1. Objective and agreed boundary

Explain **when and why an outpost is attacked, whether its defenses affect attack initiation or resolution, and what attacks can do to constructed outpost objects**. Investigate turrets **as possible defensive modifiers and damageable Workshop objects**, not their combat AI or combat effectiveness. This combines the previously separate turret and attack topics into **DA1**; do not reuse `D1`, already assigned to disappearing deposits.

The user reports ordinary attacks near a visited outpost, perhaps while exploring the surrounding terrain, but does not recall remote attacks while off-world. This is a hypothesis, **not an accepted negative finding**. The user separately reports occasional hostile Starborn encounters associated with an outpost Armillary, possible defensive relevance of watchtowers, and attacker interest in objects with an **Integrity** bar. A prior Kreet extractor screenshot shows a full Integrity bar; it does **not** prove that the object has experienced attack damage. Respect these observation/evidence boundaries.

An outpost encounter, Armillary-associated Starborn attack, and incidental hostile NPCs entering the area may be different mechanisms. Trace each and document any actual convergence; do not collapse them based on proximity alone. Likewise, a turret or watchtower's physical utility in combat is not proof of an abstract *Defense* score or attack-probability modifier.

Read `AGENTS.md`, `WORKFLOW.md`, `docs/EVIDENCE_STANDARD.md`, `docs/RESEARCH_EXECUTION_PROTOCOL.md`, `docs/templates/completion-contract.md`, and the relevant P1, E1–E3, S1/S2, CR1–CR3, R1, L1–L3 reports/registries before beginning. Reuse previous native locations, script members, Workshop membership and saved-instance evidence, checking actual version/hash/provenance. Do not repeat resolved turret quotas (L1), power (P1), crew/robot skill rules, or generic damage/combat mechanics without a concrete DA1 dependency. Fallout 4 may supply search leads, but explain **Starfield** on its own terms.

## 2. Mandatory questions and research paths

### A. Ordinary attack initiation, eligibility and scheduling

- Identify actual ordinary outpost-attack quest/event/script/native initiation paths, including RNG, probability, cooldown/timer, progression, encounter and faction inputs **where they exist**. Trace producers and consumers; a quest/editor ID or script name alone is insufficient.
- Distinguish ordinary outpost-targeted attacks from roaming/prespawned hostiles and generic encounters. Establish what identifies an outpost as a target and how a chosen event reaches actual spawning/hostile activity.
- Identify whether attacks depend on player distance, active cells, encounter/3D residency, player worldspace, or the existence of a resolvable outpost; distinguish initiation from ongoing attacks, post-unload continuation and reload restoration. Evaluate specifically: player at outpost, elsewhere in same traversable terrain, and off-world. Do **not** infer off-world absence merely because no timer was found.
- Characterize any elapsed-time, waiting/travel, cooldown and rearm rules with actual clock/timebase where supported. If there is no general attack scheduler in the bounded mapped system, provide a defensible scoped negative with a trace of the relevant candidate entry points and alternatives examined.

### B. Armillary/Starborn branch

- Investigate construction/activation/placement state, relevant quest progression, any special Starborn encounter path, and its location/proximity/cooldown requirements.
- Determine whether an Armillary at an outpost changes the ordinary attack system or participates in an independent attack mechanism. Investigate removal, relocation and reload state only to the degree it affects eligibility.
- Preserve uncertainty where Armillary-associated attacks have no positive matching native/script mechanism; do not infer a rate or universal trigger from testimony.

### C. Defense contributors and turrets

- Establish whether there is an outpost defense rating, actor value, calculated statistic or equivalent, **and whether the actual attack-selection or resolution path consumes it**. Trace reads as well as writes; absence of a named “Defense” AV is not an absence proof.
- Examine the installed turret types and their Workshop ownership/persistence sufficiently to resolve L1's **historical turret owner-join gap** where the relevant save representations support it. No need to re-explain their shared numerical limit or power requirements.
- Check watchtower, other defensive constructions, powered/unpowered turrets, security robots and assigned human crew for genuine defense contributions or encounter effects. Distinguish definition tags, construction categories, AI cover positions and combat participation from native numerical modifiers.
- Follow attack-specific selection of damageable Workshop targets only far enough to determine whether attackers preferentially target Integrity-bearing objects. No general turret/NPC AI, target tactical decisions, weapon damage, accuracy, pathfinding or combat balance investigation.

### D. Integrity, operational consequences, repair and persistence

- Catalogue representative ordinary damageable constructed objects (extractor, generator, storage, cargo pad, turret and pertinent exceptions). Identify the source of maximum/current Integrity; trace the Build-mode indicator's data provider and actual calculation. Do not assume it is simply actor Health without evidence.
- Trace how native/script damage is admitted, applied, persisted and restored; distinguish damaged, nonoperational/disabled, destroyed and deleted states. Identify threshold consequences for production, power and connected logistics by reusing existing E/P/S mechanisms.
- Trace repair entry points, eligibility/material or cost checks if relevant, health restoration and whether the same construction reference persists. Determine how repair/removal interacts with L1 numerical limits and L2 budget where warranted.
- Look for saved damaged/repair-positive witnesses in a **purpose-selected** mature-save corpus; sample selection is evidence-driven rather than restricted to Save52. Missing suitable damage in a save is not evidence that Integrity cannot persist. Saved data need not contain an attack history or a defense-rating field to establish the native model.

## 3. Evidence method and reporting standard

Use the pinned retail executable, installed main-game definitions, shipped PEX (validated against source where available), existing native read-only exports, and appropriately selected protected historical saves. Build a source/function/definition register with exact paths, IDs, addresses, instructions and relevant operands; distinguish source-reported script behaviour from compiled and native execution. Existing helpers may be adapted as **research-only** tools; do not develop a production attack simulator, turret AI mod or arbitrary save importer.

The report must begin with a succinct plain-language **answer-first matrix**: ordinary attack cause/frequency, player proximity and off-world behavior, Armillary branch, defense modifiers, Integrity/damage, repair, and what is saved. Use `PROVEN`, `STRONG`, `PROVISIONAL`, or `OPEN` as specified by project evidence policy, with static/save/runtime bases and coverage kept separate. Provide a causally ordered attack-to-damage worked trace and a separate Armillary trace (or a precise missing edge), plus at least one concrete damaged/healthy object contrast if available.

Apply **reasonable engineering confidence and explanatory sufficiency**. A positively mapped mechanism supported by appropriate controls can be accepted without exhaustive hypothetical exclusions. Negative claims require a bounded examination of likely actual paths, not an unsuccessful name search; unsupported hypothetical alternatives do not receive equal weight without positive evidence. Do not make all conclusions contingent on an impossible universal proof or automatically propose live instrumentation. If a consequential issue cannot be resolved offline, identify the **smallest discriminating prospective live test**, inputs and observable outcomes, but do not execute it.

Maintain historical evidence and prior findings. Separate a user's reported observation, a screenshot, a saved snapshot, native-reachable logic and actual observed runtime execution. Do not label an object damaged simply because its Integrity UI is present. Identify real records and qualified membership, not bare spatial proximity.

## 4. Deliverables

1. Answer-first `docs/experiments/outpost-defense/report.md` and supporting native/script, attack lifecycle, Armillary, defense contributors, Integrity/repair, persistence and evidence records (choose a coherent minimal file organization; do not create empty documents).
2. A clear **defense-contributor matrix** for turrets, watchtower, security robots, crew and Armillary, differentiating demonstrated modifier, physical combat role, no effect within tested path, and unknown.
3. A **damageable-object/Integrity matrix**, including provider, thresholds, operational effect, repair, saved state and exceptions, with relevant object-specific examples.
4. A **player-presence/remote attack state matrix** distinguishing initiation, ongoing damage, unloaded/distant behavior and save/reload, and documenting which statements remain hypotheses.
5. Native/script/save provenance and independent negative/positive controls, selected mature-save evidence, relevant reproducible research checks, and a finite list of concrete remaining gaps. Update `docs/RESEARCH_STATE.md`, `docs/DECISIONS.md` or `docs/BACKLOG.md` and subsystem indices only where evidence or decisions warrant it. Preserve L1 turret ownership gap as unresolved if the selected evidence cannot close it; no unsupported assertion.
6. An independent review against the frozen mandatory criteria and original evidence. Preserve failed attempts and corrections; perform UTF-8/LF, malformed-spacing/mojibake, formatting/link and source-locator audits (recurring documentation defect).
7. A task-only patch and a **complete** all-uncommitted-text patch, precise Git status/inclusion/exclusion manifests, hashes, exact forward/reverse reconstruction checks in disposable trees, and local-only receipts per `WORKFLOW.md`. Keep proprietary binaries, raw save content and private paths out of text patches.
8. A Conventional Commit subject suggestion for the whole current uncommitted package; **do not stage, commit or push**.

## 5. Compact assignment completion contract

- **Task type:** Bounded offline scientific research and documentation, not an implementation/integration task.
- **Question/deliverable:** Explain attack selection, defensive contribution, and constructed-object Integrity/damage/repair with native causality and appropriate save correspondence.
- **Scope/authority:** Read-only installed EXE/ESM/PEX/PSC, existing native database and protected saves; local evidence and authored documents allowed. No live session, observer, edits to game/assets/original saves or databases, installs/downloads, or Git staging/commit/push. Respect source permissions, local-only evidence controls and the established **40,000,000,000-byte** free-space guard on C: and D: for relevant operations.
- **Mandatory acceptance:** The eight deliverables above, with genuinely substantive mapped mechanisms or defensible bounded negative findings and explicit consequential gaps; reviewer checks the original brief rather than Codex's summary.
- **Optional:** Suggest a narrowly specified follow-on live discriminator only if a material causal edge remains unresolved; no such test required for acceptance of sufficiently supported offline findings.
- **Negative-result closure:** State exact searched entry points, consumers, code/record coverage and competing explanations; neither an unknown save field nor an absent name proves a universal absence.
- **Continuation:** Diagnose and correct in-scope failures, re-evaluate source locators, retest and re-review under this assignment. Preserve failed receipts; do not seek a new brief for ordinary rework.
- **Exit/escalation:** Stop prohibited or unsafe operations, preserve evidence and request only the specific missing permission/input. No artificial scientific time/event quotas; health, integrity and disk safeguards take priority.
- **Review/disposition:** Provide PASS/FAIL/NOT TESTED by criterion; scientific confidence, engineering completion, live validation and publication permission remain separate. Independent reviewer returns ACCEPT/REWORK/ESCALATE; only maintainer authorizes integration.

## 6. Out of scope

General combat AI, turret targeting/performance, weapons, ammunition and pathfinding; detailed actor tactics; construction material requirements unrelated to repair; repeated crew/robot/production/power/limits research; unrelated terrain/renderer mechanics; runtime injection/deployment; broad save parsing tools; and implementation of defenses or mods. Follow a boundary dependency only as far as necessary to explain the stated attack/defense/Integrity result.
