# RG2-D5AA — Resource-generation chronology from Save52 load to Feynman V arrival

**Repository:** `D:\Projects\starfield-outpost-research`  
**Assignment:** Offline native-event chronology and gameplay-transition research; no live run authorization  
**Parent:** D5R ordinary construction-query winner remains OPEN; D5X-B1 target first construction remains unobserved. D5Z visited-state findings are a prerequisite, not an inferred B1 history.  
**Reference case:** Load protected Save52 with player at the Lodge interior; direct ordinary fast travel to **Feynman V Cu IL F**. Target source key `0:37536:20928:0029d20e` (verify against current durable records).

## 1. Controlling question and completion rules

**D5AA-CQ:** Starting with the ordinary empty visited state during Save52 full loading, establish the actual event ordering and causal conditions by which selected resource sources first pass the unvisited gate, undergo cache lookup/construction or bypass, are marked visited, and are subsequently bypassed, across the Lodge load, travel initiation, destination streaming and arrival. **Recover the strongest possible B1 chronology from retained native evidence, and independently map the game's player-action-to-demand path.** The desired historical target first event must not be replaced with a generic explanation or a different source's event without an explicit distinction.

Freeze the following controlling questions and their required result scope before investigation:

- **D5AA-Q1 — Retained B1 chronology:** What source-level first-processing/append/bypass sequences can actually be authenticated from B1, with native event timing, scope, provenance, identity and loss bounds? For the target, was its first processing recorded? If not, why not and what exactly is absent? Use other sources as controls, **not substitutes**.
- **D5AA-Q2 — Save-load/Lodge boundary:** What ProcGen reset and generation-demand events can occur during or after Save52 full load while the PC remains inside the Lodge? Is an exterior Jemison source-demand route reachable via interior-linked cells, context initialization, preload or another mechanism? Demonstrate positive native call chains/predicates or a bounded negative; do not assert Lodge-to-Jemison loading without evidence.
- **D5AA-Q3 — Fast-travel causality:** Which native actions initiate destination context acquisition, landscape/grid streaming and source demands, and how do they relate to travel confirmation, loading-screen period, arrival and subsequent movement? Distinguish necessary ordering constraints from asynchronous scheduling and observed events; map the earliest eligible target demand, if provable.
- **D5AA-Q4 — Firstness and visited transitions:** For a specific source, distinguish original query, selected source, visited comparison, source-map hit/miss, generation/sampler, attempted and successful visited append, later bypass, retirement and reset epochs. Establish sufficient evidence for a *complete* ordinary source chronology; test available B1 controls. Do not infer append success solely from its call-site reachability.
- **D5AA-Q5 — Next discriminating evidence:** Which **specific** missing observed boundary or native correlation prevents target attribution and first-query/mask determination? Can the existing evidence and offline native analysis resolve it? If not, specify the minimum observer capability and loss-control validations necessary for a future separately authorized run, without implementing or executing that run by default.

Apply `docs/RESEARCH_EXECUTION_PROTOCOL.md`, `docs/EVIDENCE_STANDARD.md`, `docs/EDITORIAL_STANDARD.md`, reviewer instructions and `docs/templates/completion-contract.md`: question-level **COMPLETE / INCOMPLETE / BLOCKED**, independent challenge and original-criteria adjudication. A completed offline *feasibility* result or other-source chronology does not close the target historical question. Continue material authorized leads under this assignment; if historical data have irrecoverable loss, state that as a scoped factual limitation and complete the separately answerable native causal map rather than claiming historical reconstruction.

## 2. Starting evidence and constraints

Read and verify latest committed `AGENTS.md`, `WORKFLOW.md`, `docs/SAVE_PROTECTION.md`, D5Q/D5R/D5S/D5V/D5W/D5X, the full B1 records, D5Y and D5Z, and especially the committed `docs/experiments/resource-retained-population/resource-generation-gameplay-checklist.md`. Retain its **31 entries and five gameplay headings**; do not invent new completed ticks or erase open questions. Inspect all existing B1 local-only raw/authenticated receipts, checkpoint QPC clock/frequency, path reporter, D5Y alias and queue-forensic methods, D5Z reset certificates and writer census, and their original evidence. Confirm version/build fingerprints and static/runtime address translation; baseline Starfield **1.16.244.0** unless verifiably updated. Do not infer from summarized counts where raw record-level checks are possible.

Known baselines to verify: provider `0x14079f860`, source selection `0x14079fa90`, visited decision `0x14079fc37..0x14079fcd4`, protected pointer-map lookup and generation near `0x14079fdf9..0x14079ff18`, visited append near `0x14079ff3e`, ProcGen reset `0x14079ddf0`; all are preferred static VAs, not runtime addresses. D5X-B1 retained **19 authenticated ordinary sampler paths on non-target keys**, 24 authenticated source-map decisions (19 misses / 5 hits), and **9,957 queue-full record losses**; D5Y's **119 target-compatible visited bypasses** rely on geographic/frame assumptions and lack copied positive target identity. D5Z identifies **two qualified empty-state reset certificates** but does not establish an uninterrupted source history from them to the later bypasses. Verify these bounds and correct discrepancies explicitly.

The owner reports Save52 loads inside **the Lodge**, followed by direct ordinary fast travel to **Feynman V Cu IL F**. This is an operator account, not an event timestamp. Distinguish phase checkpoints (main menu, loaded/not travelled, first arrival) from native transition instants. The 110 pre-travel admitted-record watermark alone does not prove no source event occurred: analyze its contents and recorder activation scope. No target first-event attribution from pointer alias alone.

## 3. Mandatory work

### A. Recover exact retained B1 event ordering

Build or reuse an offline event-correlation pipeline operating on preserved original records, with reproducible commands and read-only source validation. Reconcile sequence numbers, thread/invocation/request IDs, epochs, source identities, pointer aliases and lifetime limits, relative QPC timestamps, phase checkpoint time **intervals**, writer ACK/flush bounds, drops and reset fences. Explicitly test if each displayed event order is strong native order, thread-local order, interval order or just archival order. Never place unknown dropped events at invented times.

Search for **complete source examples**: last qualified empty/reset state (if observable) → selected source and identity → unvisited → pointer-map decision → construction/sampler or legitimate non-construction path → *successful* visited append → subsequent selection and visited bypass, with source identity and epoch/lifetime held constant. If no exact example exists, document which edges are absent and determine whether other non-target partial examples can be correlated. Analyze the 19 full ordinary paths and 24 cache decisions individually; find positive first/next evidence, including counterexamples (e.g. prior visited, cache hit, invalidated lifetime). Identify target-compatible selection observations and whether a positive descriptor could ever be copied before bypass. Inspect the 110-record pre-travel prefix and recorded resets specifically for any Jemison/exterior or Feynman activity, without negative claims from a partial instrument.

Produce a **machine-readable event ledger** with raw source refs, exact identities where known, absolute/relative timestamps and clock provenance, confidence, phase interval, record loss exposure, correlation rule, and unresolved edges. Keep raw native evidence local; summaries must cite reproducible pointers into it.

### B. Native player-action → ProcGen causal mapping

Trace **both directions**: from Save52 full-load and Lodge interior context through possible exterior-linked cell/world tasks; and backward from source demand/provider via landscape source-grid, descriptor and streaming schedules to the actual game-triggering call sites. Do not rely on UI labels or generic statements that travel "streams the destination". Investigate fast-travel confirmation, transition initiation, owner/component switch, destination grid preparation, task registration/worker execution, player arrival, and ordinary post-arrival demands. Establish guard predicates, relevant callbacks/queues, ownership and what can execute in parallel; check whether the resource source may be processed before the visual arrival or during interior residency. If an edge crosses an unexamined module, follow it within the offline scope.

Create a native transition table with player-visible milestone, actual initiating function/caller, native predicate, state precondition, possible resource effect, minimal/maximum provable relative ordering, independent static/runtime proof and remaining uncertainty. Cite executable hash, source offsets/address ranges and exact evidence. Treat "can happen" separately from "did happen in B1". A code-possible Jemison precursor does not prove a Jemison request in Save52; a missing B1 record does not disprove it.

### C. Visited/cache/reset state correctness

Integrate D5Z's empty full-load visited state and reset certificates with resource demand scheduling, scope/epoch and worker overlap. Clarify *precisely* when an unvisited check sees earlier marks, whether concurrent first-lookups can race or are ordered by the verified lock contract, whether append may fail, and how subsequent resets/retirement alter the interpretation. Compare the actual visited bypass with the alternative source-map hit and prior density aggregate reuse. Establish the minimum valid state sequence for the target and for separately evidenced examples, with edge labels **OBSERVED / PROVEN STATIC / CONDITIONAL / UNKNOWN**. Do not assume direct persistence of visited entries, successful generation after a visit mark, or automatic target generation on any particular milestone.

### D. Gap closure and future live-readiness *recommendations only*

Before recommending new instrumentation, exhaust recoverable B1 evidence and feasible static tracing. If target historical first processing is still not recoverable, name exactly what is missing: e.g. positive source identity before visited bypass, complete reset-to-first event record, timing/epoch join, loss-free sample or direct append witness. Propose the narrowest observer improvements and offline validations: safe identity capture from stable lifetime context **without unsafe pointer dereference**, bounded timing/correlation if required, queue-size changes such as 8,192 or 32,768 **evaluated by tests not assumed successful**, worker throughput/wake/flush diagnostics as warranted, and retention of global reset/firstness events. No blind target filtering or inference that larger capacity proves capture completeness. Estimate memory and concurrency cost where evidence allows. **No code modification, observer build/deploy or live test** under this brief unless separately requested and authorized; design suggestions are not implementation authority.

### E. Checklist and durable visuals

Update the **existing** 31-item gameplay checklist in place only where independently justified; preserve all items and grouping, and state B1-observed versus native-path-mapped separately. A newly mapped caller chain may support a native-mechanism tick but not an actual gameplay chronology tick. Add stable links to the D5AA report and evidence. Do not turn historically unknowable target firstness into a checked item.

Create (1) a **B1 event chronology SVG** with phase/checkpoint interval and lost-record exposure, exact observed points and separately styled unknown events; (2) a **save-load/Lodge → fast-travel → Feynman arrival causality SVG** separating code-supported possible/required order from historical runtime confirmation; and (3) a **one-source state-machine SVG** (unvisited, map hit/miss, sampler, append success/failure, visited bypass, reset, retirement) with explicit observation/unknown styling. Include reproducible machine-readable backing tables/scripts; no invented event times or spatial coordinates. Native geographic figures, if any, use actual documented native axes and outpost centre/boundary.

## 4. Deliverables

Use `docs/experiments/resource-retained-population/` with established conventions:

- `d5aa-report.md`: direct answers Q1–Q5, negative results and qualification; explicit section **"What B1 did and did not establish"**.
- `d5aa-b1-chronology.md` and machine-readable derivative event/phase table (sanitized; raw remains local).
- `d5aa-gameplay-transition-map.md`: precise native caller graph, guards, order and source links.
- `d5aa-investigation-ledger.md`: started early; evolving hypotheses, edges, counterexamples, omissions and continuing actions.
- `d5aa-sources.csv`: static offsets, exact decomp/disassembly provenance, hashes, B1 record/receipt and verification pointers.
- `d5aa-decision.md`: sufficiency versus remaining parent science, best-supported next step and minimum capability if missing.
- `d5aa-review.md`: original question/criterion-by-criterion independent completeness, science, evidence/engineering and editorial disposition, exact final snapshot.
- `d5aa/` figures, generators, machine-readable backing data; updated `resource-generation-gameplay-checklist.md`.
- Applicable offline scripts/tests, instructions, fixtures, complete/task-only manifest and patch/identity/diff verification; no original raw capture in tracked deliverables.

## 5. Safeguards and scope

Offline-only. Read existing native/console disassembly, Ghidra, local original B1 evidence, source code and authorized copies of Save52 as needed; **do not mutate** protected saves, raw B1 capture, installed game, plugins or archived evidence. No game launch, SFSE or observer modifications, attachment, Vortex interaction, binary patch, resave, live debugger or B2 approval. No Git stage/commit/push; changes remain available for maintainer review. Verify the pinned identities and disk/output guards, including the existing **40,000,000,000-byte caller-available floor on both C: and D:** where applicable. Apply all current project safety gates, local-only handling and evidence standards. A necessary new live observation or permission is a documented narrow escalation, **not** permission to take it.

## 6. Mandatory acceptance criteria

| ID | Requirement |
|---|---|
| **D5AA-AC1** | Verify scope, authorization, environment, protected-input identity and exact version pin; no unauthorized actions. |
| **D5AA-AC2** | Freeze original Q1–Q5 and create/maintain active ledger; no narrowing from historical target to other sources. |
| **D5AA-AC3** | Reconstruct all recoverable B1 source-level order with raw-correlated identities, timestamps and loss bounds; explicitly audit 19 ordinary paths, 24 map decisions, reset certificates, 110-record pretravel window and 119 conditional bypasses. |
| **D5AA-AC4** | Determine whether an *authenticated complete source first→visited→bypass chain* exists in B1; positive evidence, or an adequately controlled negative with enumerated missing links. Other-source evidence cannot satisfy target historical firstness. |
| **D5AA-AC5** | Map native Save52 full-load/Lodge/interior-linked exterior possibilities and exact eligibility for resource demands; prove guards and avoid claiming actual Jemison requests without witness. |
| **D5AA-AC6** | Map fast-travel confirmation → destination context/streaming → first eligible resource demand → arrival and post-arrival operations, with verified native paths/ordering and explicit unknown edges. |
| **D5AA-AC7** | Integrate visited/cache/reset lifecycle, append success/failure, concurrency and identity/epoch correctness; never conflate different gates. |
| **D5AA-AC8** | Specify precisely what was and was not observed in B1, the strongest warranted target attribution, unrecoverable loss limits and next discriminating evidence. |
| **D5AA-AC9** | Preserve and evidence-audit every original gameplay checklist item and five groups; change ticks only on demonstrated scope. |
| **D5AA-AC10** | Reproducible three SVGs, backing chronology/causal data and tested generators; readable and faithful evidence styling. |
| **D5AA-AC11** | Independent reviewers challenge actual historical firstness, chronology, missing upstream paths, negative claims, timestamp/provenance/loss logic, diagram accuracy and omitted viable investigation avenues. |
| **D5AA-AC12** | Full final report/ledger/sources/review, tested reproducibility and exact final snapshot; complete/task-only diff and clean protected original checks, no stage/commit/push. |

**Terminal disposition:** Per original controlling question, mark **COMPLETE** only for an answer at its required generality or a rigorously supported bounded negative; **INCOMPLETE/REWORK** when authorized avenues remain; **BLOCKED/ESCALATE** only for demonstrated missing indispensable evidence/permission with smallest actionable request and resume point. Clearly separate *offline investigation completeness* from the **still-open historical target first-construction / D5R parent research**. A successful diagram, coherent hypothetical story, evidence loss, or independent reviewer signature cannot convert an unknown historical first processing event into a known event.
