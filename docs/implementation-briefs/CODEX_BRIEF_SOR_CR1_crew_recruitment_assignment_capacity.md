# Codex research brief — CR1 crew recruitment, assignment, capacity and persistence

**Project:** `starfield-outpost-research`  
**Type:** Bounded offline native/definition/PEX/save research, documentation and independent review  
**Authority:** Read-only evidence investigation and authored documentation/evidence helpers only. No game launch, live observer, save modification, deployment, mod development, staging, commit, push or publication. Preserve protected originals and repository state.

## 1. Purpose and research boundary

Begin the crew research programme by establishing **who can be recruited or assigned to an outpost, what capacity limits apply, how assignments change, and how those facts are represented in the runtime and saved game**. Treat these as practical mechanisms to explain, not merely a census of labels or functions. Crew effectiveness/skills and remote contribution will receive deeper CR2/CR3 investigations; trace relevant interfaces now rather than avert inquiry where eligibility depends on them.

Include named companions/recruits (for example Lin and Heller) and generic hireable Outpost Specialists. Include *ship assignments only insofar as needed* to understand recruitment, capacity competition, eligibility and location changes. Do not expand into full ship systems or ship-bonus research. Some outpost assignment eligibility is controlled by player perks or construction restrictions; investigate those fully where relevant rather than deferring them reflexively to later Limits research.

**Carry forward the earlier accepted E1 crew-assignment and timer-contribution evidence**, including replacement/stacking observations, as prior findings to cross-reference—not a reason to reopen production arithmetic. Inspect actual current source paths, formats and build pins before relying on named files or addresses.

## 2. Mandatory research questions

### A. Candidate eligibility, recruitment and assignment

- Which NPC categories and specific actors can be recruited, hired, assigned or reassigned? Distinguish generic recruitment/hire state from eligibility to serve at a particular outpost; do not infer eligibility from a name or NPC skill list alone.
- Map the native and/or script predicates, UI data providers and actual assignment operations for assigning, unassigning, transferring between outposts, moving to a ship, dismissing and any relevant follower-state conflicts. Distinguish **UI option visibility** from **native enforcement**, success/failure return codes and side effects.
- Determine whether outpost assignment requires a Crew Station, the precise qualifying object(s), whether construction alone is sufficient, and how powered, disabled, damaged, deleted or inaccessible stations are treated. Establish whether multiple stations add capacity and how removal/deconstruction affects existing assignments.
- Identify whether recruiting more people than current assignment capacity is permitted, and whether an unassigned roster can be retained independently of station slots.

### B. Effective capacity, skill/perk gates and limits

- Establish the **effective per-outpost maximum**, the role of Crew Stations and all relevant player perks/skill ranks, with real construction definitions and native calculations. Check caps, additive versus replacement rules, minimums and any hard-coded maxima.
- Investigate whether there is a **global recruit/assignment limit**, whether ship and outpost assignments draw on a common pool, and how unassigned crew count toward any bound. Distinguish ordinary gameplay rules from exceptional/quest/story cases.
- Explain what happens if the configured capacity falls below existing assignments, or if crew/station objects become temporarily inaccessible. Does the game automatically displace someone, reject the change, preserve an overcapacity state, or revalidate later?
- Capture limits shared with later construction research without attempting the full Limits census. Document rank-to-result tables and separate definition-derived defaults from actual effective/current runtime values.

### C. Assignment lifecycle and update timing

- Trace **assignment request → owner/location relationship → actor/crew registry updates → capacity revalidation → effect-registration/notifications**, distinguishing synchronous operations, queued events, actor travel and post-load restoration.
- Identify when an assignment becomes authoritative and when dependent systems could see it. Are updates immediate on successful assignment, at the next engine tick, after arrival, after cell load, or at a later refresh? State actual native/event basis, not a guessed wait duration.
- Trace relocation/unassignment/dismissal and change-of-ship/outpost symmetry, including cleanup of stale participation and any reported handling of unavailable/disabled/dead actors.
- At the CR1 boundary, locate where an assigned member's skills/modifiers are enumerated and dispatched to consumers; **do not assert specific bonuses or stacking outcomes without tracing them**. Record the interfaces and questions handed to CR2.

### D. Runtime-to-save correspondence (mandatory)

For representative actual saved instances, establish, where recoverable:

1. Crew actor identity and stable reference/definition relationships, including generic specialist instances.
2. Recruitment/availability state and assignment to a specific outpost, ship or unassigned roster.
3. Outpost crew stations and capacity-relevant constructed objects, joined to actual Workshop identities.
4. Persisted skill/perk packages, actor values, assignment-related flags, script/quest state and any explicit crew registry links **versus definition-derived or runtime-reconstructed values**.
5. Information available for detecting a pending transfer, physical presence, actor resolution, capacity state or contribution after reload; mark fields genuinely absent/unknown rather than equating missing record with false or empty.

Reuse the project's protected saves, native Workshop owner/membership analysis and existing record readers. Qualify positive joins by exact saved reference identity and owner/location; avoid ungrounded nearest-outpost or name-only matching. If historical saves contain no qualified crew assignment, complete the other authorized native/definition work, record the precise corpus gap and propose the smallest later controlled save pair; **do not create gameplay saves under this brief**.

### E. CR2/CR3 handoff and cross-system boundaries

Create a concise evidence-backed handoff identifying the actual machinery to examine next for: crew skill catalogue and rank/stacking semantics; effects on extractor/fabricator rates, generator output, capacity, cargo and combat; and remote actor residency versus persistent crew contributions. Explicitly flag the user's examples—**Payloads, Aneutronic Fusion, Geology and Pistols**, as well as named versus generic Outpost Specialists—without resolving them by assumption in CR1. Trace any directly encountered contradictions now; do not conceal consequential prerequisites behind phase labels.

## 3. Evidence and conclusions

Begin the main CR1 report with a **plain-language answer-first table** for recruitment/assignment, station requirement, per-outpost and global capacities, ship competition, reassignment timing and save recoverability. Give the strongest grounded conclusion, confidence (`PROVEN`, `STRONG`, `PROVISIONAL`, `OPEN`), evidence type (`STATIC`, `SAVE`, etc.) and consequential exceptions. Follow with native/PEX/definition paths, causal event timeline, capacity formulas/rank table, named/generic comparison and concrete saved-instance joins.

Use the project's accepted **reasonable engineering confidence / explanatory sufficiency** standard. Positive mechanisms and bounded negatives count; hypothetical unseen alternatives do not force endless investigation. Conversely, native reachability alone does not prove a particular historical actor took the path, and a saved assignment does not prove presence or a currently effective bonus. Investigate concrete in-scope gaps seriously, then stop at the agreed boundary. No live observer or general-purpose crew/save importer is an implied deliverable.

## 4. Future applications backlog — mandatory

Add two **separate documentation-only** future application entries to `docs/BACKLOG.md`, preserving any previously recorded ideas and avoiding duplicates:

- **Cargo Link Fuel-Efficiency Correction (in-game mod):** investigate whether eligible production-speed/interval modifiers accelerate periodic inter-system He-3 consumption without increasing freight trips, identify which actual crew/player perks apply and scope possible decoupling or per-voyage fuel economics. Treat proposed balancing/design as unimplemented; retain C3's five-unit/108-base-scheduler-second evidence and eligibility caveats.
- **Starfield Save-to-Network Importer (Outpost Network web-app feature, not an in-game mod):** reconstruct saved outpost identity/site, production configurations, pads and pairings, and defensible inferred outbound products into a draft network; preserve uncertainty, player-entered planning intent and existing UUIDs on reimport. Note outstanding completeness problems (selected biomes/site resources, skill ranks, exceptional constructed-object membership, identity matching and arbitrary/modded saves). **Do not build an importer or promise full JSON parity.**

Keep existing cargo-link UI enhancement and time-skip reconciliation entries separate.

## 5. Frozen completion contract

**Task type:** Bounded offline research and documentation. Not a live test, generalized import tool or implementation assignment.

**Mandatory acceptance — all eight:**

1. Positive native/definition/PEX evidence identifies candidate/recruit/assignment eligibility, enforcement and consequential exclusion cases, with named and generic roles distinguished.
2. Crew Station and capacity model explains actual per-outpost/per-character constraints, all relevant perks and ranks, ship/outpost competition and overcapacity handling, or gives an evidence-backed exact unresolved predicate after bounded investigation.
3. Assignment/reassignment/unassignment lifecycle traces persistence, authoritative update, events/travel and observable-delay boundaries without inventing instant or deferred behaviour.
4. Runtime-to-save matrix and positively grounded historical crew/station instances—or documented corpus-specific absence/gaps and exact smallest missing save control—distinguish persisted from reconstructed values.
5. CR2/CR3 interfaces are clearly documented, with requested skill examples and production/power/cargo effects retained as explicit questions rather than unsupported statements.
6. Both requested future application backlog additions are included accurately, remain separate from existing entries and authorize **no implementation**.
7. Source/native/version pins, answer-first report, evidence and coverage register, existing research-history/decision/subsystem updates as appropriate, in-scope tests and preserved negative findings meet `AGENTS.md`, `WORKFLOW.md`, `docs/EVIDENCE_STANDARD.md` and source/permission policy.
8. Independent reviewer ACCEPT against the frozen brief and actual primary evidence; PASS/FAIL/NOT TESTED matrix; source/protection checks; final verified task-only and all-uncommitted complete textual diffs, manifests and retained reviewer decision.

**Optional:** additional representative saves, small reproducible offline checks or a targeted future live experiment *proposal* where essential. Optional checks are not retroactive acceptance gates.

**Negative closure:** A well-examined scoped negative finding is valid research, not a reason to demand universal absence proof. If an essential question cannot be answered, state actual paths tested, evidence missing, competing supported models and the narrow follow-up; do not label unexplained mandatory research omission a PASS. Engineering/regression failures remain REWORK until fixed or genuinely escalated.

**Continuation:** Correct/diagnose/retest in-scope errors and address independent reviewer defects under this assignment, without unnecessary new briefs. Changing mandatory criteria, executing live actions or broadening into CR2 ship systems requires maintainer authorization.

**Safety / exit:** Preserve installed game files, original saves, databases, source archives and Git HEAD/index. Keep documented C:/D: **40,000,000,000-byte free-space guards** where applicable; no arbitrary healthy-run time/count cutoff. No mutation to game, save, process, plugin, deployed assets, staging, commit or push. Genuine access/integrity blockers must be evidenced with a narrow resume requirement.

**Review artifacts:** Authored UTF-8/LF Markdown and required compact tables/function/source ledgers. Validate encoding, whitespace, local links and relevant existing reader tests; do not mask earlier failures. Retain local raw/native/save materials as `LOCAL-ONLY`, authored interpretation `REVIEW-REQUIRED`. Produce task-only and complete review diffs (including untracked text), status/inclusions/exclusions and a hash-bound manifest; verify full forward/reverse patch reconstruction in disposable trees without staging. Preserve final independent reviewer receipt. Suggest a Conventional Commit subject; integration remains the user's decision.

## 6. Explicit exclusions

No full ship-system bonus research, complete CR2 crew skill/stacking catalogue, CR3 remote actor simulation, comprehensive later Limits census, robot/turret/attack research, save writer, generic actor inventory extractor, live instrumentation or mod/plugin implementation. Follow cross-boundary native paths only where needed to explain **CR1 assignment and capacity**, recording any direct relevant finding without granting authority for the next phase.
