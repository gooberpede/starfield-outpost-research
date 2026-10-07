# EXP0002A — Steam correction and adapter qualification

2026-10-07 Australia/Sydney; SOR-D-0016. **Adapter implemented; disposable qualification FAILED. Do not enable Starfield mode.** No Starfield launch/attachment, deployment, game/save/configuration change, commit or push occurred. Stage A is preserved and Stage C remains blocked.

## Current launch and capture contract

Prospective Stage B is ordinary **Steam without SFSE**. No Vortex/SFSE-profile attestation is required. The native preflight enumerates loaded modules and rejects case-insensitive basenames beginning with sfse or sorexp0002; incomplete enumeration fails closed. It repeats the check before ARMED and on DLL-load events. Disk presence alone is not evidence of loading. Renamed/manual-mapped modules are not detected by this basename policy.

The [operator card](../experiments/EXP0002A-operator-card.md) retains: launch normally, load disposable Save3-based state, Pause > Save > highlight New Save, **do not confirm**, report ready; only then attach/configure. Validate PID/image hash/base/code hash, absent forbidden modules, complete existing-thread inventory and owned hardware state. Release setup stops and report ARMED; only then user confirms once. No current live command is provided: the native --starfield entry refuses before target access.

Selected backend remains maintainer Win32 hardware/RF after the earlier ordered Ghidra/dbgeng assessment. Explicit OS-thread ownership, one DR0 execution address and RF continuation fit this request. The new failed lifecycle evidence weakens readiness; it does not justify a silent x64dbg fallback or reject the static save path.

Exactly **REQUEST_ENTRY at observed base +0x0183c590**, 32-byte SHA-256 fd2719cc562926625e1305fed3c5b5913d953b9ea7717fe34fbb67562d4d2877. Game SHA-256 remains 7e9adb1414a8e1b325e5e1f097b9b17b78deb7eebeda37a333351a43a60f9d28. No serializer/completion/return research breakpoint.

The adapter records TID, module base/RIP/RVA, RSP, RCX/RDX/R8/R9, RAX/EFLAGS/DR6, raw return validity/value and expected game caller comparison, 96 stack bytes, candidate manager+0x50/+0x8c reads, and null or at most260 name bytes at RDX. Fixed reads include validity/length/error; raw name bytes are not an inferred generated filename. Optional unwinding is explicitly not requested; raw return is primary. Mismatched game arguments are evidence, not forced values.

Setup has a300-second watchdog separate from120 seconds waiting for operator confirmation. One request or a10-second no-hit deadline after after-click confirmation receipt bounds acquisition. A hit arriving before receipt is durably retained provisionally and retired immediately; subsequent confirmation does not prove causality. Actual click time remains distinct from receipt/first-hit time. The fixture deliberately delays receipt. Windows/filesystem operations are not hard real-time cancellable. Capture, retirement and health records carry monotonic ticks, UTC FILETIME, version and source identity.

Evidence uses WriteFile/FlushFileBuffers before retirement. Normal retirement is bounded by15 seconds/1024 events, restores owned DR0/DR6/DR7, balances owned suspensions, checks code hash/debugger absence, and checks presence at0/1/5/15 seconds. The separate fixture validator checks actual worker progress and cooperative exit. The recovery path is best effort, not qualified as a safe game recovery mechanism; unresolved recovery holds rather than killing/suppressing exceptions. Two quiet event waits are an empirical boundary, not an OS guarantee that all latent exceptions are gone. The new failure demonstrates this limitation.

## Implementation and provenance

Sources: [adapter.cpp](../../debugger/exp0002a/native/adapter.cpp), [rf_core.h](../../debugger/exp0002a/native/rf_core.h), [request_fixture.cpp](../../debugger/exp0002a/native/request_fixture.cpp), [build_adapter.py](../../debugger/exp0002a/build_adapter.py), [qualify_adapter.py](../../debugger/exp0002a/qualify_adapter.py).

rf_core.h adapts the maintainer-owned sibling core at commit6a77579a184c64e0c080c8f3b7883c34bd17e24b, source SHA-256 190aead16b8dcd9b6f7d3dd5561b53a4f458c498f49362de5a23af9dd6ed3751. Original main/capture are removed; logging, bounds, setup/new-thread handling and no-held-event retirement are adapted. New adapter uses the consulted smoke adapter's module/break-in approach. [Per-file provenance](../../debugger/exp0002a/maintainer/PROVENANCE.md) distinguishes copied/adapted/conceptual work. No third-party debugger implementation or new dependency is incorporated.

The build uses installed MSVC/Windows SDK, C++17, /W4 /WX, and system bcrypt for SHA-256. It generates an ignored identity header from the sole0.1.0 version source, plan, fixture PE export and source hashes. Every native evidence row carries0.1.0 plus exact source ID; manifest pins binaries and generated fixture site. These are unreviewed development builds of tooling0.1.0, not observer DLLs or packages. Observer0.1.0 remains reserved; no plugin metadata or package was fabricated. Historical reviewNN/v1–v4 are unchanged. Vortex/SFSE deployment and matching observer package/metadata/evidence/manifests apply only to later separately authorized Stage C; subsequent reviewed patches increment0.1.1,0.1.2.

## Fresh qualification and counterexamples

Local evidence root: .local-work/exp0002a-adapter/. No historical replay substitutes for these trials. Only four fresh disposable attachments occurred: one failed initial case, then the three requested cases after the handle correction. No retry followed the new-thread failure.

| Build/run | Result | Evidence and limit |
|---|---|---|
| build-01 | Compile failed | /WX rejected two unused inherited helper functions. No target launched; removed unused helpers |
| build-02 / qualification-01 existing | FAIL | Captured expected one request; detach returned access denied, then one resume failed with invalid handle. Initial adaptation had closed Windows-managed debug process/thread handles too early. Failed record/source/binaries retained |
| build-03 / qualification-02 existing | PASS | Already-running fixture; delayed trigger; exactly one known request, raw stack argument/return and null-name checks; provisional hit before confirmation receipt; restored registers/bytes, detached, continuing worker through15 seconds, normal fixture exit |
| build-03 / qualification-02 timeout | PASS | Already-running fixture, delayed confirmation, zero hits,10-second receipt-based timeout; restoration/detach, progress through15 seconds, normal exit |
| build-03 / qualification-02 new | **FAIL** | Two fixture worker threads created after ARMED; one request retained, nonnull name captured. Native cleanup/presence checks reported success, but one worker stopped at pulse1, only one of two fixture calls completed, and cooperative exit timed out. No claimed healthy new-thread lifecycle |

Final compiled native source ID 0f13ab636778f934ac78bec7b9750687317a4b08c6bcc1f6188d42a1e44c1845; adapter SHA-256 a2c3eb979143ce1925710935808d1261890174ec0e7d21dcd6196e67d51cd6cb; fixture SHA-256 bd492883b90e2618c6bad3e0610822520fe5068e4f681a81d2bc25ee7b3ba0bb. Build manifest SHA-256 65dbcede086128983705dba2f629237b835eddc2ed650796779556be55466d88. Native complete.success covers its acquisition/API checks, **not** the independent qualification verdict. qualification.json contains only completed passing cases; the failed new case is documented here and in qualification-summary.json.

The handle correction follows Microsoft's [WaitForDebugEvent handle ownership](https://learn.microsoft.com/en-us/windows/win32/api/debugapi/nf-debugapi-waitfordebugevent) and [ContinueDebugEvent cleanup](https://learn.microsoft.com/windows/win32/api/debugapi/nf-debugapi-continuedebugevent) documentation. Independently opened handles are retained; OS-managed event handles are not prematurely closed/recycled. No Microsoft example source was copied. For the first failure, fresh handles verified the exact fixture PID and resumed only the two recorded still-owned suspension counts (both returned1). The fixture then logged its normal exit; adapter completed with failure. No forced termination or exception suppression.

The final new-thread failure is an observed stalled worker, not a proven exception code or established root cause. A latent competing debug exception is a hypothesis. The two workers exercise retirement contention in a bounded case; no stress matrix was run. Pending-event accounting returned zero despite failed progress, so it cannot certify complete event-state retirement. The disposable PID16100 remained stalled at the final check, with stop signal already present; debugger process exited and owned suspensions had balanced readbacks. No repeated resume, injected exit or forced kill was attempted. Any forced cleanup requires an explicit exception to the current no-kill plan.

## Review package and remaining gate

[Task-only diff](../../.local-work/exp0002a-adapter/adapter.diff), [complete working-tree diff](../../.local-work/exp0002a-adapter/review.diff), [Git status](../../.local-work/exp0002a-adapter/status.txt), [validation and changed files](../../.local-work/exp0002a-adapter/validation.json), [qualification summary](../../.local-work/exp0002a-adapter/qualification-summary.json), [build manifest](../../.local-work/exp0002a-adapter/build-03/manifest.json). New files are included without staging; prior Stage-A work remains separately identifiable.

No engine finding is promoted. The reviewed architecture has an unresolved retirement/new-thread failure in this adaptation. Return for review before more qualification or any Starfield launch/trace. Stage C still needs ordinary-save live evidence establishing initiating context, manager/object, arguments, naming and request/completion relationship. A one-entry synthetic capture establishes none of those game semantics.
