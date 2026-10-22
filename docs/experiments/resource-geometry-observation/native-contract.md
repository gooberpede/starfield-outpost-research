# Native observation and replay contract — design revision 1

[Answer and authority](report.md). Source basis: [RG1 native map](../resource-geometry/native.md),
[region lifecycle](../native-availability-map/region-lifecycle.md),
[ownership](../spatial-equivalence-feasibility/geometry-lifetime/ownership.md),
[exact per-use operand map](../spatial-equivalence-feasibility/geometry-lifetime/operands.md),
[D1 gate](../disappearing-deposits/native.md). No new native export or layout is asserted.

Pinned retail EXE SHA256 `7e9adb1414a8e1b325e5e1f097b9b17b78deb7eebeda37a333351a43a60f9d28`,
1.16.244.0, preferred image base `0x140000000`. All full addresses in this
document are preferred **static VAs**; RVA subtracts that base. Future runtime
VA = measured module base + RVA after identity/instruction validation, never a
saved token. Hex object offsets are relative to the named owner. Analyst aliases
are semantic labels, not changes to Ghidra symbols or supported integration APIs.

| Semantic boundary / locator | Actual static dataflow and proposed observation |
|---|---|
| Area refresh `FUN_1421e07d0` (RVA `0x021e07d0`) | Reference/frame/displacement guard; query descriptor and radius/upper locals; `1421e09d4..1421e0a77` manager→+0x130, shared ProcGen+0x40, occupied source slots. Callback callsite `1421e0a46`; no direct provider call mapped here. Capture guard outcome too: no callback can mean retained lists. |
| Region callback `FUN_1421e0f50` | Closure/query, source slot value, resource-map ordinal, resolved IRES and collection lead to current 0x30-byte region. At `1421e1060` RBX is current region. Normal callback return EAX=1 at `1421e18f2` is not region ACCEPT. |
| Native region decision | `1421e1119..1140` XY broadphase; count1 acceptance/count0 rejection at `1421e1146..1154`; multi-point strip/helper branches. REJECT edge `1421e174e` before RBX advance; ACCEPT `1421e1772` before RBX replacement. Record exact edge and active region ancestry, not function return alone. |
| Point alternative `FUN_14079df70 → 1407affb0 → 14079b020` | ProcGen+0x40 shared lookup of resource collections; bounded positive-width disks/max-width segment volumes. `140c5c550` condition supplies reference XYZ and keyword result. Point classifier differs from area callback; natural execution trigger for these named extractors is not established. Do not invoke it experimentally under C1. |
| Selected extractor gate `FUN_1421f68f0` | Resource/category/default/property resolution; `1421f6b3a..6b5c` selected collection pointer intersection. PlaceAnywhere bypass, SkipResourceVeinCheck biome list, HarvesterAtmosphere atmosphere list, otherwise spatial list. This is a resource gate, not all collision/territory/footprint checks. Exact full-placement decision boundary remains a named gap. |
| Source provider `FUN_14079f860` | Current source index/selection, source+0x68 visited key, source-pointer cache; exclusive lock at `14079fcb3`, insertion `14079fde2..fe27`, synchronous producer setup/call `14079fed3..ff18`, visited append `14079ff1d..ff60`, release `14079ff99..ffa5`. Source insertion/visited do not certify success. |
| Generation `14079b520 → 14079c470 → 14079a330` | Component-selected/current/alternate RSGD, BIOM/map prerequisites, resource rarity order, outer X/inner Y cells; generator CALL `14079c4f7`. Capture effective operands and actual prior different-resource geometry, not an assumed family from BIOM RNAM. |
| Source/key ancestry | `140985870` bounded index and source enumeration; `140982d90` source fields; `14078d7b0/14096f5c0` packed key; `14096e060/140970d50` surface selection CRC. Manager owner writer `14078a144` and lineage in [seed-lineage](../resource-geometry-mature-context/seed-lineage.md). |
| Population ownership / reset | ProcGen source map+0x10, slots+0x20/capacity+0x28; slot+8 source wrapper; wrapper resource map+0x10; resource slot+8 collection; collection count+8/capacity+0xc/data+0x10. Region bound XYZ+0/+4/+8, radius+0xc; point count+0x18/capacity+0x1c/data+0x20; points 16-byte XYZ/width. Reset `14079ddf0`; destruction `14079d910`, manager cleanup `140788d4f..d66` lacks a locally demonstrated owner fence. |

The callback is the preferred actual spatial consumer because it binds region,
query and result while naturally consuming cached geometry under the mapped
lock. The extractor gate is a linked secondary observation when the scientific
claim concerns extractor admission. UI folding `141578500` and raster
`1407a0820` / aggregate `14079ee50` are separate products. The colored-preview
drawing consumer remains unjoined; never label an area verdict a pixel oracle.

## Minimal schema `sor-rg2-coherent-evaluation/1` (not implemented)

Every row carries read status: OBSERVED, UNOBSERVED, NOT_EVALUATED or INVALID.
Null/unobserved differs from an observed empty population. Raw native arrays
stay local. Observer tokens below are proposed side records, not fields claimed
to exist in the engine. A field without qualified acquisition blocks its claim.

| Group | Required values, type/domain/units and time semantics |
|---|---|
| Session | Schema, EXE/plugin/load-order/settings/evaluator hashes, measured module base u64, instrumentation revision and guards, monotonic clock basis, MXCSR and supported numeric policy; session token never reused |
| Evaluation | Thread ID plus thread-lifetime token, thread-local sequence u64, nesting/parent token, updater/callback/gate tokens, BEGIN/END/LOSS suffix and durable flush status; wall time diagnostic only |
| Case identity | Original/protected save SHA256/display fields, plugin-qualified body/base/IRES; Workshop identifier bytes and saved beacon/parent/extractor tokens; independently resolved runtime reference/FormID/handle and parent/Workshop edges. Runtime u32 FormIDs require load-map resolution; handles and pointers are distinct. World/cell/actor/Workshop epochs UNKNOWN until actually witnessed |
| Frame/query | Raw beacon/extractor XYZ f32 bits, descriptor/index u32/domain u64, saved 0b/2b chart/anchor separately, translation operands and actual reduced queries; native units. Query point and footprint descriptor distinct. Actual radius and absolute upper f32 from descriptor+0x360/+0x364 via updater; nominal radius150 is only a frozen prediction parameter |
| Selected context | Manager/source pointer u64 with lifetime token; owner+0x80 u32, manager mode/descriptors, source selection index, source+0x68 key and source anchor/dimensions/padding; SFBK/SFPT/BIOM/RSGD/IRES identities and effective definition hashes; valid source windows and orientation. Selected source index is not a FormID |
| Generator provenance (conditional second observation) | Packed cell u64, CRC u32, resource/cell/source order and accepted/rejected attempts; effective DNAM binary32 words, masks/chance/weights, atmosphere/shared-family selection, surface seed/settings, component choice, prior different-resource population digest plus complete relevant inputs. Per-call MT seed/schedule or exact prestate when nonstandard; no invented history from output paths |
| Consumed population | Source/resource slot keys and ordinals, collection count/capacity, complete ordered region bounds and ordered XYZ/width points including outside-footprint starts, native region ordinal and IRES; content digest plus generation/population epoch join evidence. Generated output digest recorded separately |
| Uses and outcomes | Actual Qb broadphase XYZ, Qc containment XY per strip, Qv XY/radius/absolute upper per executed vertex helper, Qe XYZ/radius per edge path; original bound/count/radius bits, branch and region terminal. Resource set, gate selector/properties/produced IDs and true/false result joined through the exact operation-list epoch; negative candidates and short-circuit skips explicit |

Generator origin is `100*(source local anchor-padding)`; dimensions raw−2padding.
Native key adds that origin to integer cell **without division by100** before
geographic transformation. CRC folds LE64 packed cell then LE32 owner, initial
zero/no final XOR; no IRES fold. MT is reset per generator call. Retain effective
rarity order including ties, special/everywhere branches and prior competing
resources. RSCS, surface seed and owner suffix are different inputs. Actual
frame conversion is ordered binary32 arithmetic; do not use rounded screen
coordinates or decimal display to choose keys.

## Coherence admission and size

One logical evaluation requires valid native owner/alias protection throughout
copy and uses, complete invocation ancestry and one terminal per visited region.
Use per-thread nested stacks and helper return-site ancestry. Unloaded references,
unwind, missing/duplicate terminal, sequence loss, count/pointer overflow,
unqualified pointer reuse or a producer on another uncorrelated thread makes
the affected group INCOMPLETE. Preserve native outcome separately if witnessed.
Sequential reads across frames or equal headers/digests do not establish an
immutable interval or reject ABA.

The shared lock excludes mapped producer/reset mutation during consumption;
it does not prove complete owner lifetime, all aliases, successful construction,
or cross-operation epoch equality. No native monotonic generation counter has
been established. Side epochs require witnessed owner birth/reset/destruction,
population insert/replace and readiness transitions, with no observation gap;
otherwise generator→consumer attribution remains UNKNOWN. Do not label a
pointer plus wall time an epoch.

For the frozen single-query area evaluator, used Qc/Qv XY and Qe XYZ must agree
bitwise with corresponding Qb components and every used radius/upper must match
the supplied scalar. Capture each actual use or prove its stability. Different
uses yield valuable dataflow evidence but no single-query evaluator mismatch.
Full paths are required even for tails skipped by early acceptance if claiming
generation identity; record the extra read/interference cost.

For S source slots, J resource slots, R regions and P total points, a deep copy
needs at least `24*S + 24*J + 48*R + 16*P` bytes plus identity/use/transport records;
capacity traversal costs depend on actual hash capacities, not only occupancy.
Native u32 point counts permit about64GiB per maximal vector and supply no
practical safe latency bound. No retail maxima/cold-page measurements exist.
Before live approval measure/qualify complete source scope, capacities, checked
arithmetic, owned buffer budgets and copy/flush costs under the natural lock.
Overflow/refusal is LOSS, never native absence. Do not impose arbitrary healthy
scientific time/event quotas or read the whole manager as a substitute.
