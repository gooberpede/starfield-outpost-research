# SOR-EXP-0002A bounded manual-save capture

**Current controls — stop for review:** S0 no-debugger manual save passed and is archived; S1 debugger-without-DR0 save passed and is archived. S2 armed only the reviewed game-window thread, then the game exited after one click with no REQUEST_ENTRY evidence. A remaining pre-exit-notification cleanup defect is recorded; both processes are gone and sync completed. Crash dumps are secured locally. No widening/rerun or Stage C. The entire 0.1.2 evidence remains unchanged. [Full 0.1.3 audit](../../docs/audits/exp0002a-adapter-0.1.3.md).


**Current result — adapter 0.1.2:** the authorized Stage-B attempt reached ARMED on 92 existing threads. The operator clicked New Save once, then Starfield exited before any REQUEST_ENTRY capture. Evidence is incomplete; the controller exit-event recovery defect is recorded separately. Both processes are gone, the user reports Steam sync finished, and protected Save3 hashes remain unchanged. No retry or substantive adapter fix before review. Stage C remains blocked. [Live audit](../../docs/audits/exp0002a-adapter-0.1.2.md).

## Historical 0.1.1 qualification review hold

SOR-D-0017 selects **adapter0.1.1: one REQUEST_ENTRY, thread population frozen at ARMED, later threads recorded but unarmed, capture-first recovery**. [Current audit](../../docs/audits/exp0002a-adapter-0.1.1.md), [plan](next_capture_plan.json), [operator card](../../docs/experiments/EXP0002A-operator-card.md). The three focused disposable controls passed;0.1.0’s dynamic-new-thread retirement failure remains preserved. User manually terminated old PID16100 after review; no further cleanup required. Starfield mode and the historical x64dbg CLI remain disabled before target access. No live action follows from disposable qualification.

`maintainer/hardware_evidence.py` and `maintainer/lifecycle_checks.py` are offline-only reuse under SOR-P-0002; [exact provenance](maintainer/PROVENANCE.md). They read explicit historical disposable JSON records and return verdicts; no native debugger/process access or writes. `test_correction.py` validates the new plan/version and refusals, and optionally replays an explicit disposable record with in-memory negative controls; only its local output file is written. Dependencies are CPython standard library and these maintainer modules. `tooling_version.json` separates adapter0.1.1 from the reserved, unbuilt observer0.1.0; there is no generated plugin metadata/package yet. These checks are not live qualification.

## Historical x64dbg attempts

Authority: [native-save brief](../../docs/implementation-briefs/CODEX_RESEARCH_BRIEF_SOR-EXP-0002A_native_save_thread_mapping.md), SOR-D-0014. **Live setup failed; no ordinary save trace acquired. Do not rerun without reviewing the attach/pause failure.** [Research record](../../docs/experiments/SOR-EXP-0002A-native-save-thread-mapping.md). Current controller v4 is not observer0.1.0; no new SFSE package exists. v1 failed process access, v2 encountered unintended default TLS breakpoints, v3 disabled defaults but failed pause confirmation. All attempts detached; user exited normally. Raw v1/v3 restoration flags are vacuous for zero sites; v4 corrects reporting to null and adds counts, not live-tested.

## Historical x64dbg inputs, outputs and effects

| File | Reads/dependencies | Writes/effects |
|---|---|---|
| capture_plan.json | Independently checked retail instruction locations/hashes | Authored plan, no executable bytes; four software breakpoint sites |
| capture.py | Existing protected-parent baseline; original/backup integrity; target path/hash; SFSE file; loaded code; OS thread creation times; directory metadata; installed x64dbg | New ignored run root; attaches/pauses/resumes through x64dbg, four temporary INT3 execution breakpoints, bounded logs, removal/detach. Never calls a game function, deploys, launches game, edits/deletes saves or issues console commands |
| transport.py | Installed headless.exe command interface, supplied commands | Isolated local debugger settings/database; incrementally flushed JSONL stdout. fsync on SOR evidence/acknowledgments and final drain. No kill method; acknowledgment is not semantic validation |
| process_read.py | Explicit PID identity/debug state and bounded <=4096-byte reads through Windows APIs | No target writes/control APIs; used to verify loaded sites and restoration independently of debugger messages |
| fixture.cpp | One private trigger path | Original synthetic target; waits <=60 seconds for trigger, invokes known marker on startup/worker threads, then normal exit; optional 100-hit test. No game/save access |
| test_transport.py | Explicit original fixture and installed debugger | New ignored synthetic runs; exercises attach, production log expressions, breakpoint-byte insertion/restoration, two-thread logging, zero-hit deadline and 25-hit cap. No game access |

CPython standard library, installed MSVC/Windows SDK and installed x64dbg are separate tools. No downloaded dependency, debugger header/library, hook implementation or SFSE source is incorporated. Sources SOR-S-0113/0117/0121; Bethesda static inputs/Ghidra SOR-S-0104/0105. The script is source-informed command/API use, not a claim of clean-room isolation.

The local x64dbg `commithash.txt` reports `9c8ca1cae0b6d56cc44f31fddcb10e3b02ffbb87`; this does not prove reproducible source/binary equivalence. capture.py pins headless.exe, x64dbg.dll and x64bridge.dll hashes. Other installed support DLLs are external dependencies; this is not a hermetic debugger build. No plugins were present in the inspected plugins directory. A changed debugger/core/bridge or discovered .dp64 autoload stops capture. Local symbol lookup produced missing-PDB messages; no symbol-download command was requested.

## Historical four-site configuration — not current

| Label | Retail RVA | Capture purpose |
|---|---|---|
| REQUEST_ENTRY | 0x0183c590 | Actual request TID, RCX/RDX/R8/R9, caller stack, candidate manager +0x50/+0x8c state |
| NEW_SLOT_RETURN | 0x0166c1c3 | Specific normal UI new-slot caller continuation; raw RAX and RSP/TID correlation |
| SERIALIZER_ENTRY | 0x01814220 | Independent TID, pointer-to-object argument, arguments and bounded name bytes |
| COMPLETION_WAKE | 0x0183b86d | Finalization epilogue after manager +0x8c exchange; wake address/value, TID and stack |

Static VA = 0x140000000 + RVA. Live VA = observed module base + RVA. Code windows are checked before arming; their original bytes are re-read after detach. The completion site is a candidate state transition, **not** a durability certificate. Successful result.json acquisition never means successful save qualification.

All sites log raw registers and 96 stack bytes, with read-validity indicators. Serializer name capture is at most 260 raw bytes; encoding/name role needs interpretation. Invalid reads remain invalid evidence, never silently valid zero pointers. These are bounded stack bytes, not a trustworthy unwound call chain. RSP/TID and the known caller must agree before pairing request/return. No thread is preselected or assumed to be main.

The first window covers one operator new-slot save, <=10 seconds after arming, <=25 hits/site (<=100 total). Each site's 25th hit stops target execution until cleanup. The independent controller clock handles zero hits. Capture ends earlier once return and completion-candidate records exist; that is an acquisition condition only and needs later correlation. Capture output <=2,000,000 debugger-text bytes; individual line <=32,768 characters. Directory metadata polling is every 50 ms in this window, not game-state polling. C:/D: available space must remain >=40,000,000,000 bytes. Initial debugger startup <=20 s, attach acknowledgment <=10 s, pause confirmation <=5 s; individual setup command <=5 s. OS/tool/file operations and cleanup can overshoot nominal time. No hard real-time guarantee or cancellation of an in-progress filesystem call.

## Intervention and cleanup

Software breakpoints temporarily replace one instruction byte with INT3 and the debugger performs its ordinary trap/step/resume mechanics. Attachment and pauses change scheduling. This is **not non-invasive**. No arbitrary patches, gameplay register changes, exception suppression or native save invocation are supplied. Unexpected exception output ends acquisition; no automatic resume-through-exception loop is used. Crash-tolerant means preserved records may remain useful; a missing/truncated record is incomplete.

Cleanup requests pause, clears only the four attempted sites and detaches. Independent OS debug-state and 32-byte readback verify cleanup while the process survives. If it exited, restoration is recorded unavailable, not passed. Failure to verify detach/restoration creates recovery-required.json and holds the controller/debugger alive. Do not close/kill them; recover under review. No automatic target termination/relaunch/retry. Output-write failure can prevent a final record; preserve whatever reached disk. A debugger crash/pipe failure can affect the target despite the absence of a kill command.

Original/backup hashes and timestamps are rechecked after the window. No save is archived or deleted by this tool. Filesystem metadata observations cannot prove close, durability, cloud synchronization, reload validity or semantic equivalence. After user normal exit and sync confirmation, separately correlate/copy/hash the resulting file and any exit save.

## Historical researcher operation — disabled and superseded

The old profile requirement below describes failed historical attempts only. Current Stage B uses ordinary Steam without SFSE, verifies SFSE/SorExp0002 module absence, and follows [the current operator card](../../docs/experiments/EXP0002A-operator-card.md). Vortex/SFSE deployment is reserved for separately authorized Stage C.

The obsolete `--profile-sfse-only-confirmed` flag remains only inside the disabled historical function, explicitly labelled historical. No current invocation uses it.

For interactive coordination, the researcher must run this as a hidden background helper with stdout/stderr preserved. After prepared.json, create arm.signal in that exact run root within60 seconds; while waiting, the game is paused. Verify the ARMED stdout marker and announce the short save window promptly. Do not mistake prepared.json or armed.json alone for a running target. Never arm before the operator is waiting at the new-slot action. No save if setup fails. If the operator misses the window, keep the zero-hit record and review before another attempt. Restricted tool execution could not acquire x64dbg's required process access; the two actual attachments used an approved execution escalation, not a game privilege/configuration change.

## Actual qualification and limits

Synthetic results under `.local-work/exp0002a/`: transport-two-threads-03, transport-zero-hit-02 and transport-hit-cap-02. Known arguments captured on distinct startup/worker TIDs; zero-hit timeout detached; cap produced exactly25 hits; restored bytes and normal fixture exit verified. Four production log formats were evaluated. Later transport-tls-disabled repeats two-thread/format/restoration checks with explicit isolated Events settings. Starfield attachments occurred in manual-002/003, but no four-site save sequence, file-write timing, crash durability or native invocation was qualified.

Fresh isolated headless.ini now disables TlsCallbacks/TlsCallbacksSystem, DllEntry/DllEntrySystem, DllLoad/DllLoadSystem and ThreadEntry/ThreadStart. The controller rejects unexpected automatic-breakpoint setup rows. Earlier default TLS sites were a disclosed deviation; separate readback verified all four observed extra32-byte windows against their DLLs after detach. Headless defaults must not be assumed safe merely because a synthetic executable has no relevant TLS callbacks.

Earlier transport attempts are preserved: immediate exit raced command initialization; a QUERY_LIMITED_INFORMATION handle failed detach-state verification; fsync on every verbose startup line delayed acknowledgments. Corrections wait for initialization, use QUERY_INFORMATION, and synchronize evidence/acknowledgment boundaries. Failed synthetic target outcomes were not independently established and must not be called normal exits. No game was involved.

Fixture build uses installed vcvars64.bat and `cl /W4 /O2 /EHsc /std:c++20`, exporting only the original marker. The local build command/output/identities are in the evidence root. Never use `test_transport.py` with an unrelated executable renamed fixture.exe. Synthetic tools do not grant live authority.

## Current native adapter0.1.1 — disabled for Starfield

native/adapter.cpp and adapted native/rf_core.h implement the one-request handshake/capture/retirement. The native --starfield entry refuses before process access. --fixture accepts only the exact adjacent fixture path/hash compiled into the generated identity header; --fixture-retirement-fault adds an explicitly labelled disposable-only failure before detach, after durable capture and retirement work. Neither entry launches a target. The capture-first recovery gate can terminate only the retained, reverified experimental process after complete flushed evidence, or after an independently measured low-disk condition. The final record separates evidence completeness, acquisition status, cleanup status and target outcome.

build_adapter.py --output <new-folder-under-.local-work/exp0002a-adapter-0.1.1> reads local sources/plan/version and installed MSVC/SDK; writes only that create-new ignored directory, generated header, EXEs/OBJs/logs/manifest. No game/deployment access or downloads. The adapter binary is named save_request_adapter-0.1.1.exe. No SFSE plugin or package is built; observer0.1.0 remains reserved separately.

qualify_adapter.py --build <build-folder> --output <new-evidence-folder> verifies source/binary hashes, launches only its own hidden paired fixture/adapter and runs three focused controls: existing-thread capture with two new unarmed workers, new-thread-only NO_HIT, and post-capture retirement-fault recovery. Writes create-new evidence and trigger/confirmation/cooperative-stop files; no runner kill or automatic retry. On failure it records the error/PIDs and stops. The adapter itself owns the tested destructive-recovery gate. Fixture normal loop has a90-second bound; scheduling/debugger faults can prevent cooperative exit. A pre-flush unresolved failure remains a review hold absent machine safety.

Normal cases validate all three workers through15-second health and normal exit; the injected recovery case validates durable evidence before exact-handle termination. Raw native presence is not functional-health proof, and complete evidence is not game semantics. Both Python scripts use only the standard library. The native fixture has no game/save/plugin access. After these focused runs, return for review without further qualification or Starfield launch.

## Offline dump reader

`inspect_minidump.py --dump <existing-dump> --image <pinned-PE> --output <new-json>` reads only the explicit AMD64 minidump and PE, using installed Python's standard library. Writes one create-new JSON under `.local-work/exp0002a-dump-comparison`; refuses overwrite/outside-root output. No process APIs, game/save access, downloads, live attachment or analysis-database changes. Installed Windows SDK format declarations inform independently authored field offsets; no header/implementation incorporated. Records validity flags and file offsets, exception/control/debug registers, module normalization and bounded memory windows. Missing ranges are UNAVAILABLE. Not a general minidump validator; bounded memory reads do not stitch across range boundaries. CDB separately provides unwind/disassembly. [Comparison and reproduction limits](../../docs/audits/exp0002a-crash-dump-comparison.md).


## Final software attempt (supersedes prospective hardware instructions)

SOR-D-0021 authorizes one CDB/dbgeng one-shot software breakpoint only. Native adapter0.1.3 is historical and must not be used for another hardware run. final_deadline.py version0.1.4 is a narrow log-flush/deadline guard, not a new debugger adapter/framework. It reads explicit target identity/hash, disk space and bounded CDB log; writes receipts under .local-work/exp0002a-final-software; may request one exact-target debugger control break at the deadline. No DR writes, launch, detach, termination or retry. See [authority](../../docs/implementation-briefs/EXP0002A-final-software-attempt.md) and [actual preparation/result](../../docs/audits/exp0002a-final-software-attempt.md).
