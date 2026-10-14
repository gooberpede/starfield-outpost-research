# Archived final thread-control diagnosis

**Outcome B: ABANDON EXTERNAL DEBUGGER PATH.** These are diagnosis tools, not an
acquisition release. See the [completed report](../../docs/experiments/event-latency/thread-control-final-report.md).
The final brief's authorization has been consumed; this is no invitation to run
another debugger iteration or use any executable against Starfield.

Original project-authored tools, GPL-3.0-or-later. The source adapter/fixture and
bounded process reader retain SOR-S-0132 / SOR-P-0002 provenance. Windows API
contracts consulted are credited as SOR-S-0139; no third-party implementation or
new dependency was copied. Installed MSVC/SDK and Python stdlib only.

`diagnose.py` reads the pinned unchanged 0.1.4 adapter source, shared headers,
original fixture executable/assembly object and generated retail guard metadata.
It generates diagnostic source in a NEW ignored `.local-work/thread-control/`
directory. Original baselines are never overwritten. Its generated executables
inherit 0.1.4 event labels solely to retain the baseline's data format; their
different hashes and `diagnostic_only` receipts identify them. They are not a
new 0.1.4 release, version upgrade, or live candidate.

The executable variants add immediate API/context traces; optionally open thread
handles with explicit query/synchronization rights, deliberately reduce duplicate
handle rights, and try rewinding queued other-thread owned traps. The last trial
is incomplete engineering and is retained as negative evidence. Explicit handles
are process-local diagnostics and may remain open until the diagnostic process
exits. No system/thread DACL or global security setting changes.

Only Popen-created, hash-checked `event_fixture.exe` targets are attached, patched,
paused, single-stepped and suspended. The observer changes timing. A synchronized
32-thread burst exercises queued traps; a separate burst has 24 threads exit and
8 call the original fixture function. Affinity requests use the first eight mask
bits; return values are not asserted and affinity is not a proof of simultaneous
execution. The atomic arrival/start barrier is explicit; exact trap ordering is
observed, not assumed. Fixture native register/output checks remain intact.

The final fixture's breakpoint handler counts exceptions and advances RIP only
over a still-present INT3 when required. A delivered debugger trap at restored
code remains observable as an unexpected exception, even when outputs match.
Earlier broken handler pilots are preserved and distinguished in the report.
`stop-queued` injects an operator stop at the first confirmed queued-trap handling
state; `stop-replay` injects a stop after replay setup. These are deterministic
state interventions, not scientific event caps. `target-exit` calls ExitProcess27
inside the owned fixture. Genuine writer failure uses the established injection.

The harness requests cooperative STOP and checks original site bytes and debugger
absence independently **even after adapter failure**, before fixture release.
If the target has exited, its original Popen handle exit code and WAL target-exit
marker replace unavailable live queries; that never proves byte restoration.
An unresponsive owned disposable may be terminated through its original Popen
handle after cooperative cleanup fails. It is recorded as a failure. No looked-up
PID or game is terminated. All targets/process handles were gone at final review.

The harness enforces both-drive 40,000,000,000-byte guards before launches/output;
the original per-record WAL guards/flush/hash chain remain unchanged. Trace I/O
is extra diagnostic output, not a substitute for durable WAL. The 300-second
workload and 20/15-second cleanup bounds are orchestration timeouts, not acquisition
quotas. Initial ordinary trace controls used a 90-second diagnostic wait; none hit
that bound. Receipt collection historically exits 0 on completed collection even
when a control fails: use individual results and the B disposition, not shell
exit 0, to interpret it. It is deliberately not a qualification runner.

Recorded command forms, repository root, installed 64-bit Python:

```text
python -X utf8 -B debugger/event-thread-control/diagnose.py --run NEW_NAME
python -X utf8 -B debugger/event-thread-control/diagnose.py --run NEW_NAME --adversarial --query-handles --defer-queued --modes exit-burst queue-burst stop-queued stop-queued stop-queued foreign-break stop-replay target-exit
python -X utf8 -B debugger/event-thread-control/summarize.py
```

`thread_api_probe.cpp` creates only its own worker thread, duplicates its handle
with reduced rights, measures running/exited suspension/query results and verifies
that an existing suspend increment survives the probe's increment/resume pair.
It emits JSON to stdout; no file, remote process, memory or policy access.

`summarize.py` reads the frozen local matrices, streams API traces, decodes WALs
and validates the expected negative evidence. It writes one NEW result matrix
and never opens a process. Raw WAL/memory, traces, compiler intermediates, source
snapshots and diagnostic executables remain local/ignored and excluded from the
diagnosis archive. Exact commands/hashes are in each private build/run receipt.
