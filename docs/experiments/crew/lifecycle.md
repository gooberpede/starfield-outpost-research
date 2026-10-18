# Assignment authority, travel and restoration

**2026-10-18 corrective continuation:** [Current saved assignments](current-assignments.md)
now demonstrates reciprocal actor4C/outpostE2 relationships in HIST-0021/22/24/0255 and three positive saved available-roster actors.
[Rework review and exact package](current-review.md) controls this continuation.
The initial CR1 observations and review below are retained as the earlier snapshot;
its missing-positive-assignment boundary is superseded for the new positive subset.
Real saved unassigned-roster inputs are now qualified; universal post-load authority remains OPEN.

Addresses use the [CR1 static domain](report.md#evidence-and-version-boundary).
Primary: native exports 001/003/004/005/010/011/014/016/019/020 and installed
PEX06, particularly SQ_CrewScript, OutpostBeaconScript and SQ_PlayerShipScript.
Authored interpretation REVIEW-REQUIRED; no live events were observed.

| Boundary | Positive mechanism | What this establishes |
|---|---|---|
| Recruit | Inherited `Recruited` charges if not already available, sets role available, opens assignment dialog. | Recruitment and destination admission are separate. |
| UI request | `ShipCrewAssignMenu_Assign` carries target and old-owner handles. `141625260` resolves selected actor and destination, sums charged slots and checks the player-clamped allowance. | A visible choice is not success. Missing handles terminate the request; capacity failures have command-specific or generic messages. |
| Ordinary native insertion | `1404076b0` deduplicates the actor handle, checks `1404074f0` unless bypassed, resolves owner and removes the actor from a different owner's E2 list. | One ordinary assignment owner; no perk-based deduplication. Script bypass and save restoration are separate paths. |
| Native authority | Appends the handle; `140ba0d40` writes keyed CrewAssignment through linked-reference machinery; owner change flag `80000000` is marked. | Membership and relationship change in the operation, before arrival. These are not one demonstrated atomic transaction across all consumers. |
| Notifications/effects | Native event dispatch follows relationship update. `140408bb0` runs conditional registration through `14040a230`/`14040a9d0`; location context can postpone the applicable registration path. | Do not promise an immediate effective bonus solely from menu acceptance. E1's scheduler independently consumes the assigned list under its eligibility rules. |
| Script handling | Beacon OnCrewAssigned and ship collection OnCrewAssigned forward to SQ_Crew under script guards. Active role/aliases and outpost marker links update here. | Script state is downstream of native membership, not a required proof of prior physical arrival. |
| Travel | If actor or beacon is 3D-loaded, add actor to CrewGoingToOutposts. If neither is loaded, MoveTo occurs, except the locked-in/non-following companion branch. | Movement is conditional; no fixed number of seconds is supported. |
| Later unload | OutpostBeaconScript.OnUnload processes CrewGoingToOutposts; helper resolves current assignment and moves actor, with the same locked-in exception, then removes the pending alias member. | Physical location can lag, and current assignment is reread before movement. |
| Unassign/transfer | `140407a10` removes matching handles (recursively removing duplicates), restores unassigned availability where applicable, performs conditional effect cleanup, clears the keyed relationship and emits dismissal. | Availability and assignment cleanup are causal operations, not merely changed UI labels. |
| Script dismissal | `HandleOnCrewDismissed` rereads GetCrewAssignment; if there is a replacement assignment it avoids dismissing the transferred actor. Otherwise it clears active role/follower state as applicable and queues/moves home. | A dismissal notification during transfer is not proof of final unassignment. |
| Generic unload/death | Generic + no current assignment triggers availability/persistence-reference cleanup and deletion; OnDeath handlers remove available crew. | Stale historical identities do not prove live roster membership or contribution. |

Normal ship/outpost transfer uses the same E2 insertion/removal primitives, with
ship-specific home-ship and physical/docked-ship checks in picker/enforcement.
The outpost branch of `1404074f0` bypasses that final ship-location restriction.
CrewReassignDisabled blocks an already assigned actor in this predicate; the UI
also exposes the AV as its own row/button condition. Native script assignment
does not enforce all those ordinary checks. The APIs are OBSERVED-INTERNAL or
script-exposed interfaces, not VALIDATED-INTEGRATION points.

## Persistence classes

| State | Class and evidence | Remaining boundary |
|---|---|---|
| Owner's E2 member array | PERSISTED-capable / STATIC. Runtime +18 count, +1c allocation capacity, +20 handle storage, +28 owner FormID. Loader `140521620` case E2 creates owner extra then invokes `1404089e0`. | No actual sampled beacon E2 instance recovered; allocation capacity and runtime pointer are not serialized identities. |
| Loaded actor handles | RECONSTRUCTED / STATIC. Reader gets a compact count then `140306e40` resolves saved form identities, casts to Actor and obtains fresh handles; unresolved entries get invalid sentinel. | This reader does not call ordinary insertion/capacity enforcement. Do not infer uniqueness, current bonus registration or travel completion from its return. |
| CrewAssignment keyed link | PERSISTED-capable / STATIC. Native setter uses ExtraLinkedRef machinery; existing 4C save grammar stores keyword/target/mode. | No `0026beac` queued relationship was recovered in the three selected R3 scans. Other representations/defaults remain unqualified. |
| Unassigned roster and owned-ship registry | MIXED. Player-keyed runtime record has ship handles at +8/+10 and available actor handles at +20/+28; Add/Remove update it. `14130d540` reads saved identity/array containers; `14130d650` reconstructs qualifying handles from retained identities. | Exact enclosing saved block/version, complete available-array writer/reader correspondence and actual roster instances remain unqualified. Do not label an empty beacon as an empty roster. |
| Station identity/construction/owner | PERSISTED / SAVE plus DEFINITION-DERIVED classification. PackIn extra and exact 4C owner joins in [stations.csv](stations.csv). | Exceptional/default/alternate construction representations remain outside the positive subset. |
| Effective capacity | MIXED. Saved BF base values exist; installed defaults, additive construction changes and player modifiers feed current effective queries. | Saved base value is not a current effective measurement or proof of authority after load. |
| NPC base perks / quest-added perks | DEFINITION-DERIVED versus PERSISTED-capable additions. Generic PRKR differs from Lin/Heller's scripted grants; normal selected ranks feed native entry registration. | No historical actor perk/rank or active-bucket decode is qualified here. |
| Active/available role and pending movement aliases | MIXED script/quest/actor state, with actual PEX read/write paths. | VMAD properties define bindings, not saved variable values. Actual saved alias/Papyrus instance decoding remains unknown. |
| Physical presence / loaded state | TRANSIENT current 3D/cell/resolution versus potentially persisted position. | A saved assignment, saved XYZ or absence of actor change record cannot establish current physical presence or effective contribution. |
| CrewInfoA / skill images / sort state | RECONSTRUCTED/TRANSIENT UI data. Native row builders feed the installed movie. | Do not import UI handles as stable saved IDs or serialize row snapshots as gameplay authority. |

The load reader, construction/restoration code and downstream role/travel handlers
establish a useful partial restoration model. Full startup ordering, available-roster
restoration, concurrent coherence and actual post-load contribution are not closed.
No passing file-integrity check is used as proof of those semantics.
