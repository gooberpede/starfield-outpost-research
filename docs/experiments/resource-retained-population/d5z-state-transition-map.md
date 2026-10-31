# D5Z visited-state transition map

2026-10-31, Australia/Sydney. [Report](d5z-report.md),
[sources](d5z-sources.csv), [active ledger](d5z-investigation-ledger.md),
[gameplay checklist](resource-generation-gameplay-checklist.md).
All native VAs are preferred static addresses for Starfield 1.16.244.0,
image base `0x140000000`; offsets are bytes. Pointer, visited identity,
geographic key, FormID, observer epoch and serialized identity remain distinct.

## Conditional native sequence

| Transition | Established boundary | Evidence strength and limit |
|---|---|---|
| Absent manager → created manager/ProcGen | Manager constructor `0x140787830`; ProcGen constructor `0x14079d660`; registration at manager `+0x130` and module vector | STATIC. Normal constructor initializes visited count/capacity/data to zero. Does not identify when the B1 manager was constructed. |
| Context installation → source index / eligible demands | `0x14078b030 → 0x14078bc30`; focus and request producers in D5W | STATIC conditional dependencies. Not a complete historical save-load order. |
| Selected source → visited test | `0x14079fc37..0x14079fcd4`; source qword `+0x68`, ProcGen u32 count `+0x48`, data `+0x50` | STATIC exact identity comparison under the visited shared lock. Match bypasses construction before map lookup; no holder retrieval is implied. |
| Unvisited → exclusive pointer-map lookup | Provider releases visited reader before acquiring ProcGen exclusive protection | STATIC. The visited check and later construction are separate critical sections; do not infer an atomic check-and-append or global duplicate uniqueness. |
| Lookup miss → inserted holder → generation → append attempt | Provider generation `0x14079ff18`; append helper `0x1422cc0d0`, call `0x14079ff3e` | STATIC. Complete geometry success is not an append prerequisite. Failed append returns `0xffffffff` and skips the identity write. |
| Source retirement → map entry removed, visited retained | `0x140982b70` under ProcGen exclusive lock | STATIC path-specific non-removal. A future selected source with equal visited identity can bypass even after its old pointer-map entry has gone. |
| Qualifying broad reset → empty stores | Manager `0x140788e70` or false variant `0x140789850`; actual registered ProcGen slot `+0x18 → 0x14079df60 → 0x14079ddf0` | STATIC under valid native state. Reset clears/releases map and visited allocation; it is not a capacity-preserving count-only clear. For malformed null-data/nonzero-count state, the conditional clear branch does not prove zeroing. |
| Empty stores → later construction opportunity | A later demand passes source/BIOM/visited/map/generator prerequisites | Conditional inference from compiled branches. Reset is not itself construction or proof of a successful population. |

The reader/append gap allows multiple providers to pass a shared test before an
exclusive map decision. There is no second visited scan under that exclusive
lock; duplicate prevention therefore also depends on source/map identity and
lifetime. A retained pointer-map hit jumps to `0x14079ff64`, skipping both
generation and visited append. It is not a visited hit.

## Reset callers and predicates

These are compiled capability paths, not a mapping of every player action or a
historical B1 call trace. The source ledger gives the exact exported instruction
windows. The manager's true and false variants both dispatch the registered
ProcGen `+0x18` reset; their other effects differ.

| Native path / call site | Predicate and sequence | Consequence / coverage |
|---|---|---|
| Owner installation `0x140789ce0`, calls `0x140789d61`, `0x140789feb`, `0x14078a012` | Incoming owner zero; same owner with different current/incoming component; or changed owner with existing nonzero context, respectively | Broad reset, followed by branch-specific installation/recursive reinitialization. Owner/body name equality alone is insufficient. |
| Same owner/component, call `0x140789e10` | Same-context branch chooses `0x140789850` | False variant still clears visited; descriptor setup/pool behavior differs from full replacement. |
| Component release `0x14078cf00`, call `0x14078cf76` | Current owner nonzero and qualifying current world's component differs from supplied component | Broad reset; other branch tidies matching retained world references. Direct caller `0x14057ffea` is in the world-component setter path. |
| Cell transition `0x14057abc0`, call `0x14057b084` | Admitted transition, manager state byte `+0x20 >= 2`, and the qualifying incoming-cell flag described below | True broad reset. Not every cell transition or travel action takes it. |
| Same cell-transition body, call `0x14057b0a1` | Incoming qualifying flag false and setting at `0x145e8fd90` nonzero | False reset variant. No visited-capacity predicate. |
| Context processing `0x1417df210`, call `0x1417df632` | Computed context differs from manager owner `+0x80`, with `0x142116840` null/context-flag gates | Can transition old world and reset. Same-context branch can instead update focus through `0x14078c5f0`. |
| Transition helper `0x1417dec70`, call `0x1417def9b` | Local transition flag false, retained local context nonnull, manager module `+0x148` object's `+0x18` null | False reset variant; gameplay label remains conditional. |
| Subsystem teardown `0x14076b3e0`, call `0x14076b43d` | Teardown entry; drain, reset and guarded teardown, then singleton destruction/nulling | Visits cannot survive as old process allocations. This is not evidence that B1 used this route. |
| Full game reset `0x141896280`, call `0x141896e4e` | PerformGameReset body; reset plus guarded subsystem reinitialization | Broad lifecycle reset, not a visited-size limit. |
| Global revert `0x141827960`, type 3, call `0x1418279db` | `!bAvoidClearOnReload || phase_flag`; ordinary full-load range helper passes phase flag zero | Calls wrapper `0x1407895a0`, then broad reset. |
| Global-type-3 manager loader `0x1407896d0`, call `0x140789837` | `bAvoidClearOnReload` nonzero; saved/resident context and compatibility comparisons determine forwarded flag | Calls the same wrapper for compatible or incompatible flag. Zero setting skips this loader's reset; it does not negate the complementary revert branch. |

The qualifying incoming-cell flag in `0x14057abc0` is established at
`0x14057ac21..0x14057ac4e`: nonnull cell; cell `+0x48` bits `0x1` and
`0x8000` set; cell `+0x58` nonnull with pointed byte `+0x68 == 1`; and
`0x140922b30(cell+0x28)` resolves differently from invalid handle sentinel
`0x1461fae90`. The function first returns if the incoming cell already equals
TES `+0xe8` and the force argument is zero. Later reset logic additionally
requires no selected reference, or `0x14211a000(selected)` to return zero.
That helper returns one only for a resolved reference with nonnull parent cell
whose `+0x48` bit `0x1` is clear.

All five direct call sites of that cell-transition body are followed in the
fresh exports: three branches in `0x141a25420`, plus starting-world path
`0x141895460` and fallback-cell path `0x141895cc0`. This bounds the native
predicate explanation without asserting a complete UI-to-fast-travel trace.

Whole existing-listing module-offset scanning identifies the real manager
count/data loops after receiver/width/stack disambiguation. Only the two reset
variants dispatch the actual ProcGen `+0x18` slot; its other audited non-destructor lifecycle
slots are no-ops. A numeric displacement match is not evidence of a module alias.
Apparent wrapper DATA references at `0x14549c074` and `0x14549c084` are positively
classified as chained unwind records: three u32 RVAs, not a callable u64 pointer.
The local proof `.local-work/d5z-reset/unwind-ref-01.json` pins installed bytes
and read-only Microsoft SDK/MSVC ABI-source consultation. No header code is copied.

Allocator recovery and its bound cleanup callbacks are independently traced
through typed cell unload/destruction and worldspace membership removal in
[the report](d5z-report.md#reset-causality-and-lifecycle-purpose). That closure
supports the scoped absence of a dedicated size/pressure reset policy; generic
recovery can still service independently eligible lifecycle work.

## B1 checkpoint and reset evidence

Fresh reauthentication uses unchanged D5Y analysis under
`.local-work/d5y/d5z-recheck01/`, then the task-owned
[B1 analysis](../../../research/resource-retained-population/d5z_b1.py).
The corrected receipt is `.local-work/d5z/b1-02/b1.json`; earlier `b1-01`
remains preserved. Raw capture SHA-256 is
`cd4762095a422fb537844546e923fff667e894a63b082b0205f3107786f49a5c`;
the 47-member archive SHA-256 is
`5f4bf02d5f1994996f1a178cc50986d22bcb91cfc9ff7a8ac41bb90cc3e75ccf`.

| Evidence | Strongest supported reading | What it does not establish |
|---|---|---|
| Reset begin / protected unlock / normal end, sequences 2 / 3 / 4, observer epoch 2 | Same ProcGen; zero visited count/capacity word and data pointer at unlock; matched hazard/epoch closeout. A qualified empty-state boundary exists. | Reset caller identity, save-derived origin or future continuous target history. |
| Pre-travel nonce ACK, 110 acknowledged records and zero counted losses | Prefix contains READY 1, fence begin 54, fence end 54, cold 1. No provider entry or selection is admitted in this prefix. Last prefix event is 128.4452 seconds after first admitted event; ACK collection window is later. | Every engine operation, uninstrumented append/serializer activity, exact load completion time or no activity after the ACK. |
| Second matched reset, sequences 115 / 116 / 117, observer epoch 113 | Another empty-state boundary after the authenticated pre-travel prefix. This is stronger than reset-site execution alone. | Travel itself as the reset cause, or continuity through later losses/invalidators. |
| 119 conditional target-compatible selected/visited pairs, selection sequences 3297–10445 | Each retained pair witnesses a taken visited branch. Installed support permits only the target contributor under D5Y's explicit frame/content/Grid premises. | Direct copied target identity, a historical append, the actual target constructor or sampled mask. |
| First reported loss admission 1236; zero qualified cold-first chains | The conditional target observations occur beyond the initial loss boundary. The unchanged scientific reducer cannot qualify their historical firstness. | No target construction occurred, or a particular missing event must have happened. |

The first empty certificate excludes retention of pre-reset entries across that
specific reset under the verified normal-state contract. Reset counts alone do
not identify the later writer history. The completed ordinary native census
constrains visit creation to successful provider append after a returned
generation attempt; saved context/world inputs can rebuild sources and trigger
demand, but do not restore old visited membership. B1 still does not identify
which earlier token/source/query supplied a later hit. No source identity is
copied by the selected/visited-only hooks; borrowing a pointer identity from a
different epoch would add an unproved lifetime premise.

The minimum missing historical observation is an authenticated source identity
and effective descriptor/Grid binding at the target bypass, joined to the
relevant visited writer or complete earlier post-reset target access history.
A constructor/sample witness would additionally need an actual unvisited miss.
Existing B1 cannot supply those lost/uncaptured fields; no live retry or observer
change is authorized here. The ordinary native persistence/reset model is
resolved separately; it does not manufacture the missing historical observations.
