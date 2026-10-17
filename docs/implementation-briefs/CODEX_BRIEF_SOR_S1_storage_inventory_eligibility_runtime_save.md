# Codex research brief — S1: Outpost storage, inventory and output-link eligibility

**Project:** `starfield-outpost-research`  
**Type:** Bounded offline native-runtime and save-file research; durable reference, reproducible checks and independent review  
**Status:** Proposed first storage/logistics phase after accepted P1 power work  
**Authority:** Offline read-only investigation of approved installed definitions, native analysis exports and protected existing saves. Authored research documents and bounded local analysis/verification scripts are permitted. **No game launch, live attachment/observer, save creation/editing, deployment, original-input mutation, staging, commit, push or external publication.** Any later live/save experiment requires separate approval.

## 1. Objective and success standard

Establish a useful, evidence-grounded reference explaining **what inventories exist in player-built Starfield outposts; what each can contain and how capacity is enforced; which Workshop objects qualify as output-link sources and destinations; and how these properties exist in both the running game's native structures and saved state**. Connect native concepts to actual saved records wherever supportable. Do not treat either live-runtime mechanics or save serialization as an appendix: investigate both systematically and identify precisely where they join or diverge.

This is **S1**, not the full local-transfer engine. S2 will address directional movement, transfer triggers/scheduler, multi-hop routing, full-destination handling, cycles, batching and backpressure. S3 may address integrated production behaviour. S1 should locate relevant native entry points and data representations for later work, without pre-emptively implementing S2.

Use **reasonable engineering confidence** and the project's `docs/EVIDENCE_STANDARD.md`: prefer a coherent native mechanism corroborated by definitions and saved examples; accept scoped `STRONG` working findings when justified. Do not demand exhaustive proof against speculative exceptions, but also do not claim current live values from static code or historical saved bits. Explicitly separate scientific confidence, research-assignment completion, and publication status. An unsupported counter-hypothesis bears an evidence burden; a concrete contradictory path does not disappear merely through explanatory simplicity.

## 2. Starting material and scope boundaries

Read `AGENTS.md`, `WORKFLOW.md`, `docs/RESEARCH_EXECUTION_PROTOCOL.md`, `docs/EVIDENCE_STANDARD.md`, the completion-contract template, P1 power and E1/E2/E3 production reports, existing Workshop membership/population/save-record research, relevant registers and the existing source/permission pins. Check installed executable/definition build/version and hashes rather than assuming old pins remain current. Reuse project-owned readers and native exports; preserve raw evidence and protected corpus. Locate existing save examples by independently corroborated identities, not guessed label/record coverage.

**Primary catalogue:** dedicated Solid, Liquid, Gas and Warehouse containers in all installed size variants; Transfer Container (including enough ship-inventory interaction to distinguish its special role); internal extractor, greenhouse/animal producer and fabricator inventories; fueled generator He-3 input; cargo-pad incoming, outgoing and inter-system He-3 compartments; other ordinary outpost production/logistics inventory-bearing objects found by a bounded census. Treat the user's size/category/mixed-content descriptions as testable leads, not facts. Where an object has distinct input, output or fuel stores, report each separately.

**Boundary examples:** compare one ordinary chest with an extractor, a dedicated storage unit and a fabricator to discover link eligibility. Do not research general chest/display contents, restrictions or persistence, Shared Outpost Storage cross-outpost access, crafting-workbench sourcing, or the outpost-database **Stored Resources** inventory aggregation; record these as later questions, including whether Shared Outpost Storage contributes to the displayed quantities. The player's screenshot at Schrod II Ad is a question prompt, not proof of the list's provenance. Cargo pads are in scope as *local inventory/compartment and local-link endpoints* only; defer ship scheduling, inter-/intra-system transportation, returned freight, remote saturation and He-3 voyage consumption. Preserve the user's observed possible outgoing-to-incoming cargo spillover as an unresolved later transport hypothesis; do not attribute its cause now.

## 3. Research questions — native and persistence paired

### A. Inventory and capacity catalogue

For every supported inventory/compartment class, determine:

- Constructible forms, installed base definitions, keywords/components, rank/size variants and actual admission restrictions (including whether multiple different items are allowed). Differentiate UI category labels from native filters and transfer-time checks.
- Capacity units and governing values (mass, item count, stack count, another unit); actor-value, perk or difficulty modifiers where relevant. Explain full/empty and partial-add semantics only to the extent necessary to understand admissibility/capacity, deferring transfer routing.
- Runtime inventory owner/interface, input/output/fuel role, whether inventory is physically stored on the reference or exposed through a broader Workshop abstraction, and native reading/writing boundaries. Avoid conflating a producer's recipe inputs with a separately stored item stack.
- Saved location and encoding of container inventory, compartment identity, quantities, capacity-relevant configuration and associations to owner/Workshop. Identify absent, derived, runtime-only and unknown fields separately. Demonstrate selected object-level joins to actual saves, including negative/comparison examples where feasible.
- Whether the inventory survives disable, unloaded-cell, save/reload, and local power loss *as established from code and saved examples*; do not imply real-time simulation from persistence alone.

Deliver a **runtime ↔ save correspondence matrix** with columns for class/variant, role, eligibility/filter, capacity/units, runtime owner/path, saved representation and sample, strength of cross-layer join, and outstanding limits. Where a category cannot yet be decoded from saves, state what native or serialization boundary was actually examined and the narrow missing prerequisite.

### B. Output-link source/destination eligibility — architectural boundary

Identify what makes a Workshop reference eligible for a local output link, comparing at least extractor, dedicated storage, fabricator and ordinary chest. Trace separately:

- Creation UI's source selection and target selection gates; direction-specific requirements; any keywords/AVIF/PRPS/base components, reference state or native predicates involved.
- Underlying native add/remove or validation paths: do they reject unsupported endpoint classes even if UI selection is bypassed, or is exclusion solely UI-level? Distinguish confirmed enforcement from a plausible untested bypass.
- The relationship's level: connection between references/Workshop objects, inventories, resource-keyed producers or inventory ports; identify any endpoint role mapping and filter compatibility.
- Saved representation of directed links, endpoints, link-eligibility-related settings and how these are reconstructed into runtime lookup structures. Reuse E1–E3 destination/source maps where applicable, rather than assuming electrical `ExtraCB` is the output-link format.

S1 should **identify direction capabilities and validation mechanisms** (can be a source, destination, both, neither), without concluding S2's actual one-way flow or reverse/backpressure behaviour. A chest's absence from the normal UI does not prove the native transfer system would reject it: report that distinction accurately.

### C. Transfer Container and cargo pads, limited special cases

Identify the Transfer Container's own inventory, link eligibility and native handoff/access relationship with the player's ship cargo hold at a reference level (including whether access/transfer is automatic versus UI-mediated, when supportable). Defer exact extended-distance measurement and broad ship cargo behaviour unless essential to distinguish its storage role.

For cargo pads, identify individually owned or logically distinct inbound/outbound/fuel compartments and local-output-link participation, capacity/filter rules and saved representation. Do not reconstruct shipment, travel, cargo return or remote transfers. If the native compartment interface cannot be understood without invoking shipping code, record the minimal boundary and defer it.

## 4. Method, falsifiers and finite stopping rule

1. Build a definition-driven bounded candidate census (include clear exclusions and exceptions). Reuse production object listings, and independently verify representative base/keyword/size classifications.
2. Trace relevant native inventory owner/capacity/admission and output-link endpoint predicates through their actual consumers; prefer dataflow and positive references over a decompiler's absence or a keyword search alone.
3. Use protected saves to corroborate multiple distinct positive object examples and at least one exclusion/negative case where possible. Reuse identified mature saves only after record/owner confidence is established. Distinguish *historical saved inventory* from current loaded inventory.
4. Test competing eligibility/capacity interpretations against native code and saved examples. Preserve credible counterexamples, rather than broadening into an exhaustive game-wide container decoder.
5. Stop when the scoped ordinary-case model answers the matrix and eligibility questions at reasonable engineering confidence, or document a specific material unresolved boundary after the established native and saved routes are exhausted. A plausible unobserved exception alone does not require a new observer or further research. Do not repeatedly broaden the call graph to chase hypothetical possibilities.

No live intervention is a prerequisite for bounded S1 completion. Where actual runtime values or UI interactions are essential to choose between materially supported explanations, propose a *separate*, smallest discriminating validation; do not silently build or run it. Report **established / strongly supported / unresolved** per material conclusion and what observation would change the decision.

## 5. Output and documentation

Create an answer-first S1 report in an appropriate `docs/experiments/` subdirectory; include (i) a short plain-English description of storage types and restrictions, (ii) the runtime/save correspondence matrix, (iii) a directional endpoint-eligibility comparison explaining the chest distinction as far as evidence permits, (iv) Transfer Container and cargo-pad inventory findings, (v) saved-example evidence and native/version pins, and (vi) an explicit handoff to S2 and deferred chest/database/cargo-transport work. Update `docs/RESEARCH_STATE.md`, `docs/DECISIONS.md`/`docs/BACKLOG.md` and registers only where warranted, preserving historical findings and links. Record an implementation brief entry per repository convention.

Give the user-facing executive summary **direct answers first**: what can store what, what governs capacity, what qualifies as a sender/receiver, and what is represented in saves. Do not hide a conclusion behind an elaborate list of caveats. Detailed tables, RVAs, source excerpts and caveats belong below the summary. Keep no-evidence statements distinguished from evidence of absence.

Run scoped existing reader/script regressions plus any appropriate original offline tests; preserve original input hashes and record failures/corrections. Obtain an independent reviewer decision under `WORKFLOW.md` and `docs/RESEARCH_EXECUTION_PROTOCOL.md`. Export task-only and complete text diffs and manifest (including untracked text), exact forward/reverse patch verification, changed/excluded inventory, `git status --short`, whitespace/encoding/link audit, and suggested Conventional Commit subject. Never include proprietary binary saves/native exports in the diff. **Do not stage, commit or push.**

## 6. Compact completion contract (frozen for this assignment)

- **Task type:** bounded offline discovery/research hypothesis, semantic reference and documentation; no product integration.
- **Question/deliverable:** catalogue major outpost storage-bearing objects and restrictions; map their runtime and save representations; establish link-source/target eligibility architecture; delimit Transfer Container and cargo-pad storage roles.
- **Scope/bounds:** approved read-only native/definition/save evidence, owned reproducible local scripts and authored documentation only. Protected inputs and both-drive 40,000,000,000-byte caller-available free-space guards retained wherever applicable. No game/live instrumentation, save edits, deployment, external downloads, git staging/commit/push or publication.
- **Mandatory acceptance:** (1) bounded definition census with explicit exclusions and size/variant coverage; (2) native inventory/admission/capacity results with exact source evidence or precisely bounded unresolved items; (3) saved schema/object joins and a runtime/save matrix, including explicit coverage limits; (4) separately evidenced UI/native eligibility and chest comparison; (5) Transfer Container/cargo-pad storage-only treatment; (6) concise S2/deferred backlog boundary and answer-first report; (7) protected hashes, relevant regressions and audit evidence; (8) independent review ACCEPT and verified complete/task-only review package.
- **Optional acceptance:** extra variants, additional independent saves or small original offline probes that materially increase confidence without scope expansion.
- **Negative-result closure:** adequate bounded evidence can establish an identified field/path is not present in *examined representations*; cannot promote to universal absence. A candidate distinction that remains unresolved after agreed routes are examined is a scoped research result if its concrete missing discriminator is specified. Do not mark unperformed mandatory investigation as complete.
- **Continuation authority:** debug, correct and requalify in-scope failed tests without requesting a fresh brief; freeze acceptance criteria unless maintainer explicitly changes them.
- **Exit/escalation:** halt unsafe or unauthorized action, failed integrity/disk guards or genuinely missing essential inputs; record exact obstruction/attempts/resume point while pursuing other permitted work. Do not manufacture deadlines, arbitrary event/test quotas or more restrictive live run rules. If a later live test is recommended, request separate approval with a falsifiable outcome matrix.
- **Review artifacts/disposition:** mandatory PASS/FAIL/NOT TESTED matrix, evidence/source ledger, scoped claims and their confidence, preserved failures and regression cases, protected hashes, manifest/exclusions, status and exact patch checks, independent reviewer verbatim result and proposed commit subject. Maintainer reviews the diff before integration.
