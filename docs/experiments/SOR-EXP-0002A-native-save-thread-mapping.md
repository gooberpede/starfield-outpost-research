# SOR-EXP-0002A — Native save request and execution context

**Latest controls:** S0 and S1 passed; S2 single-thread DR0 attempt exited without request evidence. [0.1.3 audit](../audits/exp0002a-adapter-0.1.3.md). Stop for review; no ownership widening or Stage C. Historical results below remain unchanged.


**Latest Stage-B outcome, 2026-10-07:** approved adapter0.1.2 reached ARMED with92 existing threads; one ordinary New Save click was followed by target exit before REQUEST_ENTRY evidence. No live save contract acquired. The stuck controller was closed separately after preserving evidence; user reports sync finished and protected parents match. [Full live audit](../audits/exp0002a-adapter-0.1.2.md). Stage C stays blocked; next substantive changes/live attempt require review.


**Current Stage-B launch correction, SOR-D-0016:** ordinary Steam without SFSE; verify SFSE/SorExp0002 are not loaded. Vortex/SFSE deployment belongs to later Stage C only. [Adapter and disposable qualification](../audits/exp0002a-adapter-qualification.md). No new Starfield trace is authorized.

**Correction, SOR-D-0015 (2026-10-07):** the prior failures are debugger setup/transport failures, not a test rejecting the static save path. Stage-A mapping below is preserved. [Current correction audit](../audits/exp0002a-debugger-correction.md) selects a one-site Win32 hardware/RF preparation after ordered Ghidra/dbgeng assessment, separates setup from confirmation-based capture, and disables the old x64dbg CLI. No new live attempt, deployment or launch until review; Stage C remains blocked. Historical four-site preparation and attempt descriptions below are not the next-run plan.

**2026-10-07, Australia/Sydney. Stage A ANALYZED; Stage B setup attempted, no manual-save trace acquired; Stage C not entered.** Authority: [invoked brief](../implementation-briefs/CODEX_RESEARCH_BRIEF_SOR-EXP-0002A_native_save_thread_mapping.md), SOR-D-0014. SOR-EXP-0002 remains paused before A1. User exited normally, reports sync complete and no manual save. Review is required; this report does not approve integration.

The current retail instructions support a higher-level request candidate at `FUN_14183c590`, reached from the ordinary UI's new-slot branch. They also expose a distinct serialization and finalization path. **No live call contract or safe plugin invocation is established.** The older SFSE relocation sites do not match this binary and must not be transferred. Observer `0.1.0` has not been built or deployed.

## Question, controls and provenance

Determine which ordinary manual-save operation, execution context, arguments and completion signal could support one later observer checkpoint. Compare direct retail instructions with the pinned SFSE source lead; then compare the proposed trace against an original synthetic target with known arguments and two threads. Synthetic debugger behavior is not game qualification. No outpost construction, native selected-reference query, console, save parsing/editing or achievement test occurred.

SOR-ENV-0003 revalidates Starfield 1.16.244.0, SHA-256 `7e9adb1414a8e1b325e5e1f097b9b17b78deb7eebeda37a333351a43a60f9d28`, preferred base `0x140000000`. Addresses below are **static VA**; RVA is VA minus that base. Runtime ASLR base in manual-002 was `0x7ff60a5b0000`; save-call pointers/TIDs remain UNKNOWN. Neither an RVA nor an object-relative operand is a save-file offset. Existing Ghidra 12.1.2 analysis was exported with `-readOnly -noanalysis`; no new analysis, symbols, types or comments. CK inputs were rehashed but no new CK mapping was needed.

SOR-EV-0005 [evidence index](evidence/exp0002a-static/README.md) identifies local exports, independent PE windows, synthetic records and preservation checks. All raw decompilation, instruction bytes, logs, private paths and debugger databases are LOCAL-ONLY. Authored summaries/addresses/hashes are REVIEW-REQUIRED, not publication-cleared.

## Source lead and rejected transfer

SOURCE-REPORTED: SFSE pin `48535cc4306ab345252bf740c20a1c6194929b0e`, `sfse/Hooks_Serialization.cpp`, declares a save call at RVA `0x02551df0 + 0x12b`, original target `0x02554fd0`, and a four-argument hook involving BGSSaveLoadGame and a name. Its hook installation is disabled with `#if 0`. Credit SOR-S-0120 and earlier SOR-S-0118. This is a discovery lead, not a current address/ABI contract.

PROJECT-VERIFIED STATIC: the alleged call at VA `0x142551f1b` starts with `0x81`, not an E8 call, and is not an existing Ghidra instruction start. `0x142554fd0` is not a defined function entry. The failed source-site export is retained. No relocation, hook body, type definition or source signature was incorporated. Existing permission SOR-P-0001 still covers only the previously approved PluginAPI.h use.

## Current candidate map

All original identifiers are Ghidra-generated `FUN_` names, not recovered symbols. Roles/signatures are **PROVISIONAL**, inferred from call-site instructions and decompilation. Direct calls listed below were independently decoded from the pinned PE. Return types, lifetime, reentrancy, complete locks, ownership and thread prerequisites remain unqualified.

| Original function / static VA | RVA | Candidate role, arguments and relationships | Side effects and limits |
|---|---|---|---|
| FUN_14166c0a0 | 0x0166c0a0 | UI selection callback; obtains selection through 14166e4a0; direct or queued dispatch to 14166c190, queue thunk 14166f3c0 | Reads service global 145fd9b80 +538; original UI initiator may differ from request thread. Full callback ABI unresolved |
| FUN_14166c190 | 0x0166c190 | Save-selection handler. New slot uses EBX=-1. At 14166c1af–1be: RCX=[145e6d6e8], RDX=0, R8D=EBX, R9D=0, call 14183c590; return 14166c1c3 | Other branches route existing names through 14183c3c0 or 14183c590 and later 14184cee0 bookkeeping. Never invoke the UI callback with guessed arguments |
| FUN_14183c590 | 0x0183c590 | Highest current practical request candidate: RCX manager, RDX optional name, R8D slot/index candidate, R9D option of unknown semantics. Calls 14183c830 at 14183c65d | Tests manager+50, calls status helper 141850940(manager,5), records timings +950/+960, gate 141846ef0; creates name/storage; serialization and finalization; changes +170 and +108/+110/+118. AL is a bool-like result, not durability |
| FUN_14183c830 | 0x0183c830 | Preparation/file-object path; calls 141814050 at 14183c9a0; original RDX contains name at object start | Object also carries +108 storage pointer/+110 status. A plain character buffer is not a qualified replacement. Error/quota paths and 14184ab70 metadata update |
| FUN_141814050 | 0x01814050 | Name/serialization wrapper; uses global 145e6d6e0, builds name with .sfs; captures context for callback 141822170 -> 141821b70 | Diagnostic saving-game text; BSComponentDB command dispatch then helper 1423ff430. Stack-backed captured values suggest synchronization; asynchronous return is NOT established |
| FUN_141814220 | 0x01814220 | Serializer candidate, called at 141821ba8. RCX points to a stored object pointer, RDX to service reference, R8 original file/storage object, R9 generated name buffer | Entry dereferences RCX and locked-ORs object+3a8 with 4. BGSSaveLoadGame::SaveGame diagnostic at 141814a97. Large body; not fully mapped. Old source's direct-this ABI must not replace observed indirection |
| FUN_14183aaf0 | 0x0183aaf0 | Finalization setup; manager/file inputs and R8B flag. With flag1, exchange sets manager+8c at 14183ab21. Direct call 14183ac80 at 14183ac25 or callback thunk 141855a20 | Scheduling/storage-dependent branches; exact ownership and wait semantics unresolved |
| FUN_14183ac80 | 0x0183ac80 | Completion candidate: context holds manager/file, DL status. Local-storage branch closes/frees storage, handles temporary/final/backup names and errors | Conditional _wrename/DeleteFileA and cached-path helper calls. At 14183b850 clears manager+8c; epilogue 14183b86d tail-jumps through WakeByAddressAll IAT. This is not proof of disk durability or cloud completion |

Supporting candidates: `14184eec0` (RVA0184eec0) generates names using Save/Autosave/Quicksave/Exitsave prefixes; `14183a8d0` (0183a8d0) constructs the file/storage context; `141846ef0` (01846ef0) checks menu/player/game conditions; `141850940/1418509c0` (01850940/018509c0) handle status changes. Manager-construction candidate `141839c60` (01839c60) has BGSSaveLoadManager/BGSSaveLoadThread names and an AsyncRequest queue, including the SaveLoad thread label at `14183a11e`. Thread naming alone does not prove which thread executes this manual path. `14166cf00` references PauseMenu_DeleteSave while registering UI behavior; it is **not** a demonstrated deletion implementation.

Independent E8 checks: `14166c1be -> 14183c590`, `14183c65d -> 14183c830`, `14183c9a0 -> 141814050`, `141821ba8 -> 141814220`, `14183ac25 -> 14183ac80`. See SOR-F-0007 and capture-sites.json. The request's RDX is treated as narrow name data downstream despite a decompiler wchar_t annotation; do not adopt that annotation as a type declaration.

## Thread map and live contract

| Context | Evidence/status |
|---|---|
| Plugin-load / SFSE loader-reported startup thread | No EXP0002A plugin/load observation. Historical review14 loader TID21756 is session-specific |
| SFSE AddTask dispatch | Historical A0/A0C TIDs15592/21756; no single-thread contract. SOR-EV-0004 is preserved, not relabeled as this run |
| UI initiating thread | UNKNOWN. Direct/queued dispatch split statically visible; four-site first trace does not instrument the earliest UI callback |
| Save-manager request thread | UNKNOWN until REQUEST_ENTRY; planned capture includes TID/RIP/registers/stack |
| Serializer / finalizer thread | UNKNOWN until SERIALIZER_ENTRY / COMPLETION_WAKE; captures can expose differences, not all file-worker threads |
| Thread creation / process-start relationship | Planned read-only OS thread creation inventory. Earliest visible thread is not automatically the original startup thread; do not infer current thread identity from historical SFSE loader evidence; prospective Stage B excludes SFSE |

No runtime object identity, argument values, acceptance/completion latency or designated dispatcher was recovered. Static new-slot arguments predict manager/null/-1/0, but do not qualify a native invocation. Even a successful manual-save trace cannot establish that this context is safe for GetWorkshop. Selected-reference lifetime, callback convention and thread safety need their own qualification.

## Historical bounded x64dbg capture preparation

Tool revisions `SOR-EXP-0002A-x64dbg-capture-v1` (manual-001), v2 (manual-002 coordination handoff), v3 (manual-003 automatic TLS breakpoints disabled), v4 (post-run reporting correction; not live-run). Plan and effects in [debugger README](../../debugger/exp0002a/README.md), user steps in [operator card](EXP0002A-operator-card.md). Installed x64dbg headless source revision label `9c8ca1cae0b6d56cc44f31fddcb10e3b02ffbb87`; actual executable/DLL hashes pinned in the tool and evidence index. Source label is not a reproducible-build claim. CPython 3.14.3; original fixture built with installed MSVC/Windows SDK. No new dependency installation or downloaded implementation.

The exact four software execution breakpoints are request entry RVA0183c590, new-slot return RVA0166c1c3, serializer entry RVA01814220, and completion wake RVA0183b86d. Each requires a matching 32-byte loaded-code hash before insertion. INT3 insertion, pauses, single-step/rearm and debugger scheduling **intervene in execution**. They may change timing or crash the process. No unrelated writes, exception suppression, game launch, console or native invocation are implemented.

One operator new-slot save; stop after 10 seconds armed, 25 hits at any site (at most100 relevant hit records), or request-return plus completion-candidate observation. Fixed-size reads: 96 stack bytes, 260 serializer name bytes and selected manager/status fields; invalidity retained, no arbitrary pointer traversal. Raw stack words are not a symbolized or validated caller chain. UTC log receive time and debugger ticks are different clocks; file metadata is sampled at approximately50ms, not a write/flush trace. A completion candidate might belong to other save activity: correlation must be assessed before promotion.

Preflight rehashes protected parents, game, SFSE and debugger; rejects existing debugger/historical observer, requires current user profile/scene confirmation and >=40,000,000,000 bytes free on C:/D:. Evidence is flushed incrementally; critical SOR records are fsynced. Output is bounded. Clear only this run's breakpoint sites, detach, independently verify debugger absence and original bytes. Failed restoration/detach holds the controller alive for recovery; no forced termination/retry. On target exit, byte restoration is unassessable. Keep save artifacts untouched until normal exit/review.

## Actual validation and failures retained

- Independent PE checks verify the five direct calls and four 32-byte site hashes. Ghidra name scan terminates normally; lexical/reference/instruction caps mean this is not exhaustive coverage.
- Latest synthetic two-thread run (`transport-two-threads-03`) recorded two hits with known arguments1–4 and5–8 on distinct TIDs20668/2836. All four production log expression formats evaluated. Software-byte insertion, full32-byte restoration, OS detach and normal fixture exit0 verified.
- Latest zero-hit run (`transport-zero-hit-02`) terminated at its synthetic deadline with no hits, restored bytes, detached and exited0. Hit-cap run (`transport-hit-cap-02`) produced exactly25 records, restored bytes, detached and exited0. These test transport/cleanup components, not the entire game's capture lifecycle or safe Starfield attachment.
- First two-thread attempt failed independent debugger verification because the initial OS query access mask was insufficient; its debugger log reported detach but that is not accepted as independent verification. First hit-cap attempt timed out waiting for an acknowledgment during excessive per-line fsync backlog; revised transport fsyncs evidence/command boundaries. Failed attempts remain unassessed rather than silently promoted by later passes. No synthetic target process remained when checked afterward.
- Partial `source-sites` export failed at the stale source address; partial `final-windows` export failed at a guessed non-instruction center. Corrected exports were created under new names. Headless wrapper exit0 did not imply successful script completion. A premature headless command smoke test also failed; waiting for initialization fixed command sequencing.
- Several large functions reach the600-instruction export cap, including serializer/finalizer/name generation; retained decompilation is interpretation, not a substitute for uncaptured instructions. Unknown helper semantics, side effects and error paths remain open.

Preservation/check results and exact hashes are in SOR-EV-0005. Stage A had no game execution. Stage B's actual interventions follow below. No observer semver/package/DLL hash exists; these values are not fabricated as 0.1.0. Historical review labels remain unchanged.

Ghidra preservation check: all15 existing project files retain size/hash, but four project index files under idata/versioned have changed mtimes. Byte preservation passed; full filesystem metadata preservation did not. This project-container side effect of headless access is disclosed, not silently equated with no writes. No symbol/type/comment or analysis-content change was observed.

## Stage B attempts, deviation and recovery

User reported ready at New Save; PID20804 started at 2026-10-07T10:22:20.9645253+11:00. Preflights preserve OS thread creation inventories; they identify existing threads, not save-path roles. No SOR_HIT record exists in any attempt. The user was never told to confirm a save after observing a usable armed state and later explicitly confirmed no manual save was created.

| Run/tool | Actual evidence and result | Target/cleanup outcome |
|---|---|---|
| manual-001 / v1 | Restricted context could not open process; reported PID5144 is hexadecimal20804, not a PID parsing error. No attach, no sites validated/inserted, no save evidence | OS showed detached and alive. Outside-restriction read-only handle test succeeded; next attempt used the authorized elevated tool context |
| manual-002 / v2 | Attached; loaded SFSE/base and all four code windows matched; four intended sites inserted. Default Events/TlsCallbacks=1 also inserted four TLS breakpoints in libxess.dll, steamclient64.dll and tier0_s64.dll. Two libxess callbacks caused pauses; ten-second armed bound expired without save hits | **Acquisition deviation:** unrelated default breakpoints exceeded the intended four-site configuration. Disclosed immediately; no save instructed. Detached, four intended32-byte windows restored. Separate bounded readback of all four TLS locations matched32 disk bytes each; OS confirmed detached/alive. No crash |
| manual-003 / v3 | Fresh isolated settings disabled automatic TLS/DLL/thread sites. Corrected transport passed synthetic two-thread run transport-tls-disabled. Attach log reached game/modules but no paused context within five-second setup bound; no save sites inserted, no arming | Detached/alive, no automatic TLS breakpoint rows. Cause of missing pause remains UNKNOWN; no retry with extended bounds or arbitrary thread manipulation |

Manual-002's arming handoff waits at most60 seconds for an agent-created arm.signal while paused; actual signal arrived within that bound. The normal armed bound remains10 seconds. Later v3 also rejects unexpected automatic-breakpoint log rows before inserting research sites. These corrections did not establish a successful live capture. Standard debugger detach removes its registered breakpoints; the TLS readback independently checked the observed extra locations. No game binary/configuration, gameplay registers or save content was patched, no exceptions suppressed, and no process was force-terminated.

Raw v1/v3 result.json says site_bytes_restored=true despite no validated sites: that was a vacuous empty-set check, **not evidence of byte restoration**. Interpret as NOT_APPLICABLE for those attempts. Raw records are preserved. Post-run v4 reports null when no original windows exist and adds explicit validated/attempted counts; it has not been run against the game. The v2 positive restoration result is supported by four actual readbacks, plus the separate TLS verification. Capture results marked UNASSESSED are acquisition records, not scientific success.

The user canceled without saving, exited normally and confirmed sync finished. Subsequent process check found no Starfield/headless process. Protected parent/backup remain hash/size/mtime-identical to the durable baseline and byte-equal. One changed incidental exit save was copied after exit to ignored `.local-work/savegames/exp0002a/exit-001/`, verified source/copy/source metadata and byte equality: size2,083,584, SHA-256 `f3151898f7dcfb430457bcfea7916d49c2b98d5e28937eac03bdecf6b79fe387`. Live copy retained; no deletion or load-list cleanup. This is not a manual/prototype save or a successful checkpoint, and receives no qualification-sample promotion. Exact private name and archival receipt remain local in post-exit.json.

## Completion, names and bookkeeping

The serializer's finished-saving diagnostic at `141814ee6` is followed by further storage activity (including `141814f74`), so the text alone cannot mark completion. The higher finalizer's clear/wake plus close/rename path is a stronger candidate, still requiring live correlation with the exact generated file and status/error path. Request return, file appearance, stable size, engine completion, OS durability and cloud synchronization are distinct observations. None is equated here.

Optional-name handling and generated prefixes are static leads only. Safe caller-supplied names, collision policy and deterministic naming remain UNKNOWN. Save UI list/cache and backup/final rename operations exist; directory-only load-list behavior is not established. Steam/cloud behavior and safe external deletion after exit remain UNKNOWN. No automatic archive/delete implementation is added. Future checkpoint archive is copy-first after completion/normal exit/sync review, verify size/hash/bytes, retain incidental exit save separately, and remove a live copy only with the brief's cleanup authority and demonstrated safety. The incidental exit artifact above does not answer manual-save completion questions.

## Remaining gate and review package

Stage B stopped after setup failures; no credible live contract was recovered. This meets the brief's stop boundary for ambiguous native invocation, not its scientific success criteria. Diagnose and review the attach/pause setup offline before proposing another bounded attempt; do not silently enlarge time/trace scope. Do not build a callable serializer prototype to fill that gap. The next observer, if qualified, must begin 0.1.0 with one version source, documented integer encoding and all brief section27 tests; none of those prospective tests is claimed as passed here.

Before resuming EXP0002: establish live request contract and completion correlation; demonstrate a bounded dispatcher on the evidenced context; qualify selected-reference queries separately; review any additional code rights before incorporation; preserve Save3 and defer construction until tooling review. SOR-EXP-0002A's overall success criteria are not yet met.

Changes: bounded save-string Ghidra scan; original PE-window helper; original debugger transport/fixture/capture preparation; this report/operator card/evidence index; source/credit, provenance, authority and static function/state/finding updates. No modification of historical observer or SFSE header. No additional third-party code incorporated, upstream contact, fork/PR, staging, commit, push or publication. No unresolved incorporation permission request is needed for Stage A/B; Stage C may introduce a separate boundary.

The evidence index links the complete local review diff (including untracked additions), status and checks. Suggested commit after review: `docs(research): map native save execution path`. Do not use a qualification-success message for this preparation result.

## Subsequent offline dump evidence — SOR-EV-0007

[Comparison report](../audits/exp0002a-crash-dump-comparison.md),2026-10-07: both failed0.1.2/0.1.3 DR0 runs reached REQUEST_ENTRY and produced matching STATUS_SINGLE_STEP crash signatures. S2 fault TID equals its selected owner. This supersedes any inference that missing ordinary capture meant the entry was not reached, while preserving both INCOMPLETE_PRE_CAPTURE_TARGET_EXIT classifications and every prior run record. Stage-A mapping remains useful; complete manager/argument/naming/completion contract remains unqualified. Recommended S1.5 is not authorized by this offline analysis. No live action or Stage C.

## Final-attempt boundary — SOR-D-0021

Native save invocation is optional infrastructure. [One final one-shot software breakpoint](../implementation-briefs/EXP0002A-final-software-attempt.md) at REQUEST_ENTRY is now the only authorized next save-path attempt. No DR0/DR7, S1.5, expanded thread selection, multisite tracing or backend retry. Prior evidence/F0008 remain unchanged. Complete durable request evidence yields MATERIAL_SUCCESS_PENDING_REVIEW even if cleanup crashes; otherwise DEFERRED_NO_MATERIAL_ADVANCE closes this phase's detour and the next active task is [manual beacon checkpoints](EXP0002-manual-beacon-resumption.md). Neither outcome automatically authorizes Stage C. The central outpost project is not blocked on this experiment.


Final outcome: **DEFERRED_NO_MATERIAL_ADVANCE**; [SOR-EV-0008 / final audit](../audits/exp0002a-final-software-attempt.md). One software site, zero request captures; delayed operator save after cleanup, normal exit/sync, preserved evidence. No more native-save debugger attempts in this EXP-0002A phase. Next active project task is resumed manual beacon research.
