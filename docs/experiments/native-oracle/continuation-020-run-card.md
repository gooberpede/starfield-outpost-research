# Native-oracle 0.2.0 executable run card

2026-10-12. SOR-EXP-0031 / SOR-EV-0039. **REVIEW CANDIDATE; no live execution
before the maintainer's combined approval of this exact package and card.**
[Contract](continuation-020-contract.md), [architecture](continuation-020-architecture.md),
[qualification](continuation-020-qualification.md) and [review](continuation-020-review.md)
are part of that decision. Approval may include controls only or controls + N1;
record which. No second routine approval follows successful reviewed preflight.

## Release lock and responsibilities

| Release field | Exact reviewed value |
|---|---|
| Build | `D:/Projects/starfield-outpost-research/.local-work/native-oracle-020/builds/final-review-04` |
| ZIP SHA256 | `6dfb89713c4d8aedd072170ffdc2b8436509ce634eb037275ef6e78a52a6b0b9` |
| DLL SHA256 | `00fa1c2d42871a0ba096d49d235f88917f025f9b0f97ec24a7a246c056744201` |
| Config SHA256 | `6894da75d4face7b9d366a67c436fe75b100a434e073f7184bcca55e19d953c9` |
| build.json SHA256 | `1d678414a3938b888a62fc525ba9aaa0f99982ae25f3f35fa80eca73aa85536a` |
| release-lock.json SHA256 | `11d1725be9c08d10b8c8c019066fe7213a3a2d13ddf2c3174769e43d948238a1` |
| Starfield.exe retail1.16.244.0 | `7e9adb1414a8e1b325e5e1f097b9b17b78deb7eebeda37a333351a43a60f9d28` |
| SFSE0.2.21 sfse_1_16_244.dll | `28c5bda41d9959c885efcb6e889de69e92767c80a1a66842d711d215f722f82b` |
| sfse_loader.exe | `16916c2ec47e31774e3d550609a1844fcb368b03060c03511891564b7f5f7526` |

User deploys/removes through Vortex profile `Starfield - SFSE`, launches via the
pinned sfse_loader.exe and performs every in-game action. Codex checks files and
limited process metadata, monitors evidence, writes markers/nonces/STOP and
analyzes offline. No debugger, live process-memory reader, forced native call,
suspension/kill, hot removal, console command or byte repair is authorized.

The release lock pins build.json and all source tools independently. Verify its
printed SHA before trusting any path. This card is executable with the built0.2.0;
old0.1.0 tools/cards cannot substitute. All output paths must be new and exclusive.
Run commands from `D:/Projects/starfield-outpost-research`:

```powershell
$oraclePython = 'C:/Users/User/AppData/Local/Python/pythoncore-3.14-64/python.exe'
$oracleTools = 'D:/Projects/starfield-outpost-research/runtime/native-oracle-020'
$oracleBuild = 'D:/Projects/starfield-outpost-research/.local-work/native-oracle-020/builds/final-review-04'
$oracleLock = 'D:/Projects/starfield-outpost-research/.local-work/native-oracle/continuation-020/release-lock.json'
Get-FileHash -Algorithm SHA256 -LiteralPath $oracleLock
```

Compare with this card's lock SHA. Hash build.json and every source/tool against
the lock/build manifest before invoking tooling; a mismatch halts. No rebuild,
download, staging or automatic new release. Retain manifest membership: two
plugin files under Data/SFSE/Plugins plus three ResearchNotices files. Vortex must
map ZIP root to game root; no extra Data/Data nesting. Preserve0.1.0/observer0.1.1
archives independently. Only this reviewed SFSE plugin DLL is enabled/deployed.

Protected originals (full paths/hashes in build.json/lock): installed Starfield.exe,
Save25/Save26 in the user's Saves directory and their exact-beacon-01/initial-01
archive copies, observer0.1.1 ZIP. Also pin frozen23 predictions and imported replay
sources via build manifest. Save25 SHA d4df86bc01c2105933fe856a1be5ebbe0c3fc78a4d67fe1a790e18129faf75f5;
Save26 SHA 2b4781e75226f2ff7c6aa47470fb47ff179c1754461aa208c46716d7c3935104.
Never overwrite/delete them or select an active personal playthrough. Inventory
save-folder filenames, sizes and SHA before launch, at any new N1 checkpoint and
after exit; retain new receipts under the ignored continuation directory. Incidental
autosaves/exit saves may appear; preserve and identify them, do not delete or change
autosave settings. User identifies load entries by exact verified filename/time.

## Preflight and launch

Normal Steam/NVIDIA overlays remain enabled as usual; no settings changes,
service kills, DLL renames or Vortex purge. Module unfamiliarity alone is not a
block. Record actual roles/hashes; evidence of a specific owned-site conflict or
credible competing instrumentation is a hard stop pending assessment. No silent
exception to failed identity, byte guard, disk, sole-thread or health gates.

With target/loader/debuggers absent and user-deployed bytes confirmed:

```powershell
& $oraclePython -B "$oracleTools/operate.py" preflight --build $oracleBuild --deployed --receipt continuation-live-preflight-01
```

Require exit0 and every receipt check true, installed SFSE/loader pins, exactly
SorNativePositionOracle.dll/config, default both channels, all protected/source
pins and caller-free C:/D: at least40,000,000,000 bytes (tool preflight reserves an
additional100MB). Record Vortex profile and enabled-mod attestation separately;
file checks do not attest its UI. Confirm no known competing injector outside
accepted overlays. After this PASS Codex gives the go-ahead; user launches once
through Vortex's sfse_loader.exe. Remain at main menu. No automatic retry.

## Runtime admission and action release

Choose the single **new** session under
`D:/Projects/starfield-outpost-research/.local-work/native-oracle-live/` whose
PID/creation FILETIME matches the actual process. Never reuse attempt01 or an
archived session merely because it is newest. Set $oracleSession to that exact
absolute path. Require admission.json, patches.json, ready.json, modules-pre-edit
and initial health; absence, not-ready.json or failure.json blocks all save loads.
Plugin waits at most120 seconds for observed sole-thread SFSE pre-main startup;
no wait extension or thread suspension. If startup refuses, exit normally and
preserve NOT_READY, not a retry with weaker guard.

Codex reads these receipts and records a new main-menu admission report:

- Identity agrees across READY/admission/patch/health and reviewed lock: version0.2.0,
  schema2, event_size17768, exact DLL/game/SFSE, actual base, PID and creation time,
  QPC frequency positive; grid/center true, heartbeat1000ms/deadline15000ms.
- Admission says owned_sites_original, sole_thread_observed and
  standard_overlays_accepted true, patches_installed_at_receipt false, with pre-edit
  module inventory. It precedes native writes; final install rechecks all six
  preimages and sole thread. This is instrument self-attestation, not external
  proof of thread-creation exclusion.
- Patches are exactly four5-byte CALLs at base+AD0C36/AD0D36/AD93FA/AD0AB5 and
  two8-byte slots base+4B916F0/4B916F8. Original CALL hashes agree with the pinned
  complete instruction bytes; slot originals encode base+AD8EC0. Installed hashes,
  relay/protection provenance and startup native guards agree with reviewed source.
  Worker checks installed edits and untouched target guards while idle/draining.
- Review current module inventories against pre-edit and historical roles. Accepted
  overlay names are not evidence of a conflict. A new unknown module gets a
  specific assessment; stop only for credible interference/failed guard or failed
  enumeration/mandatory identity hash. Optional module hash_status UNREADABLE is
  explicitly assessed for specific risk, not presumed valid or blocked by name. No universal compatibility claim.

READY alone does not release gameplay. Issue one new nonce and require a fresh
worker-only durable ACK within15 seconds:

```powershell
& $oraclePython -B "$oracleTools/operate.py" control $oracleSession challenge
# Copy the returned 32-hex nonce into the next command.
& $oraclePython -B "$oracleTools/operate.py" health $oracleSession --nonce $oracleNonce
```

$oracleNonce is the exact returned nonce, never a fixed example. Poll at one-second
intervals only until15 seconds from request, stop on explicit failure/stale health.
Require exit0/pass_check true, matching live PID/creation metadata, no historical
heartbeat gap>15s, no loss/depth/watchdog fault and current health within15s. A
recovered stall still fails. Codex records admission PASS only after all gates.
Heartbeat proves worker response, not boundary reachability or native equivalence.

Before/after every action Codex checks health, module changes, both disks and
protected pins; monitor at least once per second while waiting for user action
reports. One action at a time. Write unique request and completion marks, e.g.:

```powershell
& $oraclePython -B "$oracleTools/operate.py" control $oracleSession mark --label Save25-load-request --note 'Main-menu admission PASS; exact protected Save25 requested'
& $oraclePython -B "$oracleTools/operate.py" control $oracleSession mark --label Save25-load-complete --note 'Record actual operator location/build/response/settling state'
```

Notes are operator testimony, not reference identity. Do not treat note text or
chronological proximity as a native join. Use distinct labels for every row below;
repeat a fresh challenge at each completed travel/load/build checkpoint. If an ACK
or ongoing health check fails, stop further actions.15s is health latency, not a
scientific no-hit quota or a demand that the user finish travel within15s.

## Finite control matrix

Continuous Q/E/C/center/grid capture starts before loading. User confirms actual
location, game response, build state and ordinary arrival/settling after each row.
No mandatory scientific waiting interval/event quota; record unclear state as
UNKNOWN and resolve operator state before proceeding within approved actions.

| Phase | Permitted user action; diagnostic value |
|---|---|
| Main menu | Responsive no-action control + nonce; healthy zero-native baseline only. |
| Save25 / SOR-003 | Load exact protected Save25; closed no-action control; open build mode without selecting/placing/moving anything, no-action control, close. Tests earlier revisit/build hypothesis with upstream scopes. |
| Save25 / SOR-002 | Ordinary map fast travel to existing SOR-002; closed control; open/no-change control; close. No alternate landing selection. |
| Save25 / SOR-003 return | Ordinary fast travel back to existing SOR-003; closed control. |
| Save26 / SOR-003 | Load exact protected Save26; confirm SOR-003 and repeat its003ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢002ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢003 closed/build-open/no-change/return controls. Existing relocation is input, never reenacted. |

Complete both controls even if a healthy scientific mismatch or optional read
failure occurs. No-hit is useful only with qualified health/ancestry. Parent-linked
Q without E, E without C, C without center/grid or complete native pairs discriminate
stages; they do not by themselves prove exact gate causes. Route/site/UI discrepancy
halts that action; no silent substitution. After controls, either retire or perform
N1 **only if the combined approval explicitly included it**.

## Conditional N1: one new accessible Kreet landing

Purpose: stronger natural fallback-candidate opportunity than revisiting an
existing reference. Static supporting chain and competing existing-match branch
are in the architecture. Q/E/C positivity remains a hypothesis. This card proposes
one landing, no beacon/new outpost construction; no specialized unlock/high-level
travel or additional outpost slot is required. Low-level cap is eight total; no
outpost deletion to create capacity. No Save52 fallback in this run.

Prerequisites: user-approved N1, exact Save26 lineage on Kreet, accessible map and
ordinary ship/landing capability, no wanted/combat/quest interruption that changes
route; protected originals verified. User confirms a practicable ordinary landable
point distinct from SOR-002/SOR-003 and every existing Landing Area/outpost icon.
Avoid POI/quest markers, ocean/unlandable terrain; if no suitable point, record N1
infeasible and retire, without trying another experiment.

1. From Save26 at returned SOR-003, user creates a **new manual save slot** as
   checkpoint `N1-baseline`; never overwrite Save25/26 or an active playthrough.
   These are research labels, not a claim that Starfield permits custom filenames.
   Record actual new file, timestamp, SHA, parent Save26, character/body/location,
   outpost count (UNKNOWN if unverified), autosaves and current build/time state.
2. User takes the ordinary ship/orbit route needed for Kreet's planet map, then
   selects the one agreed new landable point and lands once. Codex marks each
   request/completion and maintains health during loading. No scan/console/native
   injection, beacon preview, selection, relocation, construction or deletion.
3. Confirm actual location/response and closed-build arrival/settling. User creates
   one further **new slot** `N1-landed`; map actual filename/hash and lineage back
   to N1-baseline. Preserve incidental autosaves; no reload/new landing/repetition.
4. Retire. Do not add an outpost merely because Q/E/C are absent. New site evidence
   is diagnostic holdout only; independent expectations were not frozen for it.

If baseline cannot be made without overwrite, or route requires unapproved actions,
stop N1 and retire. New checkpoint filenames are acquired during approved live work,
not guessed now. Codex does not modify save contents or change autosave settings.

## STOP, failure, cleanup and analysis

Hard stop: user direction; disk query/floor failure; identity/protected drift;
site/preimage/relay/patch conflict; failed admission/worker/ACK; loss/depth/watchdog;
unexpected corruption or credible new interference. Preserve novel native values
and complete healthy approved actions; scientific mismatch alone is not a safety
failure. Write STOP once, even below the disk floor:

```powershell
& $oraclePython -B "$oracleTools/operate.py" control $oracleSession STOP
```

From successful STOP publication, poll terminal/health at one-second intervals for
at most **30 seconds**. This is an operational retirement bound, not a scientific
capture quota or a claim every native call must return in30s. If terminal is absent,
active/queue remains nonzero or terminal checks fail at that deadline, record
RETIREMENT_INCOMPLETE and stop waiting for capture completion; request ordinary
user exit if possible, preserve the durable prefix and follow the recovery rule
below. Do not reset the deadline, retry, unhook or kill. A failed heartbeat already
stops new actions at its shorter15s bound.

Require fresh retired_utc/retired_tick, agreeing identities, activeQ/E/C0, queue0,
flushed event/offset counts matching complete journal, entered counts matching stage
begins and no loss/depth/watchdog. Patches/relays/DLL remain resident inert until
exit; never claim hot restoration. A stuck native call/disk failure may prevent
complete retirement: preserve failure and last durable prefix, stop actions and
ask user for ordinary exit when possible. For unresponsive target, halt and seek
a narrow recovery decision; no forced termination or attach. Crash/abnormal exit
is recorded separately from evidence completeness and scientific result; no retry.

User exits normally, confirms Steam sync, disables candidate via Vortex. Codex
checks actual target/loader absence and every installed package file absent
(including ResearchNotices), then hashes **installed** SFSE/loader/game, protected
inputs, frozen predictions/source snapshot and save-folder differences:

```powershell
& $oraclePython -B "$oracleTools/operate.py" preflight --build $oracleBuild --postflight --receipt continuation-live-postflight-01
& $oraclePython -B "$oracleTools/inspect_events.py" $oracleSession --output "$oracleSession/continuation-analysis-01.json"
```

Removal absence is a separate explicit file check; postflight's boolean does not
itself attest removal or Vortex state. No direct deletion, autosave cleanup,
settings restoration/change or relaunch. Retain all receipts/raw/partials privately.

Report separately: operational admission/overlay conformance, stage reachability,
useful native pairs/identity/frame support, durability/loss, target survival and
cleanup. Orphans/incomplete scopes, contradictory entered counters or failed health
cannot qualify branch negatives. Native replay uses unchanged frozen23 predictions;
ordinary base002C60E9, Workshop002 f1517de43e171745 /003 0efca066ee4c7b9b and actual
body0003F59F must be captured independently. Output equality cannot select identity.
Actual saved-to-loaded selected-frame reconciliation remains independent and not
automated. No fitted offset/epsilon, retuning, full-equivalence claim or promotion
from synthetic qualification. Return reviewed patches/result; no automatic second
run, scope expansion, publication, staging, commit or push.
