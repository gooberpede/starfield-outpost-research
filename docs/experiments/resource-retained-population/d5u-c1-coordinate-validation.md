# D5U-C1 coordinate join and numerical validation

The seven saved centre joins are authenticated and independently reproducible.
They support historical-frame conditional reference disks. They do not establish
a current loaded manager, native population epoch or hardware-derived boundary.
See [the report](d5u-c1-report.md) for question statuses and resource conclusions.

## Evidence and domains

The C1 controlled lease contains D2 `inventory-v2.json` and `requests-v1.json`,
seven D5 frozen cohort outputs, D5A's 26 conditional populations and four framed
native primary controls plus ACKs. The resource access API authenticates these
against the active archive/index/member manifest. Exact member paths/hashes,
owned readers and independent controls are in [the source ledger](d5u-c1-sources.csv).
The builder verifies all 18 member lengths/hashes before use.

Independent authored controls predate this join:

- [Saved centre/frame table](../static-exhaustion/saved-center-frame.csv): sample
  `HIST-0267`, beacon token, parent/secondary/body, descriptor, saved centre bytes,
  site cell and selected site-frame base.
- [Durable-centre projection](../durable-center/projection.csv): same sample/token,
  zero compensation bytes, local XYZ and angular-grid reconstruction residual.
- [Mature-context points](../resource-geometry-mature-context/points-mature-v2.csv):
  P3/P4 `beacon` rows independently supply primary and Carinae descriptor-frame XY.
- [D5G source matrix](../resource-predictability-contrast/source-matrix.csv): U-source
  anchors, descriptor, generator origins, saved beacon/workshop identity and frozen
  control provenance. [Native controls](../resource-predictability-contrast/native-controls.csv)
  identify the four primary capture/resource/source associations.

Saved beacon/extractor tokens are serialized tokens, not FormIDs or runtime
pointers. Source keys are `(chart, fine-cell X, fine-cell Y, SFBK FormID)`.
The inventory record offset is in the decoded logical save stream; it is not a
compressed file offset. No raw save access is required for this correction.

## Equations and units

Let `O` be the saved manager descriptor in geographic fine cells, `S` the
qualified site cell and `L` the saved local compensated native centre. In saved
frame `0x2b`, D2's qualified ordinary initialization uses:

```text
Cxy = float32(Lxy + 100 × (S − O)); Cz = Lz
radius = 150 native units; upper = float32(Cz + 100)
```

Both charts 0/1 are supported interior faces. The site and descriptor chart must
agree; no seam, wrap, rotation or unsupported orientation is guessed. One fine
cell corresponds to 100 native units in this contract. No metre conversion is
asserted. Zero saved Workshop compensation independently establishes beacon =
compensated centre in these seven saved representations. It does not prove
coincidence at another loaded epoch.

For source anchor geographic fine cell `A` and padding two cells:

```text
anchor_native = 100 × (A − O)
generator_origin = anchor_native − (200,200)
historical_source_relative_point = native_point − anchor_native
historical_source_relative_centre = Cxy − anchor_native
outpost_relative_point = native_point − Cxy
```

Do not substitute the generator origin, descriptor or source anchor for `C`.
Native clipping centre is `generator_origin + floor(nominal_size/2) × 100`;
clipping half extent is `floor(nominal_size/2) × 100 + 200`. Cell traversal is
`[1,width+3) × [1,height+3)`. Exact source contracts and packed keys are retained
per layer in the JSON. Candidate coverage uses the existing frozen halo
`radius + 400 + 2 × corpus.maximum_width`, followed by native source resolution;
its 34 keys equal the frozen successes plus recovered failed source branches.
This is bounded ordinary-model coverage, not all possible retail content.

Packed seed arithmetic deliberately mixes its qualified native-origin operands
without dividing them by 100:

```text
seed_XY = descriptor_fine_XY + generator_origin_native_XY + generator_cell_XY
packed = (((((system << 6) | body_index) << 3 | chart) << 16 | seed_Y) << 16) | seed_X
```

System/body/chart and integer coordinate ranges are checked by the owned
`context.packed_seed_key`. For U01 cell `(1,1)`, historical seed XY is
`(21353,31049)`; prospective D5U uses `(24917,32237)`. Their complete keys are
`190147515717866345` and `190147515795726677`. A display translation cannot
change the seed of already generated geometry. U01's 30 versus 28 paths are a
direct counterexample to treating these two frame contracts as identical.

## Seven independent saved joins

The table displays XY to six decimal places for reading; JSON/CSV retains exact
values. Each saved local XYZ byte vector agrees with the independent table;
all seven reconstructed requests agree exactly with authenticated D2 requests.

| Case / outpost | Chart | Descriptor O | Site S | Descriptor-frame centre XY |
|---|---:|---|---|---|
| D2-83388f / Feynman V Cu Co Ni IL | 0 | 25152,32448 | 25124,32446 | -2716.539307, -132.112289 |
| D2-82be17 / Carinae III-a Rc Fe | 0 | 21408,15648 | 21399,15640 | -813.361938, -729.520874 |
| D2-81a75b / Arch III W H2O Lub | 0 | 27168,36000 | 27165,35995 | -242.654449, -400.523834 |
| D2-81bf2a / Feynman VI-b Al Be He3 | 0 | 29568,10944 | 29569,10936 | 161.802246, -741.450012 |
| D2-825f95 / Feynman VII-b Nd Al He3 | 1 | 32160,15168 | 32150,15149 | -909.920166, -1871.573608 |
| D2-844cc6 / Feynman VIII-b Au Sb | 1 | 38112,960 | 38118,970 | 678.213562, 1018.052185 |
| D2-84e101 / Feynman V Cu IL F | 0 | 37536,20928 | 37536,20928 | 81.190742, 90.277481 |

Primary U01–U04 anchors are `(-3600,-1200)`, `(-3600,0)`, `(-2400,-1200)` and
`(-2400,0)`. Their generator origins subtract `(200,200)` from each. The primary
centre relative to U01 is `(883.460693359375,1067.887710571289)`; adding its
anchor recovers descriptor XY exactly. All 34 source joins and seed comparisons
are in [coordinates.csv](d5u/outposts/coordinates.csv).

The maximum angular-grid residual for each site is retained in its JSON and is
less than 0.001 fine cells. This is reconstruction error relative to a site-cell
centre, not a measured physical error bar on the outpost. Historical rebase,
effective overrides and loaded epoch remain unobserved. Saved binary32 inputs
and reconstructed requests are exact within their qualified representation.

## SVG transform, radius and fidelity

All outpost zoom panels use outpost-relative coordinates, extent `[-240,240]²`,
X right/Y up, scale `s=1` pixel per native unit, and a 480-pixel square. For
viewport left/top `(l,t)`:

```text
pixel_x = l + (native_x − Cx + 240) × s
pixel_y = t + (240 − (native_y − Cy)) × s
native_x = Cx + (pixel_x − l)/s − 240
native_y = Cy + 240 − (pixel_y − t)/s
pixel_radius = 150 × s
```

The circle has 90 native units of margin on every side. Insets have separately
declared source-layout extents/scales; they are not deposit maps. The diagnostic
uses common source-relative extent `[-500,1450]²`, 500 pixels and scale `500/1950`.
Every transform and transformed disk is in
[map-manifest.json](d5u/outposts/map-manifest.json). No circle is clipped.
Main zooms deliberately clip geometry beyond their labelled extent; full points
and bounds remain in JSON. The source-layout panel contains every source anchor,
generator origin and nominal box, including sources with zero disk overlap.

The numerical inverse checks have maximum double-precision round-trip error
`4.547473508864641e-13` native units. SVG primitive coordinates serialize to nine
decimal pixel places: at scale 1 this adds at most `0.5e-9` native units per
coordinate, separate from native arithmetic/model limits. Exact binary32 ordered
point/bound bytes remain authoritative. Footprints use positive-width endpoint
disks and max-width consecutive rectangles intersected with the retained bound
disk `max(radius,0.5)`. Native quaternion/transcendental and marginal segment
rounding are approximate in the continuous SVG reconstruction. Finite native
callback agreement is not a proof of exact continuous boundaries or UI identity.

## Independent native controls and reproduction

Primary captures 299/325/696/716 are parsed with the existing framed reader,
sequence/digest/ACK closure checks. Each exact ordered XYZW sequence and native
bound matches one and only one relevant frozen source path. Their retained
query XY equals the Save52 descriptor-frame centre exactly. Their query Z is
`-0.10489535331726074`, while Save52 has `-0.153639554977417`. This discloses
the non-atomic historical difference rather than forcing 3D equality.

All four paths have certified positive planar area and accepted callbacks at
the authenticated Save52 research request. The local
`.local-work/d5u-c1/data-checks.json` retains exact per-control cells and witnesses;
the [primary reconciliation CSV](d5u/outposts/primary-reconciliation.csv) is its
authored review derivative. Build/replay and checks are described in
[the map README](d5u/outposts/README.md); actual raster/prose review and exact
snapshot disposition are recorded in [the review](d5u-c1-review.md).
