# Startup diagnosis and candidate 0.1.4 controls

Original project-authored Windows/CPython stdlib utilities for
[SOR-EXP-0027](../../docs/experiments/event-latency/startup-failfast-investigation.md).
The event-oracle architecture README remains the preserved 0.1.3 description;
this supplement describes the 0.1.4 startup correction and its review limits.

`disposable_target.py` launches only as an explicitly owned Python child. It
optionally replaces its own process DACL with an empty ACL, waits for stdin
release, restores the saved ACL and exits. It never opens or controls another
process. No global security setting, file, game or save is changed.

`startup_regressions.py` reads/hashes explicit adapter/fixture inputs and launches
only those approved original executables plus its owned Python helper. Retail
tests intentionally reject the Python image; no game guard is bypassed. Genuine
fixture tests may attach/patch/step only event_fixture.exe, independently read
restored code/check detach, then release the fixture normally. A directory at
timing.json injects a post-detach telemetry failure. Both-drive 40-billion-byte
caller-available guard fails closed. 30-second test waits bound disposable harness
failures, not scientific acquisition quotas. No downloads/dependencies.

Commands from repository root, installed 64-bit Python (`python -X utf8 -B`):

```text
debugger/event-startup/startup_regressions.py --adapter ABSOLUTE_APPROVED_OR_CANDIDATE_EXE --fixture ABSOLUTE_GENUINE_FIXTURE_EXE --version 0.1.3_OR_0.1.4 --output NEW_IGNORED_DIRECTORY
debugger/event-oracle/qualify.py --run NEW_RUN_NAME --vcvars INSTALLED_VCVARS64_BAT --keep-going
```

The first command creates new private logs, fixtures/WALs and JSON results; it
performs 19 startup controls. It canonicalizes environment-key case only in its
PowerShell child to avoid duplicate Path/PATH launch rejection. Inherited-stream
testing intentionally writes the diagnostic to the harness's own console.
The second builds and runs the established six controls/12 health/11 Python tests;
`--keep-going` retains failed controls, completes others and exits nonzero if any
failed. No retry of a failed live session is supported.

Capture exact binary/source/helper hashes and OS/compiler provenance. Do not use
these tools for Starfield, modify original receipts or replace approved packages.
The candidate is not automatically live-ready; see the retained runtime
counterexample and [review gate](../../docs/experiments/event-latency/startup-review.md).
