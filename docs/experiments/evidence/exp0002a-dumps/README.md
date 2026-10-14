# SOR-EV-0007 — offline DR0 crash comparison

2026-10-07. [Authored analysis](../../../audits/exp0002a-crash-dump-comparison.md), [authorization](../../../implementation-briefs/EXP0002A-offline-dump-comparison.md). Review-required summaries only; raw artifacts LOCAL-ONLY and ignored. No raw dump is incorporated in this directory.

SOR-EV-0007-A is original `Starfield.exe.10364.dmp`, analyzed from the existing `crash-012-host/artifact-000.dmp` archive. SOR-EV-0007-B is original `Starfield.exe.15608.dmp`, analyzed from `s2-crash-records/artifact-000.dmp`. Archive root is `.local-work/exp0002a-adapter-0.1.3/`; complete identities/hashes/timestamps are in the report. Originals and archives are byte-identical and unchanged. Dump MiscInfo PIDs confirm the original correlation.

New derivative root: `.local-work/exp0002a-dump-comparison/`:

| Artifact | Role |
|---|---|
| input-manifest.json | Original/archive path, filename, size, SHA-256, creation and last-write timestamps |
| tool-hashes.json; format-source-hashes.json | Installed CDB/dbgeng/dbghelp and SDK declaration provenance |
| commands.txt; analyze.py | Exact CDB extraction sequence and invocation; analyze.py also records the starting worktree snapshot and must not be rerun over this evidence root |
| broad-012.cdb.txt; single-013.cdb.txt | Independent Microsoft exception/register/stack/module/disassembly/stream output |
| broad-012.extracted.json; single-013.extracted.json | Bounded raw-reader extracts, original dump SHA-256 and exact file offsets |
| application-events.json | Fresh unelevated Application 1000/1001 evidence, three matching events per run |
| wer-access.json | Exact matching ReportArchive access denials, no elevation attempted |
| verify.py; verification.json | Re-extraction equality, final four-file hash/size checks, context cross-checks, PE/site equality, address normalization, adapter event counts and matching stacks |
| artifact-manifest.json | Hash inventory of new analytical inputs/outputs/scripts, excluding the manifest itself and review products |
| review-checks.json; review.py | Markdown links, whitespace, task-only changed-file list, raw exclusion and preserved prior file checks |
| task-only.diff | Actual this-task diff against the starting worktree, including new files |
| git.diff; untracked-files.diff; git-status-short.txt | Aggregate tracked Git diff, complete nonignored untracked-file review diff, and literal git status --short |

Reproduction: use the [reader](../../../../debugger/exp0002a/inspect_minidump.py) with an explicit archived dump, pinned EXE, and a **new** output filename inside the ignored comparison root. CDB invocations use `-z`, installed tools and local symbol/image directories; do not substitute a live attach command. Reader output is a private derivative, not cleared publication material. No proprietary dumps, memory images, stack text or binaries are newly tracked.

Validation: both CDB invocations returned 0; both raw extracts independently reproduce; all extracted faulting ThreadList/exception register values agree; code-window bytes/hash and preferred-base normalization match the pinned PE; raw first returns and 13-frame CDB address chains agree; original/archive sizes and four SHA-256s unchanged. Remaining review checks and exact counts are in review-checks.json. No new third-party implementation/header was incorporated. Existing maintainer adaptation remains unchanged. Actual scientific limits include partial memory coverage, no private PDB, saved DR6 without a cause bit, absent adapter research exception delivery, and no recovered completion/exit-code contract.

Final review checks passed: git diff --check exit 0; 123 internal Markdown links across all 15 task-changed files resolve; no trailing whitespace in task-changed files; reader syntax passes; no nonignored/tracked DMP/EXE/SFS/DLL/OBJ/PDB files; no prior adapter implementation changed. Aggregate Git status includes pre-existing uncommitted work; task-only.diff isolates this analysis.
