# Prospective integrated live run card â€” observer 0.5.0

2026-10-13, Australia/Sydney. SOR-EXP-0031 / SOR-EV-0039.
**DELIVERED FOR REVIEW, NOT EXECUTED OR LIVE-AUTHORIZED.**
[Original brief](../../implementation-briefs/CODEX_BRIEF_SOR_ship_relocation_native_grid_observer_integrated.md),
[qualification and exact binary identities](report.md), [independent review](review.md).
The maintainer must review these together once, deploy the exact ZIP through
Vortex and authorize this defined experiment. Then Codex may preflight and launch
this exact procedure without another routine approval if mandatory checks pass.
Maintainer controls all gameplay. No console, synthetic trigger, outpost build,
settings change, debugger, new plugin, additional trip/session or expanded hooks.

## Exact candidate and runtime admission

|Artifact|Exact local path / SHA256|
|---|---|
|DLL|.local-work/native-oracle-050/builds/qualification-03/SorNativePositionOracle.dll / b75b7889966a76e84059349acea869482b027f6e3afce70e53e2f5d2d5a483f0|
|Vortex ZIP|.local-work/native-oracle-050/builds/qualification-03/SorNativePositionOracle-0.5.0.zip / 7741c88dd69fca63773e42f291334df4d251dabdaf5dee1a5dcf3b92ecd0f15d|
|Build manifest|.local-work/native-oracle-050/builds/qualification-03/build.json / d7b1bf845bbdd770f1088e8d59c51409d24312fe8fdadac4b7857b0d7eaca501|

Only Data/SFSE/Plugins/SorNativePositionOracle.dll is required in deployed Plugins.
No TXT, README, config or manifest is required beside it. Microsoft /MD runtime
prerequisites are installed system libraries pinned in build.json, never bundled.
ZIP notices remain package review/distribution material. Native 21-site transaction,
19RX relays and exact 32-byte code guards must pass at runtime. Standard Steam and
NVIDIA overlays are accepted; assess unfamiliar modules for demonstrated conflict,
not a blanket allowlist. Competing native SOR observers/debuggers/instrumentation,
wrong loaded identity or an owned-site conflict prevent admission. No live waiver
or unreviewed patch change is allowed.

## Save selection supplied in advance

Human-supplied screenshot20261013121245_1.jpg is a visual reference, not binary
menu-metadata extraction. Its SHA256 is in sources.csv. Character name **Attila
Kiraly** comes from the maintainer's statement, not visible pixels. Displayed UI
values below are local values, not a filename-time conversion. Ignore [C].

|Research identifier|Visible label|Displayed date|Displayed time|Level|Screenshot order|
|---|---|---|---|---|---|
|Exit save|EXIT SAVE Kreet - Outpost|10/13/26|10:18:26 AM|4|1|
|Save28|Kreet - Landing Area|10/12/26|12:18:28 PM|4|2|
|Save27|Kreet - Outpost|10/12/26|12:11:19 PM|4|3|
|Save26|Kreet - Outpost|10/10/26|12:24:53 PM|4|4|
|**Save25**|**Kreet - Outpost**|**10/9/26**|**9:22:22 PM**|**4**|5|
|Save3|Kreet - Kreet|10/6/26|12:34:27 PM|3|6|
|Autosave|AUTO SAVE Kreet - Landing Area|10/6/26|12:30:18 PM|3|7|

Screenshot order and [C] are dynamic, never durable IDs. ExitSave rotation cannot
change which timestamp/label is instructed. Save25 physical input:
C:/Users/User/Documents/My Games/Starfield/Saves/Save25_D6036588M417474696C61204B6972616C79_000231_20261009102224_4_0_4.sfs
SHA256 d4df86bc01c2105933fe856a1be5ebbe0c3fc78a4d67fe1a790e18129faf75f5.
The protected archive and Save3/25/26/27/28, old observers/raw/frozen inputs are
machine-side preservation responsibilities; do not ask the user to certify a
UI-to-file mapping the menu cannot expose. No preparatory Save29. Save25 does
not contain later LZ2/LZ3/LZ4 markers as guaranteed selectable origins.

Before the action, prompt once:

> **Load Attila Kiraly Save25 â€” Kreet - Outpost, dated 10/9/26 at 9:22:22 PM (Level 4).**

Record this instruction, action acknowledgement and any actual mismatch. Do not
then ask the maintainer to repeat the character/label/timestamp/save number.
If absent, materially conflicting, ambiguous duplicate or wrong character filter,
ask one targeted question or request a fresh screenshot; never guess by ordinal.
Menu parsing (including character/type/place/level/time/playtime/collisions) is a
separate near-term backlog task and is not a prerequisite for this run.

## Machine preflight after combined approval and Vortex deployment

Run commands in D:/Projects/starfield-outpost-research. Use fresh exclusive names.
Variables below are operator conveniences, not permission to execute this card now.

```powershell
$py = 'C:/Users/User/AppData/Local/Python/pythoncore-3.14-64/python.exe'
$build = '.local-work/native-oracle-050/builds/qualification-03'
$game = 'C:/Program Files (x86)/Steam/steamapps/common/Starfield'
$run = '.local-work/ship-relocation-050/live-' + (Get-Date).ToUniversalTime().ToString('yyyyMMddTHHmmssfffZ')
New-Item -ItemType Directory -Path $run -ErrorAction Stop | Out-Null
& $py -B runtime/native-oracle-050/operate.py preflight --build $build --deployed --receipt preflight-UNIQUE
if ($LASTEXITCODE -ne 0) { throw 'Preflight failed: inspect receipt before launch' }
Get-ChildItem '.local-work/native-oracle-live' -Directory | Select-Object Name | ConvertTo-Json | Set-Content "$run/sessions-before.json"
Get-ChildItem 'C:/Users/User/Documents/My Games/Starfield/Saves' -File | ForEach-Object {
  [pscustomobject]@{path=$_.FullName;length=$_.Length;mtime_utc=$_.LastWriteTimeUtc.ToString('o');sha256=(Get-FileHash -LiteralPath $_.FullName -Algorithm SHA256).Hash}
} | ConvertTo-Json -Depth 4 | Set-Content "$run/saves-before.json"
```

Verify the reviewed build.json hash before using its pins. Preflight verifies
Steam Starfield 1.16.244.0 SHA256 7e9adb1414a8e1b325e5e1f097b9b17b78deb7eebeda37a333351a43a60f9d28;
SFSE runtime 28c5bda41d9959c885efcb6e889de69e92767c80a1a66842d711d215f722f82b;
SFSE loader 16916c2ec47e31774e3d550609a1844fcb368b03060c03511891564b7f5f7526;
effective deployed DLL, package, source/dependency and protected-file hashes,
no target/loader/debugger process, and C:/D: caller-available free space each at
least 40,000,000,000 bytes plus write reserve. Failure blocks launch; do not replace
pins, overwrite originals or regenerate expectations. Record maintainer approval
reference, active Vortex profile and actual competing-plugin/instrument assessment
in $run/authorization-and-environment.md. Effective DLL hash, not Vortex's label,
is decisive. Preflight process names are limited evidence; runtime guards and
module inventory remain mandatory. Record fresh evidence-root inventory and
forbid reuse of any prior session path.

## Launch, health and operator sequence

After all preflights and existing approval, Codex may launch the approved loader:

```powershell
Start-Process -FilePath "$game/sfse_loader.exe" -WorkingDirectory $game
```

Record the actual launch method/time. Wait at menu before loading. Locate the
fresh session-* under .local-work/native-oracle-live, absent from sessions-before.
Set $session to its exact absolute path. Verify ready.json/admission.json/
patches.json against the reviewed version0.5.0/schema5/event_size17768, DLL/game/
SFSE identity, current PID+creation time, grid=true/center=true, all 21 edits and 19
relays. Assess modules-pre-edit.jsonl and latest modules-N.jsonl. Runtime-native
identity checks are cooperative, non-atomic evidence, not blanket external proof.
No READY deadline. A waiting-sole-thread receipt means no edits have been admitted;
keep the operator updated. Operator STOP can retire this pre-READY wait using the
same control STOP command below. Actual not-ready/failure requires inspection,
normal operator-controlled exit and no automatic retry.

Challenge worker health before load and before each travel action:

```powershell
& $py -B runtime/native-oracle-050/operate.py control $session challenge
# Use exactly the returned nonce; wait for its durable ACK, without a response deadline.
& $py -B runtime/native-oracle-050/operate.py health $session --nonce RETURNED_NONCE
```

A fresh valid response and live PID/creation identity are mandatory for proceeding.
Stale/missing ACK is unresolved health: update the operator, await/rechallenge and
inspect receipts. A historical heartbeat gap or delayed monitoring poll alone is
not termination. Actual failure.json, lost/depth errors, guard/identity mismatch,
failed disk protection or operator STOP closes capture. Poll routinely while
working (roughly every second when practical), record delays, never create a
hard cadence, session clock, event quota, 2 GiB cap or operator-response deadline.
No-hit healthy worker is scientifically useful reachability evidence.

For each step, mark an exclusive before and after label; notes distinguish actual
operator testimony from native fields. Example:

```powershell
& $py -B runtime/native-oracle-050/operate.py control $session mark --label control-start --note 'Actual operator state and instruction'
```

1. Give the single advance Save25 instruction above. Record acknowledgement and
   actual SOR-003/site/player/ship state. If ship-at-LZ1 near SOR-002 is supported,
   record it; otherwise record actual state and consult on material mismatch.
   Do not assume the control observation is guaranteed.
2. Mark control-003-to-002 before/after normal fast travel, then control-002-to-003.
   Maintainer controls both actions. Record visible ship/player locations, whether
   ship stayed or moved, and any fauna/combat/loading interference. No build-mode
   trigger or extra route is required. Native misses remain misses.
3. Instruct one previously unvisited, accessible **Kreet** landing location
   LZ-new through normal gameplay. Mark lz-new-selection/arrival, record requested
   destination, actual landing/player/ship positions and acquisition. The action
   may itself yield descriptor/grid evidence. Do not require old LZ markers or
   distant-system travel, and do not assert creation from visible relocation.
4. Optional one new manual checkpoint **after landing at LZ-new**, only if useful
   for repeatability/saved-state comparison and explicitly coordinated with the
   maintainer during the approved sequence. Agree a new slot/name/receipt; never
   overwrite a protected save. Record physical inventory/hash and fresh screenshot
   if needed. Material scope/slot uncertainty requires consultation. Omit otherwise.
5. Mark lz-new-to-003 before/after ordinary fast travel to SOR-003. Record stays/
   relocates/newly selected natural marker as actually observed; LZ3â‰ˆ450m is prior
   human testimony, not a promised result or calibrated native distance. Record
   native request/decision/selected marker/fresh source/grid and separate Workshop
   events if naturally reached. No extra trip to manufacture hits.
6. Record sequence completion or operator STOP and begin retirement. Maintain
   evidence first: no premature exit before admitted records drain when healthy.
   No automatic additional travel, session, outpost, plugin or hook expansion.

## STOP, normal exit, postflight and sealing

```powershell
& $py -B runtime/native-oracle-050/operate.py control $session STOP
```

This also works before READY with the owned waiting/admission identity receipt
and remains available below the capture disk floor. STOP closes admission,
drains accepted callbacks/queue and produces retired.json if evidence integrity
allows. Do not dynamically unhook/unload or force game termination. Await clean
retirement without an arbitrary deadline. If a callback/worker is truly failed,
preserve flushed records and failure receipts and consult the operator on normal
exit/recovery. A healthy delay alone does not justify quitting. Capture completeness,
instrumentation integrity and target survival are separate dimensions.

After retirement, user exits normally. Record actual process outcome and Steam
sync as observed. Only after game exit, remove/disable the observer through Vortex;
verify effective deployed DLL absent and retained archive unchanged. Leave normal
Steam/NVIDIA configuration alone. Run file/process postflight and save inventory:

```powershell
$postflightName = 'postflight-' + (Get-Date).ToUniversalTime().ToString('yyyyMMddTHHmmssfffZ')
& $py -B runtime/native-oracle-050/operate.py preflight --build $build --postflight --receipt $postflightName
$postflightFile = ".local-work/native-oracle-050/operations/$postflightName.json"
Get-ChildItem 'C:/Users/User/Documents/My Games/Starfield/Saves' -File | ForEach-Object {
  [pscustomobject]@{path=$_.FullName;length=$_.Length;mtime_utc=$_.LastWriteTimeUtc.ToString('o');sha256=(Get-FileHash -LiteralPath $_.FullName -Algorithm SHA256).Hash}
} | ConvertTo-Json -Depth 4 | Set-Content "$run/saves-after.json"
& $py -B runtime/native-oracle-050/inspect_capture.py $session --output "$run/analysis.json"
$sealInputs = @(Get-ChildItem -LiteralPath $session -File) + @(Get-ChildItem -LiteralPath $run -File) + @(Get-Item -LiteralPath $postflightFile)
$sealInputs | ForEach-Object {
  [pscustomobject]@{path=$_.FullName;length=$_.Length;sha256=(Get-FileHash -LiteralPath $_.FullName -Algorithm SHA256).Hash}
} | ConvertTo-Json -Depth 4 | Set-Content "$run/sealed-session-files.json"
(Get-FileHash -LiteralPath "$run/sealed-session-files.json" -Algorithm SHA256).Hash | Set-Content "$run/sealed-inventory.sha256"
```

Compare save inventories: protected inputs must match; list new manual checkpoint
and incidental autosave/ExitSave rotation separately, never restore over an
original automatically. Postflight failure requires preservation/recovery decision,
not a falsified PASS. Raw bytes/receipts remain local/untracked. Preserve failed
attempts and mismatches. Parser verifies journal/record hashes/extents/sequences,
normal scopes/ancestry, health/terminal counters, lost/incomplete/raw-tail evidence.
Sealing must include SHA256/size of every raw/journal/health/module/control/operator/
retirement/failure file and postflight receipt; hash the sealed inventory itself.
No moving/deleting originals or network upload.

Scientific report: classify deepest observed route, generic terrain-grid result,
ship-marker identity, ordinary Workshop center/grid and full durable equivalence
separately. Compare unchanged 23 frozen predictions only when actual ordinary
base 002C60E9/concrete Workshop identity, body/site and loaded-frame provenance are
independently qualified. SOR-002=f1517de43e171745; SOR-003=0efca066ee4c7b9b are
Workshop identifier bytes, not pointers/handles/FormIDs. Same numbers/time/thread
alone do not join a saved sample. Nonzero/carry coverage is encountered evidence,
not an event target; absent cases remain NOT TESTED. Full Workshop equivalence,
marker creation and applied ship assignment are never inferred by this helper.
A post-capture crash can leave useful complete flushed records but cannot be
called orderly target exit; a pre-evidence crash is not acquisition success.
