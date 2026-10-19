# Native territory and placement decisions

[Answer](report.md), [persistence](persistence.md), [function register](functions.csv).
`nNNN` denotes `.local-work/l3-placement/native/NNN.request.tsv`; line ranges and
whole-export hashes are in the register. All VAs are hexadecimal preferred
static image addresses, with image base `0x140000000`, never runtime pointers or
save offsets. Memory offsets, vtable offsets, status codes and form-type values
below are hexadecimal when prefixed with `0x`; mode values are ordinary integers.
EXE SHA256 `7e9adb1414a8e1b325e5e1f097b9b17b78deb7eebeda37a333351a43a60f9d28`;
main ESM `1dabed00c3f4282dd3bb54d2e9601e40b577d8742d078b7ccef203adbfef0da7`.
Both were freshly pinned against existing analysis for retail 1.16.244.0.
Decompiler pointer/float/IMAGE_DOS_HEADER labels are not accepted native types.
XMM instructions, integer discriminants, exact registrations and physical
definition fields qualify the authored aliases below.

## Territory and POI context

The installed ACTI `002c60e9` (OutpostBeaconActivator) has a PRPS entry for
AV `00063fc5` (OutpostBuildAreaRadius), with little-endian float bytes
`00 00 16 43`, representing 150. DFOB `00063fc6`
WorkshopBuildRadiusAV selects that AV. `140157cc0` binds its native slot;
`140f38e30` reads the selected beacon/base property, including PackIn member
fallback, and otherwise returns fItemPlacementRadius:Workshop. That fallback's
compiled value of 71.4 is a different operand from the ordinary beacon's 150.
`140157700` registers the fallback at static VA `145f0b318`, with its value at
offset `0x08` (export n019). Actual selected effective data/overrides can differ;
150 is not claimed as a universal constant.

`140f4a140` constructs an ordinary boundary descriptor in caller-owned memory.
Its integer mode field is at offset `0x34`: 0 selects a region, 1 selects the
special keyword/linked route, 2 selects a radius, and 3 selects a permissive
special case. The other descriptor fields have separate roles:

| Descriptor offset | Role |
|---|---|
| `0x18` | Region pointer |
| `0x10` | Owner/frame context |
| `0x00`, `0x04`, `0x08` | Centre X, Y and Z |
| `0x28` | Radius |
| `0x2c` | Upper-height limit |
| `0x30` | Secondary height value |

These are memory offsets, not saved-file offsets. The function obtains the
compensated centre through `140f4ab80`, which adds the three ExtraWorkshop
components at offsets `0x60`, `0x64` and `0x68` when applicable. The resulting
centre is not automatically the moved beacon's present XYZ. The function selects
region/location/default data and encounter shape type 5 where present.

Ordinary membership `140f4aa50→140f4aab0` first requires a matching world/frame
identity from `140b4e5f0`; it applies retained origin translation as needed, then
`140f4a910` dispatches on the descriptor mode. For mode 2, `140f4ac50` accepts
`dx²+dy² <= radius²` AND `candidateZ <= upperHeight`; this is a horizontal radial
test with an upper-height limit, not a full sphere. Mode 0 queries its region;
mode 1 uses a linked-keyword volume path; mode 3 returns true. Candidate support,
footprint and collision tests remain additional gates, not part of that equation.

`140f391c0` tests selected-Workshop membership, assigning status `0x0a` if outside;
the no-selected-Workshop/beacon branch calls `140f38cb0`, which can return `0x16`.
That helper resolves the proposed reference's cell location via `140af4c50`,
then `140f38d80` follows each location's parent pointer at offset `0xc0` and tests
native keyword slot `145f0a4a8`. `140156bc0` identifies it as
OutpostNoPlacementKeyword_DO; physical DFOB `0006a236` points to KYWD `0006902e`.
In ordinary exterior cell contexts it also resolves
`140ad3610→140ad36d0` encounter/location state and rejects a present result whose
flags at offset `0x20` have neither low permission bit set. Null encounter state is not
unconditionally rejected. This is actual world/location permission data, not a
fixed distance from the visible POI map-marker.

Final `140f3f9a0` separately revisits current and selected-cell location/encounter
contexts, producing status `0x16` where restricted or contexts disagree. A common
candidate frame can therefore be within radius 150 and still be restricted on its POI side.
The selected site's loaded encounter object, exact generated compound template,
and all photographed candidate operands are UNKNOWN. An excluded location is a
supported mechanism, not proof that the specific image ran a particular branch.

`140f49440` builds the border scene. In radius mode it calls `140f48a60`, sampling
36 angular positions around the radial centre. `140f47de0` inventories nearby
loaded grid cells, their location groups, and encounter permissions; it excludes
the current/allowed groups and accumulates disallowed group rectangles with a
record stride of `0x1c` bytes.
`140f48480` intersects the circle's segment sequence with those rectangles and
adds adjusted boundary vertices before `140f46910` builds geometry. Thus the
displayed circle can be clipped by cell/location eligibility. Geometry is created
for display; it is not evidence of a serialized permanent polygon. No exact
clipped polygon/area can be reconstructed here without the selected loaded grid
and location operands. The 203 m scanner label measures something else.

`140f39010` is a separate restricted-build-radius/other-reference overlap test,
using DFOB WorkshopRestrictedBuildRadius_DO → AV `0006ca31`; do not substitute that
name for the POI ancestry/encounter branch above.

## Admission, errors and precedence

Candidate initialization `140f33180` obtains orientation/support modes and
member/property information; it caches clearance dimensions and admission flags.
`1421d74b0` refreshes candidate transforms and nearby clearing; `140f3f9a0` folds
support, collision, resource, territory and L1/L2 results into the status field
at frame offset `0x193`. `140f7ba90` maps status `0x04` to “Intersects with an
existing object,” `0x0a` to “Outside buildable area,” `0x16` to “Area is restricted,”
and `0x02` to success. This is a shared error-status contract; the
standalone scanner start `1415f6a90→140f38a40→140f387f0` also has its own
Cannot place outpost messages. It must not be confused with final beacon preview.
`1421b2e20` requires the status at frame offset `0x193` to equal `0x02` before
construction. It then calls item creation `1421de3f0` and commits clearing
through `140f30820`, passing the clearing state at `frame + 0x1a8`.

These are ordered assignments, not a single universal first-error selector.
For example `140f391c0` can assign out-of-range before later support tests;
`140f3f9a0` performs late location checks and then the known L1/L2 requirement,
component, budget and group-limit overrides. The return's AL and displayed
status are separate values. No exact competing-failure precedence is inferred
from one photograph. Earlier [L1](../limits/report.md) and
[L2](../build-budget/report.md) gates are retained, not reopened.

## Nearby scenery clearing versus collision

`1421d64f0` obtains size R through the item's virtual method at vtable offset
`0x1f8`, adds small-item padding or large-item
padding according to the large-item threshold, and enumerates nearby references
at the proposed position (`1421eab70`). The compiled small padding is 5 and
the large-item threshold is 10; actual settings may override them. Its radius filter's
callback `1421ea490` ignores candidate/current item members, calls
`140f2f0e0(selectedWorkshop, item, target)`. On classifier result 0, it adds the
reference handle to the clearing state at `frame + 0x1a8` via `140f2ffb0`.
`1421d6100` follows limited
associated-reference dependencies when enabled; no complete PackIn expansion is
asserted. Moving/initializing previews (`1421d74b0`, `1421d5ce0`) runs this pass.

`140f2f0e0` is an eligibility classifier, not an overlap-depth measurement. Its
gates include the already-bulldozed flag (mask `0x04` in the reference byte at
offset `0xd3`), exterior/context restrictions,
Workshop ownership/markers and effective form categories. An ordinary item must
allow clearing through its virtual method at vtable offset `0x158`; a
candidate/target size ratio below fOutpostBulldozeRelativeSizeFactor (compiled
value 0.1) can reject clearing. Main form types `0x29`, `0x2b`, `0x2c`, `0x2e`
and `0x38` take distinct paths, with OutpostAllowBulldoze keyword
exceptions. Do not label every tree, harvestable, static or gas vent alike.
`140f33180` suppresses the item's usual clearing permission when a member has
nonzero OutpostNoBulldozeAV; OutpostBulldozeOnly and OutpostAlwaysBulldoze AV
bindings are separately present. Definition categories are evidence of branches,
not proof that the pictured rock's generated reference has those properties.

`140f2ffb0` maintains temporary clearing sets and initiates scene fading through
`140f3a640`; `140f412c0` reconciles old/new sets and restores removed references'
scene visibility. None of those operations alone proves persisted bulldozing.
The physics path `140f3e2e0→140f460c0→140f46370→140f3f680` tests candidate
collision shapes/transforms with IntersectionTestCollisionfilter and
hknpWorkshopIntersectCollector (`140f51ee0`, at offset `0x20` in vtable `144c24408`).
It skips resolved ignore-set references, selected-item members and particular
categories/keyword/property exceptions before recording remaining intersections.
The collector distinguishes player contact through its field at offset `0x11b`;
final status handling has its own player-specific case `0x19`. Actor/NPC content has no ordinary scenery
whitelist simply because a collision becomes deeper. Qualify exceptional
keyword/property behavior separately; animal AI was not examined.

The causal explanation of the solar pair is therefore a **changing clearing
set**, not a monotone rule on penetration depth. Radius/pivot/bounds eligibility
and collision meshes have different boundaries. Exact same-rock/pivot/shape and
settings operands are unrecorded, so the particular threshold is not fitted.
Camera fade settings are a competing visibility-only explanation; camera fading
alone cannot establish physics admission or saved clearing. The code and positive
saved channel establish a separate construction suppression mechanism, while the
individual screenshot-to-channel join remains absent.
