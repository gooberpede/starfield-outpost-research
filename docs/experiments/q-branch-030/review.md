# Offline Q branch candidate review package

2026-10-12. [Contract](../../implementation-briefs/README.md#archive-lookup) (`implementation-briefs.zip :: docs/implementation-briefs/CODEX_BRIEF_SOR_Q_branch_observations_offline.md`),
[qualification/matrix](qualification.md), [schema](../../../runtime/native-oracle-030/schema.md).
**Independent disposition: ACCEPT — offline engineering complete.** The reviewed
candidate remains unintegrated and not live-qualified.

## Exact offline candidate

Local directory `.local-work/native-oracle-030/builds/qualification-02/`:

| Artifact | SHA256 |
|---|---|
|SorNativePositionOracle-0.3.0.zip|bc51e7aad714880f419d07dab5dad1f8451934148ac5180564ee2a34891c627f|
|SorNativePositionOracle.dll|a2b0c90525928f287e2168f0d0c7150253f4d6c2089e79a8ab3b9925c9f5bfa6|
|build.json|6bdadc78ebfe1552adae913bb75cd5c0d54fc44ab4a5a4d12eb2bb4742b222f7|

The ZIP/DLL are LOCAL-ONLY offline review artifacts, not deployment instructions.
Exact packaged sources and tool/guard/protected-input identities are in build.json.
qualification.txt has 520 PASS checks; branch-qualification.txt has 240; inspection-
tests.txt30; branch-inspection-tests.txt6; branch-decoder-qualification.txt12
actual wrapper-output cases with details in branch-cases/qualification.json.

## Reproduction and changes

Use the [README build command](../../../runtime/native-oracle-030/README.md) with
a fresh name. Additional checks, from repository root, using existing CPython:

```powershell
& 'C:/Users/User/AppData/Local/Python/pythoncore-3.14-64/python.exe' -B -m unittest discover -s save-analysis/scripts -p test_*.py
& 'C:/Users/User/AppData/Local/Python/pythoncore-3.14-64/python.exe' -B save-analysis/scripts/verify_position_v2.py --output .local-work/q-branch-030/frozen-reproduction
```

Unchanged 020 inspector regression used its retained disposable fixture bytes,
producing newly named synthetic derivatives only. No original evidence overwritten.
Local `.local-work/q-branch-030/` contains initial baseline/before text copies,
regression logs/receipt, frozen 23 replay, preserved failures and package manifests.
Changed-file inventory distinguishes original uncommitted Q/E research from this
task's separate 030 sources and incremental summary/index additions.

`.local-work/diffs/q-branch-030-complete.diff` includes all uncommitted tracked
changes and untracked text since HEAD, including the supplied prior brief and
previously reviewed Q/E work. `q-branch-030-task-only.diff` starts from this task's
actual initial working tree, preserving earlier uncommitted bytes in its base.
Plain disposable validation trees receive each patch forwards and are compared
byte-for-byte with the current tree. package.json binds patch hashes/inventories,
status, inclusion/exclusion lists, links/whitespace checks, source pins and unchanged
HEAD/index. No staging is used to construct patches.

Excluded/LOCAL-ONLY: `.local-work/` raw/journals/native exports/test binaries/ZIPs/
generated native preimages/private saves/receipts, original installed game/SFSE,
save/Vortex directories and external native analysis databases. Exclusions are
explicit in exclusions.json; a “complete patch” means complete authored uncommitted
text, not permission to include raw or proprietary evidence.

## Actual independent review

Reviewer `/root/q_branch_review` runs read-only under WORKFLOW/protocol authority.
Initial challenges tightened Q return/latch and helper-argument/output linkage,
structured mutable-sample disagreement reporting, overlapping loaded guard handling,
and qualification of native x87/MXCSR/LastError effects across rounding modes.
The implementer authored corrections; the reviewer did not edit files.
Initial missing-module failure and intermediate manual/compile errors are preserved.
Formal decision: **ACCEPT**, all six mandatory criteria PASS. Exact submitted
manifest SHA256 `e038bb4c280a7941773246d36c3e4dd985266f9fa1523bd30782d69248f03012`;
immutable `.local-work/q-branch-030/reviewed-submission/` preserves 39 authored
files and the initial reviewed complete/task patches. The reviewer independently
verified all 39 tree hashes, build/source/ZIP identities, 238 protected pins,
534 unchanged starting files, patch hashes and retained validation-tree bytes.
The reviewer also checked reverse applicability and tracked whitespace. Forward
applications and 422 links were assessed through the packaging source/receipts;
native test results were read from primary logs/code, not independently rerun.
HEAD/index and reviewed snapshot remained unchanged during review. Full actual
decision is retained in `.local-work/q-branch-030/independent-decision.md`.

Initial reviewed patch hashes: complete
`f80ce09fb64d5a9c9df4777c2c51c350ba60ad11dd9fa3557526a52a60659c81`;
task-only `485e5177aca7b94e634cb8fdc4f58690a5197dd45801fc4b8968021467512abc`.
Final patches refresh only this decision/criterion closure; current hashes are
bound by package.json. Closure consistency is reviewed separately, with its
actual disposition retained locally. Acceptance does not bypass maintainer review.

Scientific outcome remains **native equivalence NOT TESTED**. Offline engineering
acceptance cannot approve deployment, launch, live capture, integration or publication.
No permission issue or external contact arose; no Git mutation occurred.
