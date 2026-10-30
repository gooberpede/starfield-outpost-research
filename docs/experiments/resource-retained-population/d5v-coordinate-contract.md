# D5V native coordinate contract

2026-10-30. [Report](d5v-report.md), [source pins](d5v-sources.csv),
[domain diagram](d5v/coordinates.svg), [numerical backing](d5v/spatial.json).
The established [C1 coordinate proof](d5u-c1-coordinate-validation.md) was read
before creating D5V plots. D5V supplements its historical-frame figures; no C1
or original D5U map or source geometry is changed.

**D5V-C1 presentation correction:** the earlier D5V plots used centre-relative
axes. That reversible display did not satisfy the required native-axis
presentation. [Correction report and acceptance](d5v-c1-report.md) supersede the
earlier D5V-AC6/AC7 visual acceptance. The current figures use absolute historical
native descriptor-frame X/Y for data, axes, centre and beacon labels.

## Native domains and owners

All VAs below are preferred static image addresses, base `0x140000000`, on the
pinned 1.16.244.0 executable. Field offsets are bytes. Native units are not
asserted to be metres. X/Y mean the engine's X/Y operands, not east/north.
Z is the separately read height coordinate. These 2D predicates do not establish
a global 3D handedness or planetary compass orientation, so neither is invented.

| Domain | Producer / owner | Native representation and operation | Plotted use |
|---|---|---|---|
| Source/request cell | Provider `0x14079f860`; source Grid/cell | Signed 32-bit Int2. Spatial lookup uses origin subtraction and cell bounds. Current descriptor conversion `0x14078d660` joins requests to chart/body-face geography. | Source coordinates are tabulated; request cells are not pasted onto a world-XYZ grid. |
| Body-face geography | Manager descriptor and source geographic record | Chart plus integer fine-cell coordinates. Qualified interior chart 0 for both reference sites. One fine-cell displacement is 100 native units under this source contract. Geographic projection is a different transform. | Supplies saved-site/source joins only in the qualified same-chart frame. No seam/wrap or geographic grid overlay. |
| Generator origin | Provider `0x14079feda..0x14079fefb` | Source anchor minus padding, times 100, binary32 conversion and floor to Int2. Source origin is not outpost centre. Packed seed arithmetic uses the actual origin operands, not a plot translation. | Frozen C1 historical-frame geometry is preserved; no prospective-source renormalization. |
| Generated region | Wrapper resource map → collection → 48-byte region | Binary32 bound XYZR, count and ordered 16-byte XYZW points. W is width, not homogeneous position. Owned copied geometry lives under the ProcGen source wrapper. | Original values stay in C1 JSON; D5V records hashes, layer IDs and exact input references. Continuous silhouette has disclosed marginal rounding limits. |
| Saved site-local centre | Historical saved representation `0x2b` | Binary32 local XYZ; separate site S and descriptor O. Zero saved Workshop compensation qualifies beacon equality in these two representations only. | Independent frame/projection CSVs verify the original bytes and descriptor-frame reconstruction. |
| Native compensated centre | `0x140f4ab80` | Starts with reference `+0x8c/+0x94`; qualifying ExtraWorkshop adds `+0x60/+0x64/+0x68`. It is not universally the visible beacon's current position. | Saved zero-compensation join is labelled historical; no present loaded equality is claimed. |
| Workshop area | Descriptor builder `0x140f4a140`; updater `0x1421e07d0` | Indexed binary32 XYZ, u32 index and domain pointer; radius and upper scalar separate. Callback adds the current 12-byte translation at index when in range. | Supplied model query is already in the geometry comparison frame. Current loaded translations are not recovered or guessed. |
| Extractor candidate | `0x140f7c390..0x140f7c408` | Raw reference XYZ copied into `0x14079df70`; `0x142346b30` compares query XY with resident region geometry. No indexed translation at this edge. | Tests supply explicitly same-frame model coordinates. No actual saved extractor or loaded candidate position is overlaid. |
| SVG display | D5V renderer only | Native data/axes remain absolute descriptor-frame X/Y. Subtract viewport xmin/ymax, scale and invert Y only to obtain SVG pixels. | Explicit inverse, absolute ticks and centre labels, full 150-unit circle and source-input hashes. |

The candidate path itself establishes the comparison contract: resident geometry
and raw candidate XY are the operands used together by the original native point
predicate. It does not supply an arbitrary saved/current-frame conversion.
Thus a current reference from another origin epoch cannot be overlaid just by
matching its body or assuming translation index zero means zero translation.
D5V avoids that join entirely; its consumer comparisons supply the same qualified
historical descriptor frame to both original predicates in an offline fixture.
No mandatory diagram purports to recover an unobserved current position.

## Independent historical join

Read [saved centre/frame](../static-exhaustion/saved-center-frame.csv) and
[durable-centre projection](../durable-center/projection.csv), sample HIST-0267,
tokens `83388f` and `84e101`. Tokens are serialized identifiers, not FormIDs.
These tables were authored independently of D5V and the native area evaluator.

For local saved centre L, site cell S and manager descriptor O:

```text
Cxy = float32(Lxy + 100 × (S − O)); Cz = Lz
source_anchor = 100 × (A − O)
generator_origin = source_anchor − (200,200)
```

| Case | Descriptor O | Site S | Local Lxy | Descriptor-frame Cxy |
|---|---|---|---|---|
| Cu Co Ni IL | 25152,32448 | 25124,32446 | 83.460693359375,67.88771057128906 | -2716.539306640625,-132.11228942871094 |
| Cu IL F | 37536,20928 | 37536,20928 | 81.19074249267578,90.27748107910156 | 81.19074249267578,90.27748107910156 |

The independent centre-byte comparison is exact. Both Workshop compensation
vectors are zero; beacon = compensated centre is therefore qualified in those
saved representations. Primary source anchors U01–U04 are `(-3600,-1200)`,
`(-3600,0)`, `(-2400,-1200)` and `(-2400,0)`, distinct from C. Their generator
origins subtract `(200,200)`. [Coordinates](d5v/coordinates.csv) retain all
included layer values. No source anchor is drawn at the beacon by convenience.

This join uses the original frozen historical-frame geometry. C1's U01 example
has 30 historical-frame paths versus 28 in a normalized prospective generation;
changing packed seed operands is not an SVG translation. D5V preserves both
histories and does not regenerate or relabel one as the other.

## Radius, height and border

The ordinary installed beacon ACTI `0x002c60e9` has OutpostBuildAreaRadius AV
`0x00063fc5` value 150, selected through DFOB `0x00063fc6`.
[L3's definition/native evidence](../spatial-placement/native.md) and D5V's
fresh `0x140f38e30` export qualify this selection. Its fallback setting is 71.4,
not 150; effective data/property overrides can change it. Descriptor radius is
`+0x28`; mode 2 membership is horizontal radius plus a separate upper-height
test through `0x140f4ac50`. The generated-region callback has additional branches.

Every D5V outpost panel shows the full **150-native-unit default radius** about
the verified historical centre. It is a conditional ordinary build-radius
reference and the fixed research query disk, not a recovered effective saved
hardware boundary. Native border drawing can clip to location/POI eligibility.
Neither a terrain outline nor an exact current usable border is overlaid.
Model upper values are `float32(Cz+100)`, inherited from the C1 supplied query;
they are not measured current effective height limits.

## Display transform and controls

Both outpost figures use absolute native descriptor-frame X/Y. Their detailed
480-pixel panels span `[Cx−240,Cx+240] × [Cy−240,Cy+240]`, at one pixel per
native unit. These bounds are absolute coordinates; the centre is never a
data-coordinate `(0,0)`. Two full-extent companion panels use a common square
extent encompassing every displayed native region bound, with a 40-native-unit
margin. The two outposts need different viewports because their native centres
differ. Comparison panels within each outpost/view use identical bounds/scale.

Let `(xmin,xmax,ymin,ymax)` be the native viewport, `(t,l)` its pixel top/left,
and `s=480/(xmax−xmin)` pixels per native unit. For native point `(x,y)`:

```text
u = l + (x − xmin) × s
v = t + (ymax − y) × s
x = xmin + (u − l)/s
y = ymax − (v − t)/s
display_radius = 150 × s
```

The circle has 90 native units of margin in each detailed view. Deposits beyond
that zoom are deliberately clipped there and shown fully in the lower panels;
every displayed native region bound fits inside those full-extent viewports.
Native bound clipping of each deposit is retained as part of its supplied shape.
X increases right and native Y increases up; no compass or metric conversion is
asserted. Integer native tick labels remain absolute. Adjacent centre labels
round to three decimals for reading; exact binary32 centre values remain in JSON
and the figure header. This rounding does not change marker position.

The renderer serializes primitive pixel coordinates to nine decimal places.
Independent controls use exact centres/beacons, four cardinal radius points,
corners and every supplied displayed deposit point/bound centre. Unrounded
round-trip tolerance is `1e-9` native units; serialized-pixel tolerance is
`0.5001e-9/s + 1e-9` native units. The correction's check receipt and report
retain actual errors, visible tick checks and byte-identical SVG replay.

IRES TINC colors are inherited unchanged from C1's pinned palette. Silhouettes
use endpoint disks and max-width consecutive rectangles, clipped by native bounds;
quaternion/transcendental and marginal segment rounding remain approximate.
Finite native callback and point controls validate their tested membership
predicates, not an exact continuous pixel boundary or screenshot identity.

The coordinate/lifecycle diagrams are explanatory schematics and have no spatial
scale. They must not be mistaken for native object layouts or gameplay maps.
