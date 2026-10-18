# Human crew versus constructed robots

[CR1](../crew/report.md), [CR2](../crew-skills/report.md),
[CR3](../crew-lifecycle/report.md), [robot report](report.md).

| Dimension | Ordinary recruited human | Ordinary constructed robot |
|---|---|---|
| Acquisition | Recruitment quest/role and availability roster | Direct NPC COBJ construction; no hiring prerequisite in the placement assignment path |
| Destination admission | Menu checks charged candidate+occupied slots against beacon slots and player command clamp | Robot build-category admission, then placement-script AssignCrew with native bypass |
| Charged human slots | Usually cost 1; explicit Sarah exception | Placement config mods default cost 1 by −1, ordinarily 0 |
| Assignment state | Owner E2 and actor 4C CrewAssignment | Same native E2/4C; separate construction WorkshopItem edge also retained |
| Reassignment | Ordinary picker/command gates | Placed CrewReassignDisabled=1 blocks ordinary reassignment; reconstruction is separate |
| Skill possession | Direct named/template grants and conditional quest-added ranks | Five process-bonus variants have direct rank 1; three combat variants have no demonstrated A1/DB grant |
| Timing effects | Management/Engineering per eligible actor, player afterward | Garden/Sanitation/Engineering/Management use the same actual A1 dispatcher with their own conditions |
| Generator power | No ordinary recruited human holder of outpost Fusion established | Model A03's separate `20d24f` reaches DB additive per-generator consumer |
| Remote participation | Logical assignment; actual handle/life/Health/bucket gates | Same conditional query; construction/base does not waive those gates |
| Removal | Unassign/dismiss, separate generic unload cleanup | Workshop removal event invokes UnassignCrew; construction registry cleanup is an additional path |
| Save | E2, 4C, selected template/additional ranks | Same shared channels plus constructed actor/base/Workshop owner; no need for an extra serialized copy of a definition rank |
| Restoration | Handles, assignment context, selected ranks and runtime buckets rebuild | Same ordinary actor finalization; restored identity is not observed operating state |

The shared paths are `1404076b0/140407a10` membership, `140f7bd20` timing,
`140c93cf0` active entry dispatch, `1404089e0` E2 restoration and
`1419198a0 → 141955400` rank replay. The concrete divergences are construction
admission and ownership, script slot/reassignment settings, rank acquisition,
resource selectors and Model A03's DB power perk. The normal strongest-only ship
capacity/type 1 ability mechanisms cannot replace these robot A1/DB rules.
