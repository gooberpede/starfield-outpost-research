# SOR-EV-0011 — Structural containment validation and review package

2026-10-08, Australia/Sydney. [Full report](../outpost-save-structural-containment.md). Selected numeric summaries and authored scripts/docs REVIEW-REQUIRED; local raw/bulk evidence LOCAL-ONLY. No publication or integration approval.

## Checks and limits

- All 22 requested labels / 21 unique original/archive saves freshly match prior SHA-256 and sizes before/after analysis. L0 reuses immutable S4C; no new raw/decoded copy. Original modification timestamps were compared before/after this pass. Access times were not controlled. Existing decoded derivatives also rehashed against prior analytical hashes.
- 484 label-stream transform checks / 462 unique-save streams pass the existing checksum/EOF/input-consumption/expected-size/full-file/alignment checks. No second decoder was introduced. The independent audit separately closes the BCPS compressed-size table against physical file EOF.
- Independent direct-byte checks confirm all 22 directory word sequences, exact 48777-entry uint32 table closure, counted string bounds and all 20 beacon/name/animation index matches. That uint32 table is byte-identical across all labels, including L0→L0C. Relationship endpoint pair states and envelope bounds verified independently of the analyzer's matching functions. Original/copy/decoded hashes and source/tool/brief provenance are in local receipts.
- Five existing decoder/diff synthetic tests and five new malformed-directory/string-index/tail tests pass. These are tool checks, not game semantics. A first synthetic invalid-index stimulus accidentally left a matching shifted triple; the test stimulus was corrected, the initial fixture retained locally. This reinforces that matching alone does not prove schema semantics.
- No tracked .sfs/.raw/.bin/.dmp/.mdmp; all archive/output roots ignored; staged diff empty. No staging, commit, push, process interaction, deployment, original-save modification, database/configuration mutation, new dependency or outside disclosure.
- `git diff --check` and separate UTF-8/no-BOM/LF/trailing-whitespace checks cover all task-authored changed/new files. The supplied pre-existing brief is hash-preserved with its original line endings. Markdown file targets and heading fragments are checked against pre-task HEAD to distinguish pre-existing missing targets from introduced links; all **199 links passed**, with no introduced or pre-existing broken links in these changed/new documents; details are in local `validation-results.json`. External URLs were not fetched.
- Final independent audit/results, current status and tracked-plus-untracked diff are persisted locally. Successful integrity checks do not prove object framing, workshop ownership, token semantics, minimal complete footprint, load authority or safe mod integration.

## New review files

- [Structural report](../outpost-save-structural-containment.md).
- [Directory/pointer/count ledger](directory.csv), [all present anchor containment](anchors.csv), [22-label region growth](growth.csv).
- [Physical stream inventory](chunks.csv), [deliberate/reload chunk differences](chunk-density.csv), [region action/control density](region-density.csv), [density ranges](density-summary.csv).
- [Compact-token tests and counterexamples](token-mapping.csv), [candidate window/payload comparisons](candidate-changes.csv), this validation record.
- [Original narrow analyzer](../../../save-analysis/scripts/analyze_structural_containment.py), [synthetic bounds tests](../../../save-analysis/scripts/test_structural_containment.py).

Modified tracked files: README.md, CREDITS.md; docs/PROVENANCE.md, RESEARCH_STATE.md, SOURCES.md, known-facts.md, state-register.md, subsystems/initial-map.md, implementation-briefs/README.md, experiments/manual-save-corpus-S0-S7C.md; save-analysis/scripts/README.md. The old corpus report gains only a separate correction notice; historical wording/evidence are preserved.

Pre-existing untracked supplied input: docs/implementation-briefs/CODEX_RESEARCH_BRIEF_outpost_save_structural_containment.md, unchanged. No unrelated initial modifications existed. No new third-party permission blocker; existing installed separate-tool credit and original project code only. Selected metrics still require scientific/privacy/rights review before staging or publication.

## Local-only tooling and outputs

Ignored `.local-work/structural-containment/` contains:

- `explore.py`, `header_probe.py`, `directory_probe.py`, `frame_probe.py`, `family_probe.py`, `family_probe2.py`, `offset_probe.py`, `validate_directory.py`, `header_lengths.py`, `name_pointer.py`, `stringpool_probe.py`, `name_index_probe.py`, `rename_length_check.py`, `inspect_result.py`: bounded exploratory reads of existing decoded copies and numeric/hex console probes. No source input writes; failed framing hypotheses retained. Final analysis/audit independently verify input hashes and selected observations.
- `extend_pool.py`, `update_records.py`, `finalize_refs.py`, `normalize_test.py`, `normalize_validation.py`, `final_check_extension.py`: task-authoring helpers, writing only authorized new script/documentation text. No save/process/database effects. They are not rerun/reusable automation; some deliberately append and must not be repeated.
- `build_review_tables.py`: reads completed local numeric results and creates the nine selected CSVs, omitting personal filenames/unrelated strings/raw blobs. Its analysis-05 numerical inputs match final analysis-06 outputs; common selected CSVs are byte-compared in the independent audit. Directory/growth/density summaries reflect identical final numerical observations.
- `validate_review.py`: originals/copies/derivatives for preservation and direct-byte audit; Markdown/Git read-only checks; local JSON/inventory/status/diff writes. No index/history/network mutation.
- Retained initial synthetic fixture `test-fixture-initial.py`; partial analysis-01–03 roots; completed pre-string-pool analysis-04; analysis-05; final analysis-06 with `analysis.json`, `anchors.csv`, `candidate-changes.csv`, `chunks.csv`, `density.csv`, `growth.csv`, `token-mapping.csv`; run-05/run-06 logs. No decoded/raw output is written by the new analyzer.
- Final `independent-check.json`, `verification-final.json`, `validation-results.json`, `artifact-inventory.json`, `git-status-short.txt` and `review.diff`. Artifact inventory hashes local helpers/results and every authored changed/new file; self-referential mutable bookkeeping exports excluded.

`review.diff` contains Git's tracked diff and every untracked authored file plus the supplied brief marked as pre-existing input, without staging. Untracked additions use an authored unified diff; raw saves/decompressed blobs and bulk analytical JSON are excluded. It remains a local review artifact. [Workflow](../../../WORKFLOW.md) still requires critical review before integration; this report does not approve the next proposed analysis or live experiment.
