# Evaluator contract and nominal intersection

Project-original GPL-3.0-or-later. [Native lineage](native.md), [pins](sources.csv),
[validation](validation.md). No third-party implementation/dependency is incorporated.

| Source | Reads, writes, prerequisites and effect |
|---|---|
| [geometry.py](../../../research/resource-geometry/geometry.py) | Pure calculations; imports owned CRC/strip arithmetic from save-analysis/scripts. No target/file writes. Stdlib only. |
| [context.py](../../../research/resource-geometry/context.py) | Pure parsing/calculation over caller-owned bytes/definitions; no file/process operations. Returns ordinary map/pattern/source/halo/key operands, or raises ValueError for unsupported context. |
| [qualify_sites.py](../../../research/resource-geometry/qualify_sites.py) | Bounded Kreet qualification driver. Reads named ignored installed-definition, BIOM-map, planetary-selection and prior saved-frame receipts, existing constant receipt and fresh EXE; validates constant bytes/EXE and pre/post input pins. Writes exclusive --output JSON beneath .local-work only. No save decode/mutation, target execution or DB access. Requires those prior qualified local derivatives. |
| [reference_check.py](../../../research/resource-geometry/reference_check.py) | Reads a qualified receipt and owned sibling explicit MT module. Independently regenerates with double/libm/distance geometry; exclusively writes ignored --output. No primary geometry/context import or target effects. |
| [analyze.py](../../../research/resource-geometry/analyze.py) | Earlier actual-definition/synthetic-context control. Fresh EXE/ESM walk, exclusive JSON; not a site assignment. |
| [test_geometry.py](../../../research/resource-geometry/test_geometry.py), [test_context.py](../../../research/resource-geometry/test_context.py) | Synthetic stdlib tests, no proprietary fixtures or target activity. |

## Context contract

The source entry needs a qualified chart/geographic fine-cell origin and beacon
local XY, body/system identity, registered SFPT order, BIOM values/masks and styles,
SFBK dimensions, selected per-biome family/RSGD and owner suffix. A true context
flag is a caller assertion, not evidence. The driver consumes fresh installed
derivatives and existing SAVE-qualified 0b frames; it does not infer hidden mutable
state from a beacon name or a runtime pointer from a saved token.

Qualified baseline: 256×256 map faces, interior chart 0/1, main Starfield.esm
registration order and native defaults: surface seed 0x20201215, whole-pattern
random rotation disabled, block orientation enabled, block size 10/merge zone 2.
SFPT style candidates retain registry order. The surface CRC folds LE body-index,
system and surface seed; each multi-choice map pixel consumes one MT probability.
Map raster row inversion and SFPT column-major indexing are explicit. An anchor
slot is recovered before deriving a source; nonanchor back-links are not new blocks.

Source dimensions subtract twice grid padding from raw SFBK dimensions. Generator
origin is 100×(source local anchor−padding), in native units. The native seed helper
adds that origin to the integer cell before geographic translation: **no /100
correction** is applied. The saved geographic descriptor and native seed packed
u64 are different domains. Unsupported seams, missing definitions/keys, invalid
domains or unqualified selection stop the affected evaluation rather than invent
an operand. Current Kreet owner 259487 is supported by earlier Kreet captures;
the same numeric value as PNDT is not promoted to a general body mapping rule.

Planetary family selection uses maintainer-owned reproducer code under SOR-P-0002,
fed fresh installed definitions rather than its catalogue CSVs. Its exact source
pins and complete selection receipts remain local. These are component predictions,
not a newly observed loaded CTPerBiomeData. For these Kreet sources there is one
main family, no selected Special or Everywhere branch, and unique descending
rarities. The selected root DNAM is shared by its descendants; each uses block
40×(rarity+7). Uniform source-neighborhood masks establish chance-weight independence
from first-cache-query position in these cases. Other contexts must resolve those
dependencies, not assume them away.

## Generation and spatial products

`generate_cell` consumes explicit source/resource/provenance, packed u64 key, owner
u32 suffix, Int2 cell/native origin, clip center/half-extents, ten-float block,
weight and complete earlier different-resource region population. It preserves
binary32 draw/branch arithmetic, resets MT per call, records attempts/words and
returns CONDITIONAL_PLANAR_CELL or UNKNOWN. `unopposed_cell` remains an explicitly
narrow control. `populate_source` traverses ordered resources then X/Y half-open
bounds, retains every accepted region, and returns CONDITIONAL_PLANAR_SOURCE.
It never radius-culls starts or discards predecessors needed by competition.

`native_bound` follows the inspected sequential sphere merge, including width
increases and the 1e-6 native distance threshold. `competition_rejects` preserves
its broadphase, nine binary32 candidate samples, same-resource exclusion, endpoint
disks and max-width segment rectangles. Rational planar segment tests replace
native atan2/quaternion arithmetic; exact marginal native equivalence is unclaimed.
The separate conservative diagnostic bound is never substituted for native rejection.

`region_membership` is the sphere-clipped disks/max-width-rectangles point product.
`point_membership` is the separately named tapered-strip product (with a count-one
disk convention), not proof of full native availability admission. `region_circle`
is explicitly an **unbounded** primitive-union outer result.
Its rectangle/disk distance uses exact rational and squared-radical comparisons,
so normalizing/rounding rectangle vertices cannot create a false outer negative.
`bounded_region_circle` certifies a disjoint outer union/bound or a strict interior
witness/query containment; unresolved sphere-clipped arrangements return UNKNOWN.
It never treats a failed point sample as a negative. Actual reported resource
presence resolves even if a constituent arrangement remains unknown and another
same-resource region is already proved present.

`nominal_strips` constructs binary32 tapered quads with the prior owned method.
`polygon_circle` uses exact Fraction operations: polygon containment or minimum
edge-distance squared establishes positive-area overlap, equality is tangent-only.
Convexity/finite-domain checks reject folded/concave unsupported geometry. Slivers,
contained regions, containing polygons and outside-start crossings need no sampling
spacing. Count-one area shortcuts, native height/Z and UI percentage admission are
separate; nominal_strips returns UNKNOWN for singleton paths.

## Finite neighborhood and completeness

Let W bound every selected width. Any retained point lies in its source clip box
expanded by W; a planar primitive extends by at most another W. For ordinary base
source ownership, padding+merge cells conservatively enclose clip extension beyond
the owned footprint. Enumerate owner fine cells in beacon radius plus
100×(padding+merge)+2W and resolve every distinct anchor source; then generate each
entire source and all earlier ordered resources. The driver uses global installed
second-half DNAM maximum W=111, though these selected blocks have W≤33. For the
7×7 ±300 lattice it enlarges query radius to sqrt(300²+300²), also covering the
150-unit circle. Paths starting outside the circle and large multi-slot sources
are retained. Unsupported chart seams fail explicitly.

This completeness is for modeled ordinary base-source geometry. Native provider
reads the primary grid; the inspected POI overlay functor writes the secondary
grid. Effective buildable POI-clipped territory and overlay/height-dependent
admission are not quietly included. Full rendered terrain, loaded cache epoch,
historical settings/plugin state and all possible native floating boundaries
remain outside the qualified claim.
