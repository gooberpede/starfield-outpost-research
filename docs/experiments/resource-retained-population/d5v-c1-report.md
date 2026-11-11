# D5V-C1 native-axis correction

2026-10-30, Australia/Sydney. [Invoked correction brief](../../implementation-briefs/README.md#archive-lookup) (`implementation-briefs.zip :: docs/implementation-briefs/CODEX_BRIEF_SOR_RG2_D5V_C1_native_coordinate_plot_correction.md`).
This is REWORK of D5V-AC6/AC7, not a new scientific investigation.

**Answer: COMPLETE.** Both corrected outpost figures visibly plot absolute native
descriptor-frame X/Y and label the actual nonzero native centres. The full
150-unit circles, qualified saved beacon, canonical geometry and native consumer
findings are preserved. Independent scientific/engineering and editorial reviewers
accepted the rendered output; final closure identities are recorded below.

## Frozen question and active correction ledger

**D5V-C1-Q1:** Can the two D5V outpost figures present the qualified historical
native descriptor-frame X/Y coordinates directly—for axes, plotted data, outpost
centre, beacon and boundary—while retaining the established geometry,
native-consumer findings and reproducibility?

C1-AC1–AC9 are frozen as written in the brief. No scope amendments are approved.
Question status at this initial checkpoint: **INCOMPLETE**.

| Branch | Initial evidence / next action | Disposition |
|---|---|---|
| C01 Preservation | Prior D5V work is still uncommitted. Freeze its 25-file starting inventory, including both supplied briefs; verify installed/analysis pins and C:/D: floors. | Verified in `.local-work/d5v-c1/initial.json`; preserve starting bytes for a genuinely correction-only diff. |
| C02 Frame | Read D5V contract, D5U-C1 proof and canonical geometry. Both centre and region points already use each site's qualified historical descriptor frame. | Join established; retain original native values and saved zero-compensation beacon correspondence. |
| C03 Presentation | Existing renderer shifts every region by centre and supplies `[0,0]` to its panel. | Confirmed defect: relative axes were incorrectly accepted as satisfying the requested native-axis presentation. Replace with native data coordinates and absolute ticks. |
| C04 Controls | Existing round trips validate a reversible relative display, not the demanded visible axes. | OPEN: check actual SVG ticks/centre/cardinals/corners/deposits, preserve scientific inputs/results, replay and render. |
| C05 Review | Prior scientific conclusions stand; old AC6/AC7 visual acceptance is superseded for this defect. | OPEN: independent rendered-output scientific/engineering and editorial review against the correction brief. |

Only authored plotting/documentation changes, existing-data checks and local
offline rendering are permitted. No native execution, game/SFSE/Vortex operation,
save/configuration/analysis-database mutation, staging, commit, push or disclosure.
Both caller-available free-space floors remain 40,000,000,000 bytes. Preserve all
proprietary/raw artifacts locally and all pre-correction evidence bytes in the
ignored baseline. The lifecycle schematic and native-consumer findings are not
being reopened.

## Correction and native-to-pixel contract

The corrected figures are [Feynman V Cu Co Ni IL](d5v/D2-83388f.svg) and
[Feynman V Cu IL F](d5v/D2-84e101.svg). Their public data coordinates are the
qualified historical native descriptor-frame X/Y from the canonical C1 JSON.
The centres remain exactly `(-2716.539306640625,-132.11228942871094)` and
`(81.19074249267578,90.27748107910156)`. Both are placed and labelled at those
native coordinates, rather than assigned native `(0,0)`. Adjacent marker labels
round to three decimal places; exact values remain in the header/backing data.

The root cause was reuse of a centre-relative C1 panel renderer. D5V called
`shifted(layer, centre)` and passed `[0,0]` to `panel()`. Its inverse was valid,
but accepting that arithmetic as native-axis presentation was wrong. The new
owned `native_panel()` receives the original region values and actual native
centre directly. No geometry is renormalized or regenerated; there is no
centre-relative public data layer or primary displacement grid.

Canonical points/bounds, centre and qualified saved beacon already share the
site's historical descriptor frame under the [C1 join](d5u-c1-coordinate-validation.md).
This was verified before editing: saved frame `0x2b`, same qualified chart 0,
`Cxy=float32(Lxy+100(S−O))`, zero saved Workshop compensation. Source anchors
and padded generator origins remain distinct fields. No current loaded epoch,
planetary global XYZ, compass orientation or metre conversion is asserted.

For native viewport bounds `(xmin,xmax,ymin,ymax)`, pixel left/top `(l,t)` and
scale `s=480/(xmax−xmin)` pixels per native unit:

```text
u = l + (x − xmin) × s
v = t + (ymax − y) × s
x = xmin + (u − l)/s
y = ymax − (v − t)/s
pixel radius = 150 × s
```

The two detailed comparison panels span each site's absolute centre ±240 native
units in both axes. For example, the primary X ticks include `-2900`, `-2800`,
`-2700`, `-2600`, `-2500`; its native Y ticks include `-300` through `100`.
The second site's detailed ticks include `-100` through `300`. Common bounds and
scale are used across the paired comparison panels. Separate outposts correctly
have different absolute viewports. The renderer's viewport subtraction and SVG
Y inversion produce pixels only; they do not redefine the native coordinates.

Two full-extent companion panels per figure show every displayed region bound
inside the viewport, with at least 40 native units of margin on each limiting
side. Detailed views still deliberately zoom; the lower views avoid hiding the
rest of a clipped deposit. Native bound clipping remains part of the original
shape. All four panels retain the full 150-unit circle and qualified beacon.
Masks, selected layers, IRES colors and comparison meanings remain unchanged.
The lifecycle SVG is byte-identical. The coordinate schematic changes only its
pixel-transform explanation.

## Numerical, preservation and rendered checks

The focused [checker](../../../research/resource-retained-population/d5v_c1_checks.py)
reads the pre-correction snapshot, canonical C1 JSON, independent saved-frame and
projection CSVs, current SVGs and backing data. It does not execute native code.
`.local-work/d5v-c1/checks03/checks.json` records:

- Both exact saved-centre joins and zero-compensation beacon relationships pass.
- Eight panels check native→pixel→native for actual centres/beacons, all four
  cardinal-radius points, corners, and every relevant supplied point/bound centre.
- Native tick text and tick pixel positions are checked against the independently
  evaluated transform. SVG centre/beacon metadata, boundary pixel centre/radius
  and every displayed region-bound clip circle agree with canonical native data.
- Unrounded round-trip error is at most `9.094947017729282e-13` native units,
  below the explicit `1e-9` tolerance. Nine-decimal pixel serialization gives at
  most `2.626507011882495e-9` native units in the tested lower-scale overviews;
  the checked tolerance is `0.5001e-9/s + 1e-9` native units.
- All affected SVGs and spatial JSON reproduce byte-for-byte. Scientific
  reference/consumer fields and canonical input hashes are unchanged.
  `consumer-results.csv`, `coordinates.csv`, native method and lifecycle SVG are
  byte-identical to their pre-correction versions.

The existing D5V checker also passes in
`.local-work/d5v/c1-presentational-regression01/checks.json`. Its boundary check
now converts each displayed radius through that panel's scale, accommodating
the full-extent views. The original 606 area/point results are read from their
unchanged receipt, not newly executed or reclassified by this correction.

`spatial.json` changes presentation schema from `sor-d5v-spatial/1` to `/2`:
panels now store native bounds, absolute centre/beacon and tick values, with
separate pixel positions/scale. Each figure has two additional full-extent
panels. Reference metadata, source JSON hashes, native query values, masks,
resource membership and consumer-result records compare exactly to the starting
snapshot. This is a presentation schema change only.

The existing bundled sharp/libvips renderer produced full-size PNGs and readable
crops in `.local-work/d5v-c1/png01/`. The implementer actually inspected both
outposts' detailed/full views and the coordinate schematic. Absolute ticks,
actual centre labels, complete circles, legends and comparison scales are visible.
All displayed deposits are contained by the lower views; upper zoom clipping is
explicit. Actual renderer versions and stderr are retained. Font-cache warnings
did not prevent rendering. Independent visual acceptance remains mandatory.

## Implementation matrix at review01 — historical checkpoint

| Criterion | Implementer result | Evidence / remaining requirement |
|---|---|---|
| C1-AC1 Authority/preservation | PASS | Starting snapshot, three installed/15 analysis pins and both-drive floors; no prohibited operation. Final preservation check remains. |
| C1-AC2 Frame qualification | PASS | Original canonical native geometry plus two independent exact saved-frame joins; no unqualified live layer plotted. |
| C1-AC3 Native presentation | PASS, review pending | Actual native data/ticks/marker labels visible in both rendered figures; centre is not native `(0,0)`. |
| C1-AC4 Boundary/fidelity | PASS | Full circles, absolute qualified beacon, unchanged scientific inputs/results, masks/colors; lifecycle bytes unchanged. |
| C1-AC5 Controls/replay | PASS | Actual SVG tick/bound/centre checks, all round-trip categories, explicit tolerances and deterministic replay. |
| C1-AC6 Rendered visual QA | Implementer PASS; independent NOT TESTED yet | Full-size PNGs and crops inspected; separate reviewers must inspect actual renderings. |
| C1-AC7 Documentation | PASS, review pending | Contract/gallery/report/review and coordinate schematic distinguish absolute native data from pixels and supersede incorrect earlier visual acceptance. |
| C1-AC8 Independent review | NOT TESTED yet | Scientific/engineering and editorial exact-snapshot rendered-output review pending. |
| C1-AC9 Exact delivery | NOT TESTED yet | Correction-only versus complete diffs and exact manifests pending final export/review. |

C02–C04 now have supported implementation/control results. C05 remains OPEN for
independent rendered-output review and exact delivery. C1-Q1 therefore remains
**INCOMPLETE at this review checkpoint**, not accepted by arithmetic alone.
No scientific/native regeneration, save work or live operation occurred.

## Independent acceptance and final closure

Two separate reviewers accepted the exact review01 snapshot. Its 27-file
manifest SHA-256 is
`3bab780484ecd62f70270203d34db71bb27652e182790c46ebf363a11791ce3e`.
Their complete actual returns are retained as
`.local-work/d5v-c1/visual-review01.md` and
`.local-work/d5v-c1/editorial-review01.md`. Both reviewers actually inspected the
two full-size outpost PNGs, four detailed/full-extent crops and coordinate PNG.
The scientific/engineering reviewer independently recomputed both binary32 joins,
actual SVG tick/centre positions and 4,978 numerical controls. The editorial
reviewer read all changed prose/schema/comment sets and visible qualifications.

The scientific/engineering return explicitly concludes that original D5V-AC6/AC7
intent is met by visible absolute axes and qualified native joins, rather than
reversibility alone. It found no remaining authorized scientific lead necessary
to answer D5V-C1-Q1. Both returns distinguish direct reviewer checks from retained
implementer execution receipts. Their acceptance grants no integration or
publication authority.

| Criterion | Final result | Actual basis |
|---|---|---|
| C1-AC1 | PASS | Initial/final installed and analysis identity checks, both-drive floors, unchanged HEAD/index and offline-only actions. |
| C1-AC2 | PASS | Canonical native frame joins independently checked for both sites. |
| C1-AC3 | PASS | Absolute native axes/ticks and genuine labelled nonzero centres independently viewed. |
| C1-AC4 | PASS | Complete circles and full displayed-deposit overviews; canonical geometry/consumer records and lifecycle unchanged. |
| C1-AC5 | PASS | Exact SVG/JSON replay, actual SVG numerical controls and explicit tolerances; independent calculations agree. |
| C1-AC6 | PASS | Both separate reviewers actually viewed both final figures and all specified crops. |
| C1-AC7 | PASS | Current captions/schema/contract agree; earlier incorrect visual acceptance is explicitly superseded and preserved. |
| C1-AC8 | PASS with final closure receipt | Separate scientific/engineering and editorial ACCEPT returns, plus required final exact-snapshot delta review. |
| C1-AC9 | PASS with final closure receipt | Verified correction-only/complete patches, 27-file manifest, status, inclusion/exclusion inventories and byte application checks. |

The final package is `.local-work/d5v-c1/final01/delivery.json`, with
`.local-work/diffs/d5v-c1-final01-task-only.diff` and
`d5v-c1-final01-complete.diff`. Task-only covers the 17 correction-authored changes
against the frozen starting working tree. Complete covers all 27 uncommitted
text paths against HEAD, including previous D5V work and both supplied briefs.
No staging is used. Both patches undergo forward/reverse application and exact
byte comparison in isolated `.local-work/review-patches/` scratch, with parent
repository discovery blocked. Whitespace, local links, path inventory and final
editorial screen pass. The actual narrow closure review must exist at
`.local-work/d5v-c1/final-delta-review.md`; a planned path alone is not acceptance.

`.local-work/d5v-c1/postflight.json` verifies three installed inputs, 15 analysis
pins, two canonical geometry hashes, preserved scientific artifacts and unchanged
Git identities. Both caller-available drives exceed 40,000,000,000 bytes.
`exclusions.json` pins the 75 task-local files present at its checkpoint; later
review/closure metadata is separately identified. Baseline snapshots, intermediate
maps, renderings and private receipts remain ignored/local. Prior raw native,
save, database and installed artifacts remain excluded from both text patches.

The zero-diagnostic screen, full manual reading of the 17 correction prose/code/
schema/figure changes and both independent readings satisfy editorial coverage.
No unresolved editorial exception or product failure remains. The reviewer's
initial PowerShell calculation syntax failure was corrected before its complete
independent numerical pass; it was not a plotting defect. Font-cache renderer
warnings are preserved with successful previews. No source or consumer result
was regenerated to repair presentation.

C01–C05 are resolved, subject to the actual final closure delta receipt.
D5V-C1-Q1 is COMPLETE within the frozen historical native descriptor-frame
presentation scope. The main D5V lifecycle/consumer science is unchanged.
Engineering and visible-output acceptance are separate from maintainer
integration. No game/SFSE, Vortex, save/configuration/analysis-DB mutation,
external disclosure, staging, commit, push or publication occurred.
