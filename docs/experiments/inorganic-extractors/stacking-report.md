# E1 stacking and Research Projects: offline result

2026-10-16. SOR-EXP-0038 / SOR-EV-0046 continuation, under the
[chat-authorized durable brief](../../implementation-briefs/CODEX_BRIEF_SOR_E1_stacking_research_projects.md).

**The ordinary timer path supports multiplying contributions from distinct
assigned actors, followed by the player's applicable bonuses. Different ranks
of one perk replace one another on the traced rank-change path. Outpost Research
Projects supply construction prerequisites, not a separate production multiplier
in the inspected main-game definitions and completion path.** No game was run.

| Question | Strongest supported scoped answer |
|---|---|
| Two crew with the same timer perk | Distinct assigned actor handles are retained; each eligible actor is dispatched. Assignment does not deduplicate by perk. The separate highest-rank routine is not the timer's dispatcher. |
| Crew plus robots / multiple robots | The shared CrewExtraData list and A1 consumer support composition. Explicit robot script configuration joins the same assignment API. Template-dependent robot script inheritance and actual loaded membership remain qualified. |
| Several ranks of one perk | Normal change removes entries matching old rank and installs entries matching new rank, using entry rank +1. It does not install all earlier ranks. |
| Different player perks | Separate selected entries compose. Outpost Management rank 4 (.5) and Special Projects rank 4 (.95) give .475 of base duration before other factors. |
| Guide magazine timer entries | Its zero-based ranks 3 and 4 each contain .95. On the traced rank transition they replace each other; they do not yield .95 squared together. Acquisition/pickup history is not measured. |
| Completed Research Projects | All 82 inspected RSPJ records have NNAM=0; 20 Outpost projects gate 307 recipes. Completion records status 2; conditional recipe availability queries that state. No direct production perk grant was found in the traced completion branch or the inspected definitions. New equipment/robots can affect production when subsequently constructed and used. |

The [native contract](stacking-native.md), [practical matrix](stacking-matrix.md)
and [Research Project analysis](stacking-research.md) give exact provenance,
conditions and limits. [Review and verification](stacking-review.md) controls
acceptance. This is a **scoped static stacking result**, not completion of the
general realized-rate model. Earlier E1-P3–P9 dependencies on effective extractor
AVs, insertion outcomes, elapsed policy and current state remain open.

E1-P1 is narrowed from an unidentified list to a handle-unique assignment list
with explicit creation, insertion, migration and consumer edges. E1-P2 is narrowed
to selected current-rank registration/removal for normal rank changes. Full
startup/load restoration closure, arbitrary scripts/mods and every exceptional
actor state are not claimed. No actual actor, perk possession, output count or
working control save was observed live. Definitions are not proof that a named
companion currently possesses the displayed rank.

The earlier [REVISE proposal](production-feasibility.md) remains preserved history.
For its specific ordinary-path alternative—highest crew only versus consuming
each eligible assigned actor—the new static evidence answers the mechanism.
A live probe merely repeating that question is now **NO-GO for duplication**.
Runtime testing could still establish actual participants or output for a
particular loaded outpost, but that is a separate question and needs a separate
brief. No new observer, live card or instrumentation is proposed here.

Scientific support is STATIC / strong within the named paths and main ESM.
Publication remains REVIEW-REQUIRED for authored interpretation and LOCAL-ONLY
for bulk native/definition/script evidence. Prior uncommitted work and evidence
are retained. D1, organic E2, saves and installation configuration are unchanged.
