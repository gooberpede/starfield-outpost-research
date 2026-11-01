# D5AB proposed B2 operator run card

2026-11-01, Australia/Sydney. **B2 NOT AUTHORIZED.** P4 prepares a candidate for
separate maintainer review. This card authorizes no installation, launch, game
load, travel, live control-file write, exit/disablement or retry. Final readiness
is recorded in [P4 decision](d5ab-p4-decision.md); exact candidate/tool identities
are in [P4 manifest](d5ab-p4-package-manifest.md).

## Proposed episode and responsibilities

Exactly one new Starfield process, one load of **Save52 at the Lodge**, and one
ordinary direct fast travel to **Feynman V Cu IL F** are proposed. The maintainer
owns install/enablement through Vortex, launch through the pinned SFSE loader,
save choice/load, travel, STOP instruction, normal exit and disablement. A session
operator runs only separately approved checks and request/STOP writes. No forced
source path, artificial reset, resave, second load, second visit or retry follows.

The analytical target is `0:37536:20928:0029d20e`, body FormID `0x0005e0de`.
It is not a menu destination identifier or memory address. Exact protected input:
`Save52_BA75E3CDM43616F205472616E_580743_20260818064541_319_15_4.sfs`,
16,411,136 bytes, SHA-256
`6b4a10084c7e752c31fd2de121a00850aaa2bf1decd700b437d7dccfcdbc82e8`.
Use the protected menu mapping and maintainer knowledge to identify it; do not
guess an ordinal. The Lodge starting state must be confirmed before travel.

## Ordered checkpoints

| Step | Responsible person and action | Required result before proceeding |
|---|---|---|
| 1. Offline preparation | Session operator verifies final package/tool/card pins, no Starfield process, full protection and restoration COPY using the command below. | Fresh `PASS_OFFLINE_PREFLIGHT`; 40,000,000,000 caller-available bytes on both C: and D:; all protected inputs/backups/remote saves/configs/definitions match. This is not GO. |
| 2. Separate authorization | Maintainer reviews final accepted package/card and gives explicit scoped GO, if desired. Record the actual instruction locally. | No GO exists under P4. Approval must bind plan/card/package hashes, one episode, control-file writes, install/enable/launch, exit/recovery, and no automatic retry. |
| 3. Install and launch: NOT AUTHORIZED | Maintainer confirms Cloud disabled where applicable, Vortex profile `Starfield - SFSE`, no prior attempt and no competing SOR observers; installs/enables exact candidate and launches once via the pinned SFSE loader. | Effective deployed DLL and SFSE hashes checked; remain at main menu with no save loaded. A Vortex checkbox alone is insufficient. |
| 4. READY and arming: NOT AUTHORIZED | Operator selects only the newly created live session, binds actual process image/PID/creation, DLL/game/SFSE, startup nonce, eighteen site guards and worker identity; starts controller and obtains a fresh request/ACK. | `BOUND_READY`, then `HEALTHY_ACK` with no prior loss/fault before load. Identity-bound approval receipt records the earlier actual GO plus this newly known session. A slow ACK means wait/investigate, not permission to load. |
| 5. Save load: NOT AUTHORIZED | Maintainer loads exact Save52 once and reports loaded at the Lodge, not travelled. Operator records load-request/load-complete observation intervals and obtains another fresh challenge. | Distinct nonce, same process/session, healthy worker and coverage counters. No full content/save/archive scan during play. |
| 6. Direct travel: NOT AUTHORIZED | Maintainer initiates one direct fast travel to Feynman V Cu IL F. Operator records the travel-request interval. | No alternate destination, forcing, reset or second travel. Native events recorded only at the eighteen actual instrumented boundaries. |
| 7. Arrival and STOP: NOT AUTHORIZED | Maintainer reports ordinary arrival. Operator records the observation interval and obtains fresh health/coverage. Maintainer directs STOP; operator issues owned same-session STOP. | Preserve losses/faults and all evidence. Do not wait for a preferred mask or target event. `RETIRED_PENDING_POSTFLIGHT` is metadata only, never scientific success. |
| 8. Exit/disablement: NOT AUTHORIZED | Maintainer exits normally and disables/removes effective observer through Vortex, retaining the reviewed offline package. | Original process creation identity gone; effective DLL absent. No hot unload, unpatch, process kill, exception suppression or automatic relaunch. |
| 9. Offline postflight | Operator repeats full protected audit and checks exact session identity/owned STOP, raw frames, CRCs, ACKs, terminal and final reader/reducer. | Protection and admitted-byte integrity stated separately from target science. Partial/faulted evidence stays partial. |
| 10. Archive and review | Operator finishes companion receipts, seals quiescent roots, creates ZIP, stream-verifies every member and independently reconstructs required members. | Original raw tree retained; no upload, deletion or publication. Independent scientific review decides the observed result. |

Operator-reported moments are observation intervals. This candidate does not add
an exact native visual-arrival/loading-screen hook. A source query near an arrival
note is not the arrival instant, nor proof that that travel caused it.

## Failure and STOP decisions

Actual identity/site/relay/guard mismatch, worker death, disk-query/floor failure,
output fault/corruption, protected-input incident or explicit maintainer STOP
precludes continued capture. Preserve receipts, issue owned STOP where possible
and follow the separately approved normal-exit/recovery policy. Never replace a
pin with a newly observed hash to bypass a failure. STOP remains available after
disk/deployment/protection failures, with trusted control tools and session owner.
If STOP/state/receipt writes fail, retain the error and ask the maintainer to exit
under that policy; no clean finalization is inferred.

`ALIVE_ACK_PENDING` and `REQUEST_PUBLICATION_PENDING` mean the worker may still be
healthy. Reissue the pending challenge with the same nonce and investigate progress
without arbitrary age, event, size or monitoring-cadence limits. Reconnect retains
owned state under an exclusive lock. A new successful phase challenge uses a new
nonce. A conflicting controller, stale session or foreign STOP never passes.

Ordinary counted loss may coexist with safe acquisition, but invalidates precisely
the affected scientific history. `TELEMETRY_INCONSISTENT` means contradictory
counters; preserve the incident, deny affected integrity/firstness and use the
approved fault/STOP response. Health checks read metadata, not the complete raw
stream, and therefore cannot guarantee byte integrity or detect a contradiction
recorded only in another flush receipt. Postflight must authenticate every frame.
A healthy worker delay alone is not failure. No new attempt follows a crash.
Unexpected corruption outside the declared evidence boundary requires a maintainer
recovery decision; never restore over protected originals.

## Outcome definitions

| Outcome | Evidence required; allowed conclusion |
|---|---|
| Qualified target first processing | Positively identified target birth/publication after qualified empty reset/cold epoch; complete relevant earlier history; unvisited decision; constructing map miss; original query and consumed descriptor; direct low-nibble sample; required real reserve and executed token store; consistent owner/allocation/epoch/native causal order. Report sample, construction, append and geometry separately. Later bypass corroborates but is not mandatory. |
| Already visited | Positive same-identity bypass plus earlier authenticated same-allocation/owner/epoch insertion. Without the insertion, report a positively identified bypass with unproven earlier insertion history. It is distinct from a map hit or aggregate reuse. |
| Narrower negative or inconclusive | No positively identified target, missing sample/generator, prerequisite skip, failed/omitted append, map hit, pre-arming birth or incomplete owner history. Report observed boundaries and unavailable evidence. Silence is not native absence and supplies no mask. |
| Faulted or ambiguous history | Loss, missing reset/retirement, ABA/collision, contradictory telemetry, worker/controller/guard/ACK/raw fault or partial finalization. Preserve useful authenticated prefixes while refusing precisely unsupported firstness; never fill gaps with pointer equality, proximity or simulations. |

Successful append or sampled mask does not prove complete/nonempty geometry.
One future process cannot establish retail frequency or universal reliability.
D5R stays OPEN until separately observed evidence answers its question. B1 remains
PARTIAL NATIVE COVERAGE and D5AA's historical gap remains unchanged.

## Technical appendix: pinned commands and receipts

These commands describe a future procedure. **Do not run live actions under P4.**
Use installed CPython 3.14 with `-B`, never `-O`. Run canonical repository scripts;
`review-tools` in staging are source snapshots, not a relocated installation.
Use a new output path for each receipt and the exact hashes in the final manifest.

```powershell
$py = 'C:/Users/User/AppData/Local/Python/pythoncore-3.14-64/python.exe'
$plan = '.local-work/d5ab/p4-package04/plan.json'
$planHash = '8bb356e6e5ce700d131b579bc40b4fb5c55f66788792da7487eaa38ac53a7e80'
& $py -B research/resource-retained-population/d5ab_p4_operations.py preflight --plan $plan --plan-sha256 $planHash --out .local-work/d5ab/B2-NEW-PREFLIGHT
```

A preflight snapshots all pre-existing sessions. It does not confirm current
Cloud settings or create permission. After a separate actual GO and main-menu
identity, the operator records a local identity-bound approval JSON containing
`authority: B2_EXPLICIT_MAINTAINER_GO`, plan/preflight hashes, absolute session,
identity hash and `one_process_one_load_one_direct_travel: true`. Retain the actual
maintainer instruction/initial GO as its provenance; JSON is not consent. Session
identity cannot exist before launch, so this binding follows the separately
approved launch and precedes any save load. No approval is generated by P4.

```powershell
# Every command in this block is a FUTURE LIVE ACTION, NOT AUTHORIZED.
$control = @('--session', $session, '--plan', $plan, '--plan-sha256', $planHash,
  '--preflight', $preflight, '--preflight-sha256', $preflightHash,
  '--approval', $approval, '--approval-sha256', $approvalHash)
& $py -B runtime/construction-winner/p4_controller.py start @control --out $newStartReceipt
& $py -B runtime/construction-winner/p4_controller.py request @control --out $newRequestReceipt
& $py -B runtime/construction-winner/p4_controller.py poll @control --out $newPollReceipt
# Only on the maintainer's STOP or approved proven safety-fault response:
& $py -B runtime/construction-winner/p4_controller.py stop @control --reason $actualReason --out $newStopReceipt
```

At main menu, loaded Lodge and arrival, request and poll a distinct fresh challenge.
If publication/ACK remains pending, retry that pending request, preserving nonce.
Each CLI exit releases its lock/handle, so a later invocation reconnects to the
same persisted owner. No timed watchdog unloads or kills the process.

After normal exit and disablement:

```powershell
& $py -B research/resource-retained-population/d5ab_p4_operations.py postflight --plan $plan --plan-sha256 $planHash --preflight $preflight --preflight-sha256 $preflightHash --approval $approval --approval-sha256 $approvalHash --session $session --out $newPostflightDirectory
```

Use that directory's `receipt.json` as the hash-bound postflight for the existing
[archive commands](../../../runtime/session-tools/README.md#archival-contract).
Create roots JSON with this exact raw session and finished private companion
receipts; seal/ZIP/verification outputs must be outside sealed roots. A failed or
crashed capture uses `PARTIAL_POSTFLIGHT` plus an explicit partial reason. Preserve
the original failure and every available byte. Stream verification is bounded;
the scientific reader materializes events and may require additional memory for
larger captures. A reduction failure is retained, not an authorization to trim raw
evidence or retry gameplay. Future live approval must name final plan/card/package
hashes and the actual retained operational/scientific limitations.


## Operator setup template for a separately approved attempt

The following is a **future procedure, NOT AUTHORIZED by P4**. It makes the
appendix variables concrete; use the single approved attempt label. If a label
already exists, stop and resolve it rather than incrementing an attempt or retrying
launch. Receipt GUIDs distinguish observations within the same approved attempt.

```powershell
Set-Location 'D:/Projects/starfield-outpost-research'
$py = 'C:/Users/User/AppData/Local/Python/pythoncore-3.14-64/python.exe'
$plan = (Resolve-Path '.local-work/d5ab/p4-package04/plan.json').Path
$planHash = '8bb356e6e5ce700d131b579bc40b4fb5c55f66788792da7487eaa38ac53a7e80'
$attempt = 'B2-APPROVED-001'
$preDir = Join-Path $PWD ".local-work/d5ab/$attempt-preflight"
$notes = Join-Path $PWD ".local-work/d5ab/$attempt-notes"
if (Test-Path $notes) { throw 'Existing attempt notes; do not reuse' }
New-Item -ItemType Directory -Path $notes | Out-Null
function ReceiptPath([string]$phase) {
  Join-Path $notes ($phase + '-' + [guid]::NewGuid().ToString('N') + '.json')
}
function Pin([string]$path) { (Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash.ToLowerInvariant() }
& $py -B research/resource-retained-population/d5ab_p4_operations.py preflight --plan $plan --plan-sha256 $planHash --out $preDir
if ($LASTEXITCODE -ne 0) { throw 'Failed offline preflight; no launch' }
$preflight = Join-Path $preDir 'receipt.json'
$preflightHash = Pin $preflight
$pre = Get-Content -Raw -LiteralPath $preflight | ConvertFrom-Json
```

After a separate actual GO, the maintainer installs/enables/launches exactly once
and stays at main menu. Record the actual approval text and its plan/card/package
hashes in the notes directory. Then select the newly created session, refusing
multiple or absent candidates:

```powershell
# FUTURE main-menu read/binding, NOT AUTHORIZED now.
$liveRoot = Join-Path $PWD '.local-work/d5x/live'
$newSessions = @(Get-ChildItem -LiteralPath $liveRoot -Directory -Filter 'session-*' |
  Where-Object { $_.Name -notin $pre.existing_sessions })
if ($newSessions.Count -ne 1) { throw 'Ambiguous or absent new session; do not load save' }
$session = $newSessions[0].FullName
$identityFile = Join-Path $session 'identity.json'
$identityHash = Pin $identityFile
$approval = Join-Path $notes 'identity-bound-approval.json'
# This record transcribes the prior actual GO; it cannot create permission.
$approvalValue = @{
  authority = 'B2_EXPLICIT_MAINTAINER_GO'
  plan_sha256 = $planHash
  preflight_sha256 = $preflightHash
  session = $session
  identity_sha256 = $identityHash
  one_process_one_load_one_direct_travel = $true
  actual_maintainer_instruction = 'TRANSCRIBE THE ACTUAL SCOPED GO HERE'
}
if ($approvalValue.actual_maintainer_instruction -eq 'TRANSCRIBE THE ACTUAL SCOPED GO HERE') {
  throw 'Actual maintainer GO must be recorded before creating approval'
}
$approvalText = ($approvalValue | ConvertTo-Json -Depth 5) + "`n"
$stream = [IO.File]::Open($approval, [IO.FileMode]::CreateNew)
try {
  $bytes = [Text.UTF8Encoding]::new($false).GetBytes($approvalText)
  $stream.Write($bytes, 0, $bytes.Length)
  $stream.Flush($true)
} finally { $stream.Dispose() }
$approvalHash = Pin $approval
$control = @('--session', $session, '--plan', $plan, '--plan-sha256', $planHash,
  '--preflight', $preflight, '--preflight-sha256', $preflightHash,
  '--approval', $approval, '--approval-sha256', $approvalHash)
$newStartReceipt = ReceiptPath 'main-menu-start'
& $py -B runtime/construction-winner/p4_controller.py start @control --out $newStartReceipt
```

At each main-menu, Lodge and arrival checkpoint, set `$phase` to that checkpoint,
record the maintainer's statement and observation bounds in a companion note,
then use the following. Read the returned state before proceeding. Pending
publication/ACK uses the same command again with a new output receipt; it does
not permit a save load or travel. A successful challenge clears its nonce so the
next phase gets a fresh one.

```powershell
# FUTURE LIVE checks, NOT AUTHORIZED now.
$phase = 'main-menu' # Later: 'loaded-Lodge' or 'arrival'; no new travel implied.
$newRequestReceipt = ReceiptPath ($phase + '-request')
& $py -B runtime/construction-winner/p4_controller.py request @control --out $newRequestReceipt
$newPollReceipt = ReceiptPath ($phase + '-poll')
& $py -B runtime/construction-winner/p4_controller.py poll @control --out $newPollReceipt
```

The following block is separate from ordinary phase checks. Use it only after
the actual maintainer STOP at arrival, or the separately approved proven-fault
response. Never issue it as part of the main-menu or Lodge checkpoint.

```powershell
# FUTURE LIVE STOP, NOT AUTHORIZED now.
$actualReason = 'RECORD THE ACTUAL STOP INSTRUCTION OR SAFETY INCIDENT'
$newStopReceipt = ReceiptPath 'stop'
& $py -B runtime/construction-winner/p4_controller.py stop @control --reason $actualReason --out $newStopReceipt
```

STOP after arrival remains maintainer-directed. After confirmed normal exit and
disablement, perform the exact postflight and archive procedure below. Only
`PASS_POSTFLIGHT` can be sealed COMPLETE; for `PARTIAL_POSTFLIGHT` append
`--partial-reason` with the real incident. A `CHECK_ERROR`, unknown process exit or
nonquiescent source requires resolution before sealing, never a fabricated receipt.

```powershell
$postDir = Join-Path $PWD ".local-work/d5ab/$attempt-postflight"
& $py -B research/resource-retained-population/d5ab_p4_operations.py postflight --plan $plan --plan-sha256 $planHash --preflight $preflight --preflight-sha256 $preflightHash --approval $approval --approval-sha256 $approvalHash --session $session --out $postDir
$postflight = Join-Path $postDir 'receipt.json'
$postflightHash = Pin $postflight
$archiveDir = Join-Path $PWD ".local-work/d5ab/$attempt-archive"
New-Item -ItemType Directory -Path $archiveDir -ErrorAction Stop | Out-Null
$roots = Join-Path $archiveDir 'roots.json'
$rootsValue = @{
  raw = @{ path = $session; kind = 'raw-capture' }
  notes = @{ path = $notes; kind = 'private-receipt' }
  preflight = @{ path = $preDir; kind = 'private-receipt' }
  postflight = @{ path = $postDir; kind = 'private-receipt' }
}
[IO.File]::WriteAllText($roots, ($rootsValue | ConvertTo-Json -Depth 5), [Text.UTF8Encoding]::new($false))
$seal = Join-Path $archiveDir 'seal.json'
$zip = Join-Path $archiveDir 'capture.zip'
$created = Join-Path $archiveDir 'created.json'
$verified = Join-Path $archiveDir 'verified.json'
& $py -B runtime/session-tools/archive.py seal --input $roots --sha256 (Pin $roots) --postflight $postflight --postflight-sha256 $postflightHash --out $seal
& $py -B runtime/session-tools/archive.py create --input $seal --sha256 (Pin $seal) --archive $zip --out $created
& $py -B runtime/session-tools/archive.py verify --input $seal --sha256 (Pin $seal) --archive $zip --archive-sha256 (Pin $zip) --out $verified
```

Check each command's exit/result before the next. Finish all notes and scientific
outputs before sealing; if notes change afterwards, retain the old seal and make
a new seal/archive with new paths. Never add outputs inside sealed roots. Retain
raw originals and independently reconstruct selected members using the shared
archive contract and their exact sealed hashes. This procedure grants no upload,
raw retirement, retry, publication or protected-original restoration authority.
