# D5U-C1 outpost composite maps

These seven maps place all qualified ordinary source contributions in a common
outpost frame, with the authenticated saved native centre, saved beacon
correspondence and fixed 150-native-unit research disk. Geometry uses frozen
historical-frame conditional models. Historical winner, loaded epoch, terrain
and final UI availability remain unknown. Special Helium-3, separate Water
admission and atmosphere are excluded. See [the report](../../d5u-c1-report.md),
[coordinate proof](../../d5u-c1-coordinate-validation.md),
[source provenance](../../d5u-c1-sources.csv) and [review](../../d5u-c1-review.md).

| Recorded outpost | Composite | Exact geometry/reference data | Source coverage |
|---|---|---|---|
| Feynman V Cu Co Ni IL | [D2-83388f](D2-83388f.svg) | [JSON](D2-83388f.json) | U01–U04; all four observed resources intersect. |
| Carinae III-a Rc Fe | [D2-82be17](D2-82be17.svg) | [JSON](D2-82be17.json) | U05–U08. |
| Arch III W H2O Lub | [D2-81a75b](D2-81a75b.svg) | [JSON](D2-81a75b.json) | U09–U12; corrected component/slot model. |
| Feynman VI-b Al Be He3 | [D2-81bf2a](D2-81bf2a.svg) | [JSON](D2-81bf2a.json) | U13–U16 + C1-X01/X02. |
| Feynman VII-b Nd Al He3 | [D2-825f95](D2-825f95.svg) | [JSON](D2-825f95.json) | U17/U18 + C1-X03–X06. |
| Feynman VIII-b Au Sb | [D2-844cc6](D2-844cc6.svg) | [JSON](D2-844cc6.json) | U19–U21 + C1-X07–X09. |
| Feynman V Cu IL F | [D2-84e101](D2-84e101.svg) | [JSON](D2-84e101.json) | U22–U25. |

The [coordinate diagnostic](coordinate-join.svg) shows why a historical circle
can be a reference on prospective source geometry without making that geometry
a historical replay. U01 has 30 frozen historical-frame paths versus 28 in its
normalized prospective native output. The original [source gallery](../README.md)
retains all 26 support figures and selected prospective native-generation maps.
U26 has no associated outpost and receives no disk.

The top geometry panel combines only invariant-source conditional contributions.
Every variable source has its own two alternative panels in the same outpost
frame. These are independent layers, not asserted joint initialization states.
For example, the first second-V panel is empty inside the disk because its
invariant sources contribute no positive area; U25's two panels below supply
Ionic Liquids, Fluorine and Copper. All zooms show `[-240,240]²` at one pixel
per native unit. Geometry outside the zoom is deliberately clipped; the full
disk is visible. Purple crosses/boxes are source anchors/nominal boxes, gray
crosses are generator origins, and the black circle/cross/diamond identify the
research disk/saved centre/saved beacon. Resource colors use IRES TINC.

## Backing tables and additional sources

- [coordinates.csv](coordinates.csv): all 34 source joins, native anchors/origins,
  source-relative centres, seed-frame keys and exact source round trips.
- [contributions.csv](contributions.csv): each independent source/mask/resource's
  retained paths, positive-area paths, unknown area and accepted/unknown callbacks.
  Repeated ordinary IRES slots retain their ordinals; resource totals are not
  double-counted. Zero-path placeholders are not interpreted as separate routes.
- [coverage.csv](coverage.csv): complete finite-halo source counts and exclusions.
- [primary-reconciliation.csv](primary-reconciliation.csv): the four historical
  observations, serialized extractor tokens, contributing sources and native controls.
- [map-manifest.json](map-manifest.json): exact SVG hashes, extents/scales,
  panel centres/radii, all displayed layer/source IDs and explicit viewport clipping.

The D5U comparative census was not an exhaustive per-outpost halo. These nine
additional frozen sources receive separate C1 IDs; U identities are unchanged.

| C1 ID | Outpost | Exact source key |
|---|---|---|
| C1-X01 | VI-b | `0:29556:10920:0006ce58` |
| C1-X02 | VI-b | `0:29568:10920:0006ce58` |
| C1-X03 | VII-b | `1:32136:15132:00298a44` |
| C1-X04 | VII-b | `1:32136:15144:00298a3c` |
| C1-X05 | VII-b | `1:32148:15132:002c2520` |
| C1-X06 | VII-b | `1:32148:15144:002c5875` |
| C1-X07 | VIII-b | `1:38100:972:002c17d3` |
| C1-X08 | VIII-b | `1:38112:972:0029d20e` |
| C1-X09 | VIII-b | `1:38124:972:002c17d1` |

## Deterministic reproduction

From the repository root, using the existing local CPython 3.14:

```powershell
$python = 'C:/Users/User/AppData/Local/Python/pythoncore-3.14-64/python.exe'
& $python -B research/resource-retained-population/d5u_c1_maps.py --output .local-work/d5u-c1/FRESH_MAP_DIRECTORY
& $python -B research/resource-retained-population/d5u_c1_checks.py FRESH_CHECK_DIRECTORY
```

The first command uses only delivered JSON and owned primitive-rendering code;
it reconstructs all eight SVGs and the manifest byte-for-byte. It requires a new
destination. The checks additionally require the retained C1 baseline, installed
identity inputs and local receipts; they do not regenerate procedural geometry
or execute native code. Renderer-only replay requires no game assets or saves.

To rebuild numerical derivatives from authenticated existing evidence, with the
C1/D5R leases, D5U census and independent authored controls already available:

```powershell
& $python -B research/resource-retained-population/d5u_c1.py
& $python -B research/resource-retained-population/d5u_c1_maps.py
```

This intentionally replaces only C1 authored numerical/map outputs. Preserve
reviewed snapshots before a scientific rebuild. It reads the exact lease members
listed in the source ledger, verifies independent coordinate controls, reuses
frozen historical geometry and recomputes area/callback derivatives. It does not
open a raw save, generate procedural populations or access a target process.
Missing or changed evidence fails closed; no download is attempted.

Local previews use the already bundled sharp/libvips renderer. The review record
lists renderer versions/warnings, inspected raster inventory, prose screening
and independent disposition. A successful render alone does not establish
scientific correctness or publication eligibility.
