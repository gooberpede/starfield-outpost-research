# D5AO counter and critical-path census

2026-11-04, Australia/Sydney. Parent: D5AO-Q1–Q4; GC-10/D5R remains OPEN.
This is an offline source/native census, pending exact-final independent review.

| Element | Answer |
| --- | --- |
| Question | Where can counter work alter progress toward ordinary resource construction? |
| Best-supported answer | D5AN's two shared CAS helpers can sleep at admission and teardown, including while a native reader/exclusive interval or an observer registration gate remains held. Generic bridges admit unmatched receivers too. Removing their OS wait removes that specific mechanism; retries and all other observer work remain. |
| Confidence and coverage | PROVEN / STATIC for the inspected source and pinned native operations; conditional overlap where caller-held locks are not established. No retail frequency or zero-effect claim. |
| Evidence | The source anchors and retained original/native domains below; D5AO exact-object and comparative qualification receipts supply the separate engineering evidence. |
| Limitation | Native scheduler wrappers can inherit locks from callers. Absence of a local acquire does not prove an unlocked callback. Unresolved outer-lock ownership is explicitly conditional. |

## Domains and immediate provenance

Maintainer-owned code is adapted under SOR-P-0002, with source hashes in the
D5AO build receipt. Original 0.9.1, 0.9.2 and their raw observations remain
unchanged. [D5AN's census](d5an-counter-census.md) supplies the retained original
linked-code mapping; the present census rereads its producer sources and the
native reader/exclusive/release instructions, rather than interpreting hashes
as semantic proof.

Game addresses below are preferred static VAs for 1.16.244.0, base
`0x140000000`, EXE SHA-256
`7e9adb1414a8e1b325e5e1f097b9b17b78deb7eebeda37a333351a43a60f9d28`.
Observer DLL RVAs and COFF offsets belong to separate images/domains.
Retained `.local-work/d5af/prelock-export01/native.tsv` contains the complete
reader/exclusive/release instruction bodies. Its SHA-256 is
`bad793664b90b987bd5dc4d91fb70936a2d9590029b17dc2eb7e7d1e2c807b47`.
The provider is `.local-work/d5q/export01/native.tsv`, SHA-256
`60cc949338e9e0211b87f56c376e1a057d8b7af2da6f9e34a4ae3e84339f8fcd`.
The [D5AM receiver census](d5am-owner-lock-census.md) supplies independently
byte-audited receiver/alias continuations and the five formerly missing releases.
No analysis database was opened for this source census.

For exact 0.9.2 final09 the helper exports are DLL RVAs `0x1ecc0` (next) and
`0x1ec20` (leave), in `.local-work/d5an/native-final01/candidate-exports.txt`.
The linked disassembly shows leave's LOCK CMPXCHG at RVA `0x1ec57`, then
`MOV ECX,1` / imported call at `0x1ec61` / `0x1ec66` following failure.
These are actual owned DLL instructions, not game instructions or inferred
hardware spurious failures. The increment helper has the corresponding retry
and Sleep import path. D5AO builds a separate 0.9.3 primitive while preserving
the diagnostic ABI; exact generated-source and object receipts control its bytes.

The new [native helper checker](../../../research/resource-retained-population/d5ao_helper_native.py)
independently bounds exports using PE unwind-function ranges and decodes import
targets for the actual dumpbin call instructions. Final05's next range is
observer DLL RVA `0x1ecc0..0x1ed78` and leave is `0x1ec30..0x1ecbf`, with
exclusive upper endpoints. Each has one LOCK CMPXCHG and actual LastError
preservation imports; neither has a direct wait import call. The matched
historical-sleep03 algorithm comparator positively retains one direct Sleep
call in each helper. Receipts are `.local-work/d5ao/helper-native-final05/`
and `.local-work/d5ao/helper-native-sleep03/`. This direct-call check does not
claim that indirect fixture callbacks cannot wait or that execution cannot be
preempted. Actual retail fixture pointers remain zero by source contract.

## Operations and invariants

The [0.9.2 helper](../../../runtime/construction-winner/d5an_counter.h), lines
58–82, is the sole production source of counter `Sleep(1)`: strong CAS failure
in next or leave. It saves/restores LastError, refuses MAX/zero without mutation,
and performs default sequentially consistent atomic operations. Its fixture
callback pointer is zero in retail. Fault publication has one strong CAS and
atomic stores/ORs, no wait loop. Publication 1 explicitly means incomplete
first-fault provenance. A completed publication identifies the first successful
claimant, not necessarily the earliest physical fault.

Every counter in the following table is a 64-bit unsigned object. Concurrent
next/leave operations use sequential consistency unless a queue/registry edge
below specifies acquire/release. IDs identify diagnostic source families, not
different objects: scheduler ID 1 and causal ID 33 alias `winner::active`.

| Object / diagnostic ID | Operation, multiplicity and actual producers | Invariant and interference peers |
| --- | --- | --- |
| `winner::active`, 1 / 33 | Increment/decrement; scheduler C++ Producer, five scheduler ASM bridges, causal C++ Producer, ten causal ASM bridges, inherited core/lifetime producers | Number of acquired admissions; partial entry must unwind only held counts. Every family shares the same cache line/object and can collide with another family. |
| `scheduler::active`, 2 | C++ Producer entry/exit, including capture nested beneath an ASM admission | Own admitted C++ work. Shared by registration, callback, provider, claim and queue wrappers; claim constructs a Producer before relevance filtering. |
| `scheduler::drops`, 3 | `lose` from queue reservation, reentrancy and signed-range refusal | Monotonic failed-record count; increment itself can collide. Actual loss sets failed even if this diagnostic cannot advance. |
| `scheduler::reentrant`, 4 | Recursive emit on the same thread | Monotonic diagnostic across threads; TLS prevents concurrent recursion on one recording scope, not different threads using this count. |
| `scheduler::tokens`, 5 | Task birth `identity(...,publish=true)` | Nonzero allocation identity; MAX must refuse without wrapping. Called while that registry cell's serial is odd. |
| `scheduler::registry_faults`, 6 | Busy/overflow/full birth/retire paths | Monotonic diagnostic. Serial overflow can call fault publication before this increment. Duplicate birth releases its odd serial before diagnostics. |
| `scheduler::identity_faults`, 7 | Missing birth, changed cookie, duplicate birth, snapshot mismatch | Monotonic diagnostic, potentially from all matched scheduler producers. Does not itself authenticate a task lifetime. |
| `D5AM_sched_bridge_active`, 8 | Five ASM admissions and leaves/disable rollback | Bridge ownership count, distinct from C++ own activity; core admission precedes it. |
| Registry publish serial, 9 | One guarded serial CAS plus release store to serial+2 | Per-cell gate, not generic next. Refuses serial above MAX−2. CAS contention yields RegistryBusy, without sleeping on the serial itself. |
| Registry retire serial, 10 | One guarded serial CAS plus release store | Same width/invariant, separate fault source. A busy live cell is uncertainty, not permission to steal ownership. |
| `scheduler::written`, 11 | Worker-only non-atomic checked increment after successful packet write | No contenders under the one-worker contract; no CAS/sleep. MAX refuses before increment. |
| `causal::active`, 32 | C++ Producer before capture/register/lifecycle/exclusive/visited callbacks | Own C++ admissions; own entry precedes core entry, unlike scheduler. Failed core entry rolls own back. |
| `causal::drops`, 34 | `lose`, including reservation/reentrancy/range refusal | Monotonic diagnostics; actual lost record fails capture independently of diagnostic count. |
| `causal::reentrant`, 35 | Recursive emit TLS path | Monotonic diagnostic across producers. |
| `causal::tokens`, 36 | Owner registration generation allocation | Nonzero generation; bump while registering flag held and registry serial odd. |
| `causal::baseline_unknown`, 37 | Registration busy or nonzero/unreadable initial lock baseline | Monotonic scientific uncertainty; busy flag path returns, never waits for flag ownership. |
| `causal::multiowner`, 38 | Registration observes a different watched owner | Monotonic uncertainty; does not silently switch the active owner. |
| `causal::uncertain`, 39 | Capture sees zero generation, odd/changed serial, changed owner or generation | Monotonic uncertainty. Called after displaced lock operation on matched receivers. |
| `causal::written`, 40 | Worker-only atomic bump after packet write | Only one normal writer; no normal competing writer. Explicit MAX precheck and helper refusal remain. |
| `D5AM_registry_serial`, 41 | Register and Retire lifecycle bumps | Publication-generation serial; register can retain registering flag, retire does not acquire it. Serial changes invalidate dependent snapshots. |
| `D5AM_causal_bridge_active`, 42 | Ten ASM bridge admissions, leaves and partial/disable rollback | Core acquired first; subsequent capture nests a C++ own/core Producer. |
| Fault `publication`, bitmap and first fields | Fault-only; one claimant CAS, sticky fetch-ORs and fixed atomic field stores | No allocation, filesystem operation, OS backoff or retry loop. Readers refuse incomplete publication. |

Fallback IDs 31/63 identify unclassified helper references, not a discovered
additional logical counter. All normal references in the two headers map to the
named IDs. Producer numbers 1–19 describe the C++/ASM family and rollback/leave
edge; they do not supply a native thread identity until an actual fault records it.

| Operation class | Historical 0.9.1 | Historical 0.9.2 | Proposed 0.9.3 |
| --- | --- | --- | --- |
| C++ next/bump and ASM entry | At most 32 CAS attempts; saturation/exhaustion refuse. C++ weak CAS lowers to actual hardware CMPXCHG in the retained build. | Shared strong guarded helper retries; each failed comparison calls Sleep(1). | Same strong guarded update and provenance; failed comparison retries immediately. |
| Producer leave/rollback | Original decrements have wrap/short-circuit hazards under corrupted-count injection; no new checked-leave provenance. | Checked strong CAS refuses zero; independently releases other held counts; failed comparison sleeps. | Checked nonwrapping leave retained; no OS backoff. |
| Monotonic diagnostics/tokens | Shared bounded increment can refuse legitimate contention. | Checked helper distinguishes ordinary contention from terminal MAX. | Same exact MAX refusal and returned token; contention does not cause a sticky fault. |
| Serial and written guards | Direct terminal overflow refusal; no precise first-source publication. | Source-attributed diagnostics added; serial operation and writer ownership remain distinct. | Preserved without converting registry gates to generic increments. |
| Queue reservation | Finite capacity and 32-attempt loss/refusal. | Same reservation policy; drop diagnostic can sleep. | Same reservation policy; drop diagnostic has no OS wait. |

The original 0.9.1 scheduler ASM has five core/bridge admission pairs; causal
ASM has ten pairs. Their original code offsets and DLL mappings are retained in
[D5AN's census](d5an-counter-census.md), including core/own constructor exhaustion
at original observer DLL RVAs `0x4453` / `0x44a4`. A same-algorithm comparison
inside a new host is labelled derivative, never the original historical DLL.

## Reservation and inherited operations are separate

Both scheduler and causal `emit` reserve enqueue with at most 32 weak-CAS
attempts, capacity 32,768, signed ticket arithmetic and explicit full/range/loss
refusal. Cell ticket acquire/read and release/publication protect the copied
event. The worker releases a consumed cell by ticket=n+capacity, then advances
dequeue. An earlier reserved but unpublished cell stalls ordered drain; a later
published cell cannot authorize skipping it. These loops never call Sleep
directly. Their failure calls a drop diagnostic that can call Sleep in 0.9.2.
Removing that wait does not remove the reservation quota or claim losslessness
under arbitrary contention. A true failed reservation is recorded as failed
acquisition, not treated as a successful event.

Registry node CAS and odd-serial CAS are single-attempt gates; cookie lookup
probes at most 64 cells. They have no voluntary descheduling. Other clients
return uncertainty instead of blocking on an odd serial. The token increment
inside a held odd serial is the avoidable 0.9.2 OS-wait edge.

Inherited `observer.h` uses atomic RMWs for active, tokens, diagnostic counts,
epoch/hazards and bounded queue/loss-bound CAS. Lifetime producers increment
`winner::active` and their own active/generation/tokens, emit through a separate
finite queue and release on exit. Geometry owns active-capture and slot state,
and copies the population while a native shared interval is held. These are
contention peers/residual work, not repaired-counter Sleep sites. Their existing
wrap/failure contracts are not silently strengthened by the D5AO helper change.
The diagnostic helper therefore cannot be qualified by testing only scheduler
activity in isolation.

## Bridge and caller critical-path matrix

The scheduler header anchors are `d5an_scheduler.h:70–101` (counter and queue),
`:120–162` (identity), `:165–219` (callers), `:233–242` (worker).
The causal anchors are `d5an_causality.h:59–100`, `:102–181`, `:245–258`.
Assembly macros are `d5an_scheduler.asm:164–225` and
`d5an_causality.asm:98–142`; actual expansions are listed below.

| Call site / phase | Held or prospective synchronization at counter work | Affected rivals and mechanism |
| --- | --- | --- |
| Registration wrappers, game VAs `0x14076cea4`, `0x14076d07b`, `0x1407b56c5`, `0x1407b57eb` | Producer and task snapshot precede original `0x1427e5630`; no observer registry gate held at Producer entry. Upstream engine locks remain conditional. | Delays publication of this request relative to another ready request. Token increment later retains the per-cell odd serial. |
| Activated ASM, `0x1427ec100` | Gate by watched task vtable, then core/bridge, capture adds C++ own/core, then leaves. Original callback registration/state decision has not run. Outer command-pump synchronization is conditional, not established absent from entry instructions. | Delays activation/dispatch and can extend a caller-owned pump interval. |
| Dispatch ASM, `0x1427e6a00` | Same admission nesting before native state update/dispatch. Calls may be inline under an upstream server operation. | Changes when the task reaches queue publication or direct execution. |
| Retire ASM, `0x1427e4ab0` | Same admission and capture; retirement serial CAS owns a cell only during update. | Delays retirement/dependency or storage reuse; can change later availability even when target construction has ended. |
| Ready-tree ASM, `0x1427e4957` | Before original serial consumption `MOV R9,[RCX+0x50]`; no demonstrated local native lock acquire at this site. Caller-held serialization remains conditional. | Extends the ready insertion operation; does not itself prove a changed rank or geographic priority. |
| Dependency ASM, `0x1427e61a4` | Admission before native dependent decrement; capture after it. | Delays the last-prerequisite transition/its evaluation and follow-up queueing. |
| Density/layer callback wrappers, `0x14076d14f`, `0x1407b585f` | C++ Producer spans original task callback. Layer enters provider under its manager reader; detached density does not inherit the preparation reader. | Begin/end copies, queue work and entry/leave contention change task progress; layer can extend the manager reader. |
| Provider bridge / causal register-owner | `observer` ingress calls register-owner before its core Active; scheduler provider join occurs with a task scope when present. Registration retains flag, then odd serial across generation token and baseline capture. | Longer registration uncertainty window; global shared-core counter contention reaches both request families. Source eligibility is not established by a counter alone. |
| Claim entry, `0x1428d3960` | Unconditional C++ Producer before original claim, including capture-disabled/unmatched work. Original helper's local queue synchronization occurs inside original, not claimed held at wrapper entry. Caller lock state conditional. | Delays owner-back/peer-front/external attempts, thereby changing which callback is claimed. Leave follows matched emit after the original helper. |
| Queue entry, `0x1428d2b80` | C++ Producer and QueueBefore before original publish; QueueReturn/leave afterwards. External queue lock inside original is not proved held at entry. | Changes publication progress and possibly a caller-held interval; no evidence establishes FIFO equivalence across routes. |
| Visited-done callback, `0x14079fca3` | Native shared decrement is already done; exclusive helper call at `0x14079fcb3` has not occurred. C++ Producer, event copy and queue emit lie in this exact gap. | Direct pre-admission delay permits a later request to register/acquire first. No geographic computation occurs in the native gap. |
| Exclusive-call wrapper, `0x14079fcb3` | C++ Producer before original; Approach before acquisition; HelperReturn and destructor after original returns holding exclusive ownership. | Entry delays admission; exit extends held ownership and can delay all same-owner readers/writers, including foreign sources. |
| Pending ASM, `0x1422cc410` | Core/bridge before native writer-count XADD; matched capture and leave after it, before ownership CAS at `0x1422cc42b`. | Pre-XADD delay changes registration order; post-XADD delay permits overtaking. Pending bits are not tickets. |
| Acquired ASM, `0x1422cc48f` | Ownership CAS already succeeded; core/bridge admission precedes owner-TID store/MFENCE. Matched capture and all leaves execute while exclusive bits remain held. | A helper Sleep can delay owner publication and native protected work; rivals cannot acquire until the holder releases. This can convoy waiters but cannot transfer this already won acquisition. |
| Recursive ASM, `0x1422cc3f2` | Same native TID already owns lock; admission precedes recursive XADD; capture and teardown stay inside exclusive ownership. | Extends a recursive exclusive interval; distinct threads cannot both be recursive owners. |
| Reader ASM, `0x1422cc366` | Admission before reader-count XADD. After XADD, capture/leave occur before native exclusive-bit test/wait; this may be a registered reader waiting on an existing writer, not yet usable shared access. | Adds registered reader time, can prolong a reader cohort or waiting state. Never infer usable shared ownership merely from reader XADD. |
| Reader-ready ASM, `0x1422cc3c3` | Reader admission completed; this includes same-owner recursive read. Core/bridge, capture and leave execute before helper returns. | Extends the shared/recursive interval before the consumer. |
| Six typed reader release sites | All core/bridge admission executes BEFORE native decrement; matched capture and leave execute after it. An outer lock can remain held. | Pre-decrement sleep extends reader occupancy; post-decrement work can postpone native wake/continuation. |
| Final writer-release ASM, `0x1402c45c2` | Owner TID already cleared at `0x1402c45b7`, exclusive packed-state bits still held until displaced XADD. Admission before XADD; capture/leave before original wake branch. | Sleep can prolong held bits with zero owner TID, or postpone wake after release; waiter admission is not ownership transfer. |
| Recursive release ASM, `0x1402c45e7` | Exclusive ownership persists before and after depth decrement; admission before displaced MOV/XADD. | Extends recursive ownership and same-owner waiter convoy. |
| Inline releases, `0x140982a5a` / `0x140982a92` | Native caller has prepared owner/delta; admission before XADD, matched capture/leave after XADD. Final release has owner cleared; recursive release retains owner. | Same packed-state and wake/continuation interference; original ECX delta, old value and flags must survive. |
| Reset/Retire lifecycle callbacks | Register/reset events and serial changes can run in lifecycle code; exact surrounding ownership depends on the reset/destructor path. | Invalidates dependent snapshots. Scientific uncertainty must hold dependent conclusions without automatically stopping healthy capture. |
| Worker written/drain/guard/STOP | Worker serializes packet writes/flushes and waits for producer counts. It does not run normal producers under a native owner lock. | CPU/cache/IO pressure competes with task progress; failed teardown or stalled publication can extend STOP. No healthy terminal with outstanding admitted work is allowed. |

Native synchronization statements here follow actual instruction order, not
inferred thread scheduling from call adjacency. In particular, final writer
release has a zero owner word before its state decrement; treating that bridge
as unlocked because owner==0 would miss the material lock-held sleep.

## Receiver aliases and all five additional release edges

The watched receiver is ProcGen `+0x40`, with packed state at `+0x44`.
The singleton manager's `+0x130` points to ProcGen; ProcGen's own `+0x130`
is a different exact-word cache mutex. Neither offsets nor those locks alias
merely because both contain 0x130.

| Actual owner path | Native release boundaries | Extra held synchronization |
| --- | --- | --- |
| Provider visited scan | `0x14079fc85` | Shared owner lock already held before typed release admission. |
| Point consumer | `0x14079e027` | Shared owner lock. Geometry observation may add population work. |
| Area consumer | `0x1421e0a87` | Shared owner lock; geometry acquire guard shares the native reader target with causal patching. |
| ProcGen `0x1407a50d0` | **Additional** `0x1407a51b7` | Distinct ProcGen `+0xd0` already owned while shared `+0x40` is used. Counter delay can extend both. |
| ProcGen `0x1407a5210`, branch one | **Additional** `0x1407a5386` | Distinct `+0xd0` plus shared `+0x40`. |
| Same method, branch two | **Additional** `0x1407a547c` | Same two receiver-specific intervals, separate site identity. |
| Owner-map client `0x1409829b0` | **Additional** final `0x140982a5a`, recursive `0x140982a92` | Exact inline owner-lock releases, not covered by generic release helper. |
| Reset `0x14079ddf0`, client `0x140982b70`, provider exclusive | Generic release helper `0x1402c45a0`; callers at `0x14079dec4`, `0x140982bc9`, `0x14079ffa5` | Same watched lock, including clients without provider TLS. Reset later uses distinct `+0xd0`. |

The D5AM forwarding census follows captured contexts and excludes manager `+0x24`,
nested object `+0x20`, other singleton `+0x30`, returned cache `+0x18`/`+0xb8`
and exact ProcGen cache-mutex clients from watched-owner attribution. Generic
causal assembly nevertheless admits these unmatched native receivers before
its post-operation filter, so their counters and delays are real interference
peers. The census is scoped to the demonstrated ordinary receiver graph; it
does not pretend to enumerate arbitrary modified-code or indirect replacement
clients. Unknown outer locks at scheduler entry remain a residual coverage
qualification rather than a proof that native locks are absent.

## Corrective decision by invariant

The 0.9.3 [D5AO helper](../../../runtime/construction-winner/d5ao_counter.h)
uses the same guarded strong CAS and immediate retry, with no Sleep, yield,
allocation or filesystem operation. This is the smallest coherent correction
to the newly introduced OS-wait mechanism. It does not globally convert
reservations, registry serials or diagnostics into unchecked fetch-add.

For active/core/bridge counts the primitive retains MAX refusal and checked
zero leave; per-constructor held bits and assembly rollback preserve ownership.
For tokens it retains nonzero identities and no wrap. Diagnostics remain exact
until genuine terminal saturation, then explicitly fail with source provenance.
Worker-written counters have no normal contention, but retaining the common
primitive avoids a different diagnostic contract. Serial gates and enqueue/ticket
reservations retain their own invariants and refusal policies.

A single unchecked RMW could transiently wrap at MAX and let a racing admission
observe zero; rollback would not restore a unique correct history. No finite
per-process bound is proved for all monotonic counters, and active depth bounds
alone do not cover corrupted-input controls. Therefore one-RMW replacement is
not justified by the present evidence. Immediate guarded CAS removes deliberate
descheduling, but cannot prove bounded per-thread retries under arbitrary
preemption/adversarial mutations. Each failed strong CAS proves some object
progress; it does not prove this thread's progress. Cache-line contention,
preemption and native owner locks remain in the measurement threat model.

Hook entry/return, flag/GPR/vector preservation, target-field copying, QPC,
finite queue reservation, population copying, source/task identity validation,
guard checks and periodic drain continue to perturb execution. The complete
instrumented history can establish what actually happened under that instrument;
it cannot guarantee the same hidden winner without it. Comparative controls
must measure this rather than turning removal of Sleep into a zero-bias theorem.
