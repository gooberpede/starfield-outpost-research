# Shared Outpost Storage

The Shared Outpost Storage add-on fixture gives access to one inventory held
by a player-side object. Two recognized fixtures can open the same stock.
The local fixture still has its own placed reference and Workshop membership.
That membership can let a bench or construction provider reach the backing
inventory through the local outpost.

[Guide index](README.md) · [Technical reference](../reference/shared-storage.md) · [Glossary](../reference/glossary.md#ingredient-providers-and-reporting)

## Build and access the fixture

The examined `SFBGS00D.esm` recipe on retail 1.16.244.0 requires rank 4 in both
Outpost Management and Outpost Engineering, passes a location/parent keyword
exclusion and has a quota of one at the selected Workshop. The ordinary
construction and placement gates still apply. The installed definition carries
a stash keyword recognized by native code. Opening that fixture substitutes
the player-held inventory for the target. Moving to another qualifying fixture
can therefore give access to the same items without a freight trip.
[Construction](../experiments/shared-outpost-storage/prerequisites.md) · [Recognition and ownership](../experiments/shared-outpost-storage/shared-inventory.md).

## Count and spend from qualified sources

Crafting and research can consider the bench, its explicit linked source,
selected ship, eligible Workshop members and player. Construction uses its
own selected-ship, Workshop and player sequence. A member must resolve and
pass container capability and effective `OutpostBuildContainer` gates in
these walkers. A recognized eligible fixture inserts the backing reference
once per enumeration. A remote fixture by itself does not add that stock to
every bench.

A temporary copy supports counting for bench work. Spending uses the actual
sources in forward order and can request part of the requirement from each.
The order among Workshop members is unqualified and the copy and individual
removals have no demonstrated global transaction. For example, a local cargo
outgoing child may hold freight but fail the ingredient gate when its
effective build-container value is zero. A qualifying ordinary chest can
supply ingredients despite both local-link prohibitions.
[Source order and spending](../experiments/shared-outpost-storage/consumers.md).

[Fabricators](fabrication.md) and [cargo freight](cargo.md) follow their own
input and transfer paths. [Locations Stored Resources](stored-resources.md)
uses similar member eligibility to report per-outpost unit counts. It has a
different output and does not perform ingredient spending.

## What was saved

Historical saves identify fixture references and their beacon owners. The
native player writer saves the backing inventory separately from the fixture.
The historical analysis did not parse exact saved backing quantities, so
fixture records cannot be added up to recover them. Current source resolution,
post-load contents and actual craft debits remain separate questions.
[Saved joins](../experiments/shared-outpost-storage/saves.md) · [Independent review](../experiments/shared-outpost-storage/review.md).
