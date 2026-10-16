# Research Projects: unlocks versus production modifiers

**For the inspected ordinary main-game path, completed Outpost Research Projects
unlock recipe availability. They do not supply an additional production timer
factor.** This is separate from player skills required to undertake research and
from the performance or abilities of objects/robots subsequently constructed.

Installed Starfield.esm SHA-256
`1dabed00c3f4282dd3bb54d2e9601e40b577d8742d078b7ccef203adbfef0da7`.
The original [bounded reader](../../../research/e1-extractors/stacking-definitions.py)
walked all RSPJ and COBJ records using the owned strict ESM reader: 82 projects,
3,009 recipes. Twenty projects have Outpost_Research EDIDs, all category keyword
2956bf. All 82 project NNAM fields are zero. The fields present are EDID, FULL,
DESC, BNAM, FVPA, RQPK, CNAM, NNAM, SNAM, TNAM, KNAM and optional RNAM.
RQPK contains prerequisite perk/rank pairs; it is not a grant list. No PRKE/EPFD
production-modifier entries are present in these project records.

For example, RQPK in Resource Extraction 1/2 requires Skill_OutpostEngineering
`2c59e0` at rank 1/2. Power Generation 4 additionally requires
Skill_SpecialProjects `04ce2d` at rank 1. These requirements do not grant those
skills on completion. Special Projects' separately mapped production timer
entry is at rank 4; satisfying this rank-1 research prerequisite does not activate
that rank-4 bonus.

| Outpost project family | FormIDs / number of recipes gated by each project |
|---|---|
| Decoration 1–3 | 100b8b / 63; 100b8a / 65; 100b8c / 44 |
| Horticulture 1–2 | 389f09 / 1; 389f0a / 1 |
| Resource Extraction 1–2 | 389f0b / 51; 389f0c / 51 |
| Outpost Defense 1–2 | 389f0d / 3; 389f0e / 4 |
| Robots 1–2 | 389f0f / 3; 389f10 / 2 |
| Manufacturing 1–3 | 389f11 / 3; 389f12 / 5; 389f13 / 5 |
| Power Generation 1–4 | 389f14 / 1; 389f15 / 1; 389f16 / 1; 389f17 / 1 |
| Domestication 1–2 | 3e3d4d / 1; 3e3d4e / 1 |

These are 307 unique COBJ records whose CTDA function low ushort is 036a and
first FormID parameter names one of these 20 projects; counts are definition
gates, not 307 objects currently constructible in a save. Other conditions,
materials and prerequisites can still restrict construction. Native registration
metadata at `1400e1fb5` associates name `144bca368` (IsResearchComplete) and
ID 136a; wire/native flag encoding and the complete condition-table dispatcher
are not reimplemented here. Game.IsResearchComplete's independently bound
callback provides the matching completion-state query described below.

Concrete example: COBJ 203dbd (`co_Outpost_Harvester_Solid_Aluminum_02`), ESM
offset 1300497276, builds CONT 20a06b and tests RSPJ 389f0b. COBJ 203dbc,
offset 1300496891, builds CONT 20a053 and tests RSPJ 389f0c. The baseline iron
construction recipe 008404 at offset 1300087907 has no such research CTDA.
RSPJ CNAM names representative output objects (CONT, ACTI, PKIN or FURN in this
20-project subset), not PERKs. It does not mean completion creates that object.

Native completion chain, all static VAs/base `140000000`, same pinned retail
executable as [the native contract](stacking-native.md):

- Export 04 registers ResearchProject.Complete to label `141f06f80`. Export 06's
  complete instruction window resolves the project's FormID in manager
  `1461e26a0` and tail-jumps to `141801ee0`.
- Export 08's `141801ee0` recursively completes prerequisite nodes and supplies
  remaining material quantities to `141800f20`, also exported in 09. It is a
  mutating in-game operation, never invoked here.
- `141800f20` records progress 1.0 and status byte 2 on completion. Its potential
  product-insertion branch requires nonnull recipe+88 and nonzero unsigned
  recipe+90 count. The inspected RSPJ NNAM=0 bypasses it. Completion can still
  award XP and emit BGSOnPlayerCompleteResearchEvent; “only unlocks” must not be
  read as “has no other game side effects.”
- Game.IsResearchComplete binding at `1420128d6` (11) points to `14200e610` (12):
  lookup by project FormID and true exactly for existing state byte 2. The
  same-state condition query `140c07e70` (11) returns a float Boolean.

The ordinary producer timer instead reads resource definitions, E2 actors and
active A1 entries. All 502 main-ESM PERK records from the prior pinned census
were inspected for CTDA function 036a: zero. Thus there is no Research Project
completion condition in that inspected perk set. This negative is narrower
than exclusion of every engine or mod mechanism.

The installed ContentResources.zip census (5,033 PSC members, same pinned hash
as prior production work) found seven files containing OnPlayerCompleteResearch.
Four are base event declarations; concrete handlers in DebugPlayerSummonShip,
Drug02_CraftAmp and MQTutorialPlayerResearch log or advance quests. No Outpost
modifier grant occurs in those inspected handlers. Source text is not proof that
all possible native event sinks, compiled-only scripts or overrides are absent.

Accordingly, completing Resource Extraction research is not itself another .95
or .5 factor applied to an existing extractor. It permits recipes for different
equipment. Robotics research can similarly permit a robot whose own selected
perk later participates after construction/assignment. This is an indirect
consequence of using the unlocked object, not evidence of a permanent research
timer bonus. DLC/mod overrides, native event-sink closure and realized output
remain explicitly outside this scoped negative.
