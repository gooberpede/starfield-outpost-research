# EXP0002 operator-settled synchronization correction

2026-10-06 Australia/Sydney. User-authorized offline correction after the [first primary attempt](../experiments/EXP0002-gate-b-run.md). **Prepared for critical review, not deployed or live-qualified.** No deployment, rerun, debugger attachment, staging, commit or push is authorized by this correction. Prior A0 anomaly and raw evidence are preserved; no new scientific claim.

## Resulting acquisition contract

No loading latch or mandatory PreLoadGame/PostLoadGame event remains. Listener registration is still part of READY initialization; notifications only increment descriptive counters. Capture/consistency functions never accept those counters. Missing, unpaired or extra events cannot grant or deny acquisition.

Each explicit request includes operator-settled attestation, with reload-specific attestation for A2R. request.ps1 requires -OperatorSettled, and A2R also requires -ReloadedAndSettled. The native worker rejects old single-line requests and malformed/unconfirmed controls before queueing a task. Each primary task contains only a checkpoint index; it freshly reads the global player, identity/transform/stored cell, cell/world/persistent-cell relationship, collection headers and bounded candidates. A2R takes no A2 snapshot input. Prior JSON remains comparison evidence only, never a dereferenced primary input.

Repeated fresh views gate selection completion, every selected-reference query (including after begin flush), returned-query handling and final success publication. Readable player/cell/collection/reference inconsistencies persist bounded anomalies; unsafe reads and integrity failures remain terminal. Candidate ambiguity never guesses or queries. Existing READY ordering, output limits, six slots, disk threshold, native build/site guards and cooperative time bounds remain. No new native address, layout, game hook, dependency or third-party code reuse was introduced. Optional diagnostic request plumbing now requires the same settled attestation but no diagnostic was run or authorized.

## Actual offline checks

| Check | Result |
|---|---|
| Native synthetic suite | 167 checks pass, including 42 new acquisition/synchronization checks and all prior READY/anomaly/safety checks |
| Native-output validation | 35 checks pass; new player/cell/reference/collection/during-acquisition anomaly files and synchronization metadata validated |
| Zero notifications | Confirmed A0 and A2 acquisition/query eligibility with both counters zero |
| Fresh A2R | All old player/cell/world/array/reference addresses removed from synthetic memory; same FormIDs at new addresses; read log proves no old-address dereference |
| Optional notifications | Unpaired pre-load and notifications during every read do not block or change successful selection |
| Inconsistent live state | Player movement, cell flag change, changed collection, reference stored-cell change and mutation during acquisition block query eligibility and persist bounded anomalies without global stop; structural read failure remains terminal |
| Request guards | Three offline negative tests reject absent Gate B authority, absent settled confirmation and absent A2R reload confirmation before session/process access or writes |
| Timestamp regression | Thirteen checks pass under en-AU/en-US, including stale-PID rejection |
| Packaging | Four ZIP regression tests pass; actual final ZIP CRC, exact LF config, unchanged intended output path and packaged-DLL identity verified |
| Native build | Observer, trace helper and native tests compile without compiler warnings/errors |
| Repository | Source manifest, UTF-8/LF, links, Python syntax, diff whitespace, unchanged index, full tracked/untracked review and unrelated-file preservation checked |

Tests use original synthetic memory and injected services, not Starfield. They establish code-path/serialization behavior, not actual engine lifetime, ABI safety or atomicity. The observer cannot lock reference ownership or detect every transient transition; a change between final check and call can escape detection. Operator confirmation is a procedural precondition, not proof of engine quiescence. Cooperative bounds cannot cancel a running native call. The first-run notification failure remains evidence of the previous build, not a passing live result for this one.

## Exact package for review

Build: `.local-work/exp0002-builds/review14-settled/`. ZIP contains the original observer/config and licence notices; external SFSE/runtime files are not bundled. Vortex is still exclusively user-managed. New binary/protocol requires reviewing this package and current operator card together; do not deploy it into the old session.

| Artifact | SHA-256 |
|---|---|
| SorExp0002.dll | `9a1636adacdcd0967e7873fcdbc161fed04876d3c368f9e37735f707e9e191ed` |
| workshop-trace.exe | `4da7d3252238b0b40aa257e867ef28697485a39e96df738d7bdc753afb4daa3a` |
| SorExp0002-local-test.zip | `970dce992d665eeda0fcf8fcdbcb4d363016756e02e2e3a9ca4c7eeed4a37ff4` |

Source/toolchain/site hashes and compiler logs are in build.json and *-build.txt. Earlier review13 was an intermediate passing build; review14 supersedes it for this handoff. Both remain local.

Complete review artifacts: `.local-work/exp0002-settled-fix/review.diff`, `changes-this-request.diff`, `validation.json`, `status.txt`, `hashes.json`. Full diff is LOCAL-ONLY because prior task changes include the supplied private-path brief. No new permission issue. [Operator card](../experiments/EXP0002-operator-card.md) and [runtime documentation](../../runtime/exp0002/README.md) explain the changed synchronization model.

Suggested commit after review (not executed): `fix(observer): gate captures on settled requests and fresh live state`.
