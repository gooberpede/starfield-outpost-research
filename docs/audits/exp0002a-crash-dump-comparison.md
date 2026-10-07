# EXP0002A — offline comparison of the two DR0 failures

2026-10-07; authority SOR-D-0020 / [retained scope](../implementation-briefs/EXP0002A-offline-dump-comparison.md). Evidence SOR-EV-0007; finding SOR-F-0008. Publication REVIEW-REQUIRED; raw dumps, debugger output and private paths remain LOCAL-ONLY. No live action, save access, adapter change, installation, staging, commit or push was performed.

**Classification: SAME_FAILURE_MECHANISM at the observed exception signature.** Both dumps report `STATUS_SINGLE_STEP` at exactly REQUEST_ENTRY, on an armed thread, with DR0 equal to the site, DR7=1, identical bounded return chains, and the same WER crash bucket. This is decisive evidence that the site was reached in both failed runs. It does not identify the exact debugger delivery/ownership defect or prove every causal step from register installation to process termination. Both original adapter runs remain **INCOMPLETE_PRE_CAPTURE_TARGET_EXIT**; a later dump-derived finding does not make either an ordinary successful adapter capture.

## Inputs and preservation

| Property | SOR-EV-0007-A / broad-012 | SOR-EV-0007-B / single-013 |
|---|---|---|
| Original filename | Starfield.exe.10364.dmp | Starfield.exe.15608.dmp |
| Original directory | C:\Users\User\AppData\Local\CrashDumps | Same |
| Size, bytes | 152746596 | 152465020 |
| SHA-256 | ed6d66eab9696aae09b1de5d7edb7a74c449893fe8374c29582a9c152a49ff18 | 35da8e8b7459ec67ec30d9ad7fcb878cee38ac26f445cb603da68bfec9bf23eb |
| Original creation UTC | 2026-10-07T01:59:11.055345Z | 2026-10-07T04:35:14.462633Z |
| Original last-write UTC | 2026-10-07T01:59:12.079360Z | 2026-10-07T04:35:15.402928Z |
| Dump header UTC, one-second precision | 2026-10-07T01:59:11Z | 2026-10-07T04:35:15Z |
| Existing archive analyzed, relative to .local-work/exp0002a-adapter-0.1.3/ | crash-012-host/artifact-000.dmp | s2-crash-records/artifact-000.dmp |
| Archive creation UTC | 2026-10-07T04:22:39.736612Z | 2026-10-07T04:36:37.146849Z |
| Originating run | 0.1.2/live-02, target PID10364 | 0.1.3/s2-live-01, target PID15608 |
| Configuration | REQUEST_ENTRY, 92 existing threads; later threads unarmed | REQUEST_ENTRY, only selected existing TID19140; 91 members total |

The archive names predate this analysis; neither original nor archive was renamed, normalized or written. Initial and final hashes match each other and their pre-existing collection manifests. PID is now independently confirmed by each dump's MiscInfo stream, beyond the original filename/time correlation. Filesystem timestamps are reported to Python's microsecond precision, separately from dump-header and event times.

Both runs used Starfield **1.16.244.0**, pinned EXE SHA-256 `7e9adb1414a8e1b325e5e1f097b9b17b78deb7eebeda37a333351a43a60f9d28`. The current pinned image in `D:\ReverseEngineering\Starfield\Starfield.exe` independently rehashes to that value. Module timestamp `0x6a1e0c18`, checksum `0x061bf3b7`, image size `0x089c2000` agree with the module records. Full executable hash identity comes from the preserved run preflights and pinned image, not a claim that a partial minidump contains the entire executable.

Adapter0.1.2 source-set ID `2b5c2438a45e1c70414328437563ca5c400039e6c531ccf538847a27513f4628`; adapter0.1.3 source-set ID `138338e445a174b2037a251b7e95bd2f272fff805ecc6a01cded8f6909837d3c`, qualified build-02 executable SHA-256 `eb5ca14ad76ccb685daf6aed6f7ea8a81f99e43a7fa8e1ef277c7061ac391692`. Exact old package/build provenance remains in the [0.1.2 audit](exp0002a-adapter-0.1.2.md) and [0.1.3 audit](exp0002a-adapter-0.1.3.md). Both used plain Steam without SFSE/SorExp0002, pinned site bytes and frozen ownership. The intended one-request/10-second acquisition bound did not start in0.1.2 because of its operator synchronization defect; it did start before CLICK NOW in S2.

## Method and traceability

Existing Microsoft CDB/dbgeng **10.0.19041.5609**, installed under `C:\Program Files (x86)\Windows Kits\10\Debuggers\x64`, opened only the two archived files with `-z`. Local-only symbol directory and pinned executable directory were supplied; symbol environment paths were cleared, `-sins` used, and no symbol server or download was configured. No live attachment or target execution occurred. CDB and DLL hashes are retained in `tool-hashes.json`.

Commands: `.exr -1`, `.ecxr`, `r`, `r dr0,dr1,dr2,dr3,dr6,dr7`, `kn 10`, `lmvm Starfield`, `db @rip-10 L40`, `u @rip L10`, `~`, `.dumpdebug`, then `q`. Counts use CDB's default hexadecimal radix: the stack cap is16 frames and returned13. The result is based on exception/context/module/memory streams and bounded unwind, not a generic analyze summary.

The independently authored [bounded reader](../../debugger/exp0002a/inspect_minidump.py) cross-checks AMD64 stream records, context validity flags, raw stack return and32 dump-resident instruction bytes against the pinned PE. Each JSON context field and memory window includes its exact dump file offset. Exception stream offset is1620 in both; exception CONTEXT offsets are41680 and41632 respectively. Separate faulting ThreadList contexts at42912 and42864 agree on every extracted register. Both have flags `0x10001f`, including the debug-register group: **DR6=0 is present, not UNAVAILABLE**. Code windows are at dump file offsets152159020 and151848950. Their SHA-256 is `fd2719cc562926625e1305fed3c5b5913d953b9ea7717fe34fbb67562d4d2877`, matching the expected site and pinned PE file offset25410448.

Installed Windows SDK10.0.26100.0 `um/minidumpapiset.h` and `um/winnt.h` supplied file-format declarations only (SOR-S-0117 extension). No third-party implementation/header was copied or incorporated, no new dependency installed, and no new sibling-project code reused. Existing adapter provenance is unchanged. Microsoft tool/format credit is recorded in SOURCES/CREDITS.

## Fault state and direct comparison

| Property | 0.1.2 / broad DR0 | 0.1.3 / S2 single-thread DR0 |
|---|---|---|
| Exception code/class | 0x80000004 / STATUS_SINGLE_STEP | Same |
| Exception flags / parameters | 0 / count0, empty list | Same |
| Exception address / faulting RIP | 0x00007ff60bdec590 | Same |
| Faulting TID | 18056 / 0x4688 | 19140 / 0x4ac4 |
| Faulting module | Starfield.exe | Starfield.exe |
| Loaded game base | 0x00007ff60a5b0000 | Same |
| Faulting RVA | 0x0183c590 | Same |
| RSP | 0x0000002b1faff4c8 | 0x000000161b7cf6b8 |
| RBP | 0 | 0 |
| EFLAGS | 0x244 | 0x244 |
| TF / RF | 0 / 0 | 0 / 0 |
| DR0 | 0x00007ff60bdec590 | Same |
| DR1 / DR2 / DR3 | 0 / 0 / 0 | Same |
| DR6 | 0; B0 clear | Same |
| DR7 | 1; local slot0 enabled, execute condition | Same |
| Armed TID relation | Fault TID belongs to frozen92-member armed population | Fault TID equals selected sole DR0 owner19140 |
| RIP == REQUEST_ENTRY? | YES | YES |
| RIP near REQUEST_ENTRY? | YES, exact; byte delta0 | YES, exact; byte delta0 |
| DR0 == runtime REQUEST_ENTRY? | YES | YES |
| DR6 owned-bit evidence? | NO positive B0 evidence in saved context | Same |
| Top stack similarity | All13 CDB frame instruction/return addresses match | Same |
| Process-exit classification | Exception-associated APPCRASH, not evidence of ordinary intentional exit | Same |
| Ultimate OS process exit code | UNAVAILABLE; adapter did not preserve it | UNAVAILABLE; adapter saw no exit event |
| First/second chance | UNAVAILABLE | UNAVAILABLE |

The dump's AMD64 CONTEXT stores EFlags as32 bits; upper RFLAGS are UNAVAILABLE separately. TF clear excludes a saved trap-flag indication, not every possible source of a single-step exception. RF clear describes the saved context only; it does not prove a particular resume sequence. DR6 provides no positive hardware cause bit here. Do not turn zero into an inferred B0=1, or treat it as proof no hardware trap occurred. Exception code, exact armed site, DR0/DR7, matching stacks and WER jointly support the breakpoint-associated failure interpretation. This is not a recorded access violation, int3 breakpoint (`0x80000003`), or fast-fail.

Address normalization: `0x7ff60bdec590 - 0x7ff60a5b0000 = 0x0183c590`; pinned preferred image base `0x140000000 + 0x0183c590 = 0x14183c590`. The latter is the Stage-A static candidate, not a runtime address. Runtime bases happen to match across these two processes; no assumption of stable ASLR is needed.

At RIP, bytes `48 89 5c 24 10` disassemble as `mov qword ptr [rsp+10h],rbx`. Following bounded prologue instructions store RBP/RSI, push RDI/R14/R15 and allocate0x140 stack bytes. Full bounded bytes/disassembly remain in ignored outputs. These are entry/prologue instructions, not an observed exit routine. CDB only has export symbols: its distant Scaleform/ffx labels are nearest-export artifacts and must not be promoted to actual function identities.

Additional entry state: RCX=`0x000001b5e8ec9000` (broad) / `0x0000015dbeff9000` (S2); RDX=0, R8=`0xffffffff`, R9=0 in both. These agree with the static new-slot call shape but RCX remains a candidate manager pointer and a null RDX does not establish generated-name semantics. Manager fields+0x50/+0x8c are **UNAVAILABLE** in the bounded dump memory lookup. Raw96-byte stack windows are retained with offsets/hashes; shadow-space contents are not assigned argument semantics. No completion, manager lifetime, serializer execution or safe native ABI follows.

## Bounded stack, normalized

Both unwinds give the same sequence below; stack pointers differ. Entries after frame0 are unwind return locations, not independent proof that every named candidate function was called. Raw `[RSP]` independently confirms the first return address `0x7ff60bc1c1c3`, RVA`0x0166c1c3`: precisely after Stage-A's E8 call at static`0x14166c1be`.

| Frame | Instruction location, both dumps |
|---|---|
| 00 | Starfield+0x0183c590 / REQUEST_ENTRY |
| 01 | Starfield+0x0166c1c3 |
| 02 | Starfield+0x028d7ba6 |
| 03 | Starfield+0x028d80bf |
| 04 | Starfield+0x0254271e |
| 05 | Starfield+0x01890f06 |
| 06 | Starfield+0x01885d6f |
| 07 | Starfield+0x0188911a |
| 08 | Starfield+0x0189d7fb |
| 09 | Starfield+0x01881569 |
| 0a | Starfield+0x0365d896 |
| 0b | kernel32!BaseThreadInitThunk+0x14, VA0x7ff8cf227374 |
| 0c | ntdll!RtlUserThreadStart+0x21, VA0x7ff8cf8bcc91; return0 |

## Adapter observations versus dump/event evidence

| Observation | Broad0.1.2 | S2/0.1.3 |
|---|---|---|
| ARMED population / DR0 owners | 92 / 92; TID18056 present | 91 / 1; TID19140 selected and armed |
| Setup suspension/resume | 92 released | Selected thread released |
| Post-ARMED CREATE_THREAD | 0 recorded | 0 recorded |
| Post-ARMED exception events | 0 recorded | 0 recorded |
| Other post-ARMED debug events | 90 EXIT_THREAD; 1 EXIT_PROCESS | 0 of any type |
| Ordinary REQUEST_ENTRY captures | 0 | 0 |
| Capture window | No capture_started record before exit | Active04:35:05.340055Z to04:35:15.346745Z;10,000ms |
| Exit event | Event code5 seen01:59:21.348330Z; actual exit code not retained | No exit event or target_exit record |
| Retirement/recovery | Handler throws; recovery suspend fails error5; recovery hold | Raw NO_HIT at deadline; retirement SuspendThread TID196 error5, then recovery hold |
| Terminal record | None | None |
| Target outcome | User-reported exit; process absent; Steam synced | Same; no new save observed |
| Dump/event report | Single-step at armed REQUEST_ENTRY | Same, inside scientific window |

Native log SHA-256s: broad `8606daadbbe11e399e9bbd1842924ea2cc3746cf147ddb3b336883b1360bcfeb`; S2 `e204aa3deffb99ce0f81f48e81c0961638d1b0584a4a362209e3d407347299d9`. The broad log's `code:5` is the Windows debug-event type, **not exit status5**. No game termination was requested in either recorded outcome; controllers were stopped after target absence. Cleanup failure happened after the independently timestamped crash reports and cannot itself explain the earlier recorded fault at the site.

**Discrepancy:** the dumps and Windows report a REQUEST_ENTRY single-step exception that neither native adapter log surfaces. No-hit is not evidence that the path was unexecuted or that S2 selected the wrong thread. The0.1.3 exit handler's disposable test does not cover absent delivery; fixing a received exit event does not fix this missing-event boundary.

The preserved adapter's `owned_hit()` requires `(Dr6 & 0xf)==1`. The saved dump context would fail that predicate **if the same state were delivered**, but there is no corresponding logged exception event to demonstrate such rejection. Do not attribute all missing capture to this predicate, blindly relax ownership checks, or infer that RF was set/cleared by an unobserved adapter action. Dump-time context can differ from first-chance hardware state. Delivery, debugger association, context transformation, other in-process exception handling and logging visibility remain unresolved.

## Windows evidence and access limits

Earlier collection manifests are preserved unchanged and returned no matching Application events at that time. A fresh unelevated read of Application1000/1001, bounded to01:55–02:05Z and04:29–04:39Z on2026-10-07 and filtered for Starfield, **now returns three records per run**: one Application Error and two WER APPCRASH records. New records remain in `application-events.json`, separately from old collections; the reason the earlier query returned none is not established.

| Property | Broad | S2 |
|---|---|---|
| Application1000 UTC | 01:59:10.4326443Z | 04:35:13.934891Z |
| Application PID | 0x287c / 10364 | 0x3cf8 / 15608 |
| Exception / offset | 80000004 / 0183c590 | Same |
| Application/module version | 1.16.244.0 / 1.16.244.0 | Same |
| WER report ID | b060a400-e43b-4ddf-81d1-ce508c90ecee | 1ac49d36-51c6-4364-8966-a90fff6ebfdf |
| WER bucket | 2008904367921163929, type4 | Same |
| WER hashed bucket | d98f382e8ffcf4bdfbe10fe105abee99 | Same |

Event timestamps were serialized with the local UTC+11 offset and normalized here to UTC. Event module timestamp fields are0; do not substitute them for the nonzero dump/PE timestamp. WER grouping corroborates the signature; bucket identity alone would not prove root cause. Both exact ReportArchive folders named by the current WER events still deny directory access. That limitation is recorded in `wer-access.json`; no elevation, ACL changes, new handler, or tool install was attempted. No additional crash-log contents or complete WER metadata were recovered. Actual OS exit codes remain UNAVAILABLE.

## Interpretation and one next experiment

Strongest interpretation: the two ordinary-save attempts reached the same mapped entry on an armed thread and failed with a breakpoint-associated single-step exception that the adapter did not surface as an event/capture. The broad thread population and a wrong single-thread selection are unnecessary explanations. The useful Stage-A mapping is strengthened for this entry/caller only, not invalidated. Completion and safe invocation remain unknown; Stage C stays blocked.

Alternatives retained: an exception/context transformation could erase DR6 cause bits; debug association or event delivery could have failed before the research exception; an in-process handler could have changed the state; selected-thread suspend/context intervention may contribute independently of DR0; a software-raised single-step is not excluded by the saved context alone. The matched site, registers, stack and APPCRASH records make an unrelated arbitrary game fault less persuasive, but do not identify a unique underlying implementation bug.

**Recommend exactly one next live control, S1.5, for separate review:** use plain Steam/Save3 and the paused Save→New Save handoff; identify the new process's game-window thread afresh (never reuse numeric TID19140); reproduce S2's bounded selected-thread suspend/context-read/resume lifecycle and debugger attachment, **without any DR0/DR7 write**. Record identity, thread creation identity, debug state and raw debug events before ownership classification; activate the10-second window before CLICK NOW; one ordinary save, bounded retirement and delayed health observation. Preserve the existing save/disk/module protections. Do not implement or run this control under the present offline authority.

Reason: S1 passed but omitted S2's explicit selected-thread suspension. S1.5 removes that remaining thread-control confound before another hardware intervention. A pass would strengthen the case for DR-register/event-delivery interaction; a matching failure without register writes would implicate the shared thread-control/debugger lifecycle. A different failure is a separate result, not automatic proof. Neither outcome alone locates the event-delivery defect. Do not widen ownership, retry92 threads, remap the static chain, or treat a successful control as Stage-C authorization.

## Validation and review package

Both CDB runs returned0. Independent extraction reproduces both records, exception/ThreadList contexts agree, dump-resident code equals pinned PE, normalized addresses agree, first raw stack returns agree with the static call return, and the13-frame address chains match. Four original/archive hashes and sizes reverified unchanged. No original run log/source was edited. Internal link, whitespace, tracked-artifact and task-only diff checks are recorded with exact results in the [evidence index](../experiments/evidence/exp0002a-dumps/README.md). The full worktree contains earlier uncommitted work; review the task-only diff separately from the aggregate Git diff. No commit or push.
