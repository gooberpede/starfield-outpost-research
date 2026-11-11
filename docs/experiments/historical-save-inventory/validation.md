# SOR-EV-0013 — Historical inventory validation and review package

2026-10-09, Australia/Sydney. [Report](../historical-save-inventory-triage.md). SOR-EXP-0007 / SOR-F-0013. Critical review pending. Authored summaries/helpers/selected numeric tables REVIEW-REQUIRED; originals, archives, full local inventory and exploratory probes LOCAL-ONLY. No publication/integration approval.

## Checks and limits

- Whole-directory enumeration: 278 distinct original hashes, exact source paths/sizes/ctime/mtime and two separate header-version fields retained locally. All original identities rechecked after the scan and final archive validation. Reads can affect access times; access-time immutability is not claimed.
- Physical BCPS/table/stream/padding/EOF bounds pass for all 278; 275 full bounded zlib transforms pass checksum/length/EOF and directory/string/envelope grammar. Three saves exceed the 64 MiB decoded limit and receive first-stream inspection only. Resource limits are not bypassed to obtain a result.
- Final inventory is scan-04. Prior scans are preserved: scan-01 exposed plugin-version regex contamination, an invalid fixed-offset float probe and incomplete name calibration; scan-02 narrows version/name extraction; scan-03 permits an explicitly qualified empty-keyed-collection absence case. A later independent audit caught the header uint32 probe being one byte early (+15); scan-04 corrects it to +16, observed 27, semantic meaning UNKNOWN. No original or old receipt was repaired. Earlier scan-03 classification counts remain unchanged by that metadata correction.
- Twenty-five control labels (Save3, 17 manual labels including incidental exit, seven L labels including their incidental exit and S4C/L0 alias) match existing manifest source-copy hashes and prior decoded hashes where available. Save3/S0/S0C satisfy the negative gate; S1/S1C/S2/S2C retain named beacons with empty reference collections; S7/S7C retain named saved state despite the controlled deletion stage. These calibrations do not cover every historical version or every residual-state class.
- Mature baseline HIST-0267 matches the previously frozen decoded SHA-256, directory, all 19 names and exact 24 reciprocal pairs. All 61 marker windows remain, with the validated associated subset of 25 regular / 28 interstellar. Physical-pad UUID identity and runtime activity are still unproven.
- Separate physical reconstruction and an independently written count cursor check five profiles: HIST-0267, 0265, 0268, 0250 and 0271 (empty-collection positive). Exact stream hashes and full relationship grammar agree. These checks corroborate structural extraction, not semantic absence or loader behavior.
- Four new exclusive copies total 80,590,416 bytes; the existing mature archive is reused. All five archive hashes/sizes and source identities are verified again. Originals and previous offbook/research artifacts remain unchanged; no save/cloud cleanup occurred.
- Ten new synthetic tests pass: physical closure, bounded decompression/checksum behavior, header version scope, empty-collection positive, absence-gate safeguards, retained markers, candidate-window matching, low-disk stop, variable-index location probe and unsupported-inspection classification. Six existing mature grammar tests pass. No proprietary fixture is included. Decoder rejection maps to INDETERMINATE/UNSUPPORTED, never an absence or corruption assertion.
- Location fallback is a separate post-inventory hypothesis generator. Thirty-six name-associated float triples across four saves are finite; exact source/decoded hashes and logical offsets are retained. A fallback name pair plus plausible numbers does not prove a body ID, complete object record, local transform or planetary coordinate.
- Final review checks cover `git diff --check`, all changed/new authored text UTF-8/LF/no-BOM/trailing whitespace, local Markdown file/fragment links, selected-manifest equality, unchanged supplied brief, empty staged diff and absence of forbidden tracked artifacts. Pre-existing broken links are distinguished from new ones; web links are not fetched. A full tracked-plus-untracked text patch is exported without staging.

No scientific confidence or publication status is promoted by these checks. The no-active-outpost classifications remain PROVISIONAL and the residual-state exclusion category is unused. Runtime/old-to-new migration, planet-ID resolution, frame/units and authoritative restore are untested.

## Complete change inventory

New authored files:

- [Report](../historical-save-inventory-triage.md), this validation record.
- [Durable-safe per-file manifest](inventory.json), [presence matrix](presence-matrix.csv), [version ledger](versions.csv), [location candidates](location-candidates.csv).
- [Inventory helper](../../../save-analysis/scripts/inventory_historical_saves.py), [location helper](../../../save-analysis/scripts/probe_inventory_locations.py), [ten synthetic tests](../../../save-analysis/scripts/test_historical_inventory.py).

Pre-existing untracked input: [supplied brief](../../implementation-briefs/README.md#archive-lookup) (`implementation-briefs.zip :: docs/implementation-briefs/CODEX_RESEARCH_BRIEF_historical_save_inventory_triage.md`), byte-preserved and included in the complete review diff.

Modified existing files: README.md, CREDITS.md; docs/DECISIONS.md, EVIDENCE_STANDARD.md, PROVENANCE.md, RESEARCH_STATE.md, SOURCES.md, known-facts.md, hypotheses.md, state-register.md, subsystems/initial-map.md, experiments/README.md, experiments/evidence/README.md, implementation-briefs/README.md; save-analysis/scripts/README.md. The methodology addition is narrow; prior experiment reports are unchanged. No unrelated source file changes are intended.

Durable records: SOR-EXP-0007, SOR-EV-0013, SOR-F-0013, SOR-D-0023; dated follow-ups to existing location/relationship hypotheses/state. No new controlled sample, environment, function/interface or safe integration claim is created. No new third-party permission issue; existing installed-tool/source credit applies. No upstream contact, staging, commit, push or publication.

## Local receipts and reproduction

`.local-work/historical-inventory/scan-01` through `scan-04` retain per-file flushed progress and input/tool provenance; partial/exploratory results are not erased. Final `scan-04/inventory.json` is the exact-path/metadata/fingerprint catalog. Initial copy/control/baseline/documentation receipts remain in `scan-03/shortlist-archives.json`, `controls.json`, `baseline-check.json` and `documentation-before.json`; final review independently rechecks them. `scan-04/location-final.json` holds the final separate location extraction. Intermediate location diagnostics remain in scan-03 and are not authoritative inventory revisions.

`.local-work/historical-inventory/review/` retains independent checks, exact final tool/file identities, commands/results, preservation audit, selected-summary checks, local-link audit, Git status, file inventory and **review.diff including every new text file and the unchanged supplied brief**. These are local review artifacts, not publication-cleared evidence. Inline one-off archive/summary authoring commands are described by their receipts; the reusable analysis methods are the committed-path helpers above.

From the repository root with the already installed Python (no dependency install):

```text
python -B save-analysis/scripts/inventory_historical_saves.py --run <fresh-name>
python -B save-analysis/scripts/probe_inventory_locations.py --run <completed-run> --ids <one-to-five-HIST-IDs> --output <fresh-name>.json
python -B -m unittest discover -s save-analysis/scripts -p test_historical_inventory.py -v
python -B -m unittest discover -s save-analysis/scripts -p test_mature_outposts.py -v
```

New inventories assign IDs by their own frozen ordered input set; use hashes to resolve correspondence. Do not overwrite completed runs or assume ID continuity after files are added/removed. `--resume` is for an incomplete same-input run and preserves existing receipts. No live action follows these commands.

Suggested commit after review only: `research: inventory historical saves and triage outpost location evidence`.
