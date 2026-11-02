# D5AI dedicated content-lifetime journal

Versioned candidate contract; exact qualification and readiness are recorded in
the [component record](d5ai-recorder-qualification.md) and
[decision](d5ai-readiness-decision.md). This supplements the
unchanged schema-4 core event contract; it does not reinterpret historical B1/B2.
Raw1 development sidecars are retained and explicitly rejected by the Raw2 reader.

## Wire representation

The identity declares `sor-d5ai-lifetime/1`, header/event sizes 96, capacity 32768,
and three ordered sites. Each site records runtime VA, five stolen bytes, full
32-byte preimage SHA-256, typed kind and receiver-to-allocation adjustment.
For the pinned retail image the site RVAs are `0x7aab10`, `0x7ac260`, `0x7ac2f0`.
Native fixtures use their independently guarded host addresses.

`lifetimes.bin` begins with `<8Q32s>`: magic `0x31464c4941493544`, version 1,
header size 96, event size 96, armed QPC, armed thread, core epoch at arm,
reserved zero and the raw 32-byte session identity SHA-256. Arming occurs after
all journal hooks are installed and guarded, before capture admission.

Each event has a 16-byte `<4I>` frame: magic `0x314a4c53`, payload size 96,
low 32 bits of sequence and payload CRC-32. The `<12Q>` payload preserves full
sequence, kind, phase, invocation, parent, thread, QPC, receiver, allocation,
status, core epoch and hazards. Sequence begins at 1 and has no admissible gaps.
Kinds are holder resource-map ending (1), collection geometry ending (2), and
collection mutation (3). Phases are BEGIN (0) and END (1). Allocation identity
is receiver minus 16 for kind 1, minus 8 otherwise. Runtime addresses, source
allocation serials, geographic keys, QPC and file offsets remain distinct domains.

BEGIN invalidates old content continuity. END confirms the function body returned,
not that the caller subsequently freed the outer object. Mutation refuses old
backing-survival classification; it is not evidence of complete deallocation.
Exceptions, loss, malformed framing, unmatched intervals and ambiguous boundary
ties cannot establish continuity.

## Durability and interval qualification

`lifetimes-flush.jsonl` uses `sor-d5ai-lifetime-ack/1`. A row binds session identity,
record/byte count, CRC of the entire prefix including its header, coverage onset,
coverage watermark, loss/failure and a producer-safe marker. Bytes equal
`96 + 112 * records`. The core ACK/terminal separately carries matching lifetime
counters and watermark. Unacknowledged file tails are outside the admitted prefix.

A marker contains eight unsigned 64-bit fields: cursor, QPC, generation before,
generation after, active before, active after, loss and failed. Coverage advances
only with equal generations, zero active/loss/failure and cursor no greater than
the durably flushed prefix. A paused unpublished producer cannot establish a
quiescent watermark. A worker clock alone is insufficient.

Every completed admitted call increments generation twice and emits BEGIN/END.
With zero loss and no unlogged call, a quiescent marker therefore has generation
equal to cursor. The reader checks this invariant and the event-time cut: records
at or below the cursor cannot be later than the marker, and records above it
cannot precede it. Merely equal before/after generations are insufficient.

The first unlogged disabled-hook entry establishes a sticky cutoff before its
original body runs. No coverage marker may reach or cross that cutoff. Previously
completed evidence can remain eligible; later unsupported history cannot acquire
continuity through a final healthy-looking JSON file.

Raw2 geometry has a 456-byte header: the prior 328-byte fields plus start and end
markers, each eight Q words. It retains the old magic with version 2. Resource
records are `<II4Q>`: FormID, reserved zero, collection pointer, region count,
region capacity and region data pointer. Region records are `<24s4Q>`: raw header,
point count, point capacity, point data pointer and region address. Raw pointers
are diagnostic identity witnesses, never instructions for subsequent traversal.
Semantic normalization still compares represented fields/points, independent of
spare capacity and allocation address.

The reader requires onset before the baseline and coverage through the measured
completion and its end marker. The baseline graph binds every resource key and
represented region/point count to captured allocation shape. Null-empty content
continuity is separate from surviving allocated spare backing. Zero collections
cannot prove an external owner by vacuous equality. Complete, partial and ended
collection-content lifetimes remain separate from consumer exposure.

A normal completed collection-geometry ending establishes an irreversible fact
about that baseline content. A later mutation at the same numeric address cannot
erase that ending. The evaluator requires END sequence and QPC both strictly
before the later operation's BEGIN, applies the rule per typed collection, and
records subsequent address activity separately. It does not attribute a second
ending to the old allocation or infer the new contents or outer allocation's
free/rebirth. Holder-map ending alone cannot suppress mutation of an externally
surviving collection. Earlier, overlapping or tied mutation remains UNKNOWN.
An exceptional original ending cannot establish ENDED; a strictly later operation's
exception does not erase an already established ending. Malformed or lossy
history cannot produce a qualified full result. BEGIN status must be zero;
END status is zero for normal return or 16 for a recorded exception.

Aliased collection pointers must agree on allocation shape and represented
content. A zero-capacity/non-null backing pointer remains raw evidence but gives
UNKNOWN ownership, rather than becoming proof of no storage. Results separately
count surviving content-vector lifetimes, collections with represented regions
and collections with nested backing. If all backing ended and only null-empty
content lifetimes survive, the result says precisely that; it is not positive
partial physical geometry survival.

Construction-frame qualification examines complete paired intervals intersecting
Generated return through copied content, including an operation that began
earlier. Native synchronous mutations that completed strictly before Generated
return remain permitted. Relevant QPC ties at the measurement boundary refuse
qualification. An earlier decoder also refused every internal BEGIN/END tie.
The actual unpaced concurrent workload preserved 32 such pairs with zero loss.
Independent source review and receiver controls now accept equal samples only
for exact matching phase identities with strictly increasing journal sequence:
the hook emits BEGIN before calling the body and END after return or exception.
Decreasing times, mismatches and reordered phases remain invalid. Sequence numbers
from the core and lifetime journals are never compared to each other, and this
internal ordering proof does not relax ambiguity at a measurement boundary.

See the [native ending proof](d5ai-population-ending-proof.md),
[geometry schema](d5ai-geometry-schema.md) and
[active ledger](d5ai-investigation-ledger.md). Native hook/worker/reader, fault,
STOP, compatibility, performance and independent-review receipts are separate
premises of any readiness or prediction-freeze claim; this schema alone cannot
establish them.
