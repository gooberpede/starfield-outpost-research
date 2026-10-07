# Manual corpus coordinate/status correction

2026-10-07, Australia/Sydney. Documentation/offline-analysis only; REVIEW-REQUIRED. The user's correction request authorizes verification of prior A0/A0C coordinates, arithmetic comparison with existing save candidates, conservative location-record updates, historical-status repair and review exports. No game launch, SFSE deployment, debugger, live-save mutation, next experiment, staging, commit or push.

## Evidence and result

Authoritative live sources are the original archived `A0.json` and `A0C.json`, JSON pointer `/player/coordinates/reference_xyz/value`, under ignored `.local-work/exp0002-review14-live/archive/observer/`. Both files' exact size/SHA-256 match [SOR-EV-0004](../experiments/evidence/exp0002-review14-live/README.md). Their captured XYZ is identically `(120.827057,270.736237,17.5202465)`; difference and distance are zero at recorded precision. The [full correction section](../experiments/manual-save-corpus-S0-S7C.md#offline-comparison-with-earlier-exp0002-live-player-coordinates) retains hashes, capture times, exact decoded candidate inputs, offset domains, method and limits.

Distances from either recorded live tuple: beacon **6.830539**, pre-S6 solar **8.997486**, post-S6 solar **26.000118**, with no assigned physical unit. Decimal calculation and `math.dist` agree within 1e-12. OBSERVED numerical proximity is plausible for placement near the reported site; INFERRED same/related local Cartesian frame remains PROVISIONAL (SOR-H-0004). UNKNOWN origin, units, axes, ownership, planetary/body-relative interpretation and lat-long conversion. Earlier live and later save sessions are not a paired checkpoint. Neither object roles nor output-link/transform authority was promoted.

Kreet remains the supported site/body label, Narion only a provisional script-name/system lead, local XYZ provisional with additional numerical support, and planetary coordinates unresolved. The storage short-token collision remains documented. Output-link remove/recreate remains a recommendation predicting present→absent→present with principal objects unchanged, not executable authority.

## Documentation changes

- Manual corpus report: exact source/coordinate/distance comparison and observed/inferred/unknown separation.
- Research state, findings, state register and hypotheses: scoped cross-reference and SOR-H-0004; no broader semantic strengthening.
- Initial subsystem map: the construction pause is explicitly historical during EXP-0002A; subsequent manual outpost work resumed independently of native saving.
- This audit: durable correction scope, validation and handoff.

## Preservation and review

Before editing, prior repository text was snapshotted into ignored `.local-work/manual-corpus-coordinate-correction/before/`; 115 evidence/corpus files were hashed, including the 17 live corpus originals, archived copies, decoded/analysis outputs, earlier review package/manifests, the review14 archive and durable evidence indexes. All 115 are rechecked unchanged at handoff. Existing save/dump evidence hashes and indexes are preserved. Unrelated raw crash dumps were neither opened nor modified; their full contents were not redundantly rehashed. No claim of a fresh all-dump integrity audit is made.

Local `compare_positions.py` reads verified prior captures/index and three existing decoded copies/candidate records; writes only new `comparison.json`. Installed CPython/standard library, no downloads or new dependencies. Local `finish_review.py` rechecks preservation, text/links/Git state, and creates correction-only/full diffs and status/validation outputs without Git writes. These helpers and new outputs stay in the correction directory; earlier corpus review outputs remain unchanged.

Validation results and exact file lists: `validation.json` in that directory. `git diff --check`, correction text UTF-8/LF/trailing-whitespace checks and internal Markdown file/heading links pass; no raw save/dump/binary becomes tracked and the Git index is unchanged. There is no new live result and no need to rerun the unchanged decoder's tests for this documentation/arithmetic correction.

Review files in `.local-work/manual-corpus-coordinate-correction/`: `correction-only.diff` compares this correction against the pre-correction working tree; `full-review.diff` includes all existing corpus work and every untracked file, including the unchanged supplied brief; `git-status-short.txt` gives final status. The original corpus review package is preserved rather than overwritten. No publication/commit approval follows from this audit.
