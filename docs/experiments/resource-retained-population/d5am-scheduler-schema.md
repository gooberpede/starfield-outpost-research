# D5AM task-observation journal contract

2026-11-03, Australia/Sydney. **OFFLINE CANDIDATE / NOT AUTHORIZED.**
This journal connects typed task publication, conditional readiness/dispatch,
worker scope and provider invocation. Exact original-site/caller/ABI qualification
and independent final review remain mandatory. It does not supply the missing
historical task events in B2, A0/A1 or B0.

## Representation and domains

Identity declares `sor-d5am-scheduler/1`. `scheduler.bin` has a 96-byte header:
four little-endian unsigned 64-bit words (magic `0x314843534d413544`, version 1,
event size 272, reserved zero), then the 64 ASCII SHA-256 characters over exact
session `identity.json` bytes. Every frame is a 32-bit length (272), 32-bit CRC32
of the payload and the 272-byte payload, with no additional padding.

The payload format is `<24Q2i6I6Q`. Its first 24 unsigned words are:

```text
sequence kind thread ticks node allocation family server rank serial
dependencies registered state_flags pool mode status core_invocation
core_selection source claim_context route epoch hazards extra
```

Next are two signed task-request coordinates, three unsigned 32-bit native-key
words, three unsigned 32-bit discriminator words, and six unsigned 64-bit queue-
context words. The native key comes directly from task `+0x08`; its words remain
raw native identity operands. Do not interpret the middle word beyond the
qualified source proof. Request/discriminator fields come from the typed payload
at task `+0xb0/+0xb8`. The request is the **task's** original Int2. In the two
mapped ordinary worker paths it passes unchanged into the provider, so a
qualified typed join requires matching original requests. The provider's
selected neighboring source and translated descriptor are separate coordinate
domains. Join them through the actual core invocation; do not substitute those
coordinates for the provider's original Int2.

The six queue words are direct copies at context byte offsets `0x00`, `0x40`,
`0x80`, `0x88`, `0x90` and `0x98`. They are diagnostics, not a later traversal
of borrowed pointers or an assertion that all six have decoded semantics.
Node/server/context/source values are runtime pointers within their qualified
event meanings. The field named `pool` initially copies raw node `+0x98`, part
of the native callable's two-word storage; it is **not** an established worker-
pool identity in those events. For ClaimReturn only, the revised producer copies
the actual claim-helper receiver/pool argument into that field. Exact source
revision determines which meaning is available. For ClaimReturn and both Queue
events, revised `extra` copies the raw tagged command operand immediately; that
operand is not a task pointer, allocation identity or proof of command lifetime
continuity after address reuse. Earlier zero values do not establish absence.
With `scheduler_dispatch_argument_schema=r8-low-byte/1`, Dispatch `extra`
instead copies the actual native R8 low byte; raw node `mode` is not that
dispatch argument. With `scheduler_ready_serial_schema=consumed-r9/1`,
ReadyTreeBefore `extra` copies the actual native R9 serial consumed from the
tree, while `serial` remains the older node-field snapshot. The displaced read
executes exactly once before this callback; the later native assignment and
insertion have not yet occurred. Earlier producer revisions do not supply these
operands merely because a zero field is present.
Allocation is a
private task-lifetime counter, distinct from native key, ready-tree serial,
source allocation, core selection and global observer epoch. Raw values remain
local. Timestamps are callback QPC ticks at the session's declared frequency.

Direct field copies must not be treated as an atomic aggregate snapshot unless
the particular native ownership/control-flow proof supplies that guarantee.
Rank, ready serial, dependency count and registered/state flags are distinct
properties; an observed callback does not retroactively timestamp their writes.

## Boundaries and refusal

| Kind | Boundary | Interpretation |
| --- | --- | --- |
| 1 | Typed publication | Private task allocation/key/family copied before the original asynchronous registration call. Already-existing or ambiguous tasks do not receive an invented birth. |
| 2 | Activation | Captured activation boundary and operands; eligibility remains conditional on the exact native predicate and dependency route. |
| 3 | Dispatch | Actual dispatch boundary, including native R8 low byte in `extra` under the declared operand schema; separate from registration, ready-tree consideration and eventual worker service. |
| 4 | Registry retirement | Ends the logical observed task lifetime. It is not proof of a physical allocator free. |
| 5 | Ready-tree before | Before the later node `+0x88` assignment and insertion. `serial` is the older node field; declared `extra` is actual consumed R9. Neither callback time nor consumed value timestamps successful insertion. |
| 6 | Dependency decrement | Instrumented native decrement boundary with original instruction/flag semantics preserved. Do not substitute a later field read for an unrecorded atomic instant. |
| 7 / 8 | Callback begin / end | Typed density/layer worker scope, including nested inline work and restoration of parent scope. |
| 9 | Provider join | Current typed task scope linked to actual core invocation/selection fields as available. Missing scope remains unknown, not proof of no contender. |
| 10 | Claim return | After the generic native claim helper returns. It bounds completed claim progress; it is not the exact queue CAS timestamp. |
| 11 / 12 | Queue before / return | Queue-publication call boundaries. Original claim-context/route operands remain distinct from later execution. |

Status bits are `0x001` read fault, `0x002` no birth, `0x004` identity changed,
`0x008` registry busy, `0x010` duplicate birth, `0x020` registry full,
`0x040` exceptional return, `0x080` no task and `0x100` counter overflow.
Such records preserve evidence but refuse affected scientific joins. Equal
node addresses or keys after retirement do not repair an allocation identity.
Native pre-operation identity cookies and later validation must prevent a paused
old probe from acquiring a new task's allocation ID.

Preallocated event and registry capacities and bounded probes are engineering
memory/latency bounds, not scientific event quotas. Saturation, reentrancy,
counter overflow and failed admission remain explicit. Native fast filtering
and callbacks still perturb scheduling, including claims and readiness head
starts. Unmatched native paths must preserve original registers, full live
YMM state, flags, LastError and instruction semantics.

## Durability and independent interpretation

Core ACK/terminal records include scheduler written/enqueued/active counts,
drops/reentrancy, registry/identity uncertainty and failed state. Native bridge
admission and counter-overflow/contention diagnostics supplement those counts.
The worker must flush the owned scheduler bytes before reporting the associated
written count. At completed STOP, counts agree with the framed file and both
C++ and native-bridge admitted producers have retired. Source-pinned tests must
exercise that actual path; a plausible terminal alone is insufficient.

The [independent reader](../../../runtime/construction-winner/d5am_read_scheduler.py)
checks complete framing/CRC/sequence, exact identity, typed terminal/ACK counters
and non-regressing fault history. It reports task/registry uncertainty separately
from byte/accounting completeness. Its task associations remain conditional on
native/site coverage and actual provider/core joins; it does not infer a retail
frequency or close GC-10.
Final identity declares `scheduler_bridge_admission_schema=sor-d5am-scheduler-bridge/1`.
Its ACKs and terminal must contain typed native activity and overflow/contention
flags, with zero native activity at terminal and sticky faults throughout the
history. `native_bridge_accounting_complete` distinguishes that proof from older
byte-valid journals without the declaration. The reader also flags incompatible
recorded family, key, original task request or discriminator within one clean
allocation; equal node pointers and a silent producer status cannot repair them.

The [reader controls](../../../research/resource-retained-population/d5am_scheduler_reader_controls.py)
independently encode synthetic complete-field/refusal cases. Optional component
replay decodes the actual compiled producer's queue-event derivatives, retaining
their original sequence origins and synthetic header labels. Those derivatives
are **not** authenticated production spool, session identity or worker-flush
evidence. Final integrated `scheduler.bin`, identity, ACK and terminal replay is
a separate mandatory check. No original capture is rewritten to make it pass.
