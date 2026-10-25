# D5G selector and demand proof boundaries

[Report](report.md), [methods](methods.md), [pins](sources.csv). All native addresses
are preferred static VAs on the pinned 1.16.244.0 executable, image base
`0x140000000`; offsets below are bytes. These are existing exports, read offline.

## Installed inputs and precedence

The [C2D native ledger](../resource-pattern-selection/native.md) establishes
PNDT's FNAM outside BDST as the typed SFTR link, installed at PlanetData `+0x38`.
The existing-tree getter `0x14096b8e0` prefers that tree; missing-tree creation
can instead reach `0x14096e060`. That alternate requires seed, registry and
orientation state; its existence does not license substituting a regenerated
tree for the available installed one. Feynman's two sites share the PNDT and
typed tree link, while their table coordinates can select distinct SFPTs.

The complete linked SFTR has two 256-square FNAM/GNAM arrays, indexed as
`coarseX*256+coarseY`. This is different from the inverted-Y BIOM raster index.
The [D4C installation diagnosis](../resource-owner-root/source-layout.md) proves
that SFPT serialized FNAM/GNAM pairs are transposed into runtime X-major order
by `0x14096bae0`, at `0x14096bb20–0x14096bb54`. Tree arrays are not transposed.
Backlink/type selection at `0x140784e95–0x140784fcd` translates once before typed
SFBK lookup. A missing block can reach a default; valid base-source matches do
not establish that overlays, special components or all defaults are absent.

The [D4E initialization](../resource-slot-provenance/native.md) and
[D5 precedence](../resource-feynman-d5/native.md) distinguish PNDT RSCS/PPBD,
BIOM-local RNAM, effective RSGD overrides, initialized owner components and the
selected root-DNAM. The sixth slot is the first BIOM-local rarity-6 entry;
it does not simply copy effective Everywhere data. Append/exchange preserves
occurrences and can carry another family's descendants into the selected root.
Descriptor lookup checks current effective RSGD, then current BIOM RNAM, then
eligible same-root alternates in unsigned creation-key order. Selected Special,
ordinary zero-weight Water, biome Water admission and atmosphere remain separate.
These rules are independently derived within the documented initialized-main
route; the exact historical runtime population is not supplied by installed data.

## Demand and source enumeration

The [D5D demand ledger](../resource-construction-demand/native.md) traces
coordinate/cell requests to dependency registration and the two provider callers
at `0x1407a1a3c` and `0x1407b526a`. A cell request can reuse an aggregate without
calling the provider. Workshop scanning at `0x1421e07d0` consumes resident
populations; it is not the original construction-query oracle.

Two primary exports narrow the remaining static gap:

| Boundary | Exact primary location | Consequence |
|---|---|---|
| Context admission | `resource-region-dependencies-01.tsv`, `0x14078c4e0–0x14078c53a` | The current manager's worldspace/context must qualify. Context selection has a flagged alternate; installed planetary coordinates alone do not provide these live fields. |
| Index lookup | Same export, `0x140985870–0x1409858cc` | Obtain index origin through `0x1409870d0`; subtract from caller Int2; require both deltas nonnegative and below index `+0x48/+0x4c`; load the pointer at `+0x20 + 8*(dx + width*dy)`. Out-of-range returns null. |
| Per-cell sources | `resource-milestone-b-producers-01.tsv`, provider `0x14079f860`, decompilation after `0x140985870` call | The returned object dispatches virtual method `+0x10` into a temporary source list. The provider iterates that list; the lookup rectangle is an index rectangle, not the nominal extent of one source. |
| BIOM and cache admission | Same export, `0x14079fa90–0x14079fd02` | BIOM lookup uses source `+0x10`, then visited source `+0x68`, exclusive map lookup by full source pointer and miss insertion. A visited skip and a map hit differ. |
| Query conversion | Same export, `0x14079fe81–0x14079ff18` | Manager mode 3 chooses descriptor `+0x1c0`, otherwise `+0xc8`; convert the original provider Int2, then geographic projection, before calling `0x14079b520`. Source origin is rounded separately. |
| Mask sample | `resource-availability-cont-01.tsv`, `0x14079b8dd–0x14079b8ed`; `d5-mask01.tsv`, `0x142339340–0x14233942f`; `d5-raster02.tsv`, `0x1423390f0–0x1423391ce` | Geographic round trip, chart folding and clamped/floored inverted-Y raster lookup supply one low nibble for ordinary construction. Later generator-cell traversal does not resample it. |

The exact missing predicate is not simply “which biome is the beacon in?” For
each candidate caller Int2, one needs the effective manager/index origin and
dimensions, the returned object's concrete source-list implementation and
contents, the descriptor-to-geographic round trip, BIOM success, visited/map
state and successful construction. No complete inverse of this combined
predicate is established by the existing base selector. An empty witnessed
first-query set therefore cannot become an absence or uniqueness proof.

Two distinct in-range Int2 values can in principle return objects whose virtual
lists contain the same source pointer; the source-pointer key does not include
the query. The installed base-selector inverse supplies many distinct cells with
the same analytical key, which makes that hypothesis concrete, but does not prove
the same live pointer is returned by both virtual calls. To establish order
dependence, both must also survive admission, sample different masks and have
the relevant first miss precede reuse within one protected lifetime. D5C proves
the retain/hit mechanism statically; none of these data join an earlier outpost
epoch. Identical pointers after teardown need not be the same allocation.

## Why nominal and reachable domains cannot be equated

The source rectangle, conservative predictor margin, inverse base-selection
tile and provider demand set are different sets. Their nesting has not been
proved. A source's nominal mask can be uniform while its margin crosses a
raster boundary; the inverse base selector can be uniform while an unexamined
virtual neighbor enumeration reaches across that boundary. Conversely, a
mixed nominal footprint need not imply both masks are admissible first misses.
`query-domains.csv` reports these distinctions rather than claiming false nesting.

The low-nibble mask matters through the vector of effective rarity weights:
mask 8 or mask less than rarity uses the inactive weight; otherwise weight 1.
Different masks can yield the same vector, and different vectors can yield the
same resource presence while changing ordered paths. Even uniqueness of the
ordinary vector is insufficient for an unconditional prediction if component
selection, Special admission, seeds, source frame or historical overrides differ.
