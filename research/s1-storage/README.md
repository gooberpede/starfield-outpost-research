# S1 bounded offline readers

Capacity follow-up: [contract](../../docs/experiments/storage/capacity-contract.md),
[report](../../docs/experiments/storage/capacity-report.md).
Encoding correction: `verify_capacity.py --text-only --run textvalidation02`
validates UTF-8 and detects likely Windows-1252/Latin-1 mojibake, replacement
characters, C1 controls and BOMs in newly authored text. It reads only text/Git
inventory and writes a fresh ignored receipt; no native/save analysis or scientific
regressions run in this mode. `text_validation.py` provides the same check to the
review exporter. `test_text_validation.py` exercises observed corruptions,
wrong-decoding variants and legitimate Unicode using in-memory text only.
`capacity.py --run calculations03 --table` reads the four accepted S1 receipts,
rehashes their original saves/readers, physically rereads selected installed
definitions and writes a fresh local calculation receipt plus optional authored
capacity-examples.csv. It does not extract new inventories or extend grammar.
`verify_capacity.py --run verification01 --tables` verifies the fresh protected
baseline, final calculations, selected native instruction locators, independent
expected float bits/decimal arithmetic and four existing regressions; writes
local JSON plus optional capacity-sources.csv. No live/native execution, new
dependency, database/save/Git mutation or external contact. All follow-up scripts
use the same CPython -B/stdlib/owned-reader safeguards described below; fresh run
names are mandatory. Local review packaging adapts the owned S1 exporter.

[Authorized brief](../../docs/implementation-briefs/CODEX_BRIEF_SOR_S1_storage_inventory_eligibility_runtime_save.md),
[report](../../docs/experiments/storage/report.md),
[execution contract](../../docs/experiments/storage/contract.md).
Original GPL-3.0-or-later research code, adapting maintainer-owned E2/E3 ESM
readers and P1 saved-instance prefix/extra grammar; provenance in sources.csv.
No new third-party implementation or dependency.

Run installed CPython with `-B` from repository root. Standard library and existing
project readers only; all inputs must already exist. Use fresh alphanumeric run
names; output receipts are retained under ignored `.local-work/s1-storage/`.
Both-drive 40 GB guards and strict source save/header/decompression framing apply.
No game, native execution, save/configuration/database/Git mutation or network.

| Script | Reads | Writes / actual final use |
|---|---|---|
| catalog.py | Pinned E2 inventory02 and installed main ESM | census02.json; 241 primary/comparison definitions, direct filter/classification dependencies and 573 physical record rereads; no raw fields promoted |
| assemblies.py | Same ESM/index; selected cargo/generator PKIN cells | assemblies01.json; full bounded header walk, selected child fields and outpost ACTI definitions |
| saved.py | Explicit qualified prior receipt/source; census02 and E2 index; owned stream/prefix/extra readers | saved03-06.json for HIST-0077/HIST-0083/HIST-0036/mature-Save52; temporary decoded scratch removed; item quantity subset and exact gaps retained |
| verify.py | Final receipts, unchanged originals/native database, scripts, authored text, HEAD/index and existing four regression suites | Fresh verification JSON; `--tables` writes catalogue.csv and source hash metadata; real-data boundary checks do not prove native semantics |

Examples: `python -B research/s1-storage/catalog.py --run census02`;
`python -B research/s1-storage/assemblies.py --run assemblies01`;
`python -B research/s1-storage/saved.py --sample HIST-0077 --run saved03`;
`python -B research/s1-storage/verify.py --run verification01 --tables`.
Existing run names cannot be reused. Evidence functions are internal research
helpers, not a supported importer, inventory dumper, save writer or gameplay mod.

Native export uses unchanged owned E2ReadSession.java and OutpostRecon.java under
existing Ghidra 12.1.2_PUBLIC/Temurin 21.0.12+8 readOnly/noanalysis invocation.
The request files and entire exports are local. Early address guesses, unrelated
literal field hits and instruction-cap flags are retained rather than negative
semantic evidence. Local packaging adapts the owned P1 exporter and applies
patches only in fresh disposable .local-work/review-patches directories, never the working tree.

[ScopedFieldUses.java](../../ghidra/scripts/ScopedFieldUses.java) is an original
read-only/noanalysis bounded literal instruction locator. It reads an explicitly
supplied <=1 MiB existing instruction/function range and writes one fresh ignored
TSV; no symbols, types, comments, program bytes or database changes. Actual runs
cover only the ContainerMenu and shared inventory-model ranges in
`.local-work/s1-storage/native-menu/` and `native-final/`. They establish literal
use coverage, not object alias identity or an exhaustive callable assignment map.
