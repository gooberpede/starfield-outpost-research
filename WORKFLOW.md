# Research and Implementation Workflow

## Decision and integration path

**Discuss and agree scope -> issue a downloadable implementation/audit brief -> receive explicit execution instruction -> perform the bounded work -> return evidence and complete changes -> critical diff review -> user-approved integration.**

The initial scaffold was requested directly as a ZIP, not through a Codex brief. This is a recorded setup decision, not an exception that authorizes future unbriefed implementation.

Implementation and audit briefs are downloadable `.md` files and are retained in [docs/implementation-briefs/](docs/implementation-briefs/README.md). A short correction may be delivered in chat; substantial corrections/follow-ups need a durable Markdown brief. Record accepted corrections beside the work they govern.

Reading a brief does not authorize every action it mentions. Identify permitted operations, especially deployment, live observation, process intervention, save changes, external communication, and repository writes. When blocked, stop the affected action, explain the missing evidence or approval, and continue only unrelated authorized work.

## Execution and completion contract

The [Research Execution and Completion Protocol](docs/RESEARCH_EXECUTION_PROTOCOL.md)
controls assignment completion, continuation, escalation and independent review.
Embed its compact [contract](docs/templates/completion-contract.md) in every
substantive future brief; trivial corrections need only proportionate criteria.
Freeze mandatory criteria unless the maintainer approves a material change.
A newly discovered obstacle is work, not a handoff: diagnose, correct and retest
within existing authority. Diagnostics and requalification belong to the same
assignment. Adequately tested scoped negative research is completed research;
failed mandatory engineering tests remain unfinished work. Never invent a PASS.

Use an independent reviewer against the original contract and primary evidence.
ACCEPT, REWORK and ESCALATE have the meanings in the protocol. REWORK returns the
same assignment for correction and resubmission without a new brief. Halt unsafe
or unauthorized actions and evidence genuine blockers; continuation never waives
existing permission, protected-input, live-operation or publication gates.
Return a mandatory-criterion PASS / FAIL / NOT TESTED matrix, preserved failures,
separate outcome dimensions and verified review patches under the rules below.
See the [reviewer procedure](docs/reviewers/research-completion-reviewer.md) for
session-specific invocation, access limits and the manual two-pass fallback.

## Question-led research loop

Apply the [scoped-conclusion, coverage and reporting rules](docs/EVIDENCE_STANDARD.md#scoped-conclusions-and-coverage). Within the approved scope, select authorized offline tests by information gain; this does not waive experiment approval or the review required for durable promotion/reclassification. Answer substantive research questions before listing limitations.

1. Select a bounded question from [the subsystem map](docs/subsystems/README.md). Review existing findings, alternatives, and relevant third-party sources.
2. Complete the necessary source/permission gates before incorporating material or using an external implementation. Record source-specific facts separately from project validation.
3. Write an experiment plan using [the template](docs/templates/experiment.md): hypothesis or question, controls, baseline, actions, evidence, success/falsification criteria, risk, stop, and cleanup.
4. Execute only after authorization. Capture observations before interpretation; include negative results and deviations. Runtime and save analysis may alternate within the approved scope.
5. Validate interpretations on independent examples or repetitions appropriate to the claim. State exactly what remains untested.
6. Update the experiment, relevant subsystem notes, registers, and [RESEARCH_STATE.md](docs/RESEARCH_STATE.md). Do not overwrite historical evidence to make it fit a new model.
7. Propose the next bounded step; do not automatically begin it.

No project-wide debugger backend or instrumentation framework is mandated; each experiment records its selection. Maintainer-authored sibling tooling has standing reuse authorization under [SOR-P-0002](docs/PERMISSIONS.md#sor-p-0002--standing-maintainer-owned-material-grant); provenance and experiment/execution scope still apply. Third-party components remain separately gated.

## Scientific experiment continuation and health

Prospective save preservation follows [SAVE_PROTECTION](docs/SAVE_PROTECTION.md):
protect explicitly designated research saves, manual saves and quicksaves;
exclude reliably classified active exitsaves/autosaves from preservation/equality
gates while retaining diagnostics; fail closed on unclassified saves. An explicit
research designation overrides kind and requires independently verified backup
readiness. Historical evidence and backup records remain strict. Apply this
classification consistently before reusing a legacy operational helper; old
manifests and failed-run verdicts remain historical, not rewritten baselines.

Prospective correction, 2026-10-12, under the [fallback-grid brief](docs/implementation-briefs/CODEX_BRIEF_SOR_fallback_grid_provenance_and_workflow_policy.md).

**Elapsed time, evidence volume, a delayed operator action, or a routine monitoring-cadence overrun alone must not terminate an otherwise healthy scientific experiment.** Do not invent hard session/admission deadlines, event counts, evidence-size quotas or arbitrary capture cutoffs. Preserve the **40,000,000,000-byte caller-available free-space guard on both C: and D:**, verified target/plugin identities and instruction guards, protected inputs, instrumentation/evidence integrity, actual worker failure, and explicit operator STOP.

Health checks must distinguish an actual failure (for example a failed worker, corrupt evidence, identity/guard mismatch or failed free-space protection) from a slow operator response or delayed routine poll. During an unexpected delay, warn and continue where safe; consult the operator before terminating solely for the delay. A missed monitoring interval remains a recorded deviation, not proof of worker failure. Never retrospectively redefine a violated approved limit as a pass.

If an additional hard limit is essential for a demonstrable safety or engineering reason, document that reason, its exact trigger and recovery behavior, and obtain maintainer approval **before the live run**. Finite question/action scope and memory/queue integrity controls remain required; they do not justify arbitrary scientific event quotas. Scientific completion, evidence integrity, process health and target survival are separate outcomes.

Apply this policy to every future run card and its operational helper configuration. Historical cards, approved limits, failed criteria and results remain immutable historical records; this correction neither reruns them nor changes their verdicts. An old card/helper must be prospectively reviewed against this policy before reuse. No safety control may be silently removed for throughput.

## Critical review of every diff

Every substantive future Codex delivery must follow the mandatory
[editorial finalization standard](docs/EDITORIAL_STANDARD.md): finish science and
tests, screen changed authored text, manually read and correct the complete
changed prose set, obtain independent review of the exact final snapshot, then
verify/export its diffs and manifest. Preserve diagnostics, exceptions and review
disposition. Substantive post-review edits require independent delta review;
material prose or scientific-qualification defects return the same task as REWORK.
The screen alone never satisfies finalization. Historical contracts are unchanged.

For prospective approved observer sessions, use the [shared phase-aware
commands](runtime/session-tools/README.md) and [future run-card fragment](docs/experiments/session-infrastructure/future-run-card.md).
Perform full protected-content/save audits before launch and after exit; use
hash-bound prelaunch receipts and lightweight READY/ACK/health checks during play.
Only a specific documented integrity incident justifies a full live rescan.
After offline postflight, seal and stream-verify a lossless archive while keeping
raw originals. The [infrastructure qualification](docs/experiments/session-infrastructure/report.md)
does not authorize a live run or revise historical cards and verdicts.

Review against the governing brief and accepted corrections, not only the implementation summary. Assess requirement conformance; omissions and unsupported claims; scope creep; regressions; source permission and credit; privacy/rights boundaries; evidence quality; tests and their coverage; reproducibility; documentation consistency; and integration readiness.

Report blockers separately from non-blocking improvements. State what was independently checked and what was merely reported. A checksum verifies bytes, not their interpretation. No live run must remain clearly distinguishable from a passed live validation.

For every implementation, audit, documentation and research review, retain review
patches in `D:\Projects\starfield-outpost-research\.local-work\diffs\`. Use a
consistent descriptive task prefix and these coverage suffixes:

- `<task>-task-only.diff`: changes attributable to the current task.
- `<task>-complete.diff`: all uncommitted changes since HEAD, including untracked
  text files and earlier uncommitted work.

When prior uncommitted work exists, supply both patches; otherwise supply at
least the complete patch. A supplied, previously untracked brief belongs in the
complete patch and is identified separately from task-authored changes. Ordinary
`git diff` omits untracked files: append valid Git-style new-file text patches,
without staging to construct diffs. Preserve exact text/newline semantics and
identify renames, deletions, generated scripts and new documents distinctly.
Ambiguous `review.diff` or `cumulative.diff` names without coverage labels are
insufficient. Existing historical packages are not retroactively renamed.

Supply `git status --short`, a changed-file manifest, an exclusions manifest for
ignored/binary/raw artifacts, and verification of patch completeness and
applicability against the actual working tree. Check `git diff --check`, new-file
whitespace and internal links. Reverse applicability alone does not prove complete
coverage: compare the patch path inventory and contents with Git's tracked and
untracked text inventory. Do not stage merely for review export. Keep exports
ignored/local, serialize bytes without PowerShell text redirection, and inspect
payloads before sharing. Exclude raw saves, memory, proprietary binaries/assets,
analysis databases and other uncleared data; report local locations and hashes.
An exclusion is disclosed rather than silently labelled complete. No export,
binary patch option or private remote clears publication or staging permission.

## Durable state and text

Routine Cargo evidence preservation uses the
[active archive baseline](docs/experiments/cargo-evidence-cutover/active-baseline.json)
and its pinned `routine_command`, following the
[authorized retirement](docs/experiments/cargo-evidence-cutover/execution.md).
Authenticate the committed baseline, archive/index and three loose holds rather
than hashing the 1,051 retired payloads. Scientific use restores and verifies
members explicitly. This Cargo-only selection does not change save protection,
other-system checks or historical inventory identities.

Create disposable review-patch application/comparison trees under
`.local-work/review-patches/`, creating the parent before allocating a unique
child. Keep exported review diffs under `.local-work/diffs/`. Each
exporter's Git environment must stop parent-repository discovery at
`.local-work/` (using `GIT_CEILING_DIRECTORIES`) so scratch application checks
operate on the standalone tree. Normal Git reads from the repository root
continue to use the repository. The
[2026-10-19 housekeeping brief](docs/implementation-briefs/CODEX_BRIEF_SOR_review_scratch_housekeeping.md)
records the relocation of earlier `D:/tools/sor*` trees; historical receipts and
snapshots retain their original paths and bytes.

Use stable IDs defined in [EVIDENCE_STANDARD.md](docs/EVIDENCE_STANDARD.md), relative links, and ISO dates. Record actual timestamps and timezone when material. Unknown values remain `UNKNOWN`, not guessed. Do not infer the current executable/tool baseline from a prior project's version.

Authored text is UTF-8 without BOM with LF endings, except Windows batch files configured for CRLF. Exact-byte evidence under `docs/experiments/evidence/` is protected from automatic Git text conversion, except authored `README.md` files. Do not normalize an original capture in place: make a separately named derivative and record input/output hashes and the transformation.

## Scientific and publication milestones

The programme is broad; an agreed first-publication scope must be bounded and contain both runtime and persistence objectives. Do not quietly drop an unresolved required topic. Record scope changes and their reasons in [DECISIONS.md](docs/DECISIONS.md).

The user's publication objective is mandatory, but not permission to disclose prematurely. Apply [PUBLICATION.md](docs/PUBLICATION.md) to release contents and the history that would become public. Later product decisions follow the completed and published research, not the reverse.
