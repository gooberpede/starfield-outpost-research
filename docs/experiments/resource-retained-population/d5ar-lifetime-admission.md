# D5AR owner and source lifetime admission

2026-11-05, Australia/Sydney. **STATIC AND OWNED CONTROLS / REVIEW-REQUIRED.**
Epoch validation rejects overlap but cannot prevent a read racing a free. The
current candidate protects every borrowed owner/map read with an admission
barrier in addition to the existing native reader. The separate source-ending
gate protects source scalars against retirement and reuse. The reviewed
ordinary native graph, exact method identity and fresh acquisition provenance
remain necessary; successful file validation does not prove those premises.

## Ordering and current binding

The pinned original area consumer starts at `0x1421e07d0`. Its actual entry
bridge samples the operation's epoch **before** the original body loads the
manager singleton at `0x1421e09d4`, loads its `+0x130` ProcGen at `0x1421e09db`,
acquires the native reader at `0x1421e09ed` and calls the protected callback at
`0x1421e0a46`. The callback is not supplied an already-selected ProcGen by the
established-operation caller. These are preferred static VAs in the pinned
Starfield build, not runtime pointer tokens. Full original instructions are in
the [native record](d5ar-native-investigation.md) and its D5V provenance.

The callback must obtain a generation-checked observer shared lease without
waiting and see zero admitted lifecycle phases. It verifies the entry epoch
before borrowing native memory. Under that lease it reads the current binding;
missing/incomplete binding or a different attached ProcGen refuses **before**
any holder-slot, ProcGen or map read. A complete current binding is a geometry
safety precondition, not merely a source-identity hint. Then the actual foreign
native reader and observer lease jointly protect the holder/resource/region/point
traversal. Final binding reads remain inside the lease.

Replacement at the same address after native entry changes the epoch and
refuses with zero borrowed reads. Replacement before entry can yield the newly
selected current ProcGen; this establishes no historical allocation continuity.
The observer does not validate an arbitrary corrupt engine pointer or repair
the original engine's behavior outside the reviewed ordinary graph.

## Why the two locks do not invert

| Path | Observer acquisition and release | Engine interaction |
| --- | --- | --- |
| Borrowing callback | Try shared lifetime admission; require no active phase and current entry epoch; hold through all owned copying; release in `finally`. | Already holds the original ProcGen reader. It never waits for the lifetime gate while holding that reader. No game method is called under the observer lease. |
| Whole lifetime phase | Brief exclusive admission waits out existing shared copies, publishes active count and epoch, then releases. `finally` updates the epoch before decrementing the active count. Nested same-thread phases use the admitted outer scope and balanced counts. | The original initializer, installer, reset or destructor runs with **no observer mutex held**. It can take or wait for its own engine locks. |
| Source scalar group | Under the lifetime lease, holds shared source admission for the entire fixed diagnostic group, then releases. | No source pointer is followed if history is unavailable or its address ever retired. No geometry allocation, game method or file IO occurs under the source group gate. |
| Source ending CALL | Under exclusive source admission, records only the existing address operand; releases before forwarding original free. | The two original ending sites are after ProcGen erase/unlock. No source read or lifetime-gate acquisition occurs under source-exclusive admission. |

An observer mutex held across an entire phase would be unsafe: B030 can enter
the installer with manager exclusive already held, while another phase can
acquire that engine lock inside its original body. The admission barrier does
not serialize the two original mutators. A phase waiting for an engine reader
does not make the callback wait for an observer lock: the callback refuses and
returns to the original consumer, which can release its native reader.

Source and owner guards are separate. The owner barrier cannot establish that
an already retired source key was never published late. The [ending proof](d5ar-source-frame-proof.md)
and [fresh-process preload history](d5ar-preload-history.md) supply the other
premises: every actual ending address is marked before free; reuse never clears
the mark. The source-group copy establishes owned bytes at that time only.

## Exceptions and operational limit

An abnormal original lifecycle phase disables future borrowing before its
active count is dropped. Original C++/SEH exceptions propagate. Later native
phases forward in the sticky inert state; observer failure does not repeatedly
raise in ordinary teardown. If a command is already armed, a phase failure can
produce one failure-only owned tombstone, with no new borrowed reads or geometry.

The supported reader performs fixed checked memory reads, ordinary nonalertable
OS operations and stock CRT allocations without engine-reentrant callbacks.
The approved effective load set must preserve that contract. A deliberately
reentrant allocator or new handler that dispatches and waits on engine work is
outside it. A current-thread copy-to-phase upgrade is an unsupported protection
fault: the candidate propagates a private exception before native mutation,
disables copying and releases observer leases. This can abort native control
flow; it is not claimed to be ordinary successful read-only operation. No
fail-fast, game termination, hot unpatch or original exception suppression is
implemented. The pilot remains separately approvable and unexecuted.

Normal snapshot publication follows the original consumer's return and reader
release. Failure-only publication carries no geometry and reports native reader
release UNKNOWN if original unwinding prevents that conclusion. A healthy
source-only refusal retains complete holder geometry and does not itself call
for machine emergency action. The exact adverse tests and package pins are in
the [native record](d5ar-native-investigation.md) and [handoff](d5ar-handoff.md).
