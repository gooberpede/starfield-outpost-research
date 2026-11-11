# D5AH geometry lifecycle and ownership

2026-11-02, Australia/Sydney. Proposed D5AH-Q1 COMPLETE for the qualified native ownership graph;
D5AH-Q2 BLOCKED for actual return/reconstruction evidence. Parent D5AH-CQ
is BLOCKED; D5R OPEN. Independent review controls acceptance.
[Original questions](../../implementation-briefs/README.md#archive-lookup) (`implementation-briefs.zip :: docs/implementation-briefs/CODEX_BRIEF_SOR_RG2_D5AH_geometry_persistence_reconstruction.md`),
[active branch ledger](d5ah-lifecycle-ledger.md),
[exact primary locators](d5ah-lifecycle-sources.csv).

**A source's resource geometry is retained by a separate reference-counted
population holder and nested collections. Source retirement removes the map
owner but retains the visited token; broad reset removes both map and visited
state. Neither a Grid alias nor a visited hit certifies surviving geometry.**
Save/load restores descriptors and PCM preparation data, then ordinary demands
can construct geometry anew. An actual complete departure/return geometry pair
is absent from B1/B2; the conditional table does not substitute for that pair.

| Element | Scope |
|---|---|
| Questions | D5AH-Q1 ownership; D5AH-Q2 reuse/reconstruction/return. |
| Confidence | PROVEN / STATIC for the stated compiled branches and layouts; executed native retirement controls corroborate their stated fixture contract. |
| Tested | Pinned Starfield 1.16.244.0, static image base `0x140000000`; fresh D5S replay, seven native erase/clear/final-release controls, and twelve explicitly emulated lifetime controls. |
| Inferred | State consequences after the named native predicates; historical map insertion between authenticated B2 miss and generator. |
| Unknown | A retail outpost's complete geometry before and after departure/return, actual reset callers, and unrecorded winner/input history. |
| Publication | Primary exports and numeric receipts LOCAL-ONLY; this authored synthesis REVIEW-REQUIRED. |

All addresses below are preferred static VAs; offsets are receiver-relative
bytes. Source pointers, FormIDs, source birth tokens, visited identities, saved
world keys, collection pointers and observer epochs occupy different domains.

## Owners, readers and release boundaries

| Object / owner | Positive native edges | Consequence and boundary |
|---|---|---|
| Manager and registered ProcGen | Constructor `0x140787830` installs manager `+0x130` and module vector `+0x170/+0x178`; ProcGen constructor `0x14079d660` initializes stores. D5AH-L045/046. | The registered ProcGen is the reset receiver; the manager can survive a reset with its stores emptied. |
| Geographic source | Constructor `0x140982d90` holds Grid `+0x5c`, rejects nonoverlap, deduplicates anchors, initializes a new `0x1a0` allocation, then publishes into Grid source array `+0x10/+0x18`. D5AH-L038; [P1 L01–L06](d5ab-p1-source-identity-lifetime.md). | The Grid source array owns source allocation lifetime. Dedup return is reuse, not birth. Failed publication is not a published allocation. |
| Cell, cursor, auxiliary and GridFillFile aliases | The source-rooted [P1 primary ownership census](d5ab-p1-source-identity-lifetime.md#l01l21-accounting) distinguishes source getters, cell/cursor arrays, auxiliary `0x40` records and GridFillFile raw source `+0x278` from its owned file data `+0x270`. | Copying a raw pointer or holding the Grid reference does not create a source lease. Cell destruction and file-holder destruction are different operations. |
| Provider and population map | `0x14079f860` retains Grid, emits raw sources, reads source fields, compares token `+0x68` under ProcGen shared `+0x40`, then releases that reader before exclusive lookup. Miss inserts a pointer-keyed holder and calls generator `0x14079ff18`; map hit skips generation. D5AH-L007 and [D5AC exact windows](d5ac-sources.md#owned-source-and-primary-native-graph). | The map key is the full source pointer. Visited and pointer-map decisions are separate critical sections; two requests can both observe unvisited before one constructs and the other hits. |
| Nested resource geometry | Holder resource slots are `0x18` bytes: u32 FormID and collection pointer at `+0x08`; collection has reference count at `+0x00`, region count/capacity/data at `+0x08/+0x0c/+0x10`. Regions stride `0x30`, points stride `0x10`. `0x1407ac2f0/0x1407ac0d0` append/deep-copy; `0x1407ac260` frees every nested point array and region backing. D5AH-L052 and native release addendum below. | Successful outer return is insufficient: failed region/point reserve can leave empty or partial represented geometry. See [fresh copy controls](d5ah-geometry-reproducibility.md). |
| Point consumer | `0x14079df70` takes ProcGen shared protection before map traversal; callback `0x1407affb0` increments collection reference at `0x1407b0031`, reads every region, then decrements and destroys only on final reference at `0x1407b0138..0x1407b0159`. D5AH-L040/043/052. | Local collection retention protects its nested arrays for this traversal. Returned resource pointers are definition identities; they do not retain the original source or resource contours. |
| Workshop area consumer | `0x1421e07d0` scans resident map under ProcGen shared protection; callback `0x1421e0f50` resolves IRES, transforms/tests regions and inserts admitted identities into consumer lists. D5AH-L028/029. | Area cache/list survival can differ from geometry lifetime. Radius/upper values are not independent refresh guards in this local branch; cached list equality does not prove present geometry equality. |
| Layer versus detached density | Layer `0x1407b5160` owns a manager reader across neighbor preparation and provider; detached density `0x1407a1940` only skips provider when its aggregate `+0x08` already exists. D5AH-L005/006. | A real spanning reader excludes another thread's manager-exclusive shift. A captured validity triple or destroyed preparation reader confers no continued reader ownership. |
| Ambient terrain reader | [D5AG concrete terrain graph](d5ag-terrain-resource-map.md#preparation-terrain-work-and-conditional-protection): terrain nodes hold the manager reader; cooperative wait can execute queued callbacks. | A provider actually nested inside that reader interval gains conditional shift protection. The protection ends at outer release, is not a source lease, and is not captured by B2's schema. |

Map-holder final release and map erase/clear destructors are traced separately
in the native release addendum below. No long-lived Workshop ownership of a
resource contour collection is inferred from its returned IRES list.

## Transition matrix

`Conditional` means all named predicates and valid native invariants are required.
Each row is a native state transition, not an assertion about every gameplay
operation bearing a similar name. Extractor state is a distinct dependency in
[the continuity investigation](d5ah-extractor-continuity.md).

| Transition / native predicate | Geographic source | Source Grid/cell aliases | Population holder | Full geometry collections | Visited token | Saved PCM/context | Placed extractor/resource attachment | Workshop consumer state | Native event / owner epoch |
|---|---|---|---|---|---|---|---|---|---|
| First construction: valid Grid/source/BIOM, unvisited, exclusive pointer-map miss | Existing published source selects output. | Grid retained; selected source remains raw. | New map entry before synchronous generation. | Constructed/copied subject to every reserve/copy succeeding. | Append attempted after generator return; reserve failure can skip store. | Context/definitions/preparation are inputs, not restored contour bytes. | Placement/producer association follows separate interfaces. | A later area/point scan reads resident geometry. | Real constructing invocation; observer epoch alone is insufficient. |
| Overlapping source demands: shared visit checks precede exclusive decisions | Same live allocation can be selected twice. | Two raw selections, neither adds a source lease. | First protected miss inserts; later hit reuses holder. | Same retained collection for the hit branch, including partial output. | Both can have observed absent; map hit skips append. | Unchanged unless another independent operation changes it. | No extractor mutation is implied by a provider hit. | Aggregate reuse can skip provider before either decision. | B2 positively records this arbitration; admission sequence differs from QPC order. |
| Normal movement below threshold: `0x14078c5f0`, mode 2, no blocking transition, both displacements below setting-derived bound | No source retirement by this branch. | Existing aliases survive absent other transitions. | Existing map entries retained. | Retained; new source demands remain possible. | Retained. | No serializer or PCM reset implied. | Movement alone establishes no association change. | Refresh may reuse or recompute its own lists. | No broad-reset witness follows from moving focus. |
| Threshold shift: `0x14078c5f0 → 0x14078ce00`, manager-exclusive owner; overlap remains true | Overlapping source retained; nonoverlap handled next row. | Grid cells/origin shift; raw source aliases confer no pin. | ProcGen shift slots are no-ops; retained source entries remain. | Retained absent retirement/reset. | Retained. | Descriptor/frame bookkeeping can change independently. | No automatic placed-extractor remapping established. | Query translation/refresh can change consumer answers. | Native shift differs from observer invalidation epoch. |
| Source retirement: `0x140987080` negates `0x140982d00` overlap; `0x140988100 → 0x140982b70` | Source storage freed after map unlock. | Selected/cell/file aliases do not postpone free. | Present pointer-map entry erased. | Map ownership released; a genuine outstanding collection reference may delay final free. | Not removed by retirement. | Source metadata can later reconstruct from inputs. | Producer continuity must be checked independently. | Cached admitted identities are not erased here as contours. | Source allocation lifetime ends even with Grid reference count 2. |
| Grid clear: `0x1409829b0` | Every source in source array erased/freed. | Source array freed; cells/auxiliary cleared and modifier callbacks dispatched. | Present entries erased under ProcGen protection. | Reference-counted release, not blanket guaranteed final free. | Not cleared locally. | Does not serialize or restore PCM. | No producer save/load conclusion from Grid clear. | Already copied definition lists are separate. | Schema-4 clear fences advance observer epoch; no ProcGen reset is implied. |
| Full reset: true `0x140788e70` or false `0x140789850`; registered ProcGen `+0x18 → 0x14079df60 → 0x14079ddf0` | Landscape reset `0x1407846d0` nulls/releases Grids. | Normal source teardown follows released owner graph. | Map cleared under ProcGen exclusive `+0x40`. | Map ownership released; final destruction follows references. | Storage freed/zeroed when data is nonnull under valid native invariants. | PCM/context are separate stores; reset is not a saved population reader. | Separate object/producer restoration and validation required. | Consumer list lifetime is distinct; later scans see then-resident map. | Same ProcGen allocation can survive reset; actual reset witness needed. |
| Depart worldspace: owner/component/cell predicates below | Depends on whether reset is actually selected. | Shift/clear/reset must be distinguished. | Reset branch clears; no universal departure rule. | Same conditional consequence. | Reset clears; retirement alone retains. | World/component metadata can persist independently. | Existing object may unload; association route is Q3. | A list is not a world/source retention pin. | Gameplay label cannot select native path without recorded operands. |
| Save writing: global type 3/7 writer branches | Runtime source not serialized by these branches. | No original pointer identity written as contour ownership. | No ordinary map-image restoration contract. | Generated point arrays are not the type-3 descriptors or type-7 maps. | No visited writer in audited serialization graph. | Type 3 writes context compatibility/descriptors/components; type 7 writes PCM seed/content/placements. | Reference/producer serialization follows separate objects, Q3. | Workshop saved state is not a saved resource population. | Writing a save does not itself imply reset or generation. |
| Full save load: stable `bAvoidClearOnReload`, valid ordinary objects | Runtime world/source objects reconstruct under context/readiness gates. | Old allocation aliases cannot be restored as live source leases. | Complementary revert/loader branches clear map. | Fresh construction is possible; demand/copy success is separate. | Complementary load reset clears visits. | Type-3/7 readers restore their own data; queued finish work can remain pending. | Reference/producer restoration is independent of contour completion. | Area list/placement/production are distinct readers. | Reset does not prove manager construction; load return is not all-input readiness. |
| Direct return with source/holder retained and no reset/erasure | Same allocation can remain. | Actual live ownership must span interval. | Reuse when the map is reached; visited can bypass earlier. | Existing geometry survives only through established owner/reference continuity. | Usually bypasses if equal token present. | Same saved key is insufficient evidence of same effective request. | Continuity measured independently, Q3. | Consumers can read existing map or cached answers. | No B1/B2 complete departure/return pair exists. |
| Re-entry of same source after retirement without reset | Fresh pointer/allocation may have equal content-derived token. | New aliases belong to new lifetime. | Old holder absent; equal token bypass does not fetch it. | New contours are not guaranteed by source reconstruction. | Equal surviving token suppresses construction before lookup. | Metadata rebuild is weaker than contour rebuild. | Production can only be interpreted with Q3 evidence. | An old list may coexist with no mapped source geometry. | Pointer reuse and equal geography cannot prove allocation continuity. |
| Return after reset or new manager | Sources rebuilt under owner/descriptor/PCM and streaming gates. | Fresh allocation witnesses required. | An eligible first miss can construct; no demand means no construction. | Same complete effective input contract can reproduce geometry; differing consequential inputs can differ. | Starts empty under valid reset/constructor state, then new stores. | Restored PCM is an input, not a geometry image. | Restored producer association is a separate outcome. | Recomputed queries must bind correct native frame. | Need positively observed new generation plus complete outputs to distinguish reconstruction from retention. |
| Manager teardown/replacement: `0x140788bc0`, `0x14079d910`; new-process bootstrap only when singleton absent | Old allocation lifetimes end. | Old raw pointer aliases cannot be transferred to new owner. | ProcGen destructor clears map and storage. | Final release rules apply; no pointer restoration across process. | Old visited allocation released. | Persisted definitions/context are separately readable after load. | Serialized references can restore; old runtime pointers cannot. | New owner/read state must be established. | Native manager generation and observer counter remain separate evidence. |

## Reset and return predicates

The focus threshold branch is explicitly conditional: mode byte `+0x20 == 2`,
no active blocking transition, and comparison of absolute translated X/Y
movement against the setting-derived threshold. Shift execution owns manager
exclusive protection and dispatches module `+0x50` then `+0x58`; ProcGen's
corresponding callbacks do not regenerate populations. See D5AH-L032/033/035.

Owner installation `0x140789ce0` resets for incoming owner zero; for the same
owner with a different current/incoming component; or for a changed owner with
an existing nonzero context. The same-owner/same-component path calls the false
reset variant, which still clears ProcGen. World-component release
`0x14078cf00` resets when current owner is nonzero and the qualifying current
world component differs from the supplied component; otherwise it tidies
retained world references. D5AH-L018 and L015 preserve those distinctions.

Cell transition `0x14057abc0` first returns when incoming cell already equals
TES `+0xe8` and force is zero. Its qualifying incoming-cell flag requires a
nonnull cell, `+0x48` bits `0x1` and `0x8000`, nonnull `+0x58` with pointed
byte `+0x68 == 1`, and a resolved handle different from invalid sentinel
`0x1461fae90`. Later reset also requires manager mode `+0x20 >= 2` and no
selected reference, or `0x14211a000(selected) == 0`. The qualifying flag takes
true reset at `0x14057b084`; otherwise setting `0x145e8fd90 != 0` permits false
reset at `0x14057b0a1`. D5AH-L044 and the [D5Z caller/predicate census](d5z-state-transition-map.md#reset-callers-and-predicates)
retain the concrete context-processing, transition-helper, subsystem-teardown
and PerformGameReset routes. These callers do not identify B1/B2's reset cause.

Full-load revert type 3, `0x141827960`, calls reset wrapper when
`!bAvoidClearOnReload || phase_flag`. Ordinary full-load range passes zero.
Type-3 manager reader `0x1407896d0` consumes saved context/compatibility;
when that setting is nonzero it calls the same wrapper with the comparison's
flag. Both flag variants clear ProcGen. With a stable setting, the complementary
branches establish clearing for the ordinary graph; a compatible comparison
is not retention. D5AH-L002/004 and [D5AD synchronous/queued chronology](d5ad-load-chronology.md#native-dependency-order)
separate this order from later queued component and demand completion.

Saved PCM seed `+0x420`, PNDT content map `+0x360` and placement map `+0x3e0`
restore through `0x1418b22c0`. Preparation `0x14079da80` consumes placement
results from `0x1418aa1c0`; `0x1407b5bd0` performs preparation subpasses.
The placement manager can reuse, prune or refresh according to day/settings
predicates. Fixed seed/cell alone therefore does not freeze all preparation,
and these arrays are not the source-pointer resource map. Primary D5AH-L003,
L047/L051 and [D5AD type-7 proof](d5ad-save-state-matrix.md#state-classification-and-its-limits)
preserve the actual saved/restored representation.

## Historical observation and adversarial controls

B1's corrected receipt `.local-work/d5z/b1-02/b1.json` records reset triads
2/3/4 and 115/116/117, 110 pretravel records, zero copied target identities,
119 conditional target-compatible bypasses, first loss admission 1236 and no
qualified cold-first chain. Its source identity and historical append gaps
cannot supply an actual full target return episode.

B2's `.local-work/d5ac/reconstruction05/summary.json`, `target.json` and
`carried-empty-oracle.json` directly distinguish 224 observer increments from
two reset triads and 111 Grid clears. Forty-seven intervening clears account
for observer epoch 113 to 207 without a further reset. The derived empty anchor
starts at sequence 883; last clear 1731 precedes first provider entry 2470.
Target birth/publication 2074/2075 identify allocation 932; requests 3837 and
3844 concern the same live source `0x1f4ed839520` and ProcGen `0x1f46b67eaf8`.
Both see unvisited; 3844 reaches miss/construction/store before 3837's map hit.
The actual target sample is `0x3`. No complete target region/point image,
retail departure/return pair, or loaded extractor behaviour was captured.
Neither this mask nor a source birth can supply those absent observations.

Fresh D5S replay in `.local-work/d5ah-lifecycle/d5s-replay01/` passes all eleven
retained method invocations and independent retained-result comparisons.
`native-retirement04.json` executes native Grid origin, shift and overlap/filter
instructions: source survives 37 three-cell shifts and retires at shift 38,
with Grid reference count 2. Terminal retirement is a recording callback;
actual source free is the separately read static `0x140982b70` path. It is no
retail race, live free or production observer test.

[Owned emulation](../../../research/resource-retained-population/d5ah_lifecycle_controls.py)
produces twelve contract checks at `.local-work/d5ah-lifecycle/contract-controls02.json`.
It covers retained holder, two prechecked contenders, retirement with surviving
visit/no holder, same-address new birth with equal/different token, consumer
collection leases across retirement/reset, fresh collection after reset, partial
output hits and reset without subsequent demand. Two independent owner-set
checks reconcile surviving references and final release. These are deliberately
emulated contracts, corroborating the documented distinctions; they do not
execute a native destructor, prove retail scheduling or repair a source lease.

## Native release addendum

The verified disposable-copy exports `.local-work/d5ah-extractor/export02/native.tsv`
and `export03/native.tsv` supply D5AH-L065–L069. Original/copied core preservation
is recorded by the extractor export receipts; this specialist only read those
outputs. The actual caller-bound joins are:

| Release edge | Exact predicate and instruction | Outcome |
|---|---|---|
| Source retirement/Grid clear to erase | `0x140982bbc/0x140982a36 → 0x140975030` after present-slot lookup, under ProcGen exclusive lock. | Erases one source-pointer owner; no visited removal. |
| Terminal-chain erase | `0x1409750a1 → 0x1407ab6a0`; slot `+0x08` nulled, decrement at `0x1407ab6ca`. | Final prior count 1 calls `0x1407aab10(holder+0x10)` at `0x1407ab6d7` and frees `0x40` holder; all branches mark slot metadata sentinel. |
| Linked-chain erase | `0x1409750e9` decrements removed holder; `0x1409750f7` destroys only at prior count 1. | Moves surviving chained slot into erased position and nulls moved-from ownership; a changed slot address is not changed contour identity. |
| Reset/destructor to map clear | `0x14079de8d/0x14079da46 → 0x1407aa8a0`; occupied slot sentinel distinguishes active entries. | Nulls each slot's owner, decrements at `0x1407aa8df`, calls nested destructor only at prior count 1, frees holder and marks empty metadata. |
| Holder final release to collection | `0x1407aab10` scans occupied resource slots, nulls pointer, decrements collection at `0x1407aab59`. | Prior count 1 calls `0x1407ac260(collection+0x08)` at `0x1407aab66`, frees `0x18` collection, then releases resource-slot backing. |
| Collection final release to points | `0x1407ac260` walks each `0x30` region; `0x1407ac29e` frees point capacity times `0x10`, then `0x1407ac2c2` frees region backing. | Nested point arrays are independently owned, not aliases of generation temporaries. |
| Attractive wrong destructor | `0x1407abe80` calls `0x1427b0d90` plus path/reference release rather than `0x1407ac260`. | Positively excluded from the contour-owner chain; same-sized refcounted objects are not interchangeable. |

[The original-instruction host](../../../research/resource-retained-population/d5ah_lifecycle_native.py)
executes seven native controls in fresh receipts
`.local-work/d5ah-lifecycle/native-release03.json` and `native-release04.json`.
It runs real map erase/clear, terminal-chain release, holder final release and
nested collection/point destructor instructions. Recorder-only free callbacks
retain Python-owned backing and independently compare exact freed address sets,
counts, cleared fields and surviving owner references. It checks last-owner
full release, two independent holders sharing a collection, final second-owner
release, empty map, terminal erase, linked-chain relocation without an extra
release and exactly-once release of the relocated survivor. The two full method
runs agree on all seven named results. Earlier `native-release01/02.json`
preserve the four-control pre-extension method, not failed or final-equivalent runs.

These native fixtures substantiate conditional ownership and final-reference
semantics, including a collection surviving removal of one genuine owner.
They do not establish that a Workshop object holds such a second collection
reference, exercise retail concurrency, or execute an outer ProcGen reset.
Twelve emulated reset/visit/adversarial controls remain separately labelled.

The native ownership branch is resolved at the pinned ordinary receiver graph.
Q2 remains BLOCKED specifically because the historical captures contain neither
complete geometry pairs nor the actual independently reconstructed return
inputs/outputs. Static mechanisms, saved PCM, fixed-input fixtures and producer
behaviour cannot recover an observation the historical schema never recorded.
