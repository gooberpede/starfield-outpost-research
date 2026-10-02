# Research and Implementation Workflow

## Decision and integration path

**Discuss and agree scope -> issue a downloadable implementation/audit brief -> receive explicit execution instruction -> perform the bounded work -> return evidence and complete changes -> critical diff review -> user-approved integration.**

The initial scaffold was requested directly as a ZIP, not through a Codex brief. This is a recorded setup decision, not an exception that authorizes future unbriefed implementation.

Implementation and audit briefs are downloadable `.md` files and are retained in [docs/implementation-briefs/](docs/implementation-briefs/README.md). A short correction may be delivered in chat; substantial corrections/follow-ups need a durable Markdown brief. Record accepted corrections beside the work they govern.

Reading a brief does not authorize every action it mentions. Identify permitted operations, especially deployment, live observation, process intervention, save changes, external communication, and repository writes. When blocked, stop the affected action, explain the missing evidence or approval, and continue only unrelated authorized work.

## Question-led research loop

1. Select a bounded question from [the subsystem map](docs/subsystems/README.md). Review existing findings, alternatives, and relevant third-party sources.
2. Complete the necessary source/permission gates before incorporating material or using an external implementation. Record source-specific facts separately from project validation.
3. Write an experiment plan using [the template](docs/templates/experiment.md): hypothesis or question, controls, baseline, actions, evidence, success/falsification criteria, risk, stop, and cleanup.
4. Execute only after authorization. Capture observations before interpretation; include negative results and deviations. Runtime and save analysis may alternate within the approved scope.
5. Validate interpretations on independent examples or repetitions appropriate to the claim. State exactly what remains untested.
6. Update the experiment, relevant subsystem notes, registers, and [RESEARCH_STATE.md](docs/RESEARCH_STATE.md). Do not overwrite historical evidence to make it fit a new model.
7. Propose the next bounded step; do not automatically begin it.

No fixed language, debugger backend, save parser, or instrumentation framework has been selected. Reusing tooling from a sibling project requires provenance and authorization, not an assumption that adjacent work is already in scope.

## Critical review of every diff

Review against the governing brief and accepted corrections, not only the implementation summary. Assess requirement conformance; omissions and unsupported claims; scope creep; regressions; source permission and credit; privacy/rights boundaries; evidence quality; tests and their coverage; reproducibility; documentation consistency; and integration readiness.

Report blockers separately from non-blocking improvements. State what was independently checked and what was merely reported. A checksum verifies bytes, not their interpretation. No live run must remain clearly distinguishable from a passed live validation.

Include all new files. An unstaged `git diff` alone can omit untracked files. The user may stage reviewed files and export a full patch with Git's own output option:

```powershell
New-Item -ItemType Directory -Force '.local-work\reviews' | Out-Null
git status --short
git diff --cached --check
git diff --cached --binary --output='.local-work/reviews/review.diff'
```

Only stage material already cleared for this repository. `--binary` makes a patch complete; it does not authorize sending binary evidence. Inspect the export before sharing. Avoid PowerShell redirection or `Out-File` for patch serialization; keep review exports out of commits. These commands are owner-operated examples, not agent authorization to stage.

## Durable state and text

Use stable IDs defined in [EVIDENCE_STANDARD.md](docs/EVIDENCE_STANDARD.md), relative links, and ISO dates. Record actual timestamps and timezone when material. Unknown values remain `UNKNOWN`, not guessed. Do not infer the current executable/tool baseline from a prior project's version.

Authored text is UTF-8 without BOM with LF endings, except Windows batch files configured for CRLF. Exact-byte evidence under `docs/experiments/evidence/` is protected from automatic Git text conversion, except authored `README.md` files. Do not normalize an original capture in place: make a separately named derivative and record input/output hashes and the transformation.

## Scientific and publication milestones

The programme is broad; an agreed first-publication scope must be bounded and contain both runtime and persistence objectives. Do not quietly drop an unresolved required topic. Record scope changes and their reasons in [DECISIONS.md](docs/DECISIONS.md).

The user's publication objective is mandatory, but not permission to disclose prematurely. Apply [PUBLICATION.md](docs/PUBLICATION.md) to release contents and the history that would become public. Later product decisions follow the completed and published research, not the reverse.
