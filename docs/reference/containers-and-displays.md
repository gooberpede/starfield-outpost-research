# Containers and displays technical reference

[Reader guide](../guides/containers-and-displays.md) ·
[Selected claims](../history/claims.md#containers-and-displays) ·
[Sources and build](../experiments/containers-displays/methods.md) ·
[Independent review and corrections](../experiments/containers-displays/review.md)

This reference uses installed 1.16.244.0 definitions and native paths, plus
selected supported historical saves. Preferred static VAs use base
`0x140000000`. Base FormIDs, resolved save-local IDs, save storage words
and runtime handles are separate. The save report's decimal positions
locate the decoded logical stream.

## Identify the actual fixture

The main-game census found 41 matching recipes, 97 recipe/leaf rows and 68
unique leaf definitions. Nested lists can reach the same leaf through
different recipe routes. The selected leaves include 26 mannequin NPCs, four
generic case pack-ins and a decorative STAT comparison. Ten CONT children of
the case pack-ins are separately identified. A pack-in root need not own
the child's inventory or display rules. Selected installed add-ons are
qualified by file and definition. World, test or mission comparisons and
name-based census exclusions do not expand ordinary construction coverage.
[Classification and exclusions](../experiments/containers-displays/report.md#classification-and-admission) ·
[Definition rows](../experiments/containers-displays/definitions.csv)

The ordinary decorative CONT variants have CarryWeight contributions of
10, 40 or 150 by definition and both ordinary directional link prohibitions
set to 1. The transfer menu reads effective capacity where the weight clamp
applies. It has item and quest gates. Generic insertion can follow another
path. Actor CarryWeight and perk adjustment govern applicable mannequin
capacity, so the mannequin's −85 base contribution cannot supply a final
capacity. Ordinary preview explicitly empties qualifying case and mannequin
stock, even if the base supplies defaults.
[Admission](../experiments/containers-displays/native.md#recognition-definitions-and-ordinary-admission) ·
[Preview and defaults](../experiments/containers-displays/native.md#new-construction-suppresses-default-stock) ·
[Industrial storage](storage-and-output-links.md) · [Shared storage](shared-storage.md)

## Runtime residence and ownership

| Channel | Owner and writer | Reader and limits |
| --- | --- | --- |
| Ordinary item stack | Fixture inventory, populated through transfer/insertion. Form, quantity and selected stack extras travel through row operations. | Ordinary inventory consumers see these stacks. Base and effective fit are distinct. An absent change may allow a default, while a serialized empty inventory can override default stock. |
| Display item and slot | BGSDisplayCase on reference/base supplies DCSD rules. Menu preflight tests admissible rules. Insertion can create or reuse a reference, register it in the fixture's runtime DisplayCaseComponent and remove the represented quantity from inventory. | Rule index differs from snap-node index. Include/exclude lists, group conflicts, per-rule limits and actual snap-node validity matter. BOOK reuse can combine quantities. Slot removal `0x141304f40` has a separate path. |
| Mannequin equipment | Recognized mannequin actor owns inventory rows. ToggleEquip resolves the selected instance and calls the actor equip path. | Actor equipment manager and scene update use slots and instance identity, outside native display rule lists. |
| Membership and permissions | Fixture Extra4C WorkshopItem, explicit Extra1F fixture ownership, separate item ownership and item-to-fixture backlink are distinct. | Ownership and crime branches inspect the actual transfer context. New displayed references copy permitted extras and can inherit explicit fixture ownership. Reuse follows another branch. No measured theft or ownership-cleaning transition. |

[Runtime slot selection and creation](../experiments/containers-displays/native.md#inventory-instance-to-displayed-reference) ·
[Ownership branches](../experiments/containers-displays/native.md#ownership-and-player-action) ·
[Equipment consumer](../experiments/containers-displays/native.md#mannequin-script-equipment-and-restoration)

## Serialized joins and fixup

Inventory writer/reader `0x1406447c0`/`0x1406448b0` use rows, quantities and
stack extras. Native display components have their own type 6 channel.
The loaded writer reaches `0x1412fd300`, writing a byte flag, a 16-bit group
count and per-group 16-bit counts with saved item identities. The loader
`0x1412fe810` reaches `0x1412fd450`. Subsequent owner and item resolution
rebuilds handles through `0x1412fd650` and queues attachment work. Inventory
reconciliation and scene construction have separate conditions. Qualified
mannequin inventory rows carry equipment bits read by the actor's equipment
rebuild. HIST-0256 and HIST-0257 each preserve three modified equipped rows
with row state 1, the low equipment bit. This supersedes the initial no-positive
search result for mannequins. Unsupported extras and actor tails remain unknown.
[Save writer, loader and fixup](../experiments/containers-displays/native.md#saveload-and-lifecycle) ·
[Equipment restoration](../experiments/containers-displays/native.md#mannequin-script-equipment-and-restoration) ·
[Saved equipment rows](../experiments/containers-displays/saves.md#corpus-search-controls-and-limits)

HIST-0021 fixture `0xff05bb90` at decoded offset `0x596fa4` has a zero
inventory count. Its component row at `0x181b0d` points to helmet reference
`0xff05bb92` at `0x59705c`. The item carries modification extras and an
explicit backlink. Fixture player-reference owner `0x00000014`, helmet
NPC owner `0x00000007`, and fixture Workshop target `0xff029ca0` are three
different joins. Neither rendered reload nor a live deposit can be inferred
from those bytes. The ordinary scrap caller can first materialize qualifying
displayed items back into inventory for transfer, with unresolved handles
and actor predicates limiting that path. Generic deletion gives no equivalent
transfer guarantee.
[Saved fixture and item](../experiments/containers-displays/saves.md#positive-native-display-witness) ·
[Scrap and reconstruction](../experiments/containers-displays/native.md#saveload-and-lifecycle)

**PUBLICATION DEPENDENCY — EVIDENCE ACCESS PENDING.** The definition census
and tracked witness description support bounded checks. The protected save
and original native/compiled traces remain separate dependencies.
