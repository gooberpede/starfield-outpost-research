# D5I native proof and source-specific traces

[Report](report.md), [source ledger](source-cases.csv), [pins](sources.csv).
All native addresses are preferred static VAs for Starfield 1.16.244.0,
image base `0x140000000`; member displacements are bytes. Geographic keys are
analytical identities, never native pointers, visited keys or saved tokens.
The [D5H native register](../resource-query-reachability/native.csv) locates full
bodies and exact byte ranges; raw native exports remain local.

## Common initialized state QS1

Instantiate the following state separately for each ledger source S. Keep S's
same allocation, `+0x68` identity, owning ProcGen, seeds, ordered owner map and
matching BIOM component fixed in both continuations. A denotes the native
signed Int2 at S `+0x10/+0x14`. Use the installed main-file source route with
stitch 2, no overlay replacement, and coherent interior descriptor/chart.
Require a completed grid containing both requests and their density neighbors,
and real current-region bounds admitting both roots. This is membership in
native-derived rectangles, not an invented singleton region or independently
free coordinate translation. No particular historical numeric A is recovered.

| Native edge | Evidence and obligation retained in both continuations |
|---|---|
| Ordinary source/index | `d5h-admission08.tsv`, `0x1407847b0`; `d5h-parent09.tsv`, `0x140982d90`; `d5h-postsetup36.tsv`, `0x140785190`. Source collection/deduplication precedes fill/edge/corner completion; actual grid clipping must admit the cells. D5H N02–N11 and its closed padded upper remain controlling. |
| Empty state and completed index coexist | `d5h-density19.tsv`, `0x140787830`, and `d5h-initial18.tsv`, `0x14079d660`, retain initially empty owning ProcGen map/visited storage. Successful master installation calls `0x1409a7950` before installing terrain `+0xe8`; `d5h-focusjoin44.tsv` / cleanup46 show focus `+0xe0` remains zero. Fixed module callbacks and index completion do not demand S. No old source jobs are assumed. |
| Current region and prewarm | `d5h-setup28.tsv`, `0x1407b2370/0x1407b30c0`, establish the actual current-worldspace discriminator/bounds before queuing AcquireHandles. `d5h-cellprefix37.tsv`, `0x1407b3c50/0x1407b2390`, cannot prewarm while focus is invalid. Retain this initialized prefix before a later focus setter. Reset is unnecessary and is not used. |
| Ordinary demand predecessor | `d5h-cell25.tsv`, `0x140aed020`, retains exterior-cell flags, nonzero matching owner, existing-state gate and original cell `+0x58` Int2. Before resource demand, `0x1418b4270/0x1418aa1c0` prepare placement, and CellRefDB uses its separate converted key. D5H's fixed LoadingCells DFOB→PCMT tree, 108 branch / 525 content nodes and 38 CNDF closure remain the main-definition qualification. Eleven concrete callbacks do not force earlier BaseProcGen S construction; condition 865 reads file DensityMapDB, whose readiness is retained. See D5H feasibility, fixed placement predecessor, and exports 41–56/63. |
| New resource request | `d5h-demand15.tsv`, `0x1407a1580/0x1403625e0`; `d5h-entry22.tsv`, `0x1407b5a00` calls `0x1407b4bb0` synchronously. The same original Int2 address is passed as min/max; no singleton global bounds inference follows. |
| First density request | `d5h-admission08.tsv`, `0x1407b4bb0/0x1407a1260`, registers `(-1,+1),(-1,0),(0,+1),(+1,+1)` before their respective higher requests. Retain ready file inputs and stable nonzero discriminator through `0x1407c07b0/0x1407c0720`. |
| Executable worker | Exports 16–27 show the ready mode-2 node, zero dependency `+0x80`, false `+0xa9/+0xab`, concrete table `0x144b3d0e8`, `+0x10→0x14076d140→0x14076c560`. `0x1427ec100→0x1427e6a00→0x1427e56d0` has no parent-ready barrier on this branch. |
| Permitted order | D5H exports 59–67 resolve scope `{DAT_1461fabe8+0x140,tag=2}`, initialized positive worker count, started GroupThread/capture dispatch and actual callback `0x1427ec2e0→0x1427e5880`. `0x1428d2b80` publishes a ring slot before its counter; `0x1428d3960` can claim peer work without producer completion. Thus the first ready density worker may complete before its producer publishes a later higher request. Compatible read locks permit it. No FIFO reversal or arbitrary function invocation is required. |
| Provider call | Fresh aggregate level 0 calls `0x1407a1940`; absent payload reaches `0x14079f860` at `0x1407a1a3c`, using manager `+0x130` ProcGen. Source-grid lookup receives the original density Int2. |
| Actual successful miss | In the primary producer export, `0x14079fc37–0x14079fcaa` rejects visited `+0x68`; `0x14079fccb–0x14079fcd4` checks full source-pointer map absence; `0x14079ff18` invokes `0x14079b520`. The initialized matching owner/BIOM component must pass `0x140771f30`, copied by `0x14076e810`; body/raster acquisition `0x140478350/0x140478a30` must return status 0 or 6, with resident inputs and successful allocations. These prerequisites are explicit QS1 conditions, not consequences of a map insertion or visited append. |

The owner-component premise is source-specific: matching BIOM `0x000fc61a`
for VIII-b, `0x00145440` for second V, and `0x000c5718` for VI-b, with the
ledger's fixed root/RSGD and ordinary order. `0x140771f30` searches actual owner
components and compares component `+0x40`; a BIOM definition alone does not prove
the component exists. This proof has the same conditional scope as D5H's
accepted successful-construction join, not complete installed-data prediction
of every owner population. Missing component, nonresident raster, stale request,
pending file data, failed allocation or an earlier visited/map entry invalidates
that continuation rather than becoming a successful empty construction.

## Source-specific traces

Both continuations start from QS1 for S. Request L is `A+(5,-2)` and request H
is `A+(5,0)`. The first density query is respectively `A+(4,-1)` / `A+(4,1)`.
The new replay checks all four registered neighbors for both SIMD branches.

| S | L original root → first query / mask | H original root → first query / mask | Below competitor at L |
|---|---|---|---|
| `1:38100:960:002c17d5` | `(38105,958)→(38104,959)` / 0 | `(38105,960)→(38104,961)` / 3 | `1:38100:948:002c17d1` |
| `1:38112:960:0029d211` | `(38117,958)→(38116,959)` / 0 | `(38117,960)→(38116,961)` / 3 | `1:38112:948:002c17d5` |
| `1:38124:960:002c17d3` | `(38129,958)→(38128,959)` / 0 | `(38129,960)→(38128,961)` / 3 | `1:38124:948:0029d20d` |
| `0:37524:20928:00257f37` | `(37529,20926)→(37528,20927)` / 0 | `(37529,20928)→(37528,20929)` / 3 | `0:37524:20916:0029d211` |
| `0:29568:10944:0006ce56` | `(29573,10942)→(29572,10943)` / 8 | `(29573,10944)→(29572,10945)` / 0 | `0:29568:10932:0006ce58` |

These geographic query labels use the declared coherent descriptor. They are
not literal native coordinates assumed for every worldspace. Chart 1 is retained
explicitly: legacy `resource-availability-cont-01.tsv` at `0x14078d68e` copies
the descriptor chart byte, `0x14078d6f4` calls `0x14096f5c0`, and
`0x14078d741/0x14078d750` copy the resulting chart. `d5h-frame07.tsv`
supplies the signed-remainder/recomposition body and `0x14096f4d0`.
The inherited interior transform and current CRT/RN qualification therefore
apply on chart 1 as well as chart 0; no chart-0-only translation is substituted.
Both arithmetic branches return chart 1 for VIII-b and chart 0 for the others.

### Complete contributing tiles, identity and slots

The authenticated corpus maximum nominal dimensions are 22 by 22. For query Q,
all potentially contributing anchors lie in inclusive bounds
`[Qx-23,Qx+2] × [Qy-23,Qy+2]`. The helper scans every 256-entry FNAM tile
intersecting that bound, then filters by each actual SFBK's padded dimensions.
VIII-b uses tiles `1:198:4/5`, both SFPT `0x0026f7ef`; second V uses
`0:195:108/109`, SFPT `0x0023ddf4/0x0023ddf3`; VI-b uses
`0:153/154:56/57`, including SFPT `0x000c7ab0/0x000c7ab3/0x000c7ab4`.
All selected tile flags are 8. The VI-b left tiles are included even though they
contribute no surviving pointer at the chosen query.

The installed transpose mapping, inherited from D5H, is
`anchor=(192*tileX+12*slotX,192*tileY+12*slotY)`, with each slot coordinate
in `[0,16)`. It is injective across tile/slot pairs. With one collection of
the qualified ordinary main-file tiles, no different noncontributing tile entry
can supply an earlier same-anchor descriptor. The replay also rejects repeated
contributing anchors. Overlays, runtime replacement and repeated competing
collection epochs remain excluded, rather than resolved by that assertion.

At every L first query the target has nominal-relative `(4,-1)`, raw `(6,1)`,
10 by 10 nominal / 14 by 14 raw dimensions, and lower-Y flag 2. The below
competitor has nominal-relative `(4,11)`, raw `(6,13)`, upper-Y flag 1.
`d5h-dispatch05.tsv`, `0x1409884e0`, stores these respectively at `+0x18`
and `+0x20` only when empty. Both insertion orders retain the same two pointers.
`0x140988330` emits `+0x18` before `+0x20`, so S is first. At H, only S
contributes a fill at relative `(4,1)`, raw `(6,3)`; `0x140988220/0x140988240`
retain/emit it. No X-edge, corner conversion or same-slot conflict occurs in
these chosen first queries. The helper fails closed on those unmodeled cases.

Collection and grid/region clipping remain QS1 membership premises. They cannot
be removed using the padded support alone. Under them, S's BIOM lookup succeeds,
S is first emitted, unvisited and absent from its source-pointer map; the ready
worker takes successful generator prerequisites. Let that worker complete before
later registrations. L and H are thus separate first-successful continuations
of the same common state, not successive first insertions in one map history.

## Alternatives rejected and closed scope

The ten corresponding D5H spatial candidates at corner/X-edge offsets remain
candidate-only in its unchanged counterexamples ledger. This work does not
upgrade them. Layer-first demand through `0x1407b5160` has the separate
`0x1407a0fa0` neighbor-preparation prefix; a direct layer query with the desired
mask does not prove it wins. The ready density branch supplies the actual
constructive route instead. Reset clears storage and drains through
`0x1407b4770`; it is rejected as an unexplained fresh-state shortcut.

For each source, D5H's 196-cell completed ordinary support upper and both SIMD
arithmetic results exclude other masks in this qualified route. The two new
first-successful witnesses attain both masks. Therefore their qualified
first-miss mask set is closed and their effective ordinary inputs are variable.
Singleton nominal masks are falsified as universal prospective selectors.
No additional native operand remains open for this conditional classification;
actual historical A, effective owner state, winning query and lifetime remain
unobserved. Broader runtime prediction and saved association are separate questions.
