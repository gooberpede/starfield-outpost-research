# EXP0002 original observer and bounded diagnostic

**Settled-checkpoint correction prepared offline; review required before deployment or a fresh run.** The first primary attempt and its load-notification defect are preserved in the [run record](../../docs/experiments/EXP0002-gate-b-run.md). This revision uses explicit operator confirmation plus fresh live-state checks. Optional SFSE load messages are telemetry only. [STATIC-CONTRACT.md](STATIC-CONTRACT.md) separates static operands from unqualified live safety assumptions.

## Files and effects

| File | Reads / dependencies | Writes / target effect |
|---|---|---|
| build.py | Hash-pinned local Starfield PE, own source, installed MSVC/SDK and CPython, approved MIT SFSE header | New ignored build directory; generated site hashes, DLL, debugger EXE, synthetic tests, logs, installable ZIP and manifests. No download, game run or installation. |
| core.h / format.h / win_support.h | Original byte-view selection, JSON serialization, Windows hashing/read/file APIs | Used by observer/tests; bounded RPM views, CREATE_NEW/WriteFile/FlushFileBuffers, no source-save access. |
| observer.cpp | Current-process build/code guards, selected parent/persistent-cell references, three callback queries, explicit request files | SFSE task + control-file worker; new ignored session, fixed records. Additional engine calls affect timing/caches; no hooks or byte patches installed by this observer. SFSE itself is runtime instrumentation. |
| request.ps1 | Existing ready/previous checkpoint files and process identity; requires GateBApproved | One atomically published request, optionally separate TRACE permit; never launches/deploys/attaches. Switches document prior human authority; they do not grant it. |
| request_time.ps1 / test_request_time.ps1 | Pure UTC conversion for string/JSON DateTime inputs; two culture fixtures | Thirteen offline checks; no request, file or process access. Avoids locale-dependent stale-session false rejection. |
| acquisition.h / acquisition_tests.h | Fresh per-task player/global, cell/world, collection and candidate views; synthetic changed-address and mutation fixtures | No shared selected-pointer cache; repeated checks gate acquisition/queries. Optional notification counters cannot grant or deny capture. |
| test_request_gate.ps1 | Original request helper negative authority/settled/reload guards | Three offline early-rejection checks; no live request or session access. |
| test_package.py | Production ZIP verifier with synthetic ZIPs | Four temporary-file tests for exact config LF/path and DLL identity; no deployment. |
| trace.cpp / trace_state.h | Future existing Starfield process, selected A2R identity/thread, loaded byte guards | Windows debugger attachment, main-thread DR0/DR1/DR2, RF resume flag, suspend/resume for cleanup; flushed bounded JSONL. No live attach in this preparation. |
| trace.py | Completed A2R and build manifest | Runs future separately approved diagnostic, issues TRACE only after ARMED, local console log; does not kill a stalled debugger/target. |
| validate.py | One native checkpoint, anomaly or trace file | Read-only structural/correlation result; does not certify engine semantics. |
| initialization.h / initialization_tests.h | Original startup ordering, atomic marker publication; injected services and private synthetic Windows thread | Only the initialized worker publishes READY after listener registration; tests write private fixtures, no SFSE/game execution. |
| observation_policy.h / observation_tests.h | Original failure classification, copied-candidate serializer, C:/D: available-space reads, synthetic policy/continuation tests | Persist bounded scientific anomalies without terminal stop; fail closed for safety/integrity or persistence failures. |
| tests.cpp / test_output.py | Synthetic memory and serializer output; load own DLL in test process | New local fixtures only; no Starfield process access. |

## Offline reproduction

From repository root, choose a **new** build name:

```powershell
& 'C:/Users/User/AppData/Local/Python/pythoncore-3.14-64/python.exe' runtime/exp0002/build.py --game 'D:/ReverseEngineering/Starfield/Starfield.exe' --vcvars 'C:/Program Files/Microsoft Visual Studio/18/Community/VC/Auxiliary/Build/vcvars64.bat' --name review-next
```

No directory is reused. Output goes under `.local-work/exp0002-builds/<name>/`. Build logs record compiler passes; build.json records source, executable, guard, DLL/debugger/ZIP hashes. Generated guards contain hashes, not copied instructions. `SorExp0002-local-test.zip` contains Data/SFSE/Plugins/SorExp0002.dll and config plus notices, never SFSE runtime or game content. The package is an installable local test artifact, not publication-cleared. The source tree plus exact manifest is required for review; no public binary distribution is authorized.

## Output contract and limits

Native schema `SOR-EXP-0002-native-v1` is separate from the earlier Python design schema; do not feed it to capture_contract.py. A checkpoint includes runtime provenance, UTC and declared local timezone, optional pre/post load-notification counters (explicitly telemetry_only), synchronization/settled attestations, thread, elapsed time, non-atomic snapshot flag, selected scope count, player/context and role records. Each role has pointer, FormID, stored base, candidate identifier distinct from resolved handle, extra-data pointer, stored parent cell, reference XYZ/raw rotation, unavailable coordinate domains and separately named GetWorkshop/GetCurrentLocation/GetWorldSpace results. Null query, failed read and unavailable field are distinct.

Six sequential requests only, A0/A0C/A1/A1C/A2/A2R. A0/A0C require no selected candidates; A1/A1C one beacon; A2/A2R beacon then storage. Scan cap 8192 total entries. No pointer is retained across checkpoints. A query-begin record flushes before each native call; return flushes afterwards. `CHECKPOINT_COMPLETE` follows successful capture. A scientific anomaly instead produces `<checkpoint>-anomaly.json` with `ANOMALY_RECORDED`; the request is consumed and the observer remains available for the next explicit checkpoint. No retry of the consumed checkpoint, automatic construction action or fabricated success. After A2R, complete.json says `CHECKPOINT_SEQUENCE_COMPLETE` only if all six succeeded, otherwise `CHECKPOINT_SEQUENCE_RECORDED_WITH_ANOMALIES`. The optional TRACE remains gated on six successful checkpoints. It too can record one anomaly without setting global stopped; after the finite request budget the worker idles until session expiry. Partial/missing terminal files are incomplete. The write-through/flush APIs are tested, not power-loss/crash-survival guarantees.

Initialization registers the SFSE message listener before creating the worker. The worker publishes READY on entry, before polling requests: write/flush/close ready.pending, then rename without replacement to ready.json. A failed write/flush/rename cannot expose a partial READY marker. Once a session directory exists, snapshot/profile/listener/thread/publication failures and C++ exceptions attempt failure.json; unavailable storage or allocation can prevent even that report. A successfully registered callback requires keeping the DLL resident on subsequent failure (SFSE load returns true); READY remains absent and stopped is set. Load success alone is therefore not readiness. No loader-thread wait for worker startup is introduced.

Output remains bounded: six primary requests and at most one separately approved TRACE. Each has at most one 32 KiB anomaly artifact, with at most 16 copied candidate identities plus bounded context. Scanning stops when a seventeenth matching candidate is seen; observed counts are then explicitly incomplete/lower bounds and candidate truncation is flagged. Ordinary scans remain capped at two cells / 4096 entries each. A conservative upper bound is 64 files at 32 KiB including all JSON records, emergency trace disk failure and ready.pending (2 MiB), plus fixed tiny controls and the separately bounded trace JSONL. Existing begin/return evidence is retained if an anomaly occurs after a query.

The worker checks control files and available C:/D: space every 250 ms for at most 45 minutes; it never polls world state. Space is checked at initialization, before tasks/queries and evidence writes; the debugger checks before attachment and each event-loop iteration, and request.ps1 checks before request creation. **Each drive must have at least 40,000,000,000 available bytes (40 decimal GB).** A below-threshold result or unavailable space reading is terminal. A small best-effort failure record bypasses the low-space guard; no further acquisition is allowed. Checks cannot cancel an already running engine call or filesystem operation. Zero automatic retry/recovery. Loaded module profile remains startup-only and is not a resolved ESM load order.

## Synchronization: operator confirmation and fresh state

For each request the researcher first obtains a fresh operator statement: intended scene, normal controllable gameplay, menus closed, stationary for five real seconds, no loading/combat/dialogue. Keep that state until the result; a delayed request or intervening change invalidates the procedural assumption and must be reported. `-OperatorSettled` records that confirmation, not a substitute for obtaining it. A2R also requires `-ReloadedAndSettled` after ordinary UI reload of the exact A2 save. No event receipt, counter threshold or loading latch is an acquisition gate.

The request protocol is now `<checkpoint>\nSETTLED\n`, except A2R requires `A2R\nRELOADED_SETTLED\n`. The worker accepts at most 64 bytes and rejects legacy/unconfirmed requests. It queues a new task containing only the checkpoint index. All player, context, candidate and query-result state is local to that task; no A2 pointer/handle becomes an A2R input. Completed JSON is immutable comparison evidence, never read back by the primary observer for dereferencing. For A2R, reacquire the global player, its identity/transform/stored cell, cell flags/worldspace, persistent-cell candidate and bounded collections/candidates from scratch.

Fresh successful views must agree after selection, before each query (again after begin-record flush), after returned-query evidence, and before successful checkpoint publication. Checks re-read the player global, player identity/transform, cell flags/world/persistent-cell relation, collection headers and selected identities. Changed readable views become bounded anomalies; unsafe reads remain terminal. Zero notifications is valid; pre/post counters are optional descriptive telemetry and are never passed into the acquisition/consistency functions. Listener registration remains part of READY initialization, without waiting for delivery.

These are non-atomic checks, not engine locks or retained ownership. An unobserved transition that restores identical checked bytes, or a mutation between the last check and native call, can escape detection. Operator confirmation does not prove quiescence; successful checks do not prove lifetime/ABI safety. Existing 1 s selection/2 s cooperative capture and 45-minute session bounds, strict integrity/disk stops and anomaly/no-retry rules remain. The new build is not live-qualified.

## Observation anomalies versus instrument failure

Scientific anomalies abort the current acquisition, persist copies already obtained safely, and leave stopped false after successful persistence. They consume that checkpoint, not the whole session. To continue, the operator reviews the anomaly and supplies `-AcknowledgePriorAnomalies` to request.ps1 for the **next** explicit checkpoint. That acknowledgment does not grant extra live scope, authorize repairing the scene, or turn an anomaly into a successful sample. Current failure.json always overrides earlier availability markers.

| Condition | Disposition and rationale |
|---|---|
| Candidate-count disagreement / ambiguity | Anomaly with expected/observed role counts, count completeness, scan/truncation flags and copied candidates; no guessed target or selected-reference query. |
| collection_changed | Anomaly only when both header reads succeeded but differ. Stop using the view; a fresh later checkpoint can reacquire. Failure to read the header remains terminal. |
| unstable_identity | Anomaly when successful bounded identity reads disagree (including changed stored base). Retain first/rechecked views; no call with the unstable selection. Actual read/structural validation failure remains terminal. |
| player_context_changed / cell_context_changed | Successfully re-read player or cell/world context differs: bounded anomaly; no remaining queries. Re-read global player first. Missing, extra or unpaired load notifications cannot gate capture. Historical load-state anomaly names remain accepted for old evidence only. |
| Selection >1 s / acquisition >2 s after a query | Anomaly; abandon further reads/calls and retain completed invocation records. Check selection budget inside the entry loop and acquisition budget after each returned query. Cooperative limits cannot interrupt an engine call in flight. |
| Collection scope >4096 entries / candidate evidence >16 | Bounded anomaly, no wider scan or chosen target. Positive count with null array is instead a structural failure. |
| Nonfinite transform / null or exterior context unavailable | Anomaly when safely read; preserve nonfinite values as explicit strings, never invalid JSON numbers or a guessed conversion. |
| Wrong build/site, unsupported structural layout or failed pointer/array/form read | Terminal instrument/safety failure; no further acquisition. Unknown reason codes fail closed. |
| Failed evidence write/flush/publication, invalid request/diagnostic permission, allocation/C++ failure, low/unknown C:/D: space | Terminal; best-effort failure.json, no hidden retry. A failed anomaly write is an instrument failure, not a recorded scientific outcome. |

Anomaly schema `SOR-EXP-0002-anomaly-v1` contains checkpoint/reason/time, expected and observed counts, scope/completeness flags, at most 16 candidate copies (pointer/FormID/stored base/cell/extras/type/raw transform/candidate handle), optional rechecked/context copies, query count, elapsed time and runtime provenance. It performs no additional game dereference to serialize the evidence. Counts from an aborted scan are partial, never an exhaustive membership claim. `instrument_available:true` describes successful handling at that time, not a promise against a later safety stop. Neither kind of outcome changes research confidence automatically.

## Diagnostic intervention and bounds

Default: primary checkpoints only; diagnostic separately approved after A2R. It uses the A2R main thread and selected storage, resolves ASLR from the module snapshot, rehashes game and 18 loaded code windows, refuses occupied main-thread hardware breakpoints, and restricts selected return provenance to the observer DLL. DR0 callback, DR1 tail and dynamic DR2 return are execution breakpoints. Return requires same thread, entry stack then RSP+8. RF and DR6 resume-control changes are explicit; original debug registers are restored on cleanup. No software breakpoint is inserted by this tool; Windows debugger attachment itself delivers an initial breakpoint. Only that verified DbgBreakPoint and owned hardware traps are consumed; unexpected exceptions are forwarded and stop acquisition.

One selected operation OR 100 callback hits OR 5 seconds armed, whichever first; 5 s setup bound; 1000 debug-event cap; <=300 records, <=4096 bytes/record, <=1,250,000 output bytes; zero retries. WaitForDebugEventEx polls at 50 ms, so zero-hit timeout does not depend on breakpoint arrival. OS scheduling, file flush and cleanup latency can overshoot nominal wall time. This is not a hard real-time guarantee. No gameplay register edits, stepping, exception suppression or forced game termination. DebugSetProcessKillOnExit(FALSE) is requested immediately after attach; attach/setup itself is an intervention and failure risk.

Cleanup prefers restoring debug registers while an event already pauses execution; on timeout it suspends only the selected thread for restoration, resumes and detaches. Failure is logged, never treated as success or silently retried. If both setting no-kill policy and early detach fail, acquisition ends and the debugger stays alive for explicit operator recovery: exiting it under Windows' default policy could kill the target. This exceptional recovery hold is not bounded acquisition or successful completion. Other restoration/detach failures likewise require operator recovery. Target can exit/crash independently. Completeness, scientific result (initially UNASSESSED) and target outcome remain separate. Neither synthetic tests nor a compile qualify actual Windows attach/context/cleanup behavior against Starfield.

## Future commands (NOT Gate A)

Researcher supplies the current session path; user never transcribes pointers or registers:

Use the existing PowerShell 7 environment (`pwsh`, checked here at 7.6.5). Windows PowerShell 5.1 currently refuses scripts under its existing policy. No execution policy is changed or bypass switch supplied; trace.py explicitly resolves pwsh and stops if unavailable.

```powershell
./runtime/exp0002/request.ps1 -Session '<current session directory>' -Checkpoint A0 -GateBApproved -OperatorSettled
& 'C:/Users/User/AppData/Local/Python/pythoncore-3.14-64/python.exe' runtime/exp0002/validate.py '<current session directory>/A0.json'
```

Repeat the exact checkpoint from the run card, once each. Separately approved optional diagnostic:

```powershell
& 'C:/Users/User/AppData/Local/Python/pythoncore-3.14-64/python.exe' runtime/exp0002/trace.py --session '<current session directory>' --build '<reviewed build directory>' --gate-b-approved --separate-diagnostic-approved --operator-settled
```

No auto-retry, auto-relaunch, deployment, save-copy or cleanup deletion is supplied. Configuration changes and installing/removing the reviewed observer are future explicit Gate B actions; they are not performed by building.

## Reviewed Gate B deployment owner

**Vortex is the explicit and exclusive deployment owner.** After separate Gate B approval, the user manually installs the exact reviewed ZIP through Vortex, enables/deploys it there, and later disables/retires it and deploys the resulting change through Vortex after the game has exited. Codex/research helpers must not copy DLL/config files directly into the game, remove deployed files by hand, create unmanaged overrides or use a parallel deployment path. Vortex staging/deployment links are expected, not an instruction to replace them.

Record the reviewed ZIP hash, Vortex mod/profile identity and resulting DLL/config paths and hashes. Confirm exactly one observer and the intended Data/SFSE/Plugins layout without changing other mods. A conflict, duplicate or hash mismatch requires review through the user-managed Vortex workflow. Preserve notices and local research evidence when retiring the mod. No deployment/profile changes or Vortex operation occurred in Gate A. See the [operator card](../../docs/experiments/EXP0002-operator-card.md).
