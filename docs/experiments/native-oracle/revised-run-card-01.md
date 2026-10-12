# Proposed revised run card 01 — reachability before interpretation

2026-10-11. SOR-EXP-0031 / SOR-EV-0039. **OFFLINE REVIEW DRAFT; NOT EXECUTABLE
WITH0.1.0. NO LIVE/SETTINGS/DEPLOYMENT AUTHORITY.** Read the
[revised acquisition plan](revised-acquisition-plan-01.md) and its scope/risks with
this card. This is one proposed diagnostic attempt after a separately reviewed
implementation. It does not authorize running the existing plugin again.

## A. Release lock and ownership — mandatory BLOCKED items

Before any deployment/live approval, replace BLOCKED with actual reviewed values
in an immutable release-lock manifest; retain this proposal and the amendment.
No invented hash, wildcard module approval or old0.1.0 acceptance is sufficient.

| Lock field | Current value / required evidence |
|---|---|
| Candidate | Proposed SorNativePositionOracle0.2.0/schema2; NOT BUILT. |
| ZIP/DLL/config/tool hashes, exact paths | BLOCKED — versioned build plus membership/hash manifest required. Install path remains `Data/SFSE/Plugins/SorNativePositionOracle.dll` and `.config`; any extra installed policy file must appear in the reviewed manifest/removal checks. |
| Module policy | BLOCKED — exact reviewed identities/roles/phases; forbidden overlays below cannot be excepted by a policy row. |
| Six patch guards | BLOCKED — full PE/runtime preimage/signature/relocation/relay ledger for four CALLs and two slots. |
| Schema/health protocol | BLOCKED — exact event sizes/format, Q/E/C scopes, tested1-second heartbeat and15-second action/ack deadline or explicitly reviewed replacement. |
| Qualification and source snapshot | BLOCKED — all mandatory plan tests, source hashes and independent ACCEPT. |
| Game/SFSE/loader | Reverify retail1.16.244.0 / existing pins below; no compatibility transfer. |
| User approval | BLOCKED — exact release lock/card, overlay-setting changes and named diagnostic controls must be approved. |

User controls settings, Vortex installation/removal, `sfse_loader.exe` launch,
save selection and all gameplay. Codex performs approved file/process-metadata
checks, marks/health monitoring, STOP, offline analysis and receipts. No native
process-memory reader/debugger, suspension, forced termination or byte repair.

Build-specific pins to reverify:

| File | SHA256 |
|---|---|
| `Starfield.exe` | `7e9adb1414a8e1b325e5e1f097b9b17b78deb7eebeda37a333351a43a60f9d28` |
| Installed `sfse_1_16_244.dll` | `28c5bda41d9959c885efcb6e889de69e92767c80a1a66842d711d215f722f82b` |
| Installed `sfse_loader.exe` | `16916c2ec47e31774e3d550609a1844fcb368b03060c03511891564b7f5f7526` |

Protected existing source-save entries in
`C:/Users/User/Documents/My Games/Starfield/Saves/`:

| Input | Exact filename; SHA256 |
|---|---|
| Save25 | `Save25_D6036588M417474696C61204B6972616C79_000231_20261009102224_4_0_4.sfs`; `d4df86bc01c2105933fe856a1be5ebbe0c3fc78a4d67fe1a790e18129faf75f5` |
| Save26 | `Save26_D6036588M417474696C61204B6972616C79_000241_20261010012454_4_0_4.sfs`; `2b4781e75226f2ff7c6aa47470fb47ff179c1754461aa208c46716d7c3935104` |

Also protect the two immutable archive copies, frozen23 predictions and
observer0.1.1 using the retained six-pin baseline; lock their exact paths/hashes
in the new release manifest. Loads use the named, verified existing entries; no
tool writes them, no manual save/overwrite or active-playthrough replacement.
Inventory save-folder names/sizes/hashes before launch and after exit so incidental
autosaves are separately detectable; do not delete or overwrite them. No autosave
setting change. Native calls may affect execution even without deliberate gameplay
mutation; target survival is unqualified until the live attempt.

## B. Approved future environment preparation

After explicit settings/deployment approval only, with Starfield/loader absent:

1. User records previous settings, disables Steam's Starfield overlay and NVIDIA
   overlay/capture features, and confirms no other injector/overlay/observer is
   enabled for this launch. Preserve exact settings and attestation locally.
2. User installs the exact approved ZIP through Vortex profile `Starfield - SFSE`;
   only this reviewed SFSE plugin is deployed. Preserve observer0.1.1 artifacts.
3. Codex verifies actual deployed bytes and configuration, module-policy hash,
   sources, protected inputs, actual game/SFSE/loader files, absence of target and
   debugger processes, save-folder inventory and caller-available
   **40,000,000,000 bytes on both C:/D:**. Unknown/query failures are failures.

Forbidden module basenames regardless of path/hash:
`gameoverlayrenderer64.dll`, `nvspcap64.dll`, `nvppex.dll`.
The complete phase-specific allowlist additionally rejects unreviewed modules.
File names alone do not establish safe behavior; see the plan's residual limits.
No fallback to Steam/NVIDIA exceptions, service termination or altered DLLs.

## C. Command contract — fill and verify during implementation review

The PowerShell templates below preserve the existing tool interface, but **must
not be run now**. `release-lock.json`, version2 tools and policy enforcement do
not yet exist. The reviewed final card must give the actual absolute lock path,
SHA256 and supported command help/output schemas. A failed/missing schema is a
gate failure; the current0.1.0 tools cannot clear the new mandatory checks.

```powershell
# FUTURE TEMPLATE ONLY: use the absolute lock path and its separately approved SHA256.
$oraclePython = 'C:/Users/User/AppData/Local/Python/pythoncore-3.14-64/python.exe'
$oracleLockPath = '<BLOCKED: reviewed absolute release-lock.json path>'
$oracleLock = Get-Content -LiteralPath $oracleLockPath -Raw | ConvertFrom-Json
$oracleBuild = $oracleLock.build_directory
$oracleTools = $oracleLock.tool_directory
& $oraclePython -B "$oracleTools/operate.py" preflight --build $oracleBuild --deployed --receipt revised-live-preflight-01
```

Run from `D:/Projects/starfield-outpost-research`. Independently hash the lock
before trusting paths, verify tools against its snapshot, and require exit0,
all named checks true and an untouched new receipt. No automatic rebuild or
download. Preflight must explicitly report all new environment/policy/protected
checks, not just reuse0.1.0's overall boolean. User attestation and future runtime
pre-write admission are separate pending gates; disk-file checks alone cannot
prove the module load state of a process that does not yet exist.

Once this exact card/package is approved and offline prelaunch checks pass,
Codex gives the loader go-ahead. User launches once through Vortex using the
pinned loader. Stay at the main menu; no save/gameplay action until section D.
No retry follows refusal. Routine progress through already approved successful
gates does not need another permission question.

## D. Pre-write admission, READY and main-menu release

The revised plugin must enforce the plan's pre-write inventory/policy and final
sole-thread gate **before any six edits**. Require a flushed admission receipt
with PID/creation FILETIME, actual base, clock, source/policy/module hashes,
phase and explicit checks. Inventory/hash failure, forbidden/unknown module,
thread timeout or preimage mismatch means NOT_READY and no installation when
refusal preceded mutation.120-second sole-thread wait is the maximum; no thread
suspension or reduced check.

Find one unique new session under
`D:/Projects/starfield-outpost-research/.local-work/native-oracle-live/`; never use
an archived session/PID. Codex compares PID/creation identity to process metadata,
game/SFSE/DLL/schema/policy hashes to the approved lock, and admission/patch/READY
receipts to each other. Require the six sites, original/installed guards, valid
rel32/RX islands, SFSE successful load and no NOT_READY/failure marker. Check the
full main-menu module inventory against its approved phase policy again.

READY is initialization, not release for gameplay. Require a fresh worker heartbeat
and a durable acknowledgement of a unique, newly written control nonce within
the qualified15-second deadline. This worker-only challenge must not execute an
engine function. The final tool CLI for writing/checking the nonce is BLOCKED
until implementation; no invocation of old `mark` is an acknowledgement.

Codex issues a single recorded main-menu admission PASS only when every mandatory
check is true. If modules/health fail after patches were installed, request STOP,
preserve the distinction, and follow section F. Do not load saves to see whether
an admission failure is harmless. No routine user approval is needed after an
already authorized PASS; no PASS is inferred from a responsive menu alone.

## E. Diagnostic operator sequence

For every action: verify a fresh heartbeat/ack and module/patch/disk/queue health,
write a unique request mark, obtain the user's actual completion/state report,
then write a distinct confirmation mark. Record unknown location/settling/time
state as unknown. Existing marking interface, if retained and qualified:

```powershell
# FUTURE TEMPLATE ONLY: $oracleSession is the verified new session from section D.
& $oraclePython -B "$oracleTools/operate.py" control $oracleSession mark --label Save25-load-request --note 'Operator will select exact Save25; main-menu admission PASS'
```

Continuous Q/E/C/center/grid collection is armed before loading. No engine event
is requested by the operator tooling. The user performs one complete matrix:

| Phase | Exact permitted action and control |
|---|---|
| Main menu | Responsive no-action control and worker nonce acknowledgement; no claim of native query positive control. |
| Save25 / SOR-003 | Load exact Save25. Confirm actual location/build closed, ordinary arrival/settling and no-action closed control. Open existing outpost build mode without selecting/placing/moving anything; no-action open control; close. |
| Save25 / SOR-002 | Normal map fast travel to the existing SOR-002; confirm completion/closed, no-action control, open/no-change control, close. No new landing location or alternate route. |
| Save25 / SOR-003 return | Normal fast travel to existing SOR-003; confirm completion/closed, no-action control. |
| Save26 | Select exact existing Save26 through normal UI; confirm actual SOR-003. Repeat the same003→002→003 controls. Its existing relocation is input; do not relocate anything. |

If site, route or UI capability differs from the card, stop that action and
preserve the checkpoint; no silent substitution. The card allows ordinary loading
and settling, not an arbitrary seconds-long scientific observation quota. Safety
health deadlines remain active. If the game is responsive but state/settling is
unclear, ask the operator for that state rather than interpreting an elapsed timer.

At every confirmed checkpoint, retain durable Q/E/C/center/grid counts and paired
scope/health analysis. Inspect only flushed bytes; do not rewrite raw evidence.
No scientific mismatch or incomplete identity alone stops a healthy permitted
matrix. Complete both saves' matrix unless a safety failure or user stop occurs.
After its completion, retire and analyze; identical repetitions are not automatic.
Additional repetitions require a specific diagnostic reason and reviewed scope.
This finite action matrix bounds the attempt, not a claim that absence is proven
after a particular number of seconds/events.

Prohibited fallbacks: new landing site/map selection, beacon placement preview,
construction/selection/relocation/deletion, new save/resave, console/native calls,
Save52/holdouts, gate-helper hooks, settings changes while running, overlay
reenablement, debugger or patched observer retry. Existing build-mode reticle
behavior is recorded, not repaired or made an acquisition dependency.

## F. Stop, exit and cleanup

Stop new actions on user direction, forbidden/unknown module, missing/failed
health/ack, writer/queue/depth/integrity failure, disk query/floor failure,
protected-input drift, mismatched identities/guards or unexpected corruption.
Close admission through the qualified STOP path once:

```powershell
& $oraclePython -B "$oracleTools/operate.py" control $oracleSession STOP
```

Require terminal identity, a **fresh retirement timestamp/QPC**, active Q/E/C
scopes drained, flushed offsets/hash chain and loss/depth/health status.0.1.0's
reused startup UTC is not a retirement clock. All six patches/islands/DLL remain
resident and inert until process exit; no hot-unhook or original-byte restoration
claim. A stuck native call or disk failure may prevent a complete terminal receipt.
Retain failure and the last durable prefix; do not suppress exceptions or promise
recovery. User exits normally when possible. An unresponsive target needs a narrow
recovery decision; no forced kill or attachment is part of this card.

After actual exit and the user's normal Steam-sync confirmation, user disables
the candidate via Vortex. Codex checks Starfield/loader/debugger absence and all
installed candidate files absent, rehashes the actual installed game/SFSE/loader,
six protected inputs, frozen fixtures and source snapshot, and records disk and
save-folder differences. Existing interface, if retained and qualified:

```powershell
& $oraclePython -B "$oracleTools/operate.py" preflight --build $oracleBuild --postflight --receipt revised-live-postflight-01
& $oraclePython -B "$oracleTools/inspect_events.py" $oracleSession --output "$oracleSession/revised-analysis-01.json"
```

Both deployed DLL/config paths and any reviewed extra installed policy path must
be absent. No direct deletion by Codex. Postflight must hash **installed** SFSE
and loader even after removal; a staging-path check is insufficient. User may
restore only the approved recorded overlay settings after exit, documenting
actual values; do not relaunch to test restoration. Preserve incidental saves
separately; no deletion/overwrite or automatic evidence upload/Git operation.

## G. Analysis, completion and reporting

Verify original byte hashes, journal prefixes, schema2 sequencing/pairing and
Q→E→C identity before interpreting absence. Use the plan's diagnostic outcome
table; heartbeat confirms worker response, not engine-hook reachability. Do not
combine unknown/orphan scopes or turn sampled gate fields into observed branches.

Native output analysis retains all original identity/frame constraints. Frozen
Save25/26 identities:002 `f1517de43e171745`,003 `0efca066ee4c7b9b`, body0003F59F.
Require actual ordinary reference/base/Workshop/source/input/result linkage;
operator location is testimony. Compare actual input/output/intermediate bytes
against unchanged frozen expectations only after capture. Conditional native-input
replay is separate from saved-to-loaded authority/reconciliation and full native
equivalence. No retuning, fitted offset/epsilon or substitution of diagnostics or
synthetic qualification output for native grid evidence.

Return module admission/conformance (including deviations), Q/E/C reachability,
useful oracle support/counterexamples/missing branches, transport/durability,
target survival and cleanup as separate dimensions. A diagnostic-only result can
complete this bounded diagnostic session while leaving useful acquisition/native
equivalence incomplete. An unvalidated/missing detector cannot establish a
scientific negative. Preserve raw evidence, complete/task-only diffs/manifests,
actual checks/limits and independent critical review. Further experiments require
their scoped decision; this card grants no publication, stage, commit or push.
