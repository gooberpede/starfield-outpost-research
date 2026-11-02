# D5AI prospective operator command correspondence

**NOT AUTHORIZED.** These commands describe a later separately approved episode.
Do not deploy, launch, load, travel or record under the offline D5AI brief.
Use canonical repository tools from `D:\Projects\starfield-outpost-research`;
frozen review-source copies are not executable replacements for that root.
The final bundle manifest supplies exact plan/source/receipt hashes. Hashing an
arbitrary replacement file is not independent verification of the reviewed file.

## Separate admission and control

Choose exactly one reviewed plan: Episode A or Episode B. Each needs its own
maintainer approval file matching that plan, card, Save52, exact action scope
and new session. The approval authority must be
`D5AI_EPISODE_A_EXPLICIT_MAINTAINER_GO` or
`D5AI_EPISODE_B_EXPLICIT_MAINTAINER_GO`, respectively. Historical B2 approval and
the offline preflight are insufficient. Do not manufacture an approval file.

In the following PowerShell templates `$plan`, `$planHash`, `$approval`,
`$approvalHash` and `$session` come from that separate reviewed decision and the
new actual process/session. Every output path must be fresh and outside sealed
roots. The cards determine the operator's finite gameplay actions; none is
automated by these helpers.

```powershell
$py = 'C:/Users/User/AppData/Local/Python/pythoncore-3.14-64/python.exe'
function Pin([string] $path) { (Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash.ToLowerInvariant() }
& $py -E -B research/resource-retained-population/d5ai_operations.py preflight --plan $plan --plan-sha256 $planHash --out $newPreflightDirectory
$preflight = Join-Path $newPreflightDirectory 'receipt.json'
$preflightHash = Pin $preflight
```

Preflight must pass before any later approved launch. Confirm Steam Cloud and
the intended profile separately; the helper does not change them. Bind the
actual new session at the main menu before the one Save52 load:

```powershell
& $py -E -B research/resource-retained-population/d5ai_episode.py start --plan $plan --plan-sha256 $planHash --preflight $preflight --preflight-sha256 $preflightHash --approval $approval --approval-sha256 $approvalHash --session $session --out $newStartReceipt
& $py -E -B research/resource-retained-population/d5ai_episode.py request --plan $plan --plan-sha256 $planHash --preflight $preflight --preflight-sha256 $preflightHash --approval $approval --approval-sha256 $approvalHash --session $session --out $newRequestReceipt
& $py -E -B research/resource-retained-population/d5ai_episode.py poll --plan $plan --plan-sha256 $planHash --preflight $preflight --preflight-sha256 $preflightHash --approval $approval --approval-sha256 $approvalHash --session $session --out $newPollReceipt
```

A healthy delayed request stays pending. Poll with fresh receipt paths; do not
invent a timeout or replace a pending challenge. Keep native lifecycle and
content-lifetime history continuous before load and travel.

## One-shot geometry and the A0 departure gate

At the card's arrival checkpoint, `$label` is A0, A1 or B0, naming one immutable
request. Invoke `arm` repeatedly with that same label and a fresh output receipt
path on each invocation. It advances the initial challenge, publication and
post-publication ACK through `GEOMETRY_CHALLENGE_PENDING`,
`GEOMETRY_ARM_PUBLICATION_PENDING`, `GEOMETRY_PUBLICATION_PENDING` or
`GEOMETRY_ARM_ACK_PENDING`. Do not change labels or publish another request.
File publication alone is pending. Wait for `GEOMETRY_ARMED` before the card's
one ordinary consumer action. `GEOMETRY_CAPTURED_BEFORE_ARM_ACK` means a natural
scan already consumed the request: inspect it without another query.

```powershell
& $py -E -B research/resource-retained-population/d5ai_episode.py arm --label $label --plan $plan --plan-sha256 $planHash --preflight $preflight --preflight-sha256 $preflightHash --approval $approval --approval-sha256 $approvalHash --session $session --out $newArmReceipt
```

After the permitted consumer action, invoke `geometry-poll` with fresh receipt
paths until its capture receipt exists. This command reads capture completion;
it does not advance the arming challenge and cannot replace repeated `arm`.

```powershell
& $py -E -B research/resource-retained-population/d5ai_episode.py geometry-poll --plan $plan --plan-sha256 $planHash --preflight $preflight --preflight-sha256 $preflightHash --approval $approval --approval-sha256 $approvalHash --session $session --out $newGeometryReceipt
```

For A0, obtain a fresh post-capture challenge through request/poll above. From
its authenticated ACK take `$nonce` and the captured `$snapshotId`. Read the
reviewed plan's checkpoint source-lock path/hash and candidate DLL hash; do not
substitute a newly generated lock. The read-only checker does not contact the
worker or issue another query:

```powershell
& $py -E -B research/resource-retained-population/d5ai_checkpoint.py $session --dll-sha256 $dllHash --snapshot $snapshotId --nonce $nonce --source-lock $checkpointSourceLock --source-lock-sha256 $checkpointSourceLockHash --out $newBaselineReceipt
```

Require BASELINE_PREFIX_QUALIFIED and current controller health before departure.
This authenticates complete A0 geometry and its source/frame/journal prefix
without requiring terminal finalization. It does not itself grant permission to
depart. Cached/no scan, missing attribution, journal cutoff, loss or partial data
ends the measurement honestly; no forced refresh or automatic extra travel.

## STOP, preservation and complete-content comparison

```powershell
& $py -E -B research/resource-retained-population/d5ai_episode.py stop --reason 'approved episode checkpoint complete' --plan $plan --plan-sha256 $planHash --preflight $preflight --preflight-sha256 $preflightHash --approval $approval --approval-sha256 $approvalHash --session $session --out $newStopReceipt
```

Poll owned STOP finalization using the same controller; preserve any pending or
failed result. Do not hot-unload or terminate the game. After operator normal
exit and disabling the exact candidate, perform offline postflight:

```powershell
& $py -E -B research/resource-retained-population/d5ai_operations.py postflight --plan $plan --plan-sha256 $planHash --preflight $preflight --preflight-sha256 $preflightHash --approval $approval --approval-sha256 $approvalHash --session $session --out $newPostflightDirectory
```

The actual postflight receipt supplies process_state, status and session root
to the unchanged [archive procedure](../../../runtime/session-tools/README.md).
Finish companion receipts first. Inventory the entire raw session and companion
roots, then seal/create/stream-verify outside those roots. PASS_POSTFLIGHT alone
can seal COMPLETE; use an explicit partial reason for PARTIAL_POSTFLIGHT.
Preserve original raw files and failed artifacts; no upload or cleanup deletion.

After authenticating both sessions and snapshot IDs, use the exact reviewed
reducer. Episode A uses its one session for both operands; Episode B uses A's
baseline session and the independent B session:

```powershell
& $py -E -B research/resource-retained-population/d5ai_reduce.py $baselineSession $comparisonSession --dll-sha256 $dllHash --before-snapshot $baselineSnapshotId --after-snapshot $comparisonSnapshotId --out $newComparisonReceipt
```

The output keeps complete normalized equality, native lifetime and prior storage
survival separate. Assess D5AI-PRED-01 using its original frozen criteria. A
failed or unavailable measurement cannot be converted into equality. No result
here approves a retry, another visit or the other episode.
