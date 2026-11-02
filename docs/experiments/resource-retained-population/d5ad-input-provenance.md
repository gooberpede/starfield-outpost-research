# D5AD input provenance and readiness

2026-11-02, Australia/Sydney. [Frozen questions](../../implementation-briefs/CODEX_BRIEF_SOR_RG2_D5AD_initialization_save_load_reconstruction.md),
[active ledger](d5ad-investigation-ledger.md). Authored synthesis is
REVIEW-REQUIRED; Q1 is **COMPLETE** for the qualified ordinary
source-to-ready-input contract after independent review. Native exports,
archive members and local receipts remain LOCAL-ONLY.

**Ordinary construction can acquire and finish loading its biome/mask map at
the point of generation.** A ready Lodge checkpoint therefore cannot, by itself,
certify that every destination raster was already resident. This is a positive
compiled path, not an observation that Save52 used the deferred branch.

All native locations are preferred static VAs for Starfield 1.16.244.0, image
base `0x140000000`; RVA equals VA minus that base. Member offsets are bytes.
Fresh export `D5AD-EX03` is `.local-work/d5ad-inputs/export03/native.tsv`,
SHA-256 `a77f62bb43ab82cc4a7a81d3f8d3e9f32c3373306a45765d12e65d0f430ebe2d`.
The command and generated owned exporter beside it record exact targeted inputs.
The unchanged core-database-pin check passed after export. Read-only Ghidra
still reported removal of an old temporary presave file; this side effect is
recorded in its local stdout log. The investigation does not claim zero writes
to the original database directory. Subsequent exports moved to a verified
disposable project copy; no manual restoration or cleanup of the original ran.

| Necessary input | Source and upstream producer | Readiness, owner and consumer | Qualification / open dependency |
|---|---|---|---|
| Biome identity and mask raster | Body-name component → `0x140478350` builds plugin-qualified `PlanetData/BiomeMaps` resource key; `0x140478a30` acquires/creates BiomeMapDB entry; `0x140478030 → 0x14047a2b0 → 0x14047a930` opens and decodes map/face arrays. | Entry `+0x20` owns map; map `+0x18` owns faces, stride `0x30`; face `+0x10` contains identity array and `+0x20` mask bytes. Generator `0x14079b520` acquires entry and only continues for ready/claimed-load outcomes; sampler `0x142339340` reads low nibble. | Native path supports deferred synchronous loading and fallback. Actual historical file priority, runtime effective map and branch timing remain unobserved. |
| Source Grid and index | Landscape initialization `0x1407847b0` allocates ordinary/overlay/MultiFiles Grids; `0x140785190` selects current descriptor, traverses base blocks through `0x140784c40`, adds overlays and finalizes Grids. | Reference-counted landscape Grid owners; terrain holder interfaces link file access. Completion writes landscape `+0x60 = 1` after Grid finalization. Source constructor `0x140982d90` copies geographic definition/anchor data and derives token. | Constructed Grid/index does not imply populated resource output or complete file/density readiness. Initialization can take an unsuccessful holder path. |
| Surface hierarchy and definitions | PNDT's linked SFTR can supply the existing tree through `0x14096b8e0`; a missing tree plus creation permission takes allocation and `0x14096e060`. SFTR loaders install faces/slots, and SFPT forms enter the typed registry before style selection. | `0x14096e060` can acquire the same biome map, then builds hierarchy selections using body/system/surface-seed inputs and eligible SFPT registry entries. SFBK resolution and fallback feed source construction. | [Qualified native chain](../resource-pattern-selection/native.md) distinguishes precomputed tree reuse from reconstruction. Effective registration order, seed and historical mutation are separate inputs, not inferred from file order. |
| Geographic descriptor and source metadata | Current manager descriptor selects ordinary or mode-3 frame; generator `0x140771f30` looks up body and BIOM match through CTPerBiomeData storage. PNDT PPBD/optional CSV and typed creation/copy supply the component; startup population supplies its resource slots. Source constructor copies geographic descriptor fields into source. | Generator exits if metadata lookup fails; selected source/BIOM and manager context remain separate inputs. | The startup producer and retained component boundary are traced below; descriptor save restoration is treated separately in the save-state matrix. |
| Resource relationship dictionary | `0x1407bc300` acquires component-storage reader and calls `0x1407bc3d0`, which builds a temporary root-to-array map from CTPerBiomeData. Generator resolves listed resource FormIDs with `0x1405de3b0`. | Native form-type `0x9f` checks distinguish valid IRES; RSGD type `0xab` supplies per-resource generation entries. Six nonzero slots append to staging; nonzero root exchanges staging with its map entry. | This is a derived temporary map, not a dictionary loaded directly from a file or save. Component initialization and effective override sequencing remain material. |
| Initialized per-biome resource slots | PNDT PPBD and CSV component builders initialize root/slots to zero; `0x140779760` later clears/populates them through BIOM/RSGD/IRES selection. Typed PNDT callback `0x14077c470 → 0x140779610` reaches this initializer through the retained component-storage context. | Root `+0x50`, ordinary descendants `+0x54..+0x60`, Special `+0x64`, first BIOM-local rarity-6 resource `+0x68`. Queued component creation/copy preserves these fields. Initializer uses PNDT `+0x50` raw seed input and atmosphere occupancy, with per-component seed fallback when that input is zero. | [D4E producer evidence](../resource-slot-provenance/native.md) supersedes D4C's earlier unqualified slot projection. The normal startup dispatch is traced below; effective historical operands and exceptional reinitialization remain separate. |
| Effective IRES/RSGD and related forms | Plugin enumeration creates TESPackedFile objects in the handler file list; startup's ordinary file loop dispatches their concrete open method. Typed record loaders consume plugin records; generic `0x140594980` dispatches virtual `+0x88`, and `0x14059e000` distinguishes allocation/registration from loading an existing override. | IRES primary table `0x144b6f0b0` dispatches to `0x1409e7900`; RSGD table `0x144b6fd98` to `0x1409eed50`. Global postlink iterates the relevant form types and dispatches virtual `+0xf8` before returning. | The concrete TESPackedFile binding corrects the earlier base-stub ambiguity. Effective historical plugin/override selection remains an input, not inferred from the installed main file. |
| Effective rarity settings | Registered constructors and main GMST DATA reader `0x140684160 → 0x140684b30` populate mutable setting `+0x08`; command/text route reaches same setter. | Ordinary generator reads actual setting payloads for inactive rarity branches. | [Prior native account](../resource-selection-operands/native.md) proves EXE Exotic default differs from main ESM DATA; no historical override-order inference is made. |
| Persisted PCM seed, content and placements | Global type 7 restores PCM seed `+0x420`, PNDT-keyed content `+0x360` and world/cell placements `+0x3e0`. Ordinary revert drains work and clears these maps before restoration. Existing content/placement entries can be reused; missing or aged state has separate generation/refresh paths. | Content consumer `0x1418ad2b0` can reconstruct and activate its missing world. Placement consumer `0x1418aa1c0` feeds `0x14079da80`; worker `0x1407b5bd0` incorporates accepted definitions, positions and IDs into preparation, performs four subpasses, then publishes its ready collection. PCM demand reseeds working MT from saved PCM seed plus PNDT/cell operands. | The [state matrix](d5ad-save-state-matrix.md#pcm-lifecycle-consumers-and-the-ordinary-load-boundary) traces readers, writers, lifecycle and exact Save52 contents. Saved content is a material preparation input, not a saved image of ProcGen's visited array or resource collections. Resolution, age/flags, settings and asynchronous scheduling remain separate guards. |
| Terrain/file and density prerequisites | MultiFiles holder installed by `0x1407847b0`; acquisition/queue paths documented in [D5W](d5w-normal-path-model.md). Terrain window `0x140783080 → 0x140998fc0 → 0x140999120 → 0x140993110` reaches block acquisition. | TerrainDB has independent entry state, PageStitch/PageTransform or streaming dependencies. Layer/BaseProcGenDB entries are separate; `0x14076c560` builds density levels and publishes the aggregate only after claiming its entry. | Readiness must be checked in its owning subsystem. A source index, cached file pointer or one completed parent cannot certify every future block. The positive operand/consumer boundary below separates physical height decoding from the numeric resource-generation inputs. |

## Definition loading and postlink readiness

The generic record path is concrete: `0x14059e000` allocates a new form through
`0x14059d6e0`, loads it through `0x140594980` and registers it through
`0x140594ad0`; its existing-form route loads the existing receiver. The loader
wrapper calls receiver virtual `+0x88`. PE/RTTI independently binds IRES to
primary table `0x144b6f0b0` and RSGD to `0x144b6fd98`. Their load slots are
`0x1409e7900` and `0x1409eed50`, respectively. IRES SNAM's low byte becomes
rarity `+0x110`; RSGD installs generation entries and tagged resource references.
The postlink helpers `0x1409e8570` and `0x1409efb20 → 0x1409efc60` remap and
resolve references in the owning plugin/master/light namespace. Invalid
resource references resolve to null rather than proving a valid IRES.

The startup definition driver `0x1405994a0` calls global postlink
`0x14059ac20`. Its per-type job construction covers types below `0xdc`, including
IRES `0x9f`, BIOM `0xa0`, RSGD `0xab`, SFPT `0xb5` and SFTR `0xb6`.
The SFPT/SFTR type bindings are independently retained in the
[surface-pattern account](../resource-pattern-selection/native.md). Its callbacks reach
`0x14058e810`, with both serial enumeration and parallel-array routes;
`0x1405b5bb0`/`0x14058e9d0` ultimately dispatch form virtual `+0xf8`.
`0x140591ae0` and the final graph operation provide the completion boundary,
rather than mere job submission. These are native order/ownership facts, not
an observation of the historical override values. Sources: `D5AD-IN117`,
`D5AD-IN132`, `D5AD-IN164..166`, `D5AD-IN175..178`,
`D5AD-IN181..183`, `D5AD-IN185..186`, and the primary report's independently
bound PE/RTTI and generic-loader receipts.

The ordinary file-open boundary uses the actual dynamic file class.
The TESFile base table `0x144b29a70` has a false-returning `+0x18` slot;
`0x14059d7c0` exits when that slot returns false. Thus its otherwise concrete
record-load body alone does not prove that a base TESFile receives ordinary
plugin bytes. The constructor `0x1405b9750` calls base constructor
`0x1405b6340` and then installs TESPackedFile table `0x144b29b80`.
Plugin enumeration `0x1405972b0 → 0x140597a70` uses that constructor and inserts
the resulting objects into handler file list `+0x1570`, the same list consumed
by `0x1405994a0`. The actual startup connection is
`0x141883440 → 0x140573090 → 0x1405972b0`: the caller at `0x141883550`
precedes the definition phase in that startup driver. `0x140573090` constructs
and publishes the data handler before plugin enumeration. Thus the ordinary
startup chain reaches the concrete file implementation before the typed load
and postlink phase, and then reaches the component-population pass described
below. TESPackedFile's `+0x18` slot is
`0x1405b5be0 → 0x1405b9950`; `+0x20` is `0x1405bb020`, testing whether its
stream at `+0x378` is nonnull. `0x1405b7310 → 0x1405b68d0` also reaches these
virtual open/read methods. The concrete open helper returns low byte one only
after success; failure returns low byte zero and stores an error classification
(including missing-file/permission errno branches). Consequently the main
file-loop guard has a positive ordinary-open path and an explicit failure exit;
it is not a ready-input assumption. The helper is retained in the save
specialist's `swap-export02`, SHA-256
`98d2659f4da103c2302e9d49b50d4c5b8cdddc92f57d4b4577afc76b7b05cb99`.
The inspected `0x1405a3cc0` creates default forms, while `0x14059d540` tunes
stream buffers; neither substitutes for ordinary plugin ingestion.
The separate reconstruction worker
`0x141804c70 → 0x14060d920 → 0x14060dbe0 → 0x140609d20`
does reach generic record loading, but has save/reconstruction callers and is
not relabelled startup ingestion. Its missing-file-stream branch reaches
`0x14060b6d0`, separately from its physical-stream route.
Sources: `D5AD-IN197..216`, exports `D5AD-EX31..37`; `D5AD-IN215` is the
constructor window in `.local-work/d5ad-save/swap-export01/native.tsv`, and
`D5AD-IN216` the concrete open helper in
`.local-work/d5ad-save/swap-export02/native.tsv`. The exact file hashes and
function line ranges are in the source ledger. No scientific absence follows from the
base stub; the concrete class supplies the material ordinary-file branch.

## Deferred map loading and failure controls

`0x140478a30` calls the DB cache acquisition helper and constructs a new typed
entry when required, with initial state at entry `+0x14` and a null map pointer.
Existing entries are reused through their state machine. `0x1427d4be0` waits
while another load owns the entry, can claim it with an atomic state change,
returns `6` for the claimed path and `0` for a ready state. In the generator,
the claimed path calls `0x140478030`, then publishes completion with an atomic
state update and `WakeByAddressAll`. Other results bypass the generation body.
The entry is released after use. Numeric state-return meanings here describe
these concrete branches; they are not universal BSResource API declarations.

The file loader accepts resource-open result `0` or `6`, constructs a map and
reads its version, catalogue, face dimensions, identity arrays and mask arrays.
Identity values are remapped through owner/plugin context and resolved as BIOM;
invalid forms select DefaultBiome. Missing map or invalid face populations can
select an initialized default map. Consequently, missing file data cannot be
reported as an empty-resource result without following this fallback. Loader
read-state checks and version branches are retained in the raw export; no claim
that every malformed file is safely handled follows from the ordinary path.

This supplies a meaningful compiled counterexample to both “all map data must
be resident before demand” and “failed file lookup means no biome.” It does not
supply an executed fixture for the entire loader.

The [owned native control](../../../research/resource-retained-population/d5ad_readiness_control.py)
executes the original `0x1427d4be0` helper against six synthetic uncontended entry
states in a disposable Python process. All six expected transitions pass:
initial and retry classes can claim loading, the two tested completed-state
classes return zero, and the flagged single-reference branch returns without
claiming. A zero helper return is not, by itself, a decoded-payload validity
certificate. Other synthetic entry words remain unchanged. No wait/recovery
call, stream decode or real concurrent
loader executes. Receipt `.local-work/d5ad-inputs/readiness02/control.json` pins
the exact code, script and PE reader. This independently challenges the claim
that entry existence alone means ready. The initial framing guard incorrectly
expected a final RET and refused execution before allocation; inspection showed
the shared RET at helper offset `+0xb3`, followed by another branch. The corrected
guard and successful run preserve that distinction.

## Independent input counterexample

The [effective-setting investigation](../resource-selection-operands/native.md)
records EXE Exotic default `0.01` and main ESM GMST DATA `0.05`, with separate
native constructor, DATA reader and setter paths. A reconstruction that uses
only executable defaults can therefore give a different rarity weight despite
the same geographic mask. This is independent installed-definition evidence;
neither value alone establishes the historical effective Save52 setting.

## Grid, terrain and density preparation

The normal startup branch of `0x14187f9d0`, selected by initialization state
zero, calls `0x141893ee0` before signaling its completion event and notification
5. That initialization reaches `0x1409518b0`; when the StarField module singleton
is absent, it constructs the module and calls `0x14094e3d0`. After optional CSV
work and component maintenance, `0x14094ef57` enumerates typed PNDT forms through
`0x140593280`, using table `0x144b3d9e8`. Its callback `0x14077c470` requires
form type `0xba` and calls `0x140779610 → 0x140779760`. Thus this resource
population pass has a concrete startup producer. A reused module can skip its
construction branch; a save load is not automatically another module creation.
These are native ordering constraints, not measured B1/B2 initialization times.

Source Grids use a concrete MultiFiles Grid, whose table is `0x144b3e0b8`.
Its master preparation method `0x140782070` constructs a `Data/Terrain/` name
from the world or its redirect at world `+0x388`, creates a MasterFile and calls
its initialization slot `+0x18`. That path string is not a disk-read witness.
The actual MasterFile table `0x144b3dea0` binds this call to `0x14099ab90`.
Its virtual `+0x58/+0x60` checks both bind to `0x1402b75d0`, which returns true;
`0x14099ad20` allocates and initializes metadata arrays for nonzero dimensions.
These concrete methods do not open a physical terrain stream. Preparation
`0x14099acd0` computes LOD dimensions and optional min/max state, then sets its
prepared byte. The optional min/max helper returns immediately when its height
storage at `+0x38` is null. Physical block acquisition remains a distinct branch
below rather than a presumed prerequisite of this synthetic master metadata.

Grid finalization `0x140983270` calls `0x1409832e0` to build fill, edge and
corner contributors, dispatches the modifier vector through slot `+0x18`, then
calls `0x140983880` for its further indexed/combined file state. This
explains how source descriptors become searchable without equating them with
generated resource geometry. `0x1407824b0` is a protected MultiFiles cache lookup
by an eight-byte key; its returned pointer alone is not a successful file-read
or decoded-block certificate.

The modifier vector is at Grid `+0x38/+0x40`. Constructor `0x140982390`
positively populates it according to flags with RerangeHeight, HeightAdjustment,
Alignment, Continental, OceanBiome, OverlayHeight and UpdateHeight objects.
Actual tables bind their `+0x18` methods to `0x140989730`, `0x140850ff0`,
`0x140971e20`, `0x1409754b0`, `0x140976020`, `0x140988c70` and the no-op
`0x1402b56d0`, respectively. The first six build private file-ID maps, alignment
groups or height maps; OceanBiome reads ready map water flags and nearby BIOMs.
Alignment helper `0x140972f00` consumes the separate Grid corner index at
`+0x28`, not a serialized resource list. The normal base Grid flags `0x3b`
exclude OverlayHeight's bit `0x04`; overlay Grid flags `0x0c` can select it.
Its helper `0x140989170` can update an existing world-height context and queue
later world work. That side effect remains relevant to context/lifecycle
analysis; no claim of universal absence of indirect resets follows.

The inspected ordinary numeric construction path is
`0x14079b520 → 0x14079c470 → 0x14079a330`. Its operands are the transformed
geographic query and map sample, source XY/dimensions, selected ordered IRES/RSGD
data, seed/settings and earlier generated geometry. The modifier maps and
decoded terrain heights are not read as contour operands on that path. This
positive field/call argument bounds the investigation without claiming that
all terrain data is ready or that terrain work cannot affect demand timing.
The existing [D5T native controls](d5t-report.md#native-evidence-and-validation)
execute the geometry route with supplied definition/coordinate inputs; their
scope remains distinct from a complete loaded-retail initialization test.

An earlier working hypothesis incorrectly bound the Grid finalizer's vector to
GridFillCell. It was rejected by the constructor's field assignments and actual
table binding: GridFillCell `+0x18 = 0x140988260` is a pure source getter, not a
file-preparation callback. The modifier vector, spatial cells, corner index and
source array are separate allocations. No conclusion depends on the rejected
binding.

Height acquisition can run serially or through the configured worker pool.
`0x140998fc0` checks/clips the requested window and selects a file-state route.
The paged path reaches `0x140993110`, which creates or reuses a TerrainDB entry.
Its branches register PageStitch work when the backing block table is absent,
PageTransform work for the qualifying base case, or a streamed compressed-block
request. Dependency nodes and entry-state publication remain separate from
completion of their workers. A stream-open error has an explicit release/failure
path; it is not silently treated as resident data. The fresh export preserves
the intermediate state transitions rather than relabelling them all ready.

`0x14076c560` supplies a separate positive reconstruction path for base density:
it tests coordinate validity, builds an aggregate through four calls to
`0x1407a1940`, acquires the BaseProcGenDB entry, and only a claimed-load outcome
stores the aggregate at entry `+0x20` and publishes/wakes. Invalid coordinates
remove the entry. This is not the biome raster loader and cannot be substituted
for it. It also does not prove a completed layer request necessarily produced
nonempty resource geometry.

Fresh source windows for these paragraphs are `D5AD-EX08`,
`.local-work/d5ad-inputs/export08/native.tsv` (SHA-256
`896599b41f4e5b14cb2c8fd17b0530e991241c798c356dcf04eec965700f04a2`),
`D5AD-EX11`, `.local-work/d5ad-inputs/export11/native.tsv` (SHA-256
`17405b4df7910de1a35200b57f4172882cf5f75e4232a293edbc7ce91c4e9c73`),
and `D5AD-EX12`, `.local-work/d5ad-inputs/export12/native.tsv` (SHA-256
`5c7d1722161146a5160fe6c63de69bd59ff3a70c44e72be7a34a23a374eff67b`).
Exports `D5AD-EX14` through `D5AD-EX37` add the concrete startup, virtual-table,
modifier, plugin enumeration and postlink evidence. [The source ledger](d5ad-sources.csv) records
exact hashes and per-function line ranges; export aliases identify files,
whereas `D5AD-INnnn` IDs identify individual source windows.

## Method preservation and corrections

The local method/receipt directory `.local-work/d5ad-inputs/` retains commands,
generated owned Java exporters, source-window hashes, selected archive restores,
the native-state fixture and failures. Original D5S/D5AA owned export methods
were adapted; no third-party code was incorporated. Eleven historical biome-map
exports were restored from the authenticated resources archive into a fresh
directory, preserving their member identities. The native-state fixture reads
the installed executable and owned PE reader, writes only fresh local receipts,
executes in its own process and releases its private executable page.

The RSGD constructor decompilation failed in export 05; export 06 completed the
material loader/postlink targets without that constructor. Export 09 failed to
lock the original project before script execution. The input-provenance
specialist then moved subsequent exports to disposable copies. The primary
report separately records other workers' original-project operations and the
later mistaken original-project invocation; this is not a task-wide claim of
zero later launches. A verified disposable copy of the 15 pinned core files was
created. Ghidra rejected its first location because a path element began with
a dot; a second verified copy outside Git supplied the compatible analysis location. Exports
11 and 12 completed there, and the copied core files still match all 15 pins.
These failures and changes of method do not establish a scientific absence.

## Scoped Q1 answer and limits

The qualified ordinary source-to-ready-input path is traced end to end:
startup enumerates concrete plugin files, loads/registers and postlinks typed
definitions, builds the module's per-biome resource slots, supplies or
reconstructs the surface hierarchy, and constructs geographic source Grids.
Generation obtains descriptor/component context and the temporary relationship
dictionary, incorporates restored PCM content/placement state through the
qualified preparation paths, and acquires the body raster under its own deferred-load/readiness
guard. Terrain metadata, density and stream/block dependencies retain their
separate owners and completion/failure conditions. The numeric contour
consumer boundary justifies stopping unrelated physical height decoding;
source-index existence alone remains insufficient evidence of resource output.
This supports **Q1 COMPLETE** for the frozen qualified ordinary path rather
than every possible exceptional game path. Independent question-level review
accepted the loader/readiness chain with the subsequently traced PCM
persistence/preparation dependency integrated into the final model.

Historical effective overrides, registry arrival order, mutable settings,
raster priority and asynchronous wall-clock completion were not observed by
this offline graph. Their exact Save52 values are not invented. The report's
chronology joins actual B1/B2 events separately, and the save-state matrix
classifies restoration and conditional surface-tree swap context. Neither a
ready Lodge checkpoint nor these possible deferred paths alone identifies
which raster branch the historical destination used. Exotic/default-setting
and synthetic entry-state controls supply independent counterexamples to
default-equals-effective and entry-exists-equals-ready assumptions; they do
not execute an entire world load.
