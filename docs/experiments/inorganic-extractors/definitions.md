# Extractor identity, family and definition evidence

[Report](report.md), [native dataflow](native.md), [source inventory](sources.csv).
All definition IDs below are plugin-qualified local FormIDs; an unprefixed ID in
the table means `Starfield.esm`. They are not runtime pointers or saved tokens.

The existing [extractor association](../extractor-resource-association.md) uses
CONT plus category KYWD `008406`, not EditorID spelling, to select 159 installed
bases. Positive resource PRPS AVIF → IRES NAM1 → NAM2 COBJ → CNAM item resolves
all 159. This is DEFINITION-DERIVED configuration, not measured production.
Builders/fabricators and organic facilities are not admitted merely by a name or
generic Workshop keyword. The native category tests in `140f7c9f0`, `140f7cab0`
and `140f7cb70` are separate consumers; their default identities must be resolved
before interpreting them as one family. E2 mechanics were not investigated.

Family KWDA entries `299548` gas, `299549` solid and `29954a` liquid classify
43, 89 and 24 catalog bases respectively. Three category-qualified Tetrafluorides
bases `06ac88`, `20a074`, `20a06d` have none of those keys; their MODL paths
identify GasSmall01, GasMedium01 and GasLarge01. Requiring a family key would lose
these valid definitions. This counterexample limits a universal keyword classifier.

| Family / resource | Small base / physical ESM offset | Medium base / offset | Large base / offset | Independent model evidence |
|---|---|---|---|---|
| Solid iron | `05ef19` / 5403487 | `20a062` / 5658658 | `20a04a` / 5641314 | Driller01; SolidMedium01; SolidLarge01 |
| Gas He-3 | `06ac84` / 5410474 | `20a07c` / 5678334 | `20a084` / 5684279 | GasSmall01; GasMedium01; GasLarge01 |
| Liquid water | `27ab66` / 5784407 | `20a073` / 5671521 | `20a06c` / 5666198 | LiquidSmall01; LiquidMedium01; LiquidLarge01 |

MODL is definition evidence alongside family/resource properties. The small solid
model is `SetDressing\Driller\Driller01.nif`; medium/large solid and ordinary
gas/liquid paths are under `Harvesters`. This supports model/size classification
of these examples. A universal numeric native tier field is not established.
The 159-base census is completeness within the existing qualified category
catalog, not completeness of all installed equipment or all runtime objects.

Atmospheric water `06ac92` and He-3 `0083fe` use `GasExtractor\GasExtractor.nif`
and PRPS `0083ff=1` (HarvesterAtmosphere). Ordinary liquid-water tiers carry
`271128=1` (SkipResourceVeinCheck). The existing availability N34 contract
selects biome instead of the ordinary spatial list for that property; these
are substantive exceptions to equating all inorganic extractors with vein checks.

X-Tech bases `SFBGS050.esm:01662c`, `07e613`, `07e614`, `07e615` use Driller01
but have `271128=1` and `31986f=1` (PlaceAnywhere). Their resource association is
`SFBGS00D.esm:033e3f` → recipe `05f4db` → item `033e3d`. The static flags are
useful classification evidence; no qualified placed X-Tech instance or runtime
production result exists in this corpus. No ordinary size/rate rule is forced
onto this exception.

PRPS AVIF `008407` is WorkshopHarvesterRateMultAV. The sampled gas/liquid small
bases contain 1; medium −0.2; large −0.5. Small iron lacks this key, with medium
−0.2 and large −0.5. X-Tech lacks it. These are raw properties, not literal units
per second or a multiplier formula. The native effective interval dispatch is
documented separately; complete linkage of every property to its modifier chain
remains qualified. Iron COBJ `05ef53`, physical offset 1300253652, has CNAM
`00556e` and NNAM bytes `0100`; NNAM alone is not promoted to realized quantity.

Save examples are retained in the original evidence rather than re-exported as
bulk data. Controlled S3 token `822da9`, record ordinal 10539, decoded-stream
range 1299733–1300165, body 1299791, resolves base `05ef19`, PRPS entry 2 AVIF
`05ef18`, IRES `0057c7`, COBJ `05ef53`, item `00556e`. S7 deletion and all
no-action controls constrain the classification. Save52 has 63 recognized
references, 37 bases and 29 resource associations; the subsequent
[availability validation](../resource-availability/validation.md) joins all 63
to saved ordinary owners and producer/root representations. These are supported
installed examples, not an exhaustive current active-player census.

The verifier checks 13,276 cached CONT/KYWD/AVIF/IRES/COBJ records directly at
their original ESM offsets, reconstructs the catalog, and hashes the original
24 distinct archived saves and installed source files. It does not freshly
decode saves or measure current status. Exact selected models and all category
rows remain in the ignored verification receipt; no game assets are bundled.
