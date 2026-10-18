# Native movement and round-trip timing

2026-10-18. SOR-EXP-0045 / SOR-EV-0053, continuation under the
[transit brief](../../../implementation-briefs/CODEX_BRIEF_SOR_C2_transit_time_continuation.md).
[Earlier answer](report.md), [dock clock](timing.md), [completion](lifecycle.md),
[continuation review](transit-review.md). Earlier accepted coverage remains a
historical result; this document adds the subsequent native investigation.

## Answer and claim scope

**Movement contributes time in addition to link loading/unloading and departure
waits.** Native code offers a thresholded detached flight path and a fully
simulated flight path. They are different implementations, not two names for
an astronomical-distance timer. Ordinary and fueled cargo ships share their
Travel packages and freight timer defaults. No separate in-system versus
inter-system duration constant is present in those bodies or the detached
consumer. This establishes a shared conditional timing model, not equal measured
journey durations for every route.

The installed calendar settings add a consequential modifier: ground 15 and
space 5. A script initialized with ground 15 retains the same dock deadlines when
the live calendar rate changes to 5; their wall-time equivalents triple. This
depends on player/ship context and current settings, not simply the cargo link's
system category. The calendar and movement clocks must be kept separate.

A conditional round trip can be calculated from four dock waits, two native
movement legs and explicit admission/queue/fuel delays. A universal retail
round-trip time, or an empirically calibrated error bar, has **not** been
established by this offline study. The specific unresolved operands and usable
conditional estimates are below. Confidence is strong for the traced static
mechanisms; coverage does not include a historical per-ship execution trace.

## Provenance and evidence convention

All native addresses are preferred static VAs, image base `0x140000000`;
object/interface offsets are hexadecimal. They are not runtime pointers or
safe callable APIs. Retail EXE 1.16.244.0 SHA-256
`7e9adb1414a8e1b325e5e1f097b9b17b78deb7eebeda37a333351a43a60f9d28`;
main ESM SHA-256
`1dabed00c3f4282dd3bb54d2e9601e40b577d8742d078b7ccef203adbfef0da7`.
These match fresh physical preflight reads, not an assumed earlier baseline.

`tNNN` means `.local-work/c2-transit/native/NNN.request.tsv`, and `nNNN`
means the prior `.local-work/c2-transport/native/NNN.request.tsv`. Exact export
lines, function bounds and hashes are in [native locators](transit-functions.csv)
and [source pins](transit-sources.csv). Original exports, decompiler warnings,
failed requests, strings and definition fields remain LOCAL-ONLY. Authored
interpretation/metadata remain REVIEW-REQUIRED. The existing matching Ghidra
project was opened readOnly/noanalysis; no imports, reanalysis or analysis-state
edits. No game launch, attachment, instrumentation or save editing occurred.

## Movement selection and admission

Travel's `140e08e90` resolves its controlled object through `141994ed0`, submits
FlyLand, then queries that object's path state through `1412ab460` (prior C2).
`1412aa5c0/1412aa710` distinguish Actor type 4b, whose controller is Actor+240,
from a non-Actor's MovementControllerComponent obtained through ComponentDB.
Do not silently equate the autopilot actor with its ship reference.

The component constructor `140689180` installs vtable 144b35198 and constructs
MovementControllerComponentData at controller+78. `140689740` registers that
state provider under CurrentMovementState key 145f9d830. The common controller
maintains an active set of arbiters/agents. `14068a750` selects description
1461e0220 when controller+5c equals 2, otherwise 1461e0248. The latter is built by
`140688510` with PathManager/Planner arbiters and the detached flight agent key
from `142731ed0`; `1406859d0` builds the former with the full flight agent.
`140684ba0` also builds a full-flight description 1461e0250 for another set.
The flight-set method is vtable+40; normal movement has a distinct +38 selector.
These are explicit state-conditioned choices, not a single global flight mode.
Specifically `142738c60`'s state 1 rebuild queries provider+e8: value 4 selects
flight+40 when controller+5d is zero, or alternate+50 otherwise; other values
select normal+38/+48 respectively. The mapped +40 flight description therefore
has an explicit admission condition, not unconditional use by every ship.

`142739530/142739590` change mode to 2/1 only when the corresponding virtual
+80/+88 admission succeeds. The component's +88 implementation `14068a7c0`
also clears cached motion/speed state. Actor process transitions such as
`141922590` choose these modes using current-process+e7; component and actor
callers are separately retained in the locator ledger. Thus loaded/process
residence can change the applicable mechanism. The installed base definitions
alone do not recover which mode a particular Save52 ship used throughout a leg.
The reference transition `140b2d0c0` resolves its component, resets state,
chooses mode 2 when parent/context pointer+b0 is non-null and `140574ef0(ctx,0)`
is true, otherwise mode 1, then rebuilds through `142738ef0 → 142738d90`.
The predicate returns true for context state+4f values 9/10, has conditional 5..8
branches involving context flags/ship resolution, and false defaults. It is
not a simple cargo-route-category test. No semantic name is assigned to every
raw state value. Rebuild can be deferred while update+71 is active; merely
writing mode does not prove the final active set already changed.

## Elapsed producer and staged consumers

Decompiler signatures lose floating-point arguments at important indirect
calls. The following interpretation uses actual instructions:

| Step | Concrete data flow | Meaning |
|---|---|---|
| Common caller | `1412af0e0`: XMM2 saved in XMM7 at 1412af110, moved to XMM1 at 1412af274 before CALL RDX at 1412af27b; RDX is controller vtable+18 | Actual float supplied to the common controller update |
| Cargo-reference route | `1405883b0 → 140b04ad0`: XMM7 = 145fbf9a8 times a normally 1 relative factor; at 140b04b71 it supplies XMM1 to 1412aeb90 when the separate Extra9d movement route did not handle the reference | Explicit reference movement update, including non-Actor components |
| Controller resolution/dispatch | `1412aeb90`: gates through reference+730 and 1412ac500; 1412aa710 resolves Actor/component controller; at 1412aebf6 R8 receives that controller and XMM1 receives saved delta before reference+698 dispatch at 1412aec02 | Reference primary table 144b95fb8+698 = 144b96650 selects 1412aee90; constructor 140b21e70 and table receipts establish this provider |
| Reference wrapper | `1412aee90`: XMM1 retained in XMM6, copied to XMM2 at 1412aeec0 before calling 1412af0e0 | Floating elapsed survives preliminary state work |
| Actor route | `1418e9cb0`: accepts supplied positive elapsed, or in its admitted zero-input branch reads 145fbf9a8 at 1418e9d8d; special controlled-reference branch applies a relative scale | A concrete path from engine frame seconds, not DaysPassed or the VM integer tick |
| Common consumer | `1427342e0`: VMOVAPS XMM6,XMM1 at 142734309; stores delta in the frame context; active arbiter vtable+48 receives that context | Shared AI/NPC/component vtables point here at +18 |
| Detached stage | `142707520` advances context pointer by 8, `142707540 → 1427076d0` invokes the agent update interface+18 | Detached 142731f50 reads the supplied float directly |
| Full flight stage | `14271e190` reads nested motion context+48 and later multiplies its motion calculation by that scalar | Physical path following also consumes elapsed; its initial state+38 read is current speed, not time |

The upstream frame clock is independently mapped in
[E1](../../inorganic-extractors/arithmetic-clocks.md#frame-elapsed-calendar-progression-and-skipped-time-differ):
QPC → integer milliseconds → `1422cce10`, context 145fbf990+18 = 145fbf9a8.
Its ordinary branch clamps 166 ms, converts × .001, optionally smooths, applies
frame scale 1458d58f4 and respects a nested freeze counter. This supplies engine
seconds; engine seconds need not progress one-for-one with wall seconds during
freeze, slowdown, overload or fixed-time overrides. Calendar scale 15/5 is a
different operand. The reference route above closes the ordinary component
delta connection. `140b04ad0` applies the special relative factor when the
reference equals the player's current controlled object; this is not a cargo
category coefficient. `1412ac500` resolves current controller state, messages
and component inputs before admission; it is not a duration-from-distance
formula. Historical admission, overrides and delivered delta sequence remain
unobserved, so there is no universal movement-seconds/wall-seconds guarantee.

There are other actual callers: `141271140` reads the same frame scalar for its
process-state movement work, and `141a850a0` has conditional frame-scaled and
zero-input updates. The travel/skip path `141a27d80` passes its XMM6 elapsed
to 1412aeb90 at 141a28108..0f for a qualified process list. This is the same scalar
used to advance calendar and production in E1, with an input+7c/scale/speed
conversion. A skip can therefore deliver a large movement delta to admitted
objects; it is not evidence that every remote cargo reference is in that list,
nor that freight VM stages replay while calendar jumps.

## Detached path: thresholded completion

Constructor `1427327f0` has its PlannerStage interface at whole+18,
notification/cleanup at whole+20 and query-following at whole+28.
`1427321d0` accepts a path with more than one entry, retains request/path and
resets the movement accumulator. Update `142731f50` adds the admitted float.
Native settings at 145f9d7f0/145f9d810 have defaults 2/4, set by
`14024ae20/14024ae50`. They are mutable Pathfinding settings.

For a fresh path with positive delivered deltas, first payload publication
occurs when the accumulated value crosses **strictly greater than 2**. When
it exceeds **2+4**, remaining payloads are published, its own cleanup interface
calls `142732280`, retained request/path are cleared and accumulator resets.
Query-following `142732320` then reports completion; `142707540 → 1427091d0`
can publish MovementMessagePathComplete. Later Travel/package/fragment/VM work
still has to run before unloading. Clearing a path through a failure/cancel
route must not be counted as successful freight arrival.

There is no distance, mass, cargo count, star-system category or per-planet
clock multiplier in the complete detached update body. Its threshold is per
admitted path, not per entry: remaining entries are delivered in a loop at the
second threshold. More entries do not multiply the 4 setting. A replacement
path can reset timing; admission and subsequent callbacks are additional work.
The primary agent reset's whole+38 is **not** the update accumulator at
whole+50 (update-interface+38). Interface-relative offsets matter.

## Full flight: geometry, movement profiles and actions

Constructor `142723220` installs the full agent. Its PlannerStage+18 update
is a no-op; **MotionStage** at whole+20, vtable 144d94958+10, selects
`14271e190`. Calling this a detached timer would miss the actual motion work.
The function uses current velocity/speed, current path entry/position, local
coordinate origins, turning/easing and MovementType curves. `1426cca70` obtains
a profile through CurrentMovementState+68; `1426cd920` interpolates speed and
`14273c7f0` interpolates further movement coefficients. These are local path
geometry and motion operands, not direct light-year travel divided by speed.

The component provider `140689e00` copies nine rows of seven floats via
`140689d30`, optionally scales the first six rows by an object-derived scalar,
and calls the object's +5e0 override. Main-ESM MOVT 008e74 Spaceship_Default and
MOVT 051b25 Spaceship_NonModular_MT each contain 252-byte SPED data, consistent
with the nine-by-seven consumer. The actual per-cargo selected profile and
override values must be resolved before assigning speeds. Equal packages are
not proof of equal physical ship performance: NPC 255cc5/219041 and their
GBFM 255cc6/219042 have inheritance relationships but different base fields.

An additional conditional branch reads motion-context+65 and
`fCruiseModeForwardThrottlePercentage:Spaceship` (145f9d650, default 1), multiplied
by 145921f4c. `1427231e0` clamps that input to 0..1. This is a shared-controller
input, **not a demonstrated ordinary cargo perk or user-adjustable route bonus**.
Neither presence of the branch nor a setting name establishes its activation
for a particular cargo flight.

`1427212f0` retains a new path, starts its index at 1 and publishes its first
payload. `1427216f0` queries current path-action state; it returns pending 0
when action identity/status predicates continue, otherwise 3 for that test.
`142721910` clears/releases request/path/index. FlyLand builder `140eb0340`
and `140eb4530` construct/adjust local path entries and payloads;
`140eb4a40 → 142682e60/1426830e0 → 142685190` is geometry/LOS modification,
not a discovered transit-clock producer. Native action completion, path
replacement and controller admission therefore remain material timing inputs.
The full-flight consumer does not supply a fixed six-second loaded flight.
It publishes passed-node payloads through `14271fc50` and increments its index;
at the final admitted geometric/action/rotation condition it
publishes the last payload and calls notification+30 at 14271f532, selecting
the same `142721910` cleanup. Query-following `1427219c0` (whole+30 interface,
vtable 144d946f0+8) then sees cleared path at interface+40. This connects physical
progress to the arbiter's completion query, rather than inferring completion
from the lack of 3D. `14271fd10` computes steering/avoidance corrections;
its boolean result can also clear a movement flag, not replace final-path
completion. No new timer or astronomical-duration coefficient is identified
in these complete helpers.

## In-system versus inter-system and modifiers

| Contributor | Supported consequence | Bound of the conclusion |
|---|---|---|
| Link category | Both ship definitions use the same Travel package pair and freight timer properties | No category-specific scripted interval; does not prove equal loaded geometry/actions |
| Detached start/delay |2+4 per fresh admitted path; strict comparisons; mutable settings | Distance-independent in this consumer, conditional on detached selection and delivered elapsed |
| Full movement | Path geometry, speed profile, object-derived scaling/overrides, turning/easing, actions | Actual selected values and path required; no numeric universal distance coefficient |
| Cached ground setting G | Initialization builds game-hour waits once; installed G = 15 | Saved/overridden script cache need not match today's installed default |
| Live calendar rate T | Installed ground 15/space 5 can change wall-time equivalents by 3 | `1417df210` uses current player/ship context predicate; not cargo route category |
| Frame scale/freeze/admission | Changes movement elapsed delivered per wall second; may suspend progress | Distinct from calendar scale, production catch-up and VM service |
| Game-timer quantization and phase | 5/2 ticks per endpoint with G = 15; one tick 86.4 UT seconds | Binary32 clock precision and actual arm epoch matter |
| Fuel readiness | Fueled ship can re-enter arrival/readiness on timer 2; retry 5 ticks with G = 15 | No finite trip upper bound while readiness fails; detailed He-3 remains C3 |
| Inventory/VM/package work | Transfer loops, queued events and completion fragments add latency | No evidence-calibrated bound in this offline sample; no fullness wait in ordinary departure |
| Wait/sleep/fast travel/reload | Calendar deadlines and restored state can change without replaying full voyages | Do not convert skipped calendar time into completed round trips |

Settings containing “UnreachableStarDistance” or “FlatPenaltyParsecs” were
retained as pathing leads; their names are not evidence of a duration penalty.
The bounded negative here covers the decoded scripts, compared packages,
detached update and mapped full-controller arithmetic. It does not certify
every path-action implementation or every reachable native branch.

## Round-trip model and tolerance

Choose a cycle boundary: **arrival/unload at A to the next arrival/unload at A**,
through B with one shared ship. Creation/retirement and route changes are
outside this normal-cycle model. Let D be the four dock waits (load/depart at
each end), M_AB and M_BA be movement intervals from admitted request to its
completion, and Q be remaining inventory/script/AI/package/admission latency.
Let F include extra fuel retries/readiness delay. Then:

```
R_wall = D_wall + M_AB_wall + M_BA_wall + Q_wall + F_wall
```

Every interval has its own clock. For uninterrupted constant live calendar
scale T and cached G = 15, the ideal integer-clock dock contribution is:

```
D_wall = sum((N_i - phi_i) * 86.4 / T),  N_i = [5,2,5,2]
0 <= phi_i < 1                 # fractional tick at each actual arm
```

This deliberately excludes callback lateness (Q) and assumes an adequately
resolved, monotonic DaysPassed clock without jumps. Independent possible arm
phases give `(10,14] * 86.4/T`: **(57.60,80.64] s at T = 15**, or
**(172.80,241.92] s at T = 5**. This is an analytic phase envelope, **not a measured
confidence interval or an all-game bound**. Prompt exact-boundary callbacks
correlate later phases; they cannot be treated as four independent random
errors. Binary32 DaysPassed precision, changing rates, pause and queued work
must be added explicitly before predicting a particular save.

For detached movement, use the first update index whose binary32 accumulated
delta exceeds start+delay. Wall time follows only after the actual delivered
delta rate is qualified. At continuous unscaled frame-seconds delivery,
defaults imply approximately 6 engine seconds per fresh path plus update
overshoot, not 6 UT seconds or 6 VM ticks. At fixed delta 1, completion is update 7;
at binary32 delta 1/60 a finite calculation establishes the exact crossing.
Neither this overshoot nor a nominal 60 fps assumption bounds queue delay.

With both legs detached, default thresholds, movement/wall rate 1 and the
nominal 12-second two-leg contribution, the corresponding phase-only examples
are **(69.60,92.64] s at calendar 15** and **(184.80,253.92] s at calendar 5**,
before movement overshoot/rounding, Q and F. The high-end nominal values are
about **1 min 33 s** and **4 min 14 s**. These are usable conditional budgets for
uninterrupted background operation, not claims that all such trips fall in
those ranges. At prompt boundary delivery, only the first wait retains an
arbitrary phase within a consecutive load/depart timer pair, but each flight
creates a new arrival/load-arm phase. The four phases are therefore not four
independent uniformly distributed errors. Any real queue slack must be treated
separately.

An additional **ideal steady-cycle calculation** accounts for that coupling.
Let `u=86.4/T` wall seconds/tick, prompt handlers at integer deadlines, each
flight exactly M wall seconds, one fresh path/leg, no other delays or clock
precision loss. Departure at integer k reaches the next arrival at `k+M/u`;
its load/depart deadlines yield the next departure at `k+floor(M/u)+5+2`.
Consequently the steady two-leg period is `R=2*(7+floor(M/u))*u`.
For M = 6 this is **92.16 s at T = 15** and **241.92 s at T = 5**. Flight still takes time:
its fractional-tick part can be absorbed by the next dock timer's arm phase.
These are more specific ideal predictions, not evidence that transit is free
or an observed tolerance. Starting an initial arrival exactly at tick 0 instead
gives first-cycle 92.40/247.92 s before that steady phase is reached. The aid
checks the explicit event recurrence against the steady expression. Different
M, frames, VM latency, clock precision and rate changes can change the result.

The [finite calculation aid](../../../../research/c2-transit/README.md) keeps
these assumptions explicit. Its conditional examples must not be presented
as observed retail round trips. For full-flight legs, replace the detached
term with durations from the actual geometry/profile/action state. With no
fuel or scheduling upper bound, a finite guaranteed upper limit is unsupported.

What prevents a calibrated estimate is specific: per-ship controller history,
actual delivered clock/admission sequence, effective movement profile/override,
actual path/action durations, timer arm phases/cached G and bounded dispatch
latency. Save52 inventories and target links do not encode those observations.
More inventory-only mature saves would not resolve the missing execution history.
No live work is implicitly authorized by documenting that boundary.
