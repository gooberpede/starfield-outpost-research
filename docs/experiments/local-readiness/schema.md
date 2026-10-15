# Event and loss contract — schema 8

**Current disposition: NO-GO.** Schema bytes and observer code are unchanged. This repaired description remains historical documentation; see [the scientific reassessment](scientific-value-reassessment.md).

[Implementation](../../../runtime/local-readiness-080/capture.h),
[transport](../../../runtime/local-readiness-080/history.h), [native map](native-map.md).
All scalar bytes are little-endian. Event size 3328: twelve u64 fields
sequence/invocation/parent/thread/QPC/site/kind/phase/reference/command/result/status,
four u64 arguments, eight 400-byte blobs named ref/base/extra/cell/world/operand/
aux/output. Blob = address u64, length u32, read-ok u32, owned bytes[384].
Phase 1/2/3 means before/normal return/unwind. Session declares version 0.8.0,
schema 8, event size, PID/creation FILETIME, actual base, QPC frequency and hashes.

Tags 101–110 retain [the 0.7.0 roles](../../../runtime/beacon-resource-070/README.md).
Tag 111, SOURCE_VISIT, records the four forwarded argument channels. Blob `ref`
contains the 0x18-byte closure; `operand` contains the 8-byte source-value slot;
`reference` identifies the pointed source; `base` contains its 0x40-byte header.
Tag 112, PROVIDER_BOUNDARY, records Int2 in `ref`, a 0x78-byte ProcGen snapshot in
`base`, and the 8-byte aggregate output pointer slot in `output`, before and after
the call. The captured return is not assigned a success or geometry verdict.

Persistent sequence is **worker serialization order**, not callback admission
order or a total engine chronology. A detached SLIST batch is reversed to FIFO;
concurrent publishers may interleave. Invocation identity is atomic, parent is
TLS, and QPC/thread phases qualify causal nesting. Decoder rejects mismatched
thread/site/parent, duplicates and unpaired scopes. No timestamp-nearest joins.
IDs are process/session-local. Asynchronous queue identity is a candidate link;
the queue does not carry a population snapshot.

Status bits inherited: 2 missing population read; 8 changed header reread;
0x100 unwind; 0x200 observed writer overlap; 0x400 bad final-row range;
0x800 completion after STOP; 0x1000 wrong model/getter. New 0x2000 means snapshot
capacity exceeded and admission failure. Member/header read statuses retain
their separate meanings. Header equality does not exclude member ABA or an
unhooked writer. Writer overlap is a warning, not full concurrency coverage.

NOT_OBSERVED: provider hit/miss, constructor exit reason, reset/publication epoch,
initialization before capture and actual translation table. UNAVAILABLE: a blob
read failed or population/ancestry is incomplete. UNQUALIFIED: full region geometry
and accept/reject replay. UNKNOWN: readiness completeness/freshness/player-location
independence. None is encoded as a default zero semantic value.

Callbacks allocate no event storage dynamically and perform no file I/O, hashes,
disk queries or waiting locks. Windows interlocked SLIST APIs publish to a fixed
4096-node pool; finite vector/row walks allow at most 256 entries per collection.
Queue exhaustion or snapshot overflow is sticky instrumentation failure, closes
admission and remains visible through failed/losses/queued counters. The worker
alone writes events.bin and records.jsonl, group-flushes and reports durable
sequence. A stopped admitted scope still completes into the queue. STOP does not
unpatch or unload wrappers. Real worker failure preserves partial evidence.

Each WAL line binds offset, size, worker sequence and SHA256. Decoding validates
raw/WAL bytes, phases and terminal attempted/written/durable/queued/loss counts.
A useful verified prefix may survive a corrupt/partial tail; no decoder trims or
repairs originals. A writer failure can lose an unpersisted detached suffix;
this is explicit incomplete evidence, not a lossless claim. Queue integrity and
target survival remain separate from scientific completeness.
