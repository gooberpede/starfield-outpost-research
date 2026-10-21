# B2 frozen criteria and review package

**Current full-snapshot qualification:** [focused rework and revised AC1–AC8](focused-rework.md).
The review03/final01 acceptance below is historical evidence for the pre-rework
candidate, not an assertion that the maintainer's focused correction is accepted.

2026-10-21. [Original authorized brief](../../implementation-briefs/CODEX_BRIEF_SOR_B2_documentation_quality_technical_presentation_evidence_context.md#9-frozen-assignment-completion-contract--eight-mandatory-criteria),
[report](report.md), [corrections](corrections.md), [semantic checklist](pseudocode-review.md).
No criterion amended. Implementer checks below are distinct from the actual
independent ACCEPT/REWORK/ESCALATE. The original brief controls full wording.

| Frozen criterion | Independent result, review03 | Exact evidence and limits |
|---|---|---|
| AC1 — Authority and input safety | PASS | baseline.json hashes all 1,589 starting Git-visible files; index/HEAD/brief unchanged; preservation.json checks protected tracked evidence and pin CSVs. Only documentation and bounded B2 diagnostic source edited. |
| AC2 — Historical defect-led audit | PASS | corrections.md prior-review table; original local L3/SD1/BM1 returns read before audit.py loop; fixtures.json 37 controls; corpus.csv 1,074 tracked text files/138,508 lines; scan.json and candidate-dispositions.csv. Context classifications are bounded, not exhaustive semantic reinterpretation of every CSV cell. |
| AC3 — Prose, UTF-8, Markdown | PASS | corrections.csv ordered 469 operations replay exactly to 60 current files; 103 encoding occurrences repaired; historical cards/quotations explicitly retained. check.py UTF-8/BOM/fences/tables and relative-link candidate checks; new-file whitespace plus Git diff check. |
| AC4 — Precise notation | PASS | notation.md; L2 native/025 at 1421f2b69/1421f2b8c; activated-grid-05:1848 at 14096bc7a; P1's existing mask exclusion proof. preservation.json records five explicit numeric-spelling exceptions; remaining digit sequences unchanged, with separate identifier checks. |
| AC5 — Scientific-quality pseudocode | PASS, document comparison | pseudocode-review.md evaluates all eight B1 candidates and edge cases; mechanisms.md three original decision tables cite accepted source reports/reviews. No engine execution or live semantics revalidation. |
| AC6 — Reader context and dependencies | PASS | evidence-dependencies.md explains sample/outpost/property/result/access; dependency-locations.csv indexes baseline occurrences and B3/B4 handoff. III-c remains unidentified; no save publication assumed. Link validation distinguishes local-only locators from promised documents. |
| AC7 — Durable documentation and coverage | PASS | B2 package, roadmap and index routes; before/after documentation hashes; original evidence/pins/verdicts unchanged; unresolved label and reproduction/rights limits explicit. |
| AC8 — Independent critical review and package | PASS | Actual independent ACCEPT on package-review03.json; all eight original criteria PASS. Exact hashes, both patch directions, corpus/fixtures, residual/alias controls and semantic comparisons independently checked within the limits below. |

## Actual checks and their limits

`check.py` reads tracked authored text plus new B2 documents and writes only
`.local-work/b2/checks.json`. It checks strict UTF-8/BOM, fenced-block closure,
table-width transitions and relative targets/fragments outside fenced code.
Links are a bounded regex check with manual candidate disposition, not a renderer.
Original `.local-work` targets are local-only and do not promise public downloads.
No external URL availability or public fresh-checkout experiment was tested.

`registers.py` reads baseline/ledger/scan and emits authored metadata plus local
preservation receipts. It replays literal edits from the exact baseline, checks
decimal digit streams and verifies all non-edited original files. Navigation
and dated context additions are separately declared. The exporter records the
protected identifier-family comparison, source/primary hash inventory, Git state,
changed/untracked inclusions, local exclusions and exact forward/reverse patches.
These mechanical checks establish neither semantic truth nor rights clearance.

Preserved implementation failures: an initial combined read exceeded output
limits and was reread in focused sections; PowerShell brace/glob assumptions
failed read-only searches; one draft correction overlapped an already separated
rank label and asserted before any prose writes; a diagnostic lacked `__file__`
and failed before source writes; one multi-file patch had a mismatched final
context and failed atomically. A draft context link named nonexistent inputs.md;
the check exposed it and it was corrected to the actual inputs.csv. None changed
primary evidence, save/game state, index or source pins. Failed local helper
versions remain available rather than deleted.

## Protected inputs and separate outcome dimensions

- Baseline protected tracked inputs: raw/selected exact evidence, existing source
  and pin CSVs, code and supplied brief; all untouched except the explicitly
  authorized native-map description CSV and ledgered authored Markdown.
- Edited explanations: documentation-hashes.csv records original and revised
  SHA-256, without replacing any historical manifest/hash claim.
- Referenced local primary locators: original reviewer returns, L2 native/025,
  activated-grid-05 and typed-full03 summary. Their identities are recorded in
  package source-receipts.json; no payload is included in review patches.
- Scientific outcome: no new research; prior confidence/coverage retained.
  Engineering/text integrity: actual checker and reconstruction receipts control.
  Instrumentation/target survival: NOT APPLICABLE; no target was operated.
  Authority: offline documentation scope; no new rights or external action.
  Publication: NOT CLEARED independently of any B2 ACCEPT.

The complete patch includes the unchanged previously untracked B2 brief;
task-only excludes that user input. No earlier unrelated dirty work existed.
Exported patches/manifests live under ignored `.local-work/diffs/` and
`.local-work/b2/`, with explicit coverage labels. Disposable application trees
stay under `.local-work/review-patches/`, with parent Git discovery stopped at
`.local-work/`. Only generated scratch patch application is inverted; no prior
local work or protected input is removed.

## Independent disposition

Review01 returned **REWORK** against `package-review01.json`, SHA-256
`930816b6133599ac2f5fc47c91cfea21749619477774b501adff9256eb20b14f`.
AC1/AC4/AC5/AC6 passed; AC2/AC3/AC7/AC8 failed for residual prose and fixture
accounting. The verbatim response is local `independent-review01.md`.
It independently replayed 464 operations into 57 files, reconstructed both
patch directions, checked all 78 submitted hashes and 1,589 baseline copies,
reproduced corpus/candidates/37 fixtures/structural checks, inspected native
mask windows and compared the three analytical tables against source reports.
On-disk scratch applications and historical execution order were receipt-only.

The same assignment corrects all four required prose cases, an additional
human-readable type label, fixture counts and candidate-status accounting.
Five explicit residual controls are added; no criterion or scientific claim
changes. The strengthened reader dependency index is documentary triage with
source aliases/routes. Review02 returned **REWORK**, AC1–AC5 PASS and AC6–AC8
FAIL, against `package-review02.json`, SHA-256
`ea38db8dd3a741a927173a345b51f99315f2a026edf2d90adf399570c770474a`.
The new index had extracted a fused baseline sample/count as a purported source
alias. Its verbatim result is local `independent-review02.md`. The corrected
generator now applies the ordered literal ledger before extracting identities;
the exact affected row is asserted as S1 and Save52. Baseline line locators are
unchanged. No original sample, report or scientific result changed. Review03
assesses the regenerated snapshot; no future ACCEPT is implied. Maintainer
critical review remains necessary before integration.

## Actual acceptance and final delivery

Review03 returned **ACCEPT, AC1–AC8 all PASS**, against
`package-review03.json`, SHA-256
`bb897982f724ae7b0403243fd3ffa78bb8ea57b9c3c0c8afc3918c5eb91222f2`.
The actual verbatim return is `.local-work/b2/independent-review03.md`.
All 82 submitted hashes, 1,589 baseline copies, source receipts, 469 literal
operations/60 files, both patch directions, 37 initial fixtures, five residual
controls and corrected alias assertion were independently checked. The reviewer
reproduced the 1,087-file structural computation and verified all 105 local-only
link targets exist. Semantic tables retain the earlier substantive comparison;
on-disk scratch application and historical operation ordering are receipt-only.
No scientific/live/public reproduction or rights clearance was retested.

The final administrative delta changes this review record only, recording the
actual ACCEPT and final matrix. Its exact package is
`.local-work/b2/package-final01.json`, with status, inclusion/exclusion,
preservation, identifier, source and structural-check receipts using `final01`.
Verified diffs are `.local-work/diffs/b2-documentation-final01-task-only.diff`
and `.local-work/diffs/b2-documentation-final01-complete.diff`. Complete includes
the unchanged supplied brief; task-only covers 81 authored/edited files.
Exact final-delta confirmation is retained separately as local
`independent-review-final01.md`; that actual return controls these final bytes,
avoiding a self-referential manifest hash. Any later content change needs review.

Suggested conventional commit after maintainer review:
`docs(research): improve documentation quality and evidence context`.
Nothing was staged, committed or pushed. Publication remains **NOT CLEARED**;
III-c identification, B3 method closure and B4 per-asset decisions remain as
qualified in the report. No integration or scope expansion is authorized here.
