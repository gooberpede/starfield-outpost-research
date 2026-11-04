# Codex Implementation Brief — SOR RG2 D5AO

**Title:** GC-10 Observer Perturbation and Measurement Validity  
**Authority:** Maintainer-approved offline investigation and bounded engineering, 2026-11-04 (Australia/Sydney)  
**Project:** `D:\Projects\starfield-outpost-research`  
**Research parent:** GC-10 / D5R — ordinary resource-construction winner and its causal/consistency account  
**Status:** Implementation brief; **not** live authorization

## 1. Purpose and decision to be supported

The GC-10 observer has twice failed before a useful retail construction observation. N0 exposed overlapping hook/geometry-guard assumptions, repaired in 0.9.1. N1 reached READY but failed counter admission before Save52 load. D5AN corrected the counter design in a separately qualified **0.9.2** candidate and improved fault provenance. The correction replaces a fixed 32-attempt compare/exchange failure with retry-and-`Sleep(1)` behavior on contention. That improves liveness relative to the erroneous limit but can change the relative progress of competing game tasks. **GC-10 studies that relative progress.**

The purpose of D5AO is to establish whether counter instrumentation itself can change normal construction-winner selection; eliminate avoidable observer-induced blocking and ordering bias without sacrificing event integrity; independently qualify the integrated result; and specify which future GC-10 inferences it can support. A fully captured but observer-biased run must not be misrepresented as an unqualified account of uninstrumented Starfield.

**Do not turn this into a broader investigation of why resource geometry varies.** Continue to defer that separate question. No new gameplay, observer deployment, hook attachment to Starfield, or N2 trial is authorized here.

## 2. Controlling questions — freeze at kickoff

| ID | Original controlling question | Required completion evidence |
|---|---|---|
| **D5AO-Q1 — interference census** | For every repaired counter and its C++/assembly call site, where and under what actual native/observer-held synchronization can retries, yields, sleeps or extra work delay a competing resource-generation request? | Receiver- and call-site-specific critical-path map, actual code/instruction provenance, concurrency and lock-state assumptions, bounded exclusions and explicit unknowns; independent adverse challenge. |
| **D5AO-Q2 — interference removal** | Can avoidable blocking or excessive retries on winner-sensitive instrumentation paths be removed while retaining counter correctness, overflow/underflow prevention, event-accounting integrity, and failure provenance? | Implemented and explained per-counter strategy with proven invariants, actual concurrent/adverse tests, explicit reasons for any remaining blocking and a separately versioned candidate if code changes. |
| **D5AO-Q3 — measurement validity** | What demonstrable effect can the old 0.9.1 counter, current 0.9.2 counter and proposed implementation have on task progress and construction-lock admission, especially in close races? | Controlled uninstrumented/instrumented and before/after comparisons using actual owned native scheduling/lock paths where feasible; timing, retry, blocking and winner-reversal evidence; no false claims of retail frequency or zero observer effect. |
| **D5AO-Q4 — N2 evidence admissibility** | Is the resulting instrument suitable to obtain scientifically interpretable ordinary GC-10 observations, and which kinds of causal and usual-winner conclusions would remain qualified or uncertain? | Explicit admission and interpretation rules, residual bias register, fresh exact-package readiness proposal, independent review and frozen prospective prediction preserved or separately amended without retroactive alteration. |

Question completion is **not** granted merely by producing documentation, passing isolated counter throughput tests, or compiling a DLL. If a material feasible branch remains unexamined, report **INCOMPLETE/REWORK**; if essential proof genuinely needs missing permission/input, document the precise terminal barrier and propose the smallest next step (**BLOCKED/ESCALATE**, not COMPLETE). A bounded, evidence-based negative conclusion can be COMPLETE if it meets the original question.

## 3. Scope and governing constraints

### 3.1 Mandatory grounding and reading

Read and *apply* the current `AGENTS.md`, `WORKFLOW.md`, research charter/state, relevant decisions, `docs/RESEARCH_EXECUTION_PROTOCOL.md`, `docs/EVIDENCE_STANDARD.md`, `docs/EDITORIAL_STANDARD.md`, reviewer instructions and completion-contract template; current save protection and archival rules; D5AM/N0/N1/D5AN contracts, reports, reviews and active evidence ledgers; source-locked 0.9.2 build and native observer/reader/controller code; and relevant D5AE/D5AF scheduling, lock and construction-authority work. Recover truncated documents instead of treating excerpts as a complete reading. Required **substantive** reading and independent verification remain mandatory, but **reading order is not an acceptance criterion** per the maintainer's prospective AC01 revision. Historical failures remain historical.

Freeze the four D5AO questions, the acceptance criteria below and an active investigation ledger before substantive conclusions are accepted. Do not silently narrow their meaning. Independent substantive and editorial review must examine the **exact final snapshot**. Up to **two concurrently active subagents**; specialist may implement, non-implementing reviewer independently challenges and does not accept its own work. Primary agent retains integration responsibility. Record any deviation transparently.

### 3.2 Authorized operations

Authorized: offline source/static-native analysis; read-only examination of existing local raw captures, candidate sources and diagnostics; native original-instruction controls in owned/disposable hosts; build and test fresh derivative instruments, readers and supporting tooling; independent source/byte/ABI tests; preparation of a proposed run card and exact N2 admission design. Use a **verified disposable copy** for any Ghidra analysis; never open/alter the original research analysis project. Preserve game EXE/site version and source provenance with hashes. Use pinned local tools; do not install external dependencies or incorporate third-party code without separate authority. The existing provenance/licence and publication controls apply.

Not authorized: launching Starfield, live attachment, Vortex deployment, modifying protected saves/configuration, restoring original saves, forcing a generation order, introducing deliberate gameplay scheduling changes, pushing/staging/committing, uploading local raw/proprietary material, or treating N0/N1 approvals as reusable authority. Work in fresh ignored local namespaces; leave previous 0.9.0/0.9.1/0.9.2 builds and N0/N1 recordings unchanged. Maintain **40,000,000,000 caller-available bytes on each of C: and D:** at existing applicable checkpoints. Do not make arbitrary time/event/file-size caps that terminate healthy research.

## 4. Required investigations and implementation

### Workstream A — Complete counter and interference census (Q1)

1. Enumerate **every** changed counter site in the D5AN derivative, including `scheduler::next`, all assembly admission loops, producer entry/exit, queue reservation, registry/token and diagnostic paths. Distinguish the actual code responsible for `Sleep(1)` from loops merely capable of spinning or failing. Include the prior 0.9.1 32-attempt implementation as comparator. Do not assume all counters share semantics.
2. For each site, record its operation (`reserve`, `increment`, `active`, `decrement`, `ticket`, `fault`, etc.), thread multiplicity, invariant and width, memory order, possible contention peers, fast-path instructions, retry/failure mode, call chain and activation phase. Identify whether it may execute during request origin, registration, readiness, claim, visited-check-to-exclusive-lock gap, inside the watched native owner lock, while holding any engine lock, or while an observer registry/queue gate is held. Distinguish demonstrated from conditional overlap; do not infer thread scheduling solely from call adjacency.
3. Follow real synchronization ownership and aliases; account for the **five previously missing release edges** from D5AM and every relevant producer. A call-site census that ignores those paths is incomplete.
4. Draw a critical-path interference matrix marking sites capable of altering relative request progress, affected rivals, and any potential lock-convoy or waiter interference. If native instructions permit a sleep under a native lock or a priority-sensitive interval, treat it as a material unresolved risk until experimentally or structurally addressed.
5. Record the impact of **instrumentation beyond counters** (hooks, event copies, queue reservation, timestamps, guard checks and periodic draining) enough to avoid claiming that removing sleeps proves a zero-effect observer. Keep the detailed D5AO intervention focused on preventable counter perturbation, but list material residual risks.

### Workstream B — Per-counter corrective design and implementation (Q2)

Prefer avoiding OS-level waits and voluntary descheduling in GC-10 winner-sensitive paths. Do **not** simply globally replace `Sleep(1)` with spinning or unsafely replace every CAS with `fetch_add`: select by actual invariant and side effects. In particular:

- Evaluate whether a monotonic non-saturating count can use one atomic RMW with a separate mathematically sound overflow/accounting proof; where terminal overflow must not mutate state, establish a correct guarded approach.
- Distinguish counters used as **reservations** from diagnostics and producer-active counts; do not conflate a failed reservation with legitimate contention or ignore overflow/underflow.
- Verify that producer entry/exit counters cannot leak on failed partial entry, wrap on teardown, or report a healthy terminal with active work outstanding.
- Avoid additional blocking, allocation, filesystem calls and unbounded work inside native locks or callbacks. If any contention path must spin/retry, justify its forward progress, bounded impact assumptions, failure accounting and behavior under preemption; never invent an arbitrary retry cap merely to make a test pass.
- Preserve exact source/site/hook guard and relay validation including the 0.9.1 shared-helper overlap correction; retain D5AN diagnostic source identification and late-terminal failure checking.
- Ensure a genuine fault produces an explicit, source-attributed, authenticated failure; neither swallow failures nor silently truncate events. Distinguish ordinary contention from resource exhaustion or broken invariants.

Implement the smallest coherent correction. If no code change is justified, provide a robust proof and measurement qualification for the existing implementation instead. A changed implementation gets a **new unambiguous versioned native candidate and package**; do not replace historical 0.9.2 bytes or reuse an existing Vortex name. `NOT-AUTHORIZED` must remain visibly part of the offline package identity.

### Workstream C — Integrated perturbation and sensitivity tests (Q3)

Use actual qualified shared-target paths; N0 exposed the danger of testing separate copies that fail to reproduce retail aliasing. Explicitly compare where technically feasible:

- Native reference without observer hooks (same owned input and schedule constraints).
- Historical 0.9.1 bounded-CAS path (including legitimate 32-plus-interferer schedules).
- Historical 0.9.2 repaired path with sleep/backoff.
- New proposed path.

Exercise simultaneous producers, read/write lock participants and competing task callbacks. Include controlled closely matched contenders capable of changing the winner under small delays; widely separated competitors as controls; high contention, preemption/interleaving, recursive and nested callback situations; producer exit during failure; queue and registry adverse cases; identity ABA, source mismatch, lost record and STOP/drain races. Distinguish wholly synthetic schedules, original-instruction/native fixture controls, and genuine later retail evidence. Do not claim native fixtures reproduce Windows scheduler frequencies.

Measure, at minimum, **per-site fast-path latency and retry/yield/suspension behavior**, where waits occur relative to lock ownership and request progression, the presence of observed/induced winner reversals, event drops/unknowns and any guard or ABI regression. Avoid introducing heavy measurement hooks into the timing-critical comparison itself; explain timer effects, repeat runs and timing uncertainty. Prefer paired controlled workloads and observation-off controls; no arbitrary acceptance threshold such as “under 1% total CPU overhead” substitutes for winner-sensitive causality. A deterministic adverse case demonstrating a reversal matters even if average throughput looks acceptable.

Produce a **claim-tier matrix**:
- **Historical event observation:** what a complete instrumented record proves about the winner that actually ran.
- **Causal ordering:** what it proves about eligibility, admission and overtaking, and where history is incomplete.
- **Normal preference/consistency:** what remains unproved without repeated independent ordinary retail trials and an assessed observer-effect envelope.

Explicitly explain why unavoidable instrumentation cannot guarantee identical unobserved execution, and why any accepted inference nevertheless remains defensible within qualified bounds.

### Workstream D — Future N2 admission and forecast (Q4)

Prepare an offline **proposal only**, building on D5AN's N2 proposal and the existing normal-gameplay itinerary. One fresh process, protected Save52 Lodge load, direct Feynman V Cu IL F arrival and one ordinary Build Mode observation unless a scientifically indispensable, separately reviewable change is justified. No artificial task delays, forced refreshes, repeat queries, forced regeneration or itinerary expansion.

The proposed card and instrumentation-readiness matrix must include exact packaging/source/plan pins, installed DLL/site verification, healthy READY and fresh authenticated worker ACK **before** Save52 load, owner/source attribution, all-core/causal/scheduler/lifetime evidence quality, STOP/recovery, content-based protected-file validation (mtime-only changes cannot abort when unchanged content is positively verified), both drive floors, archive/postflight, and an independent prelaunch check. Scientific uncertainty must hold only dependent analysis/action, not automatically terminate healthy acquisition. Actual safety/integrity fault retains protective refusal. No silent change to live authority.

**Prospective prediction:** Retain the frozen histories and distinguish D5AM-PRED-01, N0/N1 PRED-02 outcomes and any N2 proposal. Do not silently roll an inconclusive previous forecast into a new one or rewrite its oracles. If the prediction text, eligible trial or instrumentation changes materially, freeze a separately identified prospective forecast after independent review and **before** any future observation. A wrong prediction is acceptable evidence, not an engineering failure. The N2 plan must not make matching masks/winners prerequisites for evaluating a prediction designed to test their variability.

## 5. Mandatory acceptance criteria

| ID | PASS requires |
|---|---|
| **AC01 — Governance and preservation** | Complete required reading applied by completion; independent verification, ≤2 active subagents, protected original evidence and research states intact, exact authority boundaries, both drive floors, no unauthorized live/deployment/Git operation. No reading-order gate. |
| **AC02 — Complete counter census** | Counter-by-counter C++/assembly and caller/lock matrix with actual native provenance, contested and uncontested operations, relevant release edges, no unclassified material winner-critical path. |
| **AC03 — Interference mechanisms** | Correct explanation of when old/new counter attempts, sleeps, spins or waits can affect winner progress, with positive and contrary test cases and explicit absence-of-evidence limits. |
| **AC04 — Correctness-preserving remedy** | Each proposed change has verified counter/queue/registry/producer invariants, overflow/underflow/progress/failure guarantees; no silent data loss or optimistic healthy terminal; no arbitrary cap disguised as safety. |
| **AC05 — Integrated native/ABI coverage** | Requalified shared-target hook/guard composition, ABI/unwind and relevant original-instruction coverage, full 0.9.1 guard regression and D5AN fault-diagnostic/STOP tests on the **exact final candidate**. |
| **AC06 — Contention and sensitivity qualification** | Genuine multithreaded integrated tests, close-race winner-reversal discrimination, comparative baseline/0.9.1/0.9.2/new evidence, measurement uncertainty and observer perturbation documented without unsupported retail claims. |
| **AC07 — Data and operational integrity** | Readers/producer accounting, source/task/lock joins, recorder loss/refusal, optimization (`PYTHONOPTIMIZE`, `-O`, `-OO` with prescribed `-E -B`), owner STOP, disk and content-based protection controls pass for declared scope. |
| **AC08 — Scientific fitness and prospective handoff** | Reviewer-challenged claim-tier and residual-risk matrix, N2 proposed finite card and exact package/plan binding, prediction freeze policy, no live authority, parent GC-10/D5R unchanged. |
| **AC09 — Independent closure** | Original frozen Q1–Q4 and AC01–09 separately adjudicated; non-implementing independent substantive/editorial final review of exact bytes; original failures and unknowns preserved; complete and task-only diffs checked forward/reverse and handoff manifest verified. |

**No “PASS” based solely on the number of tests or an error-free build.** An independent reviewer must challenge whether the tests would actually detect both data-integrity failure and winner-selection bias, including a case that reverses the winner because of instrumentation.

## 6. Required durable deliverables

Keep filenames coherent with existing `docs/experiments/resource-retained-population/` and `research/resource-retained-population/` conventions; proposed names below are illustrative, not excuses to duplicate documents.

1. `d5ao-investigation-ledger.md`: frozen questions, hypotheses, tested branches, primary-evidence locations, failures, unresolved and next actions.
2. `d5ao-counter-critical-path-matrix.md`: precise receiver/counter call-site and synchronization census, prior-version comparison and code/evidence anchors.
3. `d5ao-interference-controls.md`: test methods and outcomes, controlled contender reversals, counter/latency data, methodological and native-fixture limits.
4. `d5ao-measurement-validity.md`: explicit threat model, causal claim tiers and residual instrument effects, version-specific fitness findings.
5. `d5ao-report.md`, `d5ao-review.md`, checklist/RESEARCH_STATE updates, exact source/evidence manifest and independent sign-off; GC-10/D5R remain OPEN absent real usual-winner evidence.
6. Corrected, reproducibly built and independently qualified native source/package **if justified**; corresponding readers/controllers/operational scripts, source locks and qualified exact-byte manifest.
7. Proposed `run-card-d5ao-n2-proposal.md` (or reviewed evolution of existing D5AN N2 proposal), exact proposed plan, frozen/approved forecast register and a clear **NOT AUTHORIZED** banner. Codex final summary must link the package and run card directly using local paths, plus report/review/handoff/diffs.

Keep proprietary native exports, raw recordings, binaries, local receipts, original save/backup content, Ghidra cores and archives in `.local-work` or established private namespaces, not Git patches. Prior N0/N1 evidence and prediction text remain immutable. Preserve failed controls and corrected-repeat provenance; distinguish independently executed checks from reviewed receipts.

## 7. Handoff and next decision

The final handoff must state, in separate fields: scientific Q1–Q4 dispositions; AC01–09; exact version/DLL/ZIP identifiers; what changed from 0.9.2; evidence of counter correctness and effects on winner-sensitive scheduling; residual uncertainty; native/ABI/operational qualification actually executed; scope and limits of independent review; preservation outcomes; and exact complete/task-only diff identities. No staging, commit or push without maintainer approval.

**Desired next decision:** whether the independently qualified D5AO design is sufficiently nonintrusive and informative to warrant **separate** N2 live authorization. The decision must not be framed as proof that an invasive observer has no effect on scheduling. Its burden is a justified scientific measurement envelope, robust counter correctness, and no unaddressed *avoidable* winner-critical perturbation.

