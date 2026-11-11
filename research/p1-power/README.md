# Bounded P1 offline research utilities

`save29_feasibility.py --run NAME` is an original bounded feasibility probe,
**not a save writer**. It reads the exact existing Save29 archive/receipts,
protected Save3/29 originals, installed executable/ESM and owned readers. It
writes exclusive ignored `.local-work/p1-save29-derivatives/NAME/feasibility.json`
and temporary decoder coverage probes that are removed on exit; no `.sfs`
candidates, original edits, game/database/network/Git writes. Run CPython `-B`
from repository root, with matching prior pins and C:/D: 40 GB free guards.
[NO-GO report and serialization prerequisite](../../docs/experiments/power/save29-derivatives.md)
explain why reader acceptance does not qualify repacking.

[Brief](../../docs/implementation-briefs/README.md#archive-lookup) (`implementation-briefs.zip :: docs/implementation-briefs/CODEX_BRIEF_SOR_P1_power_generation_distribution_native_mapping.md`),
[report](../../docs/experiments/power/report.md).
Original GPL-3.0-or-later code, using owned strict ESM/save readers from E1–E3.
Run installed CPython 3.14.3 with `-B` from the repository root. Standard library
and existing `save-analysis/scripts` only; no download or dependency install.
All input files must already exist. Fresh run names preserve earlier receipts.

| Script | Reads / prerequisites | Writes / actual final receipt |
|---|---|---|
| definitions.py | Pinned main ESM, E2 selected-type inventory, supplied Pascal exporter and maintainer sibling source files | `--run definitions03 --tables`: exclusive local JSON, authored catalogue/environment/construction CSVs; 770 physical selected records and full group/header construction join |
| verify-definitions.py | Final definitions receipt, source CSV and installed ESM | `--input .local-work/p1-power/definitions03.json --run definitionVerification02`: 1,765 PNDT physical field comparisons, 17 generator ratings and fuel chain; exclusive local JSON |
| saved_instances.py | Selected prior hash-bound source receipt, original save, P1/E2 definitions; supported counted-extra grammar | Six final runs `instances04`–`instances09` under local `saved/`; decoded scratch is temporary and removed, exact record/extra offsets retained. CLI arguments are documented by `--help` |
| saved_graph.py | Six final instance receipts and their original/hash identities | `graph03.json`: endpoint resolution, word distributions, reciprocal graph components and explicit unsupported boundaries; no runtime graph construction |
| verify.py | Final receipts, authored text, native exports, stopped database, HEAD/index and protected inputs | `--run verification01 --pins`, then fresh verification names: exclusive local JSON; source metadata CSV with `--pins`; byte/identity, syntax, registry VA/RVA, prose/link and preservation checks |

Definitions and save utilities hash originals before and after, apply existing
free-space/decompression/framing guards and preserve unsupported records.
None launches the game, invokes native functions, edits saves/configuration,
changes an analysis database or mutates Git. Current runtime values remain absent.
Exact original source/tool hashes are in the receipts and source CSV.

Native exports use the unchanged owned `.local-work/e3-fabricators/native/E2ReadSession.java`
and `ghidra/scripts/OutpostRecon.java`, through Ghidra readOnly/noanalysis.
Numbered selector requests and outputs remain under `.local-work/p1-power/native/`;
the stop marker and process exit delimit the completed session. The first
WindowsApps Python alias and standard Ghidra launcher failed during startup;
the explicit CPython path and direct existing JVM workflow resolved these.
A default Ghidra cache-maintenance write was denied and logged; static exports
completed, and database preservation is checked separately. No denial was
bypassed by changing permissions or requesting escalation.

The local review exporter adapts owned `.local-work/e3-fabricators/export.py`.
It reads HEAD/index and changed text; writes complete/task-only diffs and
manifests; applies them only in disposable `.local-work/review-patches` trees and verifies exact
forward/reverse contents. Raw saves/game/native/database evidence is excluded.
No staging, branch/ref write, commit, push or upload occurs. Hash equality
proves byte identity, not the correctness of the semantic interpretation.

## Focused order/state follow-up

`followup.py --run NAME` freshly reads two protected originals with existing
owned strict save readers, verifies prior selected records, and emits exclusive
ignored receipts under `.local-work/p1-order/saved/`. Its real ordered-tree
fixtures assume resolved handles, eligible generators and matched predicates.
No demand/supply calculation or live validation. `verify-followup.py --run NAME`
audits source pins, preserved inputs and all modified documentation. See the
[research derivation](../../docs/experiments/power/followup.md).

## Load follow-up checks

`load-checks.py --run verification01 --pins` checks stopped read-only native
exports, protected originals/database/HEAD/index, source locators, real saved
nominal component coverage and all changed Markdown encoding/link inventories.
It reads local research receipts and Git state; writes only an exclusive ignored
JSON receipt and, with `--pins`, `docs/experiments/power/load-sources.csv` metadata.
Uses Python stdlib only. No game, network, database mutation or save decoding.
Its nominal screen is not a current-power calculator or determinism test.
