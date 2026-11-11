# D5O hybrid hardware coverage diagnosis and qualification

2026-10-28, Australia/Sydney. [Source/evidence ledger](d5o-sources.csv),
[review record](d5o-review.md), [proposed card](run-card-d5o-v1.md). The [invoked brief](../../implementation-briefs/README.md#archive-lookup) (`implementation-briefs.zip :: docs/implementation-briefs/CODEX_BRIEF_SOR_RG2_D5O_hybrid_coverage_diagnosis_repair.md`)
freezes AC1–AC8 without amendment. Work is confined to offline analysis and
disposable Windows targets. Retail execution, integration and publication remain
unauthorized. Final synthetic qualification passes. Both independent reviewers
ACCEPT the substantive review01 snapshot; final delivery also requires their
closure-delta acceptance and the matching external delivery manifest.

## Diagnosis and correction

**The retained D5N records do not identify the failing peer or context state.
The new implementation distinguishes context API failure from register mismatch and
excludes only positively terminated thread objects from live coverage duties.**
This repairs a source-level lifecycle inconsistency; it does not establish that
the inconsistency caused D5N's failure or that retail delivery is reliable.

The original [D5N account](d5n-phase-b.md) remains authoritative. A fresh offline
recheck authenticates all fifty ledger pins and reproduces the diagnostic
reduction. Event 261 delivered Reset RVA `0x79de92` on TID 22364, lifetime 17;
85 peer suspensions succeeded. There is no dead-peer branch record. Control row
1763 records the combined failure without the failing peer, API return or debug
registers. No such operand can be recovered from the barrier or `last_error=0`.
No scientific sample, historical construction, reuse or qualified non-hit follows.

The owned [D5O adapter](../../../research/resource-retained-population/coverage_hybrid.py)
preserves the original D5N/D5M files. In D5N, suspension can retain a proven dead
peer until its EXIT event, while coverage subsequently reads every map entry.
Bookkeeping retention and live coverage membership are distinct. D5O tests the
retained thread object for termination before requesting its context. A
signalled object cannot execute another source/Grid lifetime event. Its owned
duplicate remains registered until normal EXIT cleanup; fixture-only retention
after EXIT tests the same object-state branch. An ambiguous or failed lifecycle
query remains an error, never an exclusion.

The [coverage reader](../../../research/resource-retained-population/coverage-hybrid.h)
separates `GetThreadContext` success, immediate meaningful error and named
subpredicates. Successful records contain requested/returned `ContextFlags`,
DR0–DR3, DR6, DR7, EFlags and RIP, expected DR0 and DR7 mask/value. Failed reads
mark registers unavailable rather than reporting initialized zeroes as observations.
Each record binds process creation, event sequence/PID/TID/site, inspected peer
TID, verified creation time, monotonic lifetime, owned duplicate and explicit
suspend ownership. The event owner is stopped by Windows; peers retain their
additional owned suspension during software rearm. The control batch is flushed
before continuation; scientific SRO1/ACK capture remains separate.

| Hypothesis | Evidence and disposition |
|---|---|
| Missing debug-register flags or alignment | Old code already initializes `CONTEXT_DEBUG_REGISTERS`; the SDK-aligned local object requests that group. No missing-flags defect is established. D5O also requests control state for diagnostics. |
| Stale borrowed handle or reused identity | D5N retains checked owned duplicates, creation times and monotonic lifetimes. No new borrowed-handle defect is established. Reuse controls must preserve separate lifetimes. |
| Exited thread retained in live coverage set | Concrete source inconsistency. A checked zero-time wait distinguishes proven termination from a live or transitional thread, including actual exit code 259. |
| Suspend/exit transition | A denied suspend is not proof of death. Existing deferral before sampling/disarming remains; failure to qualify a relevant live thread still stops. Concurrent-exit and retained-object tests have separate scopes. |
| DR0/DR7 loss, foreign slots or GD | Expected ownership remains unchanged. Actual DR0/enable loss must stop. Windows sanitization of an attempted GD write is distinct from an explicitly injected successful-return snapshot fault. |
| TF/RF or mixed trap handling | Original software rearm and hardware RF resume remain. Queued hardware/software tests must demonstrate real delivery and retrap; passing them cannot explain an unrecorded retail transition. |

Microsoft's [GetThreadContext](https://learn.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-getthreadcontext),
[debug-event](https://learn.microsoft.com/en-us/windows/win32/debug/debugging-events),
[GetExitCodeThread](https://learn.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-getexitcodethread)
and [wait](https://learn.microsoft.com/en-us/windows/win32/api/synchapi/nf-synchapi-waitforsingleobject)
contracts support the stopped-context, handle and termination distinctions
(SOR-S-0117 extension, consulted 2026-10-28). API contracts are source-reported;
actual disposable receipts establish tested behavior. No example code is copied.

## Experiment envelope and provenance

Baseline HEAD is `6d2526145870b97fc6e63e0ad8ee3e471af719c0`. Initially only the
supplied D5O brief was untracked; no staged changes existed. D5N controller,
fixture, build and qualification methods are adapted under SOR-P-0002. The
native reader, reducer, geometry, source selection and fourteen observation
sites remain unchanged. This is source-derived maintainer-owned reuse, not a
new third-party implementation or a clean-room claim.

Allowed inputs are pinned project-authored native-shaped fixtures and existing
local evidence. Installed MSVC/MASM/SDK compile them; installed CPython drives
the owned SRO1 transport and independent decoder. Tests create and attach only
hash-bound sibling disposable executables, use thirteen software probes plus
hardware Grid-clear, suspend/resume peers and modify owned RIP/TF/RF/debug
state. Specific fault controls change fixture DR0/DR7, use an invalid context
handle, retain terminated fixture identities, or alter a returned GD snapshot
with an explicit synthetic label. Controlled target crashes/termination are
allowed; no Starfield process, save, configuration or analysis state is changed.

Risks include changed scheduling, fixture crashes/hangs, unavailable coverage
and diagnostic/transport failure. Stop on identity/guard/ownership/integrity or
worker/pipe failure, explicit STOP, fixture completion, or either caller-available
drive falling below 40,000,000,000 bytes. Fixed synthetic loops define traffic,
not healthy scientific-session quotas. Cleanup independently checks target
absence and handle accounting. Outputs stay in bounded ignored D5O build/test
folders; original captures and protected inputs remain untouched.

## Qualification and preserved development failures

The final candidate is `.local-work/resource-retained-population/d5o-build08/`.
Its 72 source/tool/output pins remain exact, with no operational source exception.
Build manifest SHA-256 is
`d645a6cb8ee2969813262a7679bfd1008054b3cfa0f7b5743ab1385244cb0c55`.
The [card](run-card-d5o-v1.md) pins all three executable hashes and fourteen
observation sites. Installed CPython is 3.14.3; MSVC reports 19.51.36256.0,
with toolset path 14.51.36231. Build logs retain four retail-compilation warnings:
two unused fixture-only parameters and two inherited unused/removed helpers.
They are not suppressed or counted as semantic validation.

All 55 exact-build Windows cases and four actual pump cases pass. The complete
checker authenticates 1,524 SRO1/ACK receipts, reproduces 37 synthetic chains,
checks 357 hardware Grid-clear samples and confirms zero Grid-clear patch
intents. It validates 23,211 coverage reads by actual identity/register fields.
Four damaged/missing receipt controls are refused; all 27 inherited adversarial
scientific controls pass. Counts support the field-level oracles; counts alone
are not the proof of coverage or semantics.

| Actual control group | Supported result and limit |
|---|---|
| Reset with many peers | All 32 Reset events have 98 suspended peers on this host. Each event has exactly one successful context read per fenced lifetime plus its owner. The 96 intended workers are admitted before Reset; auxiliary threads remain covered too. |
| Context API and register loss | A suspended peer's deliberately null API-handle query records real API failure/error 6 without invented registers. Actual DR0 loss, enable loss and isolated RW0 type loss stop before Reset sampling. Returned-GD corruption is separately labelled synthetic; native GD sanitization is preserved as observed. |
| Exits and numeric reuse | Actual code-0/code-259 terminated objects are excluded only after signal proof. The concurrent-exit case records 68 access-denied suspensions with nonsignalled state, matched deferral count/owner order, eventual lifetime exits and 32 successful Reset samples. Early churn demonstrates actual TID/handle reuse with distinct identities. This is tested transition coverage, not exhaustive race coverage. |
| Software/hardware rearm | Real same-site, different-site and mixed queued traps are deferred, replayed and retrapped while rearm remains fenced. Creation/destruction during rearm, foreign slot occupancy and controlled API/diagnostic failures retain their required outcomes. |
| Scientific chain and counterexamples | Actual copied geometry, final ownership and later same-lifetime hit survive. Failed copy, incomplete generation, source/manager replacement and poisoned teardown windows cannot borrow a successful join. Contrary masks/geometry remain contrary. |
| Durability and target outcome | Late crash preserves one complete authenticated chain; early crash has none. The actual pump passes normal, pre-arm STOP, post-READY collector loss and broken-pipe controls. Every tested target is absent afterward; intentional deaths are separate from evidence validity. |

Primary paths below have prefix `.local-work/resource-retained-population/`:
`d5o-qualification08/results.json`, `aggregate.json` within that same folder,
`d5o-checks08/checks.json`, `coverage-checks.json` and `qualification-proof.json`
within the checks folder, `d5o-pump08/results.json`, `d5o-ready08/preflight.json`
and `d5o-admission08.json`. The aggregate verifies all 3,378 copied case files
against their originals. The proof captures inputs/methods/build before and
after checking and refuses a changed snapshot. Its SHA-256 is
`108a4cf94e294876f75f92f4476089441a58a7de5a69e843a535080a558f1bf9`.
The same proof binding is rechecked before the fresh preflight is written.

Eleven inherited admission controls pass through the actual new guarded function;
eleven additional proof/admission refusals and the separate missing-proof CLI
control pass without creating a real GO or consuming admission. Twelve inherited
protection unit tests also passed in the execution transcript; those tests do not
replace the actual full preservation and proof checks. Exact code and selected
primary/failure evidence are bound by the 117-record ledger.

Early `d5o-probe01` runs demonstrate the Reset boundary and actual context API,
DR0 and DR7-enable failures. Their initial postprocessing used handle value as
a global identity key and was corrected to monotonic lifetime; those raw records
remain unchanged. `d5o-probe03` shows that an attempted native GD write is cleared
on readback, contradicting the initial expected failure. Its EXIT-event probe
also shows that the object need not yet be signalled during EXIT delivery.
Neither observation justifies excluding a nonsignalled relevant thread.

The separate `coverage-gd-return-fault` control explicitly changes only a
successful returned snapshot to test GD rejection. It is not evidence of native
GD occupancy. `coverage-gd-sanitized` preserves the actual API result. Development
review also found a default exit-code diagnostic introduced by the first adapter;
the corrected path queries the actual code only after positive termination proof.
Superseded builds and meaningful diagnostic failures remain local, not promoted.

Disabling DR7 enable returns DR0 and DR7 as zero on this host. The initial oracle
incorrectly demanded a sole `dr7` failure; the reader correctly identified `dr0`
first and retained both actual values. The corrected oracle accepts the actual
precedence, while a separate real RW0 type-change control retains the expected
DR0 and tests isolated DR7 rejection. A first exit-race verifier also assumed
exactly 100 registered threads; an auxiliary Windows thread contradicted that
assumption. The corrected verifier identifies all 96 repeated-entry waiters
before the final Reset, with two later scientific callers and other admitted
threads accounted for separately. These are test-oracle corrections, not new
retail findings or relaxed coverage duties.

Readiness review found that generic `results.json` is written before field-level
qualification. It can therefore remain all-passed after an oracle fails. The
separate [readiness gate](../../../research/resource-retained-population/ready_coverage_hybrid.py)
requires the completed independent coverage/lifecycle/receipt checker and seals
its exact build, methods, checks and full input inventory. Preparation verifies
all sealed bytes; future admission checks the pinned proof and lightweight
metadata alongside existing approval/protection gates. It also joins concurrent
exit deferrals by exact count and owner order across the separate journals;
the stdout deferral record itself has no serialized debug-event ID. This
Python gate changes no native observer behavior; the final build and proof
bind its source and method identities.

Build07 completed all 55 generic executable cases, but its strict stress oracle
failed: Reset arrived before every intended worker CREATE event had been admitted.
The fixture had no user-mode startup rendezvous. Build08 adds a 97-participant
barrier for the 96 stress/fault workers and main thread, so each worker must have
passed CREATE/arm continuation before Reset. The exact peer-set oracle is
unchanged. A focused read of completed build08 stress evidence passes all 32
Reset checks, with 98 suspended peers at each on this host. Final build08
qualification and the independent receipt checker both pass.
These results do not erase build07's strict failure or establish D5N's historical
cause.

## Integrity, confidence and coverage

Initial and final full checks use the active archive-backed baseline: 91,933
archive-backed historical rows and 1,401 surviving loose hashes, with zero
unacknowledged differences. Cargo's separate active five-object routine also
passes. The historical strict four-ZIP failure remains FAIL; no protected original,
archive/index, baseline, configuration or save is repaired or rewritten.

All thirteen applicable pre/post protection comparisons pass, covering policy,
98 protected save names, remote saves, independent backups, installed identities,
definitions/configuration and scratch Save52 recovery-copy equality. These are
D5O's thirteen comparisons, not the earlier D5N sixteen-field preparation ledger.
`remotecache.vdf` remains diagnostic and happens to match. Fresh preparation
records C: 73,736,110,080 and D: 86,127,861,760 caller-available bytes. Canonical
save-policy SHA-256 is
`daa11fe3b12c350d6f45d12b48b5df382085d7d25c2ff2525a758de2bf112157`;
the actual policy-file and governing-document hashes are separately in the
ledger. All native targets and Starfield are absent at final enumeration.
HEAD and index bytes remain unchanged, with no staged changes, commit or push.
`.local-work/d5o/summary08.json` records the exact comparison and Git identities.

| Dimension | Scoped conclusion |
|---|---|
| Confidence/basis | PROVEN / STATIC for the source membership inconsistency and repaired predicates; PROVEN / RUNTIME for the exact tested Windows controls and retained evidence. Historical D5N cause remains UNKNOWN. |
| Tested coverage | Final build08 and the 55 declared disposable scenarios on this host, with explicit admitted-thread identity and source/manager lifetime controls. |
| Inferred/unknown | Windows API contracts support the design. Retail exception delivery, the missing D5N context operands and actual Save52 construction/reuse remain untested or unknown. No lower retail crash probability is established. |
| Completeness | Exact membership for each checked admitted live set and authenticated recorded fixture chain. No universal Windows/kernel transition, hidden-thread, full intended native population or persistence completeness is claimed. |
| Publication | Authored work REVIEW-REQUIRED; raw contexts, receipts, binaries, private protection records and proprietary inputs LOCAL-ONLY. No release or B6 clearance. |

Scientific retail result: none. Engineering qualification passes within the
stated synthetic envelope; both independent reviews accept review01. Final
closure and delivery binding remain separate requirements.
Target survival is not a scientific criterion: deliberate fixture crashes and
disposal are recorded, while no retail target was used. The proposed card is
ready for critical review, with retail use still NO-GO until independent
acceptance and later separate maintainer GO. No new reuse/disclosure permission issue or outside implementation/dependency
was introduced.

## Acceptance and remaining scientific boundary

| AC | Disposition | Required evidence |
|---|---|---|
| AC1 authority/integrity | PASS within Phase A | Active archive-backed pre/post checks, thirteen comparisons, all 98 protected names/backups, exact installed/build/policy identities and unchanged HEAD/index. No game execution; HEAD/index unchanged. |
| AC2 forensic diagnosis | PASS for scoped diagnosis | Exact historical boundary and missing operands reproduced; lifecycle inconsistency, flags, ownership, transitions and DR7/GD alternatives investigated without inventing historical cause. |
| AC3 diagnostic fidelity | PASS | 23,211 actual identity-bound coverage reads; API/error/register and first-failed-predicate assertions, including meaningful unavailable-register handling. |
| AC4 correct coverage handling | PASS within tested scope | Relevant live losses stop; proven exits and ambiguous transitions have distinct real controls; all fourteen source/lifetime witnesses remain. |
| AC5 Windows qualification | PASS | All 55 final exact-build executable cases, four pump cases, strict Reset peer-set checks, real exit races, five new failure controls and complete synthetic chain/counterexample checks pass. |
| AC6 retail decision | PASS for proposal only | Complete build08/proof-bound card, actual offline preparation and guarded admission controls. Phase B remains NOT AUTHORIZED; no retail reliability claim. |
| AC7 durable record | PASS | Versioned methods, exact ledger and failures, compact local evidence, complete manual prose coverage and screening are supplied for review. |
| AC8 independent review/delivery | PASS with final closure gate | Both reviewers ACCEPT review01, including editorial scope and independently checked primary evidence. Final delivery requires both exact closure-delta ACCEPT records and the external manifest. |

No new resource-science finding is made. First captured is not first-ever;
retention without a later hit, same-lifetime reuse, cached-only observation,
qualified non-hit and failed coverage remain distinct outcomes under the
unchanged [causal contract](d5n-contract.md). Frozen masks/geometry, the selected
second Feynman V/Save52 question, B6 and publication holds remain unchanged.
Synthetic qualification cannot establish which unrecorded state occurred in
D5N or guarantee retail debugger delivery. Authored work is REVIEW-REQUIRED;
raw contexts, receipts, proprietary evidence and binaries remain LOCAL-ONLY.

Both actual final returns are retained verbatim under `.local-work/d5o/`.
Each reviewer independently authenticates all 1,524 receipts, reproduces every
reduction, validates the coverage/lifecycle fields and checks the full proof,
117 source/evidence pins and 72 build pins. Their tested-versus-supplied limits
are preserved in [the review record](d5o-review.md). Only this report and that
record change after review01; no code, card, ledger or scientific evidence changes.
Final delivery requires both closure reviews and matching
`.local-work/d5o/final-delivery.json`. No new authority follows from acceptance.
