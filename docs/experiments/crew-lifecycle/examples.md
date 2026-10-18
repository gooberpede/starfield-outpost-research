# Consequences, transitions and robot handoff

[Answer](report.md), [native gates](native.md), [saved inputs](persistence.md). These calculations are PREDICTIONS conditional on actual eligibility, registration and matching producer context; no inventory output was measured.

| Actor/state | Consumer and modifier | Observable consequence and boundary |
|---|---|---|
| HIST-0255 Lin assigned to ff047885; registered Management3 and eligible | A1 duration ×.87 on qualifying inorganic/organic/manufactured base | Next interval reset can adopt .87; current old countdown is not rescaled. |
| HIST-0255 Heller at the same destination; registered Engineering3 | A1 ×.77 for manufactured base only | Inorganic query has no passing Engineering effect. Geology1 adds no native PRKE entry. |
| Both named actors eligible on manufacturing | ×.87×.77 = .6699 of otherwise identical base duration | Approximately 1.49276 nominal rate factor, subject to binary32 rounding, other modifiers, scheduling and actual inputs/output. |
| Generic Engineering, e.g. HIST-0021 ff04e381 | Selected part3 02e91c supplies Engineering1; A1 ×.91 on manufacturing | Same consumer as Heller with a different rank source/factor. No inorganic timing contribution from this entry. |
| Generic Management, HIST-0255 ff084217 | Selected part3 02fdf7 supplies Management1; A1 ×.95 | Owner ff038542 differs from Lin/Heller's owner. Never multiply its factor into their outpost merely because all occur in one save. |
| Generic Security, HIST-0255 ff084219 at Lin/Heller's owner | Selected part3 26f93b supplies Pistols1, entry23 actor/weapon/target conditions | No A1 timing entry in this selected skill; no transferred turret aura. Qualifying personal combat is a separate consumer. |
| Sarah assigned to saved ship registry target; positive available Barrett/Sam/Andreja | Different/no outpost E2 membership and assignment context | No automatic contribution to Lin/Heller's owner. Saved roster inputs are distinct from observed final loaded UI or current Health. |
| Same retained E2 actor, no 3D but resolvable and active entries retained | Same A1/DB query path | Can contribute on remote interval reset; absence of graphics alone is not the exclusion condition. |
| Same retained handle temporarily fails resolution | No actor dispatch during that call | Factor omits that actor; next successful query can include it if the slot and qualifying entries survive. Old producer interval may conceal either transition until reset. |
| Process entry storage freed, relationship retained | Dispatcher has no relevant bucket | Possessed rank/assignment can persist while contribution disappears. Entry replay with suitable storage restores query opportunity; handle recovery alone is insufficient. |

## Old clocks and new modifiers

Use an otherwise unmodified nominal base interval of 36 scheduler seconds. Suppose remaining=5 and old interval=36 before Lin becomes eligible. Elapsed10 crosses the old countdown and makes one cycle due; after that work the row can reset to `36×.87=31.32`. It does not retrospectively calculate that ten seconds at the new rate. With elapsed50, the native large-elapsed branch uses `trunc(50/36)=1`, independent of old remaining5, then adopts the current reset interval. This is the existing [E1 arithmetic](../inorganic-extractors/arithmetic-clocks.md), not continuous phase-preserving simulation.

If Lin is removed after remaining has been set to31.32, that prior field can persist until the next due branch, then reset without her factor. That is a reachable cache lag in the traced algorithm, not evidence of a lingering actor aura or a gameplay defect. Likewise, losing an actor's entries and restoring them can leave the same old interval for a while. Initial/newly registered rows and external re-registration can have separate resets; this example concerns an existing ordinary row, not a claim that only one writer exists.

Inorganic extraction and fabricators share this clock adoption rule. Fabricators also cap output by recipe inputs and remove them before creation. Neither Management nor Engineering changes the recipe's ingredient cost or makes due work automatically successful. UI nominal-rate caches and power allocation updates have their own refresh paths; no crew-specific fixed delay in seconds is established.

Frame `1417cab70`, wait/sleep `141a38ba0` and travel/skip `141a27d80` reach the shared elapsed scheduler. Wait converts skipped time in calendar/local-day-aware chunks; travel passes its own computed scalar. These calls evaluate the state available then, rather than replaying each historical assignment/Health transition over the skipped period. A single large batch and many small batches can differ. See [E1 clocks](../inorganic-extractors/arithmetic-clocks.md) and [S2 remote lifecycle](../local-output-links/lifecycle.md); no new timing theory or live-count claim is introduced.

## Short robot handoff

CR2's five constructible robot definitions use actor perks and outpost assignment machinery. Garden/Sanitation have OutpostActorScript assignment-on-creation configuration; ModelA01/02/03 supply Engineering/Management/outpost Fusion respectively under their qualified inheritance rules. E2 handle lookup, life-state/Health, active-entry storage and assignment environment are shared gates, not robot exemptions. The DB power consumer adds ModelA03's passing +1/+2/+3 per generator base-power band; it does not use the producer countdown adoption rule. Power recalculation/output scheduling remain distinct.

Named humans use story/quest grants and their retention rules; generic human specialists use saved selected template parts and can be deleted on unassigned unload. Robot construction/script initiation and perk definitions differ. These are verified differences from CR1/CR2, not a comprehensive robot census, robot repair/death study or proof of any saved robot currently contributing. Ordinary ship Fusion on Vasco is still not the robot's outpost Fusion. No full ship-skill, companion AI or robot investigation follows.
