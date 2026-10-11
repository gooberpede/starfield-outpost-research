# Research and Implementation Workflow

## Decision and integration path

**Discuss and agree scope -> issue a downloadable implementation/audit brief -> receive explicit execution instruction -> perform the bounded work -> return evidence and complete changes -> critical diff review -> user-approved integration.**

The initial scaffold was requested directly as a ZIP, not through a Codex brief. This is a recorded setup decision, not an exception that authorizes future unbriefed implementation.

Implementation and audit briefs are downloadable `.md` files and are retained in [docs/implementation-briefs/](docs/implementation-briefs/README.md). A short correction may be delivered in chat; substantial corrections/follow-ups need a durable Markdown brief. Record accepted corrections beside the work they govern.

Reading a brief does not authorize every action it mentions. Identify permitted operations, especially deployment, live observation, process intervention, save changes, external communication, and repository writes. When blocked, stop the affected action, explain the missing evidence or approval, and continue only unrelated authorized work.

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

## Critical review of every diff

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

Use stable IDs defined in [EVIDENCE_STANDARD.md](docs/EVIDENCE_STANDARD.md), relative links, and ISO dates. Record actual timestamps and timezone when material. Unknown values remain `UNKNOWN`, not guessed. Do not infer the current executable/tool baseline from a prior project's version.

Authored text is UTF-8 without BOM with LF endings, except Windows batch files configured for CRLF. Exact-byte evidence under `docs/experiments/evidence/` is protected from automatic Git text conversion, except authored `README.md` files. Do not normalize an original capture in place: make a separately named derivative and record input/output hashes and the transformation.

## Scientific and publication milestones

The programme is broad; an agreed first-publication scope must be bounded and contain both runtime and persistence objectives. Do not quietly drop an unresolved required topic. Record scope changes and their reasons in [DECISIONS.md](docs/DECISIONS.md).

The user's publication objective is mandatory, but not permission to disclose prematurely. Apply [PUBLICATION.md](docs/PUBLICATION.md) to release contents and the history that would become public. Later product decisions follow the completed and published research, not the reverse.
