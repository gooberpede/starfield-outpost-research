# Production clocks and elapsed scheduling

[Report](arithmetic-report.md), [production operands](arithmetic-production.md).
All native addresses are preferred static VAs in the pinned retail build;
object offsets are hexadecimal. `aNN` means the local arithmetic export NN.
This is a path-specific clock contract, not a measured timing experiment.

## Frame elapsed, calendar progression and skipped time differ

The ordinary scheduler input is XMM1 at `140f7ef20`. Its traversal snapshots
registered Workshop handles at `145916528/530`, resolves ExtraBC, gets ExtraE2
and passes the same scalar to each resource producer-row updater. It does not
derive elapsed time from a planet's displayed local clock. It also does not
enumerate all saves or prove every unloaded object resolves.

| Path | Native producer and conversion | Scope / implication |
|---|---|---|
| Frame update | `1417cbbe0` → `1417cab70` reads binary32 `145fbf9a8` immediately before calling `140f7ef20` (`a02`, `a14`, `a17`). | Engine frame seconds, with its own scaling, smoothing, clamping and freeze behavior; not necessarily raw wall-clock seconds. |
| Frame clock source | `141887c90` reads QueryPerformanceCounter, subtracts the initialized origin, converts ticks to integer milliseconds with `×1000/frequency`, then calls `1422cce10` with context `145fbf990` (`a14`–`a17`). | The context's +18 is exactly global `145fbf9a8`. The QPC origin/frequency initializer is `1402036f0`. |
| Wait/sleep loop | `141a38ba0` reads `iSecondsToSleepPerUpdate` (default 900) and divides by calendar scale at calendar+38/global+48; local/UT conversion factor is then applied. XMM7 supplies elapsed to `140f7ef20` at `141a3901d..21` (`a02`, `a23`). | Explicit skipped-time updates, rather than waiting for the corresponding real duration. Calendar scale and local-day conversion must be accounted for. |
| Travel/skip caller | `141a27d80` forms XMM6 from its input+7c divided by a selected scalar times `fFastTravelSpeedMult`, advances the calendar and passes XMM6 at `141a281c9..cd` (`a02`, `a23`). | Separate caller-supplied conversion; no universal equivalence to frame or wait timing is claimed. Exact input+7c producer remains conditional. |
| Calendar advance | `1418778e0` computes `GameHour += elapsed × calendarScale / 3600`; carries whole days/month/year and updates days-passed state (`a04`, `a25`). | Calendar progression is a consumer of an elapsed value with a separate scale, rather than proof the extraction interval itself is UT seconds. |

The frame-clock helper `1422cce10` first handles a nonzero nested freeze counter
by zeroing the output seconds and storing a timestamp. Otherwise its normal
wall-clock branch limits an elapsed millisecond interval to `0xa6` (166 ms),
converts with binary32 .001 and optionally smooths a ring of at least three
samples by discarding maximum/minimum and averaging the remainder. A nonzero
override input follows another branch with fractional millisecond carry.
It multiplies the result by `1458d58f4`, then stores context+18 and retains
unscaled seconds separately at +1c. `1422ccd40` can change that scale while
rescaling the current frame value. Do not confuse this frame scale with the
calendar's scale pointer. Paused/frozen engines, fixed-time overrides and
ordinary open-menu behavior are not interchangeable; this assignment does not
claim every menu activates the same counter.

`1422cd140`/`1422cd0c0` nest freeze/resume timing and adjust QPC-derived timing
origins. The frame loop's `1417cc1d0` schedules callback `1417cbbe0` through its
task/dependency machinery; one callback address is not a complete threading,
load or pause policy. All these functions are observed internal operations,
not safe APIs, and none was invoked.

## Local day and the wait conversion

`141a38ba0` asks `140839820` with the current body identifier; that wrapper's
`140839900` reads the selected body data scalar at +d4. For a nonzero absolute
scalar the latter returns `24 / abs(scalar)` when its Boolean argument is false;
the fallback is 24. The raw body-field physical interpretation beyond that
conversion is not assigned from the offset alone (`a18`/`a19`).
The wait caller bounds the returned day-hours quantity by
`24 × fMaxUTHourPerLocalHour`, clamps its lower end to zero and divides by 24.
The named setting is bound by initializer `14012a8d0` (`a19`). Let the resulting
dimensionless factor be L and the current calendar scale be T. The traced
900-setting branch supplies elapsed `binary32((900 / T) × L)` and advances
calendar time using the same elapsed scalar. Its skipped local seconds budget
also scales by L. When the remaining budget does not exceed the next chunk
threshold, the caller takes tail `141a38840`. Its complete instructions in `a08`
clear player+dd4, perform cleanup/events and contain no further calendar or
production elapsed call. Its decompilation failed, but that does not hide the
instruction-backed tail behavior. Initialization/other callers can already
have advanced time; do not derive a universal total wait-cycle count from the
main loop alone.

Conceptual precision test: **if** a local day is approximately 49 UT hours,
one local hour is approximately 49/24 UT hours. That conversion belongs to
local display/wait selection. It does not turn a 36-second extractor interval
into 36 local seconds or establish 49 hours of actual wall-clock waiting.
For a hypothetical T=20, a UT-hour advance corresponds arithmetically to
180 engine elapsed seconds before caller-specific factors and update policy.
No actual Jemison body period, current scale override or production count was
sampled here. The ESM `TimeScale` default (GLOB 00003a, FLTV 20) is definition
evidence, not a runtime observation. The direct binding of calendar+38 to that
GLOB is not established by the traced initializer/lookup routes; the conversion
contract uses the actual scalar read from that slot. `a25` also distinguishes a
native missing-TimeScale fallback of 30 from the installed ESM value of 20,
and `a26` observes writes to GLOB 00003a from other setting sources. Neither
value can be silently substituted for the current calendar divisor.

## Countdown, catch-up and reset

`140f7f1e0` (`a01`, repeated `a14`/`a23`/`a25`) consumes rows of stride 1c:
handle+00, base ID+04, integer pending bookkeeping+08, integer registration
quantity/iteration count+0c, binary32 remaining+10, interval+14 and cached
eligibility+18. R14 in its body points to row+08. This distinction avoids the
older decompiler's erroneous integer interpretations of float stores.

1. With elapsed at least a positive interval, it divides elapsed by interval,
   calls `truncf` through import `143a40540`, converts to signed integer with
   VCVTTSS2SI and tests the low count. **This branch does not subtract the saved
   remaining countdown first.**
2. Otherwise it subtracts elapsed from remaining using VSUBSS. A nonpositive
   result makes one cycle due; a positive result retains the fractional
   countdown until the next update.
3. For a resolved producer, it obtains the positive effective interval multiplier,
   loops the integer registration quantity, rechecks current reason in mode 1
   and only calls creation when reason is zero. Nonzero reasons have separate
   bookkeeping/state branches. No universal “eligible always produces” rule.
4. After the due branch it resolves the base, recomputes the timer (or nominal
   fallback), multiplies by the retained multiplier and resets **both** remaining
   and interval. A reason failure does not itself preserve a due-time debt for
   later realization. A failed handle instead marks the sentinel and adds
   integer due×iteration bookkeeping; no universal replay of that counter is
   established.

Illustrations of the actual branch contract: with interval 36 and remaining 5,
elapsed 10 makes one cycle due then resets to the full current interval, dropping
the five-second overshoot. With those same prior fields and elapsed 50, the
large-elapsed branch yields trunc(50/36)=1, ignoring the earlier countdown;
it does not yield the two cycles a continuous phase-preserving model could.
These are operation-derived examples, not a replacement simulation or observed
retail counts. Repeated batching can change effective realized cadence.

There is no demonstrated universal cycle cap in this branch. Float division,
integer conversion and 32-bit multiplication/addition have finite machine
domains; NaN/infinity/out-of-range conversions and overflow must not be
relabeled a safe clamp. A zero/nonpositive interval goes through the smaller
elapsed/countdown path, whereas the nominal UI rate helper returns zero for
interval zero. This is another counterexample to equating UI rate and output.

## Loaded, unloaded and persistence limits

The producer registry traversal is global among its registered, resolvable
Workshop handles; no nearby-terrain query controls the elapsed scalar in this
path. Normal frame callbacks and explicit skipped-time calls both reach it.
Accordingly, “production only catches up on load” is not a description of these
traced mechanisms. Conversely, a global registry does not prove continuous
simulation of all unloaded references, complete restoration or fresh power and
modifier state. Exact failed-handle, residency, initialization and callback
coverage remain conditional.

Producer rows have the existing saver/loader evidence; their saved countdown is
historical state, not guaranteed current authority after load. This assignment
does not establish a separate last-visited timestamp or a universal on-load
catch-up algorithm. No new save was decoded/restored, no original overwritten
and no actual output measured. These are justified coverage limits, distinct
from the established native arithmetic and caller conversions above.
