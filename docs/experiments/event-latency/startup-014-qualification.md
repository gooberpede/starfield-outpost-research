# 0.1.4 qualification — startup repair passes, runtime gate remains closed

SOR-EXP-0027 / SOR-EV-0035;2026-10-11 Australia/Sydney.
[Investigation](startup-failfast-investigation.md), [fault map](startup-fault-map.md),
[review/package](startup-review.md). **Not live-qualified.** This is a narrowly
corrected candidate for review, not an approved replacement for0.1.3.

Delivered executable: `.local-work/event-instrumentation/startup-candidate-014-03/adapter.exe`.
SHA-256 `aee2d1cc12a3f46818a3a8d5c01ee3a38e05af8adb44b4479971bbbc241d93d3`.
Candidate fixture SHA-256
`bea013e77724b7c68e1fe5d59c64e1c05675b27c2ea3853dbf90794f52a9f4c2`.
Its [source/toolchain/control result](../../../.local-work/event-instrumentation/startup-candidate-014-03/result.json)
is pinned independently of the original0.1.3 package. All six controls ran;
the overall qualifier correctly exits nonzero because one failed.

## Startup and health

- **19/19 startup controls** on the delivered0.1.4, compared with19 correctly
  classified0.1.3 controls (many deliberately reproduce fail-fast). [Original matrix](../../../.local-work/adapter-startup/startup-controls-013-final/results.json),
  [candidate matrix](../../../.local-work/adapter-startup/startup-controls-014-03/results.json).
- **12/12 health assertions**, including storage guard and retained WAL-prefix
  health, in `startup-candidate-014-03/health.log` and `wal-health.json`.
- **11/11 original Python WAL/inspector tests**, `inspector-tests.log`.
- Fresh-root genuine-fixture startup/retirement and injected post-detach timing
  failure independently verify original code and no debugger; fixtures exit0.
  Timing failure now reports `profile_write stage=timing_write attached=0`, then
  `secondary_timing_failure`, exits1 and preserves the valid WAL prefix.
- Permission-negative helper restores its own DACL and exits normally. No system
  policy/security change or game process access. Native-site guards are not spoofed.

## Established six controls, final exact binary

| Control | Result | Evidence/limit |
|---|---|---|
| Full | PASS |42 entries,41 paired exits,1 intentional unwind,870 raw sections, bad0/fixture exit0; restoration/detach independently checked |
| Center-only | PASS |42 entries,41 pairs,1 intentional unwind,830 raw sections, bad0/fixture exit0; independent checks |
| Grid guard failure | **FAIL** | Adapter exits1 with `suspend_live_thread:5 stage=event_loop attached=0`; expected normal completion not met |
| Zero hits | PASS | No boundaries/raw sections; independent restoration/detach; fixture exit0 |
| Retire active | PASS |1 entry/retired unpaired scope, then fixture completes normally; independent restoration/detach |
| Writer failure | PASS | Injected genuine WriteFile failure; expected exit1, independent restoration/detach, fixture bad0/exit0 |

The failed grid-guard-failure case still disables the bad grid preimage, then fails
in the existing other-thread suspension path during center acquisition. Its last
WAL frame is a complete center-entry boundary; no tail corruption, retirement
marker or terminal. WAL486 valid frames,369832 committed bytes, SHA-256
`5ae232c2c3b27a27b1a9543796da7ad36ace7b47cd14981f4dcfcb2f72be1cd5`.
The `suspend_live_thread` diagnostic reports a failed SuspendThread followed by
failure to prove that thread exited; GetLastError5 is not a complete pair of API
results. Do not claim a particular handle/thread race is proven without those
missing values. The adapter reports attached=0 after its rollback path; the
fixture later completes42/41, bad0/exit0. The harness assertion precedes its
independent code/detach checks, so **that failed case lacks an independent live
restoration receipt**. Keep the assertion/cleanup limits visible.

## Other retained attempts and counterexamples

`startup-candidate-014-01`: preliminary diagnostic fix; all six case assertions
completed, but end-of-run source-identity assertion failed after source refinement
while it ran. Not qualified/delivered. Its source snapshot/binary/logs are retained.

`startup-candidate-014-02/full`: pending replay followed by another breakpoint
exception, reported restored:true and terminal RETIRED before workload completion.
WAL369 valid frames,278340 committed bytes, SHA-256
`36b6331f90acb605bed05844777a234ea31a749759c0ad8c02f4ce3eeaa721a8`.
24 boundary rows:13 center entries and11 paired exits; intentional unwind and
active retirement are separate missing partners. Exception address and final
process exit codes were not retained by that fail-fast harness. No independent
postflight was completed for that failed case. A queued second breakpoint during
replay is a hypothesis requiring exact address/context evidence, not established
from exception code alone.

The delivered03 and failed02 have identical adapter.cpp hashes and **identical
compiled .text SHA-256**
`62651b045fd8b617847563a4b109a8fc32004f4ca860566ab0577c70a68d683d`;
[comparison receipt](../../../.local-work/adapter-startup/runtime-code-comparison.json).
Their full PE hashes differ.03's later Full PASS does not erase02's counterexample
or establish statistical reliability. Existing event-loop/patch/replay/suspension
logic is unchanged from the original0.1.3 source except version labels; the
startup repair did not address either runtime condition.

Original startup harness pilots013-01/02 failed on child PowerShell Path/PATH
environment-key duplication, before their adapter launch.013-03 and014-01 were
earlier15-case completed matrices; final19-case matrices supersede coverage,
not history. Incomplete CDB pilots, corrected dump relocation and their commands
remain explicit local artifacts. None counts as a live game sample or final pass.

## Preservation and next gate

Original0.1.3 executable/ZIP,116 incident/review/input files and0.1.2 baseline2683
files/original six controls remain hash-identical. Shared observer0.1.1/reader/
collector/writer/profile/fixture/decoder inputs remain unchanged; protected
Save25/26 originals/archives and four frozen files pass post-work hashes. Both
drives remain above40-billion caller-available bytes. Raw dumps/WALs/private
configuration inventory remain ignored and excluded from the review patches/ZIP.

No performance comparison is claimed: qualification runs and small startup
experiments overlapped in time. These are correctness/error-path tests, not an
isolated latency benchmark. No scientific output/frame claim is promoted.

Recommendation: accept the startup correction for consideration, keep the live
gate closed, and commission focused disposable investigation of the two retained
thread-control conditions. Do not retry until that evidence/recovery behavior and
a version-specific live card receive review/authorization. No game attachment,
deployment, staging, commit or push is implied or performed by this assignment.
