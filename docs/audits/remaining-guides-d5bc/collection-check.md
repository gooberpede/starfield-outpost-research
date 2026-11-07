# Eighteen-subject collection check

[Handoff and dispositions](README.md) · [Claim crosswalk](claims.md) ·
[Proposed subject architecture](../publication-architecture-d5ax/architecture.md)

## Coverage and navigation

The root [reader route](../../../README.md) reaches the [guide index](../../guides/README.md).
Every subject is linked there within two clicks from the root. That index
links the [reference index](../../reference/README.md). Each guide links its
own technical page, with an original report and review reachable on the
subject route. The reference links back. The inventory reconciles the
[pilot](../reader-pilot-d5ay/README.md), [foundations](../foundation-d5az/README.md),
[production](../production-guides-d5ba/README.md) and
[logistics](../logistics-guides-d5bb/README.md) with the five new stems.

| Group | Stems accounted for |
| --- | --- |
| Pilot and foundations, 5 existing | resource-generation, identity, position, nominal-biomes, construction |
| Production, 4 existing | inorganic-production, organic-production, fabrication, power |
| Logistics, 4 existing | storage-and-output-links, cargo, shared-storage, stored-resources |
| Remaining, 5 new | crew-and-robots, defense, containers-and-displays, locations-ui, access-and-save-framing |

The bounded local check covers direct Markdown destinations and GitHub-style
heading fragments across the 36 subject pages, indexes, glossary, authoring
standard and new audit pages. It checks each path segment's case. It skips
fenced examples and web URLs and does not recursively certify historical
pages or their evidence access.

## Terms and authority at the handoffs

| Handoff reviewed | Term or authority boundary |
| --- | --- |
| [Position](../../reference/position.md), [nominal biomes](../../reference/nominal-biomes.md), [generation](../../reference/resource-generation.md) → [inorganic production](../../reference/inorganic-production.md) | A saved position supports a qualified frame, a base biome supplies a nominal field and the generation source supplies geometry. A point-admission result differs from a registered producer's IRES key. The row retains scheduling inputs, without retaining authority over the source geometry. |
| [Identity](../../reference/identity.md) → [crew](../../reference/crew-and-robots.md), [defense](../../reference/defense.md), [Locations](../../reference/locations-ui.md) | WorkshopItem owner identifies a member relationship. CrewAssignment records another edge. A selected attack quest can target eligible reverse members, while Locations admits registry rows using a different predicate. None of these implies the others or an exhaustive active-player census. |
| [Construction](../../reference/construction.md) → [crew quota](../../reference/crew-and-robots.md#admission-ownership-and-roster), [turret condition](../../reference/defense.md#health-state-flags-and-repair) | Shared JNAM threshold counts qualifying construction representatives. Crew slot charges, electrical allocation and destroyed state have separate consumers. Repair retains the reference in the mapped route. |
| [Inorganic](../../reference/inorganic-production.md), [organic](../../reference/organic-production.md), [fabrication](../../reference/fabrication.md), [power](../../reference/power.md) → [crew effects](../../reference/crew-and-robots.md#from-rank-to-a-consumer) | The actual producer row uses due timing and a current reason. A1 scales time at reset, while DB adds per generator before allocation. Assigned, active perk entries, powered bit, eligible operation and actual output describe different states. |
| [Production](../../reference/fabrication.md) → [storage and output links](../../reference/storage-and-output-links.md), [displays](../../reference/containers-and-displays.md) | New product can insert into a receiver. Redistribution moves stock already in source inventories. Capacity is effective weight on named paths. Display rule occupancy and actor slots supply different limits. Recipe resource identity, physical item form and a displayed world reference differ. |
| [Local stock](../../reference/storage-and-output-links.md) → [cargo](../../reference/cargo.md), [shared](../../reference/shared-storage.md), [Stored Resources](../../reference/stored-resources.md) | Physical bays and hold, a player-held backing inventory, ordered provider sources and a transient report have separate owners. Cargo's stage timer is separate from the producer or fuel countdown. Inventory units and resource grouping do not certify delivery or spending. |
| [Locations](../../reference/locations-ui.md) → underlying systems | Crew counts handle-list length, Cargo Links counts admitted endpoints, power copies summary and Outposts Built uses base deployment maximum. These neither resolve present crew nor confirm freight, current allocation or the effective placement allowance. Selected body metadata has a separate request and delivery. |
| [Save framing](../../reference/access-and-save-framing.md) → reconstructed claims | Persisted identifies a stored representation. Restored fields and reconstructed runtime structures have different obligations. Frame closure and resolved joins support their named result, while unsupported forms, opaque tails or queue timing limit claims of present state. Shipped compiled behavior and installed definitions have bounded version/override scope. |

### Findings and dispositions

| Issue and cited pages | Severity | Action and reason |
| --- | --- | --- |
| Coverage and reciprocal entry routes | Mechanical | All 18 pairs are accounted for. Five entries added to each index. NONE missing. |
| Identity guide linked its production-state handoff to geometry alone | Navigation | Routed it to [extractor production](../../guides/inorganic-production.md), which distinguishes ownership, point admission and actual production. |
| Readers moving from existing construction, power, storage or Stored Resources material needed routes to the new topics | Navigation | Added narrow cross-references for quotas and condition, DB eligibility, fixture residence and Locations field lineage. Preserved accepted mechanisms. |
| Refresh epoch previously illustrated only the copied inventory route | Terminology | [Glossary](../../reference/glossary.md#ingredient-providers-and-reporting) now distinguishes selected-body metadata from copied summary/inventory lanes. No global refresh authority inferred. |
| [RC1 C25 configuration column](../outpost-rc1-2026-10/capability-access.md) uses `0x0023826f` and `0x002c59e0` in the crew modifier row. [CR2](../../experiments/crew-skills/report.md) gives crew Management `0x0021b8c3` and crew Engineering `0x0021b8c8`. [Player timing](../../experiments/inorganic-extractors/arithmetic-modifiers.md) identifies `0x0023826f` as the player perk. | Historical identity ambiguity | New crew reference uses the direct CR2 grants, and the selected RC1 capability excerpt does not adopt the C25 IDs as crew grants. Original matrix preserved. Any historical corrigendum is a maintainer decision. |
| Older five-robot effect-bearing subset could be read as the complete category | Scope | Both new crew pages explicitly apply the [R1 eight-variant correction](../../experiments/robots/report.md). CR2 and its positive effects remain at their original scope. |
| Other material contradictions among accepted subject pairs in this bounded comparison | Semantic | NONE identified. Differences in source, item, owner, active, eligible, capacity and refresh refer to the named consumers above. |
| Exhaustive active-player census, live attack frequencies and repair, fully restored displays and crew, atomic panel freshness, safe arbitrary integrations | Scientific coverage | Open where indicated by original evidence. These questions require separate experiments or authority and do not invalidate the documented conditional mechanisms. |
| Direct primary witness access and first-release eligibility | Publication dependency | See the claim-specific record below. Resolvable authored links do not clear release rights or provide raw replay. |

## Representative independent reader route

Start at [Power](../../guides/power.md) with a base-20 generator and a roster
showing two Model A03 robots. Follow the new crew link to [eligible entries and
the generator example](../../guides/crew-and-robots.md#expect-the-effect-at-the-relevant-update).
Follow the [crew reference](../../reference/crew-and-robots.md#from-rank-to-a-consumer)
to the original [DB examples](../../experiments/robots/effects.md) and
[review](../../experiments/robots/review.md). The example predicts 26 only
under its premises. The nonpositive preliminary generator example and
the process-storage counterexample explain why a roster cannot certify
contribution. The [Locations badge reference](../../reference/locations-ui.md)
then explains what the visible count can support. The missing guide-level
power-to-crew transition was repaired. This route ends in authored evidence
and review without requiring private receipts or familiarity with brief IDs.

A second route starts with a visible item but an empty chest inventory.
The [storage guide](../../guides/storage-and-output-links.md) now points
to [fixture residence](../../guides/containers-and-displays.md). Its
[reference](../../reference/containers-and-displays.md#serialized-joins-and-fixup)
leads to the original [zero-count positive helmet join](../../experiments/containers-displays/saves.md#positive-native-display-witness)
and [review](../../experiments/containers-displays/review.md). Follow the
[access guide](../../guides/access-and-save-framing.md#reconstruct-a-saved-fact)
to distinguish record closure and load-time handle reconstruction from
settled visible state. Primary save replay remains a separate access tier.

## Fifteen reader journeys

| Pair | Understand | Reproduce | Challenge |
| --- | --- | --- | --- |
| [Crew and robots](../../guides/crew-and-robots.md) | The menu charges human slots, while robot placement counts constructions. A listed actor can have no active entry. | Count eight ordinary rows, five direct grants, three without direct grants and one limit global. | Follow [CR3 process loss](../../experiments/crew-lifecycle/native.md#entry-storage-loss-and-return) and [review](../../experiments/crew-lifecycle/review.md) plus [R1 report](../../experiments/robots/report.md) and [review](../../experiments/robots/review.md). The older subset and saved ranks do not establish historical output. |
| [Defense](../../guides/defense.md) | A one-shot check can return without a quest. The displayed condition has its own Health operands. | Extract saved damage from the authored row and use its documented 400 denominator. Compare 0.64 with 1 under default assumptions. | Follow [attack branches](../../experiments/outpost-defense/attacks.md), [report](../../experiments/outpost-defense/report.md) and [review](../../experiments/outpost-defense/review.md). Saved damage leaves causality open and Starborn roll is per eligible check. |
| [Containers and displays](../../guides/containers-and-displays.md) | A mounted item can be represented outside fixture stacks. An actor equips an instance through another route. | Check recipe/leaf/child counts from the authored definition rows. | Follow [SD1 report](../../experiments/containers-displays/report.md), [review](../../experiments/containers-displays/review.md) and [zero-inventory control](../../experiments/containers-displays/saves.md#positive-native-display-witness). A saved join leaves rendered restoration open. |
| [Locations](../../guides/locations-ui.md) | Crew and cargo badges describe different counts. Selection requests separate body metadata. | Check the three badge source relationships in the tracked lineage table. | Follow [LO1 report](../../experiments/locations-outpost/report.md), [review](../../experiments/locations-outpost/review.md) and [refresh boundaries](../../experiments/locations-outpost/native-and-ui.md#refresh-boundaries). A screen does not establish an atomic epoch. |
| [Access and save framing](../../guides/access-and-save-framing.md) | The route depends on whether the question asks about a definition, saved record or actual operating state. Internal discovery leaves caller safety open. | Count RC1 capabilities and run six synthetic framing checks. | Follow [RC1 report](../outpost-rc1-2026-10/report.md), [review](../outpost-rc1-2026-10/review.md), C20 and the [reference-queue decoy](../../experiments/active-outpost-identification.md#competing-rules-predictions-and-falsification). Exact framing leaves semantic classification open. |

Run these PowerShell examples from the repository root. The last needs
CPython 3 on the command path. Each reads tracked data or runs a synthetic
test. The checks do not replay installed data, proprietary instructions,
historical save bytes or any live event.

**Crew.** Expected output `8,5,3,1` in row, grant, no-grant and global counts.

```powershell
$rows = Import-Csv docs/experiments/robots/catalogue.csv
$grants = @($rows | Where-Object direct_perks -ne 'NONE')
$globals = @($rows.limit_global | Sort-Object -Unique)
"$($rows.Count),$($grants.Count),$($rows.Count - $grants.Count),$($globals.Count)"
```

**Defense.** Expected output `0.64,1`, the two conditional ratios.

```powershell
$text = Get-Content -Raw docs/experiments/outpost-defense/persistence.md
$row = [regex]::Match($text, '(?m)^\| ff0202dc .*?\| (-?\d+) \| ff047885 \|$')
if (!$row.Success) { throw 'Expected saved damage row absent' }
$damage = [int]$row.Groups[1].Value
$permanent = 400
'{0},{1}' -f (($permanent + $damage) / $permanent), ($permanent / $permanent)
```

**Containers.** Expected output `41,97,68,10` in matching recipes, recipe
rows, unique leaves and separately recorded pack-in children.

```powershell
$rows = Import-Csv docs/experiments/containers-displays/definitions.csv
$main = @($rows | Where-Object plugin -eq 'Starfield.esm')
$leaves = @($main | Where-Object role -eq 'recipe-variant')
$recipes = @($leaves.recipe | Sort-Object -Unique)
$bases = @($leaves.base | Sort-Object -Unique)
$children = @($main | Where-Object role -eq 'packin-child')
"$($recipes.Count),$($leaves.Count),$($bases.Count),$($children.Count)"
```

**Locations.** Expected output `True,True,True` for base maximum,
endpoint predicate and assignment-list count.

```powershell
$text = Get-Content docs/experiments/locations-outpost/field-lineage.md
$maximum = $text -match '^\| OUTPOSTS BUILT denominator.*base getter'
$cargo = $text -match '^\| Cargo Links integer.*active local endpoint predicate'
$crew = $text -match '^\| Crew integer.*handle-list count'
"$([bool]$maximum),$([bool]$cargo),$([bool]$crew)"
```

**Access.** Expected output 31 capabilities and six passing synthetic methods,
including unsupported/truncated input rejection and the decoy.

```powershell
$rows = Get-Content docs/audits/outpost-rc1-2026-10/capability-access.md
@($rows -match '^C\d{2} ').Count
python -B save-analysis/scripts/test_outpost_record_framing.py
if ($LASTEXITCODE -ne 0) { throw 'Synthetic framing checks failed' }
'6 synthetic framing tests passed'
```

## Publication dependency inventory

**PUBLICATION DEPENDENCY — EVIDENCE ACCESS PENDING** applies to the primary
witnesses below if the corresponding claims are selected for publication.
The [claim crosswalk](claims.md) gives specific paths, reviews and tracked
derivatives. The smallest outstanding witness classes in this pass are:

- **Crew and robots:** installed catalogue, selected grants and actual
  limit/dispatch/replay paths, plus protected historical reciprocal joins.
- **Defense:** compiled scheduler and quest branch evidence, native Health
  and repair, and the protected damaged and control records.
- **Containers and displays:** original admission, residence and fixup paths,
  with the protected slot/item/owner and mannequin equipment witnesses.
- **Locations:** installed/native/compiled producer-to-provider and graphics
  mappings. Historical screenshots are contextual and do not resolve epochs.
- **Access and framing:** decisive compiled/native inputs for the reviewed
  routes and protected originals for historical joins and coverage. The
  synthetic framing check is reproducible on tracked inputs.

Carry forward [B4-F1 policy](../../PUBLICATION.md),
[D5AS/C19 and historical-save dependencies](../publication-architecture-d5ax/evidence-access.md)
and the [resource reference access boundary](../../reference/resource-generation.md).
No original data, derivative package or release asset was acquired here.
Mechanical coverage and source-scoped semantic review do not substitute for
B6 clean-checkout, actual hosting, rights and final release decisions.
