# D5X-B1 retail instrumentation preauthorization audit

2026-10-31, Australia/Sydney. [Original contract](../../implementation-briefs/CODEX_BRIEF_SOR_RG2_D5X_B1_preauthorization_audit.md),
[active ledger](d5x-b1-audit-ledger.md), [proposed amended card](run-card-d5x-b1.md),
[frozen schema](d5x-schema.md), [original offline qualification](d5x-report.md).

**The frozen candidate can support a discriminating one-load/one-travel B1
instrumentation test without a cold winner.** The existing scientific reader
alone cannot produce the required coverage report. A separate offline reporter
now authenticates prefixes, reports each site and validates ordinary paths before
considering any cold-state question. It leaves the DLL, ZIP, schema, sites and
packaged scientific reader unchanged. Independent scientific, engineering/
operational and editorial reviews return **GO-READY**. B1-AUD-Q1–Q3 are
**COMPLETE within the offline audit contract**. This permits considering a
separate B1 approval; it authorizes no retail action.

| Element | Supported answer |
|---|---|
| B1-AUD-Q1 | The exact candidate and amended card are suitable for separately considering the bounded retail instrumentation test; actual game admission and branch availability remain untested. |
| B1-AUD-Q2 | Positive site exercise and valid path correlation are reportable. Silence cannot perfectly distinguish nonexecution, loss or failed admission. The reporter marks those cases INDETERMINATE, including inseparable converter/normalizer silence. No native counters are invented. |
| B1-AUD-Q3 | The amended card specifies one Save52 load, one ordinary travel, fresh challenges/checkpoints, exact future writes, protection, STOP and separate full/partial/failure decisions. All live actions still require explicit approval. |
| Confidence/basis | PROVEN / STATIC for inspected fixed event semantics and guards; existing disposable RUNTIME observations plus DERIVED adverse controls qualify the offline reporting method. No new native process was executed. |
| Tested coverage | Fresh installed/package/source/guard/Save52 hashes, authentic existing sessions, missing-boundary/loss/crash/damage cases, warm-path contradictions and bounded-memory analysis. Exact results are below. |
| Unknown coverage | Retail loader/admission, actual native timing/rates, natural downstream path availability and asynchronous unwind behavior. A single trip may yield only partial coverage. |
| Parent and publication | Accepted D5X offline capability is preserved; D5R stays OPEN. B1/B2 NOT AUTHORIZED; publication/B6 ON HOLD. |

## Identity, provenance and unchanged candidate

`.local-work/d5x-b1-audit/identity01/identity.json` freshly verifies installed
Starfield 1.16.244.0, ESM, PlanetData, SFSE 0.2.21 and actual game-root loader.
All fourteen original 32-byte site windows/displaced instructions and six call
targets match their frozen guards. It checks every original build output and
source pin, the ZIP inventory and DLL bytes, and the packaged reader.

| Frozen input | SHA-256 |
|---|---|
| Starfield.exe | `7e9adb1414a8e1b325e5e1f097b9b17b78deb7eebeda37a333351a43a60f9d28` |
| Starfield.esm | `1dabed00c3f4282dd3bb54d2e9601e40b577d8742d078b7ccef203adbfef0da7` |
| PlanetData.ba2 | `2fb1fff5d8fc074718bf05022c099f3c87ef70e00050229b368ae7d680fbe5d5` |
| sfse_1_16_244.dll | `28c5bda41d9959c885efcb6e889de69e92767c80a1a66842d711d215f722f82b` |
| sfse_loader.exe | `16916c2ec47e31774e3d550609a1844fcb368b03060c03511891564b7f5f7526` |
| D5X DLL | `20160e2ccdf183c84baddae0214c0438eb471b3eb0ec34dee0632bb5880ddaeb` |
| Retail ZIP | `4dc510f1ed6aa283483d7de43d588cd78d28c5db30101f091245ca47ea3c4525` |
| Packaged scientific reader | `1251527e82e39ff597c9921bcc4dfd9c9211575856cc08f64a2490c024ee978a` |

The approved Save52 is exactly
`Save52_BA75E3CDM43616F205472616E_580743_20260818064541_319_15_4.sfs`,
16,411,136 bytes, SHA-256
`6b4a10084c7e752c31fd2de121a00850aaa2bf1decd700b437d7dccfcdbc82e8`.
Its active Documents bytes match the designated policy; they were hashed, not
parsed, loaded, copied or changed. This is not a fresh full protection/Cloud/
backup preflight. That remains mandatory under separate B1 approval.

The original `.local-work/d5x/compatibility01.json` is immutable. Its original B1
card pin is historical after this proposed amendment. Audit identity receipts
compare that old card with HEAD bytes and bind the amended card separately.
The final audit manifest binds the new card/reporter/tests and unchanged binary
pins. Existing SFSE permission/notices remain sufficient; no new third-party code,
dependency, native interface or package is incorporated.

## Fourteen-site acceptance matrix

All addresses here are module-relative **RVAs**, not runtime addresses. Add the
observed module base only for this exact build. In every row, READY plus matching
identity proves installation/guarding, not execution. Only authenticated records
prove the listed positive exercise. Record counts are witness counts, not invented
native call counters. Parsed unacknowledged tails and aggregate losses are reported
separately. Missing records never prove zero native executions.

| Site / RVA | Native execution condition and available witness | Correlation / semantic prerequisite | Silence and remaining limit |
|---|---|---|---|
| 0 / `0x79f860` | Provider wrapper enters: Entry 1; normal/exception closeout: Returned 9. Entry `a` is original Int2 pointer; request is signed copy. | Unique invocation, thread/parent, ProcGen, request, epoch/status; entry precedes selection. Returned need not exist in a durable sample prefix. | No provider record means NOT OBSERVED. Missing entry/return can be admission, unfinished invocation or crash; not proof of no call or hook failure. |
| 1 / `0x79fa90` | Actual cursor source load/store: Selected 2, source pointer, new selection token and working-stack W. | Same invocation/owner/request; each selection starts fresh. Pointer capture alone is not geographic identity or lifetime proof. | Provider-only does not prove selected hook failed: cursor may be empty or evidence unavailable. |
| 2 / `0x79fca3` | Visited TEST/JNZ: Visited 3, operand `a` is low visited value. | Selection/W/owner match; nonzero is a witnessed bypass for that selection. | Downstream construction is not expected on that bypass. Silence elsewhere stays indeterminate. |
| 3 / `0x79fccb` | Exclusive source-map lookup returns: Lookup 4. `a/b/c/d` are result/capacity/actual source key/actual decision epoch. | Selected source equals key, actual owner and decision epoch match; result equal capacity is miss, unequal is hit. Bounded source copy must be read-valid. | Hit legitimately skips construction. Missing lookup after unvisited is unresolved branch/admission/context; never silently diagnosed as broken hook. |
| 4 / `0x79feaf` | Converter CALL creates TLS scope; **no separate event/counter**. Descriptor 5 from site 13 indirectly witnesses this matching scope. | Site 13 requires conversion owner equal current provider scope; actual input and manager operands are retained there. | Missing Descriptor cannot separate site 4 failure/nonreach from site 13 failure/nonreach. INDETERMINATE; no fabricated converter counter. |
| 5 / `0x79ff18` | Generator wrapper: Generating 6 and Generated 8; owner FormID, BIOM, geographic pointer and output holder. | Consumed descriptor precedes generator; selected source/context agree. Generated is closeout, not evidence of successful sampling prerequisites. | Generator may return without sampling. Missing end can be interruption/crash; first missing scope is named. |
| 6 / `0x79b8e8` | Sampler CALL returns: Sample 7, actual raw AL, sampler pointer and geographic pointer. | Same generator/invocation/source/epoch; query pointer equals generator operand; AL must be 0–15. Both 0 and 3 are accepted. | It witnesses return, not entry. Missing Sample cannot distinguish skipped prerequisites, pre-return failure, loss or context gap. |
| 7 / `0x79ddf0` | Reset wrapper: FenceBegin/End 10/11, `a=0`, RCX ProcGen and global hazard/epoch. | Reset begins before protected unlock and normally closes for cold science; B1 warm path does not need reset. | Unexercised reset is permitted and must remain unvalidated in retail. Missing end does not alone prove failed hook. |
| 8 / `0x79d910` | Destruction wrapper: FenceBegin/End, `a=1`, raw RCX object in `proc`. | Global epoch/hazard protects overlapping scientific contexts; raw object argument is not a persistent identity. | No destruction may occur on the visit. Pair/owner semantics remain untested where not exercised. |
| 9 / `0x975030` | Erase wrapper: FenceBegin/End, `a=2`, raw RCX object. | Distinguish its object from ProcGen/source identities; overlap invalidates affected path. | No erase may occur; absence stays indeterminate rather than failed instrumentation. |
| 10 / `0x9829b0` | Grid-clear wrapper: FenceBegin/End, `a=3`, raw RCX Grid object. | No mutable Grid enumeration; global hazard/epoch is the recorded continuity witness. | Unreached clear is not a full-B1 failure or proof of a cold Grid. |
| 11 / `0x982b70` | Retirement wrapper: FenceBegin/End, `a=4`, raw RCX retirement object. | Never equate this raw operand with every event's ProcGen owner. No cross-epoch pointer reuse join. | Missing retirement cannot establish stable source allocation forever. |
| 12 / `0x79dec4` | Protected reset unlock CALL: Cold 12, ProcGen from lock operand, direct visited count/data, hazard/depth status. | Scientific cold proof additionally requires matched reset entry/anchor/normal end and no uncertain prior activity. B1 does not demand it. | Missing cold is not a sampler malfunction, and Save52 load does not substitute. |
| 13 / `0x78d6f4` | Scoped normalizer: Descriptor 5 after actual engine-local descriptor/query copies. | Actual manager/input route must be primary `manager + 0xc8`; working-stack W is separate from geographic descriptor. Query/context and order are checked. | Temporary route `+0x1c0` is frame-unqualified. Descriptor silence is inseparable from site 4 and other capture gaps. |

The reporter emits all fourteen rows even when none was exercised. Each contains
installation state, exercise state, witness type, authenticated/tail counts,
first/last sequence, first invalid reference, status failures, correlation count
where applicable, unavailable per-site loss count and explicit absence/failure
limits. It does not claim lifecycle pair validation from two arbitrary fence
records; untested semantic correlation stays distinct from positive hook exercise.

## Minimal repair, reproducibility and diagnosis

Three routes were assessed before implementation: use the frozen reader's existing
diagnostics; add an independent offline reporter; change native hooks/counters.
The first fails B1 because cold qualification precedes boundary-order checking
and there is no fourteen-site output. Merely promoting a no-cold diagnostic could
accept a reordered warm trace. Native redesign is unnecessary for truthful
positive exercise and explicit uncertainty, and is outside this repair authority.
Exact per-site entry/drop counters would require a separately reviewed native
revision if a later decision demands that stronger discrimination.

Use installed CPython with fresh output names:

```powershell
& 'C:/Users/User/AppData/Local/Python/pythoncore-3.14-64/python.exe' -B research/resource-retained-population/d5x_b1_identity.py identity-check01
& 'C:/Users/User/AppData/Local/Python/pythoncore-3.14-64/python.exe' -B research/resource-retained-population/d5x_b1_report.py .local-work/d5x/build24/prior-unknown .local-work/d5x-b1-audit/report-check01
& 'C:/Users/User/AppData/Local/Python/pythoncore-3.14-64/python.exe' -B research/resource-retained-population/d5x_b1_tests.py .local-work/d5x-b1-audit/tests-check01
```

Use fresh names on repetition. These examples use the pinned installed CPython,
not the WindowsApps alias, and an existing disposable session rather than live data.
The reporter imports the unchanged reader only for fixed-record decoding/source
key interpretation. It independently streams frame/ACK validation and path
correlation. It writes `coverage.json`, `coverage.md`, exhaustive `paths.jsonl`
and local-only `events.sqlite`; refusals produce named machine-readable output.
Path references name sequence/kind/QPC ticks. Raw offset is
`(sequence - sequence_origin - 1) × 328`; identities, raw and flush hashes bind
the originals. SQLite/native bytes and generated examples remain ignored.

A full local path needs unique Entry/Selected/Visited/Lookup/Descriptor/Generating/
Sample, correct order, context/pointers, primary descriptor route and direct
low-nibble return. It independently rejects duplicate/reordered boundaries,
wrong actual map source/decision epoch, frame/thread/request/parent/source
contradictions and overlaps. No cold/firstness requirement is imposed. Native
status/epoch poisoning rejects a gap during a path; an unaffected later complete
path can remain useful after aggregate loss. No admission-sequence hole is
expected for dropped events. Loss totals cannot be allocated to particular sites.

## Frozen B1 grading and operational approval checklist

| Evidence situation | Required disposition |
|---|---|
| Exact READY/challenge and healthy capture, no authenticated native boundary | STARTUP-ONLY / PARTIAL, never full B1. |
| Provider/selection/hit/bypass activity, missing downstream mechanism | PARTIAL NATIVE COVERAGE. Name every exercised/unavailable/uncertain site and where correlation stopped. |
| Authenticated valid target ordinary path, possibly without cold | Local CORRELATED PATH PREFIX. Full B1 instrumentation PASS additionally requires genuine retail identity, fresh challenge, exact approved load/travel/arrival/STOP, protected postflight and independent operational/evidence grading. |
| Invalid context/order, unresolved decisive gap, bad identity/guard/output/transport or missing protection | ENGINEERING FAILURE / UNCERTAINTY as appropriate; retain useful prefixes separately. A record with read failure is not a hook-failure diagnosis. |
| Lifecycle/reset sites not naturally reached | NOT OBSERVED; disposable proof and installed guarding remain separate. Do not demand artificial reset or call this proof of retail execution. |

The machine reporter never automatically grants full B1 PASS. It reports local
evidence and required operational review separately. A crash prefix can preserve
the path while operational completion/target survival fails. Cold-winner science
is not evaluated by this B1 reporter and remains separately gated B2.

Before considering an explicit B1 GO, bind the final audit/card/reporter/source
manifest and frozen artifact hashes, then require:

1. Fresh offline full current-policy protection using the reviewed adapter-free
   preservation helper, including exact Save52, protected/manual/quick saves,
   namespace classification, independent backups and restoration COPY, remote
   protected saves, active archive guards, definitions and configuration. Unknown
   saves fail closed; correctly classified transient/Cloud metadata is diagnostic.
2. Fresh Cloud-disabled/profile/Save52/operator confirmation, process absence,
   both caller-available disk floors and exact unchanged installed/loader guards.
   No old operator confirmation or this audit's Save52-only hash can substitute.
3. Maintainer-only Vortex install/enable/deploy and exact deployed/staging/hash/
   competing-plugin checks; maintainer-only launch once through the pinned loader.
4. Fresh main-menu retail identity/READY and fresh identity-bound challenge ACK
   before loading the exact Save52 once. A pending/missing READY is not permission
   to continue or proof of failed native execution.
5. Load-complete and pre-travel annotations/health watermark, one ordinary travel
   to second Feynman V / Feynman V Cu IL F, first arrival and fresh health ACK.
   The route/destination must be confirmed with the operator before approval;
   the analytical key is not a navigable route.
6. Explicit approved Codex writes only for fresh request temporary-file/atomic
   replacement and session STOP, with external checkpoint annotations as defined
   in the amended card. No 070/080 D5X adapter is invented or invoked.
7. Maintainer STOP/normal exit/disable or removal; fresh full offline protected
   comparison, Cloud confirmation, deployed-DLL absence and staging disposition.
   Preserve crashes/tails; no game kill, hot unpatch, automatic restore or retry.
8. Offline authentication, site/path report and independent full/partial/failure
   grading. Only a separate B2 decision after B1 review may consider science.

The planned endpoint is one arrival plus health/STOP, not elapsed time or a
record/byte quota. Ordinary observation loss and delayed operator action alone
do not terminate capture. Proven disk/identity/guard/worker/output/protected-input
failure and operator STOP prevail. The R2 chronology—post-load/pre-travel watermark
55 versus arrival 9,736 with 6,101 unqualified demands—demonstrates why travel
checkpoints and boundary diagnostics matter. Those are receipt/admission bounds,
not exact native request times or proof of gameplay causality.

## Checks, limits, review and delivery

`.local-work/d5x-b1-audit/tests05/tests.json` reports PASS for **39 authentic
session checks, nineteen semantic contradictions, one many-hit partial-coverage
control, six damage controls, two refusal controls and four scale measurements**.
All fourteen sites have positive witness records across the authentic cases.
No native host was rerun. The supplied raw sessions/old damage copies remain
byte-identical to build24/qualification05. Every generated semantic/scale session
is explicitly labelled DERIVED, never a new native observation.

| Example | Actual result and meaning |
|---|---|
| READY only | One durable record; all fourteen native sites NOT OBSERVED. Startup-only, no native absence proof. |
| Source absent / selection-only | Provider-only or missing visited diagnostic. No claim that absent records prove failed hook. |
| Visited / map hit | Expected bypass/hit, zero complete paths; downstream construction legitimately not expected for that selection. |
| Prior unknown | Ten authenticated records, one valid target ordinary path; frozen scientific reader has zero cold-qualified chains. B1 capability and B2 firstness are different. |
| Skipped / missing descriptor / missing sample | Named prerequisite or converter/normalizer uncertainty; neither cold failure nor asserted sampler malfunction. |
| Normal / edge / corner / nested | One / two / four / two correlated ordinary paths; nesting never borrows another invocation's query or sample. |
| In-flight loss / overlap | Invalid context is rejected with exact first invalid sequence/kind/status/hazard/field references. |
| Recovery after one / 37 retry losses | Two intact local paths survive in each; known loss totals retained. Acquisition need not terminate. |
| Crash through sample | One valid prefix path with incomplete terminal transport; survival/operational completion are separate. |
| 1,000 hit-only derived invocations | 5,004 authenticated records and no complete path. More records do not supply missing downstream evidence. |
| Wrong hit source / decision epoch | Both report the exact contradictory-map-operands diagnostic, rather than being mistaken for legitimate hits. |
| Damage / wrong identity / wrong DLL | Preserve earlier authenticated prefixes or refuse interpretation; no repair of originals. |

The old full-materialization reader has a demonstrated scaling limit. With
10,000 versus 40,000 derived READY records, traced Python peaks grow from
**13,707,324 to 54,836,157 bytes**. The independent streaming reporter measures
**1,223,181 and 1,223,149 bytes** respectively. These are Python allocations,
not total RSS, SQLite C allocations or OS caches. The reporter keeps bounded
boundary state, a 2 MiB SQLite page cache and file-backed temporary storage;
exhaustive events/path results are disk-spooled. It maintains indexes during
guarded ingestion rather than bulk indexing afterwards. Both-drive disk guards
run every 128 ingested records/path outputs, at site reporting and completion,
with a 16 MiB analysis-write reserve. Metadata/ACK parser allocation bounds apply
to their fixed shape, not raw capture size or session duration. No arbitrary
retail record/byte/time cap is introduced. Runtime worker behavior is unchanged.

After tests05, one reporter delta renames a generated Markdown column from
Context failures to Native status failures, matching its actual counter. The
exact single-string comparison and normal/bad-read/overlap output equality are
verified in `.local-work/d5x-b1-audit/label-delta.json`; every machine field except
the reporter self-hash remains identical. `reporter-tested05.py` retains the tested
source. A second CLI-only correction prevents a repeated output-directory name
from overwriting an existing refusal receipt; two actual CLI exits and byte-equal
retention are checked in `refusal-preservation.json`. Exact source comparisons
bind both narrow deltas; no correlation/authentication algorithm changed after
tests05. The final source hash is separately pinned. Original reports remain
unchanged; corrected human examples are in `label-normal`, `label-bad-read` and
`label-overlap-reset` under the audit scratch root.

Tests01 has no completion receipt and no inferred exit cause. Tests02 exposed a
test-oracle error: a deliberately changed identity correctly refused, while the
test expected ordinary output. Tests03/04 qualified their earlier source. Tests05
adds the reviewed hit-operand diagnostic correction. These attempts and actual
reviewer REWORK findings remain preserved in the ledger and private receipts.

| Criterion | Final disposition and exact evidence | Limit |
|---|---|---|
| AC1 | PASS: identity02, fourteen site/six target guards, immutable artifact/source/output pins, exact Save52 hash. | No B1/B2/Vortex/game/save/control operation. |
| AC2 | PASS: initial ledger plus checkpointed alternative/failure/correction state, unchanged original questions/criteria. | All questions COMPLETE within the offline audit scope. |
| AC3 | PASS: fourteen explicit matrix rows and fourteen machine rows in every admitted-session coverage report. | Indirect site 4 and absent per-site counters stay explicit. |
| AC4 | PASS: streamed independent authentication, warm correlation, named first failures, human and machine references. | Silence remains indeterminate; complete operational PASS is not automatic. |
| AC5 | PASS: tests05, preserved development failures and exact label-only delta checks. | Derived controls are distinct from authentic native evidence. |
| AC6 | PASS: frozen grading above and amended card require authenticated downstream retail capability, not a cold winner. | Partial outcomes cannot authorize B2 or retries. |
| AC7 | PASS proposal: exact one-load/one-travel card, controller writes, protected/full future pre/postflight and both disk floors. | Fresh full protection/Cloud/operator checks are future approval gates. |
| AC8 | PASS: memory limitation measured/remedied offline; all retail/native absence/performance/science claims scoped. | Retail integration/unwind/rates remain untested. |
| AC9 | PASS: three separate GO-READY reviews of exact review02, retained verbatim, plus narrow final closure review. | GO-READY is not retail authorization. |
| AC10 | PASS: exact complete/task-only diffs, identities, source/status/exclusion inventories, screening and final closure manifests. | No stage/commit/push/publication. |

The scientific adverse scenario is authentic in principle and reproduced as a
labelled control: valid READY plus many provider/selected/hit/bypass records,
healthy transport and no descriptor/generator/sample mechanism. This is partial
coverage and cannot justify B2. A natural one-trip B1 that yields this outcome
needs a separate decision, never automatic repeated travel or forced reset.

The final audit manifest binds current code/card/source/receipts separately
from immutable D5X compatibility01; complete/task-only patches include all new
authored text and identify the supplied brief separately. Raw captures, SQLite
spools, proprietary/binary inputs, protected save bytes and private review returns
remain local-only/excluded. Q1, Q2 and Q3 are COMPLETE, with Q2's observational
limits explicitly retained. Readiness is GO-READY within this audit contract,
not a guaranteed full-path retail outcome or an operational GO.

## Exact review closure and remaining gates

Scientific, engineering/operational and editorial reviewers independently verify
the twelve-file review02 snapshot, delivery SHA-256
`162cc83c052527ee8850efdfcf9823c417a2d3b08588f2a259a5fa5b61278599`.
Its complete/task-only patch hashes are
`ce3fee40039e4182e8001ab3ed850116e833ff69fb6588693c956256de184aec`
and `fdcecfb79fa7e4acfc598c1e833116288540edb4f3bf005401d6c6bb0b200f88`.
Engineering independently applies both patches in memory from exact HEAD bytes
and independently checks 610 raw frames/79 ACK lines across 39 authentic sessions.
Science independently decodes/replays representative warm, missing-boundary,
loss, crash and corrected hit controls. Reviewers inspect full-suite/memory/
installed-file checks through pinned receipts; they do not rerun native hosts.

Actual returns are `.local-work/d5x-b1-audit/scientific-review02.md`,
`engineering-review02.md` and `editorial-review02.md`. Earlier engineering REWORK
is preserved alongside corrections. Only this report and the ledger change for
self-describing closure; the reviewers receive that narrow delta independently.
The final package is `.local-work/d5x-b1-audit/final01/`: delivery/check manifests,
current status, review-return pins and exclusions/seal. Complete/task-only diffs
are `.local-work/diffs/d5x-b1-audit-final01-complete.diff` and
`.local-work/diffs/d5x-b1-audit-final01-task-only.diff`. Forward/reverse scratch
application compares exact bytes; complete includes the unchanged supplied brief.

Editorial screening has zero diagnostics across twelve eligible files. Manual
and independent reading covers both new documents, the complete amended card,
supplied brief, all four Python modules' explanatory/operator text and all five
changed existing sections. The status-column label and exact post-suite source
deltas are verified; no suppressions are used. Tool screening alone is not
semantic proof. Final snapshot/patch/source/receipt checks bind that reading.

| Outcome dimension | Disposition |
|---|---|
| Audit questions/readiness | Q1–Q3 COMPLETE; GO-READY for considering separately scoped B1 authorization. |
| Reporting/evidence integrity | Qualified offline method and explicit uncertainty; authentic and derived evidence remain distinct. |
| Native integration and target survival | Frozen candidate unchanged; retail integration/survival NOT TESTED by this audit. |
| Protection | Save52 hash verified only. Fresh full protection, backup/Cloud/operator confirmations and pre/postflight remain mandatory future gates. |
| Science | No winner/preference/coldness claim; D5R remains OPEN; B2 NOT AUTHORIZED. |
| Publication/integration | B6 ON HOLD; await maintainer critical review. No staging, commit, push, deployment or live control writes. |

Original [D5P-R1 diagnosis](d5p-r1-diagnosis.md),
[D5P-R2 retail account](d5p-r2-retail.md), D5X native observations/qualification,
and owned R1 protection/patch/export methods supply provenance. Central sources
and credits record these uses. No original captures, native package, scientific
conclusion, save or historical failed verdict is rewritten by this audit.
