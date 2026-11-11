# Project technical glossary

[Reference index](README.md) · [Guide index](../guides/README.md)

Use this glossary for technical terms and the
[research identifier index](../history/research-identifiers.md) for study labels. Bethesda and CK names, recovered native labels, research
abstractions and observer labels serve different purposes. Unless a cited
source establishes an original name, descriptive native names here identify
the audited role. Native behavior is scoped to the cited build and path.

## Geography and runtime geometry

### Geographic source

A researcher-defined term for a landscape contribution represented at
runtime by a Grid-owned allocation. Its geographic key describes chart,
anchor and terrain identity within a body/frame. The same key can describe
successive allocations. A request can use several contributors, and an
outpost area can intersect geometry from several sources. Historical
“source” can mean the geographic key, the allocation or a cited research
artifact. State the intended domain.
[Allocation and publication](../experiments/resource-retained-population/d5ah-lifecycle-matrix.md#owners-readers-and-release-boundaries).

### Grid

An audited native landscape structure that indexes local cell contributors
and owns the published source allocations. Shifting it can preserve sources
whose coverage still overlaps. Retaining the Grid does not pin each source.
The name here denotes that native role, distinct from a raster atlas or a
research plot's grid.
[Grid lifecycle](../experiments/resource-retained-population/d5ah-lifecycle-matrix.md#transition-matrix).

### ProcGen

The native procedural-generation module registered with the landscape
manager on the audited path. It owns the pointer-keyed population map and
separate visited storage. A reset can clear both without ending the
manager allocation. “ProcGen” names this specific module here. Procedural
generation in general includes other objects and stages.
[Module and reset receiver](../experiments/resource-retained-population/d5v-lifecycle-consumer-map.md).

### Population holder

A researcher label for the reference-counted native object retained by a
ProcGen entry keyed on the live source pointer. Its resource FormID slots
retain geometry collections. “Wrapper” appears in earlier records. Removing
the map owner releases its reference. Final destruction follows the
reference count. The holder is distinct from the Grid-owned source and
from a Workshop list.
[Holder and release evidence](../experiments/resource-retained-population/d5ah-lifecycle-matrix.md#native-release-addendum).

### Resource collection

In resource generation, a reference-counted native allocation retained by
a holder slot for one resource identity. It stores a region array whose
entries own point arrays. An outstanding collection reference can extend
the lifetime of those arrays beyond map erasure. This research label
does not imply an inventory, a list of admitted identities or continued
ownership of the geographic source.
[Nested layout and readers](../experiments/resource-retained-population/d5ah-lifecycle-matrix.md#owners-readers-and-release-boundaries).

### Region

In this subsystem, a native geometry record with bounds and nested point
data, grouped under a resource FormID. The records do not establish a one-to-one
mapping to gameplay deposits. Elsewhere a region may be a geographic or task
window. The shape and coordinate frame come from the relevant
representation, and “region” alone conveys neither outpost membership
nor a biome identity.
[Geometry contract](../experiments/resource-retained-population/d5ai-geometry-schema.md) ·
[Consumer qualification](../experiments/native-availability-map/region-contract.md).

### Deposit

Gameplay-facing term for a spatial occurrence of an inorganic resource
that a point or area query may encounter. It describes a resource in
terrain, whereas the native collection contains discrete geometry records
and a placed extractor has its own resource association. Treat “same
deposits” as a visual description unless a source/frame and comparison
scope are given.
[Point and area contracts](../experiments/resource-retained-population/d5v-lifecycle-consumer-map.md) ·
[Equal rebuild](../experiments/resource-retained-population/d5ak-a-report.md).

### Raster mask

A numeric sample used as a generator input. The audited ordinary sampler
uses the low nibble of a planetary raster byte in rarity comparisons.
“Mask” here is project shorthand for that sampled value. It differs from a
resource FormID, a rendered coverage polygon or a canonical geometry
class. The Special path can use different bits.
[Native sampling](../experiments/resource-retained-population/d5aq-mask-method.md#compiled-conversion-and-sampling).

### Nominal biome

A research term for a base BIOM FormID whose lookup cells overlap the
qualified nominal outpost disk with positive area. The raster and selected
frame supply the assignment. A resource source's BIOM input, blended terrain,
usable territory and UI resource list represent separate consumers.
[Biome coverage](nominal-biomes.md) ·
[Original assignment proof](../experiments/outpost-biomes/nominal.md).

### Coordinate frame

The origin, axes, units and transform context needed to interpret a
coordinate. In this project the native consumed descriptor, source-planar
comparison origin, saved site/base, outpost centre and beacon may differ.
“Original Int2” means the signed request coordinate pair in its request
frame, distinct from the source anchor and packed generator seed-cell
key.
[Source coordinate contract](../experiments/resource-retained-population/d5v-coordinate-contract.md) ·
[Original query conversion](../experiments/resource-retained-population/d5aq-mask-method.md#compiled-conversion-and-sampling).

### Saved site anchor

A saved angular pair associated with the typed site world. It describes site
geography and can supply a discrete base for a qualified site-based frame.
The occupied cell can differ, and the stored angles do not establish the
beacon's continuous coordinates.
[Position reference](position.md) ·
[Saved numerical controls](../experiments/coordinate-sufficiency/saves.md).

### Compensated Workshop centre

A local position computed from the ordinary reference XYZ and its Workshop
compensation vector, with a bit-preserving copy for the all-zero vector.
It can remain stable across a beacon move in qualified saved comparisons.
A current loaded centre requires the invocation and effective frame.
[Position specification](../position-model/specification.md#ordered-transformations).

### Terrain lookup cell

A discrete indexed address on a body chart. Its local preimage consists of
coordinates that quantize to the same integer offsets in a selected frame.
A biome raster pixel can label many such cells.
[Position conversion](position.md#qualified-conversion) ·
[Biome traversal](nominal-biomes.md#quantizer-cells-and-raster-lookup).

### PlanetContentManager

The native subsystem abbreviated **PCM** in the save research. It owns
content and placement data keyed separately by planet-data identity and
world identity. Global type 7 restores its seed and maps under the audited
loader, subject to resolution. Its records differ from resource region
collections and from the working state of the resource generator.
[Save-state classification](../experiments/resource-retained-population/d5ad-save-state-matrix.md).

## Lifetime and decisions

### Source retirement

The research label for ending one published source allocation, for example
after loss of Grid overlap. The mapped path erases its exact pointer-map
entry if present, releases ownership and frees the source. It leaves
visited storage in place. A surviving collection reference only protects
that collection.
[Retirement predicate and release](../experiments/resource-retained-population/d5ah-lifecycle-matrix.md#transition-matrix).

### Grid clear

A native operation on one Grid that releases its published sources and
matching map entries. It can be nested inside a broader reset. A clear
on another Grid need not end the target source. Historical observer
“clear fence” names an instrumented boundary, with scope determined by
its typed receiver.
[Receiver controls](../experiments/resource-retained-population/d5aj-invalidation-matrix.md#correct-the-receiver-domain-before-scoping-a-fence).

### ProcGen reset

Shorthand for the registered-module clear reached by the audited true and
false manager reset variants. It clears both the pointer map and the visit
store under exclusive protection. The Grid's source teardown has its own
edges, and module reset does not imply a new manager allocation.
[Reset predicates](../experiments/resource-retained-population/d5ah-lifecycle-matrix.md#reset-and-return-predicates).

### Map hit

A successful protected lookup of the full live source pointer in the
ProcGen map after the request passed the visited check. It skips
construction and can reuse a partial holder. Earlier “cache hit” wording
may refer instead to an upstream aggregate, a token match or a consumer
list. Identify the store and lookup.
[Observed lookup order](../experiments/resource-retained-population/d5ac-target-lookup-chronology.md).

### Visited-token bypass

The provider decision to skip map lookup when a content-derived source
token matches the visit store. The visit store and map have different keys
and lifetimes. A surviving token can suppress generation after the holder
has been erased. A token append can also follow incomplete generation.
[Visit and lookup path](../experiments/resource-retained-population/d5w-normal-path-model.md#arbitration-original-query-authority-and-retention) ·
[Retirement control](../experiments/resource-retained-population/d5ah-lifecycle-matrix.md#transition-matrix).

### Retained, reused and rebuilt

Research outcome labels. **Retained** means continuity of the relevant
live ownership over a stated interval. **Reused** adds actual use, such as
a protected lookup or consumer traversal. **Rebuilt** means a new
construction. “Rebuilt identical” adds a complete, qualified equality
comparison. These labels supersede ambiguous “persistent” when discussing
whether the same contour allocations survived.
[Player-action evidence legend](../experiments/resource-retained-population/d5av-player-action-matrix.md#evidence-and-outcome-legend).

## Forms, references and ownership

### FormID

Bethesda form identifier used for definitions and reference forms in the
applicable data/runtime context. Use plugin-qualified identities when
comparing definitions across load orders. A FormID, a packed saved
identifier, a runtime handle and a native pointer require different
interpretation and resolution rules.
[Identity discipline](../EVIDENCE_STANDARD.md#address-and-identity-discipline) ·
[Resolved availability identities](../experiments/native-availability-map/output-contract.md#storage-and-identity-domains).

### EditorID

CK-facing textual identifier used to find or refer to an authored form.
It is separate from the numeric FormID, a localized display name and an
identity assigned to a placed instance. Keep plugin context when
resolving an authored identifier. [Definition examples](../experiments/inorganic-extractors/definitions.md).

### Saved identifier

A serialized value representing an identity in a particular record
grammar. Its meaning depends on the field, save tables and reader. It may
resolve or remap to a current reference and then to a runtime handle.
Use the decoded identity separately from its original bytes and offset.
[Save identity rules](../EVIDENCE_STANDARD.md#address-and-identity-discipline) ·
[Producer remap](../experiments/resource-retained-population/d5ah-extractor-continuity.md#what-is-serialized-and-reconstructed).

### Runtime handle

An engine token resolved through the current runtime's reference machinery.
It can become invalid or fail to resolve. A restored producer can receive a
current handle from a saved identity. Numeric equality across loads does not
establish continuity, and a handle is not directly dereferenceable as an
address.
[Producer handle resolution](../experiments/resource-retained-population/d5ah-extractor-continuity.md#what-is-serialized-and-reconstructed).

### Native pointer

A virtual address used by native code to refer to an object or location.
Reading it requires the appropriate process and valid object lifetime.
A borrowed pointer can remain in an alias after the object ends, and its
numeric address can later be reused. A pointer copy does not confer an
ownership reference.
[Source alias census](../experiments/resource-retained-population/d5ab-p1-source-identity-lifetime.md).

### Base object

The CK definition that supplies type and properties for instances.
Multiple placed references can share it. Effective properties can depend
on additional state or overrides. Save and runtime records can carry
the base identity separately from the identity of the placed object.
[Extractor definitions](../experiments/inorganic-extractors/definitions.md) ·
[Separate base and producer identity](../experiments/resource-retained-population/d5ah-extractor-continuity.md#what-is-serialized-and-reconstructed).

### Placed reference

An instance of a base form in the world, with its own identity and
instance state. “Reference” in CK/object discussions usually means this
entity. A C++ ownership reference, pointer or handle is a different
concept and has separate lifetime rules.
[Workshop membership](../experiments/workshop-membership/report.md).

### Workshop owner

A placed reference that serves as the owner target for Workshop members.
In the audited ordinary saves, the unique mode-0 WorkshopItem link targets
the beacon reference. Loaded metadata can affect native resolution.
Registration and a beacon's base form are separate evidence.
[Workshop ownership and membership](../experiments/workshop-membership/report.md) ·
[Active population limits](../experiments/workshop-population/report.md).

### Outpost beacon

The placed gameplay object used to establish and interact with an outpost.
Distinguish its base form, placed identity, saved state and physical
position. An ordinary beacon record is evidence for a site under the
audited framing. Its presence alone cannot certify active membership or
that its position equals the native outpost centre.
[Beacon evidence](../experiments/active-outpost-identification.md) ·
[Position model](../position-model/specification.md).

### Construction root

A representative placed reference for one physical Workshop construction
in the project's qualified projection of the native item model. A direct
item can represent itself. A compound PackIn uses a qualifying dummy.
Generated members and foundations do not each add a root.
[Root selection and correction](identity.md#counting-physical-roots).

### PackIn

An installed compound-object template (PKIN). An instance can have an
ordinary construction representative, generated members and foundations
linked through qualified saved relationships. A template definition alone
cannot establish that a particular instance was placed or saved.
[Ordinary construction controls](../experiments/workshop-membership/validation.md) ·
[Variant assemblies](../experiments/construction-variants/report.md).

### Canonical assembly

A research grouping of references deduplicated by qualified source,
replacement and group relationships. It can identify retained structure
without proving ordinary Workshop ownership or how the structure was built.
[Retained Hab challenge](../experiments/workshop-population/report.md#completed-location-context-challenge).

### Workshop registry and Almanac entry

The registry is a runtime collection of Workshop handles. An Almanac entry
is a UI record produced after handle resolution and filtering. A saved owner
edge and active player control require separate evidence.
[Native enumeration](../experiments/active-outpost-identification.md#independent-native-membership-route-and-exact-obstruction).

## Construction decisions and state

### Recipe quota

An admission predicate that compares the selected Workshop's matching
construction representatives with the effective shared limit global.
An ordinary COBJ JNAM supplies the group key. The player's deployment
allowance and the scalar build budget are separate decisions.
[Numerical limits](../experiments/limits/report.md).

### Build budget

A scalar construction allowance used when the budget gate is enabled.
A valid positive effective Workshop allowance takes precedence over the
configured fallback. Admission compares the allowance with current
effective usage plus candidate charge. Assemblies can sum charges from
eligible members. The meter uses a cached ratio. The serialized base
usage is one input to restored state and is not a census of objects.
[Accounting and saved controls](construction.md#scalar-budget).

### Snap Behavior

A CK STBH form containing rules for a component's snap context. Grouped
condition-eligible entries can supply manual CHANGE choices. Ungrouped
rules can respond to connections. These are separate from pre-placement
recipe variants.
[Hab and automatic rule trace](../experiments/construction-variants/report.md).

### Workshop bulldozed state

A reference state used for confirmed scenery suppression in the mapped
construction path. The live reference bit and saved change mask have
different domains. Load or cleanup can restore or clear suppression.
Preview clearing has a separate transient state.
[Writer, loader and cleanup](../experiments/spatial-placement/persistence.md).

## State origin and authority

These project classifications answer different questions and can coexist.
For example, an identity can be persisted, its current handle reconstructed
and its eligibility cached. State the writer, reader, restoration order
and effective consumer when claiming authority.
[State rules](../EVIDENCE_STANDARD.md#state-and-integration-claims) ·
[State register](../state-register.md).

| Term | Definition and distinction |
| --- | --- |
| Persisted | A value or representation carried in a saved channel. A writer and record witness establish the representation. A reader and consumer establish what it can control after load. |
| Reconstructed | Runtime state rebuilt from inputs such as saved values, definitions or current context. For example, resolution builds a current producer handle from a saved identity. Restoring an input and rebuilding a dependent structure are separate steps. |
| Inherited | Effective state supplied by a definition or another owner rather than separately recorded as an instance value on the named path. A saved reference to the definition can coexist with inheritance. |
| Derived | A result computed from identified inputs. Specify whether the engine computes it or researchers compute it offline. Derived values may themselves be persisted or cached. |
| Cached | A retained result that can be reused under the owning reader's refresh rules. A cached list can survive changes to its input geometry. The term alone gives no save or lifetime guarantee. |
| Transient | State limited to the audited runtime path and lifetime, with no restoration of that representation through the audited saved channels. Transient state can be long-lived in one process and can be reconstructed on demand. |

[Worked save and runtime classifications](../experiments/resource-retained-population/d5ad-save-state-matrix.md).

## Availability and production

| Term | Entity and behavior |
| --- | --- |
| Resource availability | A result for a stated consumer and scope. **Available Resources** is the game's UI component/list assembled from operation-owned populations. Its area-level identities differ from point admission, nominal biome and stock availability. [UI contract](../experiments/native-availability-map/output-contract.md). |
| Placement eligibility | The outcome of a validation branch for an object and target location. For ordinary natural extractors the audited branch intersects a point-admitted resource set with effective produced-resource properties after bypass checks. This gate differs from registration and later operation. [Placement evidence](../experiments/resource-retained-population/d5ah-extractor-continuity.md#placement-and-registration-use-distinct-resource-operations). |
| Resource property | An AVIF-keyed actor value on a definition or reference. In the ordinary builder menu, presence in the base property sheet can support a recipe even at value zero. A positive effective resource value can identify a current selection or be consumed during registration. [Admission](fabrication.md#catalogue-identities-and-selection). |
| IRES | The form type for a resource definition. The audited production paths use a resolved IRES as a Workshop producer-map key. It links a resource AVIF, production recipe and usually an interval global. A recipe can also refer to an IRES as an ingredient, which the inventory path can resolve to its item. [Extractor identity example](inorganic-production.md#definition-and-placement). |
| COBJ | The form type for a constructible recipe. A construction COBJ can select a facility or family list. A production COBJ can identify a builder-menu row and define ingredient counts and a product. These are distinct roles of the same form type. [Fabricator identity table](fabrication.md#catalogue-identities-and-selection). |
| Registered production | An audited runtime association between a Workshop producer reference and a resource key plus row state. Save/load can restore the association through identity resolution. Registration makes the producer available for update under its gates. It cannot certify an inventory change. [Producer rows](../experiments/resource-retained-population/d5ah-extractor-continuity.md#what-is-serialized-and-reconstructed). |
| ExtraWorkshop producer row | Runtime record in an ExtraWorkshop resource-keyed array, with a producer handle, base FormID, bookkeeping, iterations, timers and cached eligibility. The save representation stores identities and scalars in its own order. A due update resolves the handle and evaluates current eligibility. [Row and wire fields](inorganic-production.md#saved-channels-and-return). |
| Production reason | A numeric result of native evaluator `0x140f7d120` on the mapped build. Zero marks current eligibility. Reasons include applicable missing power, insufficient ingredient stock on the input branch and production halt. The row's cached eligibility is separate. [Current state](inorganic-production.md#scheduling-current-state-and-delivery). |
| Domesticability knowledge | A scanner category stored by planet and species in the native knowledge manager. The organic selector reads it to classify a supported candidate as known or unknown. It differs from the species' domesticability condition and from ingredient supply. [Knowledge writer and reader](organic-production.md#facility-species-and-knowledge). |
| Due cycle | A scheduler-derived opportunity to request work from a producer row. The count depends on engine elapsed time, interval and countdown. Current eligibility, ingredient caps and receiver acceptance can prevent a due cycle from becoming delivered inventory. [Timing path](inorganic-production.md#scheduling-current-state-and-delivery). |
| Local transfer link (output link) | A directed source-to-destination relationship. The runtime transfer registry indexes each destination handle by its incoming source set. Production can use it to find a downstream receiver or count upstream ingredients. Electrical connections and Workshop ownership use other stores. [Input graph](fabrication.md#reconfiguration-input-graph-and-delivery). |
| Realized output | An actual produced quantity delivered through the applicable output/inventory path. A nominal rate, due tick, pending count or registered resource describes a different stage. Current eligibility and destination fit matter. [Output path](../experiments/resource-retained-population/d5ah-extractor-continuity.md#unload-return-and-production). |

## Inventory and local links

| Term | Entity and behavior |
| --- | --- |
| Item stack | A quantity of one item form grouped in a single inventory entry. Separate stacks of that item can carry different per-stack extras. The reference inventory writer can persist those extras and quantities. [Wire fields](storage-and-output-links.md#persistence-and-remote-update). |
| Effective capacity | The current weight value read by an applicable fit or fullness check. For an ordinary non-actor store it comes from effective CarryWeight and can differ from the base fallback through reference overrides or modifiers. [Capacity and admission](storage-and-output-links.md#definition-effective-capacity-and-pair-gates). |
| Producer output buffer | The inventory on a producer reference that can keep its products. A downstream receiver can instead receive fresh output, and builder ingredients can be withdrawn from separate upstream inventories. [Creation path](storage-and-output-links.md#graph-movement-and-creation). |
| Source inventory and target inventory | Roles in one transfer operation. The source supplies the stock being removed and the target receives it. An intermediate graph node need not act in either role for that call. ContainerMenu can also substitute another reference for the selected target. [Movement](storage-and-output-links.md#graph-movement-and-creation) · [Shared target](shared-storage.md#fixture-admission-and-backing-ownership). |
| Transfer Container | An ordinary placeable local store whose installed special keyword supports ship access. Its local output links use ordinary pair gates and its stock belongs to the placed reference. [Storage roles](../guides/storage-and-output-links.md#choose-a-store-for-the-item-and-the-operation). |

## Cargo and time

| Term | Entity and behavior |
| --- | --- |
| Cargo incoming and outgoing children | Two placed inventory references in a pad assembly. Freight unloading targets the incoming child and loading draws from the outgoing child. Local graph permissions and cross-outpost shipment have separate gates. [Cargo stages](cargo.md#endpoint-and-stage-ownership). |
| Cargo ship hold | The inventory on the route's ship reference. It can retain stock that failed to fit at the last dock, and the next leg can add stock from that dock's outgoing child. [Return model](cargo.md#repeat-the-worked-round-trip). |
| Fuel marker | The inter-system pad reference registered as a recipe consumer. Its due work requests He-3 removals on reachable upstream sources. Its charge and halt state are separate from those inventories. [Fuel cycle](cargo.md#fuel-readiness-and-accepted-cycles). |
| Cargo timer | A native VM game-time heap entry keyed by a bound ship script and ID. Due dispatch queues a load, departure or retry callback. Its saved remaining time and pause state have their own channel. [Clocks](cargo.md#clocks-and-native-completion). |

## Ingredient providers and reporting

| Term | Entity and behavior |
| --- | --- |
| Shared backing inventory | The stock on the player-held reference that recognized Shared Outpost Storage fixtures expose. The player save channel carries its inventory, while fixture placement and membership use separate channels. [Backing ownership](shared-storage.md#fixture-admission-and-backing-ownership). |
| Provider source vector | An ordered temporary list of references whose inventories a particular ingredient operation can consider. Crafting and construction build different lists, and spending walks each actual list forward. [Source order](shared-storage.md#providers-counts-and-removal). |
| Virtual removal | An inventory-removal request dispatched through the source reference's native virtual interface, such as slot `0x458` on the mapped build. A request or its planned count cannot establish a completed mutation by itself. [Removal path](shared-storage.md#providers-counts-and-removal). |
| Resource aggregation | The Locations collector's per-outpost sum of admitted stack units keyed by associated resource FormID. The physical items and the UI's resource definitions can have different identities. [Aggregation](stored-resources.md#item-identity-units-and-presentation). |
| Refresh epoch | The collection and delivery context of a UI snapshot. For Locations, entry collection includes inventory, queued delivery replaces provider arrays, and selection can repaint copied values while requesting body metadata separately. [Inventory lifetime](stored-resources.md#collection-delivery-and-saved-boundaries) · [Locations providers](locations-ui.md#collector-and-refresh-lanes). |
| Locations entry | A copied row for a Workshop reference admitted by the Locations collector. It carries reference, body and system identities and sampled summary lanes for selection and display. The row's Crew badge uses assignment-list length. [Collector and fields](locations-ui.md#collector-and-refresh-lanes). |

## Assignments and defenses

| Term | Entity and behavior |
| --- | --- |
| CrewExtraData (ExtraE2) | Data on a destination reference that holds its crew assignment handles. Its save writer records actor identities for load-time resolution. CrewAssignment on the actor supplies a separate destination relationship. [Membership](crew-and-robots.md#admission-ownership-and-roster). |
| Possessed perk rank and active perk entry | A rank selects a perk's effects. Registration can create active entries in the actor's process storage for particular engine queries. The roster can report possession while those entries are unavailable or fail a query's conditions. [Dispatch](crew-and-robots.md#from-rank-to-a-consumer). |
| Robot construction quota | A threshold shared by recipes that point to the same robot limit global. The selected Workshop's qualifying representatives consume it. Crew slot costs and active robot effects are evaluated elsewhere. [Quota](crew-and-robots.md#admission-ownership-and-roster). |
| Attack opportunity timer | A one-shot beacon-script timer armed by load or qualifying placement. Its callback attempts the eligibility and encounter checks. A timer callback can finish without an attack. [Script branches](defense.md#opportunity-eligibility-and-quest-lifecycle). |
| Integrity | Build Mode's selected-object Health ratio, computed from effective current over permanent Health on the qualified paths. The card hides the invalid-denominator sentinel. The destroyed flag and Health damage have separate writers. [Indicator](defense.md#health-state-flags-and-repair). |

## Display and access

| Term | Entity and behavior |
| --- | --- |
| Display slot and displayed item reference | A slot rule admits a compatible item under filter and count conditions. The fixture's runtime display component records the handle of the represented world item in that rule's list. A saved list instead uses item identities. [Residence and fixup](containers-and-displays.md#runtime-residence-and-ownership). |
| Mannequin equipment | Instance and slot selection owned by the mannequin actor. Equipping updates the actor's equipment state using inventory rows. It uses a different mechanism from mounting an item on a display case. [Equipment and save channels](containers-and-displays.md#serialized-joins-and-fixup). |
| Saved record framing | The byte grammar that determines a record's boundaries and divides optional header fields, queues and body. It gives a safe region to decode. Record type, identity and payload meaning still require supported interpretation. [Framing](access-and-save-framing.md#frame-the-sample-before-interpreting-a-field). |
| Capability surface | The specific definition, script or configuration route checked for an action. Its status describes the evidence for that route and action, including a declaration or an established consumer where applicable. [Capability matrix](access-and-save-framing.md#capability-and-access-matrix). |
| Native Papyrus declaration | A script signature marked native that describes an engine-bound operation. The declaration gives the callable name and argument/return contract in that script context. Native registration, installed use and validated external integration each need separate evidence. [Declarations](rc1/papyrus-interfaces.md). |

## Electrical state

| Term | Entity and behavior |
| --- | --- |
| Generator rating | Definition-supplied PowerGenerated base for an ordinary variant, before instance modifiers, qualifying crew and electrical graph admission. [Ratings and contribution](power.md#ratings-effective-contribution-and-fuel). |
| ExtraPowerLinks (ExtraCB) | A per-reference extra with ordered FormID and connection-word entries. Words distinguish simple, automatic, explicit and qualified spline-mediated relationships. Load resolves the saved identities for current traversal. [Electrical graph](power.md#typed-graph-and-allocation). |
| Powered bit | ExtraFlags (Extra9C) mask `0x40` on the audited references. It can preserve the previous allocation result in a save and change when current allocation applies differences. It describes a different state from the switch's open state and a producer's cached reason. [Saved power and authority](power.md#saved-edges-flags-and-load-authority). |
| Cumulative demand | The binary32 total of eligible base PowerRequired values added in consumer discovery order during the mapped allocation. A consumer's demand stays in the sum when the consumer fails to fit. [Allocation example](power.md#typed-graph-and-allocation). |
| Generator charge | The ordinary fueled generator's WorkshopProduceUntilNextCycle actor value. It distinguishes Charged and Uncharged states for the due-cycle transition logic. The transitions can change effective contribution, while current reachable fuel stock is evaluated separately. [Fuel transitions](power.md#ratings-effective-contribution-and-fuel). |

## Addresses and offsets

These are standard RE terms applied to the pinned build or specified
artifact. Record the domain with every numeric locator.
[Address discipline](../EVIDENCE_STANDARD.md#address-and-identity-discipline) ·
[Build and method pins](../PROVENANCE.md).

| Term | Domain and use |
| --- | --- |
| Static VA | Preferred-image virtual address in an executable or static analysis database. Subtract the preferred image base to obtain its RVA. It need not equal the relocated address in a process. |
| RVA | Relative virtual address within the loaded image layout. Add it to the actual module base for the corresponding runtime VA. It is distinct from the byte position in the PE on disk. |
| Runtime VA | Actual virtual address in one running process, such as a relocated instruction or heap object. A heap pointer need not have a module RVA. |
| Native offset | Byte displacement from an explicitly named native object, structure or other runtime base. A member displacement such as ProcGen `+0x40` requires that object's layout and differs from an image RVA. |
| Source-file offset | Byte position in a named input file. A decompressed-stream offset instead locates a byte in the logical payload. State which representation supplies the offset, since compressed save bytes, logical save bytes and PE file bytes have separate domains. |

## Input, identifier and timing notation

| Term | Definition and distinction |
| --- | --- |
| N244 and H? | N244 refers to the principal pinned Starfield 1.16.244.0 native and installed-definition baseline. H? marks an unknown historical executable of origin. A save's embedded version metadata does not establish an originating executable hash. [Build and input identities](evidence-access.md#build-and-input-identities). |
| ESM, BA2 and PEX | An ESM supplies installed game definitions such as resource and recipe forms. A BA2 is an archive of installed assets such as terrain inputs. PEX is compiled Papyrus script code. Declarations, compiled script behavior and actual native execution have separate evidence. [Access layers](access-and-save-framing.md). |
| Papyrus virtual machine (VM) | The engine's script execution environment. A queued, due game-time callback still requires dispatch and execution. A native recipe scheduler or flight package has its own clock and admission conditions. [Cargo clocks](cargo.md#clocks-and-native-completion). |
| Saved RefID token | In qualified R3 framing, a three-byte big-endian tagged reference operand whose interpretation uses save-local tables and remapping. A decoded reference identity can resolve to a runtime handle. [Framing](access-and-save-framing.md#frame-the-sample-before-interpreting-a-field). |
| Epoch | The interval or snapshot in which an identity, pointer alias, graph, timer or UI payload is meaningful. A matching address or source key alone cannot establish continuity across retirement or a fresh process. [Lifetime](resource-generation.md) and [UI refresh](locations-ui.md#collector-and-refresh-lanes). |
| Vtable byte offset | Displacement from a named virtual method table, separate from a slot index or a field offset in the receiver object. For example, SD1 uses byte offset 0x130 from the item interface's table. [Native example](../experiments/containers-displays/native.md). |
| Bit mask and bit index | A bit mask selects positions in a field. The mask 0x10 selects zero-based bit 4. A multi-bit raster sample, a saved change mask and a native extra tag use separate domains. |
| Nominal and effective | Nominal describes the stated model or base conditions, such as a horizontal outpost disk or base rate. Effective describes the active inputs and gates of a particular consumer, such as clipped territory or a rate under current modifiers. Realized output further requires an observed result. [Biomes](nominal-biomes.md) and [production](inorganic-production.md). |

## Evidence language

These project reporting terms describe basis, premises or verification
coverage. Confidence and access eligibility are separate dimensions.
[Evidence and identifier standard](../EVIDENCE_STANDARD.md).

| Term | Meaning in a claim |
| --- | --- |
| PROVEN, STRONG, PROVISIONAL and OPEN | PROVEN means decisive evidence within an explicit scope. STRONG means substantial independent support with a material gap. PROVISIONAL is an unconfirmed model. OPEN has no accepted explanation. Record coverage separately. [Evidence standard](../EVIDENCE_STANDARD.md). |
| STATIC, SAVE, RUNTIME and SOURCE-REPORTED | These identify the source of support. STATIC maps definitions or code. SAVE decodes a named serialized sample. RUNTIME records activity under the stated observation or execution. SOURCE-REPORTED attributes an account to its origin. CROSS-VALIDATED joins independent bases with the stated limits. |
| Fixed native fixture | A bounded native-code stage run with exact supplied inputs and host. Independent execution or comparison is recorded with the individual result. Its controlled output or refusal is distinct from what an instrumented retail session observed. [Fixed-stage route](evidence-access.md#fixed-native-geometry). |
| HELD and HISTORICAL ONLY | HELD marks an affected evidence or release route awaiting a stated condition. HISTORICAL ONLY retains the attributed report and its original scope without an exact selected replay tier. These are access or selection statuses. [Scope](../first-release-scope.md). |
| Local qualification and publication clearance | Local qualification checks a named route with exact inputs in a stated setting. Clearance requires approval of exact contents, rights and privacy, transfer, candidate verification, and authorized release. PENDING RELEASE indicates that proposed assets are still unavailable as release downloads. [Access](evidence-access.md) and [publication policy](../PUBLICATION.md). |
| Observed | Recorded for a particular sample or event through a named acquisition. A trace, decoded bytes and operator report have distinct origins. Inferred cause or missing events require further evidence. |
| Inferred | Interpretation derived from observations or static relationships, with reasoning and counterexamples stated. A geometry-class match supports a proxy without directly observing the original sample. |
| Conditional | Supported consequence if specified premises hold. A proven native branch can remain conditional for a player's unrecorded action. |
| Reproduced | Obtained again with declared inputs and comparison criteria. Repeating arithmetic on a tracked table verifies the aggregate. Reproducing an original event or native output has different prerequisites. |
| Independently verified | Checked by a separate reviewer or genuinely independent method over stated evidence and exact scope. A review of an aggregate, source code or access route does not imply raw-event replay. |
| Capture ID | Observer-assigned label for an acquisition or schema record, such as a UUID. It helps join evidence and has no native object or save identity semantics. [D5AS qualification](../experiments/resource-retained-population/d5as-producer-profile.md#exact-producer-and-admission). |
| Canonical geometry body | Research comparison format that preserves specified native geometry bytes in a stable resource order. Older envelope-inclusive normalization includes extra source and frame metadata. Equality is scoped to the represented content and frame. [Byte domains](../experiments/resource-retained-population/d5as-producer-profile.md#pilot-and-byte-domains). |

Extend these entries when another guide introduces a materially different
meaning or a better-qualified definition. Preserve historical labels and
cite the result that supersedes them.
[Authoring standard](../guides/AUTHORING-STANDARD.md).
