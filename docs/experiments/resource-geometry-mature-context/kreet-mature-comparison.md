# Symmetric input reconstruction

**The body-owner edge is supported for all three bodies. The continuation also
supports a conditional mature ordinary-initialization frame, with frozen
predictions. Historical loaded/rebased frame and effective override correspondence
remain unobserved.** [Lineage](seed-lineage.md), [current machine assessment](operands-v2.json),
[preserved initial UNKNOWN](operands-v1.json), [validation](validation.md).

## Shared dependency matrix

Cells are fine geographic indices; local XY and translations are native units.
All descriptor/world offsets below are **decompressed-save-stream byte offsets**,
not physical `.sfs` offsets. Body values are installed PNDT FormIDs, saved
beacon/parent tokens remain their own wire-reference domain.

| Dependency | Kreet25 SOR-002 | Kreet25 SOR-003 | Kreet39 | Save52 Feynman mixed P3 | Save52 Carinae single P4 |
|---|---|---|---|---|---|
| Body / system / index | `0003f59f` / 88327 / 15 | same | same | `0005e0de` / 86469 / 5 | `0005e4da` / 118021 / 8 |
| Beacon → parent | `822821→822834` | `84b985→84b996` | `841421→839160` | `83388f→84ec80` | `82be17→84655c` |
| Workshop identifier bytes | `f1517de43e171745` | `0efca066ee4c7b9b` | `41da48765780cc0c` | `c3a5866f4cfcf585` | `91bac704da9b1e34` |
| Qualified saved frame | 0b, chart 1 | 0b, chart 1 | 0b, chart 0 | 2b, chart 0 | 2b, chart 0 |
| Saved site base | `(10464,21120)` | same | `(14304,12768)` | `(25124,32446)` | `(21399,15640)` |
| Saved local center XY | `(122.700454712,273.046234131)` | `(356.820404053,2459.05859375)` | `(1088.759765625,1179.728515625)` | `(83.460693359,67.887710571)` | `(86.638061523,70.479125977)` |
| Exact secondary-world join | inherited RG1/B1 frame receipt | same region | independent RG1/B1 frame receipt | `84ec80→817a70`, world offset 1343498 | `84655c→818832`, world offset 1341648 |
| Joined secondary descriptor | inherited 0b origin | inherited 0b origin | inherited 0b origin | offset 5076, key `02a38a287ec06240`, origin `(25152,32448)` | offset 4416, key `039a0a403d2053a0`, origin `(21408,15648)` |
| Site-minus-descriptor translation | zero under qualified 0b model | zero | zero | candidate `(-2800,-200)` | candidate `(-900,-800)` |
| Current main-file owner | `259487` STATIC + earlier RUNTIME field | same | same | `385246` STATIC | `386266` STATIC |
| Historical same-site manager/frame capture | no exact epoch join; inherited scoped qualification | same | same | none qualified | none qualified |
| RSCS uint32 | 2842708811 | same | same | 427600259 | 3128886084 |
| Surface seed/default registry | RG1 main-file/native defaults | same | same | same method; installed body-specific map | same method; installed body-specific map |
| Source masks in tested halo | RG1 uniform 0 | RG1 uniform 0 | RG1 uniform 8 | all four sources uniform 8 under both frames | all four sources uniform 4 under both frames |
| Main families at relevant source BIOMs | Iron/Alkanes | same | Lead/Silver | FrozenNoLife09 Nickel/Cobalt; CanyonsNoLife06 Copper/Fluorine/Ionic Liquids | HillsNoLife08 Iron/Alkanes/Rothicite |
| Actual component-selected RSGD correspondence | RG1 qualified conditional main-file baseline | same | same | UNKNOWN | UNKNOWN |
| Frozen veins/points | preserve RG2-A v1 | preserve RG2-A v1 | preserve RG2-A v1 | conditional initialization v2 | conditional initialization v2 |

The Kreet owner capture was **not** an observation of these later save epochs.
Its first `baseline-003` record is observer 0.1.0 on 2026-10-10T01:16:44.465Z,
PID 17596, module runtime base `0x00007ff73b380000`, game SHA-256
`7e9adb1414a8e1b325e5e1f097b9b17b78deb7eebeda37a333351a43a60f9d28`,
observer DLL hash `0e910a3ec6362adf050add3a9cd754246ac12f25e5ae55426d1c44ed93848a31`.
The terrain raw file is a 512-byte real manager extent: uint32 at offset `0x80`
is `259487`, vtable RVA `0x04b3e328`. The nine checkpoint/19-file replay verifies
original manifest hashes before/after. It is non-atomic; no source-region or UI
epoch linkage is added retrospectively. RG1's conditional frame qualification
and current static producer are stronger than treating numeric coincidence as
proof of a universal identity rule, but neither establishes historical cache equality.

## Discriminating the two mature frames before generating veins

The initial audit fixes the candidate population in code and uses the same maps,
registry, 150-unit radius and maximum width 111 in both variants. Descriptor
variant translates **both query and frame**; neither chooses sources from a
desired resource list. Every source is retained whole; no path is generated.

| Exact example | Site-origin hypothesis | Descriptor-origin hypothesis |
|---|---|---|
| Feynman geographic source `(25116,32436)` | native source origin `(-1000,-1200)`; first packed key `02a38a287a0f5e3d`; CRC with derived owner `3312174398` | origin `(-3800,-1400)`; key `02a38a2879495369`; CRC `2611716712` |
| Carinae geographic source `(21372,15612)` | origin `(-2900,-3000)`; key `039a0a4031614844`; CRC `3024406632` | origin `(-3800,-3800)`; key `039a0a402e4944c9`; CRC `1875245605` |

All eight paired first keys differ; sixteen independently recomputed key/CRC
values agree with the primary arithmetic. These counterexamples reject the
shortcut “select a plausible frame, generate, translate the output afterward”.
They do **not** falsify either frame as the engine's actual selected input.
Equal geographic sources and masks likewise cannot choose between frames.

## Selection reconstruction and remaining exact edges

Current installed PPBD/RSGD/IRES data plus the owned model select Feynman's
Nickel root `000057cb` through RSGD `0037c672` and Copper root `000057cf`
through `00258050`; Carinae's Hills root is Iron `000057c7` through PNDT override
`0018ce04`. No Special selection occurs in these model rows. The actual installed
FrozenNoLife09 RSGD additionally contains Everywhere Water `000083ec` (rarity
byte 6); Canyons/Hills relevant RSGDs do not. The initial no-Everywhere assertion
failed and was preserved. Existing primary `resource-availability-cont-01.tsv`,
`FUN_14079b520` decompilation lines 2359–2402, resolves the separately selected
Everywhere resource, searches its own descriptor in component/current BIOM
tables, and calls `14079c470` after main and Special with weight 1 (constant
initialized at line 2085). It is not another inactive-weight Common root.
This task records that required branch without silently treating the Kreet
main-only driver as a complete Feynman population evaluator.
Main-family equality holds across the two tested atmospheric populations;
final view equality fails and the failed equality is retained.

For uniform mask 8 the mapped inactive multipliers apply: common 0.3,
uncommon 0.2, exotic 0.01. Mask 4 admits the selected ordinary rarities at weight
1. Descending distinct rarity gives Feynman Cobalt→Nickel or Ionic
Liquids→Fluorine→Copper, Carinae Rothicite→Alkanes→Iron. These are current
**candidate main-family operands**, not a captured CTPerBiomeData or proof that
the historical descriptor-selected branch chose the same definition.

The static attempts include manager initialization/reset, exact world-component
system/body lookup and context copy (`N001–N006`), packed-key decoding/body check
(`N006–N008`), map initialization and PNDT registration (`N010–N014`).
`14078b030` demonstrably accepts angular context or optional explicit key;
`14079c540/14079c5e0` demonstrably permit component/current/alternate RSGD
choices. Existing S1/Save52 component catalogs and archived terrain extents were
consulted; no qualified saved-component-to-these-selected-operands mapping is
present in those receipts. This is scoped archive coverage, not whole-save absence.

The subsequent [angular-snap/prediction continuation](predictions.md) supplies a
positive discriminator for **ordinary initialization** and freezes complete
conditional geometry. The paragraphs above preserve the initial uncertainty;
they do not retract that stronger scoped result.

For historical loaded/rebased correspondence the smallest discriminator is the
selected descriptor and owner-grid local frame
for each exact Workshop epoch, plus the selected per-biome root/RSGD where the
lookup's alternatives differ. An already archived coherent matching receipt
would suffice; a later acquisition requires a new authorized method. A UI list,
nominal BIOM set, atmosphere FormID or extractor name cannot supply this missing
edge. The initial code and candidate input assessment retain UNKNOWN; they do not
claim every possible offline method has been closed.
