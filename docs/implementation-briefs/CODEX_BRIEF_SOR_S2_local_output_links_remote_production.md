# Codex research brief — S2 local output links, redistribution and remote outpost simulation

**Project:** `starfield-outpost-research`  
**Type:** Bounded but substantive offline native/runtime-model and save-file research, with independent review  
**Status:** Proposed S2 investigation following accepted S1 storage/capacity work  
**Authority:** **Offline research only.** No Starfield launch, live capture, observer/plugin engineering or deployment, save creation/modification, original-input mutation, staging, commit, push or publication. A future live experiment needs an independently approved brief/run card.

## 1. Research objective and agreed boundary

Explain **how local outpost output links actually move items**, including the behaviour of linked extractors and fabricators at **remote / unloaded outposts**. Establish a coherent native mechanism and its save-file representation rather than merely cataloguing functions or producing an inventory-dumping tool.

This investigation includes the **production–transfer lifecycle** while the player is elsewhere: how production is scheduled, realized and conveyed through local inventories/links; how loaded versus unloaded registration or simulation affects it; and whether skipped time, travel and reactivation lead to catch-up, lost production, deferred realization or some other result. This is **new integration research**, not a reopening of the accepted E1–E3 production arithmetic, recipes or modifier findings. Reuse those findings as baselines and follow newly relevant paths far enough to explain the actual integration.

Study cargo-pad **local receiving/sending storage compartments and local output links**, but reserve inter-outpost transport, ship loading/unloading, flight schedules, remote deliveries/returns, inter-system He-3 freight logistics and the user's possible returning-freight spillover for the later cargo-link investigation. If transport and local redistribution share code, **identify and document the boundary and shared mechanism**; do not assume they are independent or omit a necessary local explanation. Do not follow the transport subsystem beyond the minimum needed to establish that boundary.

General chest/display storage, Shared Outpost Storage cross-outpost access, workbench crafting inventory and the outpost database's *Stored Resources* aggregation remain deferred. Ordinary chest link ineligibility is already established by S1; do not re-investigate absent a relevant contradiction.

## 2. Required sources and state preservation

First read `AGENTS.md`, `WORKFLOW.md`, `docs/EVIDENCE_STANDARD.md`, `docs/RESEARCH_EXECUTION_PROTOCOL.md`, `docs/templates/completion-contract.md` and the relevant registry/subsystem and permissions documents. Read the **current accepted S1 storage and capacity reports**, including `docs/experiments/storage/` native, saved, capacity, review and register documents, and E1/E2/E3 producer reports, especially `docs/experiments/inorganic-extractors/arithmetic-clocks.md` and production/link contracts. Use the actual current repository tree and verified paths; do not assume every historical path still exists. Cross-reference P1 power/activation only where it governs local transfer or production eligibility.

Use existing project-owned, pinned executable/ESM/Ghidra/native-export material and the protected save corpus under established permission and provenance rules. Check installed build and relevant source hashes; distinguish saved reference identifiers, remapped runtime FormIDs, handles and pointers. Preserve originals and previously accepted findings. Unparsed inventory extras are **unknown**, not empty. Reuse existing bounded readers and focused verification scripts only as evidence aids; **do not build a production logistics simulator, generalized save importer, inventory extractor or new instrumentation framework**.

Previously established S1 baseline (reverify exact source where relied on): dedicated storage has category admission and effective weight capacity; local redistribution limits requested units to a fitting quantity; certain producer/direct-add paths can exceed nominal capacity. Inventories and directed reference relationships are distinct persisted channels. These facts **do not yet establish** actual link routing, trigger order, transfer timing or remote operation.

## 3. Questions to answer

### A. Direction and identity of local links

1. Identify the native relationship, owner, source, destination, keyword/slot, link ordering and saved fields that define an ordinary local output link; distinguish construction/UI validation from actual runtime movement and from electrical/cargo relationships.
2. Establish whether ordinary local redistribution **ever moves items against the recorded edge**, and distinguish true reverse transfer from production, manual addition, source/receiver role switching, cargo returns, rejected insertions and other nonlocal writers. Give a positive bounded argument for ordinary one-way behaviour if supported; do not demand proof against all hypothetical engine features.
3. Distinguish eligibility for link construction from eligibility for transferring an individual item. Explain item filtering, source stock selection and receiver choice using the mapped native contracts.

### B. Redistribution and graph behaviour

Trace a complete **source item removal → destination acceptance/addition** path, including failure and partial acceptance. Answer: what triggers a transfer; how many units are attempted; whether transfer is atomic or staged; what remains upstream if space is exhausted; whether multiple eligible destinations compete in saved or runtime order; what happens with incompatible goods; and how zero remaining capacity is handled.

Examine chains, forks, merges and cycles. Determine whether intermediate storage relays items immediately or via later scheduled passes; whether repeated redistribution can occur in one call; and what controls reentrancy, visited references, cycle termination or work budgets. Do not infer routing simply because a graph permits an edge. **A full receiver is not automatically evidence of upstream reverse flow.**

### C. Scheduler and throughput

Identify transfer triggers (production-completion callbacks, inventory-change events, menu/player events, container activation, explicit Workshop update, periodic ticks, load/attach or other sources) and their relation to producer scheduling. Establish whether there is a distinct transfer scheduler; native timebase, cadence, per-event/batch limits and conditions for processing deferred work. Distinguish **attempt frequency**, **items transferred per attempt**, and **long-run throughput**. If the mechanism is event-driven, demonstrate this with actual caller/dataflow evidence rather than extrapolating from missing timers.

### D. Production and transfer when the player is absent — mandatory, not optional

This is a **central S2 deliverable**. Trace the relevant engine lifecycle from leaving an outpost/cell through remote registration, unloaded state, time passage (ordinary play elsewhere, wait/sleep and fast travel), return/attach and save/reload. Reuse E1–E3's global producer registry and elapsed callers but examine the missing **residency and transfer coupling**:

- What makes an extractor or fabricator eligible to continue producing while remote? Is it tracked by a global registry, simulated out of cell, deferred, or only realized on return?
- Does an unresolvable producer/reference accumulate pending work, drop cycles, or rebuild its state? Distinguish native bookkeeping from effective inventory creation.
- Can output links redistribute items while all their endpoints are remote/unloaded? If so, identify the native route; if not, identify whether stock accumulates at sources, transfers on return, or uses another mechanism.
- How do production deadlines, inventory capacity, local transfers and actual stored output interact during elapsed-time catch-up? Distinguish cached counters from materialized item deltas.
- Does a loaded/unloaded outpost change transfer semantics or only the timing of when the same operation is executed? Examine enough concrete branches to answer for ordinary inorganic extractors and fabricators; address organic producers where they share the mechanism, noting real differences.
- Which state is persisted (inventories, edges, producer timer rows, pending transfer work, ordered lists), and which runtime registries/queues are reconstructed? Can a save alone describe outstanding local redistribution, or only source/destination inventory snapshots and the graph?

Do **not** assume that remote production implies remote redistribution. Similarly, native elapsed scheduling does not prove that every unloaded reference stays resolvable or that all missed cycles are later materialized. Separate the ordinary **active but distant** condition from genuinely **unloaded/unregistered** references and skipped-time paths. Trace the actual predicates rather than using the player's physical distance as a substitute for engine state.

### E. Boundary objects and operational edge cases

Include local output buffers for inorganic/organic extractors, fabricators, dedicated storage, Transfer Container, fueled generators as incoming consumers where applicable, and cargo-pad inbound/outbound child containers. Establish which objects can source or receive ordinary local redistribution, whether unpowered/disabled/production-halted objects can still passively receive or forward stock, and how full producer buffers affect the next production attempt. Keep actual freight transport separate as above. Preserve identified interaction with manual inventory flows only when it changes interpretation of a local output-link result.

## 4. Runtime ↔ saved representation and evidence expectations

Produce an **object- and mechanism-level correspondence matrix** showing saved link identity/ordering, selected inventories/quantities, timer/pending state where identified, native readers/writers, loaded runtime registration and limitations. Select **real, positively identified** linked outpost examples from the existing protected corpus; independently join their owners, endpoints, item types and quantities wherever possible. Include full, near-full or overfull examples from S1 when relevant, but do not claim historical movement solely from a snapshot. Explicitly identify unknown or unsupported save representations instead of treating them as absence.

Provide a finite set of **worked native traces or controlled offline replays** for representative outcomes: one fitting transfer, partial/full rejection, a fork or multi-hop, and a remote/unloaded or skipped-time path. If a particular live timing or inventory transition cannot be demonstrated from existing offline evidence, supply the mapped mechanism and a **specific unresolved predicate** rather than fabricate a runtime measurement. Tests/replays must validate the traced native contract and disclose assumptions; a model that simply reproduces its own premises is not independent runtime evidence.

Use the existing evidence vocabulary (`PROVEN`, `STRONG`, `PROVISIONAL`, `OPEN`; `STATIC`, `SAVE`, `RUNTIME`, etc.) and answer-first style. Present the strongest supported **ordinary-case** conclusion, its version/object scope and why it is sufficient. Do not treat merely conceivable unexamined paths as equally supported counterhypotheses. **STRONG with a specific material gap is usable engineering knowledge**; do not automatically expand into a live observer to eliminate it.

## 5. Explicit stopping and escalation rules

This brief authorizes a **substantive exploration** of previously unmapped remote production/redistribution, not a superficial fixed-count scan. Follow relevant native call/dataflow chains until the agreed scientific questions have meaningful answers or a concrete, demonstrated boundary. Do not stop after a preliminary function list or return “unknown remote behaviour” without investigating registered producer states, load/attach paths, actual redistribution triggers and relevant save persistence. Conversely, do not chase unrelated engine internals or cargo transport indefinitely merely because they are reachable.

Where positive evidence provides a sufficient causal explanation, accept it under **reasonable engineering confidence**; apply explanatory sufficiency/burden of evidence, as agreed during P1. An absence claim requires bounded coverage of the actual relevant dispatch/writer paths, not a failed search. Separate **completion of this bounded offline research assignment** from universal runtime proof, general model completeness and future live validation.

If the remote mechanism truly cannot be discriminated offline, document: paths tested, exact missing state/observability, competing predictions, evidence value and cost of the *smallest* proposed test. **No live experiment or observer construction is authorized.** A finding may call for a later targeted live experiment, but must not silently create an instrumentation prerequisite or overstate impossibility.

## 6. Required deliverables

1. **Answer-first S2 report**, in `docs/experiments/` following existing layout, covering local direction, timing, routing, fullness, integration and remote/unloaded behaviour. Include plain-language conclusions distinct from long technical derivations.
2. **Native contract and function register** with verified build pins, exact VA/RVA conventions, source–destination inventory mutation path, triggering/scheduling dataflow, remote registration and save/load lifecycle; document significant alternatives and counterexamples.
3. **Save/runtime correspondence** with real linked examples, provenance, boundaries, sample evidence and an explicit inventory/edge/elapsed-state matrix.
4. **Remote outpost lifecycle analysis** that separates active-distant, unloaded/unresolvable, wait/sleep, travel, catch-up and return, and accounts for extractor/fabricator production **and local transport** in each supported case. This deliverable may not be silently deferred wholesale to a future topic.
5. **Specific full-container, branch/chain/cycle and partial-transfer conclusions**, with minimal worked examples and no unsupported reverse-flow or freight-return attribution.
6. **Updated durable research state**, hypotheses/decisions/backlog and S3/cargo-boundary notes where warranted; preserve and link existing S1 and E1–E3 results, do not rewrite history or claim a product-ready logistics planner.
7. **Reproducible offline checks and provenance**, source/permission/rights classification, protected-input pre/post hashes, regression results and recorded failures; no original/save/Ghidra database mutations without separate authority.
8. **Independent review against the frozen brief and actual evidence**, mandatory PASS/FAIL/NOT TESTED matrix, reviewed corrections, no invented approval, `git status`, file/exclusion manifest, and task-only/complete diff exports with exact forward/reverse applicability and completeness checks under `.local-work/`. Identify supplied untracked brief separately. Suggest a conventional commit subject for maintainer review. No stage/commit/push.

## 7. Compact completion contract (governing)

- **Task type:** Bounded scientific research and documentation; offline deterministic checks may be developed as evidence aids.
- **Question/deliverable:** Explain ordinary local link movement and remote production/redistribution, with supported runtime/save correspondence as specified in §3–6.
- **Scope/authority:** Existing source/evidence read and bounded owned tooling only. Protect proprietary binaries, originals, save corpus, databases and Git state. Preserve existing project C:/D: free-space and data-integrity safeguards. No live/process access, deployment, save writer, staging, commit or push.
- **Mandatory acceptance:** All eight deliverables above, including meaningful remote-production/transport investigation; accepted scientific unknowns must have explicit investigated boundaries. Fix in-scope failures before final submission. Review the original frozen criteria; no retrospective lowering.
- **Optional:** Independently useful additional examples or diagnostics confined to scope; never substitute extras for missing mandatory work.
- **Negative-result closure:** Supported bounded negatives may be accepted when established through actual paths and appropriate controls. Unobserved runtime effects must not be invented as negative evidence.
- **Continuation:** Investigate and remediate within this assignment; diagnostic corrections and reruns do not require a new brief. Material scope/criteria changes require maintainer approval and a dated amendment.
- **Escalation:** Stop prohibited actions on an actual authority, safety, identity, inaccessible essential-input or resource blocker; preserve checkpoint, receipts and precise minimal request. Do not classify an unresolved but reachable native branch as an external blocker.
- **Review/disposition:** Follow `docs/RESEARCH_EXECUTION_PROTOCOL.md`, `WORKFLOW.md` and the independent reviewer procedure; report scientific confidence, assignment completion, live coverage and publication/rights status separately.

**Desired endpoint:** A practical, defensible explanatory model of **what moves locally, when and why**, including the case in which a producing outpost is remote or unloaded. Leave remote cargo shipments for the later phase, but do not leave remote *local* logistics unexamined.
