# Seed lineage and operand provenance

The installed path supports **three distinct deterministic seed domains**.
Stored resource-selection input does not establish stored vein geometry.
[Report](report.md), [source/hash ledger](sources.csv), [methods](sources.md).

All retail addresses here are preferred static VAs at image base `0x140000000`,
Starfield 1.16.244.0 EXE SHA-256
`7e9adb1414a8e1b325e5e1f097b9b17b78deb7eebeda37a333351a43a60f9d28`.
CK VAs belong to **CreationKit.exe**, database/executable SHA-256
`ed54e4906bc13b0fbc43ec7624fec4af2389a9a1e12b2789d73c5617f5a14020`,
same preferred base; CK product version is not established here. Never transfer
offsets between these executables. Hex member offsets are relative to the named
object. Saved descriptor keys are packed identities, not native pointers.
`Nnnn` means `.local-work/resource-geometry-mature-context/native/nnn.request.tsv`;
`Cnnn` means the sibling `ck-native/nnn.request.tsv`. These are task-local export
namespaces. Full decompilation and bounded instruction coverage differ.

## CK field, signed display and Apply plumbing

The screenshot shows the Kreet tree selection, Resources tab and signed value;
its capture time/loaded plugin state are UNKNOWN. The current installed main
ESM PNDT Kreet record starts at **original ESM file offset 1402105313** and has
RSCS payload `4b4b70a9`. Interpreting these four little-endian bytes as int32 gives
`-1452258485`; as uint32 gives `2842708811`. Equality is directly checked, not
inferred from the display label.

C005 `FUN_1431ef760` reads selected CK PlanetData `+0x130` and passes a signed
int to the decimal `QString::arg` overload, then `QLineEdit::setText`. C006
`FUN_1431d4ea0` resolves the selected body from widget `+0x30`'s key `+0x40`,
requires native form type `0xba` and returns that PlanetData object. C004's
widget constructor connects Apply and Apply Random buttons to
`FUN_1431f10b0` and `FUN_1431f0fe0`. Apply sets widget dirty byte `+0xc0`, calls
`FUN_1431fabe0`, then refreshes. The setter uses decimal `QString::toInt`, writes
the same CK `+0x130`, and calls `FUN_14158dbe0` after eligibility checks.
Random obtains a value through `FUN_1431ef1f0`, displays it as signed decimal,
then uses the same dirty/set/refresh path. This is a mutation path: no button,
Qt callback or native function was executed here.

C006/C007 connect `FUN_14158dbe0` → `FUN_14152cbc0`: the latter reads the same
`+0x130`, initializes MT with the standard recurrence, shuffles the PNDT-order
biome work list, and calls `FUN_1415dcfb0`. Nonzero RSCS retains a shared evolving
stream; zero RSCS has a per-biome reseed branch. This directly corroborates the
owned sibling's nonzero-selection account within this CK database. It does not
map CK allocator addresses to retail. The old sibling
`OnApplySeed → 1431bc320 → generic leveled lists` interpretation remains
SUPERSEDED as a primary allocator trail.

Retail N012 `FUN_14076ec00` recognizes subrecord integer `0x53435352` (RSCS)
and reads four bytes into retail PlanetData `+0x50`. The equivalent CK record
loader-to-RSCS case is not exported in this task: the CK/UI-field ↔ installed
RSCS association is supported by matching bits and the allocator lineage,
not a claimed cross-executable equal layout. Retail `+0x50`, CK `+0x130` and
manager `+0x80` name different fields.

## The owner key has an actual producer

N012, `FUN_14076ec00`, instructions **0x14076ec81–0x14076ec86**, copies retail
PlanetData FormID `+0x28` to `+0x54`. The BDST GNAM case reads the system/parent/
body tuple and queues satellite metadata through `FUN_140475740` and body-index
metadata through `FUN_140475810` (N013). Both key their component commands by
the body identity. N006/N007 `FUN_142332d90` first probes the `(system,index)`
cache, otherwise resolves system and traverses its bodies. N009's callback
`FUN_1423353a0` compares the indexed body's component value, returning its
owner ID. This is lookup plus caching, not an arithmetic seed hash.

N005 `FUN_140ad3c30` uses a world-context component's system/body pair at
`+0x18/+0x1c`, returns the lookup key and an associated spatial context.
N004 `FUN_1417dfdf0` passes it into N003 `FUN_14078b030`, which calls N002
`FUN_140789ce0`; N001 `FUN_14078a120` writes its uint32 argument to
manager `+0x80` at **0x14078a144**. Name/biome-map/context acquisition follows.
N007 `FUN_14096b8e0` independently stores that same owner at surface context
`+0x54` and resolves its system/body fields at `+0x58/+0x5c`.

Thus ordinary main-file reconstruction supplies the PNDT FormID as body-owner
key. Kreet's `259487` is independently corroborated by archived manager bytes;
the new mature values are STATIC derivations, not newly observed manager values.
Historical override/remapping and actual loaded epoch remain unobserved.

## Surface patterns, vein calls and consumption order

The [RG1 primary trace](../resource-geometry/native.md) remains controlling.
`FUN_14096e060 → FUN_140970d50` folds LE uint32 **body index, system, effective
surface seed**, raw CRC initial zero/no final XOR. Native default is
`0x20201215`. BIOM style and registered SFPT order determine choices and MT
consumption. SFBK/raw dimensions, orientation, anchors and padding determine
source local origin and bounds. Whole-pattern rotation default is false, block
orientation true; stitch block/merge defaults are 10/2. These are conditional
defaults, not a reconstructed historical override inventory. The inspected
path does not use the CK RSCS directly as its surface seed.

Original analytical pseudocode for the ordinary interior route:

```text
body_owner = lookup_body(system, body_index)       # PNDT FormID in mapped loader
surface_rng = MT(raw_crc32(LE32(index, system, surface_setting)))
sources = choose_and_orient_registered_patterns(surface_rng, map, styles)
for source in whole_required_sources:
    selected = resolve_CTPerBiomeData_and_effective_RSGD(body_owner, source.biome)
    for resource in actual_selected_rarity_order:
        for cell in full_source_X_then_Y_bounds:
            key = native_pack_cell(manager_descriptor, source.origin + cell)
            rng = MT(raw_crc32(LE64(key) + LE32(body_owner)))
            generate_with_chance_clip_and_prior_resource_competition(rng, selected)
```

N002 `FUN_14078d7b0` reads manager kind, current descriptor and linked owner
grid; `FUN_14096f5c0` transforms the integer point. Packing is system 18 bits,
body index 6, chart 3, Y16, X16. N003 `FUN_14078b030` can acquire its descriptor
from angular context or an explicit packed key; it writes `+0xc8` and copies
to alternate `+0x1c0`. N006 `FUN_14096fb40` unpacks a key only after checking
the body lookup, fills hierarchy indices, SFPT/source data and orientation.
This identifies real acquisition alternatives; the Save52-to-selected-branch
join is still missing. Grid existence is not evidence of a particular frame.

Vein generator `FUN_14079a330` folds LE64 key then LE32 manager owner and
reinitializes MT **per resource/cell call**. IRES is not in that CRC. Chance,
count/fraction, heading, widths and walk/rejection draws consume the stream;
different-resource predecessors can change acceptance. Shared seeds therefore
do not imply shared paths. RSGD main descendants use their selected root's DNAM,
rarity block byte offset `40*(rarity+7)`. Low-nibble masks select inactive
weights; Special/high-nibble and Everywhere processing remain separate.
Atmospheric IDs can affect the shared-eight selection guard; BIOM water and
later atmospheric UI contributions are distinct from vein geometry.

## Operand provenance and arbitrary-body acquisition

| Input / type and domain | Producer → consumer | Storage/lifetime | Source/coverage and acquisition |
|---|---|---|---|
| RSCS uint32 | Installed PNDT RSCS → planetary selection MT | DEFINITION-DERIVED; copied mutable native field | Kreet `2842708811`, Feynman `427600259`, Carinae `3128886084`; current ESM derivative and N012. CK signed UI C004–C007; no claim of historical mutation. For another body read its effective PNDT and ordered PPBD. |
| BIOM/PPBD seed/override, RSGD/IRES order | PNDT loader/component construction → selected CTPerBiomeData → `14079b520` | DEFINITION-DERIVED / reconstructed component state | RG1 plus N010/N012. Main-file candidates can be reproduced; actual component-selected/alternate descriptor needs the selected component or a qualified reconstruction, not merely BIOM RNAM. |
| Atmosphere/IRES population | PNDT INAM → ATMO RFDP/reflection inheritance → selection shared IDs | DEFINITION-DERIVED, effective context may differ | Current ATMO chains read; empty/inherited-Water alternatives retain these main families. Zero-LIST clearing remains source-reported provisional; do not turn sensitivity into an atmosphere proof. |
| Surface seed uint32, settings and registration | Effective settings/default initializers → `14096e060/140970d50` | Configuration/DEFINITION-DERIVED | RG1 exports 019–022 and focused CRC export. Obtain effective settings and registry; no new environment-variable override is asserted. |
| Body/system uint32/index | PNDT BDST GNAM → component lookup/cache → manager setup | Installed metadata, reconstructed cache | N005–N013, exact main-file joins for all three bodies. Reject invalid/sentinel lookup rather than substitute a name. |
| Owner uint32 | PNDT FormID `+0x28→+0x54` → lookup → manager `+0x80` → vein CRC | DEFINITION-DERIVED value, transient manager copy | N001–N013; numeric values now derived for each body. Kreet old capture corroborates only its recorded epoch. Obtain effective PNDT with its native remapping context. |
| Manager geographic descriptor | Angular/context or explicit-key branch → `14078b030` → `14078d7b0` | RECONSTRUCTED/TRANSIENT selected context; saved candidates exist | N002–N006 plus the [angular-snap continuation](predictions.md) support conditional ordinary initialization. Historical selected/rebased owner-frame remains UNKNOWN. |
| Spatial source, origin, clip, bounds | BIOM/SFPT/SFBK/orientation/grid → source constructor → generator | DEFINITION-DERIVED plus selected local frame | RG1 source chain and new frame discriminator. `100*(local anchor-padding)` is added to integer cell **without /100 correction** for CRC. Source IDs/pointers/cache keys and saved descriptor IDs are different domains. |
| Masks, chance weights, order | Map/first cache-query plus rarity settings → `14079b520/14079c470` | Installed field plus transient query/selection | Initial four-source frame audits have Feynman mask 8 and Carinae mask 4 under both hypotheses; final wider Feynman coverage has six sources, all mask 8. No first-query weighting ambiguity in this tested subset. Unique rarities give descending order; ties need actual ordering. |
| Vein key/MT state/prior regions | Packed spatial key + owner → `14079a330` | DERIVED per-call seed; TRANSIENT stream/regions | RG1 raw CRC/MT schedule; 16 new integer/zlib checks. Need complete ordered sources, not UI totals or named extractor installations. No claim that these cache arrays serialize. |

Negative conclusions are bounded to these inspected routes. No saved-seed absence,
all-context sufficiency, rendered raster equivalence or callable integration
point is established.
