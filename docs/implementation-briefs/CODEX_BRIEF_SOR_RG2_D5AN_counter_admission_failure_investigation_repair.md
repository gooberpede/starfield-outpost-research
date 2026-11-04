# RG2-D5AN — D5AM Scheduler/Causal Counter-Admission Failure: Root Cause and Offline Repair

**Codex implementation and research brief — 2026-11-04 (Australia/Sydney)**  
**Project:** `D:\Projects\starfield-outpost-research` (`gooberpede/starfield-outpost-research`)  
**Authority:** Offline investigation, owned instrumentation changes, native/operational fixtures, reproducible packaging, documentation and independent review **only**. **No Starfield launch, plugin deployment, process attachment, Save52 loading, live experiment, new N-series authority, protected-save modification, publication, staging, commit or push.**

## 1. Purpose and controlling context

The completed D5AM N1 attempt reached external READY with the corrected 0.9.1 geometry-composition guard, then failed before the controller obtained ownership/`HEALTHY_ACK` and **before Save52 was loaded**. The reported terminal set `failed=true`, `resident_inert=true`, `output_fault=causal_or_scheduler_guard`, `scheduler_counter_contention=true` and `scheduler_failed=true`. The retained core has one internal READY event; causal, scheduler and lifetime streams contain headers but no relevant events. The exact failing counter, site, thread and contention mechanism are **unknown**. The N1 scientific acquisition failed; PRED-02 is **INCONCLUSIVE**, not falsified or confirmed. GC-10/D5R remain OPEN.

The immediate objective is not to revisit the resource-generation model. It is to identify and correct the observer's counter-admission failure sufficiently that a new normal-play GC-10 observation can be considered without repeating an avoidable startup failure. N0's separate guard-composition failure and its 0.9.1 repair remain historical; **do not regress that repair**.

**Controlling question (D5AN-CQ):** Which exact counter operation produced N1's sticky admission fault, under what real native concurrency/ordering conditions could that happen, and what evidence-backed repair preserves integrity without turning normal contention into an unnecessary experiment-ending fault?

Freeze these subordinate questions and their acceptance criteria at task start; do not redefine them after seeing results:

- **D5AN-Q1 — Attribution:** Identify the precise producers/counters that can set the recorded failure bit; establish the exact N1-supported explanation versus unobservable details. Distinguish `scheduler::next`, its callers, inline/assembly producers and any shared aggregate guard; do not equate a named bit with proof of its cause.
- **D5AN-Q2 — Mechanism:** Explain and test the bounded-attempt behavior, memory ordering, contention, recursion, wraparound and accounting consequences. Determine whether legitimate CAS failure, code defects, state corruption or other causes explain or could explain N1. Preserve counterexamples.
- **D5AN-Q3 — Repair:** Implement the narrowest justified correction, including trustworthy, source-specific failure provenance where feasible, with sound bounded resource behavior and truthful failure accounting. Do not merely increase 32 to a larger arbitrary number or suppress a sticky fault.
- **D5AN-Q4 — Readiness:** Independently qualify the **actual integrated binary** and its observed startup/admission behavior in realistic offline shared-target/concurrency fixtures. Prepare a new versioned, uniquely named, **NOT AUTHORIZED** candidate and a precise future-admission delta if justified. Do not claim retail reliability from fixtures.

These four offline questions can be complete while GC-10 and any future retail test remain open. If an answer cannot be completed, preserve its INCOMPLETE/REWORK or evidenced BLOCKED/ESCALATE status; reports or plans alone are not completion.

## 2. Sources, governance and initial preservation

Read the current `AGENTS.md`, `README.md`, `WORKFLOW.md`, `docs/RESEARCH_EXECUTION_PROTOCOL.md`, `docs/EVIDENCE_STANDARD.md`, `docs/EDITORIAL_STANDARD.md`, `docs/SAVE_PROTECTION.md`, third-party/reuse policy, research charter/state, independent reviewer instructions, and relevant D5AM/N0/N1/0.9.1 briefs, code, reports, ledgers and reviews. **Required reading and demonstrable application are mandatory; reading order is not an acceptance condition.** The independent reviewer must challenge applied understanding. Use `docs/templates/completion-contract.md` and existing decision/ledger conventions.

Priority historical anchors:

- `docs/experiments/resource-retained-population/d5am-n1-report.md` and `d5am-n1-review.md` (N1 actual admission failure, failed acquisition, partial postflight and archived evidence).
- `docs/experiments/resource-retained-population/d5am-guard-fix-qualification.md` and `d5am-n0-repair-review.md` (0.9.1 shared geometry/causal guard correction and its limits).
- `docs/experiments/resource-retained-population/d5am-report.md`, `d5am-review.md`, owner-lock census, N0/N1 cards, controller and prediction/measurement contracts.
- `runtime/construction-winner/d5am_scheduler.h` and relevant causal assembly/bridge, worker, transport, guard and fixture sources. In current 0.9.1 sources `scheduler::next` contains a 32-attempt `compare_exchange_weak` loop, marks overflow with bit 1 and exhaustion with bit 2 of `D5AM_sched_counter_faults`; assembly includes analogous bounded counters. **These are investigation leads, not a pre-adjudicated root cause.**

Before modification, fingerprint current Git HEAD/index/worktree, exact native binaries, source manifests, N0 and N1 original recordings/partial archives, protected Save52 and backups, the existing 0.9.0/0.9.1 packages, installed build/compiler/toolchain inputs and prediction freeze. Do not alter sealed roots or original analysis projects. Use verified disposable copies for any Ghidra work, preserving core hashes before/after. Keep original raw evidence and pre-repair source/fixtures intact. Require at least **40,000,000,000 caller-available bytes on both C: and D:** before significant writes and at existing relevant checkpoints. Honor the two-active-specialist-subagent limit; primary agent integrates, independent reviewer remains non-implementing/read-only, and any breach is disclosed without rewriting history.

## 3. Investigation protocol: discriminate before editing

### 3.1 Exact failure-producer census

Create a source-to-machine-code map of every path that can set `D5AM_sched_counter_faults` or otherwise feed `scheduler_counter_contention`, `scheduler_failed`, `output_fault=causal_or_scheduler_guard` and terminal admission refusal. Include C++ inline sites, wrapper calls, assembly counters, state aggregation, worker timing, and initialization/enable transitions. Inspect native code actually built, not just assumed source equivalence. Account for flags with potentially multiple producers and for faults before event enqueue or metrics accounting. Name precise executable/bridge locations, counter objects, increments/decrements, owner/thread contexts and potential control-flow races.

Authenticate N1's retained terminal, lone READY frame and header-only sidecars against immutable raw files and reported hashes. **If the surviving bytes cannot identify the specific producer, say so explicitly.** Never infer a unique N1 thread/site from an aggregate sticky bit or absence of logged events. Separate (a) retrospectively proven N1 facts, (b) compiler/native possibilities, and (c) new fixture evidence.

### 3.2 Causal root-cause tests

Reconstruct full entry/exit and guard order around READY and first attempted health/command admission. Examine all possible bounded counter operations, not just `scheduler::next`: their memory ordering, contention/wakeup behavior, weak-CAS spurious failure, initialization, queue occupancy and capacity, recursion, same-thread nested producers, safe active-count decrement and STOP quiescence. Probe whether a failed partial admission leaves an unbalanced active counter, false health, lost event or unsafe shutdown. Explicitly test overflow separately from exhausted retries; distinguish finite genuine capacity pressure from benign contention and instrumentation bugs. Review timer/callback/atomic overhead and possible observer perturbation, but do not claim scheduler equivalence.

Run controlled realistic concurrency on **actual integrated observer-owned code**, with deterministic barriers/adversarial interleavings and varied contention. Fixtures must include multiple producers and competing counters using the same objects and startup/guard sequence that retail uses; isolated mock helper-only tests are insufficient. An independently reproducible failure or verified logic defect is preferable. If N1's exact interleaving cannot be reproduced, present a bounded causal explanation with alternative hypotheses and the precise evidence limit—do not invent the historical cause.

### 3.3 Correction criteria

Make the smallest safe change justified by findings. In particular:

- Avoid a new arbitrary retry threshold, busy-spin without a reasoned bound, weakened patch/site verification, skipping admission errors, unbounded memory queues or masked loss.
- Where contention is nonfatal, use a justified concurrency algorithm or bounded/adaptive progress rule whose safety, quiescence and forward-progress assumptions are explicitly verified. If an actual hard failure remains necessary, establish its cause and preserve a precise fault disposition.
- Preserve exact identities, sequence accounting, overflow checks, queue/reader invariants, native ABI/unwind behavior, hook restoration/STOP, resident-inert semantics, save protection and effective source/site guards.
- Add **specific diagnostic provenance** before evidence becomes unavailable (counter identity, producer/site, fault class, state/context, and thread if safely obtainable). Any new sidecar/terminal schema must be versioned, backward-compatible with retained recordings or explicitly separate, and independently read/validated. Do not add unsafe memory access or disk I/O in hot instrumented paths.
- Maintain or improve core, causal, scheduler, geometry and lifetime data integrity under concurrent activity. A no-drop counter alone is never proof of full coverage.

Do not expand this into a general winner/scheduler research project or change the GC-10 prediction. Instrumentation should serve the already defined ordinary winner experiment.

## 4. Offline qualification and adversarial gates

Use exact final source and binary (not stale pre-repair objects) for all release qualification. At minimum:

1. **Original-failure regression:** demonstrate the pre-repair counter limit's failure mode in an authentic or rigorously explained bounded shared-state fixture, and demonstrate post-repair behavior on the same conditions; keep the original failed test/proof intact. If only a plausible path can be reproduced, identify that limit explicitly.
2. **Shared-target composition:** exercise integrated causal+scheduler+core+geometry+lifetime instrumentation on overlapping real fixture targets; retain N0 0.9.1 original-geometry/causal guard controls, including foreign edit/refusal and relay corruption.
3. **Contention matrix:** test benign high contention, simultaneous producer entry, recursive producer activity, weak CAS failures, overflows, full queue, actual exhaustion, partial admission, startup before ownership, STOP during admission and failure during active producer teardown. Include randomized stress alongside deterministic interleaving controls; report seeds, workload and actual coverage rather than a pass count alone.
4. **Integrity/discrimination:** independently decode exact emitted frames; verify identity, CRC, sequence/prefix, loss/reentrant/counter/fault accounting and truthful terminal semantics under positive and adverse cases. Ensure failure provenance identifies the injected producer; differentiate operational failure from mere scientific uncertainty.
5. **ABI and portability:** rerun the appropriate original expected-exit native suite, 0.9.1 guard-composition cases, exact-object ABI and Windows unwind tests, assembly/C++ integration, and existing replay/regression checks. Rebuild independently from frozen sources and compare byte identities.
6. **Operational interface:** test READY, healthy ACK, counter refusal, trusted STOP when feasible, failure-before-ownership, owner/session binding, current source locks, protected pre/postflight adapters and archive paths. Do not conflate modeled retail premises with actual retail runs. All new Python entry points must reject `-O`/`-OO` and inherited optimization before safety-sensitive execution; use the pinned `-E -B` interpreter. Timestamp-only protected-file changes must be recorded and accepted **only after positive content-equivalence verification**; genuine content changes remain refusal conditions.
7. **Independent challenge:** non-implementing reviewer examines exact source and built code, reproduces relevant controlled tests where possible, tries concrete counterexamples and checks the final release snapshot and all criteria. Do not substitute test summaries for authentic logs, bytes, offsets or raw diagnostic receipts.

There is **no arbitrary number of test iterations that substitutes for passing the original controlling questions**. Stress testing alone is not proof of liveness under every schedule. Conversely, a particular retail failure should not lead to blanket guardrails that terminate a healthy capture without demonstrated safety/integrity need.

## 5. Future package and run readiness — no live authority

If the repair qualifies, produce a uniquely versioned native candidate and ZIP following the established pattern, e.g. `SorConstructionWinner-<new-version>-D5AN-counter-r1-NOT-AUTHORIZED.zip`; choose the version from the actual DLL metadata and do not reuse the existing 0.9.0 or 0.9.1 Vortex package identity. Supply the exact SHA-256 of ZIP, DLL, source set, plan/card proposal and all operational locks. Do not silently substitute a different DLL beneath old plan hashes. Name and preserve old failure packages and their provenance.

Review whether the existing N1 gameplay procedure can be reused unchanged; prefer a **small, explicit admission/source-lock delta** over a redesigned run card. A future N2-style session still needs a fresh reviewed plan binding the new package, a distinct explicit maintainer GO, full preflight against the actual protected inputs, effective installed-candidate verification, READY and subsequent **healthy ACK before Save52 load**, with normal owned STOP/exit/postflight/archive safeguards. No new live run follows automatically from passing this task. No deployment, game process, debugger attachment or protected-save writes are authorized here.

Keep the originally frozen D5AM prediction and its N0/N1 historical dispositions intact. A future prediction amendment or new trial identifier must be decided prospectively and separately; do not recycle a failed attempt as an eligible observation. GC-10 and D5R remain OPEN.

## 6. Deliverables

Produce authored, reviewable materials in the existing `docs/experiments/resource-retained-population/` structure and local `.local-work/d5an/` receipts:

- **D5AN report:** explicit answers to Q1–Q4, exact N1-support versus new proof, tested alternatives, residual unknowns, causal timeline, root-cause classification, why the correction is safe, observer effects and limitations.
- **Producer/counter census** with machine/source locations, sticky bits and the complete relevant admission/worker call graph; include all C++ and assembly edges and a durable decision/negative-evidence ledger.
- **Versioned corrective source**, native fixtures, automated test commands, byte/provenance manifests, old/new comparative diagnostics and independent reproducibility evidence. If binary repair is unwarranted or blocked, deliver proof and the smallest remaining discriminator rather than an untested package.
- **Validated fault-provenance design/reader** and adverse-case results; explicitly state what a future failed startup would reveal that N1 could not.
- **Named not-authorized package** and, if justified, a concise revised N1/N2 admission delta, proposal run card/source-locked plan. Include direct clickable local paths in Codex's final summary to the ZIP, report, review, proposed card/plan, both diffs and final handoff.
- **Checklist/research-state updates** preserving N0/N1 chronology, protected outcomes, PRED-02 INCONCLUSIVE, GC-10/D5R OPEN, earlier completed scoped findings and all legacy IDs; add new open items where material rather than declaring broader completion.
- **Independent substantive and editorial review**, explicit AC matrix and exact frozen-final-snapshot verification, task-only and complete patch exports with forward/reverse application checks, excluded proprietary/raw evidence inventory and local handoff manifest. **Do not stage, commit or push.**

## 7. Mandatory acceptance criteria

| ID | Acceptance requirement |
|---|---|
| **AC01 — Governance and preservation** | Complete required reading and applied understanding independently checked (no reading-order gate); correct authority, two-active-subagent cap, original recordings/save/backup/Ghidra preservation and both drive floors; no unauthorized live or Git action. |
| **AC02 — Exact N1 diagnosis** | Exhaustive relevant counter/producer/guard census with precise original-native paths; N1 claims limited to authentic terminal/raw evidence; missing historical origin not fabricated. |
| **AC03 — Mechanism and discriminator** | Adversarially tested causal account covering CAS contention, overflow, accounting and startup/STOP interleavings, with counterexamples and no arbitrary premature closure. |
| **AC04 — Correct and observable repair** | Narrow independently justifiable correction; truthful counter/provenance/terminal semantics; original safety/integrity guards and source identities retained. |
| **AC05 — Real integrated native qualification** | Full applicable native, shared-target composition, concurrency, ABI/unwind, replay and adverse-integrity controls pass on exact candidate; failures and fixture limitations retained. |
| **AC06 — Operational compatibility** | READY/ACK/STOP/failure and source/package binding, interpreter optimizer refusal, protected-content timestamp policy, pre/postflight/archiving tested without claiming retail execution. |
| **AC07 — Future-readiness handoff** | Unique candidate/version/hash and minimal proposed next-run delta, explicit no-live authority, frozen predictions/historical dispositions unchanged, GC-10 still open. |
| **AC08 — Evidence and research record** | Source-indexed native findings, durable ledger, Q1–Q4 completion judgments, preservation and negative results; no unsupported claim of winner consistency or retail reliability. |
| **AC09 — Independent final acceptance** | Independent reviewer challenges actual final source/binary and primary evidence; substantive/editorial judgments on frozen contract, exact complete/task-only diff and final manifests verified. |

**Completion rule:** Mark D5AN COMPLETE / ACCEPT only when all four offline questions and all nine mandatory criteria are supported on the exact final snapshot. If the original retail counter origin cannot be identified from surviving data, this does not automatically block completion **if** the producer coverage, failure mechanism, safe correction and future discriminating diagnostic are independently demonstrated; the precise historical uncertainty must remain explicit. If essential engineering work remains, return REWORK. Claim BLOCKED only with an evidenced terminal barrier and smallest required action per research protocol. Neither a successful fixture nor independent review authorizes another gameplay attempt.

## 8. Suggested Codex final summary

State the root-cause finding and its evidence limits first; then AC01–AC09, precise test scopes, package version and hashes, remaining retail unknowns and next admission decision. Link the new ZIP, any proposed run card/plan, report, independent review, full/task-only diffs and final handoff. Keep N1's failed status and PRED-02's inconclusive evaluation visible. A wrong scientific hypothesis is acceptable; a misleading health/admission claim is not.
