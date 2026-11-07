# Nominal biomes

**Can one outpost cover more than one biome?** Yes. The ordinary base-biome
lookup gives each terrain query cell a discrete biome identity. To find
the biomes under a nominal outpost, include every cell that overlaps its
horizontal disk with positive area, then collect the distinct identities.
Sampling just the beacon, the perimeter or a few points can miss a cell.
[Coverage proof](../experiments/outpost-biomes/nominal.md).

## What the map assigns

Start with the body, its resolved biome map and the qualified Workshop centre
and frame. The ordinary beacon definition supplies a radius of 150 native
units. The mapped consumers quantize local XY to roughly 100-unit cells,
map each cell to an address on a body chart, and look up the raster pixel
at that cell's centre. The raster can assign the same biome to many cells.
Terrain materials, visual blending and water/coast behavior have their own
consumers. [Native lookup and exceptions](../experiments/outpost-biomes/native.md).

| Saved example | Reconstructed nominal coverage |
| --- | --- |
| Save52, Feynman V Cu Co Ni IL | 14 cells. Twelve select FrozenNoLife09 and two select CanyonsNoLife06 in a narrow cap. |
| Save52, Carinae III-a Rc Fe | 14 cells, all HillsNoLife08. |
| The other Feynman V site, Cu IL F | 15 cells cross two raster rows, both CanyonsNoLife06. Crossing a raster boundary need not add a biome. |

These are conditional reconstructions using the pinned Starfield 1.16.244.0
lookup and installed maps with qualified saved positions.
The names identify examples after the typed joins. The screenshots and
resource labels do not measure the base-biome assignments.
[Case evidence and scope](../experiments/outpost-biomes/saves.md) ·
[Independent review](../experiments/outpost-biomes/review.md).

## Which part can you use?

A POI restriction can remove part of the nominal disk from eligible territory.
Removing area can remove a biome from the result. It cannot add another base
biome to the same field. The exact surviving footprint depends on loaded
location and encounter state. Actual placement adds support, collision and
item-specific conditions. [Territory and resource boundaries](../experiments/outpost-biomes/effective-and-resources.md) ·
[Construction guide](construction.md).

A base-biome identity can inform resource generation, but the source biome
and mask sampled for generation, generated deposits, area availability and
point-specific extractor eligibility are different products. A nominal
two-biome result does not establish that any particular extractor can be
placed. [Resource generation guide](resource-generation.md).

Use the [biome reference](../reference/nominal-biomes.md) to check the tracked
Feynman cell tally and its map addresses. For the frame and anchor
prerequisites, see [position](position.md).
