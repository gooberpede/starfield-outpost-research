# SOR-EXP-0011 validation and review package

2026-10-09, Australia/Sydney. [Answer-first report](../ordinary-outpost-beacon-detection.md). REVIEW-REQUIRED; no integration/publication approval. Starting HEAD `4029c5242edc8dde2651260b896d22b31c401744`. Initial Git status contained only the supplied untracked brief, which this task retained unchanged. No staging, commit, push, remote or branch change.

## Actual checks and their limits

- Installed CPython 3.14.3, `-B -m unittest discover -s save-analysis/scripts -p 'test_*.py' -v`: **54 tests pass**, including nine new detector tests. The tests use synthetic bytes and actual R3/prefix readers; the new directory is injected to isolate record semantics. Existing physical, directory, grammar, inventory and launch-corpus suites remain green. Synthetic behavior is not gameplay proof.
- Six primary archived saves: all specified zero/one/19 outcomes pass; exact hashes in [saves.csv](saves.csv). Candidate identity/counts are extracted without expected labels.
- Separate arithmetic R3 walker plus independent flag-position/value computation: **six saves / 309,057 records**, matching all primary ordinary tokens, record bounds, offsets and flags. Shared decompression/directory/native evidence limits independence to implementation.
- Fresh protected JSON comparison after detection: **17 clear records match all 17 distinct manual network outpost names**, both disabled-set records fall outside. Existing mature token/name association is reused; no prior active labels are consumed. JSON hash is checked against its earlier manifest, and before/after identities match. The oracle's independent gameplay documentation is not engine authority and retains prior timing/capture-history uncertainty.
- Bounded frozen historical/donor challenge: per-label outcomes and embedded-version coverage are recorded in [saves.csv](saves.csv) and [versions.csv](versions.csv); see the report for exact aggregate measurements and unsupported files. Unlabelled gameplay states remain UNVERIFIED.
- Final challenge: 412 labels / 389 hashes; 409 full framings / 48,863,625 records; 1,804 ordinary occurrences (1,717 clear / 87 set); 21 case-6 omitted-state template leads plus 130 reference-only cargo-quest leads. Three decoded-size limits are explicitly unsupported. All 111 donor saves frame with zero matches, without semantic absence claims. Frozen `results.json` SHA-256 `6e08254c5dd075d9c9adbdc6a5cb08ffb10deeaa4ae8d7ba70793973296394b8`; full-run time 666.6 seconds. All comparable ordinary counts/flags agree with the previous prototype; previous labels are comparison evidence only.
- Every analyzed input is a manifest-verified existing local archive. Original saves are hashed for preservation only. Fresh receipts record before/after equality for inputs, manifests, tool files and catalog. No new save copies or decoded blobs were written. Private oracle and raw inputs remain unchanged.
- Final preservation receipt: **700 paths unchanged**, including **667 save paths**. Tool hashes cover executed reader/runner files and the installed interpreter; the final review inventory additionally hashes the newly added synthetic test and local audit/ledger/packaging scripts. The test file was added during the long challenge but was not imported by that runner; executed files were unchanged.
- `git diff --check`, new-text whitespace/encoding checks, local Markdown target/anchor checks, Git status and raw-artifact inventory are captured in the final local `review/checks.json`. Existing missing links are distinguished from newly introduced failures. These checks do not clear publication or certify all historical repository links.
- Final checks pass for all changed/new text: UTF-8 without BOM/LF and whitespace, Markdown file targets/anchors, empty staged diff, unchanged HEAD, ignored raw receipts and no tracked raw save/ESM/archive/dump/database artifacts. All **23** changed/new source files (14 modifications, eight task-authored new files, unchanged supplied brief) are included. Git reverse-apply `--check` validates the complete diff against current file contents without applying it. The initial link check correctly stopped before the pending challenge ledgers existed; the final check passes with those ledgers present.

The plain `python` command initially resolved to an inaccessible WindowsApps alias and failed before running the tool. All successful invocations use the explicit installed interpreter path in the report. No installation/configuration change was made.

## Exact new and modified files

New task-authored source/deliverable files:

- `save-analysis/scripts/ordinary_outpost_beacons.py`
- `save-analysis/scripts/detect_ordinary_outpost_beacons.py`
- `save-analysis/scripts/test_ordinary_outpost_beacons.py`
- `docs/experiments/ordinary-outpost-beacon-detection.md`
- `docs/experiments/ordinary-outpost-beacon-detection/saves.csv`
- `docs/experiments/ordinary-outpost-beacon-detection/versions.csv`
- `docs/experiments/ordinary-outpost-beacon-detection/save52-records.csv`
- `docs/experiments/ordinary-outpost-beacon-detection/validation.md`

Existing modified files:

- `save-analysis/scripts/outpost_membership.py`: optional diagnostic output for known-base reference occurrences and record/queue positions; default membership decisions preserved.
- `save-analysis/scripts/README.md`: read/write/prerequisite/effect/limit documentation for the detector and tests.
- `README.md`, `docs/RESEARCH_STATE.md`, `docs/known-facts.md`, `docs/state-register.md`, `docs/subsystems/initial-map.md`: scoped result, proposed interpretation and boundaries; historical records retained.
- `docs/DECISIONS.md`, `docs/PROVENANCE.md`, `docs/SOURCES.md`, `CREDITS.md`: authorization, evidence and reused tool/source attribution.
- `docs/experiments/README.md`, `docs/experiments/evidence/README.md`, `docs/implementation-briefs/README.md`: navigation and review status.

The initially untracked user-supplied `implementation-briefs.zip :: docs/implementation-briefs/CODEX_BRIEF_SOR_scoped_ordinary_outpost_beacon_detection.md` is included unchanged in the complete review diff; it is not task-authored work. Ignored local independent-audit/summary/packaging scripts and exact identities are retained alongside receipts. They contain no incorporated third-party implementation.

## Review artifacts and remaining issues

Local review directory: `.local-work/ordinary-beacons/review/`.

- `task-only.diff`: every authored tracked/untracked text change, excluding the unchanged supplied brief.
- `complete.diff`: all tracked changes and every non-ignored untracked text source, including that brief.
- `files.json`, `checks.json`, `status.txt`: complete source inventory/hashes, actual check outcomes and verbatim final Git status. Diffs use Git-generated binary-capable output without staging; no raw payload is included.

Raw-analysis/preservation results are `.local-work/ordinary-beacons/primary-01/` and `challenge-01/`; separate primary/oracle audit is `independent-primary.json`. Exact absolute source paths and names remain local. Authored numeric ledgers retain only selected identifiers/counts/offsets; substantial third-party material is excluded. Source/code confidence does not establish publication eligibility. No new reuse permission is needed for the project-owned helpers; donor SOR-P-0003 restrictions remain unchanged.

Remaining unknowns are inherited type certainty, full R1/template reconstruction, historical content/override equivalence, omitted/default flags, ExtraWorkshop/keyword/parent/registration filters, player ownership and load authority. They restrict exhaustive enumeration and absence, while leaving the ordinary supported positive result useful. Deferred IsDeleted/quest/native-save work remains deferred. No permission blockage prevented this bounded implementation. Await critical review; suggested commit message only:

```text
research: implement scoped ordinary outpost beacon detection
```
