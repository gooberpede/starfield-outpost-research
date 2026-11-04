# D5AN counter and admission census

2026-11-04, Australia/Sydney. **Exact-final native inspection complete;
independent whole-contract acceptance recorded.** N1's retained bytes prove aggregate scheduler bit 2,
not a particular counter, producer, thread or interleaving. This census does
not identify a historical winner or close GC-10/D5R.

## Original failure producers

Original source is frozen in `.local-work/d5am/guard-final02/candidate/` and
matches the retained 0.9.1 build receipt. Source line references below refer to
the original files under `runtime/construction-winner/`, not a repaired copy.
The exact built objects, DLL, source manifests and old packages are protected
by `.local-work/d5an/baseline.json`.
Numeric fault names denote masks: `0x1` saturation, `0x2` original attempt
exhaustion and `0x4` new checked underflow, rather than bit-position indexes.

| Original producer | Exact operation and source location | Effect and relevant callers |
| --- | --- | --- |
| Scheduler C++ increment | `d5am_scheduler.h:68–74`, `next`/`increment`; weak CAS, at most 32 attempts | MAX sets scheduler bit 1; exhausted attempts set bit 2. Both set scheduler failed; overflow also sets the inherited core overflow flag. |
| Scheduler C++ admission | `Producer`, lines 78–83 | Calls `next(winner::active)` then `next(scheduler::active)`. Destructor unwinds only counters actually acquired. A second-counter refusal must release the first. |
| Scheduler ancillary counters | `next` callers for drops, reentrant, tokens, registry faults and identity faults | The same aggregate bit 2 can arise in telemetry or allocation accounting, not only initial active admission. Refusal may happen before event reservation or useful error accounting. |
| Registry publication serial | `identity`, line 120 | A two-step serial transition is refused above MAX−2 and directly sets scheduler bit 1. A busy registry CAS is scientific uncertainty with an incremented registry diagnostic; it is not itself bit 2. |
| Registry retirement serial | `identity`, line 140 | Separate serial overflow path, also bit 1. |
| Scheduler written | `advance_written`, line 228 | Saturates at MAX and sets bit 1. Worker-owned rather than a native producer counter. |
| Scheduler ASM core admission | `d5am_scheduler.asm:162–209`, core loop at 168–179 | At most 32 strong hardware CAS attempts on the shared core active object. Exhaustion sets scheduler bit 2; MAX sets bit 1. |
| Scheduler ASM bridge admission | Same macro, bridge loop at 184–196 | A separate counter object, same bits. Failure rolls back the acquired core count. Disablement after admission releases both. |
| Causal C++ increment | `d5am_causality.h:58–64`, `bump` | Independent 32-attempt weak-CAS helper. Exhaustion sets causal failed; MAX additionally sets causal overflow. It does not set the scheduler aggregate or native causal bit 2. |
| Causal C++ admission | `Producer`, lines 90–93 | Own counter first, core second. Original destructor's short-circuit `||` can skip the second decrement if the first returns zero. This is an injected-corruption/accounting counterexample, not proof it happened in N1. |
| Causal ASM admission | `d5am_causality.asm:96–143`, two counter loops | Same core/bridge ordering and bounded loops, but a distinct native causal aggregate. Exhaustion is causal bit 2; MAX is causal bit 1. |
| Queue reservation | Both headers' `emit` loops | Separate 32-attempt reservation limits, finite capacity and signed ticket-range guards. Refusal is actual dropped event/failed recording; it is not scheduler counter bit 2. Reentrancy also records loss. |
| Existing core/geometry/lifetime accounting | Retained observer, geometry and lifetime headers | Other writers of the same core active object and additional queue/epoch/token counters. Their increments/decrements compete with the new channels. Their preexisting overflow/corruption assumptions are not silently replaced by the new helper. |

## Full relevant native edges

Scheduler `enter_producer` expands in five actual bridges: activated, dispatch,
retire, ready-tree and dependency decrement. Each expansion has two bounded
counter loops in the original object, for ten machine admission sites. Original
macro expansions begin at source lines 237, 255, 278, 296 and 329. Claim/queue
entry bridges instead reach C++ proxies, so the C++ admission paths are required
in addition to the five assembly bridges.

Causal `enter_producer` expands in ten bridge functions: pending, acquired,
recursive, reader registration, reader release, writer release, recursive
release, reader-ready, inline writer release and inline recursive release.
Original source expansion lines are 164, 207, 249, 290, 333, 379, 422, 465, 505
and 557. These yield twenty original native counter loops. Typed reader release
sites share a bridge implementation while retaining distinct site return
addresses. An object function is not interchangeable with a game hook site.

The sixteen causal game RVAs, thirteen scheduler RVAs, six original scheduler
CALL destinations, three vtables, callback and complete native-helper guard
domains are enumerated with their exact original hashes in the candidate build
receipt. Those game RVAs remain the 1.16.244.0 domain, image base `0x140000000`,
executable SHA-256
`7e9adb1414a8e1b325e5e1f097b9b17b78deb7eebeda37a333351a43a60f9d28`.
Observer DLL RVAs use a different image and must never be added to that game
base. COFF disassembly offsets and native source lines are separate domains.

The independently executed `d5an_native_census.py` preliminary inspection retains
six exact original artifacts, their hashes, complete disassembly and 422 selected
original/candidate symbol references in `.local-work/d5an/native-prelim03/`.
The candidate portion is superseded; the original 0.9.1 objects are unchanged.
In original `transport.obj`, standalone `scheduler::next` performs hardware
LOCK CMPXCHG at COMDAT section offset `0x10`, compares its failed-attempt count
with 32 at `0x1a`, sets bit 2 at `0x20` and MAX bit 1 at `0x3d`. There is no
software-only spurious-failure branch in this exact lowering. The constructor's
inlined core/own exhaustion writes are at section offsets `0x53`/`0xa4`;
its corresponding saturation writes are `0x11f`/`0x14d`.

| Original scheduler ASM symbol | Core exhaustion write | Bridge exhaustion write |
| --- | --- | --- |
| `D5AM_sched_activated` | `0x1ec` | `0x22e` |
| `D5AM_sched_dispatch` | `0x7a4` | `0x7e6` |
| `D5AM_sched_retire` | `0xd5b` | `0xd9d` |
| `D5AM_sched_ready` | `0x1312` | `0x1354` |
| `D5AM_sched_dependency` | `0x1920` | `0x1962` |

These are COFF text-section offsets in `d5am-scheduler.obj`, not function-relative
offsets or DLL RVAs. Every row is an actual LOCK OR to the original scheduler
aggregate. Original causal text-section exhaustion pairs are pending
`0x96/0xd2`, acquired `0x300/0x33c`, recursive `0x55e/0x59a`, reader
`0x7b8/0x7f4`, reader release `0xa23/0xa5f`, writer release `0xc93/0xccf`,
recursive release `0xefe/0xf3a`, reader-ready `0x1169/0x11a5`, inline writer
release `0x13bd/0x13f9` and inline recursive release `0x1653/0x168f` in
`d5am-causality.obj`. Those writes target the separate causal aggregate.

The original C++ compiled inventory also contains saturation/exhaustion writes
in Producer, next, increment, lose, emit, snapshot, identity and written/drain
instances. COMDAT instances repeated across transport/fixture/plugin objects
are compiler instances, not three independent logical runtime counters. Metrics
and guard references in the raw inventory are consumers rather than producers.
Final `.local-work/d5an/native-final01/census.json` inspects the actual final09
DLL and all original/new objects, retaining 1,112 selected references and complete
raw disassemblies. The original assembly text sections match uniquely in the
0.9.1 DLL at scheduler RVA `0x53cb0` and causal RVA `0x52450`; add the table's
COFF section offsets to those bases for the exact original DLL instruction RVAs.
Final09's corresponding section RVAs are `0x5fff0` and `0x5e810`.

Matching masks only declared COFF relocation fields and compares every remaining
code segment. It does not claim that masked fields were byte-identical or that
an object section offset is already a DLL RVA. Original scheduler Producer,
emit, identity, increment, lose, snapshot and drain bodies match uniquely at
RVAs `0x4400`, `0xd950`, `0x10840`, `0x10d50`, `0x10eb0`, `0x1a210` and
`0xa9d0`. Thus the original constructor's actual core/own exhaustion writes
are DLL RVAs `0x4453`/`0x44a4`, with saturation at `0x451f`/`0x454d`.
The original causal Producer is at `0x4340`; guards are at causal `0xe4d0` and
scheduler `0xfd60`, and worker body at `0x1afb0`.

Unmapped standalone next/bump/advance-written COMDAT bodies are not invented as
live functions: their relevant operations occur in retained inlined callers.
The raw census marks every unmapped/ambiguous body explicitly and binds mapped
instruction references to their owning DLL. Final helper export RVAs, observer
module domain and actual producer return addresses are independently checked
against the exact final PE in the 176 diagnostic controls.

## Startup, producers and terminal admission

```text
configure original sites/targets -> write identity/open core outputs
  -> initialize core queue -> install exact bridges -> begin sidecars
  -> worker initial guard/disk pass
  -> external READY -> controller ownership/challenge/request -> owned ACK

scheduler registration/callback/queue wrappers
  -> enabled + begun gate -> C++ Producer -> snapshot/identity -> emit
scheduler claim wrapper
  -> C++ Producer unconditionally -> original claim -> conditional matched emit
scheduler five typed ASM bridges
  -> enabled + watched vtable gate -> core admission -> bridge admission
  -> native operation / C++ capture -> independent releases
causal generic ASM bridges
  -> enabled gate -> core admission -> bridge admission
  -> displaced native operation -> watched receiver filter -> optional capture
  -> independent releases
causal capture/register/lifecycle/exclusive/visited completion
  -> C++ Producer -> enabled/begun/context checks -> optional emit

worker guards/drain + sticky failure state -> refuse health on hard failure
STOP/failure -> disable capture -> await admitted producers -> final drain
  -> final failure aggregation -> resident-inert terminal
```

The last failure-aggregation edge is a required repair: original worker checks
could miss a hard sidecar fault occurring after the last guard while STOP waited
for a held producer. Its terminal must not claim success merely because final
drains succeed. Exact final implementation and deterministic test pass the recorded
independent qualification.

The unconditional claim wrapper can contend on the shared active objects
before a relevant task exists and can still touch accounting after disablement.
Generic causal native operations also admit before the watched-owner filter.
These are concrete ways of obtaining counter traffic with no relevant emitted
sidecar events. They do not establish that N1 actually took either path.
Resident-inert means capture is disabled; it does not promise that every resident
wrapper will cease executing or that an active-count snapshot stays zero forever.

## Mechanism, alternatives and limits

The retained terminal and CRC/identity-bound bytes are independently authenticated
by `evidence01.json`. One internal READY and three header-only sidecars cannot
recover a counter/site/thread that the old schema never stored. The observed
scheduler bit 2 is compatible with any mapped bounded scheduler counter producer.
It does not establish capacity exhaustion, a geometry regression or changed
instruction bytes. Corruption and unobserved timing remain alternatives; neither
is proven by zero telemetry or by a successful new fixture.

The sticky scheduler bit is independently sufficient for guard refusal, but the
combined causal/scheduler reason cannot exclude an additional simultaneous byte
or relay failure. Initial guard success precedes READY publication; the fault's
exact onset can be in that gap or later. No fault timestamp or unique first
short-circuit guard is retained.

The old algorithm can refuse after 32 genuine interfering admissions while
the active count is only 32. The controlled witness uses an instrumented copy
of the old loop and real competing causal Producers on the actual shared
object. It omits the old sticky write so the comparison can continue; original
source/native inspection separately establishes that write. The repaired branch
uses the actual integrated scheduler Producer and survives forty controlled
interferences. This is a bounded mechanism proof, not historical N1 replay.

C++ weak-CAS semantics permit spurious failure in general. The relevant exact
MSVC x64 lowering must be assessed from its actual LOCK CMPXCHG instructions;
the language allowance alone does not establish spurious failures in this
binary. Overflow, two-step serial saturation, queue capacity, reservation-attempt
exhaustion, recursion and partial teardown are separate controls.

The repair uses strong saturating CAS with `Sleep(1)` after a real comparison
failure. It removes the contention-fatal attempt quota, preserves MAX/zero
refusal and uses fixed storage. Each failed strong comparison witnesses an
intervening mutation; the helper acquires no lock of its own. Progress still
depends on scheduling and finite producer work. Sleep(1) requests one millisecond
and can resume much later; no latency bound, wait-freedom, uninstrumented
scheduling equivalence or retail winner distribution follows.

Callers can retain gates while the helper yields: scheduler publication holds
an odd registry serial while allocating a token, and causal owner registration
holds its registration flag while incrementing registry/generation counters.
Other clients return RegistryBusy or record unknown baseline rather than wait
for those gates. The helper acquires neither gate, so this graph introduces no
identified lock-wait cycle, but longer uncertainty windows and STOP latency are
possible. Existing busy controls establish refusal behavior, not its frequency
or duration. The superseded source comment “No lock is held across the sleep”
was scoped to helper-owned locks; corrected source explicitly names caller gates.

Queue reservation retains its existing bounded-work and finite-capacity policy.
It can still lose an event under contention; that genuine integrity loss remains
fatal and explicitly accounted. No-drop counters alone prove neither complete
event coverage nor retail reliability. The original protected save, prediction,
N0/N1 outcomes and 0.9.1 guard repair remain unchanged.
