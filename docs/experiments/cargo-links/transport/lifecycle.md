# Remote transport, restoration and interruption

[Answer](report.md), [clock authority](timing.md), [saved fields](saves.md).
All native addresses are preferred static VAs, image base0x140000000.
The native/function ledger locates primary evidence; none was invoked live.

## What progresses without a visible ship

Game-time timers belong to the **bound ship script**, not a Workshop producer
row or renderer. `142032570 → 1420fb880` retains a bound script/ID in the timer
handler's game-time heap. `141fb3710 → 1420f9f90` compares its deadline to the
game clock and queues OnTimerGameTime. Neither heap traversal nor the shipped
freight handler tests player distance, current planet, 3D presence or Workshop
registration. Native inventory planning/removal likewise does not require 3D.
Thus a resolvable graphically unloaded ship and endpoints have a real reachable
load/unload/timer route. Merely being distant is not a causal stop condition.

Travel is **additional native work**, not an implicit timer-triggered delivery.
The installed autopilot package pair uses Travel template002cb0 and the Current
linked landing marker. BGSProcedureTravel constructor/vtable and its entry/update
methods are exported: `140e065f0`, `140e06760`, `140e06a80`, `140e06bb0`. Its update
selects process+e7 branches0,1,2/3 to `140e06f60`, `140e09360`, `140e09c90`.
Those routines inspect current target/path and admission flags; they are not
another Workshop elapsed updater. The 2/3 branch has explicit target/movement
handling and procedure-completion stores, rather than an unconditional skip
because there is no high-process renderer.

`141994ed0/141995020` resolve an actor's controlled object/ship; movement request
submission follows `141924dc0 → 141924af0 → 141a9e680`, with actual path-state
construction at `141a9eb00`. Flight/landing work can use PathingRequestFlyLand,
created by `140ea62c0`; the Travel flight branch `140e08e90` submits that request
and later checks `1412ab460`. The latter queries **IMovementQueryPathingState**
virtual+58, defaulting true when the interface is absent. In contrast,
`140e06ea0` only compares request identity; that is not a completion-time oracle.
On the completed branch the procedure marks its completion, with target
resolution/disabled handling before positional finalization. Package end then
calls the shipped fragment, which is the explicit bridge to inventory unloading.

This supports a **conditional native remote transport model**, not a claim that
every unloaded/dormant actor receives identical updates or every unresolved pad
is loaded on demand. Travel requires admitted native AI/pathing/completion work;
saved target/stock alone cannot reveal the historical branch or its duration.
Graphics/light callbacks are separate consumers and do not govern stock mutation.

### Concrete completion provider and detached movement

The virtual completion query is resolved beyond its interface name.
`1427073d0` registers MovementPathManagerArbiter+20 under the pathing-state key;
its vtable144d92b58+58 is `142708c90`. It returns true only with a nonnull
request and state3 (interface-relative+20/+40, whole arbiter+40/+60).
`142707540` polls the query-following interface while state2 is active;
successful completion calls `1427091d0`, which writes state3 and publishes
MovementMessagePathComplete. Failed/cleared paths instead use `142708e50` and
their distinct messages. Thus request identity, completion and failure are
different observations (n35/n39/n40/n41).

The executable also supplies a concrete **MovementAgentFlightControllerDetached**,
not just a generic offscreen hypothesis. Constructor `1427327f0` installs its
update interface at whole-agent+18 and query-following interface at+28.
`1427321d0` accepts a path with more than one entry, retains request/path and
resets its accumulator. `142731f50`, called with the update-interface pointer,
adds the supplied float movement delta; crossing the start threshold publishes
the first path payload, and exceeding start+delay publishes the remaining
payloads and calls its own cleanup interface: n032 at142732119 forms
update-interface+8 (whole-agent+20), whose vtable144d95dd8+30 selects
`142732280`. That routine clears/releases the retained request/path.
Query-following `142732320` consequently reports completion because its retained
path is absent. This is controller cleanup, not a call on the retained request.
These are real completion/provider paths, not freight animation callbacks.
`140eb4b90 → 140eb0340` is the registered FlyLand path builder, producing path
entries for this movement machinery (n32/n33/n35–n47).

The settings and strict comparisons are detailed in [timing](timing.md#native-flight-duration-boundary).
This investigation does not recover which controller and movement-delta source
were admitted for a particular historical Save52 ship. Neither a six-second
universal flight duration nor distance-independent loaded animation duration
follows from detached defaults. The concrete unmeasured operands are controller
selection, delivered update deltas/pause state, current request/path and event
queue latency. Ordinary remote transport has a native causal route; arbitrary
dormant/invalid references are not thereby certified to progress.

## Distinct operating and failure states

| State | What the mapped mechanism does | Cargo consequence / recovery limit |
|---|---|---|
| Distant, bound/resolvable ship and endpoint references | Timer and inventory calls remain reachable; native package/pathing has process-state alternatives | Normal two-end transfers can run; no player-presence requirement in these paths |
| No visible ship3D | PEX freight handlers and inventory planner have no Is3DLoaded gate; marker OnLoad restores light display | Absence of animation is not evidence no transport; actual movement admission still separate |
| Graphically unloaded but registered Workshop | Cargo timer heap does not enumerate S2 Workshop producer rows | Cargo/production can have different cadence and stalls; S2 registered/resolvable producer model cannot substitute for cargo |
| Workshop unregistered | Script timer can still be bound; arrival fuel gate may fail current Workshop production admission | Ordinary RequiresFuel=false avoids that fuel check. Unregistered state is not automatically a cleared route or a valid remote outpost |
| Pad/ship handle unresolvable | Linked-reference lookup or script binding may fail; no universal load-on-demand/retry is present in TransferCargo | Not the same as full capacity. Missing endpoint pointers are not qualified receivers; no guaranteed item preservation or recovery from already lost ship |
| Fueled route lacks eligible supply at both ends | Arrival unloads what fits, then arms timer2; retry repeats arrival/unload/check | Stock already aboard is retained under valid capacity refusal; either non-mission endpoint becoming eligible can resume timer0 |
| Fuel becomes unavailable after passing arrival check | Timer0/1 contain no fresh fuel readiness comparison | No demonstrated mid-flight fuel abort or rollback; next arrival/retry rechecks. He-3 charge/production coupling remains C3 |
| Incoming full / partially blocked | Native transfer returns early or plans fitting subset; script still moves to load/depart if readiness passes | Retained stock can return/circulate; incoming flush after unload can free space too late for that attempt |
| Outgoing empty / ship partly full | Load loop ends on unchanged count and arms timer1 | Ship leaves empty/partial; no minimum-load wait |
| Ship disabled when a timer runs | Handler checks IsDisabled and returns | That event does not rearm itself; simply re-enabling is not proven to restart a stranded timer chain |
| Retarget or remove link | Marker change clears old pair before creating replacement; no manifest is redirected to new peer | Resolve old hold→home ship capacity fit, then remainder→player; retire old ship and cancel timers |
| Pad deconstruction | OnWorkshopObjectRemoved calls ClearCargoLink(self,None); quest resolves peer then clears both | Same old-hold recovery if ship resolves; incoming/outgoing child stock follows separate construction cleanup, not this ship-hold routine |
| Busy/failed ship placement | At most30 failed PlaceShipAtMe attempts,1-second real waits; failure message and route clear | No normal transport starts without a ship; rollback of native pairing is explicit marker/quest cleanup |
| Unexpected ship loss/despawn | No automatic replacement loop is present in ship timers or marker load callback | Absence is not proof of deletion semantics; the ordinary creation and clearing paths do not certify recovery from all engine faults |
| Concurrent unlink and already executing callback | Create/Clear use cargoLinkGuard; TransferCargo is not guarded by it | Cancel removes pending timers but cannot be assumed to undo an already running transfer. No universal race/atomicity proof |

## Wait, fast travel and reload

During explicit wait/sleep, player+dd4 suppresses game-time timer delivery in
`141fb3710`; E1's wait loop advances calendar/production in chunks separately.
When normal VM service resumes, each existing due timer can queue once. A later
stage is armed using **then-current** clock; no loop replays every lost voyage.
Ordinary gameplay away from endpoints can service timers without that wait flag.
Fast travel's calendar skip can make a deadline due, but its exact ordering with
AI movement and VM service is not inferred from E1's producer caller. Neither
sleep nor travel warrants multiplying ship capacity by elapsed/calendar cycle
count. A pending route leg still requires its native completion/fragment.

Saved hold/links/destination are concrete persisted state. Native timer saving
`1420fa390` writes the bound script, ID, remaining deadline and pause fields;
load `1420fa9a0/1420fcc70/1420f8d00` remaps and rebuilds the heap relative to current
clock. Mutable script cached intervals/RequiresFuel belong to VM instances,
not the decoded REFR inventory tail. Travel procedure save/load
`140e0a140/140e0a360` and FlyLand `140ea6420/140ea6540` retain/remap their own
polymorphic/path state. These channels are distinct; restoring an item or a
target reference does not prove an actual historical completion event.

Marker OnLoad restores animation state; it does **not** reconstruct a lost ship,
flush the hold or reset the freight timer sequence. No separate script
OnPlayerLoadGame catch-up routine exists in these fully decoded ship/marker
bodies. An existing timer can resume under native restoration, with missing/
invalid bindings handled by the loader's failure branches; no guarantee of
whole-route convergence after all exceptional interruptions is asserted.

## Specific remaining operands and possible discrimination

The ordinary inventory-return discriminator is resolved by actual code. Exact
historical Save52 flight phase, live AI process/resolution, effective capacity,
cached intervals and bound timer entry are not recovered. Source/direct-native
completion paths are distinguished from proof a specific saved ship took them.
These unknown historical operands prevent a precise observed-trip duration or
incident attribution, rather than negating the two-end causal cycle.

If actual remote residence or a particular stall becomes consequential, the
minimum useful evidence would match one ship's bound timerID/deadline delivery,
Current/destination, native path request/completion, endpoint resolution and
inventory before/after one ordinary absence interval. It would distinguish
timer waiting, delivered-but-queued script work, native travel pending and
capacity refusal. Screenshots of stock alone cannot do that. No observer or
live test is authorized or made a prerequisite merely because historical
execution was not captured. C3 remains detailed He-3 acquisition/rate/fuel
transport/replenishment/persistence, not a deferral of this remote transport study.
