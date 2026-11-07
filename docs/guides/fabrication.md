# Fabrication

An ordinary fabricator is built with a preset product and can switch to
other supported recipes in its family. In the mapped Starfield 1.16.244.0
main-file catalogue the ordinary families offer 11 simple, 10 compound
and nine multiplex products. Each family has distinct construction-linked
producer bases for its presets. Its supported catalogue and current recipe
tell you what it could make. Power, ingredients, the clock and output
acceptance determine whether items appear.
[Fabricator report](../experiments/fabricators/report.md) ·
[Independent review](../experiments/fabricators/review.md#independent-review01-and-final-package).

## Choose a construction preset or change the product

The construction recipe chooses an assembly containing a producer whose
definition supplies a positive resource value for the starting product.
The same base also carries the resource properties for the other supported
recipes in its family, typically with value zero. The recipe menu uses the
presence of a supported property to admit a choice. A positive value gives
the current selection. Construction research can govern which facility
you can build. The ordinary generic recipe menu emits its admitted choices
as known without testing current stocks or reapplying the mapped construction
gates. The original catalogue includes an exceptional multiplex-labelled
Comm Relay definition outside the ordinary construction set. Comm Relay
is an ordinary simple choice. [Catalogue and exceptions](../experiments/fabricators/definitions.md#population-and-construction-relationships) ·
[Selection evidence](../experiments/fabricators/native.md#catalogue-and-current-configuration).

Changing a recipe successfully removes the old resource registration
and starts a new row with zero timer fields. The old countdown is lost on
that path. An input source that no longer matches can lose its link.
Outgoing checks consider the facility's candidate catalogue and can remove
the first incompatible outgoing membership on one invocation. A zeroed
timer or a visible selection gives no assurance of immediate output.
[Reconfiguration and link checks](../experiments/fabricators/native.md#choice-application-timer-replacement-and-persistence).

## Follow ingredients to their local sources

A fabricator can count and request ingredient removal from suppliers reached
through incoming local links, including paths through a storage buffer. A
path back to a producer can establish how stock might reach the input check.
It cannot tell you the quantity there now or where existing buffer contents
came from. A cargo incoming container is a local stock boundary for this
walk. See [local output links](storage-and-output-links.md) and
[cargo](cargo.md) for how stock reaches the bay.

At a due check the engine can reduce the batch to what every ingredient
supports. For a recipe that needs two units of an ingredient per cycle, five
usable units cap that ingredient's contribution to two cycles. Another
required ingredient can lower it further. The engine requests source removals
and then attempts output insertion. It can create the output at a selected
connected store, so checking the fabricator alone can miss it. This is a
conditional native mechanism. The saved graph and recipe table cannot tell
how much actually arrived. [Stock cap and insertion](../experiments/fabricators/native.md#operating-eligibility-and-actual-request).

## What survives a save

The engine can save a changed selected resource value separately from
the resource-keyed row and transfer links. In the detailed mature sample,
17 producer rows agree with their definition presets, with no explicit
selected-resource override in their saved AV data. A saved path can
identify the producer and structural suppliers. Resolution and current
evaluation determine which references and stocks take part after load.
Current actors, power, effective ingredients and output delivery were
outside those observations.
[Saved examples](../experiments/fabricators/saves.md).

[Technical reference and tracked catalogue check](../reference/fabrication.md) ·
[Glossary](../reference/glossary.md#availability-and-production) ·
[Evidence and access](../audits/production-guides-d5ba/claims.md).
