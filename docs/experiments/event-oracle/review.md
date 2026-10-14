# EXP0024 review package and validation

2026-10-11. [Answer-first report](../event-associated-position-oracle-and-build-mode.md),
[scope](../../implementation-briefs/CODEX_BRIEF_SOR_event_associated_oracle_and_build_mode_failure.md).
Authored derivatives REVIEW-REQUIRED, raw native/save/capture/private data
LOCAL-ONLY. No publication clearance, live implementation or execution authority.

## Deliverables

New authored files: main report and this directory's native map, ranked
acquisition design, preview state investigation, prior-art ledger, terminal
dependency ledger and review. New original integrity script
`save-analysis/scripts/audit_event_oracle_inputs.py` and its usage/effects
documentation. Updated root/state/decision/source/provenance/credits/function/
state/finding/subsystem/evidence/experiment/brief indexes. The user-supplied
brief is preserved unchanged and listed separately from task-authored changes.
Complete exact inventory and hashes are in the ignored final review manifest.

Local `.local-work/event-oracle/` retains `before.json`, `after.json`,
`input-integrity-before.json`, `input-integrity-after.json`, source/export
identities, validation receipts, Git status and complete review diffs. The
review-package ZIP includes authored source/docs, supplied brief, LICENSE,
task-only/cumulative diffs and selected validation metadata. It excludes game
executables/assets, saves, decoded saves, memory captures, Ghidra exports/DBs,
runtime DLLs and third-party implementations. It is a local review artifact,
not cleared for publication.

Task-only diff includes every tracked edit and new authored file, excluding the
pre-existing supplied brief. Cumulative diff includes that brief as well, against
starting HEAD `dda84e2af385cae8d7f24563aed6c8554dd75076`. No staging is used
to generate either diff. The package builder reads Git/source/receipts and writes
new ignored artifacts only; its original local source is retained for audit.
Final package and receipts live under `.local-work/event-oracle/review-03/`:
22 authored files plus the supplied brief, 602 checked relative-file links,
zero link issues. Both complete diffs pass `git apply --check --reverse` against
the resulting working tree; this checks review-patch completeness without
applying, staging or committing anything.

## Actual checks and their limits

- Fresh original integrity audit before/after: **25 checkpoints, 14,645 raw
  sections PASS**, comprising Phase 1's16/9412 and initial 9/5233. Original
  inspector verifies raw sizes/hashes/path safety; final markers present and no
  truncated final journal lines. Journals hashed. Four protected Save25/26
  source/archive hashes match prior postflight receipts on both audits.
- Before/after 20-file snapshot covers the installed executable, all persistent
  files under the selected Ghidra project directory, frozen inputs/predictions,
  validation protocol and Phase 1 CSV. Compare hashes/sizes in final receipt.
  No claim of full filesystem/metadata equality; the snapshot records content,
  not original timestamps. Ghidra runs were readOnly/noanalysis.
- All 13 new Ghidra export commands completed; script/log errors and selector
  coverage checked separately from exit code. Whole-existing-instruction +130
  scan 14,392,060 instructions/3394 candidates, not cancelled. Broad symbol
  searches sometimes reached 256 entries; none supports an absence claim.
  Wait3D entry/exit NO_FUNCTION_AT yielded existing defined instruction bodies;
  no function/type/symbol was created. Decisive typed branches have successful
  decompilation/instruction coverage; unrelated broad symbol inventories are
  not an exhaustive semantic census.
- Existing saved-position regression suite: **8 tests PASS** using installed
  CPython 3.14.3, `-B -m unittest discover -s save-analysis/scripts -p
  test_durable_position_model.py`. No new engine equivalence follows from these
  arithmetic/input-domain regressions. Original integrity script exercised
  against the real archived corpus, rather than implementation-mirroring tests.
- Final changed/new Markdown relative-file links, whitespace checks, complete
  diff and Git status are retained in validation receipts. Link checking covers
  local target existence; not web availability, Markdown anchor rendering or
  external source truth. Prior-art direct-access limitations remain explicit.
- C:/D: free space above 40,000,000,000 bytes at both preservation/capture audits
  and final packaging. No game/config/Vortex state was changed.

Initial plain `python` helper invocation resolved to inaccessible WindowsApps
alias; corrected to the installed explicit CPython path. Initial audit prototype
used `checkpoints` rather than receipt's actual `captures` key and failed before
writing a receipt; corrected before the passing audits. Initial lowercase preview
symbol search missed case-sensitive matches; corrected to typed UI names and
constructors. Initial metadata patch's header mismatch made no edits; corrected
to actual headings. Missing exploratory paths/PowerShell wildcard searches were
corrected with exact paths/rg globs. These failed exploratory commands are not
counted as passing controls or native evidence. No input mutation resulted.
Packaging attempt 01 caught a trailing blank line in the brief index (fixed);
attempt 02 passed checks but failed ZIP completion because it assumed `COPYING`
rather than the existing `LICENSE`. Both local attempts are retained; attempt 03
uses the actual licence file and supplies the completed package. No GPL text
was edited.

## Review decisions still needed

Review typed ownership and caller associations, zero-radius interpretation,
actual-reference versus descriptor-input distinction, entry/common-epilogue
bridge feasibility, frame qualification and raw-identity lifetime plan.
The exact Phase 1 writer/reset sequence, actual effective radius, native grid
reachability/current-frame join and spinner failure resource/UI epoch remain
unobserved. Review must precede a separate implementation brief and any live
card; none is implicitly approved by this handoff. No third-party reuse request
or permission blockage arose: consultation only, maintainer exception retained.

Suggested later commit subject, after critical review:

```text
research: map event-associated position oracles and build-mode state
```
