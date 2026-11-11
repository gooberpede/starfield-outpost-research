# Planetary location and position reference

[Guide](../guides/position.md) · [Glossary](glossary.md) ·
[Selected claims](../history/claims.md#position)

## Saved coordinate joins

| Domain | Representation and role |
| --- | --- |
| Body | Installed PNDT FormID in a qualified content namespace. Join the typed saved world component's system/body pair to installed PNDT GNAM. A body or its name does not identify one site. |
| Reference and worlds | Qualified saved beacon record → parent site world → secondary generated-world descriptor, using typed relations. A fixed POI world can supply a separate landmark. Save-local world/reference tokens can remap. |
| Saved site anchor | Associated geographic longitude and latitude as doubles in radians, longitude first. A qualified projection can recover an anchor cell. An anchor and the occupied cell can differ. |
| Source origin | The terrain descriptor's packed key holds low 16 bits X, next 16 Y, 3 tag bits, 6 body-index bits and 18 system bits. Reject reserved or unsupported fields. This anchor is an origin for the supported source frame and distinct from a deposit generator's source anchor. |
| Initial XYZ and Workshop centre | Ordinary case-5 inline reference data supply local XYZ `P`. The Workshop compensation vector `D` is read from ExtraWorkshop. The qualified saved centre is `C = f32(P + D)`, componentwise, with a bit-preserving copy when the entire vector compares zero. |
| Indexed XYZ | A native consumer can translate coordinates into the indexed context it actually selected. Its origin, caller and lifetime must be qualified. Saved local XYZ or a source anchor alone cannot supply those operands. |

[Save39 typed joins and decoded offsets](../experiments/coordinate-sufficiency/saves.md) ·
[Specification and accepted review](../position-model/review.md) ·
[Resource source/frame proof](../experiments/resource-retained-population/d5u-c1-coordinate-validation.md).

## Qualified conversion

1. Decode the supported descriptor under the pinned 1.16.244.0 model.
   Convert tags 2/3 from packed coordinates by reflecting **both** axes
   with `49151 - index`. Tags 0/1 copy. This is separate from terrain
   pattern orientation.
2. Select the native descriptor origin for saved frame `0x0b`. For
   `0x2b`, require the qualified site base with tag 0 or 1. If absent,
   keep the centre and local residual and report the cell as unknown.
3. On each horizontal axis compute `q = floor(f32(C * f32(0.01)))` and
   `r = f32(C - f32(100 * q))`. Retain binary32 order and negative floor.
   Use the supported numeric range and round-to-nearest environment.
4. In the chart interior, add `q` to the base. The full v2 model uses
   signed C remainders modulo 49,152, wraps crossings and XORs the tag
   by 1 for X, 3 for Y or 2 for both. Repack using the resulting tag.
   The hierarchy is `192*coarse + 12*middle + fine` per axis.

The cell-centre inverse gives a display angle under the hemisphere-square
model. In that body frame, +X defines zero longitude and +Z the positive
pole. Subcell phase, compass/texture calibration and metre conversion
remain unestablished. Local Z stays in native local units.
[Exact arithmetic, exceptional cases and numeric assumptions](../experiments/position-resumption/algorithm.md) ·
[Accepted Kreet coordinate review](../experiments/coordinate-sufficiency/review.md).

## Saved descriptor-frame comparison

For the historical resource comparison, let `S` be the qualified saved site
cell, `O` the saved descriptor origin and `L` the compensated centre in saved
frame `0x2b`. For the validated interior cases with equal charts, compute
`Cxy = f32(Lxy + 100 × (S − O))` in descriptor-frame native units and
retain `Cz = Lz`. A resource source at fine-cell anchor `A` has a
descriptor-frame offset `100 × (A − O)`. The padded generator origin is
another offset. This saved-frame translation does not identify the loaded
manager edge or preserve a procedural seed when substituted for the original
generator operands. The control covers seven saved joins, without seam or
rotation equivalence.
[Authenticated coordinate proof](../experiments/resource-retained-population/d5u-c1-coordinate-validation.md#equations-and-units) ·
[Generation input frames](resource-generation.md#generation-inputs-and-frames).

## Loaded centre and regional repeatability

The historical 050 comparison captures 40 horizontal grid calls across two
Kreet Workshop geometries, including nonzero XY and a hierarchy carry.
Translated XY/grid agreement is conditional. Raw 050 XYZ disagrees with the
saved XYZ. The 060 setters and sampled centres match at different boundaries,
with zero calls at the 050 comparison site. A prior-site centre can also
remain during transition. These observations leave the frame/writer/epoch
join and general loaded XYZ unknown. Synthetic reflected and seam branches
exercise arithmetic, with no equivalent retail Workshop seam control.
[Capabilities](../position-model/capabilities.md) ·
[Cross-session counterexample](../experiments/cross-session-center/report.md).

The base terrain table is built from the body inputs, configurable surface
seed and an **ordered** registered pattern population filtered by style.
The separate Planet Content Manager seed can vary. The native dependency
trace supports ordinary region repeatability given the same definition
order, style relationships, load order and terrain settings. It supplies
no measured fresh-character or landing-selection result.
[Repeatability trace](../experiments/coordinate-sufficiency/repeatability.md) ·
[Review of the candidate-population correction](../experiments/coordinate-sufficiency/review.md#independent-review-history).

## Inspect and challenge

Take Save39's beacon XYZ from the tracked [positions table](../experiments/coordinate-sufficiency/positions.csv)
and its zero compensation and descriptor origin from the [controlled saves](../experiments/coordinate-sufficiency/saves.md#regional-test-matrix).
Apply the binary32 multiply and floor above. Adding (10, 11) to (14304, 12768)
gives (14314, 12779). The reported residual is (88.759765625, 79.728515625)
local units. This recomputes the tracked held-out example. Compare the mature
negative-X frame-`0x2b` counterexample in the [original report](../experiments/coordinate-sufficiency/report.md#quantitative-sufficiency-and-actual-limits)
and its [review](../experiments/coordinate-sufficiency/review.md).

**PUBLICATION DEPENDENCY — EVIDENCE ACCESS PENDING** for original-witness
verification of historical loaded-centre comparisons and the broader frozen
position set. The reported calculations are inspectable. Source replay
requires lawful pinned inputs and the recorded extraction method. Selected F1
controls remain **PENDING RELEASE** and cannot supply a historical runtime
epoch. [Reader access and limits](../reference/evidence-access.md).
