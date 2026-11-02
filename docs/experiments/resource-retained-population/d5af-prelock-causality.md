# D5AF visited-to-map causality

**The shared check does not reserve construction order. The exclusive helper
uses a packed count and a competing compare-exchange, not a writer ticket.**
B2's earlier visited timestamp precedes neither a measured exclusive attempt
nor a measured acquisition. This identifies a precise missing execution edge:
the relative order of callback return, exclusive registration and successful
ownership compare-exchange for the two requests.

All addresses below are preferred static VAs for Starfield 1.16.244.0, image base
`0x140000000`. Member offsets are bytes. Primary instructions remain LOCAL-ONLY:
`.local-work/d5q/export01/native.tsv`, provider `0x14079f860`, and fresh
`.local-work/d5af/prelock-export01/native.tsv`, functions `0x1422cc350`,
`0x1422cc3d0`, `0x1402c45a0`. The [source ledger](d5af-sources.csv) supplies hashes
and exact export windows. [D5AE](d5ae-scheduler-causality.md) supplies the traced
upstream graph; this investigation follows its material admission gap.

## Instruction and ownership graph

| Boundary | Exact operation | Ownership and possible intervening work |
|---|---|---|
| Provider prefix | Source BIOM/remap, temporary collection allocation, source token read at `0x14079fc37` | These precede the shared visited decision. They cannot be a geographic computation placed between its timestamp and map lookup. Grid retention alone does not protect the individual raw source. |
| `0x14079fc45` | Call shared helper `0x1422cc350` with ProcGen `+0x40` | Helper increments low reader count at lock `+0x04`; waits while exclusive bits are set unless current thread is owner. |
| `0x14079fc4a..0x14079fc74` | Linear scan of visited tokens at ProcGen `+0x48` | Shared ownership protects the scan. Token is source `+0x68`, not the full source-pointer map key. |
| `0x14079fc85..0x14079fc9d` | Atomic reader decrement; conditional imported wake | Wake condition tests remaining reader/exclusive bits and pending writers. The imported target is `WakeByAddressSingle`; no exclusive ownership is transferred by this call. |
| `0x14079fca3` | Visited bridge; native `TEST SIL,SIL` / bypass decision | B2 instrumentation executes here, after shared release. `visited_capture → emit` timestamps before enqueue CAS and event publication. Register/flag/vector restoration and the displaced stack store still precede native continuation. |
| `0x14079fcac..0x14079fcb3` | Save lock pointer and call exclusive helper | No raster, query conversion, geographic comparison, task reprioritization or resource generation lies in this native interval. A thread can be delayed in the callback, its return gap or helper. The capture has no timestamp for these boundaries. |
| `0x1422cc3ed..0x1422cc3f2` | Current-owner comparison; recursive count increment | Same-thread recursive ownership bypasses the ordinary contender loop. B2 contenders are different threads, so they cannot both be this same owner. No captured nested provider call establishes this as their deciding path. |
| `0x1422cc410` | Add `0x1000` to packed lock state | Registers a pending/existing writer count. This is not an ordinal or ticket. |
| `0x1422cc420..0x1422cc431` | Test `state & 0xffc00fff`; CAS in `0x00400000` | Pending-writer bits `0x003ff000` are excluded from the blocking predicate. Multiple pending writers can compete for the ownership CAS when reader/exclusive bits clear. Registration order does not select the winner. |
| `0x1422cc450..0x1422cc486` | Reload, bounded spin, `PAUSE`, imported `WaitOnAddress` then retry | After 100 spins, the wait compares four bytes of lock state with infinite timeout. Wake/return alone does not grant ownership; the CAS still decides. B2 does not record spin counts, wait calls or outcomes. |
| `0x1422cc48f..0x1422cc492` | Store current thread as owner; `MFENCE` | Exclusive acquisition has succeeded. Native map work follows in the same call chain. |
| `0x14079fccb..0x14079fcd4` | Pointer-map lookup; compare with capacity sentinel | The actual constructing miss decides authority for a stable owner/source allocation. There is no second visited check. |
| `0x14079fdf9..0x14079ff60` | Insert holder; convert original query; generate; reserve/store visited token | All occur while exclusive ownership holds. Allocation/metadata/raster failure is not synonymous with another request gaining authority. Returned empty output can still leave a holder and visitation. |
| `0x14079ffa5 → 0x1402c45a0` | Exclusive release | Final release clears owner, subtracts `0x00401000`, then wakes all if readers exist or one if other writers remain. Recursive release subtracts only `0x00400000`. No successor request identity is selected by geographic key. |

The same lock protects the visited scan and map path, in **separate acquisitions**.
Incoming readers test exclusive bits `0xffc00000` at `0x1422cc36a`; pending
writers alone do not block them. Thus a reader cohort can delay pending writers,
and a later writer can compete before an earlier pending writer runs its CAS.
These are positively evidenced admission rules, not a claimed retail fairness
distribution or a measured explanation of B2's particular wait history.

## Authenticated B2 constraints

Fresh reconstruction `.local-work/d5ac/d5af-reconstruction01` independently
decodes all 32,141 frames, verifies CRC/sequence and original reader agreement,
and retains three damaged-input refusals. It preserves 97 adjacent admission/QPC
inversions and zero qualified cold-first chains. The
[D5AC chronology](d5ac-target-lookup-chronology.md) gives full original operands.

| Sequence | Invocation / thread | QPC ticks | Supported meaning |
|---:|---|---:|---|
| 8006 | 3837 / 42984, `[4,-1]` | 3761445485668 | Unvisited event stamped after shared release. |
| 8020 | 3844 / 44268, `[5,0]` | 3761445496360 | Same source also unvisited. |
| 8091 | 3844 / 44268 | 3761445560087 | Protected miss, result/capacity 64/64. |
| 8094 | 3844 / 44268 | 3761445560191 | Ordinary sample `0x3`. |
| 8106 | 3844 / 44268 | 3761445576040 | Matching token store after generation/reserve. |
| 8339 | 3837 / 42984 | 3761445739159 | Protected hit, slot 18/capacity 64. |

Both requests use owner, full source pointer, allocation 932, epoch 207 and
identity `0:37536:20928:0029d20e`; birth/publication 2074/2075 precede them.
No target replacement, source retirement or reset is recorded between them.
The actual QPC order and exclusive interval require insertion/construction before
the hit. The durations 253,491 and 63,727 ticks are stamp-to-lookup elapsed
intervals at 10,000,000 Hz, **not lock-wait measurements**.

Fresh controls identify same-owner protected decisions for other sources at
8054, 8069, 8081, 8090, 8113, 8142 and 8184 between the target's stamps and final
hit. They establish real competing work on the owner-wide map lock. They do not
show where either target thread was delayed. Treating this lock as source-local
would omit a material contender class.

## Tested distinctions and unresolved historical edge

Earlier check, first registration, same priority and pending-writer registration
are each weaker than first successful exclusive ownership. The native admission
predicates explain how overtaking is permitted. The call-level controls also
hold the recorded order fixed while moving A's callback return, proving that the
observations do not identify callback duration versus later pre-call delay.
This is a synthetic discrimination test, not an invented historical clock.

Two additional measurements would distinguish the material historical branches:
exclusive-call entry/registration relative to both visited callbacks, then the
successful ownership transition. If A enters after B has acquired, the deciding
delay lies before admission. If A registers first and B wins, the helper's
non-ticket admission is exercised. Read/writer counts and wake/wait events then
distinguish an active reader cohort from exclusive-holder competition. B2
recorded none of these operands. Static code and replay cannot recover their
historical values. This precise unknown meets Q1's allowed missing-edge answer;
it does not prove the primary stabilization hypothesis or a usual retail winner.

## Interrupted and detached work

A suspended constructor retains exclusive ownership across insertion, generator
and store. The helper has no elapsed-time takeover or abandoned-writer branch;
wait returns feed the ownership predicate again. The contended native controls
hold a foreign-owner state until an explicit release transition, then require
the original helper to acquire. This tests the lock consequence of interruption,
not exception unwinding of the full generator. Safe recovery from an exception,
invalid source dereference or holder allocation failure is not established.
These failures cannot be relabelled an ordinary stabilizing successor policy.

Density work detached from the preparation reader retains Grid rather than an
individual source reference. D5S's independent retirement witness remains a real
invalid-lifetime counterexample. Grid clear/removal can erase the map while
retaining the visited token; broad reset clears both. B2's authenticated fences
exclude these transitions between its target decisions. A new allocation at an
equal address needs birth/token/owner requalification; pointer equality alone
does not preserve the competition domain. Reentrant ownership is measured by
actual owner TID and depth, not inferred from a zero observer parent ID.
