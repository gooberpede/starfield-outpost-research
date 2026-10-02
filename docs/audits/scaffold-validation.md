# Scaffold Validation

**Date:** 2026-10-01.

**Scope:** Delivered initial scaffold only, not Starfield research or public-release readiness.

**Result:** Scaffold hygiene checks passed; research baseline remains unestablished.

## Checks performed

- Every delivered file decodes as strict UTF-8, has no BOM or CRLF, and has a final newline. The GPL file was not rewritten or normalized.
- Internal Markdown file links were resolved against the completed scaffold tree.
- `LICENSE` is byte-identical to the 35,149-byte, 674-line installed GNU GPLv3 text identified in `docs/PROVENANCE.md`; all numbered sections 0 through 17 and the complete application appendix are present. This is not a claimed byte comparison with a freshly downloaded GNU file.
- A disposable copy was initialized as a local Git repository and staged. All intended scaffold files staged; `git diff --cached --check` passed.
- Ignore-rule probes checked local work, original/derived saves (including uppercase suffixes), proprietary binaries/assets, imported analysis databases, dumps, traces, logs, archives, credentials, editor state, and generated outputs.
- Trackability probes checked authored documentation, directory READMEs, future project-authored scripts, selected JSON/CSV evidence, and a future cleared data file. No blanket evidence/data ignore rule is present.
- With `core.autocrlf=true` in the disposable test repository, synthetic CRLF text/JSON evidence retained exact bytes in the index. Authored Markdown and evidence READMEs normalized to LF. Windows batch-file attributes resolved to CRLF.
- Standing-order/policy sanity checks and a content review checked the separate fork/PR/reuse gates, rights-holder permission versus user authorization, attribution, private/public boundaries, and preservation of downstream GPL rights.
- The completed tree contains no initial Codex brief, executable research code, dependency/build/CI manifest, proprietary evidence, imported reference-handle finding, or adopted experimental baseline.
- ZIP packaging was checked for CRC integrity, exact correspondence with the scaffold files, safe root-relative paths, and absence of Git metadata or symlinks. The archive has no enclosing project folder, matching the supplied example's extraction layout.

## Limits and actions not taken

No game executable, save, live process, Ghidra database, or deployment was inspected or changed. No runtime/save experiment, parser validation, or Windows-local execution occurred. No fork, PR, author contact, user-workstation change, remote write, commit, push, release, or visibility change was performed. Git initialization/staging was confined to a disposable local validation copy, not the delivered archive.

GitHub setup instructions were checked against the official documentation and the read-only observed remote state; they were not run on the user's machine. Actual first-push success, installed Git/PowerShell versions, credentials, and any later remote changes are not validated by this report.

Presence checks and policy review are not an independent legal opinion or proof of future agent compliance. Git ignore rules cannot replace rights/privacy review. The first experimental baseline, source permissions, publication scope/build matrix, and desired public author-credit wording remain unresolved as stated in `docs/RESEARCH_STATE.md`.

The publication status remains **NOT READY**. This report establishes scaffold hygiene only.
