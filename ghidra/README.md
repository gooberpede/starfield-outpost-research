# Static-Analysis Workspace

No Ghidra project or executable baseline is selected or included. Keep imported game binaries, Ghidra projects/repositories, and analysis databases in a designated external or ignored local workspace.

Future reusable project-authored scripts belong in [scripts/](scripts/README.md). Default work reads/exports existing analysis state. Changing bytes, function boundaries, names, types, labels, symbols, comments, or analysis configuration must be explicitly authorized and disclosed; do not silently reuse a sibling project's analysis state as this project's baseline.

Record actual executable hash, image base, language/compiler ID, Ghidra/tool versions, script commit, options, exact address ranges, and output hashes in the experiment. Static evidence may guide runtime/save questions but does not prove a selected object executed the path live.

Generated bulk output goes to ignored `exports/` or `.local-work/`; selected evidence requires review before inclusion. Third-party scripts and decompiled output are governed by [the policy](../THIRD_PARTY_POLICY.md) and [evidence standard](../docs/EVIDENCE_STANDARD.md).


## Active identification read-only exports (SOR-EXP-0009)

`scripts/Invoke-OutpostRecon.ps1` accepts `-Reader OutpostSaveConstants.java` for bounded existing-instruction searches of promotion constants and selected Almanac member offsets. It scans only stated static ranges, caps matches at 3,000 and records cancellation/limit; no exhaustive claim follows. `OutpostRecon.java` also accepts `full:STATIC-ADDRESS`, raising only the decompiled-text cap from 50,000 to 250,000 characters for a specifically requested function; its 600-instruction cap and existing decompiler timeout remain. `win:`/`ref:` continue to export bounded existing instruction/xref views. All modes require the existing pinned Ghidra project/JDK, run `-readOnly -noanalysis`, read existing state only, and write fresh ignored exports plus local settings/cache/logs. No game process, analysis, bytes, symbols, types or comments are changed. Full executable text stays LOCAL-ONLY. [Research and preservation limits](../docs/experiments/active-outpost-identification.md).
