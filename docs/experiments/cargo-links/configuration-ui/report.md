# C1: cargo-link configuration and management interface

2026-10-18, Australia/Sydney. SOR-EXP-0044 / SOR-EV-0052.
[Invoked brief](../../../implementation-briefs/README.md#archive-lookup) (`implementation-briefs.zip :: docs/implementation-briefs/CODEX_BRIEF_SOR_C1_cargo_link_configuration_ui_save.md`),
[contract](contract.md), [native contract](native.md), [Save52 case](save52.md),
[review](review.md), [functions](functions.csv), [source pins](sources.csv).

| UI field | Meaning and exact population source/gates | Refresh | Provenance | Save52 / screenshot explanation | Confidence / consequential limit |
|---|---|---|---|---|---|
| Available Outposts | Registered eligible Workshops with qualifying target references; enabled inclusion branch for same/different system, required keyword, reference resolution and occupied-target gates. Native `1417219c0` / `1417278b0`; SWF `aOutposts[].aTargets` | Candidate collection on menu initialization; list rendered on target-data update | Saved owner/base/link identities plus RECONSTRUCTED registration, handles and candidate arrays | VII-b and V appear; VII-b expands to the current Cargo Link | STRONG STATIC/SAVE; exact historical registry/list execution unobserved |
| Row order | Native ordinary registered-Workshop order followed by supplemental location-keyed target-map iteration; SWF preserves supplied parent/child order when filtering/expanding | Initialization/list rebuild | TRANSIENT | No alphabetic/distance priority follows from the two rows | STRONG within mapped population/list methods; no stable cross-load ordering guarantee |
| Selected pad / green arrows | Selection is a UI list index; linked arrows use outpost `bCurrentLink` and pad `bCurrentTarget`, obtained by comparing resolved references to existing target | Initial selection seeks linked child; navigation changes selection and comparison checks | PERSISTED pair; RECONSTRUCTED comparisons; TRANSIENT selection | Both arrows and footer identify VII-b as linked; child row is selected | STRONG; selection alone is not a successful pairing transaction |
| Left Outgoing Resources | `SourceRef.aOutgoingResources`: actual outgoing-child inventory entries, with base-container fallback through shared inventory iteration; not a declared export plan | Source population on opening; subsequent source comparison changes checkmarks without rereading its inventory | PERSISTED inventory/default definitions -> TRANSIENT resource rows | Feynman I outbox explicitly empty in Save52 | STRONG; historical screen timing and current load overrides unknown |
| Right Outgoing Resources | Selected child `aOutgoingResources`, same provider; selecting a parent row intentionally hides these panels | Target rows rebuilt on initialization/confirmed pick; hover/selection displays cached child rows and changes comparison checks | Same inventory provenance; TRANSIENT selection/rendering | VII-b outbox explicitly empty; screenshot selects a child, excluding parent-hide as its ordinary explanation | STRONG; no historical invocation trace |
| Left Build Resources Needed | `SourceRef.aResourcesNeeded`: recipe ingredients of qualifying **immediate** local destinations of the incoming child; `141723c80 -> 140f80af0 -> 140f7fd50` | Source population on opening; hover updates cross-end `bNeeded` comparisons | Definition/selected recipe and local graph -> RECONSTRUCTED/TRANSIENT rows | Incoming feeds Warehouse ff039669 directly; it fails builder/recipe-consumer predicate. Further-downstream Microsecond Regulator does not enter this direct-only query | STRONG; this is not a whole-outpost construction bill or transitive demand list |
| Right Build Resources Needed | Same direct-successor recipe query for selected destination's incoming child | Initialization/confirmed pick; selection renders cached rows | Same MIXED inputs -> TRANSIENT rows | VII-b incoming feeds Warehouse ff02c389 directly; Supercooled Magnet fabricators farther downstream do not populate it | STRONG; underlying production/delivery remains S2/C2, not measured here |
| Cargo Ship current/300 | `fCargoShipWeight`: ship inventory weight when pending target equals current linked target and ship resolves; otherwise 0. Max: effective ship capacity in that branch, source marker fallback otherwise. SWF rounds both values | Target refresh, not freight scheduling; visible if linked-name string nonempty | Inventory PERSISTED/default; effective capacity MIXED; displayed floats TRANSIENT | Both pads point to ff02dc37; its saved inventory is explicitly empty. Marker source sets default capacity 300; screenshot shows 0/300 | STRONG; zero can also be the unmatched/unresolved branch, not proof of a particular flight state |
| Names / planet / system / distance | Native `1417239e0`: current Workshop/reference name, location/system data and system displacement norm times LY scale; SWF concatenates planet/system and formats distance (precision argument 1) | Population/list update; right header follows selected parent | Saved site/name plus DEFINITION-DERIVED geography -> RECONSTRUCTED text | Feynman I and VII-b are in Feynman; 0 LY is system separation, not the interplanetary journey length | STRONG; names and distance are not physical pad UUIDs |
| Linked Outpost footer / Remove Link | Resolved current-link owner name; nonempty string enables linked UI state. Confirmed removal dispatches target handle 0 | Target data update; confirmation updates pending choice; menu close applies the relationship change | PERSISTED pairing -> RECONSTRUCTED name; TRANSIENT controls | Footer agrees with reciprocal saved relation | STRONG; ship creation can still fail after selecting an eligible endpoint |

**The empty panels have a positive ordinary explanation.** Save52 contains an
ordinary reciprocal pair between these sites, empty outgoing bays and an empty
cargo ship. Both incoming bays feed Warehouses first. The build-needs provider
does not recurse through those Warehouses to the fabricators. Linking two pads
does not populate an assigned-export list. No defect or freight-in-transit
assumption is needed to explain these fields together.

This is a **STRONG / STATIC + SAVE** scoped explanation, proposed for maintainer
review. Fresh byte/framing/hash results are PROVEN within their tested bounds.
The screenshot is a user-supplied observation associated with Save52, not an
atomic capture of that saved instant. No claim is made that its historical UI
session executed every traced branch. C1's ordinary mechanism is sufficiently
explained without a live observer; independent completion disposition is separate.

Coverage: installed retail 1.16.244.0, main ESM, installed Interface menu and
development script source, imported matching native database, protected mature
Save52 copy. Twenty-nine selected saved references, all 205,557 R3 records framed,
246 local edges, 80 physical definition rereads, four source ZIP comparisons and
100 selected ABC bodies. Winning load-order overrides, historical PEX/source
equivalence, live caches and freight lifecycle are not established by this study.
Raw/native/save/UI payloads remain LOCAL-ONLY; authored synthesis REVIEW-REQUIRED.

## Explanation ranking and negative cases

1. **Best supported:** empty outboxes/ship and immediate Warehouse destinations,
   as directly joined in [save52.md](save52.md). Inventory and demand are distinct
   providers. This predicts empty lists even with functioning downstream production.
2. **Supported alternative for another instant:** source rows can retain their
   opening snapshot; ordinary hover compares cached arrays without rereading inventories; confirmed pick refreshes targets and weight.
   Thus a later source stock change need not immediately appear. No such timing
   history was observed in this screenshot.
3. **Concrete UI alternative excluded for the ordinary pictured selection:**
   selecting an outpost parent intentionally hides target lists, but this image
   has the Cargo Link child selected. Parent-hide cannot explain both sides here.
4. **Not required / unsupported here:** defect, wrong endpoint, blocked remote
   receiver or returned freight. Local Warehouse ff039669 already holds 21
   Supercooled Magnets, yet the cargo child/ship can be empty. That coexistence
   proves neither shipment direction nor a return. Isotopic Coolant recollection
   remains unverified as stock/flow on this pair.

These conclusions would reopen on a same-build provider that recursively adds
indirect fabricators, a saved direct edge to a qualifying recipe consumer that
was missed, or nonempty selected bay inventory with the same native/UI inputs
yielding an empty list. Recipe requirements are not a reliable live production
diagnostic, nor is ship weight a shipment history.

## C2/C3 boundary and optional discriminator

C2 retains departures, loading/unloading, round trips, interruption, stranded or
returned freight and the user's hypothesis of undelivered cargo returning into
an origin incoming bay. C3 retains inter-system He-3, distant/unloaded transport,
saturation and recovery. C1 identifies their shared ship-reference/weight boundary;
it does not trace voyage simulation. [Backlog](../../../BACKLOG.md) preserves all
six requested deferred topics. S1/S2 local distribution conclusions are unchanged.

No new test is necessary to establish the direct-only provider. If historical
timing becomes consequential, a separately authorized small live test could open
this pair, change one known outbox stock, navigate away/back, then reopen. The
opposing predictions are source opening-cache retention versus immediate source
repopulation; the smallest discriminator is its displayed resource row before
and after reopening. This costs gameplay/save-state changes and is **not
authorized** here. A direct-pad-to-builder versus pad-to-Warehouse-to-builder
comparison would discriminate the documented direct-only rule, at greater cost
and with separate link/save protection authorization. No observer is proposed.
