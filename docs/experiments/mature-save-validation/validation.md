# SOR-EV-0012 — Validation and complete review package

2026-10-08, Australia/Sydney. [Report](../mature-save-outpost-validation.md). Critical review pending; authored documentation/helpers/selected ledgers REVIEW-REQUIRED, source and bulk artifacts LOCAL-ONLY. No staging, commit, push or publication approval.

## Checks performed and limits

- Mature compressed length 16411136, decoded length 36934800, 141 stream checksum/EOF/bounds/full-consumption checks. Separate direct physical reconstruction agrees with decoded SHA-256. First stream aligns table end 636 to 640; four opaque gap bytes remain uninterpreted.
- Final run-07 has identical frozen extraction to run-05/run-06, SHA-256 `a1d4490a6b41c05ad08f68b2efa28f71d6ebac56cb9aabf55eb61356833b57e2`. JSON content is read only after extraction close/hash. Comparison repair altered only the JSON key; no expected topology was used to revise extraction.
- Independent count/reference consumption agrees on mature plus all 24 small envelopes, including two separately classified incidental terminal saves. Twenty-two controlled labels / 21 unique saves match original archive manifest hashes and prior decoded hashes; incidental archive hashes are rechecked in final review. Source/copy provenance is inherited, not re-created by this task. One historical manual-corpus original exit-save locator is now unavailable; its preserved archive matches the recorded hash. No unavailable original was replaced or reconstructed.
- Six synthetic unittest methods pass, covering unsigned count widths, truncation, overflow/implausible cardinality bounds, tag 3, trailing bytes, zero keys, duplicates and invalid envelope boundaries. All 1588 proper mature truncations reject; 96 mismatched envelopes and 2000 deterministic random trials reject. Eight shifted small payloads are grammar-valid but framing-invalid; this counterexample is retained. Mature nearby shifts reject. No canonical tag-width rule is asserted.
- Name/table/window checks expose a fixed-three-index counterexample in 15/19 mature beacon windows. All 324 distinct nonzero unit tokens have one matched window; 236 mapped endpoint occurrences share the source's beacon association. This is not complete object framing or engine ownership proof.
- Associated graph has 53 pads (25 regular / 28 interstellar), 48 distinct participating pads, 24 reciprocal pairs and three retained self repeats. All 17 JSON names/counts/types and the full multigraph match. Two parallel connections and three unconnected regular pads permit app-pad permutations; even unique signatures do not establish physical UUID identity. Eight unassociated marker-like windows remain unresolved.
- Original mature save, JSON, existing controlled archives and all offbook material are preserved by final before/after SHA-256, length and mtime checks; access-time behavior is not controlled. New work writes no decoded blob, uses a per-save 64MiB decode bound and checks C:/D: free space above 40000000000 bytes. No game/process/database/configuration effects or external disclosure.
- `git diff --check`, explicit new-file LF/UTF-8/no-BOM/trailing-whitespace checks, local Markdown target/fragment validation, staged-empty and ignored/raw-artifact checks are recorded in `.local-work/mature-save-validation/review-checks.json`. Existing missing links are separated from new ones using pre-task HEAD. Links to external URLs are not fetched. Final checks passed: 258 local Markdown links, no broken links; 239 pre-existing files preserved, 15 authorized existing files modified; 13 new authored files plus the byte-preserved supplied brief. The complete review patch and its final size/hash are in local receipts. These checks do not clear publication rights or prove game semantics.

## New authored review files

- [Separate report](../mature-save-outpost-validation.md), this validation record.
- [All beacon/name hops](beacons.csv), [all small envelopes](envelopes.csv), [199 groups](groups.csv), [all mature count fields](count-fields.csv), [324 token windows](token-windows.csv).
- [All 61 pad candidates](pads.csv), [24 reciprocal connections](connections.csv), [per-outpost comparison](pad-count-comparison.csv), [outpost-pair multiset](multigraph.csv).
- [Narrow validator](../../../save-analysis/scripts/validate_mature_outposts.py), [six safety tests](../../../save-analysis/scripts/test_mature_outposts.py).

Modified existing files: README.md, CREDITS.md; docs/RESEARCH_STATE.md, known-facts.md, state-register.md, hypotheses.md, DECISIONS.md, PROVENANCE.md, SOURCES.md, subsystems/initial-map.md, experiments/README.md, experiments/evidence/README.md, experiments/outpost-save-structural-containment.md, implementation-briefs/README.md; save-analysis/scripts/README.md. The historical structural report has only a dated separate-work cross-reference. No unrelated modifications existed initially. The supplied mature-save brief was already untracked; it remains byte-identical and is included as a pre-existing input in the local full review diff.

Durable additions: SOR-EXP-0006, SOR-EV-0012, SOR-SAMPLE-0029, SOR-F-0012, SOR-ST-0015–0016, SOR-H-0005, SOR-D-0022, SOR-S-0124. No function/interface record or safe integration finding was added. Semantic STRONG promotions remain proposed pending critical review. No new third-party permission issue; existing installed-tool credit and prior project/maintainer research provenance remain mandatory.

## Local-only work and reproduction

`.local-work/mature-save-validation/` retains `before.json`, exact `source-inputs.md`, partial run-01–05, successful run-06/run-07, separate independent/corpus audits, final preservation/checks, file inventory, Git status and **review.diff including all new files and the supplied brief**. No raw/decompressed save is in the review patch.

- `snapshot.py`: repository/archive/offbook/scratch identity inventory and initial Git status; local JSON only.
- `name_diagnostic.py`, `offbook_names.py`, `pad_diagnostic.py`, `inspect_results.py`, `inspect_final.py`, `challenge_summary.py`: bounded direct byte/JSON inspections, console output; no input edits. Exploratory outputs are not independent proof.
- `independent_checks.py`: mature compressed-size/stream reconstruction, separately reasoned counts/references, random/nearby negatives, local ownership and excluded-token checks; writes independent-checks.json only.
- `corpus_challenge.py`: controlled and two incidental archived copies, independently consumes payloads, checks alignment and mismatched framing, every mature truncation; writes corpus-challenge.json only.
- `adjust_directory.py`, `adjust_names.py`, `adjust_pads.py`, `finalize_helper.py`, `update_final_refs.py`: sequential source/document authoring only, no game effects; not reusable analysis automation. Initial failures retained; no offbook code is modified.
- `build_report.py`, `update_records.py`: select numeric/name fields into authored report/CSV/registers; no raw gameplay fixtures or private UUIDs promoted. Do not rerun append/exclusive-create helpers over completed outputs.
- `final_review.py`: verify preserved bytes/timestamps, compare selected tables with final frozen extraction, check links/encoding/Git boundaries, export tracked-plus-untracked review diff and inventory without staging.

Run the installed Python with `-B save-analysis/scripts/validate_mature_outposts.py --run <fresh-name>`; no installation. Focused tests: `-B -m unittest discover -s save-analysis/scripts -p test_mature_outposts.py -v`. Exact runtime/tool/helper hashes, command configurations and derivative timestamps are retained locally; checksum success is evidence integrity, not semantic approval.

Remaining unknowns: reference collection inclusion/owner, zero-key purpose, retained-state history, complete object bounds, stable identities, loader authority and cargo timing/direction. The bounded task stops here for critical review. Any next controlled live experiment requires its own brief. Suggested later commit: `research: validate mature-save outpost relationships and cargo topology`.
