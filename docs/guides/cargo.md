# Cargo links and fuel

An ordinary paired route uses one ship and one hold. The ship takes stock from
the docked pad's **outgoing** child and tries to unload it into the other pad's
**incoming** child. It can then take stock from that pad's outgoing child for
the opposite leg. Pairing identifies the endpoints. Actual progress depends on
resolving objects, running ship stages and completing native travel.

[Guide index](README.md) · [Technical reference](../reference/cargo.md) · [Glossary](../reference/glossary.md#cargo-and-time)

## Follow the hold

1. The ship arrives and tries to put as much eligible freight as fits into
   the current incoming child. It then requests local redistribution there.
2. When readiness permits, the ship schedules loading. It refreshes the
   current outgoing child from the local graph and loads eligible stock
   subject to hold capacity. The next leg can leave empty or partly full.
3. Departure selects the opposite landing marker. The native travel package
   must finish before the arrival script tries that end's incoming child.

Stock that does not fit on the unload attempt stays aboard. The subsequent
local flush can open space without triggering a second unload in the same
arrival. A fuel retry can try again before departure. If the stock stays
aboard, it can return into the original endpoint's **incoming** bay. Exports
newly loaded at the far end share the hold with those retained items. A
static stack in the origin's incoming bay cannot identify its journey.
[Cycle and worked return](../experiments/cargo-links/transport/cycle.md) · [Native inventory path](../experiments/cargo-links/transport/inventory.md).

## Fuel and elapsed time

Ordinary in-system configuration skips the fuel readiness test. The examined
inter-system configuration looks for either eligible non-mission pad at arrival
or retry. Arrival attempts unloading first. When neither end passes readiness,
the ship schedules another unload and check at the same dock. Once loading
is admitted, the ordinary load and takeoff handlers proceed without another
fuel poll in that leg. [Stage cases](../experiments/cargo-links/fuel/stages.md).

These two paths use different triggers.

~~~text
Fuel marker due cycle -> recipe and input gates -> He-3 withdrawal
Ship arrival or retry -> either-pad readiness -> schedule loading
~~~

The fuel marker requests He-3 through [incoming local links](storage-and-output-links.md).
The pinned recipe withdraws **five He-3 per accepted fuel-production cycle**
with a base interval of **108 engine scheduler seconds** before modifiers. The
marker is a logical recipe consumer. An uncharged eligible pad can pass
readiness before withdrawal if its recipe is accessible. An already charged
pad can pass without checking those five units again at that poll. Fuel
consumption follows native producer work independently of the ship's departure
and return stages. [Recipe and charge chain](../experiments/cargo-links/fuel/native.md).

Constellation's Guide has a candidate **0.95 interval multiplier**. If it
applies to an eligible periodic fuel-production cycle, the interval becomes
**102.6 engine scheduler seconds**. This can increase He-3 consumption per
elapsed scheduler time. Actual delivery throughput and transit time are
separate measurements. The historical saved interval is compatible with
the multiplier, with its actual source and rank unresolved. The study
demonstrated no delivery-rate or transit-time effect of the magazine.
[Modifier candidates](../experiments/cargo-links/fuel/native.md) ·
[Saved interval](../experiments/cargo-links/fuel/saves.md)

The ordinary shipped stage defaults are 30 seconds before loading, 15 before
departure and 30 before fuel retry, converted to **game-time deadlines**.
Dispatch depends on service by the **Papyrus virtual machine (VM)**. Queueing
a due timer and running its script handler are separate steps. The native
movement leg has a separate path to completion. Explicit wait/sleep can
advance the producer's elapsed clock while freight timer delivery is
suppressed. A due callback after the wait can arm a new
stage from the current clock. Calendar passage alone cannot count completed
voyages. The native detached and full flight paths have different timing
inputs even though both ordinary ship bases use the same package pair.
[Timing](../experiments/cargo-links/transport/timing.md) · [Reviewed timing follow-up](../experiments/cargo-links/transport/transit-review.md).

## Distance, interruption and recovery

On the mapped 1.16.244.0 script and native paths, a graphically unloaded ship
can progress while its bindings and references resolve and its package work
completes. A lost binding, disabled ship or unresolved endpoint has different
failure paths. Retargeting clears the old route first. The successful old-hold
recovery route sends what fits to the home ship and the remainder to the
player, with no stock route back to the old outgoing bay in that recovery.
Saved bays, hold contents and selected target can establish those fields at
one epoch. They cannot establish prior receipts or current VM/AI progress.
[Lifecycle and save restoration](../experiments/cargo-links/transport/lifecycle.md) · [Original transport review](../experiments/cargo-links/transport/review.md).

The original mature Save52 comparison reported agreement with a private
manually maintained network. That comparison and the historical Papyrus
context are attributed research history. They supply no replayable voyage
or measured flight clock. The selected Save52 original-byte checks cover
saved relationships and inventories and still require the exact CORE
member, exact Cargo C3 supplement and qualified offline reader.
[Reader inputs](../reference/evidence-access.md#selected-original-witnesses)
[Mature network comparison](../experiments/mature-save-outpost-validation.md) ·
[Selected evidence and limits](../first-release-scope.md)
