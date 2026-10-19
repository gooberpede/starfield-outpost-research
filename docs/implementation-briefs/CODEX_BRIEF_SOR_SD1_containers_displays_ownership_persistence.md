# SD1 — Containers, displays, ownership and persistence

**Project:** `starfield-outpost-research`  
**Assignment:** bounded offline Starfield runtime-definition/script/native and saved-state research  
**Issued:** 2026-10-19  
**Integration:** user critical diff review before any commit or synchronization

## 1. Objective and questions

Map the ordinary outpost **container and display subsystem** as the first of three phases:

- **SD1 (this assignment):** classify constructible containers and displays, their capacity and item-admission rules, ownership/access semantics, item residence and display attachments, and construction/interaction/removal/save persistence.
- **SD2 (later):** Shared Outpost Storage cross-outpost access and crafting integration.
- **SD3 (later):** Locations database **Stored Resources** aggregation, providers and refresh.

The essential deliverable is a **causal, evidence-backed classification and lifecycle model**, not a list of FormIDs alone. Answer separately (a) what stores the item, (b) what visually presents it, (c) who owns it and the fixture, (d) who can interact with it, and (e) how each fact survives save/reload. A fixture's inventory record alone does **not** establish successful display attachment or visual restoration.

## 2. Required starting context

Read and reuse current repository instructions, permissions and research records rather than assuming this brief supersedes them:

- `AGENTS.md`, `WORKFLOW.md`, `docs/RESEARCH_EXECUTION_PROTOCOL.md`, `docs/EVIDENCE_STANDARD.md`, `docs/PERMISSIONS.md`, `docs/PROVENANCE.md`, `docs/PUBLICATION.md`, and third-party source restrictions.
- `docs/experiments/storage/` (S1 storage inventory, capacity, and link admission), S2 output movement, L1 numerical construction limits, L2 build budget, L3 placement, R1 robots, DA1 damage/repair where relevant.
- `docs/BACKLOG.md`, `docs/RESEARCH_STATE.md`, subsystem map, previous save decoder notes, and suitable historical save inventories.

S1 already mapped CONT inventory framing, standard resource storage capacities, industrial endpoints and a **bounded** decorative-chest/output-link exclusion: 16 ordinary decorative-container recipes in three FLSTs have the relevant link-blocking actor values; `TESContainer` possession does not imply output-link participation. Reuse these facts; do **not** assume they settle ordinary ContainerMenu admission, theft, display mounting or current overrides. L1's mannequin construction quota and DA1's damage model are references, not new investigation mandates.

## 3. Questions and evidence requirements

### A. Classification and ordinary constructible catalogue

Enumerate the installed ordinary outpost-buildable classes at the **recipe → created base/assembly → runtime reference/component/script** level, with variant counts and qualified exclusions. Include ordinary chests, crates, lockers, storage furniture, weapon racks and displays, display cases/shelves, mannequins, and any distinct specialized storage/display mechanism discovered in the same bounded catalogue. Include nonconstructed/world-container comparison only where needed to explain effective ownership or interaction rules. For **Shared Outpost Storage**, identify its ordinary construction form and classification only; leave all cross-outpost behaviour to SD2.

Determine the actual recognition predicates (form type, components, keywords, actor values, scripts, furniture/actor/rack attachment system, conditions, menu/native tests) for: ordinary storage, direct transfer, displayed/attached items, inventory vs slot/equip residence, and Workshop ownership. Do not classify by name or visible appearance alone. Compare variants where definitions differ materially; don't trace every cosmetic mesh.

### B. Capacity, filtering, admission and transfer

Identify per-class/default capacity semantics: total carry weight, item or slot count, equip slots, compatible form classes, or unlimited storage. Distinguish base-record defaults, per-instance overrides/modifiers, UI gating, native capacity checks, and script/forced insert exceptions. Provide a bounded test or executable/static counterexample for important distinct mechanisms. Separate “allowed by data/runtime machinery” from “ordinary player action succeeded.” Explain partial stacks, nonstacking item instances, modified equipment, special/stolen item metadata and how inventory transfer preserves them where supported.

### C. Ownership and permitted access

Investigate independently:

1. Workshop membership of constructed fixture/reference.
2. Physical fixture's owner (actor/faction/reference ownership state where applicable).
3. Ownership and stolen status of contained item instances.
4. Player access rights, steal/transfer UI treatment and the ordinary insert/remove action.

Establish whether construction or deposit changes item ownership and/or theft marking, whether retrieval differs, and whether the ownership metadata survives container-to-display transitions. Use the **relevant** native/script/UI decision path, not just owner field decoding. No general NPC crime system investigation. Avoid conflating a Workshop ownership handle with a faction ownership rule.

### D. Display presentation and unique-item residence

For weapon racks, display cases and mannequins (and other materially distinct mechanisms), identify:

- What references/inventories/equipment slots actually hold an item, including any surrogate or displayed world reference.
- How slot admission and attachment indices/markers are selected and verified.
- How instance-specific modifications, enchantment/legendary/quality data, charge/condition, ownership and quantity are retained or transformed, **to the extent present in Starfield's installed representations**; do not assume every example property exists.
- Creation/removal of visible displayed geometry or references; mapping from logical stored instance to visual placement.
- Persisted fields vs native/script restoration and runtime-only/transient state, including any known failure modes.

A positive **fixture → specific item (plus extras) → attachment/equip relation → restored representation** join is preferred for each distinct mechanism; don't label an inventory-only join as a visually validated display. If exactly identifying the displayed item in a save isn't possible, preserve the stronger lower-level evidence and explain the narrow gap.

### E. Construction, use, removal, damage and persistence

Trace bounded ordinary lifecycles: construct empty fixture; store/equip item; visible presentation; save and load restoration; retrieve; move; delete/scrap; and destroy/repair where these have distinct effects on contents. For each, determine whether contents return to player inventory, are dropped/spawned, remain stored, or are deleted, with explicit action paths and preconditions. Distinguish ordinary Workshop moving/scrapping from physical damage/destruction. Reuse DA1 for Health/repair infrastructure rather than reopening combat research.

### F. Actual saved witnesses and controls

Search the **broader historical/mature save corpus**, not only Save52. Choose candidates according to positive evidence density (e.g. stored mixed items, filled rack, equipped mannequin, populated display case). Use canonical save identity, provenance/hashes, protected copies and decode validity checks before comparisons. Actual saved positive witnesses are expected for materially different mechanisms **when present in the authorized corpus**; negatives require a documented bounded search and capability limits. Include empty controls and distinguish absent change records from verified empty inventories. Never infer causation merely from historical change between two unrelated saves. Where no positive saved example exists, establish the native mechanism to reasonable engineering confidence, record the coverage and propose the *smallest* discriminating controlled save experiment—**do not execute live tests without authorization**.

## 4. Expected artifacts

Create `docs/experiments/containers-displays/` (or a compelling consistent equivalent), with:

- `plan.md`: frozen questions, hypothesis/alternatives, source and save selection, evidence/counterexample plan, permission and safety boundaries.
- `report.md`: **answer-first** cross-layer classification/lifecycle summary, confidence, supported coverage, observed vs inferred and unresolved cases.
- `definitions.csv` (or equivalent): canonical build recipes, forms/components, filters/slots/capacity, significant variants/exclusions, complete row provenance.
- `native.md` and/or `scripts.md`: actual branch/predicate and call/event chains, addresses or source symbols pinned to executable/script versions and evidence anchors.
- `saves.md`: sampled positive/negative witnesses, instance-level joins and serialisation/restoration details, hashes, parse validation and limitations.
- `review.md`: criteria matrix, independent review, failed/reworked iterations, checks, final patch receipts and decision.
- Relevant function/source/evidence registers, if needed for reproducing claims; update subsystem map, backlog, research state and implementation-brief index according to current repository conventions.

Prefer a compact, navigable evidence set over repetitive dumps. Distinguish original research findings from reuse of accepted S1/S2/L1/DA1 results. Keep raw game/source/save binary material local-only under existing permissions.

## 5. Explicit exclusions

- No SD2 cross-outpost Shared Outpost Storage behaviour, synchronization or workbench sourcing; no SD3 Stored Resources UI/aggregation tracing. Classification dependencies may be noted without expanding.
- No general physics/Havok clutter positioning, general crafting recipe logic, unrestricted crime/NPC trading simulation, combat AI, general damage engineering, or redoing industrial storage/output links.
- No claims that all display slots or all object variants are exhaustively understood without a demonstrated qualified census.
- No game launch, gameplay, debugger attachment, injection, observer deployment, active save writes, save editing, alteration of original archives, or user-only actions under this brief.
- No staging, commits, pushes, publication or repository release. Text evidence/reports and disposable read-only decoding/validation tooling are allowed subject to repository rules and safeguards.

## 6. Embedded assignment completion contract (mandatory, frozen)

**Task type:** Bounded research/discovery and documentation, with optional disposable offline analysis scripts only where evidence demands.

**Question/deliverable:** Answer the classification, admission/capacity, ownership/access, logical item residence/display attachment, lifecycle and save correspondence questions above for the **ordinary constructible** classes, with qualified exclusions and reproducible source pins.

**Scope/bounds:** Existing permitted offline executable/ESM/compiled scripts/save inputs; originals immutable. Respect `AGENTS.md`, `WORKFLOW.md`, `docs/RESEARCH_EXECUTION_PROTOCOL.md`, `docs/EVIDENCE_STANDARD.md`, permissions, evidence integrity and third-party source rules. Enforce existing both-drive disk free-space guards and protected-input hash/identity, output size, worker cleanup and STOP controls on operations for which they apply. Any new hard resource guard requires justification rather than an arbitrary premature scientific cutoff.

**Mandatory acceptance (eight criteria):**

1. **Classification:** Trace the ordinary constructible container/display census to actual recipes and runtime base/component/interaction recognition; qualify completeness and material variants, with Shared Outpost Storage classified only.
2. **Admission/capacity:** Explain capacity and compatibility per mechanism, and where enforcement occurs, with at least one discriminating example or native decisive branch per distinct mechanism.
3. **Ownership/access:** Separate Workshop ownership, fixture ownership, instance ownership/stolen status and interaction permissions; provide relevant decision/transfer path and scoped answer on depositing and retrieving.
4. **Display residence:** For racks, cases and mannequins, explain the item-holding model and the native/script link to visible attachment/equipping; separately mark any **unproven** rendered/save join.
5. **Lifecycle:** Trace construction, ordinary item add/remove, movement/scrap and destruction/repair consequences; preserve conditions and cases where no ordinary confirmation exists.
6. **Persistence:** Connect native writer/load/restoration paths and valid save example(s) or bounded negative corpus coverage for each materially distinct mechanism; preserve instance extras and item/slot identities wherever genuinely supported, without conflating saved contents and successful rendering.
7. **Research quality and limits:** Answer-first report, reproducible pins, source/version/hash provenance, distinction of observations/inferences, controls and serious counterexamples; preserve SD2/SD3 and existing S1/S2 boundaries, and report concrete remaining tests without executing unauthorized live actions.
8. **Integrity, completeness and independent review:** Safe protected inputs, deterministic relevant checks, malformed-prose/spacing audit, independently reviewed full assignment against **these original criteria**, criterion-by-criterion PASS/FAIL/NOT TESTED, verified exact task-only and complete diffs, reviewed revision and final disposition.

**Optional acceptance:** Exact joins for every cosmetic variant; comprehensive visual asset layouts; positive populated representatives of every mechanism if not present in the corpus; generalized reusable decoding tooling. These do not justify postponing adequate scoped research, and cannot substitute for mandatory criteria.

**Negative-result closure:** A claim such as “no general display inventory for this class,” “no capacity gate on ordinary transfer within inspected path,” or “no positive mannequin in sampled corpus” requires qualified, bounded executable/definition/save coverage and explicit competing paths, not absence from a single save or an unsupported universal negative. A full renderer model is not required to establish a strong scoped native attachment mechanism. Missing historical examples may be recorded with a specific future live acquisition card; do not replace positive native findings with global uncertainty.

**Continuation authority:** Diagnose in-scope failures, improve offline analyses and documentation, test plausible alternative branches, rerun regressions and obtain independent re-review in the **same assignment**. Mandatory criteria remain frozen unless the maintainer explicitly approves a dated amendment. Reviewer REWORK is not a new-brief requirement.

**Exit/escalation:** Halt affected action on failed hash/identity or unsafe disk/output/worker conditions; preserve receipts and request a narrowly identified decision. If only a live save/action can resolve a mandatory answer, complete authorized offline work, identify the precise gap and proposed minimal experiment, and escalate **only** the unauthorized action. Actual terminal dependency exhaustion must be evidenced with attempted paths and durable resume checkpoint. No automatic timeout/test-count cap for healthy authorized science.

**Review and disposition:** Independent reviewer sees the *original brief*, primary evidence, records of failed attempts, actual final tree, complete/task-only patches and receipts; reviewer must be independent of author and corrections. Report separate scientific result/confidence, engineering/validation integrity, protected-input status, permissions, reviewer `ACCEPT`/`REWORK`/`ESCALATE`, and publishability (not automatically cleared). No integration before user review.

## 7. Return package

Return a concise summary of what distinguishes containers from displays, supported capacities/admission, ownership and retrieval findings, one representative display persistence chain, the remaining named gaps, evidence paths, validation, reviewer decision and proposed commit message. Package untracked text with complete and task-only patches, exact forward/reverse applicability or reconstruction checks, inclusion/exclusion manifest, status, hash receipts and checks. Do not leave substantive records untracked outside the complete patch; do not conflate tool SUCCESS with scientific acceptance. Explicitly declare that nothing was staged, committed or pushed (or report any deviation).
