# Independent review and handoff

[Original brief](../../../implementation-briefs/README.md#archive-lookup) (`implementation-briefs.zip :: docs/implementation-briefs/CODEX_BRIEF_SOR_experiment_A_x87_state_preservation.md`),
[report and exact field comparisons](report.md), [mandatory matrix](validation.md),
[correction eligibility recorded before implementation](correction-plan.md),
[source/commands](../../../../research/x87-preservation/README.md).

Independent decision: **ACCEPT**, corrected scoped offline **PASS**. Original
uncorrected route remains FAIL. No observer, live or Git action is authorized.

An explicitly authorized fresh-context reviewer independently reads the original
contract, baseline/source/generated assembly, raw frame bytes, regression/build
receipts, protected pins and complete/task-only changes. Its first design pass
confirmed correction eligibility and the before/entry/context/after distinction.
It identified deterministic STOP-in-flight as a coverage concern; final paired
runs hold a handler across admission closure and retain that assertion in logs.
The correction itself did not change. Formal **ACCEPT** applies to package SHA256
`6757d9c6d3a218b33b65dff1651b0ff1e4608f8d733f156513a33a21e9e025c6`.
That exact package, both patches and all reviewed text are retained under local
`review01/`; the actual return is `reviewer-formal-accept.txt`.

The reviewer independently parsed the raw final state corpora, checked all
required x87 and GP/flags/XMM/YMM fields, reconstructed the invocation-owned
restore image, rehashed 206 selected preservation pins and 146 evidence files,
and reconstructed both patches exactly against HEAD and current bytes. It
inspected all 16 task files plus the supplied brief, including authored prose,
tables, spacing, count distinctions, Markdown, UTF-8/LF, whitespace and relative
links. HEAD, index and reviewed worktree hashes stayed stable. Native execution
and the seven regression commands were not rerun by the reviewer; those results
are receipt-backed and source-reviewed. Acceptance is bounded to the stated
masked fixture state, CPU/Windows installation, nesting and R15-owned storage.
This final reporting update changes only this review record; it does not change
source, experiments, criteria or scientific conclusions.

Local review artifacts under `.local-work/x87-preservation/` include manifests,
preservation receipts, primary run evidence and package.sha256. Both patches
include all task-authored text; the complete patch also contains the supplied
unchanged untracked brief:

- `.local-work/diffs/x87-preservation-task-only.diff`
- `.local-work/diffs/x87-preservation-complete.diff`

The packaging checks enumerate tracked and untracked changes without staging,
validate UTF-8/LF and added/new-line whitespace, relative Markdown link targets,
patch path/content inventories and exact forward/reverse application in disposable
text trees. The exclusions manifest identifies ignored native binaries, raw
synthetic evidence and receipts; none is silently labelled shared text.
Manual prose review covers spaces around addresses/counts, terminology and
Markdown. Hashes identify bytes, not scientific correctness or publication rights.

Suggested Conventional Commit subject:
`test(research): qualify x87 preservation across exception continuation`

Await maintainer critical review. A scoped PASS resolves this offline question;
it neither justifies automatic retail instrumentation nor changes the rejected
0.8.0 candidate, Experiment B deferral or native spatial NOT TESTED status.
