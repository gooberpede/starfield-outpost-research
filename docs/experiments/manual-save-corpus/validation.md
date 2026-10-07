# Manual corpus validation — SOR-EV-0009

2026-10-07, Australia/Sydney. [Full report](../manual-save-corpus-S0-S7C.md). Selected authored summary REVIEW-REQUIRED; local raw/derived artifacts LOCAL-ONLY.

- 17/17 originals and fresh archived copies match the initial manifest SHA-256/size; original modification timestamps unchanged. Final details: ignored `.local-work/manual-S0-S7C/verification-final.json`. Access-time behavior was not controlled; this is content/mtime preservation, not every filesystem attribute.
- 17/17 archived files confirmed ignored. No tracked `.sfs`, `.raw` or `.bin` file. Git index remains empty of staged changes. No staging, commit, push, game execution, debugger or external disclosure.
- 374/374 zlib streams pass checksum/EOF/input-consumption/decoded-length checks; 17/17 outer lengths and complete file bounds pass. Five synthetic tests pass. No independent second decoder or inner-schema validation; no reload test.
- Every candidate main signature is unique when present; candidate script verifies each decoded SHA-256 before reading. Role and coordinate meanings remain provisional.
- `git diff --check` and separate trailing-whitespace/UTF-8/LF checks for all authored new/modified text passed. The user-provided pre-existing untracked brief is preserved byte-for-byte, including its original line endings.
- Local Markdown file targets and heading fragments in changed/new documents were checked, distinguishing pre-existing broken targets from introduced ones; details/counts in local `validation-results.json`. No introduced broken links. External URLs were not fetched.

## Review files

`.local-work/manual-S0-S7C/review.diff` includes the ordinary tracked diff **and every untracked task file**, including the supplied brief labelled as a pre-existing input. Nothing was staged to create it. `git-status-short.txt` records final status. `artifact-inventory.json` records paths, sizes and SHA-256 for local analytical outputs and authored changed/new files; it excludes itself and mutable final review-export files to avoid recursive hashes.

New task files: experiment report; `manifest.csv`, `transitions.csv`, `candidates.csv`, this validation record; `archive_manual_corpus.py`, `analyze_manual_corpus.py`, `probe_manual_candidates.py`, `test_manual_corpus.py`. Existing untracked input: invoked brief, unchanged. Modified tracked files: root README, CREDITS, PROVENANCE, RESEARCH_STATE, SOURCES, known-facts, state-register, initial subsystem map, save-analysis README and script guide.

Local-only scripts: `build_review_tables.py` reads manifest/analysis/candidates JSON and writes the three selected CSVs. `validate_review.py` reads sources for final hashes/metadata, copies, authored text and Git state; writes local verification/status/diff/inventory and this summary, with no Git mutation. It normalizes only task-authored text to UTF-8/LF. Local exploratory probe outputs are retained; no source save or existing archive is rewritten.

The selected manifest omits exact personal filenames/absolute paths; the exact manifest retains them locally. Save-derived windows, decompressed blobs, full string lists and bulk analysis JSON are excluded from the review diff. The original brief itself contains personal filenames and still needs a publication privacy decision. Neither successful checks nor this completion summary clears publication or integration.
