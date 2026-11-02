# D5AG terrain specialist primary-evidence findings

2026-11-02, Australia/Sydney. This is a bounded specialist contribution to
D5AG-Q1/Q2, not independent review or a question-level completion decision.
The original [brief](../../implementation-briefs/CODEX_BRIEF_SOR_RG2_D5AG_terrain_resource_consistency_lifecycle.md)
and root investigation ledger govern the assignment. All native addresses are
preferred static VAs for Starfield 1.16.244.0, image base `0x140000000`;
member offsets are bytes. Native payloads and disposable projects remain local.

## Source identity and request identity have different producers

The terrain graph stabilizes source metadata within a qualifying allocation.
It does not replace every eligible provider request with the source anchor.
These are primary instruction/data-flow findings, not inferred retail clocks.

| Producer and receiver | Consequential operands and ownership | Checked native evidence |
|---|---|---|
| Focus to service demand | `0x1407b2390` reads terrain focus `+0xd8/+0xdc`, floors to Int2, and suppresses another request for the service's unchanged cached focus cell `+0xec/+0xf0`. It derives a block-aligned region using effective settings before region registration. | Instructions `0x1407b2492..0x1407b260d`; original export02 in the source ledger. This limits locality; the region still contains multiple cells. |
| Cell to preparation | `0x140aed020` reads cell Int2 through cell `+0x58`, prepares content/context and supplies the cell endpoints. The geographic packed key is produced separately. | Original D5R export01, function `0x140aed020`; no source-anchor substitution at its Int2 ingress. |
| Demand to density work | `0x1407a1260` packs a DB/discriminator key through `0x1407c07b0`, but separately copies the original 32-bit Int2 into its registrar payload. | `0x1407a13b4..0x1407a13d0` versus `0x1407a12a8`. The key helper uses low coordinate words; that encoding is not authority to replace original operands. |
| Landscape to sources | `0x140785190` protects landscape setup, selects current mode descriptor, traverses base blocks, adds overlay blocks, finalizes ordinary/overlay Grids and MultiFiles state, then writes landscape `+0x60 = 1`. | `0x140785303`, `0x1407853d8..0x1407853f8`; D5AD export03. Source publication and complete geometry generation remain separate. |
| Base/overlay callbacks to source allocation | `0x1407862a0` and `0x140785490` derive positive interior dimensions after padding, anchor and shifted surface descriptor, then call the common allocator. Overlay construction also stores source `+0x178` from overlay metadata. | Calls `0x140786382` and `0x1407855dc`; D5AB specialist-export01. |
| Surface Grid construction to source allocation | `0x140849670` traverses surface descriptors, resolves content or default, obtains interior dimensions and calls the same allocator, then rebuilds its contributor index. | `0x140849bf2`; D5AB specialist-export01. This alternate writer is included rather than dismissed by its terrain name. |
| Source allocator to published source | Under Grid `+0x5c` protection, `0x140982d90` deduplicates existing allocations by anchor `+0x10/+0x14`. New sources retain a shared definition/path reference at `+0x08`, copied from definition `+0x38`, plus anchor, dimensions `+0x18/+0x1c`, padding/context `+0x20..+0x30`, and copied surface bytes `+0x38..+0x60`; token is stored at `+0x68`. | D5Z export02, `0x140982e21..0x140982e39`, `0x140983017..0x1409830c9`, `0x140983121..0x14098313c`. The shared reference increments allocation `+0x10`; it is not identified with the separately traced BGSTerrain File object, whose count is at `+0x08`. Dimensions are clamped to at least one. This is allocation metadata, not the generator's incoming Int2. |
| Shared surface transform to distinct clients | `0x14096f5c0` shifts a descriptor by the supplied Int2, crosses face/block boundaries and reads SFTR/SFPT content. `0x14078d7b0` packages a geographic content key from the shifted descriptor. Source and demand clients supply different operands. | Original D5S export55 and D5T function export. Sharing the transform does not prove equal input or output coordinates. |

## TerrainDB is a real scheduling and context-lifetime dependency

Cold height work is not simply outside the resource investigation. It can
retain the manager context and execute work from shared worker infrastructure.
The material distinction is between that scheduling/ownership effect and the
numeric fields consumed by resource contour construction.

`0x140993110` creates or reuses a TerrainDB entry keyed by block coordinates,
class/level and file identity from file `+0x50`. A missing block table at file
`+0x230` selects PageStitch. Its constructor retains the file reference and a
manager reader; the registrar invokes file virtual `+0x40` to gather block
handles/dependencies and commits the node. The qualifying nonnull-table branch
selects PageTransform and uses `0x140852100` to enumerate dependent blocks.
That helper calls `0x140993110` recursively with the same file receiver and
derived height-block coordinates. The streamed compressed-block branch has
separate open/error/release handling. Entry existence is not completion.

Both constructors select the current TLS pool at worker `+0x88`, falling back
to `[0x1461fabe8]+0x140`, with mode 2. They save manager `+0xb0` and reader-held
byte `+0xb8`. PageStitch destructor `0x1409921f0` and PageTransform destructor
`0x140995d20` release buffers, file references and entry handles before
decrementing manager reader count `+0x28` and conditionally waking a waiter.
Thus their lifetime can delay an exclusive context transition. This does not
transfer an individual-source reference to detached density work.

PageTransform's `0x140852460` maps the block/LOD sample window and calls
`0x140851e10` for each sample. For levels below four that reader obtains ready
TerrainDB payload `+0x20` and reads two 16-bit arrays separated by `0x8000`
bytes; higher levels read file-owned arrays. The fallback acquisition
`0x140993e70` calls `0x140993110`, then loops while pending. Inside that loop,
`0x1428d4540(false,false)` can call `0x1428d2e80`, which calls the existing
worker claim helper `0x1428d3960` and executes a claimed callback `+0x08`.
If no work is done, the loop progresses through `Sleep(0)` and `Sleep(1)`.

This is an explicit compiled opportunity for shared work to execute while
height acquisition remains pending. It rejects a whole-terrain-pass barrier
inference from a synchronous-looking height caller. It does not measure how
often a resource callback is available there, establish a geographic winner,
or reconstruct B2's missing worker/lock timestamps.

There is also a conditional lifetime consequence. The retained reader is on
the same global manager used by ordinary movement. ShiftToTask
`0x14078ce00` admits its `0x14078c190/0x14078c290` shift work only after
exclusive acquisition: a zero-state compare-exchange or existing same-thread
exclusive ownership. A reader held by the outer terrain node therefore
excludes another thread's manager-exclusive movement shift while a nested
resource callback executes. Existing same-thread exclusive ownership and
recursive admission must remain separate predicates. This is ambient context
protection, not an individual-source lease transferred to every density job.
It ends when the outer node releases the reader. It supplies neither a
canonical original query nor cross-episode geometry retention, and B2 does
not establish that either target invocation ran in this nested context.

### Concrete File callbacks and the numeric boundary

The actual polymorphic receiver was followed beyond the tempting Grid/File
name match. `0x140976950` is the GridFile base constructor, called by Grid
finalizer `0x140983880` and constructors `0x14097c380/0x1409816d0`.
Those callers install final GridFillFile, GridEdgeFile, GridCornerFile and
GridCornerEdgeXFile tables. Independent installed-PE table reads supplied by
the root bind their inherited `+0x38/+0x40` methods to
`0x140978760/0x1409783c0`, and their concrete block/dependency callbacks to
the locations below. This is a positive final-table join; MultiFiles Grid
slots are not substituted for File slots.

| Concrete File | Dependency callback `+0x88` | Numeric callback `+0x90` | Checked behavior |
|---|---|---|---|
| GridFillFile, table `0x144b67c70` | `0x1402d4ce0`, returns one | `0x140979060` | Resolves source-grid cells and adjoining contributors, then applies ROI payload operations. |
| GridEdgeFile, table `0x144b67ba8` | `0x14097b6d0` | `0x14097b7f0` | Enumerates qualifying child File references and combines their ROI payloads. |
| GridCornerFile, table `0x144b67ae8` | `0x14097d080` | `0x14097d190` | Enumerates edge constituents and combines corner ROI payloads. |
| GridCornerEdgeXFile, table `0x144b67a20` | `0x14097b6d0` | `0x14097b7f0` | Uses the shared edge implementations with its constructor's distinct constituents. |

GridFile `0x140978280` protects an individual block's preparation bit with
compare-exchange, calls its actual `+0x90`, then publishes its level bit.
While another preparation owns the block it also calls the work-helping
`0x1428d4540` loop. This serializes that terrain block's preparation, not
the resource source-pointer map or all requests touching a resource source.

The final material ROI helpers were inspected directly. `0x14098ed90`
selects the caller's ROI storage by operation class, then rewrites packed
16-bit terrain payloads through five 3-bit channels. For class one its
storage is the second TerrainDB array at payload `+0x8000`.
`0x14098f380` combines contributor channels into the same selected storage,
with geographic-indexed perturbation under its effective setting predicates.
The geographic helper's return feeds a table index on this path; no join
to the resource provider's original Int2 or source-map authority is inferred.
The remaining channel interpolation/decoding is not expanded into unrelated
terrain research: the checked writes target the supplied ROI payloads, and
the ordinary resource contour receiver consumes different operands. This is
an operand/write-domain boundary, not a universal assertion that every
terrain callback has no indirect gameplay effect.

## PCM/content preparation has a different mutable map

Fresh `0x1407a1f80` follows the material subpasses after restored PCM placement
preparation. It sets a query origin from original Int2 multiplied by 100,
uses the subpass's preparation record, obtains candidate placements through
`0x14079ee50`, resolves their definitions and tests them through
`0x14079e220`. Accepted definition/position/ID records are appended through
`0x1407ac3d0`, which copies `0x60` bytes into its output blocks. For subpasses
below three it calls `0x14079ea40`. These numeric factors describe this native
coordinate contract; they do not establish the missing physical landing-zone
tile size.

The inner map relationship is concrete. `0x14079e060` looks up or creates a
content-cell collection in receiver `+0xf0`, keyed by geographic content key
and a separate discriminator. `0x14079e6d0` obtains a radius-keyed map within
that collection under its own lock. Its new map has width 100, 10,000 bytes,
initial fill `0xff`. `0x1407ad160` writes zero at selected local sample
indices in these maps. `0x1407ac4d0` and `0x14079e3b0` read the radius maps
under content-cell reader protection and can clear the availability boolean
when a qualifying sample is below its effective threshold.

`0x14079ee50` reads prepared byte-density arrays with bilinear weights and
the fixed 64 by 64 threshold table at `0x144b3f430` to select candidate
definition/coordinate records. `0x14079ebe0` supplies its geographic phase
through the current surface transform, with a separate no-surface fallback.
These arrays, map locks and outputs differ from ProcGen's source-pointer
population map, visited tokens and retained region/point collections.

The joined operand boundary supports a scoped negative: this preparation
filter does not canonicalize the resource provider's original request or
serve as its source-map lock. Its completion can affect downstream readiness;
the resource generator's ordinary numeric contour route receives the source,
transformed original query/raster sample, definitions, seed and settings rather
than these mutable byte maps. This does not assert that preparation or restored
PCM state is irrelevant to gameplay.

## Method and remaining coverage

The specialist used read-only existing exports and eight fresh disposable
project exports. [The exporter](../../../research/resource-retained-population/d5ag_export.py)
adapts the maintainer-owned D5AF method under SOR-P-0002. Each invocation
authenticates the original 15-file core roster, copies only those files to a
new `D:/tools/sor-d5ag-terrain-specialistNN` directory, opens only that copy
with `-readOnly -noanalysis`, and authenticates original/copy core hashes
afterward. No original project was opened by this specialist. No game,
debugger, save, native fixture, network, deployment, staging or publication
operation ran. Raw logs/projects remain local; no cleanup ran.

The [source locator ledger](d5ag-terrain-sources.csv) provides exact primary
paths, hashes and function ranges. Historical interpretation documents guided
target selection; the findings above were checked against primary native
instructions/decompilation. The specialist is not its own independent reviewer.
Root integration must retain Q1/Q2 and parent D5R at their actual question-level
status and challenge any remaining material route before declaring completion.

## Active branch checkpoints

These checkpoints accompany root-ledger updates sent during investigation.
They distinguish actually inspected source paths from provisional bindings.

| Checkpoint | Path checked and result | Disposition and concrete continuation |
|---|---|---|
| T1, initial primary pass | Focus, original Int2 capture, source constructor and all three recorded source-allocation callers were reread. DB keys and source anchors remain distinct from provider operands. | Resolved at these boundaries; joined to the root's provider/generator map. |
| T2, cold TerrainDB challenge | Fresh exports 01/02 followed PageStitch/PageTransform constructors, workers, dependencies, sample reader and destructors. Their manager-reader lifetime and current-TLS/shared-pool selection are concrete. | Resolved ownership effect; physical file virtual callbacks still required qualification. |
| T3, wait continuation | Fresh export03 established synchronous block fallback `0x140993e70`; existing `0x1428d4540 → 0x1428d2e80 → 0x1428d3960` executes available callbacks while waiting. | Resolved compiled work-helping opportunity; no retail frequency or B2 historical queue state assigned. |
| T4, preparation inner maps | Fresh `0x1407a1f80`, `0x1407ac4d0`, `0x1407ad160`, `0x14079ee50`, plus original/fresh content-map readers identify separate mutable preparation maps and their reads/writes. | Resolved numeric/map boundary; does not substitute for full resource-generator coverage. |
| T5, rejected virtual binding | Base File and MasterFile table `+0x38` bind to a no-op and `+0x40` to return-one. MultiFiles table `0x144b3e0b8` is a Grid interface: `+0x38` is `0x1407823d0`, an erase/release by file key; `+0x88/+0x90` are dimension getters. | The tempting PageStitch-to-MultiFiles-slot binding is rejected. A Grid interface pointer cannot be substituted for the actual File receiver. |
| T6, wrong target retained | Export04 target `0x140976940` was a dimension getter, not the constructor containing base File-constructor call `0x140976976`. | Failed target selection preserved. Export05 correctly targets the containing constructor `0x140976950`; its caller chain is the next concrete route. |
| T7, abstract receiver challenge | Abstract terrain File table `0x144b67d48` has real `+0x38/+0x40` loops, which call `+0x90/+0x88`; those latter slots are purecall in that table. Base construction alone therefore does not bind a concrete final subclass. | Resolved constructor chain in export06: containing functions `0x140983880`, `0x14097c380` and `0x1409816d0` install final GridFillFile, GridEdgeFile, GridCornerFile and GridCornerEdgeXFile tables. |
| T8, concrete callbacks | Root's independent installed-PE table reads bind the final File callbacks, keeping them distinct from the MultiFiles Grid interface. Export07 targets fill `0x140979060`, edge `0x14097b6d0/0x14097b7f0` and corner `0x14097d080/0x14097d190`. | Resolved at the material dependency/ROI boundary above. Concrete callbacks enumerate constituents and operate terrain ROI payloads; no source-anchor substitution follows. |
| T9, final ROI boundary | Export08 follows `0x14098ed90/0x14098f380` to supplied terrain storage and packed-channel writes. Geographic perturbation uses a returned table index. | Resolved scoped numeric distinction. Further unrelated interpolation detail is not necessary to distinguish these write domains from resource contour inputs; no whole-engine side-effect absence is claimed. |
| T10, conditional ambient reader | Fresh node ownership/destructors joined to original `0x14078ce00` exclusive shift admission. | Established conditional other-thread movement exclusion during a nested callback, with same-thread exclusive recursion and actual callback choice unobserved. Root must incorporate this conditional lifecycle mechanism, not claim a universal source lease. |

Editorial screen found one `JOINED_PROSE` suspect in the exporter's literal
local path on line 5. It is a valid disposable-project path, not joined prose;
no executable change was needed. The original exporter bytes were restored
after a temporary docstring-only wording diagnostic, preserving the method
hash recorded by the completed export receipts. The specialist's authored
findings were manually read; final independent review remains the root's gate.
