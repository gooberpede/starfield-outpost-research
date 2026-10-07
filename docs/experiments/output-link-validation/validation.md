# SOR-EV-0010 — Validation and review package

2026-10-07, Australia/Sydney. [Experiment and limitations](../output-link-validation-L0-L2C.md). Authored summaries REVIEW-REQUIRED; local raw/derived artifacts LOCAL-ONLY.

## Checks

- Six new copies plus historical L0: 7/7 source/copy/source SHA-256 and size checks passed before analysis. Final original/copy hash, size and original modification-time checks passed; no original writes, moves, renames or deletions. Access times were not controlled.
- L0's filename, sample ID, compressed hash and freshly decoded hash match prior S4C evidence; no duplicate raw copy. Historical S3C/S4/S4C decoded hashes reverified for structural comparison.
- Seven bounded transforms / 154 zlib chunks passed checksum/EOF, length, input consumption, alignment and complete-file bounds. Five existing synthetic decoder/diff tests passed. These are tool checks, not proof of game semantics or an independent decoder.
- Independent direct-byte audit of ledger offsets confirmed all ten listed historical/current envelopes, their length/end-marker boundaries, exact pair presence/absence and canonical correspondence after explicitly substituting candidate role tokens and sorting the two proposed entries. Source method and normalization remain hypotheses; the audit does not independently establish object identity or record ownership.
- All seven archives and local output directory are ignored; no tracked `.sfs`, `.raw` or `.bin`. Staged diff remains empty. No staging, commit, push, external upload/contact, game launch, debugger, SFSE deployment or configuration/database mutation.
- `git diff --check` passed. All task-authored changed/new text passes UTF-8 without BOM, LF and trailing-whitespace checks. The pre-existing supplied brief is preserved byte-for-byte, including its original line endings.
- Local Markdown file targets and heading fragments checked across changed/new Markdown. No introduced broken links; existing broken targets are enumerated separately in local `validation-results.json`. External URLs were not fetched.

## Negative checks and limits

The Windows `python` app alias could not execute; the previously recorded installed executable was used, version/hash independently rechecked. An attempted read of nonexistent `docs/subsystems/production-storage-distribution.md` supplied no evidence; the actual existing `initial-map.md` was read instead. Initial strict analysis stopped on missing old L0C beacon signature after all copies were verified; partial L0/L0C derivatives and preregistration are retained. This failure led to the separately labelled exploratory structural matching, not a rewritten preregistered success. Final scripts/outputs have their own hashes. No live-run validation, full schema decoder, runtime identity map, independent second decoder or authoritative reload test was performed.

## Complete changed/new inventory

New task files:

- [Main report](../output-link-validation-L0-L2C.md).
- [Selected manifest](manifest.csv), [transition metrics](transitions.csv), [candidate ledger](candidates.csv), [endpoint-window comparison](endpoint-windows.csv), this validation record.
- [Archive/analysis wrapper](../../../save-analysis/scripts/validate_output_link.py), [structural follow-up probe](../../../save-analysis/scripts/probe_output_link_structure.py).

Modified tracked files: root README and CREDITS; docs/RESEARCH_STATE.md, known-facts.md, state-register.md, PROVENANCE.md, SOURCES.md and subsystems/initial-map.md; save-analysis/scripts/README.md. Historical evidence/manifests and existing decoder/diff/candidate scripts are unchanged.

Pre-existing untracked input, unchanged: `docs/implementation-briefs/CODEX_RESEARCH_BRIEF_output_link_validation_L0-L2C.md`. Its filenames encode personal information; publication privacy review is still required. No licence/permission blocker arose from new implementation: project-authored additions plus previously authorized installed separate tools only.

Local-only scripts under `.local-work/output-link-L0-L2C/`:

- `build_review_tables.py`: reads local manifests/analysis/probes and hash-verifies decoded inputs for window comparison; writes four selected CSVs. No raw/personal windows exported.
- `validate_review.py`: reads originals for preservation, local copies/decoded inputs, Markdown and Git state; writes verification/validation JSON, artifact inventory, status and complete review diff. No index/history/network mutation.

Local outputs: `preregistration.json`, `manifest.json`, initial partial `L0.decoded.bin` / `L0C.decoded.bin`, seven `analysis-01/*.decoded.bin`, `analysis-01/analysis.json`, `structure.json`, `verification-final.json`, `independent-structure-check.json`, `validation-results.json`, `artifact-inventory.json`, `git-status-short.txt`, `review.diff`. The inventory records hashes/sizes of analytical, authored and helper-script artifacts; self-referential final bookkeeping files are excluded. Interactive exploratory probes were read-only and printed bounded windows; reproducible final structural/window results are persisted in the scripts and JSON/CSVs.

`review.diff` includes the ordinary tracked diff **and all untracked files**, with the supplied brief identified as pre-existing input. `git-status-short.txt` records exact status. The patch remains local and may contain the supplied brief's personal filenames; it is not publication-cleared. No raw save, decoded stream or bulk JSON is included. Critical review, integration and publication decisions remain outstanding.
