# D5P-R3 Grid investigation: bounded offline NO-GO

2026-10-29, Australia/Sydney. [Brief](../../implementation-briefs/CODEX_BRIEF_SOR_RG2_D5P_R3_grid_membership_context_validation_repair.md),
[prior decision](d5p-r3-decision.md), [review](d5p-r3-review.md),
[source ledger](d5p-r3-sources.csv), [held proposal](run-card-d5p-r3.md).

**The native Grid is a dynamically allocated pointer array. Replacing its
observer limit with 512 is unsupported, and removing the limit alone preserves
demonstrable membership errors. Production validation, DLL, schema and readers
remain unchanged. This is a bounded offline investigation, not a completed
engineering repair or a candidate for retail GO consideration.**

| Element | Supported result |
|---|---|
| Question | What native representation and membership guarantees justify removing the R2 coverage barrier? |
| Answer | Count/capacity/data and eight-byte stride are supported. Growth copies then frees old storage before publishing the replacement; append publishes count before the new source slot. No independently checked allocator extent or coherent observer snapshot protocol has been established. |
| Confidence/basis | STATIC for inspected instructions on the freshly pinned executable; PROVEN within disposable fixtures for the stated source-path outputs. These are proposed findings pending maintainer review. |
| Coverage | Ordinary native Grid, inspected allocator and consumer routes; 41 native cases per unchanged/counterfactual build, five timing sizes per build, 25 unchanged-DLL regressions, historical R2 replay and four damaged derivatives. No retail execution or repaired-DLL qualification. |
| Limits | Counterfactual success is altered-source evidence. Allocation aliases and the interposed race are constructed controls, not observed retail events. Complete writer coverage, lock-qualified snapshot safety and consumer-container identity remain unresolved. |
| Next step | Establish a bounded storage-ownership/consistency contract or a separately defined invocation-selection witness before implementing a versioned production repair. Neither route is proved impossible. |
| Publication | Authored work REVIEW-REQUIRED; executable excerpts, raw captures, binary hosts and private receipts LOCAL-ONLY. B6/publication remain on hold. |

## Native facts and alternatives examined

The installed EXE matches SHA-256
`7e9adb1414a8e1b325e5e1f097b9b17b78deb7eebeda37a333351a43a60f9d28`.
All addresses below are preferred static VAs on image base `0x140000000`;
subtract that base for an RVA. They are not runtime addresses.

Three task-owned exports used existing Ghidra state with `-readOnly -noanalysis`.
The final superset is `.local-work/d5p-r3/investigation03/native.tsv`; its command,
reader hash, installed pins and unchanged database hashes are retained beside it.
Earlier exports remain identifiable rather than silently replaced.

The [decision](d5p-r3-decision.md) gives the field/call evidence. Further inspection
found the heap-array growth wrapper `0x1402c5bd0` delegates to `0x1422cba00`.
In the inspected non-overflow growth path, new capacity is the larger of twice
the previous capacity and the requested count. Growth
allocates, copies existing elements, frees old storage at `0x1422cbb13`, then
publishes the new pointer at `0x1422cbb18` and capacity at `0x1422cbb1c`.
The later append helper increments count before its caller fills the source slot.
Thus there is a concrete stale-storage window and a partial-publication window;
512 is one capacity, not a universal representation envelope.

Allocation/free wrappers `0x1402ba260` and `0x1402ba340` dispatch through engine
pool/custom allocator paths. The exports do not establish an observer-safe
allocation-size query. Windows page readability cannot certify the logical
extent of one suballocation. Increasing an inspection bound does not repair this.
The existing loop's `uint32_t i * 8` also requires widened arithmetic before any
very large-count traversal; no billions-of-slots fixture was attempted.

Grid acquire/dedup uses a lock at Grid+`0x5c`. The lock helper `0x1422c8d10`
records an owning thread, changes recursive/waiter state atomically and may wait
indefinitely. Adding a native CALL is inappropriate without a separate safety
proof. Passive lock/header sampling is a plausible alternative. It still needs
relevant writer coverage, publication-order reasoning and independently validated
storage bounds. Equal samples are not an allocator lifetime token. The tests
below do not falsify a future correctly designed reread protocol.

The smaller consumer route was also followed. Provider retains Grid at W+`0x100`,
calls spatial-cell lookup `0x140985870`, materializes enumeration through virtual
+`0x10`, and copies a selected entry into W+`0x38` at `0x14079fa90`–`0x14079fa93`.
Cell helper `0x140988240` delegates to `0x140988ab0`; that helper appends a pointer
to caller-owned chunk storage, allocating `0x108`-byte blocks when necessary.
It is not a side-effect-free membership query. Reading the resulting cursor may
offer a useful invocation-selection witness, but its container ownership, bounds,
aliasing and relationship to complete current-Grid membership need a distinct
contract. No direct helper was called or new hook added.

The rejected production change is therefore the simple fixed-bound increase or
unqualified full scan. The unresolved alternatives are more specific than a
claim that safe observation is impossible. A diagnostic acquisition path that
continues while withholding scientific qualification is also viable in principle;
it would require an explicit schema/reader change because schema 2 uses zero
status to qualify scientific chains. R3 supplies no such candidate.

## Actual native qualification and counterexamples

Reproduce with installed CPython, MSVC/SDK, pinned R1 DLL/host and local evidence:

```powershell
& 'C:/Users/User/AppData/Local/Python/pythoncore-3.14-64/python.exe' -B research/resource-retained-population/d5p_r3_investigate.py new-native-label
& 'C:/Users/User/AppData/Local/Python/pythoncore-3.14-64/python.exe' -B research/resource-retained-population/d5p_r3_qualify.py new-qualification-label
& 'C:/Users/User/AppData/Local/Python/pythoncore-3.14-64/python.exe' -B research/resource-retained-population/d5p_r3_replay.py new-replay-label
```

Each script documents reads, writes, dependencies and target effects. Fresh
labels prevent overwriting receipts. The replay uses the retained qualification01
context stream; it does not claim to consume an arbitrary qualification label.
No network downloads or new external implementation are used.

The [native fixture](../../../research/resource-retained-population/d5p-r3-context.cpp)
includes the actual production header. A second ignored header removes exactly
the `n <= 256` predicate. Both builds interpose `ReadProcessMemory` for a declared
deterministic race; all ordinary reads forward to the real Windows API. This
interposition and the removed predicate are explicit instrumentation differences.
The counterfactual is unsafe experimental source, never a production DLL. Both
same-path `/Brepro` rebuilds are byte-identical; compiler logs retain MSVC
19.51.36256.0. The SDK selection was not separately captured, so fully pinned
cross-environment reproduction remains incomplete. No cross-toolchain
reproducibility is claimed.

| Control | Actual result and qualification |
|---|---|
| Counts 0/1/255/256/257/324/512/1024 | Early/middle/last hits and full-array absence execute. Unchanged production rejects every count above 256 at reason 24; zero count yields reason 22. The counterfactual reaches reason 0 for hits and 22 for absence, including 324/512. |
| Later predicates | Unchanged and counterfactual one-member contexts independently reject retained/current Grid mismatch at 26 and lifetime hazard/broken state at 23. Counterfactual large positive cases reach all later checks; large negative versions of 26/23 were not separately exercised. This does not qualify repaired-production AC4. |
| Malformed/unreadable | Count 2/capacity 1 rejects at 19; null/out-of-domain storage rejects at 21. A protected second page fails at 21 even after an earlier matching slot. Failed reads retain returned/requested lengths; failure is not an observed zero member. |
| Readable allocation alias | A fixture-owned page contains a logical one-slot array followed by a distinct logical slot with the source address. Corrupted count/capacity 2/2 is accepted at reason 0. This is a missing logical-extent check, not a real retail heap observation. |
| Reallocation interleaving | After the storage pointer is copied, the fixture publishes a new two-slot array retaining the source and overwrites the old readable slot. Both builds return reason 22 from the stale array. The epoch is unchanged because append has no existing fence. This falsifies the simple scan's negative, not every possible guarded strategy. |
| Eleven-hook DLL regression | The unchanged DLL executes 25 actual disposable cases: ordinary, nested/concurrent, ABA/reset/clear/retire, one/many queue/contention losses, cross-gap/fence/in-flight loss, post-gap recovery, unpaced hooks/transport, crashes and five late output faults. Receipt reductions and native exits satisfy their enumerated oracles. |
| Historical reader and damage | The original R2 reduction replays identically after JSON key normalization. Torn tail preserves 16 authenticated diagnostics; first-frame corruption and torn ACK qualify zero; wrong DLL refuses. Original R2 bytes and first-failure reason 24 remain unchanged. |

The native regression runner uses four independent processes concurrently.
Fixture source/manager mutation is confined to disposable models. Its concurrency
and ABA regressions retain the original qualification scope; historical
partial-generation controls were not newly rerun here, and
they do not reproduce every retail mutation or natural CAS-exhaustion timing.
General unwind, genuine allocator reuse and a full safe large-array adversarial
matrix remain unqualified. No passing integrity check supplies those semantics.

The initial replay comparison failed because in-memory reason-map keys were
integers while JSON disk keys were strings. The failed source is retained at
`.local-work/d5p-r3/replay01/failed-source.py`. Normalizing through JSON before
comparison produces exact equality in replay02; no historical result changed.

## Performance and recorder consequences

Each timing distribution contains 1,000 QPC-measured calls, includes capture/read
overhead and excludes DLL recorder work. Units are microseconds. Production's
large-count timings measure early rejection, not successful inspection.

| Count | Production mean / p99 / maximum observed | Counterfactual mean / p95 / p99 / maximum observed |
|---:|---:|---:|
| 1 | 2.3944 / 2.5 / 3.3 | 2.4031 / 2.5 / 3.0 / 5.3 |
| 256 | 34.2356 / 39.5 / 54.5 | 33.6736 / 34.4 / 35.2 / 65.9 |
| 324 | 2.0152 / 2.1 / 2.7 | 41.8322 / 42.7 / 43.4 / 61.9 |
| 512 | 2.0157 / 2.1 / 2.6 | 65.2409 / 66.7 / 90.8 / 100.3 |
| 1024 | 2.0146 / 2.1 / 2.7 | 128.643 / 130.6 / 172.6 / 208.7 |

Measured maxima are not universal bounds. O(n) RPM calls are a material trade-off,
and u32 metadata permits unacceptable work if simply uncapped. No arbitrary
replacement count, run-wide record quota or capture-byte cap was introduced.
The source fixture emits 41 JSONL case rows plus five timing summaries per build,
not scientific recorder events. The unchanged-DLL stress reductions retain actual
admitted bytes/drop pressure in qualification01/dll-regressions.json. Unpaced
eight-producer hooks retain 2,058 records (3,177,552 bytes), 99,709 queue-full
losses and 506 intact-epoch fixture chains. Unpaced transport retains 2,058 records
of the same byte length, 4,291,734 queue-full losses, one contention-exhaustion
loss and one fresh post-gap chain. Both reach scheduled STOP without output
failure; these saturated 250 ms requested producer intervals are fixture load,
not a measured retail burst rate. There is no
measured new large-Grid DLL throughput because no new DLL exists.

## Safety, scientific state and disposition

Installed input hashes, original production source hashes, R1 binary identity,
selected Phase B/R1/R2 local evidence and database state were verified. Both
caller-available disk floors exceed 40,000,000,000 bytes. No protected-save audit
was newly run: originals were untouched, and this is not a newly established
whole-save equality claim. No game/SFSE/Steam launch, deployment, Vortex change,
save/configuration write, debugger attachment, staging, commit or push occurred.

R2 still authenticates 9,736 admitted records, 6,101 reason-24 demands and 5,190
queue-full losses. Its membership/invocation-Grid/final-lifetime checks were not
reached. Original D5P Phase B's 319 failures remain historically unexplained;
the selected-source construction–retention–reuse hypothesis remains UNRESOLVED.

R3-AC3 is FAIL for production repair and R3-AC4 is NOT TESTED at repaired-production
scope. No candidate DLL, deployment ZIP or executable retail card is issued.
The [review matrix](d5p-r3-review.md) distinguishes accepted investigation closure
from unfinished engineering gates. The smallest missing capability is an
independently justified storage-ownership/coherence witness, or an explicitly
versioned diagnostic/consumer contract that cannot promote uncertainty to a full
chain. A future implementation must qualify that choice before retail GO
consideration. The held card is preparation only; no R3 outcome authorizes retail.
