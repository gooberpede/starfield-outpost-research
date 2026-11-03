# D5AM upstream scheduler component

2026-11-03, Australia/Sydney. **The separate offline scheduler component passes
113 bounded engineering controls.** It observes typed task publication, activation,
readiness/dependency boundaries, dispatch, callback scope, queue/claim boundaries,
retirement and provider-to-task joins. Full candidate integration and independent
review remain separate. GC-10 and D5R remain OPEN; no live run is authorized.

| Element | Result and limit |
| --- | --- |
| Parent questions | D5AM-Q2/Q3: discriminate upstream progress before source-lock arbitration; this component does not accept either parent question. |
| Source baseline | Starfield 1.16.244.0, EXE SHA-256 `7e9adb1414a8e1b325e5e1f097b9b17b78deb7eebeda37a333351a43a60f9d28`; preferred static image base `0x140000000`. |
| Native grounding | Existing D5AE/D5S/D5R exports, actual installed instruction/site and vtable guards. No Ghidra execution or database access was needed. |
| Engineering result | Compiled production header and bridges on owned synthetic task backing; original-instruction ADD/flags oracle; bounded identity, ABI, concurrency, loss, STOP and overflow tests. |
| Unknown | Actual normal-retail registration/readiness/claim histories and usual winning request/mask. No tested retail scheduling distribution follows from synthetic policy calls. |
| Next step | Integrate the exact component into the separate candidate, replay actual producer spools into independent readers, run old observer regressions and obtain exact-source independent review. |

## Exact component and methods

Production candidate sources are
[d5am_scheduler.h](../../../runtime/construction-winner/d5am_scheduler.h) and
[d5am_scheduler.asm](../../../runtime/construction-winner/d5am_scheduler.asm).
They are new derivative inputs; the original 0.7.0 source tree, DLL, frozen plans
and packages are unchanged. The
[qualification driver](../../../research/resource-retained-population/d5am_scheduler_qualify.py)
compiles the component with an
[owned C++ fixture](../../../research/resource-retained-population/d5am-scheduler-fixture.cpp)
and a separate [assembly ABI oracle](../../../research/resource-retained-population/d5am-scheduler-fixture.asm).
All are source-informed maintainer-owned methods under SOR-P-0002; native bytes
and exports remain local Bethesda-derived research evidence.

Invoke installed Python with `-E -B`, repository cwd and a fresh bounded label:

```text
research/resource-retained-population/d5am_scheduler_qualify.py scheduler-NEW-LABEL
```

The final component receipt is
`.local-work/d5am/scheduler-component20/qualification.json`. It records 113 PASS
cases, exact source hashes, installed PE identity, all native site windows and
actual caller-available disk space. The fixture DLL SHA-256 is
`149d37b7b9792bb7e807527836b3ea727f56448e037911068fa171c2cd971dc3`.
Its output directory retains the source snapshot and compiler/linker logs.
The component DLL is an owned test host, not an installable observer package.

Allowed effects are reading the installed pinned PE/retained exports and writing
fresh `.local-work/d5am/` builds, receipts and synthetic evidence; executing
installed MSVC/MASM and the owned fixture DLL; and temporarily mapping a private
host page for seven original ADD bytes plus the declared test entry/return glue.
The page is released after the oracle. Native host exit releases its remaining
backing. Both caller-available drive floors remain 40,000,000,000 bytes. Failed
identity, ABI, arithmetic, accounting or disk checks stop the affected test;
there is no game/process/deployment/save/configuration/network operation.

## Native boundary map

Addresses below are preferred static VAs for the pinned build. Configuration
verifies complete 32-byte windows, exact displaced instructions, original call
targets, three task vtables and the command callback before sole-thread install.
Runtime metadata records relocated addresses and hashes separately.

| Boundary | Exact site | Captured meaning |
| --- | --- | --- |
| Density pending / ready publication | `0x14076cea4` / `0x14076d07b` | Completed typed node before calling asynchronous native registration `0x1427e5630`. |
| Layer pending / ready publication | `0x1407b56c5` / `0x1407b57eb` | Same boundary for the layer node. |
| Registration activation | `0x1427ec100` entry | RCX/RDX are server/node pointer containers; copy their dereferenced values before the `+0x94`/state/rank predicates, preserving both original arguments. |
| Dispatch | `0x1427e6a00` entry | Node/server, current native state and actual incoming R8B before state 3 and dispatch processing. |
| Retirement | `0x1427e4ab0` entry | Invalidate the observed task allocation before destructor and allocator return. No freed-task traversal follows. |
| Ready tree | `0x1427e4957` | Exact-once displaced native tree-serial read into R9, before its later node `+0x88` store. Consumed value is recorded separately from the old node serial; neither is a successful insertion timestamp. |
| Dependency decrement | `0x1427e61a4` | Exact original decrement executes once; copy the resulting count and retain its branch flags for native `JNZ`. |
| Density / layer worker scope | `0x14076d14f` / `0x1407b585f` | Wrap the typed worker call; node is its actual adjusted argument minus `0xb0`. A nested scope restores its parent. |
| Claim helper | `0x1428d3960` entry interface | Preserve its five arguments and actual return; observe matching command data immediately after helper return. This is a return bound, not the queue CAS instant. |
| Queue publication | `0x1428d2b80` entry interface | Copy matching command/task/context before the original helper and emit its return using only the owned copy. Return fields are not a second context-memory snapshot. |

The typed vtable RVAs are `0x4b3d0e8`, `0x4b3d138` and `0x4b406b8`.
Their execution slots bind density callback `0x14076d140` and layer callback
`0x1407b5850`. These call the two inspected ordinary provider-producing workers;
the worker bodies and provider callsites are the existing
[D5AE pathway](d5ae-scheduler-causality.md), not newly observed retail coverage.
The generic command filter admits callback `0x1427ec2e0` and immediately copies
its task/server operands. Other jobs follow their original native paths.
All four qwords in each 32-byte vtable window have actual PE relocation type
DIR64. Original B2 positively used a relocated module base. A raw runtime hash
would therefore refuse that valid image. The final guard derives the actual
image base from the first pinned site, copies exactly those four image pointers,
checks their domains, normalizes them to preferred base `0x140000000` and hashes
against the unchanged static PE preimage. It never learns a new runtime baseline.
The worker repeats that canonical check. Metadata labels this basis
`preferred-image-vtable64/1`; unconfigured fixture policy tables are separately
labelled `unconfigured-fixture/1`. Component14's relocation-table census verifies
no relocation in all 34 listed code guard ranges: 28 site/callback windows and
full causal helper ranges, plus six original-call target windows. Those form
31 distinct address/length pairs, with overlaps; the four registration calls
share one target. They are not 34 distinct functions or disjoint byte ranges.
This component's set contains the earlier 11 causal sites and three helper
bodies alongside the scheduler ranges. The expanded candidate's separate
16-causal-site release census requires its own exact-source qualification;
Component20 does not stand in for that coverage proof.
The six original call destinations (four registration calls plus density/layer
workers) also have static PE-pinned 32-byte preimages, checked before admission
and on each worker guard pass. Initial runtime bytes are never accepted as a
new expected target baseline. Metadata exposes `scheduler_targets` with each
source site index, relocated destination and static hash. The actual workers are
`0x14076c560` and `0x1407b5160`, called by the typed callback wrappers above.
The activation's `MOV RBX,[RDX]` at `0x1427ec10a` and `MOV RDI,[RCX]` at
`0x1427ec10d` establish those container domains. The frozen assembly and its
independent ABI fixture already use that double indirection; stage-2's positively
recorded allocation and all-YMM/GPR/flag checks would fail if the container itself
were gated as a node. Dispatch uses RDX directly (`0x1427e6a13/1a`) and retirement
uses its RDX object directly (`0x1427e4aba/bd`); the domains are not transferred
between the three interfaces.

The common constructor `0x1403623f0` writes the native key, zero count/serial,
rank, mode and state/flag fields. Typed constructors then complete their vtable
and payload before the four publication calls above. The observer allocation ID
therefore starts after completed construction but **before asynchronous
publication**, rather than at a possibly reused callback address. This does not
timestamp the allocator's earlier allocation or reconstruct a pre-observer task.

Primary source locators are D5AE-N031/032/033/035/036/037/041/045/046/047/066/076/077/082
in the [existing source register](d5ae-sources.csv), plus
`.local-work/d5s/export29/native.tsv`, function `0x1427e4ab0`, lines 3262–3330,
and `.local-work/d5r/export02/native.tsv`, typed callbacks beginning at lines
702 and 723. The component receipt authenticates the five principal retained
exports; the local scheduler reading/source manifest records the additional
retirement/callback export hashes. Instructions were read in context; matching
source hashes alone are not the causal proof.

## Identity, copying and STOP

Each event copies node key bytes at `+0x08`, original signed Int2 at `+0xb0`,
three discriminator words at `+0xb8`, rank `+0x80`, serial `+0x88`, dependency
count `+0x90`, registered word `+0x94`, raw qword `+0x98`, raw byte `+0xa0` and state/flags
at `+0xa8`. The native key and payload discriminator remain distinct opaque
three-word identities; a pointer or equal key alone is not a new lifetime.
For kinds other than ClaimReturn, the wire name `pool` denotes the raw
`node+0x98` operand. The inspected common
constructor stores the two-word target callable at `+0x98/+0xa0`; this field
does **not** establish an actual worker-pool identity. ClaimReturn instead
copies its actual helper argument A into `pool`. QueueBefore, QueueReturn and
ClaimReturn copy the exact native tagged command operand into `extra`, including
its low tag bit. A matching command address/tag does not establish a task
lifetime: registry allocation/serial and native key checks remain mandatory.
QueueReturn retains the owned before-copy rather than rereading a possibly
reused command. Dispatch instead copies actual incoming R8B into `extra`, with
metadata `scheduler_dispatch_argument_schema=r8-low-byte/1`. Native entry
`0x1427e6a0f` saves this argument in ESI; tests of SIL at `0x1427e6ac0`,
`0x1427e6afc`, `0x1427e6b34` and `0x1427e6b61` affect dispatch paths. The raw
node `mode` byte at `+0xa0` is not this argument.

`ReadyTreeBefore.serial` still records the old node `+0x88` value. Its `extra`
now records the exact consumed tree serial, with metadata
`scheduler_ready_serial_schema=consumed-r9/1`. Native `0x1427e4950` sets R11 to
native RSP. The hook executes displaced `MOV R9,[RCX+0x50]` exactly once before
its callback, retains that actual value in saved R9, then replays only
`MOV [R11+8],RDX`: this writes the native stack slot, not a node field.
Unadmitted paths execute both original instructions. Later native code stores
R9 into node `+0x88` at `0x1427e497f` and calls insertion at `0x1427e4996`.
The consumed value is useful ordering evidence, not an observation of either
later operation completing. Engine serial UINT64_MAX is raw engine data and
does not trigger observer-counter overflow. A later dispatch snapshot may
observe the assigned node serial. Neither boundary is a queue CAS timestamp.

For the inspected typed workers, original task Int2 must match the provider's
original request; mismatch marks the association uncertain. The selected
neighboring source's coordinates are a separate identity domain and do not
relax this guard. The fixture explicitly challenges an original-request mismatch.

A bounded 32,768-cell registry issues a new observer allocation ID at typed
publication and invalidates it at retirement. Generic native probes copy the
native key and registry allocation/serial before the native operation and C++
callback. The producer subsequently verifies those copied values against the
owned registry. The private cell retains the exact vtable as well as its coarse
density/layer family, so replacing a node with another density vtable is not
silently accepted as the same identity. Changed-key and same-key address reuse, odd serials, duplicate
live publication, unknown preexisting tasks and full probe ranges refuse the
affected identity join. No worker follows a stored node, command, source or queue
pointer after the producer returns.

The queue has 32,768 fixed cells and a bounded reservation loop. Full queues,
contention exhaustion and recursion produce explicit loss/failure accounting.
Registry/identity faults remain scientific uncertainty, separate from byte
integrity. Saturating bounded CAS preserves maximum counter values; overflow or
unresolved counter contention is sticky and cannot appear as a healthy zero.
Registry serials and the worker's written count also refuse wrap.

Generic bridge producers participate in the existing `winner::active` handshake
and carry a separate `scheduler_bridge_active` counter. Every producer increments
its counters and then rechecks enabled before admission. If STOP has already
disabled recording, the producer rolls back its counters and offers no packet.
An admitted native bridge instead passes its admission through the internal
`*_admitted` adapter; disabling recording cannot silently discard that already
admitted prefix. Claim admission precedes the original helper. Saturated inner
counters roll back successful outer increments without wrapping the saturated
value. STOP leaves resident inert wrappers. Rejected probes still execute their
displaced native instruction but offer no new event. A stopped prefix does not establish native behavior after
recording ended, and a missing task completion cannot be filled from terminal
accounting. Unrelated observer epoch changes are copied as context, not used as
automatic task invalidation or a scientific STOP rule.

## Wire and worker contract

Schema is `sor-d5am-scheduler/1`. `scheduler.bin` has a 96-byte `<4Q64s>` header:
magic `0x314843534d413544`, version 1, payload size 272, reserved zero and the
ASCII session identity hash. Each frame is `<II>` size and CRC-32 followed by
`<24Q2i6I6Q>`. The source header names all fields and enumerates kinds/statuses.
The six context diagnostic qwords are copied at offsets `0x00`, `0x40`, `0x80`,
`0x88`, `0x90` and `0x98`; no undocumented queue semantics are assigned to them.
Identity also declares `scheduler_bridge_admission_schema=sor-d5am-scheduler-bridge/1`.
The packet remains 272 bytes, the registry cell 64 bytes, native cookie 48 bytes
and assembly save area 640 bytes; operand and admission additions introduce no
new hook site or pointer traversal by the worker.

The worker writes owned packets, flushes the file, and only then lets an ACK or
terminal expose `scheduler_written`. It emits no separate scheduler ACK file.
Complete admitted byte accounting requires written equal enqueued, no active
producer, loss, reentrancy, failure or counter fault, and valid identity/core
finalization. `scheduler_counter_overflow` and `scheduler_counter_contention`
are booleans; `scheduler_failed` includes their sticky native flags. Registry and
identity counts cannot justify a positive identity join in the presence of its
refusal status.

## Actual controls and preserved failures

The original 65-control milestone includes publication before synchronous work; density/layer
nested provider joins; unknown/duplicate/busy identities; changed-key and same-key
ABA; five generic native bridge ABI cases and two function-entry proxy cases;
all sixteen live YMM registers, GPRs, flags, LastError and actual Windows stack
walking; unmatched native filtering; four original PE ADD/flags oracles; queued
claim/publication boundaries; a producer paused after its native copied cookie
while retirement/reuse occurs; inert STOP; concurrent 40,000-offer queue
saturation; recursion; 65 colliding registry tasks; nine saturated counter
classes plus serial wrap; and all three Python optimization refusal modes.
Saturation losses are reconciled with offers and are not called lossless.
Five additional controls verify exact tagged-command copies, the actual owned
claim pool argument, refusal of a reused command with a foreign callback, no
allocation join for the same command tag after task retirement/reuse, and a new
allocation ID after qualified republication at that reused command address.
Six moved-base vtable positives include B2's actual high image-base value. Six
changed callback negatives, three invalid image-pointer domain cases and the
exact PE relocation-map census test the canonical guard independently of actual
retail hook installation.
Three copied actual PE callee windows pass the production target guard; changing
one byte in each owned copy refuses the static baseline. The PE relocation
census includes all six target windows (three unique destinations).

The final revision retains all 65 controls and adds 48: 34 STOP-cut interleavings
cover five native bridges, the two claim/queue assembly entry paths and ten C++
registration/callback/queue/claim/provider/capture paths at both sides of
admission; two exact-vtable/family substitutions; one original-request mismatch;
four saturation rollback cases; four actual dispatch R8B cases distinct from
the raw node byte; and three ready-serial cases. The pre-counter barrier sees
zero activity, disables recording, and proves resumed work cannot enqueue late.
The admitted barrier sees positive activity, disables recording, and proves
the admitted event prefix is retained. Original-helper call counts prove
admission happens before their invocation. Native arithmetic/flags, YMM state
and counter balance are checked after resumption.

These barriers execute actual producer/assembly admission primitives with owned
objects. Disabling the flag models the STOP cut; the component has no real
worker terminal/flush transaction. That integration remains separately required.
Its fixture-only probe pointer is zero in production and does not introduce a
live pause facility. Ready controls mutate the actual owned tree after its
native read, independently verify that mutation and preserve the original
returned R9/recorded serial for 0, 1 and UINT64_MAX. They also check the original
native stack MOV, flags and all sixteen YMM registers.

Component01–07 retain development failures involving MASM operand-size spelling,
C++/assembly symbol emission/export, ambiguous fixture aliases and the fixture's
LastError setup. Component08 passes 23 controls at its earlier source revision.
Component09 preserves the later fixture counter-alias build failure.
Component10 preserves its 38-control snapshot. Component11 is the fresh final
43-control revision carrying the command/pool operands. Component12 adds the
ASLR guard correction and passes 59 controls. Component13 refuses before native
compilation because the qualification's expected worker RVAs mistakenly named
the typed callback wrappers; direct PE call decoding and primary native exports
corrected that distinction. Component14 adds static original-target guards and
passes 65 controls; earlier outputs are not
silently substituted for it. These were owned-host failures, not retail failures.
After preliminary independent REWORK, Component15 passes 101 admission/identity
controls, Component16 and strengthened Component17 pass 106, Component18 adds
dispatch operands and passes 110, and Component19/20 pass 113 with consumed
ready serial and independent mutation verification. These new milestones do not
relabel the earlier 65-control snapshot or independently accept the revision.

The 78 `.bin` files beside the final receipt are **qualifier-authored derivative
frames around actual producer Event values**. They retain the original admitted
sequences after each drain. Synthetic identity `c` repeated 64 times is not a
production identity-hash preimage; these derivatives do not execute the real
worker spool/header/flush path or clear production-reader identity/sequence
requirements. Independent struct/CRC replay is useful, while refusal of an
incompatible production identity or incomplete sequence is correct. The merged
candidate must supply its own authentic scheduler file, identity and ACK/terminal
evidence for the end-to-end reader test.

The [fixture-only integration adapter](../../../runtime/construction-winner/d5am_scheduler_fixture.inc)
wraps an existing native geometry action with the production registration,
callback/TLS and retirement methods. Its owned task has explicit synthetic keys
and request `[10,11]`; temporary policy callbacks are restored on return. It must
never enter the retail plugin translation. A positive integrated task/provider/
geometry join tests these engineering links, not execution of the whole retail
task scheduler.

## Measurement influence and remaining coverage

Native gates avoid observer callbacks for unrelated task families, but matched
probes add bounded copying, registry/queue atomics, QPC and callback work. Full
YMM preservation and stack traffic also have a cost. These probes can change
relative progress and the eventual instrumented winner. A callback's QPC is a
measurement bound; it is not the engine's earlier queue or lock CAS time.
There is no fixture-derived normal-retail probability or fairness claim.

This component does not capture every upstream geographical ingress or file
dependency, all rank commands, every native queue CAS operand, or OS scheduling.
Its current task scalar snapshots discriminate actual observed progress while
preserving those gaps. Publication/activation/readiness, claim-return, callback
entry and exclusive lock ownership remain different boundaries. Full ordinary
path coverage and whether additional indispensable discriminators remain are
questions for the original-contract independent review; this component's PASS
cannot be used as documentation-only closure of D5AM-Q3 or GC-10.
