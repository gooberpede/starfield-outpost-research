# Effective territory and resource relationships

[Answer](report.md), [nominal derivation](nominal.md), [native chain](native.md).
These are distinct consumers of shared planetary context.

## Secondary effective footprint

Let D be the nominal disk, B(x) the base-biome lookup field, and E(x) the
territory eligibility predicate after location/encounter restrictions. Effective
biome coverage is the set of labels with **positive area** in
`D ∩ E ∩ {x:B(x)=label}`. Clip each already enumerated cell's intersection with
D against E before adding its identity. Nominal coverage is an upper bound;
clipping can remove, never introduce, a base identity.

[L3](../spatial-placement/native.md) supplies actual native operations:
`140f38d80` follows location ancestry and OutpostNoPlacement keyword;
`140f38cb0/140f3f9a0` additionally inspect encounter permissions and cell/context
agreement. Border construction `140f47de0` gathers disallowed loaded
cell/location rectangles; `140f48480` clips the 36-segment displayed radial
outline against them. Do not mistake that display approximation for the exact
point admission predicate or a permanently saved exclusion polygon.

Save30→31→33 is L3's known clipped control. This task redecodes 31 and 33,
recovers the same ordinary beacon/Workshop frame and computes a single nominal
base biome, MountainsLifeKreet. L3 independently records one beacon root then
three completed construction roots and photographs territorial exclusion.
It does not identify every photographed point's native location operands.
For any positive-area surviving footprint in this qualified base field, the
effective biome set must still be MountainsLifeKreet. Neither surviving area
nor an exact exclusion outline is measured here.

Complete secondary geometry remains **OPEN**: the missing operands are the
selected loaded grid-cell/location groups, their encounter permission flags,
world/frame translation and exact eligibility boundaries for that site.
Saved beacon position/radius and map pixels cannot reconstruct those operands
by themselves. Reusing L3's display segments would answer a different question.
The smallest proposed observation would bind the selected SOR-004 grid and
location/encounter records to points on both sides of its restriction, in one
qualified frame. This would require a separate live brief with explicit
intervention, protected-save, flush/exit/recovery and cleanup boundaries; no
test is launched or instrumentation prepared here.

Actual object buildability additionally applies footprint, support, collision,
height, resource, budget and group-limit gates. A buildable point for one item
is not an exact universal E polygon. These secondary gaps do not block the
nominal enumeration proof.

## Inorganic relationships

The [existing native resource map](../native-availability-map/dataflow.md) is
reused with its source/residency/freshness limitations. New n011 rereads the
central generator and per-biome component lookup. Installed BIOM RNAM fields
reference RSGDs: FrozenNoLife09→`0037c672`, CanyonsNoLife06→`00258050`,
HillsNoLife08→`000083f1`, MountainsLifeKreet→`00007edd` and
VolcanicRoughLifeKreet→`000083ea`. The map header and PNDT PPBD biome catalogue
are separate from those descriptor references. PNDT RSCS is a four-byte
subrecord in each selected body, not a separate RSCS form in this census;
its bounded native handling is recorded below.

`14079b520` obtains body/source context, BiomeMapDB data and per-biome component
selection through `140771f30`. That helper requires the component's BIOM ID
at `+0x40` to equal the requested identity before copying its configuration.
Generation consults both the identity raster and mask nibble
(`1423390f0/142339340`), chooses component/current/alternate-BIOM resource
descriptors, sorts and traverses generation cells, and constructs resource
strips using source/owner keys, RNG and earlier competing geometry.
`14079c540/14079c5e0`, `14079c470`, `14079a330` and `1407af1a0` retain their
mapped roles and unqualified full-generator equivalence in the prior report.

Thus base BIOM boundaries are one selection input; generated inorganic regions
are not identical to BIOM pixels. The area updater then tests actual strip
geometry, atmosphere and selected water through separate populations. A biome
catalogue resource can be absent locally; a UI list can retain earlier state;
an extractor registry records configured producer objects. None alone measures
every resource or biome in a territory. This task performs no resource geometry
census, production simulation or full deposit prediction.

Fresh PNDT tag dispatch `14076ec00` (n013, successfully re-exported in n014)
recognizes literal `RSCS` and reads exactly four bytes into the planet record
at `+0x50` (`140770114..140770122`). PNDT PPBD dispatch is in the same loader.
The resulting record pointer is registered through
`140773910→142346a60` under the body-keyed static-data component; the direct
biome resolver instead uses the body-name-selected map and its identity array.
The selected RSCS bytes are Kreet `4b4b70a9`, Feynman V `83a97c19`, Carinae
III-a `44037fba`. No RSCS-to-biome membership equation, RNG-seed meaning or
complete downstream checksum/invalidation contract is established here.
Do not infer such semantics from the subrecord spelling. This limited field
trace does not weaken the directly mapped BIOM/RSGD/mask generation connections.

## Organic relationships

Biome definitions participate in natural flora/fauna/content context, but the
facility's available organic choices are not a direct biome-overlap query.
[E2's native selector](../organic-facilities/native.md) resolves a Workshop
planet key, iterates planet-scoped species ranges, tests domesticability and
knowledge and folds supported IRES recipes. It supplies no facility-local BIOM
operand on that mapped route. Species/resource/knowledge state must not be
replaced with the current ground appearance or this disk's BIOM set.

These resource connections use Bethesda definitions/native data and existing
project research, with their source pins and credit preserved. No resource
presence—Copper, Nickel, Ionic Liquids, Memory Substrate or otherwise—is used
as an inverse proof of biome membership.
