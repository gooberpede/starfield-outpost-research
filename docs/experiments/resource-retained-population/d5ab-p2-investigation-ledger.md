# D5AB P2 active investigation ledger

2026-11-01, Australia/Sydney. Authority: [P2 brief](../../implementation-briefs/CODEX_BRIEF_SOR_RG2_D5AB_P2_controller_reducer_transport_qualification.md).
Baseline HEAD: `8a51dfce00cb2fcf4886d83561b2ad502d03c21d`.
Only the supplied P2 brief was untracked at admission. No staging, commit or push.

The frozen controlling questions are P2-Q1 transport, P2-Q2 actual worker/controller,
P2-Q3 reader/reducer and P2-Q4 reproducible bounded integration. All begin
INCOMPLETE. Their full normative wording and AC01–AC08 remain in the brief.
Parent D5AB-Q1–Q5 remain INCOMPLETE; D5R OPEN; B2 NOT AUTHORIZED.

## Checkpoint 1 — admission and investigation plan

Read repository policy, parent handoff and C2 decision. Existing source provides
production queue tests, native disposable observer fixtures, schema-3 reducer and
a worker lease helper. The helper's watch loop does not authenticate ACKs or STOP
ownership. Historical Python-thread tests cannot establish recorder health.

| Branch | Status and next concrete action |
|---|---|
| P2-Q1 / AC02 | Open: compile exact production queue at all three capacities, inspect accounting and add missing workload controls. |
| P2-Q2 / AC03 | Open: integrate controller lease, challenge ACKs and STOP finalization with actual disposable DLL worker; preserve fault outcomes. |
| P2-Q3 / AC04 | Open: qualify final reducer against final native build and adversarial derivatives; preserve historical Build08 receipts. |
| P2-Q4 / AC01, AC05–AC08 | Open: freeze source lineage, map parent obligations, obtain independent final review and verify exports. |
| C2 L1/L2 source lifetime | Outside P2 closure: preserve unresolved ownership, initialization, alternate cleanup and detached reuse obligations for P1/P3. |

Offline experiment bounds: read existing owned source, pinned installed inputs and
local receipts; compile with installed MSVC/MASM/SDK and CPython; execute only
fresh disposable hosts and original tests. Write synthetic receipts/binaries only
under ignored `.local-work/`; durable authored code and summaries stay in the
repository. Preserve the 40,000,000,000-byte caller-available floor on C: and D:.
Stop affected experiments on identity, disk or evidence-integrity failures.
No game, deployment, live attachment, save/configuration/database mutation,
downloads or disclosure. Crash controls affect their own hosts only. Keep original
failures; no arbitrary scientific monitoring deadline. Test bounds describe finite
engineering workloads and do not authorize future live retirement policies.

## Checkpoint 2 — concrete defects and corrections

The reader specialist reproduced five historical API counterexamples: duplicated
or regressing ACKs, damaged tail, missing terminal and late terminal loss retained
a prefix chain. P2 now distinguishes that candidate from a finalized claim and
tests malformed loss/count telemetry. Four development consumer runs preserve the
initial JSONL harness failure and reach 184 passing checks against Build08;
packaged-consumer mismatch is explicit, so P2-Q3 remains open for final-source tests.

The controller now binds the actual DLL worker handle, process birth, session
identity and fresh durable ACK prefix. It uses exclusive ownership and exact STOP
bytes. Specialist source review found that initial finalization ignored closed raw
and ACK tails; independent stopped-session readback and three damaged-closeout
controls correct that defect. The first controller admission test expired before
sole-thread readiness; its cleanup and eventual closeout are preserved. A longer
finite engineering admission wait does not alter the controller's delay policy.

Queue tests disproved the proposed lossless hot-round workload: finite contention
retries can lose events with spare capacity. That workload remains an intentional
loss control. A separately declared paced concurrent envelope must remain lossless.
All producer admissions are compared with consumed IDs/order, including the held
burst. See the two specialist note files for original failures and exact paths.

Native development build `p2-native01` completed 61 cases with zero unexpected
exits but reports `source_unchanged=false` because consumer/test edits overlapped.
It is not final qualification. `p2-native02` is also development. After runtime
sources froze, `p2-native03`, `p2-controller04` and `p2-queue06` began the intended
final qualification. No outcome is promoted before the exact receipts finish.

P2-Q1–Q4 remain INCOMPLETE at this checkpoint. Next actions are final consumer
qualification on native03, complete actual-worker fault/readback tests, source and
historical-evidence preservation, independent review and exact delivery exports.

## Checkpoint 3 — independent challenge and final remedies

The read-only independent reviewer found three further session refusal gaps:
missing READY and contradictory terminal fault count/name could retain a chain.
Nine Generated-return context mutations were also accepted. Baseline receipts
under `p2-reader-review-baseline01` preserve each counterexample before correction.
The reducer now validates Generated context through append and requires complete
READY/output-fault consistency for finalized-session claims. The reviewer and
specialist also identified a sequence-only retirement check; modeled delayed
admission and cross-thread timestamp ties now refuse a birth-through-store join,
while a lifecycle entirely after store remains a positive control. This is a
conditional synthetic ordering result, not a claim about feasible engine timing.
Development qualification reaches 202 passing checks; final packaged-source
qualification remains required.

The reviewer additionally found that a challenge ACK could deny losses already
authenticated in its durable prefix. The controller now checks typed loss/cause
totals, prefix and prior-challenge lower bounds, overflow and output-fault state.
Six added controls test denial, malformed counts, cause mismatch and regression.
The regression case explicitly models a greater prior counter in controller state
without altering the actual worker or its open flush file.

`p2-controller03` and `p2-controller04` preserve intermittent fixture command-read
failures in disk and ACK-flush controls, respectively. The bounded Windows file
read replacement is exercised by `p2-controller05`: all twenty cases pass. Its
consumer/source context predates final reviewer remedies, so it remains a
development result. `p2-native04` also predates those consumer fixes.
The intended final combination is now `p2-native05`, `p2-controller06`,
`p2-queue06` and the final reader receipt. All four questions remain INCOMPLETE
until those results, provenance, review and exports satisfy the frozen contract.

## Checkpoint 4 — final impairment failure and file-open correction

Native05 completes all 61 expected-exit cases with `source_unchanged=true`;
Reader Final01 passes 202 checks with exact packaged-consumer equality. These
are valid bounded results for that combination. Controller06 passes 25/26 cases
but its loss-denial host fails at the command `CreateFileW` check. The command
remains on disk. The original log records the failed line but no Win32 error;
its exact cause is UNKNOWN. This does not establish a parsing defect or a
cybersecurity refusal. The complete failed suite remains preserved.

The fixture now uses the production request reader's read/write/delete sharing
policy and immediately logs any file-open error. Only transient sharing or lock
errors receive finite fixture input retries; other errors fail immediately.
This is an offline command-admission correction, not worker retirement or a
permission workaround. No production source-acquisition or hook semantics change.
The final qualification target is Native06, Controller07 and Reader Final02,
with unchanged Queue06. A second identical-input DLL build, `p2-repro01`, checks
binary reproduction and two independent disposable controls. All final evidence
and review remain necessary; the earlier 25/26 failure is not waived.

## Checkpoint 5 — final engineering evidence and delivery verification

Native06 passes all 61 expected-exit cases with unchanged source. Repro01 uses
identical inputs and produces identical DLL bytes, with two passing controls.
Controller07 passes 26/26 with exact source snapshots unchanged; Sharing01 adds
one passing actual-worker file-publication control. Sharing01 directly observes
error 32 from the former share-read-only contract under a held DELETE-access
handle, then confirms the final reader accepts the published command under that
same handle. It does not recover Controller06's missing original error code.
Reader Final02 passes 202 checks with final packaged-consumer equality, and
Queue06 passes all nine compiled runs. No final engineering test is waived.

`.local-work/d5ab/p2-provenance01/receipt.json` verifies the combined source/DLL/
receipt lineage and 826 original local preservation records. The source observer,
assembly bridges, fixture assembly, patch admission and plugin acquisition source
match HEAD. Original source-lifetime and native observation premises remain open.

A draft review export during active local outputs failed with `PermissionError`
while hashing an excluded artifact; its original traceback did not identify the
path. After the tests closed, Review01 exports both patches and verifies all 25
changed/supplied text paths, scratch forward/reverse bytes, actual-tree reverse
applicability, links, whitespace and unchanged HEAD/index. The excluded artifact
inventory is retained locally. No unreadable artifact is silently skipped.

P2-Q1–Q3 are proposed COMPLETE within their declared engineering scope. P2-Q4
remains INCOMPLETE until independent exact-snapshot review and final delivery
closure. The independent reviewer receives all original contracts, sources,
specialist findings, failed cases and final receipts. Parent questions and P1/P3
dependencies remain as recorded in the unchanged parent mapping.

## Checkpoint 6 — final coverage challenge and original semantic regressions

The final reviewer verified Review02's 25 file hashes, native outputs and all
26 controller receipt/source pairs, then identified missing final-source execution
of original equal-token/different-source and different-token/same-geography
controls. The new 202-check driver did not cover every original semantic fixture.
This is a mandatory coverage gap, not an optional follow-up.

`d5ab_p2_legacy_semantics.py` executes only the exact unchanged owned
`d5ab_qualify.py` semantic AST block, lines 105–230, against final packaged
consumers. It preserves original source and selected block hashes and all
expected constants. All 54 controls pass, including both collisions, altered
ancestry, shuffled arrival, unmatched lifecycle and qualified fresh-boundary
recovery. It does not execute the historical native-session final-chain oracles
that predate P2's stronger API; Final02 independently covers those refusals.
No runtime source or native binary changes. `p2-provenance02` verifies the combined
final evidence including this added receipt. Final review and refreshed delivery
remain required before closing P2-Q4.

## Checkpoint 7 — independent acceptance and bounded closeout

The fresh-context independent reviewer returns **ACCEPT** for Review03, all four
P2 questions COMPLETE and all eight mandatory criteria PASS. The verbatim return
is `.local-work/d5ab/p2-independent-review03.md`. The reviewer independently
checks all 26 file hashes, native output pins, controller per-case receipt/source
pins and all 826 historical preservation records, with zero mismatches. It runs
no build or experiment and authors no implementation. Engineering/completeness
and editorial dispositions are accepted separately from parent science readiness.

The reviewer finds no remaining tractable mandatory P2 branch. Longer randomized
producer/flush-jitter tests near the measured service limit are optional future
work, not performed or used to claim a maximum rate. All initial P2 engineering
branches are resolved by the final receipts and independent challenge; C2 L1/L2
ownership, initialization, cleanup, source lease and actual reuse remain outside
P2 closure and mandatory for P1/P3. Parent D5AB remains INCOMPLETE / REWORK,
D5R OPEN and B2 NOT AUTHORIZED.

Only self-describing closure documentation and refreshed exact exports follow.
The final delivery directory is `.local-work/d5ab/p2-delivery/final01/`; its
manifest, canonical patches and narrow independent closure return control the
delivered snapshot. No code, fixture, schema, test result or scientific claim
changes after the reviewed runtime/source snapshot.
