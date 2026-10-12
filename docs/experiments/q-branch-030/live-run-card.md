# Q030 single-session acquisition run card

**Historical lock02 procedure:** [offline inventory repair and prospective amendment](module-inventory-fix.md)
supersedes the external module acquisition dependency. Revised tools require an
explicit cooperative-source lock; old lock02 cannot silently switch provenance.
This amendment grants no new launch or retry. Original reviewed card below retained.

2026-10-12. **OFFLINE PREPARED — combined maintainer review/authorization required.**
This card proposes one controlled session; it does not authorize execution now.
After approval of this exact card and user Vortex deployment, passing mandatory
preflight authorizes the specified machine-side actions without another routine
approval. User controls launch, loading, map selection, landing, optional save creation
and normal exit. [Trigger basis](trigger-justification.md), [checks/review](procedure-qualification.md),
[tool contract](../../../research/q-branch-030-procedure/README.md).

## 1. Exact candidate and approval choices

Approve **one new Kreet landing from Save27**; default **no new manual saves**.
The optional pair means both fresh `Q030-before` and `Q030-after` manual slots,
explicitly included in the same approval. No Save25/26 controls, second landing,
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
|release-lock-02.json|16dad23320df928e63e0c7a1ffc9d00c5b65ae0008d4270f0a14173c3c164e5f|

ZIP/build are in `D:/Projects/starfield-outpost-research/.local-work/native-oracle-030/builds/qualification-02/`.
No rebuilding, config edits or substituted candidate. User installs/enables this ZIP
through Vortex only, confirms profile `Starfield - SFSE`, deploys and later removes it.
Archive has five members: `Data/SFSE/Plugins/SorNativePositionOracle.{dll,config}`
and `ResearchNotices/{PROJECT-LICENSE,READ-ME,SFSE-PluginAPI-LICENSE}.txt`.
Installed paths must be relative to game root without an extra nested Data directory.
Only this candidate DLL may be present in the SFSE Plugins folder for this run.
Inventory other load-order/config files and record Vortex active profile/mod state
read-only; no automatic installation/configuration correction. Steam and NVIDIA
overlays are accepted baseline modules; log them. Assess actual competing native
instrumentation/patches specifically; unknown names alone are not evidence of conflict.

## 2. Preflight while game/loader/debuggers are absent

Commands below are **future approved execution only**. Use repository-root PowerShell.
All paths are actual installation paths; `$session` is resolved from the new native
receipt, and optional `$newSave` is resolved from inventory/operator confirmation.

```powershell
Set-Location D:/Projects/starfield-outpost-research
$py='C:/Users/User/AppData/Local/Python/pythoncore-3.14-64/python.exe'
$tool='D:/Projects/starfield-outpost-research/research/q-branch-030-procedure/procedure.py'
$lock='D:/Projects/starfield-outpost-research/.local-work/q-branch-030-procedure/release-lock-02.json'
$lockSha='16dad23320df928e63e0c7a1ffc9d00c5b65ae0008d4270f0a14173c3c164e5f'
$native='D:/Projects/starfield-outpost-research/runtime/native-oracle-030/operate.py'
$run='D:/Projects/starfield-outpost-research/.local-work/q-branch-030-procedure/live-'+[DateTime]::UtcNow.ToString('yyyyMMddTHHmmssZ')+'-'+[guid]::NewGuid().ToString('N')
& $py -B $tool --lock $lock --lock-sha $lockSha audit --mode deployed --out $run
if ($LASTEXITCODE -ne 0) { throw 'NO LAUNCH: deployed audit failed' }
$environment='D:/Projects/starfield-outpost-research/research/q-branch-030-procedure/environment.py'
& $py -B $environment --lock $lock --lock-sha $lockSha files --out ($run+'/environment-before.json')
if ($LASTEXITCODE -ne 0) { throw 'NO LAUNCH: environment inventory failed' }
```

Audit verifies274 pinned files, ZIP member CRC/hash/membership, five installed
members, loader identities, required paths, save inventory, prior session names and
target/loader/debugger absence by process names. It does not open Starfield.
At least40,000,000,000 **caller-available** bytes on C and D is mandatory throughout;
failed queries fail. Pin drift or conflicts mean no launch; no bypass/repair within run.
Preserved inputs include Save25/26 originals/copies, Save27/28 originals/copies,
prior raw020 evidence, frozen predictions and unchanged030 sources/build receipts.
No active save is overwritten or renamed. Current offline inventory contains no
plugin DLL; this is not a future deployment attestation.

Environment inventory retains contents/hashes of
`C:/Users/User/AppData/Local/Starfield/{Plugins.txt,loadorder.txt}` and
`C:/Users/User/Documents/My Games/Starfield/{Starfield.ini,StarfieldCustom.ini,StarfieldPrefs.ini}`
locally, plus game-root/Data file names and sizes. ABSENT is explicit, unreadable
fails; absence is reviewed against operator-confirmed profile, not silently treated
as an empty readable file. Vortex profile display name remains operator-confirmed;
folder identifiers do not establish it. No configuration is changed.

## 3. Launch, bounded admission and independent worker clearance

Operator launches once via the confirmed Vortex SFSE profile and remains at main
menu. Record launch UTC. Allow at most135 seconds from launch for a fresh native
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
$phase='load' # later: map, landing, checkpoint-before, checkpoint-after
& $py -B $environment --lock $lock --lock-sha $lockSha modules --session $session --out ($run+'/modules-'+$phase+'.json')
if ($LASTEXITCODE -ne 0) { & $py -B $native control $session STOP; throw 'NO CUE: module inventory failed' }
```

The metadata-only helper checks PID/creation before/after Toolhelp loader snapshot
and hashes on-disk module files. It reads no target memory and uses no debugger;
it does not prove modules' live bytes unpatched. Parent bounds it to30 seconds,
terminating only the inventory helper on timeout. Query/hash/timeout failure gives
no cue and STOP. Codex assesses newly present/changed modules against pre-edit and
previous snapshots, records notes locally, accepts Steam/NVIDIA overlays and stops
on specific competing instrumentation. Keep the independent health monitor running;
perform fresh challenge/health **after** inventory/review and before cue.

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
3. Optional approved pair only: create one new manual slot `Q030-before`; do not
   overwrite anything. Inventory, identify actual new manual filename with operator,
   immediately protect its copy using commands below. Do not guess numbering.
4. Open Kreet planet map; within3 minutes select **one** unmarked accessible terrain
   point with normal landing enabled. Exclude ocean and existing landing/outpost/
   POI/quest markers. Operator confirms never used and distinct from old N1.
   If novelty/prior-N1 distinction or accessibility cannot be confirmed, record
   `NO_ELIGIBLE_CONFIRMED_SITE`, STOP/exit; no second scenario or Save28 fallback.
5. After machine clearance, operator lands once. Allow up to3 minutes for arrival,
   then60 seconds settlement with build closed. Record actual location/responsiveness,
   no event quota and no repeated landing. Unexpected scientific events are retained.
6. Optional approved pair only: create new `Q030-after` manual slot and protected copy.
   Both pair receipts are required if that option was approved; an incomplete pair
   is reported incomplete, never silently waived. Finish at the earlier time bound.

Optional copy commands (future only, once per label):

```powershell
& $py -B $tool --lock $lock --lock-sha $lockSha inventory --out ($run+'/after-before-save-inventory.json')
# $newSave is the actual full new manual-save path confirmed by operator and inventory.
& $py -B $tool --lock $lock --lock-sha $lockSha checkpoint --run $run --source $newSave --label Q030-before
# After landing repeat inventory under a NEW name, then checkpoint --label Q030-after.
```

Copy command rejects pre-existing saves, creates an exclusive ignored copy and
rehashes both. No original rename/delete/replacement. Save27/28 archive copies are
already in `.local-work/q-to-e/saved-correspondence-04/`. Record autosave/exit rotation
separately; rotation does not excuse a changed protected manual save.

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
via Vortex. All five deployed package members must be absent, SFSE/loader unchanged.
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
candidate package fully removed, loader identities, save differences and checkpoint
copy hashes. It writes unchanged030 inspector and branch analysis outputs to new
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
forced recovery requires fresh authority. Current assignment stops at combined review.
