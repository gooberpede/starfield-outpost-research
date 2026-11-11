# D5N alternative native observation — Phase A

2026-10-28, Australia/Sydney. [Invoked brief](../../implementation-briefs/README.md#archive-lookup) (`implementation-briefs.zip :: docs/implementation-briefs/CODEX_BRIEF_SOR_RG2_D5N_alternative_native_observation.md`),
[frozen contract and comparison](d5n-contract.md), [Phase B proposal](run-card-d5n-v1.md),
[source/evidence ledger](d5n-sources.csv), [review](d5n-review.md).

**The implemented hybrid retains the complete fourteen-witness region contract,
using a hardware Grid-clear breakpoint and thirteen software probes. Retail
reliability and the Save52 construction question remain untested.** Final
qualification and independent disposition are recorded below; no Phase B,
installation, B6, integration or publication is authorized.

| Element | Scoped answer |
|---|---|
| Question | Can an alternative observer associate first observed miss/query/mask, an actually copied retained region and later same-lifetime reuse? |
| Best-supported answer | The hybrid associates witnessed copied regions, final ownership and later same-lifetime hits in all required real Windows controls. It retains native reads with a different Grid-clear trap mechanism; no retail observation follows. |
| Confidence | PROVEN / RUNTIME for the tested synthetic contract on the exact built pair/host, with independent review and its stated limits. Native field/control relationships retain their earlier STATIC qualification. No new retail semantic finding is proposed. |
| Coverage | Fourteen pinned native boundaries, ordinary chart-0 source selection, synthetic first misses, copy/ownership/hit, lifecycle/ABA, concurrent/nested requests, real thread churn and declared failures. |
| Completeness | Per-witnessed-region ancestry inside uninterrupted observed segments. No full intended population, source census, universal writer/allocator coverage, historical first construction or serialization claim. |
| Limitation | Debugger event delivery may fail in retail for either hardware or software traps. The earlier DR0 and D5L/D5M failures remain adverse evidence with unknown causes. |
| Next decision | Critical review and, only if desired afterward, separate explicit GO for the exact one-session proposal. No automatic retry or alternate target. |

## Implementation and provenance

Baseline HEAD is `9740f0a3d35dc42d2651715bfeb23f718c9e1412`; the index is
`66e79cb39728d83923f1e0d5de234a154400212a6ca3ab1aab1f4a5f0bbce210`.
The only initial untracked file was the supplied D5N brief. No staged changes
existed. Historical D5C–D5I, D5L/D5M code, run cards and post-mortems stay intact.

The new [source adapter](../../../research/resource-retained-population/hybrid.py)
uses checked transformation anchors against the existing owned D5M
controller/build/reducer, refusing a changed checked anchor. Additional bounded
fixture/path substitutions are visible in the adapter. Generated translation units
and original source snapshots are pinned by the build manifest. This is openly
source-derived reuse under SOR-P-0002 at the baseline above, not a clean-room
implementation or a new third-party dependency. The original reader and native
semantics are unchanged. New entry points have I/O/effect headers; the
[methods note](../../../research/resource-retained-population/README.md) records
their use. Installed Python 3.14.3, MSVC/MASM/linker and SDK are separate tools;
the build's `/Bv` output and tool hashes establish the actual versions.

DR0 holds the relocated Grid-clear RVA `0x9829b0` on every admitted thread.
DR1–DR3 remain unused; enabled foreign slots or GD are refused. The initial
barrier and each post-barrier CREATE_THREAD receive explicit register readback.
Thread IDs are paired with independently checked creation identity and monotonic
lifetimes; no inheritance assumption substitutes for arming. Every sample checks
the known threads' hardware coverage and all fourteen instruction guards.
Grid-clear's original byte remains intact, with an explicit prohibition on patching
site 10. Its raw CONTEXT RIP equals the instruction; software samples retain
INT3+1. The hybrid reducer checks those actual bytes/registers without rewriting
captured contexts or normalizing the hardware stop into a software one.

Hardware resumes clear owned DR6 and set/read back RF while preserving the
sampled GPR/FPU groups. Software sites keep D5M's fenced rewind/TF step/rearm.
A queued hardware peer during software rearm remains suspended, keeps its RIP,
clears RF/DR6, then retraps after rearm; software peers rewind their INT3 RIP.
Foreign exceptions are passed through under the inherited rules, not suppressed.
The observer still pauses threads and can alter race winners. Context readback
does not establish universal architectural-state preservation or event delivery.

## Tests and preserved failures

The final candidate is `.local-work/resource-retained-population/d5n-build11/`.
Its `build.json` SHA-256 is
`b7d9db154ba2b166da96adc579f937fc3eb07f5f5343abc4e5183bfe2de1b2c3`,
with 64 source/tool/output pins. The retail controller is
`96c9b8e50ad2858e781501de83952b83044325e6b801055b4d61907d8f5b90b7`;
the fixture controller is
`c415de13bae2c126294ef1b50c1a4b6bf8d55f3b788077f514a06bc89964cc2f`;
the fixture is
`586493df16c36242f1539e1ca66d32d40bef55cfe46284dffa7bc8ec0c8515e7`.
Generated controller source is byte-identical to build09; the later corrections
affect the offline receipt validator. Build11 recompiles and binds the complete
current source closure. Two inherited retail-build warnings concern an unused
fixture variable and removed helper; neither is hidden or counted as validation.
Fresh PE/export checks pass all fourteen instruction shapes and thirteen backed
ranges, 16,736 installed bytes; no retail instruction was executed or patched.

All 46 final exact-build real Windows cases PASS in `d5n-qualification11/`;
all four actual pump cases PASS in `d5n-pump11/`. The independent binder in
`d5n-checks11/` authenticates 1,276 SRO1/ACK receipts across 2,910 journal events
and reproduces every reduction. It checks 320 hardware Grid-clear samples and
zero Grid-clear patch intents. Final scientific and engineering reviewers each
independently authenticated all 1,276 receipts and reproduced the reductions;
their exact-snapshot disposition remains separate in d5n-review.md.

| Actual final control group | Result and limit |
|---|---|
| Construction, different later query, source/Grid/owner ABA, reset/teardown windows | Qualified region chains, mask-0/mask-3 segments and poisoned-window rejection pass. This is fixture evidence, not historical Save52 ancestry. |
| Concurrent/nested and contradictory histories | All selected concurrent decisions remain accounted for. A nested hit before append/completion cannot borrow future geometry. Direct mask 3 with mask-independent points remains a contrary observation. |
| Thread churn and rapid Grid-clear | Stress retains 624 receipts, including 289 actual hardware Grid-clear samples. Real early/repeated creation/exit and reuse of TIDs/handle values are checked without conflating lifetimes. |
| Deterministic queues | Same/different software-site and mixed hardware/software controls all pass. The mixed control contains actual queued site 10 during software step site 11, followed by hardware retrap/resume. |
| Crash timing and receipt survival | Post-chain crash retains 13 independently authenticated receipts and one chain; early crash retains four receipts and zero decisions/chains. Both target outcomes are exceptional exits, reported separately from evidence validity. |
| Coverage, containment and incomplete/corrupt evidence | Hardware loss, foreign-slot refusal, software guard loss, interrupted collection and declared API/diagnostic failures fail closed. All final registered/plain owners reach zero and targets are independently absent. Four damaged receipt/ACK controls are refused; 27 adversarial replay controls pass. |

The final four pump controls cover normal completion, pre-arm STOP, post-READY
collector loss and broken pipe. Context preservation is limited to the checked
groups/host; neither successful API calls nor fixture survival prove retail
delivery. Full source/build/receipt hashes and original batch/copy equality are
retained rather than inferred from these totals.

The independent summary checks 49,505 control rows, including 736 hardware-arm
readbacks across 740 registered thread lifetimes and 18 queued hardware rewinds.
Registered threads in intentionally failed admissions need not reach arming.
Every continuation result has its matching intent and event/process identity;
deliberately failed APIs remain failures. Four additional raw-context controls
reject wrong hardware RIP, DR0, GD and DR6. None replaces actual process tests.

The first exploratory hybrid build passed basic ancestry and Grid teardown but
failed the inherited same-site queue control. Its stimulus still used hardware
Grid-clear to open what the fixture assumed would be a software step window;
fixture bookkeeping later referenced a retired thread. The next fixture revision
missed its deferred-stimulus boundary by one sample and left the second worker
waiting on an unsignalled gate. Those exact failed records remain local. Only
the identity-checked disposable targets were terminated to release these broken
fixtures; a CIM identity query was denied, then ordinary Get-Process path/creation
identity succeeded. No Starfield process or security setting was touched.

The corrected software controls use SourceInit and GridInit. A separate
`queued-hardware` test defers a real DR0 trap, opens a SourceInit software rearm
window and replays the hardware event inside it. Independent initial engineering
inspection confirmed the actual queued site 10 / step site 11 transition and
subsequent hardware resumption in the focused build06 control journal. This
qualifies a mixed-event path that the unconstrained stress run need not exercise.

The initial pump test exposed an inherited fixture race: its idle pipe-loss
injection could close stdin before ARM_ACK if attachment took more than the
reader's polling interval. The resulting closed-file exception is preserved.
The D5N adapter injects idle test failures only after READY exists; production
collection has no synthetic failure flag. Corrected normal, pre-arm STOP,
collector-loss and pipe-loss controls are requalified on the final build.

The first full receipt-validator run stopped when the intentionally malformed
ACK raised `KeyError`, an expected rejection type missing from the test wrapper's
catch list. The wrapper now counts that rejection correctly. A second invocation
used a broader scratch root than the inherited adversarial helper permits and
was refused; the maintained entry point now enforces the narrower root before
writing. The corrected validator authenticates all 46 preliminary-build cases,
rejects all four damaged receipt/ACK copies and passes 27 adversarial controls.
Final-build qualification is repeated because the build pins these offline
methods too. No captured evidence or native observer logic changed for these
validator corrections. Their diagnostics remain local.

Early-crash and post-chain-crash are separate actual targets. A positive chain
must still be independently decoded and ACK/hash-bound after the crashed target
is absent. Missing ACK, changed ACK, missing receipt and corrupted receipt copies
must be rejected. Supplemental adversarial replay removes construction stages,
changes lifetime/frame/ownership/geometry and retains contrary direct masks;
it supplements the actual debugger cases. A crash before construction remains
incomplete acquisition. A crash after complete durable evidence does not erase
the already witnessed result or become an engineering failure solely for exit.

## Preservation, outcomes and frozen criteria

The full initial and subsequent protection audits pass: all 98 protected save
names have independently verified backups; archive-backed inputs, installed
EXE/ESM/PlanetData, definitions/configuration and Save52 scratch restoration
agree. The comparison also preserves HEAD/index and both drive floors.
The final end-to-end `operate_hybrid.py prepare` also passes with fresh full
protection, exact build11/matrix/site binding and scratch Save52 restoration.
It is actual execution, without mocked/replayed preservation. The eleven
in-memory hybrid admission controls pass, including old-fourteen-software and
missing-hardware refusals. No real GO file, consumption sidecar or retail
collector invocation was created. The actual token/child test correctly refuses
the sandbox account; real ordinary-user retail acceptance remains untested here.
Twelve inherited synthetic preservation tests pass; the ordinary-user requirement
is retained rather than bypassed to obtain live readiness.

Final preparation reports C: 75,029,590,016 and D: 86,714,900,480 caller-available
bytes. Its protection comparison passes all sixteen checks against the initial
audit; the active archive proof authenticates 91,933 archived references and
1,401 surviving loose hashes. The historical strict four-ZIP verdict remains
FAIL; zero unacknowledged surviving-input/protected differences are reported.
`remotecache.vdf` remains diagnostic. No restoration or baseline repair occurred.
All native and fixture controllers/targets are absent after the completed tests.

Exact primary paths are `.local-work/resource-retained-population/` followed by
`d5n-build11/build.json`, `d5n-qualification11/results.json`,
`d5n-qualification11/aggregate.json`, `d5n-pump11/results.json`,
`d5n-checks11/checks.json`, `d5n-checks11/adversarial/results.json`,
`d5n-ready11/preflight.json` and `d5n-admission11.json`.
`.local-work/d5n/summary11.json`, `comparison11.json` and `extra-controls11.json`
bind the independent synthesis, full protection and supplemental hardware
controls. The ledger pins these records, methods and preserved failures.

| AC | Assessment | Evidence or remaining gate |
|---|---|---|
| AC1 authority/protection | PASS within Phase A | Fresh full preparation and sixteen-check comparison preserve all 98 protected names/backups, content, archives, HEAD/index and disk floors. Phase A only. |
| AC2 feasibility | PASS | Three approach classes, native lifetime alternatives and adverse retail evidence in d5n-contract.md. No impossibility/safety claim. |
| AC3 minimal contract | PASS | Exact input/mask/copy/owner/reuse/fence matrix; no unproved snapshot replacement. |
| AC4 actual acquisition | PASS within the qualified envelope | Final build11: all 46 real Windows cases, including actual mixed queue. Exact source/tool/output pins and lossless aggregate are retained. |
| AC5 discrimination/durability | PASS | Actual early/late crashes, 1,276 authenticated receipts, four receipt refusals and 27 adversarial controls; survival is separate. |
| AC6 live readiness proposal | PASS for the proposal | Complete one-session card, actual fresh offline preparation and eleven hybrid admission controls. Ordinary-user live admission and retail behavior are NOT TESTED; no GO. |
| AC7 reproducibility/editorial | PASS | Exact ledger and failures, methods, full manual prose coverage, zero-diagnostic screen, complete/task-only inventories and exact forward/reverse patch checks. |
| AC8 independent review | PASS with final closure gate | Engineering and scientific reviewers both ACCEPT review01, including editorial scope. Final delivery additionally requires both accepted closure deltas and matching final-delivery.json hashes. |

Scientific retail result: none. Observer qualification, target survival and
protected-input integrity are separate dimensions. Disposable intentional exits
and disposal do not imply retail cleanup/survival qualification. Raw contexts,
native exports, binaries, receipts and protection records stay LOCAL-ONLY;
authored text/code is REVIEW-REQUIRED. No staging, commit, push, external contact,
new dependency, analysis mutation or publication is performed.

Both independent reviewers ACCEPT the exact review01 snapshot. They each
authenticated all 1,276 receipts and reproduced the native reductions; scientific
review also directly challenged premature nested reuse, ABA, contrary inputs
and removed construction stages. Their verbatim returns and limits are retained
under `.local-work/d5n/`. Only this closure and the review record change afterward.
Final delivery is valid only with both independent closure-delta ACCEPT records
and matching `.local-work/d5n/final-delivery.json`; no new scientific or code
change is included in that closure. Acceptance does not authorize the proposed
Phase B session, integration or publication.
