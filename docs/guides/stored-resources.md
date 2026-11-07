# Locations Stored Resources

The Locations panel reports resource units from eligible inventories belonging
to each registered, resolvable outpost. It collects arrays for the outpost
rows and displays the selected row. Physical stock stays on the contributing
references, including the player-held backing inventory when an eligible
Shared Outpost Storage fixture exposes it.

[Guide index](README.md) · [Technical reference](../reference/stored-resources.md) · [Glossary](../reference/glossary.md#ingredient-providers-and-reporting)

## From Workshop member to displayed resource

In the mapped retail 1.16.244.0 path, the collector resolves the registered
Workshop, follows its member relationships and checks container capability
and effective `OutpostBuildContainer`. Recognized shared fixtures substitute
the same backing inventory, counted once per outpost enumeration. An ordinary
chest or producer output buffer can qualify. An outgoing cargo child can hold
stock yet fail the effective build-container gate. The collector does not
independently add player pockets, ship cargo or other outposts' ordinary
inventories. [Provider](../experiments/stored-resources/provider.md) · [Membership](../experiments/stored-resources/membership.md).

The item visitor maps qualified physical items to their associated resource
definitions, then sums **stack units** per resource FormID. It orders the
result by resource name and supplies icon metadata for the panel. For example,
the named HIST-0036 beacon has 375 Caesium units in an incoming bay, 94 in a
liquid store and 12 in an extractor buffer. All three are MISC `0x0057DF`
associated with IRES `0x0057E0`. Assuming the named member references resolve
and pass their effective gates, those listed contributions sum to 481 units.
Another 375 in an outgoing bay would be excluded at effective zero. The
tracked example is a partial saved projection, with no screenshot pairing.
[Source rows](../experiments/stored-resources/saves.md#positive-mature-mixed-source-witness) · [Item aggregation](../experiments/stored-resources/aggregation.md).

## Read the count at its collection epoch

Entering Locations collects from inventories and queues data for the UI.
Selecting another row repaints from the delivered arrays on the mapped path.
Stock can change between collection, delivery and repaint. Counts from two
screens at different times cannot establish conservation or an immediate
update subscription. The panel arrays are transient. Saves carry item and
membership state in their own channels rather than a separately persisted
universal outpost inventory. Unsupported saved stack data remains unknown.

The totals express units, independent of weight or production rate.
[Shared storage and ingredient providers](shared-storage.md) can have
additional sources and spend from them. The Locations total alone cannot
establish whether a crafting recipe can spend the same units.
[Refresh boundaries](../experiments/stored-resources/aggregation.md#three-separate-freshness-boundaries) · [Independent review](../experiments/stored-resources/review.md).
