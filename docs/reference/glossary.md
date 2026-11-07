# Project technical glossary

[Reference index](README.md) · [Guide index](../guides/README.md)

This glossary is for readers familiar with reverse engineering or Creation
Kit (CK) modding. Bethesda and CK names, recovered native labels, research
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

The project's label for a biome identity assigned through a specified
site/definition traversal. It characterizes that assignment rather than
all source biomes, all terrain within the outpost area or the resources
shown in the UI. State which field or coordinate supplied a biome.
[Biome assignment](../experiments/outpost-biomes/report.md).

### Coordinate frame

The origin, axes, units and transform context needed to interpret a
coordinate. In this project the native consumed descriptor, source-planar
comparison origin, saved site/base, outpost centre and beacon may differ.
“Original Int2” means the signed request coordinate pair in its request
frame, distinct from the source anchor and packed generator seed-cell
key.
[Source coordinate contract](../experiments/resource-retained-population/d5v-coordinate-contract.md) ·
[Original query conversion](../experiments/resource-retained-population/d5aq-mask-method.md#compiled-conversion-and-sampling).

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

Project shorthand for the reference identified through the outpost
Workshop ownership relationship in the audited ordinary joins. It is
the target of an ownership association. A beacon base definition, UI
entry or other active-registration record supplies different evidence.
Exceptional and retained relationships need their own proof.
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
| Registered production | An audited runtime association between a Workshop producer reference and a resource key plus row state. Save/load can restore the association through identity resolution. Registration makes the producer available for update under its gates. It cannot certify an inventory change. [Producer rows](../experiments/resource-retained-population/d5ah-extractor-continuity.md#what-is-serialized-and-reconstructed). |
| Realized output | An actual produced quantity delivered through the applicable output/inventory path. A nominal rate, due tick, pending count or registered resource describes a different stage. Current eligibility and destination fit matter. [Output path](../experiments/resource-retained-population/d5ah-extractor-continuity.md#unload-return-and-production). |

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

## Evidence language

These project reporting terms describe basis, premises or verification
coverage. Confidence and access eligibility are separate dimensions.
[Evidence and identifier standard](../EVIDENCE_STANDARD.md).

| Term | Meaning in a claim |
| --- | --- |
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
