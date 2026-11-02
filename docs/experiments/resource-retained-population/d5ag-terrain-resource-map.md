# D5AG terrain-to-resource dependency map

2026-11-02. Primary verification and branch checkpoints are recorded in the
[ledger](d5ag-investigation-ledger.md) and [specialist findings](d5ag-terrain-findings.md).
Question dispositions are separate in [the review](d5ag-review.md).
All native VAs below are preferred static VAs for Starfield
1.16.244.0, image base `0x140000000`; offsets are object-relative bytes.

| Producer → receiver | Consequential operand/owner | Ordering or authority | Evidence and GC |
|---|---|---|---|
| Focus setters `0x14099f230/280` → service `0x1407b2390` | Focus-derived Int2 and aligned geographic request rectangle | Restricts locality; does not select a canonical query for a source. | [D5W ingress](d5w-normal-path-model.md#ordinary-initialization-and-ingress); GC-07/08. |
| Exterior cell preparation `0x140bbb170/0x140afb220` → `0x140aed020` | Cell original Int2 `+0x58`, passed as both region endpoints | Placement/content predecessor; independent demand can compete with focus prewarm. | D5W cell route; GC-06/08. |
| Bounded LOD `0x141429880/0x1403e0080` → grouped-cell and neighborhood acquisition | LOD current/fallback rectangle, class bits and 3×3 cell neighborhood | Local dependencies before dependent continuation; no source-anchor election shown. | D5W bounded LOD chain; GC-08/09/10. |
| `0x1403625e0 → 0x1407b4bb0` → layer/density registration | Coordinate keys, original request and four density neighbors | Key reuse deduplicates work; original coordinate remains a distinct provider operand. | [D5S](d5s-query-winner-model.md); GC-08/11. |
| Landscape `0x1407847b0/0x140785190` → Grid/source constructor `0x140982d90` | Source identity, anchor/extent, BIOM/context and token `+0x68` | Definition-derived source publication precedes selection; source index is not generated geometry. | [D5AD inputs](d5ad-input-provenance.md); GC-02/11/12. |
| Layer `0x1407b5160` / density `0x1407a1940` → provider `0x14079f860` | Original request plus actual selected raw source, retained Grid | Layer holds manager reader; detached density has the qualified lifetime gap. | [D5V ownership](d5v-lifecycle-consumer-map.md#construction-and-ownership); GC-11/12/27. |
| Descriptor conversion at `0x14079fea1..0x14079febe` → generator `0x14079b520` | Original Int2 converted through current geographic frame | Request-specific; source origin and seed-cell keys remain separate. | [D5W arbitration](d5w-normal-path-model.md#arbitration-original-query-authority-and-retention); GC-15/16. |
| PNDT/CTPerBiomeData → resource relationship dictionary | Owner/component, resource order, root/ordinary/Special/Everywhere slots | Startup postlink and component initialization; loaded effective values matter. | D5AD input map, D4E provenance; GC-02/05/17. |
| BiomeMapDB `0x140478a30` → sampler `0x142339340` | Remapped face BIOM and numeric low-nibble raster | Deferred load can claim/wait/fallback; entry presence alone is insufficient. | D5AD inputs; GC-02/16. |
| PCM type-7 restore → content and placement preparation | Saved seed/content/placements, PNDT/cell operands | Real preparation dependency; not serialized ProcGen resource arrays. | [D5AD save matrix](d5ad-save-state-matrix.md); GC-05/08/31. |
| Protected ProcGen map → synchronous generation and visited store | Full source-pointer key versus separate source token | Exclusive first miss chooses holder; visited bypass and map hit differ. | D5V/D5AF; GC-13..19/26. |
| Grid retirement / broad reset → population lifetime | Map erase alone versus map plus visited clear | Retention can stabilize an episode; reconstruction needs new effective inputs. | D5V lifecycle; GC-27..31. |

## Primary joins and attractive negative controls

[The terrain source ledger](d5ag-terrain-sources.csv) pins exact function ranges
and file hashes independently of the older narrative reports. Source allocation
`0x140982d90` compares anchors under the Grid lock, copies anchor/dimensions,
surface context and a shared definition/path reference, derives its token and
publishes the allocation. The path reference is distinct from a cached concrete
terrain File instance. Base, overlay and surface-Grid producers all call that
allocator with their derived source metadata.

By contrast, density registration `0x1407a1260` copies original Int2 at
`0x1407a13b4..0x1407a13d0`, separately from packed DB key production. Focus
service `0x1407b2390` floors focus and restricts an aligned rectangle; cached
focus suppresses repeated demand but does not collapse all cells to a source
anchor. Cell preparation and bounded LOD introduce their own actual locality
demands. The shared descriptor shift helper has distinct source, key and request
clients; common code does not prove common operands.

The target source's source-cell seed keys and the incoming geographic raster
query are therefore different inputs. Complete native mask-0/mask-3 populations
provide an adverse control against treating source publication/deduplication as
full resource-geometry authority. [Geometry controls](d5ag-geometry-controls.md)
state the fixed frame, definitions, extra-pass qualification and represented
output contract.

| Further effective operand | Producer / exact native receiver | Authority and scope |
|---|---|---|
| Resource-selection seed | PNDT RSCS loader `0x140770114..0x140770122` writes PNDT `+0x50`; initializer `0x140779760` reads it at `0x1407797f0`, or component fallback `+0x48` when zero. | Builds resource slots from effective BIOM/RSGD/IRES/atmosphere state; distinct from later vein RNG. D5AD-IN046/SV73 and the input-provenance map. |
| Surface hierarchy seed/context | Existing PNDT SFTR via `0x14096b8e0`, or missing-tree generation `0x14096e060`, CRC call `0x14096e0a4..0x14096e0c3`. | Body/system/effective surface seed select hierarchy/orientation when generated; existing-tree reuse bypasses regeneration. D5AD-IN026/SV74–75. |
| Per-cell contour seed and working RNG | `0x14079a330`, especially `0x14079a3c4..0x14079a555`, obtains packed cell key through `0x14078d7b0`, folds eight little-endian key bytes and manager-owner u32 through CRC, then initializes working MT. | Source-origin plus candidate cell supplies the key coordinate. Original raster-query coordinate and persisted PCM seed are separate. Authenticated D5AD-SV27. |
| Effective generation parameters | Typed IRES/RSGD loader/postlink, component storage reader and effective GMST payloads feed `0x14079b520` and ordered per-cell generation. | File defaults, executable defaults and loaded overrides are not interchangeable. D5AD's EXE Exotic `0.01` versus main ESM `0.05` is a retained independent counterexample. |

Saved type-3 world/context reconstruction and type-7 PCM restoration are joined
in [the lifecycle model](d5ag-lifecycle-consistency.md); neither a restored world
token nor a calendar scalar is relabelled a contour seed. Physical height and
packed terrain channel writes have their own receiver/storage domains below.

## Preparation, terrain work and conditional protection

The PCM connection is traced through actual output records, not inferred from
the manager name. `0x14079da80` copies accepted restored placement data;
`0x1407b5bd0` executes four `0x1407a1f80` preparation subpasses. Those obtain
definition/coordinate candidates from `0x14079ee50`, filter them through
`0x14079e220 → 0x1407ac4d0`, append 96-byte records, and update radius-keyed
content-cell byte maps through `0x14079ea40 → 0x1407ad160`. Newly allocated maps
are 100 by 100 bytes filled with `0xff`; selected cells can be zeroed. These
maps and their locks constrain content preparation. They are not ProcGen's
source-pointer map, visited array, BiomeMapDB raster or retained resource points.
The ordinary contour generator's mapped operand list does not receive these
arrays. Preparation still matters to downstream readiness and scheduling.

Height acquisition follows TerrainDB `0x140993110`, PageStitch/PageTransform
tasks, dependent blocks and actual entry publication. Constructors retain the
file receiver and the current global manager reader; destructors release the
reader only after file/buffer/entry cleanup. Pending sample acquisition
`0x140993e70` calls `0x1428d4540 → 0x1428d2e80 → 0x1428d3960`, permitting
another queued callback to execute before height completion. Thus a synchronous
height caller is not a universal terrain-before-resource execution barrier.

This creates a useful conditional lifetime rule. A resource callback actually
executed inside that cooperative wait can run while the outer terrain reader
still protects the same manager. `ShiftToTask 0x14078ce00` requires exclusive
admission; another thread cannot take that ordinary shift while the reader
remains. Same-thread pre-existing exclusive ownership/recursion needs separate
qualification. The reader is not an individual-source lease, does not outlive
its terrain node and does not choose the original resource query or survive a
later broad reset. No B2 field identifies this nested execution context.

Concrete terrain file callbacks require their final subclass, not a Grid
interface or abstract table. Direct PE table reads are retained as
`.local-work/d5ag/vtables01.json` through `vtables04.json`, cross-checked with
native constructors. The specialist findings preserve the rejected base-stub
and MultiFiles-interface shortcuts and the completed concrete callback paths.

The physical terrain height/page decoder is not presumed irrelevant merely
because it belongs to TerrainDB. Its positive file/readiness and shared-worker
edges are in scope; a numeric geometry input or source/request side effect must
be established before treating height values as resource-generation operands.
The missing physical landing-zone tile size is not inferred from Grid settings.
Source-footprint overlap permits competing requests; physical deposit overlap is
deferred by the brief and is not investigated.
