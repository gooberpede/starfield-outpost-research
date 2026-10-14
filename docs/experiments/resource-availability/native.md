# Native route and exhaustion ledger

2026-10-14. Original authored synthesis of primary exports and specialist
contribution. [Source hashes](sources.csv), [report](report.md), [schema](schema.md).
All addresses are preferred **static VA** in image base `0x140000000`;
**RVA = VA − base**, only for retail 1.16.244.0 executable SHA256
`7e9adb1414a8e1b325e5e1f097b9b17b78deb7eebeda37a333351a43a60f9d28`.
No runtime base is invented. Original `FUN_` names remain; descriptive roles are
research aliases, OBSERVED-INTERNAL and not safe callable integration points.

## Qualified call/data-flow edges

`uiNN` below means ignored `.local-work/recon/resource-availability-ui-NN.tsv`;
associated `.log` files preserve the exact request and any partial/failing result.

| Original function / VA (RVA) | Primary evidence | Supported role and decisive edge |
|---|---|---|
| `FUN_141578250` (0x01578250) | ui06 | Constructs `WorkshopAreaResourcesDataModel` vtable 144c75468; payload constructor at call 14157827f; registers name pointer 144a52798 with native UI service and creates typed event shuttle. |
| `FUN_14157d570` (0x0157d570) | ui07 | Binds `aAreaResources` at 14157d721 and `bSearchedResources` at 14157d735 in embedded typed payload. |
| `FUN_141578440`, `FUN_141581a80` (0x01578440 / 0x01581a80) | ui08/09 | Actual model+8 shuttle request and shuttle+0x10 owning-model callback reach row updater; independent ownership proof beyond function adjacency. |
| `FUN_141578500` (0x01578500) | ui08/09/10/11 | Clears/rebuilds typed AreaResource rows, sets searched state, unions first vectors at 1415785b4–5da and special-filter loop at 1415785f9 onward. Row constructors/binder prove typed output. |
| `FUN_1421f8120`, `FUN_14042e250` (0x021f8120 / 0x0042e250) | ui09/20 | First helper deduplicates exact pointer values in first-occurrence order. Special append is separate. Allocation failure paths prevent unconditional set-completeness claims. |
| `FUN_1421e07d0` (0x021e07d0) | ui15/16/26 | Actual producer at context+0x520; RCX query state, RDX indexed center, XMM2 radius, XMM3 separate geometry operand. Native CALL register loads override the inferred decompiler prototype. |
| `FUN_1421b2570` (0x021b2570) | ui15 | Established initialization state+0x630==0; resolves Workshop through 140f3df70/interface+0x268 and obtains descriptor via 140f4a140 before producer call. |
| `FUN_1421b41f0`, `FUN_1421b64c0` (0x021b41f0 / 0x021b64c0) | ui15/17/26 | Placement/preview update uses indexed position via 140b4cee0 and the same producer; change leads to event code 7 through 145f5e658. Other caller supplies bounds +0x28/+0x2c to XMM2/XMM3. Actual unplaced/placed traversal remains unobserved here. |
| `FUN_1421e0f50` (0x021e0f50) | ui16 | ProcGen resource-region callback: resolved form type 0x9f; 48-byte region center/radius/point fields. Scalar broadphase 1421e1119–1154, count-one acceptance, count-zero rejection; multi-point descriptor/edge sample calls. |
| `FUN_140f4ac50`, `FUN_140f4af20` (0x00f4ac50 / 0x00f4af20) | ui17 | Supplied descriptor containment/geometry helpers in the multi-point branch. Center/frame/radius/other geometry operands must be qualified independently; broadphase alone is insufficient. |
| `FUN_14076b950`, `FUN_14076bd20`, `FUN_1409dd080` (0x0076b950 / 0x0076bd20 / 0x009dd080) | ui16/32/33 | Resolve world-component +0x108 identity against current record context; type 0xad is BGSAtmosphere. Copy ATMO +0xf8 count/+0x100 pointer array into second population; fallback object exists for unmatched resolution. |
| `FUN_14078ee90` (0x0078ee90) | ui34 + ui33 factories | Spatial identity lookup checks type 0xa0 at 14078ef8b: BGSBiome, not TESObjectCELL. Third population takes BIOM +0x308/+0x310 RSGD list and every descriptor's first resource pointer, stride 0x238, without planetary RNG selection. |
| `FUN_140787830`, `FUN_14079d660` (0x00787830 / 0x0079d660) | ui28/31 | BGSPlanet::Manager installs BGSPlanet::ProcGen at manager+0x130; concrete ProcGen vtable 144b3f3a8. This is generated-region ownership, distinct from Workshop::ExtraData. |
| `FUN_14079f860`, `FUN_14079b520` (0x0079f860 / 0x0079b520) | ui28/29/31/32 | Spatial generation/cache path resolves mapping/source data and RSGD type 0xab or BIOM descriptors; sorts through 1407af470 and iterates cells through 14079c470→generator14079a330; the earlier constructor interpretation is superseded below. World/site generation context and loaded spatial selection remain separate from a planet resource list. |
| `FUN_1409df850`, `FUN_1409e1640`, `FUN_1409e4690` (0x009df850 / 0x009e1640 / 0x009e4690) | ui35/36 | BIOM RNAM loader appends raw IDs to +0x308/+0x310; fixup resolves them. Direct installed definition edge, not a claimed saved CELL payload. |
| `FUN_1409eed50`, `FUN_1409efc60` (0x009eed50 / 0x009efc60) | ui40/42 | RSGD RNAM nonzero resource ID pairs with following structured DNAM, with version branches. Fixup resolves first qword of native 0x238 entries at +0x38/+0x40 and removes unresolved rows. DNAM's first word must not be labelled an IRES ID. |
| `FUN_1409dd250`, `FUN_140852f20` (0x009dd250 / 0x00852f20) | ui43/40 | ATMO resource list +0xf8/+0x100 is rebuilt by dynamic-casting reflected +0xd0/+0xd8 Form entries to BGSResource; generic REFL/PTTA source loading. Full reflection wire/property schema remains unresolved, with sibling effective-ATMO extraction as separately scoped prior knowledge. |
| `FUN_1421f68f0` (0x021f68f0) | ui10 | Selected-harvester resource gate, not producer or full placement. Category default equality, definition/produced-resource resolution, property-presence bypass/source selection, any pointer intersection. |
| `FUN_14044b610`, `FUN_14044b670` (0x0044b610 / 0x0044b670) | ui24 | First tests exact property-pointer presence in 24-byte entries; second is the distinct numeric getter. Presence does not mean value>0. |
| `FUN_1409e6c20`, `FUN_1409e6ed0` (0x009e6c20 / 0x009e6ed0) | ui19/24 | BGSDefaultObject resolved pointer +0x48 and DATA loading; initializer/name/type bindings in ui18/21/23 join independently to installed DFOB records. |
| `FUN_140c5c550`, `FUN_14079df70` (0x00c5c550 / 0x0079df70) | ui19/22/26 | `ResourceVeinHasKeyword` native condition 0x13aa; planet-worldspace reference and reference XYZ feed point query; returns numeric 0/1 via keyword test. Not a whole-site set or verified Papyrus call. |
| `FUN_140f50660`, `FUN_140f515a0`, `FUN_140f50880` (0x00f50660 / 0x00f515a0 / 0x00f50880) | prior workshop-origin-08-retry/durable-center-05 + current save controls | ExtraWorkshop +0x20 producer map save/load, outer resource FormID, row handle/base FormID and 17 body bytes. No identity substitution with generated region hash. |

Concrete form factories (ui33) independently map BGSResource/IRES=159 (0x9f),
BGSBiome/BIOM=160 (0xa0), BGSResourceGenerationData/RSGD=171 (0xab),
BGSAtmosphere/ATMO=173 (0xad), ActorValueInfo/AVIF=109 (0x6d).
These are native form types, not optional save-record buffer versions.

## Cache, lifecycle and persistence classification

The three collections live at static context `145f5d2e0` offsets +0x520/+0x538/
+0x550 (data/end globals 145f5d800/808, 818/820, 830/838). First-set update is
conditional on reference-domain comparisons and, in the applicable branch,
translated current versus cached XY displacement compared with setting
`145f5e228²`. Cached indexed XYZ/frame are query-state +0x48/+0x54,
reference +0x58 and second/third source IDs +0x60/+0x64. No actual threshold
value or activation epoch was measured. Radius +0x360 and the separate +0x364
operand belong to the selected operation descriptor, not an assumed global
ordinary-beacon constant. Frame translations use 1461fae80/1461fae88 count/data;
these must not be supplied from an unrelated earlier positioning invocation.

Second and third populations refresh on changed resolved definition IDs.
`1421ae260 → 1421ae590` teardown frees vectors/reference; selected transitions
`1421b6a10`/`1421d0650` clear range ends. These are direct cache/lifecycle
observations in static code. No every-move-recomputes claim or exact live freshness
guarantee follows. Native UI searched state is a separate application state.

Installed ATMO/BIOM/RSGD identities and descriptors are DEFINITION-DERIVED.
Loaded region geometry and the operation-context collections are generated/
cached state; their complete save relationship remains UNCLASSIFIED. The sampled
Workshop object map is PERSISTED, with ordinary producer interpretation supported
by controls. Generated caches were not found in that map, but it is not a
complete global save-schema proof. Archived manager+80 and later ProcGen headers exist; complete source arrays and
same-invocation cache/UI operands are not captured. The fresh probes below qualify
this boundary; no blanket absence of archived operands is claimed. Native loader/saver,
generation ownership and definition origins were followed independently.

## Credible routes completed and remaining bound

| Route tested | Result and precise boundary |
|---|---|
| UI label/model/event/typed rows | Real producer and final identity fold recovered. Screenshot is not a native invocation oracle; row fields/timing still need actual observation. |
| Direct and indirect array writers | Byte-address xref census 145f5d000..145f5e000 plus 92,823 existing instructions 1421a0000..142200000 identified indirect operation-context updater; subsequent typed exports qualify the result. Literal census alone is never absence/completeness proof. |
| Geometry and source generation | Callback, containment, ProcGen owner, spatial cache/generation and RSGD/BIOM definition suppliers traced. Seed/first-gate arithmetic is reproduced below; full region assembly and invocation-specific source/frame/cache inputs are not reconstructed. This is an unvalidated operation/input join, not a claim all theoretical offline regeneration is impossible. |
| Atmosphere and special biome source | Actual ATMO and BIOM types, source lists, loaders/fixup and independent installed definitions checked. Conditional RNAM calculation is runnable; effective ATMO reflection inheritance/current record context and selected spatial BIOM are not fabricated. |
| API/placement | Installed Resource/ObjectReference declarations, native condition registration, point predicate, category/AVIF resource gate and full-placement consumer leads inspected. No verified whole-area API or exhaustive valid footprint enumeration. |
| Save object/resource map | All 29 labels including beacon-only stages, two-beacon controls and mature associations; strong producer-registry counterexamples. No whole-save availability absence claim. |
| Maintainer deterministic resource model | Actual two revisions and documented canonical extraction inspected. Planet/biome allocation can supply candidates and atmosphere provenance, but not loaded region intersection/freshness/valid-footprint evidence. Its CK addresses and validation totals are not transferred to retail. |

The minimum sufficient missing **observation** is the actual producer vectors,
selector and linked UI epoch, rather than full geometry. Complete offline
**generation** would additionally require a qualified world/site/spatial BIOM
lookup, effective ATMO reflection/load context, actual ProcGen resource-region
generation inputs/operations and cache state. Precise RSGD/ATMO/BIOM definitions
already exist and are not called inherently unavailable. The continuation recovers seed/first-gate arithmetic and follows the concrete
source/generation helpers. Unresolved same-invocation source/cache joins prevent
a validated complete-site reconstruction; missing independent controls also
prevent claiming model output as Outcome A. [Acquisition](acquisition.md)
states the competing hypotheses and the independent point/footprint boundary.

No speculative all-vein polygon reconstruction, production importer, observer
implementation, installation or new live request was used to evade the brief.
The selected route coverage justifies the scoped offline disposition for review;
it does not certify whole-engine static exhaustion or finish broader research.

## Reproduction tools and actual execution failures

Installed Ghidra **12.1.2_PUBLIC** and Temurin **21.0.12+8-LTS**, existing program
`D:/ReverseEngineering/Starfield/GhidraProject/Starfield`, were read through the
owned [wrapper](../../../ghidra/scripts/Invoke-OutpostRecon.ps1),
[OutpostRecon.java](../../../ghidra/scripts/OutpostRecon.java) and
[ReadNamed.java](../../../research/workshop-population/ReadNamed.java).
Exact tool/source hashes and selector commands are sealed in
`.local-work/resource-availability/specialist/sources.json`, `commands.md` and
the original logs; native outputs stay local. All headless calls used existing
program `-readOnly -noanalysis`, with exclusive exports. Decompiler inferred
prototypes do not replace instruction-register evidence.

The three original census sources are retained in
[research/resource-availability](../../../research/resource-availability/README.md).
They read existing instructions/xrefs only, writing exclusive TSV/log derivatives.
The historically named ResourceCellFields query examined 115,921 instructions
140760000..1407d0000; subsequent type proof shows BIOM, so its filename is not a
CELL semantics claim. Full-function instruction output can cap at 600 while
decompilation remains complete within the 250,000-character guard; exact
decisive windows and actual log/error/cancellation checks bound each claim.

The specialist seal retains **82 export/log files**, **10 equal stable non-user
project files**, five separately excluded tool/user transient entries and zero
stable-file mismatches/read errors. Two early user-cache temporary files were
locked. The initial snapshot overlapped initial exporter startup, so it cannot
bracket all first exports; final stable equality has that explicit timing limit.
Lock-rejected and instruction-interior SCRIPT ERROR attempts are preserved;
exit code zero alone was not treated as success. No symbols/types/comments,
analysis actions, game bytes, runtime registers/memory or saves were altered.

## Criterion 6 continuation: generation and saved-source leads

The continuation supersedes the earlier working description of **1407af470**:
it sorts descriptor pointers descending by the resource's **+110 rarity byte**;
it does not generate geometry. **14079c470** iterates grid cells and calls the
actual generator **14079a330**. Fresh local exports `resource-availability-cont-01..13.tsv`
retain these functions and dependencies. Addresses remain preferred static VAs
for the pinned executable above, with RVA obtained by subtracting 140000000.

**14079f860** resolves terrain/spatial sources, queries a ProcGen cache and calls
14079b520 for a missing entry. At 14079fed3..14079ff18 its arguments include
**manager+80**, a transformed/floored discrete origin, spatial BIOM, bounds and
output regions. 14079b520 queries **CTPerBiomeData** through 140771f30 with owner
key=manager+80 and BIOMFormID=BIOM+28; failed lookup exits generation. This makes
the archived manager+80 scalar an available source key as well as seed suffix.
Its historical value must not be described as missing merely because other
operands were not archived.

Registration 14231d000 names CTPerBiomeData and stores its factory vtable
**144d5f5c8** at +100 (14231d19b..1a2). Earlier working addresses 144d5f688 and
144d5f668 were interior/adjacent CTBiomeData addresses and are superseded.
Factory slots +28/+30 both invoke 142322520, which creates/copies
StoredComponent<1,CTPerBiomeData>, not an established byte-stream serializer.
Source copy 14076e810 retains reference-counted fields at +0/+10/+20/+30,
scalars at +40/+44/+48/+4c, qwords at +50/+58/+60 and a scalar at +68.
Lookup matches +40 to BIOMFormID. Descriptor selection
14079c540 first searches a component-selected RSGD, then current BIOM RNAM;
14079c5e0 can select another BIOM with a matching component +50 discriminator.
Thus installed current-BIOM definitions alone do not establish descriptor choice.

The exact type word 1461dfa4c references were followed: 1405f7a80 lookup;
140773180/140773be0 typed queued creation/copy; 140774970 edge removal;
14077bce0 runtime-pointer enumeration into a scratch array; 14077d090 PNDT
owner (record+54) traversal resolving component BIOM IDs; 142322520 factory copy;
14231d000/14231da10 registration. None of those observed paths exposes a
byte-stream schema. This scoped disposition does not establish absence from
generic saved component sections or exclude regeneration during load.

A separate exact search of the **42 existing native37..78 TSV exports** in the
workshop-population specialist archive queried CTPerBiomeData, PerBiomeData,
1461dfa4c, 142322520 and 14076e810. It returned zero literal matches;
`specialist/continuation-catalog.json` hashes every searched file and retains the
terms and scoped interpretation. That existing 43-section catalog therefore
provides no direct named-type/address mapping for this source. It does not
establish that a generic component serializer lacks the type, that the whole
save omits it, or that regeneration cannot reconstruct it. Full saved-section
joins remain a separate bounded check owned by the save analysis.
The CTName table supplies component names, rather than a proven saved-type
registry. Its names cannot substitute for a native factory-to-stream mapping.

IRES loader 1409e7900's SNAM case stores the low byte at +110, establishing
**rarity=SNAM&255**. The selected modern 560-byte DNAM payload contains a 40-byte
block at 40*(rarity+7), with chance float at block+28. Generator 14079a330 rejects
its first gate when f32(weight*chance)<=f32(uniform*100). Seed preparation folds
eight little-endian packed-cell-key bytes, then four little-endian manager+80
bytes, using CRC initial value 0 and no final XOR. The installed table 144d58d70,
original file offset 81101680, SHA256
`12f3e0576d447eb37b36d82ba0c1c5481b8f0d12fdc70347ce4a076b229d4c86`,
matches all 256 entries for polynomial edb88320. Native initialization seeds 624
MT19937 words with recurrence 1812433253*(previous^(previous>>30))+index modulo 2^32,
index 624; no additional warm-up was observed. One 32-bit draw produces the f32
canonical value divided by 2^32, then range conversion uses lower 0 and upper
**bits 3f7fff58**, rather than 1. These available arithmetic operations support a separately
runnable partial gate with supplied key, weight and selected DNAM; a passing gate
does not establish a generated region or UI availability.

The exclusive local `specialist/continuation-gate-bytes.json` independently
pins the executable and the four-byte file ranges: mask 145921e84 at original
offset 93456004 is ffffffff; 2^32 at 144f050f4/82855668 is 0000804f;
precision 24 at 144f04b5c/82854236 is 0000c041; 1 at 144f044e8/82852584
is 0000803f. It includes a SHA256 for each byte range and the lower/upper range
bytes. The first native twist, 1402fbc98..1402fbcd7, writes word i+624 from
word i+397 and the joined high/low bits of words i/i+1. From i=227 its source
is an earlier newly generated word; at i=623 the next word is new word 0.
That sequential double-buffer operation matches the classic in-place 624-word
twist. A simultaneous old-array modulo recurrence would be a different model.

Packed-key helper 14078d7b0 depends on manager mode+20, descriptor+c8/+1c0, owner+58 grid,
14096f5c0's transformed discrete point and stitch settings 145ea6770/145ea66f0.
Full generation additionally consumes source-selected candidate ordering,
rarity weights 145e901b8..145e90258, border/dimensions, effective bounds, stochastic
count/XYZ/radii and prior generated regions via overlap iterator 1407af1a0.
The archived-input boundary therefore concerns the same-invocation source BIOM/
CTPerBiome values, discrete key/origin/bounds, candidate order/weights and prior
regions, followed by the UI context and complete region arrays at that epoch.
Installed definitions, native arithmetic and archived manager/grid prefixes are
available. Further saved-component joins may resolve some operands. Neither
whole-save absence nor fundamental offline impossibility follows from this boundary.

Continuation tools are unchanged Ghidra 12.1.2_PUBLIC/Temurin 21.0.12+8-LTS with
`-readOnly -noanalysis`; exact selectors are in each local log. Exclusive
`specialist/continuation-before.json` precedes cont01 and
`specialist/continuation-seal.json` follows completed cont13: **26 export/log
files, 10 equal stable project/program files, zero mismatches and zero logged
errors**. Full-function disassembly still caps at 600 instructions; decompilation
and exact exported instruction windows supply the scoped evidence. Original
seals and superseded working interpretations remain preserved.

## Final saved-component and archived extent disposition

`component-catalog01.json` compares fresh native-qualified S1/Save52 replay
against existing 43-section receipts: exact sections, names, decoded hashes,
source pins and closure all agree. Runtime owner key 259487 is not interchangeable
with a serialized storage-ID word. Neither CTName nor equal byte patterns supply
a verified CTPerBiome mapping. The concrete native typeword paths expose typed
creation/copy/query/enumeration, while the saved catalog remains unjoined to this
source. This bounds persistence knowledge without claiming whole-save absence.

The nine initial captures retain manager+80 but no ProcGen root; sixteen later
captures retain roots with incomplete hash-slot/member extents. Fresh union-range
checks find no complete required array in those later snapshots. Neither archive
links generated regions/source choices/cache state to the supplied screenshot or
a typed UI update. The decision-ready shortest observation therefore remains the
natural source vectors plus linked UI epoch, rather than another planetary list.
These concrete missing joins and tested archived routes support scoped Outcome B
subject to independent original-criterion disposition. Broader regeneration and
complete serialization remain research questions, not an impossibility claim.
