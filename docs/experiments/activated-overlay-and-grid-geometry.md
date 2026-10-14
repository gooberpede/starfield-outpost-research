# SOR-EXP-0019 — Activated overlays and planetary grid geometry

2026-10-10, Australia/Sydney. Authorized by the user invoking the retained
[brief](../implementation-briefs/CODEX_BRIEF_SOR_activated_overlay_and_planetary_grid_geometry.md).
SOR-EV-0027. **Strong partial, REVIEW-REQUIRED.** The supported durable location is
the resolved body, saved discrete site anchor, qualified local frame and compensated
workshop XYZ. Exact continuous center longitude/latitude remains unestablished.

The new result closes several concrete stages: activation computes integer shifts
from active/requested angular pairs; the typed overlay payload carries those shifts,
bounds and height; a terrain-manager writer rebases shifts and bounds together.
All nine existing captures contain an active pair projecting to the independently
observed origin `(10464,21120)`. The two controlled site displacements are `(1,2)`
and `(3,24)`. This is a demonstrated frame-construction mechanism, not a fitted
offset. It does not identify the actual selected edge for every serialized parent.

The grid has `49152` fine **cells per hemisphere-square axis**, designated by their
centers. A half-cell offset is explicit in two native forward paths. Landing-origin
snapping is a separate 96-fine-step operation. Installed SFBK data and the native
pattern remapper demonstrate actual 2×2 subdivision footprints; neither those
footprints nor the saved site's cell is synonymous with the traversable landing
area or a visually recognizable terrain tile.

Confidence: exact sampled bytes/arithmetic PROVEN; native paths STATIC; their
scoped frame/grid semantics STRONG interpretation proposed. Coverage: pinned build,
23 archived saves/128 selected prefixes, nine prior non-atomic snapshots, 41 angular
rows, installed Starfield.esm and the exported paths below. Completeness: neither
universal serialized-frame reconstruction nor continuous geographical embedding.
Authored evidence REVIEW-REQUIRED; raw saves/native exports/captures LOCAL-ONLY.

## Bounded experiment plan

Question: which restored/activated frame positions the saved compensated workshop
center, and what geometrical reference does the planetary lattice designate?

Allowed actions: read/hash pinned installed native/content inputs, verified local
save archives and nine existing observer captures; export existing Ghidra state
with `-readOnly -noanalysis`; run project readers and original stdlib probes;
consult the two cited community discussions; write original research and review
artifacts. No launch, debugger, deployment, save/configuration/database mutation,
native invocation, outside code incorporation, external communication, staging,
commit or push. Source hashes and 40,000,000,000-byte C:/D: guards apply.

Development cases: Save25/26 and S1. Held-out checks: S1C, mature Save52's 17 direct
site associations and three fixed cities; existing prior knowledge makes these
replications rather than blind discoveries. Save52's 19 beacons were not moved
(user-confirmed); zero compensation is not explained by hypothetical resets.

Outputs: fresh ignored `.local-work/activated-grid/` receipts and
`.local-work/recon/activated-grid-*.tsv`; selected authored tables, original
scripts and reports. Inputs remain immutable. Temporary decoder mappings use
existing context-manager cleanup. Stop affected work on source mismatch,
uncontrolled output, disk guard, ambiguous essential grammar or tool failure;
preserve partial failures. Wrong native type, numerical overfitting and confusing
saved site anchors with actual centers are principal scientific risks.

Success: predict the durable center's planetary position independently of beacon
relocation without fitted per-site constants. Strong partial: close demonstrated
frame/grid stages and localize remaining terms to exact producers/consumers.
Falsification: changed compensated center, inconsistent held-out frame prediction,
or discrete-only results presented as continuous ground truth. Counterexamples
and prior interpretations are retained. Review/publication gates remain separate.

## Supported planetary-position model

Keep seven quantities separate: resolved PNDT/body; saved site angles; activated
frame; compensated local center; current beacon XYZ; other references' own
transforms; any derived continuous surface point. Body identity comes from qualified
reference/PNDT associations, never from names. The Save52 manual network is a
previously independent identity cross-check, not a positional-formula input.

Within the tested Workshop lifecycle, `C = float32(P + delta)`, componentwise.
Case-5 saved beacon XYZ `P` and Workshop type 0xBC `+0x60` compensation `delta` are
persisted separately. Their typed serialization/consumers remain supported by
[EXP0017](workshop-origin-beacon-relocation-persistence.md) and freshly replicated
[EXP0018 tooling](durable-outpost-center-and-object-transforms.md). This run does
not change their earlier critical-review status.

| Case | Durable center XYZ, native units | Site `(tag,I,J)` | Quantized displacement; XY residual |
|---|---|---|---|
| SOR-002 Save25/26 | `(122.70045471191406,273.0462341308594,18.352506637573242)` | `(1,10465,21122)` | `(1,2)`; `(22.700454711914062,73.04623413085938)` |
| SOR-003 Save25/26 | `(356.8204040527344,2459.05859375,-31.89084243774414)` | `(1,10467,21144)` | `(3,24)`; `(56.820404052734375,59.05859375)` |

The two SOR-003 center byte strings are both `0369b243f0b019457220ffc1`, despite
the moved beacon's changed XYZ and nonzero compensation. SOR-002 is
`a266f542eb858843efd19241` in both. Identity 98 values are respectively
`0efca066ee4c7b9b` and `f1517de43e171745`; parents change across saves and are not
interchangeable with these identifiers or FormIDs. Exact decoded offsets and
parent tokens are retained in [invariance.csv](activated-grid/invariance.csv).

For a **qualified active frame**, the studied angle consumer uses
`qXY = floor(float32(CXY * float32(.01)))`, integer-offsets the effective terrain
origin with seam handling, and projects the resulting cell center. Residual
`CXY - 100*qXY` remains a separate local quantity. Other-world/cached-angle and
initial-data branches must first select/convert the frame; applying this formula
directly to every saved XYZ is falsified by the mature negative-X case below.
The stored site pair is a useful discrete geographic anchor. It is not a verified
continuous angle pair for either the beacon or the durable center.

## Activated-overlay reconstruction map

All addresses here are **static VAs**, Starfield 1.16.244.0, preferred base
`0x140000000`; RVA = VA minus that base. Offsets are members of the specified
type, not file offsets or universal object labels. Full instruction/decompiler
evidence stays in ignored `activated-grid-01` through `12` exports. The selected
[native map](activated-grid/native-map.csv) gives exact evidence locators.

| Stage / ownership | Concrete evidence | Result and boundary |
|---|---|---|
| Definition component | `1404595c0`, named `BGSWorldSpaceOverlay_Component`, key `1461dd7ec`; loader `1404597a0` | BNAM → tagged reference at component+8; PNAM → +1c; SNAM → +18. These are ESM component reads, not ActivatedOverlayProperty save records. |
| Resolve definition | `140459a30 -> 14045a2d0` | BNAM remapping/resolution requires form type 0xb3, BGSSurface::Block (SFBK). Bounds use its +40/+44 dimensions. This corrects a tempting Pattern-type attribution: SFPT is type 0xb5. |
| Body/world association | `140ad3c30`, `140adbc50` | Component+18/+1c feed `142332d90`; PlanetWorldSpaceData is searched by world ID for the associated pair. World/body keys are not Workshop IDs. |
| Active/requested pair → shift | `1407986d0` | Mode 3 chooses terrain+1a8, otherwise+b0. Both active and requested pairs pass `14096eb90`; `14096f940` differences their integer grids. Source world comes from terrain+78 chain/+98; `140ad30a0` may select an existing overlay. If requested equals selected world, activation is skipped; linked overlay world can be unwrapped before activation. |
| Construct or reuse overlay | `140ad1660`, collision `140ad0fb0` | Distinguishes matching identity/force conditions from occupied inclusive-bounds overlap; existing world/component and generated-overlay paths differ. Both converge on typed payload initialization and registration, not one unconditional translation rule. |
| Initialize payload | `140ad47e0`, `140ad4a00`, `140accd30` | ActivatedOverlayProperty: world pointer+0; int32 shifts+8/+c; inclusive bounds+10..1c; angle doubles+20/+28; float height+30; flags+34/+35. Definition component and expanded bounds feed this construction. `140694f80` handles related navigation remapping when bounds exist. |
| Height | `140acf480`, called by `140ad1660` | Terrain-sampling path supplies vertical term. It is not a continuous center lon/lat calculation or a universal persisted altitude. |
| Registration | `140adcde0 -> 140add2e0 -> 140adccf0 -> 140add310`; `140ad7330 -> 140ad7b80`; typed copy `140adcfd0` | Named ActivatedOverlayProperty key `145eaac2c`, manager+268 component store and +300 keyed edges. Immediate/deferred command conditions exist. Copying a typed payload is not wire deserialization. |
| Factory evidence | `141881660` registration at `141881f98`, vtable `144b91788`, RTTI `145a62070`, factory pointer `14590a3f0` | Name Overlay, type key, null fifth descriptor; methods `14036cca0` empty iterator, `1402b75f0` false, create `140ad7330`. Inspected factory supplies no demonstrated wire reader. Null descriptor/no-op does **not** prove the state is never persisted elsewhere; generic/custom serializer closure remains open. |
| Deferred selection/update | `140ad9810`, `140ad1d30`, `140ad4fa0` | Processes queued key pairs (global 145ead238..240), copies selected edge state and updates flags/cell context conditionally. Not a raw-save pointer map. |
| Invalidation | `140ad94a0 -> 140ad11c0` | Invalidating/updating selected-world context is separate from registration. Actual post-load flag values are not captured by this run. |
| Rebase writer | `140797dc0 -> 140ad9cd0` | Caller reads terrain+1ec/+1f0. Callee subtracts this integer displacement from payload shifts **and all four bounds** on relevant manager+300 edges, then caller continues terrain update. A translation reconstructed before this operation is stale afterward. |
| Select/read effective translation | `140ad30a0`, `140ada3a0` | World-keyed inclusive bounds and invalid flags select edges. Reader requires payload+35 clear, emits `(100*shiftX,100*shiftY,height)`. Edge+20 is payload origin; edge+55 is thus payload+35, not a second unrelated flag. |
| Saved reference XYZ | prior `141856d10`, save callers `14181aa30/14181af40`, loader initial-case branches | Conditional initial-data0x20/frame conversion subtracts/adds selected translation. Own XYZ/rotation and Workshop compensation are distinct. Full wire→world-key→edge choice for each archive is not yet a qualified decoder. |
| Grid/angle and residual consumers | `14078d1f0 -> 14078d660 -> 142332410`; `14077fc20`, `14077fbc0 -> 14077f900` | First path quantizes XY/ignores Z. Second retains residual and uses integer-grid differences/cell selection. Inspected consumers do not establish continuous spherical residual embedding. |

**Restoration judgment:** save-resident reference XYZ, compensation and site/body
association are demonstrated in the sampled grammar. Definition bounds are
ESM-derived. Activation shift/height/bounds and manager rebasing have concrete
runtime constructors/writers. The factory inspection narrows the hypothesized
direct wire-restoration route but neither closes a generic serializer nor proves
absence. The actual selected edge, validity and rebase epoch are missing for the
unqualified saved frames. This is a specific missing join, not an unidentified
“overlay offset.”

## Grid geometry and topology

`B = block + merge = 10+2 = 12`, `R=256`, `N=16*B*R=49152` in pinned
settings/captured grid. Hierarchical index is `I=192*coarse +12*sub +fine`, with
coarse 0..255, sub0..15, fine 0..11. Native coordinate struct members are tag+0,
coarseXY+4/+8, subXY+14/+18, fineXY+24/+28. Intervening resolved record/flag
members are not extra coordinate levels. Each axis has N cells and N designated
center samples; an abstract closed square has N+1 boundaries. This is not a
49152-face planet or a six-face cube map.

`14096ecb0` projects angles into a hemisphere square and uses nested floor/fmod
decomposition. Its upper normalized clamp is `1 - 1/(B*N)`, **not** exactly
`1-1/N`; at B12 both lie in the final fine interval. The previous project's
uniform mathematical quantizer is not a bit-exact boundary implementation. No
claim that all floating edge ties match Python is made.

`14096f4d0` and `14078d660` reconstruct normalized square coordinates as
`u=(I+.5)/N-.5`, `v=(J+.5)/N-.5`, then use the nonlinear hemisphere projection.
Thus the **cell-center hypothesis is supported for designated angular outputs**;
corner/lattice-boundary hypotheses are rejected for those outputs. This does not
establish that local terrain XYZ zero is that center, or determine how a fractional
XYZ should extend it. Saved angular pairs reproduce these designated outputs;
inverse-square residuals are nonzero at mixed-float precision, not evidence of a
physical displacement from the center.

Canonical angle encoding emits north tag 0 / south tag 1. Tags 2/3 occur in seam
operations; the projection reverses X for 1/2, Y for 2/3, and uses northern Z for 0/2.
`14096eb90` maps tag 2→canonical 1 and tag 3→canonical 0 while reversing both **coarse**
indices for record lookup. Fine/sub coordinates and lookup orientation are separate
from this canonicalization. Do not conflate these tags with a pattern rotation.

`14096f5c0` first takes signed C remainder of each displacement by N, adds it to
the hierarchical index, wraps a crossing once, then changes tag. For X-only
crossing tag XOR1, Y-only XOR3, both XOR2, regardless of crossing sign. Whole-N
displacements are discarded by this procedure. It is a particular indexed seam
operation, not ordinary longitude modulo or a globally flat periodic torus.
`14096f940` chooses seam-aware differences when tags differ. No globally uniform
surface-distance metric follows from these integer differences.

Analytically, square `(0,0)` maps to a pole, the square perimeter to the equator.
With even N the exact pole is between designated cell centers, so no fine-cell
center is exactly polar. Longitude at an exact pole is not a unique physical
direction. Boundary/pole/roundtrip tests below are mathematical tests of the
source-informed model, **not runtime polar/seam observations**. Native seam and
lookup branches support topology; a full rendered-terrain seam continuity audit
was not performed.

`14096efb0` clears fine indices and snaps sub0..3→0, sub4..11→8, sub12..15→next
coarse/sub0, with final-coarse seam handling. Therefore adjacent landing-origin
snap positions are `8*B=96` fine steps apart. The 16 subdivisions span 192 steps
per coarse index. Neither 96 nor 192 is automatically a visual tile width. The
studied local conversion uses 100 **native position units** per fine step; physical
metres, body-dependent metric and surface-distance errors remain ungrounded.

## Tiling lead register

| Lead | Direct result | Limits |
|---|---|---|
| Block dimensions | `14096ae90` reads SFBK DNAM's8 bytes directly into Block+40/+44. Native type 0xb3/RTTI Block agrees with overlay resolver. [Dimension table](activated-grid/block-dimensions.csv):1753 records, 14 distinct dimension pairs. | All installed base-ESM pairs square; no universal permitted-size list inferred. Zero/undersized records are not positive footprints. |
| Actual multi-subdivision blocks | `14096bba0` uses `(dimensionX-merge)/B`, separately Y, for bit 8-marked 16×16 SFPT placements. DNAM14→1 subdivision; 26→2; 100→8 under B12/merge 2. [Actual placements](activated-grid/pattern-positive-spans.csv) join explicit FNAM FormIDs/GNAM flags to SFBK. | These are pattern subdivision spans, not guaranteed visual repeated features or 100-unit fine cells. 3×3 and non-square1×2/2×4 actual blocks are not observed here. No absence claim for other plugins/builds/asset contents. |
| Rotation/reflection | `140851d20`, matrix table staticVA 145907c10, byte>>5 selects 8 centered integer 2×2 matrices. `14096be70` selects remapped cache+850 versus original+38; `14096bba0` moves footprint corners and copies span entries. | Remapping gated by 145e91df8 and orientation byte≥32. Eight square permutations are verified; no loaded orientation selection was observed. Axis-independent code is capacity evidence, not proof of deployed non-square blocks. |
| Overlay extent | `140accc10`: `[-dimX/2,(dimX-1)/2]` and analogous Y, optionally union component+24..30 then add displacement. | Inclusive integer coverage bounds; not the ordinary Workshop circle, not a visual terrain-tile boundary. |
| Community 2×2 / repetition | SOR-S-0131 supplied Reddit threads, retried 2026-10-10, both fetches unavailable. Original authors/text not recovered; brief supplies the larger 2×2-looking observation as a lead. | Full requested reading uncompleted and disclosed; no authenticated quote/specification. Engine data independently supports multi-subdivision spans, not identity with the reported pictured feature. |

The native orientation matrices are `(1,0,0,1)`, `(0,-1,1,0)`, `(-1,0,0,-1)`,
`(0,1,-1,0)`, `(1,0,0,-1)`, `(0,1,1,0)`, `(-1,0,0,1)`, `(0,-1,-1,0)`.
They transform centered indices in a 16×16 pattern; reflections and quarter turns
are explicit. The selected table is independently extracted from the pinned PE,
not inferred from terrain screenshots. No raw asset or decompiler text is copied.

## Existing-case validation and counterexamples

Fresh receipts: `.local-work/durable-center/activated-grid-01/`,
`.local-work/workshop-origin/activated-grid-01/`,
`.local-work/activated-grid/corpus-audit/` and `geometry-03/`.
The prior session's5265 files were verified before selected capture rereads.
The installed scan finds 53165 positive-span flagged slots: 48960 with 1×1 spans,
4205 with 2×2 spans. The retained 16 placement rows are deterministic examples
(first eight distinct pattern/block joins per span), not the full slot dump.
The 100×100 block yields an 8×8 arithmetic span but is not observed among those
positive-span SFPT placements; it does not verify an 8×8 visible terrain array.

| Check | Actual result | Scientific reach |
|---|---|---|
| Save25/26 SOR-003 | Compensated center bit-identical, zero component error; site pair unchanged. SOR-002 likewise invariant. | Move remains within the same 100-unit cell even without compensation. Site invariance alone is insufficient; typed center consumer and exact vector recovery discriminate. |
| Nine snapshots | Active pair `(-0.221212926466995,-0.5112328034126492)` at mode 2+b0 in all 9; projects `(1,10464,21120)`. Pair reconstruction max error 1.6653345369377348e-16 rad; origin+c8 independently agrees. | Calls' requested shifts predict `(1,2)`/`(3,24)` without fitting. Does not observe the selected overlay edge payload or its activation event. Alternate+1a8 equals the same pair but mode 3 is not sampled. |
| S1/S1C | Same Kreet/SOR-002 site cell; zero compensation; control XYZ/rotation bytes unchanged. Seven full no-action pairs replicated. | Prior-known independent session replication, not a blind holdout. Residuals can differ with the same site pair. |
| Save52 | 17 direct documented site/body associations retained, 19 studied beacons all zero compensation; 53 storage+19 beacon+1 extractor prefixes decoded. | User confirms beacons unmoved. No reset/deletion explanation substituted. Manual JSON is identity comparison only. |
| Negative-X falsifier | Token 84ede9, body 0005E0DB, frame 0x2b, X=-53.4358024597168,Y=58.03339767456055, compensation 0; site `(13152,45120)`. Naive site-minus-floor infers Xorigin 13153, inconsistent with 96-snap13152. | Rejects universal site=current-local-cell/naive origin recovery; frame selection 0x2b differs from controlled0x0b. Not a compensation failure. |
| Save2/fixed cities | Save2 player-associated New Atlantis pair equals installed 0001251B pair; Akila/Cydonia retained. Total 41 angular rows max error 8.881784197001252e-16 lon, 3.3306690738754696e-16 lat rad. | Projection/association replication, not continuous outpost-center ground truth. Repeated rows are not 41 independent locations. |
| Other objects | Own case 5 XYZ/conditional rotation and seven unchanged controls replicated; same-parent versus frame-unqualified differences retained in [object table](activated-grid/object-transforms.csv). | No new attachment/snap transform composition, authoritative membership or generic frame alignment claimed. |

Two previously explicit unqualified SOR-003 continuous extensions still produce
`(-.21973838091541562,-.5116797847638825)` versus
`(-.21976066051647306,-.5116457946804763)` radians. Both use the same durable input
and remain move-invariant; neither is a validated geographic position. The
cell-center result resolves the **discrete output phase**, not the missing native
residual-to-surface embedding. A physical-distance error would invent units here.

## Exact remaining join and next step

The useful durable representation now is `(body, saved site cell/pair, saved
parent/world and frame discriminator, compensated local XYZ)`, plus effective
active-frame origin/translation **when independently qualified**. It preserves
the center and its discrete planetary neighborhood. The engine's studied public
angle consumer is many-to-one within each 100-unit XY interval; there is no evidence
here that it defines a unique continuous center angle. This does not prove the
engine lacks some other continuous geometric representation.

Two specific gaps remain. First, map a selected saved reference's initial-data
frame branch to the world-keyed edge and rebase epoch used by `140ada3a0`, including
validity+35 and height+30. The producer `1407986d0` and rebase writer `140797dc0`
are now known; a hypothesized directly serialized payload is not established.
Second, identify a consumer that combines the retained residual from `14077fc20`
with the projected cell/body geometry into a subcell global point; inspected
`14077fbc0/14077f900` and earlier `1407bcfb0` do not supply it.

Most decisive next evidence, **separate authorization required for acquisition**:
at one settled controlled Kreet checkpoint and the specific mature 0x2b case,
capture the actually selected world/cell/key and typed overlay payload,
terrain+b0/+1a8, +c8/+1c0 and +1ec/+1f0, initial-data discriminator, own saved versus
loaded reference XYZ, Workshop compensation and effective translation. This tests
the missing saved-frame join without movement/save creation. A bounded traced
caller or geometric consumer that receives nonzero XY residual is additionally
needed to decide continuous embedding; another quantized Starmap pair cannot do
so. Any breakpoint/hook would affect execution and needs its own finite live brief,
flush/exit/recovery terms and source-save protection. No such work occurred here.

## Provenance, reproduction and review

Pinned executable SHA-256
`7e9adb1414a8e1b325e5e1f097b9b17b78deb7eebeda37a333351a43a60f9d28`;
Starfield.esm `1dabed00c3f4282dd3bb54d2e9601e40b577d8742d078b7ccef203adbfef0da7`.
Save25 original `d4df86bc01c2105933fe856a1be5ebbe0c3fc78a4d67fe1a790e18129faf75f5`,
decoded `0c27c10c1f07d5a480da4f857072cafc17e198b981350e01de2fa6b09f972cfd`;
Save26 original `2b4781e75226f2ff7c6aa47470fb47ff179c1754461aa208c46716d7c3935104`,
decoded `bb07dd976e369349a602c40461a4017b51aed88b81cc0acc5483220d9fcb6160`.
All 23 source identities/decoded hashes stay in fresh receipts and selected
[decoded table](activated-grid/decoded-inputs.csv). Protected baseline was taken
**before** new native exports and matched prior EXP0018 identities. Final comparison
and limitations are in the [review package](activated-grid/README.md).

SOR-S-0127/0128 installed Bethesda native/content, SOR-S-0124 prior original project
readers/math, SOR-S-0132/EV0024 prior captures and separately installed
Ghidra 12.1.2/JDK 21/CPython standard library supply evidence/tools. The two Reddit
URLs are [tiling example](https://old.reddit.com/r/Starfield/comments/1vqcjk3/found_a_perfect_example_of_starfields_tiling/)
and [tile observations](https://old.reddit.com/r/NoSodiumStarfield/comments/1cr7w8t/obervations_on_starfields_tile_system/).
Consultation only; no outside implementation/assets, downloads, contacts, forks,
PRs or new permission basis. Credits and source/provenance extensions accompany
this report. Original tools are source-informed, not claimed clean-room work.

Twelve Ghidra exports used existing state with `-readOnly -noanalysis`, Xmx2G,
30-second decompiler timeout, 600-instruction windows and 50k decompiler-character
caps (explicit full 141881660250k). Reference inventories cap 4096 where refall,
ordinary queries24. Existing-analysis xrefs and bounded exports do not prove
whole-executable writer/serializer coverage. Selected mathematical tests execute
no native code. Full commands, hashes, checks and diff locations are retained in
the review package. No live work, staging, commit, push or publication.
