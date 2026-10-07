# EXP0002A adapter 0.1.2 — enablement checks and live handoff

Authority: SOR-D-0018 and [retained instruction](../implementation-briefs/EXP0002A-adapter-0.1.2.md). The user approved 0.1.1 as qualified base. Status: offline checks passed; the authorized live attempt reached ARMED, then ended with a pre-capture target exit after the operator's save click. No request contract was acquired. Further substantive changes and another live attempt require review.

The native delta removes the explicit Starfield refusal, admits the existing game mode in argument validation, changes its setup evidence label to starfield_late_attach and updates the authorization comment. There is no breakpoint, capture, population, retirement or recovery logic change. Build, plan and version metadata now identify adapter 0.1.2; observer 0.1.0 remains unbuilt. The plan differs only in status/live_enabled. rf_core.h, request_fixture.cpp and the historical 0.1.1 qualifier are byte-identical to the approved base. Do not use that historical qualifier as a 0.1.2 runner.

No additional third-party or maintainer code was incorporated. Existing adaptation provenance remains in [the maintainer record](../../debugger/exp0002a/maintainer/PROVENANCE.md). All 217 files in the prior 0.1.0/0.1.1 local evidence roots were hashed and preserved unchanged. The failed 0.1.0 dynamic-new-thread retirement outcome remains failed; PID16100 cleanup remains the user's reported manual termination.

Installed MSVC rebuilt both executables with /W4 /WX. Native --self-check returned 0; the offline correction checks passed (pinned PE receipt, one site, independent timing bounds, version consistency, recovery scope and continued historical x64dbg refusal). No fresh disposable process was executed. git diff --check passed. These are enablement checks, not evidence of live save semantics.

Local-only receipts: .local-work/exp0002a-adapter-0.1.2/build-01/manifest.json, offline-checks.json, preflight.json, preserved.json, enablement.diff and before/ snapshot. Source-set SHA-256: 2b5c2438a45e1c70414328437563ca5c400039e6c531ccf538847a27513f4628. Adapter executable SHA-256: 4f312ace0f52940f7403a9db7442f8c0855189aaed6668b3c2564b7f39782d15.

Prelaunch integrity at 2026-10-07T01:55:10Z: original Save3 and backup both 2,096,496 bytes, SHA-256 d06123ee32bd5b3e244650852fac9714697a19fd6243384966414d1d1f4ffbfe, timestamps unchanged. Installed game hash matches pinned 7e9adb1414a8e1b325e5e1f097b9b17b78deb7eebeda37a333351a43a60f9d28; version 1.16.244.0. C: free 101,533,958,144 bytes; D: free 121,479,081,984 bytes, both above 40,000,000,000. No Starfield process was present at the prelaunch process check. This does not certify the future process's loaded modules: fail-closed module inventory occurs before attach, before ARMED and at DLL-load events.

The [operator card](../experiments/EXP0002A-operator-card.md) retains Steam without SFSE, paused New Save, REQUEST_ENTRY only (runtime base +0x0183c590), population frozen at ARMED, post-ARMED threads unarmed, one request/10-second receipt-anchored bound, and capture-first destructive recovery. Setup and operator coordination are separately bounded. Stage C remains blocked. No commit, staging, push or deployment.

## Live attempt and actual result

The operator reported ready at New Save. Read-only preflight identified PID10364, creation FILETIME134358117292536961, installed build1.16.244.0 and 158 modules without a forbidden prefix. The PowerShell preflight receipt serialized an empty property projection as [null]; the native complete enumerations below independently report explicit absence. This is not evidence of a loaded unnamed module.

The first adapter invocation (live-01, controller PID1900) was sandbox-denied at module snapshot, Win32 error5, before DebugActiveProcess. It installed no breakpoint, completed its delayed presence observations and exited. Its generic cleanup_status is not proof of attempted retirement: attachment had not happened. The same unchanged, hash-verified executable was then run with approved host access (live-02, controller PID13448). There was one actual attachment and one operator save click, not two save traces.

| Boundary | UTC / observation |
|---|---|
| Setup start | 2026-10-07 01:58:08.470186Z |
| Identity | PID10364; runtime image base 0x7ff60a5b0000; REQUEST_ENTRY runtime VA0x7ff60bdec590; pinned executable and 32-byte site hashes matched |
| ARMED evidence | 01:58:49.018628Z; 92 member TIDs/creation times frozen; preexisting debug-state checks passed; all module guards reported SFSE/SorExp0002 absent |
| Last setup resume | 01:58:51.799699Z; 92 owned suspensions balanced before .armed marker and operator handoff |
| Operator action | USER-REPORTED: clicked New Save exactly once; game exited after a short delay. Actual click timestamp unknown |
| Target exit event | 01:59:21.348330Z; EXIT_PROCESS_DEBUG_EVENT, 32,328ms after ARMED evidence; this interval is not save latency |
| Request evidence | Zero first_hit/capture/capture_durable records; no post-ARMED new_thread_unarmed records; no scientific request record |
| Cleanup | Native recovery suspend failed error5 after exit event; recovery_required, no terminal complete record. Verified adapter alone was stopped externally after preserving its flushed log; no Starfield TerminateProcess requested |
| Final state | Starfield PID10364 and controller PID13448 absent. User reports Steam sync finished |

Scientific outcome: **INCOMPLETE_PRE_CAPTURE_TARGET_EXIT**, not a successful capture and not a completed bounded NO_HIT test. The click confirmation arrived after the exit/recovery hold; a separate operator report and .confirm receipt were written, but the native loop did not consume confirmation. Accordingly the 10-second receipt-anchored scientific deadline never started. No argument, manager, name or initiating-thread contract was acquired. There is no evidence here that the request executed on a new unarmed thread, nor proof that the static candidate is wrong. The only recorded exception debug event was the owned attach break-in; the adapter did not log the process exit code. The cause of the game exit remains unresolved, with debugger intervention a material possibility.

Separately identified cleanup defect (STATIC implementation plus RUNTIME counterexample): rf_core.h throws on EXIT_PROCESS_DEBUG_EVENT without continuing it. The catch path attempts recovery suspension against the exiting target, fails, then waits for process completion while the exit event is held. This explains the stuck controller; it does not explain the earlier target exit. DebugSetProcessKillOnExit(FALSE) was established on successful attachment. The externally stopped controller was identity/hash checked and its raw evidence copied first. No game force-kill, exception suppression, code patch or retry was performed. Fixing this handler would exceed narrow 0.1.2 enablement and is deferred to review.

Raw local-only live-02/capture.native.jsonl: 272,556 bytes, SHA-256 8606daadbbe11e399e9bbd1842924ea2cc3746cf147ddb3b336883b1360bcfeb. It contains 343 debug events, 159 successful module-preflight records and the incomplete recovery boundary. The pre-controller-cleanup copy has identical bytes. outcome.json, operator-report.json and controller-cleanup.json are separate derivatives; do not insert missing terminal rows into raw evidence. live-01 remains preserved separately.

Post-attempt integrity reverified original Save3 and backup hashes, sizes and timestamps against the pinned baseline. All 217 historical evidence files and all built-source hashes remain unchanged. Save-folder metadata showed no file newer than the pre-existing 2026-10-06T23:28:30Z exit save; this supports no newly visible save file at inspection, not a semantic save-format claim. No save contents were parsed except protected-parent hashing; no archive/delete or save modification was performed. C:/D: remained above40GB. Stage-A candidates and the failed0.1.0 / qualified0.1.1 outcomes are preserved without reinterpretation.

Subsequent interpretation only,2026-10-07: [offline comparison](exp0002a-crash-dump-comparison.md) interprets the preserved dumps and newly available event records. Both report a single-step at REQUEST_ENTRY, despite no ordinary adapter capture. Earlier raw run/collection records and incomplete classifications remain unchanged.
