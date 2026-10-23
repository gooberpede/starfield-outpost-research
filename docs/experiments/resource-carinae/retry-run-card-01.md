# C2A Phase B retry 01: actual Build Mode trigger

2026-10-23, Australia/Sydney. This addendum prospectively authorizes only the
maintainer-requested corrected retry after independent review and fresh successful
preflight. It preserves the [original card](run-card.md) unchanged. No additional
retry, retargeting, Phase C interpretation, configuration change, publication or
Git mutation is authorized.

## Reason and authority

Attempt01 attached to the pinned Steam-launched PID 24528 and armed 99 startup
threads. It recorded zero breakpoint samples and no LOSS/error records. After
the operator initially reported Build Mode complete, the collector received the
card's bounded no-hit STOP and the game exited with code `0xc1d0`; controller
exit was 0. The operator then corrected the action: “Sorry, my fault: I opened
the scanner but not Build Mode”, and explicitly requested, “Can we try again?”

The first attempt is **SCANNER ONLY — BUILD MODE NOT EXECUTED**. It does not
test the intended Build Mode trigger and establishes neither native Iron absence
nor failure of the qualified collector. Preserve both the original report and
correction, raw events, zero-capture accounting and authorized disposal. Do not
silently revise the historical sequence or blame a native cache path.

The original authorization remains the maintainer's approval of the Phase B
run card subject to preflight, with Steam Cloud confirmed disabled. The later
explicit retry request supplies authority for one further fresh process/session
with the corrected action. Independent review must accept this addendum before
that launch. The collector, target/site, instruction guards, useful-stop rule,
read/queue budgets and safety boundaries are unchanged.

Attempt01 postflight found zero live/backup save, definition or configuration
additions, changes or deletions. All 254 Steam remote files and remotecache bytes
also match their prelaunch inventory. No restore or active-save change occurred.
The full protected-content audit and fresh preflight must still pass before retry.

## Exact inputs and commands

Reuse only the original card's exact Starfield 1.16.244.0 EXE, installed-definition
pins, Save52/HIST-0267 hash, Carinae Workshop identifier and build05. The build
manifest SHA-256 remains
`42ecda7762331206c80efb650db0c02511673c7baed9e90224d6aa4fe4c0a6fd`;
controller SHA-256 remains
`3efbec07288bcba47df7151feeb5a5c765433d1c135caa1953c76cf195311f50`.
The existing build's exact source and binary pins must match; no rebuilding or
instrumentation change is part of this retry. Never use the old consumed approval.

From repository root, with the exact installed interpreter:

```powershell
$c2aPython = 'C:/Users/User/AppData/Local/Python/pythoncore-3.14-64/python.exe'
& $c2aPython -B research/resource-carinae/qualify.py --build .local-work/resource-carinae/build05 --output .local-work/resource-carinae/pilot-qualification02
& $c2aPython -B research/resource-carinae/preflight.py --build .local-work/resource-carinae/build05 --qualification .local-work/resource-carinae/pilot-qualification02/qualification.json --name pilot-preflight02
```

Require all 40 fresh synthetic cases, guards, installed inputs, protected save/
independent-backup parity, scratch restore and both-drive 40,000,000,000-byte
free-space checks. Audit the declared Steam remote/sync paths again. Cloud remains
disabled under the operator's existing confirmation; do not change it or game
settings. Unknown sync paths or a changed protected input stop launch.

Retain a new `pilot-approval02.json` with original-card, build and fresh preflight
hashes, `status: GO_PHASE_B`, actual original/retry instructions,
`cloud_disabled_confirmed: true`, `used: false`, and this addendum's
`retry_addendum_sha256`. The wrapper enforces its existing original-card/build/
preflight gates; the operator/implementer must independently verify the additional
reviewed addendum hash before dispatch. No collector source change is required.

## One corrected natural session

1. After all audits and independent addendum acceptance, record fresh launch UTC.
   Launch once through ordinary Steam URI `steam://rungameid/1716740`, using the
   operator if necessary. Verify the new PID, later process start, exact image
   hash/path and main-menu state with no save loaded. No existing process qualifies.
2. Attach with the original card's ordinary unrestricted-user route if needed;
   no administrator elevation or privilege/security change. Pass the ISO timestamp
   as a literal argument through the established Python argument-list transport:

   ```powershell
   & $c2aPython -B research/resource-carinae/collect.py --retail-pilot --approval .local-work/resource-carinae/pilot-approval02.json --preflight .local-work/resource-carinae/pilot-preflight02/preflight.json --build .local-work/resource-carinae/build05 --pid PID --launch-utc UTC --output .local-work/resource-carinae/retail-attempt02
   ```

3. Require SESSION, correct instruction sites and startup arm/readbacks before
   loading the exact Save52. Travel directly to Carinae III-a Rc Fe and confirm
   body/site and existing Iron equipment. **Enter actual Build Mode:** construction
   catalogue/build controls must be visible. Opening only the hand scanner does
   not complete this action. Do not select or place an item, move/delete equipment,
   save, reload, invalidate a cache or force a native call.
4. Preserve naturally observed Iron and Alkanes/Rothicite control evidence. The
   unchanged collector may issue durable useful-evidence STOP during travel or
   before Build Mode completes. Record remaining actions as NOT EXECUTED; do not
   relaunch. If no useful event occurs after the one actual Build Mode entry,
   record the completed UI state and request the bounded no-hit STOP. Missing
   events are not absence. There is no event/time/operator-delay cutoff.
5. Remain attached through controlled disposal/exit. Preserve partial/LOSS/crash
   evidence. Hardware breakpoints, pausing and owned DR/RF changes remain declared
   interventions; no injection, byte patch, stepping or exception suppression.

## Postflight, completion and stopping

After process exit:

```powershell
& $c2aPython -B research/resource-carinae/postflight.py --preflight .local-work/resource-carinae/pilot-preflight02/preflight.json --output .local-work/resource-carinae/postflight-attempt02.json
```

Verify all protected content and sync/save paths, preserve changes before any
recovery decision, audit receipt framing/ACK/loss/EXIT/accounting, and seal a
stream-verified lossless local archive while retaining originals. No automatic
restore is authorized. The original recovery decision procedure applies.

Mandatory completion is: reviewed addendum and fresh preflight PASS; new process/
guard/READY admission PASS; corrected actual Build Mode action witnessed or an
earlier useful-stop reason explicitly recorded; useful evidence or an honestly
classified no-hit/incomplete result; postflight and durable evidence accounting;
editorial finalization, independent exact-snapshot review and verified complete/
task-only diffs. These are operational criteria, not a promise of an Iron hit.

Stop on the original safety/integrity/worker/STOP conditions. Any additional
retry or changed target needs a new reviewed card and fresh maintainer authority.
Retail Phase C still needs its separately explicit authorization; audit/describe
Phase B operational evidence without running the nonfitting scientific comparator.
