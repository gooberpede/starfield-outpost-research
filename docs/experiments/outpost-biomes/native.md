# Definition, assignment and consumer chain

[Answer](report.md), [coverage derivation](nominal.md), [pins](sources.csv).
All native addresses below are preferred static VAs at image base
`0x140000000`; RVA is VA minus that base. Memory member offsets are hexadecimal.
Native aliases are analyst descriptions, OBSERVED-INTERNAL, not callable APIs.
`nNNN` means `.local-work/outpost-biomes/native/NNN.request.tsv`; exact sections,
line ranges and file hashes are in [functions.csv](functions.csv).

Installed retail executable 1.16.244.0 SHA-256
`7e9adb1414a8e1b325e5e1f097b9b17b78deb7eebeda37a333351a43a60f9d28`;
main ESM SHA-256
`1dabed00c3f4282dd3bb54d2e9601e40b577d8742d078b7ccef203adbfef0da7`.
Both were freshly hashed before analysis and checked after native worker retirement.

## Planet, map and identity

Fresh main-ESM traversal finds 431 BIOM and 32 RSGD records and rereads PNDT
`0003f59f` Kreet, `0005e0de` Feynman V and `0005e4da` Carinae III-a.
Record-file offsets are respectively 1,402,105,313; 1,411,909,071; and
1,425,228,291. Their body ANAM names are Kreet, Feynman V and Carinae III-a.
Their PPBD entries' initial FormID words equal their maps' three-member BIOM
catalogues. This is catalogue correspondence, not site selection.

`142332f70/142333000` (n007/n006) retrieve the body-keyed name component.
`142403520` (n010) independently names that type
`TaggedFixedStringComponent<CTNameTag>`; do not rename it CTBiomeData merely
because a biome loader consumes it. `140478350` (n005) builds the body-name
resource path, including a plugin directory when applicable, and requests the
BiomeMapDB entry. `14001e340/14001e370` (n009) initialize the extension/path
strings; the path is `PlanetData\BiomeMaps\`. The matching installed members
are `planetdata/biomemaps/{body name}.biom` in Starfield - PlanetData.ba2.
This study uses the explicitly pinned main-data members, not a reconstructed
historical archive priority or every possible overriding mod.

`140478030→14047a2b0→14047a930` (n004–006) construct and fill
`BSGalaxy::Biomes::Map`. The selected files are version 5, flag byte 1,
three catalogue FormIDs and two faces. Each face has width/height 256/256,
a counted 65,536-element little-endian uint32 BIOM array and a counted
65,536-byte mask array. Each member is exactly 655,414 bytes; parsing both
faces closes exactly at EOF. The uint32 identity array starts at member byte
34 for face 0 and 327,730 for face 1. These are map-member offsets, not BA2
compressed offsets or runtime addresses.

The loader recognizes earlier version branches: extra legacy vectors before
version 4, obsolete structures before version 3, and different mask reading
for version 1. This task's parser deliberately accepts only the observed
version 5. Native identity loading remaps FormIDs through the owner's plugin
context, resolves type `0xa0`, and substitutes DefaultBiome on invalid identity.
`140478030` can replace invalid/empty face populations with the initialized
default map. Missing/failed lookup is therefore not evidence of empty terrain.
No fallback default is substituted silently by this research calculation.

## Integer address to BIOM

`14078d660` (n001) chooses terrain-manager context and transforms its Int2
through `14096f5c0` (n002). It recombines hierarchy indices and returns the
**fine cell center** `(I+.5)/N-.5, (J+.5)/N-.5`, with tagged chart and
`N=(fine settings sum)*landscape resolution*16`, installed default 49,152.
This reuses [the established hierarchy and seam rules](../position-resumption/algorithm.md).

`14078ee90` (n001) selects manager descriptor at `+0xc8`, or `+0x1c0` when
manager kind is 3; calls that transform; leases manager `+0xf8` map entry;
requires its ready-state predicate; normalizes charts 2/3 by negating both
coordinates and mapping tag 2→0, 3→1; selects a face at map `+0x18` with
stride `0x30`; then calls `1423390f0`. That helper clamps `u+.5,v+.5`, floors
`width*(u+.5)` and `height*(1-(v+.5))`, clamps to valid last indices, and
returns row-major `row*width+column`. The lookup reads **one uint32**, resolves
it and requires form type `0xa0` (BIOM). A missing map/failed state/type returns
null. No interpolation, noise, PRNG, character, quest or session seed is
consulted on this identity path given its map and address inputs.

`14078efa0` returns the corresponding numeric identity without final form-type
resolution (n002). `1423391d0/142339250` accept chart/angles respectively and
use the same raster path (n005/n002). The angular version requires projection
qualification; it is unnecessary for territory traversal once the frame is known.
`142339340` selects the separate mask byte and returns its low nibble (n002).
The identity lookup does not use that mask to interpolate BIOMs.

## Actual consumers and exceptions

`1405e68e0` (n007), a resource/biome-conditioned consumer, reads reference XY
at `+0x8c/+0x90`, multiplies by binary32 `.01`, performs negative-corrected
floor, calls `14078ee90`, and compares the resulting BIOM pointer with its
required biome. It separately tests generated resource membership. This is
direct evidence of the approximately 100-unit assignment granularity, rather
than an assumption from terrain appearance. Constants are read in n011.

The existing area updater `1421e07d0` likewise floors translated XY and uses
this lookup for its biome resource vector; unchanged/null identities can retain
the previous vector ([prior causal map](../native-availability-map/dataflow.md)).
`1418a9900` (n007) passes the selected BIOM into generated content construction
after separate site/context/CRC inputs. That content selection may vary without
changing the base raster field.

Water/coast consumer `14078e900` and water-neighbor search `140975e00` (n006)
inspect BIOM `+0x3f8`, nearby cells and terrain source modes. These are additional
water/coast operations, not bilinear identity interpolation in `14078ee90`.
`14078abc0` (n002) can use atmosphere/world/encounter overrides before its
biome-derived fallback for a different environmental consumer.
`140aef010/140aef1e0` (n006) similarly prefer cell/world/extra state for their
own outputs. Do not call every environmental field the authoritative base BIOM.

Visual materials, noise masks, biome markers and special fixed worlds are not
exhaustively reconstructed. This scoped conclusion concerns ordinary generated
surface base-biome identity consumed by the mapped reference/resource routes.
It does not promise that every point in a cell looks alike or that one local
BIOM result overrides every environmental or encounter consumer. Actual loaded
manager/frame selection, historical overrides and restoration are not observed.

## Lifecycle and persistence

Installed PNDT/BIOM/RSGD/map values are DEFINITION-DERIVED. The selected ready
map, source descriptor and cached environmental/resource outputs are
RECONSTRUCTED/TRANSIENT context. Saved parent/Workshop identity, site tuple,
initial XYZ and compensation are PERSISTED in the qualified samples; the
combined answer is MIXED. This task does not establish that every save lacks
biome IDs or that any serialized component is automatically authoritative after
load. Its reconstruction uses actual saved coordinates plus the pinned map,
not a decoded per-outpost list of measured biome membership.
