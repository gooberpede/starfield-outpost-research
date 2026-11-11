# Resource-region review package

2026-10-15, Australia/Sydney.
[Original brief](../../implementation-briefs/README.md#archive-lookup) (`implementation-briefs.zip :: docs/implementation-briefs/CODEX_BRIEF_SOR_resource_region_dependencies_minimum_requirements.md`),
[frozen contract](region-contract.md), [technical report](region-dependencies.md).
Outcome B independently ACCEPTED after rework. User critical review remains
required before integration; authored material REVIEW-REQUIRED, native/raw LOCAL-ONLY.

| Original mandatory criterion | Status / primary evidence |
|---|---|
| Technical account with positive/negative findings | PASS: region-dependencies.md with pinned address domains and scoped minimum-state answer |
| Provider/generation lifecycle and state ownership | PASS: region-lifecycle.md, functions N15–26/N35–66, new six exports; request versus completed geometry distinguished |
| Minimum-input matrix for all requested contexts | PASS: region-requirements.md; presence, current world, residency, completion and freshness separated |
| Existing native register/dataflow extended | PASS: functions.csv 66 records, sources.csv 26 pins and dataflow.md cross-reference; no parallel native register |
| Evidence/uncertainty register and defensible B boundary | PASS: region-uncertainty.md RD01–RD07, traced routes and precise missing state; no mandatory-travel or remote-success claim |
| Offline tests and preservation | PASS: 57 existing tests, 16 instruction contracts, eight focused groups; 6,868 protected pins and 15 Ghidra files equal; HEAD/index unchanged; region-validation.md and local receipts |
| Reviewable task-only/complete diffs | PASS review03: 24 complete paths / 23 task paths; 802 relative-link file checks; whitespace and exact forward/reverse reconstruction; refreshed revision below |
| Independent completion assessment | PASS: independent reviewer ACCEPT of corrected final01, with exact snapshot and limits below |

Scientific result: positive STATIC dependency/lifecycle reconstruction with
runtime sufficiency and spatial equivalence NOT TESTED. Engineering: focused
source-linked assertions and existing regressions pass. Target survival/cleanup:
not applicable; no game/process/live instrumentation. Authority: offline only;
no save/configuration changes, staging, commit, push or external contact.

Changed-file inventory: new region contract/report/lifecycle/requirements/
uncertainty/validation/review and source metadata; new focused verifier; existing
function/source/dataflow/minimum-input/report documentation and research README;
project indexes/state/source/credit updates. Exact path/hash manifest and Git
status are supplied by the export receipt. The supplied original brief is
included only in the complete diff. Ignored local exports, raw evidence,
proprietary game/analysis inputs and disposable verification trees are excluded.

Credit/provenance: SOR-S-0149; earlier SOR-S-0145–0148 preserved. No new outside
code/dependency, licence acceptance, permission issue or disclosure is introduced.
Protected-input hashes prove preservation, not semantics or publication rights.

## Review findings and rework

The independent reviewer identified an incorrect solid Mermaid edge from
neighbor preparation `007A0FA0` to provider `0079F860`. Actual worker `007B5160`
calls both at static VA `1407B524C` / `1407B526A`. The map now shows sibling
call edges and explains sequential order separately from ancestry. Primary
inspection also found and corrected a brief-index encoding regression; its final
diff contains only two task-added lines. The earlier EOF whitespace/export
failure is retained in region-validation.md. Neither failure is hidden or
relabelled a scientific test pass.

The reviewer independently checked the two cache-key domains, lock scope,
producer gates/no-success-certificate, async request ancestry and neutral
remote/travel conclusions. Decision: **ACCEPT — corrected final01 satisfies
the original brief's Outcome B criteria; no remaining substantive blocker.**

Exact actual return: ignored
`.local-work/resource-region-dependencies/reviewer-final01-verbatim.md`.
Reviewed manifest `package-final01.json` SHA256
`984c58a65813837c2be7f31fe812124a7b514edef7fc0fac48e268f883476ccc`,
HEAD `6475a1fb4a70711d3035e2c89a05085b9b57f5b4`, index SHA256
`0e869b2c4add032b12ff8b2593cf326821b613f78a43efa49a18ca15946b94ca`.
Reviewer verified all 24 current file hashes before/after, 26 native source
hashes, 66 function declarations/address pairs, 16 instruction contracts, eight
focused assertion groups, installed executable pin, 802 relative-link targets,
whitespace/encoding, inventory and both patches' exact in-memory reconstruction.
The 57 regression passes were inspected in receipts rather than independently
rerun; 6,868 protected pins and 15 Ghidra maps were compared between receipts
rather than independently rehashed. These limits remain explicit.

Final disposition-only packaging revision:
`.local-work/resource-region-dependencies/package-final02.json`,
`status-final02.txt`, and `.local-work/diffs/` patches:

- `resource-region-dependencies-final02-task-only.diff`
- `resource-region-dependencies-final02-complete.diff`

The manifest holds exact current path/hash inventory, exclusions, patch hashes
and forward/reverse exact-apply checks. The complete diff includes the supplied
brief; task-only includes 23 authored/modified paths. The final administrative
recheck is retained as `reviewer-final02-verbatim.md` beside the receipts. This
disposition does not authorize integration, publication or a future live test.
