# Frozen spatial prediction contract

Version `sor-rg2a-prediction/1`, method `rg2a-points/1`.
[Freeze and hashes](freeze-v1.json), [machine predictions](predictions-v1.json),
[points](points-v1.csv), [source pins](sources.csv).
No live answers were used. Preserve v1; any correction creates a new version,
reason and reviewer record before observation. Never fit a prediction to RG2-B.

## Qualified Kreet inputs and geometric products

The accepted [RG1 evaluator contract](../resource-geometry/evaluator.md) controls
generation, ordering, native-bound competition, halo and supported source types.
P1/R1 chart 1 source origin is `(10464,21120)`, P2 chart 0 `(14304,12768)`.
Exact local XYZ, saved frame, body and Workshop identifiers are in [cases.csv](cases.csv).
All are 0b, zero compensation. Body PNDT `0x0003f59f`, owner suffix `259487`
is the **scoped earlier Kreet observation**, not a general PNDT identity rule.
Resources include Iron `0x000057c7`, Alkanes `0x000057c9`, Lead `0x000057c1`
and Silver `0x000057c3`; source receipts control exact selected order and weights.

| Case | Sources / resource-cell calls / retained paths | Nominal 150-unit circle |
|---|---|---|
| P1 | 6 / 2592 / 766 | Iron intersects, Alkanes absent in modeled bounded regions |
| P2 | 4 / 1152 / 123 | Lead and Silver do not intersect; both occur nearby |
| R1 | 4 / 2016 / 589 | Iron intersects, Alkanes absent in modeled bounded regions |

The local full RG1 JSONs retain **all whole sources**, path starts beyond the
circle, prior different-resource competition and complete cell/key inputs.
These source receipts, source-definition derivative, installed-map bytes,
planet-selection inputs and current evaluator files are hash-indexed, not bulk
copied into Git. They inherit RG1's finite halo for the ±300 lattice, greater
than the new query segment's extent. No source regeneration or source selection
was fitted to a UI list or current extractor. RG2-A adds point selection, not a
new generator or mature owner-key assumption.

`bounded_region` columns are RG1's native-sphere-clipped disks/max-width-rectangle
product; `tapered_strips` are its separate area-strip product with explicit
single-point disk convention. They are **not equivalent**. P1 edge−5/−1 and
R1's positive center distinguish them; P2 edge−1 does too. Neither column is a
qualified prediction of scanner pixels/raster or full extractor admission.
Those are predeclared alternative correspondence hypotheses, with UNKNOWN where
an interface does not expose the same quantity. Resource-name agreement alone
does not satisfy geometry validation.

The deterministic selector chooses the nearest occupied and empty points of
RG1's predeclared fixed lattice (distance then XY order), chooses the first
resource in the occupied set and bisects opposite labels 30 times. This brackets
a local crossing on that segment; it does not prove there is only one crossing.
It then evaluates the actual aggregate at offsets −5,−1,+1,+5 along the segment.
Signs indicate movement from occupied toward empty, **not universal edge-normal
distance**. The original lattice points are the broad positive/negative controls.
Near samples are nominally one unit from the local bracket; native rounding and
other boundary arrangements remain separate. Every sample records all resources
under both products, and whether it lies inside the nominal circle.

Maps [P1](map-p1-v1.svg), [P2](map-p2-v1.svg), [R1](map-r1-v1.svg) show clipped
centerlines, samples and the circle. They are orientation aids, **not filled
width contours**. The tables carry the classifications; complete widths and
native bounds remain in pinned local receipts. SVG viewport clipping changes
display only and never removes source operands from calculation.

## Position, tolerance and vertical qualification

For qualified Kreet 0b coordinates, operator target is `beacon live XY + (dx,dy)`
from points-v1.csv **only after** independently confirming a common live parent,
axes, scale and beacon-center association. Model fine cell is origin plus
`floor(f32(local XY * .01))`, chart retained. This is a terrain-cell address,
not global latitude/longitude or an asserted metre scale. Do not assume compass
north is +Y. No teleportation, setpos, rotation, reference/memory mutation or
console execution is authorized by RG2-A.

Prospective read-only console `getpos x/y/z` has prior user-transcribed support
in [Save29](../power/save29-test-plan.md#subsequent-user-console-identity-evidence),
not a newly instrumented validation. If approved for RG2-B, first demonstrate
selected-beacon and player coordinates, then a small reversible walking motion
to establish axes; capture actual text and selected reference. Otherwise use
another independently measured position interface or classify location UNKNOWN.
Player feet and aimed scanner patch are distinct points: capture reticle/ground
projection and its uncertainty; player XYZ alone cannot qualify an aimed patch.

Proposed XY positioning tolerance is **0.25 native unit** per target. This is a
prospective engineering acceptance gate, not demonstrated manual accuracy or a
proof of geometric clearance. RG1 alternate arithmetic's 0.01 comparison tolerance
is not a universal native boundary error bound. Near-edge comparisons are
INDETERMINATE if position, aim/footprint or model margin exceeds the gate; broad
controls can still be useful. Estimate actual boundary intervals from continuous
walk scans and repeated approaches from both sides, retaining measurement error.
Never treat an approximate screen cursor as a sub-unit position instrument.

Generated path Z=0 is an operand domain, not terrain height. Record actual player,
selected beacon and queried patch Z, slope and loaded terrain. Native area
admission also has radius/upper and 3D branches. Projecting XY does not qualify
those branches or require the player to occupy model Z=0. Missing terrain/upper
conditions block semantic equality, not the retention of a visible observation.
Nominal radius 150 is separate from POI-clipped usable build territory and the
36-segment displayed outline. Test and record exclusions independently.

## Mature alternatives actually examined

Read-only diagnostics in `.local-work/resource-geometry-live-prep/` are pinned
in sources.csv. They use the exact HIST-0267 typed world/descriptor receipts,
not a filename search or same-planet approximation.

| Site | Parent→secondary; descriptor origin vs nominal site | Concrete result and blocker |
|---|---|---|
| P3 Feynman mixed | `84ec80→817a70`, decompressed world offset 1343498; descriptor offset 5076/key `02a38a287ec06240`, chart 0 `(25152,32448)` vs site `(25124,32446)` | Candidate plane translation `(-2800,-200)` native units. Site-as-origin counterfactual resolves four base sources, each mask `[8]`; it does not qualify the generator's selected owner frame or manager suffix. |
| P4 Carinae single | `84655c→818832`, world offset 1341648; descriptor offset 4416/key `039a0a403d2053a0`, chart 0 `(21408,15648)` vs site `(21399,15640)` | Candidate translation `(-900,-800)`. Four counterfactual sources each mask `[4]`. Both spatial representations are available, but the site is not thereby the generator frame. |
| R2 Feynman other | `859b49→817855`, world offset 1345977; descriptor offset 4386/key `02a38a2851c092a0`, `(37536,20928)` equals site | Four counterfactual sources have masks `[0,3]`; first-query chance weighting cannot use RG1's uniform-mask shortcut. Coincident origins remove one ambiguity, not unknown owner suffix/effective family inputs. |

All offsets above are **decompressed-stream byte offsets** in the pinned Save52
derivative; descriptor keys are packed saved identities, not source pointers.
`mature-alternatives.json` retains full joins and translation arithmetic;
`mature-diagnostics.json` retains counterfactual sources, map/pattern context and
mask checks. They are explicitly **unqualified** and never output vein predictions.
The diagnostic source catalog/registry is the same pinned installed main-file
derivative used by RG1. Other same-body descriptors exist; joining by body alone
would silently choose the wrong local origin.

The existing PNDT INAM payloads expose Feynman atmosphere-reference prefix
`0x0000c19b` and Carinae prefix `0x000096df`; the complete raw fields are local.
An atmosphere definition reference is not a captured effective atmosphere or
qualified CTPerBiomeData selection. RG1 planet-context01.json's non-Kreet rows
explicitly say NOT_SUPPLIED_EXPLORATORY. Reusing them unchanged, substituting
PNDT as manager+0x80, or translating only final generated points would invent
inputs: owner suffix and source-native origin affect CRC **before generation**.
R2's nonuniform masks additionally require the actual weighting/cache query.

Existing [saved-position 2b](../position-resumption/algorithm.md) and
[native source frame](../resource-geometry/native.md) support different scoped
operations. A correct nominal BIOM result is not a proof of resource-frame
identity. The examined alternatives are (1) saved site origin, (2) exact joined
descriptor origin with translated center, (3) independent same-body site with
coincident bases, (4) existing planetary-selection receipt and PNDT atmosphere
reference, and (5) archived capture coverage from RG1-V06/V07. None supplies a
qualified mature manager suffix/frame/selection epoch. Archived records do not
contain complete matching source/region arrays; no new failed search is presented
as proof those operands can never be recovered offline.

**Smallest remaining qualification:** establish each mature generator's owner
suffix, source/Workshop transform and effective per-biome family/atmosphere inputs
from an exact existing native/serialized source path or a separately approved
coherent observation. For R2 also resolve actual mask-weight position. This is
an evidenced input boundary, not authority to start an engine-wide campaign or
reuse a NO-GO observer. Until then mature vein samples/edges are UNKNOWN.

For a separately approved *biome-only* control at P3, saved-plane points
`(83.460693359375,190)` and `(83.460693359375,210)` lie on opposite sides of
the nominal row boundary at Y≈200 and inside radius 150 (offsets +122.112289
and +142.112289 from the beacon). Earlier biome quantizer rules govern rounding.
P4's center and ±100-axis points remain nominal HillsNoLife08. These are
preparatory biome controls, **not vein geometry predictions**; they cannot close
the RG2-B vein comparison requirement.
