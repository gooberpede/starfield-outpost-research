# SOR-EXP-0009 validation and review inventory

2026-10-09. SOR-EV-0015. [Report](../active-outpost-identification.md). Critical review pending; no staging, commit, sync or publication. This is the review package for a documented reconstruction/semantic obstruction, not a validated active-outpost classifier.

## Actual scientific checks

- Full frozen corpus: 412 labels / 389 distinct source hashes; 409 exact directory-count/R3-end closures, 48,863,625 records, three decoded-size exclusions (HIST-0252/0256/0257). Seven embedded first-version strata; originating executable identities unknown.
- Six synthetic test methods pass: supported count widths, explicit/default headers, queues/body framing, truncations, exact closure and conditional prefix offsets/reference decoys. Final command: `test_outpost_record_framing.py --corpus --run final`.
- Separate arithmetic walker matches 11 verified inputs / 874,242 records, including zero/one controls, S7, reload, mature, historical alternate-representation examples and one donor. Implementation-independent, same native format evidence/shared physical decoder. Final receipt `.local-work/active-outpost/independent-final.json`; initial receipt preserved.
- All 23 control labels reproduce expected inline diagnostic counts: three zero labels and 20 one labels; L0/S4C and HIST overlap prevent independence claims. Mature 19 diagnostics split 17 disabled-clear / two disabled-set; all deleted-clear. HIST-0083 has 18/2, with collection 17. HIST-0016 has 1/1 inline diagnostics plus three collection members lacking that inline base. No historical gameplay label inferred from these metrics.
- 1,804 inline diagnostic occurrences: 1,717 disabled-clear/promoted/auxiliary 0x40; 87 disabled-set/not-promoted/auxiliary 0x41. Exact correlation does not discriminate causality or establish active player ownership.
- Native code/callback operands and queue readers support conditional field semantics. Read-only Ghidra exports compiled/executed both original reader modes and new constant/full-text modes. Caps/cancellation and failed searches remain local. No bounded scan is treated as exhaustive native coverage.

## Preservation and provenance

`.local-work/active-outpost/final-preservation.json` rechecks **411 source/archive paths**, the original donor archive, pinned retail executable and 60 tool/export/script identities. All expected originals/archive identities match. Fifteen retail Ghidra-project files match mid-run/final snapshots **and** the retained earlier retail snapshot; CK entries in the older combined snapshot are outside this run's comparison. The missing contemporaneous pre-first-export snapshot remains a limitation. No Ghidra analysis, symbol/type/comment changes occurred; settings/cache/log output is documented separately.

Raw saves, decoded bytes, private paths/names, fingerprints and native decompilation are ignored/local. Selected CSVs contain neutral source labels, hashes and relevant authored numeric measurements. Donor raw redistribution remains excluded under SOR-P-0003; no permission correspondence or bulk payload is included. Original project code only; source-informed installed native semantics (SOR-S-0127), prior project methods (SOR-S-0124), definitions/scripts (SOR-S-0103/0104) and installed separate tools are credited in SOURCES/CREDITS.

## Exact changed-file inventory

New authored files:

- `docs/experiments/active-outpost-identification.md`
- `docs/experiments/active-outpost-identification/manifest.csv` — 412 labels; not 412 independent saves.
- `docs/experiments/active-outpost-identification/record-ledger.csv` — selected exact record/flag measurements.
- `docs/experiments/active-outpost-identification/versions.csv` — seven full strata plus three size-limited entries with no version extracted by this run.
- `docs/experiments/active-outpost-identification/validation.md`
- `ghidra/scripts/OutpostSaveConstants.java`
- `save-analysis/scripts/investigate_active_outposts.py`
- `save-analysis/scripts/outpost_record_framing.py`
- `save-analysis/scripts/test_outpost_record_framing.py`

Modified files:

- `CREDITS.md`
- `docs/DECISIONS.md`
- `docs/PROVENANCE.md`
- `docs/RESEARCH_STATE.md`
- `docs/SOURCES.md`
- `docs/experiments/evidence/README.md`
- `docs/hypotheses.md`
- `docs/known-facts.md`
- `docs/state-register.md`
- `docs/subsystems/initial-map.md`
- `ghidra/README.md`
- `ghidra/scripts/Invoke-OutpostRecon.ps1`
- `ghidra/scripts/OutpostRecon.java`
- `save-analysis/README.md`

Pre-existing user-supplied untracked file, preserved without edits and included separately in the review inventory:

- `implementation-briefs.zip :: docs/implementation-briefs/CODEX_RESEARCH_BRIEF_active_outpost_identification.md`

All remaining new research files are ignored under `.local-work/`. No unrelated tracked changes existed at task start. Repository/Markdown/CSV/syntax checks and a complete tracked-plus-untracked review patch are retained in `.local-work/active-outpost/review-checks.json`, `review.patch` and `final-status.txt`. These artifacts are local and are not publication approval.

## Repository checks and final status

`git diff --check` PASS; Python AST parsing PASS; 198 internal Markdown target paths checked with zero broken targets; authored new-file whitespace and CSV counts/control regressions PASS. The first broad whitespace audit flagged three existing Markdown hard-break lines in the user-supplied brief; they were preserved and excluded from the authored-file whitespace test. No staged entries or new tracked raw/binary files; ignored evidence remains ignored. Final inventory: 14 modified tracked files and ten untracked files (nine authored plus the supplied brief). The complete review patch includes tracked changes and all untracked review files, without staging.

```text
 M CREDITS.md
 M docs/DECISIONS.md
 M docs/PROVENANCE.md
 M docs/RESEARCH_STATE.md
 M docs/SOURCES.md
 M docs/experiments/evidence/README.md
 M docs/hypotheses.md
 M docs/known-facts.md
 M docs/state-register.md
 M docs/subsystems/initial-map.md
 M ghidra/README.md
 M ghidra/scripts/Invoke-OutpostRecon.ps1
 M ghidra/scripts/OutpostRecon.java
 M save-analysis/README.md
?? docs/experiments/active-outpost-identification.md
?? docs/experiments/active-outpost-identification/
?? docs/implementation-briefs/CODEX_RESEARCH_BRIEF_active_outpost_identification.md
?? ghidra/scripts/OutpostSaveConstants.java
?? save-analysis/scripts/investigate_active_outposts.py
?? save-analysis/scripts/outpost_record_framing.py
?? save-analysis/scripts/test_outpost_record_framing.py
```

## Remaining review questions

Milestone A is partial, B is not achieved, and C is mechanically complete within guards but only partially blinded. Review the conditional initial-data/base interpretation, alternate representation records, registry/keyword/ExtraWorkshop reconstruction requirements, causal-test need and absence claim restrictions. Confirm that the selected authored ledgers are appropriate for eventual tracking/publication; no raw evidence has been cleared. A separately authorised removal/reload control would discriminate candidate activity rules but would not by itself prove completeness. The report does not assert that offline reverse engineering is impossible or that all static paths are exhausted.

Suggested commits **after critical review only**:

```text
research: document active outpost identification evidence and blockers
tools: frame save change records and decode conditional beacon state
```

The originally proposed `research: identify active outpost membership in save files` would overstate the present semantic result. Nothing has been committed or synced.
