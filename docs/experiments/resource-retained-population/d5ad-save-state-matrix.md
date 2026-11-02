# D5AD saved and reconstructed generation state

2026-11-02, Australia/Sydney. [Original contract](../../implementation-briefs/CODEX_BRIEF_SOR_RG2_D5AD_initialization_save_load_reconstruction.md),
[report](d5ad-report.md), [input provenance](d5ad-input-provenance.md),
[chronology](d5ad-load-chronology.md), [sources](d5ad-sources.csv).
Authored synthesis is REVIEW-REQUIRED; native/save evidence and numeric receipts
remain LOCAL-ONLY. D5R remains OPEN.

**Save52 stores generated-world descriptors and distinct context/component data;
the ordinary ProcGen visited array and retained geometry are process state.**
The saved active-context prefix is a comparison input to reset handling, rather
than an instruction to install that value as the manager origin. A compatible
comparison does not preserve ProcGen visits: the false reset variant still
dispatches its clear. These are positive reader/writer and lifecycle arguments,
not a search for matching values in a save.

All native VAs are preferred static addresses for Starfield 1.16.244.0,
image base `0x140000000`; subtract that base for an RVA. Member offsets are
byte offsets in the named receiver. Save offsets below are in the decompressed
logical stream, not the compressed file. Saved tokens, FormIDs, source pointers,
visited tokens and observer epochs have separate domains.

## State classification and its limits

| Material state | Classification | Native provenance / reconstruction and owner | Save52 corroboration / qualification |
|---|---|---|---|
| Manager and ProcGen allocations | TRANSIENT; manager conditionally reused within a process | Bootstrap constructs only when the singleton is absent. Manager constructor `0x140787830` owns and registers ProcGen at manager `+0x130`; ProcGen constructor `0x14079d660` initializes its storage. Reset dispatch can clear an existing object without reconstructing the manager. | B1/B2 reset receiver observations do not date manager construction or prove every load allocates a new manager. New process allocations cannot be restored as the old pointers. See D5Z source windows and the D5AD chronology. |
| Visited token array | TRANSIENT | ProcGen count/capacity/data at `+0x48/+0x4c/+0x50`. Provider append follows returned generation and successful reserve; actual clear `0x14079ddf0` releases/zeros it under valid native invariants. D5Z's ordinary receiver/writer census found constructor, reserve/store, reset and destructor paths, with no ordinary deserializer. | Global type 3 positively restores different inputs. No absence claim depends on token scanning. Later visit hits require a successful post-clear token store within the audited ordinary mutation graph; token equality alone does not prove unique source identity. |
| Retained source-pointer map and generated resource collections | TRANSIENT; CONDITIONALLY RETAINED within an owner interval | ProcGen map `+0x10`; provider `0x14079f860` inserts holder, invokes generation at `0x14079ff18`, then attempts visitation. Reset releases holders; source retirement `0x140982b70` removes the map entry without clearing visited. Deep-copied regions own nested point storage. | Native reader/writer scope and positive lifecycle distinguish these from saved descriptors. A map hit can retain empty/partial output. Neither a save prefix nor a successful token store establishes nonempty geometry. |
| Active saved context key and compatibility value | PERSISTED comparison input; not a direct origin restoration | Global writer `0x141824a60`, case 3, writes world component `+0x310` as u64, then the `0x140798130` compatibility result as u32. Loader `0x141825ac0 → 0x1407896d0` reads them and compares the already resident world/context; reset wrapper selection follows the comparisons and setting. | Reverified 12-byte prefix at `0xff5`. Header structure version 27 and buffer-version byte 153 qualify the `>= 0x3e` compatibility branch. Native unpacker `0x14096fb40` and an independent installed PNDT GNAM join identify system 71456/body index 3 as `0x0003f5a1`, `JemisonPlanetData`. This identifies saved context, not an actual Lodge resource request or a later selected manager origin. |
| Generated-world descriptors | PERSISTED descriptors; RECONSTRUCTED runtime world objects and component registrations | `0x14132d260 → 0x1403a5130` extracts body, packed key from world `+0x310`, world token and two strings. `0x14132d500 → 0x1403a5560` reads/remaps body and token; missing body marks an invalid descriptor. DB lookup/creation gates lead through `0x1403a5e00 → 0x1403a53b0`, copying key to reconstructed world `+0x310`; reference ownership and component commands are separate from byte decoding. | 88 rows begin at `0x1005`, stride 15 bytes: body u32, key u64 and legacy token of three bytes. Array ends at `0x152d`; 176 queued string references accompany it. Full-stream and independent selected-block decompression agree. Saved body/key identity joins have independent historical PNDT corroboration in EXP0020. |
| Two auxiliary ID lists in global type 3 | PERSISTED lists; separate restored global containers | Writer `0x140ad6cb0` writes both list counts and legacy IDs; `0x141825ac0` restores the first container and `0x140ad8930` restores the second. These are not ProcGen visits. | Both u32 counts are zero at `0x152d` and `0x1531`. This means the sampled serialized lists are empty; it does not imply no active outposts, no residual worlds or no reconstructed sources. |
| Typed PlanetWorldSpaceData game-day value | PERSISTED GameDaysPassed snapshot; float sorting/ID-list bookkeeping use; runtime component reconstructed | `0x1403a6ae0 → 0x1403a70a0` writes typed components. Load queues `0x1403a7eb0 → 0x1403a74e0 → 0x1403a7cc0`; each entry has tagged ID, u16 subkey and u32 bits written to distinct component `+0x10`. Initializer `0x1403a7910` has a zero-write branch; `0x1403a6dd0` copies values. After successful descriptor setup, `0x14078a5b0` queues current GameDaysPassed, or zero if its supplier is absent, through `0x1403a7ee0 → 0x1403a75e0`. Calendar binding `0x14059ac20` establishes global `0x145fdcdf8`, Calendar `+0x30 = GLOB 0x00000039`; the supplier's float is at GLOB `+0x48`. Getter `0x1403a69e0` returns the stored value through XMM0 to linked-world sorting. | Count 88 at `0x1535`; exactly 88 ten-byte rows end at `0x18a9`. Receipts preserve raw u32 bits. Installed GLOB `0x00000039` has EDID `GameDaysPassed`; this identifies the native supplier independently of the values' numeric appearance. `0x14077d960` filters/sorts worlds, then `0x140ad80d0` appends selected IDs to the first auxiliary list. The append is not completed world destruction. No vein seed, abundance or UTC timestamp meaning is assigned. DB type `0x145fdce08` and tagged-ID remapping remain separate. |
| Galaxy site tuples, generated-world links, secondary worlds and bounds | MIXED: persisted identity/context and reconstructed activation edges | Unit-6 typed writers `0x14140ff80/0x140ad5f20`; readers `0x1414128c0/0x140ad6150` restore their distinct galaxy/world components. `0x140798030/0x1407986d0` activation and `0x140ad1660` edge creation use them. Immediate/deferred edge registration and invalidation have their own lifetimes. | EXP0020's independently framed Save52 parent/secondary-descriptor/site joins corroborate saved identity and indexed frames. They do not choose the actual edge validity, terrain instance or activation schedule at an unrecorded post-load instant. See its [traced map](../static-exhaustion/call-and-dataflow.md) and [dependency ledger](../static-exhaustion/dependency-ledger.md). |
| Landscape, ordinary/overlay source Grids and MultiFiles Grid | RECONSTRUCTED runtime owners; inputs MIXED | Context initialization `0x14078b030` constructs landscape; `0x1407847b0` constructs its Grids and `0x140785190` completes preparation. Reset module callback `0x1407846d0` releases Grids. Grid clear `0x1409829b0` removes/frees sources and map entries, without locally clearing the visited array. | B2 records Grid pointers and source publication before the Lodge checkpoint, but no complete world-bound landscape/Grid inventory. Resource/file prerequisites and source-ready guards are in the input map. Ordinary Grid reconstruction does not mean every file or generated resource is ready at load completion. |
| Source allocation and visited identity | RECONSTRUCTED from descriptors/content and generated path | `0x140982d90` bounds-checks and deduplicates coordinates or allocates a new source. It copies terrain/face/coordinate fields, derives token at `+0x68` using descriptor/content and generated path, then attempts publication in the Grid-owned source array. Semantic writes precede birth; actual publication and retirement remain separate events. | B2's Lodge checkpoint prefix contains 383 source births and publications but zero provider records; this is observed metadata reconstruction, without a directly recorded body identity or generation claim. No serialized raw source pointer is inferred. Equal visited tokens are not guaranteed collision-free; a fresh pointer can carry an equal token. Source memory is not retained merely by retaining its Grid. D5AB-P1's [owner/alias census](d5ab-p1-source-identity-lifetime.md) supplies the qualified closure and detached-retirement counterexample. |
| PNDT resource-selection seed, per-biome fallback seed and initializer RNG | DEFINITION-DERIVED seed inputs; RECONSTRUCTED resource slots; TRANSIENT initializer RNG | PNDT loader `0x14076ec00` recognizes RSCS at `0x14076fd7f`, then reads its u32 into PNDT `+0x50` at `0x140770114..0x140770122`. Initializer `0x140779760` reads that value at `0x1407797f0` and initializes its MT state. If zero, the per-component branch `0x140779c33..0x140779c76` reseeds from CTPerBiomeData payload `+0x48`. BIOM/PPBD, atmosphere occupancy, effective resource definitions and order also determine the rebuilt root/slots. | This is the positive definition/component initialization route, not a claim that PPBD is a serialized runtime slot image or that no save component can retain related state. Native source aliases D5AD-IN046 and D5AD-SV73 cover the loader/initializer. Actual historical seed values and initializer scheduling remain separately qualified. |
| Surface-tree selection seed and hierarchy state | DEFINITION-DERIVED linked tree or RECONSTRUCTED missing tree; TRANSIENT generation RNG | `0x14096b8e0` returns an existing typed PNDT `+0x38` tree; only a missing tree with nonzero owner and creation permission reaches allocation/registration and `0x14096e060`. At `0x14096e0a4..0x14096e0c3`, that generator passes body index, system and effective surface seed to CRC helper `0x140970d50`, then initializes MT. This selects SFPT hierarchy entries and orientation, before later source/vein generation. | Reuse is a concrete counterexample to reseeding/regenerating the hierarchy on every load. This seed is distinct from PNDT RSCS and the later cell/resource CRC. D5AD-IN026, D5AD-SV74–75 and the [pattern native ledger](../resource-pattern-selection/native.md) cover inputs and existing-versus-missing branches. The swap-component and changed-tree boundary are qualified in the following row; actual historical tree choice is not inferred from the setting name or installed file order. |
| SFTR `SurfaceTreePatternSwapInfo_Component` definition block and changed-tree save boundary | DEFINITION METADATA without a factory in the audited ordinary retail registration graph; SFTR changeforms persist generic flags, not tree arrays | SFTR ESM loader `0x140970830` routes BFCB to `0x1405e0930`. Exact interned-name dispatch `0x140463ed0 → 0x1404628b0` consults the registry initialized by `0x1404639f0`; a missing factory yields no loader, and the BFCB loop skips DAT2 to BFCE. The complete 74 direct callers of registration `0x1404613d0` resolve to 74 explicit names, including one inline LensFlare name; none is the exact swap-component name. SFTR vtable `0x144b674c8` slots `+0xd0/+0xd8` select base `0x1405df980/0x1405dfa40`, which serialize self identity and change-bit-0 generic flags only. | Pinned installed Carinae SFTR `0x00177c6f` has the exact named BFCB with one nine-byte DAT2; Feynman SFTR `0x00168814` has no BFCB. No swap-count/flag semantics are inferred from those bytes. The factory census plus explicit null-loader branch supports ordinary-path omission, rather than a search for serialized values. This is static coverage, not a captured live registry; indirect or externally installed factories are outside that census. The separate PCM serializer below prevents treating base SFTR changeforms as the whole persistence story. |
| PlanetContentManager seed, per-PNDT BlockContent and per-world placement state | PERSISTED PCM inputs and selection/placement outcomes; RECONSTRUCTED runtime references/containers | Global type 7 writer `0x1418b1eb0` and reader `0x1418b22c0` serialize/restore PCM `+0x420` seed, PNDT-keyed map `+0x360`, world-ID-keyed map `+0x3e0`, two triples and a version-gated final ID list. `0x1407791d0` positively types the first map's raw u32 key as PNDT identity. Block writers/readers `0x1418b36b0/0x1418b38a0` restore numeric state, coordinates, item IDs and selected content-node/world references, with remapping/type checks and failed-resolution filtering. Existing BlockContent lookup `0x1418ae790` reuses an entry; only missing entries allocate a new one. | Save52's full 335338-byte type-7 frame at logical `1451268..1786606` is consumed exactly: seed `1008349248`, 478 PNDT entries/3686 blocks/3656 items; 96 world entries/2864 blocks/2678 placements; final 74 IDs. All 478 PNDT keys independently join installed records. Carinae `0x0005e4da` has 58 blocks/81 items; Feynman `0x0005e0de` 144/131; Jemison `0x0003f5a1` 32/56. These are PCM content records, not ProcGen resource geometry or SFTR face-array images. Successful ID resolution, live contents after filtering, effective runtime seed and demand order remain separate. |
| Cell/resource generation seeds and generator RNG working state | RECONSTRUCTED seed and TRANSIENT RNG for the inspected ordinary generator | `0x14079a330` obtains packed cell key through `0x14078d7b0`, folds its eight little-endian bytes and manager-owner u32 through CRC, and initializes the 624-word generator at `0x145920b00/+0x04` before drawing. Source-derived origin plus candidate cell supplies the cell input; the original raster query is a different operand. | The positive reinitialization path makes a serialized RNG-state restoration unnecessary for this inspected call. This is not a no-save claim about every engine RNG or every source generator. Owner/frame, definitions, order and sampled weights remain material effective inputs. D5T's fixed-input counterexamples distinguish two populations without choosing a historical winner. PNDT/SFTR seeds and the separately persisted PCM seed remain distinct prerequisites. |
| Resource definitions, BIOM/component dictionaries and geographic raster | DEFINITION-DERIVED plus TRANSIENT cached/prepared runtime data; readiness conditional | Concrete producers/loaders and consumer guards belong to the [input provenance map](d5ad-input-provenance.md). Saved world context selects inputs but does not serialize the installed definition corpus into the ProcGen map. | No inference from resident sampler pointers to game-start loading completeness. Actual Save52 readiness and pending asynchronous input work require the chronology qualifications. |
| Existing outpost centre/reference/world context | MIXED: serialized reference/context inputs plus load-time frame/registration reconstruction | Initial/reference readers `0x141835c20/0x141835610`, parent/world selection `0x1418325a0`, created-reference loading `0x141833b20`, and conditional translation `0x140ad3ed0/0x140ad3240` distinguish saved coordinates and loaded world frames. Saved mask `0x20` is a framing input, not proof of current resource geometry. | Historical Save52 ordinary-beacon/direct-owner and saved-frame studies provide positive persisted outpost context; complete active player membership and all later loaded-frame states are separate claims. Outpost existence does not require its resource population to have been generated during Lodge residency. |
| Terrain focus, service commands, request keys/density aggregates, worker queues and outstanding work | TRANSIENT; conditionally reused or rebuilt | Context initialization and focus setters enable service requests under explicit state/context/focus guards. Ready handles can activate asynchronously; existing DB keys and density aggregate `+0x08` can skip fresh provider work. Manager drains do not imply completion of every future demand. | B1/B2 lack a complete load-time inventory of these operands. The pre-travel checkpoint is an observed boundary, not a proof that all potential resources are ready or target keys are cold. |

**D5AD-Q3 is COMPLETE for the material-state classification contract after
independent review.** Review reopened the earlier
proposal using the concrete swap-component definition and separate type-7 PCM
serializer. The follow-up positively traced exact-name factory dispatch, all 74
direct registrations, SFTR changeform virtuals, PCM writer/reader and actual
Save52 frames. It adds persisted PCM state and does not equate that state with
retained resource geometry. Earlier seed provenance alone was insufficient.

The supported state classes have native producers, ownership and reader/writer
or reconstruction paths, with protected Save52 corroboration where
discriminating. The ordinary receiver/writer census bounds the transient
visited/map conclusions; serialization absence is not inferred from byte
searches. Definition seeds, persisted PCM seed/content, restored world
components, reconstructed sources and downstream request state remain distinct.
A live registry snapshot, arbitrary indirect factory installation and historical
resolution/scheduling are outside the audited ordinary graph. Unmeasured
historical values constrain Q1/Q2/Q4 chronology rather than changing these
storage paths.

This is not a census of every save field or engine variant. The
[destination analysis](d5ad-save-destination.md) leaves 76 later type-9 bytes
UNCLASSIFIED: they are outside the proven initial destination/context branch,
which consumes its operands before the common later-buffer path. They supply no
missing initial branch operand and are not promoted to a resource-generation
seed or source image. No universal claim that those bytes are irrelevant to
every downstream subsystem is made. Raw typed bits and source receipts remain
preserved independently of the now-established GameDaysPassed supplier.

The following IDs select exact function windows and whole-input hashes in the
[source ledger](d5ad-sources.csv); the surrounding reports preserve earlier
scope and counterexamples.

| State / mechanism | Decisive primary windows |
|---|---|
| Global type-3 ordering and reset comparison | D5AD-SV01, D5AD-SV11–12 |
| Descriptor extraction, reading, remapping and reconstructed world key | D5AD-SV02–03, D5AD-SV18–23 |
| Auxiliary lists and typed component tail | D5AD-SV04–10; D5AD-SV28–30 establish four-byte count/value and two-byte subkey writes |
| World links, site data and saved-reference frame reconstruction | D5AD-SV13–17 |
| Ordinary constructor/clear and reconstructed source/token | D5AD-SV24–26; D5Z and D5AB-P1 retain the wider receiver/alias census |
| Cell-key/owner-derived CRC and RNG initialization | D5AD-SV27, especially `0x14079a3c4..0x14079a555` |
| Actual selected Save52 bytes, independent decoding and controls | D5AD-SV35–37 |
| Saved-key unpacking and fresh installed body corroboration | D5AD-SV38–42 |
| Typed component initialization/copy/update and float sorting use | D5AD-SV43–51; getter return `0x1403a6a89/0x1403a6ac2` overrides its incorrect decompiled pointer-return type |
| Fresh-output, optimization and protected-input negative controls | D5AD-SV52–53 |
| Owned seed arithmetic and independent controls | D5AD-SV54–56 |
| Typed scalar producer, sorting consequence and auxiliary-ID append | D5AD-SV57–62 |
| Earlier PNDT/component and surface-tree seed classes | D5AD-IN046, D5AD-IN026 and D5AD-SV73–75; these are distinct from D5AD-SV27's later vein RNG |
| Calendar/GameDaysPassed supplier identity | D5AD-SV79–80; exact binding `0x14059ad27..0x14059ad94` and GLOB `0x00000039` EDID |
| Saved Lodge CELL DATA and native runtime flag | D5AD-SV77–78, D5AD-SV81–82; [destination route](d5ad-save-destination.md) |
| SFTR ESM BFCB, explicit null-loader boundary and inherited changeforms | D5AD-SV84–93, D5AD-SV110 |
| Complete direct registration/name census and inline-name control | D5AD-SV94–96, D5AD-SV113–114 |
| Separate global-7 PCM writer/reader, items, typed IDs and reuse | D5AD-SV97–109 |
| Actual full Save52 PCM frame, installed joins, controls and pinned SFTR blocks | D5AD-SV111–112 |

## Controlled Save52 corroboration

The protected controlled copy is 16,411,136 bytes with SHA-256
`6b4a10084c7e752c31fd2de121a00850aaa2bf1decd700b437d7dccfcdbc82e8`.
Fresh decoding agrees with decoded SHA-256
`e3c0dc34cbbdcd26bb85d212fc458378b44404b37a5f54b635070e03e1565b93`.
Buffer version 153 also takes the native `> 0x22` typed-tail load branch.
The type-3 envelope starts at `0xe8b`, its payload at `0xff5`, length 2,228
bytes, ending at `0x18a9`. D5AD adds a native-backed exact framing of the
892-byte tail previously left undecoded by D5Z. It does not reinterpret D5Z's
historical test scope or claim that byte framing establishes runtime authority.

The [owned method](../../../research/resource-retained-population/d5ad_save_tail.py)
uses the existing D5Z controlled-copy reader. It checks full-stream output
against separate selected-block zlib decoding, checks every typed row with an
independent `struct` walk, and verifies the protected hash after analysis.
Positive fixtures cover empty and nonempty legacy/typed arrays. Five malformed
fixtures reject truncation, trailing bytes, impossible legacy count, impossible
typed count and wrong typed-ID width. These test bounds and representation,
not whether a saved value is authoritative after load.

Set `$D5adPython` and `$D5adEsm` to the verified interpreter and installed ESM
paths in the local receipts. The Windows `python` alias was unavailable in this
session; it was not used for the successful checks.

```powershell
& $D5adPython -E -B research/resource-retained-population/d5ad_save_tail.py .local-work/d5ad-save/FRESH-TAIL
& $D5adPython -E -B research/resource-retained-population/d5ad_save_body.py .local-work/d5ad-save/FRESH-BODY --prefix .local-work/d5ad-save/FRESH-TAIL/prefix/save-prefix.json --esm $D5adEsm
```

The local receipt is `.local-work/d5ad-save/tail01/save-tail.json`; its nested
prefix receipt retains inherited method hashes and controlled-copy provenance.
The [body-check method](../../../research/resource-retained-population/d5ad_save_body.py)
independently rereads the controlled source payload and joins the saved key and
all 88 descriptors to installed PNDT GNAM fields. Its fresh final receipt is
`.local-work/d5ad-save/body03/body-check.json`; the ESM and controlled copy retain
their pinned identities. Four process controls reject a wrong prefix key, wrong
ESM, optimized execution and an existing output destination, without creating
failed output. A retained earlier diagnostic expected EDID `Jemison`; the actual
installed EDID is `JemisonPlanetData`. Correcting that exact expectation did not
change the system/body mapping.

Five existing owned generation-seed controls also pass: CRC folding agrees with
an independent stdlib convention, the reconstructed generator reproduces its
known first-word control, repeated cell inputs agree, owner changes alter the
seed, and missing/invalid operands retain their qualified outcomes. Their local
receipt is `.local-work/d5ad-save/seed-controls.json`. These are arithmetic/model
tests, not retail RNG execution or a census of every engine RNG serializer.

Temporary decoded scratch is removed. The save methods change no original save,
protected backup, configuration, analysis database or game process.

The native work has a separate tooling qualification. D5AD's Ghidra runs used
`-readOnly -noanalysis`, but Ghidra performed project-directory temporary/presave
housekeeping, detailed in the main report. The Q3 worker was already started when
the instruction to stop original-project exports arrived; no further export was
started afterward. Its selected export ends in `END`, and all 15 pinned core
database files independently match their prior hashes. Its launcher exit status
was not retained. No manual original-project cleanup, restoration or symbol edit
was performed. These checks establish core-content preservation, not an absence
of project-directory writes.

## Reviewer follow-up: surface-tree metadata and PCM persistence

The exact-name registry route is a dispatch argument, not a negative string
scan. The owned local method `.local-work/d5ad-save/d5ad_swap_registry.py`
checks every direct call site against its containing initializer and resolves
every supplied name, with the inline LensFlare singleton as a separate case.
Its fresh `registry01/receipt.json` records 74/74 and zero exact target matches.
The four noncall references to the registration routine remain in the export;
this census does not transform possible indirect calls into observed absence.
No supported factory, loader or serialized component is invented for the
installed swap block. The base SFTR changeform route cannot restore tree arrays;
its positive field writes cover generic flags only. The alternative creation
path `0x1418af8e0` still reuses PNDT `+0x38` when present and calls the existing
hierarchy generator only when missing, before PCM content demand.

PCM is a separate persisted selection/placement layer. The owned local method
`.local-work/d5ad-save/d5ad_save_pcm.py` follows paired native type-7 grammar,
checks the protected Save52 pin before/after, independently decompresses the
selected range, and rereads the pinned installed ESM. `pcm01/receipt.json`
records the same post-read ESM identity and a complete 478/478 PNDT join.
The raw u32 PNDT key is neither system/body identity nor a packed world key;
legacy IDs in the second map and item payloads have their own remapping domain.
The numeric content/placement fields retain raw representations where a more
specific semantic name is unproved. The count/layout is therefore distinguished
from runtime acceptance of every saved item.

The frame begins with PCM seed u32 and PNDT-map count u32. Each PNDT entry has
key/count u32 pairs; each block has a u32 key, 25-byte header and 34-byte items.
The second map uses legacy world ID, u32 block count, then u64 block key,
u32 state/count and 20-byte placement items. After two 12-byte triples, the
buffer-version-153 branch consumes a compact count at logical `1786382`:
`29 01` represents 74, followed by 222 ID bytes. Exact exhaustion reaches
`1786606`. Truncation, trailing data and an oversized first count are rejected;
an independent struct prefix agrees, and independent physical zlib extraction
matches the complete frame. This verifies framing and input identity, not
historical worker demand or current retail object contents.

Both follow-up methods write fresh ignored local outputs and remove decoded
scratch through the existing owned reader. Native exports used only the
verified copied project under `-readOnly -noanalysis`, with no game execution or
symbol edits. Their completed `END` and preserved original core pins do not
claim that Ghidra performs no temporary directory housekeeping. All new source
IDs append after SV83; historical method/source IDs remain unchanged.

## PCM lifecycle, consumers and the ordinary load boundary

The current owned [PCM reader](../../../research/resource-retained-population/d5ad_save_pcm.py)
and [registry audit](../../../research/resource-retained-population/d5ad_swap_registry.py)
are retained in the repository. Their qualified commands and controls are in
the [methods record](d5ad-methods-and-tests.md). Frozen task-local versions and
their original receipts remain at their existing SV identifiers. Promotion
adds explicit guards, source pins, UTF-8/LF output and count bounds derived from
remaining bytes. All decoded PCM state agrees with the original after line-ending
normalization and as JSON; no raw-byte equality between CRLF and LF is claimed.

The seed is restored authority for later PCM demand, rather than a saved MT
working image. Constructor `0x1418a8b80` creates both map stores and calls
`0x1418a9270`: an effective override supplies PCM `+0x420`, or its zero branch
uses a local random supplier. The type-7 reader subsequently overwrites `+0x420`
with the saved u32. The demand path `0x1418a9350` derives a fresh seed through
`0x1418a9810`, combining the caller's packed-cell bytes, PNDT identity and this
PCM seed, then initializes MT count/state at `+0x424/+0x428`. Overlay content
requests use related `0x1418a9550/0x1418af110` operands and may queue work.
An explicit later seed-reset/setting callback can replace the value; its mere
existence does not establish that it ran in Save52's observed interval.

For the PNDT map, loader `0x1418b22c0` rebuilds `+0x360` entries, resolves a
PNDT through `0x1407791d0`, and uses its SFTR with `0x14096eb90` to derive block
context from saved coordinates. That helper reads the existing tree/SFPT
hierarchy; it does not rewrite its face arrays. Saved content items restore
world, additional form and content-node IDs through distinct typed readers.
Failed content-node resolution can discard an item. `0x1418ae790` reuses an
existing block when found. Consumer `0x1418ad2b0` can create a missing item
world from the retained content-node/position through `0x1418ab8d0`, which
reuses or creates its world via `0x140ad0650`, and conditionally calls manager
activation `0x140798030`. `0x1418aee00 → 0x1418ba850` separately replays existing
content items when its request selects that branch. These are concrete restored
selection inputs to later world preparation; successful activation is still
conditional on the guards, types and ID resolution.

For the world map, `0x1418aa1c0` selects `+0x3e0` by loaded world FormID and
packed-cell key. It reuses an existing placement entry, compares its stored day
value with scaled/truncated current GameDaysPassed and effective settings,
and may refresh it through `0x1418b4170`. Refresh removes items with zero
saved byte at item `+0x1c`, resets `+0x1d`, then fills residual target demand;
this is not unconditional discard of all saved placements. New results from
`0x1418a9900` append through `0x1418ab1c0` in the same representation the writer
serializes. Thus placement history, elapsed game time, retained flags and
current definitions can affect preparation even with fixed PCM seed/cell inputs.

The handoff reaches the ordinary preparation collection. `0x14079da80` calls
`0x1418aa1c0`, checks the returned objects' type, computes local placement ranges
with `0x14079ea40`, and copies accepted definitions, positions and IDs into
`0x60`-byte records. Its caller `0x1407b5bd0` is gated by context/request checks,
uses the manager-owned ProcGen at `+0x130`, performs four subsequent
`0x1407a1f80` subpasses, then publishes the collection at request `+0x20` with
a ready-state transition. This supplies a native connection from persisted PCM
outcomes to later source/cell preparation. It does not claim the provider has
already generated the final resource point collections during Lodge residency.

The ordinary type-7 revert is explicit: `0x141827960`, case 7, dispatches
`0x1418b2cb0`. It first calls `0x1418b1b40`, whose loop services work while
PCM counters `+0x348/+0x34c` remain nonzero. It visits both restored maps,
collects referenced world IDs into deferred set `+0x17b8`, clears/frees both map
stores, resets working RNG and resets auxiliary state. InitGlobalData's case 7
is in its no-op group. Load restores the saved maps/seed. FinishGlobalData
`0x141827380`, case 7, calls `0x1418b2f90`, which processes the deferred ID set,
conditionally unlinks/removes eligible world records, and clears that set;
it does not clear the newly restored PCM maps or wait for all future demand.
The chronology binds this ordinary type-7 restoration before the saved type-9
Lodge destination branch. Native ordering is distinct from a measured timestamp
of every reconstructed world or a complete checkpoint inventory.

## Registry namespace qualification and retained method failures

The complete name census uses the same namespace as the SFTR loader. Both BFCB
name creation and each factory's literal name enter `0x1428cba80` with the same
zero mode. Insertion `0x1404613d0` and loader lookup `0x1404628b0` both obtain
registry `0x14620e240` through `0x1404639f0`. Insertion helper `0x1402d26d0` and
lookup `0x1402cb870` hash the interned character pointer and compare the same
interned-object key; registration stores the supplied key and factory in that
map. Type-number lookup uses separate registry `0x140463af0` and does not replace
BFCB's exact-name lookup.

The direct alias census covers all 49 calls to the name-registry getter in 48
containing functions. Only registration invokes its map insertion helper;
the other direct consumers look up a factory and operate that returned factory.
Direct references to the BSS map fields cover initialization and shutdown.
The shutdown reference is a bounded, undecorated thunk: bytes at `0x14388f200`
compute registry `+8` and tail-jump to `0x1402cb9f0`, which releases keys and
clears storage, without inserting a factory. This closes the concrete alternative
population lead within the ordinary direct graph; it remains distinct from a
captured live registry or arbitrary indirect/external installation.

Two failed read-only export attempts are preserved locally: `swap-export14`
stopped on selector `0x1418a8b70`, and `swap-export17` on `0x14388f200`, because
those addresses have no defined Ghidra function. Neither was analyzed or given
a new function. Fresh exports 15 and 18 used the existing containing constructor
and bounded thunk bytes; export 19 read the already-defined destructor target.
All cited replacement exports end in `END`. No missing-function exception is
used as evidence of absent executable code or absent behavior.
