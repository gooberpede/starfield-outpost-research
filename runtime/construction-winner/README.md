# Construction-winner observer: D5AB candidate

Offline P3 integration candidate, schema `sor-d5x/4`, following accepted P1
source/lifetime and schema-3 P2 controller/consumer qualification.
The [P3 ledger](../../docs/experiments/resource-retained-population/d5ab-p3-investigation-ledger.md)
tracks the integrated native and consumer qualification; its report and exact
independent review govern the final disposition. P4/B2 remain separately gated.
The [P1 ledger](../../docs/experiments/resource-retained-population/d5ab-p1-investigation-ledger.md)
tracks source identity and lifetime closure; its final report/review controls
qualification. P4 and B2 remain separately gated.
[P2 ledger](../../docs/experiments/resource-retained-population/d5ab-p2-investigation-ledger.md)
records the active work; final qualification is governed by its report and review.
[D5AB report](../../docs/experiments/resource-retained-population/d5ab-report.md),
[native map](../../docs/experiments/resource-retained-population/d5ab-native-map.md)
and [schema delta](../../docs/experiments/resource-retained-population/d5ab-architecture-schema.md)
govern qualification. **No retail operation or deployment is authorized.**
Historical D5X 0.2.0/schema 2 and B1 receipts remain preserved. The reader keeps
schema 2's original interpretation; B1 does not acquire an append observation.
Schema 3 retains its original reducer. Schema 4 leaves native lookup source bytes
zero and reconstructs semantic identity offline from a qualified birth witness.
It does not reread the selected source under the ProcGen map lock. The identity
uses terrain FormID, face and coordinate components, and the consumed visited
token; padding and other unused bytes do not enter semantic comparisons.
Allocation IDs, pointers, geography and visited tokens remain separate.
Missing publication, changed epoch, invalidation, loss or contradictory native
order refuses a join. This includes surviving sources across a reset without a
new birth witness. Native immutability is a static proof premise, not a comparison
between two independently observed source copies.

Build and exercise only disposable Windows hosts with installed CPython,
MSVC/MASM and Windows SDK:

```powershell
& 'C:/Users/User/AppData/Local/Python/pythoncore-3.14-64/python.exe' -B runtime/construction-winner/build.py NEW-LABEL
```

Use a fresh lowercase/digit/hyphen label. Optional case names select a development
subset and do not qualify the full contract. `SOR_QUEUE_CAPACITY` may explicitly
select 1024, 8192 or 32768; the default is 32768. Builds read pinned installed
EXE/data/SFSE, the approved unchanged SFSE PluginAPI header and owned source.
They write only exclusive `.local-work/d5x/LABEL` outputs, source snapshots,
guards, compiler logs, disposable binaries/packages and synthetic receipts.
The host never launches, attaches to or terminates Starfield. Declared crash
controls terminate only their own host. A bad-source observer control substitutes
a consumed operand instead of intentionally dereferencing invalid native memory.

Qualify the exact completed build and separately measured queue with:

```powershell
& 'C:/Users/User/AppData/Local/Python/pythoncore-3.14-64/python.exe' -B research/resource-retained-population/d5ab_p1_qualify.py .local-work/d5x/BUILD .local-work/d5ab/NEW-CONTROLS
& 'C:/Users/User/AppData/Local/Python/pythoncore-3.14-64/python.exe' -B research/resource-retained-population/d5ab_queue.py .local-work/d5ab/NEW-QUEUE 8000
& 'C:/Users/User/AppData/Local/Python/pythoncore-3.14-64/python.exe' -B runtime/construction-winner/worker_health.py --qualify .local-work/d5ab/NEW-WORKER
```

The queue driver compiles the production queue at all three capacities, retains
its generated source and runs independent offered-ID/count/sequence oracles.
The 8000 argument gives four producers and a 32,000-record held-consumer burst;
3000 gives the earlier 12,000-record control. These are constructed workloads,
not a universal retail throughput guarantee. The native representative case
also emits all seventeen categories through actual observer callbacks under an
injected three-second raw-flush pause, with honest overload/fault controls.

The reader authenticates framed raw/ACK prefixes and reduces only qualified
source/request/epoch chains. Constructors and actual source publication provide
allocation witnesses. Visited records carry an already consumed token without
following the selected pointer. Reserve result and actual store are separate.
There are eighteen guarded sites, fixed 312-byte records and no Grid membership
scan, geometry-array capture or target filtering. P3 changes the five inline
bridges to CALL-entered framed helpers and widens the visited window to thirteen
bytes, retaining the conditional branch in the original image. The erase
trampoline has registered partial-prologue unwind metadata and a guarded
register tail transfer. P3's native controls test instruction-boundary context
recovery, synchronous exceptions and an actual unhandled store fault in an owned
host. These finite controls do not establish arbitrary corruption tolerance or
retail behavior. STOP leaves resident wrappers forwarding originals; hot
unloading/unpatching is unsupported.

`controller.py` binds the actual worker query/synchronization handle, process birth,
session identity, fresh challenge ACK and durable raw/ACK prefix. It holds an
exclusive controller lock, authenticates its own STOP bytes and reconciles closed
evidence before declaring admitted-record completion. Delayed ACKs remain alive
and pending without a retirement deadline. Disconnect and controller-process death
release the lock; reconnect requires a fresh worker lease and challenge.
It deliberately accepts disposable sessions only. No live use is authorized.
`worker_health.py --watch` is an older unqualified helper; its STOP-file-based exit
label is not the P2 controller or proof of authenticated finalization.

Run the actual-worker controls against a completed build:

```powershell
& 'C:/Users/User/AppData/Local/Python/pythoncore-3.14-64/python.exe' -B research/resource-retained-population/d5ab_p2_controller.py --parallel .local-work/d5x/BUILD p2-controller-UNIQUE
& 'C:/Users/User/AppData/Local/Python/pythoncore-3.14-64/python.exe' -B research/resource-retained-population/d5ab_p1_qualify.py .local-work/d5x/BUILD .local-work/d5ab/p1-reader-UNIQUE
```

The controller tests create synthetic impairment commands only in their own
disposable hosts. They preserve intentional writer/flush/ACK/guard faults,
unexpected worker exit, missing terminal and damaged closed-evidence derivatives.
Finite engineering waits do not define live monitoring policy. The current
reader separates authenticated prefix candidates from finalized chain claims,
refuses damaged/incomplete/loss-contaminated whole-session claims, and keeps
retail source lifetime and scientific firstness explicitly unqualified. The P3
report and independent host oracles qualify the tested offline witness scope.
Schema-2 B1 and accepted schema-3 session interpretations remain separately tested.
Schema 4 also reports `reset_scoped_chains`: complete reset-to-store witness
histories can survive an earlier bounded loss when a new authenticated empty
reset and fresh source lifetime establish a complete later scope. Whole-session
lossless and retail qualification remain separate. `candidate_chains` preserves
useful partial evidence on incomplete closeout; it is not finalized qualification.
`evidence_states` distinguishes observed records, conditional witness conclusions,
unsupported retail/geometry claims and explicit contradictory evidence.
The schema-4 fixture additionally tests inaccessible source memory at lookup,
retirement/reset there, unpublished construction and modeled constructor unwind.
These are controlled host schedules, not a retail constructor or allocator test.

The owned D5X/R1 transport, patch admission, existing native/export controls and
protection methods are reused under SOR-P-0002 with [provenance](../../docs/experiments/resource-retained-population/d5ab-sources.csv).
The existing D5X approval covers the same unchanged pinned SFSE PluginAPI header;
its MIT notices remain in local packages. No additional SFSE/CommonLib or outside
implementation is incorporated. All authored code is GPL-3.0-or-later.

Disposable native bytes, captures, saves, DLLs, generated guards and packages are
LOCAL-ONLY. The fixture emitter excerpt is excluded from retail ZIPs. Private
packaging grants no redistribution, installation, live, Git or publication
permission. B1 remains PARTIAL, D5AA ESCALATE and parent D5R OPEN. The proposed
B2 card requires a distinct explicit maintainer GO after independent review.
