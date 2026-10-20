# Controlled saves and local numerical checks

2026-10-20. SOR-EV-0066. [Full selected matrix](positions.csv), [input hashes](inputs.csv), [local primary receipts](evidence.md). Decimal offsets are decoded logical save-stream offsets. Tokens are tagged save identities before load remapping; they are not pointers or cross-game IDs.

| Sample / role | Token / parent | XYZ in saved local units | Frame / meaning |
|---|---|---|---|
| Save37 player | `400014 / 725868` | `(950.5491333007812,782.48193359375,43.021602630615234)` | shape `0x14`; fixed WRLD `00325868`; reported Lab fast-travel baseline |
| Save38 player | `400014 / 81482d` | `(1087.2198486328125,1180.0147705078125,-19.421180725097656)` | shape `0x14`; generated Kreet source world; no detected ordinary beacon |
| Save39 player | `400014 / 839160` | `(1087.2198486328125,1180.0147705078125,-19.421165466308594)` | shape `0x14`; new site world linked to source `81482d` |
| Save39 beacon | `841421 / 839160` | `(1088.759765625,1179.728515625,-18.834455490112305)` | ordinary case 5, frame `0x0b`, ACTI `002C60E9`, zero compensation |
| Save25 SOR-002 | `822821 / 822834` | `(122.70045471191406,273.0462341308594,18.352506637573242)` | frame `0x0b`, source `8147f8`, zero compensation |
| Save25 SOR-003 | `84b985 / 84b996` | `(356.8204040527344,2459.05859375,-31.89084243774414)` | same source/frame; distinct site and Workshop identity |

Save38→39 player XY bits agree exactly. Z differs by `0.0000152587890625`; do not silently call full XYZ identical. Beacon minus Save39 player is `(1.5399169921875,-0.2862548828125,0.5867099761962891)`: horizontal 1.56629697, full separation **1.67257729 local units**. Both have the same saved site parent. This supports the user's close-placement control, not zero separation or a calibrated metre statement.

Save39's beacon record is `[1355959,1356294)`; XYZ starts 1356036. Its site angular pair starts 216256, repeated-parent tuple starts 216250. The typed world component is at 278737, secondary `81482d`, system 88327/body index 15, resolving to Kreet PNDT `0003F59F`. Descriptor starts 3890; key `02b20e7831e037e0` gives chart 0 / `(14304,12768)`. The Workshop identifier bytes are `41da48765780cc0c`; compensation begins 1356082 and is all zero. The selected matrix and actual primary receipt control these offsets.

Save37/38/39 retain that same source descriptor and active-context key; checksums differ and are not treated as geographic IDs. Parent changes across fixed/source/site worlds are explained as distinct saved associations. Source-compatible subtraction across the fixed/generated boundary is a scoped numerical comparison, not independently measured loaded-frame equality.

## Construction identity and churn

The supported ordinary detector finds 0/0/1 beacons in Save37/38/39. This is a positive scoped result, not an exhaustive active-outpost census. Save39 has one supported constructed PACKIN root `ff041428`, six serialized members, explicit owner beacon `ff041421`, base `Starfield.esm:0015804`, construction definition `0029a8c6`. Its root XYZ equals beacon XYZ. The reciprocal/native root representation comes from the existing [Workshop membership](../workshop-membership/report.md) and [population](../workshop-population/README.md) readers. Loaded defaults and unhandled representations remain outside this projection. No save-wide byte-difference count is used to infer gameplay causality; player/world association and the new explicit root are compared by typed identities.

## Regional test matrix

| Control | Descriptor origin | qXY | Anchor cell | Result |
|---|---|---|---|---|
| Save39 new holdout | chart 0 /14304,12768 | 10,11 | chart 0 /14314,12779 | exact integer agreement; residual 88.759765625,79.728515625 |
| Save25 SOR-002 | chart 1 /10464,21120 | 1,2 | chart 1 /10465,21122 | exact integer agreement |
| Save25 SOR-003 | same | 3,24 | chart 1 /10467,21144 | exact integer agreement; delta 2,22 |
| Kreet fixed Lab | independent PNDT entry | not a beacon offset | chart 0 /14312,12774 | both native-order AVX/FMA diagnostic candidates agree |

The angular-to-square center residuals for the three beacon pairs are below 0.0002 cell on both axes; the boundary is roughly half a cell away. This is numerical reconstruction error, not physical surveying error. Both diagnostic dispatch candidates recover the same indices. Native scalar-cos/FP-environment equivalence remains unmeasured, with no consequence demonstrated for these comfortably interior samples.

Prior held-out Jemison/Akila/Mars fixed anchors were freshly reread and diagnosed with the same constants; their indices are in [fixed-controls.csv](fixed-controls.csv). These check fixed-anchor projection, not ordinary beacon offsets. The old [25-row audit](../exact-beacon/matrix.csv) and [v2 counterexamples](../position-resumption/algorithm.md) retain broader scope and exclusions; this task does not silently reclassify them.
