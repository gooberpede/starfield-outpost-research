# Capacity, construction and enforcement

Use the [build/address domain](report.md#evidence-and-version-boundary).
Evidence: exports 001, 003, 005, 008, 012, 014, 016 and 020; installed definition
receipts and PEX06 in `.local-work/cr1-crew/`. Authored REVIEW-REQUIRED.

## Charged slots and the player clamp

`1404073c0(owner)` returns integer destination capacity. For the recognized
outpost-beacon branch it reads SpaceshipCrewSlots; the ordinary ship branch takes
the minimum of crew rating and crew slots. `1404074a0` then takes the minimum
of that result and the player's effective SpaceshipCrewCommandSlots. This second
function has no outpost exemption. Installed DFOB bindings, rather than the names
alone, join the native defaults to AVIFs:

| Native resolved default | Main-ESM AVIF | Meaning here |
|---|---|---|
| `145ea1ef8` | `00019080` | SpaceshipCrewRating |
| `145ea1f50` | `002cc9ea` | SpaceshipCrewSlots |
| `145ea2000` | `00160030` | SpaceshipCrewCommandSlots on player |
| `145ea2058` | `00172f8f` | CrewSlotCost, default 1 |
| `145ea20b0` | `00172f8e` | CrewReassignDisabled |
| `145e818a0` | KYWD `0026beac` | CrewAssignment keyed relationship |

`1404088c0` sums `truncate(max(0, actor CrewSlotCost))` for resolvable handles;
if the default is unavailable it falls back to raw list length. It does not count
unassigned recruits, another destination's members, physical seats or arrived actors.

The menu worker `141625260` independently requires `occupied + candidateCost <=
1404074a0(destination)` before removing the old assignment. Ordinary insertion
then calls `1404074f0` with the player clamp enabled. The picker uses that predicate
with the raw destination-capacity option, so a visible/enabled destination can
still fail the final command check and show the specific command-level message.

For normal nonnegative values, ordinary outpost admission is consequently:

`sum(charged costs at this beacon) + charged candidate cost <= min(integer effective beacon slots, integer effective player command slots)`.

This is a per-destination command ceiling, not subtraction of all assigned actors
from one global allowance. The insertion predicate uses unsigned subtraction of
occupied from capacity, whereas the menu worker uses the positive sum comparison.
Do not generalize the former as safe handling of an already overcapacity list.
The script AssignCrew callback `142068d70` passes the insertion bypass argument;
its void return does not certify ordinary menu eligibility.

Player NPC `00000007` explicitly defines command slots 3. Ship Command
`002c53b3` selects abilities `00009b24/25/28/29`; their MGEF `00009b20` targets
`00160030`, with magnitudes 1/2/3/5. These are selected-rank additions, not
cumulative 1+2+3+5. Prior normal rank-transition evidence controls that distinction.

| Ship Command rank | Definition-derived ordinary command allowance |
|---|---:|
| None | 3 |
| 1 | 4 |
| 2 | 5 |
| 3 | 6 |
| 4 | 8 |

These are defaults with ordinary selected ability applied, not measurements of
the historical player's effective AV. No literal universal hard-coded maximum
of eight occurs in the mapped capacity function. Modified AVs and zero-cost actors
can change actor-count results. Sarah's attached Crew_LeadershipScript modifies
CrewSlotCost by -1 on initialization; the script property defaults to -1, and its
installed actor binding is retained in npc-category01.json. This is a concrete
capacity exception, not authority to infer all Leadership bonuses.

## Crew Station assembly and construction gate

COBJ `002ab8f7` builds PKIN `00299f59` (OutpostPI_CrewStation01), using
JNAM global `001b4bb2` (initial float 3). The PackIn has SpaceshipCrewSlots and
SpaceshipCrewRating PRPS values 1, and event/dummy-related properties. VMAD
attaches OutpostCrewStationScript. It has no power-demand property in the
inspected record. Native placement `1421dd600` adds the constructed reference's
effective slots to the owner through `140f3dc80`; deletion `1421de660` subtracts
them. The helper recognizes the outpost-beacon branch and adjusts its AV.

**A PackIn value is not an assembly total.** Fresh Save52 station examples have
two stamped contributing references (for example ff01fa65 and root ff01fa66),
each with saved base slots/rating 1 and the same construction identity. The exact
beacon owner ff01a75b has saved base slots 2. Seventeen positive native-root joins
and all 19 sampled beacon slot values are retained. This supports two capacity
slots for the sampled ordinary station assemblies; it does not make every desk
member a separate constructed station or prove a controlled one-station delta.

PlayerSkills quest stage 703, called by Outpost Management rank 3, mods the station
construction-limit global by `OutpostManagementBonus`. Bundled source defaults
that property to 1, but the installed quest VMAD configures **3**; actual PEX calls
the property. Using the source default alone would give the wrong limit. Ranks
1/2 affect cargo-link/robot limits; rank 4 is the separately mapped production
interval entry. No additional Crew Station increase occurs at those ranks.

| Outpost Management rank | Ordinary station build limit | Conditional physical slots if every station contributes the sampled 2 | Ordinary charged-slot admission |
|---|---:|---:|---|
| None, 1 or 2 | 3 | 6 | min(actual effective slots, command allowance) |
| 3 or 4 | 6 | 12 | Same native clamp; default command 3, selected Ship Command maximum 8 |

The 6/12 column is explicitly an assembly-based extrapolation; the capacity
function's effective AV input is stronger evidence than multiplying definitions.
Construction counters, extraordinary scripts, mods and current AV modifiers can
change those inputs. Neither a global station build limit nor a crew name is an
alternative to reading the actual destination state.

## Removal, inaccessibility and overcapacity

Installed OutpostCrewStationScript.OnWorkshopObjectRemoved passes the owner to
`SQ_Crew.CheckCrewCountAtOutpost`. Under its own guard the handler reads integer
beacon slots, collects active crew whose LinkOutpostCrewMarker01 equals that
beacon, and unassigns members from the end until array length fits. It compares
**actor count to raw beacon slots**, not summed CrewSlotCost or the player clamp.
This is concrete asynchronous script cleanup, not rejection of deconstruction.
Native subtraction precedes the later script reaction; a transient excess is
possible. Array order is not an asserted player-visible priority.

No equivalent automatic displacement on a decrease of the player's command AV
was established. Existing assignments can therefore not be declared revalidated
merely because the next menu admission checks a lower allowance. Exact generic
AV-change/event handling for that exceptional transition remains OPEN.

The assignment/capacity paths do not inspect a station's current power, damage,
seating, navigation reachability or 3D residency. Outpost destinations resolve
through the registered beacon list and `140f386a0` base/keyword qualification.
No distance predicate is applied to outpost admission in `1404074f0`; the screen's
distance check only supplies its current-location flag. A temporarily unresolved
beacon/handle is different from capacity zero.

For arbitrary disabled/damaged stations, the precise remaining question is whether
the generic disable/destruction path adjusts the beacon slot AV or delivers the
Workshop removal event. Direct slots-default xrefs and the add/remove handlers
establish construction/deconstruction; they do not qualify every generic disable
or damage route. No automatic eviction or guaranteed retained capacity is claimed
for those routes. This is the bounded unresolved predicate, not a demand for a
new live experiment or permission to modify station state.
