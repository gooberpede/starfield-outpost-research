# Fabricator definitions and exact recipe identities

The installed main-game definitions provide **three ordinary fabrication
families, with 11, 10 and 9 products**. Each construction choice has a distinct
product-preset producer base; those bases share their family's complete property
catalogue. The working expectation of ten products in every family is therefore
superseded. [Facilities](facilities.csv) retain all 45 manufactured builder CONT
records, including 15 exceptions outside the ordinary construction lists.
[Recipes](recipes.csv) retain 43 recipe-bearing property-linked IRES definitions;
the `ordinary_tiers` column selects the 30 ordinary products. The exceptional
rows are deliberately distinct from ordinary menu choices.

Evidence: definition-backed, with physical record equality checked. All FormIDs
are eight-digit, file-relative **Starfield.esm** identities, SHA-256
`1dabed00c3f4282dd3bb54d2e9601e40b577d8742d078b7ccef203adbfef0da7`.
All CSV offsets are decimal original ESM file offsets. These are not addresses,
save offsets or runtime load-order IDs. Main ESM only; no DLC/plugin override
merge or actual loaded-menu enumeration is claimed. Raw record fields remain
local in `.local-work/e3-fabricators/catalog03.json`.

## Population and construction relationships

The complete prior E2 selected-type inventory is reused with attribution to
[E2's catalogue and assembly readers](../../../research/e2-organic/README.md).
[E3's reader](../../../research/e3-fabricators/catalog.py) selects the conjunction
of KWDA OutpostCategoryBuilders `002731a0` and ResourceTypeManufactured
`0023ceb6`. It then associates properties through exact reverse IRES NAM1 AV
links, with no producer or resource EditorID substring filter. Names label the
result after structural classification.

| Family | Construction COBJ → FLST | FLST PKIN choices / producer bases | Research condition |
|---|---|---:|---|
| Tier 1 | `002731a1` → `0029c458` | 11 / 11 | Manufacturing 01 `00389f11` |
| Tier 2 | `00249ba4` → `0029c459` | 10 / 10 | Manufacturing 02 `00389f12` |
| Tier 3 | `00249ba3` → `00249ba5` | 9 / 9 | Manufacturing 03 `00389f13` |

Every FLST LNAM targets a PKIN; each PKIN CNAM targets a CELL. An independent
full ESM group/header walk finds exactly one manufactured producer REFR in each
of these 30 cells. The CSV preserves the PKIN, CELL, child REFR and CONT join.
Construction roots and operational members remain separate identities under
the established [Workshop membership contract](../workshop-membership/report.md).
The construction CTDA wire function is IsResearchComplete, using the named RSPJ
above; see [E1's research contract](../inorganic-extractors/stacking-research.md).
These conditions unlock construction; they do not substitute for output-recipe
conditions during selection.

Every ordinary base has all of its family's output AV properties. Each has one
preset AV = 1 and all other catalogue AVs = 0. The shared presence set admits
candidate resources; positive selection and effective production state are
separate contracts in [the native report](native.md). All ordinary bases have
PowerCanBePowered `0005fbbb` = 1. Built-in property `00000330` has raw values
5 / 8 / 12 by family. HarvesterRateMult AV `00008407` is absent from ordinary
base PRPS; the [shared effective-provider rule](../inorganic-extractors/arithmetic-modifiers.md)
and its default 1 apply conditionally, with saved overrides and modifiers still
possible. Raw property `000003a2` = 1 is retained as a separate property and is
not relabelled HarvesterRateMult.

The tier-3 property union has exactly nine members. OutpostBuilderC01_CommRelay
`00249b9f` is outside the ordinary construction FLST; its presence among the 45
keyword-classified bases does not create a tenth ordinary tier-3 product.
Thirteen other exceptional bases have CUT names and one has DELETEME; these
labels are not used as the exclusion criterion. The criterion is actual
construction-list reachability. Those definitions may have broader or obsolete
property sheets. One property-linked IRES, SubstrateGravLaminate `00203ea5`, has
NULL NAM2 and no resolvable COBJ; it is retained as `NULL_NAM2` in the local
receipt. The ordinary catalogue does not include it. All 30 ordinary recipes
have nonempty input requirements; exceptional empty-input recipes do not prove
ordinary free production. The separate TEST construction recipe `002407d9`
targets `002407d8`, outside the three ordinary family lists.

## Inputs, output counts and conditions

For every ordinary property AV, reverse IRES NAM1 identifies exactly one IRES.
IRES NAM2 identifies its automated-production COBJ; COBJ CNAM identifies the
output MISC; IRES NAM3 identifies the interval GLOB. The table preserves every
IRES, AV, recipe and output identity. Inputs are ordered FVPA triples of IRES
FormID, u32 required quantity and u32 trailing value. Every ordinary input has a
positive count and trailing value zero. This is an input-requirement list, not
inventory possession or proof of sufficient connected supply. Each ordinary
COBJ NNAM is 1 and the 30 output MISC identities are distinct.

Tier-1 ordinary output COBJ records have no CTDA. All ten tier-2 and all nine
tier-3 recipes have a Skill_SpecialProjects `0004ce2d` condition: wire function
`01fb`, flags `60`, comparison float 2, 3 or 4. The exact bytes are retained in
the `conditions` column as definition metadata. In
particular, Sterile Nanotubes, Nuclear Fuel Rod, Control Rod, Microsecond
Regulator and Power Circuit use comparison 3; the seven unique-resource tier-3
recipes use comparison 4; the other seven tier-2 recipes use comparison 2.
These are definition prerequisites; they are **not established native
fabricator selection gates**. The native generic selector walks AVIF records,
checks type 9 and clear flag bit 1 (mask 2), follows the AV's linked IRES and uses the
shared admission predicate. That mapped selector does not call the recipe CTDA
evaluator. All 30 ordinary AVIFs have NAM1 = 9 and AVFL bit 1 clear. See
[native.md](native.md) for the exact positive native gates and the boundary
between recipe metadata and actual enforced selection conditions.

No Industrial Workbench recipe or rate is substituted for these exact IRES →
COBJ links. Main-game product intervals are resource-linked GLOB hours ×3600,
rounded to binary32, rather than a single common family interval. The actual
ordinary values are approximately 7.92, 11.88, 15.84, 31.68 and 63.72 seconds.
Their binary32 values are preserved in the CSV. The shared scheduler and timer
modifiers still determine conditional effective production.

## Definition-based worked cases

Assume the selected AV is 1, native power/halt/operating gates permit production, all required inputs are
available, the native due loop is reached, no eligible timer perk changes the
interval, and effective HarvesterRateMult is its positive default 1. These
examples describe requested ordinary cycles, not measured or accepted output.

* Tier-1 Adaptive Frame: CONT `0027319f`, IRES `00245775`, AV `00245794`,
  COBJ `002457c1`, MISC `00246b6a`; Iron IRES `000057c7` ×1 and Aluminum
  IRES `000057d6` ×1. GLOB `0014e8c2` yields 7.920000076293945 seconds.
  With selected AV 1 and one due cycle, the normal request is one ordinary
  product under those conditions; NNAM 1 is recipe metadata, not an independent
  quantity multiplier in the mapped creation path.
  Nominal requested capacity is approximately 7.576 units per engine elapsed
  minute (`60 / 7.920000076293945`), before input, scheduling and acceptance limits.
* Tier-2 Sterile Nanotubes: CONT `0022174e`, IRES `00245778`, AV `00245797`,
  COBJ `002457c3`; Molecular Sieve IRES `00245786` ×1, Vanadium IRES
  `000057ed` ×2 and Solvent IRES `00077827` ×2. GLOB `0014eb51` yields
  31.68000030517578 seconds, NNAM 1. The recipe's Special Projects condition
  is present metadata; native fabricator enforcement is not established.
  Quantity-one nominal requested capacity is approximately 1.894 units per engine
  elapsed minute (`60 / 31.68000030517578`).
* Tier-3 Vytinium Fuel Rod: CONT `003a8615`, IRES `00203ea3`, AV `00203eb9`,
  COBJ `00203eac`; Indicite Wafer IRES `00203ea2` ×1, Nuclear Fuel Rod IRES
  `00245783` ×1, Vytinium IRES `00005df8` ×4 and Plutonium IRES `000057ee`
  ×2. GLOB `0014eb75` yields 63.71999740600586 seconds, NNAM 1. Connected
  upstream producers do not by themselves establish these input quantities.
  Quantity-one nominal requested capacity is approximately 0.942 units per engine
  elapsed minute (`60 / 63.71999740600586`).

## Verification and limits

`catalog03` independently rereads 308 selected physical records, comparing
headers, exact repeated fields and compressed-record closure with the E2 cache.
It also walks every ESM group header to establish the 30 pack-in child joins.
The subsequent catalogue run adds explicit family-set, preset, input-count and
distinct-output assertions. Initial `catalog01` used an incorrect resource
EditorID prefix and produced zero resources; it is preserved as a failed local
attempt. `catalog02` corrected the prefix; `catalog03` replaces that filter with
the structural NAM1 reverse join. None of those intermediate omissions was
interpreted as a scientific absence.

This is a reproducible definition population and linkage result. Mod overrides,
all possible dynamically added properties, loaded menu outcomes and current
effective values are outside this definition-only coverage. Authored tables and
this interpretation remain review-required; raw ESM bytes are local-only.
