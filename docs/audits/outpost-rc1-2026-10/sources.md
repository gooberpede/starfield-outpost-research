# RC1: source-evidence and preservation ledger

2026-10-20, Australia/Sydney. [Answer](report.md), [review](review.md),
[declarations](papyrus-interfaces.md), [member hashes](papyrus-members.csv).
No source finding classifications or publication eligibility are changed.

## Actual starting state and inspected inputs

HEAD `e3c95f1a072f16602aac4e5ca19c153e232b23bc`; index SHA256
`8c22ccafd1d0cea1d3f6ec3c4538469daaddbec213b6e740f2e2a0ddc379e18b`. Starting status contained only the supplied untracked
RC1 brief, SHA256 `fed21ca931bd49ec5f2bd81b4daf7df012448aab4666ca32e7a66426ce894be6`.
The index was empty of staged changes. Local baseline.json pins all
1546 tracked/untracked nonignored starting files. None is an
authorized write target. Only new audit files are authored; the supplied brief
is preserved and included separately in the complete patch.

Fresh streaming SHA256 reads of installed EXE, main ESM and development archive:

Input | Actual SHA256
--- | ---
| `Starfield.exe` | 7e9adb1414a8e1b325e5e1f097b9b17b78deb7eebeda37a333351a43a60f9d28 |
| `Starfield.esm` | 1dabed00c3f4282dd3bb54d2e9601e40b577d8742d078b7ccef203adbfef0da7 |
| `ContentResources.zip` | b5f3f66d6041193c2db139c50a8a4a2da7a80c862a95ba5eec929c7a2c42983c |

These match the [coordinate source ledger](../../experiments/coordinate-sufficiency/sources.csv).
The inherited retail version label is 1.16.244.0, tied here by exact EXE equality;
no historical loaded configuration or winning override census is inferred.
Paths are under `C:/Program Files (x86)/Steam/steamapps/common/Starfield/`:
`Starfield.exe`, `Data/Starfield.esm`, `Tools/ContentResources.zip`.
Only the archive is semantically inspected afresh. ESM/EXE are integrity reads,
not new definition or native analysis. No save or analysis database is opened;
there is no claim of freshly rehashing all installed game/save/database files.
All writes are confined to the new audit and ignored local audit/package scratch.

Actual tools: git version 2.53.0.windows.1; Python `3.14.3 (tags/v3.14.3:323c59a, Feb  3 2026, 16:04:56) [MSC v.1944 64 bit (AMD64)]`,
installed at `C:/Users/User/AppData/Local/Python/pythoncore-3.14-64/python.exe`;
PowerShell for orchestration. No tool installation, update or dependency download.
Before evidence/package writes, caller free space exceeded 40,000,000,000 bytes
on both C: and D:; actual measurements are in baseline/package receipts.

## Source-evidence ledger

Source group | Inherited original claim and decisive pins | RC1 use / distinction
--- | --- | ---
Historical audit | [60 IDs](../outpost-coverage-2026-10/coverage.md), [report](../outpost-coverage-2026-10/report.md), [Build/Locations](../outpost-coverage-2026-10/build-mode-and-locations.md), [position/biomes](../outpost-coverage-2026-10/position-biomes-dependencies.md), [chronology](../outpost-coverage-2026-10/source-and-gap-reconciliation.md), [review](../outpost-coverage-2026-10/review.md) | Historical proposed dispositions copied as history; current proposals derive from actual later topical evidence, not study titles. Earlier review01 omission of recruitment/capacity was corrected with A60, retained here.
Coordinate sufficiency | [Report](../../experiments/coordinate-sufficiency/report.md), [repeatability](../../experiments/coordinate-sufficiency/repeatability.md), [API registration](../../experiments/coordinate-sufficiency/papyrus-current-location.md), [review](../../experiments/coordinate-sufficiency/review.md), [pins](../../experiments/coordinate-sufficiency/sources.csv) | Three ordinary beacons/two regions and ordered definition/settings dependence. Fresh-character recreation unknown. Earlier seed-only REWORK is preserved in source; no rerun or semantic promotion.
B1 | [Native chain](../../experiments/outpost-biomes/native.md), [finite traversal](../../experiments/outpost-biomes/nominal.md), [effective/resources](../../experiments/outpost-biomes/effective-and-resources.md), [review](../../experiments/outpost-biomes/review.md), [pins](../../experiments/outpost-biomes/sources.csv) | Qualified base-biome/nominal result, three maps/seven sites. Effective clipping and positive generated deposit availability remain separate. Machine map access is an engineering dependency.
BM1 | [Mechanism](../../experiments/construction-variants/report.md), [manual/automatic](../../experiments/construction-variants/manual-and-automatic.md), [saved cases](../../experiments/construction-variants/saves.md), [review](../../experiments/construction-variants/review.md), [pins](../../experiments/construction-variants/sources.csv) | Grouped STBH/PKIN versus ungrouped actions, materials and damage. No rendered reload or historical ambiguous-Hab resolution. RC1 does not adopt implementation prescriptions from extension prose.
BM2 | [Catalogue](../../experiments/build-catalogue/catalogue.md), [eligibility](../../experiments/build-catalogue/eligibility.md), [production](../../experiments/build-catalogue/production.md), [extension](../../experiments/build-catalogue/extensibility.md), [review](../../experiments/build-catalogue/review.md), [pins](../../experiments/build-catalogue/sources.csv) | First-FNAM/grouping/admission and binary32 nominal sum; actual throughput stays deferred. Physical roots do not prove actual menu size or unlimited capacity. Caption-role rework is retained in original review.
LO1 | [Report](../../experiments/locations-outpost/report.md), [field lineage](../../experiments/locations-outpost/field-lineage.md), [native/UI](../../experiments/locations-outpost/native-and-ui.md), [review](../../experiments/locations-outpost/review.md), [pins](../../experiments/locations-outpost/sources.csv) | Ordinary fields closed; base maximum versus remaining and decorate exclusion positively identified. Does not certify arbitrary-save active membership or an atomic screen epoch.
Earlier subsystems | Individual primary/review links in every crosswalk row and concrete topical links in every capability row | Source reports are reused within their recorded coverage, not primary computations rerun. Save29 ordinary-load C, CR1 reciprocal actors, CR3 process prerequisites and S1/S2 different insertion rules remain distinct.
Fresh declarations | Archive/member hashes above; exact line positions in papyrus-interfaces.md; local papyrus-check01/02/03.json | Direct read observations of declarations and properties only. Existing registration/call-path evidence adds semantics where named. No PEX/source equivalence newly established, script compiled, or API invoked.
Publication/governance | [PUBLICATION](../../PUBLICATION.md), [permissions](../../PERMISSIONS.md), [evidence standard](../../EVIDENCE_STANDARD.md), [provenance](../../PROVENANCE.md) | A52 concrete stale sentence conflicts with accepted scoped studies; A53 clean-checkout dependency applies to proposed release claims. Governance NOT READY remains valid. Flags are not cleanup/release authority.

## Bounded searches, failures and reproducibility limits

Selected archive paths: Game, Location, ObjectReference, Actor, GlobalVariable,
ScriptObject, OutpostActorScript and OutpostCrewStationScript under
`Scripts/Source/`. Check01 searched specific named functions/events, not all API
methods. Missing guessed WorkshopObjectScript/OutpostRobotScript paths and absent
Actor GetPerkRank declaration were not treated as missing capabilities. Existing
R1 evidence supplied the actual OutpostActorScript; check02 added it and
ScriptObject filter qualifiers. Check03 confirms existing positive movement/menu
invocation declarations and selected read/event surfaces on the unchanged
ObjectReference member; C1/S2 topical evidence supplies the actual uses. Exact native registrations were inherited only
for P01/P02 and named accepted subsystem bridges; other methods remain
declaration-grounded. No universal no-interface claim is made.

Initial broad console reads were truncated; selected topical reads supplied the
claims used here. A PowerShell rg query with shell brace paths failed to parse;
subsequent searches used explicit paths. A premature receipt read occurred while
baseline hashing was still running; the eventual complete baseline and declaration
receipt exist and are checked by the package. These are tool/locator failures,
not failed scientific tests or negative interface evidence. No source input was
changed to repair them. Later validation/review failures are retained in review.md
and local numbered receipts, rather than overwritten.

Local receipt root: `.local-work/rc1/`; local helper files have prefix
`.local-work/rc1-`. These are machine-local locators, not portable checkout
prerequisites or redistributed script sources. Source-inventory.csv pins cited
repository evidence and guidance. Source authors' native/member/export pins remain
navigable in the linked ledgers; underlying raw evidence is deliberately absent
from public-checkout promises. Protected ESM/script/map/save/native data, donor
archives and correspondence remain excluded. Unavailable historical originals,
unsupported grammars and rights limits in the original reports carry forward
(A51/A53); no new missing essential input blocked this documentation audit.

## Credit, rights and helper effects

Bethesda's installed declarations/definitions and prior static behavior are
primary sources; maintainer saves/screenshots and project-owned subsystem
research supply historical evidence. Each use cites its topical source. The
existing [source register](../../SOURCES.md) and [credits](../../../CREDITS.md)
retain the original researcher/tool/source lineage; no new external research,
implementation, licence acceptance, fork, PR, upstream contact or disclosure was
introduced. Only minimal declaration signatures, member hashes and authored
interpretations are included here; no script bodies or raw exports are copied.
This local ledger records the new audit's use without expanding its authorized
new-document write set to legacy registries.

Local original Python-stdlib helpers read Git/files/receipts and selected archive
members. They write ignored receipts/patches/scratch and the new authored audit.
The packaging method is source-informed adaptation of the maintainer-owned
`.local-work/coverage-audit/package.py` under SOR-P-0002 (its exact hash is in the
package manifest). It uses Git apply only on isolated trees, with discovery ceiling
`.local-work/`, and reverse `--check` on the actual tree. No staging, ref/index
write, target/save/database/configuration effect or network operation. Hashes
verify byte preservation, not semantic correctness. Original sources are read
only; no cleanup/deletion of unrelated work occurs.
