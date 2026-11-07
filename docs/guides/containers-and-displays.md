# Containers and displays

A decorative chest keeps stacks in its own inventory. A display case can take
an admitted quantity out of its inventory and represent it as a world item
attached to a display slot. A mannequin is an actor. It keeps items in actor
inventory and uses its equipment slots to show selected instances.

[Technical reference](../reference/containers-and-displays.md) ·
[Container and display study](../experiments/containers-displays/report.md) and
[independent review](../experiments/containers-displays/review.md)

## Choose the fixture for the job

| Fixture | Where the item resides | What can prevent admission or presentation |
| --- | --- | --- |
| Decorative chest or safe | Inventory on the placed chest reference | The ordinary transfer menu checks applicable effective weight capacity and item rules. The inspected ordinary decorative chests block local output links in both directions. |
| Native display case, rack or stand | A separately represented item reference in a fixture's display-rule list, with any residual stacks handled through inventory | A broad category match can still fail include/exclude filters, a full slot or incompatible snap-node setup. A display assembly can have several actual child fixtures. |
| Mannequin | Inventory on the placed actor, with equipped instances selected by its actor equipment system | The mannequin's menu filters equipment types. Storing an item and toggling equip are distinct actions. |

The table describes inspected 1.16.244.0 definitions and native paths. A
storage-shaped decorative bin may be scenery. A base case that can start
with loot in the world can be emptied by ordinary construction. Neither look
nor base stock is enough to infer what a placed fixture contains.
[Definition and admission study](../experiments/containers-displays/report.md#classification-and-admission) ·
[Construction stock-clearing path](../experiments/containers-displays/native.md#new-construction-suppresses-default-stock)

Industrial stock and [local output links](storage-and-output-links.md) use
other gates. [Shared Outpost Storage](shared-storage.md) exposes a separate
backing inventory. A fixture's membership in a Workshop identifies where it
was registered. Taking an item depends on item ownership and the transfer's
permission rules, which can differ from both fixture ownership and Workshop
membership.
[Ownership and player action](../experiments/containers-displays/native.md#ownership-and-player-action)

## What can come back after loading

One historical helmet stand has a saved inventory count of zero and a saved
slot entry that points to a specific helmet. The helmet points back to the
fixture and carries instance modifications. An inventory-only read would
miss the display. The supported loader can rebuild that relationship and queue
attachment work. The saved join cannot tell us what the player saw after load
or how the helmet originally got there.
[Helmet witness and counterexample](../experiments/containers-displays/saves.md#positive-native-display-witness)

On a mannequin, the saved item row and equipment bits support a different
restoration path. The actor can rebuild equipment from those rows. The
sampled rows and static paths leave complete actor state and rendered
appearance open.
[Actor equipment and restoration](../experiments/containers-displays/native.md#mannequin-script-equipment-and-restoration)
