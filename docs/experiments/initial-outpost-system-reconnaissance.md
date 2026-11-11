# Initial Outpost-System Reconnaissance

**SOR-EXP-0001 — 2026-10-06 (Australia/Sydney). Status: reconnaissance executed; review required.**

Governing authority: [initial brief](../implementation-briefs/README.md#archive-lookup) (`implementation-briefs.zip :: docs/implementation-briefs/CODEX_RESEARCH_BRIEF_initial_outpost_system_reconnaissance.md`), explicitly invoked by the user; SOR-D-0008/0009. Publication: REVIEW-REQUIRED for authored notes; underlying game inputs, script extracts and Ghidra/xEdit exports LOCAL-ONLY. No live/save experiment executed.

## Scope and baseline

Question: which definitions and exposed/native operations provide the best first route to identifying workshop ownership and object membership? Reconnaissance covers both runtime-system and persistence leads, without claiming either has been dynamically validated. [SOR-ENV-0001](../PROVENANCE.md) independently identifies installed/pinned Starfield and CK 1.16.244.0, matching hashes and preferred base `0x140000000`. Ghidra import hashes also match. No address here is a runtime address.

Permitted operations: inspect public pages; read/hash installed files; extract selected development-script sources to ignored local storage; export bounded existing Ghidra state with analysis disabled and read-only mode; create original small helpers and documentation; user-operated xEdit read-only extraction. No target launch/attach, save access, plugin mutation, Ghidra analysis changes, dependency adoption or external disclosure. Source saves including Save2 were not used. All helpers document reads/writes and prerequisites. Stop on wrong executable identity, database mutation, export failure, unexpected plugin writes, or data outside scope. Preserve originals and failed outputs; retain private exports for review. Installed xEdit helper remains for the requested session.

## Methods and sources

1. Read required policy/records and apply the brief's bounded crash-tolerant policy decision before research. Initial Git state: clean tracked tree/index, supplied brief untracked.
2. Inventory and hash actual local inputs; compare installed/pinned executables and Ghidra metadata. Sibling docs used only as environment locators (SOR-S-0111).
3. Search public repository/mod documentation using outpost/workshop, cargo link, production/storage, robot/crew and xEdit terms. Recheck both initial source leads. Record useful sources and limitations in [SOURCES.md](../SOURCES.md).
4. Inspect authoritative installed `Tools/ContentResources.zip`. Extract only 19 selected `.psc` entries using .NET ZIP APIs to `.local-work/recon/scripts/`; preserve entry bytes, hash the archive and extracted files. No third-party mirror or decompiler required. Exact paths/line anchors below refer to these archive entries, not copied repository source.
5. Original Ghidra helper queries existing strings/xrefs, then selected registration/callback functions. First vocabulary scans reached the 350-string cap; narrowed interface/RTTI scans also have explicit coverage limits. No absence claims from those scans. Full instructions/decompilation remain local.
6. Original xEdit helper samples matching definitions rather than dumping the ESM. User-operated run requested because an unattended Starfield route was not established. Its initial missing unit terminator caused a parser error; corrected before the retry. Results and bounds are recorded separately below.

## Third-party prior-art survey

All external behavior claims below are **SOURCE-REPORTED**, not corroborated live here. Repeated claims do not increase project confidence.

| Source | Useful contribution / limit |
|---|---|
| SOR-S-0101 Nexus Mods StarfieldSaveTool | README explicitly focuses on metadata; useful container lead, no demonstrated outpost payload interpretation. No tool execution or template reuse. |
| SOR-S-0102 rux616 vanilla-script mirror | Version-labelled source discovery; local Bethesda archive independently used instead. Mirror byte equality UNKNOWN. |
| SOR-S-0106 SKKmods Universal Stash 009 | Capacity limits, workbench reconnection after unloading and transfer-container deletion are discriminating controls to investigate. Current-build behavior untested. |
| SOR-S-0107 Community Patch issue 155 | Return-flow symptom reportedly differs with player presence/sleep. Older reported game version; needs reproduction and a loaded/unloaded distinction. |
| SOR-S-0108 CommonLibSF | Potential native interface reference; consulted README/limited directory, no workshop layouts/offsets adopted. |
| SOR-S-0109 SenterPat OUT | Build-content expansion and snippet-level robot assignment/bonus lead. Cached documentation, no implementation audit. |
| SOR-S-0110 Sgtsplat Unique-Resource Containers | Single-resource storage/link design suggests a simpler control case. No mod installed. |

Survey limitations: no exhaustive Nexus/GitHub census, no private Discord/forum material, no author contact, no mod implementation comparison. Bethesda installed development sources supply the script interface evidence. Public CK-related discovery produced useful source provenance but no independently validated CK documentation claim about runtime layout.

## Static game-data map

The user ran both readers with only Starfield.esm and xEdit's Starfield.exe pseudo-file loaded. First pass: 3,829,247 records traversed (operator report), 54,855 signature-eligible, 1,743 name matches, 120 detail records; detail cap reached in AVIF/FLST. Second exact-name pass: 15 of 20 requested names matched/detailed, no cap flags; operator reported 1:39. These are xEdit interpretations of the hashed ESM, not independent binary decoding. Five unmatched names were CK terminology guesses, not proof of absent concepts: the actual inventory includes WorkshopKeyword 00054BA7 and WorkshopItemKeyword 00054BA6. Names and default-object labels are not interchangeable.

| Starfield.esm record | Definition observation | Focused export evidence key |
|---|---|---|
| ACTI 002C60E9 OutpostBeaconActivator | VMAD outpostbeaconscript; WorkshopKeyword 00054BA7, MustPersist 0004AF68; OutpostBuildAreaRadius 150 | ScriptName; KWDA 2/3; PRPS 0 |
| COBJ 00299547 co_Outpost_Storage_Solid_01 → CONT 0023AED9 OutpostStorageSolid01Sm | Created-object edge; CarryWeight 75, OutpostBuildContainer 1; ContainerFilter_Solid FLST 0029954D | COBJ CNAM; CONT PRPS 0/1 and ONAM |
| CONT 002CE194 OutpostTransferContainer01 | OutpostContainerScript attachment; ordinary small storage has no VMAD row in this inspected definition | VMAD ScriptName; compare 0023AED9 |
| CONT 0027319F OutpostBuilderA01_AdaptiveFrame | PowerRequired 00000330 default 5; ResMfg_Tier01_AdaptiveFrameAV 00245794 default 1; CarryWeight 15 | PRPS 1/7/0 |
| COBJ 0021919F co_Outpost_Misc_PI_CargoLink01LandingPad | Created-object edge to PKIN 002191A0 OutpostPI_CargoLink01LandingPad | CNAM; PKIN body not traversed |
| QUST 002A6C44 SQ_OutpostCargoLink | SQ_OutpostCargoLinkScript and keyword property assignments | VMAD ScriptName/Properties |
| ACTI 002A6C3F OutpostCargoLinkMarker | Marker script; animation AV 00333D22, quest 002A6C44, ship template GBFM 00255CC6 | VMAD named Properties |
| ACTI 00219523 OutpostCargoLinkMarker_Fueled | Same script; RequiresFuel true, SpaceshipDefaultCarryWeight 500, ship template GBFM 00219042 | VMAD named Properties |
| KYWD 002A6C46 / 002A6C45 / 00255CC8 | Incoming / outgoing / active cargo-link definitions | Record rows/quest properties |

Beacon properties connect LocTypeOutpost 000234F1, OutpostSurveyBoost 000924F7, OutpostTutorial QUST 001ED71C, SQ_Companions 002A567C, SQ_Crew 002A567D and SQ_Parent 0007092C. These definition links substantiate the script/quest map, not execution order. Beacon/storage reflection includes BGSEffectSequenceFormComponent; no runtime layout was inferred.

The inventory includes 33 globals, 200 form lists, 51 NPC_, 577 COBJ and 36 AVIF matches. Counts include lexical false positives (e.g. Argos Extractors); they are not subsystem cardinalities. PKIN bodies, arbitrary referenced forms, unnamed definitions, robot attachments, detailed production recipes and resource-native definitions remain incomplete. No runtime winning-override/profile resolution is asserted. MustPersist is a keyword observation, not a save proof.

## Script/interface map

**PROJECT-VERIFIED STATIC**, limited to the hashed installed development archive (SOR-S-0104). Local source may differ from shipped PEX or runtime bindings; attachment/property values require ESM verification. Declared interfaces are EXPOSED-INTERFACE, not validated mod integration points.

| Area | Exact archive-entry locations (`Scripts/Source/`) | Classification and observation |
|---|---|---|
| Membership query | `ObjectReference.psc:636`; resource/owner queries 568–575 | NATIVE-DECLARED: `GetWorkshop`, `GetWorkshopOwnedObjects`, `GetWorkshopResourceObjects`. Owner/resource subsets must not be equated with every placed object. |
| Beacon lifecycle | `OutpostBeaconScript.psc:33–96` | MIXED: crew callbacks, unload/load handling, location-keyword update, placement callback and attack timer are script logic calling other scripts/native APIs. No creation authority established. |
| Placement/removal/output link | `ObjectReference.psc:1766–1782`; `OutpostEventHandlerParent.psc:1–12` | Exposed event declarations and script dispatch hooks; ordering and event sender semantics remain untested. |
| Power | `ObjectReference.psc:693,773,1677–1697` | NATIVE-DECLARED queries and event surface (`HasSharedPowerGrid`, `IsPowered`). No graph/propagation algorithm recovered. |
| Storage/local redistribution | `OutpostContainerScript.psc:4–78`; `ObjectReference.psc:823,918–921` | MIXED: load/unload inventory-event registration and ready/busy state dispatch native redistribution after selected player transfers/menu closure. Capacity-respecting native bulk-removal option exists; native behavior untested. |
| Organic extraction | `OutpostHarvesterFloraScript.psc:30–102`; `OutpostHarvesterFaunaScript.psc:93–108,129–164` | MIXED: selected resource ActorValue and flora/fauna creation/cleanup logic; does not establish inorganic extraction rate or simulation loop. |
| Manufacturing | `ObjectReference.psc:1142,1797` vicinity | Native builder-menu surface and resource-selection event are leads; no factory scheduler or recipe evaluation established. |
| Cargo endpoint pairing | `OutpostCargoLinkPackinScript.psc:8–22`; `OutpostCargoLinkMarkerScript.psc:54–81`; `SQ_OutpostCargoLinkScript.psc:188–373` | MIXED: pack-in forwards events, marker requests clear/create, quest handles endpoint/ship relationships. Name-based keyword properties identify candidate links, not assigned FormIDs. |
| Cargo movement | `SQ_OutpostCargoLinkScript.psc:110–183` | SCRIPT-IMPLEMENTED orchestration with native calls: chooses endpoint links; unload/load use inventory transfer; invokes redistribution; supports specific-cargo path. Native capacities/atomicity UNKNOWN. |
| Cargo time/loading | `SQ_OutpostCargoLinkShipScript.psc:45–66,117–165`; marker `:47–51,84–88` | MIXED: game-time timers, ship landing/takeoff handlers; OnLoad reads animation ActorValue and reapplies animation. No universal offscreen behavior inferred. |
| Crew/robots | `OutpostActorScript.psc:17–47`; `OutpostCrewStationScript.psc:5–8`; `ObjectReference.psc:212,366,1194` | MIXED: optional assignment via workshop and native crew API; station removal calls crew-count handling. Specific robot attachments UNKNOWN. |

## Creation Kit native leads

Existing analyzed CK uses the same preferred base but its own hash; never transfer its RVAs into Starfield. `ck-strings.tsv` records descriptive labels and xrefs for workshop activator, placed item, location relationship and component-container relationship. CK RTTI contains `Workshop::ExtraData` (`.?AVExtraData@Workshop@@` at static `0x14d996080`), `DialogWorkshop` and `BGSWorkshopBuildingRulesErrorDialog`. RTTI presence is a **PROJECT-VERIFIED STATIC** name observation, not a structure layout or live mechanism.

Selected CK routines `FUN_140470810`, `FUN_140470770`, `FUN_140470900`, `FUN_140470590` are implicated by these labels. Their exact roles are assessed from bounded exports; labels alone support default-object/terminology leads, not runtime membership authority. No CK UI launched.

Bounded instructions/decompilation show these routines passing Workshop/WorkshopItem/WorkshopLocationLink/WorkshopContainerLink names and descriptions to a shared registration routine. This supports the default-object registration aliases; CK names differ from some actual ESM EditorIDs.

## Starfield native leads

`starfield-interfaces.tsv` links the `GetWorkshop` literal at `0x144d351d0` to `FUN_14209be00`. Instructions `0x14209be4a–0x14209be51` load `0x142073cf0` and store it at offset `+0x50` in the native binding object. Parallel registrations associate `GetWorkshopOwnedObjects` with `0x142073dc0` and `GetWorkshopResourceObjects` with `0x142074870`. These are registration-to-callback associations, not a claim that the callback ran.

The analyzed image also contains RTTI-name strings for `Workshop::ExtraData` (`0x145a9f968`), `ExtraWorkshopSnapping` (`0x145a48440`), power/transfer-link workshop items and workshop event sources. Presence is STATIC; field layout and serialization remain OPEN.

Following the binding reveals four existing instructions at `0x142073cf0–0x142073d01`: source operand `[R8+0xc8]`, key from `0x145f0b3d8`, zeroed third argument and tail-jump to `0x140517d60`. Ghidra has no function at that callback; instructions were exported without creating one. The target contains keyed search/reference-resolution and synchronization operations; its semantic alias remains provisional. Direct PE reads confirm the callback bytes and three registration RIP-relative targets. The global's resolved keyword/form and runtime authority were not determined; its 24-xref cap is not a complete caller list.

`FUN_140c7af90` calls `FUN_1421bb570` and emits an outpost-beacon diagnostic on failure. It is a removal/validation investigation lead; a diagnostic alone does not prove the callee is a destructor. `FUN_140c05220` has workshop-activator validation and resource-damage diagnostics and calls `FUN_140f35870`; it is lower priority than membership for the first experiment.

## Persistence leads

1. `OutpostCargoLinkMarkerScript.OnLoad` reads `OutpostCargoLinkAnimState` and reapplies animation. This establishes a source-level reconstruction consumer, **not** where/how the ActorValue is saved or whether it is authoritative after load.
2. `Workshop::ExtraData` and placed-reference relationships are concrete native candidates, but no save/load virtual methods or serializer bytes are yet identified.
3. Script properties (`isLinked`, `SpecificCargo`, `OrganicResourceAV`, crew/link properties), native linked references and inventories are candidate state domains. Their saved offsets, formats and cross-domain identities are UNKNOWN.
4. `OutpostContainerScript` re-registers events on load; losing/rebuilding registrations is distinct from inventory persistence. No script-VM serialization was inspected.
5. Source-reported unloading concerns (SKKmods) and player-presence cargo differences (Community Patch) motivate paired restoration and loading-state controls. They are not persistence proofs.

## Initial subsystem map

See [initial map](../subsystems/initial-map.md) for the ten requested areas with interfaces, state candidates, persistence questions and observation priorities. Identity and script-side cargo/storage are better supported than production rates, native power graph, factory scheduling or saved representation.

## Established static findings

See [known facts](../known-facts.md): explicit scope is source declarations/control flow and independently matched native registrations. No RUNTIME, SAVE or CROSS-VALIDATED finding is claimed. All publication review remains outstanding.

## Strong interpretations

The native `GetWorkshop` callback is the best initial observation path because a local declaration, registration literal and stored callback agree. This is stronger than a string-only guess but does not establish that its returned object is the sole authoritative owner. Script code uses the query for assignment/flora context, supporting its relevance.

Cargo links span scripts and native interfaces. Pairing, transfer orchestration, game-time waits and visible animation are distinguishable paths; treating one as the whole simulation would conflate them.

## Provisional interpretations

Workshop extra data may participate in ownership/membership and reconstruction. Competing models include a direct member-to-beacon association, an indirect membership container, and location/keyword-derived association with caches. These remain discriminating hypotheses, not adopted layouts.

## Open questions

Which relationship is authoritative, what does `GetWorkshop` return before/after registration, and can the membership queries omit non-resource objects? Which pack-in reference is the member? Does removing a link differ from removing its endpoint? Which runtime objects survive unloading versus get reconstructed? Which state is restored from save versus recomputed? Are script/archive and shipped PEX versions equivalent? Which production/assignment modifiers act natively? How do unsupported or unnamed ESM records affect this initial map?

## Candidate observation/breakpoint targets

Preferred: independently qualify the `GetWorkshop` callback and its immediate native target, then observe return relationship alongside placed object/beacon identities. Secondary: placed/removed/output-link events, membership query callbacks, and later cargo marker change + quest transfer entry. Registration constructors are mapping evidence, not recommended recurring breakpoints. Resolve runtime base per process; validate instruction bytes and calling convention first. No write/hook/attach approval follows from this list.

## Remaining permission/rights issues

No third-party code copied/adapted, dependencies vendored, forks/PRs/issues/comments/contact, staging/commit/push or publication. Bethesda source extracts and all raw static outputs stay ignored/local. Small factual summaries and identifiers still require publication review. Tool licences identify tools, not rights in game-derived outputs. Any future SFSE/CommonLib/tool reuse needs its own scoped rights/user decision. xEdit script placement is explicitly authorized, but successful execution is separate from authoring.

## Files/evidence produced

Authored helpers: [xEdit reader](../../xedit/README.md), [Ghidra reader/launcher](../../ghidra/scripts/README.md). Durable changes include policy, decisions, provenance, sources/credits/notices, subsystem map, function/state registers, findings/hypotheses and research state. Local artifacts: baseline/plugin inventories, source-entry hashes/extracts, bounded Ghidra reports/logs, before/after database hashes, xEdit exports, review diff/status and verification results. [SOR-EV-0001 evidence index](evidence/initial-reconnaissance/README.md) lists exact hashes and anchors without distributing proprietary raw artifacts. [Audit](../audits/README.md#archive-lookup) (`audits.zip :: docs/audits/initial-reconnaissance-validation.md`) records actual checks and limits.

## Recommended first live/save experiment — SOR-EXP-0002 (PLANNED, NOT AUTHORIZED)

**Question:** which runtime object/relationship identifies an outpost/workshop and associates one ordinary placed storage object with it, before and after save/reload?

Start from a new disposable test-playthrough copy with fixed plugin profile, a surveyed buildable site and enough inventory for a beacon, one simple storage object, one extractor and any necessary power. Protect/hash originals and disable no features without explicit approval. Never use Save2 or an active playthrough. First qualify the exact loaded game/SFSE/probe build and the callback ABI; no presently built/deployed observer exists.

Proposed sequence: A0 before outpost; A0-control after a matched no-action wait/save; A1 beacon only; A1-control same-duration no-action save; A2 beacon + storage; A2R reload A2 and repeat identity/query observations. This is the first decisive tranche. Only in a subsequently approved extension add A3 extractor (with separately controlled power state), A4 extractor-to-storage output link, then a link-removal control. Separating A2R prevents production/cargo timing from obscuring basic membership.

Capture each beacon/placed reference's observed runtime pointer, handle and FormID as distinct fields, object/base identity, location, `GetWorkshop` input/result and owner/resource-query outputs. Qualify event argument semantics before using them as a membership label. Record player position, loaded state, elapsed/game time, operation order and loaded modules. A query returning no reference is an observation, not proof of no membership. Capture before placement, after event settlement, before save and after reload; repeat on a second independently created outpost/storage pair.

Preferred instrumentation is a separately approved small SFSE observation probe calling only qualified query interfaces at explicit checkpoints, with a bounded debugger trace if return-path authority remains unresolved. Query invocation may affect caches and scheduling; log it as intervention. For a debugger alternative, cap the selected callback/one caller trace at 100 hits or 5 seconds, whichever comes first, with synchronous persisted records and a terminal completeness marker. No register/memory patches, exception suppression, arbitrary stepping, process termination or hidden retry. Deployment and ABI validation need their own brief.

Save comparisons: retain immutable A0/A0-control/A1/A1-control/A2/A2R originals with hashes and operator action log. Initial comparison may establish only byte/container differences; semantic save decoding requires separately reviewed methods. A no-action difference is the background-variation baseline. Do not search raw bytes for a pointer and call it a saved ID. Match restored objects using independent observed identity/placement information; any FormID-to-save mapping must be explicitly demonstrated.

Discriminating outcomes: a stable beacon relation after reload supports a persistent or reconstructed logical membership but does not distinguish the two. Query result changing while placement/location stays fixed favors an intermediate owner/cache model. Owner/resource query omissions would falsify their use as exhaustive enumeration. A restored relation with changed pointers demonstrates why runtime address identity is insufficient. Missing observations or a pre-flush crash fail capture completeness; retain them as failures.

**Crash-tolerant trace recommendation:** permitted as a narrowly bounded diagnostic fallback after ABI qualification, not the default for paired save/reload acquisition. A short trace may answer return-path questions before process exit; it is unsuitable for claiming A2R restoration if the crash prevents that checkpoint. Record completeness, scientific result and process outcome separately. Stop on source-save changes or unexpected corruption, preserve artifacts, and recover only using approved disposable copies. Review this plan and the reconnaissance before authorizing execution.
