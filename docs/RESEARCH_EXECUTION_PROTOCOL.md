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

Use the [reviewer instruction and invocation procedure](reviewers/research-completion-reviewer.md).
Check actual session support; policy prose is not an automated orchestrator.
Where unavailable, use its separately initiated manual two-pass fallback. Record
NOT REVIEWED when review cannot run. A mandatory missing reviewer result blocks
accepted completion unless the original contract explicitly allows that fallback.

## Completion accounting and evidence

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
