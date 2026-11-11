# Storage and local output links

For display-mounted items and mannequin equipment, see
[containers and displays](containers-and-displays.md).

Stock belongs to individual object inventories. A Solid, Liquid, Gas or
Warehouse store can hold several matching item types. A producer can keep its
output in its own small buffer or create it directly in a downstream store.
A local output link gives the engine a direction to look for a destination or
an ingredient source. Whether stock moves depends on the operation and the
references that resolve when it runs.

[Guide index](README.md) · [Technical reference](../reference/storage-and-output-links.md) · [Glossary](../reference/glossary.md#inventory-and-local-links)

## Choose a store for the item and the operation

On the examined ordinary 1.16.244.0 definitions, each dedicated storage family
has base capacities of **75, 150 and 300 weight units** for small, medium and
large. The dedicated stores match solid, liquid, gas or manufactured-resource
item keywords respectively. The Transfer Container has a 200-weight base
and adds a ship-access route. Its local links still use ordinary pair checks.
The installed development script requests local redistribution on certain
player inventory and menu events. That source and the mapped ship-access
path establish separate uses, with no periodic ship transfer demonstrated.

The qualified ordinary cargo templates use separate 300-weight incoming and
outgoing children. Incoming can send locally and blocks incoming local links.
Outgoing can receive compatible local links and can also qualify as a local
sender. A freighter loads and unloads through different paths, described in the
[cargo guide](cargo.md). The examined ordinary decorative chest definitions
enable both native link prohibitions. Their possible use in construction ingredient
counts follows a different gate. [Storage definitions and comparison](../experiments/storage/report.md#runtime-and-persistence-correspondence).

## Follow the directed links

Consider an extractor feeding a small store linked to a larger store. When
the mover redistributes **existing stock**, it walks the forward candidates,
checks item fit and can remove units from the source and insert them straight
into the larger store. The small store need never hold those units. The mover
can split a source row among stores and leave the remainder in place. Its
current vector order controls the choices in that call.

A **new production batch** can instead be created at one eligible downstream
store, or at the producer's own buffer when the fallback qualifies. With
capacity 75, current weight 74.5 and three half-weight units due, the mapped
production branch can choose that store and request all three, for a predicted
weight of 76 on successful insertion. A weight-limited redistribution of
existing stock under those operands would plan one unit there. These are
worked native paths. [Positive and counterexample traces](../experiments/local-output-links/traces.md).

A refill request can search upstream for containers whose stock can move
downstream. A builder can search incoming links for ingredients and withdraw
from the source inventories. Its own output buffer holds its products. See
[fabrication](fabrication.md), [organic production](organic-production.md)
and [power and generator fuel](power.md) for the consumers of those inputs.
[Direction and input withdrawal](../experiments/local-output-links/native.md).

## Away from the outpost and after reload

The ordinary producer update can operate with no visible 3D when the Workshop
and producer resolve, the row is registered and due, and current eligibility
and delivery permit work. An unresolved producer or Workshop takes a different
branch. Skipped time can yield counted iterations or clear pending work
without creating stock. [Lifecycle cases](../experiments/local-output-links/lifecycle.md).

A saved link identifies its source and destination separately from their
saved contents. HIST-0036, for example, has two Europium extractors linked
through a small solid store to a cargo outgoing child, with explicitly empty
serialized lists at those four references. The chain establishes saved
topology and stock at that sample. A transfer event and current loaded stock
would require other evidence. Unsupported stack extras leave stock unknown.
[Saved examples](../experiments/local-output-links/saves.md) · [Original review](../experiments/local-output-links/review.md).

In the controlled save sequence, **L0** is the original linked baseline.
The operator described **L0C** as the linked baseline after reload, **L1**
as the unlink save and **L1C** as its same-session unlinked control. **L2**
and **L2C** are the reported relink save and its same-session linked control.
The selected relationship payload changed from **19 to 12 to 19 bytes**,
holding at the corresponding length in each same-session control.

Corresponding saved windows contain different endpoint tokens across the
reported reload. That comparison also spans elapsed time. The original
literal fails from L0C onward. Substituting the new tokens still fails at
L0C because the entry order differs. A later bounded method associates the
candidate relationship across these windows. The remapping mechanism, full
record semantics and load authority remain open. The exact inspection route
requires the CORE baseline, the five ADDENDUM saves and the qualified reader
with its controls.
[Controlled sequence](../experiments/output-link-validation-L0-L2C.md) ·
[Selected evidence and limits](../first-release-scope.md)
