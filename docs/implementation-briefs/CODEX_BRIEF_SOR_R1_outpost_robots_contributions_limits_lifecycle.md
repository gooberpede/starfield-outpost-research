# Codex research brief — R1: Constructible outpost robots, contributions, limits and lifecycle

**Project:** `starfield-outpost-research`  
**Assignment:** Single bounded offline research parcel, native runtime and saved state  
**Authority:** Read-only investigation and authored research/verification files only. No Starfield launch, save creation or modification, injection, plugin/observer development, deployment, staging, commit, push or publication.

## 1. Research question and boundary

Explain **how ordinary constructible outpost robots contribute to outpost processes, how their numbers are limited, how they are registered/removed, and how their state survives save/reload and remote operation**. Organize the explanation as a *difference analysis* against the accepted CR1–CR3 crew, E1–E3 production and P1 power mechanisms. Reuse those native contracts when genuinely shared; pursue robot-specific branches to their actual effect rather than simply assuming parity.

**Explicit exclusions:** material and research prerequisites for robot construction; construction UI outside registration/limit gates; general combat, attacks, targeting, navigation, AI pathing, animations, followers/companions such as Vasco or Delta, arbitrary NPC/robot actor types and new mod design. Follow damage, disablement, destruction or construction only far enough to explain count, contribution and cleanup consequences. Do not broaden into the future Limits, Turrets or Attacks phases.

The baseline CR2 census identified **five constructible robot variants** and the ModelA03 (`001d924e`) outpost Aneutronic Fusion perk (`0020d24f`) with additive generator contributions. **Verify these against installed definitions; do not assume they describe all eligible variants, active robots or limits.**

## 2. Required questions

1. **Variant catalogue and eligibility.** Identify every ordinary constructible robot variant, unique base/PackIn/construction association, selected perk(s), rank(s), target categories and actual effect(s). Distinguish definition possession, conditional eligibility and effective contribution. Explicitly document variants with no demonstrated operational bonus rather than inventing one.
2. **Robot numbers and limits.** Identify actual per-outpost construction, assignment and operating limits; any global cap; perk/rank/AV influence; whether robots consume human Crew Stations, Ship Command allowance or human occupied slots. Trace both the UI/construction admission decision and native/quest counter/registry state, including over-limit, removal and replacement cases. Do not infer a count limit solely from recipe conditions.
3. **Registration and ownership.** Determine how construction creates/registers the robot actor, its Workshop owner/assignment, possible `ExtraE2` crew membership and `Extra4C` `CrewAssignment`, and whether relocation or reassignment is permitted. Separate construction instance identity from the active actor identity and from saved owner references.
4. **Effect application and stacking.** Trace each robot-specific contribution through its exact effect entry, environment/conditions, native consumer and final outpost operation. Evaluate identical-robot stacking, distinct robot effects, and composition with human crew/player bonuses. Reuse CR2's multiply/add/precedence rules only where the same actual consumer and eligibility tests apply. Include a worked ModelA03 generator example and at least one production-related or explicit non-contributing contrast.
5. **Remote and exceptional lifecycle.** Compare robot assignment versus physical location, unloaded 3D, resolvable/unresolvable actor, perk-entry storage, power requirements (if any), disablement, nonpositive Health, death/destruction, deconstruction and subsequent cleanup/rebuild. Distinguish saved assignment from present effective modifier; track how counts, ownership and modifiers change. Do not re-research generic robot combat/pathing.
6. **Persistence and restoration.** Map robot-specific save records and the ordinary native restoration sequence for constructed instance, actor, assignment/Workshop association, counters and selected skills. Distinguish explicit serialized fields from definition-derived and runtime reconstructed state, including any missing/default representations. An absent decoded field is UNKNOWN, not proof a robot or contribution is absent.
7. **Crew comparison.** Produce a succinct matrix: human recruit/assignment/slots/contribution/removal/restoration versus constructed robot equivalents. Identify the specific native/shared paths and the precise divergences, not a generic summary of CR1–CR3.

## 3. Corpus and evidence strategy

Do not default to Save52 or to one previously successful save. **Inventory the available mature historical corpus first** using protected metadata, then select positive witnesses with constructed robots at outposts **(a) without assigned human crew and (b) with assigned human crew**. Include contrasting robot variants and nonrobot control outposts where available. Prior CR1 HIST-0255 and HIST-0021/22/24 are starting leads, not a fixed sample or guaranteed robot cases.

For each selected example, attempt a qualified chain: saved construction root / robot actor identity → unique Workshop owner → crew/robot membership or registration → saved rank/perk or qualified definition → expected consumer effect. Independently corroborate ownership using actual relationships rather than spatial proximity or names. Distinguish repeated snapshots of one actor from independent robot instances, and qualify actor template inheritance as CR2 did for generic specialists.

If a required category has no suitable positive witness, extend the corpus search with a documented bounded rationale. If the available corpus truly cannot establish a consequential saved relation, identify the exact missing state and smallest controlled positive/negative save pair that would discriminate it; **do not execute gameplay or new save acquisition**. No wholesale universal robot census or production-grade importer is required.

Native claims require pinned EXE/ESM/build, actual instructions/data consumers and reproducible function/source locators. Save claims require pinned hashes, record/queue/extra locations, qualified identity joins, positive and negative controls and explicit unresolved grammars. Script source is not equivalent to shipped compiled bytecode unless compared. No new Ghidra tooling unless needed to meet the existing bounded research question and permitted under project policy.

## 4. Evidence and stopping rules

Follow `AGENTS.md`, `WORKFLOW.md`, `docs/EVIDENCE_STANDARD.md`, `docs/RESEARCH_EXECUTION_PROTOCOL.md`, `docs/templates/completion-contract.md`, and the CR1–CR3, E1–E3 and P1 accepted evidence. Use **reasonable engineering confidence**: positive native causal mechanisms corroborated by representative saves may support scoped STRONG conclusions. Do not demand an instrumented retail session merely to rule out speculative alternatives; equally, a shared code path or perk definition alone does not prove a robot actually contributes.

Start the final report with concise, direct answers for the seven questions, followed by a robot-by-robot catalogue, limit model, effect/stacking examples, saved/runtime correspondence and crew comparison. Explicitly separate **configured, assigned, eligible, contributing and observed operating** states. Flag only *material* evidence gaps, their consequence and concrete falsifiers. Stop when the requested ordinary-case model is sufficiently explained; do not expand into unrelated systems or indefinitely chase theoretical exceptions.

## 5. Deliverables and frozen completion contract

**Task type:** Bounded offline native/save scientific investigation and authored documentation, not production engineering.

**Mandatory acceptance criteria (all required):**

1. Answer-first research report with a fully qualified ordinary constructible robot catalogue and supported/non-contributing effect classification.
2. Instruction-backed actual robot count, construction/assignment/crew-capacity constraints and lifecycle counter updates; uncertainties and exceptions explicitly bounded.
3. Actual registration/ownership/assignment mechanisms, including where and why they match or diverge from crew.
4. End-to-end robot effect and stacking chains, with worked power example and human/robot interaction.
5. Remote/unloaded, disable/destroy/remove and save/reload lifecycle mapped to the extent causally relevant to limits and modifiers.
6. Representative *real* saved robot instances with robot-only versus mixed-crew comparisons where present; exact saved/runtime correspondence and honest gap accounting. An evidenced corpus failure requires the smallest discriminating future control, not invented witnesses.
7. Durable linked research artifacts under an appropriate `docs/experiments/robots/` area, source/function/evidence registers, updates to `docs/RESEARCH_STATE.md`, `docs/DECISIONS.md` or `docs/BACKLOG.md` only where warranted, and relevant documentation indexes. Preserve prior historical claims and correct contradictions transparently.
8. Relevant bounded verification/regressions, protected original/analysis database and Git HEAD/index checks, UTF-8/LF/links/encoding/whitespace audit, independent reviewer decision against these criteria, manifest/exclusions, and **task-only plus complete** textual diffs with forward/reverse exact reconstruction. Supply a proposed Conventional Commit subject; do not stage/commit/push.

**Optional:** Additional variants, live test cards or unsupported exceptional branches only if decisive for a mandatory finding; proposals grant no execution authority.

**Negative-result closure:** A bounded, evidence-backed absence of a particular bonus or limit is acceptable when actual effect/consumer/admission coverage justifies it; failure to decode a sample or find a keyword does not establish absence.

**Continuation:** Diagnose and correct in-scope failures, preserve original negative evidence, rerun affected checks and obtain re-review within this assignment. Do not silently weaken criteria or label partial engineering success COMPLETE.

**Escalation/exit:** Stop unsafe/unauthorized operations or an evidenced essential dependency and report the exact blocker and recovery input. Keep the project’s disk guards and protected original requirements; never create arbitrary time or evidence quotas for a healthy investigation. No automatic live work, save manipulation, instrumentation, external download or code deployment.

**Review disposition:** Report PASS/FAIL/NOT TESTED for each criterion, scientific confidence separately from task completion, protected input status, actual reviewer ACCEPT/REWORK/ESCALATE and package hash identities. All proprietary raw/native/save evidence remains local-only; no publication or integration is authorized by reviewer acceptance.
