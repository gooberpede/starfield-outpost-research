# Standalone ordinary-vein algorithm

2026-10-24, Australia/Sydney. Authored specification, REVIEW-REQUIRED.
[Contract](../../implementation-briefs/CODEX_BRIEF_SOR_RG2_D1_minimal_corpus_standalone_geometry_reproducer.md),
[schema and dependencies](corpus.md), [validation](validation.md).
This describes a conditional installed-main model, not a reconstructed historical
cache. The inherited [native ledger](../resource-geometry/native.md),
[C2D lookup](../resource-pattern-selection/native.md) and
[consumer](../resource-availability-milestone-b/native-provenance.md) provide
instruction-level provenance. No new native function was executed.

## Preparation and selection

Resolve the requested body's PNDT record in the pinned main-file namespace.
Its FNAM outside BDST selects an SFTR. Decode two 256-square FNAM/GNAM face
pairs; select the word at `coarseX * 256 + coarseY`. This is already selected
data. Surface-seed initialization, SFPT registry order and optional rotation
draws are unnecessary on this route. They would be mandatory for regenerated
trees; that route is unsupported. Packed ENAM is also unsupported.

Read the body's version-5 biome-map member from PlanetData. Its raster index is
`(255 - coarseY) * 256 + coarseX`, unlike SFTR's native index. Retain biome
identity and the low mask nibble for each supplied tile. The builder currently
supplies three coarse tiles over two bodies; it does not supply entire planets.

Before thinning planetary dependencies, recompute all PNDT-order biome
components using the pinned maintainer-owned planetary model. Its inputs are
RSCS; PPBD biome identity, chance, shuffle operand and optional RSGD override;
BIOM fallback RSGD; ordered RSGD entries with all seven selection chances;
IRES rarity and child order; and shared resource occupancy. Shuffle and all
Special/Common/family draws precede the selected per-biome projection. Do not
generate a biome independently or discard competitors merely because the
caller does not ask to display them. This preparation uses empty atmospheric
occupancy, qualified by the prior alternative-occupancy work; historical
effective atmosphere/component state remains unknown.

The corpus stores that derived component projection: descending distinct-rarity
resource order and each resource's selected root-DNAM generation block. It does
not store the planetary draw history or rerun planetary selection at inference.
The build manifest retains root/RSGD identities, DNAM hashes, RSCS and draw counts.
The owned sibling's algorithm and earlier [seed lineage](../resource-geometry-mature-context/seed-lineage.md)
remain the preparation reference; this D1 algorithm has no sibling dependency at
inference. Equal-rarity ties and selected Special are rejected during this build.

## Resolve a location into complete sources

The caller supplies body, chart, geographic descriptor origin and query XYZ in
the translated native frame of that descriptor. Latitude/longitude conversion,
saved-world token resolution and terrain-manager rebasing are outside this API.
One fine cell is 100 native units. Descriptor coordinates are integer multiples
of 96. Interior chart 0/1 is representable; delivered data covers chart 0 only.

For query radius R and the corpus's conservative maximum width W, enumerate
fine ownership cells in the square around query XY expanded by
`R + 100 * (padding + merge) + 2 * W`, with padding = merge = 2.
Floor both ends and include both endpoint cells. Missing coarse coverage returns
UNKNOWN before a fine-cell traversal. Whole sources are generated after discovery;
paths are never culled by their starting point or stopped at the query boundary.

For each fine cell, let coarse coordinates be division by 192 and subindices be
`floor((coordinate mod 192) / 12)`. A raw SFPT slot uses index `subX * 16 + subY`.
If flag bit `0x08` is clear, subtract the two-bit X and Y backlink displacements
from bits 4 and 6 respectively. Translate once, then accept a typed SFBK;
do not retest its anchor bit or follow another backlink. Out-of-chart translation,
missing default blocks and nonraw pattern flags remain unresolved.

The resolved geographic anchor A is `192 * coarse + 12 * resolvedSubindex`.
For descriptor O and raw SFBK dimensions D:

```text
nominal = D - (4, 4)
generatorOrigin = 100 * (A - O - (2, 2))
clipCenter = generatorOrigin + 100 * floor(nominal / 2)
clipHalf = 100 * floor(nominal / 2) + (200, 200)
cellsX = [1, nominalX + 3); cellsY = [1, nominalY + 3)
```

Z is zero for generated points and clip geometry. Deduplicate by chart, anchor
and block identity. Check the source footprint plus a four-cell margin for a
uniform mask. Mixed or unavailable masks leave that source UNKNOWN. Use the
source-anchor biome's complete selected resource order. Expanded corpora store
only the resolved anchor, block and nominal dimensions per slot; the same
frame/key/generation rules then apply.

## Numeric policy and random schedule

Every native add, subtract, multiply, conversion and interpolation rounds to
IEEE-754 binary32 in the order shown by the owned reference implementation.
Do not fuse operations. Nonfinite/subnormal arithmetic, overflow and unqualified
seams return UNKNOWN. JSON decimal numbers must recover the identical binary32
value; ordered XYZW and bound bytes are also emitted as little-endian hex.

For source-local integer cell C, compute `X = O.x + generatorOrigin.x + C.x`
and similarly Y. There is deliberately no division of generatorOrigin by 100:
this operand is the native seed helper's Int2, not a geographic anchor.
Require X/Y in the supported interior domain, then pack:

```text
key = (((((system << 6) | bodyIndex) << 3 | chart) << 16 | Y) << 16) | X
seed = CRC32_raw(LE_u64(key) || LE_u32(managerOwner))
```

CRC uses polynomial `0xedb88320`, initial zero and no final XOR. The manager owner
is the PNDT FormID on this qualified producer path. Initialize MT19937 with seed,
then `state[i] = 1812433253 * (state[i-1] XOR (state[i-1] >> 30)) + i`, modulo
`2^32`, for i = 1 through 623; perform the standard twist and temper operations.
An independent implementation must reproduce MT words, not a language's default
seed API. Each resource/cell resets MT from that key/owner seed.

Let B round to binary32. A uniform draw is
`U = B(B(B(word) / 2^32) * upper)`, where upper has bits `0x3f7fff58`.
A range draw is `B(B(B(high - low) * U) + low)`.
For ordinary rarity r and the source's integer low-nibble mask m,
`weight = settings[r] if m == 8 or m < r else 1.0`. Rarity is a category index,
not a percentage. Settings are indexed Common through Special; no inactive
multiplier applies to the supported active branch.
Keep all range draws even when endpoints are equal. The eight retained block
fields are attempt minimum/maximum, width minimum/maximum, length minimum/maximum,
maximum turn in degrees and chance in percent. Original block fields at
`+0x20/+0x24` are unused by this qualified generator and reconstructed as zero
for the inherited ten-float API. They are not a claim about other consumers.

```text
for resource in selected order:
  for X in cellsX:
    for Y in cellsY:
      reset MT(key(X,Y), owner)
      reject if B(U * 100) >= B(weight * chance)
      n = range(attemptMin, attemptMax)
      attempts = floor(n) + (fraction(n) >= next U)
      return empty if attempts == 0
      heading = B(next U * twoPi)
      accepted = []
      repeat attempts times:
        width = range(widthMin, widthMax)
        if accepted is empty:
          P.xy = B(B(B(100 * cell) + B(next U * 100)) + origin)
        else:
          turn = B(B(next U * degreesToRadians) * turnMax)
          heading = B(heading-turn) if next U < 0.5, otherwise B(heading+turn)
          sine, cosine = nativePolynomialSinCos(-heading)
          direction = (cosine, sine, 0)
          length = range(lengthMin, lengthMax)
          P = B(lastAccepted + B(length * direction))
        reject outside expanded clip box
        reject if any of nine width samples hits earlier different-resource geometry
        append accepted P with width
      append one region if accepted is nonempty
```

Rejected attempts do not become walk predecessors.
Expanded clipping admits P only when each XYZ component satisfies
`B(abs(B(P-center)) - B(half+width)) <= 0`. Every candidate uses this test
before competition, including the planar Z component.

The sine/cosine polynomial
uses the 16 named constants in the schema, signed nearest-integer reduction by
twoPi, reflection into the half-Pi interval, and explicitly rounded polynomial
evaluation. [The unchanged owned math](../../../research/resource-geometry/geometry.py)
is an executable ordering reference. For language-independent reconstruction,
with z = x² and constants named by the schema:

```text
sin(x) = x * (1 + z*(-s1 + z*(s2 + z*(-s3 + z*(s4 - z*s5)))))
cos(x) = sign * (1 + z*(-0.5 + z*(c2 + z*(-c3 + z*(c4 - z*c5)))))
```

Round every operation separately; do not evaluate these as algebraically
equivalent fused polynomials. Reduction starts with `q = B(x * inverseTwoPi)`;
truncate `B(q + 0.5)` for nonnegative x or `B(q - 0.5)` for negative x to integer k.
Then set `x = B(x - B(B(k) * twoPi))`. Reflection above halfPi
uses `pi-x`; below negativeHalfPi uses `negativePi-x`; both negate cosine's sign.

Collision uses the native incremental sphere broadphase followed by positive-width
endpoint disks and max-endpoint-width oriented segment rectangles, tested at nine
candidate samples. Rational planar tests preserve semantic boundaries; marginal
native quaternion/transcendental rounding is not universally validated. Regions
retain their ordered points and sequential native sphere bound. The inherited
numeric ledgers and seven controls qualify this finite use, not every possible
competition boundary.
The nine samples are candidate XY plus width times each offset
`(0,0), (-1,-1), (1,-1), (-1,1), (1,1), (-1,0), (0,-1), (0,1), (1,0)`.
For each earlier different-resource region, require its binary32 sphere
broadphase first. An endpoint disk hit satisfies squared distance at most width²
with positive width. A segment rectangle hit requires projection dot in
`[0, lengthSquared]` and squared cross product at most
`max(endpointWidths)² * lengthSquared`. Degenerate segments are covered by disks.

For an independent bound implementation, initialize center/radius from the first
XYZW point and retain its width as previousWidth. For each later point, perform
the following separately rounded operations, then update previousWidth even when
the current width is nonpositive. The epsilon has binary32 bits `0x358637bd`.

```text
if currentWidth > 0:
  otherRadius = max(previousWidth, currentWidth)
  delta = B(center - currentXYZ), component by component
  d2 = B(B(B(deltaX*deltaX) + B(deltaY*deltaY)) + B(deltaZ*deltaZ))
  dr = B(otherRadius - radius)
  if B(dr*dr) < d2:
    d = B(sqrt(d2)); oldRadius = radius
    if d > epsilon:
      factor = B(B(d-dr) * B(0.5/d))
      center = B(B(factor*delta) + currentXYZ), component by component
    radius = B(B(B(otherRadius+d) + oldRadius) * 0.5)
  else if dr >= 0:
    center = currentXYZ; radius = otherRadius
```

Native collision uses at least radius 0.5 for its prior-region point broadphase;
the callback uses the stored bound radius with its query radius. Preserve this
consumer distinction. The constant epsilon, uniform upper endpoint and callback
quarter-turn polynomial constants are pinned algorithm literals in the authored
code, rather than per-corpus fields. They still belong to the algorithm's exact
numeric dependencies.

## Spatial conclusions

The principal availability status uses the sphere-clipped planar union of disks
and max-width rectangles. Exact dyadic/rational outer-disjoint proofs and strict
interior witnesses establish absence or positive area. An unresolved clipped
boundary arrangement returns UNKNOWN. A tangent alone does not establish positive
area. Point membership is recorded independently as INTERIOR, BOUNDARY, OUTSIDE
or UNKNOWN; counts are paths, not connected deposits or extractors.

The separate native-style area callback first tests bound overlap. Count zero
rejects; count one accepts on broadphase alone. Multipoint paths construct
consecutive binary32 tapered quads, then test XY containment, radius/upper-qualified
vertices and 3D edge distances in native order. Callback acceptance is separately
reported and verified for the seven controls. It is not interchangeable with the
principal positive-area predicate, and neither computes final UI water/atmosphere
union, extractor admission, terrain/POI clipping or a historical cache epoch.

PRESENT requires one proved positive path even when other sources are unresolved.
ABSENT_WITHIN_PROVEN_SCOPE requires resolved source coverage and every selected
path proved nonpositive. Otherwise return UNKNOWN. A resolved halo establishes
model enumeration only; native census remains UNKNOWN in every response.
