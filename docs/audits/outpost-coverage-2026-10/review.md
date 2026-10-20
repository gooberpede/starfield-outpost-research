# Coverage audit contract and review

2026-10-20, Australia/Sydney. Authored audit: REVIEW-REQUIRED. Existing research
classifications and decisions remain unchanged.

The [invoked brief](../../implementation-briefs/CODEX_BRIEF_SOR_research_coverage_gap_audit.md)
is the original contract. AC1–AC8 are frozen before audit authoring; the table
below abbreviates them for navigation, without replacing or amending them.

| Original criterion | Required evidence | Assessment |
|---|---|---|
| AC1 Project-wide coverage | report.md inclusion/omission method; source-inventory.csv; coverage.md A01–A60; required core report/review set | PASS, independent review02 after preserved review01 failure |
| AC2 Answer-first matrix | coverage.md: 60 source-linked questions with distinct confidence/basis/coverage/status, gap, use and test | PASS, independent review02 after preserved review01 failure |
| AC3 Disposition/reconciliation | source-and-gap-reconciliation.md dated comparisons; all five dispositions in matrix | PASS, independent review01/review02 |
| AC4 Build Mode | build-mode-and-locations.md first table, production/refresh and separate construction/reconfiguration/adjacency discriminator | PASS, independent review01/review02 |
| AC5 Locations | build-mode-and-locations.md selected-Outpost table, individual provider levels and SD3 exclusions | PASS, independent review01/review02 |
| AC6 Position/biomes/resources | position-biomes-dependencies.md eight-level table, interior/boundary cases and missing common-frame link | PASS, independent review01/review02 |
| AC7 Scope/publication | report.md and reconciliation scientific/publication separation; unchanged baseline and only new audit writes | PASS, independent review01/review02 |
| AC8 Quality/independent review | Preserved review01 REWORK; corrected review02 exact snapshot and independent original-criterion reassessment | PASS, independent review02; final receipt delta separately checked |

Only new audit files may change. Reads cover existing repository text and selected
existing local receipts and supplied screenshots. No native export, game/process
operation, new save, game-analysis tool execution, external consultation or disclosure
is needed. Verification uses installed Python standard library and Git read/apply
checks in disposable local trees. It never applies patches to this working tree.

Before authoring, the local baseline records HEAD/index, all existing tracked and
untracked repository files and the six supplied image hashes. Both-drive free
space must exceed 40,000,000,000 bytes before package writes. The baseline is
`.local-work/coverage-audit/baseline.json` (machine-local receipt). Original game,
save and analysis databases are outside the write set and are not opened by tools
in this audit; no claim of independently rehashing the whole installed game is made.

Independent review is mandatory under the original criteria and
[reviewer procedure](../../reviewers/research-completion-reviewer.md). ACCEPT
would apply only to this bounded documentation audit, not historical scientific
promotion, integration, publication or authority to execute recommendations.

## Executed checks and limits

The historical first check `package-check01.json` records 1,466 unchanged baseline files (tracked
repository files, supplied brief and six supplied JPGs), unchanged HEAD/index,
215 new-document link occurrences and 138 selected source paths. Matrix checks
verify 59 unique sequential keys, eleven nonempty columns, one allowed disposition
and priority per row: 28 ALREADY RESOLVED, three NEEDS CONSOLIDATION, eleven
TARGETED RESEARCH CANDIDATE, fifteen DEFERRED and two PUBLICATION BLOCKER.
These counts characterize audit proposals, not scientific completion percentages.

The independently submitted first snapshot was `package-review01.json`, with the
same historical counts and seven authored files; its exact complete/task-only
patches are `coverage-audit-review01-{complete,task-only}.diff`. The reviewer
returned REWORK: AC1/AC2 lacked CR1 recruitment/capacity coverage, AC3–AC7 passed,
AC8 withheld acceptance pending correction. Its actual return is retained
verbatim as machine-local `.local-work/coverage-audit/independent-review01.md`.
The rework adds A60, the recruitment/capacity source links and explicit ordinary
exceptions; it narrows the tooling wording and distinguishes check01 from the
submitted review01. No original criterion or historical conclusion changes.
Revised package counts and snapshot are in `package-review02.json`; its
independent ACCEPT is recorded below. The historical 59-row/138-source/215-link
figures above remain accurate for check01/review01, not claims about review02.

UTF-8/no BOM/LF, trailing whitespace, selected mojibake sentinels, portable local
links and `git diff --check` pass. Manual prose review checks the named screen,
chronology and dependency questions; no algorithm certifies absence of every
possible joined/split word. No malformed words were found in that review.
The source inventory hashes cited/guidance files; it is not a semantic coverage
score or a claim that every source line was revalidated.

Both patches independently reconstruct exact current bytes forward in isolated
trees and reconstruct the baseline in reverse. Their path inventories match
eight complete files versus seven task-authored files. Actual working-tree
reverse applicability was checked without applying. The complete patch includes
the unchanged supplied untracked brief; task-only excludes it. Ignored raw images,
local receipts/helpers and disposable scratch are disclosed exclusions. No binary
payload or raw source-game material is in either patch.

The exporter is a project-authored local Python-stdlib/Git helper at machine-local
`.local-work/coverage-audit/package.py`; its header documents reads, writes,
prerequisites and effects. Local `author_matrix.py` only writes the new matrix.
Its packaging method follows the existing maintainer-owned SD3 helper,
machine-local `.local-work/sd3-stored/package.py`, SHA-256
`9f9f053f0383f2dd8e1ba96378fcbf78522546537d96a0d3f23a0c1af95945c2`:
Git-style new-file export, discovery ceiling and exact reconstruction are method
reuse, with an audit-specific stdlib implementation; no outside code is imported.
The package contains source/changed-file hashes, exclusions, link inventory,
image provenance, free-space receipts, HEAD/index and actual patch checks.
Disposable apply trees are under `.local-work/review-patches/`, Git discovery
ceiling `.local-work/`; patches are under `.local-work/diffs/`.

Preserved minor tool failures: the WindowsApps `python` alias could not execute;
successful work used the installed Python3.14 absolute executable. Two rg queries
used unsupported Windows wildcard path arguments; explicit directory searches
replaced them. Initial link check identified four guessed review paths; they were
corrected to actual validation/evidence indices before check01. No failed search
was used as scientific absence evidence. Original images/evidence were untouched.

NOT TESTED: gameplay, native/ActionScript execution, loaded producer/actor states,
save restoration, full installed overrides, all historical source-link validity,
retail observer safety and complete release rights/history/privacy readiness.
Target process survival is NOT APPLICABLE; no target process was opened.
Scientific outcome is a bounded audit synthesis; documentation acceptance was
obtained for review02. Integration and publication remain unauthorized.

## Independent handoff

Review uses a fresh-context read-only agent under the original brief and reviewer
procedure. The local package revision and actual verbatim decision are retained
separately to avoid a self-referential reviewed-document hash. Any changed audit
file after acceptance requires a fresh manifest and independent delta review.
This section does not itself claim ACCEPT or authorize integration.

## Independent acceptance and delivery

Review02 returned **ACCEPT**, every original AC1–AC8 PASS, for
`package-review02.json`, SHA-256
`1c30d5758c16186e01aa58c0b54d7969ed9622253eeae3d8edaace9aeaa31621`.
The verbatim return is machine-local
`.local-work/coverage-audit/independent-review02.md`. It independently verifies
1,466 preserved baseline hashes, all submitted files and 141 source hashes,
219 links, 60 matrix rows, actual complete/task-only inventories, exact
in-memory forward/reverse reconstruction, actual-tree reverse applicability,
`git diff --check` and unchanged HEAD/index. Prior source/screenshot controls
remain applicable to unchanged content; the CR1 addition was source-checked.
The historical REWORK and corrected snapshot are both preserved.

Only this review/disposition receipt changes after accepted review02; the six
other authored audit files retain the accepted bytes. Final package paths are
machine-local `.local-work/coverage-audit/package-final01.json` and
`status-final01.txt`, with `.local-work/diffs/coverage-audit-final01-complete.diff`
and `coverage-audit-final01-task-only.diff`. The final independent delta return
is retained separately at `.local-work/coverage-audit/independent-review03.md`;
it controls acceptance of those final bytes without a self-referential hash here.

Separate outcomes: **science** = existing-research coverage synthesis, no
promotion/new native experiment; **documentation** = original-criteria ACCEPT
for review02 with final receipt delta independently assessed; **safety** =
baseline/HEAD/index preserved, no target process used; **integration** = awaiting
maintainer critical review, unauthorized; **publication** = NOT READY under the
existing gate, no reclassification; **permissions** = no new reuse/disclosure
basis or live authority requested or required. No staging, commit or push.
