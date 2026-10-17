# Codex research brief — S1 follow-up: capacity, inventory state and insertion semantics

**Project:** `starfield-outpost-research`  
**Type:** Bounded offline native/runtime-contract and saved-state research, documentation and independent review  
**Authority:** Offline only. No Starfield launch, live observer, save editing, deployment, third-party downloads, staging, commit or push. Preserve all protected game/save/database inputs.  
**Relationship:** Completes the semantic prerequisites left open by the committed S1 storage and eligibility research; it is **not** an inventory-extractor implementation task and does **not** reopen the accepted historical S1 review.

## 1. Objective and decision standard

Establish how Starfield **actually determines the occupied capacity, remaining capacity, fullness, and eligibility for an incoming item/quantity** for ordinary outpost inventories, and connect those native runtime rules to **actual saved contents** in representative real containers. Provide enough evidence that S2 can study full destinations, partial deliveries and backpressure without guessing at storage semantics.

**Answer first, in ordinary language:** For a specified container and candidate item stack, what data determines (a) whether the item is permitted, (b) how many units fit, (c) whether a request is wholly/partially accepted or rejected, and (d) how each result is represented or observable in running-game structures and persisted saves? Separate proven rules from unsupported assumptions. A nominal 75/150/300 capacity is **weight capacity**, not an item count.

Use the project's **scoped reasonable-engineering-confidence** policy: a coherent native mechanism corroborated by representative saved examples is sufficient for an accepted ordinary-case explanation. Require concrete contradictory evidence to expand into hypothetical alternatives; do not demand universal parsing or live observation for a bounded native/save model. Conversely, do not turn an unsupported parser branch into a claim of emptiness or fullness. Distinguish assignment completion from scientific confidence and live validation.

## 2. Sources and previously established facts

Read `AGENTS.md`, `WORKFLOW.md`, `docs/EVIDENCE_STANDARD.md`, `docs/RESEARCH_EXECUTION_PROTOCOL.md`, `docs/templates/completion-contract.md`, and the committed S1 files `docs/experiments/storage/{report,native,saves,review}.md`, `catalogue.csv`, `functions.csv`, `sources.csv`, and `research/s1-storage/README.md`. Reuse relevant E1–E3 producer/output models, pinned executable/ESM and protected saves. Verify current build hashes, actual paths and primary native evidence before extending it; reuse project-owned tooling only as bounded evidence readers.

S1 already established that dedicated ordinary Solid/Liquid/Gas/Warehouse bases have nominal capacities 75/150/300, item-class filters, multi-item stocks, and linked reference-owned inventories. It sampled actual counts, including H36 small solid `ff018b64` (MISC `00557f` ×150), gas `ff018b66` (`00557c` ×150), liquid `ff018b61` (`0057df` ×94), mixed warehouse `ff02c339` (two item types), empty rows, producer buffers and cargo inventories. The corresponding inventory representation supports ordinary zero-stack-extra rows; some nonempty stack extras and leading reference extras remain unsupported. Native CarryWeight overrides/modifiers may change the **effective** capacity. S1 has **not** validated current loaded stock or comprehensive effective-capacity calculations. Preserve these distinctions and original citations.

## 3. Investigation A — runtime capacity calculation

Trace the **actual native capacity path** for relevant ordinary Workshop CONT references, identifying with verified function addresses and dataflow:

1. Source and units of base capacity; which effective CarryWeight/other AVs, reference modifiers, perks, keywords, transient states or overrides actually affect the capacity used by the relevant inventory insertion path. Do not import the ordinary actor carrying-capacity model without proving its use.
2. Source of item weight/mass, stack signed quantity and modifiers; treatment of mixed item forms, fractional weights, zero/negative values if applicable, and representation/rounding/comparison boundaries when close to full.
3. Whether current occupied/available capacity is calculated from contents on demand or cached, and whether a persistent **full** bit/status actually exists. If cached, identify invalidation and the scope of the cached result.
4. How capacity interacts with category filters (`ONAM` and native keyword checks), and where type rejection differs from capacity rejection.

Report an executable-in-principle **formula/decision procedure** backed by traced native operands. If different interfaces use different calculations, identify the relevant native paths and boundaries instead of publishing a fictitious universal rule.

## 4. Investigation B — insertion and partial-fit behaviour

Follow the **actual ordinary inventory receiving operation** far enough to determine what happens when adding a requested quantity to a compatible destination with:

- No remaining capacity.
- Enough space for only part of the requested stack.
- Enough space for the entire requested stack.
- Free capacity but a category-incompatible item.

Identify whether the actual result is all-or-nothing, limited to a fit quantity, or conditional on the operation/caller. Ground this in code that performs, admits or refuses the insertion, not merely a helper that computes theoretical fit. Explain what is returned to the caller and what, if anything, the sender can infer. Where the mapped **generic container** insertion differs from **output-link-delivery** admission, preserve that distinction; S2 still owns sender routing, retries, redistribution and reversals. Distinguish manual UI transfer or forced/script insertion as *separate, bounded cases*, mapping only the minimal relevant difference when required to avoid a false generalization.

## 5. Investigation C — real saved inventories and capacity reconstruction

Using existing protected historical saves and the owned reader as **research instruments, not production software**, demonstrate the native capacity model on a small, diverse selection of **identified real reference-owned inventories**:

- At least one ordinary dedicated solid, liquid or gas container and one warehouse (ideally mixed contents).
- An empty or clearly underfilled comparison.
- **At least one demonstrably full or capacity-constrained container** if the available corpus provides one. Check known S1 sample candidates first; do not assume that `item count = capacity` or that a chosen container is full.
- Where evidenced and relevant, one producer output buffer or cargo child to establish which capacity rule carries across classes.

For each chosen example, give saved reference identity and base, item forms and counts (resolved to weight definitions), base/overridden effective-capacity inputs, computed occupied weight, free capacity, prospective fit of a named compatible item, and applicable qualification. **Do not label an unknown override as zero.** Use exact form IDs, pinned definitions, source locations, and explicit calculation receipts; include mixed-item arithmetic and comparison with the native branch thresholds. Determine whether the relevant values are *saved*, *definition-supplied*, or *runtime-dependent*.

If the existing corpus lacks a qualified full/capacity-boundary case, make a **genuine, bounded search** of the available protected corpus and provide a negative coverage inventory and a precise minimal future controlled-save/player observation. Do not manufacture a “full” witness or silently weaken this mandatory objective. A genuinely unavailable controlled witness is an evidenced **ESCALATE** for that evidence need; finish all independent offline semantics in the same assignment. An incomplete parser branch is a research problem: pursue bounded native grammar extension *only as necessary* for a selected substantive witness, without building a universal dumper.

## 6. Runtime/save correspondence and S2 handoff

Produce a concise matrix for each supported class/condition: native inventory owner; effective-capacity function/input; admission and partial-insert rule; saved inventory/change-state field(s); whether contents and capacity can be reconstructed at save time; and what can diverge after load. Clearly separate **current live inventory inspection interface exists/identified** from **actual running-game values measured**—no live run is authorized. Identify the minimum information that S2 must observe to discriminate **full**, **partially accepting**, **category-rejected**, **temporarily unavailable**, and **empty/nonexistent/undecodable**.

Keep cargo shipping/return scheduling, local link traversal, multi-hop routes, producer timing, Shared Outpost Storage, ordinary chest/display general research and the database's `Stored Resources` aggregation out of scope. Mention inherited facts only where they clarify receiving-inventory contracts.

## 7. Deliverables and explicit completion contract

**Task type:** Bounded semantic/native/save research; documentation only, with small disposable evidence readers/tests if indispensable.

**Mandatory acceptance (freeze before work):**

1. **Answer-first report** distinguishing occupied/full/capacity-limited/category-rejected and summarizing ordinary-case conclusions at `PROVEN` / `STRONG` / `PROVISIONAL` as appropriate, with concrete coverage.
2. **Verified native calculation** of capacity and occupied weight (including effective overrides where the examined caller supports them), data types, comparison/rounding and whether a full status is derived or stored.
3. **Actual insertion semantics** for entire fit, partial fit, full and incompatible items; if distinct paths differ, show relevant branch boundaries and precisely unresolved entry points rather than claiming an unsupported global rule.
4. **Actual saved-container calculations** for representative dedicated stores plus mixed warehouse and empty/underfilled control, with item mass definitions and provenance. A full/boundary witness is mandatory **if available**; otherwise deliver an audited bounded negative search and exact evidence prerequisite, and do not claim it was tested.
5. **Runtime-to-save matrix and S2 handoff** identifying which values are persisted, rebuilt or effective only after loading, and which real-world capacity/acceptance observations S2 will need.
6. **Preserved history, scope and permissions:** integrate a new completion report/review into `docs/experiments/storage/`, append warranted updates to state/decisions/backlog/functions/sources, retain accepted S1 results, do not reinterpret a failure to decode as an empty inventory, and avoid a general inventory dumper or writer.
7. **Evidence and independent review:** fresh pinned source hashes and checked actual native instructions, relevant regression/independent calculations, protected pre/post hashes and disk guards, actual independent ACCEPT/REWORK/ESCALATE per project protocol. Report failed paths and corrections; do not retroactively adjust acceptance criteria.
8. **Complete review package:** task-only and complete text diffs (including untracked authored text), path/status and exclusions manifest, whitespace/links/encoding audit, exact forward/reverse reconstruction verification, and proposed Conventional Commit subject. No staging/commit/push.

**Negative-result closure:** A defensible ordinary-case model may be `STRONG` without universal exceptions. A specific inaccessible essential save witness or genuine unsupported native dependency must be described with exact efforts and a narrow escalation; absence of exhaustive proof is **not** a blocker. A discovered in-scope error must be investigated/corrected/retested under the same assignment.

**Continuation authority:** Authorized offline diagnosis, focused native inspection, reuse/adaptation of local evidence readers and tests, corrections and requalification within this contract. No game launch, installation, new save generation/editing, observer build, live memory access, external network contact or Git staging/commit/push. No speculative expansion into other subsystems.

**Exit/escalation:** Stop on protected-input integrity/identity failure, failed disk safeguards or genuinely inaccessible essential evidence; retain receipts and request only the minimal required operator action. Do not add arbitrary time/evidence quotas or re-scope silently. Submission requires all feasible mandatory criteria, an explicit classification of any genuinely blocked evidence-specific criterion, and independent review against this frozen contract. The maintainer determines whether any blocked empirical boundary needs a separately approved live case.

**Review artifacts:** Criterion-by-criterion PASS/FAIL/NOT TESTED matrix, exact source/evidence ledger, test outputs, failed paths, provenance and exclusions, peer review decision, snapshot-bound diffs and checksums. Scientific disposition is separate from assignment completion and publication classification.

## 8. Success condition

A reader should be able to take a supported saved outpost storage reference, determine **what it contains**, calculate **occupied and available weight** according to the mapped native rule, and explain **what an attempted insertion would do** at/near capacity, without confusing saved state with current runtime state. An unresolved exceptional representation must be clearly scoped; it must not automatically cause further tooling work or prevent use of a well-supported ordinary-case model.
