# D5T Feynman V outpost 2 ordinary outcomes

**Exactly two ordinary geometry outcomes are possible within the frozen D5S
normal-arrival contract.** The complete native ordered populations contain
74 regions for O0 and 78 for O3. All admissible constructing winners map to one
of these outcomes. This is an exhaustive outcome census, not an exhaustive
enumeration of which individual queries can win a schedule, a retail frequency
estimate, or a reconstruction of the historical outpost's generation.

| Outcome | Ordinary mask | Effective weights: Ionic Liquids / Fluorine / Copper | Native retained regions in that order | Proven winner: original Int2 → body-face cell |
|---|---|---|---|---|
| [O0 map](d5t/O0.svg) | 0 | 0.05000000074505806 / 0.20000000298023224 / 1 | 2 / 15 / 57 | `(-2,-2)` → `(37534,20926)`, D5S peer continuation |
| [O3 map](d5t/O3.svg) | 3 | 1 / 1 / 1 | 25 / 35 / 18 | `(10,11)` → `(37546,20939)`, D5S owner continuation |

Open the [comparison SVG](d5t/comparison.svg) for directly comparable deposit
shapes. [Geometry JSON](d5t/geometry.json), [candidate table](d5t/candidates.csv),
[catalogue and proof](d5t/catalogue.md), [active ledger](d5t-investigation-ledger.md)
and [source ledger](d5t-sources.csv) support review. The
[review record](d5t-review.md) controls independent acceptance and exact delivery.
Scientific questions D5T-CQ and Q1–Q4 have COMPLETE scoped answers; acceptance
still requires that record's exact-snapshot independent disposition.

## Q1–Q3: outcome count, determining inputs and equivalence

Let S contain all integer original queries in `[-2,12) × [-2,12)`. Every
admissible winner A lies in S: the primary Grid's target-bearing interior,
edge and corner cells occupy only the nominal 10×10 source plus its two-cell
padding. Both density and layer routes pass their original query to the same
provider. Retention, arbitration and cold-map requirements can remove candidates;
they cannot emit this source outside that support. The
[catalogue proof](d5t/catalogue.md) identifies the decisive native paths.

Fresh conversion and raster evaluation cover all 196 members of S. The 28 queries
with Y equal to -2 or -1 sample mask 0; the 168 with Y from 0 through 11 sample
mask 3. X ranges from -2 through 11 in both groups. Both qualified arithmetic
branches agree at every sample. These counts describe support candidates,
not scheduling probabilities or counts of independently proven winners.

The query affects ordinary construction through its sampled mask and effective
weights. Source identity, frame, source-derived origin/clip, owner/body/system,
ordered effective definitions, cell/key inputs and successful allocation are
fixed. Ordinary construction contains no further query-dependent selector.
The complete determining-input contract is retained in each JSON outcome;
query coordinates are not substituted for origin-plus-cell seed operands.

Consequently the exact equivalence classes are `A intersect M0` and
`A intersect M3`, where M0/M3 are the explicitly enumerated mask subsets of S.
Each class is nonempty because D5S proves one feasible continuation in each.
Complete native geometry distinguishes the two classes. This establishes both
an upper bound of two and a lower bound of two, rather than inferring outcomes
from unequal weights. Every same-mask admissible winner has identical fixed
native operands and therefore identical ordinary geometry. Exact individual
membership in A is not enumerated; the other 194 rows retain conditional
eligibility, rather than being called feasible or excluded.

## Q4: visual meaning and fidelity

The three SVGs use X right, Y up, nominal source anchor `(0,0)`, native units,
common extents -500 through 1200 on both axes, and 0.4 pixels per native unit.
They show the **generation-competition footprint**: positive-width endpoint
disks and consecutive rectangles using the larger endpoint width, intersected
with each retained native bound disk. These are shaped deposits, not bounding
rectangles. Every retained path is represented; display bounds crop none of
their primitives. The source's candidate-point clipping remains part of native
generation; no extra source-box polygon clipping is imposed on the maps.

Native points and bounds are exact binary32 results exported losslessly as JSON
numbers. Continuous segment vertices use binary64 normalization; SVG boundaries
do not reproduce the native atan2/quaternion and binary32 predicate's marginal
rounding. This limited boundary approximation is explicit in every map and the
schema. Native point tests at endpoints, far controls and segment midpoint offsets
0, 0.5, 0.9999, 1.0001 and 1.5 times the larger width agree in all 1,630 probes.
This challenges both sides near segment edges without claiming exhaustive
boundary equivalence. Finite point tests do not prove every boundary point.

The maps are not tapered Workshop-strip availability, terrain texture, height,
full scanner/UI admission or an outpost boundary. No beacon position is supplied
by the fixed source contract. Actual rendered terrain and historical loaded-cache
correspondence remain unmeasured. The [geometry guide](d5t/geometry.md) documents
the separate spatial products and exact rendering rules.

Fresh installed IRES TINC values supply the colors: Ionic Liquids `#4cd7bb`,
Fluorine `#2f7869`, Copper `#275549`. The loader converts successive low bytes
into three channels at offsets `0xe0`, `0xe4`, `0xe8`. SVG uses those bytes
directly at full opacity; no fallback resource palette is used. Brightness
distinguishes the three related tints. This does not claim calibrated display
color management or identical in-game shading.

All three SVGs were rasterized and visually inspected with the bundled standalone
sharp/libvips renderer. Titles, counts, axes, source markers, shapes and legends
are readable, and frames agree. Browser-based inspection was stopped by Computer
Use's URL-verification guard; no further UI interaction occurred. Rasterization
emitted font-cache-directory warnings but produced complete readable images.
The renderer version receipt and PNG previews remain local.

## Native evidence and validation

The [native harness](../../../research/resource-retained-population/d5t_native.py)
extends the owned D5S disposable fixture. Original instructions execute cell
generation, RNG, chance/count/walk, clipping, earlier-different-resource competition,
native bounds and destination deep copies. Fixture callbacks provide previously
qualified packed keys, preallocated resource collections and successful storage;
temporary deallocation is suppressed inside the disposable process. No installed
instruction or running game is modified. The real competition consumer executes
its segment/trigonometric branch, with the pinned host CRT atan2f import.

Each population traverses 144 cells for each of three resources, in native
resource/X/Y order. O0, O3 and O3-repeat execute 1,296 cell calls. Complete retained
points and bounds exactly match the independent planar model in both outcomes;
the repeat is identical. Fresh replay and
[controls](../../../research/resource-retained-population/d5t_controls.py)
qualify the retained evidence. A checksum establishes byte identity, not geometry
semantics; the point/bound comparisons and native spatial tests supply the latter
within their stated coverage.

Comparing complete resource-tagged paths gives two shared Ionic Liquids paths,
zero shared Fluorine paths, and seven shared Copper paths. O0-only counts are
0/15/50; O3-only counts are 23/35/11. Equal Copper weight does not imply equal
Copper geometry: earlier-resource competition changes its surviving walks.
Paths are compared by resource plus complete ordered points; distinct paths are
not a claim that their spatial areas are disjoint.

The initial inaccessible Python alias and import-path failure are preserved.
An early setup error wrote every resource DNAM block at byte offset 400 and
incorrectly produced no later-resource regions. It is retained as an invalid
fixture attempt, not a negative result. The corrected native selection is
`40*(rarity+7)`, at offsets 400, 320 and 280 for these resources. Primary accepted
results are `native-full05.json`; failed attempts are not substituted into them.

## Scope, safety and disposition

The unchanged [brief](../../implementation-briefs/CODEX_BRIEF_SOR_RG2_D5T_feynman_v_outpost2_variant_enumeration_visual_mapping.md)
and [D5S contract](d5s-query-winner-model.md#normalized-arrival-contract) govern
this result: source `0:37536:20928:0029d20e`, Feynman V `0x0005e0de`, system
86469, body index 5, chart 0, descriptor `(37536,20928)`, BIOM `0x00145440`,
fixed main definitions/default settings without overrides, resident prerequisites,
cold target map/visited state, healthy queues, successful allocation and no shift,
reset or cancellation during construction. Ordinary resource order is Ionic
Liquids `0x000057d4`, Fluorine `0x000057d0`, Copper `0x000057cf`, with numeric
rarities 3/1/0. Special, Everywhere, Atmospheric and Water products are outside
the claimed ordinary census.

Fresh executable/data identities match D5S: Starfield.exe 1.16.244.0
`7e9adb1414a8e1b325e5e1f097b9b17b78deb7eebeda37a333351a43a60f9d28`,
Starfield.esm `1dabed00c3f4282dd3bb54d2e9601e40b577d8742d078b7ccef203adbfef0da7`,
PlanetData `2fb1fff5d8fc074718bf05022c099f3c87ef70e00050229b368ae7d680fbe5d5`.
Native addresses here are preferred static VAs at image base `0x140000000`.
All 15 existing database pins are preserved; Ghidra runs use `-readOnly -noanalysis`.
The 40,000,000,000-byte floor applies separately to C: and D:.

The conditional save gate was not triggered: the provider, source and ordinary
writer paths account for the consequential inputs in executable/static data.
No indispensable missing persisted selector was demonstrated. No save was opened,
decoded, loaded or modified. This does not establish that all relevant state is
absent from saves.

Scientific confidence is strong within the compiled fixed-input scope; outcome
coverage is exhaustive there. Engineering integrity, independent acceptance and
publication eligibility remain separate. Authored derivatives are REVIEW-REQUIRED;
raw code/data and local receipts stay LOCAL-ONLY. D5R's broader question remains
OPEN, D5P retail/plugin remains NO-GO, and B6/publication remain ON HOLD. No game,
attachment, deployment, protected-input change, external disclosure, staging,
commit or push occurred. This package awaits maintainer critical review.
