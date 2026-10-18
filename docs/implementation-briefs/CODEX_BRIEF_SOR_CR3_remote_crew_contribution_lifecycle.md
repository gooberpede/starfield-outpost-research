# Codex research brief — CR3: Remote crew contribution, assignment lifecycle and restoration

**Project:** `starfield-outpost-research`  
**Task:** Bounded offline native/definition/save research, durable documentation and independent review  
**Authority:** Read-only examination of permitted local game definitions, shipped scripts, native analysis and protected existing saves. No game launch, live instrumentation, save mutation or creation, deployment, third-party acquisition, staging, commit or push. Retain and respect project permission, provenance, free-space and protected-input controls.

## 1. Objective and required conclusions

CR1 established recruitment, per-destination capacity, assignment, Crew screen population and positive current saved actor-to-ship/outpost relationships. Its corrective mature-save investigation demonstrated reciprocal actor `Extra4C` / outpost `ExtraE2` assignments and positively saved unassigned roster entries. CR2 established selected crew perks and ranks, their actual entry-point/consumer semantics, and distinct stacking/precedence rules. **CR3 must now explain when a crew member's assigned contribution is operational, how it changes through loading, reassignment, absence and return, and how current runtime state follows from persistent inputs.**

Begin the final report with a concise answer-first matrix covering:

1. Does a crew member need to arrive physically, have loaded 3D, or merely be assigned and resolvable for each applicable outpost bonus?
2. When does assignment, reassignment or removal become effective for modifier evaluation and cached production clocks? Distinguish immediate logical effects from later observable output.
3. What happens while the player is remote, during ordinary frame progression, explicit wait/sleep, fast travel, and save/load?
4. Which saved assignment, perk-rank and contributor records reconstruct the active crew participant set after loading? What is computed, cached, or transient?
5. How do **named crew (Lin and Heller)** compare with **assigned generic Outpost Specialists**, including their template/perk resolution, participation and any lifecycle differences?
6. What specific loss/recovery conditions apply to disabled, incapacitated, dead, unassigned, unresolved or replaced actors?

Choose the best-supported ordinary mechanism at **reasonable engineering confidence**. A bounded supported result is acceptable without a universal execution trace. Do not promote a merely possible native path into a witnessed historical event; conversely, do not place imaginary alternate mechanisms on equal footing with positive native and saved evidence.

## 2. Starting references and evidence selection

Read `AGENTS.md`, `WORKFLOW.md`, `docs/RESEARCH_EXECUTION_PROTOCOL.md`, `docs/EVIDENCE_STANDARD.md`, and relevant CR1/CR2 documents, notably:

- `docs/experiments/crew/report.md`, `current-assignments.md`, `current-review.md`, `screen.md`, and assignment/capacity/native documentation;
- `docs/experiments/crew-skills/report.md`, `lifecycle.md`, `native.md`, `stacking.md`, `processes.md`, `population.md`, and their review/source ledgers;
- E1 producer scheduler and crew stacking contracts, S2 remote production/reference-resolution findings, and P1/C3 only where an actual crew contribution reaches them.

Verify build/version, native source pins, supplied saves and existing contract state rather than extrapolating offsets. Reuse existing owned readers only as bounded evidence aids; this is not an importer or general decoder assignment.

**Corpus rule:** Choose evidence by the state required, not convenience. HIST-0255 / Save41 supplies named Lin/Heller assigned to the same outpost with positive saved rank evidence, but is not a universal sample. Search the wider catalog of earlier mature saves for **positively assigned generic Outpost Specialists** (including Engineering/Management/Security where present), rather than relying on Save52 or on generic NPC definitions alone. Require actual actor identity, resolved assignment destination and type/template evidence, and selected skill/rank evidence where serialized or definition-backed. Favor contrasting witnesses and negative controls. A generic actor's template candidate alone is not a verified effective specialist class. If no qualified generic assignment exists after a bounded positive-led search, retain that specific evidence gap, trace its mechanism as far as authorized, and specify the minimal additional witness needed; do not silently substitute Lin/Heller or declare generic contribution nonexistent.

## 3. Investigation A — assignment and contributor lifecycle

Trace the relevant native/script chain from recruitment or existing assignment through owner `ExtraE2`, actor `CrewAssignment` (`Extra4C`), skill/rank registration, contribution dispatch and actual consumer evaluation. Identify event ordering and whether registration changes require actor arrival, actor handle resolution, physical process/3D, or an assignment refresh. Trace unassignment, transfer to ship/other outpost, dismissal and removal from the old destination; check stale/duplicate contributors and correct removal of stacked effects.

For meaningful ordinary process examples (inorganic extraction and manufactured fabricators), follow the selected actor/rank from source into **effective modifier** and then the elapsed scheduler. Distinguish freshly evaluated modifiers from cached interval/countdown values; show exactly when an existing production row adopts a changed rate. Reuse CR2's semantics, do not reopen its perk catalogue.

## 4. Investigation B — remote, unloaded and exceptional actors

Distinguish these states rather than conflating them: assigned and en route; arrived; actor/3D unloaded but handle resolvable; actor handle not resolvable; disabled/dead/incapacitated; assignment target unregistered; crew-member link retained but contribution invalidated. Trace actual predicates, listeners, caches, handle-generation checks, and re-registration paths. Follow AI or movement dependencies **only as far as they change contribution eligibility**; do not expand into general companion behaviour.

Connect each state to S2's registered/resolvable outpost scheduler, including frame elapsed, wait/sleep and travel/skip. Explain whether a distant outpost may still receive crew modifiers, how a temporarily unresolved actor affects the calculation and whether a re-resolved actor automatically re-enters contribution evaluation. Identify any condition under which old modifiers could linger or temporarily disappear; do not allege a gameplay bug without demonstrating a reachable causal case.

## 5. Investigation C — persistence and load reconstruction

Map saved assignment + selected perk ranks + any separate contributor lists or effect registration, then the actual native post-load fixups and consumers. Establish where runtime handles, actor membership, selected rank and cached modifier values are created or restored, and the order constraints required for ordinary correctness. Differentiate saved facts, definition-derived defaults, reconstructed state, runtime-only state and merely proposed effects.

Use the Lin/Heller positive assignment/rank pair, at least one qualified **assigned generic Outpost Specialist** when available, and a real nonmember/unassigned or ship-assigned contrast. Show an end-to-end, independently grounded saved-instance -> participant -> qualified effect path for both named and generic cases, with precisely scoped UNKNOWN for any unproven historical load-time execution. Compare script grants and templates with explicit saved-rank overrides and native selection; never read an absent saved rank as zero.

## 6. Comparison and handoff

Provide a compact matrix by actor/state, consumer, modifier and observable consequence, distinguishing (a) assigned, (b) eligible, (c) currently contributing, and (d) actually realized production. Revisit the CR2 concrete examples as conditional calculations only where needed to establish lifecycle. Include a **short robot handoff** identifying shared actor/assignment/effect registration mechanisms and verified differences, without commencing comprehensive robot investigation. Ship-assigned crew are a necessary counterexample/eligibility boundary, not an invitation to reverse-engineer the full ship-skill system.

If further questions remain, list **exact missing evidence and materiality** and what observation would discriminate them. No automatic observer build, live test, plugin or broad AI project. Do not resurrect resolved E1/CR2 questions without a concrete contradiction.

## 7. Deliverables and acceptance contract

**Task type:** Bounded offline research hypothesis, deterministic native/save reconstruction, and documentation.

**Mandatory criteria (freeze before work):**

1. Answer-first, plain-English conclusion separating assignment, physical presence, participant eligibility, effective modifier and actual production.
2. Grounded native/source trace of assignment-to-effect registration, activation, removal and effect/clock refresh semantics.
3. Positive remote/unloaded and failure/recovery mechanism analysis, differentiating graphics residency, handle lookup, physical arrival and actor state; frame/wait/travel comparisons.
4. Explicit save-to-runtime reconstruction and provenance for assignment, rank, effective contributor selection and cached runtime data, with supported positive and negative controls.
5. **Named versus generic comparison:** Lin/Heller plus a substantial search for real **assigned generic Outpost Specialist** witnesses from earlier mature saves; identity/template/rank/assignment validation where supported. Preserve precise search coverage and any unresolved positive-sample dependency.
6. Worked subsystem examples and concise robot handoff without broadening to ship/robot/AI investigation; negative skill/availability claims must have real bounded evidence.
7. Durable report, native/save provenance, function/source register, corpus selection ledger, check receipts and updates to `RESEARCH_STATE.md`, `DECISIONS.md` / `BACKLOG.md` only where warranted; preserve previous results and corrections. All authored text UTF-8/LF, relative links, encoding audit.
8. Independent review against original contract and primary evidence, mandatory PASS/FAIL/NOT TESTED matrix, reported failures, protected-input hashes, tests and exact task-only/complete patches, including untracked text and supplied brief. Confirm forward and reverse byte-exact reconstruction and manifest; suggested Conventional Commit message. No staging or sync.

**Negative-result closure:** A carefully bounded native negative is useful if actual consumer and lifecycle paths are covered and a credible explanatory model is presented. Mere absence of a pattern in Save52 or a narrow arbitrary save subset is not a negative. A missing essential generic witness after serious corpus search is disclosed as a specific limit, **not** a fictitious positive. The task may conclude with a STRONG ordinary mechanism and precisely delimited sample gap if independently reviewed under the frozen criteria; it may not claim universal generic runtime validation.

**Continuation authority:** Diagnose and correct in-scope failed analyses and tests; do not stop at the first decoder/locator obstacle. Preserve failed evidence. Material changes to criteria require maintainer approval.

**Exit/escalation:** Stop prohibited actions, protect inputs, and request narrowly specified authority/data only when genuinely necessary. Honor both-drive free-space/integrity/worker guards under `WORKFLOW.md`; do not invent arbitrary scientific time or record-count ceilings. No live/game operation, save editing, instrumentation or Git mutation is authorized.

**Review disposition:** Independent reviewer returns ACCEPT, REWORK or ESCALATE per project protocol. Separate scientific confidence, assignment completion and publication readiness; implementation of a practical crew tool is not part of this brief.
