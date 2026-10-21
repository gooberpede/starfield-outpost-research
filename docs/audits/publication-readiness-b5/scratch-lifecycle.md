# B5 scratch creators and prospective retirement

2026-10-21, Australia/Sydney. Governed by the [B5-A brief](../../implementation-briefs/CODEX_BRIEF_SOR_B5_A_local_work_inventory_scratch_lifecycle.md)
and [workflow](../../../WORKFLOW.md). Historical evidence, source pins and
scientific conclusions remain unchanged. No existing scratch is deleted.

Ten current tracked exporters now use context-managed application trees under
`.local-work/review-patches/`; their Git environment stops parent discovery at
`.local-work/`. The full source list and before/after SHA-256 identities are in
local `.local-work/b5/creator-changes.json`. Exact predecessors are retained at
`.local-work/b5/creator-before/` (research and runtime subtrees) and in HEAD. Historical source citations
continue to identify those predecessors; current source is a distinct revision.

| Current source | Prospective lifecycle |
|---|---|
| `research/continuous-beacon-preview/export-review-package.py` | Normal and exception cleanup replaces persistent local application tree. |
| `research/resource-availability/export-review-package.py` | Same. |
| `research/resource-availability-milestone-b/export-review-package.py` | Same. |
| `research/native-availability-map/export-review-package.py` | Same. |
| `research/local-readiness/export-review.py` | Same. |
| `research/existing-reference-grid/package.py` | Same; receipts remain outside tree. |
| `research/matching-source/package.py` | Same; receipts remain outside tree. |
| `research/x87-preservation/package.py` | Existing automatic cleanup preserved; allocation relocated and Git ceiling added. |
| `research/internal-observation-qualification/package.py` | Same. |
| `runtime/session-tools/export_review.py` | Persistent local application tree replaced with normal/exception cleanup. |

The [scratch qualification](test_scratch.py) executes only each actual context
block with synthetic text and real Git apply/check; ten normal and ten
injected first-apply exceptions passed. No experiment prologue, save/native
read, compiler, observer or installed target runs. Receipts at
`.local-work/b5/scratch-tests.json` survive outside both temporary trees.
Abrupt termination/power loss remains outside Python context-cleanup guarantees.
These are lifecycle checks, not full historical pipeline requalification.

Earlier test-harness failures are retained in [review](review.md): missing
`core.autocrlf=false` caused a synthetic byte mismatch, then a missing `pathlib`
binding stopped the internal-qualification case. Corrected final cases pass;
neither failure is reported as a historical method defect.

## Retired local entrypoints

The following historical entrypoints are **retired for prospective packaging**:
`.local-work/position-resumption/package_review.py` and
`.local-work/native-oracle/package_review.py`. Do not rerun them: both allocate
bare `sor-position-patch-*` system-Temp trees. Their source bytes and historical
receipts remain immutable, readable evidence. Retirement is a documented operator
restriction with a tested successor; it is not an OS execution block or source
rewrite. No claim assigns individual Temp trees to a specific process.

All task-bound local packaging helpers enumerated in
[creator-inventory.csv](creator-inventory.csv) have the same prospective
retirement: use the [current successor](../../../research/review_package.py)
for a new clean-start task, rather than old task-specific baseline/brief/HEAD
assumptions. This disposition follows inspection of their packaging operations
and fixed task baselines, not permission to discard the scripts. Retain exact
versions, including failed entrypoints and frozen `D:/tools` creators. Paths
inside archival snapshots are historical copies, not independently maintained
tools. The original [B3 reconciliation](../publication-readiness-b3/historical-source-reconciliation.md)
remains controlling for historical identities.

The new successor requires a starting JSON receipt (`head`, `index_sha256`,
`status`) establishing a clean start except an optional supplied brief. It
rejects prior mixed work, binary changes, reparse paths and output collisions;
prior work needs an exact before-tree exporter under the workflow. For this
task, from repository root:

```powershell
& 'C:/Users/User/AppData/Local/Python/pythoncore-3.14-64/python.exe' -B research/review_package.py --label NEW-LABEL --baseline .local-work/b5/start.json --supplied-brief docs/implementation-briefs/CODEX_BRIEF_SOR_B5_A_local_work_inventory_scratch_lifecycle.md
```

Use a fresh label on any retry; prior patches/receipts are retained. The
[successor qualification](test_successor.py) passes full Python control flow
with synthetic Git discovery responses and real Git diff/apply: normal,
first-apply failure, prior-work rejection and output-collision preservation.
It does not initialize/stage/commit a synthetic repository. Its receipt is
`.local-work/b5/successor-tests.json`. Actual B5 export separately exercises real
HEAD/index discovery and full patch coverage. The synthetic successor case uses
one new Markdown file; it does not qualify tracked deletions, mixed-work exports
or link-anchor validation. B5's actual delivery also covers the tracked repairs.

## Discovery and dependency limits

Local `.local-work/b5/creators.json` records line-level effects for 146 leads:
tracked Python outside the intentionally archival B3 source tree, and local
Python helpers at task root or one level below. The 64 local packaging leads
were individually listed with hashes and effects; deeper frozen copies are
preserved as historical state. This is bounded active-entrypoint discovery,
not a claim that every language and nested source file is maintained or retired.
The [reference register](reference-impact.md) identifies current versus historical
consumers and replacement directions.

RR1's [test inventory](../publication-readiness-rr1/temp-test-inventory.csv)
distinguishes thirteen default-Temp test files from nine explicitly local ones.
Ordinary context-managed tests remain legitimate; no leak is inferred from a
`TemporaryDirectory` call. Existing local synthetic fixtures and build outputs
remain retained unless an exact candidate says otherwise. No historical helper,
native test suite or tool installation was run for B5. Current `D:/tools` contains
the BAE, Ghidra, x64dbg and xEdit installation directories; none is a target.

The four mandated roots remain in place. A future cleanup must leave them usable;
local scaffolding is not guaranteed by Git because ignored empty directories are
not tracked. Create a missing approved scratch parent before allocation, never
replace a reparse root, and never remove the four designated roots.
