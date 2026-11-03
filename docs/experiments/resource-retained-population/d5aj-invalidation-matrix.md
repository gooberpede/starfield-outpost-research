# D5AJ source and owner invalidation

2026-11-03, Australia/Sydney. **The nine recorded clears target other owning
Grids, not demonstrably other ProcGen objects. Within the pinned ordinary
ownership graph, they cannot free the 36 captured source allocations or erase
their pointer-keyed map entries. They may erase other entries in the very same
ProcGen map.** This is a proposed scoped native/runtime conclusion, subject to
the [independent review](d5aj-review.md); it does not complete Episode A.

| Element | Answer and evidence boundary |
|---|---|
| Frozen question | D5AJ-Q1: which exact native operations can invalidate the captured source allocations, content, owner context or consumer map? |
| Confidence | PROVEN / STATIC for typed native receiver and pointer-key comparison; STRONG / CROSS-VALIDATED for continuity through these nine other-Grid clears under complete recorded history and the established ordinary ownership graph. |
| Tested coverage | Starfield 1.16.244.0, preferred static image base `0x140000000`; one immutable Episode A snapshot and all nine later-than-birth fence pairs. Fresh owned native erase/clear/consumer controls corroborate map effects. |
| Limitations | No other game build, arbitrary corrupt object, replacement vtable, uninstrumented foreign writer or general retail reliability claim. Exact sources removed by each other Grid are not recorded. Their current singleton ProcGen values are not directly copied by the Grid fence. |
| Primary evidence | `.local-work/d5aj/native-scope/native03.json`, the source registers and native windows below, original Episode A `events.bin`, and fresh `erase01/02.json` and `consumer01/02.json`. Raw/native receipts remain LOCAL-ONLY; authored synthesis is REVIEW-REQUIRED. |

## Correct the receiver domain before scoping a fence

The unchanged producer `observer.h::fence_hook<N>` writes raw first argument
`a` into the field named `proc`. That field's name does not establish its native
type. `birth_capture` and `published_capture` separately record their Grid in
`holder`; this is not a population holder. The bridge passes `R12 - 0x10`,
recovering the original Grid receiver after the constructor advanced `R12`.

| Reason | Hooked native function | Recorded `proc` domain | Native consequence and qualification response |
|---|---|---|---|
| 0 | ProcGen clear `0x14079ddf0` | ProcGen receiver | Clears its pointer map and visited storage under ProcGen `+0x40` exclusive protection. Refuse an older source/content certificate across this reset unless a separately proved new lifetime is established. |
| 1 | ProcGen destructor `0x14079d910` | ProcGen receiver | Ends that owner and releases map content without taking its own map reader lock. Refuse owner/content continuity; a reader alone is insufficient protection. |
| 2 | Map erase `0x140975030` | Pointer-map receiver, normally ProcGen `+0x10` | Removes a particular indexed key/holder and may relocate a collision-chain survivor. The hook does not copy the erased key/index. The minimal D5AJ method refuses every such intervening fence rather than inventing its origin. |
| 3 | Grid clear `0x1409829b0` | Grid receiver | Frees each source in this Grid's owning source array. For each source it loads the current singleton manager's ProcGen and erases only the equal full-pointer map key, then frees the source after unlocking. A different owning Grid can preserve a given source, while still changing the same ProcGen map. |
| 4 | Source retirement `0x140982b70` | Source allocation pointer | Loads current singleton ProcGen, erases that source key, unlocks and frees the allocation. Grid retention does not protect the detached source. The minimal method refuses such intervening fences. |
| 5 | Owner installer `0x140789ce0` | Manager receiver | Covers owner/component replacement and nested resets, including owner A to B to A. Refuse owner and source-context continuity. |
| 6 | True manager reset `0x140788e70` | Manager receiver | Covers the late owner-zero store after inner ProcGen clear. Refuse continuity even if the final body value again matches. |

Reasons 0/1/5/6 are not waived merely because their receiver differs from a
snapshot ProcGen pointer. Reasons 2/4 are not positively attributed from the
field name either. Unknown, lost, overlapping or ambiguously paired relevant
events remain uncertainty. The correction admits only the proved other-owning-
Grid case, with complete ordering, epoch accounting and source/content checks.

## Positive ownership proof

The [P1 source-rooted alias closure](d5ab-p1-source-identity-lifetime.md),
particularly L01–L10 and L18–L21, is reused with provenance under SOR-P-0002.
D5AJ independently authenticates its primary exports and rechecks the native
constructor, publication, clear, retirement, pointer-map lookup and erase paths.
The bounded closure concerns ordinary native objects, not arbitrary computed
replacement clients.

1. Constructor `0x140982d90` saves its incoming Grid in `R12`, takes Grid
   `+0x5c`, and searches only that Grid's `+0x10` count / `+0x18` pointer array.
   A matching existing source returns through `0x140983182`, bypassing new
   allocation and publication. Otherwise a fresh `0x1a0` allocation becomes
   `R14` at `0x140983006`; the one executed store at `0x14098317e` inserts it
   into this same Grid's array. The birth/publication bridge records that
   Grid, not a later lookup guess. Source `+0x08` is a different reference-
   counted input object, not an owning-Grid backpointer.
2. The ordinary graph contains no inter-Grid transfer of an existing source
   into another owning source array. Cell, cursor, auxiliary and GridFillFile
   pointers are raw aliases. P1's three constructor callers and its complete
   source-returning getter dispositions distinguish those aliases from array
   ownership. Grid construction starts an independent empty source vector;
   owning-array retirement `0x140988100` calls the standalone retire function
   and compacts that same array. Grid destruction `0x140982930` first invokes
   the recorded clear, before releasing its remaining backing and receiver.
   Thus freeing or reusing the owning Grid cannot silently bypass the clear
   witness within this graph.
3. Grid clear `0x1409829b0` saves the Grid in `R14`, reads only its own source
   array, then loads singleton manager `0x145fd9c30` and manager `+0x130` at
   `0x1409829fc..0x140982a03` inside each source loop. It locks that ProcGen
   `+0x40`, looks up the source pointer at `0x140982a24`, conditionally erases
   at `0x140982a36`, unlocks, and frees the source at `0x140982af8`.
   Consequently Grid identity and affected ProcGen identity are separate.
4. Lookup `0x1403499f0` hashes all eight pointer bytes but still compares the
   full stored qword key at `0x140349ae4`. A hash collision is not a key
   match. Erase `0x140975030` can move a different surviving key/holder into
   the removed slot at `0x140975111..0x140975128`; it transfers and nulls the
   old holder reference, without releasing the surviving content. Target slot
   location need not stay constant. Actual target release or mutation is also
   independently excluded by the source-specific lifetime journal checks.
5. Normal generation, erase and clear take the ProcGen exclusive lock; the
   completed area scan owns its reader across the copy. The destructor is a
   separately fenced exception. Owner installation/reset are separately
   bracketed, so equal raw manager values do not substitute for continuity.
   The generation's actual consumed descriptor and output holder establish
   its stored frame; current manager double reads do not establish that frame.

These premises permit source-scoped exclusion of other Grid clears. They do
not permit accepting an unidentified Grid, a clear of the source's own Grid,
unpublished/pre-arming sources, a crossed owner scope, source ABA or an unknown
ending history. They also do not assert that a cleared Grid was harmless to
every other source or gameplay consumer.

### Independent challenge: Grid construction, backing copies and the clear tail

Review correctly required more than the source-getter census. Fresh disposable
exports 05–07 directly cover both concrete Grid vtables, their construction
callers, every derived Grid method and the heap-array reserve callbacks. These
close the following specific alternatives within the ordinary typed graph:

| Challenged path | Direct native disposition |
|---|---|
| A copied Grid inherits another live owning vector | The three direct constructor calls are `0x14084974b`, `0x140784871` and `0x1407848f3`. Each receives a fresh `0x70` or `0x78` allocation, then `0x140982390` independently zeros source-vector state at `0x1409823cd..0x1409823d6`. The constructor takes dimensions, padding and flags, not a source Grid to copy. Its other allocations populate the separate cell, auxiliary and modifier stores. Vtable-reference census finds only this base constructor/destructor and the explicit derived construction store; there is no unclassified ordinary copy constructor or assignment in these concrete entry paths. |
| A derived Grid uses a differently adjusted base pointer | The `0x78` path calls the base constructor with `RCX = RAX`, the allocation base, at `0x1407848f0..0x1407848f3`, then replaces the vtable at that same base at `0x1407848ff`. Its destructor `0x140987190` calls base destructor `0x140982930` without a `this` adjustment, and that base directly calls clear with the same `RCX` at `0x140982947`. Constructor birth/publication restores original Grid with `R12 - 0x10`; clear saves original `RCX` in `R14`. Both receiver domains are this same base subobject at offset zero, not distinct subobject addresses. |
| Derived Grid `+0x70` shares parent ownership | `0x140784902` stores the parent Grid at derived `+0x70`. Derived virtual methods `0x1409871d0`, `0x140987340` and `0x1409874b0` use it to read parent cells from parent `+0x20` and derive map-lookup outputs. `0x140987720` copies selected source pointers into the caller's separate scrap output array, then calls the parent's enumeration slot. It never assigns that output or parent backing to derived Grid `+0x18`. The other derived methods copy two coordinate words to output or perform a terrain predicate. The parent alias therefore permits selection of a parent's source without transferring its owning source array. |
| Reserve/reallocation aliases another Grid's backing | Constructor publication passes its exact adjusted Grid `+0x10` vector and an allocator functor capturing that same address to `0x1422cc0d0`. Heap functor `0x1402c5b80` allocates fresh backing and writes only that captured vector's `+0x08` data and `+0x04` capacity. Growth thunk `0x1402c5bd0` passes the same vector to `0x1422cba00`, which allocates new backing, copies only that vector's old elements, frees its old backing, and updates that vector. It receives no second Grid/vector from which to borrow live backing. A moved backing pointer is not an ownership transfer of source allocations to a different Grid. |
| A whole-Grid or vector move is hidden among ordinary Grid methods | The fresh bounded component census inspects 5,544 instructions through `0x14098786f`, retaining 581 source-vector, parent, call and wide-copy operand contexts. Full constructor/caller/derived bodies and earlier base method bodies distinguish stack temporaries, cell objects, scrap outputs and source dimensions from the owning Grid vector. The only owning-vector state changes in this graph are initialization, constructor reserve/store, same-vector retirement compaction, and clear/destruction. This is a typed receiver/caller result, not an inference from an arbitrary global `+0x18` offset search. |
| Clear tail `0x140982c50` frees another Grid's sources | It iterates this Grid's cell array `+0x20`, invoking each concrete cell deleting destructor, and frees this Grid's independent `0x40` auxiliary records from `+0x28`. P1 binds the actual cell destructors `0x1409858d0`, `0x140985c20` and `0x140986050`; these free the cell receiver rather than their raw source aliases. Original-instruction controls with inaccessible source pointers retain that distinction. The auxiliary origin is a separate newly allocated record in `0x1409865e0`/`0x140988b60`, not a source allocation. |
| Modifier reset callbacks silently end target content or change owner | The final Grid-clear loop dispatches modifier vtable `+0x10`. The seven constructor-installed tables bind five cases to scratch-reference reset `0x140850f30`, alignment to `0x140971d70`, and update-height to no-op `0x1402b56d0`. The first two null their own scratch aliases and release shared scratch owners. This is not a claim that their nested destructors have no effects. Any ordinary path to source free, pointer-map erase, ProcGen destruction/reset or owner installation/reset must still cross the independently established typed source-free/map/owner boundaries or content-ending journal. Those events remain disqualifying. All nine actual clear intervals contain no nested reason 2/4/0/1/5/6 event and no relevant target content ending/mutation. Their tail callbacks therefore do not silently bypass the stated target continuity tests. |

The last row deliberately uses complete relevant coverage instead of assuming
every indirect callback is inert. Direct source allocation destruction remains
bounded by the two positively traced source-free bodies and P1's parent-correct
unwind-action exclusions; owner writes remain bounded by the separate native
owner-writer proof. A newly found ordinary path outside that graph would reopen
qualification. Corrupt vtables, allocator contract violations and injected
replacement clients are outside the stated ordinary-object scope.

Fresh primary evidence is `.local-work/d5aj/native-scope/export05/native.tsv`,
SHA-256 `9c61b7e5c8d4dfe2fadd4dbc4a1f70f2aa350254891c7420e13f3cf66ac30762`:
the census is lines 2–621, both vtables 622–645, base constructor 646–1322,
clear/tail 1428–1728, derived destructor/methods 1729–2567, retirement
2568–2737, reserve helper beginning 2738, and all creation callers beginning
6859 and 7441. Export06, SHA-256
`4b3736bca8cc04d8950cf79c119b40a99e90fd64125b5f8e44b732ada9181718`,
binds heap allocator functor table `0x144af7088` and functions
`0x1402c5b80/0x1402c5bd0/0x1402c5be0/0x1402c5c10`. Export07, SHA-256
`52a5d7eb8bf9450ff8644e4c92f1525b9e7f59785100905efc3ad53b72d146d0`,
supplies actual backing growth `0x1422cba00` and allocator `0x1402ba260`.
Final-source export08 independently reproduces export07's exact bytes and
SHA-256, with all copied core hashes unchanged. It exercises the repository
driver after the added owned-Java-reader identity guard.
The prior P1 cell and modifier primary bindings are in specialist exports 01/02,
including their exact vtable slots and full reset/destructor bodies; their hashes
are authenticated by the D5AJ native scope receipt.

The [D5AJ export driver](../../../research/resource-retained-population/d5aj_scope_export.py)
retains the authored method. `export05/06` used the separately retained task-local
development drivers; `export07` uses the repository method before its additional
owned-Java-reader identity guard. Each result receipt records the exact driver,
Java, command and independently hashed disposable core before/after. Only
`D:/tools/sor-d5ai-ownership-export01` was opened with `-readOnly -noanalysis`;
original project files were not opened by Ghidra. No symbols/types/comments or
database core contents changed. These exports read existing analysis; they do
not execute the native functions or establish retail scheduling.

Final-source `native05.json` and `native06.json` authenticate all 40 retained
export paths, including all four fresh exports and their preservation receipts,
rehash the copied project core, and repeat the 36-holder/nine-pair derivation.
The earlier native03/04 results remain the pre-challenge method version. Exact
method and export-driver hashes are recorded in each applicable local receipt.

## All nine actual Grid-clear pairs

Every occupied A0 holder has a qualified birth/publication in the same owning
Grid, denoted G0. G1–G6 below are six different recorded Grid receiver addresses;
the local receipt retains their exact runtime VAs. All pairs have begin hazard
1, end hazard 0 and status 0. All complete before A0 begins at QPC
`5252161561511`; the completed scan witness is QPC `5252161575832`. Native QPC
ticks are ordering evidence, not wall-clock times. Admission sequence alone is
not treated as causal order.

| Pair | Core begin/end sequence | Thread ID | Begin/end QPC ticks | Epoch begin/end | Grid | Effect on the 36 captured sources |
|---|---|---|---|---|---|---|
| F1 | 31904 / 31905 | 44904 | 5251582085890 / 5251582085944 | 216 / 217 | G1 | Disjoint owning Grid; no source free or equal-key erase for G0 allocations. |
| F2 | 32084 / 32085 | 30656 | 5251582978589 / 5251582978638 | 218 / 219 | G2 | Same source-scoped exclusion. |
| F3 | 32094 / 32095 | 32496 | 5251597080848 / 5251597080900 | 220 / 221 | G3 | Same source-scoped exclusion. |
| F4 | 32104 / 32105 | 41232 | 5251603225964 / 5251603226017 | 222 / 223 | G4 | Same source-scoped exclusion. |
| F5 | 32114 / 32115 | 41232 | 5251603737055 / 5251603737086 | 224 / 225 | G5 | Same source-scoped exclusion. |
| F6 | 32124 / 32125 | 41232 | 5251603739946 / 5251603739971 | 226 / 227 | G5 | Same receiver reused for another clear; neither receiver identity nor uniqueness is invented. |
| F7 | 32134 / 32135 | 41232 | 5251603742506 / 5251603742537 | 228 / 229 | G5 | Same source-scoped exclusion. |
| F8 | 32144 / 32145 | 41232 | 5251603802794 / 5251603802848 | 230 / 231 | G5 | Same source-scoped exclusion. |
| F9 | 32154 / 32155 | 47940 | 5251608088246 / 5251608088314 | 232 / 233 | G6 | Same source-scoped exclusion. |

The complete interval from the earliest occupied-source birth to the completed
snapshot contains these 18 fence records and no other fence reason. They account
for the exact epoch bridge from 215 to 233. They do not write the manager owner,
replace its ProcGen or invalidate its descriptor certificate. That conclusion
uses the typed native paths and the recorded absence of other invalidators,
not a numerical comparison between the Grid receivers and snapshot ProcGen.

The captured sources and holders remain positively present at the final scan;
this does not reveal every other Grid's contents or establish when its entries
were absent. Clearing other keys could relocate these holders' slots in the
shared map. The task therefore preserves complete map traversal and content
lifetime checks rather than assuming the map was untouched.

There is also a narrower actual-event negative: none of these nine completed
clear intervals contains a recorded reason-2 map-erase invocation. The full
capture contains no reason 2 or 4 event at all. The pinned candidate hooks the
erase function's entry, not only one caller; unchanged `fence_hook<2>` emits its
entry event whenever recording is enabled, including a call nested inside
another fence. No special Grid-clear suppression exists. The exact-site,
continuous enabled-history and zero-loss premises are independently checked in
the [A0 audit](d5aj-a0-recovery.md). Under that measured hook coverage, these
clear executions did not invoke the instrumented map erase. The native path
can simply fail to find a key, or have no source members to examine. The capture
does not identify which explanation applies to each Grid and does not justify
claiming that no source allocations were freed. Native ability to erase other
entries is kept separate from this actual absence of erase invocation.

## Contradictory schedules and actual controls

| Alternative | Consequence and evidence |
|---|---|
| Clear G0 while recorded `proc != snapshot.proc` | Frees the target despite that inequality. This direct native counterexample rejects the tempting other-ProcGen rule. |
| Same source address after retirement/reallocation | Latest private birth is a new allocation identity; an old geography or frame certificate cannot be carried through it. Full source lifetime checks must reject the old association. |
| Same visited token, different geography or owner | Token equality does not affect the pointer-map key comparison or establish geographic identity. Birth semantics and exact owner/frame chain remain required. |
| Different Grid but shared ProcGen | The normal clear path explicitly permits this; erasure is scoped to pointer keys, not a distinct ProcGen assumption. Hash collision can move a retained target holder without destroying it. |
| Erase target map entry with external collection owner | Consumer exposure can end while some old geometry survives. Native `consumer01/02` and `erase01/02` distinguish final release, external survival and partial ownership; no pointer traversal after retirement is used. |
| Broad reset or owner A to B to A | Inner clear alone misses the late owner store. Entire installer/reset invalidation and unchanged owner-context rules remain mandatory. |
| Lost/missing fence, journal cutoff or overlapping callback | Refuse qualification. A clean final map or matching pointer cannot repair missing causal history. |
| Snapshot under same-thread exclusive recursion | Shared helper can admit the exclusive owner; native consumer control executes that path. Complete snapshot status must refuse its packed exclusive state. |

Fresh original-instruction `erase01.json` and `erase02.json` each pass seven
controls, including `chain-erase-moves-survivor-without-extra-release` and
`moved-survivor-later-clear-releases-once`. Fresh `consumer01.json` and
`consumer02.json` each pass seven point-consumer controls, including external
collection survival after erasure and same-thread exclusive recursion. These
are actual original instructions on owned synthetic objects, with substituted
form-resolution and recording-free services; they are not whole Grid-clear
execution, retail source retirement, scheduler measurements or new engine
observations. The original methods and all declarations are unchanged.

The complete [A0 audit](d5aj-a0-recovery.md) and versioned qualification controls
cover the actual birth/publication/generation/content joins and adverse reducer
schedules. A native possibility is not substituted for an observed ending.

## Exact source and reproduction pointers

| Proof | Authenticated primary locator |
|---|---|
| Clear/retire/reset | [D5AI ownership sources](d5ai-ownership-sources.csv), OWN-12/13/14; `.local-work/d5v/export01/native.tsv`, lines 1900–2059, 4562–4654, 5194–5399. |
| Constructor/publication | OWN-15, `.local-work/d5v/export02/native.tsv`, lines 2–440; `runtime/construction-winner/bridges.asm`, `birth_bridge` and `published_bridge`; `observer.h`, private birth and fence hooks. |
| Full-pointer map finder | D5S-E32 in [D5S sources](d5s-sources.csv), `.local-work/d5s/export32/native.tsv`, function `0x1403499f0`, beginning line 9459; equality instruction `0x140349ae4`. |
| Erase/holder release | OWN-21/22/23, `.local-work/d5ah-extractor/export02/native.tsv`, lines 2–425; [ending proof](d5ai-population-ending-proof.md). |
| Unique owning array versus raw aliases | [P1 source register](d5ab-p1-sources.csv), P1-E01-002/003/004 and specialist exports 01–15; [P1 L01–L21](d5ab-p1-source-identity-lifetime.md), including constructor callers and every source-returning getter disposition. |
| Owner/descriptor/consumer | [Owner writer proof](d5ai-owner-context-rework.md), [owner source register](d5ai-owner-context-sources.csv) and [source/consumer map](d5ai-source-lifecycle-map.md). |
| Historical epoch counterexample | [D5AC report](d5ac-report.md), complete 224-increment accounting; global observer epochs are not native cold-reset identities. |

Run installed CPython `-E -B` from the repository root, writing fresh ignored
outputs. [Native scope authenticator](../../../research/resource-retained-population/d5aj_native_scope.py)
reads the original stopped session, authenticates 40 native export paths
(36 retained and four fresh) plus the installed executable, and records the
exact 36 Grid joins and nine pairs. Its
presence assertions authenticate cited instructions; manual instruction reading,
not textual matching, supplies the semantic proof. Development `native01/02`
precede the added full-pointer finder pin; `native03` includes it.

Unchanged [erase method](../../../research/resource-retained-population/d5ah_lifecycle_native.py)
and [consumer method](../../../research/resource-retained-population/d5ai_ownership_native.py)
accept fresh `.local-work/d5aj/native-scope/` receipt names. They independently
hash executable bytes and all executed function exports, check both disk floors,
map private pages in their own disposable hosts and retain fixture backing after
recorded frees. The local active ledger records the experiment before execution.
The first pass used existing authenticated exports. The independent challenge
then required the fresh verified-disposable-copy exports above; no original
Ghidra project was opened. No database core, protected save, game process,
installed candidate or frozen historical reducer was modified.
