# Function and Operation Register

## SOR-EXP-0017 — Typed workshop, persistence and geometry

SOR-EV-0025, pinned Starfield.exe SHA-256/base in [report](experiments/workshop-origin-beacon-relocation-persistence.md); STATIC/OBSERVED-INTERNAL/REVIEW-REQUIRED. RVA = static VA − 0x140000000; [native map](experiments/workshop-origin/native-map.csv) records decisive sites and limits. No invocation, ABI/safe integration validation or Ghidra renaming.

| ID | Original static VA(s) | Supported role / limit |
|---|---|---|
| SOR-FN-0040 | 140f4ffc0 / 14053dd30 / 140f51350 | Type-0xbc constructor, allocation, guarded accessor; +0x60 initialization |
| SOR-FN-0041 | 1421b11a0 / 1421b1450 / 1421b44b0 / 1421b2e20 | Accumulating endpoint-subtraction writer, callers and separate reset; endpoint labels inferred |
| SOR-FN-0042 | 140f50660 / 140f50880 / 140521620 | Explicit +0x60/+0x68 save/load; buffer-version and variable-prefix conditions |
| SOR-FN-0043 | 140f4ab80 | Current reference XYZ plus Workshop compensation; no planetary projection |
| SOR-FN-0044 | 140f4a140 / 140f49440 / 140f49c50 / 140f4a910 / 140f4ac50 / 140f4aab0 / 1421bb860 / 1421b2570 | Descriptor, drawing, predicates, clamp and loaded-state output; full permission not established |
| SOR-FN-0045 | 140f38e30 / 140157cc0 / 140157700 / 14044b670 | Property/binding/fallback radius; live overrides unresolved |
| SOR-FN-0046 | 140ad0b90 | Compensated center/radius into terrain/overlay coverage; discrete, not continuous current-beacon coordinates |

## SOR-EXP-0015 projection/frame consumers

Pinned SOR-ENV-0001 hash/base in [report](experiments/exact-beacon-planetary-coordinates.md), SOR-EV-0021. STATIC/OBSERVED-INTERNAL/REVIEW-REQUIRED; no live calls/ABI qualification/renaming/integration. RVA = VA minus0x140000000; member offsets are not wire offsets.

| ID | Original static VA | RVA | Supported role / limit |
|---|---|---|---|
| SOR-FN-0033 | FUN_14008cb90 /14008cc50 /14096e060 /14096da90 | 0008cb90 /0008cc50 /0096e060 /0096da90 | Defaults10+2, ordinaryR256; actual other configuration required |
| SOR-FN-0034 | FUN_14096ecb0 /14096f4d0 /14096efb0 | 0096ecb0 /0096f4d0 /0096efb0 | Quantizer, centred indices, origin snap; no visible-tile dimensions |
| SOR-FN-0035 | FUN_14078d1f0 /14078d660 /1423321f0 /142332410 | 0078d1f0 /0078d660 /023321f0 /02332410 | Local floorXY/origin displacement/projection; angle omits fractionalXY/Z |
| SOR-FN-0036 | FUN_140ad7200 /140ada960 /140ad40c0 | 00ad7200 /00ada960 /00ad40c0 | Keyed activated-overlay integerXY*100/vertical translation; restored map unqualified |
| SOR-FN-0037 | FUN_1418325a0 /141833b20 /140b4e410 | 018325a0 /01833b20 /00b4e410 | World/initial flags/restoration/rebase; final authority unknown |
| SOR-FN-0038 | FUN_140910690 /1407bcfb0 | 00910690 /007bcfb0 | Cached/active-world/fallback; body-space consumer also quantizes; no subcell proof |
| SOR-FN-0039 | FUN_140ad1660 /140ad47e0 /140ad4a00 /140add310 | 00ad1660 /00ad47e0 /00ad4a00 /00add310 | ActivatedOverlayProperty creation/registration; saved linkage unknown |


## SOR-EXP-0014 terrain-frame bridge

SOR-ENV-0001 / SOR-EV-0020, pinned Starfield1.16.244.0, preferred base `0x140000000`. [Operand locations, input gaps and export identities](experiments/two-outpost-site-anchors-and-beacon-coordinates.md#coordinate-transformation-investigation). STATIC / OBSERVED-INTERNAL / REVIEW-REQUIRED; no native invocation, callable ABI, complete branch coverage or safe integration. World creation/registration and terrain queries have effects if executed; only existing analysis state was exported here. In-memory offsets are not wire offsets.

| ID | Original static VA | RVA | Supported observation and limit |
|---|---|---|---|
| SOR-FN-0029 | FUN_140ad31a0 / FUN_140ad30a0 | 00ad31a0 / 00ad30a0 | Exterior cell/world selection with inclusive integer XY bounds. Does not prove saved parent is a loaded cell or identify one universal overlay. |
| SOR-FN-0030 | FUN_140ad3b20 / FUN_140ad3c30 | 00ad3b20 / 00ad3c30 | Eligible world/component path resolves body and searches overlay by world ID, copying two doubles. Retrieves an anchor without adding reference XYZ. |
| SOR-FN-0031 | FUN_14077fc20 / FUN_14078d370 | 0077fc20 / 0078d370 | Branch combines terrain-index displacement and reference position, splits XY into grid offsets and residual with factor100, and projects indexed point to angles. Manager origin/resolution and precise residual projection remain unresolved. |
| SOR-FN-0032 | FUN_1418ab8d0 / FUN_140ad0400 | 018ab8d0 / 00ad0400 | Conditional pair registration with existing world or generated-world construction. No proof of the branch actually used by Save25 or a universal one-overlay-per-outpost rule. |

## SOR-EXP-0013 surface-anchor chain

SOR-ENV-0001 / SOR-EV-0019, Starfield1.16.244.0, preferred base `0x140000000`; executable hash and [exact data flow/limits](experiments/planetary-surface-anchor-semantics.md#decisive-native-and-definition-chain). STATIC / OBSERVED-INTERNAL / REVIEW-REQUIRED. No callable ABI, safe integration, live invocation or project renaming. Full exports remain LOCAL-ONLY; important instruction/decompiler limits are indexed.

| ID | Original static VA | RVA | Supported observation and limit |
|---|---|---|---|
| SOR-FN-0023 | FUN_141686a00 | 01686a00 | Ray/sphere hit in inverse body orientation; atan2(y,x), atan2(z,horizontal norm), two double stores. Float intermediate stages; geographic datum uncalibrated. |
| SOR-FN-0024 | FUN_140ad0650 / FUN_140ad55b0 | 00ad0650 / 00ad55b0 | Overlay path copies pair/world ID; named formatter uses second Lat, first Lon. Exact beacon position not supplied. |
| SOR-FN-0025 | FUN_140779300 / FUN_140771ac0 | 00779300 / 00771ac0 | Supplies planet/body identity and two-double/world-ID tuple to CTPlanetOverlayData insertion command. Full wire serializer not established. |
| SOR-FN-0026 | FUN_1407772c0 / FUN_140774ee0 / FUN_140777560 | 007772c0 / 00774ee0 / 00777560 | Command callback, component-store comparison/copy at in-memory +20/+28/+30; those are not save offsets. |
| SOR-FN-0027 | FUN_14076ec00 / FUN_140773090 | 0076ec00 / 00773090 | Pre-BDST CNAM 20-byte latitude/longitude/world records swapped into overlay tuple. Main loader instruction cap; full decompilation plus fixed byte comparisons retained. |
| SOR-FN-0028 | FUN_1416874f0 / FUN_142332410 / FUN_1423321f0 | 016874f0 / 02332410 / 023321f0 | Selected pair can be adjusted through terrain indices/direction projection. Exact local-beacon bridge is a follow-up, not a decoded global transform. |

## SOR-EXP-0010 conditional restoration and ownership readers

SOR-ENV-0001 pinned Starfield1.16.244.0, preferred image base0x140000000, SHA-256 `7e9adb1414a8e1b325e5e1f097b9b17b78deb7eebeda37a333351a43a60f9d28`; SOR-S-0127 / SOR-EV-0016. [Exact supporting observations and limits](experiments/active-outpost-membership-completion.md). STATIC / OBSERVED-INTERNAL / REVIEW-REQUIRED. These loader functions mutate reconstructed objects when the game executes them; this task only reads existing instructions and never invokes them. No safe integration point, complete caller set, live ABI or authoritative player-membership predicate is established. Original Ghidra names are preserved.

| ID | Original static VA / name | RVA | Supported observation and limitation |
|---|---|---|---|
| SOR-FN-0019 | FUN_141832f00 | 01832f00 | Conditional REFR initial-case selector; flags0x92018200 select6. Does not resolve inherited form type or ownership. |
| SOR-FN-0020 | FUN_141835610 / FUN_141835c20 / FUN_1405dfa40 | 01835610 / 01835c20 / 005dfa40 | Paired initial readers and general form loader; separate queue/body consumption, self ref and bit0-gated saved flags. Omission preserves an unresolved inherited/default state. |
| SOR-FN-0021 | FUN_14054c2f0 / FUN_14053a2d0 | 0054c2f0 / 0053a2d0 | ExtraPromotedRef0x84 counted ref/byte pairs versus ExtraOwnership0x1f; player promotion ref is not an owner field. Inherited ownership and actual execution remain unvalidated. |
| SOR-FN-0022 | FUN_140f3bfc0 | 00f3bfc0 | Exclusion-property query through reference+0x68 with global145f0c6d0. Resolved keyword/FormID and equivalence to BlockPlayerActivation unknown; no complete player-control proof. |

## SOR-EXP-0002A save-path candidates

SOR-ENV-0003 / SOR-EV-0005, STATIC / OBSERVED-INTERNAL, REVIEW-REQUIRED. All Starfield1.16.244.0 addresses below use preferred base0x140000000 and the pinned hash in [the detailed candidate map](experiments/SOR-EXP-0002A-native-save-thread-mapping.md#current-candidate-map). That map records call sites, provisional argument roles, strings, side effects and limits. No candidate was observed executing in a manual save; debugger setup is not native invocation qualification.

| ID | Original name / static VA | RVA | Provisional role and principal limitation |
|---|---|---|---|
| SOR-FN-0014 | FUN_14166c0a0 / FUN_14166c190 | 0166c0a0 / 0166c190 | UI dispatch/save selection; direct or queued path, new-slot call passes manager/null/-1/0. Earliest UI thread UNKNOWN |
| SOR-FN-0015 | FUN_14183c590 | 0183c590 | Higher-level request candidate; status/gates/name/file preparation. Live manager identity, option meaning and execution contract UNKNOWN |
| SOR-FN-0016 | FUN_14183c830 / FUN_141814050 | 0183c830 / 01814050 | File-object preparation and serialization wrapper; storage context is not a bare name buffer; command/wait semantics incomplete |
| SOR-FN-0017 | FUN_141814220 | 01814220 | Serializer candidate, RCX indirection observed at caller; no old SFSE prototype transfer. Large body, not a safe integration point |
| SOR-FN-0018 | FUN_14183aaf0 / FUN_14183ac80 | 0183aaf0 / 0183ac80 | Finalization scheduling, storage/rename/cache/status-clear/wake. Completion candidate, not disk/cloud durability proof |

Supporting functions and exact evidence locators remain in the report, not bulk-renamed in Ghidra. SFSE source lead SOR-S-0120 is separately credited; rejected old sites are preserved.

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
