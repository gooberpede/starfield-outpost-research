# E2 bounded offline research utilities

[Brief](../../docs/implementation-briefs/README.md#archive-lookup) (`implementation-briefs.zip :: docs/implementation-briefs/CODEX_BRIEF_SOR_E2_organic_facility_native_mapping.md`),
[report](../../docs/experiments/organic-facilities/report.md).
Original GPL-3.0-or-later research code, using existing maintainer-owned readers.
These are bounded evidence utilities, not an importer or supported production tool.

Use installed CPython with `-B` from the repository root. Standard library and
repository `save-analysis/scripts` modules only. The UI verifier additionally
uses the explicitly pinned owned local E1 instruction decoder and private SWF/ABC
derivatives. Inputs must already exist; no download, installation or regeneration
of original captures is performed. All outputs are exclusive ignored JSON under
`.local-work/e2-organic/`; fresh run names avoid replacing earlier receipts.
Raw fields/native/UI/save derivatives are never written into tracked tables.

| Script | Reads / prerequisite | Writes / actual run |
|---|---|---|
| catalog.py | Installed main ESM; supplied Pascal/screenshot; sibling reference CSV/transformation/profile | `--run inventory02`: 41,178 selected-type records and source signatures; inventory01 retained initial narrower type coverage |
| derive.py | `--inventory` (default inventory02.json), installed ESM, sibling CSV and prior supported Save52 root inventory | `--run derived02`: typed resource/construction catalogue, source-pattern check, 340 physical record checks and six saved roots |
| assemblies.py | Same `--inventory`, installed ESM | `--run assemblies02`: full group/header walk, 753 child references across six PKIN cells |
| saved.py | Pinned prior Save52 receipt, protected original save, derived01 catalogue; existing decoder/Workshop parser | `--run saved02`: exact prior audit replay, selected groups, directed link envelope and upstream Water paths; temporary decoded scratch cleaned by context manager |
| selected-state.py | Same protected save, saved02 and derived01; owned counted-extra grammar | `--run selected-state02`: six leading ExtraBF base-value checks independent of producer rows; temporary scratch cleaned |
| verify-ui.py | Installed Interface.ba2, pinned owned `.local-work/e1-arithmetic/ui-disasm.py`, prior private SWF/ABC | `--run ui-verification02`: archive/SWF equality, all method byte spans, eight decoded selection/display methods; no Flash execution |
| verify.py | Current pinned inputs, derived02/assemblies02/saved02/selected-state02, authored tables and local native-register additions | `--run verification01`: table coverage and exact contents, six AV and directed-path joins, executable/source identity, register addresses/export functions |

Run catalog before derive/assemblies, and derive before saved/selected-state.
Existing original receipt names are intentionally retained as dependencies for
this task; later reruns can pass a fresh inventory path/run name or use a separate
authorized receipt workspace without moving protected evidence. No script launches
the game, invokes native functions, restores or changes saves/configuration,
edits analysis state or changes Git index/refs. Existing C:/D: disk guards and
reader framing/decompression bounds apply. Guard/hash failure stops the affected
analysis. Hashes do not validate semantics; inspect the decisive native evidence.

The local review exporter adapts the owned E1 helper and is pinned in provenance.
It reads HEAD/index and changed text, writes local complete/task-only patches and
disposable .local-work/review-patches apply trees, and checks exact forward/reverse contents. Its
patches omit raw/private/binary assets. No workspace patch application or staging.
