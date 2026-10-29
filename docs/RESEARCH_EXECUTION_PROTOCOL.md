# Research Execution and Completion Protocol

2026-10-11, Australia/Sydney. Prospective policy implemented under
[SOR-D-0049](DECISIONS.md#sor-d-0049--research-execution-and-completion-protocol).
[Governing brief](implementation-briefs/CODEX_BRIEF_SOR_research_execution_completion_protocol.md).
Implementation awaits maintainer integration review; effectiveness awaits a
separately approved step-2 trial. Historical scientific classifications are unchanged.

## Completion means meeting the original contract

The maintainer expects more than half of research hypotheses to fail. This is an
expectation about research, not a failure quota. Preserve falsifications and finish
their negative-result deliverables. Premature termination is the workflow defect.

| Outcome | Closure requirement |
|---|---|
| Completed positive research | Claim supported within stated scope, confidence and evidence standard; coverage and unknowns explicit. |
| Completed negative research | Original scoped negative criteria met with adequate controls, counterexamples, reproducible evidence and limitations; no universal impossibility proof. |
| Completed engineering | Every mandatory acceptance test and deliverable passes, including required review. Five of six mandatory tests is unfinished. |
| Unfinished | Failed tests, unknown initiating fault relevant to acceptance, missing validation or promising in-scope unexamined leads. Documentation alone does not close these. |
| Genuine escalation | Evidenced missing authority, user-only action, safety/integrity limit, inaccessible essential dependency or actual resource exhaustion, with a narrow request. |

An independently reviewed abandonment may close an acquisition method after a
serious bounded feasibility investigation; it leaves the larger scientific aim
open. List alternatives tried, observed failures, remaining plausible branches,
cost and safety reasons. Neither arbitrary test counts nor STRONG PARTIAL closes
an assignment. An accepted scoped STRONG scientific claim remains distinct from
engineering completion, under [the evidence standard](EVIDENCE_STANDARD.md).

## Controlling question and outcome gate

Prospective reinforcement, 2026-10-30, under the
[authorized brief](implementation-briefs/CODEX_BRIEF_SOR_research_completion_governance_reinforcement.md)
and [decision](DECISIONS.md#research-completion-governance-reinforcement---2026-10-30).
This supplements the existing safeguards; historical criteria and verdicts stand.

Every substantive research contract freezes stable IDs for its controlling
questions, success/falsification conditions and required generality. Review the
original question and recorded maintainer-approved amendments, never a narrower
reformulation in the final report. Only explicit recorded maintainer approval
can change a question, applicability, mandatory criterion or blocker definition.
Intermediate models, diagrams, scoped findings and completed files do not change
that contract. Claim confidence/coverage and assignment sufficiency are separate:
a supported partial finding remains useful while the controlling question is open.

| Question status | Required proof and reviewer mapping |
|---|---|
| COMPLETE | Positive answer or adequately controlled scoped negative meets the original question/criteria. ACCEPT requires all mandatory contract outcomes, including review. No universal impossibility proof is required after decisive scoped falsification. |
| INCOMPLETE | Answer outstanding and material authorized work remains, or required validation is missing. REWORK; retain only as checkpoint/handoff, never accepted scientific completion. |
| BLOCKED | Answer outstanding and a specific terminal barrier is evidenced under the proof below. ESCALATE the smallest missing authority/input/capability; this is not scientific completion. |

An independently accepted, separately authorized bounded subtask or negative
method-feasibility result must name its parent question ID and open status.
Method abandonment does not falsify or close the parent scientific question;
production engineering failures remain FAIL/NOT TESTED. If alternative methods
remain viable within the same controlling assignment, continue them or return
REWORK, even if one method has been decisively refuted. An unqualified ACCEPT
is prohibited while any mandatory controlling question is INCOMPLETE or BLOCKED.
A model with unresolved actual engine ordering cannot answer the real scheduling
question merely by enumerating model permutations.

## Dependency ledger and terminal-barrier proof

Create an active investigation ledger near the start, using the existing
experiment/durable-note and local scratch conventions. Update it as material
branches are discovered or tested, not solely at final handoff. Record stable
question/criterion IDs, hypotheses, native/data boundaries, evidence-backed
results, counterexamples, source/investigation paths actually checked, discovered
dependencies, viable untried leads and failed alternatives with reasons. Give
each material branch a disposition: resolved, disproved, irrelevant with evidence,
blocked with evidence, or open; include next concrete action and reproducibility
pointers. Checkpoint/timestamp meaningful changes without fabricated chronology
or routine log volume. Keep raw proprietary evidence local. Summaries and ledger
entries do not replace primary evidence or independent verification.

A material upstream caller, queue, scheduler, streaming ingress, input provenance,
native writer or reasonable alternative observation method is work within the
original question while authorized. Subsystem/document boundaries alone do not
justify deferral. Prioritize by expected discrimination, avoid irrelevant
combinations, and justify boundaries of any genuinely unbounded search, including
why residual paths cannot change the conclusion. Do not demote an essential
unresolved branch to an optional follow-up. Separate authority remains required
for live launch, deployment, database edits, protected-save writes, disclosure
and third-party reuse; continue independent authorized offline work.

A terminal BLOCKED claim must supply all of:

- The exact missing value/data, function/edge, access/safety boundary or
  indispensable action and why it is necessary to answer the frozen question.
- Attempts and verified observations with exact evidence; alternative routes
  considered, why each fails or is unavailable, and residual avenues/impact.
- Barrier class: intrinsic to the method, tool/session/resource limitation, or
  unapproved action. A failed technique does not prove intrinsic impossibility.
- The smallest permission, input, discriminating experiment or capability needed,
  plus an evidence-preserving resume checkpoint and concrete next action.

Unknown callers, failure to find something, further research, time pressure or
reviewer agreement alone are not blocker proof. Tool/session exhaustion needs
observed limits, attempted recovery and durable resume inputs; it is not a
scientific result. A prohibition on live work blocks only the essential live
action after independent offline routes are shown insufficient. Safe STOP always
prevails; no proof requirement authorizes unsafe or prohibited work.

## Contract and proportional method selection

Embed the [compact contract](templates/completion-contract.md) in every substantive
future brief. Identify task type, concrete question/deliverable, scope and bounds,
mandatory versus optional criteria and evidence, negative-result criteria,
continuation authority, exact exit/escalation conditions and review artifacts.
Freeze acceptance criteria before execution. Only the maintainer can approve a
material change; retain the original, amendment, reason and date. Never redefine
criteria to fit an output or quietly omit failed cases.

Before substantial infrastructure work, enumerate viable routes, their evidence
value, verification burden and principal intervention risks. Prefer smaller or
observation-only routes when sufficient. Reassess when infrastructure displaces
the question. Do not lower hard safeguards or add endless gates without a concrete
new risk; obtain maintainer approval for material acceptance changes. Stop testing
when a defensible scoped falsification meets the agreed negative criteria.

## Ownership, continuation and durable checkpoints

**A newly discovered obstacle is work, not a handoff.** The implementer diagnoses
in-scope failures, investigates technically plausible branches, makes warranted
corrections/refactors, reruns relevant regressions and preserves counterexamples.
Diagnostics and requalification are part of the original assignment. Do not ask
for a new brief merely because a test failed. Optional leads outside the contract
are recommendations, not authority to expand research.

Keep durable interim notes, flushed evidence and test ledgers. Use source control
only when explicitly authorized. Checkpoints are not final returns. Resume from
preserved state across compaction; do not falsely promise background execution
or cross-session continuation. Work must actually occur within available execution
opportunities. Actual tool/session/context exhaustion is an escalation with the
observed limit, attempted recovery, durable state and exact resume inputs.

Halt the prohibited action on genuine blockers, preserve evidence/state, report
what failed, attempts and minimal required input, and continue independent
authorized work. Never risk protected inputs to avoid reporting unfinished work.

| Condition | Required response |
|---|---|
| Regression fails within scope | Continue investigation/correction/requalification; reviewer REWORK if submitted prematurely. |
| No event seen, unvalidated detector | Continue controls; no scientific negative closure. |
| New live capture needed under offline authority | ESCALATE only that action, naming proposed intervention and missing permission; do authorized offline work. |
| Protected input hash changes or disk query fails | Halt affected writes/experiment, preserve receipts, request integrity/recovery decision; no overwrite from backup. |
| Essential archive inaccessible after documented locator/access checks | State exact missing input and narrow restoration/access request; do not invent absence evidence. |
| Operator must perform gameplay step | Preserve checkpoint and request that exact user action within approved run card. |

## Roles and independent review

The **Implementer** owns investigation, implementation, tests, evidence, packaging
and reviewer defect remediation. The **Independent Reviewer** inspects the original
contract, primary logs/tests, diff and actual tree; challenges shifted criteria,
excluded failures, unsupported claims, premature stops and unjustified abandonment.
The reviewer is principally read-only, reports proposed changes and must never
accept its own edits. If reviewer authors a correction, another independent
reviewer must assess that change. The **Maintainer** controls scope expansion,
criteria changes, live/destructive/irreversible actions, external disclosure and
integration. Reviewer acceptance supplies none of these permissions.

| Reviewer decision | Effect |
|---|---|
| ACCEPT | Contract satisfied with evidence references and disclosed limits; await maintainer integration. |
| REWORK | Return the same assignment to implementer with criterion-specific defects; fix and resubmit without a fresh user brief. |
| ESCALATE | Specific authority or genuinely terminal evidenced blocker needed; state narrow request and preserved state. |

The independent scientific/completeness reviewer receives the original contract,
approved amendments, active ledger, primary evidence and negative controls,
current tree and proposed claims. Challenge every material unresolved branch:
is it irrelevant, disproved, proven blocked or still tractable within authority?
Independently identify at least the highest-value omitted/untested avenue, or cite
evidence that none remains. Inspect source coverage, counterexamples and
alternative methods. Return REWORK for a tractable mandatory lead; ESCALATE for
a demonstrated terminal authority/capability barrier, preserving the unanswered
question. Accuracy or editorial acceptance cannot substitute for this challenge.
Report engineering/evidence, scientific/completeness and editorial dispositions
separately, with exact reviewed hashes and existing delta-review requirements.

Use the [reviewer instruction and invocation procedure](reviewers/research-completion-reviewer.md).
Check actual session support; policy prose is not an automated orchestrator.
Where unavailable, use its separately initiated manual two-pass fallback. Record
NOT REVIEWED when review cannot run. A mandatory missing reviewer result blocks
accepted completion unless the original contract explicitly allows that fallback.

## Completion accounting and evidence

Prospective editorial completion follows [EDITORIAL_STANDARD](EDITORIAL_STANDARD.md).
The required order is science/code/tests, automatic changed-text screening,
actual manual reading and correction of the entire changed prose set, independent
review of that exact final text and its scientific qualifications, then verified
delivery export. Retain a compliance record with inventory, findings, exceptions
and disposition. Material editorial/scientific defects mean REWORK; a missing
required independent result means unfinished, never accepted completion.
Freeze the reviewed file hashes. Substantive later changes invalidate acceptance
for those changes and require relevant independent delta review. Minor
self-describing review-record closure can use a delta review without restarting
the investigation. This prospective requirement does not revise frozen criteria
or historical verdicts and grants no integration authority.

Every substantial delivery also states controlling-question IDs/statuses
COMPLETE / BLOCKED / INCOMPLETE, scientific claim coverage, engineering/operational
integrity, reviewer disposition, and a short unresolved-dependency disposition
table. A bounded subtask shows parent ID/status visibly. Derive closure from the
original mandatory contract, not from document quality or a narrower result.

Every substantial review return includes every original mandatory criterion as
PASS / FAIL / NOT TESTED, an exact evidence path/location and one-line reason.
Include earlier failed runs, regressions and counterexamples alongside corrections.
Set overall outcome from mandatory criteria; optional successes cannot cancel a
mandatory failure. Separately report:

- Scientific result (positive/negative), tested/inferred/unknown coverage and open questions.
- Implementation/instrumentation integrity and qualification, separate from semantics.
- Target survival, restoration and cleanup, or not applicable.
- Authority/safety compliance and any deviations or permission issues.
- Independent reviewer decision, evidence and reviewed revision, or NOT REVIEWED.

Retain source/tool versions/hashes and measured versus inferred labels. Follow
[WORKFLOW review packaging](../WORKFLOW.md#critical-review-of-every-diff), including
complete/task-only patches, untracked text, status, inclusion/exclusion manifests,
exact content/applicability, whitespace and link checks. Publication eligibility
is independent of confidence and acceptance. No automatic staging/commit/push.

## Existing safeguards and retrospective boundary

These orders supplement rather than replace [AGENTS](../AGENTS.md),
[permissions](PERMISSIONS.md), [third-party policy](../THIRD_PARTY_POLICY.md),
[provenance/version discipline](PROVENANCE.md), [evidence integrity](EVIDENCE_STANDARD.md)
and [publication gates](PUBLICATION.md). Original/archive identity and controlled
copies remain protected. Pins are reverified, never assumed across builds.
The [historical inventory safety plan](experiments/historical-save-inventory-triage.md)
and [event contract](experiments/event-instrumentation/contract.md) document existing
disk/output guards; preserve applicable fail-closed checks and thresholds (including
40,000,000,000-byte C:/D: free-space guards), without treating old experiments as
current authority. Their differing output/time bounds are historical experiment-specific
criteria, not future defaults. Future cards and reused helpers must follow
[scientific experiment continuation and health](../WORKFLOW.md#scientific-experiment-continuation-and-health);
essential additional hard limits require concrete justification and maintainer
approval before a live run. Historical violations and verdicts remain unchanged.
The [operator run card](experiments/event-latency/center-only-live-run-card.md) shows
explicit live actions, pins, recovery and protected-save rules; it is historical,
not new launch/attachment authorization.

[External debugger failure analysis](experiments/event-latency/thread-control-final-report.md)
and [review](experiments/event-latency/thread-control-final-review.md) support
abandonment of that acquisition approach, not falsification of the outpost position
model. This protocol does not reopen debugger engineering or promote that historical
review to a new independent ACCEPT.

## Worked disposition examples (illustrative, not experimental results)

1. Engineering contract requires six retirement controls. Primary ledger shows
   five PASS and one unsafe queued-trap FAIL. Reviewer returns **REWORK** citing
   the failed criterion. Implementer diagnoses and retests within authority,
   preserves the failure, resubmits. If bounded feasibility warrants abandonment,
   reviewer adversarially assesses that separate closure proposal; no fake PASS.
2. Hypothesis predicts unchanged archived bytes across a specified action/control
   pair. Validated framing, immutable input hashes and independent offset checks
   show the predicted equality false while the no-action control holds. If this
   meets the original scoped falsification criteria, reviewer can **ACCEPT** the
   completed negative report. General impossibility and live authority remain open.
3. Offline analysis needs a live discriminating action for its remaining required
   criterion. No approved live card exists. Reviewer returns **ESCALATE** naming
   the precise missing authority; implementer preserves offline results and asks
   for that bounded decision. The incomplete scientific criterion remains visible.

## Step-2 recommendation only

Recommend a bounded existing-data hypothesis: do the already archived S2/S2C and
S3/S3C controlled object/link records suffice to associate the placed extractor
with its resource definition? At trial planning, verify those labels and actual
actions in [the manual corpus report](experiments/manual-save-corpus-S0-S7C.md);
do not assume filenames identify extractor content. If they are unsuitable, ask
the maintainer to amend inputs before execution rather than invent ground truth.

Example contract: **research hypothesis**; deliver an offset/identity-backed
association or completed scoped insufficiency/falsification report. Inputs are
only hash-verified existing controlled archives, prior manifests and existing
definition summaries. Read-only offline analysis and original bounded utilities
only; no new saves, game, debugger, deployment, dependencies or disclosure.
Mandatory: verified input/action provenance; validated framing/identity mapping;
action/no-action comparison; independent definition/offset check; alternatives
and counterexamples; evidence ledger, complete review package and independent
decision. Optional: historical generalization. Negative closure requires showing
why the specified representations cannot distinguish the candidate associations
with these controls, or a decisive counterexample to the proposed mapping;
a failed search/parser alone is insufficient. Continuation covers diagnostics,
fixes and retests within those inputs; escalate unavailable essential inputs or
need for live ground truth. Freeze this into a separate approved brief before
running. Reviewer reads primary comparisons, returns REWORK for missing controls,
ACCEPT for supported positive or scoped negative closure, ESCALATE for new live
authority. **The trial has not been conducted.**
