# D5L native boundary and completion register

2026-10-27. [Report](report.md), [source pins](sources.csv), [implementation](../../../research/resource-retained-population/README.md).
All `0x140...` addresses below are preferred static VAs for the freshly verified
EXE 1.16.244.0, base `0x140000000`, SHA-256
`7e9adb1414a8e1b325e5e1f097b9b17b78deb7eebeda37a333351a43a60f9d28`.
Subtract that preferred base for an RVA. The controller measures the actual
module base and adds the RVA; it never treats a static VA as a runtime address.
`native-full.tsv`, `native-owner-copy03/04.tsv` and `native-sites04.tsv` are local
read-only exports, with exact hashes in sources.csv. Existing analysis was not edited.

## Invocation and source identity

Provider entry is `0x14079f860`. Its working stack W is entry RSP minus `0x3c8`;
RBP is W+0x100. W+0x3d0 holds saved ProcGen, W+0x3d8 the original Int2 pointer,
W+0x38 the current source, W+0x100 the retained Grid. Runtime singleton at module
RVA `0x5fd9c30` leads to manager; manager+0x130 is current ProcGen and manager+0x120
leads to the source index whose +0x10 is the ordinary Grid. The reader verifies
source membership in that concrete retained Grid vector (+0x10 count, +0x14
capacity, +0x18 data), Grid/ProcGen vtables, saved/current ProcGen, query/descriptor
and repeated source/manager/query bytes. Normal provider stops also require
R13=ProcGen and RBP=W+0x100.

The invocation key is process identity, thread lifetime, W and runtime source
pointer, plus an encounter token. Nested frames have distinct W. Geographic key,
SFBK value, runtime pointer and observer lifetime token are different domains.
The selected source's first 0x70 bytes, manager first 0x200 bytes, original query
8 bytes and descriptor 0x2c bytes are retained. This is not the entire 0x1a0 source
or complete per-node file provenance. Chart-0 decoding reuses the owned [D5B method](../resource-combined-acquisition/report.md).

## Permanent observation sites

| Event | Preferred static VA | Operand/effect and exact single-step destination |
|---|---|---|
| Visited decision | `0x14079fca3` | TEST SIL,SIL; SIL is saved visited outcome, RDI=[source+0x68] identity; next `0x14079fca6`. |
| Source-map lookup | `0x14079fcd0` | CMP RAX,[R13+0x28]; capacity equality=miss; next `0x14079fcd4`. |
| Original query | `0x14079feaf` | CALL converter `0x14078d660`; R9 original query, R8 effective descriptor; single-step enters callee. |
| Ordinary mask | `0x14079b8ed` | MOV [RSP+0x30],AL; actual AL, no prediction or nibble trimming; next `0x14079b8f1`. |
| Region append result | `0x14079acf2` | MOV R12B,1; EAX is prior append result, RBX collection; next `0x14079acf5`. |
| Generation returned | `0x14079ff1d` | RIP-relative LEA; synchronous generation has returned; next `0x14079ff24`. |
| Completed ProcGen init | `0x14079d8b2` | MOV RAX,RDI; object RDI, empty map/type checked; next `0x14079d8b5`. |
| Protected reset fence | `0x14079de92` | MOV RAX,[RSI+0x28]; object RSI, after map clear under lock; next `0x14079de96`. |
| ProcGen destruction | `0x14079d910` | Entry, object RCX; next `0x14079d915`. |
| Related source-map erase | `0x140975030` | Entry PUSH RBX; receiver RCX=ProcGen+0x10, index RDX; next `0x140975032`. |
| Grid clear | `0x1409829b0` | Entry, Grid RCX; next `0x1409829b5`. |
| Completed source init | `0x140983140` | JMP `0x140983148`; source R14, Grid R12−0x10, definition R13. |
| Completed Grid init | `0x1409828d5` | MOV RAX,R15; Grid R15/type checked; next `0x1409828d8`. |
| Standalone source retirement | `0x140982b70` | Entry, source RCX, including absent-map branch; next `0x140982b75`. |

The mask stop's working generator RSP G recovers W=G+0x2e0. G+0x2d8 must equal
the relocated provider return `0x14079ff1d`; G+0x2f0 supplies the geographic input
pointer. At append stop, I=current RSP and W=I+0x560. I+0x208 must be
`0x14079c4fc`; I+0x278 one of `0x14079be25`, `0x14079c047`, `0x14079c11c`;
I+0x558 must return to `0x14079ff1d`. These are actual stack reads, not fixture
IDs. Resource u32 is I+0x230 (explicit native store at `0x14079a615`).

Descriptor is manager+0x1c0 for mode 3, otherwise +0xc8. Query-site R8/R9 must
match those actual pointers. Raw Windows x64 CONTEXT bytes independently check
RIP/RSP, relevant GPR operands and recovered-frame arithmetic. Source/type/stack
mismatch closes qualification; same geography alone cannot repair it.

## Owned maps and successful region witness

ProcGen source slots are +0x20, capacity +0x28; each slot is 24 bytes:
source pointer at +0, wrapper at +8, occupancy/link at +0x10 (empty `0xffffffff`).
The source pointer is distinct from the source+0x68 visited identity. Wrapper
resource slots use the same +0x20/+0x28 layout/stride, with u32 resource key +0,
collection pointer +8. Collection +8/+0xc/+0x10 are count/capacity/region data;
regions have stride 0x30. Region +0x18/+0x1c/+0x20 are point count/capacity/data;
points have stride 16. Nonzero valid reference states and bounds are checked.

Insertion stores at `0x14079fe14/18` precede synchronous generation. The reader
records the new owned wrapper at query, not merely the miss. At provider return,
ProcGen exclusive protection is still held until `0x14079ffa5`. It reads actual
source slots, resource slots, collection headers, region headers and ordered
points through that owner. The reducer checks raw slot values, collection extent,
reference state and `region.address = collection.data + index*0x30`.

Append CALL is `0x14079aced`; the stop immediately after it exposes its actual
index before unconditional R12B=1. Reject EAX=`0xffffffff`. Temporary region is
I+0x50. Destination must be collection.data+index*0x30 with index<count. A
successful witnessed region requires nonempty ordered points and byte equality
between temporary/destination meaningful header bytes 0..0x14, point count and
all 16-byte ordered points. Allocation pointers, capacity and padding are not
geometry. Final owner and later hit must contain that same resource/collection/
index and exact geometry; equal names or only equal aggregate hashes do not join.

False-success counterexamples are explicit. Append `0x1407ac2f0` can return −1
(the comparison at `0x1407ac33d` skips copying), yet the caller sets R12B=true.
Point-copy helper `0x1407ac0d0` can skip a failed individual append at
`0x1407ac212..215`, then return AL=1 at `0x1407ac234`. Outer return, visited
marking and nonempty partial output cannot certify an intended full population.
A directly witnessed successful region can still be qualified while other
observed append/exception failures remain attached as `population_partial`.
Unobserved attempted regions are not silently declared successful.

## Lifetimes, replacement and conservative loss

`0x140982d90` is an acquire/dedup route, not a birth. The new 0x1a0 allocation
at `0x140983001` initializes through the ordinary branch before SourceInit.
Grid destructor `0x140982930` calls clear `0x1409829b0`: sources are looked up
under current ProcGen protection, erased at `0x140982a36`, freed at
`0x140982af8`. Separately `0x140982b70` locks ProcGen+0x40, erases at
`0x140982bbc`, releases at `0x140982bc9`, frees source at `0x140982c32`.
The additional entry fence covers its absent-map branch and erase-to-free window.
These refine the bounded [D5C study](../resource-population-lifecycle/native.md); its frozen text is untouched.

Reset entry `0x14079ddf0` precedes exclusive locking and was rejected as an epoch
boundary. The chosen `0x14079de92` follows the clear call at `0x14079de8d`, with
protection held until `0x14079dec4`. No competing provider can populate between
the actual clear and this fence. Completed init verifies empty storage/type.

Reset/init/destroy increment observed ProcGen segments and invalidate pending
and retained joins. Destroyed ProcGen/Grid objects remain poisoned until their
completed init stop; reset cannot revive a destroyed object. GridClear poisons
Grid. Related erase and standalone SourceRetire poison source until SourceInit.
SourceInit is a birth fence even at the same address. A change of current manager
pointer clears all joins and advances the domain token. These are observer
segments, not engine epoch fields. All pre-barrier ancestry remains unknown.

A miss invalidates any previously retained entry even if a wrapper address is
reused. At a later hit the same actual wrapper, resource, collection, region
index and geometry are required. Changed contents are preserved as no matched
reuse; no predictor is fitted to them. Coverage gaps, incomplete reads, unknown
thread lifetimes, bad frames or sequence/site mismatches prevent subsequent
joins. Bounds are engineering safeguards: 4096 slots/regions/points and 1 MiB
read budget per stop, maximum 65536 bytes per read. Exceeding them produces an
incomplete acquisition, not proof of absent geometry or unsupported resources.

## Source provenance and export limits

The fresh fourteen-site export is checked against installed PE backing bytes,
including file offsets, instruction lengths and flow targets. The real fixture
executes matching instruction shapes; CALL/RIP-relative LEA carry their own
relocations. Complete native bodies and copy/owner exports support field meaning.
Initial exports with truncated bodies and an overly long Grid vtable walk are
superseded by complete bodies and corrected 0x48 Grid table bounds; adjacent
entries from the earlier overscan are not treated as Grid methods.

All analysis used existing saved state with `-readOnly -noanalysis`; commands,
stdout and source script versions remain local. Proprietary bodies, byte exports,
analysis database and executable stay outside authored delivery. No universal
writer coverage, mod integration safety, persistence semantics, arbitrary chart
support or retail debugger behavior is claimed.
