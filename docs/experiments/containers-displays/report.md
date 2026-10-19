# SD1: containers, displays and item residence

2026-10-19, Australia/Sydney. SOR-EXP-0055 / SOR-EV-0063.
[Frozen plan](plan.md), [original brief](../../implementation-briefs/CODEX_BRIEF_SOR_SD1_containers_displays_ownership_persistence.md),
[definitions](definitions.csv), [native paths](native.md), [saved joins](saves.md),
[review](review.md). Authored interpretation REVIEW-REQUIRED; primary material LOCAL-ONLY.

| Element | Answer |
|---|---|
| Question | What holds an ordinary constructed container/display's items, admits them, owns them and restores their representation? |
| Best-supported answer | Ordinary chests retain item stacks in the fixture inventory. Native displays additionally convert admitted inventory instances into separate item references and retain per-slot reference lists. Mannequins use actor inventory and equipment through a filtered actor menu. Workshop membership, fixture ownership, item ownership and permitted taking are separate channels. |
| Confidence | Proposed STRONG / STATIC for the mapped ordinary mechanisms; SAVE corroborates specific helmet/backpack relations, modified mannequin equipment rows and populated ordinary storage. No new RUNTIME evidence or visual-restoration measurement. |
| Coverage | Pinned retail 1.16.244.0, main-game recursive recipe variants and selected installed add-on counterparts; broader historical originals searched with explicit format/prefix limits. Full winning-load-order or every cosmetic mesh equivalence is not claimed. |
| Evidence | Native component lookup/slot admission, creation and removal from inventory; independent writer/load/fixup chains; HIST-0021 fixture-slot-item-modification-owner joins. Exact sources and offsets are in the linked records. |
| Limits | No controlled deposit/theft, scrap, equip, movement or rendered-reload trial. Actor tails and some item extras remain partially decoded. Historical world cases are mechanism comparisons, not evidence the player constructed them. |
| Next step | Independent criterion review and maintainer critical diff review. A minimal future acquisition card is in saves.md; no live action follows from this report. |

## Classification and admission

The main-game recipe expansion identifies **41 matching recipes, 97 recipe/leaf
rows and 68 unique leaf definitions**. Nested COBJ entries deliberately repeat
variants reachable through a parent list; 97 is not a count of distinct objects.
The selected leaves include 26 mannequin NPCs, four generic-case pack-ins and a
decorative storage-bin STATIC comparison. Ten actual CONT children in those
pack-ins are separately identified. [definitions.csv](definitions.csv) records
recipe/list chains and physical definition offsets rather than guessing assembly
children from names. Industrial stores/output buffers remain [S1](../storage/report.md).

| Mechanism | Ordinary variants / recognition | Capacity and compatibility | Residence and persistence |
|---|---|---|---|
| Decorative storage CONT | Six small, six large, four safe variants from three recipe lists; TESContainer, without BGSDisplayCase | CarryWeight PRPS 10 for small/table safe, 40 for three larger safes, 150 for six large boxes. Both output-link prohibitions are 1. Effective AV/ordinary menu enforcement differs from generic insertion | Inventory rows/stack extras; omitted change data can inherit defaults. Capacity is weight, not form count |
| Weapon racks | Three CONT bases; BGSDisplayCase plus SNTP, ONAM and DCSD | 12/4/12 configured display rules; per-rule include/exclude lists, node index and item limit. Rifles, pistols and ammunition have distinct slots | Separate displayed references indexed by runtime DisplayCaseComponent; inventory leftovers and displayed objects must both be considered |
| Weapon cases | Pistol/rifle/heavy CONT | 2/3/4 rules respectively; weapon and ammunition rules differ. Several bases have default loot CNTO, explicitly cleared by the ordinary construction-preview path | Same native display mechanism; world loot cases are useful comparisons but not ordinary construction witnesses |
| General cases/shelves | Five direct CONT variants plus four PKIN variants with actual child CONTs | Direct rule counts 9/4/3/6/1; child rules belong to each child, not a fictitious root inventory. A matching item may still fail occupied/exclusion/snap conditions | Native display references, child ownership/assembly state, and inventory remain distinct |
| Helmet case/stand, backpack stands, slate displays, wall mounts | 2 helmet, 3 backpack, 2 slate and 3 wall-mount CONT definitions | Helmet/backpack/wall examples have one configured rule; slate single/multi have 1/5. Filters select compatible forms/keywords rather than arbitrary decoration | Native display references; BOOK/slate quantity reuse has a separate branch |
| Mannequins | 26 NPC variants, MannequinRace and inherited MannequinScript; four top-level variants plus 22 nested recipe variants | Actor CarryWeight path and explicit menu filter; NPC CarryWeight property -85 is a base contribution, not a measured final capacity. Equipped body slots are distinct from inventory capacity | Inventory retains instances; ToggleEquip selects actor equipment. Merely depositing is not proof of equipping |
| Installed wardrobe | SFBGS050.esm local COBJ 083816 -> CONT 083819 | Eleven DCSD rules, including a rule with node -1 and limit 2. Therefore rule count is not automatically a count of visible mounts | BGSDisplayCase; same bounded native machinery, no positive saved wardrobe witness |
| Colony War Action Hero display | SFBGS00D.esm local recipe 074699 selects PKIN and sealed CONT variants | Sealed CONT has 27 native rules and inclusion/exclusion lists; music/effect scripts on decorative counterparts are not evidence for inventory attachment | Native display variant; separate decorative assembly counterpart remains qualified below |
| Shared Outpost Storage | SFBGS00D.esm local COBJ 02af79 -> CONT 02af77 | Construction/classification only: CONT, base CarryWeight 5000, both output-link prohibitions 1, no BGSDisplayCase in the read definition | SD2 owns cross-outpost access/sourcing; none is inferred here |
| Decorative bin / storage furniture | Example co_Outpost_Decor_StorageBinList01 -> STAT 134b87 | No TESContainer or display component in the selected base | Its appearance/name does not establish inventory. Generic physics placement is excluded |

These are installed definition facts, not measured effective values. Add-on
inspection covers all 37 installed non-main ESMs and expands matching Outpost
COBJ products through local/master lists; unresolved cross-master leaves are
retained in addon-census01.json. Four X-Tech extractors are explicitly S1/E1
industrial exclusions. A complete installed override merger, every differently
named workshop recipe and the Action Hero PKIN's full interactive child lifecycle
are not established by this census. Do not describe this as exhaustive installed
content coverage.

The decisive native slot test checks a free per-rule item limit, include and
exclude lists and conflicting occupied slot groups. A pistol may pass the
fixture's broad ONAM category and still have no compatible free display slot.
The wardrobe's node-1 rule requires its own template/presentation join; rule
count alone does not establish visible mounts. Base zero/absent CarryWeight on native displays does
not remove their independent slot gate. Generic forced insertion and ordinary
menu insertion cannot be treated as one policy; [native.md](native.md) records
the ordinary menu's decisive display preflight and the now-resolved bound
filter assignment and consumer.

## Ownership and lifecycle answer

Construction sets a **WorkshopItem relationship**, while explicit fixture
ExtraOwnership uses actor/faction/reference-related identities. The real
HIST-0021 helmet fixture has both channels, with different targets. Its displayed
helmet owns another ExtraOwnership record: NPC Player base 000007, while the
fixture uses player reference 000014 in its reference-owner lane. Neither item
ownership nor stolen status follows from Workshop membership alone.

The native menu distinguishes giving from taking, enforces item/quest/capacity
and display gates, and has explicit taking/crime/ownership-update branches.
The generic transfer callback changes ownership according to the transfer
reason. Ordinary menu mode 0 uses reason 4 and preserves copied ownership in that
callback for both deposit and retrieval; other modes, currency, crime processing
and display creation have separate effects. Display creation positively copies
the selected instance's permitted extras, including ownership and modification
data, then in its new-reference branch overwrites copied ownership when the
fixture has an explicit owner. Reused references follow a separate branch.
No laundering guarantee or measured stolen-to-clean transition is established.

Ordinary construction explicitly clears preview-reference inventory, including
default case stock, and resets dropped/display state. Recognized mannequins
also use the inventory-clear branch. The accepted placement commits that
prepared reference; base CNTO loot does not establish a free construction reward.
Exact predicates and null-destination behavior are in [native.md](native.md).

Construction, menu transfer, scene presentation, equipment, save/load, moving,
scrapping and physical destruction are separate operations. Native display
creation drains the represented quantity from fixture inventory and registers
the resulting item reference; save/load preserves the relation and rebuilds
handles. A real saved empty fixture inventory can coexist with a positive saved
displayed item. [saves.md](saves.md) gives this exact counterexample.

The ordinary Workshop caller positively transfers contents: after its inventory
or display predicate, a first selected recipient can receive capacity-limited
contents, then the player receives remaining transferable contents without that
capacity clamp. Native displays first materialize qualifying mounted references
back into source inventory. Actor and unresolved-handle exceptions remain
conditional in [native.md](native.md); a generic deletion call does not imply
the same behavior. This is a native causal result, not a measured conservation trial.
Moving rebuilds placement/membership; it does not by itself prove a second item
copy. [DA1](../outpost-defense/integrity.md) supplies Health/destruction/repair
infrastructure. The inspected passive chest/display definitions have no DEST
damage component; do not invent a combat-destruction content-loss rule or infer
that repair recreates missing items. Actual transitions remain unobserved.

The scientific result is useful scoped native and saved correspondence, with
the remaining lifecycle/ownership/actor-default questions stated explicitly.
The frozen acceptance matrix and independent disposition in review.md determine
whether this assignment is complete; this summary does not grant integration.
