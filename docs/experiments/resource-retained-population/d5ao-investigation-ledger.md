# D5AO active investigation ledger

2026-11-04, Australia/Sydney. Parent GC-10 / D5R remains OPEN.
Authority is the [original brief](../../implementation-briefs/CODEX_BRIEF_SOR_RG2_D5AO_GC10_observer_perturbation_measurement_validity.md), offline only.

## Frozen contract

The original section 2 questions and section 5 AC01–AC09 are incorporated
verbatim by reference; their meaning and required completion evidence remain
unchanged. No amendment is proposed.

| ID | Original controlling question | Initial status |
| --- | --- | --- |
| D5AO-Q1 | For every repaired counter and its C++/assembly call site, where and under what actual native/observer-held synchronization can retries, yields, sleeps or extra work delay a competing resource-generation request? | INCOMPLETE |
| D5AO-Q2 | Can avoidable blocking or excessive retries on winner-sensitive instrumentation paths be removed while retaining counter correctness, overflow/underflow prevention, event-accounting integrity, and failure provenance? | INCOMPLETE |
| D5AO-Q3 | What demonstrable effect can the old 0.9.1 counter, current 0.9.2 counter and proposed implementation have on task progress and construction-lock admission, especially in close races? | INCOMPLETE |
| D5AO-Q4 | Is the resulting instrument suitable to obtain scientifically interpretable ordinary GC-10 observations, and which kinds of causal and usual-winner conclusions would remain qualified or uncertain? | INCOMPLETE |

## Active branches

| Checkpoint | Branch | Evidence and current disposition | Next action |
| --- | --- | --- | --- |
| Kickoff | Governance and preservation | Initial Git status contains only the supplied untracked brief. Two subagents authorized by section 3.1: specialist census and non-implementing independent reviewer. No live/deployment/Git writes authorized. | Complete reading and retain exact baseline/preservation receipt. |
| Source inspection | Q1 sleep origin | `d5an_counter.h` next/leave call Sleep(1) after failed strong CAS; caller gates may remain held. Queue reservation loops are separate. | Enumerate all receivers, five release edges and lock intervals. |
| Design selection | Q2 alternatives | Single RMW risks forbidden terminal wrap for reservations/active counts. Guarded CAS without voluntary descheduling preserves saturation semantics but has preemption/starvation limits. | Select per-counter strategy after census; retain fault provenance. |
| Test design | Q3 discrimination | Prior uncontended timing does not exercise sleeping in a close race. Need same-target native owned controls, instrumentation-off pairs, historical algorithms and deterministic induced reversal. | Build integrated controls and measure uncertainty. |
| Prospective handoff | Q4 | No N2 authority and no new forecast freeze. D5AM-PRED-01/N0 and PRED-02/N1 remain historical. | Define exact candidate readiness and qualified claim tiers. |

This ledger is created during investigation. Entries are hypotheses or source
observations until their evidence and independent disposition are recorded.

## Investigation checkpoint: preservation, native remedy and fixture failure

`evidence-initial02.json` authenticates all nine N1 originals, twenty selected
protected inputs, 2,704 earlier preserved files and 3,265 final D5AN artifacts.
The latter set explicitly covers final09, the 0.9.2 package, proposal04 and
qualification trees created after the old D5AN kickoff baseline. The new source
baseline binds 3,543 tracked files, current HEAD/index and supplied brief.

The receiver census identifies counter sleeps under native shared/exclusive
ownership and observer publication gates. The new 0.9.3 helper preserves strong
guarded CAS, nonmutation at MAX/zero, LastError, source-attributed failure and
independent producer rollback/teardown. It removes the two voluntary sleeps;
retries/cache-line contention remain. Single unchecked fetch-add/sub was rejected
because terminal wrap would mutate a reservation/active/token value before
refusal. Fault OR and single-writer serial/written operations stay distinct.

Development final01 fails linkage because the new genuine Windows wait/wake
control needs the installed SDK synchronization import library. It is linked
in a fresh derivative; no external installation/download occurs. final02 is
superseded by source changes. final03 exact ABI and scheduler component checks
pass, but do not qualify later builds.

The first sensitivity controls then expose an actual fixture deadlock. The
private typed reader-release stub copies only XADD/MOV/RET; unlike the complete
retail callsite, it omits the conditional wake continuation. A real writer can
therefore remain in infinite WaitOnAddress after the reader decrements. This is
a test implementation failure, not evidence of game behavior or a healthy
performance result. The corrected fixture explicitly calls WakeByAddressAll
after that typed decrement and documents the omitted-continuation substitution.
Fresh final/comparator builds and exact-byte qualification are required. Known
failed owned-host cleanup is recorded separately; no game process is operated.

Independent adverse review also rejects two weaker fixture premises before
final acceptance. A thread's pre-call `entered` flag plus a delay cannot prove
that it reached native wait; the revised control records an actual wait-branch
call and positive packed pending-writer bits before reader release. The global
collision callback can be loaded by the real worker while main updates its
context; the context pointer is now atomic and read once. Prior source snapshots
are superseded rather than excused by a no-crash result. New exact builds and
reader/ABI/native checks remain mandatory.

`cleanup-development01.json` records the known-defect cleanup: four exact task
Python builders stopped, eighteen birth/path/hash/identity-verified owned native
hosts signalled STOP where READY and forcibly closed. These are failed disposable
test executions, never normal finalization. No Starfield or unrelated process
was touched. The initial stale-process query failed before mutation and the
successful correction skips already exited identities; diagnostics are retained.

After the preliminary read-only reviewer finished, a fresh-context final
reviewer was started alongside the native specialist. This follows the reviewer
procedure's anchoring safeguard without exceeding two concurrently active
subagents. Preliminary findings and final acceptance are separate records.

## Exact-final investigation checkpoint

Final05 compiles and passes all 181 expected exits with source unchanged.
The exact ABI suite passes 3,905 assertions and 160 unwind contexts. The scheduler
passes 113 controls, diagnostics pass 181, and composition/replay pass six/111.
Native/helper inspection passes on exact final bytes. The independent
three-envelope qualifier passes 48 rows and 4,092 causal/one scheduler frame per
envelope: twelve close-race reversals with the sleep helper and none with the
bounded/new helpers; all separated controls retain the reference winner.
Real native wait calls and pending-writer bits are positively recorded.

The byte-identical reproduced 0.9.3 NOT-AUTHORIZED package and 473-input N2
proposal/source lock are complete. All 173 owned operational controls and sixty
optimization refusals pass.
The final evidence audit again verifies nine N1 originals, twenty selected
protected files, 2,704 earlier preserved files and 3,265 final D5AN artifacts.
The [report](d5ao-report.md) names the actual receipts and exact identities.

| Frozen branch | Current disposition | Remaining dependency |
| --- | --- | --- |
| Q1 interference census | Resolved at the ordinary receiver/source scope; conditional outer locks explicitly classified | Independent exact-snapshot challenge of the source/native map |
| Q2 remedy and accounting | Resolved by guarded immediate CAS, per-counter invariants and actual adverse controls | Independent exact source/byte/ABI and failure-accounting review |
| Q3 sensitivity and validity | Resolved as an induced native lock-admission effect, with contrary controls and timing limits | Independent raw/paired-oracle and original-question review |
| Q4 N2 fitness/proposal | Resolved as a qualified instrumented-history envelope and exact offline proposal | Independent proposal/editorial review; future forecast/GO remains a separate permission gate |
| Ordinary retail winner/consistency | OPEN parent GC-10/D5R; no ordinary trial performed | Separate prospective forecast, review, live approval and ordinary evidence |

Q1–Q4 are proposed COMPLETE at the original offline scope. AC01–08 have supporting
evidence; AC09 remains pending exact final review/export/handoff. This is not
self-acceptance or permission to integrate or conduct N2. No feasible mandatory
offline branch is silently demoted to optional follow-up.

## Independent completion

The fresh-context read-only reviewer returns ACCEPT on handoff01 and the exact
37-file substantive snapshot: original Q1–Q4 COMPLETE, AC01–AC09 PASS, with
scientific, engineering/evidence and editorial dispositions separate. The actual
return is preserved in `.local-work/d5ao/reviews/final-whole-acceptance.md` and
summarized in [the review](d5ao-review.md). No mandatory feasible offline branch
remains. Closing status-only edits and refreshed exports receive narrow delta
verification. GC-10/D5R, retail frequency, N2 forecast/GO and all historical
failures remain unchanged; this acceptance grants no integration or live action.
