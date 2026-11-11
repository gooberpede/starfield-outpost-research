# Save25 observer operator run card — proposed for review

**Approved for initial live session, 2026-10-10:** User explicitly approves the preflight and this card and authorizes the initial live session. The review prerequisite below is satisfied for this bounded run. Operator retains launch/gameplay/save/reload/exit control. No observer implementation change is authorized by this approval. See [live ledger](initial-live-session.md).

2026-10-10. SOR-EXP-0016 / SOR-EV-0023 / SOR-D-0034. **Do not launch until this card has been reviewed.** [Actual deployment preflight and limitations](../../audits/README.md#archive-lookup) (`audits.zip :: docs/audits/beacon-observer-post-deployment-preflight.md`). Observer 0.1.0 is approved; no replacement or configuration edit is proposed.

## Purpose, allowed actions and boundaries

Compare ordinary beacon transforms, frame inputs and workshop candidate bytes before/after moving SOR-003, manual saving and reloading. Observe whether the visible outpost boundary remains at its earlier location. Save25 starts at SOR-003. SOR-002 is a useful control when available; visiting it by fast travel or several minutes on foot is acceptable. Travel cost alone is not grounds to discard a promising comparison. No exact planetary coordinate, boundary ownership or persistence semantics are assumed.

Allowed after review: operator starts via SFSE, loads the exact protected Save25, observes landmarks/boundary, moves the existing SOR-003 beacon through normal game UI, creates a **new manual save**, reloads that new save, optionally travels to SOR-002, and exits normally. Codex requests settled captures and cooperative STOP, reads/verifies evidence and archives the new save locally. No console commands, additional building/deletion, native queries, hooks, breakpoints, memory/register changes or automated saving. Vortex remains deployment owner. Worker reads are non-atomic and can affect CPU/I/O and execution; guarded copying does not prove object lifetime safety. Crash risk remains; source Save25 must never be overwritten.

## Preparation and startup

1. Codex rechecks the deployed hashes/config against the preflight report, game absence and both C:/D: caller-available capacities at or above **40,000,000,000 bytes**. Record time and available bytes. If identity changed or a guard fails, resolve/review before launch. Keep the exact original/frozen Save25 intact. Avoid unrelated disk-heavy work.
2. Operator selects Vortex profile **Starfield - SFSE**, with SFSE 0.2.21 and approved observer enabled, then starts Starfield **through SFSE**. Do not use Continue or load a save yet; remain at the main menu.
3. The observer starts automatically during SFSE plugin loading, before Save25 loads. It validates pinned identities/code guards/path/space, creates `D:\Projects\starfield-outpost-research\.local-work\beacon-observer-live\session-<PID>-<tick>`, records startup modules and writes `ready.json`. Startup is not a beacon checkpoint. There is no automatic gameplay capture or fixed session timer.
4. Codex identifies the newly created session by current Starfield PID, process-creation identity and this launch time, then checks startup records/marker and `ready.json`: ready true, version 0.1.0, game 1.16.244.0, expected game/SFSE/observer DLL hashes and matching process. Check no failure/retirement marker. Never select an old session by folder name alone. If no fresh READY appears, remain at the menu while checking fresh SFSE logs and output access; do not proceed to Save25 or send science requests with unverified instrumentation. If readiness cannot be established, exit normally and return diagnostics for review; no rebuild/redeployment is implied.
5. Only after Codex confirms fresh readiness, operator uses Load to select the exact Save25 identified below, waits for loading to finish and stands still at SOR-003. Do not overwrite this save.

Protected filename: `Save25_D6036588M417474696C61204B6972616C79_000231_20261009102224_4_0_4.sfs`, under `C:\Users\User\Documents\My Games\Starfield\Saves`. Size/hash must match the report. Another Save25 filename exists; the numeric label alone is insufficient.

## Checkpoints and in-game actions

At every checkpoint the operator reports loading/travel/save complete, closes menus/build mode and stands still in settled gameplay. Codex sends **one** unique request. Operator waits without moving, saving, loading or travelling until Codex confirms acquisition finished, including final metrics. The ordinary game continues running. Do not queue future requests: directory enumeration is not stage ordering. A full synthetic scan took about 56 seconds; live duration may differ. Healthy growing/flushed output warrants continued waiting, not an arbitrary timeout.

| Order / request label | Operator action before requesting |
|---|---|
| 1 `baseline-003` | Loaded Save25; stand at SOR-003. Record player/beacon position relative to fixed landmarks and time-state. |
| 2 `control-003` | Remain at the same location with no deliberate change. This gives an ordinary no-action comparison. |
| 3 `premove-003` | Observe existing boundary in normal build UI and record fixed landmark relationships; confirm the beacon can be moved. Close UI and settle before capture. |
| 4 `moved-003` | Move **only SOR-003's existing beacon** a clearly observable distance using the normal UI. Record approximate direction/distance and landmarks; observe boundary again, close UI and settle. Do not save yet. |
| 5 `saved-003` | After moved capture finishes, use Pause → Save → **New Save/new slot**. Record the new save's displayed identity/time. Wait for saving to finish, return to settled gameplay, then capture. |
| 6 `reloaded-003` | After saved capture finishes, load that **new manual save**, not Save25. Wait for full load, observe beacon/boundary against the same landmarks, close UI and settle. Capture uses fresh roots; no pre-reload pointer is reused. |
| 7 `reload-control-003` | Remain in place with no deliberate change; capture the no-action reload control. |
| Optional `visit-002`, `control-002` | After core checkpoints, travel to SOR-002 by fast travel or on foot if its unloaded/missing data or frame comparison makes this useful. Record route/loading/time change, settle at arrival, capture and repeat without action. Do not move SOR-002 under this card. |

If a normal UI move is unavailable, preserve the baseline/control evidence and report the constraint for review of an alternative; do not improvise destructive actions. Missing SOR-002 in a SOR-003 capture does not fail the run. Codex should assess whether a visit answers the remaining question, without dismissing it for travel convenience. Record combat, weather/time changes, unexpected travel/rebase, unloaded state and deviations rather than hiding them. No extra action is required merely to make an unexpected reading look plausible.

## Exact control and evidence handling

Codex sets these PowerShell variables once, using the **verified actual fresh session path** in place of the placeholder:

```powershell
$observerPython = 'C:\Users\User\AppData\Local\Python\pythoncore-3.14-64\python.exe'
$observerRequest = 'D:\Projects\starfield-outpost-research\runtime\beacon-observer\request.py'
$observerSession = '<verified absolute fresh session path>'
& $observerPython -B $observerRequest $observerSession baseline-003 --settled
```

Repeat the last line with each table label only after its action/settling and prior capture completion. `--settled` is an operator assertion, not a detector. Helper writes a unique `<label>.request` containing `SETTLED <label>` plus LF using an exclusive pending file and rename. Worker polls approximately every 250 ms. Do not touch pending files, reuse labels or manually delete controls during the run. A rejected request gets a rejection record; correct the cause and use a new distinct label after settling. Helper refusal before submission is not itself a global experiment failure.

Each capture writes `<session>\<label>\records.jsonl`, raw chunks with lengths/checksums and `complete.json`; final metrics follow the completion marker. Codex checks marker, journal and final metrics/quiescence before authorizing the next gameplay action. Use the unchanged inspector on each finished snapshot, with a **new** local summary filename:

```powershell
& $observerPython -B 'D:\Projects\starfield-outpost-research\runtime\beacon-observer\inspect_capture.py' (Join-Path $observerSession 'baseline-003') --output 'D:\Projects\starfield-outpost-research\.local-work\beacon-observer-preflight\baseline-003-inspection.json'
```

Choose a new output name for every invocation/run; never overwrite prior summaries. Completion means persisted acquisition, not semantic completeness. `CAPTURE_PARTIAL`, `NOT_OBSERVED`, `UNREADABLE`, `UNSUPPORTED`, `UNEXPECTED` and `QUERY_FAILED`, missing optional fields and implausible values are recorded and inspected while continuing healthy independent acquisitions. They do **not** automatically stop this experiment.

## Genuine stop conditions, exit and cleanup

Stop acquisition for a concrete instrumentation-integrity or machine-safety failure: pinned identity/code guard mismatch, wrong process/session, corrupted/truncated evidence that cannot be distinguished from a recoverable partial tail, raw hash/length mismatch, failed output writer/flush, failed disk query or either volume below the guard, or unexpected corruption outside the declared controlled-save boundary. Classify the actual cause; an optional unreadable game object alone is not this class. If progress appears stalled, inspect worker/output/process/disk evidence first; elapsed time alone is not an integrity finding. Do not suppress exceptions or force termination.

After the final checkpoint and its metrics finish, Codex sends:

```powershell
& $observerPython -B $observerRequest $observerSession STOP
```

STOP cooperatively ends polling/acquisition; it does not exit Starfield or unload the DLL. When idle, wait for `retired.json`. If STOP is needed during a capture, the current snapshot can remain partial with `failure.json` reason `operator_stop_partial`; earlier flushed evidence remains valuable. A writer/low-space failure may prevent a final marker. Retain everything and record this distinction. Never wait for a marker indefinitely when the process has exited or the writer has failed.

Once retired (or a documented failure has stopped acquisition), operator exits Starfield normally through its UI. Codex verifies process absence; operator allows Steam sync to finish. After exit, disable the observer through Vortex for ordinary play; leave SFSE/profile management to the operator. Do not manually remove deployed files or rewrite configuration. Archive/hash the exact new manual save locally by filename/time correlation, rehash protected Save25 original/archive and retain session, logs, action notes and inspection summaries under ignored local storage. No raw save/memory/log upload, Git staging, commit or push. Report scientific result, capture completeness and target survival separately; await critical review before further experiments.
