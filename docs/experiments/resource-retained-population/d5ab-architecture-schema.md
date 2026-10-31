# D5AB observer architecture and schema delta

**INCOMPLETE / REWORK.** This working record is subject to the
[bounded handoff](d5ab-report.md), including unfinished native coverage,
operational integration and review. It grants no implementation or B2 authority.

Candidate 0.3.0 uses `sor-d5x/3`. It retains all fourteen original boundaries,
adds four [qualified candidate sites](d5ab-native-map.md), and retains the
312-byte payload and 16-byte framed transport. Original `sor-d5x/2` inputs take
their unchanged reduction path; B1 append success is never manufactured.

## Capture and identities

Events 1–13 retain the [D5X field layout](d5x-schema.md). The versioned changes
and new kinds are:

| Kind | Fields and interpretation |
|---|---|
| Entry, 1 | `c` additionally records current loss generation. |
| Visited, 3 | `a` remains branch decision; `b` is engine-consumed RDI token; `c` is loss generation. Source pointer is recorded without dereference. |
| Cold, 12 | `c` records loss generation at the protected empty-state witness. |
| Birth, 14 | `source` is new R14 allocation; `holder` is Grid; `selection` is a new observer allocation ID; `a` is native constructor token; `d` is loss generation; prefix bytes are copied while constructor-private. |
| Published, 15 | `source` and `holder` identify allocation/Grid; `a` is actual vector-store destination; `b` is native index. Emission follows the actual pointer store. |
| Reserve, 16 | `a` is low-u32 return, including failure sentinel; `b` is pre-call packed count/capacity; `c` is post-call packed count/capacity; `d` is resulting data pointer. Context/status and original source/request remain attached. |
| Stored, 17 | `a` is actual token-store destination; `b` is consumed RDI token; `c` is loss generation. Emission follows the actual store. |

Packed count/capacity uses low/high u32 respectively, little endian. Geography
is decoded independently from constructor bytes and protected lookup bytes.
An observer allocation ID is process-local; it is not a game allocator cookie,
reference handle, FormID or persisted identifier. The birth/publication/lifecycle
proof establishes its admitted lifetime. Equal tokens never merge allocations.
Equal geographic keys never merge pointers or lifetimes. Ambiguity is explicit.

Records preserve native QPC ticks, thread, invocation/parent and observer admission
sequence. Sequence orders reservation, not engine scheduling. QPC equalities or
cross-thread order uncertainty cannot prove birth-before-entry. Same-source map
decisions are additionally serialized by native exclusive protection. Operator
checkpoints are external intervals and never native arrival instants.

## Queue and worker

The default is 32,768 cells, with independently compiled 1,024 and 8,192 controls.
Every cell contains the 312-byte event plus an eight-byte ticket: the measured
queue is 10,485,760 bytes. Whole-process working set is separately measured;
it includes test data, stack, runtime and allocator overhead. Capacity choice is
based on actual concurrent queue tests and writer stalls, not idealized B1 replay.

Reservation/publication use release/acquire tickets. A reserved head blocks a
consumer until publication; later published cells cannot pass it. Snapshot drains
prevent continuous producers from starving raw/ACK flush, health and STOP. Raw
records are written in batches of at most 64; raw flush precedes cumulative
identity/CRC-bound ACK write and flush. No total session/record/byte cutoff exists.

Worker telemetry is a fixed array of count/total/max QPC ticks for wake interval,
drain, write, raw flush, ACK flush, guard, disk and shutdown. It also records
unpublished-head blocks, snapshot pressure, queue high water, contention, retries,
per-cause drops and loss generation. Telemetry is included directly in ACK and
terminal receipts; its sole copy is never queued in the lossy event stream.
Measurements include scheduling effects and do not uniquely identify storage
device latency. ACK construction precedes that ACK's own flush; later ACKs or
terminal output carry its timing. Legacy combined flush maxima remain distinct.

Admission retries are bounded to 32. Loss-metric minimum/maximum updates each
have at most 32 CAS attempts; inability to establish the sampled range sets an
independent uncertainty flag. This adds a bounded diagnostic cost on loss paths.
That uncertainty refuses scientific firstness for the remaining session while
safe acquisition continues. Exact loss-generation witnesses independently bind
birth, visited, protected cold state and successful store. Ordinary loss also
advances the global epoch; a clean stretch alone cannot restore firstness.

The original two-drive floor of 40,000,000,000 caller-available bytes, exact
EXE/SFSE/data/loader identities, site/target/relay guards, output fault handling,
active-producer shutdown and same-session nonce controls remain. STOP disables
acquisition, waits for admitted producers, drains and leaves original-forwarding
resident wrappers. No live execution is authorized by these controls.

## Scientific reducer

The reader authenticates identity, schema, full-u64 sequences, frame CRCs,
cumulative raw/ACK prefix agreement and acknowledged bounds before reduction.
Durable ACK loss telemetry remains relevant without a terminal receipt. Damaged
tails never repair earlier gaps. Byte integrity, native completeness, worker
success and target survival are independent results.

The version-3 reducer first evaluates the existing request/selection/visited/map/
descriptor/generator/direct-sample contract, then requires safe birth/publication
identity and the actual reserve/store transition. A new qualified empty-state
boundary and a complete source lifetime are needed after loss. Prior eligible
same-key/token decisions and any unresolved competing source that could contain
an earlier candidate prevent first attribution. Context failures, reset overlap,
retirement, reallocation, repeated/colliding identities, omitted prerequisites,
invalid count/capacity/destination and ambiguous native order are refused.

A complete prefix through successful append can qualify without a provider
return or later bypass. A later bypass is reported when independently joined.
No event certifies complete/nonempty geometry, authoritative saved state or
Workshop availability. A complete synthetic non-target lifecycle qualifies the
instrument's tested capability only. The Feynman V D5R parent remains **OPEN**;
historical B1 remains PARTIAL and D5AA remains ESCALATE.
