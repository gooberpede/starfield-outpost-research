# D5H native proof and address domains

[Report](report.md), [function/export register](native.csv), [source pins](sources.csv).
Every native address is a preferred static VA at image base `0x140000000` on
the freshly hashed Starfield.exe 1.16.244.0. RVA is VA minus that base. Field
displacements are bytes. Source-grid coordinates are signed 32-bit integers;
source pointers, visited keys, FormIDs and analytical geographic labels differ.
Full bytes, instructions and decompilation stay local.

## Enumeration and source-admission chain

Export names below abbreviate `.local-work/workshop-population-rework/specialist/`.
`G013` is authenticated member `.local-work/resource-geometry/native/013.request.tsv`;
its lease and original member hash are in the method receipts.

| ID | Primary body / decisive instructions | Rule and proof boundary |
|---|---|---|
| N01 context | `d5h-frame07.tsv`, `0x14078c4e0` | Qualify the manager `+0x78` context, tagged-state bits and worldspace. Flagged alternate `+0xf2` bit 1 can select `0x140bbd270(+0x1f0,0)`; otherwise use `+0xe0`. Main PNDT alone is not this live context. |
| N02 index creation | `d5h-admission08.tsv`, `0x1407847b0`; `d5h-frame07.tsv`, `0x140982390` | Manager owner `+0x120` stores ordinary grid `+0x10` and separate overlay grid `+0x18`. Ordinary dimensions add twice `(4*base + 5*stitch)` to requested dimensions. Grid fields `+0x48/+0x4c` are dimensions, `+0x50/+0x54` stitch, `+0x20` cell table; `+0x28` is separate metadata. Both grids bind a MultiFiles parent through `+0x30`. Primary flags are `0x3b`; overlay flags differ. |
| N03 concrete parent | `d5h-origin10.tsv`, table `0x144b3e0b8`, slots `+0x80/+0x88` → `0x140781c80`/`0x140781cc0`; setter `0x140782070` | Dimensions come from current master `parent+0x18`, fields `+0x28/+0x2c`. Parent origin `+0x70/+0x74` is requested center minus master half-dimensions. Grid origin `0x1409870d0` adds master half-dimensions and subtracts grid half-dimensions, cancelling the master terms. Signed integer divisions truncate toward zero; no floor substitution. This dispatch/formula is resolved, although the invocation's center remains runtime input. |
| N04 source construction | `G013` / fresh `d5h-parent09.tsv`, `0x140982d90`; `d5h-admission08.tsv`, `0x140982d00`; callback `0x1407862a0` | Require the source's stitch-expanded rectangle to overlap the grid, using strict inequalities. Existing descriptors deduplicate on local anchor `+0x10/+0x14`; later same-anchor input does not overwrite the retained descriptor. Copy padding to `+0x20/+0x24`, raw dimensions to `+0x28/+0x2c`, nonnegative nominal dimensions to `+0x18/+0x1c`, definition/geographic fields and separate visited key `+0x68`. Constructor admission does not establish a first miss. |
| N05 base fill | `d5h-dispatch05.tsv`, `0x1409832e0`, especially `0x1409834ba–0x14098353c` | Iterate each retained descriptor's nominal XY. Transform anchor through the same effective grid origin, clip to dimensions, create `GridFillCell` when absent and dispatch setter `+0x08`. Source-local coordinates start at its padding. |
| N06 edges | `d5h-enumeration03.tsv`, `0x140985900`; `d5h-dispatch05.tsv`, calls in `0x1409832e0` at `0x14098371b/75e/799/7da` | For `i=1..n`, flags 1/8 add `+i` to the high boundary; flags 2/4 add `-n-1+i` to the low boundary. Require destination grid and source-local raw bounds. Create concrete X/Y edge cells as needed. Blend weights are metadata, not a filter on emission. |
| N07 corners | `d5h-enumeration03.tsv`, `0x140985c50` and `0x140986080`; corner calls in `d5h-dispatch05.tsv` at `0x1409835d9/635/67e/6cf` | Cartesian edge offsets cover corner insertion attempts. Existing edge cells can be converted to corners while preserving their contributors. Bounds still clip attempts. A nominal width `w`, stitch `n` therefore gives attempted X interval `[-n,w+n)` relative to anchor; likewise Y. Occupancy can reject a later pointer. |
| N08 concrete setters | `d5h-dispatch05.tsv`, `0x140988220/2d0/4e0/670` | Fill stores at cell `+0x18`; edges use `+0x18/+0x20`; corners use four slots through `+0x30`. Slots install only when empty and otherwise compare identity. A corner setter can touch several slots and overwrite its return flag; it is not an unconditional set union. |
| N09 concrete emission | Same export and `d5h-frame07.tsv` table data | Fill table `0x144b67eb8 +0x10` → `0x140988240`; X edge `0x144b67e28 +0x10` and Y edge `0x144b67f00 +0x10` → `0x140988330`; corner `0x144b67e70 +0x10` → `0x140988760`. Append each nonnull retained slot in order. There is no nominal-contains test or blend-weight gate in these methods. One query can emit multiple source pointers; one pointer can occupy several queried cells. |
| N10 completion | `d5h-index06.tsv`, `0x140983270`; full `d5h-parent09.tsv`, `0x140983880`; `d5h-modifiers11.tsv` and alignment helpers in `d5h-feasibility12.tsv` | Complete source insertion, then dispatch pending modifiers at `+0x18`, then materialize terrain files. Inspected modifiers build their own height/maps; `0x140983880` writes resolved cell `+0x08/+0x10` and reads candidate slots. `0x1409865e0` writes the separate grid `+0x28` metadata table. Final `0x140784530` computes a preparation-buffer CRC. No candidate-support widening occurs in this qualified phase sequence. Alternate writers, aliases and overlays are not included by assumption. |
| N11 index lookup | `d5h-enumeration01.tsv`, `0x140985870` | Subtract effective origin from original caller Int2; require both signed deltas nonnegative and below `+0x48/+0x4c`; read `grid+0x20 + 8*(dx+width*dy)`. Null/out-of-range stops enumeration. The index rectangle is not a source's nominal rectangle. |

This proves a support **upper** for a source installed by this ordinary route.
Each initial contributor is inserted through N05–N07 within its raw-supported
padded rectangle. N08 can retain or reject pointers. Edge-to-corner conversion
copies contributors at the same cell. N10 materialization and its inspected
modifier sequence do not widen those candidate-pointer slots. Clipping, omitted
descriptors and slot conflicts narrow the result. The proof does not assert
that every attempted cell retains this source or receives an ordinary demand.

## Provider and first-miss gates

Primary `.local-work/recon/resource-milestone-b-producers-01.tsv` contains the
complete `0x14079f860` body. At `0x14079f92c`, N11 receives the original argument
RDX Int2. At `0x14079f9ca`, the selected cell dispatches N09 into a temporary list.
For each source, BIOM lookup receives source `+0x10/+0x14`; source and query are
not interchangeable. Source-local/native origin calculations use multiplication
by 100, conversion to binary32 and explicit round-down instructions separately.

At `0x14079fc37–0x14079fcaa`, the eight-byte source `+0x68` identity is compared
against the visited array. A visited hit skips the population block. Otherwise
the provider acquires exclusive ProcGen `+0x40`; `0x14079fccb` looks up the full
source pointer. Capacity comparison at `0x14079fcd0/0x14079fcd4` distinguishes a
hit from a miss. A hit retains the old wrapper and bypasses generation. A miss
allocates/inserts and calls `0x14079b520` at `0x14079ff18`. The visited append
afterward is not a generator-success test. Prerequisite exits remain separate.

For source `S`, the parameterized first-miss predicate is:

```text
context qualifies AND index lookup succeeds AND completed cell emits S
AND BIOM(source anchor) resolves AND visited does not contain S.key68
AND exclusive source-pointer lookup returns capacity
AND generator prerequisites succeed
```

The first successful member also depends on the request/dependency prefix and
source lifetime. This formula is exact within the cited path, but its live
operands are not supplied by installed definitions. A source-map hit, aggregate
reuse, visited skip, insertion and successful ordinary geometry are distinct.

`d5h-feasibility12.tsv` shows ProcGen initialization and reset. Reset clears
source/visited storage, then `d5h-math13.tsv` `0x1407b4770` drains/reset server
entries. It is invalid to assume reset produces an otherwise unchanged empty
state with no intervening demand. No reset or other target operation was run.

## Original query to ordinary mask

| Stage | Primary location | Qualified operation |
|---|---|---|
| Descriptor | Provider `0x14079fe81–0x14079feaf` | Manager mode byte `+0x20 == 3` selects `+0x1c0`; otherwise `+0xc8`. Restore the original provider query, rather than the source anchor. |
| Fine-to-chart | `.local-work/recon/resource-availability-cont-01.tsv`, `0x14078d660`; fresh `d5h-frame07.tsv`, `0x14096f5c0/4d0` | Copy descriptor, signed-remainder/chart transformation, recompose coarse/subcell/residual, then `(fine+0.5)*(1/49152)-0.5` for the qualified interior route. All 25 tested supports stay interior. |
| Chart-to-geographic | `.local-work/recon/surface-projection-14.tsv`, `0x142332410` | Square-root projection and chart signs; scalar atan2; explicit binary32 horizontal conversion/sqrt at `0x142332534/538`, then promote for latitude atan2. |
| Scalar imports | `d5h-modifiers11.tsv`, `0x1434ca8d6/906`; PE import receipt | `cos` and `atan2` import `api-ms-win-crt-math-l1-1-0.dll`. Replay pins the resolved current host and RN control state. Same import names alone do not prove historical module equality. |
| Vector trig | `.local-work/workshop-population-rework/specialist/d5-mask01.tsv`, `0x142339340`; `d5h-gap14.tsv` | Wrapper `0x14374dcd2` duplicates longitude/latitude, adds lanes `(0,pi/2,0,pi/2)` at `0x14374dce2`, then jumps at `0x14374dcea`. Existing listing/decompilation omitted those final two instructions; pseudo-disassembly reads them without changing the database. CPU discriminator selects non-FMA `0x14374dda0` or FMA `0x14374e650`. Both finite fast paths are replayed; large-angle fallback is outside these inputs. |
| Vector-to-chart | Same surface projection export, `0x1423321f0` | Explicit f32 norm conversion, sqrt and reciprocal; chart sign selection; clamped inverse square projection with epsilon terms. |
| Raster | `d5-mask01.tsv`, `0x1423393a4–0x142339428`; `d5-raster02.tsv`, `0x1423390f0` | Fold charts 2/3 if present, clamp `0.5+x/y`, floor dimensions times X/inverted Y, clamp to dimension minus one, load byte and AND 15. |
| Ordinary weights | `resource-availability-cont-01.tsv`, `0x14079bdad–0x14079be20` | Mask 8 or mask less than rarity selects inactive multiplier; otherwise 1. Whole ordinary traversal retains this one sample. Special and alternate resource routes remain separate. |

[Arithmetic methods](../../../research/resource-query-reachability/roundtrip.py)
and [vector fast arithmetic](../../../research/resource-query-reachability/native_sine.py)
are instruction-derived explanatory replay. They execute no game function.
Singleton transformed uppers establish ordinary-mask invariance without proving
which demand occurred or whether a source had any admitted first miss.

## Demand prefix, admitted pair and historical invocation state

The [D5D ancestry](../resource-construction-demand/native.md) is retained and
checked against fresh `d5h-admission08.tsv` and `d5h-frame07.tsv` bodies.
`0x1407b5160` checks request discriminator `0x1407c0720`, then prepares four
neighbors through `0x1407a0fa0` before calling the provider. Density worker
`0x14076c560` checks the same discriminator, creates an aggregate and loops four
levels through `0x1407a1940`; only an absent aggregate calls the provider.
The density route is not the same prefix as the layer route.

| ID | Primary body / dispatch | Additional admission rule |
|---|---|---|
| N12 ordinary cell ingress | `d5h-cell25.tsv`, `0x140aed020`; `d5h-gates30.tsv`, `0x140ad3410`; caller `0x140afb220` in `d5h-worker26.tsv` | Eligible exterior cell with no excluded flags and false existing-state gate reads original Int2 from cell `+0x58`. After manager/placement/CellRefDB preparation, it passes the same Int2 address as min/max to `0x1407a1580`. This singleton request does not establish a singleton global region. |
| N13 resource registration | `d5h-demand15.tsv`, `0x1407a1580/0x1403625e0`; `d5h-entry22.tsv`, `0x1407b5a00` | The new resource entry synchronously calls `0x1407b4bb0` at `0x1407b5b4e`. Reused entries have different ordering. |
| N14 density dependencies | `d5h-admission08.tsv`, `0x1407b4bb0/0x1407a1260` | Gather DensityMapDB inputs, then register neighbors `(-1,+1),(-1,0),(0,+1),(+1,+1)` in that order. Each density request precedes its bounds-gated higher request. Actual active bounds derive separately; later higher requests must not be assumed absent. |
| N15 current discriminator | `d5h-density16.tsv`, `0x1407c07b0`; `d5h-feasibility12.tsv`, `0x1407c0720`; `d5h-setup28.tsv`, `0x1407b30c0` | Copy current nonzero discriminator and settings into the key; compare against the same current state in the worker. The setter obtains the discriminator from current worldspace record `+0x28`. Its name is not evidence that it is a chronological generation epoch. |
| N16 ready task | `d5h-feasibility12.tsv`, `0x14076cd40`; `d5h-dispatch17.tsv`, `0x14076d1c0/0x14076d140`; `d5h-initial18.tsv` table `0x144b3d0e8` | No-pending-input branch constructs mode 2 with dependency `+0x80=0`, `+0xa9=0`, abort `+0xab=0`; table `+0x10` is `0x14076d140`. Pending density inputs use a different table/continuation. |
| N17 actual task execution | `d5h-ready23.tsv`, `0x1427ec100`; `d5h-activate24.tsv`, `0x1427e6a00`; `d5h-cell25.tsv`, `0x1427e56d0`; `d5h-worker26.tsv`, `0x1427eb6b0/0x1427ec2e0`; `d5h-join27.tsv`, `0x1427e5880` | Mode-2 registration with zero dependency does not test parent readiness before activating the node. The selected scope-2 dispatch can execute directly or queue a callback. `0x1427e590b` invokes node `+0x10`; optional profiling does not gate invocation. Pool/queue premises still matter to the proposed first-query ordering. |
| N18 density first level | `d5h-demand15.tsv`, `0x14076c560`; `.local-work/recon/resource-availability-ui-32.tsv`, `0x1407a1940` | After discriminator success, a new aggregate has no provider payload. First level calls `0x1407a1940`, whose absent-payload branch reaches `0x14079f860` at `0x1407a1a3c`. The worker uses manager `+0x130` ProcGen, not manager `+0x70`. |
| N19 common initialization | `d5h-density19.tsv`, `0x140787830`; `d5h-initial18.tsv`, `0x14079d660`; `d5h-modules34.tsv`; `d5h-postsetup36.tsv`, `0x140785190` | Constructor retains initially empty ProcGen at `+0x130`. Actual fixed-module setup completes ordinary/overlay grids; all ten module `+0x68` callbacks return. ProcGen direct setup callbacks do not request construction. Empty constructor state alone is insufficient; frame, source population and required owner/raster readiness must coexist. |
| N20 focus and prewarm | `d5h-admission08.tsv`, `0x1407847b0`; `d5h-focusjoin44.tsv`, `0x1409a7950`; `d5h-focuscleanup46.tsv`, `0x1409a7ad0`; `d5h-cellprefix37.tsv`, `0x1407b3c50`; `d5h-postsetup36.tsv`, `0x1407b4750`; `d5h-setup28.tsv`, `0x1407b2390` | Successful master installation clears terrain focus `+0xe0`, then installs MultiFiles at terrain `+0xe8`. Cleanup does not revalidate focus. Module `+0x48` wrapper `0x1407b2370` sets the current discriminator through `0x1407b30c0`, then queues AcquireHandles. Its updater needs valid focus before prewarming. The completed initializer/placement/worker join is in [feasibility](feasibility.md). |

Generator success has its own premises: `0x14079b520` first needs a matching
initialized owner/BIOM component through `0x140771f30`, copied by
`0x14076e810`, then valid body/raster acquisition through
`0x140478350/0x140478a30` with status 0 or 6 and successful allocation.
These are required common inputs in a constructive witness; an entry allocation,
visited append or provider call alone does not prove generated ordinary output.

Cell preparation `0x140aed020` receives original coordinates from cell object
`+0x58` and requests them through `0x1407a1580`; its CellRefDB conversion feeds
a separate key. Rectangular and neighboring demand exist without a Workshop
argument. These instructions do not imply that every conceivable coordinate
can precede all other requests in one actual initialized streaming context.

For the selected S, the [constructive proof](feasibility.md) now supplies this
joint prospective state. Its original roots are A+(5,-2) and A+(5,0), where A
is the actual native source anchor. The first density queries A+(4,-1) and
A+(4,1) retain/emit S first and reach successful misses with masks 0/3.
The same allocation/key and qualified successful generator inputs are held
fixed across two alternative continuations, not replayed within one cache history.

The actual worker scope is `{DAT_1461fabe8+0x140, tag=2}`. Exports 60–67 resolve
its constructor/count, started GroupThread receiver, TLS owner, shared queue and
peer stealing, and invocation of the exact `0x1427ec2e0` callback. This closes
the earlier scheduling hypothesis without substituting a spatial halo for
admission or assuming producer completion is required before density execution.

The remaining five sources still need their own retained-slot and first-miss
prefix proofs. Historical masks remain unobserved for all relevant sources:
consumer snapshots are later boundaries, the wrapper/visited entries do not
retain the original Int2 as a lookup key, and no joined pre-demand task/index
snapshot was captured. Missing historical state is not offered as proof that
further offline admission research is impossible. The 31 spatial candidates
remain distinct from the two independently admitted static counterexamples.
