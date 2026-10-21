# Position, biome and site-resource dependencies

2026-10-20. The project can identify qualified saved bodies/sites and compute
conditional discrete cells/local residuals. It cannot yet claim exact continuous
beacon geography or every biome/resource in actual usable territory. These are
different capabilities and need different missing evidence.

This assessment cites [position specification](../../position-model/specification.md),
[capabilities](../../position-model/capabilities.md), [applications](../../position-model/applications.md)
and [review](../../position-model/review.md); these preserve source-scoped confidence,
ordinary-case exclusions and NOT TESTED full XYZ equivalence. No approximation is
silently promoted to a validated latitude/longitude result.

| Required level | Best supported existing result | Specific missing dependency / discriminator | Proposed disposition |
|---|---|---|---|
| 1 Planet/system and landing-area identity | [Capacity/body study](../../experiments/save-capacity-and-planetary-location.md) joins saved worlds/components/body indices to PNDT/STDT; 17 mature clear candidates match independent reference names. [Two-outpost study](../../experiments/two-outpost-site-anchors-and-beacon-coordinates.md) distinguishes sites on Kreet | Body identity alone does not choose unique landing marker, same traversed area, active owner or stable cross-save UUID. [Fallback provenance](../../experiments/fallback-grid-provenance.md) separates marker/source/reference identity | A07 ALREADY RESOLVED scoped; exceptional identity deferred under A03/A06 |
| 2 Saved surface/site anchors and angles | [Surface-anchor semantics](../../experiments/planetary-surface-anchor-semantics.md) supports longitude-first double radians with native names/selector and exact New Atlantis fixed-world save/PNDT equality (disk order reversed) | Generic saved-wire grammar and authoritative use after load remain bounded; site/overlay anchor is not beacon's exact point | A08 ALREADY RESOLVED for scoped angles |
| 3 Grid/cell position and projection | [v2 specification](../../position-model/specification.md): 49152 grid, native/packed tags, C=P+D, binary32 cell/remainder, qualified 0b/2b base. Pattern orientation does not rotate reference XYZ | Missing upstream site base leaves UNKNOWN. Source/caller/frame qualification and general loaded parent remapping not supplied by valid input syntax | A09 ALREADY RESOLVED conditional capability |
| 4 Exact continuous beacon lon/lat | [Static exhaustion](../../experiments/activated-overlay-static-exhaustion.md) preserves distinct same-phase off-grid countermodels even after selected saved chart/residual reconstruction | Independent continuous off-grid geographic truth; exact chart embedding/anchor/frame/residual relation and held-out seam/pole controls. Height/load epoch is a separate question | A10 DEFERRED, not fundamental impossibility |
| 5 Planet biome catalogue | PNDT/body/BIOM and installed species/resource definitions are relevant; [prior-art leads](../../experiments/planetary-surface-anchor/prior-art-and-leads.md) preserve external biome-parser provenance and unaccepted reuse basis | Authoritative full biome occurrence path for one planet, duplicate/conditional biome references, installed content/override context. WRLD BIOM reference or appearance texture is not proven complete occurrence catalogue | A12 TARGETED RESEARCH CANDIDATE |
| 6 Beacon/site biome | [Native output contract](../../experiments/native-availability-map/output-contract.md) N14 biome sampling uses translated/scaled/floored XY -> BIOM -> RNAM descriptors | Matched saved beacon/established-Workshop identity, source context/transform and selected BIOM result; one center lookup is not entire build area | A13 TARGETED RESEARCH CANDIDATE |
| 7 All territory-intersecting biomes | [L3](../../experiments/spatial-placement/report.md) explains radius 150, disallowed location/cell areas and clipped border construction | Common coordinate frame between actual legal territory and biome-map boundaries, current restriction/source epoch, treatment of boundary cells and narrow slivers. No existing cited direct L3-to-BIOM join establishes this | A14 TARGETED RESEARCH CANDIDATE |
| 8 Resources actually at site | [Availability endpoint](../../experiments/native-availability-map/output-contract.md) maps spatial + effective atmosphere + selected biome water fold; 346 preview UI folds agree. [E2](../../experiments/organic-facilities/report.md) product catalogue is planet-scoped domesticability, not wild local presence | Actual region geometry/translation/source completion/freshness and native admissions for qualified established site. Planet resource list, raw BIOM RNAM, a saved producer or displayed nominal production is insufficient | A15 TARGETED RESEARCH CANDIDATE; arbitrary remote sufficiency A16 DEFERRED |

## Dependency order and useful reuse

Qualified body/site identity -> qualified source chart/context -> transformed
indexed query position -> selected biome is a plausible native-query dependency
chain, supported only to the stages cited above. Territory biomes additionally
require an actual territorial predicate/boundary linked to that biome frame.
Site inorganic resources additionally require generated source geometry and
atmosphere/water populations with a known freshness/lifetime context. A continuous
angular export is a separate branch; do not assume it must be solved before a
native local-context capability can be useful.

For a **single-biome interior** site, a center sample can support the center's
biome, but the all-territory assertion still requires a coverage argument showing
the entire legal area stays inside that biome. For a **boundary** site, several
point samples are useful witnesses, not completeness proof: finite samples can
miss a narrow intersecting biome. A complete method needs the boundary geometry
or a qualified finite cell coverage predicate at the correct resolution.

L3 offers justified reuse of its territory restriction and border mechanisms,
not a ready-made biome polygon. Radius150 alone omits exclusions; a drawn border
is not automatically the exact admission set for every footprint. The source
study explicitly leaves rejected/photo-specific operands unmeasured. First prove
that territory queries and biome sampling refer to the same indexed source/frame;
then determine whether biome sets should describe legal point territory or
footprint-dependent construction admission, and document that intended meaning.

The [region-dependency graph](../../experiments/native-availability-map/region-dependencies.md)
and [requirements](../../experiments/native-availability-map/region-requirements.md)
identify current-manager source selection, BIOM/CTPerBiome/component inputs,
cache generation/readiness and translations. A visited key, resident cache or
published task is not proof that the complete natural geometry is ready.
Neither mandatory travel nor separate-world remote sufficiency has been proven.
The [0.8.0 NO-GO](../../experiments/local-readiness/scientific-value-reassessment.md)
explains why collecting more headers cannot fill those specific holes.

## Smallest recommended discriminating work

First authorize an **existing-data lineage assessment** of one already qualified
established beacon's context: find whether archived records connect its source
chart/translated XY to a selected BIOM result and a territory predicate in that
same frame. Require independent identities/offset domains and preserve missing
edges. An answer for one beacon would not close complete territory or arbitrary
planet sampling, but it could resolve the key dependency without exact lon/lat.

If that chain is absent, a separate prospective brief could capture the missing
operands for one interior and one boundary outpost, including clipped-side
controls. It must explicitly authorize any hooks/breakpoints/game actions and
state protected saves, finite scope, intervention, flush/exit/recovery and cleanup.
For actual inorganic completeness it additionally needs completed source region
operands and native admit/reject witnesses, not just final UI lists. No new live
card, observer, capture or analysis export is authorized by this recommendation.

Exact continuous geography should stay deferred unless needed for a particular
map feature or independent evidence appears. A held-out off-grid native geographic
reference can distinguish the current countermodels; more anchors at the same
grid phase cannot by themselves do so. Existing discretized outputs remain useful.

Planner fields such as selectedBiomeIds and localResources carry user intent and
domain rules in the [application audit](../../position-model/applications.md).
An empty selected-biome selection is not measured site truth. Importing a planet
catalogue must not overwrite manual site knowledge with an unsupported geographic
inference. No importer is implemented or authorized here.
