# D5AT ordinary Grid and request preparation

Under the fixed `D5AT-GRID-PREWARM-0` inputs, Feynman VI-b source
`0:29568:10944:0006ce56` and the three leading Feynman VIII-b sources retain
all 196 padded coordinates in the completed Grid. The density and layer
registration sets each cover those same coordinates. The same trace yields
only 56 registrations per family for two adjacent VI-b sources despite their
196 retained coordinates. Grid coverage and registration coverage can differ.

| Saved site and selected SFBK | Descriptor anchor | Source anchor | Grid / density / layer | Mask counts in each registered family |
| --- | --- | --- | --- | --- |
| VI-b `0x0006ce56` | (29568, 10944), chart 0 | (29568, 10944) | 196 / 196 / 196 | `0x0` 144, `0x8` 52 |
| VIII-b `0x002c17d5` | (38112, 960), chart 1 | (38100, 960) | 196 / 196 / 196 | `0x0` 28, `0x3` 168 |
| VIII-b `0x0029d211` | Same VIII-b frame | (38112, 960) | 196 / 196 / 196 | `0x0` 28, `0x3` 168 |
| VIII-b `0x002c17d3` | Same VIII-b frame | (38124, 960) | 196 / 196 / 196 | `0x0` 28, `0x3` 168 |

The VIII-b sources at X 38100 and 38124 have native request X ranges
([-14,-1]) and ([10,23]) respectively. The arithmetic uses the saved
descriptor as the scenario's consumed descriptor, rather than resetting
each source anchor to zero. The face-cell identity is preserved and checked
against the existing D5AT atlas results. The leading VI-b source is from SFPT
`0x000c7ab4`, BIOM `0x000c5718`. The three VIII-b keys share SFPT
`0x0026f7ef` and BIOM `0x000fc61a`. All four have 10 by 10 nominal and
14 by 14 padded dimensions. D3's competing VIII-b blocks at X 38100 and 38112
are absent from those anchor entries in the D5 installed-main selection.

## Native boundaries and replay inputs

Addresses are preferred static VAs for the pinned 1.16.244.0 PE, image base
`0x140000000`. Source IDs and signed request Int2 coordinates have separate
domains. The method checks 25 retained function entries and their PE ranges,
plus the short X/Y edge getters. The native chain below uses the existing
[D5H function and export register](../resource-query-reachability/native.csv)
and [D5S preparation trace](d5s-query-winner-model.md).

1. At `0x1407847b0`, the ordinary Grid uses terrain width 100 and a margin
   of 50 on each side under the D5S defaults. Use initial Grid bounds
   ([-100,100)` on both local axes. At `0x1407862a0` and `0x140982d90`,
   ordinary installed tile entries supply the anchor and dimensions.
   Assume a single collection of every contributing main-file tile, no
   overlay replacement and successful allocations. Scan the complete
   installed tiles that can contribute, using the corpus maximum SFBK
   dimensions and the strict padded bounds.
2. At `0x1409832e0`, fill, edge and corner insertion select different cell
   layouts. The setters keep occupied slots. The replay checks distinct
   slots before claiming order-independent retention. Mixed edge and corner
   cells need the conversion at `0x140986080`. The retained edge getters
   at `0x140988380` and `0x140988540` read opposite-side slots by selector,
   and the converter transfers each edge pointer to two corner slots. An
   edge arriving after the corner calls its setter directly and populates
   the same two slots. The `0x140988760` emitter calls `0x140988ab0` once
   per nonzero slot. That helper appends directly without a source-identity
   check. The receipt preserves emitted order and repeated pointer entries.
   The first pass left 248 rows unresolved before this
   conversion was checked. The corrected run finds no contested slots in
   the current 77 matching-source traces. Unsupported layouts and competing
   source pointers still fail closed.
3. With mode 2, valid focus zero, valid context and the fixed D5S defaults,
   `0x1407b30c0` and `0x1407b2390` give inclusive local prewarm bounds
   `[-16,23]²`. The detached preparation path validates the captured generation
   triple and reaches `0x1407af970` after ContentManager preparation.
   With cold keys and ready file inputs, `0x1407b4bb0` registers density
   neighbors and recursively visits in-bound layer coordinates. The replay
   matches the retained D5S order for all 1,600 layer and 1,720 density keys
   and checks the density set by independent set union.
4. For the density path, `0x1407a1940` can forward the original Int2 to
   `0x14079f860`. Layer reaches that provider after its separate
   `0x1407a0fa0` preparation inside `0x1407b5160`. Grid lookup uses the
   completed table at `0x140985870`. The receipt intersects retained cells
   with each registered family separately. Registration alone supplies no
   evidence of provider entry, sampled mask or first-miss success.

## Survey-wide comparison

The same input contract covers the 17 sites with supported saved descriptors.
Of 142 candidate relations, 77 match the selected D5 main-file anchor and
block, 56 differ in block, and nine have no defining anchor at the exact
slot. The 65 alternatives remain in the original ranking and are explicitly
dispositioned in the [Grid registration table](d5at/grid-registration.csv).
Within the scenario, the 77 matches retain 18,932 source-coordinate pairs.
Their density and layer intersections contain 14,182 and 14,012 pairs,
respectively. A request emitted by multiple sources contributes once per
source. Twenty source density cohorts are narrower than their Grid support,
and ten source density and layer cohorts differ. Zero registrations are
possible even with retained Grid support.

The independent auditor reopened the pinned `Starfield.esm`. It transposed
the complete serialized FNAM/GNAM arrays of 25 SFPT records and compared
394 defining SFBK DNAM dimension pairs to the normalized corpus. All fields
matched. This verifies the compared slots and dimensions of the installed
main file. Tile selection still uses the authenticated D5 corpus.
[Native SFPT installation layout](../resource-owner-root/source-layout.md).

Save52 supplies neither the loaded VI-b or VIII-b manager mode, descriptor
and focus nor the completed preparation bounds and original registered keys.
The saved descriptors are inputs to this controlled scenario. The result
does not identify an actual visit cohort or determine construction-winner
probabilities. The D5I direct-cell witnesses remain distinct from the prewarm
scenario. Existing snapshots qualify resident source/frame/geometry
attribution within their own capture conditions. They lack registration and
request-preparation evidence.
[Save52 state classifications](d5ad-save-state-matrix.md) ·
[D5I direct-cell evidence](../resource-query-variability/proofs.md) ·
[Snapshot producer](d5as-producer-profile.md).

## Reproduction

Run [d5at_grid.py](../../../research/resource-retained-population/d5at_grid.py)
with a fresh ignored JSON path using the pinned Python with `-E -B`.
Run [d5at_grid_audit.py](../../../research/resource-retained-population/d5at_grid_audit.py)
with that JSON and a fresh summary CSV path. The audit independently resolves
each main-file slot by anchor, reconstructs competing contributors and
emission order, joins the descriptor to the frozen Save52 case, reconstructs
both registration sets and recounts every histogram. It rejects a forged
emission, a substituted descriptor and a corrupted mask. The detailed receipt and
proprietary inputs stay local. Neither script launches the game or executes
game instructions.
