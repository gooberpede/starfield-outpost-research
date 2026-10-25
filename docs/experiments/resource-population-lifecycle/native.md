# Native ownership, lookup and load evidence

[Report](report.md), [address register](native.csv), [content pins](sources.csv).
All addresses here are preferred static VAs for the pinned executable in the
report, image base `0x140000000`. RVA = VA minus that base. Member offsets are
bytes relative to the explicitly named object. `FUN_` names are analysis labels,
not engine interfaces. These are OBSERVED-INTERNAL mechanisms, not validated
integration points. No runtime module base or native epoch was measured here.

N01–N18 identify bounded claim groups in `native.csv`. Confidence is PROVEN /
STATIC for explicit loads, branches, calls and copied values in those bodies;
semantic ownership interpretation is STRONG where the complete refcount/copy/free
chain agrees. Unmapped callers, aliases and event timing remain OPEN. This
distinguishes code proof from D5B RUNTIME observations and D5A DERIVED predictions.

## Actual consumer back to ownership

N01: `resource-availability-ui-15.tsv`, `0x1421e09d4..0x1421e0aa5`, loads the
singleton at `0x145fd9c30`, then manager `+0x130`, acquires shared ProcGen `+0x40`,
and scans occupied slots at ProcGen `+0x20`, capacity `+0x28`, stride `0x18`.
Slot `+0x10 == 0xffffffff` is unused. At `0x1421e0a46`, the callback receives
the address of slot `+8`, not a producer output aggregate. This reconciles
the consumer entry `0x1421e07d0` with provider `0x14079f860`: different entry
points access the same concrete ProcGen source-map storage. The consumer does
not call that provider in this inspected scan.

N02: `resource-availability-ui-16.tsv`, callback `0x1421e0f50`, dereferences
that holder, traverses its resource map and resolves a resource key to IRES
(native type `0x9f`). Collection count/data select the actual region. D5B's
ACCEPTs qualify this ancestry for its copied selected regions; a callback's
generic successful return is not itself a resource ACCEPT. Region pointer
advancement and resource short-circuiting also prevent a resource census claim.

| Object | Allocation/retention and representation | Final cleanup / qualification |
|---|---|---|
| Source descriptor | Existing index enumerates a pointer; `0x140982d90` initializes definition/geographic fields, separately documented in the [source ledger](../resource-source-enumeration/native.md). This is an input descriptor, not a region holder. | Descriptor allocator/whole-index lifetime is not newly reconstructed; native pointer reuse remains possible. |
| ProcGen | Manager constructor `0x140787830`, call `0x1407886e4`, allocates `0x138` and initializes via `0x14079d660`; manager holds `+0x130`. | Manager destructor `0x140788bc0`, `0x140788d4f..0x140788d66`, calls `0x14079d910` and frees it. |
| Source wrapper | Provider allocates `0x40`, initializes resource hash at wrapper `+0x10`; source slot `+8` retains it. Atomic count at wrapper `+0x00`; slots/capacity at wrapper `+0x20/+0x28`. | Source clear `0x1407aa8a0` decrements; old count 1 calls `0x1407aab10(wrapper+0x10)`, marks count `0xffffffff`, frees `0x40`. |
| Region collection | Generator `0x14079a330` allocates `0x18`; a resource slot retains it. Atomic count `+0x00`; region count/capacity/data `+0x08/+0x0c/+0x10`. | Resource cleanup `0x1407aab10` decrements; old count 1 calls `0x1407ac260(collection+0x08)` then frees `0x18`. |
| Region and points | Append `0x1407ac2f0` allocates a `0x30` region slot; bounds XYZ/radius `+0..+0x0c`; point count/capacity/data `+0x18/+0x1c/+0x20`. Copy `0x1407ac0d0` copies ordered `0x10` XYZ/width values to independent destination storage. | `0x1407ac260` frees each point allocation using capacity times `0x10`, then region storage using capacity times `0x30`. No shallow borrow of the generator temporary on this path. |
| Workshop area result | Callback builds a temporary accepted-resource set, transferred at D5B RVA `0x021e0bf4` to the operation vector. The region arrays remain upstream. | Query refresh/vector retention is distinct from source-map lifetime and from saved Workshop producer rows. |

N03/N06–N08 support allocation and release. A map insertion retains the wrapper
in addition to the provider's local reference; the latter is decremented before
unlock/return without removing the slot. This is direct retention evidence beyond
generic object lifetime. `0x1407a97c0` retrieves a resource collection and calls
`0x1407aabd0` to assign the caller's output holder. That is shallow refcounted
holder sharing, not deep point copying or replacement of the cached entry.
Array append/copy is a separate operation; no copy-on-write predicate is
demonstrated. A complete all-alias writer census is not claimed.

## Lookup and chronology

| Identity dimension | Exact inspected rule | What it cannot establish |
|---|---|---|
| Map key | Provider `0x14079fcc2..0x14079fcd4` passes the address of the selected source pointer to `0x1403499f0`. Full 64-bit slot-key equality at `0x140349ae4`. | Stable identity across source destruction/reallocation, process boundaries or manager recreation. |
| Hash | `0x140349a0a..0x140349ad2`: pointer's eight bytes in low-to-high order through table `0x144d58d70`; initialize `h=T[b0]`, then seven times `h=(h>>8) XOR T[(h XOR bi) AND 0xff]`; bucket `h AND (capacity-1)`. | Hash collision is not equality; no dereference of descriptor, mask or owner participates. Table identity is pinned by executable/export, without copying table bytes here. |
| Collision/absence | Slot `+0x10` links collisions; unused `0xffffffff`, chain end capacity. Lookup returns capacity when not found, including zero for zero capacity. | No timestamp, stale bit, geometry-valid flag or expiry check is present in this lookup body. |
| Visited key | Provider reads source `+0x68`; linear exact eight-byte comparison against ProcGen count/data `+0x48/+0x50`, capacity `+0x4c`, under shared lock. | This guard is distinct from map key; duplicate visited identities across source allocations are not excluded here. |
| Effective context | Provider resolves current manager/context/index/BIOM; query converts using manager mode `+0x20`, descriptor `+0x1c0` if 3, otherwise `+0xc8`; owner argument comes from manager `+0x80`. | Implicit context does not prove every source pointer has one immutable complete recipe. Mask/query/seed are not extra source-map key fields. |
| Research identity | D5B chart/anchor/SFBK plus qualified owner and Workshop identifies the study case. | It is not the hash key, a native generation version or a persistent epoch. |

N03–N05: BIOM-null skips the population block. A visited hit skips the exclusive
lookup entirely. Otherwise acquire exclusive `+0x40` at `0x14079fcb3`, lookup,
compare result with capacity, and branch. Miss allocates and inserts through
`0x1407aa5f0`; generation setup/call occupies `0x14079fe81..0x14079ff18`.
Visited append occurs at `0x14079ff1d..0x14079ff60`, and exclusive release at
`0x14079ff99..0x14079ffa5`. A hit loads slot `+8`, increments the holder count,
then joins local cleanup without calling the generator or appending visited.

Insertion's return distinguishes new slot from existing slot. The provider has
a defensive existing-slot assignment branch: retain new holder, release old,
and free old contents on final release. It follows an earlier miss under the
same exclusive lock; this branch alone does not prove an ordinary concurrent
overwrite, expiry or refresh policy. Hash growth/rehash moves slot ownership;
slots are not stable external handles. Collection retrieval via `0x1407a97c0`
is a separate key-width specialization (resource u32), not source-pointer lookup.

The ordinary mask sampling/admission path remains the [D5 native lineage](../resource-feynman-d5/native.md).
It can change generated geometry without changing the source-pointer key. The
static retention rule therefore makes first-request dependence possible under
the shared-pointer/reachable-query/readiness conditions in the main report.
Neither the first query's identity nor the set of all queries enumerating one
live pointer is measured by D5B. No deterministic concurrent winner is proved.

## Reset, replacement and fences

N08/N09: `0x14079ddf0` clears a related database first, exclusively acquires
ProcGen `+0x40` at `0x14079de83`, clears source holders at `0x14079de8d`, resets
source occupancy bookkeeping and frees/zeros visited storage, then releases the
lock. Separate locks protect other related stores; a final call reaches
`0x1407b4770(1)`. Reset is broader than one source/resource. There is no
demonstrated per-source TTL, LRU or biome-change predicate in these bodies.

The reset thunk `0x14079df60` occupies ProcGen vtable `0x144b3f3a8 +0x18`.
Direct xrefs are thunk/unwind/data entries in the inspected export. This proves
an indirect method linkage, not which load/travel operation calls that slot.
Destruction `0x14079d910` clears/frees the same map and visited storage without a
local `+0x40` acquisition. External owner synchronization remains unknown;
absence of a local lock does not prove a race. Source-index teardown/replacement
and global manager epoch changes need their own association before attributing
a pointer to a unique population lifetime. Complete alias fencing remains open.

## Save and initialization scope

N10/N11/N17/N18 record the exact bounded search, including negative coverage:

1. Inspect ProcGen initialization, provider allocation/insert/generation, reset,
   destructor, collection copy/free and resource retrieval for reads/writes of
   these fields to a save stream. Their inspected bodies establish initialization,
   computation and cleanup; they do not establish a region serializer/loader.
2. Follow the provider's two defined direct callers `0x1407b5160` and
   `0x1407a1940`. The former runs neighbor preparation then provider and publishes
   a task payload. The latter calls provider only when its separate aggregate is
   absent. The [existing task ledger](../native-availability-map/region-lifecycle.md)
   traces registration, dependency acquisition and dispatch wrappers. Those edges
   do not reach an identified Save52 load-completion boundary. An aggregate hit
   and a source-map hit are different forms of reuse.
3. Inspect the actual Workshop saver `0x140f50660` and row iterator
   `0x140f515a0`: saver passes ExtraWorkshop `+0x20`, serializes resource identities
   and object rows. Row stride is `0x1c`, with reference/base identities and 17
   body bytes. This is not the generated collection's `0x30` region/point grammar.
   Inspect loader `0x140f50880` separately, rather than infer restoration from
   save existence. Its decoded Workshop state does not supply a demonstrated
   ProcGen/source-slot/point-array restoration edge.
4. Inspect ProcGen's six exported vtable entries and manager constructor/destructor
   xrefs. Four entries resolve to `0x1402b56d0`, whose complete body is a return;
   the others are deletion and reset. This table is not a demonstrated geometry
   save/load interface. Follow the direct manager-constructor xref to
   `0x141881660`, which installs `Main::vftable`: at
   `0x141881f3d..0x141881f56`, it constructs the manager only when singleton
   `0x145fd9c30` is zero. Its defined caller is `0x141898870` (callsite
   `0x14189a69e`). This establishes a bootstrap owner-creation edge, not
   per-Save52 population construction. The deleting wrapper `0x140788b60`
   calls the manager destructor and conditionally frees `0x210` bytes when
   flags bit 0 is set. Generic manager dispatch, source-index recreation, resource-server scheduling
   and other serializers are not exhaustively reconstructed.

This search is bounded to population ownership and the concrete Workshop/load
lead. No whole-save binary pattern scan, cache reconstruction, broad format
rewrite or game load was performed. An unidentified indirect or alternate stream
path remains a real coverage limit. Geometry serialization is UNRESOLVED, not
CONTRADICTED; recipe/seed persistence and restoration authority are separately
UNCLASSIFIED. Runtime storage duration is TRANSIENT on this owned path, while
generated informational content is RECONSTRUCTED from definitions/context; these
labels do not exclude persistence of equivalent information elsewhere.

To decide load timing, observe target-source materialization or qualified
presence relative to an independently qualified load-completion event, with
manager/source lifetime identity. To decide serialized geometry, additionally
join a stream read/write to these actual fields and a cross-process population;
matching geometry after load alone would also fit deterministic regeneration.
The [draft](next-run-draft.md) separates those questions and grants no live GO.
