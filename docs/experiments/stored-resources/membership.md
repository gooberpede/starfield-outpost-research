# Ordinary inventory inclusion

[Provider](provider.md), [aggregation](aggregation.md), [physical controls](source-controls.csv).
All ordinary yes/conditional results require a qualifying enumerated Workshop,
reverse WorkshopItem membership, successful reference resolution, TESContainer
capability and effective **OutpostBuildContainer != 0** in `141368cf0` (n014).
This is the actual callback reused by SD2 construction, not an inferred rule from
the AV's name. SD2 n026 and fresh SD3 n030 bind DFOB `00f659` -> AVIF `00f65a`;
fresh definitions01 physically rereads both records.

| Population | Ordinary result | Predicate, control and qualification |
|---|---|---|
| Solid/liquid/gas/warehouse storage, small/medium/large | Conditional included | All 12 selected bases have AV 1; capacity/filter affect physical stock, not this source admission |
| Inorganic extractor buffers | Conditional included | All 154 selected main-game OutpostHarvester bases have AV 1; no extra power/production-status gate in callback |
| Greenhouse and husbandry output buffers | Conditional included | All six S1/E2 builder bases have AV 1; reports actual held resource items, not recipe input availability |
| Ordinary automated fabricator output | Conditional included | Ordinary S1/E3 builders have AV 1. Exception: OutpostBuilderSupplyMission `1fa848` omits it; don't generalize from prefix alone |
| Incoming cargo compartments, ordinary/inter-system variants | Conditional included | `219173/100b62/2a6c3b` AV 1, with a real positive saved witness |
| Outgoing cargo compartments | Excluded when effective AV is zero | `219171/100b63/2a6c3a` omit base AV; omission is not measurement of an effective override. Saved stock and freight eligibility do not override the callback |
| Transfer Container | Conditional included | `2ce194` AV 1; special ship-transfer access is not needed for SD3 |
| Constructed ordinary chests, safes and lockers | Conditional included | Example `2779fc` AV 1 despite both local-link prohibitions. Use exact source-controls row for variants; appearance alone is not admission |
| Weapon/display cases and racks | Conditional on effective AV; selected defaults omit it | CONT capability alone fails the AV gate. Example helmet stand `363cc8` and three racks omit AV. Mounted references are not separately enumerated as fixture inventory |
| Loose displayed-item references | Excluded as independent sources by this ordinary path | No display-slot/reference sweep. They would need their own qualifying source capability/AV/membership; equipment appearance is insufficient |
| Mannequin actor inventories | Conditional; ordinary effective eligibility unresolved | 26 selected NPC bases omit AV; actor template/effective values are not reconstructed here. No actor-roster or equipment-slot scan is added |
| Physical Shared Outpost Storage | Substituted, not summed physically | SD2 keyword helper `140b64da0` recognizes it; callback takes player+1008 and inserts it once if nonnull |
| Player-held shared backing inventory | Conditional included once per qualifying outpost aggregate | An eligible member fixture exposes it; several access fixtures do not multiply it. A missing backing reference inserts nothing |
| Player's ordinary inventory | Excluded as independent source | No player append in `141360e80`; +1008 substitution does not enumerate player pockets |
| Selected ship cargo | Excluded as independent source | No ship selector in this collector, unlike SD2 crafting/construction |
| Other/remote inventories | Conditional only through actual membership/substitution | No radius/same-planet/3D gate in callback; no generic census of remote chests or other outposts as sources for this outpost |
| Invalid/unresolvable/unregistered Workshop | No entry in this invocation | Outer registry/ACTI/keyword/ExtraBC gates; saved enabled beacon alone cannot establish entry |

This matrix separates **source eligibility**, **item eligibility** and **observed
stock**. A passing chest can hold a weapon that fails the single-resource item
association. A cargo outgoing bay can hold Caesium yet fail the source gate.
[Cases](cases.csv) preserve the latter as a real include/exclude discriminator.
The selected display defaults and known mounted-helmet witness from
[SD1](../containers-displays/saves.md) are controls, not a general empty-display claim.

PackIn is not recursively expanded by this collector. It follows registered
member handles; a root and child cannot be assigned invented inventories from
their assembly name. Duplicate ordinary pointers and shared backing pointers
are suppressed in the source vector. Distinct physical sources with the same
item legitimately add to the resource total. Cross-outpost deduplication is not
performed: the same shared backing can appear in each outpost that exposes it.

Compared with [SD2](../shared-outpost-storage/consumers.md), SD3 shares local
source admission/substitution but omits bench, explicit linked crafting source,
selected ship and player append, component planning and spending. Compared with
[S1](../storage/report.md), [S2](../local-output-links/report.md) and
[E3](../fabricators/native.md), it neither traverses directed production links nor
tests local-link prohibitions or recipe input availability. No inventory is moved.
