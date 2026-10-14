# SOR-EV-0019 — Surface-anchor evidence and review package

2026-10-09, Australia/Sydney. [Answer-first report](../planetary-surface-anchor-semantics.md), SOR-EXP-0013 / SOR-F-0018 / SOR-ST-0019 follow-up / SOR-D-0030. **REVIEW-REQUIRED**, critical review pending. Original source payloads/native exports remain LOCAL-ONLY. Neither scientific confidence nor this index grants publication/integration permission.

## Selected authored evidence

- [matrix.csv](matrix.csv): 21 saved observations, six sample labels (Save3 is an explicit zero control in the sample ledger), 18 bodies. Pair/parent offsets are decoded logical save-stream offsets. Parent/self tokens are tagged serialized IDs, not loaded FF FormIDs or pointers. Numerical degrees/directions are derived site-anchor views, not exact beacon geography.
- [fixed-anchors.csv](fixed-anchors.csv): three installed PNDT/WRLD anchors. `record_file_offset` locates the compressed original ESM record header; `pair_record_decoded_offset` locates the first disk double in its decoded payload, excluding the 24-byte header. Disk order is latitude,longitude; CSV semantic columns are longitude,latitude. No false file offset is assigned inside compressed payloads.
- [samples.csv](samples.csv): original and decoded SHA-256, observed header versions, recognized beacon/pair counts. Source/archive locators and full pre/post receipts are private local data. Save2=HIST-0245; Save52=HIST-0267.
- [native-exports.csv](native-exports.csv): 15 local export names/hashes/sizes, function locators and cap markers. These identify evidence; no proprietary instruction/decompilation payload is incorporated. Preferred base is `0x140000000`, matching pinned executable SHA-256 `7e9adb1414a8e1b325e5e1f097b9b17b78deb7eebeda37a333351a43a60f9d28`.
- [local-artifacts.csv](local-artifacts.csv): exact identities of key ignored numerical/preservation/tool/component-probe receipts. Files are not redistributed by this index.
- [Prior-art and secondary leads](prior-art-and-leads.md): original URLs, authors, dates, version/access/permission limits and independent-confirmation boundaries. SOR-S-0129/0130; [credits](../../../CREDITS.md).

The native string scan ends `SCAN_END cancelled=false`, within the retained selection/limits. Explicit queries still have finite xref and 600-instruction bounds. `surface-flow-08.tsv` caps the large loader decompilation; `surface-bridge-09.tsv` repeats that loader with existing `full:` allowance and no decompilation cap, while its instruction listing remains capped. Placement-12/save-11/UI-02/other indicated instruction caps remain visible. Bounded absence is not global absence. RTTI probing printed neighboring words beyond some vtables; only validated needed entries were used. `140756700` lacked a defined function; no disassembly was created. No Ghidra symbols/types/comments were changed.

## Reproduction and prerequisites

Use the existing frozen EXP0012 manifests/catalog and authorized local archives/installed content, not the numeric ledger as input. Actual interpreter: `C:/Users/User/AppData/Local/Python/pythoncore-3.14-64/python.exe`, CPython 3.14.3, standard library only. Existing read-only Ghidra project, Ghidra 12.1.2/JDK 21 and wrapper paths are required for static exports; no download/install/analysis regeneration is implicit.

```powershell
& C:/Users/User/AppData/Local/Python/pythoncore-3.14-64/python.exe -B save-analysis/scripts/research_surface_anchors.py --run <fresh-name> --frozen .local-work/save-capacity-location/body-final-03/save-derived.json --catalog .local-work/save-capacity-location/esm-index-verified.json
& C:/Users/User/AppData/Local/Python/pythoncore-3.14-64/python.exe -B -m unittest discover -s save-analysis/scripts -p 'test_*.py'
& ghidra/scripts/Invoke-OutpostRecon.ps1 -Target Starfield -OutputName <fresh>.tsv -Addresses '141686a00','140ad0650','140ad55b0','140771ac0','140777560','full:14076ec00'
```

Native wrapper accepts a simple filename; replace `<fresh>.tsv` with a valid unused filename. Full 15 export batches are identified by function lists in the CSV; reproduce only the relevant bounded batch, not a blind bulk scan. Hash source inputs and the analysis-project file inventory before/after. The runner exclusively creates its ignored output directory; refuses source/decoded hash mismatch or ambiguity; preserves originals; and removes only decoder-created scratch. C:/D: free space must stay ≥40,000,000,000 bytes. Numerical tests check analytic consistency, not actual geography or runtime authority.

## Actual checks and limits

- **72 offline tests passed**, including three new synthetic methods; actual output `.local-work/surface-anchor/tests.txt`. Existing parser/default-ESM behavior regressions remain covered. No live/second-parser/native-invocation tests were run.
- **numeric-04** succeeded on final source code after numeric-01's retained wrong-queue-offset failure and numeric-02/03 corrections/checks. All six original/archive identities matched frozen manifests, all decoded hashes matched EXP0012, and originals/archives/catalog/ESM/manifests matched pre/post. Final result equals numeric-03 exactly. All 21 pair rereads and three fixed selections pass; Kreet and New Atlantis bit equality asserted. Maximum analytical round-trip error 1.1102230246251565e-16 radians; no metric accuracy claim.
- Fresh A0/A0C hashes and nested XYZ values match earlier observer evidence; their distance to S1 is 6.830538561399593 in unassigned units. `.local-work/surface-anchor/a0-verification.json` records this comparison; source snapshots remain non-atomic/earlier-session.
- All **15 Ghidra database files** agree by path/SHA-256 in normalized before/after inventories. No code/data analysis was run. Fifteen exports' PROGRAM/SHA256/BASE metadata matches the pinned import. Console review found no ERROR/Exception/script-failure markers; caps/failed-address limitations remain separate.
- Installed executable/ESM final hashes match baseline. Initial free bytes C89,262,084,096 / D140,389,752,832; final recorded guard check C89,804,247,040 / D140,387,905,536. These are observations, not an allocation attribution or guarantee about unrelated processes.
- Final whitespace, **399 internal links/anchors**, inventory, staged-state and full-diff checks passed and are recorded in `.local-work/surface-anchor/review/checks.json`. No missing internal target/anchor was found. Git status contains **19 modified tracked files, 10 new task files and the one pre-existing supplied brief** (directory entries expand in the inventory). The index remains empty, HEAD remains `ef35d080951f976a91cfbadd3fa71219ec1db1d2`; `.local-work` evidence is ignored. No raw payload is in the new tracked-candidate set. Only authored Markdown/CSV/Python and the Java filter edit are proposed for review.

## Complete change inventory and diffs

New task files: `docs/experiments/planetary-surface-anchor-semantics.md`; this directory's README, prior-art register, matrix, fixed-anchor/sample/native-export/local-artifact CSVs; `save-analysis/scripts/research_surface_anchors.py`; `save-analysis/scripts/test_surface_anchors.py`.

Changed existing files: root README/CREDITS; docs DECISIONS/PERMISSIONS/PROVENANCE/RESEARCH_STATE/SOURCES; experiment/evidence/implementation-brief indexes; function/hypothesis/finding/state registers; subsystem initial map; Ghidra reader/README; save-analysis ESM reader/README. Existing ESM reader default remains last-field dict; `repeated=True` adds an ordered list. Ghidra `surface` adds vocabulary filtering with existing bounds. No frozen earlier evidence is edited.

Pre-existing user file: `docs/implementation-briefs/CODEX_BRIEF_SOR_planetary_surface_anchor_semantics.md`, retained unchanged and included separately in the complete review diff.

Local, unstaged review artifacts (native Git patch bytes, including untracked files):

- [Task-only full diff](../../../.local-work/surface-anchor/review/task-only.diff)
- [Complete full diff including supplied brief](../../../.local-work/surface-anchor/review/complete.diff)
- [Exact review file/hash inventory](../../../.local-work/surface-anchor/review/inventory.json)
- [Check receipt and Git status](../../../.local-work/surface-anchor/review/checks.json)

No Git index changes were used to produce these exports. Review exports remain ignored, are not publication artifacts and cannot prove their own semantic correctness. Await critical review of interpretation, byte association, permissions/privacy and scope. Generic wire serializer closure, geographic calibration and exact beacon transformation remain concrete obligations, without cancelling the supported scoped site-anchor result.

Suggested later commit, **not performed**:

```text
research: investigate planetary surface-anchor coordinate semantics
```
