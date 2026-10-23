# C2B Phase B: one corrected execution-context retry

2026-10-23, Australia/Sydney. The maintainer directly instructed:
“After postflight is finished let's make another attempt as the unrestricted user.”
This authorizes one additional disposable process after the first attempt's
successful postflight. It does not authorize further retries.

The [original approved card](run-card.md), SHA-256
`f24ce623a5352d58db33964a65a606d0eabb6f7ec00e5ce9a7f4e749d8df5b4a`,
continues to govern scientific scope, exact game/save/Workshop identities,
breakpoints, startup checks, natural actions, finite fallback, STOP/disposal,
protected-save policy, postflight and separate recovery authority.
No collector, fixture, algorithm, save or configuration change is proposed.

## Preserved failure and correction

The first process, PID 27356, reached the main menu according to the operator.
The sandboxed collector failed at `DebugActiveProcess` with error 5, access
denied, before SESSION/startup arms or samples. Its fatal cleanup attempted
disposal; the operator reported exit and the process was subsequently absent.
The actual target exit code and cleanup API result were not recorded. No save
load, travel, Build Mode or scientific evaluation occurred. This is an
INCOMPLETE acquisition, not a negative source-context finding.

The previous successful C2A dispatch receipts used an ordinary unrestricted
user collector. This attempt used a sandboxed collector against an ordinarily
launched game. That execution-context difference is the strongest supported
explanation for access denial; the exact Windows token restriction is not
established by error 5 alone. Synthetic same-context targets did not qualify
this cross-context attachment. The implementer records this dispatch mistake.

Postflight for attempt01 exited 0: 98 protected live saves, all 271 historical
backups, 12974 protected evidence entries, installed/configuration and Steam
checks passed. No save changes were observed. The 444-file lossless partial
archive retains the original failure and companion receipts, SHA-256
`a20e9517e03993cea4d45265a40a0efef9f7b2a3c010e6636f7acacfbcaacf8e`.

## Retry sequence

1. Obtain independent review of this narrow addendum. Keep Steam Cloud disabled
   under the maintainer's current confirmation. Confirm no Starfield process.
2. Use the unchanged `transient-build01`. Fresh qualification writes
   `pilot-qualification02`; fresh full preflight writes `pilot-preflight02`.
   Both must pass every original guard before launch.
3. Create `pilot-approval02.json` with the verbatim initial approval and retry
   instruction, original `card_sha256`, this addendum's `retry_card_sha256`,
   unchanged build and fresh preflight hashes, Cloud confirmation and `used:false`.
   The collector preserves the additional addendum hash in its configuration;
   its existing single-use gate still binds the original card/build/preflight.
4. Record fresh dispatch UTC and launch exactly one new process through the
   ordinary Steam URI. Dispatch both launch and collector as the ordinary
   unrestricted signed-in user, without administrator elevation, privilege
   enabling or security changes. Record exact PID/start UTC and execution context.
5. At the main menu, before save load, run the original `collect.py` command with
   approval02, preflight02, the exact new PID/dispatch UTC and new output
   `retail-attempt02`. Require SESSION and verified startup hardware-register
   readbacks before instructing Save52 load. If attachment fails again, preserve
   and close this attempt; no third process or automatic retry is authorized.
6. Follow original steps 8–9 exactly: Save52, direct Carinae outpost travel,
   actual Build Mode once; only one same-outpost exit/re-entry fallback if needed.
   No placement, movement, deletion, reload, retarget or cache manipulation.
   Stop on useful transfer or the original explicit safety/action conditions.
7. After confirmed process exit, run original postflight with preflight02 and
   output `postflight-attempt02.json`. Preserve failure/success dimensions,
   archive losslessly, analyze only complete evidence, and obtain independent
   scientific/editorial review and verified diffs before returning.

The original healthy-run continuation policy and memory/queue safety bounds
remain unchanged. No arbitrary elapsed-time or capture quota is introduced.
Save recovery, another session, integration, staging, commit, push and publication
remain separately gated.
