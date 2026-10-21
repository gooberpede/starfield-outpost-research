# Cargo scheduling, clocks and modifiers

[Answer](report.md), [cycle](cycle.md), [remote/recovery](lifecycle.md).
Prospective 2026-10-18 continuation: [native movement and round-trip model](transit.md)
extends the historical flight-duration boundary below with controller selection,
assembly-backed elapsed callers, physical-flight operands and calendar 15/5 cases.
Native addresses are preferred static VAs, image base0x140000000; object offsets
are hexadecimal. Local nNN denotes `.local-work/c2-transport/native/NNN.request.tsv`.
The production clock in [E1](../../inorganic-extractors/arithmetic-clocks.md)
is a separate mechanism, not cargo's timer contract.

## Script authority and native deadline

Both ordinary and fueled ship definitions use SQ_OutpostCargoLinkShipScript;
neither VMAD overrides its 30/15/30-second timer properties. Shipped PEX confirms
the source's consequential arithmetic and calls, with debug traces removed.
OnInit initializes once; each OnTimerGameTime calls the initializer again,
whose timersInitialized guard prevents resampling after successful initialization.
For source seconds S and initialized ground setting G:

```
H = binary32(binary32(S / 3600f) * G)     # requested game hours
N = trunc_i64(binary32(max(H, 0.03333333507180214f)
                      * 41.66666793823242f))
deadline_u32 = current_game_tick_u32 + low32(N)
current_game_tick = low32(trunc_i64(binary32(DaysPassed * 1000f)))
```

`142032570 → 1420fb880` (n04/n06) is the actual StartTimerGameTime native route.
`1420fb8fb..1420fb90b` shows VMAXSS, VMULSS and VCVTTSS2SI; constants are pinned
at 144f03fb4 and 144f04be4. The minimum request is approximately two UT minutes,
and one integer tick is .001game day =86.4UT seconds. This is **not** an integer
millisecond timer. The conversion factor is 1000/24 hours, with binary32 rounding.
Do not promote source comments equating .04/.02hours with30/15seconds to the
installed contract.

Clock producer `141887c90` writes VM+7dc from Calendar+30's GLOB value×1000;
`141fb3670` refreshes that clock explicitly and `141fb8ae0` reads it (n08/n14).
Calendar construction `14059ac20` binds+30 to GLOB000039; `1418778e0` maintains
days-passed from game hours/24 plus its retained day origin (n19/n21). The
calendar progression uses current TimeScale; player context `1417df210` writes
ground/space setting into TimeScale00003a (n14). Installed GMST00495e is 15,
whereas missing-setting native initializer14008c720 has fallback30. Current
overrides and a restored script's cached G are distinct inputs.

The handler stores the bound script pointer, timer ID, deadline+10, pause
bookkeeping+18 and paused byte+1c in a20hex-byte entry. Its game-time heap is
manager+70/+78, separate from real-time+60/+68. Starting the same bound script/ID
updates/reheaps its existing entry, clears pause bookkeeping and uses **now+N**;
it does not append one event per missed interval. `1420f9f90` pops a due unpaused
entry before queueing OnTimerGameTime with that ID (n10). The heap lock is released
before VM event execution; queue acceptance is not proof the cargo handler ran.

`141fb3710` snapshots the clocks, services timer heaps and requests VM work.
It skips the game-time heap while player+dd4 is nonzero, the wait/sleep field set
and cleared in E1's actual wait loop. `141fb3d70` explicitly refreshes the game
clock for its VM update route (n17). Timer0's handler loads then starts timer1;
timer1 reverses target and evaluates packages; timer2 calls arrival/unload again.
Disabled ships return without rearming. Ordinary arrival itself starts a timer
only after unloading/readiness. There is no fixed global cargo tick and no
producer pending-count replay in these scripts.

## Contrasting timing calculations

**A — normal calendar progression, grounded defaults; hypothetical clock phase.**
Take the physically reread main-ESM G=15 and shipped S_load=30, S_takeoff=15.
Then requested H_load=.125h and H_takeoff=.0625h; native durations are respectively
**5 and 2 integer ticks**. Fuel retry is 5 ticks. At hypothetical current tick 1000,
deadlines 1005 and, when timer1 is armed at 1005,1007 follow. With constant
TimeScale15 and prompt dispatch at exact tick boundaries these represent28.8
and11.52wall seconds; they are **calculated examples**, not measured retail
durations. Initial phase can reduce the first wait by nearly one tick, and
binary32 DaysPassed, frame/VM latency, pause and new-arm epoch affect the result.
Changing current TimeScale to30 after initialization halves these wall-time
equivalents without changing cached H or N. Native fallback G=30 instead would
initialize10/5ticks, a different case from installed15. Flight time is additional.

**B — wait/sleep across a deadline, hypothetical jump.** Start with timer0 due
at 1005 and current tick 1000. A sleep advances calendar to 1100 while player+dd4
suppresses that heap's service. When normal dispatch resumes it can emit that
**one** timer0 event. Its eventual handler loads once and starts timer1 from
its then-current tick, for example 1102 if current is 1100. There are no 20 missed
load events and no automatic20 completed round trips. Fuel polling similarly
rearms from its actual retry callback. Fast travel can advance the same calendar
through a different caller, but ordering with travel/package and VM service must
be established per case. No proportional freight catch-up formula follows.

These examples can be independently recalculated from the pinned operands and
instruction-backed rounding. They are not a replacement shipping simulator.

## Native flight duration boundary

Flight is admitted by native AI/pathing, separately from dock timers. The
[completion trace](lifecycle.md#concrete-completion-provider-and-detached-movement)
resolves the actual arbiter query and a detached flight controller. Its native
initializers `14024ae20/14024ae50` define
`fDetachedFlightPathingStartDelay:Pathfinding` and
`fDetachedFlightPathingDelay:Pathfinding`, values at 145f9d7f0/145f9d810.
The pinned executable defaults at 144f04768/144f04980 are binary32 **2 and 4**.
They are mutable settings, not ESM dock-timer properties or saved stock.

In `142731f50`, let a be its accumulator and d the supplied movement-update
delta, both in that caller's movement timebase:

```
if a <= start and a+d > start: publish first path payload
a = binary32(a+d)
if a > start+delay:
    publish remaining path payloads
    call controller cleanup interface -> release retained request/path
    a = 0
```

No LY-distance multiplier or per-item freight rate appears in this consumer.
For hypothetical start 2/delay 4/delta 1 starting at 0, first publication occurs at 3
and remaining publication at 7, because comparisons are strict. This is a
calculation in **movement-update units**, not a measured seven-second flight.
Cleanup `142732280` makes query-following `142732320` true by clearing its path;
the subsequent arbiter poll can therefore publish path completion. The supplied
delta's concrete timebase/admission and the selected controller
for each historical ship are not recovered here; converting these defaults
to wall/UT time without that connection would be unsupported. Loaded physical
path/landing work can additionally depend on target/path/actor process state;
the FlyLand request carries its own position and movement parameters. The
mapped native movement and provider contracts establish a meaningful boundary,
not a universal astronomical-distance flight formula. Neither main-ESM package
supplies a separate ordinary/inter-system scripted flight interval.

## Contributor inventory and bounded absence

| Contributor | Definition / read / arithmetic | State class and consequence |
|---|---|---|
| Dock/load, takeoff, fuel retry | PEX auto-property defaults30/15/30; InitializeTimers divides3600 then multiplies G; IDs0/1/2 select handlers | DEFINITION-DERIVED defaults; instance/cached fields PERSISTED via VM; initialization flag prevents automatic resampling |
| Calendar scale | GMST fCalendarTimeScaleGround15 at initialization; current TimeScale drives DaysPassed, ground/space context can rewrite it | Cached G differs from live calendar rate; planet-local wait conversion changes calendar amount, not a cargo planet-speed coefficient |
| Timer quantization/minimum |1420fb880 max~.0333333game hours;×41.6666679; truncation; current DaysPassed×1000 | TRANSIENT deadline rebuilt from persisted remaining time; changes short nominal waits and response to scale changes |
| VM/pause/wait state | Heap pause byte; bound script; VM update/freeze and player+dd4 wait gate; queued event execution | TRANSIENT/live-derived; game calendar passage alone does not execute script stages |
| Current target/destination | Current linked marker and AV2457af; package2457b0 condition==1, package255cc4 fallback | PERSISTED selections; native resolution and AI/package completion admit next arrival |
| Fuel readiness | RequiresFuel set by creation; either reverse-linked non-mission pad CanProduceForWorkshop at arrival/retry | MIXED; actual production reason, halt and input availability matter; no dedicated cargo quantity threshold here; detailed He-3 stays C3 |
| Freight quantity | No minimum-load/fullness test in timer branches; ordinary all-item transfer; mission SpecificCargo/Max switches operation | Live stocks and retained hold; loaded partial/empty departs; mission limits are not ordinary throughput settings |
| Capacity | CONT CarryWeight/effective AV; ship14211b700 adds CarryWeight and CarryWeightShielded (default object2407e8→AVIF02b344), then applies perk entrypointAA to a float pointer | MIXED definitions/instance modifiers/live perk context; not universally the UI fallback300 |
| Capacity perks | Main-ESM AA entries: OutpostCargoLink_OutpostManagementBuff0ce860×1.5 conditioned on player OutpostManagement rank>=4; Skill_Payloads143b6b×1.1/1.2/1.3/1.5; CREW_Ship_Payloads222f84×1.1 entries; MagPerk_KryxsJournal209094×1.05 entries | Definition candidates, **not a claim every player/crew rank applies to this cargo ship**.1421230a0 selects actual perk actor/context; current assignments/ranks/conditions must qualify. Main-ESM AA census retained locally |
| Item competition | Native eligible item/form gate, current instance/base mass, count; constrained transfer sorts value/mass; partial floor fit | Live-derived; no items-per-second loading/unloading animation rate or manifest order in ordinary TransferCargo |
| Ship movement | Same Travel template/package pair for both ship bases; native location/pathing, process-state and movement-completion gates | RECONSTRUCTED/native state; dock timer constants do not prescribe astronomical distance/LY travel time. See lifecycle.md for traced branches and remaining operands |
| Detached flight settings | Native start2/delay4 initializers, mutable145f9d7f0/145f9d810;142731f50 strict comparisons and payload/callback delivery | Live-derived movement settings; concrete controller/update timebase remains a specific boundary. No warranted universal6-second flight claim |
| Creation/retirement |30×1-second failure waits on occupied creation; cancellation of all 3 game timers on cleanup | Real-time Utility.Wait is separate from freight game timers; recovery is not another normal shipment |

Within all shipped ship/quest freight-handler bodies there is no direct read of
player skill, crew bonus, difficulty, route LY distance, per-planet day length,
or E1 production intervals to multiply the dock waits. That is a qualified
absence within fully decoded bodies, not absence from native movement, effective
capacity or fuel admission. Discovered perk definitions and native providers
are retained rather than silently declaring all cargo capacity fixed. Graphics
callbacks change trigger/light state but do not transfer stock; this separation
is directly visible in both PEX and source.
