# CR1 crew recruitment, assignment, capacity and Crew screen

**2026-10-18 corrective continuation:** [Current saved assignments](current-assignments.md)
now demonstrates reciprocal actor4C/outpostE2 relationships in HIST-0021/22/24/0255 and three positive saved available-roster actors.
[Rework review and exact package](current-review.md) controls this continuation.
The initial CR1 observations and review below are retained as the earlier snapshot;
its missing-positive-assignment boundary is superseded for the new positive subset.
Real saved unassigned-roster inputs are now qualified; universal post-load authority remains OPEN.

2026-10-18. SOR-EXP-0047 / SOR-EV-0055. Proposed STRONG findings;
authored interpretation REVIEW-REQUIRED, proprietary primary evidence LOCAL-ONLY.
[Authority and amendment](plan.md); [review and frozen criteria](review.md).

| Question | Best-supported answer | Confidence / basis | Consequential coverage or exception |
|---|---|---|---|
| Who can join? | Ordinary named elite recruits, companions and spawned generic specialists use role/recruitment machinery, then a distinct native available/assigned registry. Lin/Heller have explicit quest admission and perk grants; generic Engineering/Management Specialists have separate NPC definitions. | STRONG / STATIC | Category, name and skill possession alone do not admit an actor. Quest/story availability matters; script assignment can bypass ordinary menu checks. |
| Is a Crew Station required? | Ordinary construction supplies the beacon's crew-slot AV; the assignment predicate reads that capacity, rather than searching for a desk, power connection or seated actor. A station's PackIn and its registered members matter. | STRONG / STATIC + SAVE | Definition PRPS is 1; two sampled stamped members each carry 1 and the associated beacon carries 2. Do not treat a single PRPS field as the final capacity of the assembly. |
| Per-outpost maximum? | Charged occupied slots plus the new actor's nonnegative integer cost must fit the minimum of destination capacity and the player's command allowance on the ordinary menu path. Stations have a separate construction limit, initially 3, raised by 3 at Outpost Management rank 3. | STRONG / STATIC | Player command starts at 3; Ship Command ranks give 4/5/6/8. This clamp is also reached for outposts in the inspected build. Actor count can differ from charged slots. See the qualified station/rank table in [capacity](capacity.md). |
| Global recruit/assignment maximum? | No separate fixed hire-count or combined ship-plus-outpost numeric cap occurs in the mapped recruitment and registry insertion paths. Arrays grow; checks are destination-specific. | STRONG scoped negative / STATIC | This is not proof that every engine/quest allocation is unlimited. Generic unassigned crew are disposable after unload. |
| Ship competition? | An actor has one assignment owner. Transfer removes that actor from the old owner before adding the new relationship; other outposts do not subtract from a shared numeric capacity pool. | STRONG / STATIC | Home-ship and physical/docked-ship eligibility add ship-specific checks. A script route can bypass capacity. |
| When does reassignment count? | The native member list and keyed actor relationship change during the native operation. Notifications and Papyrus role/travel handling follow; physical arrival is a separate event-dependent process. | STRONG / STATIC | No measured wall-clock delay or atomic transaction across all consumers is established. Effect registration is conditional, not a blanket immediate-bonus promise. |
| Can unassigned crew be retained? | Recruitment can make crew available before the assignment dialog succeeds. Named/elite availability is distinct from active assignment. | STRONG / STATIC | Generic unassigned crew are removed from available aliases/registry and disabled/deleted on the traced unload cleanup path. Never promise a permanent generic reserve roster. |
| What populates the Crew screen? | Native `ShipCrewData` merges the player's unassigned handles, members of qualifying owned ships and registered outposts, and an optional selected candidate. `CrewInfoA` drives the installed list; category filtering happens in the SWF and sorting is requested from native code. | STRONG / STATIC | It is neither an NPC-definition census nor a scan for physically nearby actors. UI skills are crew-flagged perk rows, not proof of an effective bonus. |
| What can saves recover? | Fresh Save52 bytes positively join 17 station roots to exact Workshop owners; 54 ordinary beacon records across three historical inputs have fully closed counted extra lists with no E2 crew extra. Lin/Heller unique references can be joined to installed base definitions. | PROVEN bytes / SAVE; STRONG scoped associations | No qualified historical assigned crew instance was recovered. Actor grammar, available-roster serialization and pending travel state remain gaps; absence of E2 in these beacon records does not prove no crew anywhere. |

This is a bounded offline explanation of CR1 mechanisms, with explicit unresolved
predicates and a corpus gap. It does not validate current loaded state, universal
crew enumeration, realized bonuses or an integration API. The [coverage register](coverage.md)
separates answered mechanisms from genuinely missing observations.

## Evidence and version boundary

Fresh reads identify installed retail executable 1.16.244.0, SHA-256
`7e9adb1414a8e1b325e5e1f097b9b17b78deb7eebeda37a333351a43a60f9d28`,
and main ESM SHA-256
`1dabed00c3f4282dd3bb54d2e9601e40b577d8742d078b7ccef203adbfef0da7`.
The existing Ghidra program reports the same executable hash, image base
`140000000`, x86 little-endian 64-bit/windows. Every native address in this
package is **hexadecimal static VA**; subtract the image base for RVA. No native
address is a runtime pointer, FormID or save offset.

[Sources](sources.csv) pin baseline inputs, installed BA2/ZIP members, selected
definition rereads, native exports and bounded helpers. Local acquisition is in
`.local-work/cr1-crew/`; exports `native/001.request.tsv` through
`native/020.request.tsv` retain instructions and decompiler limitations.
[Functions](functions.csv) indexes exact exports. Ghidra was run readOnly/noanalysis;
no symbols, types, comments or program bytes were changed. Installed compiled
PEX is authoritative over bundled PSC when they disagree. Twenty-four selected
PEX members fully close after the disclosed local parser corrections.

The baseline contains 23 protected input pins plus HEAD/index and the original
brief. The interface archive was separately pinned before extraction. Historical
Save52/HIST-0036/HIST-0077 are independently identified observational inputs,
not an asserted chronological control sequence. [Save evidence](saves.md) gives
the actual joins, offsets and detection limits.

## Recruitment and candidate categories

`Crew_RecruitQuestScript.Recruited` charges credits only when the actor is not
already in AvailableCrewFaction, calls `SQ_Crew.SetRoleAvailable`, then opens
`ShowCrewAssign(true)`. The role base updates the available alias and AV before
the crew override calls native `Game.AddToAvailableCrew`. These are distinct
facts: payment/availability, a visible assignment option, and successful assignment.
Cancelling or failing the dialog need not undo recruitment. The native available
insertion does not compare its array length against destination slots.

Native `142008540` rejects None and only adds an actor without a current
CrewAssignment link to the player's available list. `14130caa0` deduplicates
the actor handle and grows the array at owner-record +20/+24/+28. On a new
insertion it removes old assignments through `14130cd20`. `14200f5a0` handles
removal, including assignment cleanup where needed. The native Boolean add result
and void assignment callback are not interchangeable success codes; the ordinary
menu request also returns no Boolean gameplay guarantee.

| Role | Positive admission/configuration evidence | Difference that matters |
|---|---|---|
| Lin, NPC `00005638`, unique ACHR `00005639` | Installed Lin quest fragment makes her PotentialCrewFaction rank 1, grants Demolitions once and Outpost Management three times, and makes recruitment free; recruit scene calls inherited `Recruited`. | These are quest-applied perks, not a complete base-NPC PRKR list or proof that a historical Lin received them. |
| Heller, NPC `0000563a`, unique ACHR `0000563c` | Installed Heller quest fragment sets potential rank 1, grants Geology once and Outpost Engineering three times and free recruitment; recruit scene calls `Recruited`. | Geology's display does not establish an outpost production modifier. |
| Generic Outpost Engineering Specialist `0002e91c` | NPC PRKR includes Crew_Outpost_Engineering rank 1; generic template `0026f946`; generic hire fragments call `Recruited`. | Recruitment removes the actor from its spawner's cleanup array. Later unassigned-unload cleanup can still delete it. |
| Generic Outpost Management Specialist `0002fdf7` | Separate NPC PRKR includes Crew_Outpost_Management rank 1 and the same generic template. | An encounter/template definition is not a stable placed actor identity. |
| Companions and other named elites | Shared role machinery and crew-type keywords feed the native/UI paths. Sarah has an explicitly attached Crew_LeadershipScript slot-cost adjustment. | Following, recruitment, availability and assignment have different aliases/state. Picking up an elite follower dismisses the active companion/previous elite follower; this does not establish a universal ban on assigned followers. |

The fresh [candidate ledger](candidates.csv) retains 56 direct category/template
leads, including test/unused definitions. It is deliberately not labelled a list
of 56 recruitable actors. Ordinary dialogue/quest admission and actual role state
must qualify a specific actor. A script can call AssignCrew on an actor without
proving ordinary recruitability.

`SQ_Crew.TestAndHandleUnloadedUnassignedGenericCrew` checks generic keyword and
no current assignment, then clears availability, removes the native roster entry,
clears persistence-holding references/spawner state, and calls DisableNoWait/Delete.
Named/elite and generic crew therefore cannot share a promised retention rule.
OnDeath handlers remove available crew. A dead/unresolved actor is not treated as
a known usable contributor merely because a historical handle remains.

## Reading order and downstream boundary

- [Capacity and enforcement](capacity.md): formulas, ranks, station lifecycle and exceptions.
- [Lifecycle and persistence](lifecycle.md), [saved instances](saves.md): authority versus travel/restoration.
- [Crew screen](screen.md): native sources, skill rows, installed binding/filter/sort paths.
- [CR2/CR3 handoff](handoff.md): actual modifier interfaces and the requested skill examples.
- [Coverage/negative findings](coverage.md), [review/check package](review.md).

Prior [E1 actor-list/rank work](../inorganic-extractors/stacking-report.md) remains
the shared reference. CR1 does not rerun production arithmetic or promote prior
findings. No game launch, live capture, save change, mod, importer, staging,
commit, push, upstream contact or publication was performed or authorized.
