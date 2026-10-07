# EXP0002A adapter0.1.1 — fixed population qualification

2026-10-07 Australia/Sydney; SOR-D-0017. **The three focused disposable0.1.1 controls passed. Starfield remains unlaunched and its adapter entry disabled pending review.** No deployment, save/configuration modification, staging, commit or push. These controls do not establish a live game contract or authorize Stage C.

## Prior failure and user cleanup

USER-REPORTED: after reviewing the0.1.0 dynamic-new-thread retirement failure, the user manually terminated PID16100 and explicitly said no further cleanup was needed. No process lookup, termination or other cleanup action for that PID was performed in this correction.

The [0.1.0 audit](exp0002a-adapter-qualification.md) and every file under .local-work/exp0002a-adapter remain unchanged. Its new-thread result remains **FAILED_DYNAMIC_NEW_THREAD_RETIREMENT**, not reclassified as a passing capture-first test. The changed0.1.1 experiment avoids dynamically arming new threads; passing it does not resolve the earlier failure. A before/after SHA-256 inventory is retained in the new evidence root. The complete pre-change source snapshot also preserves the exact sources named by the0.1.0 build manifest.

## Implemented contract

[Native adapter](../../debugger/exp0002a/native/adapter.cpp), [adapted RF core](../../debugger/exp0002a/native/rf_core.h), [plan](../../debugger/exp0002a/next_capture_plan.json), [operator card](../experiments/EXP0002A-operator-card.md).

The selected backend remains Win32 hardware/RF for one REQUEST_ENTRY at observed module base +0x0183c590. The Stage-A game/site hashes, candidate arguments and bounded reads remain unchanged. Steam without SFSE and explicit loaded-module absence checks for SFSE/SorExp0002 remain the baseline. No x64dbg fallback, serializer/completion site or plugin invocation was added.

During setup, existing threads are configured at debugger-owned stops. Before the ARMED evidence boundary, known threads are explicitly suspended and checked against a complete thread inventory. If a create event is still missing, only owned suspension counts are released and setup continues within its watchdog. ARMED records the frozen membership as TID/creation-time pairs while creators are suspended. Setup suspensions are then released before the operator-ready signal. This is an explicit local membership boundary, not a claim of a global atomic Windows thread-enumeration API.

After ARMED, CREATE_THREAD events record TID, creation time and unarmed status. The arming function rejects any later ownership expansion. Newly created threads receive no DR0 installation and no debug-register restoration writes during retirement; temporary balanced suspension for cleanup remains disclosed. Exit events remain recorded. Runtime TID reuse does not make a new thread eligible because membership is not reconstructed from a bare TID allow-list.

The handoff remains: ordinary Steam launch without SFSE, disposable Save3-based load, Pause > Save > highlight New Save without confirming, report ready, attach/configure, ARMED, user confirms once. Setup is bounded separately at300 seconds, operator coordination at120 seconds, acquisition at one request or10 seconds after after-click confirmation receipt. Provisional entry before receipt is retained; click, receipt and hit remain separate anchors. NO_HIT records new-thread provenance and coverage limits, with no widening or automatic retry. In Starfield, absence alone cannot prove that a request ran on a new thread.

The complete protocol record retains registers, thread/module/address provenance, raw caller/stack, candidate manager fields and bounded candidate name data with read-validity statuses. WriteFile followed by FlushFileBuffers persists the record and a durable-capture marker before retirement. “Evidence complete” means this required protocol record was flushed; it is not proof of engine semantics, valid unreadable operands, operator causality, save completion or file durability.

## Capture-first recovery

Evidence completeness is latched independently from acquisition interpretation, cleanup status and target outcome. Normal clean retirement retains the15-second/1024-event bounds. A cleanup exception after durable capture permits termination of only the verified experimental process. The adapter rechecks PID, creation time, full image path and image hash against its retained process handle; it never reopens a process by PID for termination. Destructive recovery has a10-second/1024-event exit-drain bound. Exit completion is checked, not inferred from a successful termination request.

Before durable capture, destructive recovery is denied unless independently measured low disk triggers the machine-safety exception and target identity is verified. The free-space guard uses the existing40GB threshold and checks during the capture/coordination loop. A mere timeout, missing hit, unowned exception, output failure or cleanup inconvenience does not supply that exception. Unresolved pre-capture recovery holds for review. No blanket exception suppression or unrelated-process termination.

The result has separate evidence_complete, acquisition_status, cleanup_status and target_outcome fields. A termination after capture leaves DURABLE_REQUEST/evidence_complete intact. Clean API checks and presence still do not prove healthy event state; disposable worker progress and normal exit are independently checked. Game UI responsiveness remains an operator observation. Loss of the target can make later completion/save-file observations unavailable without invalidating the captured entry.

Microsoft [TerminateProcess](https://learn.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-terminateprocess) documents asynchronous completion and process-handle termination; [GetProcessTimes](https://learn.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-getprocesstimes) supplies creation-time identity. Read-only documentation use, no copied example implementation.

## Actual focused qualification

One build, three fresh disposable attachments, no retry or stress matrix. Build used installed MSVC/Windows SDK with /W4 /WX. Each target was already running before attachment, and two additional workers were created after ARMED. Both later workers remained unarmed in every case.

| Case | Capture/acquisition | Retirement and target outcome |
|---|---|---|
| fixed-existing, PID9324 | One known request from an armed existing thread; required data and durable-flush ordering verified | Clean API retirement in1047ms; all three workers progressed through15-second delayed health; normal exit0 |
| unarmed-only, PID13440 | Fixture independently identifies its caller as a new unarmed thread; zero captures; NO_HIT_NEW_THREADS_PRESENT at10000ms after confirmation receipt | No ownership expansion or termination; clean API retirement in938ms; all workers progressed through15 seconds; normal exit0 |
| retirement-fault, PID16336 | One complete durable request on an existing armed thread | Disposable-only injected failure before detach, after bounded clean-retirement work; exact retained-handle termination completed1156ms after retirement start, exit0xe0000111; final evidence_complete=true and DURABLE_REQUEST retained |

The third case is a deliberate recovery control, not a naturally occurring retirement failure. It tests the destructive path while still attached. No process other than that verified disposable target was terminated by this run. Native self-checks also reject pre-flush/no-safety termination and absent identity, and the Starfield entry refuses before target access. The low-disk condition was not induced; no evidence claims a real low-disk experiment or general OS-failure coverage.

No scientific game claim is promoted. The0.1.0 dynamic-new-thread failure remains a counterexample to broader lifecycle safety. One passing focused control is not proof of reliable Starfield disengagement, and the new policy deliberately permits target loss after complete capture.

## Identity, provenance and review

Adapter version0.1.1 is emitted consistently in save_request_adapter-0.1.1.exe, generated identity header, every native evidence row and manifest. The separate, unbuilt observer remains reserved0.1.0 for Stage C; no plugin metadata/package or Vortex deployment was created.

- Adapter SHA-256: db25940f3989d7f68cd4ccdad85f35d24e8aaba4438cb902753d9b9c94133839.
- Fixture SHA-256: 8334d9bfeac973bd6a756346d8a0eb25905a85e3a0f5d4def01691a11cbfc1ce.
- Source-set SHA-256: 340706afcc4babe55acbcec2bf6b8827e3f26fe14415d3928e2792280ef2a9c3.
- Build manifest SHA-256: 866ca1fdb1fbf1dfc4629f80614485f994e12dddd3864863e5db30e067e642da.

Maintainer source remains gooberpede/starfield-reference-handles at6a77579a184c64e0c080c8f3b7883c34bd17e24b. The0.1.1 fixed-population, evidence latch, recovery gate, fixture and validator changes are project adaptations/additions; [exact inherited provenance](../../debugger/exp0002a/maintainer/PROVENANCE.md). SOR-P-0002 covers that reuse; third-party/SFSE boundaries are unchanged.

Evidence root: .local-work/exp0002a-adapter-0.1.1. [Qualification receipt](../../.local-work/exp0002a-adapter-0.1.1/qualification-01/qualification.json), [build manifest](../../.local-work/exp0002a-adapter-0.1.1/build-01/manifest.json), [offline/preservation validation](../../.local-work/exp0002a-adapter-0.1.1/validation.json), [0.1.1-only diff](../../.local-work/exp0002a-adapter-0.1.1/adapter.diff), [complete working-tree diff](../../.local-work/exp0002a-adapter-0.1.1/review.diff), [Git status](../../.local-work/exp0002a-adapter-0.1.1/status.txt). Diffs include new files without staging. Prior evidence roots were not regenerated. Return for review; no Starfield launch or commit.
