# P4 Python optimization correction and requalification

2026-11-01, Australia/Sydney. **Corrected P4 COMPLETE / ACCEPT. READY for independent maintainer review. B2 NOT AUTHORIZED.**

The maintainer explicitly reopened P4 under its existing correction/requalification
authority after an interpreter probe demonstrated that inherited
`PYTHONOPTIMIZE=1` disables safety assertions despite the documented `-B` invocation.
The assertion intended to reject optimization disappears too. The original
[READY decision](d5ab-p4-original-ready-decision-2026-11-01.md) is retained verbatim;
its interpretation as current readiness is superseded on this date. Original
P4/AB questions and criteria are unchanged. No historical receipt is rewritten.

## Adopted maintainer instruction

Reopen D5AB-P4 under existing correction and requalification authority. Address the
optimization vulnerability in operational entry points and B2 card. Adopt `-E -B`
where appropriate, implement guards effective under `-O`/`-OO`, and audit every
safety-critical assertion dependency. Test normal execution, inherited optimization,
explicit flags and failure before side effects. Preserve all protection, worker,
controller, evidence and authorization requirements. Rerun affected regressions,
obtain independent exact-source/procedure/package review and supply complete/task-only
diffs. Do not reinstate READY before full qualification. No deployment, Starfield,
B2, commit or push. This records the current chat instruction durably; it does not
add or waive acceptance criteria.

## Admission correction ledger (historical opening state)

Admission HEAD and source/index/old-package hashes are in
`.local-work/d5ab/p4-opt/baseline.json`. Working tree was clean. The original
Package04 remains historical and is not a live-ready package.

| Branch | Parent questions / criteria | Status | Evidence / next action |
|---|---|---|---|
| OPT-L01 | P4-Q1/Q2/Q3/Q5; AB-AC01/06/09/11/12 | Open | Trace operational entry/import/dependency graph and assertion calls/side effects. |
| OPT-L02 | P4-Q2/Q3/Q4; AB-AC06/07/08/09 | Open | Add early ordinary-conditional guards and environment-independent invocation; prove rejection before side effects. |
| OPT-L03 | P4-Q1/Q2/Q4; AB-AC03-08 | Open | Requalify affected actual worker, consumers, protection/archive and package correspondence; native DLL unchanged unless demonstrated necessary. |
| OPT-L04 | P4-Q5; AB-AC10-12 | Open | Screen/manual read, independent exact corrected package review and verified complete/task-only patches. |

At reopening all P4 controlling questions were INCOMPLETE for current readiness.
D5R remains OPEN; B1/D5AA/checklist/publication classifications remain unchanged.
Experiments use only fresh ignored disposable outputs, the current Python interpreter
and already authorized owned tools. Explicit optimization probes execute no game,
protected writes, deployment, network or process intervention. A guard failure must
occur before operational dependency imports, private/protected input reads, output creation
or control writes. No arbitrary experiment time/record/size quota is introduced.


## Answer and implemented correction

The optimization vulnerability is corrected and its affected technical suites
pass; independent original-contract/editorial review accepts the exact corrected
snapshot. Corrected READY is now reinstated for maintainer review only. The direct operational entries and relevant importable safety
modules now begin with an ordinary guard, before other imports or module work:

```python
import sys
if not __debug__ or sys.flags.optimize != 0:
    raise RuntimeError('Python optimization is forbidden; invoke with -E -B and no -O/-OO')
```

`__debug__` also detects optimized code objects executed by an unoptimized
interpreter. The guard itself contains no assertion. Commands in the corrected
[B2 card](run-card-d5x-b2.md), relevant shared procedures and actual P4 child
Python invocations use the explicit interpreter with `-E -B`; no `-O` or `-OO`.
`-B` alone is not an optimization control. The plan pins the interpreter binary,
expected flags and exact control/helper versions. Optimized invocation fails
before native API setup, private input/plan processing, session/control/receipt
creation or other operational effects. Source loading and stderr traceback are
not misrepresented as zero interpreter I/O.

Direct native process/time/image/wait queries and handle close formerly inside
assertions now execute through ordinary conditionals. The remaining assertions
include source/receipt reads and native liveness queries, not only pure
expressions. They are preserved as supported-mode invariants: optimization is
refused before they can run, and normal imports inherit the qualified process
mode. This avoids a broad change to the scientific consumer's validation logic.

## Assertion and dependency audit

The final machine audit at
`.local-work/d5ab/p4-opt-optimization-final02/receipt.json` inventories 378
assertions across 24 guarded operational/build/research-test modules, including
call-bearing assertion expressions and their line numbers. It tests the actual
early guard and rejects unexpected imports before refusal. Its 218 checks cover
explicit `-O`/`-OO`, inherited `PYTHONOPTIMIZE=1/2`, separately optimized code
objects, normal documented execution with inherited optimization and real CLI
pin rejection before session writes.

The actual full preflight additionally traces 29 project module executions and
153 assertion nodes, including private imported protection/archive dependencies.
These inventories overlap; their counts must not be added as unique assertions.
The retained execution inventory is
`.local-work/d5ab/p4-opt-preflight02/python-closure.json`. It records actual
interpreter `optimize=0`, ignored environment and disabled bytecode writes, and
source hashes. Static inspection of those executed modules finds no `compile`
or `exec` code-generation calls. The qualified guarded path includes:

- `operations` to `prepare_native`, native-reader/preservation imports, and the
  older collector/receipt modules imported by their qualification helpers;
- `full_preservation` to `remaining_inputs`, protected-save policy and sync,
  archive-backed preservation, cutover/access/retirement helpers;
- controller to worker lease/loss checks, and reader to schema-3/schema-4 reducers;
- archive to the shared path, pin, caller-available disk and inventory functions.

The private historical helpers are reached only after a guarded entry has
accepted normal execution. Their standalone historical CLIs are not newly
qualified for optimized execution. In particular, old `-B` command arrays in
cutover metadata are not executed by this full-preservation path. No blanket
claim is made about every Python program in the repository. Measured closure
exposed eleven previously unpinned protection helpers; the corrected package
includes and hashes all 29, plus the separately used PE reader. Live phases retain
small checks and do not add full protected-save scans.

## Exact corrected package and preservation

The operator-facing ZIP is now [SorConstructionWinner-0.4.0.zip](d5ab-p4-package-naming.md),
a byte-identical versioned copy of the qualified install archive. The original
staging paths and plan/source pins below remain unchanged.

The offline candidate is `.local-work/d5ab/p4-opt-package02/`. Its manifest lists
100 staged members, 99 plan package pins, all 29 measured protection dependencies,
current interpreter/source versions, exact build inputs and native compiler inputs
separately. Frozen `review-tools` are source snapshots; execute canonical pinned
repository tools. Nothing is installed or enabled.

| Artifact | SHA-256 |
|---|---|
| Corrected package manifest | `7ca5e79ac1ea0e761fe02df8fbf6640ab6453578e63ea1f5de9b28222fbbdc44` |
| Corrected operating plan | `2de7f60692af850c34cafa46de4fefb4679c33ac77f3944eeecf94f175dddc70` |
| Corrected install-shaped ZIP | `9c7a4a4d220948b3dac877b783487abc8ec65be026117158e1e883c35592d2cf` |
| Native DLL, old/new/reproduced | `9d2f0bab159f3ec23186426fb4833eb645578d2a43612bb2e8def6b1af455dcc` |
| Corrected full preflight | `4bd2441da887db2386177c6440e840df2752378c69f2428621682f286e7afe53` |
| Measured final preflight closure | `cbe7d3d2e373fcbb6147194e719d107622193d648891b7b02559eef5fd2d6051` |
| Retained original READY decision | `7ac9bc7300217474584a8a61af1c29852c82656f5566a01215c2ea5a58470b03` |

A fresh 90-case native build and four-case reproduction have identical DLL bytes
to original Final04. All thirteen true native compiler inputs remain unchanged.
Six old Python support/orchestration files changed and the P4 controller is a
new support input relative to the original build. The former whole-21-input
unchanged-source assertion is not carried forward: new full source/build and
packaged-consumer identities are used. No hook RVA, guard, displacement, ABI,
queue, event layout or native field interpretation changes.

The exact corrected full preflight passes and equals original P4 preflight04 for
98 protected saves/backups, 39 definitions, 23 configurations, archive guards and
Save52 restoration-COPY hash. Both drives retain more than 40,000,000,000
caller-available bytes; exact values are in final accounting. Original saves,
backups, configs, definitions, raw captures and analysis databases are unchanged.
The prior strict historical missing-ZIP failure remains historical; current
archive-backed protected-input differences are zero. No original is restored.

## Requalification and reproduced failures

To reconstruct the final bundle, run
`research/resource-retained-population/d5ab_p4_package.py NEW-PACKAGE BUILD REPRO CLOSURE`
after the interpreter flags. REPRO is `.local-work/d5x/p4-opt-repro01`; CLOSURE is
`.local-work/d5ab/p4-opt-preflight01/python-closure.json`. Fresh full auditing with
module-execution inventory uses
`research/resource-retained-population/d5ab_p4_opt_provenance.py trace-preflight PLAN PLAN_SHA256 NEW-OUTPUT`.
Both commands are offline only and create exclusive outputs. Reproduction binds
current sources; an old manifest never clears a changed source. The retained
final accounting method below provides the final02 receipt selection explicitly.

Use installed `C:/Users/User/AppData/Local/Python/pythoncore-3.14-64/python.exe`
with `-E -B`, without `-O`/`-OO`. Every output label must be new. Receipt paths
below are relative to `.local-work/d5ab/` except the two build directories.

| Suite / command after interpreter flags | Result / exact primary receipt |
|---|---|
| `runtime/construction-winner/build.py p4-opt-native01` | 90 expected-exit cases PASS; `.local-work/d5x/p4-opt-native01/build.json`. |
| Same build recipe with `p4-opt-repro01 normal p3-positive-bypass p3-unwind-probe p3-store-access-fault` | Four PASS, same DLL; `.local-work/d5x/p4-opt-repro01/build.json`. |
| `research/resource-retained-population/d5ab_p4_opt_qualify.py NEW-OUTPUT` | 218 PASS / 24 modules; `p4-opt-optimization-final02/receipt.json`. |
| `d5ab_p3_reader.py BUILD NEW-OUTPUT` | 133 chronology/damage checks PASS; `p4-opt-reader01/receipt.json`. |
| `d5ab_p1_qualify.py BUILD NEW-OUTPUT --original-case-regressions` | 316 checks PASS, including full B1/schema-2/schema-3 compatibility; `p4-opt-compat01/receipt.json`. |
| `d5ab_p3_native_qualify.py BUILD NEW-OUTPUT` | 257 native operand/state checks PASS; `p4-opt-native-controls01/receipt.json`. |
| `d5ab_p3_bridge_abi.py BUILD NEW-OUTPUT` | Thirteen exact-object checks PASS; `p4-opt-abi01/receipt.json`. |
| `d5ab_p4_opt_legacy.py OLD-SCHEMA3-BUILD NEW-CONSUMER-BUILD NEW-OUTPUT` | 54 unchanged original semantic oracles PASS; `p4-opt-legacy03/receipt.json`. |
| `d5ab_p4_controller.py --parallel BUILD NEW-LABEL` | 28 actual-worker cases PASS; `p4-opt-controller01/receipt.json`. |
| Historical `d5ab_p2_controller.py --parallel BUILD NEW-LABEL` in normal environment | 26 existing-controller cases PASS; `p4-opt-legacy-controller01/receipt.json`. Its unchanged historical test children are not B2 invocation commands. |
| Actual worker with inherited `PYTHONOPTIMIZE=2`, explicit `-E -B` | Positive health/STOP/finalization PASS; `p4-opt-inherited-worker01/receipt.json` and invocation/environment proof in `p4-opt-extra-regressions01/inherited-worker.json`. |
| `runtime/construction-winner/worker_health.py --qualify NEW-OUTPUT` | Nine own-thread controls PASS; `p4-opt-worker01/receipt.json`. |
| `d5ab_p4_admission.py NEW-OUTPUT` / `d5ab_p4_qualify.py NEW-OUTPUT` | 28 admission and 41 procedure/archive/owned-finalization controls PASS; `p4-opt-admission01/receipt.json`, `p4-opt-procedures01/receipt.json`. |
| `-m unittest discover -s runtime/session-tools -p test_session_tools.py -v` | 51 PASS; `p4-opt-shared01/receipt.json`, exact source pins and stdout/stderr retained. |

Script names without a directory in this table are below
`research/resource-retained-population/`. BUILD is
`.local-work/d5x/p4-opt-native01`; OLD-SCHEMA3-BUILD is
`.local-work/d5x/p2-native06`. New native/reader receipts bind all current hashes.
The legacy wrapper authenticates old captures/output snapshots, compares the
old/current reducer AST after removing only the exact guard/import, and executes
the original 54-oracle AST unchanged. It never edits the old packaged reducer or
pretends old capture bytes came from the new producer.

All controller cases preserve identity, worker death versus delay, ownership,
retry nonce, STOP, output/ACK/guard/disk faults, loss/telemetry and raw finalization
requirements. The 32,768-cell representative and burst native cases remain
lossless in their declared finite envelope. The unchanged queue/capacity/native
ownership proofs and old stress measurements remain scoped prior evidence;
Python guards do not establish universal throughput or retail behavior.

Failures are retained: the old legacy adapter correctly refuses changed consumer
hashes; the new wrapper initially mishandles Windows manifest separators and is
corrected in a new receipt; supplemental accounting first uses the wrong old/new
result key and then encounters two unavailable posthoc process queries. These
are not rewritten into passes. The final original subprocess wait/returncode
witnesses confirm exit for 146 recorded session identities. The two posthoc query
results stay UNKNOWN diagnostics and are not invented PID-reuse evidence. Future
unavailable retail process queries still fail closed. Declared native crash
controls preserve their expected survival failures separately from test PASS.

The consolidated technical readback is
`p4-opt-regression-summary03/receipt.json`, SHA-256
`3d87500a712a45930c172d2ff128a9748008503cfffc1f2b53695f36bb4c4c8c`.
Exact current package/guard/source/receipt/closure/protection correspondence is
verified by `.local-work/d5ab/p4-opt-final-accounting01.py` and its receipt.
The initial `p4-opt-provenance01` verifies its own intermediate source snapshot;
its fixed `optimization-final01` reference is not a final current-source claim.
Final accounting checks `optimization-final02` explicitly. All original P1
exports and 826 prior preservation records remain authenticated by the recorded
revalidation; no historical result is silently promoted.

## Current original-contract accounting

The [original questions and criteria](../../implementation-briefs/README.md#archive-lookup) (`implementation-briefs.zip :: docs/implementation-briefs/CODEX_BRIEF_SOR_RG2_D5AB_observer_remediation_live_readiness.md`)
and P4 contract retain their full wording. This table supplies the correction's
current evidence; the original matrix remains historical beneath its notice.

| Original criterion | Technical result / evidence | Final independent gate |
|---|---|---|
| AB-AC01 | PASS: clean baseline, exact interpreter/native/package pins, guarded offline scope, full preservation. | ACCEPT: exact independent review; closing metadata delta verified separately. |
| AB-AC02 | PASS: unchanged AB/P4 questions, original verdict retained, active correction ledger maintained. | ACCEPT: exact independent review; closing metadata delta verified separately. |
| AB-AC03 | PASS: unchanged native lifetime graph/compiler inputs; rebuilt positive bypass, collision/reuse/retirement and new consumer controls. | ACCEPT: exact independent review; closing metadata delta verified separately. |
| AB-AC04 | PASS: rebuilt actual token-store/sentinel/skip/fault witnesses and independent native memory oracles; no native semantics changed. | ACCEPT: exact independent review; closing metadata delta verified separately. |
| AB-AC05 | PASS: eighteen sites/seventeen unfiltered categories, resets/owner/source lifetimes and query/descriptor/sample joins preserved. | ACCEPT: exact independent review; closing metadata delta verified separately. |
| AB-AC06 | PASS: same native queue/writer and declared lossless envelopes; guarded disk/health/evidence checks and honest overload/telemetry refusals. | ACCEPT: exact independent review; closing metadata delta verified separately. |
| AB-AC07 | PASS: 90 native cases, current/legacy worker/controller suites, explicit optimizer and failure-before-effect controls. | ACCEPT: exact independent review; closing metadata delta verified separately. |
| AB-AC08 | PASS: 133/316/54 consumer/oracle regressions, original raw/schema history unchanged; no firstness after relevant loss/ambiguity. | ACCEPT: exact independent review; closing metadata delta verified separately. |
| AB-AC09 | PASS technical procedures: corrected `-E -B` card, new hash-bound package/closure and fresh full protection; no live authority. | ACCEPT: exact independent review; closing metadata delta verified separately. |
| AB-AC10 | PASS technical preservation: historical verdict/raw inputs intact, current inclusion/exclusions and exact hashes retained. | ACCEPT: exact independent review; closing metadata delta verified separately. |
| AB-AC11 | PASS: independent 218/28/41 controls and complete source/package/original-contract challenge. | ACCEPT: exact independent review; closing metadata delta verified separately. |
| AB-AC12 | PASS: exact editorial/manual/diff verification and independent acceptance. | ACCEPT: exact independent review; closing metadata delta verified separately. |

All AB-Q1–Q5 and P4-Q1–Q5 are COMPLETE within the original offline-readiness
scope. All twelve AB criteria and eight P4 criteria PASS with independent ACCEPT.
No original criterion is waived. The recommendation is READY for maintainer review;
this does not authorize B2. No offline correction branch remains open.

## Final question and P4 criterion status

| Question | Current status | Evidence / remaining gate |
|---|---|---|
| AB-Q1 | COMPLETE technical scope | Same native lifetime/source graph, rebuilt bypass/collision/retirement positives and refusals; new guarded current consumers. Independently accepted. |
| AB-Q2 | COMPLETE technical scope | Actual executed-store versus reserve/skip/fault and native order remain discriminated in current native/consumer suites. |
| AB-Q3 | COMPLETE finite offline scope | Native workloads, worker/transport/fault checks and optimization refusal pass; no universal lossless claim. |
| AB-Q4 | COMPLETE offline witness scope | Current 133/316/54 controls preserve positive chains and reject loss/identity/epoch/counter ambiguity; historical B1 unchanged. |
| AB-Q5 | COMPLETE offline readiness | Exact corrected bundle/procedure/card independently accepted. |
| P4-Q1 | COMPLETE offline readiness | Complete original-contract mapping and independent challenge accepted. |
| P4-Q2 | COMPLETE technical package | Current source, rebuilt/reproduced DLL, interpreter, all measured dependencies and final plan are hash-bound. |
| P4-Q3 | COMPLETE offline procedures | Normal/optimized/pre-effect controls, actual worker and fresh full protection/archival checks pass. |
| P4-Q4 | COMPLETE offline scope | New guarded consumers retain existing scientific discrimination and fail closed on invalid evidence. |
| P4-Q5 | COMPLETE offline readiness | Independent exact source/package/procedure/prose/diff and original-contract review ACCEPT. |

| P4 criterion | Current result | Evidence / remaining gate |
|---|---|---|
| P4-AC01 | PASS | Actual authorization, clean baseline, historical verdict retained and active correction ledger. |
| P4-AC02 | PASS | All AB questions/twelve criteria mapped and independently challenged. |
| P4-AC03 | PASS technical scope | Rebuilt native, exact current consumer/lifetime/identity/append/query/refusal controls. |
| P4-AC04 | PASS technical scope | Identical reproduced DLL, all current packaged consumers and interpreter/dependency pins; affected regressions pass. |
| P4-AC05 | PASS technical scope | Actual worker/controller26/28, faults, telemetry, raw/ACK and optimizer refusal tests pass. |
| P4-AC06 | PASS | Full protected equality, both-drive floors, restoration COPY, archive/owned STOP and source-version guards preserved. |
| P4-AC07 | PASS | Explicit guarded invocation and one-episode operator card independently accepted. |
| P4-AC08 | PASS | Independent exact-source/procedure/package/prose and complete/task-only delivery review ACCEPT. |

Shared 070/080 receipts remain historical; the changed shared-source hashes need
fresh reviewed pins before those separate adapters' future use. P4 does not
silently reauthorize or upgrade their old manifests.

## Active ledger update

OPT-L01 is resolved by the exact guard/assertion/dependency audit; OPT-L02 is
resolved by the ordinary guards, flags and failure-before-effect controls;
OPT-L03 is resolved by exact current requalification, full protection equality
and expanded package pins. OPT-L04 is resolved by exact-final editorial/manual
coverage, independent original-contract ACCEPT and verified delivery closure.
Science, engineering, editorial, process survival and publication remain separate dispositions.
Authored changes are REVIEW-REQUIRED; raw/private/binary material stays LOCAL-ONLY.
No new third-party code, licence acceptance, contact or external disclosure occurs.


## Independent acceptance and closing delivery

The implementation-independent reviewer accepts the frozen review01 snapshot:
all twelve AB criteria, eight P4 criteria and both sets of five questions pass
within their unchanged offline scope. It independently executes 218 optimization,
28 admission and 41 procedure controls, checks all 41 changed file hashes,
100 package members, 99 plan pins, the 29-module closure, original protection
equality and the full editorial/delivery coverage. The strongest dependency-chain
challenge is resolved by the early guard and measured pinned closure; no universal
standalone-helper qualification is claimed.

The full actual return is retained LOCAL-ONLY at
`.local-work/d5ab/p4-opt-independent-final-review01.md`.
Review01 delivery SHA-256 is
`814a68903e31dd8434d544605aba8025fe65ed55204617c2deb2c28381d5460d`;
both accepted review patches are
`cf1c7e5b8d857c96563eda31ec8ab82830bdf5df492b7531fea0b744e031f7a7`.
Closing changes record only status, tables, review and navigation metadata;
source, package, plan, native bytes and test receipts remain unchanged. Final
delivery and the narrow closing review are retained under
`.local-work/d5ab/p4-opt-delivery/final01/`. Canonical complete/task-only patches
are `.local-work/diffs/d5ab-p4-opt-complete.diff` and
`.local-work/diffs/d5ab-p4-opt-task-only.diff`.

Engineering, scientific-readiness, operational and editorial dispositions ACCEPT.
Retail SFSE admission and target scheduling remain untested future B2 outcomes.
D5R remains OPEN, B1 PARTIAL NATIVE COVERAGE, D5AA unchanged, publication ON HOLD.
No deployment, game launch, B2, staging, commit or push occurs.
