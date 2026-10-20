# Kreet Research Lab: fixed anchor versus marker

2026-10-20. SOR-EV-0066. [Report](report.md), [hashes](sources.csv), [offline method](evidence.md).

The exact reported anchor is independently verified in the currently installed ESM. PNDT `0003F59F / KreetPlanetData`, compressed record at **file offset 1402105313**, has a pre-BDST CNAM entry at **decoded PNDT payload offset 38856**. Its disk order is **latitude binary64, longitude binary64, WRLD uint32**, little endian:

| Field | Value |
|---|---|
| Latitude | `+0.4841205327255354` radians / approximately `+27.738063301°` |
| Longitude | `-2.2788728782767467` radians / approximately `-130.569797972°` |
| WRLD | `00325868 / LC003KreetBase` |
| WRLD physical file record offset | 1218114958 |
| WRLD XLCN | `00028A08 / KreetWorldSpaceLocation` |
| LCTN physical record offset / parent PNAM | 1293405225 / `0001B1D4` |
| Recovered cell | chart 0, `14312,12774` |

The ESM hash matches the prior qualified main data file. Exact compression/record identity and ordered subrecord structure are checked before selecting CNAM. Native `14076ec00 → 140773090` ingests fixed planet-overlay data; dynamic site retrieval `140ad3b20` and common projection `14096ecb0 / 14096f4d0` use the same geographic representation. Static VAs refer only to the pinned executable, base `140000000`; they are not save or ESM offsets.

Save37 independently retains the **same two binary64 values** at decoded stream offset 219008, associated with player parent 725868 resolving to that fixed WRLD. The original PNDT disk order is reversed relative to this saved longitude/latitude pair. This is an exact fixed-definition/save correspondence, not evidence that the player's local XYZ equals the anchor's physical point.

The Save39 site pair is longitude `-2.2790040301876093`, latitude `+0.48437969905281136` radians, recovered cell `0/14314/12779`. Difference from fixed anchor: **+2 X, +5 Y cells**, angular delta `(-0.0001311519108626591,+0.00025916632727596145)` radians. Both projection dispatch candidates agree in each case. This is a valid comparison of site geography.

It is not an anchor-to-beacon physical distance measurement. Save37 identifies the player in the fixed exterior world, at the user-reported fast-travel placement. The installation's fixed angular entry does not identify that XYZ, the entrance, the scanner target or the drawn icon as its physical origin. The old common source descriptor is present in all three saves. If the player coordinates are compared in their compatible local frame, the Save37→38 vector has norm 424.982755 local units, whereas the scanner target says 471 m. That 46.017245 numerical difference is retained; it is not a fitted correction, inferred metre error or proof of a coordinate failure.

For an illustrative common-origin comparison, the descriptor plus player floors would place the Save37 player at 14313,12775 and Save38 at 14314,12779, a 1,4-cell change. The fixed site's anchor is one cell lower on each axis than that conditional player point. This demonstrates why equating the fixed anchor and fast-travel player would make a false test. The illustration is conditional on cross-parent frame compatibility, not a newly validated player-to-geography API.

The six scanner witnesses show Lab 471 m, Frontier 512 m, Pipeline Terminus 499 m, Deserted Biotics Lab 694 m and Abandoned Muybridge Pharmaceutical 879 m; the silver image contains additional unassigned distance labels. The surface map shows the named outpost and nearby icons. The Lab-like southern compound and ship-like icon can be described visually, but no exact reference/anchor identities are inferred from unlabeled pixels. Map pixel distances, facing directions and icon spacing are not calibrated. Original images and hashes are preserved locally and indexed in [inputs.csv](inputs.csv).

| Original screenshot | Visible witness |
|---|---|
| 20261020112929_1.jpg | Abandoned Muybridge Pharmaceutical label, 879 m |
| 20261020112934_1.jpg | Deserted Biotics Lab, 694 m |
| 20261020112945_1.jpg | Silver/Ag selection; other unassigned distance labels |
| 20261020112949_1.jpg | Pipeline Terminus, 499 m |
| 20261020112956_1.jpg | Frontier, 512 m |
| 20261020113000_1.jpg | Kreet Research Lab, 471 m; secondary ship icon 512 m |
| 20261020113349_1.jpg | Kreet surface map, KREET OUTPOST 1 label and unassigned icons |

The geographic reference is therefore useful independently of marker selection. The smallest missing operand for a precise Lab-target metric comparison is the actual scanner/fast-travel target reference's position and its established transform to the fixed site's anchor; 471 m alone cannot supply that operand.
