# Proposed integrated run card: observer0.4.0 / Save28 → SOR-003

2026-10-12; SOR-EXP-0031 / SOR-EV-0039. **PROPOSED, not live-authorized.**
Joint maintainer approval must name this complete card and the exact candidate
below. Current assignment authorizes offline preparation only. No deployment,
launch, save creation or instrumentation has occurred. After joint approval and
Vortex deployment, passing these checks permits Codex to begin this already
approved sequence without another routine review. Changed build/hooks/scenario
or a genuine safety waiver needs separate approval.

[Scientific contract and acceptance matrix](report.md), [review](review.md),
[tool contract](../../../research/existing-reference-grid/README.md).
Repository root `D:\Projects\starfield-outpost-research`; commands run there in
PowerShell using `C:/Users/User/AppData/Local/Python/pythoncore-3.14-64/python.exe`
(abbreviated `$py` below). Replace only session/run names with fresh exclusive
names, never replace pinned inputs. No command below launches or deploys the game.

## Approved candidate identity for joint review

| Artifact | Absolute path / SHA-256 |
|---|---|
|ZIP|`D:\Projects\starfield-outpost-research\.local-work\native-oracle-040\builds\qualification-08\SorNativePositionOracle-0.4.0.zip` / `7cb69d4a968c60cf7b99eb8faae11ff93bd79ac2db47b8390c8dec221624fd2f`|
|DLL|same directory `SorNativePositionOracle.dll` / `ca25f05189ff831c84b2eaaf7e139a873578e64aa8a17b349f9882967055e7c3`|
|Build receipt|same directory `build.json` / `918625105e6b2006abcf97109f7130264b0914aa1584ed27f48e28d326567ecd`|
|Schema|`D:\Projects\starfield-outpost-research\runtime\native-oracle-040\schema.md` / `e71685c1a803e2694801e3442cfad795e6fc324fd2243afad4ba9c4f9405194c`|
|Game|`C:\Program Files (x86)\Steam\steamapps\common\Starfield\Starfield.exe` / `7e9adb1414a8e1b325e5e1f097b9b17b78deb7eebeda37a333351a43a60f9d28`|
|SFSE runtime1.16.244|game root `sfse_1_16_244.dll` / `28c5bda41d9959c885efcb6e889de69e92767c80a1a66842d711d215f722f82b`|
|SFSE loader|game root `sfse_loader.exe` / `16916c2ec47e31774e3d550609a1844fcb368b03060c03511891564b7f5f7526`|
|Frozen predictions|`D:\Projects\starfield-outpost-research\docs\experiments\engine-oracle\predictions.json` / `a8a7402697ed866a3410d4bd58796de513c7ca11f89e770a80deb5a8651a0487`|

Release-lock exact identity is recorded below after offline package preparation.
It pins historical310 inputs, new sources, call bytes, archive members and logs.
Verify its SHA before every command; no automatic regeneration on mismatch.

## Protected sample and operator identification

Only input is
`C:\Users\User\Documents\My Games\Starfield\Saves\Save28_D6036588M417474696C61204B6972616C79_000258_20261012011827_4_0_4.sfs`,
2017504 bytes, SHA-256
`7360ce427b2a51aa94efb776d09dfaa30654c44ba08c60259b52c639cde2a35c`.
Protected archive is the same basename under
`D:\Projects\starfield-outpost-research\.local-work\q-to-e\saved-correspondence-04\`,
same hash. Save25/26/27 and their archives, previous observers/captures and frozen
inputs are also pinned; no protected original is overwritten or normalized.

Expected lineage: Attila Kiraly, character tokenD6036588, level4, Kreet,
post-new-landing Save28, filename timestamp20261012011827 and sequence000258.
Timestamp encoding is recorded literally, not assumed to be displayed local time.
SOR-003 was relocated in this lineage. Exact UI wording/location must be
transcribed by the user; do not invent a menu label or interpret ordinal28 as
identity. Historical similarly named Save27/28 from other characters, including
level298, are excluded. If menu metadata cannot distinguish the file, stop for
user confirmation with file/path metadata; do not guess. Save-menu parsing is
separate backlog, not silently added here.

## Preflight and handshakes

1. After joint approval, user imports/enables this ZIP through **Vortex only**,
   confirms active profile and no older SOR observer enabled. Codex never copies
   the DLL manually or changes launch, Steam/NVIDIA, game/plugin/save settings.
   Required effective payload is exactly the hash-matched DLL at
   `C:\Program Files (x86)\Steam\steamapps\common\Starfield\Data\SFSE\Plugins\SorNativePositionOracle.dll`.
   README/config/manifests/notices absent or different beside it are noncritical;
   no optional-text waiver. Archive and DLL-member hashes still must match.
2. Codex checks both-drive free space≥40,000,000,000, all lock pins, archive and
   installed DLL, loader/runtime, no running target/loader/debugger, inventory of
   plugin DLLs, save inventory and prior session names. Use a fresh run directory:

   ```powershell
   $py = 'C:/Users/User/AppData/Local/Python/pythoncore-3.14-64/python.exe'
   $lock = '.local-work/existing-reference-grid/release-lock-05.json'
   # $locksha is the exact reviewed value printed in the lock identity below.
   & $py research/existing-reference-grid/procedure.py --lock $lock --lock-sha $locksha audit --mode deployed --out .local-work/existing-reference-grid/live-01
   ```

3. Before user launches, durably record in `live-01/operator-confirmation.json`:
   `vortex_profile_confirmed`, `no_competing_native_instrument`,
   `pre_edit_modules_assessed` (last value stays false until actual inventory
   assessment), joint approval reference, exact preload menu/file identification,
   character/level/Kreet, and intended launch method. User alone launches the
   approved SFSE setup and later transcribes the **actual** launch method. Codex
   does not infer it from module presence. Wait at menu; no load/travel yet.
4. Codex identifies the new `session-*` directory under
   `D:\Projects\starfield-outpost-research\.local-work\native-oracle-live`.
   It must be absent from preflight inventory and match PID/creation time/version4
   schema4,17768-byte events, exact DLL/game/SFSE, grid=true/center=false.
   READY requires admission originals, sole-thread startup transaction, all15
   guarded CALL edits and15 RX relays targeting the approved loaded DLL. Retain
   admission/patch/module receipts. Native sole-thread wait is capped120s;
   external READY deadline is150s from the user's recorded launch time.
   Missing READY or startup refusal stops: no load, no write to any old session,
   no forced recovery. User controls normal exit. After fresh READY, complete
   admission/module assessment and start the monitor within2min; otherwise STOP
   only the verified fresh owned session and request normal user-controlled exit.
5. Assess cooperative `modules-pre-edit.jsonl`: Windows/Steam/NVIDIA overlays
   are normal and accepted. Unfamiliar/unreadable nonessential modules require
   documented assessment, not categorical rejection. Reject demonstrated competing
   instrumentation, changed owned sites or mandatory module identity failures.
   Cooperative inventory is non-atomic, not external completeness proof. Record
   assessment and set the three confirmation booleans true only when satisfied.
   Before load, obtain the qualified last complete worker inventory plus fresh
   nonce ACK with the bounded helper, and assess its module differences too:

   ```powershell
   & $py research/existing-reference-grid/environment.py --lock $lock --lock-sha $locksha modules --session $session --out .local-work/existing-reference-grid/live-01/modules-before-load.json
   ```

   This helper terminates only its own inventory subprocess after30s on failure;
   it never terminates the game. The ACK does not contain an inventory digest or
   serial; separate scans can race, including A-B-A module changes. Treat this
   as cooperative inventory plus worker progress, not exact ACK-time membership.
6. Codex runs `admit`, then starts `monitor` in a continuing tool process using
   the actual fresh absolute `$session` path and fresh run directory:

   ```powershell
   & $py research/existing-reference-grid/procedure.py --lock $lock --lock-sha $locksha admit --session $session --run .local-work/existing-reference-grid/live-01
   & $py research/existing-reference-grid/procedure.py --lock $lock --lock-sha $locksha monitor --session $session --run .local-work/existing-reference-grid/live-01
   ```

   Monitor must remain running while gameplay proceeds. Codex announces the
   durably written `monitor-ready.json` only after a new unpredictable nonce ACK
   within15s. READY alone is not this health handshake. If no fresh ACK, no load.

## Single permitted gameplay sequence and monitoring

User confirms exact pre-load identity/label and actual launch method, loads the
verified Save28, then confirms actual character/level/Kreet scene and intended
SOR-003 marker using ordinary UI. If identity/scene is ambiguous, unsafe or
unexpected, pause the operation and stop acquisition; no console correction.
User selects/travels to SOR-003 once by ordinary interface and confirms the
selected label and arrival/failed travel. No SOR-002, extra landing, construction,
new scenario, synthetic native call or manual save is authorized. Record action
times/labels separately from native assertions. A no-hit run still completes
the permitted sequence; do not repeat for a desired result.

Codex owns receipt monitoring and evidence, user owns all game interaction.
Nominal sampling every3s allows the prior2.793s observed gap. Actual monotonic
gap>10s, worker heartbeat age>15s, initial ACK>15s, identity/patch receipt change,
failure/loss/integrity error, either drive below40GB, output≥2GiB or elapsed>20min
requests STOP. The20min timer starts when monitoring starts; launch/READY/
admission have the separate finite bounds above. No load before fresh monitor ACK.
These are operational bounds, not event/hit quotas. No requirement
to get a minimum number of grid events. Monitoring log flushes each sample.
An unpaired path or optional scientific unreadable field is not a reason to keep
travelling or terminate an otherwise healthy acquisition.

After travel, while the monitor remains running, Codex obtains another bounded
inventory and records differences/assessment against the pre-load inventory:

```powershell
& $py research/existing-reference-grid/environment.py --lock $lock --lock-sha $locksha modules --session $session --out .local-work/existing-reference-grid/live-01/modules-after-travel.json
```

A changed noncritical module set is recorded, not automatically rejected. A
demonstrated instrumentation conflict or required identity failure requests STOP.

After the action/arrival confirmation, Codex requests STOP with the existing helper:

```powershell
& $py runtime/native-oracle-040/operate.py control $session STOP
```

No STOP is written to an old/protected session. Monitor also requests STOP on
its failure path. Wait≤30s for retired receipt/drain; no arbitrary wait for hits.
CALL edits and relays remain inert/resident until normal process exit, not restored.
If target stalls/crashes, preserve persisted bytes and report target survival
separately; no debugger, process termination, memory edits, exception suppression
or recovery relaunch. User controls any subsequent recovery, outside this card.

## Reconciliation and postflight

Use [report's per-invocation matrix](report.md#scientific-coverage-and-reconciliation)
and schema4 inspector. For each route list selection producer/thread ancestry,
selected binding, saved-site association status, direct/search/fallback path,
eligibility, chosen native ref/base/parent/world/body, source angles and44-byte
fresh descriptor, floorXY/landscape fields, grid before/after, route residual and
result. Pair by stable invocation/thread/sequence, never nearest timestamp alone.
Classify deepest observed transition and missing/unwound/orphan stages.

Replay captured inputs against frozen implementation with original numeric bits;
record component agreement or disagreement. Separately list all23 untouched
predictions with applicability/identity/frame/compensation status and outcome.
Wrong frame/ref, absent grid and disagreement are useful results. A stable buffer,
center coincidence or component `scientific_complete` cannot establish selected
binding, saved load-map or full native equivalence. Preserve `saved_join` unknown
unless direct load correspondence is independently demonstrated.

User exits normally after STOP/drain, then disables/removes candidate via Vortex.
No manual checkpoint/save. Inventory incidental autosave/ExitSave additions or
rotations; never overwrite or delete protected originals. Codex runs:

```powershell
& $py research/existing-reference-grid/procedure.py --lock $lock --lock-sha $locksha postflight --session $session --run .local-work/existing-reference-grid/live-01 --out .local-work/existing-reference-grid/postflight-01
```

Postflight requires process absence, exact historical/source/save pins, candidate
DLL removal and loader identity; optional neighbor texts need no removal proof.
Retain session raw/journal, health/ACK/monitor, startup/retirement, module inventories,
operator testimony, hash/save differences and decoder report locally. Incomplete
last JSONL/raw tails may be recovered explicitly; a corrupt complete record fails.
Do not alter originals to make a partial run complete. Capture integrity,
scientific coverage, retirement and target survival each receive separate outcomes.
No upload/commit/push or follow-on run is authorized; return for critical review.

## Frozen release lock

`D:\Projects\starfield-outpost-research\.local-work\existing-reference-grid\release-lock-05.json`
SHA-256 `060db14e0000146ed13537c6b59b688eff238132819b0e42f24a94588f69ab6b`.
Set `$locksha` to this literal value. The lock has280 canonical absolute pins,
covering all310 historical entries (historical aliases collapse) plus new inputs.

## Installed runtime prerequisites, not deployed package files

Established /MD linkage uses the already installed Microsoft runtime and Windows
UCRT API-set resolution. No CRT DLL is bundled, downloaded or installed by this
card. File pins are checked in preflight and loaded cooperative inventory requires
these exact hashes/READ_OK. A missing/different prerequisite stops; do not repair
or install it automatically. Optional neighbor text still has no bearing on preflight.

| Installed path | SHA-256 |
|---|---|
|`C:\Windows\System32\msvcp140.dll`|`7c26614e1d733892c2deac7e245ce115504b1d80592dd0a01b08e3e5a55f89ca`|
|`C:\Windows\System32\vcruntime140.dll`|`d1f4225df2cd877dbf130d5668a021dce3f94118455ff5ec952061c30afc9ce7`|
|`C:\Windows\System32\vcruntime140_1.dll`|`a7146c08f89fe5b04541ab507cdb59ff7b44534d4ba3c668a426c6450a03434e`|
|`C:\Windows\System32\ucrtbase.dll`|`3c60056371f82e4744185b6f2fa0c69042b1e78804685944132974dd13f3b6d9`|
