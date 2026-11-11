# E3 bounded offline research utilities

[Brief](../../docs/implementation-briefs/README.md#archive-lookup) (`implementation-briefs.zip :: docs/implementation-briefs/CODEX_BRIEF_SOR_E3_fabricators_manufactured_production.md`),
[report](../../docs/experiments/fabricators/report.md).
Original GPL-3.0-or-later research code, adapting the existing maintainer-owned
[E2 readers](../e2-organic/README.md) and their project save/ESM dependencies.
These are evidence utilities; no player-facing production tool is implemented.

Use installed CPython with `-B` from the repository root. Standard library and
repository `save-analysis/scripts` only. Inputs must already exist; no dependency
download or original evidence regeneration is performed. All raw derivatives
and receipts remain under ignored `.local-work/e3-fabricators/`. Run names are
exclusive so earlier attempts remain preserved. Existing readers apply C:/D:
free-space guards, save header qualification and decompression/framing bounds.

| Script | Reads / prerequisites | Writes / actual run |
|---|---|---|
| catalog.py | E2 inventory02, installed pinned main ESM | `--run catalog05 --tables`: exclusive local JSON, facilities.csv and recipes.csv; 308 physical record rereads, full group/header walk for 30 pack-in producer joins; deterministic family/property/input/output/AVIF-flag assertions |
| saved.py | Frozen 278-row historical inventory, available hash-pinned originals, catalogue02 | `--run saved01`, then `--run saved01 --resume`: per-save JSON and progress/summary; 184 selected profiles, 163 available originals hashed before/after; temporary decoded scratch cleaned. Resume validates retained source identities and records unavailable frozen paths without restoring them |
| details.py | `--sample HIST-0036` saved01 receipt, its original, E2 inventory02, catalogue04 | `--run detail05`: exclusive JSON, 307 endpoint joins, 17 selected-base corroborations, required-resource incoming paths and explicit buffer/cargo boundaries; cleaned scratch, no inventory totals |
| verify.py | Authored CSV/text/scripts, catalogue05, prior/new evidence, pinned ESM/executable/cache, stopped Ghidra database files, HEAD/index and supplied brief baseline | Fresh `--run`: exclusive ignored verification JSON; checks bytes/tables/prose/register addresses and protected identities. Native semantics still require instruction review |

Earlier receipts are intentional dependency pins. Catalogue02 has the same
resource/base population used by the historical scan; catalogue04 adds AVIF
fields and checks, and catalogue05 corrects the excluded flag to bit 1 (mask 2).
Final tables come from catalogue05. Every ordinary AVFL has mask 2 clear; other flag bits remain present. The mask
correction changes the check's meaning without changing the observed population.
Catalogue01's incorrect EditorID filter and initial detailed-reader assumptions
remain failed local history, not negative scientific findings.

The saved parser originally halted at a missing frozen exit-save path. Its
resume handles missing sources explicitly and does not weaken save-version
qualification. Earlier and resumed progress are retained separately. It does
not assert complete save-instance coverage: ordinary inline-base beacon rows
are a recognized positive subset. The detailed reader decodes supported leading
extra types before BF and distinguishes explicit BF selection from a saved
producer/base join whose selected value comes from the definition preset.

These scripts do not launch the game, invoke native functions, restore/modify
saves, modify game/plugin settings, change an analysis database or mutate Git.
Read-only native exports use existing owned `E2ReadSession.java` and
`OutpostRecon.java` through the existing no-analysis session workflow; proprietary
exports stay local. No newly executed third-party implementation is incorporated.
Publication/review eligibility remains separate from confidence and integrity.
