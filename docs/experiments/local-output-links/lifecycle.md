# Remote outpost lifecycle and production/transfer coupling

[Report](report.md), [native conventions](native.md), [clocks baseline](../inorganic-extractors/arithmetic-clocks.md).
Proposed STRONG / STATIC mechanism; actual state transitions RUNTIME NOT TESTED.
Distance, graphic residency, live reference resolution and registration are
separate predicates. No historical save is silently assigned a current load state.

## Positive lifecycle chain

Fresh n08-n10 establish typed event ancestry rather than guessing from a Boolean:
`140b9a340 -> 1459780d0 -> vtable144b980a0` is
`BSTEventSource<TESObjectLoadedEvent>`. Initializer `1421ad290` subscribes
`145916510`; its vtable144c25de8 has callback+8 = `140f7dfa0` (n05/n06).
Cleanup `1421ad550` unregisters it. Separate `140b994d0 -> 145977ba8 ->
vtable144b98240` is TESContainerChangedEvent, subscribed at145916518 with
callback `140f7e530`. These identities are grounded by symbols and pointer data,
not just event-shaped argument guesses.

`140f7dfa0` resolves the event's FormID via `1405de3b0`, its reference/owner via
virtual+230/Extra4C Workshop key, and ExtraWorkshop with `140f51350`. The current
reason is evaluated in mode0. On false object-loaded state, matching rows have
pending+08 cleared and cached eligibility updated. They are **not removed** from
the resource arrays or registered Workshop set. On true state, `140f8c580`
matches current producer handle, stores eligibility, conditionally passes pending
to `140f7d6a0` and clears pending unconditionally (`140f8c68a..6b8`, n10/n12).
If no matching row exists, selected positive resources receive new zero-pending,
zero-timer rows. This is registration/reactivation, not restoration of a universal
last-visited timestamp or unlimited production debt.

Construction registration `1421dd600 -> 140f7c510` and selection registration
`141583410 -> 140f83b90` call `140f7ee40` to insert the Workshop handle and
create/update resource rows. Both are fresh native exports. Removal
`1421de660 -> 140f836e0` is positively identified as **UI deletion**, not unload;
it removes producer state and may remove the last registered Workshop. Global
reset `140f82f30` clears sets/caches. The complete direct registry data xrefs
(n01/n02/n12) distinguish these operations from the object-unloaded callback.

For a retained Workshop, `140f7ef20` resolves each registered handle and checks
Workshop identity/ExtraBC before iterating resource arrays. `140f7f1e0` uses the
same elapsed input for every row, checks due count, resolves producer and rechecks
reason in mode1. Neither the iteration nor ordinary downstream selection tests
player distance or a 3D pointer. Handle lookup `1428ccc40` (n04) checks masked
index, nonnull table entry and generation bits before invoking its callback;
it does not load missing references or require graphics. Ordinary reference
virtual+868 (`140b41a30`, n11) is flag-based in its CONT case, not a 3D lookup.
Thus ordinary resolvable unloaded references have a real production and local
delivery route, not a conjecture based only on global scheduling.

## State-by-state result

| Engine condition | Scheduling/bookkeeping | Inorganic production and local delivery | Fabricator/organic difference |
|---|---|---|---|
| Active but distant, registered/resolvable Workshop and producer | Frame elapsed reaches rows; current eligibility is recomputed | Eligible cycles create directly in selected reachable downstream store, own buffer fallback; ordinary old-stock movement still needs its caller | Same delivery, plus transitive input stock cap/removal; organic knowledge/selection remains E2 configuration boundary |
| Object-unloaded event, references still resolvable | Matching row retained; pending cleared at false event, cached eligibility refreshed; later elapsed updater does not rely solely on cached byte | Same operation is reachable without 3D/player-distance predicate; current power/halt/deleted flags still govern | Same row updater; actual species/configuration/input state may differ, no promise of active input supply |
| Resolvable Workshop, due individual producer fails handle lookup | Row handle becomes sentinel, pending += due * registration iterations; interval/remaining reset using base timer/fallback | No inventory creation by this failed path; graph/store stock does not prove pending was delivered | Same bookkeeping; no ingredient consumption/product creation on failed-handle path |
| Registered Workshop fails lookup or expected identity/ExtraBC gate | All its rows skipped in this invocation, no countdown or pending increment | No production/delivery from that traversal | Same |
| Workshop absent from registered set | Not enumerated | No elapsed creation from this traversal | Same; does not establish every other lifecycle writer absent |
| Resolved but halted, unpowered, disabled/deleted or lacking appropriate output/inputs | Nonzero reason; due path generally resets timer rather than preserving due debt | No reason-zero creation; reason3 adds full-related bookkeeping, not an inventory queue | Reason7 input shortage; output and input predicates remain separate |
| Explicit wait/sleep | `141a38ba0 -> 140f7ef20`; converted skipped-time chunks, not raw UT/local hours | Same current eligibility/receiver selection, potentially large batches and capacity crossing | Ingredient cap bounds realized request; repeated chunk rechecks can differ from one huge batch |
| Travel/skip | `141a27d80 -> 140f7ef20` with its computed scalar | Same operations for refs resolvable at that call; no universal guarantee about transition ordering | Same plus input ordering; exact current resolved set is unmeasured |
| Return/true object-loaded event with matching row | `140f8c580` updates eligibility, creates pending batch only if nonzero and eligible, clears it either way | Conditional catch-up uses ordinary downstream selector; not necessarily own inventory and not guaranteed retained debt | Same, with ingredient cap; pending clearing does not certify that all requested products materialized |
| Return after row sentinel/changed handle | Inspected matching callback requires current-handle equality; new row may instead be created | Guaranteed sentinel-to-current reconciliation/replay **not established**; do not report accumulated integer as preserved output | Same identity gap; new zero-pending registration is not proof of old debt recovery |
| Save/reload | Global saver restores registered refs and directed map; ExtraBC row loader restores/remaps scheduling state; caches rebuilt | Resolved refs can resume same mechanism; load cache rebuild alone is not inventory flush or elapsed catch-up | Saved resource selection/row and current effective AV/ingredients remain separate |

## Clocks, catch-up and capacity

E1's accepted arithmetic remains unchanged: positive interval I, elapsed>=I gives
trunc(elapsed/I), ignoring earlier remaining countdown. Otherwise subtract elapsed
and produce one due cycle on nonpositive remaining. Reset discards overshoot.
Frame scalar derives from scaled/smoothed/clamped engine elapsed; wait and travel
have explicit calendar/local-day conversions. Local-day display is not the timer
timebase. These branches can lose continuous-model cycles even with valid refs.

The due updater calls production once per registration iteration with due cycles,
not one callback per calendar second. Production selects one W<C target and
may add the batch across C. Another iteration rechecks state. Builders first cap
by inputs. Ordering between different producer rows/resources follows actual
native hash/array traversal, not a save-derived fair network schedule. Cached
counts/eligibility and ItemProduced counts do not independently measure item delta.

Remote redistribution of existing stock is possible when its explicit native
caller runs and endpoints resolve; it does not need a renderer. But ordinary
remote elapsed production primarily **creates at downstream storage**. Neither
remote production nor OnUnload proves a periodic sweep of old inventories.
The Transfer Container source unregisters its player/menu filters on unload;
one cannot infer remote player-event flushing from that source. Save/reload cache
reconstruction refreshes reachability, not all contents.

## Investigated boundary and smallest optional discriminator

Investigated: every direct registered-set data xref; add/remove/reset/save/load;
typed object-load and container-change dispatch; pending writer and consumer;
current eligibility and ordinary inventory paths; frame/wait/travel clocks;
forward cache rebuilding. No matching callback changes a sentinel row back to
the producer's current handle, and no universal historical elapsed timestamp is
established by these representations. This is a specific identity/residency gap,
not a claim that offline analysis cannot go further or that remote behavior is
wholly unknowable. Existing accepted evidence plus these paths is sufficient
for the conditional ordinary model.

If actual ordinary unload retention matters, the smallest proposed test is one
matched extractor/store and one fabricator/input/store chain, before and after
one leave/wait/return sequence on protected-copy saves, comparing actual inventory
deltas and producer handle/row/event state at the elapsed call. Predictions:
retained refs permit downstream creation before return; failed Workshop skips
rows; failed producer accrues integer without creation; return matching can
consume or discard pending. A read-only inventory snapshot alone cannot identify
which branch occurred. Value is discrimination of actual residency/order; cost
is live capture qualification and timing interference. No new instrumentation,
launch, save or test execution is authorized or made a prerequisite for S2.
