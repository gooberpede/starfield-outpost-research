# Modifier producers and the timer consumer

Basis: Bethesda main Starfield.esm, hash and record offsets in
[native contract](production-native.md); local `perks01.json` records all 502
PERK definitions, and `extra-definitions01.json` records selected globals/NPCs.
The original [inventory reader](../../../research/e1-extractors/production-definitions.py)
uses the owned ESM reader. No implementation was copied from outside sources.
All positive participants below are **confirmed static definition participants**
of timer A1 / operation 3 / EPFT 1, not actual assigned actors observed live.
Consumer: `140f7bd20` → `140c94060` → `140c93cf0` → `140c94430`.

| Producer, FormID / ESM offset | Entries / factors | Classification and exact scope |
|---|---|---|
| Crew_Outpost_Management 21b8c3 / 1290053167 | Zero-based ranks 0/1/2: .95/.91/.87 | Confirmed interval participant conditional on an eligible supplied actor and its active entry; conditions include gas/liquid/solid, organic and manufactured keywords. Assignment/list membership unresolved. |
| Crew_Outpost_Engineering 21b8c8 / 1290054956 | Ranks 0/1/2: .91/.83/.77 | Confirmed timer definition, **excluded for ordinary inorganic within these inspected keyword conditions**: manufactured keyword only. No claim that this actor has no other effect. |
| Crew_Outpost_MinibotSanitation 04297f / 1289934043 | Rank 0: .91 | Confirmed conditional inorganic timer participant. Excludes manufactured/organic and includes the three inorganic families. Robot participation uses the shared perk consumer if the actor reaches the supplied list; no separate robot quantity rule found here. |
| Crew_Outpost_MinibotGarden 04297e / 1289933539 | Ranks 0/1/2: .91/.83/.77 | Timer participant for organic; excluded ordinary inorganic within the inspected organic keyword condition. Organic behavior itself is deferred to E2. |
| Skill_OutpostManagement 23826f / 1290088099 | Rank 3: .5 | Confirmed player interval participant under the three inorganic family conditions and active-entry policy. Definition rank does not prove player's unlocked rank. |
| Skill_SpecialProjects 04ce2d / 1289934915 | Rank 3: .95 | Confirmed inorganic timer participant. Extra random production is **unresolved**, not established by this timer entry or a similarly named GLOB. |
| MagPerk_ConstellationSpacefarersGuide 208e92 / 1290020838 | Ranks 3/4: .95 each, EPFB 0300/0c00; no CTDA on these entries | Confirmed magazine-definition timer participant. Whether both entries are active together, acquisition and repeatability remain unresolved. No blanket magazine exclusion. |
| OutpostPlanetSurveyProductionBoost 30b589 / 1290346023 | Five conditional rank entries: .95 | Confirmed conditional timer definition; exact completion predicates/acquisition remain unresolved. No claim that every surveyed planet receives the factor. |
| _RENAME_TestOutpostCrewBuffProductionRateGas 26fe1a / 1290145109 | Rank 0: .5, gas condition | Confirmed test-named timer definition; actual obtainable/assigned producer unresolved. Do not advertise it as a gameplay bonus. |

These total 20 entries in nine PERKs. The 51 `MagPerk_` definitions were included
in the 502-record census; only the named magazine PERK has A1/op3 entries in
that inspected set. There are no D8 DATA entries in that set. DLC, plugin
overrides, dynamically added effects, scripts and non-PERK quantity machinery
are outside the negative's coverage. A name search is not a closure proof.

Condition wire CTDA carries function low ushort 0230 and keyword FormID at +0c.
Native registration names HasKeyword with ID 1230, callback `140c49960`
(exports 03/05/08). Matching this condition to keyword tests is a qualified
definition/native interpretation; the full condition-flag/OR evaluator is not
reimplemented here. Family keys: gas 299548, solid 299549, liquid 29954a;
organic 2c5a95 (ESM offset 668028), manufactured 23ceb6 (582803).
The three inorganic alternatives occur as OR chains in the applicable entries;
condition context and active rank selection still govern actual evaluation.
The survey PERK's additional predicates are retained raw in the local inventory,
not relabelled from a display description.

Selected NPC definitions give a producer bridge, not assignment proof:
OutpostManagementSpecialist 02fdf7 PRKR 21b8c3/rank 1;
OutpostEngineeringSpecialist 02e91c PRKR 21b8c8/rank 1;
AndromedaKepler 16b3d3 PRKR 21b8c8/rank 2;
ModelA01 1f416e PRKR 21b8c8/rank 1;
ModelA02 1d9250 PRKR 21b8c3/rank 1;
Garden minibot 04297c PRKR 04297e/rank 1;
Sanitation minibot 0bd67e PRKR 04297f/rank 1. PRKR rank encoding is not PRKE's
zero-based entry index; no rank-composition algorithm is inferred from this table.

No named candidate is proven to affect current eligibility or actual quantity
solely because it has an interval entry. Effective AV modifiers and D8 remain
separate dependencies. Evaluation order is supplied actors, then player;
within active entries the native copied-list order and predicates matter.
Multiplication can compose eligible entries, but the active-list builder may
select ranks/participants before consumption. This distinction motivates the
[prospective test](production-feasibility.md).
