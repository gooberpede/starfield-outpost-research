# Typed native map — SOR-EV-0032

All addresses static VA, retail 1.16.244.0 hash/base in the [report](../event-associated-position-oracle-and-build-mode.md).
RVA is shown for principal operations. Evidence: existing `engine-oracle-01..08`
plus new ignored `event-oracle-01..13` exports; exact export hashes in review
manifest. Decompiler names/prototypes are provisional; instruction operands and
RTTI/vtable associations supply the contracts below. This is authored analysis,
not redistributed native source.

## Ownership and lifetime

`145fd9c30` is the planetary-manager singleton. `140787830` (RVA 00787830)
constructs `BGSPlanet::Manager`, initializes its +130 pointer, allocates0x138
bytes and calls `14079d660` at `1407886e4`; subsequent alias through
`1407886f1` stores the owner at manager+130. Constructor `14079d660`
(RVA 0079d660) installs `BGSPlanet::ProcGen::vftable` and initializes its output
and processing state. This is a heap module owned by the manager, **not** one
cache allocated for each workshop. The tuple itself has no workshop key.

`14079d910` (RVA 0079d910) destroys ProcGen collections/request resources and
returns through `BGSPlanet::IModule`; manager constructor replacement and
destructor `140788bc0`, plus deletion wrappers `14078f670/14078fc90`, reference
that destructor. A raw worker pointer is not lifetime-pinned by this ownership
relationship. Reacquire roots; do not treat equal pointer values after load as
the same allocation epoch.

| ProcGen offset | Typed role / initialization / writers |
|---|---|
| +90/+94/+98 | XYZ binary32; ctor zeros +90/+98 qwords; full publication 1421b29b1 replaces 16 bytes including radius. Reset below preserves XYZ. |
| +9c | radius binary32; ctor zero; full publication; reset 1407a6690 explicitly zeroes this word. |
| +a0/+a8/+b0 | pointer collection; reset empties logical end to begin. Not XYZ/radius. |
| +b8/+c0/+c8 | derived identifier collection; publisher populates; reset empties logical end. |
| +d0 | native lock for publication/reset/activation/update; observation does not acquire it. |
| +e0/+e4 | prior update-position XY; update 1407a5210 writes them. Distinct from center. |
| +e8 | processing enabled byte; ctor 0; activation 1407a50d0; publisher 1. |
| +e9 | forced refresh byte; ctor 0; activation parameter; publisher 1; updater clears after entering refresh path. |
| +ea | dirty byte; ctor 1; reset 1; publication 1; changed activation marks1. Not a general UI-ready flag. |

The ctor-adjacent inventory `14079d660..14079e100` was expanded into actual
functions: destructor wrappers, terrain/collection lookup, cleanup and enumeration.
`14079ddf0` clears owned collections but does not reset the center tuple;
`14079df70/14079e060` enumerate or access other maps. Literal-offset scans are
lead inventories, not type proofs: new +130 scan examined 14,392,060 existing
instructions/3,394 candidates, cancellation=false; existing +90 census is
documented in EXP0021. Pointer arithmetic, undefined code and unknown aliases
prevent a universal all-writer absence claim.

## Concrete publication and reset graph

`1421b2570` (RVA 021b2570) is the +8 entry of
`WorkshopEngine::StateUpdatePlacement::vftable` at `144d49c80`.
`1421be130` and `1421b5e70` select the state through `14597a9c8`, store it at
operation-context+210 and call its entry slot. Selection is not synonymous with
every build-mode-open interval. StateBulldoze has a different table.

At entry RDX is operation context, retained in RSI. When context+630 is 0,
`140f3df70` resolves a workshop from context+268's interface and `140f4a140`
builds a descriptor into context+338 onward. That descriptor branch is separate
from the later shared ProcGen publication branch.

The latter resolves the selected object through context+268 virtual+40 and
`1428ccc40`. Null selection skips. `140f7c9f0` tests keyword 145f0a190 and
excludes the ordinary Workshop activator (keyword 145f0b380); its false path
disables ProcGen without updating the tuple. `1409e8700` builds a derived list
through form-type 0x6d enumeration; an empty list also skips publication and
disables. Do not infer list semantics solely from that form number.
After those gates global **145f5d8e8** must identify a non-null current workshop.
That reference is RBX at the actual center call, not necessarily the earlier
selected object/descriptor input.

| Instruction / function | Exact effect and qualification |
|---|---|
| 1421b28fc →140f4ab80 | Computes actual global-workshop reference center into RSP+50; post-call 1421b2901 retains RBX reference before release at 290 a. |
| 1421b2930 →140f38e30 | Radius returned in XMM0; getter uses resolved global definition/property context, not a proven RCX-reference ABI. |
| 1421b2948 →1407a6690 | Resets previous ProcGen lists/radius before publication. |
| 1421b294d/2954 | Gets owner through 145fd9c30→+130. |
| 1421b29ac/29b1 | Loads stack 16-byte tuple at RBP-68 (radius RBP-5c), stores at RDI(owner)+90 under lock+d0, marks dirty. Then enables e8/e9. |
| 1407a6690 / RVA 007a6690 | Under+d0 clears list ends, writes radius+9c=0, marks ea=1; **no XYZ clear**. Direct code callers 1421b2570,1421b2ca0,1421ba2e0. |
| 1407a50d0 / RVA 007a50d0 | Sets e8/e9 from enable parameter, marks dirty on enable-state change; disable releases owned resources. No tuple write. |
| 1421b2ca0 / RVA 021b2ca0 | Placement-state exit slot+18 disables then resets, and invokes descriptor cleanup 140f4a5b0; retains XYZ/zero radius is expected possible post-exit state. |
| 1421ba2e0 / RVA 021ba2e0 | Reset plus descriptor cleanup; another partial-invalidation path. |

No branch between the center call and full publication tests relocation-vector
zero/nonzero. Helper `140f4ab80` (RVA 00f4ab80) copies reference+8c/+94 on both
paths, adding concrete extra-bc+60/+68 only if its vector is nonzero. Zero
bypasses **addition**, not output production. This rejects the user's proposed
fast path as a sufficient explanation while preserving its useful distinction.

## Consumers and separate boundary channel

`14078c5f0` invokes updater `1407a5210` at `14078c91e`. The updater holds+d0
and does nothing when e8=0. Otherwise e9, camera/position movement threshold
and dirty ea determine refresh work. `1407a6150` constructs the typed
NiPointer<BSProjectedDecal> bounds callback; thunk 1407b0880 adjusts context by 8
and calls `1407a6540` (RVA 007a6540). Its **positive-radius** branch measures XY
distance from +90/+98 to terrain bounds and compares r²; radius<=0 skips that
distance filter, while the optional identifier filter can still apply. This
consumer is projected-decal processing, not complete building permission.

Direct center-helper code callers recovered by uncapped-in-practice refall
(7 code callers; additional packed unwind records excluded):

| Caller | Actual channel |
|---|---|
| 140f4a140 | Boundary descriptor; center+00, frame-index+0c, radius+28, heights+18/+20/+2c, modes including ordinary circle. |
| 140f49440 / 140f49c50 | Border-related consumers documented by EXP0017. |
| 1421bb860 | Camera/point clamp uses global-workshop helper result plus independent radius; does not read ProcGen tuple. |
| 140ad0b90 | Terrain coverage callback; translates center and computes selected hierarchy. |
| 141884350 | Streaming context/player alternative; not automatically active-workshop authority. |
| 1421b2570 | Conditional ProcGen publication described above. |

`140f4ac50` consumes the descriptor's ordinary XY circle/upper-ceiling geometry,
using its selected translation table when +0c qualifies. Other modes/region paths
remain distinct. Radius `140f38e30` (RVA 00f38e30) reads current-definition
145f0a088 and property 145f0ba28, snapshots/searches property components via
14048eba0/14044b670, optionally enumerates pack-in children, then uses setting
145f0b320 if unresolved/zero. Existing EXP0017 native initializer 140157700
binds **fItemPlacementRadius:Workshop**, default `cdcc8e42` =71.40000152587890625;
140157cc0 binds WorkshopBuildRadiusAV. Ordinary ACTI002C60E9 supplies
OutpostBuildAreaRadius AVIF00063FC5 =150.0. Static uninitialized globals are
not evidence that their runtime value is zero. Effective live overrides remain
unmeasured. These channels do not obtain radius from ProcGen+9c.

## Interpretation against Phase 1

All 16 checkpoints had e8/e9/ea=[0,0,1], radius 0. This is compatible with an
inactive ProcGen consumer and prior-center retention, including exact 002 after
Save26 entry. The static graph cannot recover which earlier invocation wrote
003 or 002, why Save25/002 missed it, or exclude worker lifetime/non-atomic races.
There is no per-workshop cache key here; keyed-cache semantics are unsupported.
Observe producer, reset, disable and allocation epoch to distinguish retained
unused state from an active missed update or reused pointer. UI-open testimony
alone does not provide that event history. Native center correctness and
gameplay permission correctness require different qualification evidence.
