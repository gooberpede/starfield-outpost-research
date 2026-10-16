# Stacking continuation: verification and review

2026-10-16. [Original mandatory contract](../../implementation-briefs/CODEX_BRIEF_SOR_E1_stacking_research_projects.md),
[answer-first report](stacking-report.md), [source pins](stacking-sources.csv).
Scientific result: strong scoped STATIC selection/stacking and Research Project
unlock result. General realized production remains conditional; runtime NOT TESTED.

| Mandatory criterion | Status | Evidence and limit |
|---|---|---|
| 1. Actor list construction/selection | PASS | [Native](stacking-native.md): CrewExtraData creation, handle deduplication, assignment/migration, capacity branches and timer consumer. Full restoration/startup/exception closure not claimed. |
| 2. Active perk/rank selection | PASS | Selected-rank remove/register chain, type-1 competition versus type-2 timer boundary; [matrix](stacking-matrix.md). Actual loaded ranks and named companion quest/template grants unobserved. |
| 3. Research Projects | PASS | [Research](stacking-research.md): all 82 main projects, 20 Outpost projects / 307 recipe gates, completion and status query; direct timer grant absent in inspected definitions/path. Mods/native event-sink closure excluded. |
| 4. Report/register/uncertainty/live value | PASS | Report, matrix, native contract and N110–N133 additions to shared register. P1/P2 narrowed; P3–P9 remain open; former ordinary highest-only live question now duplication NO-GO. |
| 5. Independent review, checks, preservation, package | PASS | Fresh independent ACCEPT and exact current-task/complete package; actual checks and limits below. |

## Actual checks

Installed CPython 3.14.3, `-X utf8 -B research/e1-extractors/verify-stacking.py`:
**PASS 60 checks**, receipt `.local-work/e1-stacking/verification01.json`.
Includes all 16 pre/post protected executable/Ghidra files, ESM identity, complete
selected record counts, recipe gate counts, main-PERK condition negative,
magazine entry ranks, three explicit robot VMAD Boolean encodings, native
locators, 20 direct installed RSPJ headers and unchanged Git index. Integrity,
text-presence and definition checks are not retail execution tests.

Existing regressions, same installed CPython with `-X utf8 -B -m unittest
discover -s save-analysis/scripts`: `-p test_extractor_resources.py` **11 PASS**;
`-p test_save_menu.py` **13 PASS**. They qualify the reused reader lineage and
preserve existing controls; neither suite measures in-game stacking.

The definition reader uses the existing strict owned ESM parser; raw outputs,
NPC/robot fields, script locators and PE candidate receipts stay local. The
ContentResources.zip source pin is unchanged. No original save is read or
modified in this continuation. No game/process/native call, instrumentation,
deployment, configuration or analysis-database mutation occurs. Target survival
is NOT APPLICABLE. Protected-file coverage is the named 16 files, not a new audit
of every historical trace or entire installation.

ReadOnly/noanalysis Ghidra exports 01–13 completed. Export 01's broad Research
symbol selector hit its 256-symbol cap; it is a locator, not an exhaustive
negative. Export 02's literal field scan completed uncancelled: 14,392,060
existing instructions, 1,498 candidates. Candidates were not treated as typed
aliases; the active-bucket writer and callers were then read directly.
Export 04's `140870f60` constructor decompiler failed with an illegal-op error;
instructions are retained and no semantic absence is inferred. Several exact
label probes report NO_FUNCTION_AT (`140ca3670`, `141f06f80`, `140ca3630`);
the first two are supported by existing complete instruction windows instead
of inventing functions. The last is unused. All output/log artifacts remain.

A script-locator attempt used the invalid Python codec name utf8-sig; it failed
before writing. Corrected to utf-8-sig and reran successfully. ExtraFollower was
an examined alternative, rejected because constructors set type 1B rather than
E2. An adjacent condition-registration function `140bfd6a0` proved unrelated;
the report instead cites explicit Game.IsResearchComplete binding and status
query. No failed probe was relabelled a successful semantic check.

## Preservation, prose and review packaging

Baseline `.local-work/e1-stacking/baseline.json` snapshots all 19 pre-existing
uncommitted text files and HEAD/index before this task. Prior production sources,
reports, scripts, brief and raw evidence remain historical. Current-task edits
append continuity/register material or create new files; they do not rewrite
prior results. The complete patch includes earlier uncommitted work; task-only
is relative to those saved baseline bytes, including prior changes in shared
files. The newly retained chat brief belongs to both current-task and complete
patches. Raw native/scripts/definitions, protected installations and review
scratch trees are excluded and retained locally.

The adapted owned exporter checks HEAD/index identity, no staged changes,
UTF-8/LF/no BOM for authored new files, whitespace, Markdown local links and
exact forward/reverse byte application in disposable D:/tools trees. Manifest
and status snapshots accompany patches under `.local-work/diffs/`.
The supplied earlier brief's intentional Markdown hard breaks are preserved;
complete applicability uses nowarn, without silently changing that baseline.
Manual prose audit covers authored/changed Markdown, table labels and function
rows, especially fused words, number/VA/rank spacing, evidence domains and scope.
Mechanical scans supplement it; literal identifiers remain unchanged.

Independent reviewer `/root/stacking_review` returned **ACCEPT**, all five
criteria, at package-review01 manifest SHA-256
`2b3eea2ec22e8a3129c1c04d3af3c39188494f3ddfb432aff8cc5d83f4bee5ba`.
Actual report is retained at `.local-work/e1-stacking/independent-review01.md`.
The reviewer independently checked native selection/rank/type boundaries,
completion/query/NNAM branches, file/baseline/task inventories, exact patch
reconstruction and reverse applicability, 58 source pins, 16 protected inputs,
ESM/ZIP identity, 878 local links, script syntax and whitespace. It inspected
the 60-check and regression receipts rather than claiming to rerun those suites.
It also resolved the registration adjacency ambiguity: `140bfd6a0` belongs to
the preceding record; IsResearchComplete/136a links forward to `140c07e70`.
No scientific defect required rework. The accepted precision improvements name
the prerequisite skills and limit rank-replacement claims to settled transitions.

Final outputs: `.local-work/e1-stacking/package-final01.json`, status snapshot
`status-final01.txt`, and `.local-work/diffs/e1-stacking-final01-{complete,task-only}.diff`.
The manifest supplies exact file/patch SHA-256 hashes and application results.
Final snapshot acknowledgment is retained separately without changing authored
claims afterward. Seven shared pre-existing files have additions only; twelve
prior uncommitted files remain byte-identical, and all 19 original snapshots are
retained. The working tree intentionally contains the research changes and prior
work, with no staged changes or HEAD/index mutation.
Acceptance supplies no integration, publication or live permission.

Suggested Conventional Commit subject:
`docs(research): resolve production stacking and research unlock paths`
