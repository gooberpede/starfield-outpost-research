# Center-only live smoke procedure — review before attachment

2026-10-11 Australia/Sydney; SOR-D-0046, continuing SOR-EXP-0026.
The maintainer approved external adapter **0.1.3**, then requested this procedure
for review. **This document does not authorize launch, load or attachment.**
No live run has been performed. Execute only after explicit authorization of this
card, its process reads, operator actions and recovery limits. Record that
authorization verbatim with UTC time in the session notes.

## Launch and configuration decision

Use **ordinary Steam Play**, with Steam already running. Do not use an SFSE
launcher for this first smoke. The installed launcher is `sfse_loader.exe`, not
`sfse_launcher.exe`; SFSE's installed readme instructs that loader for SFSE use
([SOR-S-0112](../../SOURCES.md)). The external debugger requires no SFSE plugin.
The ordinary Steam choice deliberately gives this smoke a configuration distinct
from earlier observer sessions; preserve the actual loaded-module inventory.

Do not deploy the adapter through Vortex or copy anything into the game directory.
Keep the external executable and evidence beneath ignored repository local work.
Existing SFSE files may remain on disk. Check Steam's launch options visually
before launch: if they invoke a loader/wrapper, stop for configuration review;
do not silently change them. Loaded modules must independently show no SFSE or
SorBeaconObserver. Inventory all other modules and the active content list;
unexplained changes or a missing-content warning on load stop this procedure.
Do not disable plugins, purge Vortex, alter launch options or accept a load warning
to make this card work. Steam launch compatibility with the selected save is an
operational prerequisite, currently untested.

## Fixed scope and pins

Exactly two INT3 sites, `--center-only`; grid remains independently available via
`--center-and-grid` for a separately reviewed session and is excluded here.
The adapter stops all target threads on debugger events, copies bounded memory,
durably writes evidence, replays the original instruction with owned TF and
temporary suspension of other threads, and rearms. STOP may use DebugBreakProcess
and create an OS break-in thread. These timing effects are explicitly accepted
only by subsequent live authorization; this is intrusive instrumentation.

| Item | Required identity |
|---|---|
| Executable | `C:\Program Files (x86)\Steam\steamapps\common\Starfield\Starfield.exe`, 1.16.244.0 |
| Game SHA-256 | `7e9adb1414a8e1b325e5e1f097b9b17b78deb7eebeda37a333351a43a60f9d28` |
| Approved ZIP | `.local-work/event-latency/review-01/SorEventOracle-0.1.3.zip` |
| ZIP SHA-256 | `2e29c452b566b992bc504cf0d6e2c4971675aabd47ad4d3408b455268c121efc` |
| Adapter SHA-256 | `b0751a86655b0a4759932f0b90cfcd7aeb9314f9a03b5a52d4522ba5bd1c1eb3` |
| Entry RVA / original instruction | `0xF4AB80` / `48 89 5c 24 08` (5 bytes) |
| Entry original 32-byte SHA-256 | `702240fe34296bf5b3845f8d877438ffc5a2343beac2811bf67307a6de0fc7cc` |
| Common exit RVA / original instruction | `0xF4AC44` / `48 8b 5c 24 40` (5 bytes) |
| Exit original 32-byte SHA-256 | `75395a678542d156d2480f475573ff5c81c9459684c7e5eabe2e2f9a9df85e6d` |

The live VA is **discovered main-module base + RVA**, never the static analysis
VA. [Qualification](qualification.md) is disposable-only: median handler 0.475 s,
observed maximum 0.724 s in one matched fixture run, with no live latency bound.
Evidence writing remains synchronous and flushed before continuation; do not
assume this is an asynchronous writer or that a busy scene stays responsive.

## A. Offline preparation and protected inputs

Run from a 64-bit PowerShell in the repository root, after card authorization.
Use a new session name each attempt; never reuse evidence or overwrite receipts.
The currently qualified executable below is byte-identical to the approved ZIP's
`tool/SorEventOracle-0.1.3.exe`. No extraction/deployment is necessary.

```powershell
Set-Location 'D:\Projects\starfield-outpost-research'
$python = 'C:\Users\User\AppData\Local\Python\pythoncore-3.14-64\python.exe'
$tool = 'D:\Projects\starfield-outpost-research\.local-work\event-instrumentation\latency-candidate-013-02\adapter.exe'
$gameSha = '7e9adb1414a8e1b325e5e1f097b9b17b78deb7eebeda37a333351a43a60f9d28'
$name = 'center-smoke-' + (Get-Date -Format 'yyyyMMdd-HHmmss')
$ops = "D:\Projects\starfield-outpost-research\.local-work\event-oracle-operations\$name"
$session = "D:\Projects\starfield-outpost-research\.local-work\event-oracle-live\$name"
if ((Test-Path $ops) -or (Test-Path $session)) { throw 'Use a NEW session name' }
New-Item -ItemType Directory -Path $ops | Out-Null
New-Item -ItemType Directory -Path (Split-Path $session) -Force | Out-Null
& $python -X utf8 -B debugger/event-smoke/checks.py offline --output "$ops\offline-before.json"
if ($LASTEXITCODE -ne 0) { throw 'Offline preflight failed; do not launch/attach' }
```

The [checker](../../../debugger/event-smoke/checks.py) hashes the game, approved
ZIP, executable, original Save25/26 and both existing protected archive copies
against the prior integrity manifest. It queries caller-available C:/D: bytes;
both must be at least **40,000,000,000**, with failed queries blocking. It only
reads inputs and writes a new JSON receipt. Review its source and preserve its
hash with the card; it is operational support outside the unchanged approved
adapter. Its live modes have not yet been exercised against Starfield.

The offline checker also verifies the four frozen files against
[the prior manifest](../../../.local-work/event-latency/input-integrity-after.json)
(`inputs.json`, `predictions.json`, `validation-protocol.md`, `Phase1-checkpoints.csv`
under `docs/experiments/engine-oracle`), inventories save filenames/size/mtime and
retains content-list text/hash. Preserve the launch options, game version and
relevant module/plugin configuration notes in `$ops`. Compare these observations
with the accepted configuration; a hash alone does not qualify the load order.
These receipts remain local, untracked.

The sole proposed load is the existing controlled **Save25**, filename
`Save25_D6036588M417474696C61204B6972616C79_000231_20261009102224_4_0_4.sfs`,
original under `C:\Users\User\Documents\My Games\Starfield\Saves` and protected
copy under `.local-work/savegames/two-outpost-anchor/exact-beacon-01`.
SHA-256 `d4df86bc01c2105933fe856a1be5ebbe0c3fc78a4d67fe1a790e18129faf75f5`.
Preserve both originals and archives; no manual saving or overwriting, save
renaming/replacement, construction, beacon relocation/deletion or native call
injection. Inventory incidental new autosaves afterward; do not delete them or
change autosave/cloud settings. If this protection cannot be maintained, hold
before loading and resolve the controlled-copy procedure separately.

## B. Operator scene and correct-process preflight

1. User launches through ordinary Steam, loads the exact Save25 entry and reports
   the existing SOR-003 Kreet outpost scene with build mode **closed**. Record the
   selected load entry, HUD/site identification, loaded content, time/scene and
   whether any warning appeared. If the expected scene cannot be identified
   without travel, stop for review; do not extend travel/load scope. Site identity
   at this stage is operator-reported, awaiting native identity evidence.
2. Hold input at the agreed scene. Query process inventory without attachment:

   ```powershell
   $games = @(Get-Process Starfield -ErrorAction SilentlyContinue)
   if ($games.Count -ne 1) { throw 'Exactly one Starfield process required' }
   $targetPid = $games[0].Id
   & $python -X utf8 -B debugger/event-smoke/checks.py pre --pid $targetPid --output "$ops\process-before.json"
   if ($LASTEXITCODE -ne 0) { throw 'Process preflight failed; do not attach' }
   ```

3. Review the receipt: exact full executable path/hash, original process creation
   FILETIME, single PID, main-module base, both actual original 32-byte windows,
   no existing debugger and no SFSE/observer module. Review all other modules
   against the accepted configuration; an unrecognized/conflicting instrument
   stops preflight. This is a read-only process open, not debugger attachment.
   The reader uses QUERY_INFORMATION/VM_READ, no target write/control APIs.
4. Recheck PID, creation time and alive status immediately before attachment by
   running `pre` again into `process-immediate.json`; compare identity/base with
   `process-before.json`. Any intervening exit, restart, hash mismatch, site-byte
   mismatch, inaccessible module or ambiguous inventory blocks attachment.
   Never substitute a newly reused PID. Receipts are point-in-time observations;
   the adapter also repeats game SHA and live byte guards at installation.

The adapter itself binds the supplied PID to a Starfield basename and pinned
on-disk hash, not to the operator's selected full path or creation time. The
independent receipt and no-restart handshake close that operational gap; do not
describe its built-in check as a creation-time lock.

## C. Attachment, breakpoint confirmation and operator handshake

Only after separately authorized attachment and all preflights PASS:

```powershell
if (Test-Path $session) { throw 'Evidence root must be absent' }
$adapter = Start-Process -FilePath $tool -ArgumentList @('--reviewed-retail', [string]$targetPid, $session, $gameSha, '--center-only') -WindowStyle Hidden -PassThru -RedirectStandardOutput "$ops\adapter.stdout.txt" -RedirectStandardError "$ops\adapter.stderr.txt"
$adapter.Id | Set-Content "$ops\adapter-pid.txt"
```

Record attachment UTC, adapter PID/hash/arguments and target creation identity.
The adapter obtains the actual base at CREATE_PROCESS, validates **both** complete
32-byte guards before patching, then installs and verifies each CC byte. Guard
failure is a stop, not permission to alter expected bytes. No grid patch is
requested. Original instruction replay is in place; no trampoline.

Wait for a **new** `$session\READY` containing `0.1.3` and a hash-valid WAL prefix
containing `session` (`evidence_kind=RUNTIME`, correct PID and image SHA) and
`ready` (same live base as preflight). Inspect the prefix using the approved
decoder in a separate Python invocation; it reads only, and writes no derivative:

```powershell
$env:SOR_SMOKE_WAL = "$session\evidence\epochs.wal"
@'
import os, sys
from pathlib import Path
sys.path.insert(0, 'debugger/event-oracle')
from materialize_epochs import decode
rows, receipt = decode(Path(os.environ['SOR_SMOKE_WAL']))
print(receipt)
print([r for r in rows if r['kind'] in ('session', 'ready', 'retired', 'target_exit', 'terminal')])
'@ | & $python -X utf8 -B -
```

Retain the output/time in the notes. A growing WAL snapshot can end in an
incomplete tail; retain that fact and repeat the read after progress. A complete
frame hash/sequence failure stops the run. File size, READY alone or a readable
prefix is not proof that all subsequent flushes have completed. The approved
writer emits the ready event durably before creating READY; there is no separate
per-site installed-preimage journal. Installation confirmation therefore combines
preflight windows, source-qualified guards, ready base and later restoration.

Before any operator trigger confirm adapter still alive, no error/retirement,
target responsive and READY/prefix identity accepted. Say **“CENTER SMOKE READY:
open build mode once, let it settle, then close it and stop input.”** User
acknowledges before acting. Record UTC before/after each action, visible state
and unexpected pauses in `$ops` notes. READY does not inhibit spontaneous native
calls; a fixture `GO` file has no retail meaning. Retain events during arming.

Allowed phases: known scene closed → **one** ordinary build-mode open → normal
UI settlement → close build mode → hold input → STOP. No repeated forcing for
hits, travel, site switch, Save26 comparison, camera experiment or game commands.
If build mode cannot settle or controls stall, use section E immediately. These
are finite operator phases, not hit/file/time acquisition quotas. Zero calls is
NOT_OBSERVED, not permission to widen scope. Timestamp proximity alone does not
prove which operator action caused a call.

## D. Normal retirement, independent checks and durable evidence

After closing build mode, or on any stop condition, request cooperative STOP once:

```powershell
New-Item -ItemType File -Path "$session\STOP" -ErrorAction Stop | Out-Null
```

Observe adapter progress without blocking the operator channel. On idle it polls
at approximately 100 ms and requests an OS break-in; on events it checks STOP
after handling. Retirement restores/verifies all original 32-byte windows, clears
owned TF, resumes only owned suspension increments, continues the event, detaches
and writes `retired/restored:true`, post-detach timing and terminal `RETIRED`.
Wait for adapter exit, preserving stdout/stderr and actual exit code. Require
exit 0 for normal retirement, then independently query the **same surviving
process**:

```powershell
$adapter.Refresh()
if (-not $adapter.HasExited) { throw 'Still running: follow stalled-target procedure' }
$adapter.ExitCode | Set-Content "$ops\adapter-exit.txt"
& $python -X utf8 -B debugger/event-smoke/checks.py post --pid $targetPid --pre "$ops\process-immediate.json" --output "$ops\process-after.json"
```

Require original creation time/path/base, alive target, debugger absent and exact
original 32-byte windows at both sites. The helper does not independently inspect
each thread's TF/suspend count: those are adapter retirement assertions supported
by disposable qualification. Report this limit, rather than claiming a separate
thread-state audit. A failed check blocks a clean-retirement conclusion.

Once adapter is exited and detached (or target definitively exited under E), hash
and retain the immutable original WAL, including any tail. Make a local snapshot
with matching hash for analysis; never truncate/repair the original. Run offline:

```powershell
Get-FileHash "$session\evidence\epochs.wal" -Algorithm SHA256
& $python -X utf8 -B debugger/event-oracle/materialize_epochs.py "$session\evidence" --output "$ops\materialized"
if ($LASTEXITCODE -ne 0) { throw 'Integrity/materialization failure: retain original' }
& $python -X utf8 -B debugger/event-oracle/inspect_events.py "$ops\materialized" --output "$ops\inspection.json"
if ($LASTEXITCODE -ne 0) { throw 'Inspection failed: retain original and report' }
& $python -X utf8 -B debugger/event-smoke/checks.py offline --output "$ops\offline-after.json"
```

Require valid sequence/hash chain/raw hashes, terminal RETIRED with no tail for
normal completeness, session RUNTIME/PID/hash, only the two center boundary sites,
ready/retirement ordering, no integrity/guard/control failure, and inspect actual
entry/exit pairing, identity and captured 12-byte center. Retain optional unreadable
fields, unwinds/unpaired events and zero hits as partial outcomes. Decoder-valid
bytes after a writer failure do not prove a failed FlushFileBuffers succeeded.
An orderly terminal establishes the adapter's flush acknowledgements, not immunity
to storage hardware or OS failure. Keep original WAL hash and decoder receipt.

The inspector intentionally defaults `live_game_qualification=false` and frame/
scientific status UNASSESSED; do not edit those flags to manufacture qualification.
Prepare a human-reviewed runtime ledger from actual records. A useful center
sample needs positive workshop/base identity, paired producing invocation and
native output; common body/frame reconciliation and frozen exact-bit comparison
remain separate scientific work. A successful no-hit run proves only scoped
readiness/restoration, not acquisition semantics. Never tune predictions/tolerance.

After independent retirement the user may exit normally. Rehash original/archive
saves and frozen files, inventory new autosaves and record loaded configuration,
target survival, latency/health, evidence completeness and scientific usability
as separate outcomes. A changed protected file is an incident, not permission to
overwrite it from archive. All raw evidence, notes and binaries stay local and
untracked. No stage/commit/push/upload follows.

## E. Stalled, failing or exiting target

Stop on operator request, unexpected integrity/patch/control failure, disk query
failure or either drive below 40 GB, sustained pauses preventing ordinary input,
unexpected corruption, or target exit. Optional missing science, ordinary foreign
exceptions and missing pairs remain partial and continue under the adapter's
continuation-first policy; do not suppress game exceptions.

- **Slow or apparently stalled but alive:** stop operator input, create STOP once,
  note UTC, adapter/target PIDs and last valid evidence/progress. Check progress
  every 10 seconds and report unresolved status at 30 seconds. These are operator
  communication/escalation intervals, not a guaranteed timeout or capture quota.
  Record file progress, process responsiveness, disk space and errors; do not run
  the pre/post original-byte check while breakpoints are armed. No additional
  debugger or automatic retry. Continue observing cooperative retirement.
- **STOP cannot complete:** synchronous WriteFile/FlushFileBuffers or an OS call
  can block before STOP is checked. **0.1.3 has no watchdog and no guaranteed
  rollback deadline.** Killing the adapter can leave INT3 bytes or owned thread
  state behind; SetKillOnExit(FALSE) does not restore code. Do not force-kill
  adapter/target, patch memory/registers, suppress exceptions, or attach another
  debugger. Preserve local artifacts, keep the operator informed and return for
  separately authorized recovery. A hard-recovery requirement blocks this card
  until a separately reviewed design supplies it. Normal Quit is available only
  if the target is responsive and retirement/detach has been independently checked.
- **Target exits/crashes:** record observed exit, process identity, adapter logs/
  exit code and `target_exit`/`TARGET_EXIT` records if actually present. The adapter
  normally continues the exit event and finalizes evidence, but writer failure
  can interrupt that path. Never promise a retirement record. Preserve the valid
  WAL prefix and incomplete tail without repair. Live code restoration and detach
  cannot be independently checked on an exited process: classify **TARGET_EXIT,
  NO_LIVE_RESTORATION_CHECK**, not clean retirement. Do not relaunch/reuse PID.
- **Adapter error/exits while target lives:** stderr `attached=0` is a report, not
  independent proof. Attempt only the read-only postflight; if original windows/
  debugger state fail or cannot be read, report unresolved instrumentation and
  hold for recovery authorization. Do not resume gameplay on assumed cleanup.

A post-capture exit does not automatically invalidate complete flushed evidence;
pre-evidence failure is not acquisition success. Evidence completeness, target
survival and scientific result are distinct. The review decision must explicitly
accept the bounded latency/stall exposure and the lack of forced recovery, or
request a separate adapter change before attachment.

## Review deliverable and authority boundary

Return authorization record, exact tool/process/site receipts, configuration and
protected-input inventories, operator chronology, original WAL hash/retained-tail
status, materialization/inspection/timing, restoration/detach result and any
incident. No scientific promotion, second run, grid enablement or live comparison
follows automatically. [Preparation review](procedure-review.md) lists actual
offline checks and unchanged approved artifacts. The card remains prospective.

## Execution status supplement — 2026-10-11

The maintainer subsequently approved this card and explicitly accepted unrecovered
debugger stall risk. [First attempt](center-smoke-20261011-result.md) passed live
preflight but adapter exited before READY/evidence. Independent postflight passed,
then the user exited normally. Earlier prospective statements describe the card's
preparation state. No automatic retry; investigate/review startup failure first.
