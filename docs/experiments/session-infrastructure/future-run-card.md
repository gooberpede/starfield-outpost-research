# Future phase sequence using the shared harness

2026-10-15, Australia/Sydney. Example only; no new experiment is authorized.
The next approved observer must name its reviewed adapter/build/manifest,
protected-input plan, gameplay question/actions and exit/recovery policy. The
current adapter supports 0.7.0 only; do not substitute a new native schema.

Before launch, review the plan described in the [tool instructions](../../../runtime/session-tools/README.md).
Use the new run's explicit pins, not opportunistically computed replacement pins
after a mismatch. After approval, the maintainer handles Vortex deployment.

```powershell
$py = 'C:/Users/User/AppData/Local/Python/pythoncore-3.14-64/python.exe'
$ops = 'runtime/session-tools/session.py'
$zip = 'runtime/session-tools/archive.py'
$run = '.local-work/NEXT_APPROVED_RUN' # create a fresh private run directory
$plan = "$run/plan.json" # reviewed local plan; schema in tool instructions
$planPin = 'REVIEWED_PLAN_SHA256'
& $py -B $ops prelaunch --input $plan --sha256 $planPin --out "$run/prelaunch.json"
if ($LASTEXITCODE) { throw 'Do not launch; resolve the recorded prelaunch failure.' }
$preflightPin = (Get-FileHash -LiteralPath "$run/prelaunch.json" -Algorithm SHA256).Hash.ToLowerInvariant()

# Identify the approved save offline using original hash-bound source metadata.
& $py -B save-analysis/scripts/save_menu.py --mapping "$run/save-mapping.json" --utc-offset '+11:00' --json "$run/menu.json"
if ($LASTEXITCODE) { throw 'Resolve save identification before launch.' }
```

Give the resulting concise load instruction once. The historical Save3 example is:
**Load Attila Kiraly — Kreet - Kreet — Level 3 — 10/6/26, 12:34:27 PM.**
For Save25, the existing utility's controlled instruction is:
**Load Attila Kiraly — Kreet - Outpost — Level 4 — 10/9/26, 9:22:22 PM.**
These examples are not a choice of control save for the next experiment. Use
the authorized mapping's actual label, character and timezone; do not choose a
menu ordinal. Only ambiguity, a missing entry or a material mismatch warrants
one targeted check. No repeated routine confirmation follows a supplied label.

The operator launches through the reviewed SFSE/Vortex entry. Select exactly the
new observer session, distinct from the prelaunch existing-session inventory:

```powershell
$session = 'EXACT_NEW_SESSION_DIRECTORY'
& $py -B $ops request --input "$run/prelaunch.json" --sha256 $preflightPin --session $session --out "$run/request-01.json"
if ($LASTEXITCODE) { throw 'Investigate request failure; preserve receipt.' }
$requestPin = (Get-FileHash -LiteralPath "$run/request-01.json" -Algorithm SHA256).Hash.ToLowerInvariant()
& $py -B $ops live --input "$run/prelaunch.json" --sha256 $preflightPin --session $session --request "$run/request-01.json" --request-sha256 $requestPin --out "$run/live-01.json"
```

`READY_ACK`, active original PID/creation, valid native admission and healthy
worker evidence permit the approved load/actions. `WAITING_*` calls for an
update and another small check with a new output name; it does not create a
deadline. Between meaningful phases, use `live` for small health snapshots and
issue a fresh `request` for a new challenge. Compare serial and durable progress.
Never perform a routine full audit while the operator stands idle in-game.
If a specific integrity incident requires one, first record the concrete incident,
scope and reason; use the approved incident policy or exit before auditing.

Keep observer-specific marks, hook guards, native decoding and scientific
comparisons in the reviewed observer tools. Normal Steam/NVIDIA overlays are
accepted. Actual integrity/identity/instruction/disk/worker failures and explicit
STOP remain hard stops, with the approved orderly retirement/exit policy.

```powershell
& $py -B $ops stop --input "$run/prelaunch.json" --sha256 $preflightPin --session $session --out "$run/stop.json"
# Continue lightweight checks with fresh output names until retirement is known.
# Operator exits normally, then removes the observer using Vortex.
& $py -B $ops postflight --input "$run/prelaunch.json" --sha256 $preflightPin --session $session --out "$run/postflight.json"
```

Run postflight after exit, without asking the user to idle in-game through it.
ExitSave additions/removals/content changes are reported separately from other
save changes and metadata-only changes. Protected-manifest pins still apply.
Any `PARTIAL_POSTFLIGHT` or check error remains a failure requiring investigation;
never relabel it complete. Target survival, evidence integrity and scientific
result stay separate.

Complete companion receipts and scientific metadata before sealing. Create
`$run/roots.json` with `raw` pointing at the original session and `receipts`
pointing at the finished run directory, plus derivative/report roots as needed.
Every directory must be quiescent. Save archival outputs in a sibling directory:

```powershell
$archiveRun = '.local-work/NEXT_APPROVED_RUN-archive'
New-Item -ItemType Directory -Path $archiveRun -ErrorAction Stop | Out-Null
$rootsPin = (Get-FileHash -LiteralPath "$run/roots.json" -Algorithm SHA256).Hash.ToLowerInvariant()
$postPin = (Get-FileHash -LiteralPath "$run/postflight.json" -Algorithm SHA256).Hash.ToLowerInvariant()
& $py -B $zip seal --input "$run/roots.json" --sha256 $rootsPin --postflight "$run/postflight.json" --postflight-sha256 $postPin --out "$archiveRun/seal.json"
if ($LASTEXITCODE) { throw 'Seal refused; preserve all originals.' }
$sealPin = (Get-FileHash -LiteralPath "$archiveRun/seal.json" -Algorithm SHA256).Hash.ToLowerInvariant()
& $py -B $zip create --input "$archiveRun/seal.json" --sha256 $sealPin --archive "$archiveRun/evidence.zip" --out "$archiveRun/archive.json"
if ($LASTEXITCODE) { throw 'Archive unverified; preserve all originals and error receipt.' }
$zipPin = (Get-FileHash -LiteralPath "$archiveRun/evidence.zip" -Algorithm SHA256).Hash.ToLowerInvariant()
& $py -B $zip verify --input "$archiveRun/seal.json" --sha256 $sealPin --archive "$archiveRun/evidence.zip" --archive-sha256 $zipPin --out "$archiveRun/verify.json"
if ($LASTEXITCODE) { throw 'Verification failed; preserve and investigate.' }
```

For an incomplete/crashed capture with confirmed exit and partial postflight,
add `--partial-reason 'EXACT_RECORDED_REASON'` to `seal`. This preserves every
byte and the failure status; it does not repair tails or claim scientific success.
Keep both raw and ZIP at first adoption. Archival receipts are outside sealed
roots and separately hash-bound; no cleanup or deletion follows automatically.
Return the scientific result, operational outcomes, sealed inventories, archival
verification, permissions/limits and complete review patches for critical review.
