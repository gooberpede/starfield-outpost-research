# Function and Operation Register

Initial records are scoped to SOR-ENV-0001 and [SOR-EV-0001](experiments/evidence/initial-reconnaissance/README.md). All addresses are static VA/RVA from preferred base `0x140000000`, not runtime addresses. No function here was executed live; all proposed observation points require qualification. Registration objects are distinct from game-state objects.

| ID | Build ID | Module / script | Static address or exact symbol | RVA / source version | Original name | Proposed semantic alias | Role and side effects | Confidence / basis | Evidence / source IDs |
|---|---|---|---|---|---|---|---|---|---|
| SOR-FN-0001 | SOR-ENV-0001 | Starfield.exe / ObjectReference | 0x142073cf0 | RVA 0x02073cf0 | LAB_142073cf0 (no function at entry) | GetWorkshop native callback | Reads source +0xc8 and global 0x145f0b3d8; tail-jumps to 0x140517d60; returned relationship/side effects not live-qualified | PROVEN STATIC binding; ownership interpretation PROVISIONAL | SOR-F-0003; registration FUN_14209be00; SOR-EV-0001 |
| SOR-FN-0002 | SOR-ENV-0001 | Starfield.exe | 0x140517d60 | RVA 0x00517d60 | FUN_140517d60 | Keyed reference lookup candidate | Callback target; synchronization and keyed search visible; helper calls mean not asserted side-effect-free; full layout UNKNOWN | STRONG STATIC association; semantic alias provisional | starfield-membership.tsv; SOR-EV-0001 |
| SOR-FN-0003 | SOR-ENV-0001 | Starfield.exe / ObjectReference | 0x142073dc0 | RVA 0x02073dc0 | FUN_142073dc0 | GetWorkshopOwnedObjects callback | Registration FUN_14209bc00 loads callback at 0x14209bc4b; output collection/owner filtering lead; no exhaustive enumeration claim | PROVEN STATIC binding; full behavior UNKNOWN | SOR-EV-0001; ObjectReference.psc:568 |
| SOR-FN-0004 | SOR-ENV-0001 | Starfield.exe / ObjectReference | 0x142074870 | RVA 0x02074870 | FUN_142074870 | GetWorkshopResourceObjects callback | Registration FUN_14209ba00 loads callback at 0x14209ba4c; larger body export capped; parameters/source declaration not ABI proof | PROVEN STATIC binding; full behavior UNKNOWN | SOR-EV-0001; ObjectReference.psc:575 |
| SOR-FN-0005 | SOR-ENV-0001 | Starfield.exe | 0x1421bb570 | RVA 0x021bb570 | FUN_1421bb570 | Beacon removal/validation candidate | Called by FUN_140c7af90 before beacon failure diagnostic; internal calls/state effects not fully resolved; unsafe to invoke from this finding | PROVISIONAL STATIC semantics | SOR-EV-0001; starfield-callbacks.tsv |
| SOR-FN-0006 | SOR-ENV-0001 | SQ_OutpostCargoLinkScript.psc | TransferCargo, lines 110–183 | SOR-S-0104 archive hash | TransferCargo | Cargo transfer orchestration | Script branches for loading/unloading/specific cargo, native inventory/redistribution calls; mutations expected if executed; never invoked here | PROVEN STATIC source, MIXED implementation | SOR-F-0002; SOR-EV-0001 |
| SOR-FN-0007 | SOR-ENV-0001 | OutpostCargoLinkMarkerScript.psc | OnLoad, lines 47–51 | SOR-S-0104 archive hash | OnLoad | Animation restoration consumer | Reads animation AV, requests animation application; storage authority/save format UNKNOWN | PROVEN STATIC source, MIXED implementation | SOR-F-0002; SOR-EV-0001 |
| SOR-FN-0008 | SOR-ENV-0001 | CreationKit.exe | 0x140470810 / 0x140470770 | RVA 0x00470810 / 0x00470770 | FUN_140470810 / FUN_140470770 | Workshop / WorkshopItem default-object registration | Binds descriptive keyword labels; initialization routines, not retail membership operations | PROVEN STATIC strings/calls; runtime equivalence UNKNOWN | ck-functions.tsv; SOR-EV-0001 |
| SOR-FN-0009 | SOR-ENV-0001 | CreationKit.exe | 0x140470900 / 0x140470590 | RVA 0x00470900 / 0x00470590 | FUN_140470900 / FUN_140470590 | Location/container default-object registration | Descriptive relationship labels; no serializer or retail layout inferred | PROVEN STATIC strings/calls | ck-functions.tsv; SOR-EV-0001 |

Use `SOR-FN-` IDs. For native functions record actual static/image bases and instruction ranges in the linked detail. For script operations record the script, exact source/version, declaration or call site, and what was independently checked. Include Address Library IDs only with version/provenance.

## SOR-EXP-0002 coordinate candidates

| ID | Build/module | Original static VA / RVA | Observation and limit | Evidence |
|---|---|---|---|---|
| SOR-FN-0010 | SOR-ENV-0002 Starfield.exe | FUN_14167f7e0 / 0x0167f7e0 | Named property binding candidate; +0x68/+0x88 addresses passed with latitude/longitude names at 0x14167f82f–854. Object/type/units unqualified; no invocation or saved-layout claim. OBSERVED-INTERNAL. | SOR-F-0005 / SOR-EV-0002, coordinate functions export |
| SOR-FN-0011 | SOR-ENV-0002 Starfield.exe | FUN_14341c0a0 / 0x0341c0a0 | Existing xrefs to both coordinate names at 0x14341c207/251; bounded function export. Relationship to a selected outpost UNKNOWN; not a callable integration point. | SOR-EV-0002 |
| SOR-FN-0012 | SOR-ENV-0002 CreationKit.exe | FUN_142b96190 / 0x02b96190 | Xrefs to Location: Longitude/Latitude labels only; function body not exported. No retail address/layout equivalence. | SOR-F-0005 / SOR-EV-0002 |

Preserve original names and addresses; semantic aliases do not authorize Ghidra renaming. Record reads/writes, callers, parameters, ownership, lifecycle, failure/cleanup paths, and unresolved parts as supported. Call-site and instruction evidence take precedence over an unverified decompiler prototype.

Separate observed internal functions from exposed or validated integration points. See [EVIDENCE_STANDARD.md](EVIDENCE_STANDARD.md).

## SOR-FN-0013 — EXP0002 native query/operand set

SOR-ENV-0002, OBSERVED-INTERNAL / STATIC. [Contract table](../runtime/exp0002/STATIC-CONTRACT.md) lists each original VA/RVA and operand: GetPlayer 0x14177a1f0, transform callbacks 0x142072580/590/5a0 and 0x1420702e0/300/320, parent 0x14208b990, worldspace 0x14208b9e0, FormID 0x14204d600, location 0x14208b8f0 -> 0x140b4e650, cell-view windows and worldspace-cell setter 0x140bbdf70 (never invoked). GetBaseObject/Is3DLoaded wrapper conventions are not reused as direct R8 callbacks. Evidence SOR-F-0006 / SOR-EV-0002; independent instruction checks take precedence over library/decompiler prototypes. Calling/lifetime safety remains unvalidated live; persistence UNKNOWN. No symbol/type/comment modifications.
