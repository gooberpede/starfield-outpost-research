# Prospective Save25 position-write history run

2026-10-13, Australia/Sydney. SOR-EXP-0031 / SOR-EV-0039 continuation.
**READY FOR COMBINED REVIEW ONLY. DO NOT EXECUTE UNDER THE OFFLINE ASSIGNMENT.**
[Brief](../../implementation-briefs/CODEX_BRIEF_SOR_workshop_position_write_history_Z_oracle.md),
[qualified package/report](report.md), [independent review](review.md),
[schema and effects](../../../runtime/native-oracle-060/schema.md).

One combined maintainer approval covers the exact package, hook/safety contract
and sequence below. After that approval, successful preflight authorizes this
reviewed live run without another routine review or confirmation. A changed DLL,
hook, live action, safety contract or further experiment needs separate approval.
Only the maintainer deploys/removes through Vortex and operates gameplay.

## Exact package and startup contract

Selected local directory:
`D:/Projects/starfield-outpost-research/.local-work/position-write-history/builds/qualification-11`.
Exact DLL/ZIP/build-manifest hashes are recorded in the [review package](review.md)
and duplicated in the selected-artifact table in [report](report.md). Verify them
against those reviewed values before use; do not compute a new hash and silently
treat it as an approved pin. The command variable below is the reviewed manifest
hash, filled from that exact final artifact.

Runtime payload requires only
`Data/SFSE/Plugins/SorNativePositionOracle.dll`. Installed Windows/Microsoft /MD
prerequisites are pinned in build.json; no new runtime/dependency installation.
ResearchNotices are package material, not neighboring deployed-file requirements.
Require pinned game/SFSE/plugin identity, 129 guarded sites/target entries and
sole-thread SFSE pre-main admission. Standard Steam/NVIDIA overlays are accepted;
actual inventories are retained. Inspect unfamiliar instrumentation for credible
conflict; wrong identity, conflicting owned bytes or unsupported admission stops
capture. Never bypass a guard, patch another component or revive the debugger.

The plugin captures generic writes before save loading and flushes copied records
in groups. It changes timing, may apply OS/file backpressure and holds a spool
lock during flush. No observer lock spans native execution. Current QPC/sequence
capture gives operation intervals; overlapping threads do not establish exact
store order. Raw optional unreadable fields, unusual XYZ and delayed actions are
scientific evidence, not STOP conditions. No elapsed-time, cadence, operator
response, event-count or evidence-volume hard cutoff applies.

## Save instruction and finite gameplay scope

Prompt once, after matching fresh READY/ACK and before the load action:

> **Load Attila Kiraly Save25 — Kreet - Outpost, 10/9/26 at 9:22:22 PM (Level 4).**

This uses the already recorded screenshot mapping in the
[050 card](../ship-relocation-050/run-card.md#save-selection-supplied-in-advance).
Character name is maintainer testimony; label/date/time/level come from that
mapping. Mutable menu ordinal and [C] are not identities. Physical protected file:
`C:/Users/User/Documents/My Games/Starfield/Saves/Save25_D6036588M417474696C61204B6972616C79_000231_20261009102224_4_0_4.sfs`,
SHA256 `d4df86bc01c2105933fe856a1be5ebbe0c3fc78a4d67fe1a790e18129faf75f5`.
Ask for a new screenshot only on an actual conflict, absent/duplicate label or
wrong character filter. Do not repeat the selection confirmation after a clear
acknowledgement, and never guess by list position.

The finite sequence is Save25 load/settle at SOR-003 → one ordinary local travel
to SOR-002 → one ordinary return to SOR-003. The return tests a second loaded state/frame transition. Prior 050 local-only
003→002→003 produced no events; its 40 Workshop centers followed a fresh landing
and return, which is outside this card. Broader 060 writer/seven-center coverage
makes local travel a qualified diagnostic, but local-only center production is
unproven. This is not a new landing. No construction, beacon move,
console, settings change, new save, extra trip, build-mode intervention, new
landing or synthetic trigger is included. Native natural calls are observed;
center absence does not authorize adding gameplay actions.

## Machine preflight, before launch or save loading

Use PowerShell in `D:/Projects/starfield-outpost-research`. The helpers only audit
files/process metadata and control this observer's own session files. Each audit
output name must be fresh; check both exit status and its explicit JSON result.
Full protected hash audits may take time; delays are not health failures.

```powershell
$py = 'C:/Users/User/AppData/Local/Python/pythoncore-3.14-64/python.exe'
$build = '.local-work/position-write-history/builds/qualification-11'
$manifestPin = '5aa022529772285369aca2a7cafa4be240368ed83e94f635fdfb463ea2c803a8'
$game = 'C:/Program Files (x86)/Steam/steamapps/common/Starfield'
$live = '.local-work/position-write-history/live'
$run = '.local-work/position-write-history/run-' + (Get-Date).ToUniversalTime().ToString('yyyyMMddTHHmmssfffZ')
New-Item -ItemType Directory -Path $run -ErrorAction Stop | Out-Null
& $py -B runtime/native-oracle-060/operate.py preflight --build $build --manifest-sha256 $manifestPin --deployed --out "$run/preflight.json"
if ($LASTEXITCODE -ne 0) { throw 'Preflight failed; do not launch or load.' }
```

Codex verifies the reviewed manifest hash, DLL/ZIP/game/SFSE/system runtime pins,
protected saves/archives/frozen predictions/previous sessions, both caller-available
40,000,000,000-byte guards and deployed DLL-only contract. Confirm no previous
Starfield/SFSE process is active using read-only process metadata, and retain the
preflight existing-session list. Verify the approved SFSE loader is the previously
pinned installed loader, SHA256
`16916c2ec47e31774e3d550609a1844fcb368b03060c03511891564b7f5f7526`;
no updater/download or launch correction is authorized.

Before launch, retain a new local save inventory with paths, lengths, UTC mtimes
and SHA256 so incidental engine-generated ExitSave rotation can be reported
separately from canonical protected hashes. A private inventory stays local.
Do not overwrite any original or archive. Existing automatic exit-save behavior
is not an instruction to create a new save.

After successful preflight, the operator launches the approved normal SFSE entry
and remains at the menu until Codex clears READY/ACK. No second routine approval
is needed. Codex identifies exactly one new matching session relative to the
preflight inventory, verifies its PID **and process creation FILETIME**, candidate
hash/version/schema, loaded module inventory, admission receipt, patch inventory
and fresh READY. Use that exact session, never merely the newest old directory.

```powershell
$session = 'EXACT_NEW_MATCHING_SESSION_PATH'
& $py -B runtime/native-oracle-060/operate.py request --build $build --manifest-sha256 $manifestPin --session $session --out "$run/menu-request.json"
if ($LASTEXITCODE -ne 0) { throw 'Request/audit failed; inspect before gameplay.' }
$nonce = (Get-Content "$run/menu-request.json" -Raw | ConvertFrom-Json).nonce
& $py -B runtime/native-oracle-060/operate.py status --build $build --manifest-sha256 $manifestPin --session $session --nonce $nonce --out "$run/menu-status-01.json"
```

Require explicit `READY_ACK`, zero failed/integrity counters, actual admission
sole_thread_observed=true, expected 129 patches, matching original preimages and
healthy durable progress before loading. `WAITING_FOR_READY_OR_ACK` is pending,
not PASS: continue read-only inspection with fresh output names. Stale heartbeat
age alone is a warning; establish actual worker/integrity state. Do not add a
response timeout or repeatedly ask the user to confirm the save. If STOP occurs
before READY, do not load; retirement/not-ready evidence governs exit/recovery.

## Scene and travel coordination

1. Codex gives the exact Save25 instruction above once. Record the actual load
   acknowledgement/UTC and preserve all early generic load events; no identity
   filtering or history reset is allowed.
2. The operator reports actual visible settled state at SOR-003, including any
   loading/spinner/control oddity. Codex records the phase and requests a fresh
   ACK using a new output name, then checks its explicit status/flush counts.
   Do not equate a stable picture or repeated center with complete writer history.
3. Codex directs one ordinary travel to the existing SOR-002 outpost. The operator
   reports actual arrival/settling. Repeat the fresh ACK and phase receipt. Do
   not select a new landing point, enter console or create a save.
4. Codex directs one ordinary return to the existing SOR-003 outpost. The operator
   reports actual visible state; repeat the fresh ACK/phase receipt. Preserve
   queued command producer/application relationships even if application occurs
   on another thread or after a producer returns.
5. Codex checks whether coherent Workshop-ID centers and useful writer intervals
   were captured, naming missing native paths/identity/epochs precisely. Continue
   healthy acquisition through delayed natural calls/odd values without inventing
   extra actions. The finite approved action scope may yield a partial scientific
   result. Agree completion on the observed evidence or honor explicit STOP;
   neither a record quota nor a wall-clock expiry decides completion.

Known stable Workshop ID byte strings are `f1517de43e171745` (SOR-002) and
`0efca066ee4c7b9b` (SOR-003), with ordinary base 002C60E9 and prior saved Kreet
association. Reacquire raw identities each epoch. Current FormIDs/pointers are
not saved tokens. Own-parent/world unavailable fields remain unavailable.

## STOP, integrity failures and recovery

Codex can request STOP before/after READY with the same verified session:

```powershell
& $py -B runtime/native-oracle-060/operate.py stop --build $build --manifest-sha256 $manifestPin --session $session --out "$run/stop.json"
```

STOP bypasses protected/deployed admission checks and writes exactly four bytes
to the preallocated flag. It is idempotent. If disk queries fail, the helper still
requests STOP and prints the result but does not grow a new receipt. Manual
fallback, after verifying the same session/path, writes those existing bytes:

```powershell
$flag = Join-Path $session 'operator-stop.flag'
$handle = [IO.File]::Open($flag, [IO.FileMode]::Open, [IO.FileAccess]::Write, [IO.FileShare]::Read)
try { $handle.Write([Text.Encoding]::ASCII.GetBytes('STOP'), 0, 4); $handle.Flush($true) } finally { $handle.Dispose() }
```

Do not mistake STOP requested for retirement. New invocation admission closes;
already admitted invocations may still be executing and must finish/unwind or
remain explicitly unfinished. The worker flushes their completion records before
closing logs. Wait for accurate retired/failure/emergency evidence, inspect active
counts and actual worker state. Never unhook/unload a running game or patch bytes
to accelerate retirement. Resident wrappers/relays stay inert until normal exit.

Actual wrong identities, native guard changes, disk-query/floor failure,
write/flush/accounting failure or dead worker are safety/integrity failures.
The plugin closes admission and records the cause/counts where possible. A missing
terminal or failed emergency page is an integrity/retirement gap, not successful
cleanup. Optional unreadable fields, nonfinite/odd scientific values, missing
centers and slow operator/monitoring response alone do not stop healthy capture.

On failure, preserve the exact current session and all traces; no retry, package
change, exception suppression, settings repair or game termination is authorized.
Ask the operator to exit normally when safe. If normal exit is impossible, report
the actual state for a recovery decision; do not force it. If the game exits or
crashes after evidence flush, retain and analyze the complete prefix separately
from target survival. A pre-evidence crash is not scientific success. No automatic
restart or second session follows. Protected-input changes require an integrity/
recovery decision; never copy a backup over the changed original.

## Normal exit, removal, postflight and immutable seal

After verified retirement, the operator exits normally, allows normal sync and
disables/removes the candidate through Vortex. Codex independently verifies the
original process identity has exited, deployed plugin is absent, original
protected hashes and both disk guards pass, and save inventory changes are
explained. Do not remove unrelated plugins or notices manually.

```powershell
& $py -B runtime/native-oracle-060/operate.py postflight --build $build --manifest-sha256 $manifestPin --session $session --out "$run/postflight.json"
& $py -B runtime/native-oracle-060/operate.py seal --build $build --manifest-sha256 $manifestPin --session $session --out "$run/sealed-session-files.json"
& $py -B runtime/native-oracle-060/inspect_history.py $session --summary --output "$run/committed-prefix.json"
& $py -B runtime/native-oracle-060/inspect_history.py $session --workshop f1517de43e171745 --workshop 0efca066ee4c7b9b --output "$run/workshop-histories.json"
```

Require explicit `PASS_TRANSPORT_POSTFLIGHT` for clean engineering cleanup.
Other statuses preserve partial/failing evidence, not a clean PASS. Seal only
after the original process is confirmed gone and before later analysis writes;
analysis outputs go in `$run`, outside the original session. Verify every sealed
length/hash after analysis. No raw events, saves, memory or private module paths
are staged/uploaded. If protected/disk audits prevent the helper, preserve all
bytes and report that blocker; read-only hash inventories may still be retained
under the unchanged guards, without authorizing input restoration.

## Required scientific handoff after the future live run

The final live handoff includes scientific reconciliation and independent review
as well as cleanup/sealing, unless the operator expressly asks only for an
intermediate operational checkpoint. Use the unchanged frozen Save25/26 inputs,
prior Z [comparison ledger](../workshop-z-restoration/comparisons.csv) and selected
saved fields; do not update predictions to match observations.

For each coherent Workshop candidate, retain exact before/after reference XYZ,
operand XYZ/mode, d3, compensation and actual returned center bytes; order native
operations by their proven invocation/ancestry/interval relations. Report the
earliest captured setter/input, last demonstrated writer before each center,
measured signed Z effect and any intervening replacement. Test per-invocation
binary32 arithmetic and raw-byte equality without inventing a height datum.
Body/frame/saved-reference associations need independent evidence; null own cells
or equal IDs do not supply a complete restore epoch or pointer lifetime.

Prospective results:

- Measured signed conversion or replacement reconciles a sampled Z difference:
  report that bounded causal interval and its identity/frame qualifications.
- Center/reference/compensation arithmetic matches but a writer/epoch is missing:
  report partial history and deepest observed operation, not full restoration.
- Observed values contradict a frozen comparison: preserve the counterexample
  and distinguish frame/identity/coverage uncertainty from arithmetic disagreement.
- No relevant writes/centers or broken transport: unavailable/partial evidence,
  never a scientific no-write negative merely because hooks were installed.
- Complete history or scoped no-write may be claimed only with an independently
  demonstrated covered writer set, lifetime/interval and ownership argument.

Deliver actual pass/fail/NOT_TESTED accounting, raw/derived provenance, exact
changed/excluded manifests, independent scientific review and complete/task-only
review patches. New native hooks, trips or experiments require a separate decision.
