# SOR-EV-0028 — Static dependency ledger

[Continuation](../activated-overlay-static-exhaustion.md). The tables below retain
the original expanding graph and superseded checkpoints. **The final disposition
table at the end is authoritative for current status.** All native addresses
are static VAs, pinned 1.16.244.0/base 140000000; RVA=VA−base. Raw native evidence
LOCAL-ONLY; authored interpretations REVIEW-REQUIRED.

| Lead | Question / typed inputs→outputs | Starting dependencies | Competing predictions | Evidence / disposition |
|---|---|---|---|---|
| A01 | Saved initial REFR XYZ/frame-byte/parent→loaded frame XYZ |141856d10 saver; 14181aa30/14181af40; initial loader branches; 140ada3a0 |0x20 relative-overlay versus absolute/other frame; negative-X0x2b should select distinct handling | Seed; trace both save/load callers and exact serialized identities. |
| A02 | Saved site/world/body→activated edge construction |1407986d0→140ad1660→140ad47e0/140ad4a00; 141881660 registration | Rebuilt from site/definition versus persisted component payload | Seed; inspect callers, factory indirect dispatch and serialization alternatives. |
| A03 | World/cell/valid flags→selected effective translation |140ad30a0/140ada3a0; 140ad9810/140ad4fa0/140ad11c0 | Selection depends on durable identity versus transient active/loading context | Seed; recover key construction and update/invalidity paths. |
| A04 | Rebase trigger/terrain displacement→edges and reference shifts |140797dc0→140ad9cd0→140797e90 | Frame-only gauge cancellation versus geographical change | Seed; trace trigger, producers of+1ec/+1f0 and consumers of applied shift. |
| B01 | Local XYZ→pair plus residual XYZ |14077fc20; 14078d1f0/14078d660 | Fraction retained for true geometry versus only local cell traversal | Seed; all relevant callers and output consumers. |
| B02 | Reference/world/cache→planet body position |140910690; 140ad3b20;ExtraData0x81 | Cached pair overrides versus continuous geometric branch | Seed; typed cache producer/load and downstream geometry. |
| B03 | Indexed pair/residual→body-oriented geometric point |1407bcfb0; 1407be780/1407bea00; 142332410 | Recoverable interpolation/tangent transform versus quantized embedding | Seed; inspect geometric callers/adjacent transforms, orientation and scale sources. |
| B04 | Pattern/fine-grid→rendered local geometry |14096be70/14096bba0;terrain consumers adjacent to B01/B03 | Coordinate-grid mapping sufficient versus asset-dependent necessary geometry | Seed; follow only links that can affect center embedding; retain existing footprint result. |

## Expanded graph / trace checkpoint

The seed rows remain unfinished parent questions. The following child conclusions
are scoped terminal dispositions; they do not close an unfinished parent. Export
names below identify ignored local receipts, not publication-cleared raw evidence.
See [trace notes](trace-notes.md) for corrections and corpus identities.

| Lead / parent | Typed dependency and evidence | Test of competing interpretation | Disposition / next edge |
|---|---|---|---|
| A01.1 / A01 |141832fd0 case 5 →141832000 and 141835450; ref+8c/+94 current XYZ or 14050f750 stored XYZ; frame byte bit 20 from inverse ref+d3 bit 2. Exports 09–11. |141856d10 was previously described too narrowly as a saver: callers 14181aa30 and 14181af40 establish load and save registration use. 141835450 copies 12 XYZ bytes, no spherical operation. | RESOLVED: actual initial-wire writer and flag predicate identified. Parent still requires matching load branch/context. |
| A01.2 / A01 |141835060 allocation callback → vtable 144af3d50+10 →1402b7070. Export 07 complete body. | Proposed hidden transform would need XYZ input/arithmetic; callback instead checks generation/ID and installs reference-counted pointer. | FALSIFIED_OR_IRRELEVANT as geometric producer. |
| A03.1 / A03 |140ad7200 keys: source-world ID high 32, ActivatedOverlayType\|10000 low 32, requested-world ID second key; 140adab20/140ada960 payload selection. Exports 03/12. | Validity must not be equated with status: 140ada760 can return valid/status 2 when component has no edge; valid/status 0 when found. | RESOLVED for lookup key and payload validity; bounds/source restoration remain parent dependencies. |
| A04.1 / A04 |14078c5f0 threshold/player XYZ →14078c060 queue →ShiftToTask vtable 144b3e3b0+8 →14078ce00 →14078c190 →listener+50 →140797dc0. Exports 08/12–14. | Separate listener+30/+38 reaches 797e90 and cannot establish rebase trigger. Task dispatch recovers actual+50 caller; mode 3 becomes 4, then 78c290 finishes mode 2. | RESOLVED: indirect trigger. Nonzero shift-vector producer and application remain A04.2. |
| A04.2 / A04 | Whole existing-instruction literal 1ec/1f0 census 07:14,392,060 examined, 2,011 candidates, uncancelled. Terrain constructor/resets write zero, constants verified 15. Expanded terrain-offset census 16 follows aliases/overlapping fields. | A callback read alone does not establish producer; offset equality alone does not establish manager type. | Unfinished dependency: trace manager shift storage, including overlapping stores/argument aliases. No exhaustion claimed. |
| A04.3 / A04 |797e90 ForEachReference →lambda 5d4655 vtable 144b91598+10 →add2a0 →add580 →acc9f0 →lambda 10609465 vtable 144b916a8+10 →ad6f40 →ad5530 →ref virtual+800. Exports 05/08/10/12/13. | Complete ad5530 only calls+800 when stored transform context matches callback context; base REFR+800 target 144b967b8 is no-op1402b56d0 (14/15). This callback does not itself perform a general XYZ projection. | RESOLVED for base REFR dispatch; broader reference frame conversion+7f8 →b734c0 →b73310 remains A01/A04 dependency. |
| B01.1 / B01 |77fc20 →state+20/+24/+28 residual f32 XYZ; pair requantized. Direct callers 78b030 and 141a20380; 78b030 returns state fields via output+10 onward. Exports 03/04/earlier durable-center 02. | Fractions survive local placement but do not enter returned pair in this function. | RESOLVED for split producer; placement consumers and equivalent continuous mapping remain parent work. |
| B02.1 / B02 | ExtraLocation0x81:0x40-byte object,+18/+20 pair,+28 body,+30 biome,+38 tagged location. Loader 546580, constructor/defaults 51b350/51b520 and inlined d0ff00/d028b0, clone 501550, setter 51b660. Exports 06/08/09/11. | Vtable slot+30 is 546700 comparison, not serializer. Constructors may preserve zero pair; clone copies bits. Pair is not inherently exact reference longitude/latitude. | RESOLVED for type/field producers; generic save writer and caller pair provenance remain B02.2. |
| B02.2 / B02 |51b660's eight direct call sites exported: 5a0520,769e90,7c3fb0,7a2df0,d06a60,d03de0,d03820,1416cf8f0.5a0520 uses 78d1f0 or saved PlanetWorldSpaceData; 7c3fb0 uses 76a340; other five construct zero pair. 769e90 copies caller pair. | Three 769e90 callers 1418a9900/1418abd60/1418b0920 use 78d660→142332410 integer projection. 1418af8e0 instead consumes queued pair array. | Unfinished: queued pair provenance/role, generic ExtraLocation wire writer. No universal claim about cache authority. |
| B03.1 / B03 |7bcfb0→7bcdc0→838730/8393e0/839b40; player XYZ, indexed-origin addition, floorXY, 142332410; sin/cos, 4a7da0 orientation, 3081d0 normalization,body+cc scale,double XYZ translation. Exports 05/06 and previous evidence. | Local fractions/Z discarded before celestial point; not an arbitrary reference-position API. | FALSIFIED_OR_IRRELEVANT as exact continuous center producer, RESOLVED quantized active-player celestial embedding. Adjacent grid seam geometry still under B03. |
| B03.2 / B03 |7be780/7bea00 integer neighboring footprint indices→142332410→142339250 location lookup, hemisphere wrap/reflection on grid overflow. Prior exact-beacon 16; freshly exported 16. | No local residual input; finds boundary neighbors with opposite location predicate. | FALSIFIED_OR_IRRELEVANT as fractional center producer; useful discrete seam semantics. |

Unfinished entries deliberately carry no terminal disposition. A terminal report
requires their resolution or a demonstrated static obstruction under the brief.

## Further resolved branches (exports 23–28)

| Lead / parent | Typed dependency and evidence | Competing interpretation / result | Disposition / boundary |
|---|---|---|---|
| B02.3 / B02 | `14051ea30`, case `0x81`, writes ExtraLocation location FormID, body ID, biome FormID and the raw 16-byte pair. Loader `140546580` reads the corresponding fields. Export 23, complete decompilation; instruction excerpt cap does not truncate the decompiled case. | A save-time fractional-XYZ recalculation would require a position input or arithmetic. This case copies the cached pair. | RESOLVED: generic ExtraLocation wire writer. This closes that part of B02.2. |
| A03.2 / A03 | `140ad30a0` scans the ordered source-world/type edge range from `140ad7040`; payload invalid byte `+0x35` must be clear, and all four cell bounds are inclusive. `140ad3240` subtracts the selected integer XY offset and returns its destination world. Exports 16/23/26. | Nearest-distance selection is falsified: the function returns the first valid containing edge in key order. Negative cells use signed comparisons. | RESOLVED: bounds selection and inverse cell translation. Producer/restoration coverage remains A02. |
| A03.3 / A03 | `140ad47e0` initializes the payload, copies integer shift and site pair; `140ad4a00` sets ownership/world linkage and definition/instance bounds; `140accc10` adds the integer shift to those bounds. `140ad1660` separately fills Z using `140acf480`. Exports 14/16/25/26 and EXP0019 export 06. | The DynamicNavmesh event `140694f80` is not the Z calculator. Height sampling is explicit and separate from the angular pair. | RESOLVED: payload field provenance; no fractional axis rotation in this constructor. |
| A04.4 / A04 | `140acd180` reference enumeration lambda vtable `144b916c8+0x10` → `140ad8ed0` → `14035d380` appends references; immediate move `140b4a0b0` or queued `1418c28b0` changes parent/world and invokes reference `+0x7f8/+0x800`. Exports 23–26. | The enumeration callback does not secretly project coordinates: its entire body collects a reference. Queued command copies the same 12-byte translation. | RESOLVED: immediate/queued application edge. Base REFR conversion is already A04.3; actor fallback is A04.5. |
| A04.5 / A04 | World/cell fallback lambda `144b91538+0x10` → `140add2d0` → `140add770`. Exports 26–28. | Complete body restricts work to actor refs and stored transform context before calling `+0x800`; no fractional projection. | FALSIFIED_OR_IRRELEVANT to ordinary outpost beacon conversion; actor-specific behavior is outside this target. |
| B01.2 / B01 | `14078b030` returns placement-state XYZ; `14078af30` replaces its local output with `14078bc30`; `1417dec70/1417dfdf0/1417df210` use placement in player/cell transfers; `141a20380` passes quantized pair into `14077fbc0`. Exports 11/23/26/27. | Surviving fractions are used in local placement and preserved across translation, rather than fed into `142332410` by these consumers. | RESOLVED: traced placement consumers, not proof about every geometry subsystem. |
| B03.3 / B03 | SurfaceMap listener `14076de40` → `14076db70` → `14076d500`: origin-derived local grid samples are floored after multiplying by float32 `0.01`, then `14078d660` → `142332410` supplies location-predicate pairs. Exports 21/27/28. | A dense SurfaceMap sample grid still uses integer planetary indices. Increased sample density is not a continuous residual transform. | FALSIFIED_OR_IRRELEVANT as exact continuous producer; RESOLVED for this map query. |
| B04.1 / B04 | `14078d370` forms local XY from 100×integer grid difference; `1409a0db0` checks landscape extent; `14099ff50` → `1409a0f20/1409a02b0` bilinearly interpolates local height samples. Exports 03/27/28. | Fractional XY is genuinely consumed, but the result is one float height, not a spherical/body direction. | RESOLVED: local height interpolation. This does not justify a metres-per-unit scale or radial interpretation of Z. |

Offset wording correction: the reference predicate is **mask `0x02` at `ref+0xd3`**
(zero-based bit 1). Earlier notes used “bit2” to mean this mask, not bit index 2.

## Content-request type correction and factory consumers (exports 29–32)

The B02.2 phrase “queued pair array” was premature. `1418af8e0` receives a
`PendingPlanetContentRequest`; its `+0x20` is a location-alias pointer, not a
longitude/latitude pair. `1418ab2d0` enumerates the body's existing content
sites through `14096f1a0` and a recovered callback vtable `144cb54c0`. The selected
candidate's pair is copied to local storage **before** constructing content
references. That pair determines quantized world/cell placement and is passed
to `140769e90`; it does not originate from the new reference's fractional XYZ.
The callback target remains a graph dependency until its body is checked.

Factory meaning is constrained by consumers rather than inferred from null
registration metadata: `142412d60` calls descriptor `+0x30` to create a component;
`142406db0` resolves a descriptor from a reflected type and calls `+0x20`;
`142406e90` resolves the same way and calls `+0x10`, returning an iterator.
Their callers `1424cb7d0/1424d39c0` manipulate reflected component collections.
Overlay's false/empty implementations differ from its creation implementation,
but the likewise false/empty PlanetWorldSpaceData factory is a counterexample
to treating those slots alone as proof of absent save persistence. **Type correction:**
the initial comparator at `144b05a80` is the world's
`BGSPlanetWorldSpace::CTPlanetWorldSpaceData`, not the galaxy's
`BSGalaxy::CTPlanetOverlayData`. The latter's actual factory is `144d5f508`,
registered by `14231d000` and creating/copying its tuple through `1423204d0`.
This distinct factory must be inspected before interpreting its wire behavior. The generic
wire mapping remains open; no serialization conclusion is drawn from these
factory slots.

Export 33 also corrects “existing content sites”: `14096f1a0` enumerates
**generated coarse candidate positions** over the planetary pattern chart,
not necessarily previously instantiated site objects. Its normalized input is
derived from integer pattern/sub-block coordinates and the `+0.5` center phase,
then passed through `142332410`. This remains independent of the subsequently
created reference XYZ. Callback `144cb54c0+0x10` resolves to `1418bb8d0`, whose
entire body forwards the pair to `1418ab600`; that classifier is the next edge.

Export 35 closes that classifier: `1418ab600` calls the location predicate
`142339250`, groups candidate positions by its location key and copies the
two doubles into a candidate array. Thus B02's content-request branch is
**FALSIFIED_OR_IRRELEVANT as a fractional beacon-coordinate producer**. All of
its angular inputs in this path originate in the coarse integer candidate
enumeration, before reference construction. This does not classify every use
of the location database.

The actual galaxy factory at `144d5f508` has `+0x28/+0x30 → 1423204d0` (typed
tuple creation/copy), whereas Overlay's `+0x28` is empty and `+0x30` constructs
its dynamic payload. Both share empty iterator/false earlier slots. This is a
real distinction worth tracing; it still does not assign serialization semantics
to a slot without a corresponding wire consumer.

Parent-probe-01 freshly joins five decoded samples (Save25/26, S1/S1C, Save52)
to frozen decoded hashes and inspects all R3 records plus qualified unit-6 site
associations. No matching R3 parent records; 23 qualified parent/site spans.
Controlled samples carry `0x0b`, mature direct-pair examples `0x2b`.
Raw spans remain LOCAL-ONLY. This probe does not decode the generic unit-6
component wire grammar or supply a continuous-position oracle.

## Direct serialization edges recovered (exports 36–40)

| Lead / parent | Typed dependency / evidence | Prediction checked | Disposition / next edge |
|---|---|---|---|
| A02.1 / A02 | `141814220 → 1418237f0 → 141825820` unit 6 → `141822570` constructs `1418698d0` WriteUtil visitor and invokes typed serializers. | Registered-factory slots are not the complete persistence route. | RESOLVED: actual global save route. Corresponding typed readers remain dependencies. |
| A02.2 / A02 | `14140ff80 → 141413a80/141413dd0` iterates `1461e1d9c` galaxy site edges; writes count, body ID, world ID, uint16 kind, raw 16-byte pair and repeated world ID. `1402b7740/1402ba430` establish uint32/uint16 wire widths. | Native field order matches 30-byte site entries in Save25/26; pair is copied, not recomputed from XYZ. | RESOLVED: scoped site tuple wire order, pending ID conversion callback and load-reader trace. Full unit-6 decoder is not claimed. |
| A02.3 / A02 | `141822570 → 140ad5f20` serializes the world's `1461dd7ec` component: world/linked IDs, two uint32 body fields, secondary world ID, flag byte and four signed bounds; ends with zero ID. | The persistent world component is distinct from both the site tuple and activated edge. | RESOLVED: writer fields. `140ad6150` and neighboring functions are reader candidates from the existing-function inventory, not yet qualified. |
| A01.3 / A01 | `1418236c0` unit-3 mask `0x0c`; unit-3 string table plus body length precedes unit 4. Parent-probe-03 closes five samples independently. | A plain tag/length envelope fails; mask-aware framing succeeds uniquely. | RESOLVED for scoped framing only. Active-context fields require native load semantics. |

Parent-probe-04 retains candidate 37-byte world records including false positives;
its initial bound filter paired the axes incorrectly. Native `140ad30a0` confirms
bound order **xmin, xmax, ymin, ymax**. This diagnostic filter is corrected in the
probe source; prior output remains preserved and is not a qualified decoder.

## Typed restoration and packed origin (exports 42–49)

| Lead / parent | Typed dependency / evidence | Test and disposition / remaining dependency |
|---|---|---|
| A02.4 / A02 | `14182dc30 → 14182e280 → 14140c8c0 → 1414128c0`; site reader restores body/world/kind/raw pair/repeated world through `140777560`. | RESOLVED: typed load route matches 30-byte writer. ID dispatch is separately A02.6. |
| A02.5 / A02 | `14182e280 → 140ad6150`; restores world component `1461dd7ec`, system/body fields, links, flag and four signed bounds; terminates at zero world ID. | RESOLVED for typed reader/order. Scoped probe 05 finds expected records but retains false positives; complete wire framing is still required for a qualified generic decoder. |
| A02.6 / A02 | Write-ID `14186b940 → 14186bd40`; read thunk `14186b8e0 → 14186bc80 → 1418599a0`. Exports 40/47/49. | RESOLVED widths and dispatch; final token remapping remains relevant work, not a blocker. |
| A01.4 / A01 | `14096fb40` world-key unpacker; `142332ea0 → 142332d90` body identity; `14078d930` key-versus-active-origin delta. Exports 47/48 and five pure decoder tests. | RESOLVED packed key formula and controlled origin/independent Jemison identity. Save3 load selection remains an expanding dependency. |
| A02.7 / A02 | `1403a5770 → 1403a5e00 → 1403a53b0`; descriptor key copied into world and active-world/persistent-ID components registered. | RESOLVED generated-world creation branch. Applicable saved-descriptor reader and its caller remain work. |
| A01.5 / A01 | Whole existing-instruction `+0x310` census 44; typed checks 45. `14079b520/14079c540/14079c5e0` use array pointer/count; `140bb5570` resource lookup. | FALSIFIED_OR_IRRELEVANT as packed-key producers; offset equality does not imply type equality. |

## Final graph expansion and dispositions

Evidence receipts: [trace notes](trace-notes.md), [frame map](call-and-dataflow.md),
[residual map](residual-map.md), selected [saved frames](saved-center-frame.csv)
and [descriptors](saved-world-descriptors.csv). Native exports 42–68 and fresh
hash-qualified saved-context 04 / saved-center-frame 01 outputs stay LOCAL-ONLY.
Previous “seed”, “unfinished” and “next edge” text above records investigation
history; it is not an additional unresolved current graph.

| Lead / parent | Expanded dependency / competing prediction tested | Current terminal disposition and exact boundary |
|---|---|---|
| A01.6 / A01.3–4 | Unit 3 actual loader `141825e00 →141825ac0 →1407896d0`; key/checksum compares resident world, resets/reuses through 7895a0. | RESOLVED: active-context key is a reuse discriminator, not a direct universal manager-origin assignment. |
| A02.8 / A02.7 | `14132d260 →1403a5130` and `14132d500 →1403a5560 →1403a5e00 →1403a53b0`; descriptor body 4/key 8/legacy ID3 plus queued strings. | RESOLVED reader/writer/creation join; six protected samples, 111 descriptors/38 installed bodies, zero identity mismatches. |
| A02.9 / A02.5–6 | Typed ID4 read `14186b8e0 →14186bc80 →1418599a0`; legacy ID3 `1418650d0`, writer 141868de0; load-order/reference-map remapping. | RESOLVED widths and domains. No universal equation raw token=live FormID. Scoped component locator requires exact selected saved tokens and unique terminated grammar, not arbitrary live-ID assumptions. |
| A02.10 / A02.5 | `140ad6150` world/linked/system/index/secondary/flags/bounds grammar and descriptor/PNDT joins; unique run covering all 28 selected parents, 724 entries locally. | RESOLVED scoped parent-component-secondary-world identity. A generic unit 6 prefix parser is FALSIFIED_OR_IRRELEVANT as necessary for these independently qualified joins; no generic decoder completeness claimed. |
| A01.7 / A01 | `1418325a0/141833b20` mask 20 and cell/world branches; `140ad3ed0 →140ad3240`; pure saved-frame audit. | RESOLVED studied active saved-frame representation: descriptor origin versus site base. 25 beacons, 23 active rows, two disabled retained. Negative floor is explicit. Predicting every future loaded frame is A03.4. |
| A03.4 / A03 | `140798030/7986d0/798a30` choose active/requested pair; `140ad30a0/ada3a0` require current edge store/validity; `140ad5950/5ba0/7ad0` clear/invalidate; `140ad9810` drains activation queues. | STATICALLY_BLOCKED **only for an unspecified future runtime instant's exact loaded edge/height/epoch**. Save records do not specify subsequent travel, resident-world reuse or queue timing. Two viable states: settled captured Kreet origin versus a later different active origin/edge validity using the same saved site. Producers/consumers are identified; another static scan cannot determine an unspecified future input history. Saved indexed center does not require that prediction. See frame map for minimum observation. |
| A04.6 / A04.2 | Constructor/reset/ordinary rebase trigger zero 1ec/1f0/1f4; whole literal census plus typed overlap/reset/queue/listener paths; `140ad9cd0` subtracts displacement from edge XY/bounds if nonzero. | RESOLVED ordinary trigger and effects. FALSIFIED_OR_IRRELEVANT **as a necessary unknown for reconstruction of the recorded saved center**: descriptor/site/saved-mask computation uses no future manager 1ec alias. Arbitrary alias writers are not proved absent, and an arbitrary live frame is covered by A03.4. This explicit scope excludes, rather than pretends to finish, a whole-program pointer-alias proof. |
| B02.4 / B02.2 | `1418af8e0` typed request correction; `14096f1a0 →1418bb8d0 →1418ab600` generates/classifies integer-centered candidate pairs before reference construction; `14076a340` floors local offsets. | RESOLVED provenance; FALSIFIED_OR_IRRELEVANT as independent continuous oracle. Together with B02.3 this closes the earlier queued-pair/wire-writer questions. |
| B01.3 / B01 | Both 77fc20 helper branches: 77f900→780a50→780aa0→781390; 77e350→780710→77f6e0→78d2c0→same reference search; 77def0 eligibility. | RESOLVED indirect fractional producer graph: existing XYZ plus integer translation, nearest eligible reference selection, no angular residual output. |
| B04.2 / B04 | Extra78d370 caller 14141ccd0→14141dc70; local camera-ray/Z-plane bounds, scalar height baseline; native 96be70/96bba0 and height 99ff50 output constraints. | RESOLVED local height/footprint roles; FALSIFIED_OR_IRRELEVANT as off-grid body embedding. Descending every scalar-height or eligibility caller would not repair the missing output relationship. |
| B03.4 / B01/B03 | Same-phase linear versus smooth-warp extensions in residual-map; integer centers, 100-unit periodic translation and nonzero residual controls. | STATICALLY_BLOCKED exact continuous embedding: required mappingE is non-unique under every recovered constraint and existing observation. Four tests demonstrate ambiguity, not truth. Precise independent geometric observable and discriminating sample are specified in residual-map. |

### Parent-question closure

| Parent | Terminal disposition | Answer / completeness |
|---|---|---|
| A01 | RESOLVED | Saved flag/parent/descriptor/site→indexed center plus residual for the studied active frames; disabled examples explicitly excluded from active placement. |
| A02 | RESOLVED | Applicable typed serialization, ID conversion, descriptor creation, world links and immediate/deferred activation registrations recovered. Scoped locator, not a whole-save decoder. |
| A03 | STATICALLY_BLOCKED | Exact future loaded-frame state requires an observation time/history and current store/validity/height. Saved frame and geographic indexed representation are reconstructed independently. |
| A04 | RESOLVED | Rebase trigger/dispatch/ordinary writes and typed edge/reference translations traced; runtime frame state distinguished from recorded durable center. No universal no-alias claim. |
| B01 | RESOLVED | Residual producers, indirect helpers, storage and applicable local placement consumers closed. |
| B02 | RESOLVED | Cache/default/copy/save/load/setter/request provenance closed; no continuous oracle in these branches. |
| B03 | STATICALLY_BLOCKED | Exact off-grid mappingE is not identified; discrete and celestial consumers lose residual before projection. Equivalent extensions tested and non-unique. |
| B04 | RESOLVED | Installed footprint/index/orientation and local height branches distinguished from coordinate embedding; no observed non-square/multi-size claim added. |

**No relevant untraced edge remains in this investigated target graph.** This
statement applies to the graph and typed exclusions above, not all functions or
possible external representations. The terminal outcome is
**STATIC_EXHAUSTION_DEMONSTRATED within this scope**, subject to critical review.
A new source supplyingE or contradicting saved-frame qualifications reopens the
appropriate parent. Neither elapsed time nor function count is a scientific
stopping premise.
