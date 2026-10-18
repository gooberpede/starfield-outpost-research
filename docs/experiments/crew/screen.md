# How the Crew screen is populated

**2026-10-18 corrective continuation:** [Current saved assignments](current-assignments.md)
now demonstrates reciprocal actor4C/outpostE2 relationships in HIST-0021/22/24/0255 and three positive saved available-roster actors.
[Rework review and exact package](current-review.md) controls this continuation.
The initial CR1 observations and review below are retained as the earlier snapshot;
its missing-positive-assignment boundary is superseded for the new positive subset.
Real saved unassigned-roster inputs are now qualified; universal post-load authority remains OPEN.

This implements the user's [accepted addition](plan.md). STATIC / STRONG within
the installed native and SWF paths; actual rendered gameplay was not observed.
Addresses use the [pinned domain](report.md#evidence-and-version-boundary).

## Native population

`14153e800` constructs ShipCrewData and publishes a TUIDataToFlash provider named
`ShipCrewData`. Its payload includes CrewInfoA, AssignmentCategoryA,
CurrentSystemBodyInfo, sPlayerLocationName and bIsPlayerInSpace.
The provider's update virtual points to `14153eb90` (vtable `144c6fef0` +8).

The update builds assignment categories and calls `14153cfe0`:

1. Look up the record keyed by the player's FormID through `14130feb0`.
2. Resolve its available/unassigned actor handles at record +20/+28 and emit
   actor rows with no AssignmentInfo.
3. Walk the player's recorded ship handles (+8/+10) and the registered Workshop
   handles at `145f0ba78/80`. Resolve each destination, apply its callback predicate,
   and classify its category through `14153c080`.
4. `14153d170` creates/updates destination rows, then resolves their E2 crew member
   handles and emits an actor row joined to that destination. Failed actor
   resolution invalidates the local handle slot; it is not an empty living actor.
5. Optionally resolve selected candidate handle at provider +30 and append/update
   that actor without AssignmentInfo. This supports the recruitment/dialog entry
   point even before a lasting assigned row exists.

`14153eda0` identifies a row by actor handle. Newly inserted rows pass through
`14144e220` and sorted insertion `14144f510`; an existing row is updated in place.
No census over all NPC definitions or proximity search supplies CrewInfoA.
Registered destinations and the separate unassigned population explain why
physically absent assigned crew can appear and why an unrecruited skill-bearing
NPC need not appear.

For the assignment picker, `14153f4d0` uses the same population framework with
different callbacks: home-ship predicate `14153f6d0` and outpost predicate
`14153f7d0` call `1404074f0`. Outpost qualification `140f386a0` recognizes the
beacon base or configured keyword. Final assignment still goes through the
separate command-capacity worker.

## Row fields and skills

`14144f190` binds sName, sFallbackLocationName, uType, bReassignDisabled, uHandle,
aSkills, uAssignmentHandle, uAssignmentType, sAssignment, sParentBodyName,
sParentStarName and bCurrent. `14153dc70` obtains actor name/handle, fallback
location, crew-category keywords, reassignment AV and slot cost.

Under the actor's perk lock, it walks both the base-NPC perk vector and additional
actor perks. `14153e290` admits only non-null perks with root flag mask 8, deduplicates
skill rows by perk FormID and calls `14153d900`. That builder reads the perk's
label/image path, skill metadata, current rank via `141955080`, FormID and
environment category. **aSkills therefore reports crew-flagged possessed perks;
it does not run each gameplay consumer or prove an outpost-relevant effect.**
This also explains why a quest-granted named actor's display cannot be reconstructed
from its base-NPC PRKR field alone.

`14153e4f0` fills assignment name, handle, category and parent labels from the
destination row; no destination uses `$UNASSIGNED`, invalid handle and type 3.
Destination `1415431c0` binds occupied, available and total crew slots. The
available field is the player-clamped capacity, not a subtraction of occupancy;
occupied is separately supplied. `14153c0f0` supplies bCurrent for outposts using
a squared-distance comparison against fCrewMenuCurrentOutpostMaxDistance. That
flag does not establish assignment eligibility or actor residency.

## Installed movie and UI actions

Fresh extraction pins `interface/shipcrewmenu.swf` from the installed Interface
BA2. The owned bounded ABC reader closes the file and 86 selected method bodies
without an unknown-opcode stop; primary receipt is menu01.json. This was static
inspection, with no ActionScript execution or UI automation.

| ABC method index | Bound method | Decisive operation |
|---:|---|---|
| 1003 | ShipCrewMenu.onAddedToStage | Subscribe to `ShipCrewData` using OnReceivedPayloadData. |
| 1004 | OnReceivedPayloadData | Retain the received payload and invoke category/list update. |
| 1007 | UpdateCategoryData | InitializeEntries from CrewData.CrewInfoA; set first selection when needed and update button hints. |
| 1006/1008 | ListFilterChanged / CrewFilterFunction | Update current category filter and compare with flag derived from uAssignmentType. |
| 740 | CrewListEntry.SetEntryText | Consume supplied name, assignment/location/category and skill rows; generic/elite presentation differs. |
| 1015/1016 | onUnassign / onAssign | Dispatch ShipCrewMenu_OpenAssignMenu with actor uHandle and action state; button state is separate from native enforcement. |
| 1017 | onSort | Change sorted column/direction and dispatch ShipCrewMenu_SetSort. |

Native sort state goes through `14153ef40`/`14153f020`; new-row comparator selection
is in `14144e3d0`. A service command may queue these updates, and UI data transport
has its own notification boundary. Neither refreshing the screen nor a fixed
five-second delay establishes that travel, effect registration or save restoration
has completed. The string/setting uPopulateCrewDataDelay was located, but no
consuming Crew screen delay path was established; its name is not timing evidence.

Large-text and assignment-menu SWFs were also pinned/extracted locally; their
complete method equivalence was not analyzed. The conclusion concerns the mapped
native provider and normal installed Crew movie, not every layout/override/mod.
