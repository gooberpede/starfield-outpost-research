# Ingredient visibility, eligibility and spending

Reader notation: [vtable versus object offsets](../../reference/notation.md#native-prose-at-first-use);
[experiment-local export namespaces and lookup](../../reference/native-export-ids.md).
These guide the existing local address/offset declarations; they do not make
export labels global symbols or raw exports available in a checkout.

[Answer](report.md), [shared model](shared-inventory.md), [prerequisites](prerequisites.md),
[methods](methods.md). All priorities below are **STATIC**, not observed craft
results. Source registration is not proof that a particular ingredient is present.

## Entry points and actual source lists

Crafting event ancestry reaches ordinary job `1417f8f70 -> 1417f9a20 ->
1417faca0` (n025/n027). Menu refresh callbacks `141445660/1414462c0/141446bb0`
(n011/n012) call `1417f6fa0`, providing the actual bench at menu object + `0x2E8`, temporary
combined inventory at menu object + `0x2F0` and source vector at menu object + `0x2F8`. This is an ingredient
provider, not the player's ordinary inventory-screen list.

Research's AddMaterial consumer is `14160fba0` (n027): immediate or queued
`141613410` reaches **`1415026c0`** (n004). It redoes `1417f6fa0` using its
bench+848, combined inventory+850 and source vector+858 before planning and
spending. Research and ordinary crafting therefore share a real provider.

`1417f6fa0 -> 1417fd940` (n007/n009) creates a temporary reference, clears its
old inventory, deduplicates the source vector and copies inventory rows into a
combined counting list. The underlying source inventories remain separate.
The **forward source order** is:

1. Actual bench reference, when supplied.
2. Its explicitly linked crafting-container reference via `145ea9f88`, when
   available. This is an actual linked-reference lookup, not proximity scanning.
3. Selected ship source from `1417f6e20`.
4. Eligible members of the bench's Workshop, or of the linked reference's
   Workshop when the bench has no such owner.
5. Player, unless already present.

Workshop ownership is queried with `WorkshopItem` (`145f0b3d8`), then reverse
Extra4D member edges are walked. Callback **`1417fe930`** requires resolved
TESContainer capability and effective **OutpostBuildContainer != 0**. The exact
default binding is `140156f40` (n026) -> OutpostBuildContainerAV_DO at
`145f0a930`, resolved +48 `145f0a978`; freshly reread DFOB `00f659` -> AVIF
`00f65a` in controls02.json. The AV's installed description explicitly concerns
crafting/building. Names and link permissions do not select ingredient sources.
The callback substitutes player+1008 for a recognized shared fixture and
deduplicates it. No traversal of every remote outpost occurs here.

Ship selection `1417f6e20` (n010) first obtains the bench's ship context with
`142116840`; it retains a qualifying registered ship through `14130c710`,
otherwise falls back to the player's ship registry via `141a6bd50`. Those
helpers and the registry lookup `14130feb0` are read in n024/n025. Membership
in the selected registry and successful resolution matter. No distance/radius,
same-planet or same-system test occurs in this mapped selector. The returned
ship source uses its inventory interface; the captain's locker and other placed
ship containers are **not separately enumerated**. Their presence on the ship
does not turn them into cargo. Complete ship activation/registry lifecycle is
outside this scope; no universal current cargo access is inferred from a save.

Construction availability **`1421a7060`** and spending **`1421a7950`**
(n008/n018) build a separate vector: selected ship, eligible members of the
specified Workshop via **`141368bf0 -> 141368cf0`**, then player. The callback
applies the same TESContainer/effective-AV/shared substitution as the crafting
callback. Thus construction and crafting share specific eligibility helpers
and the backing inventory, while using **different enumerators and order**.
Accepted placement `1421de3f0` invokes `1421a7950` (n027), not a speculative
nearby-container mechanism. Construction costs are formed by `140f3a500`
(n017) from recipe ingredients with entry-point AE modification and its
nonzero-minimum handling; displayed base FVPA quantities need not be final costs.

## Source–consumer matrix

Each triple is **visible in ingredient amount / eligible for requirement /
spent from**. `C` means conditional yes through the exact source predicates
above, matching ingredient/plan and sufficient stock; `N` means excluded by
this ordinary enumeration; `U` means unresolved. These are static capabilities,
not historical operations. General item-screen visibility is a different column.

| Inventory source | Own ordinary container/item screen | Workbench V/E/S | Research V/E/S | Outpost construction V/E/S | Decisive condition / contrast |
|---|---|---|---|---|---|
| Player | Yes | C/C/C | C/C/C | C/C/C | Appended once, generally last source |
| Selected ship cargo | Separate cargo access | C/C/C | C/C/C | C/C/C | Registered selected ship; resolve source; no radius in inspected selector |
| Captain's locker / other ship chest | When directly accessed | N/N/N | N/N/N | N/N/N | No independent generic ship-chest scan; exceptional explicit linkage U |
| Companion / crew inventory | Through its own access | N/N/N | N/N/N | N/N/N | No roster enumeration; exceptional explicit source configuration U |
| Local ordinary constructed chest | Yes | C/C/C | C/C/C | C/C/C | Workshop member, CONT capability, effective AV nonzero; fresh chest `2779fc` has base AV 1 |
| Local dedicated industrial store | Yes | C/C/C | C/C/C | C/C/C | Same source gate; `23aed9` base AV 1; local output links unnecessary for this provider |
| Local Transfer Container | Yes | C/C/C | C/C/C | C/C/C | `2ce194` base AV 1; its ship-access special keyword is a separate S1 path |
| Local cargo incoming compartment | Yes | C/C/C | C/C/C | C/C/C | Ordinary/InterSystem incoming bases have AV 1 |
| Local cargo outgoing compartment | Yes, physical stock can exist | N/N/N under zero effective AV; overrides U | Same | Same | Selected outgoing bases omit that PRPS; eligibility requires the actual effective AV, not cargo's local-link capability |
| Local Shared Outpost Storage | Shows shared backing inventory | C/C/C | C/C/C | C/C/C | Eligible local fixture inserts backing once; does not spend its own physical inventory |
| Remote shared fixture, no eligible local fixture/source | Direct access there shows same backing | N/N/N as independent remote source | Same | Same | No remote-fixture census; a local qualifying fixture can expose the same global stock |
| Remote ordinary store / cargo bay | Its own inventory persists | N/N/N as independent remote source | Same | Same | Not a member of selected local Workshop; explicit linked-reference exceptions remain conditional |

Outgoing versus incoming cargo is a concrete false-positive contrast. [S1](../storage/report.md)
establishes both physical stock and local-link capability; controls02 freshly
rereads all six cargo bases. Incoming bases `219173/100b62/2a6c3b` supply base
AV 1, outgoing `219171/100b63/2a6c3a` omit it. Omission is **not** a measured
zero effective override. With effective zero, the mapped ingredient callbacks
exclude outgoing stock despite its availability to direct menu/freight/link
consumers. The ordinary chest contrast goes the other way: its local-link
prohibitions do not exclude it from this ingredient provider when its effective
build-container AV is 1. These are separate policies.

## Counts, ingredient plans and actual depletion

The combined inventory is a **copy for counting**, not the authoritative item
store. `140b631b0` and `140643360` (n007) copy/sum source rows. Required
ingredient matching/planning uses `140a03670`, per-source `140a03550`, and
`140a02e80` (n013/n025/n028). The latter also examines
**BGSCraftingResourceOwner** component data for decomposable requirements;
an ingredient count need not simply be a raw matching-form count. This scoped
component branch is not a general catalogue of every recipe or salvage rule.

`1417f6690` (n028) checks requirements against the combined list, builds and
revalidates a plan. The ordinary craft consumer `1417faca0` (n018) then uses
`1417f7670` for unmet component/substitution handling and **`1417fb210`** for
planned items. The former computes residual requirements (`1417f7780`, n009)
and can return missing component material to the supplied player/source context;
it is not itself the source-priority algorithm. The latter iterates the actual
source vector **forward**, queries available amount via `140b63d40`, takes
`min(remaining, available)`, prepares per-source removals and calls virtual+458,
then subtracts that amount and continues until fulfilled or sources exhausted.
Partial fulfilment can span multiple sources and partial stacks through the
ordinary inventory-removal machinery reused from SD1/S1.

Consequently bench/explicit link/selected ship precede Workshop members and
player for ordinary crafting; research uses the same forward walker. Construction
spending uses its own ship/members/player vector and corresponding forward
`min`/virtual+458 loop (n018:1421a7950). **No stable order between Workshop
members** is inferred from saved relationship order or container build order.
Deduplication prevents the same reference being charged twice merely because it
was reached through two source roles. No controlled craft establishes an observed
priority or conservation result.

Research `1415026c0` plans/removes materials, updates the Research manager via
`141800f20`, emits completion feedback on the relevant result, refreshes source
data with `1414ff8e0`, and refreshes project/material data (`1415005d0/141500a80`).
Crafting has preparation/refresh callbacks and job completion (`1417f8db0`).
Individual source inventory operations take locks, but the combined-copy,
planning and sequential multi-source mutation are not shown to be one atomic
transaction. The walker decrements its remaining amount by the prepared request;
it does not prove that every asynchronous lower mutation completed exactly as
counted, nor roll back every earlier source on later failure. UI visibility and
prepared eligibility therefore do not guarantee a realized inventory delta.
No concurrency failure was observed; this is the precise static consistency limit.

## Other consumers

| Consumer | Sources and mutation | Shared provider relation |
|---|---|---|
| Ordinary ContainerMenu | One selected target; special recognized target substitutes player+1008; give/take/weight/instance rules remain SD1 | Not the combined ingredient list; ordinary chests do not aggregate one another |
| Outpost repair | DA1 `1421e3f50 -> 1421e9b50 -> 140f36310`; restores existing-reference Health/destruction state | **No material count/spending in the mapped ordinary repair route**; V not applicable, E/S N for all ingredient sources |
| Industrial fabricator | E3/P1 `140f7f6f0` uses transitive directed incoming reference inventories and actual source removals | Does not use the bench/Workshop ingredient enumerators or automatically add player/ship/shared stocks |
| Cargo freight | C2 native hold/incoming/outgoing reference transfers | Actual transport among separate inventories; not shared-backing synchronization |
| S2 redistribution | Directed downstream compatible inventories | Different pair/filter/capacity path; Shared definition's incoming/outgoing prohibitions are 1 |

Reuse [SD1](../containers-displays/native.md), [DA1 repair](../outpost-defense/integrity.md),
[E3](../fabricators/native.md), [C2](../cargo-links/transport/transit.md) and
[S2](../local-output-links/native.md), with their original coverage limits.
SD3's Locations **Stored Resources** screen was not traced or inferred from
these providers. Exact current UI totals and actual post-load/craft deltas remain
NOT TESTED.
