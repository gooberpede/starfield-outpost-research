# Independent completion reviewer instructions

Read [AGENTS](../../AGENTS.md), required repository guidance, the original invoked
brief and accepted amendments, its frozen completion contract, and the
[protocol](../RESEARCH_EXECUTION_PROTOCOL.md). Review primary evidence, not just
the implementer report. This is an instruction document, not a globally installed
agent profile or configuration change.

## Access and checklist

Remain read-only: no file edits, staging, commits, pushes, worktree creation,
game/process operations, dependency installs or external disclosure. Do not run
experimental scripts without their explicit scope authority. Read local receipts
only within authorized paths; keep private/raw evidence local. Report suggestions
to the implementer. Never accept your own corrections.

- Match every original mandatory criterion to primary evidence and actual tree.
- Inspect patches including untracked text and exclusions; verify snapshot identity.
- Challenge missing tests/oracles, excluded failures, retroactive criteria changes,
  premature stopping and scientific claims exceeding coverage.
- Inspect regressions/counterexamples, integrity, provenance, permissions, cleanup
  and separate scientific/engineering/target outcomes.
- For abandonment, challenge alternatives actually explored, failures, remaining
  plausible branches and cost/safety justification without universal impossibility.
- Return exactly ACCEPT, REWORK or ESCALATE, with criterion-specific reasons,
  evidence references, tested versus merely reported checks and remaining limits.

## Mandatory scientific completeness challenge

Use the protocol's [question-level gate](../RESEARCH_EXECUTION_PROTOCOL.md#controlling-question-and-outcome-gate).
Obtain the original questions/required generality, approved amendments, active
ledger, primary evidence/negative controls, current tree and proposed claims.
Missing mandatory review inputs require REWORK; an evidenced inaccessible essential
input requires ESCALATE. Do not accept a final-report reformulation of the question.

For each material dependency, record whether it is resolved, disproved,
irrelevant with evidence, blocked with evidence, or open and tractable. Audit
checked source paths, counterexamples and alternative methods directly. Name at
least the highest-value omitted/untested avenue, or the evidence showing none
remains. An accurate model, clean hashes and editorial ACCEPT do not establish
scientific sufficiency. Verify that the ledger was maintained during work;
a retrospective alone fails that requirement.

Return REWORK for any tractable mandatory lead, silent narrowing or missing
validation. Return ESCALATE only with the protocol's terminal proof and smallest
request; preserve the unfinished question. ACCEPT requires completed mandatory
contract outcomes, including adequately controlled scoped falsification; do not
demand universal impossibility after decisive negative completion. A separately
authorized bounded method NO-GO may be accepted only with visible parent ID/open
status and engineering failures preserved. Viable alternatives in the same
controlling assignment still require REWORK. Report question statuses, criterion
matrix, claim coverage, engineering/evidence and editorial dispositions and a
short unresolved-branch table separately. Never accept your own edits.

## Session tool procedure

For substantive future deliveries, independently enforce
[EDITORIAL_STANDARD](../EDITORIAL_STANDARD.md), separately from scientific tests:

- Check the complete changed authored prose inventory, including tables, captions,
  CSV labels, explanatory comments/docstrings and edits to existing documents.
- Read the exact final changed prose; inspect screen diagnostics, manual coverage,
  corrected defects and reasoned exceptions. A zero-diagnostic scan is insufficient.
- Challenge joined words/numbers, punctuation spacing, concatenations, encoding,
  Markdown and evidence links, and disproportionate or ambiguous numeric notation.
- Check evidence strength, attempt/path and pointer/epoch distinctions, source/
  terrain/beacon identity, consistent terminology and summary/detail agreement.
  Unsupported certainty is a scientific defect.
- Return REWORK for material defects or missing required coverage. Bind disposition
  to exact file hashes. Review substantive post-review deltas independently;
  small self-describing closure records may receive a narrow delta review.

Report editorial disposition separately from scientific conformance. These
prospective checks preserve original contracts, reviewer authority and all gates.

Recheck tool availability each session. In the implementing session, use
`collaboration.spawn_agent` with a separate reviewer task, inherited model and
the instruction above, original brief path, report/contract path, primary receipt
directory and diff paths. The invoked step-1 brief authorizes this documentation
dry run; future delegation still needs applicable authorization. Use a fresh
context (`fork_turns: "none"`) to reduce narrative anchoring. Supply explicit
repository cwd and mandatory reading. Tools share the filesystem; read-only is an
instruction boundary, **not an enforced separate sandbox**. Snapshot reviewed
file hashes/index/HEAD before and after. A changed review snapshot invalidates
acceptance for those changes and requires re-review.

Wait for the agent's result using `collaboration.wait_agent` and retain the actual
return. On REWORK, implementer corrects under the same contract, regenerates
checks/patches and calls `collaboration.followup_task` with the defect disposition,
new hashes and evidence. Repeat until ACCEPT or evidenced ESCALATE. Do not claim
unattended scheduling or cross-session continuation. `send_message` can clarify
scope with the reviewer; it does not itself restart an idle agent.

## Manual two-pass fallback and exact handoff

If those tools are absent, uncertain or not authorized, the maintainer initiates
a separate reviewer session in the same repository; no automatic orchestration
is claimed. Supply this prompt with the actual paths filled in:

> Independently review the unchanged original brief <path/hash>, accepted
> amendments <paths or none>, contract <path>, report/matrix <path>, primary
> receipts <directory>, complete and task-only patches <paths/hashes>, status
> and inclusion/exclusion/check manifests <paths>. Read required repository
> guidance and docs/reviewers/research-completion-reviewer.md. Stay read-only
> under its boundaries. Check actual working-tree hashes against the manifest.
> Return ACCEPT / REWORK / ESCALATE with criterion-by-criterion evidence and
> exact defects or narrow authority request. Do not implement fixes or authorize
> integration, staging, commit, push, live actions or the step-2 trial.

Maintainer transfers that decision verbatim to the implementer. REWORK continues
the same assignment; implementer provides defect dispositions and refreshed
artifacts for the separately initiated re-review. If no reviewer can run, record
NOT REVIEWED and the capability/authority reason. Never relabel self-review as
independent acceptance. For this step-1 task the original brief explicitly permits
that disclosed fallback; future contracts must state their own review requirement.
