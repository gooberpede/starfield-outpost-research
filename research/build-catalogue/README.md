# BM2 evidence verifier

[Research plan](../../docs/experiments/build-catalogue/plan.md),
[methods](../../docs/experiments/build-catalogue/methods.md),
[original frozen brief](../../docs/implementation-briefs/CODEX_BRIEF_SOR_BM2_build_catalogue_selection_production_aggregation.md).

Run from the repository root using the installed CPython 3.14 interpreter:
`python -B research/build-catalogue/verify.py --run <fresh-label>`.
Use the interpreter's absolute path if the Windows alias is unavailable.
Dependencies are stdlib and the owned `inventory_historical_saves.guard` and
`inspect_outpost_definitions.subrecords` modules under SOR-P-0002.

The checker reads task-local pinned native/definition/UI receipts, the installed
EXE/main ESM/add-on/Interface.ba2, existing analysis input pins, authored CSVs and
prior owned SWF/ABC derivatives. It writes only one exclusive ignored
`.local-work/build-catalogue/verification-<label>.json`. No target/Flash/native
execution, save reads, analysis changes, network, index/ref writes or installs.
The existing 40,000,000,000-byte free-space guard applies on C: and D:.

It rereads every selected physical definition's header and ordered fields,
reconstructs first-FNAM discovery and recipe/list closure, checks concrete
positive/negative controls, rebinds actual PE constants/vtable pointers, checks
native provenance/completion and selected instruction locators, rereads installed
archive members and all method-body spans, checks authored identities and derives
the mixed binary32 example from actual definitions. It checks integrity and those
specific operations; it is not a new parser of all condition semantics, native
disassembler, gameplay oracle, menu simulator or supported catalogue dump tool.
