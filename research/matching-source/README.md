# Matching-source offline tools

Original project-authored CPython 3.14 stdlib tools under GPL-3.0-or-later;
source-informed by existing pinned native exports and project readers. See
[report](../../docs/experiments/matching-source-qualification.md) and
[brief](../../docs/implementation-briefs/CODEX_BRIEF_SOR_matching_source_qualification_enumeration_reachability.md).

`verify.py OUTPUT` reads original 030 raw/journal, sealed 93 members, 310 lock pins,
prior receipts, pinned Save25–28, existing ESM catalog and native TSV instructions.
It writes only a new ignored OUTPUT/receipt.json and temporary decoder scratch;
no original input, process, game, config, network or database is modified.
Requires retained private inputs and existing project decoder modules.
The 40 GB free-space guard runs before/after substantial processing.

`package.py --baseline` captures initial tracked-file hashes/HEAD/index/status
before tracked edits; initial tracked tree must be clean. `package.py` exports
task-only and complete patches, including untracked UTF-8 text and the supplied
brief in complete only. It checks paths, LF/whitespace/links, unchanged unrelated
tracked files, exact forward application in disposable plain .local-work/review-patches trees and
HEAD/index identity. Writes ignored local manifests/diffs only; Git is read-only.
It never stages. Disposable trees are retained as verification artifacts.

No third-party source, package installation or native call simulation is used.
Pure key controls/CFG checks are separate from actual runtime operands and save
joins. Passing them does not prove live reachability or native model equivalence.
