# Exact conditional live run card — SorNativePositionOracle0.1.0

SOR-EXP-0031. **PROPOSED; Phase B joint review and explicit live authorization
required. No Phase A launch or deployment.** This card and implementation are
reviewed together. Once the user approves this exact package/card, user deploys
through Vortex; Codex runs the checks below and, if all mandatory gates pass,
continues to the approved launch/sequence without a second routine approval.
Any failed gate stops that action; no weaker gate, rebuilt binary, new hook,
different save/site or configuration workaround is authorized.

## Exact instrument and inputs

Package: `.local-work/native-oracle/builds/final-review-04/SorNativePositionOracle-0.1.0.zip`.
The [review and hash ledger](review.md) names its exact SHA256, DLL/config hashes
and final qualification. Version0.1.0 is a new SFSE component, not an external
adapter continuation. Install paths are precisely
`Data/SFSE/Plugins/SorNativePositionOracle.dll` and `.config`; ResearchNotices
contains project/header notices. Both channels enabled. Keep prior0.1.1 artifacts;
user disables conflicting/old observers through Vortex, never Codex copying files.

Game1.16.244.0 SHA256
`7e9adb1414a8e1b325e5e1f097b9b17b78deb7eebeda37a333351a43a60f9d28`;
SFSE DLL0.2.21 hash
`28c5bda41d9959c885efcb6e889de69e92767c80a1a66842d711d215f722f82b`;
loader hash`16916c2ec47e31774e3d550609a1844fcb368b03060c03511891564b7f5f7526`.
Observed file versions/hashes are build-specific; no compatibility transfer.

Protected originals in `C:/Users/User/Documents/My Games/Starfield/Saves/`:

| Save | Exact filename and SHA256 |
|---|---|
| Save25 | `Save25_D6036588M417474696C61204B6972616C79_000231_20261009102224_4_0_4.sfs`; `d4df86bc01c2105933fe856a1be5ebbe0c3fc78a4d67fe1a790e18129faf75f5` |
| Save26 | `Save26_D6036588M417474696C61204B6972616C79_000241_20261010012454_4_0_4.sfs`; `2b4781e75226f2ff7c6aa47470fb47ff179c1754461aa208c46716d7c3935104` |

Immutable archive paths/hashes are pinned by baseline.json and preflight; do not
copy over either archive/original or an active playthrough. This card loads the
hash-verified existing entries read-only; no manual save, scripted save, overwrite,
construction, placement, relocation, deletion, console command, setting change,
new landing site, arbitrary POI, Save52 or fresh holdout is included. New incidental
autosave/exit saves may occur naturally: record their separate provenance, retain
originals and stop if any protected input changes. Do not change autosave settings
or delete incidental files as an improvised workaround.

## Phase C preflight, then authorized launch

Commands run in `D:/Projects/starfield-outpost-research` using existing CPython:

```powershell
$oraclePython = 'C:/Users/User/AppData/Local/Python/pythoncore-3.14-64/python.exe'
$oracleBuild = 'D:/Projects/starfield-outpost-research/.local-work/native-oracle/builds/final-review-04'
& $oraclePython -B runtime/native-oracle/operate.py preflight --build $oracleBuild --deployed --receipt live-preflight-01
```

Receipt must exit0/PASS and all checks be true: package/deployed DLL/config bytes,
game/SFSE/loader, source snapshot, protected originals/archives/frozen fixtures,
no Starfield/loader/debugger processes, only the reviewed SFSE plugin DLL,
caller-available40,000,000,000 bytes on both C:/D: with writer reserve. Fresh receipt
name if a new separately reviewed attempt is needed; never overwrite a failure.
Script writes only ignored local receipts and cannot install or launch anything.
Check `git status --short` against the reviewed manifest; critical source/pin drift
fails, not grounds for automatic rebuilding. User attests the Vortex Starfield/SFSE
profile has exactly the reviewed observer and SFSE environment, no other SFSE
plugin, code hook/injector or competing launch; preserve the attestation locally.
Do not alter configuration to force sole-thread startup. Vortex deployment belongs
to the user and is not implied by a successful offline preflight.

After approval and mandatory PASS only, launch the pinned loader once:

```powershell
& 'C:/Program Files (x86)/Steam/steamapps/common/Starfield/sfse_loader.exe'
```

No external debugger/attachment. User remains at main menu until startup READY.
Instrument can delay pre-main startup up to120 seconds while waiting for a sole
process thread. It never suspends threads or patches concurrently. This condition
is untested in Starfield. If it cannot hold, startup emits NOT_READY and installs
no hooks; retain the failure and exit normally, with no retry or forced workaround.

Find the unique new `session-<PID>-<tick>` beneath
`D:/Projects/starfield-outpost-research/.local-work/native-oracle-live/`.
Verify its READY component0.1.0, PID/process-creation FILETIME against actual
Starfield metadata, game/SFSE/DLL hashes against build.json, event_size17,768,
QPC frequency, both channels true, startup wait and UTC. Require patches.json
with four installed guards (CALL RVAsAD0C36/AD0D36; vtable RVAs4B916F0/F8),
runtime VA=READY base+RVA, all original/installed hashes, and startup module
inventory containing those exact game/SFSE/plugin builds. Vtable guards must
use relocated pointer targets AD8EC0 and destructor31A630; CALL relays must be
within signed rel32 reach and RX. These are checked by the plugin before READY;
never infer them from the disk DLL alone. Retain SFSE log corroboration and
review module inventory for an unexpected injector/profile conflict. No failure.json
or not-ready.json may be present. An absent/mismatched READY means no scientific
actions. Runtime integrity checks continue while collecting; no external memory
reader or debugger is needed to bypass a startup refusal.

## Operator sequence and useful-event readiness

Set `$oracleSession` to that exact new session path, never an archived PID/session.
Use operator marks before and after each deliberate action; notes report save/site,
build state, loaded/unloaded/loading conditions, route, time state, normal settling
and unexpected UI behavior. Notes are testimony, not the primary identity join.

```powershell
& $oraclePython -B runtime/native-oracle/operate.py control $oracleSession mark --label load-Save25 --note 'Main menu; operator will select exact protected Save25; capture already armed'
```

Collection is continuous from READY; no manual capture request or native function
call. User performs this bounded site/action sequence, waiting through ordinary
loading/settling without an arbitrary scientific timeout:

| Phase | Operator action / control and objective |
|---|---|
| Save25 arrival | Load exact Save25 at reported SOR-003 on Kreet. Observe arrival/terrain settling with build closed. Record actual site, settling/loading and time state. Primary grid opportunity is natural terrain/site processing during arrival. |
| 003 no-action/build controls | Mark settled closed, a no-action control, normal build-open, no-action open control, then close. Change no object. Do not assume build-open invokes grid. |
| 002 arrival and controls | Use normal map fast travel to existing SOR-002 only (or the already established on-foot route in the same landing area if fast travel is unavailable; record which). Repeat settled closed/no-action/open/no-action/close. Preserve loading/rebase differences. |
| 003 return | Return via the same permitted route to SOR-003; retain terrain/site/identity-switch evidence and closed/no-action controls. |
| Save26 arrival and controls | Mark load, select exact existing Save26 through normal UI; repeat003→002→003 arrivals and controls. Save26 already contains the relocation; do not move anything or resave. |

Examples of unique phase marks:

```powershell
& $oraclePython -B runtime/native-oracle/operate.py control $oracleSession mark --label Save25-003-closed --note 'Operator confirms settled SOR-003; build closed; no deliberate action'
& $oraclePython -B runtime/native-oracle/operate.py control $oracleSession mark --label Save25-002-arrived --note 'Operator confirms arrival SOR-002; record actual route/loading and elapsed conditions here'
& $oraclePython -B runtime/native-oracle/operate.py control $oracleSession mark --label load-Save26 --note 'Operator will select exact protected Save26; no new save requested'
```

Mark every corresponding phase with actual observations, never paste an inaccurate
template note. Further repeats of those same two protected loads/two existing-site
routes and controls are within this card while healthy, when needed for branch or
repeat evidence; no arbitrary short count/time limit ends collection. Boundaries
are these named saves/sites/actions and the operator's completion/stop, not forced
terrain generation. No different hooks/settings or additional site visits.

Monitor disk, failure markers and journal growth during actions. Distinguish:
READY without callbacks; callback early return without center/grid; center event;
grid-before without return; normal paired grid; partial scientific identity; and
useful identity-bound grid. Zero events means NOT_OBSERVED, not a model failure.
Continue ordinary partial/unreadable/unknown comparisons under a healthy observer.
Do not widen gameplay or force native calls to get a hit. If all allowed arrival
paths still yield no grid, retain that scoped acquisition result; center tuples
cannot be substituted for the missing grid objective.

## Stop, recovery and postflight

Stop on operator direction, machine/instrumentation integrity/writer failure,
disk query failure/floor guard, unexpected protected-input mutation, source/module
or patch mismatch, queue loss/depth health stop, or unexpected corruption outside
the reviewed boundary. A scientific mismatch alone is valuable evidence and does
not require stopping. On an integrity stop, no new phase/action starts.

```powershell
& $oraclePython -B runtime/native-oracle/operate.py control $oracleSession STOP
```

Do not repeat a successful STOP write; CREATE_NEW deliberately rejects duplicates.
Wait for retired.json with active scopes drained, loss/depth counts, and retained
inert patches. The worker flushes each raw/journal record independently. If a
native call does not return or storage fails, retirement may be incomplete: preserve
the last durable prefix/failure receipts; no guaranteed recovery is claimed.
Never hot-unload, restore patches on running threads, suppress faults, terminate
Starfield or attach a debugger. User exits through ordinary UI when possible;
an unresponsive/unstable target requires a narrow recovery decision. Crash/exit
before sufficient evidence is not success; already flushed complete evidence
remains analyzable independently of survival.

After actual process exit and normal Steam synchronization, user disables/removes
this observer via Vortex. Verify Starfield/loader absence and that both deployed
observer files are absent; do not delete them directly. Process exit discards the
retained memory hooks; no claim of live original-byte restoration is made. Recheck
original on-disk game/SFSE, protected saves/archives/fixtures and baseline0.1.1:

```powershell
& $oraclePython -B runtime/native-oracle/operate.py preflight --build $oracleBuild --postflight --receipt live-postflight-01
Test-Path 'C:/Program Files (x86)/Steam/steamapps/common/Starfield/Data/SFSE/Plugins/SorNativePositionOracle.dll'
Test-Path 'C:/Program Files (x86)/Steam/steamapps/common/Starfield/Data/SFSE/Plugins/SorNativePositionOracle.config'
& $oraclePython -B runtime/native-oracle/inspect_events.py $oracleSession --output "$oracleSession/analysis-01.json"
```

Both Test-Path results must be False. Retain original session bytes, hashes and
all receipts in ignored local storage; do not normalize raw captures. Archive any
incidental saves as separate protected copies if separately requested; no overwrite
or cleanup of source saves is authorized here. No raw data upload or Git actions.

## Analysis and scientific outcomes

Inspector validates raw hashes and normal invocation pairing before conditional
comparisons. Independently review exact ordinary base, Workshop+98, reference/body,
source/input/result hierarchy, translation, floor, resolution/block/scale and FP
conditions. Native bytes must remain distinct from DERIVED translated arithmetic.
For Save25/26:002 ID `f1517de43e171745`,003 ID `0efca066ee4c7b9b`, body0003F59F.
Frozen centers/cells/inputs and the existing validation protocol remain unchanged.
No equality, timing proximity or operator site label creates identity/freshness.

Report exact observed matches/counterexamples/missing branches. Classifications:
NOT_READY; NOT_OBSERVED; PARTIAL/UNASSOCIATED; CONDITIONAL_NATIVE_INPUT_REPLAY
(exact match or mismatch); qualified center comparison; saved-frame reconciliation
UNASSESSED until primary evidence independently closes it. Matching final output
with wrong intermediates is not a pass. No fitted epsilon/offset or retuned fixture.
Separate native-input replay from save→loaded-frame end-to-end comparison; blinded
holdouts and additional frame/angle/seam branches remain outside this first card.
Report scientific coverage, observer health/loss/durability, target survival and
cleanup separately, with independent review of results. No full native-equivalence
claim is authorized by Phase A or by a merely installed/healthy hook.
