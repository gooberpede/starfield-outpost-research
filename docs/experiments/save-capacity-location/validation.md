# SOR-EXP-0012 review and validation

2026-10-09, Australia/Sydney. Critical review pending. [Answer-first report](../save-capacity-and-planetary-location.md). No staging, commit, push or publication.

## Checks and limits

- 69 stdlib unittest methods pass across save-analysis/scripts. New tests cover 65 MiB + 1 byte aggregate output with <2 MiB measured Python allocations; physically feasible >1 GiB header without a full 1 GiB decode; extreme/false total and chunk declarations; truncation, zlib integrity/expansion; low-space and configurable scratch/time budgets; consumer-failure cleanup; bounded queues; body-key agreement, ambiguity, wrong parents/bodies, NaN, truncation and global suffix closure. Original synthetic fixtures only. This does not prove every valid save or malformed-input behavior.
- Eleven actual capacity scans close every stream and declared R3 record, including the three formerly excluded saves. Separate ten-label primary detector regression reproduces primary counts and scans the large saves. Four common labels agree with the preserved prior primary run; six-sample body extraction includes S1C and remapped L2C plus Save2 and Save52. No live observation was performed.
- Retained ESM catalog script independently reruns the initial catalog command and returns an identical 39,055-record catalog object. This is same-parser reproduction, not a second-parser validation or historical ESM baseline.
- Save52 extraction is frozen before each comparison phase; all 17 JSON-corresponding body/system pairs agree. Earlier aggregate/name/topology knowledge and repeated runs preclude a fully blind claim. UUID correspondence and full component record grammar remain unknown.
- Original/archive identities actually read are rechecked against frozen manifests and again at final validation. ESM, JSON, pinned executables and the supplied brief are separately identified. Database-file before/after inventories agree for all six new readOnly/noanalysis exports. Checksums establish bytes, not semantics or publication rights.
- Temporary decoder scratch is removed after contexts, including synthetic failure paths. Peak actual scratch is one 129,062,006-byte save. Python allocation peaks are in [capacity.csv](capacity.csv); whole-process RSS/mapped residency was not measured. Final resource receipts stay local.
- `git diff --check`, task-authored new-file whitespace/UTF-8/LF checks and changed-document relative Markdown file-target checks pass. Existing heading anchors and external URLs are not independently validated. The legacy README code-layout mention of absent GIT_SETUP.md is preserved historical text. A transient Windows cp1252 decoding error was corrected using exact HEAD text plus task additions; final tracked documentation diffs contain additions only.
- No newly tracked or newly untracked deliverable is a raw save, memory dump, binary, private JSON or substantial ESM/native export. All new deliverables are authored Python/Markdown and selected small CSV ledgers. No index operation occurred; existing tracked raw-evidence eligibility is outside this task's publication review.

## Local receipts and preserved failures

`.local-work/save-capacity-location/` retains controls-01, mature-lodge-02, capacity-final, initial/final ESM catalogs, fixed anchors, initial body-blind/body-spatial-blind receipts, body-final-01/02/03 (final body check), database preservation, checks and review output. `.local-work/ordinary-beacons/` retains capacity-regression-01/final/verified (final decoder regression). Final checks record exact applicable run names and hashes. `mature-lodge-01` stopped on an unknown requested donor label before processing a save. The WindowsApps Python alias was inaccessible; calls used the explicit installed CPython executable. No game or source-save recovery/cleanup was needed.

## Complete change inventory and review diff

The generated local `review/file-inventory.json` records every changed/new file and hash; `review/git-status.txt` is exact `git status --short`. `review/task-only.diff` includes tracked changes and every new deliverable; `review/full.diff` additionally includes the pre-existing supplied untracked brief, identified as an input. Neither export stages anything. The package remains ignored/local and contains no raw proprietary evidence.

Task files:

- `CREDITS.md` — task change/new deliverable.
- `README.md` — task change/new deliverable.
- `docs/DECISIONS.md` — task change/new deliverable.
- `docs/PROVENANCE.md` — task change/new deliverable.
- `docs/RESEARCH_STATE.md` — task change/new deliverable.
- `docs/SOURCES.md` — task change/new deliverable.
- `docs/experiments/README.md` — task change/new deliverable.
- `docs/experiments/save-capacity-and-planetary-location.md` — task change/new deliverable.
- `docs/experiments/save-capacity-location/capacity.csv` — task change/new deliverable.
- `docs/experiments/save-capacity-location/save52-location.csv` — task change/new deliverable.
- `docs/experiments/save-capacity-location/validation.md` — task change/new deliverable.
- `docs/hypotheses.md` — task change/new deliverable.
- `implementation-briefs.zip :: docs/implementation-briefs/CODEX_BRIEF_SOR_save_capacity_and_outpost_planetary_location.md` — pre-existing supplied input; unchanged.
- `docs/implementation-briefs/README.md` — task change/new deliverable.
- `docs/known-facts.md` — task change/new deliverable.
- `docs/state-register.md` — task change/new deliverable.
- `docs/subsystems/initial-map.md` — task change/new deliverable.
- `save-analysis/scripts/README.md` — task change/new deliverable.
- `save-analysis/scripts/detect_ordinary_outpost_beacons.py` — task change/new deliverable.
- `save-analysis/scripts/inspect_spatial_definitions.py` — task change/new deliverable.
- `save-analysis/scripts/outpost_membership.py` — task change/new deliverable.
- `save-analysis/scripts/outpost_planetary_location.py` — task change/new deliverable.
- `save-analysis/scripts/outpost_record_framing.py` — task change/new deliverable.
- `save-analysis/scripts/research_save_location.py` — task change/new deliverable.
- `save-analysis/scripts/run_planetary_location.py` — task change/new deliverable.
- `save-analysis/scripts/stream_save.py` — task change/new deliverable.
- `save-analysis/scripts/test_planetary_location.py` — task change/new deliverable.
- `save-analysis/scripts/test_stream_save.py` — task change/new deliverable.

## Remaining obligations

Critical review of the decoder/CLI compatibility and proposed scoped STRONG body interpretation; publication/privacy review of selected ledgers; precise surface-pair serializer/consumer, axes/units/origin and anchor-to-beacon relationship; historical-version location challenge if later authorized. Frozen historical classifications and unrelated findings remain intact. No new third-party permission issue arose; prior donor restrictions remain.

Suggested later commits, subject to review:

```text
research: stream large saves with bounded working allocations
research: resolve saved outpost bodies and surface-anchor candidates
```
