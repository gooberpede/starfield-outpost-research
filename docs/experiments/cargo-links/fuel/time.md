# Elapsed production and one-shot freight timing

[Answer](report.md), [native fuel](native.md), [stages](stages.md).
These worked cases are conditional arithmetic from installed source operands,
not measured gameplay or a fuel simulator. [C2 clock](../transport/timing.md),
[C2 movement continuation](../transport/transit.md),
[E1 elapsed rules](../../inorganic-extractors/arithmetic-clocks.md) and
[S2 insertion rules](../../local-output-links/traces.md) remain the baselines.

## Separate authorities

Ship source defaults are load 30, takeoff 15 and fuel retry 30 seconds. Shipped
InitializeTimers converts once using initialized ground setting G:

```
H = f32(f32(sourceSeconds / 3600) * G)
N = trunc_i64(f32(max(H, 0.03333333507180214) * 41.66666793823242))
deadline = low32(current_game_tick + N)
current_game_tick = low32(trunc_i64(f32(DaysPassed * 1000)))
```

With installed G = 15, load/retry are 5 ticks and takeoff is 2 ticks. Each tick
is .001 game day, or 86.4 UT seconds. Ground calendar progression at current
T = 15 makes their ideal tick-boundary equivalents 28.8 and 11.52 wall seconds;
phase, frame/VM admission and package work add uncertainty. Space T = 5 triples
those wall equivalents without necessarily resampling cached G. Neither clock
defines a five-unit fuel cost per trip.

Native `141fb3710` suppresses the game-time heap while player +dd4 denotes
waiting/sleeping. `1420f9f90` pops each due one-shot before queueing the VM event;
`1420fb880` rearms from **now**, replacing the same bound-script/ID entry.
There is no callback loop over missed freight cycles. A disabled ship's handler
returns without rearming. Explicit timer pause and VM/script binding failures
are additional conditions, separate from waiting and from graphic unloading.

Producer updates instead receive engine elapsed from frame `1417cab70`, wait
`141a38ba0` or travel `141a27d80`. For the traced wait chunk, setting 900 and
current calendar divisor T give `elapsed = f32((900 / T) * L)`, where L is the
bounded body local/UT factor. For T = 15 and L = 1 this is 60 scheduler seconds
and 900 UT seconds of calendar advance. The wait cleanup tail contains no final
production/calendar update; actual chunk count depends on the caller's budget.
The examples specify executed chunks and do not infer an exact count from the
menu's displayed hours.

For each resolved eligible producer row with interval I and countdown R:
elapsed >= positive I uses `trunc(elapsed / I)` without first subtracting R;
otherwise subtract elapsed from R and make one cycle due if R becomes nonpositive.
A due update resets both R and I to the current effective interval, dropping
overshoot. Registration iterations and recipe/capacity conditions still apply.
Thus continuous rate × skipped hours is not the exact native production rule.

## Case 1: net supply buildup while freight is suppressed

Assume 20 actual wait chunks, each elapsed 60, T = 15 and L = 1; valid registered
and resolvable objects; no interval modifiers; ten He-3 extractors each I = 36,
quantity 1; one connected fueled pad I = 108 and initial R = 108. He-3 starts at
zero. All extractor updates precede that pad's update in each chunk. The other
pad has no eligible fuel supply. Ten independent freight producers also each
make one compatible unit per chunk into an initially empty outgoing store.
This is an illustrative network, not a claim about Save52's installed topology.

Each He-3 extractor's large-elapsed branch requests `trunc(60 / 36) = 1`, so the
ten supply 10 per chunk, or 200 total. The pad's first chunk changes R to 48;
the second makes one fuel cycle due, consumes 5 and resets R to 108. This repeats
every two chunks: ten accepted fuel cycles consume 50, leaving **150 He-3**.
At chunk 1 stock is 10 with no debit; chunk 2 stock is 15 after the first debit.
The ground calendar advances 18,000 UT seconds across the 20 declared chunks.

The declared freight producers request 200 units in total. If the effective
outgoing/store/hold access allows that mass, it can accumulate locally; no missed
voyage drains it while the freight heap is suppressed. If there is only 75 mass
units of effective downstream capacity and unit mass 1, single-unit insertion
fills at 75 and later otherwise eligible production can stop for lack of space.
Remote manufacturing depending on that freight can then starve **if** it exhausts
its existing inputs and has no other supply. Neither starvation nor buildup is
a universal observed outcome.

If timer 0 was due before the jump, resumption can deliver one load event. At
hypothetical tick 1100 it arms timer 1 for 1102, not one departure for every
five ticks missed. If timer 2 was due instead, it repeats unload/query and arms
timer 0 for 1105 when either pad now qualifies. Native flight/package completion
then remains necessary. No number of completed round trips follows from 200
produced units or from 20 elapsed chunks.

## Case 2: fuel exhaustion and partial unload during an overdue retry

Assume a linked pad has I = 108, R = 30, quantity 1 and 12 accessible He-3 units,
no replenishment or concurrency, no other ready endpoint, and a single elapsed
production call of 360 scheduler seconds. The large branch requests
`trunc(360 / 108) = 3`; the one-cycle eligibility check passes, then the removal
cap accepts `min(3, floor(12 / 5)) = 2`. It withdraws **10**, leaves **2**, and
resets the producer timer. The third requested cycle is not a recoverable fuel
debt. With prior uncharged state, successful work sets charged even though stock
is now below five. A mode-0 ship poll can therefore pass at this point.

If the next due producer update runs first with stock still 2, mode 1 yields
reason 7, withdraws nothing and changes charged to uncharged. A subsequent ship
retry then fails. This ordering distinction is why a saved low count is not a
readiness oracle. The example demonstrates two permissible interleavings rather
than promising one actual wait-loop resource order.

Independently suppose the waiting shared hold retains 20 units of freight,
current incoming has effective capacity 100 and mass 95, unit mass 1, and local
redistribution cannot free space. On the first timer-2 callback, it unloads 5,
leaves 15 aboard and, if neither pad is ready, rearms timer 2 from that callback's
current epoch. If manufacturing later frees 10 mass units, the next retry can
unload another 10, leaving 5 aboard. No fuel is charged by either retry itself.
Supply appearing at the opposite pad can admit loading/reverse travel on that
second callback even if the ship's physical endpoint remains unfueled.

## Capacity and lifecycle qualifications

Production chooses one currently nonfull eligible destination or its own buffer.
It can insert a whole batch across nominal capacity: C = 75, W = 74.5, item mass
.5 and due count 3 can produce W = 76. It does not universally split the batch.
Existing-stock redistribution instead plans item-specific floor-fit quantities,
retaining refused stock upstream. Its multi-item plans do not reserve aggregate
weight, so the simple saturation example requires its declared single-item,
single-unit conditions. No periodic local conveyor is inferred from elapsed
time; direct production delivery and explicit redistribution triggers differ.

Ordinary distant gameplay can run both registered producer updates and bound
script/AI work. Graphic unload is not failed handle resolution, VM unbinding or
AI package completion. Missing Workshop/producer handles affect elapsed work;
missing ship/bay bindings affect freight separately. Fast travel has an explicit
elapsed/calendar caller, but its input conversion and ordering with movement/VM
dispatch do not establish the same suppression window as wait/sleep. No universal
fast-travel freight catch-up or stall is claimed.

Reload restores reference inventories, local edges, producer rows and saved
charge/base-AV channels; current eligibility and native handles are reconstructed.
C2 positively traces native timer save/load as remaining time, ID, serialized
bound-script handle and pause bookkeeping, rebuilt against the current clock.
VM RequiresFuel, cached G/waits and initialization state are distinct persisted
script channels; this investigation does not decode their particular Save52
instances. Ship hold, direction and native Travel/FlyLand saved subsets differ
from current path/process/graphics. No last-visited timestamp, replay of all
missed voyages or restoration of current fuel-ready truth is inferred.
