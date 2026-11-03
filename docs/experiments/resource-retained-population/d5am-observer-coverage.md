# D5AM observer coverage and extension decision

2026-11-03, Australia/Sydney. **The retained observer is insufficient to
discriminate the winner's upstream advantage or prelock delay from lock
overtaking. A targeted offline extension is needed.** This is a positive
missing-edge decision, not an adequate-instrument or readiness verdict.
D5AM-Q3 remains INCOMPLETE until that extension and its complete qualification
meet the original contract. No live operation is authorized.

## Inspected implementation and identity boundary

The root `runtime/construction-winner/plugin.cpp` is a historical schema-4
builder input, not the 0.7.0 retail candidate. The owned
`research/resource-retained-population/d5ai_recorder_build.py` derives 0.7.0
sources into a fresh ignored candidate tree and adds geometry, context and
lifetime channels. Authentic retained build/episode manifests must identify the
actual loaded DLL and derived sources; filenames and root version fields do
not establish them. Existing bytes, build16 and deployed packages stay unchanged.

Direct source inspection covered `observer.h`, `transport.h`, `patch.h`,
`plugin.cpp`, `read_capture.py`, the recorder derivation method and context and
lifetime channel definitions. Primary native provider/lock instructions were
read from retained exports, whose hashes are in the
[causality audit](d5am-native-winner-causality.md). This audit does not claim to
have executed a newly qualified observer.

## Stage coverage

VAs below are preferred static addresses for build 1.16.244.0, base
`0x140000000`. The base event record is 312 bytes; `emit` stamps QPC before its
queue admission CAS. Queue sequence is admission order, not a universal causal
clock. Source allocation, visited token, geographic identity, holder and task
are separate identity domains.

| Stage / original site | Existing observation | Identity and semantics | Missing edge or limit; influence |
|---|---|---|---|
| Ingress/registration `0x14079d080`, `0x1407af970`, `0x14076cd40` | NOT INSTRUMENTED | Provider request does not identify its producer task. | No request activation/registration history; hypothetical added probe can change readiness head start. |
| Dependency readiness `0x1427e70e0`, `0x1427e5e80`, `0x1427e6830` | NOT INSTRUMENTED | No dependency count, evaluator status or task lifetime join. | Equal constructor rank cannot substitute for effective readiness. |
| Ready-tree insertion/scan `0x1427e4950`, `0x1427e6d10` | NOT INSTRUMENTED | No effective rank/serial/route. | No proof retail winner was first ready or scan-first. |
| Dispatch/claim `0x1427e56d0`, `0x1427eb6b0`, `0x1428d3960`, `0x1428d3d38` | NOT INSTRUMENTED | No callback/task/pool/context identity. | Provider entry TID cannot identify prior owner/peer queue selection or inline dispatch. |
| Provider entry `0x14079f860` | Entry 1 | Invocation token, parent provider token, TID, original signed Int2, ProcGen and output holder argument. | No scheduler task identity; callback precedes native prefix and can alter progress. Returned 9 brackets the full provider call, not the visited callback. |
| Selection `0x14079fa90` | Selected 2 | Source pointer, selection token, frame and invocation; no delayed source dereference. | Selection is not eligibility's first possible instant or an owning source lease. |
| Shared acquisition `0x14079fc45 → 0x1422cc350` | NOT INSTRUMENTED | Native reader increment at `0x1422cc366`; tested mask excludes pending writers. | No reader cohort or wait interval. Foreign/unscoped same-owner readers absent. |
| Shared release `0x14079fc85` | Only implied before Visited 3 | Visited carries consumed token and native result after release. | Actual decrement/wake and release time absent. |
| Visited callback `0x14079fca3` | Visited 3 QPC inside callback | Same invocation/source/selection and consumed token; `a & 255` gives decision. | Stamp precedes queue admission and register/flag restoration; callback return is NOT INSTRUMENTED. Callback can delay exclusive call. |
| Exclusive call `0x14079fcb3` | NOT INSTRUMENTED | Lock is ProcGen `+0x40`. | No approach/entry interval. An approach timestamp would still not prove pending registration. |
| Pending writer `0x1422cc410` | NOT INSTRUMENTED | Atomic XADD adds `0x1000`, returning old packed state. | This exact transition is necessary to distinguish overtaking from later registration. Probe after transition can delay CAS and its own QPC can be later than another thread's acquisition. |
| Successful ownership `0x1422cc42b → 0x1422cc48f` | Only implied before Lookup 4 | CAS adds exclusive bits; success-only path publishes native TID and executes MFENCE. | No ownership transition or owner-wide contenders. Success-path callback extends ownership. |
| Protected lookup `0x14079fccb` | Lookup 4 after original lookup returns | Result/capacity/source stack operand, ProcGen, invocation and selection. | Miss/hit is measured under existing ownership. It does not time acquisition or enumerate waiting contenders. |
| Holder insertion `0x14079fdf9` | Native-implied between miss and generator | Existing holder and generation context support joins when full native interval applies. | No standalone insertion event; failure paths require original guards. |
| Descriptor conversion `0x14079feaf`, normalizer `0x14078d6f4` | Descriptor 5 | Original query and consumed stack-copy descriptor. | Descriptor callback occurs after authority. It cannot explain prelock delay. |
| Generation/sample `0x14079ff18`, `0x14079b8e8` | Generating 6, Sample 7, Generated 8 | Invocation/selection/source/output and ordinary sampled result. | Generator return does not alone prove complete nonempty output. Geometry channel independently supplies complete population under its protected copy conditions. |
| Visited reserve/store `0x14079ff3e`, `0x14079ff59` | Reserve 16, Stored 17 | Actual reserve result/before-after count and consumed token destination. | Failed reserve differs from successful store. Neither event captures release. |
| Exclusive release `0x14079ffa5 → 0x1402c45a0` | NOT INSTRUMENTED for ordinary provider release | Native final/recursive release and wakes have different effects. | No successor identity or reader/writer cohort. Lookup-to-return is not a measured lock-hold interval. |
| Source birth/publication `0x1409830cd`, `0x140983177` | Birth 14, Published 15 | Constructor-private bounded source bytes and owning Grid witness. | Positive allocation identity needs complete lifetime/fence history; pointer equality after retirement is inadequate. |
| Reset/destruction/clear/retirement | FenceBegin 10, FenceEnd 11; Cold 12 | Raw receiver domain depends on reason; context channel adds reasons 5/6. | Epoch is uncertainty accounting, not reset count. D5AJ permits proven other-Grid exclusion; an unrelated clear can still alter this same owner lock's other map entries. |
| Geometry/content lifetime | D5AI geometry and lifetime sidecars | Complete copied geometry and allocation/end journals, qualified with D5AJ attribution. | These channels do not add missing scheduler or arbitration events. Preserve all existing functionality in a derivative. |

## Completeness and loss

The existing queue has bounded producer CAS retries, full/contention/reentrant
loss counters, sampled loss bounds and overflow refusal. An event can receive a
QPC earlier than another event but be published later. STOP waits admitted
producers and drains their durable prefix; inert hooks remain resident.
Geometry and content-lifetime channels have their own accounting. Exact
terminal/flush/sidecar checks are necessary for evidence integrity, but zero loss
cannot establish coverage at a site that was never instrumented.

For the historical schemas, task registration, readiness, claim, pending XADD,
successful ownership, ordinary release and callback return are absent by design.
The two native-compatible histories in the
[causality audit](d5am-native-winner-causality.md#observation-equivalence-witness)
therefore remain observationally equivalent. Repeated mining of those streams
has no causal discriminator for those edges.

## Minimal justified extension and qualification boundary

The first useful component must record post-visited progress, exact pending
registration and success-only ownership with same-lock readers/writers. A
preallocated registry keyed by owner allocation/generation can filter generic
helper probes; it must begin from positive owner lifecycle evidence, declare
unknown preexisting participants, and refuse ambiguity/overflow/ABA. Unscoped
same-lock events must remain visible even with no provider invocation. Native
filtering avoids a C++ callback on unrelated locks but still adds instructions.

Upstream task registration/readiness/claim needs a separately proved
task-lifetime join into provider invocation. Common task constructor
`0x1403623f0` supplies a possible birth boundary; the ordinary density constructor
callsite is `0x14076cfef`. The constructor uses YMM operations. The existing
six-volatile-XMM bridge must not be reused there without liveness, ABI and unwind
qualification. No borrowed task pointer may be traversed later by the worker.

Required qualification includes direct original-instruction execution, competing
native winner continuations, callback-delay adversaries, owner-wide foreign
users, recursive paths, reset/retirement/ABA, registry/queue saturation, honest
loss and ordering inversions, thread/reentrancy/unwind preservation, independent
reader replay, protected old D5AK/D5AL geometry joins and owned STOP. Python
entry points must refuse optimization before effects. No offline test supplies a
normal retail frequency. A versioned component is not a deployment-ready full
candidate until the complete contract passes independent review.

**Decision:** extension required; no justified no-code adequacy disposition.
The earlier 0.7.0 observer, archives and frozen plans remain unchanged. The full
D5AM implementation/qualification status is controlled by the active ledger and
report, not inferred from this design analysis.

## Implemented derivative and bounded claim decision

The separate 0.9.0 derivative implements thirteen typed scheduler sites and
sixteen causal sites. The [owner census](d5am-owner-lock-census.md) finds five
necessary release edges beyond the initial proposal; three typed decrements
alone were not sufficient. The [scheduler component](d5am-scheduler-component.md)
records exact vtable/allocation identity, actual dispatch R8 low byte and actual
consumed ready-tree R9 serial. The latter is not a timestamp of successful
assignment or insertion. Source, task, owner and core invocation domains remain
separate; mapped original task/provider requests must agree, while selected
neighboring source coordinates can differ.

The new native bridge protocol admits activity before the displaced operation,
rechecks enabled state while that activity is held, and balances a cancelled
admission without recording. An actually admitted pre-STOP operation can flush
after disable; a thread paused before admission cannot enqueue after terminal.
Exact native fixtures and independent replay test both sides. Unknown baseline,
multiple owners or relevant registry transitions still refuse affected science
without becoming recorder failure or an automatic STOP.

ClaimReturn establishes that the helper selected and returned the copied task
command. For a qualified allocation, its publication stamp is a loose lower
bound and its claim-return stamp an upper bound on that claim. Those bounds
may overlap another task's interval. Input option bytes and later context
snapshots do not prove which owner/peer/global success branch supplied it;
return-QPC order is not exact claim-CAS order.

A narrower proxy pre-call QPC would be safe additional engineering, but is not
indispensable to the frozen mask forecast and pending-registration versus
admission-overtaking discriminators. Before a matching returned command is
known, that probe adds clock/error-preservation work to all generic claim calls.
The present design therefore retains the looser interval and explicitly refuses
earliest-claim and selected-queue-route causal claims. This is a reasoned
measurement boundary, not a claim that the edge is historically recoverable or
impossible to instrument. If a later conclusion depends on that stronger edge,
pursue the necessary authorized offline correction before making it.

The non-implementing reviewer challenges this decision against the original
contract and finds no inspected claim-return overstatement. Its final exact-
source acceptance remains separate. Complete ordinary receiver forwarding,
package/operational qualification, source locks and final review still control
the full readiness disposition. GC-10 and D5R remain OPEN.
