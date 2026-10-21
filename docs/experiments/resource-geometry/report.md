# RG1: inorganic vein geometry

2026-10-21, Australia/Sydney. SOR-EXP-0063 / SOR-EV-0071.
[Authorized brief](../../implementation-briefs/CODEX_BRIEF_SOR_RG1_inorganic_resource_vein_geometry_reconstruction.md),
[scope](plan.md), [review and AC1–AC8](review.md), [source pins](sources.csv).
Authored work REVIEW-REQUIRED; proprietary native/content/save evidence LOCAL-ONLY.
Publication NOT CLEARED; B6 remains on hold.

**The inspected inorganic vein representation is an ordered XYZ/width path,
generated procedurally from selected resource definitions and spatial source
context. A qualified offline model now connects three saved Kreet beacon frames
to finite source populations, point membership and nominal 150-unit circles.**
It does not establish that those historical saves loaded these exact current-build
regions. The reconstruction uses the pinned 1.16.244.0 main-file registry and
native default settings, with explicit interior-chart and Kreet owner-key limits.

The [causal native trace](native.md) resolves BIOM → surface style → ordered SFPT
selection → anchored SFBK source → local native origin/bounds → selected planetary
family/RSGD → rarity-ordered resource/X/Y population. Each generator call resets
its CRC/MT stream, draws count/heading/width/positions, and retains points passing
clipping and earlier different-resource competition. Rejections advance the stream
and heading; subsequent steps extend the last accepted point. Whole finite sources
are generated, including paths starting outside the beacon footprint.

The native sphere broadphase is materially part of competition semantics. A
max-width rectangle can extend outside that incremental sphere. The first revision
incorrectly omitted it; independent review supplied a counterexample, now preserved
as a regression. Disks and max-width rectangles used by generation competition,
tapered strips used by availability-area processing, and the separate weighted
byte raster are distinct products. No overlay/raster equivalence was inferred.

| Qualified current-build baseline using saved frame | Source evaluations / resource-cell calls / paths | Nominal radius-150 bounded-region result | Fixed lattice point checks |
|---|---|---|---|
| Kreet39, chart 0, origin (14304,12768), local center (1088.759765625,1179.728515625) | 4 / 1152 / 123 | Neither Lead nor Silver intersects | 7 occupied, 42 empty; both Lead and Silver occur nearby |
| Kreet25 SOR-002, chart 1, origin (10464,21120), local center (122.70045471191406,273.0462341308594) | 6 / 2592 / 766 | Iron intersects; Alkanes does not | 21 occupied, 28 empty |
| Kreet25 SOR-003, same chart/origin, local center (356.8204040527344,2459.05859375) | 4 / 2016 / 589 | Iron intersects; Alkanes does not | 16 occupied, 33 empty |

These are **STATIC/SAVE-supported predictions**, not observed native vein sets or
extractor admission results. The contrasting sites were run without fitting to
names, resource labels, UI lists, extractors or production. A second calculation
independently uses the owned explicit MT implementation, double arithmetic/libm
and distance/slab geometry, without importing the primary evaluator. It reproduces
all 1478 path identities/accepted-point counts and all 147 lattice classifications;
coordinate/width differences stay below 0.000535 native unit in these runs.
The declared comparison tolerance is 0.01, an engineering criterion rather than a
universal error bound. [Validation and exact receipts](validation.md) distinguish
this mathematical cross-check from unavailable newly measured runtime geometry.

| Dimension | Strongest supported scope and limit |
|---|---|
| Confidence | Proposed STRONG for the scoped STATIC causal reconstruction with alternate arithmetic checks and existing qualified SAVE frames. Exact mathematics applies to the supplied geometric operands, not unrestricted native correspondence. No new live measurement. |
| Coverage | Interior chart 0/1, ordinary rectangular base sources, 256-square maps, main-file registry/native defaults, scoped Kreet family and owner. Seams, effective plugin overrides, other body owner mappings and historical cache epochs remain unqualified. |
| Nominal completeness | Conservative owner-cell halo and whole ordered sources bound all entering modeled regions. Exact rational polygon/disk tests cover tapered strips. Bounded disk/rectangle union uses certified disjointness/interior witnesses, returning UNKNOWN for unresolved arrangements; all three reported per-resource sets resolve. |
| Boundaries | Binary32 generation and constructed vertices; exact decisions over supplied polygons. Native atan2/quaternion marginal rounding remains unqualified. Tangency has zero area. XY nominal territory projects generated Z=0; it does not apply saved altitude/terrain height or POI clipping. |
| Persistence | Source-pointer caches and generated point collections are transient manager state; a saved beacon frame does not prove restored region identity or authority after load. No whole-save absence finding. |
| Authority | Offline only; no game launch/attachment, save/configuration/installed-data/analysis-content mutation, staging, commit, push or publication. |

The first review returned REWORK because the unopposed demonstrator did not satisfy
ordinary-site reconstruction. The continuation adds actual source context, full
planar competition and finite population, three site qualifications and alternate
spatial checks. [Review](review.md) retains that failure and governs final acceptance.
Historical findings and publication classifications are unchanged. Further native
measurement would test correspondence at a new evidence tier; it is not silently
required to invalidate this qualified static result or authorized by this brief.
