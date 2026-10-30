# D5V native-frame lifecycle and consumer comparisons

[Report](../d5v-report.md), [coordinate contract](../d5v-coordinate-contract.md),
[source ledger](../d5v-sources.csv), [review](../d5v-review.md).

**D5V-C1 correction:** the figures now plot absolute historical native
descriptor-frame X/Y. The earlier centre-relative axes did not satisfy the
requested presentation. [Correction, controls and visual acceptance](../d5v-c1-report.md)
supersede that earlier D5V-AC6/AC7 acceptance; native geometry and resource
consumer findings are unchanged.

| Figure | Meaning and backing |
|---|---|
| [Native coordinate domains](coordinates.svg) | Native ownership/transform contract and separate reversible SVG display coordinates. |
| [Lifecycle and consumer boundaries](lifecycle.svg) | Static construction, retention, retirement/reset and distinct consumer operations. Schematic; no spatial scale or observed chronology. |
| [Feynman V Cu Co Ni IL](D2-83388f.svg) | Frozen historical-frame ordinary geometry versus regions accepted by the actual native area callback at the supplied centre/radius. Four resources, without changing geometry. |
| [Feynman V Cu IL F](D2-84e101.svg) | Separate U25 mask-0/mask-3 historical-frame alternatives. Both area resource sets are Copper/Fluorine/Ionic Liquids. U23 alternatives have zero disk intersection and are omitted; no joint winner is asserted. |

All deposit figures are **conditional historical-frame reconstructions**, not
screenshots, observed full populations or an actual before/after travel sequence.
Operator qualitative comparisons appear only as labelled annotations. Default
150-unit circles are full and centred on independently verified saved native
centres. Saved beacon correspondence requires the recorded zero compensation.
The labelled centre is `(-2716.539306640625,-132.11228942871094)` at the primary
site and `(81.19074249267578,90.27748107910156)` at the second site, in their
respective historical descriptor frames. Centre markers are not data origins.
Upper panels are detailed native-coordinate zooms; lower panels show all
displayed deposits without viewport clipping, at a shared scale within each
comparison. Viewport translation and SVG Y inversion affect pixels only.
Actual loaded translations, terrain, clipped POI borders, scanner rendering,
Special/Water/atmosphere and collision are not shown. U26 remains source-only in
the earlier gallery and receives no outpost association here.

[Spatial JSON](spatial.json) records original native centres, exact upstream
geometry paths/hashes, included layer IDs, transforms and SVG hashes.
[Coordinates](coordinates.csv) retain source anchors/origins separately.
[Consumer results](consumer-results.csv) report original native per-region area
and point tests on the supplied geometry. Point tests use the model beacon centre,
not actual extractor positions. [C1's full geometry](../d5u/outposts/README.md)
preserves complete ordered points/bounds and excluded alternative layers.
Resource colors remain IRES TINC. Continuous silhouettes retain C1's disclosed
marginal-boundary approximation; native predicate results do not come from SVGs.

From the repository root, with the existing CPython 3.14 installation:

```powershell
$python = 'C:/Users/User/AppData/Local/Python/pythoncore-3.14-64/python.exe'
& $python -B research/resource-retained-population/d5v_maps.py .local-work/d5v/FRESH_MAP_DIRECTORY
& $python -B research/resource-retained-population/d5v_native.py FRESH_NATIVE_RECEIPT.json
& $python -B research/resource-retained-population/d5v_checks.py FRESH_CHECK_DIRECTORY
& $python -B research/resource-retained-population/d5v_c1_checks.py FRESH_CORRECTION_CHECK_DIRECTORY
```

The renderer needs only delivered authored data and owned plotting code. Native
replay additionally needs the pinned local executable and existing D5V function
metadata; it runs selected original instructions in its disposable process with
documented fixture callbacks. Checks authenticate the frozen final receipt and
independent authored centre tables and replay SVGs. They do not launch the game,
load saves, alter analysis databases, install dependencies or access the network.
Raw native inputs/receipts remain local-only. Fresh destinations prevent accidental
overwriting of evidence. Independent review and publication gates remain separate.
