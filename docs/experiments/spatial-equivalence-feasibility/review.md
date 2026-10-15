# Verification and independent review package

[Original brief](../../implementation-briefs/CODEX_BRIEF_SOR_experiment_A_spatial_native_equivalence_feasibility.md),
[report](report.md), [native inventory](boundary.md), [coverage](coverage.md),
[scientific value/risk](value-risk.md). Recommendation: **REVISE**.

## Mandatory completion matrix

| Original criterion | Task result | Evidence / limit |
|---|---|---|
| Feasibility report with one recommendation | PASS | report.md answers the scoped question; REVISE does not imply native agreement or implementation authority. |
| Native boundaries and field-level contract | PASS | boundary.md cross-checks pinned inline positive/negative edges and repeated query reductions. D/A locations remain separate from safe live acquisition. |
| Branch comparisons and independent oracle | PASS | coverage.md includes false candidates, short-circuit omissions, unique configurations, numeric limits and counterexamples. Every current native spatial comparison remains NOT TESTED. |
| Scientific value and safety/cost decision | PASS | value-risk.md states the consequential assertion, finite prior offline qualification, abstention and operator/transport/retirement limits. |
| Independent review and rework | PASS | Independent ACCEPT; actual return retained locally, objections and limits below. Final snapshot confirmation covers the reporting delta. |
| Patches, actual checks, preservation, proposed commit | PASS | Exact patch reconstruction, inventories, source pins, instruction facts, whitespace and links pass; no staging/commit/push. |
| Scope, prose and protected-input discipline | PASS within stated audit scope | Documentation only; no observer, DLL, package, target action, save/configuration/database change or Experiment B investigation. Selected input pins are rehashed; no full save/archive/Ghidra audit is claimed. |

## Checks and artifact locations

Ignored local root: `.local-work/spatial-equivalence-feasibility/`.
`preservation-before.json` pins 131 selected files: primary exports, observer and
evaluator sources, supplied brief, installed executable and Git index, plus HEAD.
`preservation-after.json` records their recheck. This is a selected-source audit,
not the earlier 6,868-pin protected-corpus procedure. Saves, Ghidra databases and
raw captures were not opened for content, executed or modified by task commands;
their full byte equality was not freshly audited. No game process operation was
performed, so target survival/restoration is not applicable.

`verify-package.py` is an original task-local stdlib verification helper, outside
tracked deliverables. It reads Git HEAD/worktree/index and selected receipt pins,
checks source hashes/instruction facts, changed Markdown links/whitespace and
creates textual patches and JSON/status receipts under this local root and
`.local-work/diffs/`. It applies patches only to disposable temporary text trees
for byte comparison, with no Git staging/ref mutation, target effects, downloads
or native execution. Dependencies: installed CPython 3.14.3, Git, existing files.
Its hash is recorded in `package.json`; it introduces no runtime dependency.

The local package includes `package.json`, `changed-files.json`,
`complete-files.json`, `exclusions.json`, `git-status-short.txt`,
`verification.json` and `preservation-after.json`. Two patches are retained:

- `.local-work/diffs/spatial-equivalence-feasibility-task-only.diff`: task-authored documents and bounded index/provenance updates.
- `.local-work/diffs/spatial-equivalence-feasibility-complete.diff`: every uncommitted textual change since HEAD, including the supplied initially untracked brief, whose bytes remain unchanged.

Ignored/raw/binary evidence, prior archives, databases, observer builds and local
receipts/scripts are excluded from textual patches and declared in the exclusions
manifest. Full contents remain local. Publication eligibility is unchanged.

Executed with CPython 3.14.3 and Git 2.53.0.windows.1:

```powershell
& 'C:/Users/User/AppData/Local/Python/pythoncore-3.14-64/python.exe' -B .local-work/spatial-equivalence-feasibility/verify-package.py
```

Actual results: 131/131 selected pins unchanged; five unique inherited source
pins agree with both existing manifests; 11 exact instruction assertions PASS;
41 changed-text link targets exist; `git diff --check` and new-file whitespace
PASS. Both patch inventories match the 10 task-authored / 11 complete text files,
and each applies forward and backward with exact byte reconstruction. The
script's broad prose-pattern candidates were manually inspected: all occur
within valid inline code/hexadecimal text, with no fused-word defect found.
The independent reviewer also explicitly checked prose and spacing.

Checks are documentary/integrity checks, not new evaluator/runtime tests. Existing
12 synthetic spatial tests are historical qualification, not newly executed or
native validation. Verification results and exact reviewed hashes must be read
from the actual local receipt; no PASS follows merely from this description.

## Reviewer record

One fresh-context reviewer reads the original brief, standing guidance, primary
exports, observer source, working tree, receipts and patches. Initial objections
were retained: callback return is not the native verdict; accepted regions skip
later regions; repeated query reductions defeat a single unqualified snapshot;
CALL qualification does not cover inline live state or complete geometry.
The investigator incorporated these distinctions before formal submission.
The reviewer also caught a drafting pin typo; it was corrected before packaging.

Independent disposition: **ACCEPT** of the feasibility package, with scientific
recommendation **REVISE**. Actual initial return is retained in
`.local-work/spatial-equivalence-feasibility/reviewer-verbatim-accept01.txt`.
The first submitted package SHA256 was
`22743c84f4c6aac09d7c32ad92191506d1202adcd3b76351097c3e0a95a14893`;
that snapshot and patches remain under local `review01/`. The final package
records this acceptance, actual check results and the distinction between group
completion validity and native-memory coherence. Its independent reporting-delta
confirmation is retained in local `final-review-confirmation.txt`.

The reviewer independently read primary native instructions and 0.8.0 source,
checked all task/complete file and patch hashes, HEAD/index, status/whitespace,
and rehashed all 131 selected pins. It inspected the helper and its exact patch
reconstruction receipts; it did not independently execute the temporary-tree
apply/reverse reconstruction. Remaining unknowns include internal probe safety,
geometry coherence, repeated query stability, SIMD/flags preservation, capacity,
retirement and natural branch coverage. No reviewer acceptance authorizes
integration, further implementation or live work. No permission issue was found
within this documentation task; native exports/raw evidence remain LOCAL-ONLY.

Suggested Conventional Commit subject:
`docs(research): assess native spatial equivalence capture feasibility`
