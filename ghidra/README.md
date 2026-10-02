# Static-Analysis Workspace

No Ghidra project or executable baseline is selected or included. Keep imported game binaries, Ghidra projects/repositories, and analysis databases in a designated external or ignored local workspace.

Future reusable project-authored scripts belong in [scripts/](scripts/README.md). Default work reads/exports existing analysis state. Changing bytes, function boundaries, names, types, labels, symbols, comments, or analysis configuration must be explicitly authorized and disclosed; do not silently reuse a sibling project's analysis state as this project's baseline.

Record actual executable hash, image base, language/compiler ID, Ghidra/tool versions, script commit, options, exact address ranges, and output hashes in the experiment. Static evidence may guide runtime/save questions but does not prove a selected object executed the path live.

Generated bulk output goes to ignored `exports/` or `.local-work/`; selected evidence requires review before inclusion. Third-party scripts and decompiled output are governed by [the policy](../THIRD_PARTY_POLICY.md) and [evidence standard](../docs/EVIDENCE_STANDARD.md).
