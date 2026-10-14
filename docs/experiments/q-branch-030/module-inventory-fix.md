# External inventory repair — cooperative receipts, unchanged 030

2026-10-12. [Direct user contract](../../implementation-briefs/CODEX_BRIEF_SOR_Q030_external_module_inventory_fix.md).
**Offline fix qualified; independent review ACCEPT.** The external
reader no longer attempts the denied cross-process module snapshot. It validates
the unchanged observer's complete emitted inventory plus fresh worker progress.
This is **cooperative observer evidence**, not independent external enumeration.
No game launch, deployment, live capture, elevation, native/plugin change or Git
mutation occurred. Future live behavior remains NOT TESTED; no retry authorized.

## Diagnosis and choice

Primary [failed attempt](live-attempt-01.md) traceback places the initiating error
at `CreateToolhelp32Snapshot(24,33636)` (SNAPMODULE|SNAPMODULE32), before the external
reader returned any modules. Limited creation-time query had succeeded; own-process
Toolhelp ABI qualification also passed. Thus this was not an empty loader list or
evidence of a conflicting overlay. The historical target/caller token, DACL and
protection context were not recorded. Exact Windows policy cause remains OPEN;
we cannot reconstruct it by querying an exited/reused PID. No OS privilege-policy
repair or successful retail cross-process query is claimed.

Routes considered: repairing ctypes layout is unsupported by the successful
own-interpreter test and WinError5 location; elevation, debug privilege, changed
process security, alternate memory APIs or retries would retain a privileged
cross-process dependency and exceed this offline task. Already-emitted 030 worker
inventories remove that dependency without changing native code. Source
[health.h](../../../runtime/native-oracle-030/health.h) polls `module_set()`, writes
`modules-N.jsonl` if changed, appends health and then acknowledges requests.
The stopped session retained eight numbered inventories, so the facility exists
in the exact reviewed DLL. Historical files do not retrospectively clear the run.

The original module_snapshot binding remains available only as a Python function
for the existing own-interpreter regression; production modules/worker commands
never call it. No automatic denial-to-empty fallback or alternate privilege retry.

## Changed external contract and safeguards

New locks explicitly pin `module_inventory_source=UNCHANGED_030_WORKER_COOPERATIVE_INVENTORY`.
Old lock 02 cannot silently select the new method. Before requesting anything the
reader checks pinned READY component/version/schema/event size/game/SFSE/DLL,
non-synthetic status and unchanged existing health/creation-identity validation.
Stopped/retired/failed/stale/changed-process sessions fail before publication.
Then it publishes a unique flushed nonce request and requires a fresh ACK within
15 seconds. The parent helper retains its 30-second total timeout, terminating only
its own inventory helper; failure blocks cues and caller requests STOP as before.

Reader requires contiguous bounded numbered inventory files and complete newline-
terminated UTF8 JSON rows, maximum 1 MiB/2048 rows. It rejects reparse/UNC/nonlocal
inputs, malformed/duplicate paths or bases, bad address/size fields, unreadable
worker hashes, on-disk hash drift and missing/wrong game/SFSE/candidate identities;
game base must match READY. Latest filename set and exact bytes must remain stable
across parsing/hashing and final fresh health check; READY must remain unchanged.
It records inventory path/digest/serial, pre-ACK serial, fresh nonce/ACK sequence,
PID/creation identity and explicit cooperative source/limits. Steam/NVIDIA overlays
remain accepted components, with hashes retained; specific competing instrumentation
still needs assessment, never blanket name rejection. No raw target memory is read.

**Coverage limit:** `module_set()` and `module_inventory()` are separate snapshots.
ACK contains no inventory digest or serial. A loader A→B→A race can leave emitted
inventory B associated with cached set A until another change. Stable files and
fresh ACK cannot prove exact ACK-time membership. “Complete” means a complete
emitted file/schema, not exhaustive atomic current-loader coverage. Disk hashes do
not prove loaded bytes. These limits are output fields and prospective procedure
terms, not hidden behind PASS. Owned-site/relay/admission guards remain mandatory.

## Actual offline qualification

`.local-work/q030-module-inventory-fix/` preserves initial baseline/before copies,
all 305 original pin values, logs, fixtures, old/new locks, audit and review receipts.
Only environment.py and prepare_lock.py are authorized mutable members of the
old pin set; original versions are preserved in before/. Original 030 sources,
ZIP/DLL/schema, frozen predictions, prior native capture and original save inputs
remain independently checked. Current external source hashes are in the new lock.

Sixteen focused tests PASS (`inventory-tests-04.log`), plus all 17 unchanged procedure
regressions (`procedure-regressions-01.log`). New tests cover cooperative success
while legacy external snapshot is forced to deny and asserted uncalled; new inventory
before ACK; old-contract rejection; missing/gapped/empty/partial/oversized inventory;
duplicates/missing identities/base/hash errors; nonlocal/reparse inputs; stale/stopped/
retired/failed/changed-process health; nonce timeout/late ACK; changes during parsing
or final health; and a **real bounded helper subprocess against this controlled
Python test interpreter**, with a synthetic local worker thread supplying receipts.
No test queries Starfield. Limited creation metadata is queried only for the test
interpreter; existing own-interpreter Toolhelp regression remains unchanged.

Actual offline audit PASS 310 pins, archive/member CRC/hash and native source/build
identities, required directories/process-name absence and source-save inventory.
Final lock 05 audit 02 records C caller-available 86400425984 and D138661482496
bytes; both exceed 40000000000. Earlier lock 04 audit 01 recorded 86401208320
and 138663170048 respectively; both audit receipts are retained.
Only Vortex folder marker remains in Plugins. A mistyped placeholder audit hash
was rejected before audit; corrected exact-hash invocation passed. Intermediate
locks/logs retained, not overwritten. Retired original session is separately tested
for rejection without process access/control writes; no production-mode replay pass.

Final prospective lock `.local-work/q030-module-inventory-fix/release-lock-05.json`,
SHA256 `d25345876fa33719e9aaccc3bd021e6efa131c375e357687ec8c369956cacd73`,
binds current external sources, all 31 attempt evidence members/manifest, prior 020
evidence, original lock 02, immutable 030 package and native source/frozen/protected
inputs. ZIP `bc51e7aad714880f419d07dab5dad1f8451934148ac5180564ee2a34891c627f`;
DLL `a2b0c90525928f287e2168f0d0c7150253f4d6c2089e79a8ab3b9925c9f5bfa6`.
No rebuild or native fixture rerun: native bytes unchanged, existing qualification
remains historical. The new tests qualify external behavior only.

Reproduce from repository root with existing Python:

```powershell
$py='C:/Users/User/AppData/Local/Python/pythoncore-3.14-64/python.exe'
& $py -B research/q-branch-030-procedure/test_inventory.py -v
& $py -B research/q-branch-030-procedure/test_procedure.py -v
& $py -B research/q-branch-030-procedure/procedure.py --lock .local-work/q030-module-inventory-fix/release-lock-05.json --lock-sha d25345876fa33719e9aaccc3bd021e6efa131c375e357687ec8c369956cacd73 audit --mode offline --out .local-work/q030-module-inventory-fix/offline-audit-reproduction-unique
```

## Matrix, future procedure and review

| Mandatory preparation criterion | Status | Evidence/limit |
|---|---|---|
|Initiating failure localized, historical cause confidence bounded|PASS|Original traceback; Windows/token cause OPEN; dependency removed, no OS repair claim|
|External fix with explicit provenance/freshness/identity/rejection|PASS|Cooperative reader, explicit new-lock contract and non-atomic coverage limit|
|Focused fixtures, real helper and old regressions|PASS|16+17 passing methods; no game queried|
|Unchanged 030/protected/frozen/prior evidence|PASS|310-pin actual audit, original source/build and capture SHA checks|
|Tool effects/dependencies/procedure consequences and limits|PASS|This report, tool README; no new dependency or third-party reuse|
|Complete/task-only diffs and independent ACCEPT|PASS|Independent ACCEPT on immutable submission; closure package consistency checked separately|
|Future retail inventory usability/loader coverage/live science|NOT TESTED|No launch/deploy/live capture authorized; exact ACK-time loader equality not promised|

This is a **prospective amendment** to [run card](live-run-card.md), not a new live
approval. For any separately approved new attempt, replace lock 02 with exact lock 05,
review the cooperative provenance/coverage change, retain per-phase fresh inventory
and assessment, then fresh phase ACK/health immediately before a cue. Modules command
also obtains its own ACK; it does not replace the monitor's independent liveness
challenge. Admission, disk floor, worker/writer/native guard checks, 13 edits/11
relays, 3-second external target/10-second maximum gap, 15-second health, STOP/drain,
one-session limits and operator-controlled gameplay remain unchanged. The old
failed attempt cannot be resumed. No experiment geography, saves or hook scope
is changed. Notice-location exceptions from attempt 01 remain recorded there; this
tool repair does not silently rewrite deployment/removal gates or grant their reuse.

Review package `.local-work/q030-module-inventory-fix/package.json` binds text file
attribution, status, exclusions, patch paths/hashes and exact forward applicability.
`.local-work/diffs/q030-module-inventory-fix-{complete,task-only}.diff` includes all
uncommitted text versus only this task from its actual baseline. Old uncommitted
procedure/attempt work is preserved separately; raw/native/save/build files remain
LOCAL-ONLY. Authored records REVIEW-REQUIRED, no publication authority. Primary
sources and project-derived methods are in [source ledger](module-inventory-fix-sources.csv).

Independent reviewer `/root/module_fix_review` accepted all six mandatory criteria
on immutable submission package SHA256
`df9dd824c2222c7ad344d4cfcb12cacaf50f0c6f5034bc5f5bcde9648df3caaa`.
The reviewer independently checked all 22 text hashes, complete/task-only patch
hashes and forward-applied bytes, 303 unchanged original protected pins, 27 native
source pins, all 310 lock 05 pins and unchanged HEAD/index. They inspected test source
and retained logs without rerunning experiments or querying processes. The actual
decision is retained in `.local-work/q030-module-inventory-fix/independent-decision.md`;
the accepted submission remains in `reviewed-submission/`. This closure changes
only this report to record that decision and clarify audit attribution; refreshed
patches/package receive a separate consistency review. Acceptance grants no live
qualification, integration, deployment, retry or publication authority.
