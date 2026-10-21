# Verification, provenance and reproduction

SOR-EXP-0064 / SOR-EV-0072. All local artifacts below are under
`.local-work/resource-geometry-live-prep/`, unless expressly named otherwise.
The [source ledger](sources.csv) pins exact bytes and method provenance.
Use CPython 3.14.3 at
`C:/Users/User/AppData/Local/Python/pythoncore-3.14-64/python.exe` with `-B`.
No dependency installation, network or game/static-analysis process is needed.

Initial HEAD was `9e1a984295d2cf71db2b9f63076c1770573233b2`.
Only the user-supplied RG2-A brief was initially untracked; no initial tracked or
staged changes. `baseline.json` pins HEAD/index/brief, nineteen protected
EXE/ESM/Misc/development-archive/Ghidra content files and seven prior selected
save inputs. EXE 1.16.244.0 SHA-256 is
`7e9adb1414a8e1b325e5e1f097b9b17b78deb7eebeda37a333351a43a60f9d28`;
main ESM SHA-256 is
`1dabed00c3f4282dd3bb54d2e9601e40b577d8742d078b7ccef203adbfef0da7`.
PlanetData BA2's accepted pin and reused map/definition/method pins are separately
rechecked. No new executable build provenance is inferred from a save header.

## Actual check record

`checks-check01.json` retains exact commands, stdout/stderr and exit 0 for:

| Check | Actual result / coverage limit |
|---|---|
| RG1 synthetic math/context | 24 tests PASS; no new native comparison |
| New point-selector math | 4 tests PASS: opposite-label bracket, refusal of same labels, empty union and outside-circle source preservation |
| Existing resource spatial math | 12 tests PASS |
| Existing availability math | 45 tests PASS |
| Save-menu reader | 13 tests PASS; actual new menu screenshots NOT TESTED |
| Current Load-menu metadata collision census | 271/271 current headers parsed; one hash-matched full-field/time candidate per selected save after historical/current mtime reconciliation; actual rendered kind/labels still unobserved |
| RG1 installed-field runner | 68 blocks / 52 multi-point synthetic contexts, 52 checks, zero unknown; not 52 live regions |

`alternate-check01.json` independently regenerates **all 1,478 paths** with
RG1's explicit-MT/double/libm/distance implementation, matches path identities,
accepted-point counts and coordinate differences below 0.01, and matches all
147 original lattice classifications plus 21 selected **region** classifications.
It also reproduces point selection exactly. Tapered-strip selected answers use
the unchanged primary exact polygon implementation and existing math tests;
the new alternate check does not independently reimplement them. Shared source
interpretation/context limits remain; no new RUNTIME oracle is claimed.

`verification-final.json` (or later numbered receipt after a correction) records
frozen-output hashes, original/protected and accepted-source preservation,
HEAD/index/brief equality, identifier joins, JSON/CSV/SVG parsing, text/link checks
and caller-available drive space. The exact final review manifest controls which
revision these receipts cover. Any changed freeze byte or protected hash is a
failed check, not a permission to regenerate it silently.

## Reproduction and every script's effects

| Script / immediate lineage | Inputs, outputs, prerequisites and effects |
|---|---|
| [points.py](../../../research/resource-geometry-live-prep/points.py) | New original bounded selector; imports owned RG1 geometry, pure calculations on explicit receipts. CLI reads one receipt and exclusively writes a new ignored JSON via `--input` and `--output`. No target/process/save/DB writes. VERSION rg2a-points/1. |
| [test_points.py](../../../research/resource-geometry-live-prep/test_points.py) | New synthetic stdlib unittest cases only; no proprietary fixtures or file writes. |
| `.local-work/rg2a-start.py` | Original RG1-ledger checkpoint adaptation; reads/hashes protected inputs, Git/space and supplied brief; creates exclusive ignored baseline/brief receipts. No index/refs/target effects. |
| `.local-work/rg2a-investigate.py` | Original metadata/context diagnostic; uses owned save_menu first-stream reader and RG1 context, reads exact save paths/receipts/maps/definitions; writes exclusive ignored menu and counterfactual mature-context JSON. Does not decode full saves, generate mature veins or run native code. |
| `.local-work/rg2a-menu-collisions.py`, `rg2a-current-menu.py` | Read current save-directory first streams/stats, hash matching candidates and reconcile selected original mtimes; exclusive local census/current-menu JSON and corrected authored operator table only. No save/mtime writes; original historical metadata retained. |
| `.local-work/rg2a-package-data.py` | Original selected table/SVG projection and save-copy ledger. Reads pinned receipts; creates hash-verified ignored protection copies without altering sources; writes new authored identity/case/point/prediction/map/freeze files and local alternative/source ledgers. Resume only accepts byte-identical existing outputs. No game/configuration/DB changes. |
| `.local-work/rg2a-checks.py` | Runs the five named synthetic suites and RG1 actual-input runner; independently regenerates sources and compares selected points. Writes exclusive ignored check/alternate/actual-input receipts. Owned sibling explicit MT reuse is the accepted RG1 SOR-P-0002 lineage, no new dependency. |
| `.local-work/rg2a-verify.py` | Reads/hashes prior/frozen/protected inputs, source/table identities and Git; exclusively writes ignored numbered verification. No target effects. |
| `package.py` in this local root | Adapted owned RG1 exporter, immediate source/hash recorded in package manifest. Reads HEAD/index/UTF-8 tree; writes ignored complete/task-only diffs, manifests/status and isolated forward/reverse replay trees under `.local-work/review-patches/`, with Git ceiling `.local-work/`. No real-tree apply, staging, commit or ref changes. |

To reproduce selector output, run points.py with one source path from
predictions-v1.json and a **new** ignored --output; compare samples and input/
method pins. Tests use unittest discover with the directories/patterns in the
table above; checks-check01.json supplies literal commands. Raw installed maps,
full source receipts and saves are local-only prerequisites, not promised clean-
checkout downloads. The compact tracked numerical package is reconstructible
from those authorized inputs, and exact authored review patches are independently
reconstructed from HEAD/current bytes.

## Preserved faults and limitations

An initial package-data run failed after writing the identity/protection ledger
because a relative source path was passed to Path.relative_to against an absolute
root. No original or freeze bytes were modified. The helper now resolves that
path and resumes only existing byte-identical outputs; the corrected run completed
six cases, three predicted sites and 21 points. Console-only exploratory commands
also included missing guessed paths, unsupported PowerShell wildcard paths and
one quoting SyntaxError; corrected exact reads supplied the evidence. Two draft
resource IDs in prose were corrected against installed EDIDs before review.
None of these diagnostics is counted as a PASS or native absence evidence.
The first final-integrity pass also stopped on RG1 source-ledger key `path`;
its actual column is `locator`. The corrected verifier compares 19 matching
accepted RG1 pins and passes; protected inputs were unchanged. The first menu
census preserved a zero match for historical Save25 time 9:22:24 PM. A fresh
hash-identical current-original header/stat read establishes 9:22:22 PM; the
second census uniquely matches it. No prior receipt or v1 prediction was rewritten.

No new public source was consulted. Prior RG1/B1/position/Workshop/native-
availability/interference/save-menu research and Bethesda installed definitions
are credited at use and in SOURCES/CREDITS. Maintainer-owned methods use existing
SOR-P-0002 permission with exact pins; no new third-party code/data, licence basis,
contact, upload, download, tool execution grant or publication clearance arose.
Native/static/save raw artifacts and proprietary databases remain ignored/local.

## Review package boundaries

Complete diff includes all actual tracked changes and untracked authored text,
including the unchanged supplied brief. Task-only excludes that supplied brief.
The final manifest names every included path/hash, ignored/raw/binary exclusions,
patch hashes and exact forward/reverse application receipts. Git status and
index equality are retained; no staging is used to export untracked text.
The final independent reviewer record is detached to avoid self-referential
tracked hashes. Acceptance concerns this bounded preparation/UNKNOWN accounting,
not maturity of RG2-B, native equality, integration or publication.
