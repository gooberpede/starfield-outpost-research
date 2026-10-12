# Q030 revised run card02 — one new Kreet landing, no manual saves

2026-10-12. **PROPOSED — awaiting maintainer approval of this exact revised card.**
This card proposes one controlled session; it does not authorize execution now.
After approval of this exact card and user Vortex deployment, passing mandatory
preflight authorizes the specified machine-side actions without another routine
approval. User controls launch, loading, map selection, one landing and normal exit.
No new manual saves are permitted. This is a new attempt, never resumption of attempt01. [Trigger basis](trigger-justification.md), [checks/review](procedure-qualification.md),
[tool contract](../../../research/q-branch-030-procedure/README.md).


This card supersedes the prospective execution procedure in [card01](live-run-card.md)
only after new explicit approval. [Attempt01](live-attempt-01.md) and its failed
external snapshot remain closed, unchanged evidence. The plugin, hooks, config,
schema and qualified Python tools are unchanged. Lock05 has310 pins; no regeneration.
Current task is documentation preparation and review only. Live usability of the
cooperative inventory and scientific reachability remain NOT TESTED.

## 1. Exact candidate and approval choices

Approve **one new Kreet landing from Save27, with no new manual saves**.
There is no optional checkpoint pair and no save-creation cue. No Save25/26 controls, second landing,
new outpost, construction, console, debugger, extra hooks or other geography.
Retain all unexpected observations; an unproductive trigger does not authorize retry.

Retail Starfield1.16.244.0; SFSE0.2.21 for1.16.244. Exact SHA256:

| Artifact | SHA256 |
|---|---|
|Starfield.exe|7e9adb1414a8e1b325e5e1f097b9b17b78deb7eebeda37a333351a43a60f9d28|
|sfse_1_16_244.dll|28c5bda41d9959c885efcb6e889de69e92767c80a1a66842d711d215f722f82b|
|sfse_loader.exe|16916c2ec47e31774e3d550609a1844fcb368b03060c03511891564b7f5f7526|
|SorNativePositionOracle-0.3.0.zip|bc51e7aad714880f419d07dab5dad1f8451934148ac5180564ee2a34891c627f|
|SorNativePositionOracle.dll|a2b0c90525928f287e2168f0d0c7150253f4d6c2089e79a8ab3b9925c9f5bfa6|
|SorNativePositionOracle.config|6894da75d4face7b9d366a67c436fe75b100a434e073f7184bcca55e19d953c9|
|schema.md (schema3,17768-byte events)|c5e62c7f634333285413e5f633e3c7e28c71039827ca2f45f452838a61b27492|
|build.json|6bdadc78ebfe1552adae913bb75cd5c0d54fc44ab4a5a4d12eb2bb4742b222f7|
|release-lock-05.json|d25345876fa33719e9aaccc3bd021e6efa131c375e357687ec8c369956cacd73|

ZIP/build are in `D:/Projects/starfield-outpost-research/.local-work/native-oracle-030/builds/qualification-02/`.
No rebuilding, config edits or substituted candidate. User installs/enables this ZIP
through Vortex only, confirms profile `Starfield - SFSE`, deploys and later removes it.
Archive has five members: `Data/SFSE/Plugins/SorNativePositionOracle.{dll,config}`
and `ResearchNotices/{PROJECT-LICENSE,READ-ME,SFSE-PluginAPI-LICENSE}.txt`.
DLL/config remain at game-root Data/SFSE/Plugins. Notice paths for this revised
card are explicitly mapped in section2a; no extra nested Data/SFSE/Plugins is allowed.
Only this candidate DLL may be present in the SFSE Plugins folder for this run.
Inventory other load-order/config files and record Vortex active profile/mod state
read-only; no automatic installation/configuration correction. Steam and NVIDIA
overlays are accepted baseline modules; log them. Assess actual competing native
instrumentation/patches specifically; unknown names alone are not evidence of conflict.

## 2. Preflight while game/loader/debuggers are absent

Commands below are **future approved execution only**. Use repository-root PowerShell.
All paths are actual installation paths; `$session` is resolved from the new native
receipt, from a fresh session only. No manual-save path or checkpoint command is used.

```powershell
Set-Location D:/Projects/starfield-outpost-research
$py='C:/Users/User/AppData/Local/Python/pythoncore-3.14-64/python.exe'
$tool='D:/Projects/starfield-outpost-research/research/q-branch-030-procedure/procedure.py'
$lock='D:/Projects/starfield-outpost-research/.local-work/q030-module-inventory-fix/release-lock-05.json'
$lockSha='d25345876fa33719e9aaccc3bd021e6efa131c375e357687ec8c369956cacd73'
$native='D:/Projects/starfield-outpost-research/runtime/native-oracle-030/operate.py'
$run='D:/Projects/starfield-outpost-research/.local-work/q-branch-030-procedure/live-'+[DateTime]::UtcNow.ToString('yyyyMMddTHHmmssZ')+'-'+[guid]::NewGuid().ToString('N')
# Run the exact mapped-path deployed preflight in section 2a below.
# It creates $run/audit.json only after all mapped installation checks pass.
# Do not run the environment command until section 2a succeeds.
$environment='D:/Projects/starfield-outpost-research/research/q-branch-030-procedure/environment.py'
```

Audit verifies310 pinned files, ZIP member CRC/hash/membership, five installed
members, loader identities, required paths, save inventory, prior session names and
target/loader/debugger absence by process names. It does not open Starfield.
At least40,000,000,000 **caller-available** bytes on C and D is mandatory throughout;
failed queries fail. Pin drift or conflicts mean no launch; no bypass/repair within run.
Preserved inputs include Save25/26 originals/copies, Save27/28 originals/copies,
prior raw020 evidence, frozen predictions and unchanged030 sources/build receipts.
No active save is overwritten or renamed. Current offline inventory contains no
plugin DLL in the last retained offline audit; this is not a future deployment attestation.

Environment inventory retains contents/hashes of
`C:/Users/User/AppData/Local/Starfield/{Plugins.txt,loadorder.txt}` and
`C:/Users/User/Documents/My Games/Starfield/{Starfield.ini,StarfieldCustom.ini,StarfieldPrefs.ini}`
locally, plus game-root/Data file names and sizes. ABSENT is explicit, unreadable
fails; absence is reviewed against operator-confirmed profile, not silently treated
as an empty readable file. Vortex profile display name remains operator-confirmed;
folder identifiers do not establish it. No configuration is changed.


## 2a. Explicit Vortex notice mapping and deployed preflight

Approval of this exact card includes these three **location-only** mappings:
archive `ResearchNotices/{PROJECT-LICENSE,READ-ME,SFSE-PluginAPI-LICENSE}.txt`
maps to game-root `Data/ResearchNotices/` with the same basename and exact lock05
member hash. All three notices must exist and hash correctly; nothing is waived
or optional. Canonical root notices, if present, must also match. DLL/config and
loader paths/hashes and all310 pins remain unchanged. No prior exception is assumed
to grant this new attempt. Missing/changed files stop preflight; Codex does not
move/copy/install notices or edit game/Vortex configuration. User deploys via Vortex
only after approving the card; normal Vortex mapping is checked as deployed.

The original `audit --mode deployed` assumes archive-root notice locations and
would reject this Vortex layout. The following reviewed, future-only file-check
recipe retains an original offline audit separately and writes an explicit mapped
deployed receipt for admission/monitor. It does not modify the lock or tool source,
skip a hash, fake an original deployed audit, or perform any deployment. Run after
section2 variable assignments and before environment inventory. Only this recipe
may make the mapped audit receipt; do not hand-edit PASS fields after a failure.

```powershell
@'
import copy,sys
from pathlib import Path
sys.path.insert(0,'D:/Projects/starfield-outpost-research/research/q-branch-030-procedure')
import procedure as p
lock=p.lock_file(sys.argv[1],sys.argv[2]);run=Path(sys.argv[3])
p.guard();p.pins(lock);p.archive_check(lock)
mapped=copy.deepcopy(lock); mapped['package']={}
mapping={}
for name,expected in lock['package'].items():
    actual='Data/'+name if name.startswith('ResearchNotices/') else name
    mapped['package'][actual]=expected;mapping[name]=actual
    canonical=Path(lock['game_dir'])/name
    if actual!=name and canonical.exists() and (not canonical.is_file() or p.sha(canonical)!=expected):
        raise ValueError('canonical_notice_drift:'+name)
inventory=p.installation(mapped,'deployed')
run.mkdir(exist_ok=False)
base=p.audit(lock,'offline',run/'preflight-base')
result=dict(base,mode='deployed',plugin_inventory=inventory,
    installation_method='REVIEWED_CARD02_VORTEX_NOTICE_MAPPING',
    notice_mapping=mapping,archive_lock_sha256=sys.argv[2],
    limits='Mapped file-only deployed audit; no live admission. Profile requires operator confirmation.')
p.write(run/'audit.json',result)
p.write(run/'mapped-installation.json',dict(mapping=mapping,package_hashes=lock['package'],pass_check=True))
print('MAPPED DEPLOYED PREFLIGHT PASS; no launch performed')
'@ | & $py -B - $lock $lockSha $run
if ($LASTEXITCODE -ne 0) { throw 'NO LAUNCH: mapped deployed preflight failed' }
& $py -B $environment --lock $lock --lock-sha $lockSha files --out ($run+'/environment-before.json')
if ($LASTEXITCODE -ne 0) { throw 'NO LAUNCH: environment inventory failed' }
```

This recipe reads package/game/loader/save/source files and process **names**,
writes exclusive ignored run receipts, and uses existing stdlib/project helpers.
No target process handle/memory query, deployment, privilege change or save write.
Recheck disk and installation if operator delay/deployment changes make preflight
stale. Do not reuse attempt01 audit, identity, session directory or ASLR base.

After exit/user removal, run before the normal postflight below:

```powershell
@'
import sys
from pathlib import Path
sys.path.insert(0,'D:/Projects/starfield-outpost-research/research/q-branch-030-procedure')
import procedure as p
lock=p.lock_file(sys.argv[1],sys.argv[2]);run=Path(sys.argv[3]);p.guard()
mapping=p.read(run/'mapped-installation.json')['mapping']
expected={n:('Data/'+n if n.startswith('ResearchNotices/') else n) for n in lock['package']}
if mapping!=expected:raise ValueError('mapping_drift')
paths=sorted({str(Path(lock['game_dir'])/n) for n in (*lock['package'],*mapping.values())})
if any(Path(n).exists() for n in paths):raise ValueError('candidate_mapped_removal_incomplete')
p.write(run/'vortex-mapped-removal.json',dict(utc=p.now(),paths=paths,pass_check=True))
'@ | & $py -B - $lock $lockSha $run
if ($LASTEXITCODE -ne 0) { throw 'Removal failed: preserve incident, no retry' }
```

## 3. Launch, bounded admission and independent worker clearance

Operator launches once via the confirmed Vortex SFSE profile and remains at main
menu. Record operator launch UTC and begin a monotonic stopwatch at the launch cue;
record any cue-to-launch delay separately, never subtract it to extend a bound.
Poll the fresh-session files at most1 second apart and durably record the first
external READY observation UTC plus elapsed stopwatch time. READY `utc` is session
initialization time, not READY publication/observation; do not use it as proof.
Allow at most135 seconds from the launch cue for a fresh native
session READY (plugin nominal startup wait120 seconds, not an exact scheduling
guarantee). Identify exactly one directory absent from `$run/audit.json` prior_sessions,
under `D:/Projects/starfield-outpost-research/.local-work/native-oracle-live/session-*`.
Set `$session` to its full path; never select the newest historical session blindly.
No READY, failure/not-ready receipt or ambiguity: STOP owned new session if available,
normal exit, retain incident, no retry. Never send STOP to a protected old session.
The unchanged STOP CLI requires ready.json. Before READY it may be unavailable:
record STOP unavailable/failed rather than claiming retirement, cue normal operator
exit without gameplay and retain the startup prefix. Unresponsive normal exit needs
fresh recovery authority; no automatic kill, patch or retry.

```powershell
# Substitute the one newly created receipt directory, verified against audit.json.
$session='D:/Projects/starfield-outpost-research/.local-work/native-oracle-live/session-<new-pid>-<new-token>'
& $py -B $tool --lock $lock --lock-sha $lockSha admit --session $session --run $run
if ($LASTEXITCODE -ne 0) {
  & $py -B $native control $session STOP
  throw 'NO GAMEPLAY CUE: admission failed; retire and exit normally'
}
```

Admission cross-checks PID/creation identity, runtime base, schema/DLL/game/SFSE,
grid+center channels, startup gates, thirteen edits (eleven original E8 CALL guards
and two callback slots), eleven unique14-byte FF25 RX relays, and relay targets
inside the exact loaded candidate. Receipt hashes are self-attestation, not an
external memory read. Review `modules-pre-edit.jsonl` and currently available
module inventory; accept standard overlays, reject a demonstrated conflicting
instrument/patch. Do not hot unload anything. Record review and operator profile
confirmation in a new `$run/operator-confirmation.json`:

```powershell
& $py -B $environment --lock $lock --lock-sha $lockSha modules --session $session --out ($run+'/modules-startup.json')
if ($LASTEXITCODE -ne 0) { & $py -B $native control $session STOP; throw 'NO CUE: startup module inventory failed' }
# Assess the actual returned module inventory before truthfully recording these fields.
@{vortex_profile_confirmed=$true;no_competing_native_instrument=$true;pre_edit_modules_assessed=$true} |
  ConvertTo-Json | Set-Content -LiteralPath ($run+'/operator-confirmation.json') -Encoding utf8NoBOM
$monitor=Start-Process -FilePath $py -WindowStyle Hidden -PassThru -ArgumentList @('-B',$tool,'--lock',$lock,'--lock-sha',$lockSha,'monitor','--session',$session,'--run',$run) -RedirectStandardOutput ($run+'/monitor-stdout.txt') -RedirectStandardError ($run+'/monitor-stderr.txt')
```

Booleans are truthful recorded assessments, never a canned bypass; retain the actual
module review notes. Monitor revalidates admission, challenges a fresh32-hex nonce,
and requires ACK within15 seconds before exclusively writing `monitor-ready.json`.
Wait at most20 seconds for that file and require monitor still running, no STOP,
fresh health passing the command below. Failure means no cue and STOP/normal exit.

```powershell
& $py -B $native health $session
if ($LASTEXITCODE -ne 0) { & $py -B $native control $session STOP; throw 'Health failed' }
```

Monitor runs independently of chat/operator delay: target3 seconds, reject measured
successive sampling gaps over10 seconds, preserve15-second native health gate.
Every sample checks disk, worker failure, process creation identity, durable health
history/progress and immutable startup receipts. Native site/relay integrity, disk
and writer checks remain in the unchanged worker; faults stop admission immediately
when detected there, not deferred to external polls. External failure attempts STOP.
512MiB combined raw/journal observed size or20 minutes since monitor start triggers
STOP; these are sampled thresholds with bounded drain, not exact hard caps.
Use health + fresh phase challenge before each gameplay cue; preserve actual nonce
and matching fresh ACK. A new module inventory must be assessed before the next cue;
specific interference stops, ordinary overlays do not. No cue after monitor exit,
STOP, failed health, lost records/depth errors or stale ACK.

Before operator confirmation at startup **and before each later gameplay cue**,
acquire a fresh module inventory under a unique filename (substitute the phase name):

```powershell
$phase='load' # later: map, landing; each output filename is exclusive
& $py -B $environment --lock $lock --lock-sha $lockSha modules --session $session --out ($run+'/modules-'+$phase+'.json')
if ($LASTEXITCODE -ne 0) { & $py -B $native control $session STOP; throw 'NO CUE: module inventory failed' }
```

The qualified external helper consumes unchanged030 worker `modules-N.jsonl`
receipts using explicit lock05 cooperative provenance. It validates READY and
fresh health/PID creation identity before publishing a unique nonce, requires
ACK within15 seconds, validates complete bounded rows/required identities and
on-disk hashes, and requires stable inventory bytes/file set and final health.
It never calls external Toolhelp module enumeration. Parent timeout30 seconds
terminates only its own helper; any failure blocks cues and requires STOP/exit.
Retain output inventory digest/serial, pre-ACK serial, nonce and matching health
sequence, identity and limits with phase review notes.

This is cooperative evidence, not independent loader enumeration. Worker module
set and inventory scans are separate; an A→B→A race can retain inventory B with
cached set A until another change. ACK has no inventory serial/digest binding.
Fresh progress/stable files do not prove exact ACK-time loader membership; disk
hashes do not establish live bytes. Approval of this card explicitly accepts
that scoped method from the [qualified repair](module-inventory-fix.md).
Codex reviews actual pre-edit/emitted/phase differences, accepts ordinary Steam/
NVIDIA overlays and stops on demonstrated competing instrumentation. Keep monitor
running. After inventory and assessment, use a separate fresh phase challenge and
health immediately before each cue; the inventory ACK does not replace it.

An alive worker with zero Q means READY and installation passed, creation identity
matches, fresh nonce is durably acknowledged, monotonically progressing health is
fresh with zero failure/loss/depth counters, and event/active counters can be zero.
That is worker liveness, not proof an engine operation ran or that Q is unreachable.

## 4. Fixed operator sequence

Maximum total session25 minutes from launch, including startup and normal closure;
monitor20-minute bound is an additional limit. Codex tracks wall time and requests
STOP at the earlier bound, without extending it for dialogue. No arbitrary Q quota.
Record phase request/completion markers and actual operator testimony. Commands:

```powershell
& $py -B $native control $session mark --label Q030-mainmenu --note 'Operator confirms main menu responsive; baseline begins'
& $py -B $native control $session challenge
# Retain returned nonce; within15 seconds verify: health $session --nonce <returned-nonce>.
```

Apply the same challenge/health pattern before load, opening map and landing; at
completion use unique `Q030-loaded`, `Q030-map`, `Q030-landed`, `Q030-settled` markers
with actual labels/state. A pending ACK gives no cue. Baseline main menu30 seconds.

1. Operator identifies Save27 within3 minutes. Original directory:
   `C:/Users/User/Documents/My Games/Starfield/Saves/`; full filename
   `Save27_D6036588M417474696C61204B6972616C79_000252_20261012011118_4_0_4.sfs`;
   2343376 bytes; SHA256 `9615df728ab073bd24661fdc8abc65e0d0196b5abe532ab1b611bbe7ef7fc66c`.
   Verified operator-reported tuple: **Level4,10/12/26,12:11:18 PM,2h52m**.
   Visible character name and precise menu location are UNKNOWN until reported.
   Operator confirms intended character filter and unique row, recording actual text.
   Colliding/ambiguous labels mean do not load by list position; retire if unresolved
   within the bound. Adjacent Save28 is post-landing, not the baseline:
   `Save28_D6036588M417474696C61204B6972616C79_000258_20261012011827_4_0_4.sfs`,
   2017504 bytes; SHA256 `7360ce427b2a51aa94efb776d09dfaa30654c44ba08c60259b52c639cde2a35c`;
   reported **Kreet Landing Area,Level4,10/12/26,12:18:27 PM,2h58m**.
2. Load Save27 once, allow up to3 minutes. Operator confirms actual present location
   (prior provenance expects SOR-003/Kreet), responsive game, build closed, ordinary
   ship/map access and no combat/wanted/quest obstruction. Unexpected state stops;
   no combat/travel workaround. Hold closed UI60 seconds as load baseline.
3. Open Kreet planet map; within3 minutes select **one** unmarked accessible terrain
   point with normal landing enabled. Exclude ocean and existing landing/outpost/
   POI/quest markers. Operator confirms never used and distinct from old N1.
   If novelty/prior-N1 distinction or accessibility cannot be confirmed, record
   `NO_ELIGIBLE_CONFIRMED_SITE`, STOP/exit; no second scenario or Save28 fallback.
4. After machine clearance, operator lands once. Allow up to3 minutes for arrival,
   then60 seconds settlement with build closed. Record actual location/responsiveness,
   no event quota and no repeated landing. Unexpected scientific events are retained.
5. Finish after settlement and final markers/health at the earlier time bound.
   No manual save, quicksave or exit-save command is issued. Ordinary automatic
   save/exit rotation may occur naturally and is recorded separately; it does
   not excuse any changed protected manual input. Save27/28 originals and archive
   copies remain protected; no rename, overwrite, replacement or restore from backup.

## 5. STOP, drain, normal exit and removal

```powershell
& $py -B $native control $session STOP
```

Monitor observes retirement for at most30 seconds. No further gameplay cues. Q leases
already admitted can drain helper records after STOP; E-entry marker can precede a
rejected E diagnostic lease. STOP leaves resident inert hooks until normal exit;
never unload/unhook/patch/kill. Require no active leases, flushed/retired healthy
receipt and final inspector qualification. Missing retirement/failure means incident,
retain all prefixes, no healthy-zero classification. Operator exits normally within
2 minutes; allow ordinary sync/save rotation, then user disables/removes candidate
via Vortex. All five deployed package members must be absent at both canonical archive paths
and section2a mapped notice paths, SFSE/loader unchanged. Before the original
postflight command, verify all mapped notices absent and write the exclusive
`vortex-mapped-removal.json` receipt; failure blocks removal PASS. No deletion by Codex.
If normal exit is unavailable, stop automated activity and request narrowly scoped
recovery authority; no forced termination/retry. A crash may preserve useful complete
evidence; survival, scientific result and completeness are separately adjudicated.

Before postflight, after normal exit and settled files, seal originals to a new file:

```powershell
$seal=$run+'/original-evidence-manifest.json'
if (Test-Path -LiteralPath $seal) { throw 'Manifest already exists' }
$entries=Get-ChildItem -LiteralPath $session,$run -File -Recurse | Sort-Object FullName | ForEach-Object {
  @{path=$_.FullName;bytes=$_.Length;sha256=(Get-FileHash -LiteralPath $_.FullName -Algorithm SHA256).Hash.ToLowerInvariant()}
}
$entries | ConvertTo-Json -Depth 4 | Set-Content -LiteralPath $seal -Encoding utf8NoBOM
& $py -B runtime/native-oracle-030/inspect_events.py $session --output ($run+'/independent-inspection.json')
& $py -B runtime/native-oracle-030/branch_inspect.py $session --output ($run+'/independent-branches.json')
& $py -B $tool --lock $lock --lock-sha $lockSha postflight --session $session --run $run --out ($run+'/postflight')
```

The inspector itself independently decodes every raw record and checks its journal
link; there is no different schema parser or copied decoder. Compare both independent
outputs with postflight reports; reviewer additionally inspects originals. Seal again
under a different final-manifest filename once all new analysis outputs settle.

Postflight requires target/loader/debuggers absent, all pinned inputs unchanged,
candidate package fully removed, loader identities, save differences. No checkpoint pair is expected or claimed. It writes unchanged030 inspector and branch analysis outputs to new
paths. Retain SHA256/size manifest of **every original session and run file** before
decoding; never overwrite originals or prior outputs. Independently decode raw17768-byte
records with the unchanged decoder/inspector and compare journal references/hashes,
event order, invocation/thread/caller IDs, begin/end/unwind, loss, worker/retirement
receipts and unreferenced/truncated bytes. Independent reviewer checks primary data,
not only derived summaries. Freeze final evidence manifest after outputs settle.

## 6. Scientific adjudication and authority boundaries

Retain all Q kinds7/8/9, helpers13–19, actual E-entry20 and helper-unwind21, plus
E10/11/12, callback1/4/5, center2 and grid6/3 if naturally reached. Use exact
invocation/thread/parent/caller identity and native output; chain completeness and
missing operands gate classification. `branch_inspect.py` reports scoped static-CFG
reconstructions from complete healthy helper chains, not executed branch traces.
Contradictory sampled flags/rectangles remain evidence; snapshots are sequential,
non-atomic. Q return1 means caller continues scanning. Qworld+0x310 is packed8-byte
data, not a pointer; ctx[4] supplies a24-byte source pointee. Runtime VAs use the
new READY base, never prior ASLR base or serialized IDs. Keep early, incomplete,
unwind and contradictory chains separate; no inferred absence of E globally.

If qualifying E/callback/center/grid appear, compare only with **already frozen**
predictions and existing tolerances where independent identity/source/grid linkage
exists. Retain native-input replay separately from full saved-frame equivalence;
new destination with no frozen identity correspondence is explicitly unmatched.
Never refit predictions or claim full native equivalence from Q-only records.

Report separate statuses: scientific reachability/result; raw/chain completeness;
plugin worker health; operational cadence/sequence conformance; target survival;
protected inputs/removal. A healthy zero-Q negative requires admitted instrument,
fresh ACK/progress through documented completed landing, healthy drain and intact
evidence. It means **no Q observed in this single bounded action**, not unreachable
Q or a broken engine. No eligible site is a different outcome, not completed-landing
negative evidence. Faulted/incomplete capture is not healthy zero-Q.

After future approval Codex may run these file checks/control/monitor/decoder tasks
and issue cleared operator cues autonomously. DLL/hook/schema change, geographic
change, extra attempt, protected-save change, significant safety-gate change or
forced recovery requires fresh authority. Current assignment stops at reviewed preparation; no deployment or launch until
the maintainer approves this revised card. No staging, commit, push or publication.
