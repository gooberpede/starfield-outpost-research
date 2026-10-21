# Function and Operation Register

## LO1 Locations -> Outpost adapters and metadata

[SOR-EXP-0062 / SOR-EV-0070](experiments/locations-outpost/native-and-ui.md), [export register](experiments/locations-outpost/functions.csv):141360e80/141361c10/14136c980 supply entries and base maximum;14135e270/14135f0e0/14135fcc0 refresh selected-body/system data;14135d890/140aba950 select location-owner faction;1416aacd0/1416aab70 and1413630c0/14136cf60 supply schematic and galaxy-marker data. Preferred image base 140000000, pinned retail 1.16.244.0. STATIC/OBSERVED-INTERNAL only; no safe invocation or persistence guarantee.

## C3 fuel accounting and readiness

[SOR-EXP-0046 / SOR-EV-0054](experiments/cargo-links/fuel/native.md),
[exact locators](experiments/cargo-links/fuel/functions.csv): native Papyrus
`14206ab30` passes mode 0 to `140f7d120`; scheduler `140f7f1e0` passes mode 1.
`140f7d030`, `140f7f6f0`, `140f881c0` and `140f7d6a0` connect category, incoming
sources, whole-recipe cap and source inventory withdrawal. PEX CargoLinkCanProduce
queries either non-mission endpoint; timer 2 repeats arrival/unload. Base image
`0x140000000`, retail 1.16.244.0, STATIC / OBSERVED-INTERNAL; no safe API claim.

[D1 point-query/condition cross-references](experiments/disappearing-deposits/native.md)
add N71/N72 to the existing native-availability CSV (72 entries). Existing native
evidence is reused; no new native export, invocation or integration point.

[Native output contract](experiments/native-availability-map/output-contract.md) is the concise entry point for calculation, three cached populations, identity ownership and asynchronous UI consumption. [Preview/established paths](experiments/native-availability-map/output-paths.md) distinguish static convergence from runtime equality. That stage added N67–N70 constructor/teardown/reset records (70 at that stage; D1 adds N71/N72); [completion assessment](experiments/native-availability-map/completion-assessment.md) is CONDITIONALLY COMPLETE for this reference endpoint, not general safe invocation.

## EXP0034 continuation — local inorganic native boundaries

[Resource-region lifecycle continuation](experiments/native-availability-map/region-dependencies.md) extends this register in place with current-context source indexing, task requests/dependencies/publication and ProcGen reset/destruction. [Location/state requirements](experiments/native-availability-map/region-requirements.md) and [review](experiments/native-availability-map/region-review.md) delimit sufficiency.

[Structured native register](experiments/native-availability-map/functions.csv) expands the existing SOR-FN-0060–0064 pipeline with 70 source-linked function records (local keys N01–N70, not newly allocated SOR-FN IDs). Each includes pinned executable/RVA, original name, input/output, prerequisites, effects, edges and limits. [Dataflow](experiments/native-availability-map/dataflow.md) and [minimum-input assessment](experiments/native-availability-map/minimum-inputs.md) distinguish caller-derived descriptors, internally retrieved loaded regions, provider/generation cache and asynchronous UI. STATIC/OBSERVED-INTERNAL; runtime overlay and exact scope are in the report. No safe callable API, universal freshness or established runtime equivalence is claimed.

## SOR-FN-0060–0064 — Inorganic availability pipeline

Pinned retail 1.16.244.0, preferred base 0x140000000, [exact executable hash/native domains](experiments/resource-availability/native.md). FN0060: typed AreaResources producer 141578500 and row binder 141581290. FN0061: source updater 1421e07d0 with placement 1421b41f0 and established 1421b2570 callers; XMM2 radius. FN0062: region callback 1421e0f50, qualified binary32 partial. FN0063: harvester resource consumer 1421f68f0 and property-presence 14044b610; not full placement. FN0064: generator 14079a330, conditional CRC/MT first gate only. Addresses are native VAs; RVA is VA minus preferred base. STATIC links do not establish observed invocation, universal serialization or safe integration. [Executable scope](experiments/resource-availability/schema.md).

## EXP0025 acquisition supplement to SOR-FN-0055/0056

[Contract/correction](experiments/event-instrumentation/contract.md), EV0033:
byte-checked center entry F4AB80/common exit F4AC44, grid callback entry AD0B90/common
exit AD0E94 and result AD0D3B. RBP-49 at result is pretranslation center; actual
translated X/Y are XMM0 at AD0C93/AD0C9C. Seven scoped sites with instructions
replayed in place by an external debugger candidate. Disposable qualification is
not a live hit, complete frame proof or validated integration. Historical wording
below is preserved with this correction; critical review remains required.

## SOR-FN-0056 — ProcGen lifecycle and event-associated center

SOR-ENV-0002 retail 1.16.244.0; [typed map](experiments/event-oracle/native-map.md),
SOR-EV-0032. Manager ctor 140787830 / RVA 00787830 allocates0x138 ProcGen via
14079d660 / RVA 0079d660; manager+130 owns it, destructor 14079d910. FN0054
publisher 1421b2570 is StateUpdatePlacement entry. Reset 1407a6690 clears radius
only; activation 1407a50d0 changes e8/e9; updater 1407a5210 requires e8; typed
decal predicate 1407a6540 skips distance filtering if radius<=0. Helper 140f4ab80
/ RVA 00f4ab80 always writes XYZ, common exit 140f4ac44. [Design](experiments/event-oracle/acquisition-design.md)
binds actual reference/caller/output. STATIC/OBSERVED-INTERNAL, scoped STRONG
proposed; no live freshness, safe integration or exhaustive alias-writer proof.

## SOR-FN-0057 — Preview waiting and asynchronous spinner

Same pinned build/base; [preview contract](experiments/event-oracle/preview-state.md).
Ctor 14158e280 / RVA 0158e280 and 14158f230 bind spinner/block-input.
Wait3D entry 1421b5720 is existing code/LAB, not a created function;
update 1421b5970 / RVA 021b5970 requests spinner after timer and gates advance
via readiness 14241e7f0 / RVA 0241e7f0. Exit 1421b5750 requests off through
1421f6420 / RVA 021f6420; service 1415902a0→14158fa50 updates selected UI data.
STATIC/OBSERVED-INTERNAL; no failing episode, defect diagnosis, complete
spinner-source census or live-safety finding. REVIEW-REQUIRED.

## SOR-FN-0054 — Native stored workshop terrain-center producer and bounds consumer

SOR-ENV-0002, retail 1.16.244.0. [EXP0021 contract](experiments/engine-oracle/oracle-contract.md),
SOR-EV-0029: static VA 1421b2570 / RVA 021b2570 resolves Workshop and calculates
center through 140f4ab80 / RVA 00f4ab80; writes XYZ/radius at 1421b29ac/29b1 through
terrain145fd9c30→+130→+90/+9c. Native 1407a6540 / RVA 007a6540 uses it for bounds
filtering; thunk 1407b0880, consumer installer 1407a6150, activation 1407a50d0 and reset 1407a6690
qualify lifecycle. STATIC/OBSERVED-INTERNAL only. Worker reads raw bytes without
lock/pin; no query invocation/ABI-safety or authoritative freshness claim.

## SOR-FN-0055 — Native terrain coverage selected-grid output

Same pinned module/base 140000000. VA 140ad92e0→140ad08d0→140b1e190→140ad8ec0→140ad0b90;
observe 140ad0d3b / RVA 00ad0d3b after 14096f5c0. Captures native translated center,
floor, body/resolution, input base/translation and output hierarchy. Later
142332410/14096eb90/14096f940 consume it in coverage calculations. Descriptor
140f4a140 can mutate ownership; circle/ceiling predicate 140f4ac50 is complementary
local evidence, not a planetary oracle. [Typed contract and limits](experiments/engine-oracle/oracle-contract.md).
No live hit, safe callable interface, symbol/type/comment mutation or invocation.

## SOR-FN-0052 — Typed saved-world restoration and frame selection

[EXP0020 ledger/map](experiments/static-exhaustion/call-and-dataflow.md), pinned 1.16.244.0 static VA/RVA=VA−140000000.141824a60/141825e00 unit 3 dispatch, 14132d260/14132d500 descriptor writer/reader, 1403a5560/3a5e00/3a53b0 restoration, 14096fb40/96fa90 packed key decode/encode; 141822570/14182e280 typed unit 6 dispatch; 14140ff80/1414128c0 site tuple, 140ad5f20/ad6150 world component. Typed IDs 4 versus legacy IDs 3 use distinct callbacks with 1418599a0 remapping. 1418325a0/141833b20 mask 20/cell conversion and 140ad3ed0 integer translation establish scoped saved frame. No generic full-save decoder, future live epoch or invocation authority.

## SOR-FN-0053 — Closed residual-helper and local-height branches

14077f900→140780a50→140780aa0→140781390 selects existing reference XYZ plus integer displacement; 14077e350→140780710→14077f6e0→14078d2c0 searches integer candidate overlays. 14141ccd0/14141dc70 consumes 14078d370 Z in camera/local-height calculations. [EXP0020 residual map](experiments/static-exhaustion/residual-map.md) closes these indirect/helper branches and distinguishes scalar local height from body direction. STATIC OBSERVED-INTERNAL; no exact off-grid planetary embedding or safe integration point established.

## SOR-FN-0050 — Activated overlay construction, typed definition and rebase

[SOR-EXP-0019 native map](experiments/activated-grid/native-map.csv), pinned 1.16.244.0; all entries static VA, RVA=VA−140000000.1404597a0/140459a30 load/resolve BGSWorldSpaceOverlay_Component's SFBK/body keys. 1407986d0 differences active/requested grid pairs before 140ad1660; 140ad47e0/140ad4a00 initialize typed ActivatedOverlayProperty. 140adcde0/140adccf0/140add310 register; 140ad30a0/140ada3a0 select/read; 140797dc0→140ad9cd0 subtracts terrain rebase from shifts/bounds. Factory 141881660/vtable 144b91788 inspected, no qualified wire restoration proven. STATIC, OBSERVED-INTERNAL; full saved-edge selection/continuous embedding OPEN, no invocation/integration authority.

## SOR-FN-0051 — Hierarchical grid and footprint orientation

14096ecb0 angle quantizer; 14096f4d0/14078d660 designated half-cell projection; 14096efb0 landing-origin snap; 14096f5c0 signed displacement/remainder and four-tag seam transitions; 14096eb90 canonical record lookup. 14096ae90 SFBK DNAM→Block+40/+44; 14096bba0 independent spans/remapped16×16 cache, 14096be70 cache selection, 140851d20 eight centered transforms from 145907c10. [SOR-EXP-0019](experiments/activated-overlay-and-grid-geometry.md#grid-geometry-and-topology), STATIC scoped pinned build; mathematical tests are not native/runtime seam validation.

## SOR-FN-0047 — Save-side reference frame preparation

`141856d10`, callers `14181aa30/14181af40` at `14181ae1b/14181b356`: copies own reference XYZ, selects cell/world context and conditionally subtracts `140ada3a0` translation. Static VA in pinned 1.16.244.0/base 140000000, RVA 01856d10. Predicate and frame limits in [SOR-EXP-0018](experiments/durable-outpost-center-and-object-transforms.md#transformation-map). STATIC, OBSERVED-INTERNAL; not a callable integration point or proof of every saved branch.

## SOR-FN-0048 — Activated overlay selection and translation

`140ad30a0` (RVA 00ad30a0) selects valid world-keyed inclusive-cell-bounded edges; `140ada3a0` (RVA 00ada3a0) reads typed payload+8/+0xc integer shifts and+0x30 floatZ, gated by+0x35. `140ad7b80/140add310/140adcfd0/140adcf50/140add850` establish named ActivatedOverlayProperty registration/copy lineage. [SOR-EXP-0018](experiments/durable-outpost-center-and-object-transforms.md#transformation-map), STATIC pinned executable; actual archive-to-selected-map restoration remains OPEN. No Workshop-offset/type conflation or approved live invocation.

## SOR-FN-0049 — Nonempty Workshop resource prefix

`140f50880/140f515a0/1402cef80/1402cedd0`: modern resource groups use separate reference queues and uint32 counts; each row consumes two refs plus 17 body bytes. [SOR-EXP-0018](experiments/durable-outpost-center-and-object-transforms.md#cross-outpost-challenge-and-nonempty-workshop-resource-tables) extends the bounded prefix to all 19 mature Workshop vectors, each zero. STATIC/SAVE, original reader callback; resource value semantics/full following extras/older versions remain unclassified. All addresses static VA, RVA=VA-140000000 in pinned build.

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
| SOR-FN-0033 | FUN_14008cb90 /14008cc50 /14096e060 /14096da90 | 0008cb90 /0008cc50 /0096e060 /0096da90 | Defaults 10+2, ordinary R 256; actual other configuration required |
| SOR-FN-0034 | FUN_14096ecb0 /14096f4d0 /14096efb0 | 0096ecb0 /0096f4d0 /0096efb0 | Quantizer, centred indices, origin snap; no visible-tile dimensions |
| SOR-FN-0035 | FUN_14078d1f0 /14078d660 /1423321f0 /142332410 | 0078d1f0 /0078d660 /023321f0 /02332410 | Local floorXY/origin displacement/projection; angle omits fractionalXY/Z |
| SOR-FN-0036 | FUN_140ad7200 /140ada960 /140ad40c0 | 00ad7200 /00ada960 /00ad40c0 | Keyed activated-overlay integer XY*100/vertical translation; restored map unqualified |
| SOR-FN-0037 | FUN_1418325a0 /141833b20 /140b4e410 | 018325a0 /01833b20 /00b4e410 | World/initial flags/restoration/rebase; final authority unknown |
| SOR-FN-0038 | FUN_140910690 /1407bcfb0 | 00910690 /007bcfb0 | Cached/active-world/fallback; body-space consumer also quantizes; no subcell proof |
| SOR-FN-0039 | FUN_140ad1660 /140ad47e0 /140ad4a00 /140add310 | 00ad1660 /00ad47e0 /00ad4a00 /00add310 | ActivatedOverlayProperty creation/registration; saved linkage unknown |


## SOR-EXP-0014 terrain-frame bridge

SOR-ENV-0001 / SOR-EV-0020, pinned Starfield 1.16.244.0, preferred base `0x140000000`. [Operand locations, input gaps and export identities](experiments/two-outpost-site-anchors-and-beacon-coordinates.md#coordinate-transformation-investigation). STATIC / OBSERVED-INTERNAL / REVIEW-REQUIRED; no native invocation, callable ABI, complete branch coverage or safe integration. World creation/registration and terrain queries have effects if executed; only existing analysis state was exported here. In-memory offsets are not wire offsets.

| ID | Original static VA | RVA | Supported observation and limit |
|---|---|---|---|
| SOR-FN-0029 | FUN_140ad31a0 / FUN_140ad30a0 | 00ad31a0 / 00ad30a0 | Exterior cell/world selection with inclusive integer XY bounds. Does not prove saved parent is a loaded cell or identify one universal overlay. |
| SOR-FN-0030 | FUN_140ad3b20 / FUN_140ad3c30 | 00ad3b20 / 00ad3c30 | Eligible world/component path resolves body and searches overlay by world ID, copying two doubles. Retrieves an anchor without adding reference XYZ. |
| SOR-FN-0031 | FUN_14077fc20 / FUN_14078d370 | 0077fc20 / 0078d370 | Branch combines terrain-index displacement and reference position, splits XY into grid offsets and residual with factor 100, and projects indexed point to angles. Manager origin/resolution and precise residual projection remain unresolved. |
| SOR-FN-0032 | FUN_1418ab8d0 / FUN_140ad0400 | 018ab8d0 / 00ad0400 | Conditional pair registration with existing world or generated-world construction. No proof of the branch actually used by Save25 or a universal one-overlay-per-outpost rule. |

## SOR-EXP-0013 surface-anchor chain

SOR-ENV-0001 / SOR-EV-0019, Starfield 1.16.244.0, preferred base `0x140000000`; executable hash and [exact data flow/limits](experiments/planetary-surface-anchor-semantics.md#decisive-native-and-definition-chain). STATIC / OBSERVED-INTERNAL / REVIEW-REQUIRED. No callable ABI, safe integration, live invocation or project renaming. Full exports remain LOCAL-ONLY; important instruction/decompiler limits are indexed.

| ID | Original static VA | RVA | Supported observation and limit |
|---|---|---|---|
| SOR-FN-0023 | FUN_141686a00 | 01686a00 | Ray/sphere hit in inverse body orientation; atan2(y,x), atan2(z,horizontal norm), two double stores. Float intermediate stages; geographic datum uncalibrated. |
| SOR-FN-0024 | FUN_140ad0650 / FUN_140ad55b0 | 00ad0650 / 00ad55b0 | Overlay path copies pair/world ID; named formatter uses second Lat, first Lon. Exact beacon position not supplied. |
| SOR-FN-0025 | FUN_140779300 / FUN_140771ac0 | 00779300 / 00771ac0 | Supplies planet/body identity and two-double/world-ID tuple to CTPlanetOverlayData insertion command. Full wire serializer not established. |
| SOR-FN-0026 | FUN_1407772c0 / FUN_140774ee0 / FUN_140777560 | 007772c0 / 00774ee0 / 00777560 | Command callback, component-store comparison/copy at in-memory +20/+28/+30; those are not save offsets. |
| SOR-FN-0027 | FUN_14076ec00 / FUN_140773090 | 0076ec00 / 00773090 | Pre-BDST CNAM 20-byte latitude/longitude/world records swapped into overlay tuple. Main loader instruction cap; full decompilation plus fixed byte comparisons retained. |
| SOR-FN-0028 | FUN_1416874f0 / FUN_142332410 / FUN_1423321f0 | 016874f0 / 02332410 / 023321f0 | Selected pair can be adjusted through terrain indices/direction projection. Exact local-beacon bridge is a follow-up, not a decoded global transform. |

## SOR-EXP-0010 conditional restoration and ownership readers

SOR-ENV-0001 pinned Starfield 1.16.244.0, preferred image base 0x140000000, SHA-256 `7e9adb1414a8e1b325e5e1f097b9b17b78deb7eebeda37a333351a43a60f9d28`; SOR-S-0127 / SOR-EV-0016. [Exact supporting observations and limits](experiments/active-outpost-membership-completion.md). STATIC / OBSERVED-INTERNAL / REVIEW-REQUIRED. These loader functions mutate reconstructed objects when the game executes them; this task only reads existing instructions and never invokes them. No safe integration point, complete caller set, live ABI or authoritative player-membership predicate is established. Original Ghidra names are preserved.

| ID | Original static VA / name | RVA | Supported observation and limitation |
|---|---|---|---|
| SOR-FN-0019 | FUN_141832f00 | 01832f00 | Conditional REFR initial-case selector; flags 0x92018200 select6. Does not resolve inherited form type or ownership. |
| SOR-FN-0020 | FUN_141835610 / FUN_141835c20 / FUN_1405dfa40 | 01835610 / 01835c20 / 005dfa40 | Paired initial readers and general form loader; separate queue/body consumption, self ref and bit 0-gated saved flags. Omission preserves an unresolved inherited/default state. |
| SOR-FN-0021 | FUN_14054c2f0 / FUN_14053a2d0 | 0054c2f0 / 0053a2d0 | ExtraPromotedRef0x84 counted ref/byte pairs versus ExtraOwnership0x1f; player promotion ref is not an owner field. Inherited ownership and actual execution remain unvalidated. |
| SOR-FN-0022 | FUN_140f3bfc0 | 00f3bfc0 | Exclusion-property query through reference+0x68 with global 145f0c6d0. Resolved keyword/FormID and equivalence to BlockPlayerActivation unknown; no complete player-control proof. |

## SOR-EXP-0002A save-path candidates

SOR-ENV-0003 / SOR-EV-0005, STATIC / OBSERVED-INTERNAL, REVIEW-REQUIRED. All Starfield 1.16.244.0 addresses below use preferred base 0x140000000 and the pinned hash in [the detailed candidate map](experiments/SOR-EXP-0002A-native-save-thread-mapping.md#current-candidate-map). That map records call sites, provisional argument roles, strings, side effects and limits. No candidate was observed executing in a manual save; debugger setup is not native invocation qualification.

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
| SOR-FN-0003 | SOR-ENV-0001 | Starfield.exe / ObjectReference | 0x142073dc0 | RVA 0x02073dc0 | FUN_142073dc0 | GetWorkshopOwnedObjects callback | Registration FUN_14209bc00 loads callback at 0x14209bc4b; output collection/owner filtering lead; no exhaustive enumeration claim | PROVEN STATIC binding; full behavior UNKNOWN | SOR-EV-0001; ObjectReference.psc: 568 |
| SOR-FN-0004 | SOR-ENV-0001 | Starfield.exe / ObjectReference | 0x142074870 | RVA 0x02074870 | FUN_142074870 | GetWorkshopResourceObjects callback | Registration FUN_14209ba00 loads callback at 0x14209ba4c; larger body export capped; parameters/source declaration not ABI proof | PROVEN STATIC binding; full behavior UNKNOWN | SOR-EV-0001; ObjectReference.psc: 575 |
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

## SOR-FN-0058–0059 — Saved owner and item reconstruction paths

2026-10-14, [native dependency ledger](experiments/workshop-membership/dependencies.md), SOR-EV-0040. Pinned Starfield.exe SHA256 7e9adb1414a8e1b325e5e1f097b9b17b78deb7eebeda37a333351a43a60f9d28, preferred base 140000000. SOR-FN-0058: GetWorkshop 142073cf0→140517d60,4C loader 140562ef0, construction 1421dd600→140f3cf40 and separate deletion 1421de660. SOR-FN-0059: 1421c71b0 existing-reference item builder, foundation predicate 140f5f2d0, group collector 140f366c0, reverse filter 140f44c00, compound builder 1421cbac0, root selector 1421cb740 and setter 140f661e0. Reads/writes, identity domains, callers, mask/default gaps and source locators are in that ledger. STATIC/OBSERVED-INTERNAL only; no live lifetime/calling qualification, database edits or mod interface authority.

## EXP0033 — Membership, registration and component restoration corrections

[Native route map](experiments/workshop-population/routes.md):140517c00/140500ba0/140cf72d0 resolve quest/ALLA aliases; 140518750 derives reverse 4D; 141815620 assigns actual record types from ordered footer runs; 14181cdc0/14181ce30 gate AddChange; 14182e280 restores components; 140b1e720 resolves CalculatedPackinData existing instance IDs. Type 4 selector 1421661c0 requires an existing owner, and generic reconstruction is not categorically ships-only. Static VAs/build pins in report; no safe runtime integration claim.

## SOR-EXP-0035 — prospective resource observation boundaries

[Native dependency ledger](experiments/continuous-beacon-preview/native.md) requalifies producer 1421e07d0, preview CALL1421b42e3, UI 141578500 and its two actual union/two row construction branches against the pinned retail executable. Getter14038a050 and typed payload layout are independently byte-qualified. STATIC / OBSERVED-INTERNAL; disposable ABI qualification is not a validated retail integration. Addresses and pointer/FormID domains remain explicitly distinct.

The separately approved [live continuation](experiments/continuous-beacon-preview/live-scientific-report.md)
directly observes the producer/preview/UI/consumer/row routes in this pinned
session. RUNTIME / OBSERVED-INTERNAL within the guarded ten-CALL surface;
recording success does not establish a supported or generally safe mod API.

## SOR-EXP-0036 — passive source/provider observation surfaces

[Native map](experiments/local-readiness/native-map.md) extends observation of the
existing SOR-FN-0060–0064 pipeline: RVA 021e0a46→021e0f50 captures the source-value
slot/closure during a natural scan; 007b526a/007a1a3c→0079f860 captures provider
boundaries. Exact pinned build, guards, ABI channels and limitations are retained.
STATIC/OBSERVED-INTERNAL, disposable qualification only. Continuation/return bits
are not spatial acceptance or generation-success certificates; no new live calls.

The [reassessment](experiments/local-readiness/scientific-value-reassessment.md) rejects the proposed live session without changing these native contracts.

## Experiment A geometry ownership continuation — 2026-10-16

[Ownership map](experiments/spatial-equivalence-feasibility/geometry-lifetime/ownership.md) and [operand map](experiments/spatial-equivalence-feasibility/geometry-lifetime/operands.md) extend the existing SOR-EXP-0034 consumer account. On the pinned retail build, RVA 007ac2f0 appends a 0x30 region through the native allocator and invokes 007ac0d0 to copy ordered 0x10 XYZ-width records into destination-owned storage; 007ac260 frees each point buffer then outer region storage. Resource/source wrapper final-release chains run through 007aab10 and 007aa8a0. STATIC / OBSERVED-INTERNAL; aliases are analyst descriptions. Shared +40 excludes mapped construction/reset, while owner destruction 0079d910 and manager cleanup 00788bc0 have no demonstrated acquisition/fence protecting an observer snapshot. This is a scoped lifetime gap, not observed concurrency failure. Exact source hashes/RVAs and remaining caller/alias limits are in the linked ledger. No callable integration or persistence classification is promoted.

## SOR-EXP-0038 — E1 inorganic extractors

The existing [native-function CSV](experiments/native-availability-map/functions.csv)
now includes N73–N94, with pinned preferred VA/RVA, original names, operand/output
contracts, side effects and decisive exports. [Native reference](experiments/inorganic-extractors/native.md)
maps powered mask 40, separate halted predicate, current reason-code evaluation,
producer-row scheduling, interval/modifier dispatch and unit creation.
[Link reference](experiments/inorganic-extractors/links.md) maps destination-keyed
incoming-source storage and direct outgoing destinations, add/remove and save/load.
All are STATIC / OBSERVED-INTERNAL, analyst aliases REVIEW-REQUIRED. No callable
integration or actual current operating values are claimed.

## SOR-FN-0061 — organic selector, application and input contracts

[SOR-EXP-0039 native map](experiments/organic-facilities/native.md) extends the existing [native CSV](experiments/native-availability-map/functions.csv) with planet/species/knowledge candidates, domesticability/resource admission, recipe-keyed UI, resource AV application, upstream input availability/consumption and incompatible-link pruning. Preferred VA/RVA, exact local exports, operand/output and effect contracts are retained there. STATIC / OBSERVED-INTERNAL, proposed STRONG within the pinned build; no safe invocation, current-state observation or integration qualification.

## E3 fabricator generic catalogue and compatibility - 2026-10-17

[SOR-EXP-0040 native reference](experiments/fabricators/native.md) extends the existing [native CSV](experiments/native-availability-map/functions.csv), N225-N234, with generic catalogue callback 140f8be60, fallback/property callbacks, first selected source-product set and ingredient compatibility, transfer endpoint policy and topology wrapper. Existing E1/E2 AVIF loader and producer/selection/scheduling functions are reused explicitly. Each new row pins retail 1.16.244.0 VA/RVA, original FUN identity, arguments/results/effects, prerequisites, callers and private source export. STATIC / OBSERVED-INTERNAL, proposed STRONG scoped; no safe invocation or runtime qualification.

## SOR-EXP-0041 - P1 electrical machinery

[Native contracts](experiments/power/native.md), [generation/fuel](experiments/power/fuel.md) and [registry](experiments/native-availability-map/functions.csv) identify contribution, connection predicates, typed graph mutation/traversal, cumulative allocation, switching, powered state, save loading and cached UI power. New rows carry preferred VA/RVA, exact local exports and effects. STATIC / OBSERVED-INTERNAL, REVIEW-REQUIRED; no safe invocation qualification.

The [focused P1 follow-up](experiments/power/followup.md) appends N270-N292
to the same CSV: deque insertion/rotation, owner-root enumeration, cell-context
resolution, pending open-state work, ExtraAction writers and reference default/
current-open restoration. Original P1 rows remain historical; the follow-up
corrects the queue/discovery-vector interpretation with instruction evidence.

The [load continuation](experiments/power/load-determinism.md) appends N293-N312
to that same CSV: flag restoration, association rebuilding, FormID versus
handle resolution, global-data finish, actual object-loaded sink binding,
ordered notification restoration and unresolved-owner cleanup. STATIC /
OBSERVED-INTERNAL; no safe invocation or settled-outcome qualification.

## SOR-EXP-0042 - inventory and local-link eligibility

[S1 native register](experiments/storage/functions.csv) and
[contracts](experiments/storage/native.md) retain preferred VA/RVA, original
function names, exact export locators, owner/weight/capacity, source/pair/UI gates,
inventory serialization and Transfer Container access paths. Reuse E1-E3/P1
production/input/link contracts rather than duplicating or changing their aliases.
All new interpretations STATIC / OBSERVED-INTERNAL / REVIEW-REQUIRED;
no public ABI, safe invocation or integration is qualified.

## S1 capacity continuation

[Native derivation](experiments/storage/capacity-native.md) and appended S1C rows
in [the register](experiments/storage/functions.csv) trace effective capacity,
weight/cache/invalidation, MISC mass loading, generic versus local receiving and
actual transfer descriptors. STATIC / OBSERVED-INTERNAL / REVIEW-REQUIRED;
current live values and safe invocation remain unqualified.

## C1 cargo configuration/UI

SOR-EXP-0044 / SOR-EV-0052. [Native contract](experiments/cargo-links/configuration-ui/native.md) and [exact function locations](experiments/cargo-links/configuration-ui/functions.csv) cover menu setup/candidates/picking, direct-successor recipe needs, outbox iteration, ship weight, UI binding and 4C/Extra33 restoration. Static VAs use image base0x140000000 with explicit RVAs. OBSERVED-INTERNAL only; no invocation, live validation or safe integration claim.

## C2 cargo transfer, timer and native travel

SOR-EXP-0045 / SOR-EV-0053. [Exact native locations](experiments/cargo-links/transport/functions.csv), [inventory contract](experiments/cargo-links/transport/inventory.md), [clock/modifiers](experiments/cargo-links/transport/timing.md) and [travel/recovery](experiments/cargo-links/transport/lifecycle.md) trace registration-to-mutation, timer producers/dispatch/persistence and concrete path-completion providers. Preferred static VAs, image base0x140000000, explicit RVAs. OBSERVED-INTERNAL only; no safe invocation/ABI/hook or universal flight-duration qualification.

## C2 transit continuation

SOR-EXP-0045 / SOR-EV-0053, 2026-10-18. [Additional native locators](experiments/cargo-links/transport/transit-functions.csv) and [movement map](experiments/cargo-links/transport/transit.md) trace reference/component elapsed dispatch through 1412aeb90/1412aee90/1412af0e0 to 1427342e0, detached thresholds, full MotionStage 14271e190 and path-clear completion. Definition 15/5 calendar settings and movement profile providers are separated. Preferred static VA/RVA for pinned EXE; OBSERVED-INTERNAL, no safe invocation or historical admission proof.

## CR1 recruitment, capacity and Crew providers

SOR-EXP-0047 / SOR-EV-0055. [Exact function/export register](experiments/crew/functions.csv), [capacity](experiments/crew/capacity.md), [lifecycle](experiments/crew/lifecycle.md) and [native-to-movie dataflow](experiments/crew/screen.md) cover ordinary registration, cost/capacity predicates, script bypass, effects/travel boundaries and UI row admission. All locators are static VA/RVA for the pinned executable; OBSERVED-INTERNAL only, no safe invocation or live verification.

CR1 allocates SOR-FN-0062 through SOR-FN-0071 to the ten named operations in
[functions.csv](experiments/crew/functions.csv); remaining exported addresses are
version-qualified locators without new semantic record IDs.

## CR1 current-assignment continuation

CR1 current persistence correction: [writer/load/fixup/consumer chain](experiments/crew/current-assignments.md#producer-wire-loader-fixup-and-consumer) adds actual14051ea30 caseE2, Actor141917e40 private header, registry14130ce90 writer,14130d540 reader,14130d650 fixup and141825820 type6 stream. Exact primary export/function lines are in current-sources.csv; no safe invocation or new ID allocation.

## CR2 selected-rank and process-specific consumers

SOR-EXP-0048 / SOR-EV-0056. [Function/export locators](experiments/crew-skills/functions.csv) and [causal map](experiments/crew-skills/native.md) cover registration140ca3910, dispatcher140c93cf0, timer140f7bd20, power140f3dd50, ship selector1404095c0, ability refresh14040a9d0, combat141b30b30, inherited perk copier140cd77d0 and saved rank writer/reader1412b60a0/1412b6eb0. Preferred static VA/RVA for pinned build only; OBSERVED-INTERNAL, no invocation/ABI/hook safety claim.

## R1 robot construction and shared modifier paths

[SOR-EXP-0050 native locators](experiments/robots/functions.csv) pin instruction-backed recipe-global count `140f3b170`, status `1421dcb10/140f3f9a0`, ordinary build `1421b2360/1421b2e20`, selected-owner registry `1421c6f90`, insertion `1421c6890` and removal `1421c6b90/1421c77b0`. [Limits](experiments/robots/limits.md) separates these from shared E2/A1/DB and actor restoration. OBSERVED-INTERNAL, no safe invocation guarantee.

## L2 budget, accounting and footer consumers

[SOR-EXP-0052 / SOR-EV-0060 native register](experiments/build-budget/functions.csv)
pins form calculator140f4c7f0, reference filter140f4c770, single/assembly
getters140f64b00/140f6e260, candidate cache140f33180, gate1421dcb10,
add/subtract140f4c980/140f4ca70, BF1419aec20/1419aeff0 and
ratio140f4cb70 -> statistics1421f2cb0 -> footer14143f690/8a0/fb40.
[Causal explanation](experiments/build-budget/native.md) separates static VAs,
object offsets, saved offsets and identity domains. OBSERVED-INTERNAL;
no safe invocation, hook, mod ABI or runtime measurement is established.


## SD1 container/display native contracts - 2026-10-19

[SOR-EXP-0055 / SOR-EV-0063](experiments/containers-displays/native.md), [pinned function/export register](experiments/containers-displays/functions.csv):1404321f0 display admission;1412ffae0/1412ff580 creation/owner transformation;140643360 inventory conversion;141eb01a0 and140b66680/140b67380 menu transfer reasons;1419a3330 equipment;140641180/140641320 saved row state;140b7d5b0 equipment reconstruction;1412fd300/1412fd450/1412fd650 display writer/load/fixup;1421de660/140b61610 ordinary scrap transfer. Preferred static VAs only, matching pinned image/base; OBSERVED-INTERNAL, no safe ABI/injection authority.
