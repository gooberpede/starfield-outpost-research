# Milestone B offline research tools

Invoked [brief](../../docs/implementation-briefs/README.md#archive-lookup) (`implementation-briefs.zip :: docs/implementation-briefs/CODEX_BRIEF_SOR_inorganic_resource_availability_milestone_B.md`),
[result and contracts](../../docs/experiments/resource-availability-milestone-b/report.md).
Pure installed CPython stdlib plus existing project modules; no external code or
dependency added. All outputs stay ignored/local unless specifically authored
synthetic examples or reviewed summaries. GPL-3.0-or-later.

| Tool | Reads | Writes and effects |
|---|---|---|
| `preserve.py` | Inherited 6,847 pins, sealed 070 inventory, Git HEAD/index, supplied untracked brief | Exclusive local before/after JSON; initial untracked-text baseline copy; Win32 caller-free-space guard. No evidence/target/DB/index mutation. |
| `coverage.py` | Sealed original raw/WAL, retirement and operator markers; owned 070 decoder and resource evaluator | Exclusive local JSON and disk-backed SQLite uniqueness counts. Active-invocation memory only; no raw duplication or game access. |
| `checks.py` | Focused owned unittest sources and existing owned exporter | Exclusive test receipt; first invocation writes adapted exporter source in this folder. CPython test subprocesses only; all test groups must actually run. |
| `export-review-package.py` | HEAD/index, authored tracked/untracked text, supplied-brief baseline | Ignored complete/task patches, manifest, status and disposable .local-work/review-patches apply trees. Forward/reverse exact-byte checks, whitespace/links; no staging or workspace apply. |

The exporter is adapted from owned
`research/resource-availability/export-review-package.py` under standing
SOR-P-0002; `tests-02.json` pins the original source hash. It retains its original
ownership lineage. The initial baseline snapshot was filtered to the sole
pre-existing untracked file (the supplied brief); the newly authored preservation
script is correctly included as task work. No earlier uncommitted work existed.

The executable evaluator stays in
`save-analysis/scripts/resource_availability.py`, importing `resource_spatial.py`.
It is extended in place; session-tools and 070 capture/decoder remain unchanged.
See validation for actual reproduction commands, limitations and retained failures.
