# Tracker and Planner positional dependency audit

2026-10-13. Specialist independently inspected maintainer-owned
`D:/Projects/starfield-outpost-network`, HEAD
`9e3005aff9487f11343b39a7534a2070b429ad5f`, clean read-only status.
SOR-P-0002 covers consultation. No sibling code copied/executed/edited.
An initial Git ownership check failed; command-local safe.directory allowed
read-only inspection without changing configuration.

**Neither historical native Z reconciliation nor exact subcell longitude/latitude
demonstrably blocks the current Tracker or documented network Planner direction.**
Current product evidence is the schema itself: `src/domain/models.ts:123` has
outpost id/name/systemId/bodyId, selectedBiomeIds, localResources,
explicitResourcePresence, activeProduction, manufacturing, plannedSupply,
cargoPads; no world position or deposit map. README:3–33 describes current
features; DOMAIN-RULES:1367 describes a notebook with planning assistance.
BACKLOG:454–467 proposes manufacturing/logistics/capacity and potential in-game
integration, without specifying a spatial construction planner. These are source
reports, not new user-approved final requirements.

| Feature / status | Required positional capability | Sufficient now | Fallback | Specific blocked operation |
|---|---|---|---|---|
| Current create/name/select/reorder | None | Stable application ID; names/order metadata | Manual entry | None from positioning |
| Current planet/system assignment | Body/system identity | Reference IDs and manual selection; qualified research save association | Manual selectors | Automatic save crosswalk/import remains unimplemented/separately scoped |
| Current multiple same-body outposts | Distinct application IDs | Duplicate body/name representable; IDs distinguish records | Manual labels/context | Universal automatic cross-save merging unproven; coordinates are not identity |
| Prospective save identification | Ordinary domain, typed IDs, ambiguity | Scoped detector and Save25/26 correspondences | Present unresolved candidates | Silently merge unqualified/remapped representations |
| Current cargo links/supply provenance | Endpoint outpost/pad IDs, system IDs | Existing categorical graph | Manual endpoints | No native Z/lonlat blocker |
| Current resources/active production | Body/biome references and separate presence/production assertions | Manual localResources, activeProduction, explicit X-Tech presence | Manual recording | Infer deposits or actual production from coordinates alone |
| Future biome resource combinations | Body/biome occurrence and product rules | Existing reference facts and selected-biome scope | Recommendations plus site confirmation | Exact deposit intersection finder lacks geometry/availability evidence |
| Current manufacturing / future network planning | Recipes, categorical inputs, capacities/logistics | Qualitative fixed-point feasibility today | Manual network editing | Quantitative power/rates/flow need other domain semantics |
| Prospective structure inventory | Authoritative membership and instance IDs | Object/resource classification and tentative beacon links only | Manual or unresolved associations | Assign every recognized structure to its authoritative outpost |
| Prospective local object/deposit view | Same-frame object transforms and separate deposit geometry | Own case5 transforms; scoped compensated center and horizontal model | Label qualified subset/frame | General cross-parent layout and deposit overlays |
| Prospective construction placement | Common3D frame, terrain/collision/extents/support and placement authority | Prior saved locations are observations only | In-game/manual placement | Guarantee new placement eligibility; vertical rules may need Z but remain unresearched separately |
| Prospective proximity/overlap/boundaries | Common frame, effective radius and boundary semantics | Qualified local2D comparison as diagnostic | Estimates/manual checks | Authoritative buildable boundary or global metric overlap |
| Potential in-game integration backlog | Chosen operation, validated interface/lifecycle and authority | No concrete operation chosen | Read-only reporting if separately approved | Safe writes/place/teleport unvalidated; broad blocker cannot be assigned to Z alone |

## Specialist discoveries adopted

1. Geometry is absent from the actual persisted product schema. The matrix
   consequently does not gate current Tracker readiness on universal XYZ.
2. Empty selectedBiomeIds means all valid body biomes (DOMAIN-RULES §53), not
   observed site biome. Position cannot silently populate geographic biome truth.
3. Organic farming is body-scoped. More precise coordinates do not improve that
   current eligibility calculation.
4. Local presence and active production are different assertions (§6–7).
   Recognizing an extractor/resource does not justify production/deposit truth.
5. Avoiding finicky sites is backlog direction, not a specified exact site finder.
6. Cargo type follows system IDs (`cargoConnections.ts:128`), not physical distance.

Research cross-check: [extractor report](../experiments/extractor-resource-association.md)
leaves `containing_outpost=UNRESOLVED` despite63 mature extractor beacon-link
leads. [Object transforms](../experiments/durable-outpost-center-and-object-transforms.md)
have distinct parents and the negative-X frame counterexample. Neither proximity
nor existence of a native geometry consumer establishes authoritative membership,
ore availability, effective radius or placement eligibility.

## Consulted product provenance

Paths below are relative to the sibling repository at the pinned HEAD. Consultation
and substantive discoveries credited here and in project SOURCES/CREDITS; no
third-party incorporation, external source or new dependency.

| Path / decisive locations | SHA256 |
|---|---|
| README.md:3–33,289 | ad063a372d1370ae690674106efbc361048a6ce90afbcd173f37ecae0b67a0bb |
| src/domain/models.ts:123 | 87c82d46987de9c66f26208e507dfeb72eaa63e81a0c9fe6a0582918a2f29890 |
| docs/DOMAIN-RULES.md:158,229,274,299,1214,1227,1367 | c88f647de1e54780ba7ab0e241a562a9ef8bf41ae19421fed6327c4f88bef6fd |
| docs/BACKLOG.md:121,143–161,454–467 | c3ffb59ea307063d3684768a2f358efba819bcedac87c9f8c7a394e412f632b7 |
| src/domain/cargoConnections.ts:128 | a1f122609ca6d7a925c913b9c71d42776310313cf3b92372b7fb4ea6908fb4a0 |
| src/domain/bodyResourceAvailability.ts:75 | 726027e2b36c973bd4da7e28ba2e2a913ae01c1a0331136009a1f3e6b71a4e55 |
| src/domain/resourcePresence.ts:35 | d0a5a3a843fc101a88152e12a4cb75824af49a67137f95bb986bc7072ccc8813 |
