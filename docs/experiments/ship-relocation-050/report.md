# Ship relocation observer 0.5.0 — offline qualification

2026-10-13, Australia/Sydney. SOR-EXP-0031 / SOR-EV-0039 continuation.
[Invoked brief](../../implementation-briefs/README.md#archive-lookup) (`implementation-briefs.zip :: docs/implementation-briefs/CODEX_BRIEF_SOR_ship_relocation_native_grid_observer_integrated.md`),
[frozen contract](contract.md), [native design](design.md),
[prospective integrated card](run-card.md), [review package](review.md).
Authored material REVIEW-REQUIRED; binaries/raw/private/native exports LOCAL-ONLY.

|Element|Result|
|---|---|
|Question|Can an offline-qualified observer capture naturally reached, identity-bound travel/landing/grid evidence and a separate Workshop oracle under one executable procedure?|
|Best-supported answer|The separately versioned 0.5.0 build passes disposable engineering qualification and packages a DLL-only Vortex payload. It adds source-backed travel request/decision and command handoff evidence to retained landing marker/native-grid capture, with a separate natural Workshop center/grid channel. Independent final verdict is **ACCEPT**, recorded verbatim with limits in independent-review.md.|
|Confidence|PROVEN for tested fixture transport/byte integrity and pinned on-disk contracts; STATIC for native path interpretation. No new RUNTIME or SAVE semantic finding.|
|Coverage|Pinned retail 1.16.244.0 ABI/code windows, original synthetic callback/route/travel/worker fixtures, 22 new schema 5 adverse tests, retained 030/040 regression tests. 17DEC70 dispatch is observed directly; other producers may lack that upstream binding.|
|Evidence|qualification-03/build.json, all listed logs and raw fixture/session evidence; sources.csv, unchanged 6241-path protection snapshot and verified review patches.|
|Limits|Retail runtime compatibility/reachability, nonzero native/carry evidence, marker creation, applied ship assignment, asynchronous command join, and full durable Workshop equivalence remain NOT TESTED/UNKNOWN.|
|Next step|Single combined maintainer review of exact hashes, qualification, independent verdict and full card before Vortex deployment and one defined Save25/local-control/new-Kreet-landing sequence. No live authority in this assignment.|

## Exact build and runtime dependencies

All artifact paths below are relative to D:/Projects/starfield-outpost-research.

|Artifact|Path|SHA256|
|---|---|---|
|DLL|.local-work/native-oracle-050/builds/qualification-03/SorNativePositionOracle.dll|b75b7889966a76e84059349acea869482b027f6e3afce70e53e2f5d2d5a483f0|
|Vortex ZIP|.local-work/native-oracle-050/builds/qualification-03/SorNativePositionOracle-0.5.0.zip|7741c88dd69fca63773e42f291334df4d251dabdaf5dee1a5dcf3b92ecd0f15d|
|Build/source/dependency/tool receipt|.local-work/native-oracle-050/builds/qualification-03/build.json|d7b1bf845bbdd770f1088e8d59c51409d24312fe8fdadac4b7857b0d7eaca501|

Source is runtime/native-oracle-050. Build uses installed CPython 3.14.3,
MSVC19.51.36256.0/MASM/link 14.51.36256.0 and vcvars64 from Visual Studio18.9.0;
exact tools and hashes are in build.json and compiler logs. Compiler warning C4324
reports intentional Environment alignment padding, not a failed ABI assertion.
No downloaded compiler/dependency. Reproduce from repository root using:

```powershell
$py = 'C:/Users/User/AppData/Local/Python/pythoncore-3.14-64/python.exe'
& $py -B runtime/native-oracle-050/build.py --name NEW-EXCLUSIVE --sfse 'C:\Users\User\AppData\Roaming\Vortex\starfield\mods\SFSE 106 0.2.21 2026-06-11T15-06Z F5ipYCCxI\sfse_1_16_244.dll' --vcvars 'C:\Program Files\Microsoft Visual Studio\18\Community\VC\Auxiliary\Build\vcvars64.bat'
```

The ZIP CRC/member/duplicate/content checks pass. Its Data/SFSE/Plugins contains
only SorNativePositionOracle.dll. ResearchNotices contains project GPL and
unchanged SFSE MIT notice plus package readme; these are not runtime essentials.
Imports use Windows KERNEL32/bcrypt/API-set CRT plus installed MSVCP140,
VCRUNTIME140/VCRUNTIME140_1/UCRT. All external system runtime paths/hashes and
actual dumpbin imports are pinned in build.json; none is bundled or deployed.
No neighboring TXT/config/README/manifest is consumed. Effective deployed DLL
and loaded identities still need future runtime preflight; not tested here.

## Actual checks and preserved failures

Primary evidence root: .local-work/native-oracle-050/builds/qualification-03.
Tests execute original disposable processes only, never Starfield/SFSE/native
retail instructions. Production worker tests copy pinned guard windows into
sparse private memory as data, patch those private copies, and do not call them.

|Qualification|Actual result / primary receipt|
|---|---|
|Callback/transport/patch regressions|520 checks PASS; qualification.txt and fixtures. Full integer/stack return channels, 8GPR/10XMM nonvolatile sentinels, FP/LastError, nesting/concurrency, C++/SEH, invalid reads, queue publication/loss/depth, all-preimage gate, real rollback failure/conservative residency, control/disk/write/flush, STOP/inert callbacks.|
|Q helper regressions|240 checks PASS; branch-qualification.txt. Twelve actual wrapper cases through schema/hash/path decoder PASS; branch-decoder-qualification.txt.|
|Landing route/selected-reference capture|158 checks PASS; route-qualification.txt, route-events.bin. Branches, nonzero/negative synthetic in-place grid output, true selected ref/fresh descriptor linkage, nested/concurrent/exception/FP/STOP and invalid metadata.|
|New travel MASM contracts|112 checks PASS; travel-qualification.txt/travel-events.bin. Caller frame/params/decision channels, actual native request args/output, true route enclosing scope, explicitly unassociated handoff, nested/concurrent, C++/SEH, 8GPR/10XMM/FP/native effects, STOP/inert/unreadable.|
|Pre-READY safe-admission STOP|PASS; admission-qualification.txt/admission-stop. Actual await_admission waits while multiple fixture threads exist, emits waiting receipt, responds to STOP before READY/edit admission.|
|Production worker normal/no-hit|152/149 checks PASS; lifecycle-normal.txt/lifecycle-no-hit.txt and complete synthetic sessions. Raw/journal/health/nonce/retirement, 21 private edits/19 relays and joined normal process return. No-hit stays distinct from failure.|
|Production writer/guard failure|123/125 checks PASS; lifecycle-writer-failure.txt/lifecycle-guard-failure.txt. CREATE_NEW failure/real edit mismatch stop admission and preserve explicit failure, no false retired receipt; disposable restoration checked.|
|Offline inspectors|30 generic +6 branch +23 route +22 schema 5 tests PASS, inspection-tests.txt/branch-inspection-tests.txt/route-decoder-tests.txt/capture-inspection-tests.txt. Corruption, missing/unpaired/wrong ancestry/kind/thread/racy identity, stale inputs, synthetic boundaries, wrong ready/health counters/tails, pre-READY STOP and historical delay policy.|
|Actual schema 5 analysis CLI|analysis-normal.json/analysis-no-hit.json show complete synthetic instrumentation with distinct early-return/no-hit reachability; analysis-guard-failure.json is incomplete. No native equivalence promoted.|
|Build/protected/source identity|All 6241 protected paths unchanged before/after build, including active manual saves/controlled archives, old observer sources/DLL/ZIP/raw fixtures and frozen inputs; all source hashes stable during final build. C: and D: exceed 40 GB plus reserves.|

Failed attempts remain local, not overwritten. Specialist-tests-01 compilation
found C2712 in an interim primary selector wrapper; snapshot helpers were moved
outside the SEH function and specialist-tests-04 passes 112. Build qualification-01
passed its then-current fixtures but source changed during ongoing review; final
source-stability assertion failed, so its ZIP is not the reviewed candidate.
Qualification-02 stopped at a retained historical test expecting permanent
heartbeat-gap rejection. The new brief forbids cadence-only termination; the test
was prospectively corrected to require diagnostic-only historical delay while
retaining fresh-current-health, corruption/loss/counter checks. Qualification-03
passes without source change. No old result or old 040 test was rewritten.

Independent reviewer objections also led to rejecting detected ref races, strict
helper→route ancestry, Q kind whitelisting, schema 5/Workshop/travel entered counts,
and pre-READY STOP recovery. [Review closure](review.md) identifies exact fixes
and adverse evidence. All remain within the original engineering authority.

## Scientific and operational boundaries

Raw grid inputs and actual native in-place results are preserved by invocation,
not regenerated or tuned. Generic marker output is not compensated Workshop
position. 0.5.0 captures a separate callback/center/grid chain, but the frozen 23
predictions are still unchanged: inputs SHA2569fe2924ff7bc444714fbab685893b8d8e0572dc2c7aad96cbd06de8aac93ad91;
predictions SHA256a8a7402697ed866a3410d4bd58796de513c7ca11f89e770a80deb5a8651a0487.
Identity qualification uses actual ordinary base/concrete extra-bc bytes and
native operands; full saved-to-loaded frame/restoration validation is manual
scientific work, never automatically granted by numeric equality. Nonzero/carry
fixture transport tests do not supply new native nonzero/carry observations.

The screenshot table is human-supplied, with character provenance explicit and
one advance Save25 instruction. Menu parsing remains separate near-term backlog.
Local travel is a control, then one previously unvisited accessible Kreet landing
and ordinary travel to SOR-003; optional coordinated new checkpoint only after
LZ-new. No old LZ2/3/4 assumption, event target or forced hit.

Implementation integrity is offline-qualified; scientific acquisition/native
compatibility is NOT TESTED; game target survival/restoration is NOT APPLICABLE
(no game operation); authority compliance is offline-only. Hooking changes timing
and execution. Actual worker/write/guard/disk/loss failures and operator STOP are
hard controls. Historical heartbeat delays are disclosed and current health is
re-established with fresh ACK; no arbitrary session/volume/cadence/response limits.
No deployment, game launch/attachment, save/config edits, staging/commit/push,
third-party incorporation, new licence basis, contact or external disclosure.
