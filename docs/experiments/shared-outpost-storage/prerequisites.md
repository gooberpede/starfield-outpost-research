# Construction prerequisites and admission

[Answer](report.md), [methods and address domains](methods.md),
[definition pins](sources.csv). `nNNN` locators refer to local native exports.
Installed records are definition evidence, not a measured menu interaction.

Shared Outpost Storage is add-on `SFBGS00D.esm`, local COBJ `02af79`, building
CONT `02af77`. The add-on has Starfield.esm as its sole master: file-encoded
`0102af77` is not a universal runtime FormID. Physical offsets are 100611193
for the COBJ and 266798 for the container in definitions01.json.

| Actual field | Requirement / significance |
|---|---|
| CTDA 0 | `LocationOrParentHasKeyword(Starfield.esm:319847) == 0`, run-on 0 |
| CTDA 1 | `GetPerkRank(Starfield.esm:23826f) == 4`, run-on 0; Outpost Management |
| CTDA 2 | `GetPerkRank(Starfield.esm:2c59e0) == 4`, run-on 0; Outpost Engineering |
| RQPK | The same two perks, each UI requirement rank 4 |
| FVPA | Aluminum `0057d6` x2 and Structural `0777fa` x4 before consumer cost modification |
| BNAM/FNAM | Storage category `27319a`; these do not implement the numerical limit |
| JNAM | Add-on GLOB `02af7a`, initial FLTV 1; one matching recipe-quota representative in the selected outpost |

All three CTDA flag bytes are zero: comparisons are **equality**, connected by
AND. Do not silently translate the installed comparison into a general >= 4
predicate for hypothetical higher ranks. Padding bytes beside the u16 function
index are not additional opcodes. `n017` registration windows positively bind
`01fb` / command `11fb` to GetPerkRank and `038b` / `138b` to
LocationOrParentHasKeyword. `n023:140c412a0/140c5c0c0` corroborate dispatch;
the latter uses the reference's location/parent-location keyword path. The
keyword's installed description concerns blocking construction at particular
locations; it is not evidence of an inventory-use prohibition.

## Definition to menu and accepted build

The COBJ loader `140a02160` (n017) consumes recipe fields. Existing recipe-tree
nodes are evaluated by `1421f66c0` and `1421f6f00` (n010/n019). The latter
constructs condition context with **player subject** and the current selected
Workshop context `145f5d8e8` as target, then evaluates node+68 with
`140e466f0`. Run-on selection is therefore material; the two contexts must not
be conflated. `140e466f0` (n019) ORs chains bearing flag bit 1 and ANDs completed
groups, with short-circuiting. Empty lists pass in this mapped evaluator.

`1415795f0` (n022) supplies a concrete hidden/unavailable distinction. It first
requires category/variant eligibility (`1421f68f0/1421f6bd0`) and the ordinary
condition result. On condition failure it retries while filtering command IDs
`11c0`, `11fb`, `136a` (perk/research-related predicates). A surviving retry
retains the recipe in the unavailable group and sets its corresponding boolean
through the preview data; an unfiltered location/quest failure is not rescued
by that retry. `141579fc0` (n026) builds the actual preview entry. Thus the
native provider distinguishes omitted candidates from retained unmet
prerequisites. Exact localized lock wording/art and a live screenshot are
NOT TESTED. Other category/variant gates can still omit a recipe.

Candidate refresh `1421dcb10` (n004) separately writes ingredient sufficiency
at frame+61d, prerequisite admission at +61e and quota at +61f. Its perk path
includes `14172c950`, which extracts typed PERK requirements with `1417f82b0`
and compares player selected ranks through `141955080`. It also calls the
ordinary recipe-tree condition evaluator. The status reducer `140f3f9a0`
(n008) maps failed prerequisites to status `1d`, missing ingredients to `18`,
and exceeded quota to `1f`, subject to preceding placement gates. These are
different from merely appearing in the build menu.

Reuse [L1](../limits/native.md): `1421dcb10 -> 140f3b170` compares JNAM
identity against the selected-outpost representative set; `14157b0c0` supplies
the quota card. `1421b2360/1421b2e20` require accepted status 2 before the
ordinary commit path. Creation updates that set; moving rebuilds membership,
and ordinary removal erases it. No new atomic recheck inside every low-level
placement interface, nor every disabled/destroyed event callback, is established.

## Differentiated controls

Fresh physical context01.json includes:

| Control COBJ, main-game local ID | Actual contrast |
|---|---|
| Small solid storage `299547` -> CONT `23aed9` | No CTDA/RQPK/JNAM in this recipe; resources and spatial/budget gates still apply |
| Large solid storage `2331e3` -> CONT `23aedb` | CTDA `036a` requires research project `389f13` complete; no shared-storage perk pair |
| Transfer Container `2ce193` -> CONT `2ce194` | JNAM `2ce192`, separate one-container quota; no shared keyword or two-perk requirement |

The large-store research condition is a completed-project predicate, not an
industrial production bonus. Existing [E1 Research Projects](../inorganic-extractors/stacking-report.md)
supplies completion/unlock context and its limits. No universal perk catalogue
or general progression study was undertaken.

The mapped existing-container consumers test the special keyword/backing
reference and source context, not this recipe's CTDA/RQPK. Losing a construction
prerequisite is therefore **not an identified existing-use revocation rule**.
Actual perk-removal, over-quota and reload transitions were not performed.
