# Assignment, eligibility and restoration

[Report](report.md), [effects](effects.md), [saved evidence](persistence.md),
[CR1 capacity](../crew/capacity.md), [CR3 actual native lifecycle](../crew-lifecycle/native.md).
Native addresses are preferred static VAs, image base `140000000`, pinned build
1.16.244.0. No function was invoked against the game.

OutpostActorScript's installed compiled OnWorkshopObjectPlaced gets GetWorkshop,
sets Essential and NoBleedoutRecovery from configured/default booleans, sets
CrewReassignDisabled to 1 if its property exists, mods CrewSlotCost by the configured
integer (default −1), then calls CheckAssignAsCrew. The helper checks its
AssignAsCrewOnCreation boolean and a nonnull owner before AssignCrew. Removed
passes the event's owner to the same helper with false, calling UnassignCrew.
Source text is supporting context; the shipped PEX operations/defaults are read
separately in `.local-work/r1-robots/scripts-final.json`.

Garden, Sanitation, Security and Model A01 have explicit VMAD bindings for the
two AVs and AssignAsCrewOnCreation=true. Model A02/A03/A04 and Model S01 inherit that
Model A01 binding through script part 9, independently of perk part 3. The native
NPC script-binding callback `141fb5de0 → 141f76dd0` resolves the NPC handle, tests
NPC+fe bit 9 (`141f76e43..141f76e50`), selects NPC+120 array slot 9 (+48), falls
back to NPC+130, and repeats while the selected source is an NPC with that bit.
The actual selected source stays in R8 for HandlePolicy+38 at `141f76ea4`;
the decompiler omits that third argument, so use instructions. It snapshots
the source's script list with `1427fcc10` and installs it under the original
NPC handle with `1427fd870` (`141f76ec9/141f76ed9`, n059/n060). The same setter
receives the parsed VMAD list at `1427ff366` in `1427ff160`, reached by installed
VMAD loading `1405e0230` (n042/n062). This closes script inheritance separately
from the perk copier, which does not itself copy part 9. Catalogue script_source
is therefore a selected binding source, not merely a plausible ancestor.
Real reciprocal saved assignments
corroborate Model A03/A04/S01 registration. A script property name alone does not
prove historical script execution or a current effective AV.

The native script bridge `142068d70` creates/fetches the owner's E2 and calls
`1404076b0` with its bypass argument. It does not run ordinary Crew screen
capacity admission. Normal insertion deduplicates the actor, removes a previous
owner, appends a handle, sets CrewAssignment `26beac` and emits notifications.
The WorkshopItem owner `054ba6` is a separate relationship, set in placement
`140f3cf40/1421dd600`. Construction identity and current crew assignment must not
be collapsed even when their destinations agree.

CrewSlotCost's installed default is 1. The placed script's −1 modification makes
the ordinary effective cost 0 in the absence of other changes; native occupied
slots sums truncated nonnegative costs. That explains why these auto-assigned
robots need not consume human Crew Stations or Ship Command allowance. It is not
an unlimited construction grant: construction uses its own category limit.
Ordinary menu reassignment reads CrewReassignDisabled; the placed value 1 blocks
it. Bypassing that UI with an internal function is not a supported user action or
an authorized integration point. Moving/rebuilding a constructed object, removing
an assignment and creating a replacement are different lifecycle operations.

| State/change | Effect query consequence | Count/ownership distinction |
|---|---|---|
| Assigned, still travelling | No arrival/distance/3D test in A1/DB | Owner/E2 can precede physical arrival |
| Unloaded 3D, resolvable actor and retained active entries | Same conditional A1/DB query | Missing graphics is not missing assignment |
| Missing actor or active process/bucket storage | No passing modifier now | Saved identity/owned perk can remain; CR3 setup/finalization replay may restore entries |
| Disabled flag alone | No direct disabled-bit test in A1/DB | Indirect process/resolution effects remain possible; do not infer automatic destruction or counter decrement |
| Health<=0 or excluded life state | Skipped before perk query | Actor/base/construction may remain; contribution loss is not construction removal |
| Dead/destructed | Excluded states `20000/40000/A0000/E0000` for the virtual query at +868 with false; further cleanup depends on the actual removal path | Do not treat merely reaching a dead state as proof of deconstruction/counter release |
| Unconscious `60000`, positive Health | Not excluded by that predicate alone | Other eligibility/storage gates still apply |
| Deconstruction/Workshop removal event | UnassignCrew removes E2/4C through native unassignment; later queries omit actor | The removal event/script is separate from construction registry cleanup; temporary disagreement is possible |
| Rebuild | New constructed actor gets its own placement/assignment sequence | Same base/perk does not preserve the old saved actor identity |
| Save/reload | Saved identities remap; base/additional selected ranks replay into runtime buckets | No serialized active-entry pointer or universal guarantee of remote bucket retention |

**A1 and DB differ on failed actor resolution.** A1 keeps the original E2 slot
while using a local lookup. The DB power loop `140f3dd50` writes invalid handle
`DAT_1461fae94` into the actual E2 slot on failure (instructions
`140f3deb0..140f3deba`, n001). A later power query cannot retry the lost saved
identity from that sentinel alone; restoration or reinsertion is required.
Missing entry storage after successful resolution is a separate noncontributing
case. Thus Model A03 power recovery cannot inherit A1's retained-slot retry rule.

Essential=true and NoBleedoutRecovery=true are placement settings, not a proof
that an arbitrary robot can never reach nonpositive Health or a removal path.
Do not reclassify a damaged but still registered construction as a freed slot.
The count-specific admission/removal mechanism is documented in [limits](limits.md).

CR3 establishes the shared restoration chain: E2 loader `1404089e0` rebuilds
handles through `140306e40`; actor 4C restores the assignment context; constructed
Actor framing restores base/selected template state; `1419198a0` clears active
buckets and calls BB0=`141955400` to replay effective base and added selected
ranks through normal registration. Process+8 must exist for bucket insertion.
Thus saved assignment plus a definition rank supplies a conditional participant,
not an observed loaded contribution. Failed E2 load can store an invalid sentinel;
normal query does not reconstruct an identity lost from that slot.

Frame/wait/travel elapsed production still follows the registered/resolvable
Workshop and producer paths established by S2/E1. Robot physical position is not
an operand of the modifier loops. Which historical remote robot retained process
storage and whether products actually entered inventory remain NOT TESTED.
