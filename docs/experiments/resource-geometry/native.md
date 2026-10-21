# Provider, representation and causal generation

SOR-EXP-0063. STATIC, retail 1.16.244.0, executable SHA-256
`7e9adb1414a8e1b325e5e1f097b9b17b78deb7eebeda37a333351a43a60f9d28`.
Preferred static image base **0x140000000**; addresses in the table are RVAs.
Field offsets have explicit `0x` prefixes and are relative to the named object.
Analysis `FUN_` names remain unchanged; descriptions are analyst aliases.
No runtime address/base or saved identifier is inferred from a static address.
[Pins](sources.csv), [inherited function register](../native-availability-map/functions.csv).

| RVA / original label | Source and exact decisive locations (static VAs) | Causal role |
|---|---|---|
| 0x0079f860 / FUN_14079f860 | `resource-milestone-b-producers-01.tsv`, full decompilation; 0x14079f8d6 through context/index; 0x14079fc37 visited; 0x14079fcb3–0x14079ffa5 miss/lock/construct | Current manager selects spatial sources, BIOM and frame. Source-pointer cache differs from source+0x68 visited key. Miss inserts, attempts synchronous construction then records visited, without a success certificate. |
| 0x0079b520 / FUN_14079b520 | `resource-availability-cont-01.tsv`, full decompilation; 0x14079b625–0x14079b794 prerequisites; 0x14079bc1b family; 0x14079bf06 special | CTPerBiomeData keyed by manager+0x80 and BIOM; component-selected/current/alternate descriptor, family candidates, rarity sorting, source bounds and map-derived weights. Early exits and special resources matter. |
| 0x007af470 / FUN_1407af470 | `resource-availability-ui-29.tsv`, full function/decompilation | Descending resource rarity byte at IRES+0x110. Equal-rarity order must retain the actual sort/input behavior; not silently alphabetized. |
| 0x0079c470 / FUN_14079c470 | `resource-availability-ui-29.tsv`, full instructions 0x14079c470–0x14079c538 | Outer X then inner Y bounded traversal; first index from stitch-setting/2, bounds from source dimensions plus border. Calls generator for each resource/cell. |
| 0x0079a330 / FUN_14079a330 | `resource-availability-cont-01.tsv`, full decompilation; complete continuation in cont02; exact instructions 0x14079a39a–0x14079aab6 | Selected DNAM block, CRC/MT, attempts, heading, width/XY/step draws, clipping, competition and append. See schedule below. |
| 0x0078d7b0 / FUN_14078d7b0 | producers01, full decompilation | Manager mode/current descriptor, owner grid, stitch transform 0x14096f5c0 and settings pack the cell key. Geographic address and this call's local operands are not interchangeable. |
| 0x007af1a0 / FUN_1407af1a0 | producers01 full decompilation | Tests nine candidate samples (center, four corners, four axis extremes) against earlier **different-resource** regions. Current resource ID is excluded. |
| 0x0079b020 / FUN_14079b020 | producers02, 0x14079b020–0x14079b4e8 full instructions/decompilation | Prior-region broadphase, positive-width point disks and consecutive oriented segment volumes; uses max endpoint width. It is not the tapered-strip beacon callback. |
| 0x02346f80 / FUN_142346f80 | new `rg1-generation-01.tsv`, 0x142346f80–0x142346fd7 | One canonical MT draw, binary32 range interpolation; no extra draw hidden by a range helper. |
| 0x02bf4850 / FUN_142bf4850 | same new export, 0x142bf4850–0x142bf49e7 | Enclosing-sphere expansion for region center/radius. The sphere is a broadphase bound, not the union of multi-point strip geometry. |
| 0x007a0820 / FUN_1407a0820 | producers02, full function | Copies/transforms a source byte field into 100×100 raster, with quarter-turn/reflection cases. Does not read the region-point collection at this boundary. |
| 0x0079ee50 / FUN_14079ee50 | new export, full instructions/decompilation | Related multi-level aggregate sampler: bilinear byte-field sampling, weights and threshold table; its product differs from the point-path callback. No raster/vein equivalence is established. |
| 0x021e0f50 / FUN_1421e0f50 | ui16 plus [prior predicate ledger](../resource-availability-milestone-b/native-provenance.md) | Source/resource maps → 48-byte regions → 16-byte XYZ/width points; native area callback including count-one shortcut, tapered strips, Z-qualified vertex and 3D edge branches. |

## Dataflow and independent products

Current body/terrain context → bounded spatial source index and enumeration →
source pointer, bounds, transformed origin and BIOM → CTPerBiomeData/selected
RSGD and map readiness → ordered resource/cell generation → region collections
in the manager's ProcGen source/resource maps → point/strip predicates → spatial
resource set. Atmosphere and selected biome water are later UI contributions.
The provider also manages a related raster/aggregate product. Shared ancestry
does not establish the same geometric membership function.

The [existing lifecycle evidence](../native-availability-map/region-lifecycle.md)
remains controlling: manager+0x130 owns ProcGen; exclusive construction/shared
consumption use ProcGen+0x40. Cache insertion and source visited bookkeeping are
not completion/freshness certificates. Broad reset 0x0079ddf0 clears maps/visited
and related state; destruction is separate. Exact source lifetime/reset epoch and
historical restore correspondence remain unobserved. No new persistence status
or universal loaded-area coverage is promoted.

## Generator schedule and original explanatory pseudocode

DNAM is 560 bytes for the tested modern definitions. Each rarity block is ten
binary32 scalars, at byte offset `40*(rarity+7)`. Pair 0/1 selects attempt count,
2/3 width, 4/5 segment length; scalar 6 controls angular change, 7 chance.
Meanings of scalars 8/9 are not invented. Native memory descriptor stride is
0x238, different from this serialized payload size.

CRC starts at zero, no final XOR, folds packed key little-endian u64 then current
manager+0x80 little-endian u32. No IRES identity is folded here. MT19937 is reseeded
inside each generator call, with the standard 624-word recurrence and index 624.
The range upper is float bits 0x3f7fff58, not 1. Arithmetic below rounds each
binary32 instruction separately. The source-origin operands must be supplied
from this call's coordinate domain, not substituted from saved chart indices.

```text
for resource in actual_selected_rarity_order:
    for x in source_bounded_x_range:
        for y in source_bounded_y_range:
            block = selected_DNAM[40 * (resource.rarity + 7)]
            rng = MT(CRC(native_packed_cell(x,y,origin), manager_key))
            if weight * block.chance <= uniform(rng) * 100: continue
            t = range_draw(block.count_min, block.count_max)
            n = floor(t) + (fraction(t) >= uniform(rng))
            if n == 0: continue
            heading = uniform(rng) * native_two_pi
            accepted = []
            repeat n attempts:
                width = range_draw(block.width_min, block.width_max)
                if accepted is empty:
                    p.xy = cell.xy * 100 + uniform_xy(rng) * 100 + origin.xy
                    p.z = 0
                else:
                    turn = uniform(rng) * native_degree_factor * block.turn
                    heading += (-turn if uniform(rng) < 0.5 else turn)
                    s,c = native_polynomial_sincos(-heading)
                    p = accepted.last.xyz + range_draw(block.length) * (c,s,0)
                if clipping_admits(p,width) and
                   no_prior_different_resource_rejects(nine_samples(p,width)):
                    accepted.append(p,width)
            if accepted nonempty: bound_and_append_region(accepted)
```

This pseudocode is analytical explanation, not copied decompilation. The heading
sign follows **0x14079a8c2 VXORPS** before the helper; the decompiler's apparent
two-argument prototype omits the angle in XMM2. A fresh executable read verifies
the 0x144f06670 sign mask. Initial draws and attempts rejected before the first
append resample initial XY. A later rejected attempt still advances heading/RNG;
the next attempt extends the last **accepted** point. The selected attempt count
is not an accepted-point count. A zero fractional count with a precisely zero
rounding draw takes the increment branch; no generic Python rounding replaces it.

For nonnegative widths, expanded clipping extents contain shrunken extents;
the inspected OR of those branches reduces to expanded-box admission in the
qualified finite ordinary numeric subset. It retains subtract-before-compare
arithmetic in the evaluator. This is admission of a candidate point/width, not
polygon clipping or proof that an entire generated strip lies inside the source.

## Source context recovered in the continuation

The new read-only session exports 001–022 under
`.local-work/resource-geometry/native/` retain full decompilations and selected
instruction listings from the same pinned executable. The following are static
VAs, not runtime addresses; [sources.csv](sources.csv) pins each local export.

| Static VA / export | Decisive upstream role |
|---|---|
| 0x14096e060 / exact-beacon-05.tsv and resource-availability-cont-04.tsv; 0x14096be70 / 007,011 | Surface pattern selection by BIOM style and registered candidate order; lookup into raw or orientation-remapped SFPT slots. Ordinary 256-square direct-map route only. |
| 0x140970d50 / rg1-surface-crc-01.tsv | Focused final full helper export confirms raw CRC32 folds param3 body-index, param2 system, then param1 surface seed as LE words, initial zero/no final XOR. Caller operands are pinned at 0x14096e060. |
| 0x14096bf00, 0x1409df850 / 014 | SFPT CNAM loads style at +0x848; BIOM NNAM loads style at +0x450. FNAM/GNAM are the 16×16 source IDs/flags; SFBK DNAM gives raw dimensions. |
| 0x14096bba0, 0x140851d20 / 011 | Whole-footprint inverse orientation relocation with preserved raw slot words and explicit 8-way cell matrices. |
| 0x14008d130 / 020; 0x14008d160, 0x140055360 / 019 | Native default surface seed 0x20201215; whole-pattern random flip/rotation false; block orientation true. Defaults are conditional inputs, not observed historical settings. |
| 0x14008cc50, 0x14008cb90 / 022 | Stitch merge zone 2 and block size 10; stride 12. |
| 0x1407847b0 / 022; 0x1409870d0 / 001 | Primary grid dimensions include finite border; grid origin is adjusted around its linked owner's dimensions/origin. Source local anchor uses the owner's local frame, not an index from the backing slot array. |
| 0x140785190 / 005; 0x140784c40 / 006 | Enumerates geographic base blocks including nonanchor back-links; base functor targets primary owner+0x10. AddOverlayBlockFunctor separately targets owner+0x18. |
| 0x140786230, 0x1407862a0 / 009,011 | Base block callback subtracts twice grid padding from raw dimensions and calls source constructor. Height metadata is carried, not used to render terrain in RG1. |
| 0x140982d90 / 013,014; 0x140982390 / 018 | Constructor preserves local source anchor +0x10/+0x14, dimensions +0x18/+0x1c, padding +0x20/+0x24, raw dimensions +0x28/+0x2c, geographic/source selectors +0x38 onward and cache key +0x68. |
| 0x1409832e0 / 005; 0x140985900, 0x140985c50, 0x140986080 / 003 | Grid cells, edges and corners preserve/enumerate contributing source descriptors; whole-source ownership halo avoids selecting only the beacon's center source. |
| 0x140985870, 0x140988240, 0x140988ab0 / 001,009,011 | Primary grid bounded lookup and source enumeration feeding 0x14079f860. Source pointers/cache identity remain transient. |
| 0x142339340 / 015 | Returns low-nibble ordinary rarity mask. Special selection separately reads high nibble; they are not interchanged. |
| 0x140051240…0x140051330 / 019 | Default inactive multipliers common 0.3, uncommon 0.2, rare 0.1, exotic 0.01, unique 0, special 0.3, freshly read through static constant VAs/file offsets. |

Planet definitions are freshly read from the pinned main ESM. PNDT PPBD carries
BIOM/chance/per-biome seed/override, RSCS the planetary selection seed, GNAM the
system/parent/body-index tuple and INAM the atmosphere reference. The existing
owned planetary reproducer is fed these fresh fields plus the previously observed
Kreet atmosphere input; other bodies' exploratory outputs are not qualified RG1
site results. Its selected family and effective PNDT RSGD agree with the current
source-biome resolver. Main descendants share the selected root's DNAM; descending
rarity precedes complete X/Y traversal, followed by separately selected Special and
Everywhere resources. These Kreet cases select neither latter branch.

For source local anchor L and padding P, generator origin is 100×(L−P), source
dimensions are raw−2P, clip center is origin+100×floor(dimensions/2), clip half is
100×floor(dimensions/2)+100×merge. Cell ranges are [merge/2,dimensions+2merge−merge/2).
0x14079a330 adds this native origin to each integer cell before 0x14078d7b0 applies
the current geographic descriptor. This unusual seed domain is source-supported;
dividing origin by 100 would change the inspected program. The packed result folds
system (18 bits), body index (6), chart (3), Y (16), X (16); unsupported seam
translations remain explicit failures. Existing Kreet manager+0x80=259487 supports
this scoped suffix, not a universal PNDT mapping.

The chance multiplier uses low nibble 8 or low nibble below resource rarity to
select the inactive setting. These sources have uniform masks over owner footprint
plus conservative border, so first-query cache position cannot alter that input.
This removes one mutable-query ambiguity for these cases, not all map boundaries.

## Bounds, predicates and finite surroundings

Region assembly initializes its bound from the first point; each later positive
width merges a sphere with radius max(previous width,current width) through
0x142bf4850. The point predicate first tests radius max(bound radius,0.5), then
positive-width disks and closed max-width rectangles. The sphere can clip those
rectangles. A conservative larger sphere is therefore insufficient as a semantic
replacement. Review's counterexample is first point (0,0,w1), second (1000,0,w100):
the native-model sphere is center (549.5,0), radius 550.5; point (0,99) lies in the
unbounded rectangle but fails the sphere. The regression preserves that distinction.

For nonnegative finite W, accepted centers lie in source clip expanded by W and
primitives extend at most another W. Ordinary owner-footprint padding+merge gives
the conservative halo radius R+100×(padding+merge)+2W. Enumerate all fine cells in
that halo, resolve anchor sources and generate each whole source with all ordered
predecessor resources. The executable driver uses W=111, the maximum over every
installed RSGD second-half width block, and expands R to enclose its held-out
lattice. No walk-length/start-radius truncation is used. Coverage assumes this
ordinary primary-grid route; seams, additional source classes and effective POI
clipping are not inferred from this proof.
