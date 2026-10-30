# D5T geometry and rendering guide

[Geometry JSON](geometry.json) uses schema `sor-d5t-geometry/1` and contains both
outcomes, full fixed generation inputs, resource identities/names, winner witness,
equivalence class, coordinate basis, lossless native XYZ/width points and bounds,
and explicit plotting primitives. All numbers are finite. JSON binary64 parsing
represents every original binary32 scalar exactly. Ordered point arrays are the
native retained representation; primitive vertices are a rendering derivative.

The canonical frame is D5S's fixed local manager/source frame. Nominal source
anchor `(0,0)` differs from generator origin `(-200,-200)`. There is no beacon
marker. Source clip center is `(300,300,0)`, half extent `(700,700,0)`. Generation
traverses cells `[1,13)²`, retaining accepted point/width pairs; this clipping
predicate does not clip entire polygons to a box. Native units are not labelled
metres or given a compass direction. X increases right and Y up.

For each region the plotted generation-competition footprint is the union of
positive-width point disks and consecutive segment rectangles of half-width
`max(width_a,width_b)`, intersected with the native bound disk of radius
`max(bound_radius,0.5)`. Rectangles span only between the endpoint planes;
disks provide the separate endpoint pieces. The native bound can cut a rectangle.
This follows `0x14079b020`, not the differently shaped tapered-strip Workshop
callback. The candidate's nine-sample competition dilation is not itself plotted.
Resource paint order is Copper, Fluorine, Ionic Liquids; opacity is 1. Small
same-color outlines improve legibility and are decorative, not extra geometry.

SVG circle geometry is exact for the supplied scalar circle. Segment vertices
use binary64 square roots/normalization from native points. This continuous
planar reconstruction does not reproduce discrete native binary32 and
atan2/quaternion boundary rounding. No claim of exact UI, terrain or every
boundary-point equivalence follows. The native test receipt supplies 1,630
endpoint, distant and near-segment-edge point comparisons, with zero mismatch.
The exact point/width primitives remain available for alternative reconstruction.

Both single maps and [comparison](comparison.svg) use a 680×680 plot, extents
`[-500,1200]²`, scale 0.4, stable titles/legends and the same affine transform:
`screen_x=82+0.4*(X+500)`, `screen_y=180+0.4*(1200-Y)`. The second comparison
panel adds 800 to screen X. No primitives exceed the view extents. All shapes
are clipped only by their corresponding native bound, with unique SVG clip IDs.

| Resource | FormID | IRES TINC bytes | SVG color | Original ESM record offset |
|---|---|---|---|---|
| Ionic Liquids | `0x000057d4` | `4c d7 bb 00` | `#4cd7bb` | 1301612783 |
| Fluorine | `0x000057d0` | `2f 78 69 00` | `#2f7869` | 1301611937 |
| Copper | `0x000057cf` | `27 55 49 00` | `#275549` | 1301611716 |

These are original-file record-header offsets, not subrecord or runtime offsets.
The native TINC loader at `0x1409e7c65..0x1409e7d45` extracts successive low
bytes into three normalized float channels at resource offsets
`0xe0/0xe4/0xe8`. SVG uses the bytes in that order at full opacity; the fourth
byte is not interpreted as transparency. Resource colors are record-derived;
background, grid and text use a separate authored neutral palette. This records
color provenance, not in-game shading or display calibration.

Rebuild the derivatives with
`research/resource-retained-population/d5t_maps.py` from the repository root using
the pinned CPython. It requires authenticated ignored D5T receipts and the three
IRES field rows. It reads only those receipts/owned methods and writes the named
CSV, JSON, SVG and ignored map-check receipt. It does not run a game, native
fixture, network request, save decoder or database operation. Raw native exports
and extracted asset bytes remain local; these numerical research derivatives
are REVIEW-REQUIRED, not cleared for publication.
