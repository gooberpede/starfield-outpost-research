# Independent native caller and coordinate-contract audit

2026-10-13, Australia/Sydney. Specialist work under the [authorized brief](../../implementation-briefs/CODEX_BRIEF_SOR_workshop_center_caller_semantics_idle_camera.md).
Authored interpretation REVIEW-REQUIRED; native exports LOCAL-ONLY. Native
addresses without another qualification below are module-relative RVAs for
retail 1.16.244.0, SHA256
`7e9adb1414a8e1b325e5e1f097b9b17b78deb7eebeda37a333351a43a60f9d28`;
exports use preferred-base VAs (`0x140000000 + RVA`). Runtime activation is a
separate claim from static reachability.

**F4A1D4 constructs a shared Workshop geometry descriptor, F498F1 constructs
circular border geometry, and AD0C36 supplies a terrain-query exclusion
rectangle. None selects a special center-Z mode. A real indexed native frame
translation exists downstream, but the historical captures do not contain its
descriptor/index/selected triple or an invocation join. Automatic vanity-camera
activation and its responsibility for the high-frequency calls remain not
distinguishable.** The static callers include per-reference geometric tests and
candidate iteration, so one center call need not mean one rendered frame.

## Read/export procedure and provenance

This audit independently read the retained instructions, not only preceding
reports. It then used the existing project-authored
`ghidra/scripts/Invoke-OutpostRecon.ps1` and `OutpostRecon.java`, with Ghidra
12.1.2 and installed JDK21, to read existing analysis state in six sequential
`-readOnly -noanalysis` batches (`workshop-caller-01..06.tsv`). No function,
symbol, type, comment or byte was changed; no game, process reader, native
fixture, debugger or observer was run. Tool/source lineage follows existing
SOR-S-0105/SOR-S-0127/0128/0132/0142 and SOR-P-0002; no new third-party
implementation was incorporated. Existing Bethesda material supplies native
evidence, not publication clearance.

Before/after inventories of all 15 files under
`D:/ReverseEngineering/Starfield/GhidraProject/` are retained as
`.local-work/recon/workshop-caller-db-before.json` and `...-after.json`.
Path, length and SHA256 comparison found no differences. Caller-available space
before processing: C:85,265,285,120 and D:135,615,160,320 bytes; both exceed
40,000,000,000. Exports are new ignored files; source inputs remain unchanged.
Every batch returned success, all requested functions decompiled, no xref or
symbol cap was reached. Batch06's two instruction caps are disclosed below.
Ghidra decompilation remains an interpretation; decisive call/operand claims
below name actual instruction addresses, within exported instruction spans.

Verification: all 18 ledger source-pin rows rehash correctly; six export
build/base headers match; 37 requested function exports have37 successful
decompilations; new-document trailing-whitespace check passes. An initial
PowerShell header-comparison diagnostic printed false because its tab-string
construction was incorrect; splitting the actual tagged rows verified all six.
No evidence was edited to satisfy a check. Final caller-available space:
C:85,264,855,040 and D:135,592,955,904 bytes.

The frame-index result was previously documented by
[the engine-oracle contract](../engine-oracle/oracle-contract.md) and
[the event-oracle map](../event-oracle/native-map.md). This audit independently
verifies and connects it to the current question; it does not claim first
discovery. Earlier [cross-session specialist work](../cross-session-center/specialist.md)
supplies the hook/ABI investigation; this audit checks native contracts further.

## Center and three observed consumers

| Site / enclosing function | Native operands, gates and immediate consumption | Source span and confidence |
|---|---|---|
| F4AB80 shared helper | Copies reference+8C/+90/+94 to caller output. Ordinary base/location predicate gates ExtraWorkshop BC lookup; nonzero vector+60/+64/+68 is added to output. No D3 read, caller-mode input or write to reference XYZ. | `workshop-origin-04.tsv:6–58`, RVA F4AB80–F4AC4E; PROVEN STATIC within this body. Zero compensation produces the same output whether the gate succeeds or fails. |
| F4A1D4 in F4A140 | RCX=R15 reference, RDX=stack XYZ. F4A880 can produce status1; own-cell interior or nonzero2116840 result produces status3. Otherwise obtains center, world-like pointer+10, frame index+C, radius+28, heights+2C/+30 and region alternatives. | `workshop-origin-03.tsv:25–243`, F4A140–F4A459; PROVEN STATIC descriptor writes, STRONG geometry purpose corroborated by consumers. No live parent beyond F4A1D4 was captured in060. |
| F498F1 in F49440 | RCX=R14 reference, RDX=RSP+68. Exterior/status2/enabled branch constructs `WorkshopBorderRadius`; center pointer, reference, radius and height/control scalars enter F48A60. Result is attached to scene geometry through virtual+2A0. | `workshop-origin-02.tsv:6–555` instructions and decompilation732/842/900–926; F49440–F49C4E, F498B9–F4993C and F49BF4–F49C19. PROVEN STATIC call/descriptor; STRONG presentation purpose. |
| AD0C36 in AD0B90 | RCX=RBX reference, RDX=stack XYZ. Ordinary base/location tests gate center/radius reads. Adds context's two source-translation words to centerXY, floors/scales, invokes96F5C0, expands radius in selected hierarchy and compares integer rectangles. Overlap clears caller boolean and stops this callback's enumeration. | `engine-oracle-01.tsv:6–204`, AD0B90–AD0EA8, especially AD0C3B–AD0D36 and AD0E25–AD0E8D. PROVEN STATIC exclusion arithmetic; actual050 Q/E/callback ancestry belongs to primary raw chronology. CenterZ is not consumed by this rectangle arithmetic. |

F48A60 is followed beyond the earlier unresolved call: new
`workshop-caller-01.tsv:1893–2068` (F48A60–F48D0E) gets optional terrain/grid
coverage through F47DE0, loops exactly36 angular samples around centerXY using
radius, initializes sampleZ=0, optionally refines samples through F48480, then
calls F46910. F46910 begins with a relative-height calculation subtracting
centerZ from descriptor+1C (`workshop-caller-06.tsv:2950–2987`, F46982–F4698F),
builds vertex arrays and conditionally calls F46840 for sampled heights. Its
complete decompilation is retained at batch06:3552–4375, but instructions cap
at600 at line3551. This supports the scoped geometry purpose and separates
border height shaping from reference-coordinate mutation; it is not an
instruction-complete claim about every mesh-building branch.

The radius is separately obtained by F38E30; no argument to F4AB80 carries a
radius. Its existing definition/property provenance is retained in
[the prior map](../event-oracle/native-map.md). A center-return event alone does
not measure the effective radius or prove that a border was displayed.

## Actual frame contracts and counterexamples

F4A140 copies centerXYZ into descriptor+0/+4/+8. It obtains a world-like object
through B4D0D0 (eligible base types49/56), else5A6C20. If this equals the active
source world's object through5FD9C30→+78→first→+98, descriptor+C receives
global61FAE80; otherwise it receives FFFFFFFF (`workshop-origin-03.tsv`,
F4A1E1–F4A2B6). This index assignment and the world pointer are real native
state; their semantic names remain research aliases.

F4AC50 compares unsigned descriptor+C with the **current** global61FAE80.
If less, it adds the triple at global61FAE88 + index*12; otherwise it copies
centerXYZ. It then tests horizontal squared distance against radius² and
pointZ against the separately supplied ceiling (`workshop-origin-08-retry.tsv:6–46`,
F4AC50–F4ACF5). Although translated centerZ is computed, that predicate does
not subtract it from pointZ or use it in the ceiling comparison. The constructor
assigns the then-current count; if count later grows, the same descriptor may
qualify for indexed translation. Equality at construction is therefore not a
permanent guarantee that no translation will occur. No historical count/table
epoch was captured here.

F4AAB0 additionally compares B4E5F0(reference) against descriptor+10, translates
all three center components under the same index rule and passes the resulting
point into F4A910 (`workshop-origin-13.tsv:1198–1251`, F4AAB0–F4AB78).
F4A910's status2 path tail-calls F4AC50, status0 uses a regionXY predicate and
pointZ ceiling, status1 uses F4B8C0, status3 returns true
(`workshop-origin-08-retry.tsv:341–440`, F4A910–F4AA4D).
The typed mode is a uint32 read in instructions; the decompiler's tiny-float
rendering of mode values1/2/3 is not a floating-point mode contract.

These are actual coordinate transformations and frame/ownership comparisons.
They do **not** establish a serialized-coordinate input ABI. F4AB80 accepts a
reference and copies its current native XYZ; the descriptor carries a separate
world/index convention. AD0B90 instead supplies query-sourceXY plus hierarchy
and does not encode own-cell identity in its grid operands. The historical
query-source key cannot substitute for descriptor+C/61FAE88, and own-cell/world
cannot substitute for a query-source or descriptor index.

The exact signed frame conversion B734C0/B73310 and later replacement writers
remain separately evidenced in [the restoration ledger](../workshop-z-restoration/dependencies.md).
D3 mask02 is not synonymous with a measured height translation: registration
paths can set it without changing refZ. The050 mask is uncaptured. No recovered
selected triple, historical edgeXYZ/validity/epoch or continuous reference
lifetime joins the050 and060 center operands. Consequently fitting an arbitrary
per-site Z correction would not test a native contract. Deterministic physical
terrain placement is compatible with frame-dependent numbers, but compatibility
does not prove that this missing transformation occurred.

## Caller ancestry and cadence alternatives

The existing-refall census is reproduced in new batch01:2340–2352: eleven
direct code callers of F4A140, plus packed unwind metadata (excluded as callable
ancestry). Every direct code caller was followed in existing or new exports:

| Enclosing caller(s) | Concrete use / evidence |
|---|---|
| F2F0E0 | Reference eligibility/status work; F2F479 builds Workshop descriptor, F2F497 applies F4AAB0. Batch01:6–764. |
| 69CD50 | Iterates candidate Workshop references, builds descriptor at69CE56 and tests current reference's world/point membership through F4AAB0 at69CE81. Batch01:765–1177. One invocation can iterate candidates. |
| F46420 | Resolves a candidate handle, checks world equality, computes 3D nearest distance against indexed descriptor translation; optional containment branch builds that candidate's Workshop descriptor atF46652. Batch01:1178–1492. |
| F3C8C0 | Checks player-related point against resolved Workshop descriptor and returns status through output byte. Batch01:1493–1752. F38A40 calls it; fallback F3C7E0→F35EE0 iterates registry entries through F46420. Batch03:553–857/1048–1222; batch04:1855–1965. |
| F49440/F49C50 | Border scene geometry build/rebuild, existing `workshop-origin-02.tsv`. |
| 20769C0 | Script-facing buildable-area check, explicit error text for None/non-Workshop arguments; descriptor→F4AA50 at2076AA7. Batch01:1753–1892. |
| 21B2570 | WorkshopEngine::StateUpdatePlacement entry; context descriptor separately precedes conditional ProcGen publication. Existing `engine-oracle-04.tsv`, [native map](../event-oracle/native-map.md). |
| 21B64C0/21B6DC0/21B6FC0 | Placement/selection state operations build descriptors for selected/resolved references and apply containment tests. Batch02:988–1514; batch04:1980–last function end. Their live invocation is not inferred from build-mode recollection. |

F35EE0 iterates the registry at61DD718+2C8/+2D0 under its lock and calls
F46420 for each eligible handle (batch03:1048–1138). F46420 is also called by
1C0F580 at1C0F89F inside a time-gated update which enumerates the same registry
(batch04:1061–1661). Its callback is in a vtable at4CDCCC0
(batch06:2878–2902); the dynamic owning type and activation are unresolved.

69CD50 is called by69D0E0, which subsequently constructs current-reference
bounds/transform data (batch03:858–1047). 6A5260 calls69D0E0 in a
`hknpAllHitsCollector` collision-query loop (batch04:273–728, call6A5516), and
6AEEF0 likewise calls it (batch04:729–1060, call6AEF94). Their direct parents
6A4180/6AE320 are also read in batch06:953–2877. The first parent has a600
instruction cap at1554, but the decisive6A441B call is within exported
instructions; both have complete decompilation. These are concrete
per-reference/collision/registry routes capable of multiplying descriptor calls.
They establish plausible cadence mechanisms, not the actual origin of060's
parent0 events. No count of center calls establishes a count of camera frames,
terrain updates, objects, or unique Workshops.

## Idle/free-camera audit

New batch01:2231–2244 resolves **AutoVanityState** to existing native vtable
4D03E30; batch02:6–30 reads its entries. Update slot+60 resolves to1E82060;
its static xrefs are its table and unwind metadata (batch05:986–988).
Batch03:156–353 reads the entire update: it computes transform/position,
updates the target scene node and advances angle using frame delta5FBF9A8.
1E82320 obtains the same position through1E823A0 (batch03:491–552).

This follows the genuine dependencies beyond the first indirect call:
1E823A0 resolves the target handle, uses virtual+558's scene-node position,
offsets/height and camera basis, then calls1E8DC20/1E8DFA0
(batch04:6–272). 1E8DC20 chooses physics world from target parent and performs
segment/shape collision through F128A0; 1E8DFA0 resolves interaction/target
state, including a distinct Workshop-context condition (batch05:6–879).
F128A0's complete exported instructions/decompilation are batch06:6–952;
they use Havok shape-cast collectors and target filtering. This is an actual
camera-collision route, distinct from6A5260's descriptor route. No direct
F4AB80/F4A140 call or reference+8C/+94 write is established along the inspected
AutoVanity position/collision chain. Shared generic physics services do not
prove that the two routes joined in either recorded session.

The native **DebugFreeCamera** table4C45858 is separately read at
batch02:31–55. Its update12F3D90 changes its own position/orientation from
camera controls/frame delta; getter12F4050 returns `Debug Camera Free`
(batch05:1245–1493). This is not evidence that the user's automatic idle
mode is debug free camera, nor that either activated. Workshop fly-camera
and the known21BB860 clamp are further distinct camera mechanisms documented
by the existing event-oracle map. No attribution transfers between these names.

**Static verdict:** not distinguishable for automatic-idle activation and
responsibility in the observed sessions. A unique camera/frame-loop explanation
is unsupported because there are multiple real per-reference iteration callers.
This is not a universal assertion that camera actions cannot indirectly cause
geometry checks. The graph stops at a precise evidence boundary:060's center
events carry no dynamic F4A140 parent return address/stack or camera-state
epoch; static expansion of generic collision services cannot recover that
missing historical selection. No camera-to-reference-XYZ producer dataflow has
been demonstrated. Therefore camera-caused XYZ mutation is not supported.

## Discriminating next observations and contribution

The smallest cadence discriminator is the native return address into F4A140
or its immediate dynamic parent at the center boundary, with TID and camera
state identity/epoch. This would distinguish registry/collision/placement/script
routes without assuming a frame-rate cadence. The smallest coordinate
discriminator remains a matched natural AD0C36 operation with input/outputXYZ,
D3, own parent/world, compensation and exact Q/E source; if applying descriptor
frame conversion, additionally retain descriptor+C/+10 and the selected
61FAE80/61FAE88 triple with its epoch. None is an approved observer or live run.

Specialist contribution is the independent native classification of the two060
sites; tracing F48A60 into36-sample border geometry; following all eleven known
descriptor callers; demonstrating real registry/collision multiplication paths;
and checking actual AutoVanity and DebugFreeCamera tables/position dependencies.
The indexed-frame contract is corroborated prior knowledge, with the new
counterexample that the constructor writes then-current count and the later
predicate compares current count. This prevents silently equating copied
centerXYZ with every downstream geometric frame. Primary raw chronology and
independent final review decide the integrated scientific outcome.

## Hash pins

All native filenames here resolve beneath ignored `.local-work/recon/`.

| Source | SHA256 |
|---|---|
| workshop-caller-01.tsv | 0698190d40828c9eada22b827aa3fb4f0dfbbf110b2cba9e260f85da8c898f79 |
| workshop-caller-02.tsv | 679880f9a28baafda8a3ee1aa3370fc774a374e19be196c169f8028efd5c83f4 |
| workshop-caller-03.tsv | 23aebdaba869042aa6b26a019d6a722b7c9d101ac9fbb352c662f863e0142450 |
| workshop-caller-04.tsv | 3401375edd4dd4b27fec75a4e613492226d199671cf04d49c3b71af7c04857a9 |
| workshop-caller-05.tsv | 40b7227d242dc5bc595506dc1065790feb95dad0c88fd40cdd17663ffa1aace8 |
| workshop-caller-06.tsv | 8d952e3ffc9408dae9f11d6eb166bfd84a550500aa8a971518f0fabbda1585db |
| workshop-origin-02.tsv | bf5ad254692fd06fb74aca2d47885e880330efbe7eae719ddac091d4b9e63255 |
| workshop-origin-03.tsv | 0b2b6adee14887253ad4443a5dd02c12c5f3f32d1fb283817576857097f3ccff |
| workshop-origin-04.tsv | c087406d27e0c8c04ba79e496b537ff415e264ac77f46584085fdc68b329e9a0 |
| workshop-origin-07.tsv | e1d6bae3a5268d20c8cb4a02446d5ca0712fdeb353b4c6bae79d423096d62a12 |
| workshop-origin-08-retry.tsv | f2da2c249eba21280555c23f02a56caf8b13327bef75dce39ced5b3f010ee647 |
| workshop-origin-09.tsv | 398c5f36885c1b58c5cf32e8dccfe2f7f5862061ab9a99183f2f5c66b4357992 |
| workshop-origin-13.tsv | fe563465e9e160c1e8d88277ab8761e387a85b7120d209cacc696ff064de357c |
| engine-oracle-01.tsv | 33c4508537b7993cc6942a3ecc8bc8b8bd77812a5d3bb9c7b104efa5ac35cfad |
| engine-oracle-03.tsv | 32906fa6cfe6e2e7ca8a80f04d0753d1bba59198db0b68e31dabe5d219c0921a |
| ghidra/scripts/Invoke-OutpostRecon.ps1 (repository source) | 23849f10be61a17ff681529aae96e12e98f0f5f77b858a0029d36b924ac6d8dc |
| ghidra/scripts/OutpostRecon.java (repository source) | 8faa1330593d3874150b269b3b4b9cf5b5becab9fc35bb003e1d960a61ea65b7 |
| workshop-caller-db-before.json / after.json | a8d56f6aaf834bc7529db3beb889c0124704ed097c72e14a5da34a1435395f2b |
