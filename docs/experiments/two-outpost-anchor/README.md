# SOR-EV-0020 — Two-outpost anchor evidence and review package

2026-10-09, Australia/Sydney. [Answer-first report](../two-outpost-site-anchors-and-beacon-coordinates.md), SOR-EXP-0014 / SOR-F-0019 / SOR-SAMPLE-0030. Authored content REVIEW-REQUIRED; raw saves, private JSON, full extraction, ESM payloads and proprietary native exports LOCAL-ONLY. Return for critical review; no integration/publication authorization.

## Selected evidence

- [manifest.csv](manifest.csv): Save25 source, protected copy and decoded identities; full paths/timestamps in ignored `extract-04/manifest.json`. Hashes establish identity, not coordinate semantics.
- [beacons.csv](beacons.csv): both Save25 beacons plus S1/S1C/L2C, exact pair/XYZ bytes and decoded logical offsets, conditional type, name queues, saved flags and **all** cache hits including the conflicting SOR-003 window. Blank explicit type means inherited/conditional, not missing record bounds. Token equality is scoped to one save.
- [comparisons.json](comparisons.json): exact parent/pair/body comparisons and derived local displacements/angular separations. Distances have unassigned units; no geographic/metric calibration or precise beacon coordinate.
- [native-exports.csv](native-exports.csv): four selected export identities/function lists. Preferred static base `0x140000000`; pinned executable in the report. Export payloads remain ignored. Exact xref targets and original instruction addresses stay local, not substituted for save offsets.

## Reproduction and script effects

Existing CPython 3.14.3 and standard library only, plus project-owned readers at starting HEAD `162ffba899d71bb64877d86069e0a749c16cfe0f`. No new dependencies or outside code. Original provenance remains SOR-S-0113/0124/0127/0128 and Ghidra/JDK SOR-S-0105. Existing prior-art credit/permissions are retained by reference; no new web consultation.

`research_two_outpost_anchors.py` reads an explicitly supplied live source **only to copy/hash**, then decodes exclusively created ignored copies. It reads frozen EXP0012 manifests, available original-control identities, immutable archives, the installed ESM/executable and existing private network JSON. It writes exclusive `.local-work/two-outpost-anchor/RUN` receipts and `.local-work/savegames/two-outpost-anchor/RUN` archive. Missing historical live originals are recorded; missing/mismatched archive inputs abort. Names/network fields are comparison-only after save-derived extraction. The mapped decoder has bounded per-stream buffers, exact integrity/length checks and a 40,000,000,000-byte free-space guard on C/D; no arbitrary aggregate decoded-size ceiling. Scratch is temporary and removed by the decoder. No target/database/Git/network effects.

`analyze_two_outpost_anchors.py` reads those results and exclusively creates selected authored `beacons.csv`/`comparisons.json` in an explicit output directory. It computes spherical direction separation and local differences; no radius, compass or tangent transform is inferred. Neither utility is an importer, save editor or production tool. Header/private/whole-record receipts remain local; only selected authored evidence is proposed for review.

```powershell
& C:/Users/User/AppData/Local/Python/pythoncore-3.14-64/python.exe -B save-analysis/scripts/research_two_outpost_anchors.py --run FRESH --source <exact-Save25-path-from-brief> --catalog .local-work/save-capacity-location/esm-index-verified.json --frozen .local-work/save-capacity-location/body-final-03/save-derived.json
& C:/Users/User/AppData/Local/Python/pythoncore-3.14-64/python.exe -B save-analysis/scripts/analyze_two_outpost_anchors.py --results .local-work/two-outpost-anchor/FRESH/results.json --output <fresh-selected-output-directory>
& C:/Users/User/AppData/Local/Python/pythoncore-3.14-64/python.exe -B -m unittest discover -s save-analysis/scripts -p 'test_*.py'
```

Ghidra uses existing `ghidra/scripts/Invoke-OutpostRecon.ps1 -Target Starfield -OutputName FRESH.tsv -Addresses ...` with readOnly/noanalysis. Four actual address lists are recorded in the CSV and corresponding ignored `.tsv.log`; batches 2–4 additionally request xrefs to `140ad3b20`, `140ad0650/1407be0e0` and `14077fc20` respectively. No project analysis/symbol/type/comment write. The pre/post database inventory covers all 15 files.

## Actual checks and limits

- Final **extract-04** completes seven samples; all available originals, all archives, catalog, frozen manifest, private network JSON, ESM and executable match pre/post. S1/S1C/L2C original live paths are absent, explicitly recorded in `unavailable-control-originals.json`; their archives match frozen identities/decoded hashes. Save25 copies from earlier retained runs also remain local.
- Fresh raw byte audit independently checks both queued parent/base/self triples, flag words, name lengths/text, local XYZ, direct PNDT and repeated-parent/pair bytes. A separate arithmetic envelope walker confirms **25,976** records and exact R3 closure without using `iter_records`. These checks do not constitute an independent full semantic parser.
- Save3 zero, S1/S1C/L2C one each, Save52 19 ordinary candidates. Fresh post-extraction JSON comparison: **17/17 body/system matches**. Fresh Save2/installed New Atlantis pair bit equality after disk-order swap. Two Save25 body-associated pairs differ; earlier Kreet/SOR-002 equality remains exact.
- **72 offline tests passed** (existing suite, 0.314 s). Numerical/structural tests and direct file rereads provide no runtime/load-authority validation. No new synthetic test claims a guessed planetary transform.
- **15/15 analysis database files unchanged** by path/SHA-256. All four native exports match pinned import metadata, decompile successfully and contain no cap markers. The export logs show read-only processing; selected branches were inspected, never executed.
- `.local-work/two-outpost-anchor/validation.json` records these checks and four PE constants with exact original file offsets. The local validation/probe scripts are retained for audit; their hashes appear in the local artifact index. Original/executable hashes match the pinned baseline; free-space guard passes.
- Final review receipts list whitespace, authored UTF-8/LF, internal-link checks, staged-state/HEAD checks and the entire changed/new file inventory. No raw payload is proposed for tracking. The supplied brief retains private filenames and needs publication review independently of the authored scientific result.

## Complete file inventory and diffs

New task files: the report; this README; manifest/beacon/native-export CSVs; comparisons JSON; `save-analysis/scripts/research_two_outpost_anchors.py`; `save-analysis/scripts/analyze_two_outpost_anchors.py`.

Updated existing files: root README/CREDITS; docs RESEARCH_STATE/DECISIONS/PROVENANCE/SOURCES; known-facts/state-register/function-register; subsystem initial-map; experiment/evidence/implementation-brief indexes; save-analysis README. Prior evidence, resolver implementation and historical findings are preserved. Pre-existing supplied brief is retained unchanged and separately identified in review inventory.

Local review artifacts, produced without staging:

- [Task-only full diff](../../../.local-work/two-outpost-anchor/review/task-only.diff)
- [Complete full diff, including supplied brief](../../../.local-work/two-outpost-anchor/review/complete.diff)
- [Exact file/hash inventory](../../../.local-work/two-outpost-anchor/review/inventory.json)
- [Review checks and git status](../../../.local-work/two-outpost-anchor/review/checks.json)
- [Local evidence/tool artifact identities](../../../.local-work/two-outpost-anchor/local-artifacts.json)

Await critical review of the distinct-anchor conclusion, retained cache ambiguity, native grid/residual interpretation, frame/coverage limits, provenance and publication eligibility. Suggested later commit: `research: compare two-outpost site anchors and bound beacon coordinates`. No staging, commit or push was performed.
