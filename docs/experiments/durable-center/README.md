# SOR-EV-0026 — Durable-center review package

2026-10-10, Australia/Sydney. [SOR-EXP-0018 report](../durable-outpost-center-and-object-transforms.md), [authorized brief](../../implementation-briefs/README.md#archive-lookup) (`implementation-briefs.zip :: docs/implementation-briefs/CODEX_BRIEF_SOR_durable_outpost_center_object_transforms.md`). Critical review required; authored tables/text REVIEW-REQUIRED. Raw saves/captures/native exports/databases remain LOCAL-ONLY and excluded from this package.

Best-supported answer: Save25/26 preserve the compensated local workshop center exactly. The controlled loaded terrain origin is directly recovered from nine existing captures. Ordinary objects carry their own case 5 transforms; conditional overlay rebasing and continuous geographic embedding remain distinct unresolved stages. All 19 mature Workshop compensations are now decoded and zero, retaining the negative-X/frame counterexample. No complete geographic solution or universally aligned workshop-relative object API is claimed.

## Selected authored evidence

| File | Contents / limit |
|---|---|
| [invariance.csv](invariance.csv) | Four exact Save25/26 rows; raw/compensated XYZ, identity correspondence, site angles, offsets, two explicitly unqualified continuous hypotheses. |
| [terrain-captures.csv](terrain-captures.csv) | Nine hash-checked terrain origins/resolutions from existing raw captures; no new live acquisition. |
| [object-transforms.csv](object-transforms.csv) | S3/S6/S7/L2C and six selected mature examples; conditional rotation fields and frame-qualified versus unqualified subtraction. |
| [projection.csv](projection.csv) | Forty-one site/fixed-point rows; repeated controls counted separately, no independent continuous truth. |
| [controls.csv](controls.csv) | Seven manual no-action comparisons, exact selected XYZ/rotation equality. |
| [decoded-inputs.csv](decoded-inputs.csv) | Twenty-three decoded hash/size/count receipts; no character filenames or raw save data. |
| [native-exports.csv](native-exports.csv) | Seven fresh export identities, function inventory, caps, log hashes and retained partial failure. Full native text remains local. |

These CSVs are original authored selections from local numeric receipts, serialized as UTF-8/LF. They are not copied raw evidence or cleared for publication. Byte-integrity checks do not prove interpretations. No evidence confidence automatically satisfies scientific/rights/publication review.

## Reproduction

Run from repository root using the installed runtime (the WindowsApps `python` alias failed to start; no installation was attempted). Each output name must be fresh. Existing archive paths and hashes are resolved from frozen project manifests, which must be present; the probe is a research utility, not a portable production parser.

```powershell
& 'C:/Users/User/AppData/Local/Python/pythoncore-3.14-64/python.exe' -B save-analysis/scripts/research_durable_center.py --run NEW-RUN
& 'C:/Users/User/AppData/Local/Python/pythoncore-3.14-64/python.exe' -B save-analysis/scripts/research_workshop_origin.py --run NEW-CAPTURE-CHECK
& 'C:/Users/User/AppData/Local/Python/pythoncore-3.14-64/python.exe' -B save-analysis/scripts/audit_durable_center.py --receipts .local-work/durable-center/NEW-RUN/results.json --captures .local-work/workshop-origin/NEW-CAPTURE-CHECK/captures.json --fixed docs/experiments/planetary-surface-anchor/fixed-anchors.csv --session .local-work/beacon-observer-live/session-17596-91165828 --output .local-work/durable-center/NEW-AUDIT
& 'C:/Users/User/AppData/Local/Python/pythoncore-3.14-64/python.exe' -B -m unittest discover -s save-analysis/scripts -p 'test_*.py'
```

Actual final receipts: `.local-work/durable-center/final-06/`; numerical audit `.local-work/durable-center/audit-final-04/`; fresh nine-capture/hash/save check `.local-work/workshop-origin/durable-verify-01/`; definition/PE check `.local-work/durable-center/definitions-and-rotation.json`. Earlier run folders are preserved development receipts, not the final evidence authority. Initial probes lacked some control/cross-outpost extraction or the nonempty resource reader; later runs extended those specific branches.

Native exports used existing `ghidra/scripts/Invoke-OutpostRecon.ps1 -Target Starfield -OutputName durable-center-NN.tsv -Addresses @(...)`, retaining exact command arguments in Ghidra logs. No script/database analysis writes. Export 06 retained a failed instruction-window request after successfully exporting 1402cedd0; export 07 uses existing confirmed instruction addresses for follow-up windows. No claim depends on the failed window or missing tail. Full decompilation/listing limits are disclosed in the report and CSV. The first database baseline followed the start of export 01, so a pure before-first-tool receipt is unavailable; final preservation also checks all 17 prior EXP0017 file hashes. Four Ghidra index files changed filesystem timestamps; bytes/sizes remain identical. This metadata churn is explicitly retained in the final verification receipt and is not an analysis-content mutation. No metadata restoration was attempted.

The primary probe reads exact protected copies, the ESM catalog/ESM, frozen manifests and manual identity ledger; it writes only a new ignored directory and cleaned decoder scratch. Original stdlib functions `initial_transform`, `resource_rows`, `compensated` and `model_candidates` are source-informed by the pinned native code and reuse project framing/math. The audit reads receipts/fixed CSV and optional existing raw terrain sections; it writes new numerical tables/summary only. A separately supplied resource callback extends `workshop_prefix`; default nonempty rejection is preserved for prior callers. No dependency download, target/native invocation, database edit or save rewrite occurs. C:/D: 40,000,000,000-byte floor is enforced by the existing guards.

## Actual checks and limits

Final verification and full file list are in `.local-work/durable-center/review-final/verification.json`; full tracked/untracked-inclusive patch `.local-work/durable-center/review-final/complete.diff`; `git status --short` snapshot and changed-file manifest alongside it. Review artifacts are ignored and remain local.

The complete Python suite passes **91 tests**, including eight new tests covering float32 cancellation, invalid vectors, negative grid boundaries, phase ambiguity, rotation truncation and independent resource/reference queues. Corpus audits pass 23 decodes, 128 selected prefixes, seven action/control comparisons, two center correspondences with zero bit error, 19 mature zero compensations, 18 captured beacon observations and nine terrain snapshots. The discrete chart audit has 41 rows and maximum longitude/latitude errors `8.881784197001252e-16` / `3.3306690738754696e-16` radians. These are selected numerical/parser checks, not exact continuous geographical validation or all-object membership tests.

Final checks include changed-document links and UTF-8/LF, `git diff --check`, protected-input hashes, database/executable/ESM preservation, ignored scratch, no raw save/dump/database deliverables, unchanged HEAD/index and no staged changes. Only authored numeric CSV/Markdown/Python files are in the change set, including the unchanged supplied brief. Details and count of protected artifacts actually rechecked belong to the verification receipt.

Review blockers for a **complete geographic claim**: unqualified continuous residual consumer/phase; general selected overlay map not reconstructed from archives; zero-compensation mature counterexample; absence of retained same-base ordinary objects in Save25/26. These do not erase exact local invariance or case 5 transform findings. Proposed acquisitions remain separately unauthorized. No staging, commit, push, fork, PR, upstream communication or publication occurred.

Suggested commit after review:

```text
research: investigate durable outpost center and object transforms
```
