# D5AI source, population and nested geometry ownership

2026-11-02, Australia/Sydney. D5R OPEN; D5AI-Q1/Q2 require the final instrument
and independent qualification. This map supplies the native premises, rather
than declaring the integrated observer accepted. Primary exports and native
receipts are LOCAL-ONLY; this authored synthesis is REVIEW-REQUIRED.

**Ordinary generation, map erasure and reset exclude a foreign ProcGen reader.
A genuine collection reference protects nested allocation destruction, but does
not by itself prevent geometry mutation. A complete snapshot therefore needs
the actual map reader, no same-thread exclusive recursion, and recorder fences
for owner destruction.** The observer must copy owned bytes before that native
reader ends. Queuing a borrowed collection pointer is not an equivalent design.

| Element | Answer and coverage |
|---|---|
| Questions | D5AI-Q1 lifecycle/attribution and Q2 safe complete geometry/availability. |
| Basis | STATIC original instructions and direct-reference census; seven fresh original-code consumer/erase controls on owned disposable objects. |
| Coverage | Pinned Starfield 1.16.244.0 ordinary ProcGen/source graph. All addresses are preferred static VAs, image base `0x140000000`; offsets are object-relative bytes. |
| Evidence | [Thirty-one authenticated function windows](d5ai-ownership-sources.csv); `.local-work/d5ai-ownership/audit03.json`, `consumer03.json`, `consumer04.json`; the methods linked below. |
| Unknown | Actual future retail lifetimes and geometry, absent historical complete populations, arbitrary replacement code/corruption, and universal recorder reliability. |
| Qualification boundary | Exact integrated bridges, frame capture, epoch/hazard checks, complete output and native adverse schedules have separate tests in the [component record](d5ai-recorder-qualification.md). Independent acceptance is recorded in the [review](d5ai-review.md). |

## Distinct identities and owners

| Domain | Representation and positive native edge | What it does not prove |
|---|---|---|
| Geographic source | Constructor `0x140982d90`; initialized source scalars and actual publication into the Grid source vector. D5AI-OWN-15 and [P1 L01-L21](d5ab-p1-source-identity-lifetime.md). | Equal geography is not the same allocation. Grid/cell/file aliases are raw pointers, not source leases. |
| Source allocation | Observer birth/publication token joined to the source address and admitted lifetime. | Pointer equality after retirement or reset does not preserve the birth. |
| Visited identity | Source `+0x68`, consumed separately under ProcGen shared lock. D5AI-OWN-09. | Equal tokens are not injective geographical identities and do not prove a holder exists. |
| Pointer-map entry | ProcGen `+0x10` map, slots at `+0x20`, capacity at `+0x28`; full source pointer is the key. | Hash-slot ordinal is not source identity or allocation lifetime. |
| Population holder | Reference-counted `0x40` object; nested resource map has slots at holder `+0x20` and capacity at `+0x28`. | An equal address after invalidation does not prove retained content. |
| Resource collection | Resource slot is `0x18` bytes: u32 FormID at `+0x00`, collection pointer at `+0x08`; count/capacity/data at collection `+0x08/+0x0c/+0x10`. | Collection refcount is a destruction lease, not a writer-exclusion lock. |
| Region and point allocations | Regions have stride `0x30`; count/capacity/data at region `+0x18/+0x1c/+0x20`. Points have stride `0x10`. | Successful outer append does not establish all points copied; partial reserve failures remain possible. |
| Owner/frame | Current ProcGen/manager, native descriptor and query translation identity, with actual reset/destruction fences. | An observer epoch is not a native generation number; body/source geography alone does not fix the current coordinate frame. |

## Evidence-indexed transition matrix

| Transition and predicate | Source | Map/holder | Nested collection/geometry | Visited | Evidence |
|---|---|---|---|---|---|
| New published source, no population demand | New allocation owned by Grid. | No holder follows from publication alone. | No generation implied. | Determined by separate existing token state. | OWN-15; P1 publication proof. |
| Provider sees unvisited, then protected map miss | Selected raw source remains separately qualified. | New holder inserted before generator. | Synchronous ordinary/Special/later applicable stages write collections before provider unlock. Allocation/copy failure may leave empty/partial output. | Append attempted after generator; success needs actual store. | OWN-09, 04, 08, 01-03. |
| Another unvisited request reaches a protected hit | Existing qualified allocation. | Reuses holder; no generator in hit branch. | Represented geometry remains resident, including partial output. | This contender need not append. | OWN-09; authenticated B2 hit/miss history in D5AC. |
| Visited hit | Pointer may be new or retained. | This block does not fetch a holder. | No geometry guarantee. | Equal consumed token suppresses construction. | OWN-09. |
| Ordinary coverage shift preserves source overlap | Existing allocation can survive. | ProcGen shift callbacks do not generate. | Retained unless an independent erase/reset/write occurs. | Retained. | [D5AH exact shift predicates](d5ah-lifecycle-matrix.md#reset-and-return-predicates). |
| Source retirement or Grid clear | Source allocation freed after map unlock. | Present pointer-key entry erased under ProcGen exclusive protection. | Holder/map reference released; final nested destruction depends on remaining genuine owners. | Retirement/clear does not remove token. | OWN-13/14/21-23; retained D5AH seven native release controls. |
| Broad reset | Landscape/source teardown is separate from ProcGen clear. | Map cleared under ProcGen exclusive protection. | Map references released; external genuine collection references can survive. | Visited backing freed/zeroed under valid invariants. | OWN-12/22/23; D5AH reset map. |
| Resource-map growth/collision relocation | Source identity unchanged. | Resource slots can move. | Collection pointer moves; nested regions/points are not rewritten by rehash. | Unchanged. | OWN-24/25/27; `0x1407abe00..0x1407abe06`. |
| Point query under foreign-writer exclusion | No source dereference required for geometry traversal. | Visits each occupied current ProcGen slot. | Callback locally retains collection, traverses regions, then releases it. | Not queried or modified here. | OWN-16/17; consumer02 cases 1-5. |
| Area query actually scans | No source dereference in resident callback. | Same shared ProcGen exclusion. | Reads all occupied resource collections under that reader. | Not a generation trigger. | OWN-10/11. |
| Area updater reuses cache | Native refresh guard skips scan. | No current map census established. | Old admitted identity lists may survive; no present contour conclusion. | Unchanged by this path. | OWN-10, branch `0x1421e0960`. |
| ProcGen destruction | Owner lifetime ends. | Destructor clears map without acquiring its own `+0x40` lock. | Final releases can occur despite that reader. | Storage freed. | OWN-30. This is why the existing destructor recorder fence remains mandatory. |
| Ordinary full load/fresh process | Source/owner allocations reconstruct. | Complementary full-load reset clears old map state. | New demands can generate; no demand or failed prerequisites can leave no output. | New/cleared visited state is separately measured. | [D5AH load proof](d5ah-lifecycle-matrix.md#reset-and-return-predicates), [D5AD chronology](d5ad-load-chronology.md). |

## Writer and alias completeness within the ordinary graph

The examined semantic writer chain is positively bounded:

1. `0x1407ac2f0` has one direct call, `0x14079aced`, inside per-cell generation
   `0x14079a330`. Point deep-copy `0x1407ac0d0` has one direct call from that
   append, at `0x1407ac39d`. OWN-01-03.
2. Per-cell generation has one direct caller, `0x14079c4f7`, inside traversal
   `0x14079c470`. Its three call sites are inside `0x14079b520`; that generator
   has one direct caller, provider `0x14079ff18`. The provider holds the actual
   ProcGen exclusive lock across insertion, all synchronous generation and
   visited append until `0x14079ffa5`. OWN-04/08/09.
3. Collection lookup `0x1407a97c0` and slot reservation `0x1407aa9b0` each have
   their sole direct caller in that same per-cell generator. Collection pointer
   assignment `0x1407aabd0` has its sole direct call from collection lookup.
   It increments/decrements collection references and replaces a pointer; it
   does not rewrite a surviving collection's region/point scalars. OWN-06/07/26.
4. Collision helper `0x1407ab730` and rehash `0x1407abc90` move the FormID and
   collection pointer and clear the old slot. They do not copy or mutate nested
   geometry. Final-reference release remains separate. OWN-24/25/27.
5. Point and area resident consumers read geometry. Point traversal increments
   and later decrements the collection reference. A returned IRES identity or
   area list does not acquire lasting contour ownership. OWN-10/11/16/17.

The [audit method](../../../research/resource-retained-population/d5ai_ownership_audit.py)
checks each export hash and its native line window, and classifies the core
chain's data references against the pinned PE exception directory. The apparent
extra `.rdata` references for traversal, pointer assignment and rehash are
embedded chained `RUNTIME_FUNCTION` records; `.pdata` entries are exception
metadata. There is no unclassified core data reference in this bounded census.
This is a receiver/producer-rooted proof for the pinned ordinary graph, not a
global assertion that arbitrary computed replacement clients cannot exist.
The original source P1 alias proof is reused only for source semantics; nested
copy/move/destroy/read edges above are checked separately for D5AI.

## Qualified capture and adverse boundaries

The point reader acquires shared protection at `0x14079df9b` and releases it
with atomic decrement at `0x14079e027`. The actual area scan acquires at
`0x1421e09ed` and releases at `0x1421e0a87`. A once-armed capture immediately
after either acquisition can copy the map, target holders, all resource slots,
regions and points into preallocated owned storage before original traversal.
It must not call engine generation, wait for disk I/O, publish borrowed pointers
or recursively invoke another native consumer during that copy.

There are two important exceptions to a naive reader-only argument:

- Shared helper `0x1422cc350` admits the current exclusive owner. A snapshot
  with packed exclusive bits `0xffc00000` still set after acquisition can see
  ongoing synchronous construction. It must refuse coherent COMPLETE status.
  Consumer02 executes this actual same-thread recursion path.
- ProcGen destructor `0x14079d910` does not acquire the map lock. The existing
  observer brackets that entire function with hazard/epoch fence 1. An RPM-only
  snapshot can remain read-safe without claiming an owner lease: every borrowed
  pointer/count/data read must use checked `ReadProcessMemory`, while initial
  and final hazard/epoch/loss witnesses reject any overlapping destruction.
  The integrated native tests must demonstrate that refusal. A destructor after
  the final successful check does not retroactively corrupt already owned bytes;
  it also does not prove the later original consumer completed successfully.

Normal erase/reset uses the same exclusive lock and therefore waits behind a
foreign shared reader. A pending writer alone does not block incoming readers.
Interruption does not transfer lock ownership or turn a partial arena into
complete output. Read failure, arithmetic/count overflow, allocation/arena
exhaustion, malformed nested records, unfinished capture or observed lifecycle
overlap must retain explicit failure/uncertainty status. No error is an empty
population or proven consumer unavailability.

## Geometry order and representation

Resource slot order is hash-table order. The point scan visits every occupied
slot and appends each admitted resource if absent, with no resource priority
that suppresses another matching resource. Rehash moves those slots while
preserving collection contents. Consumer02 reverses two native resource slots:
the output vector order reverses, while the admitted identity membership stays
equal. Canonical sorting by unique u32 FormID therefore removes storage order
from content comparison; duplicate keys are invalid input. Preserve each
collection's region order and each region's point order.

`0x1407ac2f0` copies region bytes `+0x00..+0x13` and byte `+0x14`, but does not
initialize/copy `+0x15..+0x17`. Keep the raw header bytes for provenance; exclude
those three padding bytes from semantic equality with this explicit rationale.
Point copy preserves all sixteen bytes, including the fourth binary32 word.
Do not apply float tolerances, signed-zero collapse, arbitrary frame translation
or a geometry digest as the sole equality oracle. The final schema/comparator
owns exact comparison and malformed/partial rules.

## Fresh native controls and provenance

The [consumer method](../../../research/resource-retained-population/d5ai_ownership_native.py)
adapts the owned D5AH private-page method under SOR-P-0002. It authenticates
original PE bytes, maps only declared original native functions in its own host,
uses owned map/holder/region/point objects, preallocates the output vector and
substitutes only form-resolution and recording-free callbacks. The original
uncontended shared helper, map/collection scans, point predicate and erase/
release instructions execute. Fixture frees are recorded; Python retains the
backing allocations. No retail process or protected input is changed.

`consumer01.json` preserves the initial five cases; `consumer02.json` adds the
resource-order and exclusive-recursion controls. Final-source `consumer03.json`
and `consumer04.json` repeat all seven cases. These establish scoped native
consumer consequences, not occurrence of retirement/recreation in retail or
the final recorder's performance/transport qualification. The latter must be
proved on its exact final sources and package.

The [export method](../../../research/resource-retained-population/d5ai_ownership_export.py)
copies the authenticated original core roster into
`D:/tools/sor-d5ai-ownership-export01`, verifies each copy independently, then
opens only that disposable project with `-readOnly -noanalysis`. Original and
copied core hashes match after export. No original project is opened. The raw
export, command, logs, native receipts and exclusion identities remain under
`.local-work/d5ai-ownership/`; source CSV records their stable local locators.

## Runtime frame certificate and rejected current-state shortcut

The holder's first context bytes at `+0x08` are not established as a source
origin. Provider generation passes the actual source-origin Int2 separately
through RDX. Do not infer its value from a zero-initialized holder context.
The fixture's supplied origin/clip contract is also not a measurement of later
retail generation operands.

The initial proposal used current manager mode/body/descriptor reads around
the snapshot. Independent review correctly rejects that as a frame-coherence
proof: equal before/after reads cannot exclude a change-and-restore ABA, and
the ProcGen map reader does not by itself exclude every manager descriptor
writer. Earlier D5X already identified temporary descriptor writes outside the
original five fences. Current manager bytes remain diagnostics, not the
authoritative geometry frame certificate. No current-state writer census or
new lock is silently assumed to cure that rejected shortcut.

The alternative uses the positively joined **actual generation descriptor**:

1. Provider chooses its descriptor input before `0x14078d660`. That converter
   copies byte `+0x00` and every word `+0x04..+0x28` into its own stack at
   `0x14078d68e..0x14078d6e1`. It separately copies the original Int2 query.
   At `0x14078d6f4` the native normalizer consumes those owned stack copies.
   The Descriptor event records these actual operands, excluding uninitialized
   padding `+0x01..+0x03` from semantic equality. OWN-31.
2. The provider then calls generation synchronously at `0x14079ff18` with an
   actual owner/body scalar and output context equal to the new holder `+0x08`.
   The schema-4 Generating/Generated events preserve the same thread-local
   Descriptor copy. Require that exact source/selection/request/owner/epoch
   chain and actual holder output identity; missing or conflicting joins refuse
   the frame certificate. OWN-09 and the observer's existing normalizer hook.
3. Source origin is a separate explicit generator input, calculated by the
   provider from source anchor/padding and passed in RDX. Generator
   `0x14079b7e8..0x14079b87f` uses that origin for native clip/traversal context;
   per-cell `0x14079a3c4..0x14079a3d7` adds the traversal cell and origin. Region
   bounds and points are copied into the joined holder by the synchronous
   writer chain above. No later resident consumer translates those stored
   points or rewrites them. OWN-01/04/09 and the established
   [D5V coordinate contract](d5v-coordinate-contract.md).
4. Subsequent snapshots may use that generation descriptor only for the same
   positively proved holder/content lifetime: no erasure/reset/destruction,
   address reuse, relevant loss or ambiguous source allocation may intervene.
   The snapshot does not reread a borrowed source or invent an origin at
   holder `+0x08`. A current manager ABA cannot change already owned generation
   evidence or unchanged represented geometry; it can still make a current
   consumer/frame interpretation unqualified and must not be disguised.

Compare exact native points only when these generation certificates agree at
the qualified interior chart-0 scope, with equal body/source geography and
semantic descriptor. Different/absent certificates yield FRAME_MISMATCH or
INCONCLUSIVE; identical numerical points alone do not establish equal geometry.
Unknown original generation clip remains unknown input provenance, not the
fixture's supplied clip. This permits complete content comparison without
claiming a current world transform, current UI membership or equal effective
construction inputs.

## Area traversal completion: two rejected oracles and the native control

Post-release EDX at `0x1421e0aa5` is not the callback result. Native release
loads `0xffffffff` into EDX at `0x1421e0a82`, exchanges it for the prior packed
reader state at `0x1421e0a87`, and can call `WakeByAddressSingle`, which may
clobber volatile EDX. Requiring post-release EDX equal to 1 can reject valid
queries with concurrent readers and can misinterpret unrelated lock state.

An iterator-only replacement is also unsound. After each callback, including
a false return, `0x1421e0a60..0x1421e0a75` increments the iterator and skips
vacant slots. At `0x1421e0a21`, equality with capacity is checked before the
callback result. A false result on the last occupied slot, or one followed only
by vacant slots, therefore reaches `RDI == R12`. The earlier specialist message
claiming otherwise was corrected before qualification; it is preserved as a
failed static interpretation, not a passing oracle.

The supported scan-completion witness is **pre-release EDX equal to 1 and
RDI equal to R12 at `0x1421e0a79`**, joined to the acquired scan and snapshot.
That witnesses completion of the native resident-geometry traversal, before
the shared reader is dropped. It does not claim the whole updater/UI completed.
Cache reuse bypasses this actual scan and cannot manufacture its witness.

The [owned interval method](../../../research/resource-retained-population/d5ai_area_interval_native.py)
executes original traversal `0x1421e09f2..0x1421e0a79` plus the relocated original
release `0x1421e0a79..0x1421e0aa5`. Only the release's RIP-relative imported wake
operand is rebound after relocation; local branch offsets remain unchanged.
Owned entry/exit adapters record registers and an owned callback supplies
positive/false schedules. This is not execution of the whole area updater or
its region predicates.

Final-source `.local-work/d5ai-ownership/area-interval03.json` and
`area-interval04.json` repeat nine controls; development `01/02` remain retained.
They supply single/additional prior reader counts, early false, last-occupied false, false followed only
by vacancies; zero capacity; all vacant; interleaved vacant success; and a wake
that deliberately clobbers EDX. Both last-failure controls falsify iterator-only
completion. Concurrent-reader success returns post-release EDX 3, while the wake
control returns `0xdeadbeef`; both preserve the correct pre-release result 1.
Prior reader counts are supplied native state, not a measured multithread
execution schedule; the original release actually executes against those counts.
The exact final observer must independently exercise its corrected bridge at
that boundary and join the witness to its actual copied population.

### Empty-map owner context after frame rework

The [owner-context rework](d5ai-owner-context-rework.md) records the native
manager owner writer/alias graph and why inner ProcGen-clear fencing alone
leaves a late owner-zero gap. Entire installer `0x140789ce0` and true manager
reset `0x140788e70` require enclosing invalidation, in addition to existing
ProcGen clear/destructor. A previously generated owner/proc certificate can
survive source retirement or Grid clear only with complete observed history
and no context invalidation. Fresh unanchored empty maps remain INCONCLUSIVE.
The separate owner-context source register and eight repeated original-native
branch/store controls preserve the bounded evidence and its coverage limits.

### Prior population storage after map removal

The [baseline ending proof](d5ai-population-ending-proof.md) separates prior
holder resource-map continuity from each prior collection's region/point
storage continuity. Typed endings are `aab10(holder+0x10)` and
`ac260(collection+0x08)`; `aa8a0` is the outer ProcGen map clear. Complete
baseline plus complete ending history can distinguish external holder/collection
survival, partial constituent survival and ended content without following old
pointers. Physical outer-object frees occur later in the caller. Current query
exposure remains a separate observation; empty and unobserved histories retain
their explicit qualifications.
