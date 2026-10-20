# Nominal coverage: explicit method and completeness

[Answer](report.md), [native producers/consumers](native.md), [actual cases](saves.md).
The result is the union of **base BIOM identities with positive two-dimensional
area in the ordinary nominal horizontal disk**. It is not full placement
admission or a continuous latitude/longitude reconstruction.

## Inputs and common frame

Require the build/data/map identities, qualified PNDT/system/body association,
ordinary beacon/Workshop reference, saved frame and source/site base, compensated
local center `C`, and effective radius definition. Ordinary installed beacon
`002c60e9` supplies radius 150 through OutpostBuildAreaRadius; different
overrides or descriptor modes must supply their own inputs or return UNKNOWN.
L3's native radius mode is horizontal `dx²+dy²<=R²` with a separate upper-Z
condition, not a sphere ([L3 native proof](../spatial-placement/native.md)).
For this nominal geographic question use the horizontal disk before height,
POI and object-specific restrictions.

Join the ordinary framed beacon's parent to the typed world component and its
system/body pair; resolve that pair against installed PNDT GNAM. Join the
secondary world to its generated descriptor. Decode the packed source key,
including chart/tag and the tags-2/3 axis reflection, under the existing
[v2 contract](../position-resumption/algorithm.md). Preserve every ID domain.
For qualified frame 0b use that native descriptor origin; for qualified frame
2b use the separately established site cell. Do not infer a frame from which
origin gives an expected biome. Recover `C` through the native compensated-center
rule, preserving raw XYZ on the all-zero delta branch. All 14 selected rows
have explicit zero compensation. Retain Z/frame/provenance even though this
base-biome lookup consumes XY only.

The common plane is the qualified local reference/Workshop plane, with integer
terrain offsets mapped to the body's native hierarchy. For each integer
`q=(qx,qy)`, native `14096f5c0` supplies a unique destination address. In an
interior chart this is base plus q; normalize seams before choosing the raster
face. Negative coordinates use floor, never truncation. Exact continuous
longitude/latitude and planet-radius metre conversion are unnecessary.

## Spatial atoms and exact membership

The mapped native consumers use `Q(x)=floor(f32(x*f32(.01)))` for their binary32
input coordinate. The familiar cell rectangle `[100*q,100*(q+1))` is a useful
geometric approximation, but binary32 multiplication can move its boundary.
Use the actual quantizer preimages when a boundary/tangency matters.

For an explicit continuous computational model, round a real local coordinate
to binary32 first, then use the mapped multiply/floor. Define `L(q)` as the
boundary between the largest input float with `Q<q` and its immediate successor
with `Q>=q`: it is their exact dyadic midpoint. A monotonic binary search over
ordered float bits finds the adjacent pair. Qualify finite range, rounding and
underflow behavior rather than assuming arbitrary floating-point environments.
Tie ownership changes only zero-area endpoints. The spatial atom for q is:

```text
Aq = [L(qx), L(qx+1)) × [L(qy), L(qy+1))
dx = max(L(qx)-Cx, 0, Cx-L(qx+1))
dy = max(L(qy)-Cy, 0, Cy-L(qy+1))
positive_area_overlap = dx² + dy² < R²
```

Use exact rational/dyadic arithmetic for that test when inputs are dyadic.
Strict `<` excludes external tangency, including a tangent corner. Containment
and all positive caps pass. A rectangle wholly inside the disk passes without
crossing its circumference. The disk is the requested mathematical nominal
radius; this is not instruction-for-instruction equivalence to every rounding
operation in the engine's radial admission predicate.

`.local-work/b1-numeric.py` independently checks the 14 saved cases using this
interval construction and exact `Fraction` distances. All cell lists agree
with the simpler 100-unit calculation. Maximum examined boundary displacement
is 0.0001220703125 local units; the smallest cell-to-tangency margin in the
seven actual sites is 0.5224901613. It also checks exact tangency and dyadic
positive-cap/negative-gap counterexamples. This surrogate assumes round to
nearest and gradual underflow near zero. Historical MXCSR FTZ/DAZ is unmeasured;
the subnormal neighborhood is not certified hardware behavior and cannot alter
these selected cell lists given their margins. `numeric-r2.json` corrects the
earlier receipt's overly narrow normal-domain wording, preserving that receipt.

## Finite enumeration

1. Find every qx interval with positive-length intersection with
   `(Cx-R,Cx+R)` and every qy interval intersecting `(Cy-R,Cy+R)`.
   Monotonic `L` permits exact inverse/range lookup; conservatively include
   touching endpoint intervals and let the strict distance test remove them.
   The selected demonstrator brackets with ideal 100-unit indices plus one
   extra cell on each side, independently verified against the actual L bounds
   in its examined local range below 4,000 units.
2. Traverse their Cartesian product. Keep exactly the cells passing the
   rectangle/disk test. Never use only the beacon, corners or radial samples.
3. Transform each integer offset through the qualified native hierarchy and
   seam normalization. `14096f5c0` and the [v2 algorithm](../position-resumption/algorithm.md)
   wrap indices at N and toggle chart by XOR 1 for X, 3 for Y, 2 for both;
   preserve tags-2/3 reflection when selecting/repacking the resulting chart.
   Use the complete native transform for exceptional/corner cases rather than
   clamping an out-of-range index into the old face. The actual demonstrator
   rejects seam-crossing cells; no seam footprint was validated here.
4. Form the **cell center** `u=(I+.5)/N-.5`, `v=(J+.5)/N-.5`.
   For tags 2/3 negate both and select face 0/1 respectively. For tags 0/1
   retain coordinates and face. Apply `1423390f0`'s clamped, Y-reversed
   row-major raster indexing, read the uint32 and resolve it as a BIOM under
   its owner/load-order context. Require complete ready map/valid identities;
   report UNKNOWN for unavailable essential operands instead of an empty set.
5. Deduplicate resolved, plugin-qualified BIOM identities. Keep the cell
   witnesses, source offsets and any unresolved candidates beside the set.

For the three 256×256 maps and N=49152, interior tags 0/1 simplify exactly to
`column=I//192`, `row=255-J//192`. The independent direct map-byte check agrees
with the normalized-double lookup for every selected cell. One map pixel is
therefore a 192×192 group of query cells in these interior charts. A global
BIOM region is a union of such labelled cells, potentially disconnected; it is
not inferred from biome catalogue order, terrain style or resource boundaries.

## Completeness argument and explicit boundaries

Within a qualified ordinary chart/frame, quantizer intervals partition the
local plane except shared measure-zero edges. The native lookup uses only
their Int2 address, hence its base BIOM label is constant on each atom.
The bounding intervals include every atom that could meet the disk. The exact
strict distance test selects precisely those with nonzero-area intersection.
Taking their label union therefore returns every qualifying base identity,
including a wholly enclosed component. A finite union of zero-area contacts
does not qualify. Large connected-region polygon recovery is unnecessary.

The coarse raster makes a small enclosed single-pixel island unlikely for
radius 150 in these interior examples, but the algorithm does not rely on
that size relationship. A synthetic enclosed 100-unit cell with its own label
has all four corners strictly inside the disk; circumference-only discovery
would miss it, while this traversal includes it. No such synthetic patch is
reported as an actual installed biome island.

This proves representational coverage, conditional on source/frame/map validity.
It does not establish every historical restored frame, arbitrary special-world
overrides, every numeric environment, polar/corner equivalence, terrain shading
or exclusion geometry. Failed map readiness/type resolution and unsupported
seams are material UNKNOWN states, not evidence of absent biomes. The scoped
interior result is useful without resolving those separate capabilities.
