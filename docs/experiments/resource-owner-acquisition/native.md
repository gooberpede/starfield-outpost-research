# D4D native acquisition contract

2026-10-24, Australia/Sydney. All native locations below are preferred static
VAs for Starfield.exe 1.16.244.0, image base `0x140000000`, SHA-256
`7e9adb1414a8e1b325e5e1f097b9b17b78deb7eebeda37a333351a43a60f9d28`.
The controller measures the runtime module base and adds RVAs. Object, iterator
and stack offsets are byte offsets, never saved identifiers. [Source pins](sources.csv)
and the [D4C instruction ledger](../resource-owner-root/native.md) retain provenance.
Existing exports were read; no Ghidra project was changed or new export executed.

## Observed boundaries and operand lifetimes

Let E be the entry RSP of `0x14079b520` and F = E minus `0x2d8`. DR0 retains
the inherited Workshop updater entry; DR1 retains generation entry outside
consumer mode. DR2/DR3 rotate per thread as follows. Generation nesting has
separate thread-lifetime/invocation/parent tokens and a 64-frame integrity bound.

| Stop | Required operands and meaning | Next DR2 / DR3 |
|---|---|---|
| `0x14079b520` | Source RCX (`0x70` bytes), origin RDX (8), converted descriptor R8 (`0x18`), owner R9D. Entry return must be the provider continuation. Retain E before the prologue. | Component loop / cleanup |
| `0x1407bc470` | RSP = F minus `0x160`; RBX points to the iterator at map-frame `+0xa0`; R15 is the output map. The return at map-frame `+0x108` must be `0x1407bc374`, and F minus 8 must contain `0x14079b925`. RDI is not yet the current node. | Component loop / cleanup |
| `0x1407bc745` | Same map frame and map pointer, before final staging free. Copy final staging and map, including an empty range. The observer count is the number of witnessed loop visits, not an independently decoded store-wide count. | Map return / generation return |
| `0x14079b925` | RSP = F; output map must equal F plus `0x210`. Copy completed map and selected root at F plus `0x130`. | Candidate ready / generation return |
| `0x14079bd71` | RSP = F, immediately after rarity sort and before the loop count test. Copy candidate count/capacity at F plus `0x40`/`0x44` and pointer at F plus `0x50`. This is a 24-byte header, unlike the map's 16-byte arrays. | Ordinary CALL / generation return |
| `0x14079be20` | RSP = F; RDX is the next IRES, R8 the selected 560-byte DNAM, XMM3 the effective weight bits. Copy the full candidate pointer array, IRES prefix/type/rarity and associated-file provenance, selected root at F plus `0x58`, and current component at F plus `0xe0` (`0x6c` bytes). | Ordinary CALL / generation return |
| `0x14079ff1d` | RSP = E plus 8. Retire this invocation and restore its parent's observation schedule. Construction completion and complete candidate/CALL coverage are separate properties. | Parent schedule, or component loop / cleanup |

The [existing consumer contract](../resource-tungsten-acquisition/native.md) remains
the authority for updater, ACCEPT, REJECT and transfer frame/reference/BC checks.
Global consumer mode replaces generation slots and records an observation gap.
Incomplete generations are invalidated; no outer frame is borrowed after an
exception, unwind, reused stack or phase interruption. Queued traps from an old
phase may produce explicit LOSS. The controller retains the D4B monotonic terminal
intent and does not rearm dying threads after STOP.

## Ordered component and map representation

The native iterator carries page at `+0x18`, page ordinal at `+0x20` and upper
key words at `+0x28/+0x30`. Node address is page plus the uint16 displacement
at page `+0x12 + ordinal*4`. Copy the entire `0x8c`-byte node prefix before
interpreting its key at `+0x10/+0x18`, BIOM word at `+0x60`, root at `+0x70`
and six uint32 resource slots at `+0x74..+0x88`. Zero slots and duplicate words
remain present. Payload begins at node `+0x20`; the corresponding payload
root/slots are `+0x50` and `+0x54..+0x68`.

`d4c-range01` at `0x1405f7a8d–0x1405f7aec` constructs the first key as
`(uint64(owner) << 32) | runtime_registered_type | 0x10000`, with second-key
bounds zero through `0xffffffffffff`. The runtime type word at preferred VA
`0x1461dfa4c` is copied, not inferred from its static initializer. Each witnessed
node must match that owner/type key, remain within the captured upper bound,
and increase in unsigned lexicographic order. The creation routes supporting
conditional BIOM-key ancestry remain in D4C; a BIOM label is not a captured key.

`d4b-owner-map01` at `0x1407bc3f2–0x1407bc404` initializes staging once. Its
header at map-frame `+0x20` has uint32 count/capacity and a pointer at `+0x28`.
Each nonzero slot appends in field order at `0x1407bc480–0x1407bc666`, subject
to allocator refusal. Zero root preserves staging. A nonzero root finds or
creates an entry and exchanges the complete array at `0x1407bc669–0x1407bc6fa`.
Displaced contents become staging; this is neither deduplication nor union.
Final staging is discarded during cleanup, not distributed to other roots.

Map header `+0x18` is the bucket pointer, `+0x20` the uint64 capacity. Each
32-byte bucket has uint32 key at `+0`, array count/capacity at `+0x8/+0xc`,
pointer at `+0x10`, and occupancy/chain word at `+0x18`; `0xffffffff` marks
an empty bucket. These offsets are independently corroborated by selected-root
lookup `cont-01`, `0x14079bb7a–0x14079bc34`. Full headers and bucket bytes are
retained alongside decoded occupied entries. Bucket order is not visitation order.

At loop boundaries, raw before/after maps and staging are OBSERVED. The D4C
append/exchange interpretation is STATIC/RECONSTRUCTED and is checked against
the following snapshot. The comparator retains the first expected/observed
disagreement with its component index and both arrays. It does not delete a
contradiction to force conformance. Exact individual allocator outcomes remain
UNKNOWN without a stop at their return sites. An unexpected boundary can identify
the first disagreement without proving whether allocation, mutation or another
transition caused it. A final map alone never certifies traversal history.

Selected-root lookup resolves root first and map words in array order, rejects
unresolved/non-IRES records, then sorts by descending rarity without deduplication.
The ready-array and every CALL independently witness resulting pointer order.
Exact root-plus-map ID multiplicity and descending rarity are checked; unresolved
filtering/allocation is explicitly UNKNOWN and cannot satisfy positive STOP.
No occurrence quota, density fallback or spatial-exhaustion substitution is
supported in this inspected path. That bounded statement is not a universal
absence claim. Both Water operands remain ordinary-loop operands; these stops
do not reinterpret them as two veins or atmospheric/terrestrial populations.

## Identity, budgets and limits

Source bytes and the current `0x200`-byte manager are reread at every generation
stop. Manager coordinates derive chart/frame and geographic source anchor under
the existing D4A convention. The expected source is `0:27156:35988:0028be0d`,
owner `0x0005de4c`. The successful selector additionally requires a separately
qualified D4A-style Workshop `e07e10e02770599b` Tungsten ACCEPT and same-evaluation
transfer with equal retained source bytes. This establishes current source
correspondence plus Workshop binding. Historical generation/consumption epoch,
all-writer ownership and identical-byte ABA remain UNKNOWN. No current native
component word is thereby established to be persisted or authoritative after load.

Each external read is at most 65,536 bytes and each sample at most 1,048,576 read
bytes and one MiB of JSON. Arrays are bounded to 4096 elements, maps to 1024
power-of-two buckets, and nesting to 64. These are copy/integrity capacities;
exceeding one records incomplete evidence or LOSS, never a truncated success.
Headers, source/context bytes and buckets are reread where implemented; receipt
readback separately verifies persisted bytes. These checks do not prove semantics.
Both C: and D: retain the 40,000,000,000-byte caller-available free-space guard.
No event-count, healthy-run duration or operator-response cutoff is introduced.
