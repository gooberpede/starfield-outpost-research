# Selected candidate, card, footer and construction request

[Answer](report.md), [catalogue](catalogue.md), [eligibility](eligibility.md),
[source domains and tools](methods.md). All native pins use the current
retail 1.16.244.0 image; `nNNN` is a task-local native export.

## Provider and compiled consumer

| Data/model | Native producer/binder | Installed compiled consumer |
|---|---|---|
| WorkshopCategoryBarData | `141578e50`; binder/model in n010/n009; `aCategories`, `uCurrentCategoryID` | workshopmenu.swf BuildPopupContainer.OnCategoryBarDataUpdate, method 593, uncompressed SWF byte 144716; dynamically builds tabs from sName/uID/bSelectable. |
| WorkshopCategoryInfoData | `1415795f0/141579fc0`; `1415791a0` binds `aPreviewIcons`; `141581060` binds nested aObjectVariants/uCurrentVariantID/bUnearned | BuildPopupContainer.UpdateCategoryInfo, method 594, byte 144936; initializes grid entries and finds selected icon by ID. |
| Concrete variant | `14157a740` supplies name/image, uID, requirement booleans and variant-count string | WorkshopUtils.GetCurrentVariantData, method 56, byte 109087; finds matching uCurrentVariantID, copies iconImage/sDisplayName/sVariantCount/bBuildReqsMet/bSkillReqsMet/uID. GetHasVariants tests length >1. |
| WorkshopObjectInfoCardData | `14157b0c0` builds selected form/recipe data; `14157c6a0` binds fields | WorkshopMenu.OnObjectInfoCardDataUpdate, method 1373, byte 190483 -> OutpostItemCard.UpdateItemData, method 1429, byte 196947. |
| WorkshopInfoData | `14158ef80` binds sOutpostName/sOutpostLocation; `1421f4310` supplies Workshop context and caption | WorkshopMenu.OnOutpostInfoUpdate -> FooterContainer.UpdateFooterInfo, method 620, byte 146761. |
| WorkshopStatusData | Existing E1/L2 `140f34590 -> 14143f690 -> queued 14143f8a0`; `14143fb40` binds metrics | FooterContainer.OnStatusDataUpdate, method 621, byte 146831; production and other metric calculations are reused. |

The normal and large Workshop SWFs and shared-assets SWF are freshly matched
byte-for-byte to the installed Interface.ba2. Every ABC method-body byte span in
four assets is checked (5,923 spans); 48 selected methods are decoded into the
local ui.json. This verifies the inspected compiled input and selected instructions,
not Flash execution or a rendered screenshot. Asset/method/offset hashes remain
in sources.csv and the local receipt; no proprietary SWF/ABC is copied into Git.

## Card fields and assets

The selection state keeps a node and its current concrete leaf separately.
`14157b0c0` resolves the selected leaf's FormID and reverse recipe mapping
(`140f3b080`); it obtains display name from the form, falling back to its
virtual name. The recipe supplies description and construction requirements.
JNAM's current count/threshold uses L1's count helper and `%d/%d` card. The card
binds `sDisplayName`, `sBuildCount`, `sDescription`, `uResourceType`, `bTracking`,
`aBuildRequirements`, `aInputRequirements`, `aResourcesProduced`,
`aRequiredAttributes` and `aRequiredResearch` (n019 `14157c6a0`).

Build costs come through `1421a7060` and the construction source/provider rules
already mapped in SD2. Rows carry required and available counts; eligibility is
separate from the mere existence of those rows. `14172cc90` collects typed
requirements and `1414421f0` the research requirement descriptors; the card
consumer shows the corresponding arrays. `141739c50` and `14173a9f0` obtain
operational inputs/produced resources using temporary form-backed references,
including PackIn members. That is a native preparation path, not a safe
side-effect-free API for an external detector to invoke.

The compiled OutpostItemCard updates name, count, requirements, production,
research and attribute sections from those fields. WorkshopUtils builds the
produced-resource and per-hour strings. Power/production descriptions are nominal
definition/effective-provider information; they are not measured successful output.
Integrity's separate existing-reference binding remains governed by DA1.
The card's description/skill layout limits are not candidate-population limits.

Preview icons have a concrete native asset path contract. `14157a420` formats
`%08xCL.dds`; qualifying plugin forms use `%s/%08xCL.dds` with plugin namespace
and a file-kind-dependent local-ID mask (`fff`, `ffff`, or `ffffff`). The image
fixture receives the resulting name plus its configured prefix in `14157a740`.
There is also a conditional recipe-specific icon override through `140a02af0`.
Thus a valid recipe/model alone does not prove a correct rendered grid thumbnail.
This study does not certify an arbitrary plugin's packaging or every override path.

## Callbacks and admission handoff

1. A tab change emits WorkshopMenu_SelectedCategory with `formID` (method 589).
   Native `14171a1a0 -> 14171a290 -> 1421a6680` changes category/current node.
2. Grid selection emits WorkshopMenu_SelectedGridObject with the **current
   concrete variant ID** (method 591). `14171a050 -> 14171a140 -> 1421a6b60`
   resolves the node and leaf.
3. Variant input emits WorkshopMenu_ChangeVariant with `variantDirection`
   (method 1384). `14171a2f0 -> 14171a3e0` advances or decrements the index,
   wraps by `1421a5fc0`'s eligible count and calls `1421a6810`.
4. These selection paths call `1421bab50`, which queues NewItemEvent when the
   Workshop is in the required ready state, carrying node and selected form.
   Category/variant data and card refresh requests follow through the UI service.
5. ConfirmAction (method 1385) emits WorkshopMenu_AttemptBuild in placement
   states. `14171d930` dispatches the event; `141719fb0` queues or directly calls
   `1421f4ed0`. Only accepted global state 2 calls `1421bb3d0`, producing
   CommitEvent; otherwise it requests the failure sound.
6. Ordinary State placement handlers `1421b2360`/`1421b2e20` still require
   frame +193 ==2 and hand off to `1421b10b0` and established creation/accounting.
   L1–L3 remain the authority for prerequisites/quota, budget and local placement.

The UI may queue callbacks onto an engine thread depending on service state;
NewItemEvent and CommitEvent are different operations. This chain establishes
the ordinary request path without asserting transaction atomicity or safe direct
invocation. BM1's CycleBehaviorEvent is a different command with an existing
reference/behavior context, not this preconstruction variant selector.

## Refresh and cache epochs

Initial map construction clears/rebuilds definition-derived maps.
`1415795f0` rebuilds selected-category candidate data; selection/variant callbacks
request a category rebuild or a narrower current-variant update
(`1415819a0 -> 1415795f0`, `141581960 -> 14157f0f0 -> 14157ad10`). Item-card update
is a separate provider operation (`14157b000/14157b0c0`). Construction preview
refresh separately reevaluates material/prerequisite/quota/budget/placement state.
These paths distinguish display regeneration from authoritative action status.

Existing E1 status requests coalesce by Workshop handle and refresh mask; a worker
updates cache fields and emits statistics events. UI summary reads copy a cache
snapshot and queue delivery. An operand-changing script is not proof that every
visible array, card and status value updates in one synchronous epoch. Actual
resource/unlock refresh timing and every invalidation source remain unmeasured;
no new timing guarantee is inferred from event subscriptions.

## Footer gaps investigated

| Field | Strongest supported binding and counted entity |
|---|---|
| Cargo | Mask 4 in `1421f2cb0` clears ExtraWorkshop+88 and calls `1421f34d0` with WorkshopItem keyword. It walks the owner's reverse-linked member entries, resolves each, requires `1421a9840` target-category keyword and `1421a98b0` active-link keyword, and excludes disabled flag `20`. Constructors `140126ce0/140126d20` bind Target_DO -> CargoLinkKeyword `255c9c` and ReservedTarget_DO -> LinkActive `255cc8`. Thus the integer counts qualifying active local cargo endpoints/members, not cargo ships, trips, freight quantity or every constructed pad. A paired route can contribute one endpoint at each owner; no universal divide-by-two rule follows. |
| Crew | Mask 8 clears ExtraWorkshop+8c and reads CrewExtraData E2+18 count, if present. Constructor `140408a50` defines count/capacity/data at +18/+1c/+20; normal assign/remove consumers maintain the handle list. The footer does not freshly resolve every actor or sum Crew Station capacity. Unresolved/restored handles and refresh age can separate displayed count from currently effective living crew. |
| Outpost name | `1421f4310 -> 14158eb10` selects reference display name, with house/ship-context handling; ordinary branch updates ExtraWorkshop name and queues the WorkshopInfoData name. `14158ef80` binds sOutpostName; method 620 writes NameLabel text. Rename delivery/current saved snapshot are separate epochs. |
| Planet/system caption | Ordinary non-house/ship branch in `1421f4310` obtains reference context and uses two named-form lookup routes, `140910bd0/140911b70`, each resolving runtime type `75`; one input also passes through `14231f9b0` at `1421f499e`. It composes `%s, %s` and calls `14158ec80 -> 141590320 -> 14158f860`. The binder names sOutpostLocation; method 620 writes SubtextLabel. These lookup/composition/binding operations are directly traced; the precise body-versus-system roles of both metadata keys remain unclassified. House/ship context can instead supply a location/reference name. Actual localized wording/overrides and live repaint timing are not measured. |

Needed/total power, Build Limit, Integrity and production basics are reused from
their reviewed studies. The distinct Locations screen's remaining fields are not
silently closed by this footer trace.
