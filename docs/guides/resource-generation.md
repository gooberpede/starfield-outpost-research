# How Starfield generates outpost resources

[Guide index](README.md) · [Technical reference](../reference/resource-generation.md) ·
[Project glossary](../reference/glossary.md)

Deposits can look identical after a return even when Starfield discarded their
old geometry and built it again. They can also differ between qualified visits
to the same geographic source. In the ordinary path studied here, the first
eligible request to find a protected source-map miss supplies the coordinate
for a raster sample. A different request can sample the same value, and a
different sample can change the complete generated geometry. Which request
usually wins remains unmeasured.
[Current scope decisions](../experiments/resource-retained-population/d5au-gap-closure-decisions.md) ·
[Native feasibility review](../experiments/resource-retained-population/d5aq-review.md).

This guide covers the pinned **Starfield 1.16.244.0** ordinary paths, with
specific main-file inputs or observed sessions identified below. Mods, other
builds and effective load orders need their own qualification.

## What is being generated

A **geographic source** is a landscape contribution with a geographic
descriptor and terrain identity. A moving native **Grid** publishes the live
source allocations used to serve local requests. A source can contribute
geometry to several queries. A query can select several sources. An outpost
has its own centre, area and object identities, so one source's complete
geometry cannot serve as an inventory of the deposits inside an outpost.

On the ordinary path a **raster mask** is a small numeric input sampled from
planetary data. The generator uses it with ordered resource definitions,
source-derived seeds, the generation frame and clipping parameters. It
produces **regions** with bounds and point arrays grouped by resource
identity. The source anchor, the request location, the generator origin, the
outpost centre and the placed beacon may each refer to a different point.

The nominal biome describes a site through a separate biome assignment
path. The Build Mode **Available Resources** list is a consumer result
assembled from several populations, including an area scan of resident
geometry. A biome label or a displayed resource name does not give you a
contour or a point placement result.
[Source and coordinate controls](../experiments/resource-retained-population/d5aq-mask-method.md) ·
[Nominal biome study](../experiments/outpost-biomes/report.md) ·
[Availability contract](../experiments/native-availability-map/output-contract.md) ·
[Availability review](../experiments/native-availability-map/output-review.md).

## How one request populates a source

1. Landscape context, the coordinate frame and the relevant data must be
   ready. Focus, cell preparation and level-of-detail work can produce
   density and layer requests. The original signed integer coordinate pair
   travels with the request. Grid lookup selects the relevant source using
   live slots and contributor rules.
2. The resource provider checks a content-derived **visited token** under
   shared protection. A match bypasses the source map entirely. If the
   request passes that check, it acquires exclusive protection and looks
   up the full live source pointer. A hit skips construction.
3. On the first eligible miss, the provider installs the map holder and
   calls the generator on the successful path. It converts that request's
   original coordinate pair through the current geographic frame to sample
   the raster. It uses separate source-derived inputs to lay out and clip
   the generated regions. An attempt to store the visited token follows.
4. The retained holder groups copied geometry by resource. Protected area
   and point consumers can inspect the resident collections. Failed
   allocation or copy can leave incomplete results, and a token store
   cannot certify complete geometry.

Two requests can both pass the shared check. The one that passed it
first can still reach the protected lookup second and hit the entry built
by the other. Readiness, queue service and lock admission matter. The
audited path contains no central selector that replaces every competing
query with the same coordinate.
[Ordinary path and arbitration](../experiments/resource-retained-population/d5w-normal-path-model.md#arbitration-original-query-authority-and-retention) ·
[Path review](../experiments/resource-retained-population/d5w-review.md) ·
[Earlier-check loser](../experiments/resource-retained-population/d5ac-target-lookup-chronology.md).

## Why two visits can produce different geometry

The Feynman V source used in these comparisons is
`0:37536:20928:0029d20e`. **C1** names a qualified main-file input and
request contract. Its 196 distinct original coordinates have corresponding
density and layer tasks. Under C1, the sampler gives mask `0x0` at 28
coordinates and `0x3` at 168. A native reachability proof exhibits an
eligible constructing continuation for each mask class. It does not establish
first-miss reachability for every coordinate. In fixed-input native controls,
mask `0x0` yields 74 regions and 193 points, and mask `0x3` yields 78
regions and 180 points. Two different queries sampling `0x3` agree across
the complete represented output when the other inputs are fixed. The
sample changes ordinary resource weights. A mask below the rarity of a
resource selects its inactive multiplier rather than unit weight. The
generator processes definitions in order, so an earlier weight change
can affect a later
resource's surviving regions even when its own weight stays the same.
[Geometry controls](../experiments/resource-retained-population/d5ag-geometry-controls.md#equivalence-and-counterexamples).
[C1 census and controls](../experiments/resource-retained-population/d5aq-report.md#what-changes-the-scientific-answer) ·
[Independent review](../experiments/resource-retained-population/d5aq-review.md).

| What was counted | Mask `0x0` or its reference class | Mask `0x3` or its reference class | Other | Denominator |
| --- | ---: | ---: | ---: | --- |
| C1 candidate coordinates, sampled under the fixed input contract | 28 (14.29%) | 168 (85.71%) | 0 | 196 distinct coordinate pairs |
| Qualified D5AS cold-start geometry, matched over all canonical body bytes | 2 (6.67%) | 28 (93.33%) | 0 | 30 qualified fresh-process snapshots |

*Comparison.* The first row counts sampling opportunities, including one
directly sampled constructor. The second counts observed complete geometry
classes. Its labels come from fixed reference comparisons. The original
winning requests and generating masks were unmeasured in those snapshots.
The 6.67% describes this qualified series under the operator-reported
Save52 load-and-visit procedure. Individual loaded saves, routes and
effective generation inputs were not independently verified for all
runs. Neither row supplies a retail winner probability or establishes
independent, identically distributed trials.
[Tracked C1 rows](../experiments/resource-retained-population/d5aq-request-mask-map.csv) ·
[Series comparison and exclusions](../experiments/resource-retained-population/d5as-series-closeout.md#frozen-roster-and-comparisons) ·
[Evidence-access review](../audits/publication-architecture-d5ax/review.md).

Other Save52 sites have indexed source associations and conditional request
censuses. Their candidate counts cannot tell a player how often a visit will
produce a particular layout.
[Active-outpost survey](../experiments/resource-retained-population/d5at-active-associations.md).

## Why identical deposits can mean different things

| What happened to the source | Consequence under the audited conditions |
| --- | --- |
| The Grid keeps the source and the map keeps its holder | Protected consumers can read the same geometry. A new provider request may bypass on visited state or reach a true map hit. |
| The source loses overlap or its owning Grid clears | The source ends and its map entry is erased if present. The visited array survives this narrow operation. A new allocation with an equal surviving token can bypass while the map entry is absent. |
| The registered procedural-generation module clears both stores, or the old process ends | Eligible later demand can build a new population. New geometry can match earlier output. |
| A Workshop list survives in consumer storage | Its contents can look stable after the source state changed. The list contains admitted resource identities and gives no source-lifetime proof. |

On the recorded Feynman V → Lodge **exterior fast-travel marker** → Feynman V
trip, the engine cleared the old source, reset the population stores and
generated on return. Two distinct original requests, `(8,3)` and `(-1,11)`,
directly sampled `0x3`. The complete compared geometry was identical. This is
a **rebuilt identical** result for one itinerary. Same-area, interplanetary and
intersystem travel labels alone cannot identify the native transition.
[Episode A proof](../experiments/resource-retained-population/d5ak-a-report.md) ·
[Episode A review](../experiments/resource-retained-population/d5ak-a-review.md) ·
[Player-action matrix](../experiments/resource-retained-population/d5av-player-action-matrix.md).

The audited Save52 channels carry generated-world descriptors and
PlanetContentManager (PCM) seed and map data. Separately saved placed references
and producer records can restore their own identities and associations.
Under the audited ordinary full-load path, valid load objects and a stable
`bAvoidClearOnReload` setting select complementary clearing branches for
the old population stores. The load reconstructs source inputs. Complete
source contour arrays are transient in this graph, and fresh geometry needs
separate eligible demand. Save52's saved destination is the Lodge interior.
The series operator reported loading it and then visiting Feynman V.
[Save state and load order](../experiments/resource-retained-population/d5ad-load-chronology.md) ·
[Save-state review](../experiments/resource-retained-population/d5ad-review.md).

## What this means for building and production

- **Available Resources** folds admitted area results with atmospheric and
  selected biome-derived inputs on the inspected UI path. A resource in
  the list can be absent at the exact point where you try to place an extractor.
  In one native control both supplied Feynman V alternatives included Ionic
  Liquids in the area result, but the same point admitted it only under
  the mask-3 geometry. That comparison tests a resource predicate on supplied
  geometry. Full placement has additional gates.
  [Area and fixed-point control](../experiments/resource-retained-population/d5w-report.md#q3--three-stability-levels) ·
  [Availability review](../experiments/native-availability-map/output-review.md).
- **Placement eligibility** for an ordinary natural extractor includes a
  point test against current geometry and a match with its effective
  produced-resource properties, subject to the branch's bypass checks.
  [Placement and registration](../experiments/resource-retained-population/d5ah-extractor-continuity.md#placement-and-registration-use-distinct-resource-operations).
- **Established production** uses a separately registered resource key.
  The audited ordinary due-cycle path uses that key, resolving the producer
  and checking current eligibility, power and destination capacity before
  insertion. Its restored row can carry the association through remapping.
  Actual output across a measured changed-geometry transition remains
  untested. [Continuity evidence](../experiments/resource-retained-population/d5ah-extractor-continuity.md) ·
  [Review](../experiments/resource-retained-population/d5ah-review.md).

Staying within retained coverage can preserve deposits. Saving and returning
can permit fresh sampling under the stated conditions. A familiar list,
an unchanged save or a repeat of a travel action gives no reliable recipe
for selecting the next sample or changing the contours.

### Why a deposit can change at a fixed point

Later research observed geometry variation at one geographic source.
It explains how a fixed point could gain or lose a deposit between
reconstructions. The older disappearing-deposit account remains
source-reported, and actual extractor output across a verified local geometry
change remains unmeasured. The synthesis also explains the separate unresolved
Exotic setting question.
[Disappearing deposits and later evidence](../experiments/disappearing-deposits/subsequent-research.md)

## Evidence you can check

Use the [technical reference](../reference/resource-generation.md) for
predicates, frame contracts, original reports and reviews. Recount the
C1 coordinate distribution from the tracked CSV using the reference's
[tracked-input check](../reference/resource-generation.md#reproduction-and-access).
That check verifies the tabulated census and its percentages.

**PUBLICATION DEPENDENCY — EVIDENCE ACCESS PENDING.** The historical B2,
D5AK, D5AL, D5AO and D5AS observations and the C19 live availability evidence
have inspectable reports. Their decisive private chronology, geometry or
UI operands need separate cleared access. The proposed Save52 release
asset is unhosted. [Dependency graph](../audits/publication-architecture-d5ax/claim-evidence-dependencies.csv) ·
[Evidence-access assessment](../audits/publication-architecture-d5ax/evidence-access.md).
The [D5BE evidence index](../audits/evidence-access-d5be/README.md) tracks
access to the D5AS full geometry comparisons and C19 native UI comparisons.

The original Kreet unplaced-beacon experiment and the bounded check of
all 346 recorded native callbacks cover different parts of the preview
process. The release decision describes what the operator saw and which
comparisons the proposed download can reproduce.
[Kreet preview evidence tiers](../audits/publication-decisions-d5bq/README.md#historical-observations)
