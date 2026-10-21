# Ship/pad state machine and full journey

[Answer](report.md), [inventory](inventory.md), [timing](timing.md).
Script method names below are actual shipped names. Native addresses elsewhere
are preferred static VAs in image base 0x140000000; they are not callable APIs.
PEX member-relative instruction offsets are retained in local `pex01.json`.

## Roles and authoritative transitions

The pad marker owns peer and ship links; incoming/outgoing bays and landing
marker are separate references. The quest creates **one shared ship per successful
CreateCargoLink call**, installs both endpoints' incoming/outgoing/marker links,
and puts that ship into both pad LinkShip slots. Endpoint01/02 is creation
orientation, not export/import direction. The ordinary script has no ship fleet,
per-item origin tag or separate return hold. Reentrant creation is guarded;
the ordinary successful pair model does not rule out duplicated exceptional
ships from faults or external changes.

| Event / condition | Source state → destination state | Authoritative side effects | Next authority / failure |
|---|---|---|---|
| Confirmed changed UI pair | Old pair → create/clear transaction | C1 native closes menu, installs reciprocal peer links, sends change event; marker clears old link before creating new | Quest CreateCargoLink, guarded; selection alone does not dispatch cargo |
| Create | No ship → linked ship at selected starting end | PlaceShipAtMe; retry failed creation with Utility.Wait(1), at most 30 failures; choose marker's ship base/start-end/RequiresFuel; install all links; destination AV=1 only for starting at end02; clear endpoint halt keywords | Failure message and marker calls ClearCargoLink; no indefinite creation retry or second normal ship |
| Travel package ends at current target | Travelling → arrived/unloading | Both installed package end fragments get actor's spaceship, cast it and call ArriveAtOutpost | Package completion is distinct from a landing animation/light callback |
| ArriveAtOutpost | Arrived → unload then readiness check | Select endpoint from Current==LandingMarker01; ship→that incoming using capacity respect; then local redistribution; send unload event | Ordinary un-fueled link passes. Fueled link requires at least one eligible non-mission linked marker |
| Readiness true | Unloaded/remainder held → waiting to load | Start game-time timer0 using cached load interval | No stock/ship-full/receiving-full threshold gates this timer |
| Readiness false | Unloaded/remainder held → waiting for fuel | Start game-time timer2 using cached retry interval | Timer2 calls ArriveAtOutpost again: unload is retried before readiness recheck |
| Timer0 delivered, ship enabled | Waiting to load → loaded/partly loaded/empty | Endpoint outgoing local redistribution/refill wrapper; repeated capacity-respecting outgoing→ship until count no longer changes; send load event | Arm timer1 unconditionally; rejected retained hold reduces room for new exports |
| Timer1 delivered, ship enabled | Waiting to depart → opposite target chosen | Change Current to the other landing marker; set destination AV1 or0; EvaluatePackage(false); set departure-end lights to landing/takeoff | Native AI/package admission and asynchronous movement, not immediate remote inventory delivery |
| Next package end | Opposite-target travel → arrival | Same unload/readiness/load sequence at opposite end | Automatic reciprocal flow if its outbox has stock; no separate reverse-link setup |
| OnShipLanding(false/true) | Visual landing in progress/completed | Notify landing-zone trigger at start; set marker animation/light AV to landing/landed | Neither branch calls TransferCargo or arms freight timers |
| OnShipTakeOff(true) | Visual departure completed | Restore departed pad's linked light state, accounting for Current already reversed | No load/unload mutation in this callback |
| Disabled when timer event runs | Any dock wait → no handler work | OnTimerGameTime returns after initialization | No automatic timer rearm in this disabled branch |
| Unlink/retarget/deconstruct | Old route → retired | Recover old hold to home ship then player; clear all old ship links, pad ship/peer links and isLinked; fuel-pad halt; disable or takeoff-disable; CancelTimers | New route creation is separate; see [recovery](lifecycle.md) |

`Current` is rewritten **before departure**. It therefore identifies the
selected receiving target during flight; it is not a current physical-position
oracle. The destination AV conditions the autopilot's first package: PACK2457b0
when AV2457af==1, followed by fallback PACK255cc4. Both use template PACK002cb0
Travel and target linked-reference keyword255cc3. Both end fragments call the
same method. The fueled and ordinary autopilot NPCs carry the same package pair.

## Worked partially blocked round trip

This is a **native-derived prediction with hypothetical stocks**, grounded in
the real principal pair's reference roles. It is not a decoded Save52 manifest.
Let A be Feynman I (marker ff03444c, out ff034474, in ff034475); B is VII-b
(marker ff02c3c4, out ff02c3ef, in ff02c3f0); ship ff02dc37. Creation orientation
in the saved links has VII-b as01 and I as02; A/B here deliberately denote
journey origin/destination, not those script indices.

Assume an eligible single item of mass1, effective ship/bay capacities300,
A.out=100, B.in=280, B.out=40, A.in=0, empty hold, no intervening production,
manual changes or successful local downstream redistribution. Those quantities
and mass are hypothetical, not installed item identity assertions.

1. At A, arrival unloads nothing. After the admitted timer0, loading removes
   100 from A.out and adds 100 to hold. Timer1 reverses Current to B and requests
   travel. No bay-full threshold or minimum cargo condition is checked.
2. At B's package end, unloading can add 20 to B.in. Hold retains 80. The subsequent
   incoming redistribution request cannot move anything under our declared
   blocked-downstream condition. No immediate second ordinary unload is issued.
3. B passes readiness. Timer0 loads B.out's40 into the **same** hold, now120.
   These40 are intentional reciprocal exports; the retained80 are refused
   outward freight. There is no new manifest splitting them.
4. Timer1 reverses Current to A. At A's package end, its incoming bay accepts120:
   A.in=120, hold=0. Both the refused80 and deliberate40 enter A.in. Nothing
   in this unload path sends them back to A.out.
5. Incoming redistribution can now move these120 downstream at A if its graph
   permits; the next load timer rearms. A future outgoing load is a separate
   operation. With B.out=0, the same trace returns80; with B.in initially300,
   it returns100 plus any opposite export that fits aboard.

The total stays420 units at every step: initially100+280+40, finally300+120.
There is no double creation. If A.in also has no room, the hold retains freight
again and can circulate. If the route is removed instead, cleanup sends hold
contents to home ship/player. [Native transfer limits](inventory.md) distinguish
this ordinary conservation model from failures, races and missing references.

**Falsifiable prediction:** a uniquely identified item loaded only at A, refused
at B and later seen entering A.in through this ship's unload supports return.
An item also exported from B cannot establish its original provenance without
counts/epochs. No new live test is authorized or necessary for this code-derived
ordinary mechanism; an incident-specific attribution would need that matched
history, not another static inventory screenshot.
