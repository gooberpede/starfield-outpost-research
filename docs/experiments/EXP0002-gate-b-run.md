# EXP0002 primary Gate B run record

2026-10-06, Australia/Sydney. Authority: SOR-D-0012, user approval in this conversation. Scope: primary A0/A0C/A1/A1C/A2/A2R only, governed by the [operator card](EXP0002-operator-card.md). No optional debugger diagnostic. This records a real but incomplete first attempt and its instrumentation anomaly, not an outpost finding.

## Current status

**Attempt ended; primary sequence incomplete.** A0 persisted a valid load-state anomaly with zero scanned entries/queries. The user exited normally, Steam sync completed, and Starfield process absence was verified. No manual checkpoint save, beacon/storage placement or debugger attachment occurred. The user reports the observer disabled through Vortex; post-exit evidence and integrity results are below. Do not restart this sequence with the same load-notification assumption.

The user confirmed corrected-package deployment through Vortex profile **Starfield - SFSE**, with SFSE the only other enabled mod. Deployed DLL/config hashes matched the table below. Starfield was not running at initial process inspection; only Vortex's folder marker was present before user deployment. A researcher launch attempt through the pinned SFSE loader at 2026-10-06 17:04:19 Australia/Sydney created loader PID 21640, which then exited without a visible game window, Starfield process, observer session or READY record. The user reported no window/error and explicitly chose to launch through Vortex instead. That user-operated launch produced Starfield PID 11240 at 17:04:52, session `session-11240-65632296`, and READY at `2026-10-06T06:04:53.667Z`, matching the reviewed observer hash. Startup module snapshot contains 61 entries, not truncated; no failure marker was present at readiness inspection. Subsequent A0 and exit outcomes are recorded below. No automatic retry, forced termination or debugger attachment occurred.

## Configuration defect found before launch

The reviewed review 12 ZIP contained a 65-byte config ending CRLF. The observer reads binary bytes and removes one trailing LF; the remaining CR fails its exact output-root validation. Thus the earlier package would not initialize. Offline native tests had not covered the actual packaged configuration bytes. This is a packaging failure, not scientific evidence or a runtime anomaly.

The new local `SorExp0002-review12-config-lf.zip` removes exactly that CR byte (64-byte config), leaving the intended path unchanged. Every other member, including DLL and notices, is byte-identical to review 12. The original ZIP is preserved. build.py now writes explicit LF and checks actual ZIP config/DLL bytes. Four new offline ZIP regression tests pass: correct LF accepted, CRLF rejected, wrong path rejected, changed DLL rejected. No native code was changed or rebuilt; the prior 125 native and 26 output results remain results for the unchanged reviewed DLL, not newly executed live checks.

| Artifact | SHA-256 |
|---|---|
| Corrected ZIP | `565c0caf6a4708080c695fae788e8e76276772db52f18de2683d8c89cdca888f` |
| Unchanged reviewed DLL | `ca167cb5e47ea90739729ee686ce1691766461238847d6a778f98530bf6ce94e` |
| Corrected config | `e6ada6592dc673d12b920864f7c944b38251fbe9a20e221b9ef551a9c4411185` |
| Superseded ZIP | `84bc87c0f7ba8f58c843f70d170bb6d31ea1e72a47a339c0e47e57f0b41a9ae1` |

Local-only receipt: `.local-work/exp0002-gate-b/config-lf-package.json` preserves the pending state at creation. The user's subsequent deployment confirmation accepts the correction; independent deployed-file hashes match. No manual game-file deployment or configuration edits were performed by Codex.

## Preflight records and limits

Ignored `.local-work/exp0002-gate-b/*-preflight.json` records actual hashes and metadata for protected SOR-SAMPLE-0001 original/backup, game/SFSE, original and corrected packages, source coherence with the explicitly recorded packaging changes, C:/D: space, native-file inventory, configuration snapshots and save-directory metadata. It reads no save contents except hashing the two protected parent copies. Scripts in that local directory document their inputs/outputs; they do not deploy, execute the game, attach or issue requests. The first preflight caught the CRLF defect before producing a completed manifest; the subsequent corrected-package check is retained separately.

Plugin list/configuration files are pre-launch observations, not resolved runtime order or winning-definition proof. Vortex profile identity was user-reported; deployed hashes and READY were independently checked. Parent selection/scene state remain operator-reported and winning-definition resolution remains unestablished. No outpost or persisted-membership finding is promoted by passing hashes or tests. Runtime evidence and save copies remain local-only.

## Operator handoff

The agreed handoff reserved Vortex deployment and ordinary game UI to the user, with helpers operated by the researcher. Deployed files were checked before launch; the parent was selected through ordinary UI and five-second settling was confirmed before the single actual A0 request. No construction or manual saves followed the anomaly. The parent was not overwritten. No forced retry/relaunch or debugger escalation occurred.

## Pre-request timestamp correction

The user confirmed A0 ready after loading the intended parent. The first request-helper invocation rejected the session as stale before any request file was written. PowerShell 7.6.5 ConvertFrom-Json returned a UTC DateTime; passing that object through DateTime.Parse caused locale-dependent conversion, turning 6 October into 10 June and losing fractional seconds. Actual process start was `2026-10-06T06:04:52.8130154Z`, before READY `2026-10-06T06:04:53.667Z`. There was no observer failure or acquired A0 record.

The pure request_time.ps1 helper now preserves DateTime UTC directly and parses string inputs using invariant culture with round-trip semantics. Thirteen offline checks pass under en-AU/en-US for string and JSON-decoded inputs, correct live-session ordering, reused-PID rejection and invalid timestamp rejection. No deployed/native file, request syntax, checkpoint scope or capture budget changed. The user was informed and asked to repeat the five-second settling confirmation before the first actual request; no automatic checkpoint retry occurred.

## A0 acquisition outcome and integration diagnosis

After a second user confirmation of settled A0 state, request-A0.txt was created once. At `2026-10-06T06:08:35.812Z`, A0-anomaly.json recorded loading_before_task, load_generation 0, scanned_entries 0, queries_invoked 0, counts_complete false and instrument_available true. validate.py accepted its anomaly schema. No A0 success file, query record or failure.json was present. Starfield was still responding. The zero counts are unobserved/incomplete, not proof that the scene lacked candidates. No A0C or later request was issued. The observer did not silently terminate on the anomaly.

The observer initializes loading=true and clears it only on SFSE PostLoadGame. Read-only inspection of pinned SFSE [Hooks_Serialization.cpp](https://github.com/ianpatt/sfse/blob/48535cc4306ab345252bf740c20a1c6194929b0e/sfse/Hooks_Serialization.cpp#L79-L99) shows the hook installation that would generate those save/load messages disabled by a compile-time guard. SOR-S-0118 credits this source. The live SFSE log records successful listener registration and messages 0/1; absence from a possibly buffered log alone is not proof of no later messages. The observer's own generation-zero record independently shows neither relevant notification was counted before A0. Source/runtime behavior is consistent with unavailable notifications, but installed-binary hook equivalence was not reverse-engineered here.

This exposes an instrumentation assumption failure, not an outpost membership/coordinate result. READY correctly proves listener/worker initialization, not useful delivery of every declared event. The sequence was paused for review instead of burning remaining slots or bypassing the load guard. A0 has been consumed and must remain recorded as anomalous. A scientifically complete A0–A2R run needs a corrected, reviewed load-state strategy and a separately surfaced fresh-session plan; no reset, reload, hook, debugger, or automatic retry was introduced. User was asked to exit normally without manual saves/building, preserving any incidental exit save.

## Exit, preservation and outcome

The user reported responsive, stationary first-person gameplay without menus at readiness; they could not confirm the exact capture-time screen state. Record both statements, rather than asserting direct visual observation by Codex. The user then reported normal exit and completed Steam sync; process absence was independently checked. No crash or forced termination was observed.

Post-exit inventory: one new incidental exit save, zero changed existing save filenames, one missing older exit-save filename. This is consistent with the game replacing its exit-save slot, not proof from semantic parsing. The older exit save was not archived during preflight (metadata only); its bytes cannot be recovered from this evidence. Codex did not delete/rename any save. Both protected parent and backup retain their original size, SHA-256 and mtime.

The new incidental save is 2,077,984 bytes, SHA-256 `fe3d299110bbf588676fc570b01b27ea2df7a08a079ef525579e16207ba91b4d`. It was copied only after known exit to a fresh ignored path, with source/copy/source hash equality and stable source metadata. It is not A0 or a primary sample. Seven exact-byte copies preserve that save, four observer/control files, and two SFSE logs. The final SFSE log also contains game-data messages 2/3; these are not save-load messages 6/7 and do not qualify reload tracking. No global failure marker appeared before exit.

The user disabled the observer through Vortex after exit; independent inspection found no SorExp0002 DLL/config remaining in the deployed plugins directory. SFSE was left in place. No researcher deployment/deletion occurred.

Evidence completeness: **A0 anomaly complete; A0–A2R sequence incomplete**. Scientific result: **no membership/coordinate acquisition, no persistence claim**. Instrument outcome: **listener/worker and anomaly persistence exercised; load-state integration unqualified**. Target outcome: **user normal exit**. Evidence index: [SOR-EV-0003](evidence/exp0002-first-live/README.md). Optional diagnostic was never authorized or attached. No changes were staged, committed or pushed.


## Accepted offline synchronization correction — 2026-10-06

After this failed attempt the user explicitly requested removal of mandatory PreLoadGame/PostLoadGame gating, operator-confirmed settled checkpoints plus fresh consistency checks, completely fresh A2R acquisition, offline coverage and a new ZIP for review. They prohibit deployment, rerun, debugger attachment or commit until correction review. This supersedes the old notification assumption for the new build only; the first-run bytes and negative outcome above remain unchanged.

The new observer starts with no loading latch. Its listener merely counts optional pre/post messages; those counters do not enter any acquisition decision. Each request carries SETTLED, or RELOADED_SETTLED for A2R, after explicit operator confirmation. The request helper requires -OperatorSettled and additionally -ReloadedAndSettled for A2R. Legacy requests are rejected before queuing a task. The new task retains only its checkpoint index; all game identities/context are local to that invocation. A2R re-reads player/global, cell/world/persistent-cell relationship, bounded collections and identities. It never consumes A2 JSON or retained A2 pointers as acquisition inputs.

Repeated successful context/identity views must agree after selection, before each native query (including after the begin-record flush), after query-return evidence and before checkpoint publication. Player/cell/collection/reference inconsistency produces a bounded anomaly with safely copied candidates. Unsafe structural reads, invalid requests, failed persistence, wrong build/site and low/unknown C:/D: space remain terminal. No query is allowed on ambiguous selection. Existing six slots, 16-candidate/32 KiB anomaly caps, 1 s selection/2 s cooperative task checks and 45-minute session lifetime remain. A2R and successful completion are never inferred from notification counts.

Operator confirmation is a recorded precondition, not engine synchronization. Non-atomic repeated reads cannot prove engine ownership or detect a transition that restores identical checked bytes, and cannot prevent every change between check and use. A running callback cannot be safely cancelled. This remains an offline-tested revision awaiting review and live qualification. The operator card and runtime README now state this model and its limitations explicitly. Vortex remains exclusively user-managed; no new deployment, launch, save access or diagnostic was performed during this correction.

Fresh build identity, checks, complete diff and hashes are recorded in the [synchronization review](../audits/README.md#archive-lookup) (`audits.zip :: docs/audits/exp0002-settled-correction.md`). The earlier Gate B approval is not treated as authorization to run this changed build before the requested review.
