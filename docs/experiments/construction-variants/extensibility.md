# Extension map and outpost/ship boundary

[Answer](report.md), [taxonomy](mechanisms.md), [source trace](manual-and-automatic.md).
This is a mechanism map, not an implementation proposal or mod prototype.
Definition-driven means an existing generic consumer accepts the demonstrated
record relationship; it does not mean an untested new record has been validated.
Script-assisted requires an actual exposed operation/event. Native-dependent
requires an identified engine restriction, not merely a missing example.

| Family / intended capability | Minimum demonstrated relationships | Classification and actual limit |
|---|---|---|
| Another ordinary wall/window in an existing hab family | Anchor/template with BGSSnapTemplateComponent; correct SNTP/STMP/STND geometry; SNBH/STBH entry with ENAM 0, valid target PKIN/CNAM children, nonzero compatible VNAM category, eligible conditions; matched opposite-side rules where connected | **Definition-driven, conditional.** Discovery iterates the behavior's actual entry array and groups by category; no fixed four-entry UI catalogue was found in this path. A model alone or a COBJ alone does not join that catalogue. No new record was built or loaded. |
| Another automatic doorway/connection response | Ungrouped STBH entry (VNAM 0), correct target/action, conditions evaluated against the connected pair, compatible snap nodes/transforms and any companion-reference key | **Definition-driven, conditional.** Connect/disconnect providers already apply/revert behavior. Merely adding a manual-group entry does not make it an automatic rule. Conflicting overlapping rules and disconnected reversion must be considered. |
| Separate inside/outside choice | Existing wall variants bundle both sides in a target PackIn; separate reference/node/behavior definitions would need to preserve compatible geometry and connectivity | **Unknown** as an independent ordinary user operation. Bundled geometry is demonstrated; no general independent-side selector or guarantee of leak-free/compatible collision follows. |
| Individual floor/ceiling appearance | A real separately addressable component plus behavior and eligible category, or a distinct mesh/material/containing-assembly relationship | **Unknown** for ordinary individual floor/ceiling CHANGE. The primary Four Wall Hab graph does not supply one. The generic behavior resolver is not restricted by a literal “wall” name, so absence of installed entries does not prove native dependence or impossibility. |
| Airlock stair/support alternative | Existing action 3 rule, object or list target, valid attachment node and foundation-generation context; target geometry and support bounds | **Definition-driven within the demonstrated foundation protocol.** Native 140f5bb30 admits those data relationships. Terrain-conforming dimensions and arbitrary player cycling are **unknown**; no manual wall entry automatically grants variable-height stairs. |
| Cargo compartment visual state | Fixed CONT model/reference in its assembly; operational cargo marker/light scripts, configured animation data and events for a state-driven display | **Script-assisted** for the demonstrated animation route, using PlayAnimation/custom events and OnLoad reapplication. This does not expose manual container geometry selection or change inventory role/pairing. Introducing a new animation requires a compatible authored asset, outside this brief. |
| Storage recolor/material substitution | Matching material key/override paths and keyword collections (LMSW); actual application to a model/reference/template array; native consumer/reconstruction | **Definition-driven material mapping; unknown user-selectable decal capability.** Warehouse white/red/blue collections are installed facts. The ordinary wall STBH catalogue does not discover them. Exact arbitrary decal injection/picker and persistence cannot be promised. |
| State-driven intact/damaged wall | Destructible-capable base with DEST/DSTD thresholds and stage DMDL models; native damage/clear/repair consumers and compatible references | **Definition-driven stages, script-assisted state changes** through the declared DamageObject/ClearDestruction/Repair operations and destruction/repair events, subject to native gates. The positive wall is a cave wall; normal hab replacement definitions lack this DEST setup. No ordinary outpost repair entitlement follows from adding a damage model. |
| Change a non-PackIn component base after construction | Accepted behavior target and reference type; main-thread/service base-change operation and OriginalBaseObject (B4) lifecycle | Existing **definition-driven action branch**. Direct calling from an arbitrary mod remains **unknown integration**; no stable exposed Papyrus base-swap/cycle API was established in the inspected declarations. |
| A genuinely new selector/action outside the admitted action protocol | A new action would need a consumer: 140a32780 handles 0/1/2; 140f5bb30 handles 3; other values do not create a new operation | **Native-dependent for a new ENAM operation**, unless implemented separately through an established exposed script/API route. Appending another data entry in an existing action is not the same as adding a new action type. |

## Eligibility and identity constraints an author must preserve

Manual cycling requires an existing selected construction/component, an eligible
current entry, a nonzero group and a next passing candidate. A unique connected
opposite component and compatible two-sided candidate may be required. The
unsnapped path uses configured category 00068f5e. Conditions, base/DA identity,
item classification, deleted state and engine/event admission are actual gates.
No research/rank/resource gate is invented for the wall path merely because the
hab's original COBJ has construction requirements.

Generated PKIN geometry can replace **child references** even while the original
anchor and outer construction root survive. References with wiring, attachments,
scripts, collision, destruction or inventories cannot be declared equivalent
merely because their replacement looks similar. The native executor handles
member registration, links and refresh; there is no demonstrated blanket
promise that arbitrary attached furnishings or power wires migrate to every new
child. Existing [P1](../power/report.md), [L3](../spatial-placement/report.md),
[SD1](../containers-displays/report.md) and
[SD2](../shared-outpost-storage/report.md) remain scoped sources.

The native model-material, snap behavior and destructible components are
different components. Adding a material path does not create a wall candidate;
adding a damage stage does not add a CHANGE option; adding a construction recipe
does not populate an existing component's category. These distinctions are
supported by the separate producers/consumers, not by editor-facing terminology.

## Ship architecture: what transfers

The complete main-ESM STBH census includes ShipBehavior wall-to-doorway,
door-plug, hatch-plug and cross-passage records. Positive bounded exemplars are
STBH 000ce207 (Nova fore/aft wall), 00051cf5 (interior hatch plugs), 0004fb78
(exterior door plugs) and 003e4024 (cross-passage plugs). They contain the same
ordered action/target/node/category/condition fields and use bases with the same
snap-component link vocabulary. They are listed beside outpost behaviors in
[behaviors.csv](behaviors.csv), without renaming them as outpost behavior.

Transferable: the **definition representation**, generic STBH target/action
interpretation, node-addressed geometry relationships and distinction between
automatic replacement/removal and visual materials/destruction.

Not established transferable: terrestrial StateInspect/CHANGE input admission,
WorkshopItem owner/group rules, 191/192 interpretation on every ship interior,
ordinary outpost resource/budget handling, or exact ship save restoration.
Ship module variant FLSTs/ShipModuleVariant AVs are an additional architecture,
not proof that an outpost component catalogue uses the Ship Builder menu.
The wider Workshop audit's ship-source replacement counterexamples are retained
in [its route ledger](../workshop-population/routes.md).

No comprehensive ship module enumeration, interior generation reconstruction,
ship combat or extension prototype was attempted. The supported conclusion is
shared lower-level declaration mechanisms with context-dependent selection and
persistence, not universal parity and not wholesale architectural separation.
