# C2 cargo transport and returned freight

2026-10-18, Australia/Sydney. SOR-EXP-0045 / SOR-EV-0053.
Subsequent authorized [native transit investigation](transit.md) maps movement
selection, elapsed callers, full-flight modifiers and conditional round-trip
arithmetic. Its [separate review](transit-review.md) does not rewrite the earlier
C2 acceptance or claim a measured universal trip duration.
[Authority/amendment](contract.md), [state machine](cycle.md),
[timing/modifiers](timing.md), [inventory](inventory.md),
[remote/recovery](lifecycle.md), [saved correspondence](saves.md),
[review and criteria](review.md), [native locators](functions.csv), [pins](sources.csv).

| Mechanism | What actually happens | Necessary conditions and inputs | Saved / transient | Evidence and consequential unknown |
|---|---|---|---|---|
| Ordinary round trip | One ship alternates between two linked landing markers. Each arrival unloads the shared hold into that endpoint's incoming bay; later loading takes that endpoint's outgoing bay | Valid linked references; successful ship creation and travel-package completion. No minimum cargo threshold in the timer/departure code | Endpoint/ship links, hold and destination AV persist; current callbacks and graphics differ | Shipped quest/ship/package PEX; C1 principal pair and wider Save52 ships. Historical movement is not observed |
| Undelivered freight | **Yes: rejected freight stays in the shared hold and can unload into the original pad's incoming bay on return** | Destination cannot accept all items; ship completes its opposite leg; original incoming has room when unloading runs | Remaining items are real ship inventory, with no per-origin manifest used by this ordinary path | Capacity-respecting native removal, same hold on both legs, PEX receiving-key selection. This supports the mechanism; it does not establish the user's particular incident |
| Partial/full/empty shipment | Load tries available eligible items up to effective ship capacity; a partial or empty ship still arms departure | Outbox stock and allowed native item forms, stack counts, mass, capacity and current hold; ordinary path excludes mission-specific selection | Physical stacks persist; each call's transfer plan is transient | No fullness/minimum-load comparison in shipped timer branch. [Mixed-item and capacity rules](inventory.md) |
| Dock scheduling | Arrival arms load timer; load arms takeoff timer; fuel failure instead arms a retry which unloads/rechecks again | Script defaults 30/15/30 seconds converted once with ground calendar setting; native integer deadline conversion and VM dispatch gates | Script interval fields and native remaining timers are separate persisted channels | **Game-time deadlines, not extractor elapsed production.** [Exact units/examples](timing.md); VM and travel latency remain additional inputs |
| Inter-system difference | Same scripts, two-end hold and package pair; fueled marker chooses another ship base and sets RequiresFuel. Either eligible non-mission pad can pass the fuel readiness gate | Current CanProduceForWorkshop result, halt/power/resource state as applicable; rechecked at arrival/retry, not continuously during every flight | RequiresFuel, endpoint configuration and inventories differ from transient readiness | Shipped bytecode and installed VMAD; stocked Schrod II/Feynman V inter-system example. Detailed He-3 consumption/replenishment remains C3 |
| Wait/sleep and time jumps | Calendar can advance past an existing deadline, but VM suppresses game-time timer dispatch while its wait/sleep field is active. Afterwards it emits due one-shot events; a handler rearms from **current** time | Calendar days-passed, current timer heap, wait flag, bound script and VM execution | Remaining time serialized; no ordinary script loop enumerates missed voyages | Native timer producer/consumer and wait field. Sleeping is not a bulk freight simulation equivalent to E1 production catch-up |
| Distant/unloaded operation | Script inventory/timer work has no 3D/player-distance test. Travel uses native package/pathing completion, with different process-state branches; unresolved references and missing completion are separate stalls | Bound/resolvable objects and admitted AI/package work; no guarantee that every unloaded reference meets these conditions | Saved links/hold/direction and reconstructed handles/AI work are distinct | [Reachable native paths and boundaries](lifecycle.md). Historical residency and an exact route's flight duration require additional operands |
| Unlink/retarget/removal | Old hold is transferred to the player's home ship respecting capacity, then remainder to player without that limit; links/timers are cleared and old ship disabled | Old ship must resolve; home ship is optional; endpoint removal calls quest cleanup | Cargo recovery changes real inventories; no origin-bay return is used by cleanup | Shipped ClearCargoLink. An already unresolvable/destroyed ship is not covered by successful recovery |

**Best-supported result:** the ordinary returned-freight explanation is
**STRONG / STATIC**, corroborated by saved shared-hold/endpoint relationships.
It predicts origin **incoming**, not origin outgoing. A deliberately stocked
opposite outgoing bay can produce the same incoming item, so a snapshot alone
cannot discriminate provenance. C1's empty panels are preserved: the principal
Save52 pair has empty bays/hold and immediate Warehouses; those facts do not
contradict operation or establish a returned shipment.

Coverage is installed retail **1.16.244.0**, main ESM, five shipped PEX members,
their installed development source and protected Save52. The wider reread frames
205,557 R3 records, qualifies 61 marker bases from 75 queue candidates and selects
24 cargo ships; unsupported ship extras remain explicit gaps. Stocked ordinary
and inter-system examples supply positive evidence beyond the empty principal
case. These are observed saved states plus native-derived transitions, not a
recorded voyage or a winning mod-load-order reconstruction.

Exact byte/framing/hash comparisons are PROVEN within their bounds. Authored
semantic conclusions are proposed working knowledge pending maintainer critical
review. Independent task disposition is in review.md. No live experiment, safe
hook, integration, C3 execution or publication is implied. Raw native/script/save
material is LOCAL-ONLY; authored interpretation is REVIEW-REQUIRED.

Read [the complete example](cycle.md#worked-partially-blocked-round-trip) for a
count-conserving outward and return journey, and [timing.md](timing.md) for the
two contrasting clock examples. Neither is presented as historical Save52 play.
