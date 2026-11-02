# D5AE native scheduler causality

**Ordinary demand is ordered locally by task readiness, service state and queue
operations. There is no single global registration-to-construction FIFO.**
[Source locators](d5ae-sources.csv) pin exact function windows and hashes.
All VAs are preferred static addresses for build 1.16.244.0, base `0x140000000`.

## Producer to provider

| From → to | Edge label | Native rule and scope |
|---|---|---|
| Travel confirmation → pending player payload | CONDITIONAL | `0x1416d3c20` accepts response zero; admitted destination routes call `0x141a67830`, swapping payload into player `+0xa08`. This slot is not a proved FIFO. |
| Pending payload → context/focus | PROGRAM-ORDER / CONDITIONAL | `0x141a20380` consumes it under loading/state gates, calls context processor; exterior `0x141a278a0` writes focus-valid and calls `0x14099f2c0` before its final `0x141a25420`. A pre-placement demand opportunity follows, not a completed worker or visual-arrival clock. |
| Focus → bounded region | CONDITIONAL | RuntimeService `+0x48/+0x70` callbacks, `0x1407b3c50 → 0x1407b4750 → 0x1407b2390`, require context/mode/owner/focus admission. `0x1407b30c0` supplies discriminator/bounds. |
| Region → preparation | PROGRAM-ORDER / CONDITIONAL | `0x1407b3aa0/0x1407b2880 → 0x14079c900 → 0x1407af790/0x14079ce00`; warm keys merge. `0x1407b1460` runs ContentManager preparation; its destructor `0x1407b19f0` releases its manager reader before follow-ups. |
| Preparation → coordinate registration | CONDITIONAL | `0x1407afd70 → 0x1407b1420 → 0x14079d080 → 0x1407af970`; discriminator validation rejects stale work. Rectangle X ascends and Y descends. Final parent waits do not delay all newly ready density jobs until enumeration ends. |
| Coordinate → layer/density tasks | PROGRAM-ORDER / CONDITIONAL | `0x1403625e0 → 0x1407b5a00 → 0x1407b4bb0`; neighbor registration order is `(-1,+1),(-1,0),(0,+1),(+1,+1)`. Bounded coordinate recursion and DB key deduplication apply. |
| Density inputs → runnable node | CONDITIONAL | `0x1407a1260` captures original Int2/discriminator/files; `0x14076cd40` selects dependency-bearing registration or ready mode-2 work. Task/dependency state, not input-array order alone, controls activation. |
| Registration → dispatch | CONDITIONAL | `0x1427e5630 → 0x1427eaf50 → 0x1427ec100 → 0x1427e6a00 → 0x1427e56d0`. Registration callback requires node `+0x94 == 0`, marks it registered, and dispatches only state `+0xa8 == 2`, scheduling rank `+0x80 == 0` and `!(node+0xa9 && server+0x78)`; otherwise pending storage is used. No speculative semantic name is assigned to the last predicate. |
| Mode-2 node → worker queue | CONDITIONAL | `0x1427e56d0 → 0x1427eb6b0`. Matching worker TLS invokes import `0x1428d3960(true,false)`, publishes new callback with `0x1428d2b80`, then requeues imported old work. External publication uses the shared queue/lock. |
| Queue → claim | CONDITIONAL | `0x1428d3960` uses owner-back, peer-front CAS and context scan, optional own-front and shared external-front branches. Worker context stride is `0xc0`, pool cursor `+0xf0`; actual contents/cursor/availability matter. |
| Claim → execution | PROGRAM-ORDER / CONDITIONAL | `0x1428d3b90` installs TLS, calls claim at `0x1428d3d16`, removes callback tag and invokes `+0x08` at `0x1428d3d38`. Matching TLS plus one-worker pool permits inline `0x1427e5880`; absent usable scope can invoke node virtual `+0x10` directly. |
| Density/layer → provider | CONDITIONAL | Density worker `0x14076c560 → 0x1407a1940` calls at `0x1407a1a3c`; layer `0x1407b5160` calls at `0x1407b526a`. Existing density aggregate bypasses provider. Layer holds a manager reader; detached density does not inherit its preparation reader. |
| Provider → target arbitration | PROGRAM-ORDER / CONDITIONAL | `0x14079f860` retains Grid, selects contributors and reads source BIOM/fields before ProcGen protection. It checks visited under shared protection, then does exclusive pointer-map lookup/insertion/generation/store. Grid retention alone does not freeze source lifetime. See [winner model](d5ae-winner-model.md). |
| B2 target checks → miss/store → hit | OBSERVED QPC | Recorded checks 8006/8020 precede protected miss 8091, sample/store and hit 8339. No upstream registration/claim clock was captured. |
| Worker claim → competing lock acquisition time | UNRESOLVED historically | B2 supplies no OS scheduling trace, acquisition timestamp or wait interval. Actual protected outcomes determine the observed winner without those invented values. |

## Service ownership and priority

ProcGen and ContentManager JobSites use getter `0x1428d1880`, returning
`[0x1461fabe8]+0x140`. Service tag 1 therefore does not identify another pool.
Wake `0x1428d96c0` marks wake-pending and publishes a pump only if running/queued
was absent. Pump `0x1428d9560 → 0x1428d89b0` executes receiver and commands.
Waking an already-running site does not authorize a second simultaneous pump.

Worker entry's pool `+0xe4 == 2` branch calls `SetThreadPriorityBoost` with
disable set at `0x1428d3bcf`; it is not a request-specific `SetThreadPriority`.
The inspected dispatch/claim path uses task mode, TLS/pool/context state and
queues, with no geographic-coordinate or mask priority operand. This is a
bounded path argument, not a claim that OS priorities or unrelated jobs never
affect execution. Pool occupancy and OS progress remain runtime inputs.

## Alternative producers and coverage boundary

Single-cell preparation `0x140aed020`, reached from `0x140bbb170/0x140afb220`,
uses the cell Int2 and real context/placement guards. Bounded LOD ingress
`0x141429880 → 0x140364280/0x1403643e0` reaches grouped-cell work and a 3×3
neighborhood. StarMap CacheHandles and ordinary focus/frame updates can also
supply locality demand. They may merge warm keys or compete when admitted.
No fixed source-anchor query follows from any of them.

The provider's inspected ordinary callsites are the density and layer calls
above. Its data reference is not automatically a third producer. Terrain
height/file/material jobs have separate callbacks and readiness and can occupy
shared infrastructure; they are not silently given density's import/requeue
rule. The existing [D5W branch investigation](d5w-normal-path-model.md)
qualifies their producers and why resident prerequisites can complete before
either paired continuation. Arbitrary indirect/injected callers and other builds
are outside this ordinary receiver graph.

## Dependency completion and effective ordering

Node `+0x90` counts outstanding prerequisites; node `+0x80` is scheduling rank.
They are not interchangeable. Common constructor `0x1403623f0` installs rank,
zero count, state `+0xa8` and flags `+0xa9/+0xaa`. Ready density construction
at `0x14076cfef` supplies state 2, rank zero and both flags zero. Ordinary layer
constructor `0x1407b58a0` also supplies rank zero. Pending-input branches create
state-zero nodes, add actual dependency handles and commit them separately.

AddDependency `0x1403623b0 → 0x1427e6f40` requires dependent state zero and a
prerequisite below state 5. Newly inserted forward/reverse edges increase the
dependent count `+0x90` and prerequisite reference count `+0x94`. Duplicate
edges do not increase those counts again. Commit `0x1403623a0 → 0x1427e70e0`
changes state zero to one; a zero dependency count invokes `0x1427e6830`.
This evaluates node virtual `+0x08`: result 2 queues ready work, result 4 records
state 4, and result 5 normally completes/removes the node. The qualified
`+0xa9/server+0x78` branch defers completion through `+0xab` instead.

Completion `0x1427e5a00` publishes a TargetBatchPage command; callback
`0x1427eecf0 → 0x1427e5e80` removes dependency edges. Category-zero removal
decrements `+0x90` at `0x1427e61a4`; the last dependency on state 1/2 evaluates
node virtual `+0x08` at `0x1427e61c6` and applies the same status distinctions.
Category one instead releases prerequisite references and can cancel a
not-yet-executing unneeded node. A decrement itself is not worker publication.
The ready scan `0x1427e6d10` subsequently calls `0x1427e6a00 → 0x1427e56d0`.
Dispatcher status 3 can retain readiness, 4 denotes dispatched/pending execution,
5 completes and 7 invokes its separate cancellation/edge-release path.

Ready insertion `0x1427e4950` assigns a monotonically increasing insertion serial
to node `+0x88` and stores `(rank, serial)` in the ready tree. Native bound
helpers `0x1406dd4f0/0x1406db950` compare unsigned 32-bit rank first and unsigned
64-bit serial second. Leftmost/in-order scan therefore considers lower ranks
first and equal ranks by insertion serial at this tree, subject to scan/state
gates. It is not a global worker FIFO or final source-lock order. The separate
ready rank-zero immediate-registration route can dispatch without that scan.

Dependency priority can lower a not-yet-running prerequisite's rank. Helper
`0x1427e6b90` notifies node virtual `+0x18`, rekeys ready work through
`0x1427e49a0`, propagates edge-rank changes and writes the new rank. Rekeying
preserves insertion serial. Both ordinary density/layer virtual `+0x18` slots
bind to the no-op `0x1402b56d0`; they do not add a geographic priority callback.
Effective rank and later priority commands remain scheduler inputs; constructor
rank zero is not claimed immutable for every generic server client.


Rank propagation is a real deferred command chain:
`0x1427e6330 → 0x1427eecc0 → 0x1427edc20 → 0x1427e7180 → 0x1427e6b90`.
The target updater returns for missing targets or state at least 3. With one
reference it changes a differing rank; with multiple references it accepts a
lower rank and raises rank only when remaining reverse dependencies do not
require a smaller value. It updates forward/reverse rank records and drains
follow-ups. The apparent extra caller at `0x1427e7708` is inside this same
updater, not an independent external writer.

A separate Reschedule command wrapper `0x140422e10` does reach that updater.
Its inspected producers are bulk server reprioritization `0x142426790`,
explicit-server/key request `0x140d25a30`, resource request `0x1424250d0` and
synchronous wait promotion `0x14041f4b0`. The last two use server
`[0x1461fab80]+0x10`, rather than the explicit ProcGen server expression
`[0x145fd9c38]+0x40`; they must not be silently treated as density dispatch.
Generic server operations remain conditional rank inputs if their receiver is
bound to the relevant server. They do not compare geographic coordinates or
sampled masks. The ordinary paired prefix keeps effective resource ranks fixed;
it does not require a claim that no other server client can reprioritize work.


The final targeted caller check follows the generic rank wrappers rather than
assuming their binding. Export11 shows both `0x140d13b80` and `0x140d14f40`
supply `[0x1461fab80]+0x10` to `0x140d25a30`; they request current rank plus one
under their retry predicates. `0x142425540` publishes the range command to that
same server, via `0x1424266f0`. Thus all inspected external Reschedule producers
have explicit non-geographic server/key/rank operands. Different global/offset
expressions alone are not offered as universal runtime non-alias proof. The
causal model accepts effective rank changes conditionally; it does not infer a
hidden coordinate priority or enumerate every arbitrary indirect client.
