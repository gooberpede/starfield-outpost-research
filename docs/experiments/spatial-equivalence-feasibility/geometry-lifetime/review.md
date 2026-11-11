# Verification, preservation and independent review

[Original brief](../../../implementation-briefs/README.md#archive-lookup) (`implementation-briefs.zip :: docs/implementation-briefs/CODEX_BRIEF_SOR_experiment_A_geometry_lifetime_operand_capture.md`),
[report](report.md), [ownership](ownership.md), [operands](operands.md),
[schema/admission](capture-contract.md), [source pins](sources.csv).
Scientific/design decision: **NO-GO, evidence-bounded inconclusive**.
Independent review: **ACCEPT** for completed scoped research and the NO-GO decision.
No integration, observer, live or Git mutation authority follows.

## Frozen completion contract and actual matrix

Task type is bounded static research/design, with evidence-triggered optional
synthetic qualification. The original brief's G/O and PASS/REVISE/NO-GO criteria
are unchanged. Negative closure requires inspected concrete ownership and operand
paths, explained missing protection/sufficiency, assessed alternatives, justified
test abstention, full handoff and independent review; a failed search alone cannot
close it. Native-execution qualification is not silently declared passed.

| Original mandatory criterion | Result | Evidence and limit |
|---|---|---|
| Scoped scientific value and hard decision, G/O separately | PASS | report.md; NO-GO design, G UNKNOWN, O mapped but unqualified. Native comparisons remain zero |
| Geometry ownership/mutation/destruction/protection and coherent-copy assessment | PASS as bounded research | ownership.md; three new primary exports trace deep copy and full free chain, reference transfer, mapped lock interval and unresolved owner fence. Coherent retail capture itself NOT TESTED |
| Every frozen branch, repeated resolution, fields/types/numeric domain | PASS as static map | operands.md; separate broadphase/count/strip/containment/vertex/edge/terminal rows and per-use scalar/query conditions. Actual capture NOT TESTED |
| Minimal correlation schema, rejected candidates, independent admission | PASS as conditional design | capture-contract.md; ancestry/nesting/concurrency, unwind, STOP, truncation and NOT_EVALUATED distinctions. No implemented live decoder |
| Static-first, narrow discriminating tests only; preserve applicable regressions | PASS | report.md test disposition; no code pathway touched, no new fixture/replay/state tests warranted or run. Corrected and uncorrected accepted artifacts rehashed, not requalified |
| Independent scientific/engineering review and bounded rework | PASS | Fresh-context reviewer returned ACCEPT for the exact package identified below; original criteria and primary exports independently inspected |
| Durable state/function map and provenance | PASS | README, RESEARCH_STATE, function-register, SOURCES, CREDITS and source pin table; no historical semantic finding overwritten |
| Review package, tests/limits, preservation, prose audit, suggested commit | PASS | Local manifests/patch verifier and independent inspection described below |
| Authority, preserved originals and publication limits | PASS within audited scope | No game/observer/native experiment/save/configuration change, staging/commit/push or external disclosure; Ghidra readOnly/noanalysis exports only |

## Authorized static procedure and provenance

Inputs are the pinned executable, existing Ghidra project/exports, inherited
reports/source manifests, frozen evaluator/tests, and accepted fixture/x87 source
and evidence. Outputs are new documentation, three local native exports plus
Ghidra settings/cache/logs and ignored review receipts/patches. Existing
`ghidra/scripts/Invoke-OutpostRecon.ps1` and `OutpostRecon.java` were read before
execution; wrapper passes `-readOnly -noanalysis`. No symbols/types/comments,
analysis or program bytes were modified. Proprietary exports remain local.
Installed Ghidra 12.1.2_PUBLIC, Temurin 21.0.12+8, CPython 3.14.3 and Git support
the checks; no install/download/auto-update or third-party implementation reuse.

Exact PowerShell command form:

```powershell
& ghidra/scripts/Invoke-OutpostRecon.ps1 -Target Starfield -OutputName geometry-lifetime-01.tsv -Addresses @('full:1407ac260','full:1407ac2f0','refall:1407ac260','refall:1407ac2f0','full:1422cc350','full:1422cc2c0','refall:14079a330','refall:1407aa8a0')
& ghidra/scripts/Invoke-OutpostRecon.ps1 -Target Starfield -OutputName geometry-lifetime-02.tsv -Addresses @('full:1407ac0d0','full:1407a9650','refall:1407a9650','full:1407aabd0','full:1407a98b0','full:1407affb0','full:1407ab730','full:1407abc90','full:14079da80','full:14079dd50','full:1422cc0d0','refall:1407ac0d0')
& ghidra/scripts/Invoke-OutpostRecon.ps1 -Target Starfield -OutputName geometry-lifetime-03.tsv -Addresses @('full:1407a54c0','full:1407a59f0','refall:1407a98b0','refall:1407aabd0','refall:1407ab730','refall:1407abc90','refall:14079d910','full:140788bc0')
```

Stop conditions were failed export/script/cancellation, changed protected input,
or caller-available C:/D: space below 40,000,000,000 bytes. Preflight free space:
C: 93,137,842,176 and D: 117,581,234,176 bytes. No observation of game processes
was performed. Cleanup is normal headless exit with new local derivatives retained;
no original deletion. Some full-selector instruction displays cap at 600; complete
decompilation and exact available instruction windows are distinguished. Xref
inventories describe existing analysis references, not all indirect runtime calls.

## Reproducible package checks and audit limits

Ignored receipt root `.local-work/geometry-lifetime/` contains preservation-before/
after.json, changed-files.json, complete-files.json, package.json, verification.json,
exclusions.json, git-status-short.txt and verifier/provenance. Baseline branch is
`main`; exact HEAD/index and changed text hashes are bound in package.json.
Initially untracked supplied brief is unchanged and belongs to complete patch only.

The local stdlib `verify-package.py` is adapted from the project-owned predecessor
`.local-work/spatial-equivalence-feasibility/verify-package.py`; original input hash
and adaptation are retained in checker-provenance.json. It reads HEAD/worktree,
index and selected pins, checks UTF-8/LF/whitespace/relative links and exact native
instruction assertions, and writes only ignored receipts/patches and temporary
text trees. It invokes Git read/apply commands with optional locks disabled; apply
targets disposable text trees, never this checkout's index or files. No target
effects, network, new dependency or original evidence transformation.

```powershell
& 'C:/Users/User/AppData/Local/Python/pythoncore-3.14-64/python.exe' -B .local-work/geometry-lifetime/verify-package.py
```

Preservation scope is 624 selected files: inherited selected pins, complete accepted
fixture sources and final corrected/uncorrected paired artifacts, existing TSV
exports, the supplied brief, executable, index and Starfield Ghidra project files.
This includes byte rechecks of prior preservation evidence, not a new execution
of those tests. Full save inventories, deployment roots and every archived capture
were not audited; no commands wrote them. New exports/logs are separately hashed.
Target survival/restoration is NOT APPLICABLE. These checks prove integrity and
text-package coverage, not native semantics, empirical G/O or publication clearance.

Two ignored patches include newly created text without staging:

- `.local-work/diffs/geometry-lifetime-task-only.diff`
- `.local-work/diffs/geometry-lifetime-complete.diff`

The complete patch includes all tracked/untracked nonignored changed text,
including the supplied brief; the task-only patch excludes that preexisting brief.
Exclusions disclose ignored exports, logs/settings/cache, receipts, databases and
raw/binary material. Exact inventories and forward/reverse byte reconstruction
in disposable trees check applicability/completeness. `git diff --check`, new-file
whitespace, links and UTF-8/LF are checked. Prose audit reads every authored/added
paragraph/table, names, version strings, addresses and source references for fused
words/missing spaces; automated pattern candidates require manual inspection.

Actual implementer check results: **624/624 protected pins unchanged**, 48 source
manifest comparisons across 31 unique source paths, 22 exact native instruction
assertions, 36 relative links, UTF-8/LF and whitespace PASS. Both textual patches
reconstruct exact forward/reverse bytes: 11 task files and 12 complete files.
All 25 automated prose candidates are valid Markdown/code/path/hex contexts.
The reviewer independently confirmed 624 pins, current text/patch identities and
HEAD/index stability, then identified a local exclusions-manifest wording defect:
it called all exports unchanged and omitted derivative settings/cache/logs.
The checker now distinguishes old protected exports, three new native exports/logs
and generated tool derivatives. Early reviewer spacing findings and recursive
ancestry ambiguity were also corrected before the final formal review.

## Independent decision and reviewed revision

The actual formal return is retained verbatim in local
`reviewer-formal-accept.txt`. **ACCEPT** applies to package SHA256
`4105da4aff8063b1531a0e95ab0b9b31a0c0c7aae5ba8ccf58eeeb7e7c9112d8`,
whose text, manifests and both patches are preserved under `review01/`.
The reviewer independently rehashed all 624 protected inputs, HEAD/index and
current text/patch identities; checked all 13 task source pins, 36 links,
UTF-8/LF, whitespace and actual primary instructions. It reconstructed the prior
patch snapshot and inspected the subsequent reporting delta/refreshed hashes.
It did not execute Ghidra, fixtures, the game or the writing verifier;
implementer forward/reverse application and automated assertions remain
receipt-backed, while primary semantics were checked independently.

No blocking defect remains. Acceptance closes this bounded research assignment,
not the native capture/lifetime question. This final review-status update changes
only this review record; the scientific decision, source maps and criteria are
unchanged. Its refreshed package requires reviewer delta confirmation, retained
locally with the formal return. Maintainer integration review remains separate.

Suggested Conventional Commit subject:
`docs(research): assess native region lifetime and operand capture`

Await maintainer critical review. Publication eligibility remains independent of
confidence and reviewer acceptance. No further live development is approved.
