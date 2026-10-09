# SOR-EV-0014 — Validation and review package

2026-10-09, Australia/Sydney. [SOR-EXP-0008 report](../launch-era-third-party-save-corpus.md). Critical review pending. Selected numeric tables, authored scripts/prose REVIEW-REQUIRED; all original source material and complete receipts LOCAL-ONLY. No staging, commit, push or publication.

## Actual checks and limits

- Archive SHA-256/size/mtime/ctime before and after agree. All 111 extracted member sizes and archive CRC32 values pass; each has an unchanged final SHA-256 identity. Exact member set matches the 111 saves/one-directory technical listing; no reparse points or unexpected files detected. No archive-provided member SHA-256 exists; extracted hashes establish new local identities, with CRC/size tying them to the archive.
- 900,829,296 extracted bytes within the 4GiB intake bound; all physical saves <=128MiB and decoded saves <=64MiB. C:/D: free-space guard remained above 40,000,000,000 bytes. Final scan-03 completed in approximately 31.5 seconds, under the 1800-second cooperative bound. No decompressed blobs written.
- All 10,007 streams in each complete scan pass bounded decoded length, zlib checksum/EOF and input-consumption checks; physical alignment/table/EOF closure passes. Unique bounded directory/pool and exactly consumed successor-framed grammar in every save. Scan-02 and scan-03 agree in source identities and structural metrics. These checks establish syntactic coverage only.
- Separate direct grammar walker consumes every launch payload without calling original grammar/Cursor. Five shortlist saves additionally receive an independent physical size-table/alignment/decode-hash walk, directory-table closure and string-length/count check. Five PASS receipts, with source SHA-256, decoded hashes and logical offsets; independently authored checks are not independent third-party review.
- Existing S0/S1/S7C archived controls reproduce prior original/decoded hashes. S0 remains negative; S1 and S7C retain named beacon evidence despite zero collection beacons. Controlled deletion history for S7C comes from prior records, not a new runtime observation. Existing historical/mature semantic confidence unchanged.
- Twenty synthetic tests pass: ten historical-inventory, six mature-grammar and four launch-intake/audit tests. Include malformed physical bounds/checksum, grammar truncations/count tags/duplicates, unsafe root/traversal/drive/device/alternate-stream paths, links/attributes/size bounds/case collisions, empty-collection positives and detection gates. These do not prove all possible hostile archives or unknown save layouts are supported.
- `git diff --check`, task/untracked diff whitespace checks, changed-file relative Markdown file targets, ignore coverage, no tracked raw saves/archives/blobs and frozen HIST inventory preservation pass in final `validation-receipt.json`. The repository-wide tracked Markdown scan also found no missing relative file targets; anchors were not independently validated. Historical prose mentions the absent `docs/GIT_SETUP.md`, without introducing a link to it here. No Git index mutation.

No positive launch-era outpost ground truth, validated plugin-load-order decoder, exact active-state bit, complete residual-state exclusion, stable character identity, planetary coordinates or load/migration authority is established. Signature absence is model-limited. Rights currentness/ambiguity remains unresolved for publication: web references are cached, no live-current permission snapshot or separate author consent is claimed. Raw redistribution is excluded under the brief.

## Reproducibility and local receipts

Root: `D:/Projects/starfield-outpost-research/.local-work/third-party/the-daily-xperience-1798/` (ignored). Original archive absolute path only in local provenance and the operator-supplied brief. Extracted members remain unchanged under `extracted/Game Complete All Saves/`. Do not load or edit them.

- Initial root `provenance.json`, `archive-listing.txt`, `archive-members.json`: failed receipt-accounting pass; extraction preserved, not discarded. No extraction stdout receipt survived that accounting error; subsequent full member size/CRC/hash validation supplies integrity evidence.
- `scan-02/` and final `scan-03/`: fresh provenance with runtime/tool/imported-script hashes and brief identity; technical archive listing/member metadata; reuse disposition; flushed/fsynced per-file `progress.jsonl`; complete local `inventory.json`; completion and free-space receipts. Character/member fields remain local.
- `scan-03/independent-spot-checks.json`: five independent physical/directory/string/grammar audits.
- `scan-03/controlled-calibration.json`: existing S0/S1/S7C calibration and hash preservation.
- Root `permission-reference.json`: author/source references, exact permission-panel section locators, paraphrased terms, cached retrieval limitations and publication boundary. Not a verbatim live-current permission snapshot.
- Root `update_records.py`: local authoring helper, reads named documentation and appends scoped records; adds research-state cross-reference. No target effects; not designed for rerun over existing updates.
- Root `final_review.py`: local validator/review exporter; reads scripts/docs, frozen receipts and Git state, runs synthetic tests, rehashes archive/member originals, writes ignored test/validation receipts and diffs only. No source or Git index writes.
- Root `task-only.diff`, `comprehensive.diff`, `validation-receipt.json`, `tests.txt`: complete review artifacts. Comprehensive includes the pre-existing user-supplied untracked brief; task-only excludes it. Both include all new task files, not just `git diff` output.

Reproduce intake only under matching authorization: installed Python `-B save-analysis/scripts/inventory_launch_corpus.py --run <fresh-name> --reuse-extracted` revalidates existing extracted contents, never overwrites them. Initial extraction omits `--reuse-extracted` and refuses an existing extracted root. The summarizer is fixed to frozen scan-03 and refuses existing docs output directory; do not rerun over retained tables. No automatic live or wider research follows.

## Complete changed-file inventory

New task files:

- `docs/experiments/launch-era-third-party-save-corpus.md`
- `docs/experiments/launch-era-third-party-corpus/manifest.csv`
- `docs/experiments/launch-era-third-party-corpus/shortlist.csv`
- `docs/experiments/launch-era-third-party-corpus/validation.md`
- `save-analysis/scripts/inventory_launch_corpus.py`
- `save-analysis/scripts/summarize_launch_corpus.py`
- `save-analysis/scripts/test_launch_corpus.py`

Modified task files:

- `CREDITS.md`
- `docs/DECISIONS.md`
- `docs/EVIDENCE_STANDARD.md`
- `docs/PERMISSIONS.md`
- `docs/PROVENANCE.md`
- `docs/RESEARCH_STATE.md`
- `docs/SOURCES.md`
- `docs/experiments/README.md`
- `docs/implementation-briefs/README.md`
- `save-analysis/scripts/README.md`

Pre-existing untracked input, unchanged: `docs/implementation-briefs/CODEX_RESEARCH_BRIEF_launch_era_third_party_save_corpus.md`. Frozen historical inventory and existing evidence/scripts were not edited. Local scratch artifacts are not proposed for tracking.

Final `git status --short` (also retained verbatim in validation receipt):

```text
 M CREDITS.md
 M docs/DECISIONS.md
 M docs/EVIDENCE_STANDARD.md
 M docs/PERMISSIONS.md
 M docs/PROVENANCE.md
 M docs/RESEARCH_STATE.md
 M docs/SOURCES.md
 M docs/experiments/README.md
 M docs/implementation-briefs/README.md
 M save-analysis/scripts/README.md
?? docs/experiments/launch-era-third-party-corpus/
?? docs/experiments/launch-era-third-party-save-corpus.md
?? docs/implementation-briefs/CODEX_RESEARCH_BRIEF_launch_era_third_party_save_corpus.md
?? save-analysis/scripts/inventory_launch_corpus.py
?? save-analysis/scripts/summarize_launch_corpus.py
?? save-analysis/scripts/test_launch_corpus.py
```

Suggested single commit after critical review: `research: inventory launch-era third-party save corpus`. No commit or push performed.
