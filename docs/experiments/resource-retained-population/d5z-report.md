# D5Z visited-state origin, reset and capacity

2026-10-31, Australia/Sydney. [Original brief](../../implementation-briefs/README.md#archive-lookup) (`implementation-briefs.zip :: docs/implementation-briefs/CODEX_BRIEF_SOR_RG2_D5Z_visited_state_persistence_reset_capacity.md`),
[state transitions](d5z-state-transition-map.md), [active ledger](d5z-investigation-ledger.md),
[sources](d5z-sources.csv), [gameplay checklist](resource-generation-gameplay-checklist.md)
and [review](d5z-review.md). Final acceptance is governed by the exact-snapshot
review record, separately from integration and publication.

**The visited array is transient ordinary ProcGen state, cleared by ordinary
full-load handling and populated by subsequent source-generation attempts.**
Saved context/world inputs are restored separately; destination streaming can
inherit visits already produced by earlier post-reset demand. Load completion
or pressing fast travel therefore does not establish a cold target.

Visited state and retained geometry have different lifetimes. A source's
derived eight-byte token can suppress construction before any pointer-map
lookup. Retirement removes the source's map entry while leaving visited alone;
a qualifying broad reset releases both stores. Load has a positive serialized
context/compatibility path into reset handling. Neither that path nor B1's two
empty-state reset witnesses identifies the target's historical append or mask.

| Element | Supported answer / current boundary |
|---|---|
| Frozen question | D5Z-CQ and Q1–Q5 unchanged: representation/census, persistence/load origin, reset causality, capacity/failure and B1 consequences. |
| Confidence | PROVEN / STATIC for scoped compiled branches, ordinary receiver/writer/load closure and arithmetic; SAVE for verified controlled-copy fields; disposable native execution for six reserve controls; RUNTIME for previously captured B1 records. Architectural purpose is INFERRED. |
| Tested coverage | Freshly pinned Starfield 1.16.244.0 executable/ESM/PlanetData, SFSE/loader and existing Ghidra state; read-only native exports/PE guards; ordinary ProcGen receiver and module graph; allocator recovery through bound cell cleanup; controlled Save52 header/type-3 fields; unchanged B1 evidence/readers. |
| Unknown coverage | Exact B1 target identity/append/constructor and worker history; actual retail OOM behavior, arbitrary plugin/memory corruption, nonordinary receiver substitution and other builds. No universal safety or collision-free identity claim. |
| Evidence | Exact exports, local receipts and source windows in the source ledger; B1 raw/archive and Save52 hashes below; investigation ledger records failed interpretations. |
| Completeness | The original ordinary native/save question is answered by positive constructor/writer/reset/load paths and a bounded receiver/dispatch argument, not by token search failure. B1's retained evidence supplies a scoped non-identifiability result, not a historical winner. |
| Next action | Maintainer critical review of the independently accepted package. A new live observation remains separately unauthorized. |

| Frozen question | Accepted result within the declared scope |
|---|---|
| Q1 | COMPLETE at the ordinary pinned receiver/field scope: token, layout, reader/writers/clearers, growth, locks and relevant aliases are accounted for. |
| Q2 | COMPLETE at the ordinary native/save-schema scope: transient visited storage, load clearing and separate restored inputs; actual B1 post-reset demand order remains unidentifiable. |
| Q3 | COMPLETE at the ordinary caller/module/recovery scope: lifecycle predicates and cleanup effects mapped; no dedicated size/pressure reset policy in the audited route. |
| Q4 | COMPLETE for compiled allocation/control semantics: dynamic capacity, exact payload arithmetic, conditional failure and wrapping behavior; no invented safe maximum. |
| Q5 | COMPLETE as a conditional state model and retained-evidence insufficiency result: B1 cannot identify historical target append/query/mask. |

## Representation, identity and synchronization

The normal ProcGen constructor `0x14079d660` initializes the 16-byte visited
control block: u32 count at `+0x48`, u32 capacity at `+0x4c`, eight-byte data
pointer at `+0x50`. Each member occupies eight bytes. This is distinct from
the full source-pointer-keyed retained-population map at `+0x10` and from the
manager's ProcGen pointer at manager `+0x130`.

The [state-access table](d5z-state-access.csv) distinguishes the source-token
producer, actual visited reader/writer/clearers, bound allocation helpers and
source retirement. Its addresses select exact instruction windows in the
source ledger; equal numeric offsets in another receiver are not these fields.

Coverage begins at actual manager construction/ownership, registered module
storage and every relevant escaped ProcGen receiver, then follows the array's
bound allocation callbacks. A whole existing-listing `+0x130` candidate scan
and singleton-reference inventory are disambiguated by receiver, operand width,
call and callback binding. The initial local function-range census was
insufficient: it missed undefined wrapper `0x14079a310 → 0x1407a5790` and
captured functors outside that range. Those paths were then exported and traced.
The nonlocal methods traverse retained geometry or presentation/reference state;
functor clones copy their small captured-pointer storage, not the ProcGen array.
PE-backed vtables and RTTI corroborate the receiver classes.

The resulting ordinary visited mutations are constructor, provider reserve/store,
bound allocation/growth helpers, reset and destruction. Other numeric-offset
matches resolve positively to unrelated globals, transforms, tree fields or
subobjects. No array copy, per-member erase, deserializer or alternate ordinary
membership writer remains in that receiver graph. This is a bounded compiled
class/alias argument, not a whole-program symbolic proof against arbitrary
computed pointers, substituted vtables, corrupt state or injected writers.

Source creation `0x140982d90` constructs a content/path-derived token and
stores it at source `+0x68` (`0x1409830c9`). This is not a pointer, FormID,
serialized identifier or player-visit counter. Its identity is derived from
source descriptors/content and a generated file path; collision properties
must not be inferred from its eight-byte width alone.

The provider scans those eight-byte values under shared ProcGen `+0x40`
protection. On equality it bypasses the construction block before map lookup.
On inequality it releases shared protection and separately acquires exclusive
protection for the pointer-map decision. There is no second visited scan under
that exclusive interval. A map hit jumps to `0x14079ff64`, skipping generation
and append; a miss reaches generation and then the append attempt. Holder
allocation, successful geometry, successful copying and successful visit marking
are separate outcomes.

The append helper `0x1422cc0d0` returns an old index and increments count when
capacity suffices. Otherwise it calls the concrete allocation/growth callbacks;
a false result returns `0xffffffff`, and the provider skips the token write.
Visit marking follows the generation attempt without testing complete geometry
success. Neither a visited hit nor an empty-state reset proves a nonempty retained
population. Destruction assumes lifecycle exclusion; it must not be described
as acquiring the same internal lock as ordinary lookup/reset.

Six disposable-process controls execute the original reserve helper with
synthetic recording callbacks. Below-capacity cases return the old index and
increment count; false initial/growth callbacks return the sentinel and preserve
count; true callbacks permit reservation. The callbacks do not allocate array
backing, so this validates reserve-helper control flow, not real allocation,
retail memory exhaustion or the complete provider. The local receipt is
`.local-work/d5z/append-01/control.json`; no game process is involved.

A visited epoch here means the interval from construction/clear to the next
qualifying clear/destruction, not an engine epoch field or observer epoch number.
Retiring source-map entries does not prune visited values on the inspected path,
so processing further distinct tokens can accumulate entries in that interval.
Capacity growth is not eviction. A broad reset releases the allocation, rather
than retaining its capacity for a later count-only reuse.

## Capacity and allocation

Normal initial allocation has minimum capacity 4. Growth selects the unsigned
maximum of requested count and twice the old capacity, using 32-bit arithmetic.
Count reservation also increments a u32 without a separate overflow guard; the
counter's bit width is not a logical maximum-entry contract.
The callback allocates a new buffer, copies the old used values, frees the old
buffer and publishes the new pointer/capacity only after successful allocation.
On a returned null allocation the old buffer remains intact and append can fail.
The real backend `0x1422c7ad0` tries selected/fallback heap allocators, calls
`0x1422c8200 → 0x14186dfc0` recovery, and can retry. TLS `+0x1eb` permits
a null return after failed attempts; without that permission the inspected
loop can continue. Heap absence takes a CRT allocation route. With a configured
heap, a zero-byte request returns `qword[0x145fb5968]`. Thus the helper's clean
failure result is conditional on the backend returning null; it is not a
promise of prompt or safe handling of actual retail memory exhaustion.

For representable byte products, used payload is `8 × count` bytes and allocated
payload is `8 × capacity` bytes, plus the 16-byte control block and allocator
overhead. Growth temporarily holds both old and new buffers, so the payload
peak is `8 × old_capacity + 8 × new_capacity`, not just the new allocation.
These are requested/retained payload calculations, not measured working set.

Multiplication by eight occurs in 32-bit operands, without a local overflow
guard in the inspected append/growth helpers. Under an uninterrupted successful
doubling sequence, capacity 268,435,456 requests 2,147,483,648 bytes; the next
capacity 536,870,912 has a byte product that wraps to zero. That is an arithmetic
threshold, **not a proven reachable entry maximum, safe memory bound or retail
bug**. A pool cutoff is not the general allocator limit. No inspected growth
branch invokes ProcGen reset. The separate caller/alias and recovery analysis
below establishes the scoped reset conclusion. These wrapping products are not a
well-defined large-array contract, and the zero-size backend behavior does not
turn the wrap threshold into a valid larger allocation.

## Reset causality and lifecycle purpose

Manager reset `0x140788e70` drains outstanding work, acquires manager exclusive
protection and dispatches registered module slots `+0x10`, then `+0x18`.
The actual ProcGen table is `0x144b3f3a8`; its `+0x18` target
`0x14079df60` calls `0x14079ddf0`. Later module `+0x20` notification is a
no-op for ProcGen and must not be mistaken for its reset. Landscape's earlier
registered callback can retire/release source Grids before the ProcGen clear.

The false reset variant `0x140789850` also dispatches the reset slots and clears
visited state. Consequently, the same-owner/same-component branch of
`0x140789ce0` does not establish visited retention: it can take that false variant.
Other positive reset callers cover owner zero/change, component mismatch,
world/context transitions, subsystem teardown, global load/revert and full game
reset. [The caller/predicate map](d5z-state-transition-map.md#reset-callers-and-predicates)
records their exact conditions, direct ingress and apparent DATA-reference
exclusions. Actual module-vector loops are distinguished from numeric-offset
coincidences; chained unwind RVAs are not callable pointers.

Under valid native structure invariants the ProcGen reset clears retained
wrappers, frees the visited allocation and zeros count/capacity/data. The
free/zero block is conditional on nonnull data; this does not prove repair of
malformed null-data/nonzero-count state. Other ProcGen maps and downstream
request state have separate cleanup after that primary exclusive interval.
Reset enables a later qualified construction; it does not itself generate output.

Coherent context replacement and lifecycle cleanup are architectural-purpose
inferences supported by these predicates/effects. A memory-pressure recovery
purpose would need an actual pressure predicate and reset edge. Removing visited
memory during reset is an effect, not proof that memory usage caused the reset.
Source retirement's different lifetime does not establish a gameplay defect.

Generic allocator recovery is a real competing path, not omitted from that
conclusion. Its main-thread phase 5 calls `0x14057a3d0` and, on a false result,
calls `0x140579cc0`, reaching cell/world-cache cleanup. The TES clearing
helper `0x14057fc40` clears TES `+0x188` directly and releases its separate
`+0x190` LoadedCellDB entry. It does not call changed-component setter
`0x14057fce0`, whose nonnull/different-input predicate can reach broad reset.
The manager separately retains its world-owner handles.

Actual LoadedCellDB entry/cache callbacks are bound through PE vtables/RTTI,
deferred release, eligibility guards, `0x140596dd0` cell unloading and typed
Cell destruction. The final worldspace removers `0x140bbe590/0x140bbe250`
remove cell membership under worldspace `+0xc0`; they do not free/install a
world component or dispatch ProcGen reset. This closes the concrete recovery
alias that a flat direct-call search would miss. Recovery can still service
independently eligible engine work, whose normal lifecycle predicates may cause
reset. The result is **no dedicated visited-count/capacity/pressure reset policy
in the audited ordinary route**, not “OOM can never precede reset.”

| Purpose hypothesis | Supporting / contrary compiled evidence | Disposition |
|---|---|---|
| Context compatibility | Owner/component/world transition predicates; reset before branch-specific installation and rebuilding | Supported operational explanation; rationale remains inferred. |
| Load/reload/teardown reinitialization | Complementary ordinary load clears; false variant also clears; teardown destroys singleton | Positive mechanism. Exact historical B1 caller still unknown. |
| Failure/memory-pressure recovery | Allocator has recovery and cell/heap reclamation; bound cleanup does not add a dedicated ProcGen reset | Recovery exists, but pressure as the reset policy is not evidenced. Independently eligible lifecycle work remains conditional. |
| Visited memory reclamation | Reset frees the allocation and zeros capacity under valid native state | Positive effect, not proof that memory pressure caused reset. |
| Maximum-entry enforcement | No visited size test or reset edge in append/growth or audited reset predicates; byte/count arithmetic can wrap | Dedicated cap/reset policy unsupported; dynamic does not mean unlimited or safe. |
| Retirement equals broad reset | Retirement erases pointer-map entries without touching visited | Contradicted at the complete inspected retirement body. |

## Persistence and load

Native global-type-3 loading is a positive dependency, not an unsuccessful
serialization search. `0x141824020 → 0x141825e00`, case 3, reaches
`0x141825ac0 → 0x1407896d0`. The manager reads an eight-byte saved context
value and, for version at least `0x3e`, a four-byte compatibility value. Its
comparisons, when `bAvoidClearOnReload` is nonzero, influence the flag forwarded
to reset wrapper `0x1407895a0`; when that setting is zero, this loader skips the
wrapper. Once called, the wrapper invokes broad reset for either flag. These prefix values
are not a serialized visited list.

LoadGame `0x141815620` first has a drain and later calls the global-revert
range helper `0x1418278c0(0,17,0)`. Type 3 dispatches reset under
`!byte[0x145e8fd70] || phase_flag`. InitGlobalData's type-3 branch is a no-op;
FinishLoadGlobalData's type-3 branch waits for a service. Bootstrap constructs
the singleton only if absent. These compiled stages must not be substituted
for exact timestamps or complete actual Save52 execution.

For an ordinary valid full load with the reload setting stable, the branches
are complementary: setting zero clears through the pre-load revert; setting
nonzero clears through the type-3 manager loader even when compatibility selects
a false flag. The effective setting value is not newly measured. A drain alone,
a setting name or compatible saved context would not establish this result;
the actual module thunk's ignored flag and both call paths do.

The paired global writer `0x141824a60`, case 3, emits the resident world's
packed key at component `+0x310` and the CRC-derived Overlays compatibility
value from `0x140798130`. It then writes generated-world descriptors through
`0x14132d260`, two auxiliary overlay-ID lists through `0x140ad6cb0`, and typed
`PlanetWorldSpaceData` through `0x1403a6ae0`. The corresponding load tail uses
`0x14132d500`, `0x140ad8930` and queued
`0x1403a7eb0 → 0x1403a74e0 → 0x1403a7cc0`. The last leaf restores one u32
per typed entry into its distinct component `+0x10`; it does not restore a
ProcGen array. Saved worlds/context remain indirect inputs to later source
creation and demand, rather than saved visit membership.

Earlier [EXP0020 notes](../static-exhaustion/trace-notes.md) described the
comparison as a “reset/reuse argument.” That shorthand is now qualified:
the false flag can change other manager/landscape cleanup, but the registered
ProcGen reset still clears visited storage. Earlier evidence/wording is
preserved; this is a scoped correction, not a rewrite of those observations.

Justified read-only inspection used the existing controlled copy of Save52,
16,411,136 bytes, SHA-256
`6b4a10084c7e752c31fd2de121a00850aaa2bf1decd700b437d7dccfcdbc82e8`.
The verified decoded stream has SHA-256
`e3c0dc34cbbdcd26bb85d212fc458378b44404b37a5f54b635070e03e1565b93`.
Save52 has header structure version 27 at decompressed offset `0x10` and native
buffer-version byte 153 at `0x14`. Header reader `0x141830550` reads that byte
for structure version at least 25, stores file-object `+0x110`, and
`0x1418240c7` copies it into global reader `+0x28`. Thus the `>= 0x3e`
compatibility-u32 branch is established for this sample without inferring a
save format from the present executable's build string.
The global-type-3 envelope begins at decompressed offset `0xe8b`; its payload
begins at `0xff5`, length 2,228 bytes, with 176 string references. The 12-byte
prefix is followed by 88 grounded world-descriptor rows; their array ends at
`0x152d`, leaving 892 bytes for the later overlay/component payload. Independent
one-shot selected-block decompression agrees with the complete inspected prefix
and descriptor span. The remaining tail is characterized by its native
writers/readers above; this task does not claim to have decoded every tail byte
of this save. The absence of a visited restore depends on the receiver/writer
census and native load paths, not on searching these bytes for a token list.

The [save method](../../../research/resource-retained-population/d5z_save.py)
reads only the pinned copy, uses the owned streaming/framing readers and removes
its temporary decoded mmap. Exact numeric fields and tokens stay in
`.local-work/d5z/save-04/save-prefix.json`. Original/protected save bytes are
unchanged. Existing world/descriptor restoration is an indirect input to later
source creation; its distinction from restoring the visited array is mandatory.

## B1 consequences and checklist correction

[The transition map](d5z-state-transition-map.md#b1-checkpoint-and-reset-evidence)
re-evaluates actual B1 boundaries. Two matched empty-state certificates exist,
not just reset-site counts. The first is inside the 110-record pre-travel
watermark; the second is after it. The 119 conditionally target-compatible
bypasses occur later, beyond the first loss boundary, without copied target
identity or a joined append. They cannot nominate a historical constructor,
ordinary mask or persistent origin. Zero qualified cold-first chains is a
coverage result, not target nonexecution.

With valid ordinary source/object state and the closed writer graph, a genuine
visited hit requires an equal token successfully appended after the most recent
qualifying clear. It is not direct restoration of old visited-array contents.
That prior append follows a returned generation attempt, which may be partial
or unsuccessful; token hash collisions and source identity are separate questions.
B1 does not capture the target's token bytes or effective Grid/frame at those
bypass-only selections, nor the complete prior access history. Thus this stronger
native explanation excludes literal list restoration within its scope without
identifying the historical source/query/mask or hiding D5Y's attribution premises.

All 31 supplied checklist items are preserved in the five required flat groups.
Each line now links evidence and distinguishes a mapped native mechanism from
an actual B1 event. The full definition/data-loading item is corrected to unchecked;
claims about complete extractor placement, successful geometry copying and
unconditional visit marking are narrowed to the demonstrated operations.
Existing open player-action/ordering questions
remain unchecked; no visual match becomes a historical geometry oracle.

## Reproduction and delivery boundary

Task-owned scripts document reads, writes, dependencies and effects. From the
repository root, with fresh destinations and installed CPython:

```powershell
python -B research/resource-retained-population/d5y_forensics.py FRESH-D5Z-FORENSICS
python -B research/resource-retained-population/d5z_b1.py .local-work/d5y/FRESH-D5Z-FORENSICS .local-work/d5z/FRESH-B1
python -B research/resource-retained-population/d5z_save.py .local-work/d5z/FRESH-SAVE
python -B research/resource-retained-population/d5z_append_control.py .local-work/d5z/FRESH-APPEND
python -B research/resource-retained-population/d5z_figures.py docs/experiments/resource-retained-population/d5z/graph-data.json .local-work/d5z/FRESH-FIGURES
```

Local native exports, captures, saved tokens, rendered PNGs, tools and databases
remain LOCAL-ONLY. Authored reports, diagrams and small derivatives are
REVIEW-REQUIRED; nothing here clears publication. No game launch, attachment,
deployment, Vortex/configuration change, protected-save write, database edit,
staging, commit or push is performed. D5R remains OPEN and B6/publication ON HOLD.
