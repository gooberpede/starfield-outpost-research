# CODEX BRIEF — SOR RG2-D5AB-P1: Native Source Identity, Ownership and Lifetime Closure

**Date:** 2026-11-01 (Australia/Sydney)  
**Repository:** `D:\Projects\starfield-outpost-research` (`gooberpede/starfield-outpost-research`)  
**Task type:** Native research, engineering correction, and offline qualification  
**Parent:** D5AB — Observer Remediation and B2 Live-Run Readiness (**INCOMPLETE / REWORK**); D5R **OPEN**.  
**Authorization:** This brief permits the offline work specified below. **No Starfield launch, retail/plugin deployment, live B2, protected-save modification, publication, staging, commit or push.**

## 1. Controlling objective and frozen questions

Establish and demonstrate a **safe, correct, positively usable source identity and lifetime contract** for the D5AB observer across construction, publication, selected-source/visited checks, protected lookup, generation, visited insertion, retirement, reset, and owner replacement. The observer must be able to identify the real Feynman V source during a future authorized episode, including bypasses, without unsafe source dereferences, mistaken allocation continuity or fabricated histories.

P1 is an authorized bounded engineering/research package within the original D5AB questions **AB-Q1** (direct source identity/safe lifetime) and the dependent parts of **AB-Q2/Q4** (same-source append/chronology). It principally targets **AB-AC03/AC05/AC07/AC08** and regression obligations from accepted P2. **P1 success does not complete D5AB, validate retail behaviour, identify B1's lost first event or authorize B2.** Preserve the original D5AB five questions and twelve criteria unaltered.

Freeze these P1 questions at start in the active ledger:

- **P1-Q1 — Ownership and lifetime:** For every observer boundary that uses a source pointer or associates its observations, what native ownership/synchronization contract prevents invalid reads and false continuity through allocation, publication, cell aliases, detached work, retirement, cleanup, and context replacement? **COMPLETE** only with positive primary native evidence for all necessary edges or an implemented redesign that removes the unsafe dependency, plus adverse controls.
- **P1-Q2 — Identity correctness:** Which observed source fields and engine-consumed operands are initialized, immutable over the needed interval, and sufficient to distinguish allocation, geographic source and visited token? What collisions and pointer reuse remain possible? **COMPLETE** only with a demonstrated qualified positive join and explicit refusal of ambiguous/colliding histories; a reducer that refuses every source is not success.
- **P1-Q3 — Native lifecycle coverage:** Do the chosen hooks, fences and correlation rules cover every relevant normal and exceptional route, or can a source disappear/change/return without an observable invalidation? **COMPLETE** only after the necessary aliases, virtual dispatch, cleanup and destruction routes are accounted for and independently challenged.
- **P1-Q4 — Final P1 engineering qualification:** Does the exact final P1 source/build/schema/consumer combination pass native and adversarial lifecycle tests and all impacted P2 regressions? **COMPLETE** only when the actual final candidate meets the test contract and independent review; passing a prior revision is insufficient.

For negative findings, retain counterexamples and implement a warranted safe alternative within authorized scope. A missing export, unexamined indirect call, failed fixture or inconvenient method is **INCOMPLETE/REWORK**, not closure. Escalate only a specifically evidenced terminal barrier under `docs/RESEARCH_EXECUTION_PROTOCOL.md`.

## 2. Required starting evidence and bounded investigations

Read `AGENTS.md`, `WORKFLOW.md`, `docs/PERMISSIONS.md`, `docs/SAVE_PROTECTION.md`, `docs/EVIDENCE_STANDARD.md`, `docs/EDITORIAL_STANDARD.md`, the original D5AB brief, the C1/C2 assessment, **`d5ab-c2-evidence-matrix.md`**, `d5ab-c2-decision.md`, accepted P2 report/provenance/review, D5S detached-retirement evidence, D5V/D5Z lifecycle findings, and the existing native observer/bridge/reducer code. Refer to full repository-relative paths under `docs/experiments/resource-retained-population/` where appropriate. Preserve frozen executable/version, RVA versus static VA distinction, original private evidence and past classifications.

Create and maintain a live P1 investigation ledger with stable branch IDs, each original C2 edge's evidence, checked native paths/callers, competing hypotheses, negative controls, disposition and next action. Start with **L01–L21**, especially unresolved **L04, L05, L06, L13, L14, L15, L17–L21**; do not assume adjacent edges are closed because their diagrams look complete.

Investigate at least these specific dependencies, following material aliases into their actual owners:

1. **Constructor and exceptional cleanup:** `0x140982d90` allocation/dedup, failure/exception/unwind handlers, source deallocation and source return before publication; prove whether any abort/free escapes existing fences. Reconcile existing incomplete export E3 rather than treating its absence of data as a negative result.
2. **Publication and cell ownership:** publication store/failed reserve, unpublished objects, constructor callers, fill/edge/corner cell insert/replace/destruction, virtual call targets, source pointer propagation, and the residual `0x1409865e0` path when material. Grid retention or a copied raw pointer is not a source lease.
3. **Identity construction and mutation:** distinguish source allocation identity, geographic descriptor/key, content-derived `+0x68` visited token and pointer address. Prove initialization/stability of each *used* byte, particularly raw `+0x39..+0x3b` padding included in an earlier reducer identity. Eliminate padding from semantic comparisons if unproven, updating schema/consumers and controls. Verify aliases/writers rather than relying on a same-size allocation scan.
4. **Protected-copy lifetime:** prove the exact lifetime/reader ownership across selected/visited engine consumption and the protected source-map lookup copy. ProcGen map lock alone is not a demonstrated lease on the raw selected source. Cover detached-density worker races identified in D5S.
5. **Retirement, destruction, reset and reuse:** standalone retirement, bulk clear, virtual destructors, alternate cleanup, context/owner replacement, pointer ABA, identical-token different allocations, missing/late fences and re-publication; establish which event invalidates what join, including failure and loss windows.
6. **Native ABI and unwind:** every added/relocated boundary must preserve original arguments, stack, flags/volatile state, exception handling and unhook/STOP semantics; compare to pinned instruction bytes and guards. Do not claim runtime safety from fixture equivalence alone.

Prefer available original Ghidra exports and exact caller evidence first. **Authorize targeted additional offline Ghidra tracing/exports when needed** (including narrow handlers, vtables, virtual-call resolutions, source aliases and lifetime operands). Avoid speculative whole-executable scans unless a particular coverage gap justifies them. Read-only examination of the pinned executable and analysis database is permitted; do not alter the Ghidra database or game executable without separate explicit approval.

## 3. Engineering authority and preferred design principle

P1 **may modify and replace** the current birth/publication/retirement identity architecture, native observation sites and assembly bridges, transport event definitions, schemas and consumers where necessary to satisfy the frozen questions. Implement the simplest defensible design, **not** an obligation to preserve every existing hook. In particular, evaluate capturing the identity operands **already consumed by the engine at a lifetime-qualified boundary**, with a separately established allocation/publication correlation, against retrospective raw structure copying. Do not use unsafe dereferences, guessed token uniqueness or pointer equality as proof.

A proposed redesign must provide a concrete coverage comparison against every original event required by D5AB and against the C2 edges, explain lost or new capabilities, and demonstrate safe behavior for both a *positive identifiable bypass* and ambiguous/unqualified cases. Do not filter out non-target events, global resets or other source firstness evidence to reduce recording pressure. Do not weaken loss fences or cause unknown records to become positives. Keep old B1/D5Y/D5AA historical interpretations unchanged; schema migration must be version-aware and conservative.

P2 was separately accepted for offline controller, queue and reader/reducer qualification; P1 must not silently invalidate it. Record all affected files, binary contracts, event kinds and interpretation changes; rerun *all impacted* P2 tests on the **exact final** source combination. Unrelated tests may be omitted only with an explicit dependency argument. End-to-end final integration and retail authorization remain P3/P4 tasks.

## 4. Mandatory adverse tests and independent oracles

Build and run offline disposable native/host tests with independent event-order/identity oracles; include at minimum:

- Constructor success, dedup, failure/exception, unsuccessful reserve and unpublished object; completed versus failed publication.
- Qualified initial unvisited selection, protected miss or legitimate hit, sampled-generation path, successful and failed visited insertion, later positive same-identity bypass.
- Source retirement during detached work and at a proposed copied-identity boundary; cell replacement and owner/context reset around selection, lookup and append.
- Pointer address reused by a different allocation; two different sources sharing a visited token; identical geographic keys with distinct allocation histories.
- Missing birth, missing publication, lost retirement, lost reset/append, reordered cross-thread events, truncated evidence and contradictory epochs; **all must refuse false identity/firstness** while preserving sound partial evidence.
- Exceptional cleanup/unwind, failed guard/read, repeated/concurrent producers and safe worker/STOP behaviour for touched boundaries.
- Native source build and consumer schema pin matching the test receipts; relevant P2 transport, controller, read/ACK, reducer and legacy schema regressions.

Use controlled native fixture evidence where feasible; distinguish modeled fault schedules from actual executable instructions, compiled-host native tests and retail observations. Do not claim universal collision freedom, absence of all races, or retail frequency from finite tests. A conservative refusal is necessary for unsafe evidence but insufficient if the normal positive lifecycle cannot be identified.

## 5. Deliverables

Place durable research artifacts under `docs/experiments/resource-retained-population/` and reproducible source/tools under existing `runtime/construction-winner/` and `research/resource-retained-population/` conventions:

1. **P1 report:** direct answers to P1-Q1–Q4, evidence basis, exact native boundary addresses/source pins, tested versus inferred results, explicit downstream D5AB/B2 limits.
2. **P1 source identity/lifetime matrix:** each C2 L01–L21 edge, current ownership, native proof and observer event/fence, ambiguity, counterexample, final status, test pointer, unresolved dependencies. Include a compact state/ownership diagram, not a diagram substituted for evidence.
3. **Updated observer/bridge/reader/reducer/schema and tests** as needed; design alternatives and why chosen/rejected.
4. **Test and provenance ledger:** exact built source/binary hashes, version compatibility, commands, passes/failures, native and modeled oracles, protected inputs, reproduced faults and corrected regressions; do not rewrite historical failures.
5. **Parent D5AB mapping:** all five original questions and twelve criteria, with P1's actual contribution; mark P3/P4 obligations OPEN and B2 NOT AUTHORIZED.
6. **Independent substantive engineering/scientific-completeness review**, separate editorial review of exact final changed prose/source docs, verified complete and task-only patches, manifests, protection and exclusion inventories. Keep native raw/proprietary and save evidence LOCAL-ONLY.

## 6. Completion contract and acceptance gates

Use the original `docs/templates/completion-contract.md` and `docs/RESEARCH_EXECUTION_PROTOCOL.md` strictly. These eight criteria are frozen absent the maintainer's recorded approval:

- **P1-AC01:** Current pinned inputs, policy and authorization verified; no live/deployment/protected-save/Git integration actions; active branch ledger maintained during work.
- **P1-AC02:** Every L01–L21 material native edge accounted for with primary function/alias/owner evidence, counterexamples and exact coverage/failure scope; no same-size heuristic passed as ownership proof.
- **P1-AC03:** A sound lifetime/identity method covers every actual positive observation site, including bypass and protected lookup; initialized immutable semantic operands or explicit disqualification; normal positive source identity possible.
- **P1-AC04:** Constructor, publication, detached worker, exceptional cleanup, cell ownership, retirement/reset, alias and pointer/token reuse are demonstrably safe or conservatively invalidated without hiding missing evidence.
- **P1-AC05:** Native and adverse fixtures exercise qualifying positive history and all required fail/refusal cases with independent identity/order/safety oracles; failure reproductions retained.
- **P1-AC06:** Final compiled candidate, recorder, source schemas and consumers have exact-version provenance and pass affected P2 and original relevant regressions; no new untested source/config drift.
- **P1-AC07:** Original D5AB questions/criteria, D5R and B1 history remain intact; P3/P4 and live approval not silently promoted; scientific versus engineering status distinguished.
- **P1-AC08:** Independent exact-final engineering and scientific challenge, complete editorial coverage, verified patches/manifest, and honest ACCEPT/REWORK/ESCALATE mapped to each frozen question and acceptance criterion.

Under **REWORK**, continue in scope: fix, investigate alternatives, rerun affected tests and seek re-review without a new brief. Under **BLOCKED/ESCALATE**, provide the precise indispensable native edge, tested alternatives and why they fail, smallest missing authority/capability and preserved resumption point. Any departure from the fixed P1 questions or mandatory criteria requires maintainer approval; a safe refusal-only reducer cannot satisfy the positive-identification requirement.

## 7. Delegation, operating limits and interruptions

Optional **specialist sub-agent** for a bounded native ownership, exceptional cleanup or proof-design problem. At most **two concurrently active sub-agents**; the independent reviewer must not have implemented the candidate it reviews. Primary agent owns integration, test validity, original-contract completeness and review follow-up. Preserve specialist evidence, failed conjectures and code contributions for the reviewer. Follow `docs/reviewers/research-completion-reviewer.md` and its fallback if collaboration tools are unavailable.

Maintain normal offline protection, file/disk identity, exact module/site guards and repository-preservation policies. No game launch, injected retail hook, deployment, SFSE install/uninstall, protected-save write, arbitrary native executable patch, public release or B2. This brief grants no blanket authority to manipulate unrelated processes. Disposable own-host native fixtures are permitted under the project's usual safeguards.

**Cybersecurity interruptions:** Do not preemptively narrow legitimate authorized research because of speculation about the prior D5AB blocks. Record any actual refusal and its effect as an apparent/suspected false positive where appropriate, without asserting an undisclosed cause. Respect enforced restrictions; do not disguise a blocked action or work around it by rerouting the same prohibited action. Continue *independent authorized work* when feasible; do not quietly drop criteria or declare completion because of a refusal. No project-wide policy change is authorized by this brief.

**Handoff:** return exact file inventory, source/build/test proof, requirement matrix, independent review, verified full diff and task-only diff when applicable, and explicit recommendation to the maintainer. Do not stage, commit or push. If P1 is accepted, propose P3; **do not begin P3 or B2 automatically**.
