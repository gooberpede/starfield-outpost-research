# Manual CHANGE, initial construction and automatic adaptation

[Answer](report.md), [census](behavior-rules.csv), [saved joins](saves.md).
`nNNN` means `.local-work/construction-variants/native/NNN.request.tsv`.
[Functions](functions.csv) supplies exact section lines, hashes and export limits.
All native VAs are hexadecimal **preferred static addresses**, image base
`140000000`; RVA = VA minus that base. Object/vtable offsets are hexadecimal.
The imported executable hash is
`7e9adb1414a8e1b325e5e1f097b9b17b78deb7eebeda37a333351a43a60f9d28`.
The freshly verified main ESM hash is
`1dabed00c3f4282dd3bb54d2e9601e40b577d8742d078b7ccef203adbfef0da7`.
Decompiler types and reused locals are not authoritative; instruction listings
resolve the action fields and virtual calls. No function was invoked.

## Definition and discovery chain

PKIN 00051f54 CNAM 00051ecf contains four wall templates with NAME 00068f6d.
That PKIN points SNTP 0005eef9 and SNBH 001e8d95, and carries wall-related
keywords 001e8e1b/00178b0b. SNTP identifies a **STMP** record, and SNBH a
**STBH** record; the subrecord and form-type names are different domains.
The wall STMP has node index 6, STND 0005eefa and transform data.

STBH loader `140a30980` (n013) starts a new entry on ENAM. The entry stores
action at +30, target from PNAM at +10, optional node from UNAM at +18, category
from VNAM at +20, and a condition list at +28. Runtime behavior count +38/array +40
preserve the ordered entry population. The `CITC` and actual CTDA counts agree
for the enumerated rows; [rules](behavior-rules.csv) retain conditions separately
from category and target. Native initialization `140a30fc0` resolves dependent
forms/conditions (n005).

Resolver `140a31340` (n007) considers a reference's OriginalBaseObject (B4),
the base's snap component and the template fallback. Thus the generated current
mesh need not itself carry the original behavior definition. `1421f0e80` (n005)
builds a context containing picked references, 191-linked originals, behaviors,
effective definitions and picked/original DA PackIn identities. This accounts for
selecting a wall through one of its generated pieces.

For STBH 001e8d95, rows 0–6 are ungrouped automatic entries. Rows 7–9 share connected
category 00178b01. Rows 10–13 share unsnapped category 00068f5e: PKIN 001dcf7f,
001dced4, 001dd05d, 00068f6d. The category DFOB 00068f5f points to KYWD 00068f5e.
This is an installed finite family, not a hardcoded list of four meshes in UI.
STBH 001e8d94, the medium wall contrast, has a different 20-entry population.

## Manual user action to authoritative operation

1. Pick/action classification `141589840` (n010) calls `1421f1500` on the selected
   component and advertises behavior bits 100/400 depending on cycling mode.
   Its broader flags also distinguish selection, repair and other actions.
2. UI action sink `14173b980` (n017) sends action 1/100/400 to `1421f4f30`.
   That entry resolves the picked handle and **revalidates** `1421f1500`; enabled
   cycling creates CycleBehaviorEvent, otherwise RevertBehaviorEvent. This is
   distinct from `WorkshopMenu_ChangeVariant`, the builder-catalogue event whose
   registration was an early lead, not the ordinary existing-wall operation.
3. Queued service `1421bfbb0` (n016) checks engine availability and event admission,
   then dispatches state virtual +68. StateInspect vtable 144d4ac60+68 points to
   `1421aec70`, which enters StateCycleSnapBehavior through state object
   14597a980 and entry `1421b2030` (n002/n006/n007/n010).
4. `1421b2030` resolves selected handle context +588. A failed resolution clears
   it. Eligibility is rechecked, item context is refreshed and a unique connected
   opposite side is resolved before `1421e48e0` (n003/n004).
5. `1421f1500` rejects deleted references (form flag 20), requires an actual item
   classification from `1421f16b0`, and checks connected/unsnapped mode gates.
   `1421f0c30` walks actual DE connections, tolerates repeated references to the
   same opposite side, and reports conflicting different opposites. Companion
   linked references and 191 replacement links are resolved explicitly.
6. `1421f0b00` finds the **current** eligible categorized entry. It tests the
   action, actual current base or DA PackIn source, condition result and supported
   unsnapped category. `1421f09a0` requires nonzero category and supported replace/
   remove target; it evaluates the real two-reference context through 140e466f0.
   An unsnapped operation uses the configured unsnapped category and a self/self
   evaluation context. A mere category match is insufficient.
7. `1421f0fc0` obtains entries in that category with 140a316c0, advances from the
   current entry with wraparound, and tests candidates using temporary references.
   For a connected pair it seeks compatible accepted entries on **both** sides.
   It excludes a no-change wrap to the sole current entry. If no candidate passes,
   no replacement is committed. Temporary base/DA state is used for condition
   evaluation; it is not a gameplay save modification by this investigation.
8. On acceptance, previously generated replacement state is cleared as needed
   with 140b4dc20; 140a32780 applies the chosen entry to one or both anchors.
   The wrapper 1421e48e0 refreshes item virtual +98 immediately or through a queued
   service, and emits item/owner/reference notifications. Failed candidate
   cycling has a conditional revert path rather than an invented success value.

The native action flag is a UI decision, not proof of available stock or a cost
transaction. No ingredient collection/spending appears in this mapped cycle/
executor chain. Full construction COBJ costs and L1–L3 placement remain their
[existing separate paths](../build-budget/native.md). The ordinary manual path
does not re-purchase PKIN 00051f54. Custom collision, wiring and furnishing
preservation are not established by the lack of ingredient spending.

## Action and identity branches

`140a32780` (n007) branches on entry +30:

| ENAM | Operation | Native consequence |
|---:|---|---|
|0|Replace|Target must pass object/type checks; 140b4d650 handles primitive versus PKIN separately.|
|1|Remove|Marks/removes representation through configured marker and reference virtual +7e8. No new target mesh is required.|
|2|Add|Requires target and node; computes transform from snap-template data, creates ordinary reference or PKIN children, and links them through SnapBehaviorLinkedRefKeyword 040210.|
|3|Foundation|Handled by 140f5bb30, not the replace/remove/add dispatcher.|

For **PKIN replacement**, 140b4d650 (n008) clears the previous representation,
captures anchor transform/cell, materializes the target with 140a1d4c0, sets each
generated reference's 191 backlink to the anchor and applies the actual Workshop
owner through 140f3cf40. `140f5eee0` (n015) adds generated handles to the resolved
compound construction; clearing uses 140f5f0d0 to remove handles and related
state. The anchor is retained/disabled. Dummy selection, DA grouping and
foundation 192 remain the [Workshop model](../workshop-membership/dependencies.md),
qualified by the [population correction](../workshop-population/routes.md).

For **non-PackIn replacement**, 1418c1f10/1418cafc0 (n009/n011) marshal the
reference/base operation onto the supported service context. Virtual +7b8 reaches
140b4d430 (n015): retain the reference, set base +98, record first original base
with 140511680 (n017), and mark base-object change 80. Extra B4 stores an original
FormID, not a queued reference handle. Revert 140b4dc20 restores the original base,
removes B4 and marks 80; it also removes generated 191-linked children when present.
This branch is a real capability, but ordinary installed hab rules choose PKINs.

## Initial and automatic paths

Initial construction follows COBJ→PKIN→CNAM templates, not a simulated CHANGE
button. The Four Wall Hab includes walls, corners, middle assembly, markers and
lights. Wall 00068f6d itself has a template cell 00068f51 supplying default geometry.
The nested middle PKIN 000185b9 has CNAM 00011083 and no own SNBH/SNTP in this
definition. Initial cloned/reference state is registered by construction
140f5b260 (n013) and 1421dd600 (n019); default and later replacement instances
must not be counted as separate purchased habs.

Committed snap connection 140904d60 (n009) writes both endpoint/node relations
through 140906160, marks change 200, and—when its action argument permits—calls
140a31400 on both sides. That wrapper resolves behavior, calls 140a31050 with
category 0 and propagates configured snap-behavior-linked children. 140a31050
iterates matching ungrouped entries, evaluates 140e466f0 against self/neighbor,
and executes eligible operations through 140a32780. The CTDA rows in the hab
behaviors use function 560 and exact keyword operands on numeric run-on 1/12;
their differing contexts select neighbor-compatible openings and connectors.
The generic evaluator 140e466f0→140e46d70 (n027/n028) closes those domains:
run-on 1 swaps the primary and other reference; run-on 12 obtains the **other
reference's DA +40 PackIn** and evaluates a temporary reference with that base
through 140e47c40 (n030). Thus these rules can distinguish the connected wall's
keywords from its containing construction's keywords. Missing DA/source rejects
that run-on 12 branch. OR-list handling is in 140e466f0; flags and comparisons
remain explicit in the CSV. HasKeyword registration at 1400d5982–1400d5a08
(n029) names the condition, binds 140c49960/140bf2fb0 and registers opcode `0x1230`
(serialized condition index `0x230`, decimal 560). This is more specific than
reading the editor ID.

Single-item and PackIn snap commits 140f60f60/140f66220 (n014) reach 140904d60;
the committed snap-edit state 1421b44b0 also calls it with explicit node indices
and behavior enabled. Preview 1421c9f90 (n020) separately gathers eligible
ungrouped proposals with 140a31550 for candidate geometry, including linked
children. Preview evaluation is not itself proof of committed geometry.

Disconnection 140904f30 (n009) walks DE edges, removes reciprocal relations and,
when enabled, calls 140a314c0 on the pair. That wrapper 140a31210 reverts behavior
effects, generated children and base overrides. Removal/edit callers include
1421de660, 140f61620, 140f688c0 and 1421aed00 (n013/n014/n010).
Automatic doorway, reverting doorway and manual window selection therefore share
an executor without sharing candidate selection or every lifecycle action.

## Foundation, material, damage and scripts

Airlock STBH 00178a51 has two action 3 entries: tower STAT 0000b191 at node 002a08b3,
and stair STAT 0003a1d0 at node 002a0891. STBH 0027fad4 substitutes stairwell
PKIN 0026b107 at node 0033dfd3. 140f5bd50 builds foundation context; 140f5bb30
selects action 3, resolves an object or form-list choices and invokes 140f5a800
or 140f5b130 (n019–n021). This is positive installed stair generation, not a
demonstrated manual choice of arbitrary stair geometry or length.

LMSW 00056f78 references keyword 00056f87 and swap 00056f79. The latter maps
`SetDressing/Outpost/Solid_Storage/Yellow.mat` to a white material; red/blue
collections 00056f84/00056f86 are contrasts. Native 1405335c0/140553a80
(n023/n024) maintain ExtraMaterialSwap (B5)'s array. This is separate from STBH.
The storage base's PTT2 values 002389ae/00178a46 resolve to **TRNS transforms**,
not material presets; their names/positions must not be misread as appearance.
Exact warehouse decal authoring, a player picker and arbitrary after-load
material authority are not established by these declarations. The direct B5
save mask is zero (n026); 140a21d10 merges source/template and destination arrays
through 1405335c0, while 140b43f80 copies them (n025). That is positive reconstruction/
copying evidence, not an arbitrary persistent dynamic material setter.

Destructible ACTI 003809d5 has DEST Health 100 and four DSTD rows, with staged
models for the 75/50/25 thresholds. Damage 1405c0530 (n012) crosses actual stage
thresholds, changes Health damage section 2 and reaches 1405c1a40 for a model
transition. That function calls 140528450 to set ExtraModelSwap 53 with the stage
model and source definition, then rebuilds scene state (n022/n023).
Repair 1405c42d0 resets eligible destruction/Health/model state (n012), through
the [DA1 existing-reference route](../outpost-defense/integrity.md).
DEST/DSTD/DMDL are independent of the manual STBH catalogue. No damaged-hab
window state is invented from the breakable-cave-wall exemplar.

Installed ObjectReference source declares DamageObject, ClearDestruction,
GetCurrentDestructionStage, Repair, OnDestructionStageChanged and OnObjectRepaired.
Its exact inspected Form/ObjectReference sources expose no material-swap or
wall-category cycling method. This is a bounded declaration census, not a claim
that no other engine/script API can ever do it. Fresh source ZIP members and
hashes stay local in scripts-source01.json. C1–C3 compiled-script evidence
separately establishes cargo marker/light animation state and OnLoad reapplication;
operational animation changes are not assembly replacement.
