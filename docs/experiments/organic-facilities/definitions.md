# Organic facility and recipe definitions

[Report](report.md), [facility catalogue](facilities.csv), [recipe catalogue](recipes.csv),
[source pins](sources.csv). Definition conclusions are proposed STRONG / STATIC;
physical field equality is PROVEN within the checked records. Authored tables
are REVIEW-REQUIRED; full record fields stay LOCAL-ONLY.

All eight-digit FormIDs in these tables are file-relative identities in the
installed **Starfield.esm**, SHA-256
`1dabed00c3f4282dd3bb54d2e9601e40b577d8742d078b7ccef203adbfef0da7`.
Offsets are decimal original ESM file bytes, not native addresses or save offsets.
There is no DLC/mod override merger or runtime load-order assumption.

## Facility enumeration and construction

The complete main-ESM CONT walk selects the conjunction of KWDA
OutpostCategoryBuilders `002731a0` and ResourceTypeOrganic `002c5a95`, rather than
an EditorID substring. Exactly six records qualify. Native selector dispatch uses
the OrganicResourceType property, built-in AV `00000387`: 1 for flora, 2 for fauna.
This distinguishes organic producers within the shared builder category; it does
not make every builder an organic facility. Names and tier suffixes below label
the independently linked definitions.

| Facility / tier | Producer CONT | Construction PKIN | Construction COBJ |
|---|---|---|---|
| Greenhouse 01 | 002965f7 | 002491f5 | 0028ad59 |
| Greenhouse 02 | 002953e2 | 002491f0 | 0028ad55 |
| Greenhouse 03 | 001fb279 | 001fb265 | 001fb25d |
| Husbandry 01 | 00298a36 | 00288f94 | 0028ad81 |
| Husbandry 02 | 001fb27b | 001fb278 | 001fb25c |
| Husbandry 03 | 001fb27a | 001fb26e | 001fb25b |

Each PKIN CNAM names a template CELL. A separate complete group/header walk
locates 753 REFR children across those six cells, with exactly one corresponding
organic producer CONT reference per cell. The CSV records those REFR identities,
physical offsets and cell identities. Thus construction recipe → PKIN → CELL
child REFR → CONT is established without treating the pack-in dummy as the
producer. The existing [Workshop root contract](../workshop-membership/report.md)
explains the distinct assembly root and operational member in saved instances.

Two additional construction-category COBJ records, `001fb259` and `001fb25a`,
create FLST category lists `001fb258` and `001fb257`, rather than another producer
CONT or seventh/eighth facility. They have no FVPA construction inputs. Six
concrete construction recipes target the six PKINs above. Recipe CTDA parameters
gate greenhouse 02/03 on Horticulture `00389f09` / `00389f0a`, husbandry 02/03
on Domestication `003e3d4d` / `003e3d4e`. The two tier-01 recipes have no CTDA.
These are construction gates; native selector gates are documented separately.
See the existing [Research Project condition contract](../inorganic-extractors/stacking-research.md)
for the wire/native IsResearchComplete distinction and research prerequisites.

All six containers carry PowerCanBePowered = 1. Each flora base has 30 organic
resource AV properties; each fauna base has 90, including canonical and both
fauna-specific alternatives. **Every resource value is initially zero.**
Property presence admits a candidate; a positive value identifies configured
production. Medium/large HarvesterRateMult raw deltas are −.2f / −.5f; tier-01
omits that property. Effective defaults, overrides and modifier addition retain
the [E1 provider contract](../inorganic-extractors/arithmetic-production.md).
No raw negative property is itself a complete current timer multiplier.

## Recipe enumeration and inputs

Collect IRES records whose NAM1 AV occurs in those facility property sets,
then follow NAM2 → COBJ, CNAM → MISC and NAM3 → interval GLOB. This yields exactly
90 resource/recipe rows: 30 canonical, 30 fauna-herbivore and 30 fauna-carnivore.
Every recipe NNAM is 1. FVPA has ordered 12-byte entries: IRES FormID, u32 count,
u32 trailing field (zero in these rows). The three complete observed patterns are:

| Definition family | Rows | Required IRES identities and quantities |
|---|---|---|
| Canonical, used by flora selection | 30 | Water `000083ec` ×1 |
| Fauna herbivore alternative | 30 | Water `000083ec` ×1; Fiber `00077821` ×2 |
| Fauna carnivore alternative | 30 | Water `000083ec` ×1; Nutrient `000777e6` ×2 |

These are recipe requirements per requested ordinary cycle before the native
availability cap and consumption; they are not inventory totals or sustained
throughput. No fourth pattern occurs in this 90-row main-game property-linked
coverage. This conclusion does not certify all modded/unused recipes.

Interval is **resource-linked**, not derived from its rarity name. For example,
canonical Structural is named common but links `0005ef3f` (54 seconds); canonical
Antimicrobial/Ornamental link `0005ed87` (36 seconds) despite uncommon names.
The CSV retains every actual link. Binary32 hours ×3600 produces nominal resource
intervals 36, 54, 72, 90 or 108 seconds in this set.

Concrete greenhouse example: small CONT `002965f7`, selected canonical Nutrient
IRES `000777e6` → AV `002ac11b` → COBJ `002ac0fc` → MISC `000777fd`.
The recipe is at ESM byte 1300739177, Water ×1, NNAM 1, interval GLOB `0005ed87`
= 36 seconds. Conditional selected resource AV = 1, no active A1 timer entries,
no overrides/modifiers and ordinary positive HarvesterRateMult default 1 yield
one requested unit per 36 seconds and nominal 60/36 units/minute. This is a
definition/native example, not a runtime measurement or proof of planet eligibility.

Concrete husbandry example: small CONT `00298a36`, selected herbivore Nutrient
IRES `00224640` → AV `002246b4` → COBJ `00224669` → the same Nutrient MISC
`000777fd`. Recipe byte 1300556297 requires Water ×1 and Fiber ×2, NNAM 1;
GLOB `0005ed87` again gives 36 seconds. With the same explicit baseline conditions,
its ordinary request is one unit per 36 seconds, capped by actual input availability.
Carnivore COBJ `00224686` at 1300561743 changes the food input to Nutrient ×2.
Resource identity must therefore retain the fauna-specific IRES/AV/recipe;
canonical output MISC alone loses the input distinction.

## Existing source implementation and corroboration

The accessible supplied script is named `Starfield - Export Planet Biome Organic
Resources.pas`, without the brief's `(2)` suffix; its internal heading and version
are **Starfield - Export Biome Organic Resources.pas, 2.0.3**. It was inspected,
hashed and never executed or incorporated. Its actual code follows PNDT biome
lists, flora MISC CVPA canonical resources and fauna resource OMOD → AVIF →
reverse IRES → COBJ → output MISC CVPA. It walks object-template links for fauna
domesticability and explicitly recognizes mod_CCT_Special_Domesticate; flora
uses OutpostCanDomesticate. Ambiguous resource lineage is retained as unresolved.
Its two input slots are deliberately not a diet export or a native menu oracle.

The available maintainer-owned `starfield-outpost-network` at commit
`9e3005aff9487f11343b39a7534a2070b429ad5f` contains the source CSV and
`scripts/biome-reference-data.mjs`. That transformation infers sourceClass from
the **input signature**: plant, herbivore or carnivore. It does not independently
prove a diet-keyword selector. The three profile records are consistent with
the 90 recipes. No sibling implementation or supplied Pascal code was copied.

The CSV has 3,855 Planet × Biome × Species rows: 1,596 flora and 2,259 fauna.
1,041 flora and 468 fauna rows are labelled domesticable (repeated species across
biomes remain repeated rows). All 3,851 resolved rows have input identities and
counts matching an installed canonical or fauna-specific recipe for that output;
four fauna rows are NoLinkedResource: Terrormorph `002b2293` on Toliman II
(biome indices 0/2/3) and Chasmbass `00194835` on Volii Alpha (index 0), all
source-labelled non-domesticable. This checks recipe patterns, **not** every
NPC OMOD, diet or domesticability lineage and not in-game menu membership.

Reproduction: run [catalog.py](../../../research/e2-organic/catalog.py) with a fresh
`--run inventory02` destination, [derive.py](../../../research/e2-organic/derive.py),
and [assemblies.py](../../../research/e2-organic/assemblies.py), using fresh
`--run` names and `--inventory` paths where supported (existing receipts are
intentionally exclusive). The first
walk includes 41,178 selected-type records; derive independently rereads every
field of 340 selected physical records, including repeated fields/decompression
closure. Inventory01 omitted PKIN/FLST and remains preserved; inventory02 adds
them rather than treating the initial omission as absence.
