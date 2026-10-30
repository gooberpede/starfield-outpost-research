# D5W ordinary paths and conditional ordering

This model tests the [frozen questions](../../implementation-briefs/CODEX_BRIEF_SOR_RG2_D5W_normal_resource_generation_operational_contract.md).
[Report](d5w-report.md), [active ledger](d5w-investigation-ledger.md),
[exact native source ranges](d5w-sources.csv) and
[paired paths](d5w/critical-paths.svg) retain the evidence boundary.
All addresses are preferred static VAs for the freshly verified Starfield
1.16.244.0 EXE, image base `0x140000000`. Member offsets are bytes. These are
research aliases and compiled possibilities, not retail event timestamps.

## State contract and what is being compared

The primary source is `0:37536:20928:0029d20e`, body `0x0005e0de`, system
86469, body index 5, chart 0, BIOM `0x00145440`. D5S's normalized arrival
installs descriptor `(37536,20928)` and native manager centre cell `(0,0)`.
Consequently source anchor `(0,0)` is an actual coincidence in this specified
descriptor frame. The saved outpost centre is separately
`(81.19074249267578,90.27748107910156,5.303274154663086)`; it is not the
descriptor origin or the first construction query.

Use ordinary mode 2, initialized owner/component, fixed effective main-file
definitions/settings, source Grid and geographic raster, successful allocations
and copies, stable discriminator and valid source lifetime during construction.
Default terrain width 100, nominal source dimension 10, padding 2, LOD base
dimension 1 and streaming margin 2 are D5S inputs, not newly measured runtime
configuration. Its ordinary Grid is width 200 with initial origin `(-100,-100)`.
The worker pool is started and has at least three workers; fixture controls use
five. Queue capacity can be warm while target source/request state is cold.

Cold here means target-relevant coordinate/layer/density entries, visited entry
and pointer-map population have not already settled the target. Metadata,
definitions, files and worker infrastructure may already be resident. With warm
keys, existing handles merge work. With a populated density aggregate, later
levels skip the provider. With a visited hit or pointer-map hit, there may be
no new constructor to schedule. These states cannot be treated as fresh trials.

## Ordinary initialization and ingress

| Stage | Native edge and evidence | Ordering scope |
|---|---|---|
| Context installation | `0x14078af30 → 0x14078b030 → 0x14078bc30`; manager reader/exclusive ownership, owner and descriptor setup; D5S/V exports. | Prior work drains before the protected installation. This is not a source-coordinate priority rule. |
| Source index | `0x1407847b0` constructs ordinary/overlay Grids and MultiFiles Grid; `0x140785190` completes them. Terrain reset `0x1409a7950` clears focus-valid. | Source descriptors can exist before generated resources. Grid readiness is not populated source output. |
| Focus and prewarm | `0x14099f230/0x14099f280` write focus then invoke `0x14099f2c0`. RuntimeService slots `+0x48/+0x70` reach AcquireHandles through `0x1407b3c50 → 0x1407b4750 → 0x1407b2390`. | A valid focus enables prewarm; focus-invalid initialization suppresses it. Independent queued service work can run after the focus write while the setter continues other terrain work. |
| Real bounds | `0x1407b30c0` derives the global region/discriminator. `0x1407b2390` floors focus, aligns its block rectangle and calls `0x1407b3aa0/0x1407b2880`. | With D5S defaults/focus zero, inclusive bounds are `[-16,23]²`. This is demand locality, not a source-specific canonical sample. |
| Detached region | `0x14079c900 → 0x1407af790/0x14079ce00 → 0x1407b1460 → 0x1418aa1c0`; continuation `0x1407afd70 → 0x1407b1420 → 0x14079d080 → 0x1407af970`. | Preparation owns a real manager reader. Its destructor runs before follow-up activation; work tracking does not transfer that reader to every density descendant. |
| Cell preparation | `0x140bbb170` calls `0x140aed020` at `0x140bbc380`; `0x140afb220` calls it at `0x140afb6ed`. The cell's original Int2 at `+0x58` is passed as both endpoints at `0x140aed393`. | Exterior/state/owner and placement preparation gates apply. It requests that cell, not an outpost-wide canonical source coordinate. The fixed CellLoad tree is a predecessor, not discarded as empty. |
| Bounded LOD dependencies | `0x141429880` derives a rectangle around current/fallback grid coordinates; `0x140364280 → 0x1403643e0` registers grouped-cell tasks; tables `0x144b00e80/0x144b00f20` reach `0x140365be0/0x140365c90 → 0x140365780 → 0x1403635f0 → 0x140363b80 → 0x140360120`. | Each admitted new bounded cell acquires a real 3×3 neighborhood before registering its dependent continuation. Warm DB entries can reuse. Nonnegative class/state gates, class bits and terrain classification matter. This is another locality policy, not a one-source/one-query guarantee. |

The fixed CellLoad predecessor has one PCMT, 108 branch nodes, 525 content
nodes, 38 referenced CNDFs and eleven concrete condition callbacks under the
[D5S/D5H proof](d5s-query-winner-model.md). Handler 865 reads DensityMapDB
files; it does not consume BaseProcGen's generated source geometry. A null
temporary context or cold-cell shortcut cannot be assumed: D5S preserved those
rejected models and qualified temporary-reference creation and resident metadata.

### Released terrain and bounded-LOD branches

D5W independently followed the setter's ordinary terrain cascade rather than
retaining D5S's scheduling barrier as an account of typical arrival. The concrete
terrain `+0xe8` holder is constructed by `0x140992ab0` around the MultiFiles Grid
installed by `0x1407847b0`, table `0x144b3e0b8`. Height interfaces `+0xc0/+0xd8`
bind to `0x1407836f0/0x140783600`. The first reads the resident per-block min/max
through `0x140782690 → 0x1407824b0`; the second reaches height-window acquisition
`0x140782910 → 0x140783480 → 0x140783080 → 0x140998fc0`.

`0x1409ac2d0` can invoke this window work synchronously or submit it through
`0x1409af3d0` to pool `+0x140`, transferring a manager reader. The worker
`0x1409ac5e0` finishes its height operation before decrementing outstanding work;
`0x1409b0570` releases the reader afterward. Separate min/max worker
`0x1409a2380` is dispatched on pool `+0x40`; material worker `0x1409a89e0`
resolves grass asset paths through `0x140626a90`. Density's pre-import rotation
must not be transferred to these distinct dispatchers.

Height-window acquisition reaches TerrainDB request `0x140993110` and explicit
file/block readiness. Constructors `0x140991db0/0x140995630` install PageStitch
and PageTransform tables `0x144b684f8/0x144b68488`; worker slots `+0x10` bind
to `0x140992110/0x140992330`. These test entry/dependency state, stitch/transform
height storage and publish completion by state change/wake. Their virtual block
decoder/stitch operations are not decoded exhaustively here. Under the declared
resident file/height prerequisites, cold block decoding is not an initiating
resource demand or mandatory earlier target constructor in the paired prefix.
Outside that contract its latency and shared-pool occupancy remain unknown;
this is not a blanket assertion that every cold TerrainDB path has no resource
side effect. The question answered here does not require such a whole-engine
negative or a retail latency model.

The bounded-LOD ingress was also followed upward. `0x1405876d0` queues the real
StarMap CacheHandles command `0x14058ccf0 → 0x14058d470`, whose enable/context
gates precede `0x141429880`. The other caller `0x141424ec0` is part of
`0x141422810`, called by `0x14141bc70`; it gathers current/fallback grid-centre
dependencies before registering further mode-2 work. Generic worker
`0x1403e0080` derives a rectangle and four class-admission bits from its LOD
object, calls manager-reader wrapper `0x140364980` and retains returned handles.
These are real additional locality demands. Their local dependencies do not
designate a source anchor as the authoritative raster query. No ordering from
them to a mandatory earlier target miss is established for D5S's normalized
prefix; they can compete when admitted. Their retail admission times cannot be
recovered by treating the controlled density-token batches as engine timings.

## Dependencies, services and claims

`0x1403625e0` requests a coordinate entry; its new-entry branch calls
`0x1407b5a00`, then `0x1407b4bb0`. For root `(x,y)`, density neighbors are
`(x−1,y+1)`, `(x−1,y)`, `(x,y+1)`, `(x+1,y+1)`, in that registration order.
The corresponding coordinate recursion occurs only inside real region bounds.
The rectangle enumerates X ascending and Y descending. This deterministically
expands roots; it does not order all worker completions.

Layer registration includes preparation, file and density dependencies. Density
acquisition `0x1407a1260` captures the original Int2, discriminator and file
handles through `0x1407a8d30`. Registrar `0x14076cd40` chooses a dependency node
when handles are pending; with no pending dependencies it creates ready mode-2
work. Registration `0x1427e5630 → 0x1427eaf50 → 0x1427ec100 → 0x1427e6a00`
can activate that work while later roots are still being registered. The final
parent handle wait is not a barrier before every density job.

| Mechanism | Proved rule | Unproved extension |
|---|---|---|
| JobSite wake | `0x1428d96c0` publishes when running/queued is absent; wake-pending does not create a second pump while running. Actual pump `0x1428d9560 → 0x1428d89b0` executes receiver and queued commands. | No common FIFO ordering between different JobSites or their receiver/command work. |
| Service routing | ProcGen and ContentManager use getter `0x1428d1880`, returning `[0x1461fabe8]+0x140`. Service tag 1 is not another worker pool. | No source-mask priority follows from service tags. |
| Density dispatcher | `0x1427e56d0` sends ready mode-2 nodes to `0x1427eb6b0`. Worker-local dispatch imports with `0x1428d3960(true,false)`, publishes new work and requeues imported old work. | Plain registration FIFO or plain LIFO gives the wrong late-batch extrema. |
| Claims | `0x1428d3960`: owner-back, peer-front, external-queue and peer-scan branches; `0x1428d3b90` installs TLS and executes callback `+0x08`. | Fairness, retail worker occupancy, callback latencies and source-map-lock arrival distribution are not measured. |
| Inline path | Matching worker TLS and pool worker count 1 select direct `0x1427e5880`; absence of usable scope can also run node virtual `+0x10` directly. | This conditional branch is not the multi-worker installation baseline. No one-worker retail result was measured. |
| Cancellation/reuse | Worker discriminator validation can cancel stale work. Existing DB/key/aggregate state can bypass registration or provider calls. | A discriminator value is not a unique historical population epoch. Reset is not an atomic proof of fresh request order. |

## Paired first-miss witnesses and incremental challenge

D5S supplies two continuations from the same declared initialization prefix.
Both keep ContentManager layer preparation pending while activating the density
batch. Target keys and source state are cold. Competing terrain/cell work is
delayed; these are explicit scheduler choices rather than failure-state inputs.

| Continuation | Required relative ordering | First target construction |
|---|---|---|
| Owner | Activate the batch, let ProcGen pump return, owner-back claims; completion pumps run before the next density claim without releasing ContentManager's preparation barrier. | Index 845 after 58 non-target claims; original `(10,11)` → body-face `(37546,20939)` → mask 3. |
| Peer | Activate the batch, preempt still-running ProcGen pump, let another worker take front claims; completion commands remain pending. | Index 874 after 28 non-target claims; original `(-2,-2)` → body-face `(37534,20926)` → mask 0. |

Every earlier density claim in each witness is outside the target's support.
The source survives all 24 relevant corner insertion orders, other emitted
sources have different visited identities, and the selected source reaches its
actual unvisited pointer-map miss. A mere dequeue is not substituted for this
selection-to-construction proof. Density level 0 calls `0x1407a1940`, then
provider `0x14079f860` at `0x1407a1a3c`; later levels reuse aggregate `+0x08`.

The new D5W challenge removes the assumption that queue activation must finish
before claims. In the same root expansion, first target density registration is
index 419, `(-2,11)`, mask 3. First target mask-0 registration is index 833,
`(-2,-1)`. That gives the early request 414 registration-index steps of
opportunity under resident prerequisites. It gives no lower bound on elapsed
time, worker service or lock acquisition. Early layer root `(-2,11)` is another
possible source path: none of its density neighbors can emit the target. A
density-only argument excluding it is false.

The original native dispatcher/push/pop was executed in twelve isolated queue
controls, with activation batches 1, 100, 420, 600, 875 and 1,720 for owner and
peer claims. Immediate draining claims `(-2,11)` for both. Whole-batch controls
reproduce D5S's opposite outcomes. Batch 875 gives the owner `(-2,-2)` and peer
`(-2,10)`, rejecting an owner-equals-mask-3 simplification. These are callback
tokens with successful supplied allocation and five empty contexts. They do
not execute the full engine's nodes or supply a retail timing model.

Thus early locality can give mask-3 requests a head start in this prewarm
expansion. Calling it a demonstrated general preference would additionally
require ordinary-route admission/ready times, available worker service and
completion through target arbitration before overtaking requests. Those
premises cannot be inferred from array order, mask-region area or this fixture.

## Arbitration, original-query authority and retention

Cell selection uses the original Int2 and the Grid's actual origin/slots.
Fill/edge/corner emitters supply retained raw contributors. Provider reads source
BIOM at its anchor and tests visited identity `source+0x68` under shared ProcGen
`+0x40`. After a false visited check it acquires exclusive protection at
`0x14079fcb3`, looks up the full source pointer at `0x14079fccb` and branches
on miss at `0x14079fcd4`. The same exclusive interval covers wrapper insertion
`0x14079fdf9`, synchronous generation `0x14079ff18`, visited append
`0x14079ff3e` and release `0x14079ffa5`.

No source-coordinate comparison chooses the lock winner. A waiter that passed
visited before insertion can subsequently hit the existing map entry. Visit
marking does not verify successful/nonempty generation. The supported contract
is a serialized first miss and conditional retained output, not automatic
successful-first-writer recovery.

At `0x14079fea1..0x14079febe`, the original query is converted using the current
manager descriptor, then passed as the generator's geographic input. Sampler
`0x142339340` returns its low nibble; generator compares that numeric rarity
control at `0x14079bdad..0x14079be20`. Source-derived generator origin, seed,
BIOM and clip remain separate. The nominal anchor, source centre, clipping
centre and beacon are not substituted for that query on this route. A location
coincidence in the [sampling map](d5w/sampling.svg) proves no canonical authority.

Retained references protect copied collections. Rehashing slots does not rewrite
their geometry. Movement retirement can erase a map entry while leaving visited;
a broad registered-module reset clears both. Source lifetime still carries D5S's
qualified detached-density gap; no valid retained-episode guarantee covers that
counterexample interval. See [D5V's native lifecycle](d5v-lifecycle-consumer-map.md)
for exact reset, load-phase and consumer sites, and the D5W report for the
distinct three-level stability contracts.
