# Reproduction, comparisons and limits

2026-10-24, Australia/Sydney. Existing CPython 3.14 executable is `C:/Users/User/AppData/Local/Python/pythoncore-3.14-64/python.exe`; the WindowsApps `python` alias failed to start. No package or dependency was installed. All authored methods are GPL-3.0-or-later; owned-method provenance is in [sources.csv](sources.csv). Native exports, installed corpora, geometry and save inputs remain local-only.

## Actual commands and effects

From repository root, `python` below denotes that explicit interpreter. Every output is exclusive and ignored. Use fresh output names for reproduction; never reuse a frozen destination.

```text
python -B research/resource-owner-root/audit.py before
python -B -m unittest discover -s research/resource-owner-root -v
python -B research/resource-owner-root/freeze.py --output .local-work/resource-owner-root/freeze01
python -B research/resource-owner-root/validate.py --freeze .local-work/resource-owner-root/freeze01 --output .local-work/resource-owner-root/validation01
python -B research/resource-owner-root/receipt_check.py --validation .local-work/resource-owner-root/validation01 --output .local-work/resource-owner-root/source-bound02.json
python -B research/resource-owner-root/audit.py after
python -B research/resource-owner-root/provenance.py --label checks02
python -B research/editorial/screen.py --changed
python -B research/resource-owner-root/package.py --label review01
```

After independent REWORK, the additional executed correction commands were:

```text
python -B research/resource-owner-root/layout_validate.py --output .local-work/resource-owner-root/source-layout01
python -B research/resource-owner-root/validate.py --freeze .local-work/resource-owner-root/freeze01 --corpus .local-work/resource-owner-root/source-layout01/D3/normalized.json --geometry-only --output .local-work/resource-owner-root/validation-layout01
python -B research/resource-owner-root/receipt_check.py --validation .local-work/resource-owner-root/validation-layout01 --output .local-work/resource-owner-root/source-bound-layout01.json
python -B research/resource-owner-root/audit.py after --label final
python -B research/resource-owner-root/provenance.py --label checks03
python -B research/resource-owner-root/package.py --label review03
```

The new read-only exports use the same wrapper with these fresh output names:
`d4c-patternloaderrefs01` (`sym:SurfacePattern`, `sym:SurfacePatternForm`, `ref:14096be70`);
`d4c-patternvtable01` (`data:144b67068:40`, `14096be70`);
`d4c-patternloader01` (`14096bf00`, `14096d1f0`, `14096eb90`);
and `d4c-patterninstall01` (`14096bae0`). The first symbol queries return no matching class names; the existing surface-symbol export identifies `BGSSurface::Pattern` for the vtable follow-up. No analysis content is edited.

`audit.py` hashes prior D1/D2/D3/D4A/D4B artifacts without interpreting answers, applies unchanged owned save protection, checks game absence/free space and compares HEAD/index identity. Its initial inventory has 11485 immutable paths. The audit reads the prior D4B pin manifest and full installed EXE/ESM/PlanetData hashes. No original is overwritten. Final results and hashes are in the local handoff package.

`owner_map.py` is a pure logical evaluator with no I/O. Eleven logical-map tests and three later SFPT-layout tests use authored expected transitions, not game fixtures. `provenance.py` also reruns the 31 existing standalone tests, retains logs and verifies the frozen trace against the final evaluator. `freeze.py` freshly reads pinned installed definitions, reuses the owned planetary selection model and writes eight conditional components, full transition trace, candidate sequence and input/output hashes. It does not read native call/geometry answers. It assumes successful map storage and an unvalidated family-to-slot projection; it is not the portable production predictor.

`validate.py` first writes fresh conditional geometry using the frozen two-resource hypothesis, installed selected-root DNAM and unchanged D3 point/key/bound/competition arithmetic. It then opens primary answers and writes sequence/shape comparisons. Its `all_three_exact` field means shape-byte equality only; the stricter `source-bound02.json` qualifies source identity separately and overrides any broader reading of that field. `receipt_check.py` independently decodes original framed receipts/ACKs for four calls and three accepted paths and compares actual source identities. It reads native data only after prediction persistence. Inference on the unchanged frozen D2/D3 and D1 bundles uses the inherited audit-hook isolation, with eight deliberate denied probes and no forbidden inference reads.

Read-only Ghidra commands use the existing owned wrapper:

```text
research/workshop-population/export.ps1 -OutputName d4c-range01 -Addresses @('1405f7a80','1403a4250','1407bc300','1405ed1b0','1422cc0d0')
research/workshop-population/export.ps1 -OutputName d4c-writers01 -Addresses @('140773180','140773be0','14077d090','ref:140773180','ref:140773be0','data:1461dfa48:2')
research/workshop-population/export.ps1 -OutputName d4c-initialization01 -Addresses @('14076ec00','142340ab0','140777290')
research/workshop-population/export.ps1 -OutputName d4c-producerrefs01 -Addresses @('ref:142340ab0','14076e720','140774e00','ref:1407bc3d0')
research/workshop-population/export.ps1 -OutputName d4c-selection01 -Addresses @('142339b20','ref:142340ab0','ref:142339b20')
research/workshop-population/export.ps1 -OutputName d4c-orchestrator01 -Addresses @('142340990','ref:1461dfa4c')
research/workshop-population/export.ps1 -OutputName d4c-buildcomponents01 -Addresses @('14233f2c0')
research/workshop-population/export.ps1 -OutputName d4c-rootwriters01 -Addresses @('ref:14076e810','ref:14076e720','ref:142340990','142322520')
research/workshop-population/export.ps1 -OutputName d4c-alternates01 -Addresses @('14079c5e0','1407766b0','142324970')
```

These run existing Ghidra 12.1.2/JDK 21 with `-readOnly -noanalysis`, read the pinned existing project and write new local exports/cache/logs. Logs and completed `END` markers are pinned. An additional `d4c-creationrefs01` attempted `ref:142340990`, nonexistent function entry `14076e6a0`, then `140774e00`. It failed at the nonexistent entry; its partial export/error log is preserved, and a successful separate export supplies the latter function. The wrapper returned zero despite the script error, so exit code alone is not accepted as export success.

## Comparisons

| Required dimension | Result |
|---|---|
| Complete ordered Archimedes candidates | FAIL for the frozen hypothesis: [Tungsten, Chlorine] versus [Water, Water, Tungsten, Chlorine]. No native-equivalent complete prediction claimed. |
| Tungsten 2881 | Exact IRES `0x000057c4`, source `0:27156:35988:0028be0d`, ordered binary32 XYZW and 16-byte native sphere bound; one matching path. |
| Chlorine 2941 | Exact IRES `0x000057d5`, same source, ordered XYZW and sphere bound; one matching path. |
| Chlorine 829, original hypothesis | Exact IRES/shape bytes, one match, but native source SFBK `0x002c17d3` differs from predicted `0x002c17d5` at (27168,35988). Initial strict source-and-geometry FAIL is preserved. [SFPT installation correction](source-layout.md) subsequently resolves the source identity without fitting; the versioned three-control source/shape comparison passes. |
| Seven Feynman/Carinae controls | Independently rerun through inherited verifier in both D1 corpus representations; final receipt supplies exact results. No new owner-root production model is being validated by these controls. |
| Save52 D2/D3 frozen roster | 17 requests each, 34 semantic-equality comparisons; all original 19 cases retained, including two disabled cases. No case or contradiction dropped. |
| Corpus cost | Incremental retained production corpus: 0 bytes. Frozen D2 normalized corpus remains 735952 bytes; frozen D3 remains 738975 bytes. Diagnostic inputs/trace are local-only and are not a proposed minimized corpus. |

D2's 16 corroborated ordinary pairs, one potential false negative and 18 indeterminate pairs remain historical. D3's 25 corroborated ordinary pairs, one potential false negative and nine indeterminate pairs likewise remain historical; four Water associations are assessed separately. The [D2](../resource-save52/report.md) and [D3](../resource-save52-d3/report.md) reports retain every case/association row. The new roster hashes verify unchanged responses, including unsupported/mixed-mask/alternate-descriptor states. Zero positive classifications, indeterminate classifications or contradictions are changed by D4C. Missing extractor equipment is never resource absence.

The later [source-layout diagnostic](source-layout.md) reruns all 17 active D3 requests with corrected preparation. All 46 association rows retain classifications; six cases change path counts and none changes resource-availability status. All seven native resource/shape/callback controls still match in both corrected representations. Original D2/D3 outputs are preserved and unchanged.

The native bound comparison covers center XYZ and radius, the first 16 bytes of the region header. It does not compare allocation pointers or the complete native region header. Source identity, ordered path equality, candidate completeness, callback acceptance, visible patch count and historical generating epoch are separate dimensions.

## Preserved failures and finalization

The inaccessible Python alias, failed partial Ghidra export, complete-list mismatch and initial strict source assertion are retained as failures. The last assertion exposed the source FormID mismatch at 829; `source-bound02.json` reports it explicitly rather than relaxing an exact-source claim. Independent REWORK then required the available offline table-route diagnosis; the [versioned correction](source-layout.md) resolves the missing native installation transpose and `source-bound-layout01.json` verifies all three source/shape matches. The correction implements the general native serialization rule. It does not replace a table entry with the observed source ID, alter geometry arithmetic or fit a frame, chance, seed or family.

A final fresh IRES EDID read also corrected four human-readable resource names in the trace table. The checked FormIDs and every numeric prediction were already unchanged. `label-check01.json` retains the installed identity and exact name mapping; the corrected review snapshot supersedes the initial one.

After the input freeze, a general evaluator guard was added for an unresolved root: native root-resolution failure must stop before supplemental resolution. The exact freeze-time `owner_map.py` bytes remain at `freeze01/owner_map-at-freeze.py`, with their original method hash in the freeze. Rechecking the final evaluator against all frozen component rows yields the same trace and two-resource candidate output. The added synthetic test covers the previously untested invalid-root domain; it does not alter the frozen prediction.

The [review record](review.md) retains final editorial/manual coverage, exact scientific disposition and patch handoff. No live run, retail teardown test, save mutation, analysis-content edit, staging, commit, push, external disclosure or publication was performed. The prospective card remains unexecuted.
