# L1 bounded offline research aids

Run from repository cwd with installed CPython 3.14 and `-B`; stdlib and owned
project readers only. [Frozen plan](../../docs/experiments/limits/plan.md),
[report](../../docs/experiments/limits/report.md), [pins](../../docs/experiments/limits/sources.csv).
Both-drive 40,000,000,000-byte guards apply. No game, save writes, database edits,
network, installs or Git mutation. Raw derivatives stay ignored/local.

`saves.py --samples S0 S1 HIST-0036 HIST-0077 HIST-0255 HIST-0267` reads frozen
metadata and existing originals, hashes each, disk-decodes with automatic scratch
cleanup and frames typed records. It retains supported beacon/turret/player
prefixes and explicitly unsupported extra data in exclusive local JSON. It
reuses R1/CR1 actor/extra readers with no new guessing around unknown extras.
Use a new local output directory/copy for repeat acquisition: existing receipts
are intentionally not overwritten. The inputs are observational save evidence,
not a production importer or exhaustive active-outpost census.

`verify.py --run NEWNAME` reads the baseline, physical ESM and six selected
originals, local definition/script/native receipts and prior root ledger. It
checks the complete COBJ census, exact selected record fields, installed VMAD,
fully decoded PEX fragments, native instruction locators, protected files,
HEAD/index, and freshly decoded limited Save52 root records. It writes an
exclusive verification receipt (or failure receipt), never modifies sources.
Assertions are required; do not use Python `-O`. Integrity/string checks are
not a runtime oracle. Exceptions and earlier failed assertions remain history.

Original acquisition/orchestration/census helpers are retained under
`.local-work/l1-*.py`, with their hashes in the source ledger. ESM reader is
`save-analysis/scripts/inspect_outpost_definitions.py`; compiled PEX reader is
owned `.local-work/cr1-crew/pex_probe.py`, also reused by R1/CR2. Native exports
adapt R1's existing Cr1Recon/E2ReadSession/TransitCalls under Ghidra's
`-readOnly -noanalysis`. The added condition-registration selector scans only
existing instructions in `1400bfd90..1400f0000` for three fixed command IDs and
exports bounded windows, without analysis/symbol/type/comment/byte edits.
Method transformation helpers preserve provenance for each selector revision.
The first worker exited on a malformed exploratory selector; the corrected
request/restarted worker and sentinel stop remain distinct local receipts.

The review exporter adapts owned R1/CR3 packaging: exact complete/task-only
text diffs, manifests, link/encoding/whitespace checks and disposable D:/tools
forward/reverse reconstruction, no staging or workspace/index apply. SOR-P-0002
applies to owned methods. Bethesda sources, Ghidra/JDK/Python/Git tools and
protected maintainer saves retain existing project credits and permissions.
