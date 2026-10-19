# SD2 — Shared Outpost Storage, prerequisite admission and crafting inventory access

**Project:** `starfield-outpost-research`  
**Assignment:** bounded offline native, installed-definition, compiled-script/UI and saved-state investigation  
**Issued:** 2026-10-19  
**Integration:** independent review, then maintainer critical diff review before any commit/synchronization

## 1. Objective

Establish **what makes Shared Outpost Storage special**, how construction prerequisites are evaluated, how an outpost detects and registers an eligible shared-storage container, where shared items actually reside, and how different game consumers discover, display and consume inventory. Produce a **source–consumer access matrix** that separates **visibility**, **eligibility**, and **actual consumption**.

This is **SD2**, following accepted SD1 (containers/displays, item ownership/persistence) and preceding **SD3** (Locations database **Stored Resources** aggregation and refresh). The name *Shared Outpost Storage* is not evidence of a single global inventory, item teleportation, or inter-outpost synchronization; establish the actual mechanism.

Use existing S1/S2 storage and movement, E1–E3 industrial production, C1–C3 cargo, L1/L2 construction and P1 power results as accepted bounded foundations. Do not repeat them except to explain a discriminating SD2 difference. SD1 established ordinary inventory stacks versus display references versus mannequin actor inventories; distinguish these from any shared-storage model discovered here.

## 2. Required repository context and provenance

Read `AGENTS.md`, `WORKFLOW.md`, `docs/RESEARCH_EXECUTION_PROTOCOL.md`, `docs/EVIDENCE_STANDARD.md`, `docs/PERMISSIONS.md`, `docs/PROVENANCE.md`, `docs/PUBLICATION.md`, `THIRD_PARTY_POLICY.md`, `docs/templates/completion-contract.md`, and the relevant subsystem, backlog, decisions and research-state records. Review SD1 (`docs/experiments/containers-displays/`), S1 (`docs/experiments/storage/`), and pertinent native/script/save/UI evidence before starting. Revalidate build/version/addresses, file identities, extraction rights and existing reader qualifications rather than silently inheriting stale pins. Honor the accepted findings' original **coverage limits**.

Select representative mature historical save examples from the authorized corpus, not Save52 alone. **Do not assume a positive Shared Outpost Storage witness exists.** If absent after a documented, qualified search, support the bounded native account with explicit save gaps and a proposed minimal controlled experiment only. Original saves and game/source binaries remain immutable and local-only.

## 3. Research workstreams

### A. Construction recipe prerequisites: recognition and enforcement

Use Shared Outpost Storage as the primary case, with a small set of ordinary buildable and differently gated constructible objects as controls. Identify the exact build recipe/form/component and **how the installed game recognizes prerequisites**: native conditions on COBJ or other records, perk predicates, conditions' owner/subject contexts, quests, research unlocks, globals or scripts as actually applicable. Trace the path from definition to build-menu **hidden/locked/available** state, placement/build admission and relevant existing-object usage checks. Determine whether multiple conditions are AND/OR/grouped, when reevaluated, and how non-perk requirements share or differ from the path. Record the actual Shared Outpost Storage requirements for context, **without turning SD2 into a universal perk catalogue**. Do not assume previously built objects lose functionality when prerequisites cease to hold; check the native/script consumer instead.

### B. Shared-storage identity, outpost membership and inventory residence

Identify how the constructed container is recognized (base form, keyword, script, registration table, linked reference, native Workshop enumeration, alias or other actual mechanism). Trace construction, registration, loading, player access, movement, deletion/scrap, disabled/destroyed state and restoration where they materially affect detection. Disentangle **reference exists**, **belongs to Workshop**, **registered for shared access**, **accessible at present**. Identify any rules for zero, one or multiple eligible containers at one outpost and across multiple outposts.

Determine whether there is (i) one authoritative global inventory, (ii) separate inventories exposed remotely, (iii) synchronization/copy/transport, or (iv) virtual aggregation, or a different positively identified model. Follow concrete item residence and writer/loader paths: who actually owns each stored stack, what is serialized, what gets reconstructed, and whether access depends on remote reference loading or persistent registration. Check requirements such as common planet/system, cargo links, power, current outpost, player/ship context **only where native/definition branches can resolve them**. Do not assert global scope solely from names or UI access. Check whether deletion/destruction strands, redistributes, returns, or preserves contents under identifiable conditions; draw on SD1's removal rules instead of assuming those rules apply automatically.

### C. Crafting and research source enumeration and actual depletion

Start at the **real consumer entry points**, not a generic claim that nearby storage is available. Trace installed crafting benches, research stations and relevant recipe/resource requirements to their inventory-provider enumeration, amount calculation, eligibility filter, inventory mutation and update/refresh callbacks. Distinguish and compare:

- Player inventory;
- current ship cargo (and, if distinct, captain's locker/other ship inventories);
- companion/crew inventories;
- local outpost ordinary chests and dedicated industrial storage;
- Transfer Container and cargo-pad outgoing/incoming compartments;
- Shared Outpost Storage at the current outpost and remote outposts.

For each source, state the **context predicate** (player position, active ship, radius, Workshop owner, current location, constructed special object, unloaded access, inventory class, power, etc.) only where proven. Establish if the UI shows a combined resource count that differs from material actually eligible for an operation. Trace **which inventory is decremented first**, handling of partial stacks and split-source fulfilment, and whether update/transaction semantics guarantee or merely attempt consistency. Avoid an exhaustive concurrency study without a material counterexample. Where no actual save witness records a controlled craft, mark priority as STATIC or unknown rather than an observed gameplay result.

### D. Other consumers and negative contrasts

Trace just far enough to compare **outpost construction resource checks and spending**, **research**, **ordinary workbench crafting**, and **outpost repair** where it actually uses inventory. Compare industrial fabricator consumption, cargo transfer and ordinary ContainerMenu access by **reusing** established research and checking whether they call the same provider. Explicitly state whether building at an outpost and crafting at a bench share any source enumerator or merely appear similar to the player.

Do not treat visibility, eligibility and consumption as synonyms. Include false positives: a container whose contents appear in one consumer but not another; a source whose inventory exists but is excluded; or a source that is included in an availability summary but is consumed differently (if the installed paths genuinely support such a case).

### E. Saved-state correspondence and remote behaviour

Search existing mature saves for instantiated Shared Outpost Storage, storage contents, Workshop associations, registry/quest/script variables and qualifying player/ship/current-location context. Record positive **container identity → Workshop / shared-access identity → item residency → loaded reconstruction** joins wherever supported. Differentiate absence of an override branch, empty inventory, unparsed representation, inaccessible save and absent fixture. Do not invent a control pairing or infer gameplay causality from unrelated historical saves.

For remote operations, separate (1) remotely **reading/counting**, (2) remotely **depleting/mutating**, (3) actual item transport or sync, and (4) any requirement that a remote cell or Workshop be loaded. Where a runtime consequence depends on callbacks not demonstrable offline, report the precise remaining discriminating question and propose (do not conduct) the smallest live test.

## 4. Required primary deliverables

Create `docs/experiments/shared-outpost-storage/` (or a clearly justified repository-consistent directory) with:

- `plan.md` — fixed hypotheses, source versions and input permissions, contrasting cases, authorized methods, reproducible criteria and stop/escalation conditions.
- `report.md` — **answer-first** finding matrix: mechanism, confidence/basis, tested coverage, meaningful unknowns and most useful next step.
- `prerequisites.md` — exact Shared Outpost Storage construction eligibility chain, comparison controls and UI/admission distinctions.
- `shared-inventory.md` — registration/presence lifecycle, authoritative inventory model, save/runtime relations, multi-container and remote access.
- `consumers.md` — concrete ingredient-source enumeration and consumption paths and a **source–consumer matrix** with at least **visible / eligible / spent-from** dimensions. Make unknowns explicit rather than guessing.
- `saves.md` — canonical save IDs, identity/hash/decoder receipts, positive witnesses and meaningful negative census/capability boundaries.
- `review.md` — original acceptance matrix and independent verdict, counterexamples/failures/corrections, evidence and patch receipts.

Use small CSV registers for recipes, functions, symbols, source pins or cases if they materially help reproduce results; avoid large repetitive dumps. Update the relevant subsystem docs, `docs/BACKLOG.md`, `docs/RESEARCH_STATE.md`, and implementation-brief index proportionately. Capture evidence links at the point of each claim. Installed definitions, executable/scripts, historical saves and user observations must have distinguishable provenance; maintain LOCAL-ONLY classifications for raw assets.

## 5. Boundary and explicit action authority

**Allowed:** bounded offline read-only analysis of authorized installed definitions, executable, UI/compiled scripts and historical saves; reusing qualified local tooling; temporary derivative analyses, deterministic tests, textual research reports, disposable offline helpers subject to existing protections; independent review and packaging. You may correct in-scope failures and retest under the same assignment.

**Not authorized:** launching Starfield; gameplay; attach/debug/inject/observer deployment; active save writes or modifying original/backup saves; new controlled live captures; game/mod deployments; modifying installed game data; destructive cleanup of user assets; staging, committing, pushing, publishing or distribution. No source-control mutation other than unstaged documentation/tool changes expressly within scope. Do not operate on an account/service externally. Escalate a genuinely indispensable live experiment or unavailable evidence **narrowly**, retaining all completed offline work.

**Reserved for SD3:** Locations database **Stored Resources** list: its full UI provider, inventory membership/aggregation, refresh and displayed remote totals. SD2 may identify a reused inventory service, but may not claim to have mapped the SD3 screen or expand into its complete UI analysis. General crafting progression/recipes, unrestricted perk systems, crime/theft, display mounts, weapon/actor AI, cargo scheduling, production physics and renderer internals are outside scope.

Follow repository-specific protected-input identity/hash requirements, immutable baseline policy, both-drive free-space safeguards (including applicable 40,000,000,000-byte minimums), output limits, stop/worker-retirement controls and preservation of any original failed run. Do not invent arbitrary timeout/sample quotas to declare healthy scientific work complete; justify and obtain maintainer authorization for material new hard limits. Do not overwrite earlier accepted evidence or silently upgrade confidence.

## 6. Embedded compact completion contract — mandatory, frozen

**Task type:** bounded scientific discovery/reconstruction, documentation and only incidental authorized disposable offline tools.

**Question/deliverable:** How Shared Outpost Storage is gated, identified, registered and persisted; what inventory model it uses; and how player/ship/outpost/shared inventories enter ingredient counts and actual consumption across representative consumers, with a causal and evidence-backed matrix.

**Scope/bounds:** Sections 2–5 above, governing repo policies; existing immutable inputs, permissions and live/Git/publication bans. Future SD3 separately scoped.

**Mandatory acceptance — eight criteria (do not redefine without maintainer approval):**

1. **Prerequisites:** Trace actual construction requirement representation and reevaluation/admission path for Shared Outpost Storage, with at least two differentiated control recipes and a defensible hidden/locked/buildable distinction (or explicit demonstrated absence of that distinction in the mapped UI). Separate perks from quests/research or other requirements as applicable.
2. **Presence/registration:** Identify how an actual Shared Outpost Storage construction is recognized and connected to its outpost; trace ordinary creation, repeat constructions, loading, removal and disabled/destroyed treatment to the extent each changes shared eligibility, preserving exact boundaries of unsupported cases.
3. **Authoritative contents:** Determine the strongest defensible inventory-residence and sharing model—global, distributed access, copying, aggregation or another—using actual producer/consumer/writer paths, not naming assumptions. Establish how multiple containers and remote access relate to item identity/count without claiming unobserved transfers.
4. **Crafting/research sourcing:** Trace actual provider enumeration and ingredient visibility/eligibility for ordinary workbench crafting and research, including relevant contrasts for player, current ship, local Workshop, shared/remote, companion and cargo storage. Record source predicates with native/script pins and negative cases.
5. **Consumption and other consumers:** Trace depletion/priority and relevant update behavior; contrast construction spending, research, repair and industrial fabricator where appropriate; produce a matrix that distinguishes **visible**, **eligible**, **spent from**, with unsupported cells marked unknown instead of filled from analogy.
6. **Save/runtime correspondence:** Qualified broad historical-save search for positive shared-storage instances and related contents/ownership when available; actual validated saved joins or a documented bounded negative corpus with decisive native mechanisms and minimal proposed—not executed—discriminating tests. Keep default-vs-overridden and loaded-vs-serialized separate.
7. **Research quality/scope:** Answer-first scientifically useful findings, actual branch/predicate chains, versioned reproducible source pins, negative controls, counterexamples, honest coverage/conclusions, explicit SD1/S1 reuse and SD3 boundary; preserve errors and unresolved live questions without claiming an unobserved result.
8. **Integrity, verification and independent review:** Original/protected hashes, applicable safeguards, deterministic relevant checks, malformed-prose/spacing and UTF-8 audits, preserved failures/corrections, final PASS/FAIL/NOT TESTED with evidence for **all eight** frozen criteria, independent review of the actual submitted revision, exact applicable forward/reverse-verified **complete and task-only** patches and manifests; no staged/committed/pushed files.

**Optional acceptance:** richer variant catalogue, disposable test harness, extra historical witnesses or a prospective live run card. Optional work cannot repair a failed mandatory criterion.

**Negative-result closure:** A bounded claim of no perk/defense/cargo/remote source dependency is valid only after tracing the relevant decision/consumer path with actual supported operands, controls and known scope; absence of a search hit or a narrow save witness isn't proof of system-wide absence. Completed scoped negative research is valid scientific completion. Unsupported executable paths, absent positive saves or no live observations must be clearly classified. A failed necessary engineering qualification remains unfinished.

**Continuation authority:** Diagnose, correct, refactor, retest, independently review and requalify in scope until the frozen criteria are satisfied or a real blocker is evidenced; no new brief required for ordinary correction. Preserve durable checkpoints and negative cases. Authorization does not expand to live/game/save mutation, deployment, commit or publication.

**Exit/escalation:** Stop an affected unsafe action on protected-input drift, failed disk guard/identity, unsafe process or evidence integrity fault, and preserve receipts; continue unrelated safe work. On missing essential inputs or indispensable user-only live step, identify exact dependency, what offline routes were exhausted, narrowly requested action and resumption checkpoint. Do not treat session inconvenience as scientific disproof.

**Review artifacts/disposition:** Independent reviewer against the original brief and primary evidence, criterion-by-criterion matrix and `ACCEPT` / `REWORK` / `ESCALATE`, separate semantic/instrumentation/safety/publication outcomes, unchanged-input receipts, worker cleanup and exact patch reconstruction for complete and task-only diffs; include untracked files and an inclusion/exclusion manifest. Reviewer may not accept its own edits; subsequent fixes require independent assessment. Return an unstaged package with suggested commit message only. Never self-stage, commit or push.

## 7. Expected final Codex response

Report (a) substantive answer-first findings with confidence and limitations; (b) all eight criteria and independent disposition; (c) any missing positive live/save evidence precisely; (d) checks, protected assets and patch receipts; (e) exact report/review and task-only/complete diff locations; and (f) a suggested commit message. **Return for maintainer critical review; do not integrate.**
