# Robot construction and crew limits

[Report](report.md), [function register](functions.csv), [catalogue](catalogue.csv).
`nNNN` means `.local-work/r1-robots/native/NNN.request.tsv`. Native addresses are
hexadecimal preferred static VAs for the pinned EXE, base `140000000`; field
offsets are hexadecimal. No internal operation was invoked.

**The ordinary robot allowance is three constructions per selected outpost,
increased to six by the ordinary player Outpost Management rank 2 quest increment.**
The same global is a shared threshold, not one quota per variant and not a
global running-actor cap. Definition/perk changes or malformed reconstruction
can change the effective inputs; six is not a literal universal hard-coded cap.

All eight robot COBJ recipes directly construct an NPC. Their JNAM points to
global `001d9f5e`, whose installed FLTV is 3; FNAM is category `001d9f5f`.
Native COBJ loader `140a02160` maps JNAM into recipe+178 (instruction
`140a0244b ADD RCX,178`), independently grounding the field used below. Player
Management rank 2 invokes PlayerSkills stage 702; installed compiled fragment
`Fragment_Stage_0702_Item_00` calls the robot global's Mod using
OutpostManagementBonus. Installed quest `002c59e4` configures that integer as 3,
overriding its source/PEX default 1. Ranks 3/4 do not add another robot increment
through their selected fragments. Construction/research materials are excluded.

## Count, display and actual admission

`140f3b170` (n021/n023) traverses the live Workshop item set at
`145f5d960` (storage+10=`145f5d970`, extent+18=`145f5d978`). Each live entry
supplies a representative handle via the virtual method at +40. A resolvable reference obtains
its construction from ExtraDA when applicable, otherwise its base through
`140b4cd10`; `140f3b080` maps that identity to a COBJ. The helper increments once
when that recipe's **+178 global pointer equals the requested recipe's +178**.
It does not sum E2 actors, check rank/Health, or compare the robot's name.
Unresolvable representatives cannot be counted by that evaluation. PackIn and
single-item cases are distinguished by the native representative/construction
lookup, not counted as every visual child.

`14157b0c0` (n025) uses the same helper and formats `%d/%d` for the object card.
`1421dcb10` (n021) sets engine-frame+61f when count is at least
`max(0, floor(current global+48))`; exact instructions are
`1421dcbce..1421dcbfc`. `140f3f9a0` (n026) consumes that flag and sets candidate
status `1f` for the count limit (alongside other unrelated admission reasons).
Ordinary build event handlers `1421b2360` and `1421b2e20` (n035/n036) require
frame+193==2 before `1421b10b0` can reach construction. The preview status and
actual build path therefore agree: a recipe condition alone is not this proof.

At/above the threshold the ordinary next construction is blocked. The check is
prospective admission, not a loop that destroys an already over-limit list. No
automatic eviction on a lowered global occurs in these handlers. Invalid/modded
globals, stale registry entries and concurrent UI transitions are outside a
settled normal-admission guarantee. Native internal script construction remains
a separate path and is not an approved bypass/integration interface.

## Why the set is per outpost and how it changes

On selection, `1421b64c0` (n027) stores the destination at frame+608 and calls
`1421c6f90(145f5d960, destination, 1, ...)`. That builder (n028) compares the
destination handle with set+98; when changed it clears old state and reads the
selected owner's **Extra4D reverse relationships**, filtering the WorkshopItem
keyword `DAT_145f0b3d8`. Callback `1421c71b0` resolves/deduplicates references,
qualifies their single/compound representation and inserts wrappers with
`1421c6890`. Thus the apparent global item set is an active-context cache, not
all outposts in the universe. Exit/reset paths `1421ba8a0/1421b6be0` clear it.

Construction `1421b10b0 → 1421de3f0` invokes the selected wrapper's virtual method at +A0;
SingleWorkshopItem vtable `144c25298` binds A0 to `140f60f60` (n033/n034).
That path calls placement `1421dd600`, while the successful caller inserts its
wrapper through `1421c6890`. Other ordinary reconstruction paths, including
`140f66ea0`, likewise insert constructed wrappers and run placement.
Insertion uses set semantics rather than blindly incrementing a scalar.

Removal `1421de660 → 140f34650 → 140f404f0` removes relevant wrappers through
`1421c6b90`; its `1421c77b0` erases the item-set entry and invalidates its slot,
then associated reference mappings are removed. The subsequent count sees the
remaining resolvable items. Edit/move paths `1421b1450` remove/rebuild associated
maps through `1421c6e30/1421c6d00`, keeping them distinct from constructing a
second robot. Rebuilding after removal creates a fresh construction/actor;
reusing a recipe does not recover the old instance identity.

No separate serialized scalar “current robot count” is required by this traced
ordinary path: it derives the count from reconstructed construction items and
the shared saved/default global threshold. This does not claim that every
counter-like field elsewhere has been decoded. Actor death, Health<=0,
disablement and loss of a perk entry do not directly decrement this count helper.
Only an actual qualifying reference/registry transition changes its operands.
Consequently a robot can stop contributing while its construction still occupies
the allowance. Exact generic death/disable event delivery into removal is not
universally established; do not promise automatic slot release on damage.

## Assignment and operating bounds

The placement script's AssignCrew bridge bypasses ordinary human capacity
admission; CrewSlotCost is ordinarily changed from default 1 to 0 and
CrewReassignDisabled is set to 1. [Lifecycle](lifecycle.md) separates configuration,
actual historical AV state and ordinary menu behavior. Human Crew Stations,
player Ship Command and charged occupied slots do not impose an additional
ordinary robot headcount through this placement path.

There is no additional robot-number comparator in the actual A1 or DB operating
loops: every eligible E2 actor can participate. No separate universe-wide robot
cap is established in these ordinary construction/assignment/consumer paths.
This is a scoped consumer-backed negative, not a proof about every script/mod or
the deferred general Limits phase. The shared threshold is applied independently
when reconstructing each selected destination. Failed actor lookup, process
storage, current life/Health or perk conditions can reduce effective contributors
without changing either configured allowance or saved assignment.
