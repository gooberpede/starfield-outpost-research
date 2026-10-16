# Practical timer stacking matrix

This table concerns the ordinary inorganic timer path and selected active ranks,
not every effect carried by these actors. Factors multiply **cycle duration**;
smaller means faster. FormIDs below are main Starfield.esm definitions. Native
selection proof is in [the contract](stacking-native.md); raw definition offsets
and factor bytes remain in the prior [modifier matrix](production-modifiers.md).

| Producer | Applicable timer factor | How it combines |
|---|---|---|
| Crew_Outpost_Management 21b8c3 | Current ranks 1/2/3: .95/.91/.87, with inorganic family condition | One selected rank per actor on normal rank changes. Distinct eligible assigned actors are each consumed, even with the same perk. |
| Outpost Management specialist NPC 02fdf7 | Direct PRKR 21b8c3/rank 1 | Concrete definition example for the first row, not proof of a loaded assignment. |
| ModelA02 robot 1d9250 | Direct same Management perk/rank 1 | Same timer factor as that perk on another actor; combines if present and eligible in E2. Its script/template inheritance remains separately qualified. |
| Sanitation minibot 0bd67e | Direct 04297f/rank 1: .91 | Inorganic condition. Explicit VMAD auto-assignment configuration reaches the same crew API; distinct instances can each contribute. |
| Garden minibot 04297c | 04297e, organic condition | Excluded for ordinary inorganic in this timer entry; organic E2 is not investigated here. |
| Crew_Outpost_Engineering 21b8c8, including ModelA01 1f416e and specialist 02e91c | .91/.83/.77 at current ranks, manufactured condition | Excluded for ordinary inorganic in these timer entries. The word “Engineering” alone is not evidence of an inorganic speed bonus. |
| Player Skill_OutpostManagement 23826f | Rank 4: .5 | Multiplies after the assigned-actor contributions; distinct perk from Special Projects. |
| Player Skill_SpecialProjects 04ce2d | Rank 4: .95 | Multiplies the timer; any extra-item effect is a separate unresolved quantity question. |
| Player MagPerk_ConstellationSpacefarersGuide 208e92 | Current native rank 4 or 5: .95 once | Rank-4 and rank-5 entries replace one another on the mapped transition. No .95 squared merely because both definitions exist. |
| OutpostPlanetSurveyProductionBoost 30b589 | .95 in each defined rank, conditional | Same selected-rank rule on normal changes; exact survey/acquisition predicates remain outside this closure. |
| Completed Outpost Research Projects | No direct timer factor found | Construction prerequisites; separately constructing unlocked objects/robots can change available equipment and participants. |

The direct NPC PRKR census also includes Andromeda Kepler's Engineering rank 2.
It is not a complete effective-perk catalog: Lin and Heller's direct NPC records
contain Companion_BasicPerk, so their effective crew ranks must not be invented
from this direct field inventory. Templates, quest grants and actual state are
distinct sources. No blanket claim about their final loaded perks is made.

Robot bridge: installed `OutpostActorScript` OnWorkshopObjectPlaced calls
CheckAssignAsCrew, which calls Workshop.AssignCrew(self) only when
AssignAsCrewOnCreation is true. Direct VMAD in Garden, Sanitation and ModelA01
sets that Boolean true (type 5, status 1, value 1). Removal calls UnassignCrew.
ModelA02 points to ModelA01 as template; this continuation does not decode every
NPC template inheritance mask. The script is Bethesda source, read only from
the pinned ContentResources.zip; no script code is incorporated in tracked files.

Illustrations, not measured game results: two eligible rank-1 Management actors
give .95 × .95 = .9025 of duration. One such actor plus Sanitation gives
.95 × .91 = .8645. The two named player skills plus a selected guide timer entry
give .5 × .95 × .95 = .45125. Native binary32 operations round each step.
These examples assume all predicates pass and effective extractor AV=1; they
do not promise actual wall-clock production or inventory delta.
