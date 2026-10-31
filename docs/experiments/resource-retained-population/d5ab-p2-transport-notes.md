# P2 transport investigation notes

2026-11-01, Australia/Sydney. P2-Q1 and P2-AC02 transport workstream.
The [P2 contract](../../implementation-briefs/CODEX_BRIEF_SOR_RG2_D5AB_P2_controller_reducer_transport_qualification.md)
governs this bounded engineering work. These queue tests cannot alone close the
integrated recorder/ACK/controller contract. B2 NOT AUTHORIZED; D5R OPEN.

## Checkpoint 1 — independent admission oracle and contention counterexample

The existing queue stress source checked sequence, uniqueness and total losses,
but did not compare every observed ID to each producer's successful emit result.
The new overload oracle compares each producer's entire successful admission list
to its observed list, including order. It retains 96,000 unpaced offers.

The first proposed lossless workload used eight concurrent producers and 200
rounds of 48 records per producer. Barriers limit outstanding traffic to 384,
below every tested capacity. It nevertheless loses records through the queue's
32-retry contention bound. Queue capacity alone cannot solve that failure mode.
No production retry or queue semantics changed.

| Attempt | Preserved primary evidence | Outcome |
|---|---|---|
| `.local-work/d5ab/p2-queue01` | Generated source, build log, executable, first stdout/stderr | Disposable host aborted without a diagnostic; a direct replay of that executable returned `3221226505`. An uncaught producer-thread oracle is the supported interpretation, corroborated by attempt 02. This is an engineering test failure, not an observed game failure. |
| `.local-work/d5ab/p2-queue02` | Generated source, build log, executable, `1024-0.stderr` | Main-thread diagnostic records 70 contention losses, zero capacity losses and 129,423 retries over 76,800 offers; proposed zero-loss criterion fails. |
| `.local-work/d5ab/p2-queue03` | Source and all per-capacity/repeat stdout/stderr | Hot rounds retained as intentional contention stress. Added paced concurrent traffic, four offers followed by a one-millisecond yield per producer. Suite in progress at this checkpoint. |

The paced workload has four producers and 4,000 records each. Every offered ID
must appear exactly once with consecutive admission sequence and zero losses.
Windows yield duration is measured, never assumed to equal one millisecond.
The independent held-consumer burst remains four times 8,000 offers; consumer
draining begins after both the initial three-second stall and producer joins.
Its actual duration is not a three-second production window.

The driver now snapshots owned source and records each return code before
asserting success. It measures throughput from QPC ticks, distinguishes compiled
queue allocation from peak process working set, and keeps both-drive free-space
checks. Original failed directories remain unchanged and local-only. No game,
saves, native lifetime semantics, new hook, dependency or deployment is involved.

## Open integration dependency

Queue-level success does not demonstrate raw/ACK durability or total native-event
coverage. The primary workstream must bind these tests to final exact source and
qualify the real recorder, fault paths and controller. P1/P3 lifetime obligations
remain independent. Do not tick the gameplay checklist from these tests.

## Checkpoint 2 — final workload oracle and source freeze

All three concurrent workloads now compare every producer's successful admission
list, in order, with the observed list. Unpaced overload and held bursts expose
separate capacity and contention loss totals. Hot rounds prove zero capacity loss
and attribute their loss total to retry exhaustion. Queue high-water values are
sampled lower bounds; the production compare/exchange can miss a competing peak.

The initially frozen source was exercised by `.local-work/d5ab/p2-queue05`.
Self-review then identified that the held burst still lacked an exact successful
admission-list oracle. The final source adds that oracle, including per-producer
ordering, and is exercised by `.local-work/d5ab/p2-queue06`, using:

```powershell
& 'C:/Users/User/AppData/Local/Python/pythoncore-3.14-64/python.exe' -B research/resource-retained-population/d5ab_queue.py .local-work/d5ab/NEW-UNUSED-LABEL 8000
```

Source SHA-256 pins at this freeze:

| File | SHA-256 |
|---|---|
| `runtime/construction-winner/queue_stress.cpp` | `51de4ff8853b6d04c8b0e5484e5542612fdfece113e1d40bf56b0c57e0521899` |
| `research/resource-retained-population/d5ab_queue.py` | `a4c12ec94a83135af2880b99bd5ca6bf569485143737ca7ee1786b8110cd058e` |
| `runtime/construction-winner/observer.h` | `ec2d731e861ede71a5159f1aae1c0cacb39d04a73c7da7b6771a184233801e81` |

Intermediate suites 03, 04 and 05 run their captured source but overlap subsequent
test-source edits. Their final comparison to the current tree is expected to
refuse qualification. Preserve them as exploratory evidence; suite 06 provides
the final source lineage. Multiple disposable suites and the primary native
suite can overlap, so timings include competing local workloads. Paced throughput
measures this explicit offered-load envelope, not maximum recorder service rate
or a retail guarantee.

## Checkpoint 3 — final compiled result

Suite 06 completes with **nine of nine executable runs passing**, source identity
unchanged and no compiler errors. Every run executes the production queue from
the pinned unchanged `observer.h`, including publication-race, wrap, full/retry/
recursive losses, uncertain loss bounds, overflow refusal and STOP with an active
reserved producer. It also checks every admitted ID and per-producer order in
the four workload families. The compiled Event is 312 bytes and Cell is 320 bytes.

| Cells | Queue bytes | Unpaced losses in repeats 0/1/2 | Hot-round contention losses in repeats 0/1/2 | Held 32,000-offer losses in repeats 0/1/2 | Paced throughput range, records/s |
|---:|---:|---|---|---|---:|
| 1,024 | 327,680 | 53,643 / 53,317 / 48,288 | 41 / 32 / 20 | 30,976 / 30,976 / 30,976 | 1,275.58–1,300.78 |
| 8,192 | 2,621,440 | 9,551 / 55,618 / 23,367 | 56 / 43 / 17 | 23,808 / 23,808 / 23,808 | 830.43–1,050.66 |
| 32,768 | 10,485,760 | 10,613 / 23,635 / 9,495 | 32 / 71 / 71 | 0 / 0 / 0 | 1,069.81–1,303.70 |

All nine paced workloads retain all 16,000 offers with **zero loss**. Their sampled
high-water lower bounds range from 16 to 36. The 32,768-cell held burst retains
all 32,000 records in all three repeats; the smaller queues honestly report their
exact capacity deficits. Unpaced 32,768-cell losses include 10, 6 and 0 contention
losses respectively; its remaining losses are full-queue losses. The other two
unpaced capacities report only full-queue losses. Hot rounds remain lossy at all
capacities despite at most 384 outstanding records. They invalidate a universal
lossless claim and demonstrate why queue enlargement alone is insufficient.

Peak process working-set ranges are 10,088,448–10,485,760 bytes at 1,024 cells,
12,222,464–13,467,648 bytes at 8,192 cells and 20,377,600–21,000,192 bytes at
32,768 cells. These include host/test-oracle allocations and are not queue bytes
or a production DLL memory estimate. Final caller-available free space is
91,063,791,616 bytes on C: and 83,858,006,016 bytes on D:.

Primary receipt: `.local-work/d5ab/p2-queue06/receipt.json`, SHA-256
`52cb5d7ab9c152b40419e355a9df338dc20c95b42ba09a1b6a7337d644037b58`.
It binds source hashes, generated source, capacity-specific executable hashes,
per-run results and QPC measurements. `sources/`, `build.cmd`, `build.log`,
per-run stdout/stderr and exit JSONs preserve reproduction inputs and actual
return codes. The build log identifies Visual Studio 2026 developer environment
18.9.0; the primary native build supplies the fuller compiler identity.

Exploratory suites 03, 04 and 05 each retain nine passing native stdout records.
The actual driver exit was observed as 1 for suites 04 and 05, whose source
identity changed during execution; their diagnostic records are local. Suite
03's final driver output was not retained, so its top-level exit is UNKNOWN.
No exploratory suite substitutes for suite 06's verified final source identity.
The two failed workload-design attempts and the failed direct replay remain
counterexamples, not erased historical results. No source or test failures are
waived by these scoped passing results. P2-Q1 still requires the integrated
recorder/ACK/controller evidence owned by the primary workstream.
