# D5E continuous source-decision acquisition

[Authorized Phase A brief](../../docs/implementation-briefs/CODEX_BRIEF_SOR_RG2_D5E_continuous_source_decision_acquisition.md),
[report](../../docs/experiments/resource-source-decisions/report.md),
[native contract](../../docs/experiments/resource-source-decisions/native.md),
[qualification](../../docs/experiments/resource-source-decisions/qualification.md).

This is bounded research instrumentation. The native build is unexecuted and
the [Phase B card](../../docs/experiments/resource-source-decisions/run-card.md)
is NOT AUTHORIZED. Four permanent probes replace D5B's phase rotation for this
separate study; existing D5B acquisition/consumer semantics are unchanged.

Use the installed CPython interpreter directly; the WindowsApps `python.exe`
alias was unavailable in this session. From the repository root:

```text
PYTHON -B research/resource-source-decisions/build.py --name BUILD
PYTHON -B research/resource-source-decisions/qualify.py --build .local-work/resource-source-decisions/BUILD --output .local-work/resource-source-decisions/QUALIFICATION
PYTHON -B research/resource-source-decisions/tests.py --label TESTS
PYTHON -B research/resource-source-decisions/verify.py
```

`PYTHON`, `BUILD`, `QUALIFICATION` and `TESTS` are placeholders. Names/output
directories must be fresh. `verify.py` writes exclusive `verification01.json`;
it cannot overwrite an earlier receipt. Optional `--modes` permits a focused
diagnostic subset; it does not replace the full mandatory qualification matrix.

| File | Reads, writes, dependencies and effects |
|---|---|
| `build.py` | Reads owned D5B utility prefix, transitive quoted headers, current source and installed MSVC/SDK. Generates one translation unit, fixture/native executables, log/command/build hashes under a new ignored build directory. Executes build tools only; no fixture or game. |
| `fixture.cpp` | Disposable process with four exported boundaries, actual target-memory retained populations and explicit fixture epochs. Synthetic branch controls intentionally create misses/hits/bypasses, invalid states, contention and crashes; no game/save access. |
| `controller-tail.inc` | Uses owned D5B hash/read/debug/disposal utilities. Fixture executable creates/attaches only the hash-pinned sibling. Separately built native executable accepts only explicit retail PID and exact retail image path/hash. Both affect DR/RF and execution timing; STOP/failure may dispose the target. |
| `native.inc` | Synchronous native register/stack/memory reads at the four permanent sites; no borrowed pointers deferred to a worker. No memory writes or epoch field invented. |
| `collect.py` | Future native admission/transport entry point; not executed on retail. Shared bounded pump journals/fsyncs/SRO1-verifies before ACK/READY. Synthetic healthy/failure pump paths are exercised by qualification. On transport failure it retires its controller, whose kill-on-exit can dispose the target. |
| `reduce.py` | Pure fixture-oracle reducer, or exclusive JSON output CLI. Preserves explicit lifetimes, ordered branches, incomplete cases and contradictory masks; refuses native sessions. |
| `native_reduce.py` | Pure native snapshot reducer, or exclusive JSON output CLI. Requires pinned native session/site, stop-local source/owner/frame checks. Returns C or D with named gaps; does not join stops into epochs. |
| `qualify.py` | Executes only pinned disposable fixture/controller and the shared transport pump. Writes fresh ignored raw receipts, independent decodes, ACKs, event/reduction/process records, expected/observed matrix and failure diagnostics. It intentionally terminates disposable processes in stop/failure cases. |
| `tests.py` | Invented-byte offline native refusal/session/coverage tests; writes a fresh named local receipt. No native process. |
| `verify.py` | Rehashes 405 inherited pins, checks ten control identities/twenty rows and frozen alternatives without regeneration. Parses Python/JSON; writes local verification receipt. |
| `event.schema.json` | Outer event schema; detailed validation belongs to reducers and native contract. No new JSON-schema dependency installed. |

The exact utility prefix is the existing file before `struct Thread {`; this
reuses its owned read/hash/debug cleanup implementation, not its changing D5B
probe schedule. SRO1 persistence is reused from `resource-oracle-retail/collect.py`
and independent decoding from `resource-tungsten-acquisition/qualify.py`.
The native geographic decoder is reused from D5B. [Per-use pins](../../docs/experiments/resource-source-decisions/sources.csv)
and build manifests preserve the actual source hashes at repository baseline
`1f521aacaa4a1d9e02ce73d843294464f9c57ba0`, under SOR-P-0002.

No new outside code, library, dependency download or network operation is used.
Windows/MSVC/SDK, CPython and Git are separately installed tools, not vendored
dependencies. Binaries, generated translation units, raw contexts and private
paths remain ignored/local. Authored code/method is REVIEW-REQUIRED; no publication
or live authority is supplied by successful synthetic tests.
