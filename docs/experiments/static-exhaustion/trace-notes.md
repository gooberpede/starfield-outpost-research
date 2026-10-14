# EXP0020 trace notes (working; not a terminal report)

Pinned static VAs only, base 140000000; raw decompilation in ignored recon exports.
These authored deductions are REVIEW-REQUIRED, pending instruction-level and corpus
cross-checks. No exhaustion/completeness claim yet.

## Material discoveries

- A01:141856d10 prepares a frame description on **both** save and load registration
  paths. 14181aa30 is a load manager (LoadError diagnostics and LoadGame dispatch),
  whereas 14181af40 saves. Earlier single-purpose save naming is over-narrow.
-141835c20 reads wire frame byte into initial-data+2c (shape-specific implicit
  defaults),1418325a0 resolves parent FormID as WRLD0x56 or CELL 0x49 and looks up
  ActivatedOverlayType edge using source-world/requested-world keys. With frame
  bit 0x20 set, raw floor(XY*.01) gets the edge's integer XY added before generated
  world cell lookup 140bbda00. The flag must not be ignored for negative-X samples.
-14181b8e0 registration branch subtracts selected translation from raw XYZ when
  frame bit 0x20 is clear and selected world has overlay predicates. 141833b20's
  created-reference branch instead **adds** selected edge translation to raw XYZ,
  then passes XYZ through NEW_REFR_DATA to 1405a0520. Exact branch conditions still
  being qualified. 141835060's local-function callback is a reference allocation
  callback, not yet evidence of a hidden geometric transform.
-140ad7200 uses high 32 source-world FormID, low 32 ActivatedOverlayType|0x10000,
  second-key requested-world ID. 140adab20 copies complete valid edge payload
  (unless force permits invalid) from reverse component index. 140ad9cd0 subtracts
  rebase dx/dy from edge translation and bounds; it does not rotate fractions.
- B01:14077fc20 stores residual f32 XYZ in state+20/+24/+28 independently from the
  pair returned via output. Both direct callers examined: 14078b030 terrain load
  and 141a20380 reference transfer. The former returns placement state fields to
  its caller; the latter invokes 14077fbc0/14077f900 for cell-local transfer.
  The pair is always requantized before return. Residual consumer beyond terrain
  load remains a dependency, not evidence of absence.
- B02:ExtraData0x81 is **ExtraLocation** (existing native RTTI/vtable name). Loader
  switch constructs 0x40-byte object then 140546580 reads it. Trace cache producers,
  vtable save/load and authority before concluding quantized or continuous.
- B03:1407bcfb0 obtains player position via 140b4cee0(DAT145f43230), adds
  indexed origin offsets from 1461fae88 if valid, floors local XY, projects discrete
  indices, builds unit sphere
  direction, applies body orientation, normalizes, scales body+cc and translates
  body double XYZ+30/+38/+40. It discards fractions and local Z in this path.
  Direct caller 1407bcdc0 selects active-body ECS data; its three consumers compute
  relative-body direction/dot products. This is an active-player celestial query,
  not an arbitrary reference XYZ continuous projection. Any earlier characterization
  as a generic body-position transform must be narrowed.
- The listener vtable actually starts 144b3e450; rebase 140797dc0 is slot+50,
  whereas 78b030 dispatches slot+30 (797e90 wrapper). Separate+50 trigger remains
  under investigation; the two callbacks must not be conflated.
- All direct 142332410 callers now exported in prior+static-exhaustion 01..05.
  The additional 04/05 callers use integer grid indices (some tile/coarse centers),
  not a residual-fed normalized coordinate. This is scoped to those calls; it
  does not rule out an equivalent continuous transform elsewhere.

## Open edges explicitly retained

A: registration constructor/serialization, negative-X flag cross-check, listener
vtable trigger and producers of terrain+1ec/+1f0, reference-application lambda,
gauge cancellation under rebase. B: ExtraLocation producers/save/load, terrain-load
placement consumers, adjacent geometric transforms, continuous alternative mapping
and independent corpus validation. Existing B04 footprint coverage is retained.

## Second trace round

- New read-only OutpostRecon queries: data windows (24 qwords with target primary
  symbols), substring symbol inventory (explicit 256 cap), whole existing
  instruction rebase-field census. Reads existing listing only, no analysis or
  mutation; output local UTF8. Census 07 visited 14,392,060 instructions and selected
  2,011 non-stack literal+1ec/+1f0 candidates, uncancelled. This is an offset
  inventory, not type proof or all overlapping/indirect writes. Terrain-region
  writers narrowed to constructor 787830 and 78c290/78c3a0/78c5f0; semantic producers
  still being followed through callees and argument-address aliases.
- Callback slots: vtable 144b3e450, +30/+38→797e90, +50→797dc0.
  Lambda 5d4655 wrapper 144b91598+10→140add2a0→140add580→140acc9f0, with a second
  callback lambda 10609465 (target recovery pending). Lambda 3a268 callback
  144af3d50+10→1402b7070 checks form identity/generation and installs ref-counted
  pointer; no XYZ/angle operations. Allocation callback eliminated as a geometry
  producer by its complete body, not by absence of direct xrefs.
- **Actual initial wire writer**141832fd0 case 5 calls 141832000, chooses current
  ref+8c/+94 or stored extra-location transform via 14050f750/14050f5b0, and emits
  through 141835450. Frame 0x20 is set when ref+d3 bit 2 is **clear**.141856d10 is
  registration-frame preparation, not itself the wire XYZ writer. Setter/state
  provenance of d3bit2 and 141832000 transformations are active dependencies.
- ExtraLocation constructors51b350/51b520 and inlined d0ff00/d028b0 initialize
  pair/body tozero while assigning location association; 501550 case 81 clones
  existing pair/body/biome/location exactly. 51b660 is the pair+body setter and is
  now an explicit producer lead. 7a2df0 calls it after flooring spawn XYZ for biome
  lookup, with locally zero-initialized pair (requires full dataflow verification).
- Fresh durable-center decode static-exhaustion 01 finished. Save25/26 retain exact
  center bits and site pairs, all 19 mature beacons have 0x20 set (17 flags 2b,
  two 3b). Two 3b samples have no points under the current qualified association
  decoder; do not treat missing rows as arbitrary body guesses. Negative-X case
  remains token 84ede9 with flag 2b, center(-53.4358024597168,58.03339767456055,
  8.46107006072998), body 0005E0DB, index 13152,45120.
- Capture verification attempt static-exhaustion 01 decoded existing captures but
  failed final protected-file enumeration because a temporary Ghidra analysis
  project file disappeared during simultaneous read-only export. No preservation
  success is claimed from that failed attempt. Preserve receipt and rerun after
  Ghidra exits; do not include volatile scratch as stable analysis content.

## Third trace round and independent replication

- Trigger recovered: ShiftToTask vtable 144b3e3b0+8→78ce00→78c190,
  mode 3 listener+50→797dc0 followed by+58, then mode 4→78c290 completion.
  Manager field1ec/1f0 literals in 07 and expanded 16 (91 selected instructions,
  14,392,060 examined, uncancelled) still expose only zero writes in the manager
  code region. This is an open dependency through aliases/overlapping writes,
  not proof that nonzero state is impossible. Constructor/listener module targets
  are being recovered. 78c5f0 computes1a0/1a4 from player position threshold but
  applies the shift snapshot after 78c060 sets18c. The prior suggestion that
  listener+60 must set 18c was wrong: 78c060 explicitly writes its byte argument.
  Global 18c census additionally identifies 788e70/789850 setters; their expanded
  transform writes are the next dependency. Module+60 slots recovered so far are
  no-ops, consistent with this correction.
- Virtual reference conversion: base REFR vtable 144b95fb8+7f8→b734c0;
  +800→2b56d0 no-op. b734c0 toggles ref+d3bit2 and calls b73310, which adds XYZ
  translation to ref+8c/+94 and associated extras29/d5. No angular rotation or
  fractional→sphere operation in this frame conversion. Subtype-specific work
  remains separate from the ordinary base REFR scope.
- Export 19 was attempted while 18 was still exiting; Ghidra rejected project
  locking before opening/exporting. No database edit or workaround. Failure log
  retained; retry 19-retry starts only after 18 completes. This is an orchestration
  error, not evidence that a scientific lead is inaccessible.
- Fresh Save52 extraction hash a1d4490a6b41c05ad08f68b2efa28f71d6ebac56cb9aabf55eb61356833b57e2
  was frozen before network JSON comparison. Its decoded hash matches HIST0267
  (e3c0dc34cbbdcd26bb85d212fc458378b44404b37a5f54b635070e03e1565b93).
  Original audit_static_exhaustion.py compares independently named active sites:
  all 17 body IDs, cached body IDs and system IDs agree with the manually authored
  network. This validates identities, not continuous positions. Topology also
  passes the existing mature validator; eight of 352 shifted grammar windows
  accept syntactically (retain this negative-control limit).
- The mature negative-X example must be retested under frame 20-relative semantics.
  The previous candidate-origin calculation subtracts floorXYZ from site index
  without interpreting the saved flag. It is not a valid counterexample to the
  existence of a save-derived frame transform. Do not retroactively erase that
  numerical observation or assert the new formula until the context is traced.

- Descriptor correction: 141881660 registers the native name "Overlay" through
 142404ef0 with optional metadata pointer null. 142404ef0 stores that pointer only
 when its+e byte is 3; it is not established as a serializer pointer. Previous
 "null serializer" inference must not be promoted. Descriptor 14590a3f0 points
 to vtable 144b91788, whose+30→ad7330 creates the component; +8/+10/+28→36cca0
 returns an empty iterator, +18/+20→2b75f0 returnsfalse, +0→4556d0 destructs.
 Generic factory/serialization meaning remains to be qualified from consumers.
- Global 18c census 20:14,392,060 instructions, 292 selected, uncancelled. Newly
 inspected788e70/789850 only clear transition state and tear down/reset terrain;
 they do not produce the nonzero vector. 78c060 is the only direct caller reached
 from 78c5f0 setting it true. 22 also queried the singleton's exact static addresses
 (146218488+1ec/+1f0/+1f4/+1c0/+18c): no direct xrefs there. This excludes those
 direct static accesses, not all overlapping/indirect writes. Do not call the
 callback's guarded nonzero branch observed or assert a runtime-variable blocker
 merely because its producer has not been found.

## Fourth trace round

- Exports 23–28 close the ExtraLocation generic writer (`51ea30` case 81), the
  immediate/queued reference move (`b4a0b0`/`1418c28b0`), the collection callback
  (`ad8ed0`) and actor-only fallback (`add770`). The first copies pair bits; the
  callbacks do not supply fractional spherical geometry. See the ledger for
  exact scopes and virtual targets.
- `ad30a0` is first-valid-containing-edge selection in ordered key range, with
  signed inclusive bounds; it is not nearest-site selection. `accc10` derives
  bounds from definition/instance extents plus the integer edge shift.
- Terrain height has a real continuous consumer: `99ff50` bilinearly samples
  the local height field using fractional XY, through `9a0f20/9a02b0`. Its result
  is a scalar height. `76d500` SurfaceMap location sampling independently floors
  even its dense local sample grid before planetary projection.
- Reference flag wording is corrected to mask `0x02` at `+0xd3` (zero-based bit 1).
  Older “bit2” wording denoted the mask and must not be read as mask `0x04`.
- `1418af110` constructs `PendingPlanetContentRequest`; `1418aefd0` queues a
  copy, `1418bc060/1418bb7e0` dispatch it, and `1418aee00/1418af8e0` create/update
  planet content. The pair-array producer still requires qualification. Native
  registration metadata null remains insufficient evidence of nonserialization;
  a constrained component-factory dispatch inventory is the next trace.

## Fifth trace round

- Exports 29–32 qualify generic factory consumers and correct the content-request
  type. See the ledger correction: queued location alias is not a coordinate
  pair. `1418ab2d0` obtains pre-existing body sites before reference creation,
  using `14096f1a0` and callback vtable `144cb54c0`; the callback body is next.
- Saved beacon parent tokens are not necessarily R3 changed-record tokens:
  the freshly extracted Save25/26 and Save52 examples have no matching R3 parent
  records. Their global-unit-6 associations are therefore the relevant next
  serialized context path. This is a record-domain distinction, not evidence
  that their world identity is absent from the save.

- Exports 36–37 reach actual global serialization. `1418237f0` routes unit 6
  through `141825820` → `141822570`, which builds the storage visitor and calls
  typed galaxy serializers plus `140ad5f20`. This is a promising unclosed A02
  dependency, independent of generic reflected factory-slot speculation.
  Unit 3 separately writes active context and invokes `140ad6cb0` (two ID lists)
  and `1403a6ae0` (typed world-data visitor). The initial simple preceding-unit-3
  envelope probe failed on Save25: unit 3 cannot be assumed to have the same
  suffix grammar as units 4–16. Its failed output directory is preserved;
  no source or earlier successful receipt was overwritten.

- Parent-probe-03 corrects that envelope assumption using the native unit-3
  buffer mask `0x0c` from `1418236c0`: compact string-reference count, uint16
  string indices, then uint32 body length. Unique envelopes close at the known
  unit-4 header in all five samples. Unit-3 bodies are 153 bytes in the four
  controlled samples and 2,228 bytes in Save52; string counts are 10 and 176.
  This is scoped framing, not a full semantic decoder.
- `141822570` explicitly invokes `140ad5f20`, which serializes the world's
  `DAT_1461dd7ec` component: world ID, linked world ID, body-related uint32 fields,
  secondary world ID, flags and four integer bounds, terminated by zero ID.
  It is distinct from ActivatedOverlayProperty (`145eaac2c`) and the galaxy
  site's pair component (`1461e1d9c`). The corresponding load path and exact
  identity remapping remain active A02 dependencies. The earlier registration
  speculation is superseded by this direct wire route, without erasing it.

- New testable packing hypothesis: the first uint64 in unit-3 body is directly
  written from active generated world's `+0x310`. Save25/26 and S1/S1C have
  `0x02b20e79528028e0`; low uint16=10464, next uint16=21120, upper uint32>>9=88327,
  `(upper>>3)&63=15`, `upper&7=1`. These independently match captured Kreet
  origin and installed system/body-index identity. Save52 has
  `0x022e401882204260`, yielding (16992,33312), system 71456, index 3, hemisphere 0;
  its save display location is Jemison/The Lodge. These are hypotheses pending
  native pack/unpack/load verification, not a new address/layout baseline.
  This makes the unit-3 context a useful A01 lead rather than an irreducible
  missing-runtime-state claim.

## Sixth trace round: typed load paths and active key

- Exports 42–46 establish `14182dc30 → 14182e280` global-unit-6 load,
  constructing `1418695e0` ReadUtil. `14140c8c0 → 1414128c0` reads the
  galaxy site tuple in writer order and restores it through `140777560`.
  `140ad6150` restores the distinct world component, including linked and
  secondary worlds, system/body-index fields, flags and signed bounds.
- Write-ID callback `144cb0c08+0x10 → 14186b940 → 14186bd40` uses
  4-byte tagged IDs and records original IDs in the visitor. These are not
  3-byte R3 tokens. Read-ID remapping remains a dependency (`144cb0bb0`).
- Export 44 examined all 14,392,060 existing instructions for non-stack
  literal offset `0x310`, returning 611 candidates without cancellation.
  Type checking rejects `14079b520/14079c540/14079c5e0`: their `+0x310`
  is an array pointer paired with count `+0x308`, not world packed identity.
  `140bb5570` uses the world key for resource lookup and does not decode it.
- `1403a5130` copies world `+0x310` into a world descriptor;
  `1403a53b0` copies descriptor `+8` back to world `+0x310`. This proves
  a restoration copy, not the proposed field packing. `140ad08d0` is a
  typed consumer passing world `+0x310` to `14096fb40`, comparing pattern
  identity with the site pair and applying integer translations. The
  unpacker is the next useful dependency.
- Correction: `1418286f0` is another writer (buffer grows and fields are
  appended), not the unit-3 reader. Its player/context-specific key write
  must not be mistaken for a load operation.
- Parent-probe-05 reruns the corrected 37-byte candidate bound filter.
  Matches remain diagnostic until framing/ID ownership is independently
  qualified; five sources retain their original identities.

- Export 47's **typed unpacker `14096fb40` confirms the packing hypothesis**:
  low 16 X, next 16 Y; upper word tag `&7`, body index `>>3 &0x3f`,
  system `>>9 &0x3ffff`. `142332ea0 → 142332d90` resolves system/body to
  the body identity and requires agreement with landscape `+0x54`.
  Tags 2/3 reverse both encoded axes before hierarchical lookup; the original
  encoded axes/tag are retained by the new pure `planet_world_key.py` decoder.
  Reserved high bits are reported; qualification rejects unsupported values.
  Five controls pass, including independent Kreet/Jemison matches and reserved,
  range, tag and sentinel rejection. This establishes encoded identity/origin,
  not the complete saved-to-loaded selection or a continuous position.
- Export 48 `1403a5770 → 1403a5e00 → 1403a53b0` reconstructs generated
  worlds from the descriptor and registers active-world/persistent-ID
  components. `14078d930` unpacks a supplied world key, compares it with the
  active (or mode 3 old) pair and returns an integer grid difference.
- Read-ID dispatch is a thunk: `144cb0ba8+0x10 → 14186b8e0` jumps to
  `14186bc80` (export 49). It consumes an existing queued ID if present;
  otherwise reads four bytes, forms the tagged reference token and calls
  `1418599a0`. The latter remapping is being traced. Two guessed function
  starts in export 49 have no existing function: no analysis was created and
  these unsuccessful guesses prove nothing about absent functionality.
  Existing-function inventories replace further start-address guesses.

## Seventh trace round: native packer and six-save context audit

- `14096fa90` (export 51) is the inverse packer. It composes integer hierarchy
  coordinates, reverses axes for tags 2/3, and packs system/body/tag/Y/X.
  Its existing xref is the unit 9 player-load path `141829ec0`, where it derives
  a snapped generated-world key while preserving a separate local XYZ.
- Correction: `141827960` is a pre-load dispatcher; its unit 3 branch clears
  terrain state through `1407895a0`, rather than reading the key.
  `141827380` is explicitly FinishLoadGlobalData. The actual load dispatcher
  `141825e00` case 3 calls `141825ac0 → 1407896d0`; this is the next edge.
- `1418599a0` resolves untagged tokens through the save-load reference map,
  handles the static/dynamic tag bits and load-order conversion separately.
  Thus raw save token equality is not a universal live-FormID comparison.
- Export 50's second inventory argument accidentally had a ten-digit endpoint;
  the script rejected it after preserving the completed first inventory.
  Retry 50 uses the correct nine-digit endpoint and succeeds. No project
  analysis or original evidence was changed. Exit 0 alone is not success:
  the script-error text is retained and checked explicitly.
- `audit_saved_world_context.py` independently redecodes six hash-verified
  archived saves and writes only selected context fields plus preservation
  receipts. Run `saved-context-01` succeeds. Save2/HIST0245 and Save52/HIST0267
  share the Jemison key; four Kreet controls share the captured-origin key.
  [Selected table](saved-world-context.csv) retains decoded hashes/offsets;
  the checksum differs across some samples and is not a body identity.
  Seven pure tests include malformed envelope and caller-boundary rejection.

- Export 58 qualifies the **purpose** of the leading unit 3 key: load
  `141825e00 → 141825ac0 → 1407896d0` reads key/checksum and compares them
  with the already resident generated world and site checksum. Agreement
  controls the reset/reuse argument to `1407895a0`; the function does not
  itself copy the key into the manager's origin. Thus this field records the
  saved active context, but treating its presence alone as the origin loader
  would be premature. The descriptor/resource restoration path remains useful.
  Unit 3 also loads temporary form handles (`14132d500`), auxiliary overlay IDs
  (`140ad8930`), and queued typed world data (`1403a7eb0 → 1403a74e0`).

## Eighth trace round: generated-world descriptor persistence

- `14132d260 → 1403a5130` serializes the generated-world descriptor array;
  `14132d500 → 1403a5560 → 1403a5e00 → 1403a53b0` reads it and creates
  the world with its packed key, body and saved world identity. Export 59/60.
  `14132e880` creates a DisposableInstancedFormDB resource entry; it does not
  supply an additional geometrical transform. The typed world-data reader
  `1403a74e0 → 1403a7cc0` restores one uint32 field under type 145fdce08,
  distinct from the descriptor and galaxy site tuple.
- Descriptor entry body is **15 bytes**, not 16: body uint32, packed key
  uint64, legacy three-byte world token. Two string references per entry are
  consumed from the envelope queue. `141868de0/1418650d0` (export 61) confirm
  this legacy ID width versus four-byte typed ReadUtil/WriteUtil IDs.
- Fresh `saved-context-03` decodes six protected sources, walks the pinned
  installed ESM's PNDT records directly, and compares descriptor system/body
  index with GNAM. **111 descriptors, 38 distinct bodies, zero mismatches**;
  Save52 supplies 88 descriptors. No per-body fit. Source and ESM identities
  agree before/after. [Selected descriptors](saved-world-descriptors.csv).
  Eight pure controls pass, including exact token width and string budget.
- Manager reset `14078c3a0` writes the known zero constants at+1ec/+1f0/+1f4;
  `14078d090` clears old world handles and `14078f0b0` drains jobs. These
  functions do not introduce an angular residual transform. Rebase aliases
  remain a scoped graph question; offset census alone is not a universal proof.

## Ninth trace round: scoped world-component runs and saved frames

- `saved-context-04` joins the typed `140ad5f20/140ad6150` 37-byte grammar
  to exact selected parent IDs, installed system/body identities and the
  unit-3 secondary-world descriptors. It finds a **unique zero-terminated run**
  per selected sample, with 78/78/76/76/416 records (724 total), all 28 selected
  object parents covered and no duplicate world IDs/body disagreement. The
  locator is scoped: it does not generically parse the preceding unit-6 fields.
  Raw runs stay ignored; selected beacon joins are in
  [saved-center-frame.csv](saved-center-frame.csv). Five malformed/ambiguous
  controls pass. Save2 has no selected beacon parent, so no component scan is
  claimed for that sample.
- `1418325a0` floors saved float32 XY times float320.01; mask 0x20 adds the
  applicable edge integer shift before generated-cell selection. `141833b20`
  case 5 conditionally adds that edge's 100×XY translation into loaded XYZ;
  `140ad3ed0 → 140ad3240` supplies the same signed integer displacement for
  cell-based conversion. No local-axis rotation is present in these branches.
  Source-world and site-relative saved frames therefore require different bases.
  This does not predict every live edge's validity/height/loading epoch.
- `audit_saved_center_frame.py`, run 01, applies one flag-qualified rule to
  **25 beacon records**, including two disabled records retained without a
  direct active-site prediction. For the remaining 23, mask 20-clear uses the
  secondary world's packed origin; mask 20-set uses the saved site anchor.
  Save25/26 both workshop identifiers produce exactly identical center bits,
  body, cell and residual. S1/S1C also agree. Independent mature examples use
  the same rule without fitted parameters; the 17 active identities were
  previously compared with the separate manual JSON. This is a saved indexed
  representation, not independent off-grid angular truth.
- The negative-X token 84ede9 is now frame-qualified: site(0,13152,45120),
  frame 2b, floorX=-1, hence selected cell(0,13151,45120), residualX
  46.5641975402832. The earlier site-minus-floor candidate 13153 is superseded
  as an origin inference; its counterexample remains valid against the earlier
  frame-unqualified rule. Four arithmetic/boundary tests pass, including a
  two-axis seam and disabled/missing-site rejection.
- The first audit call attempted all 23 historical samples against the five
  component-qualified samples and correctly rejected a missing parent. The
  tool now explicitly restricts its sample scope to the qualified component
  labels. No incomplete output directory or original mutation resulted.
- Exports 62–65 reopen both helper branches of `14077fc20`.
  `14077f900` uses integer differences between requested/site pairs and then
  enumerates existing cells. `14077e350` searches candidate integer cells,
  creates/selects an overlay and delegates to the same reference search.
  Recovered callback vtables144b3dc10/144b3dc70 dispatch through
  `140780a50/140780710`; the latter reaches `14077f6e0`, whose proximity test
  calls integer-pair displacement `14078d2c0`. The nested reference callback
  and the additional `14078d370` consumer 14141ccd0 remain the next dependencies.

## Final trace closure and packaging

- Exports 66–68 close those dependencies. Nested callback
  `140780aa0 →140781390` compares eligible existing references by local XY
  distance and copies XYZ plus integer translation; `14077def0` is eligibility.
  `14141ccd0` takes only Z from `14078d370`; `14141dc70` intersects camera rays
  with a local Z plane to choose local sampling bounds. Neither is a residual
  to body-direction consumer. See final residual map for exclusions and
  same-phase countermodels; all earlier next-edge text is historical.
- `saved-center-frame-02` additionally writes 23 explicit unvalidated countermodel
  comparisons. Four tests show agreement at integer centers, translation
  invariance, different actual interior answers and input guards. Together with
  the other new controls, the complete save-analysis suite passes 121 tests.
- Packaging's initial link check ran before its own planned diff/receipt outputs
  existed and correctly failed; the packager now validates those outputs after
  generation. A retry exposed the numeric table helper's create-only mode;
  the local packager now regenerates only its own authored locator tables.
  These are review-generation corrections, not failed scientific tests or
  changes to protected evidence. Final links/whitespace and protected hashes pass.
- Final saved-center-frame 03 guards unsupported flags and site/component body
  disagreement, reproducing the run 02 selected outputs byte-for-byte. The full
  suite again passes 121 tests. Final review rehashes all 5265 observer files and
  the separate imported executable as well as the 41 protected baseline files.
