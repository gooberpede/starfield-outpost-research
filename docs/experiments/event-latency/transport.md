# Durable transport and timing contract

SOR-EXP-0026, external adapter0.1.3; original implementation in
[epoch_writer.h](../../../debugger/event-oracle/epoch_writer.h),
[materializer](../../../debugger/event-oracle/materialize_epochs.py) and
[profile.h](../../../debugger/event-oracle/profile.h). Native ABI/site/pairing/
replay remains the [0.1.2 contract](../event-instrumentation/contract.md).

## Append format

`evidence/epochs.wal` is an original little-endian framed stream:

| Bytes | Meaning |
|---|---|
| 0..7 | ASCII SOREP013 |
| 8..15 | Payload byte length, uint64 LE |
| 16..23 | Consecutive record sequence starting1, uint64 LE |
| 24..55 | Previous frame digest; zero32 for first |
| 56..87 | SHA256(sequence LE8 + previous digest32 + payload) |
| 88 onward | UTF-8 JSON payload; raw records include exact bytes as data_hex plus section hash/length/address/origin/acquisition UTC |

Outer record sequence is distinct from adapter event sequence, native invocation
ID and raw file numbering. Event payloads retain original QPC/frequency, module/
RVA, TID, scope/parent and UTC; raw memory addresses retain runtime-VA domains and
register evidence retains its zero sentinel/origin. Hash chain detects complete
frame changes/reordering/removal in the middle. Final truncation/removal cannot
be distinguished from an earlier stop without independent receipts/terminal state.
No cryptographic authenticity or completeness-from-hash claim.

The writer checks the40-billion caller-available guard before each record/chunk,
writes to its sole new append handle and calls FlushFileBuffers before acknowledging
that logical operation. No per-boundary aggregate delays a completed field's
durability. A valid recovered frame proves retained bytes, not that a flush which
reported failure succeeded. The decoder's `committed_frames` means complete,
hash-valid framing, not independent power-loss proof. No hardware power-loss
simulation was performed. Adapter failure paths restore/detach before reporting.

The decoder preserves a complete verified prefix and reports an incomplete final
header/payload as tail bytes; it never repairs or overwrites originals. Bad magic,
sequence, prior hash, complete checksum or raw extent/hash is fatal. It validates
the entire readable stream before creating any derived output. Materialization
requires a NEW directory, uses independent sequential raw names, fsyncs outputs
and records source WAL hash/chain/tail. Terminal markers are derivative only when
the source has a terminal and no incomplete tail. A failed derivative is retried
into another new directory, not promoted by its existence.

## Timings and attribution

QPC accounting starts immediately after WaitForDebugEvent returns and ends just
before ContinueDebugEvent. Nested scopes switch exclusive buckets, so categories
sum to stopped handler time without counting memory inside patching twice:

- memory: Remote.bytes range check and ReadProcessMemory, including patch guards;
- writer: encoding/hash/construction/write/flush, plus baseline file open/close;
- control: Get/SetThreadContext, code protection/write/cache flush/verification,
  excluding memory reads counted above;
- suspension: explicit Suspend/ResumeThread paths;
- guard: GetDiskFreeSpaceExW checks, including checks nested inside the writer;
- other: collector allocations/decoding, pairing, event construction and remaining
  handler work; QPC instrumentation overhead is included, not subtracted.

ContinueDebugEvent API duration is recorded separately. Time from its return to
the next replay single-step delivery is a **transport/scheduling/one-instruction
upper bound**, not an exact kernel transport measurement. All other wait time
includes target execution, deliberate fixture sleeps and polling; it is reported
without attributing it to debugger transport. Breakpoint notification delay before
WaitForDebugEvent returns is unmeasured. No claim of an exhaustive end-user pause
or pure OS-overhead decomposition is made.

Auxiliary timing JSON is written after detach; it is not the authoritative capture
and is not guaranteed crash-durable. Profiling changes only timing instrumentation,
not the native control protocol. Sample arrays grow with event count; allocation
failure follows existing restoration rather than silently discarding samples.
The runner's1200-second per-phase wait limits a finite disposable test, not live
acquisition. No event/hit/time/file quota or background writer queue is introduced.
