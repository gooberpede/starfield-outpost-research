# Authoritative Locations -> Outpost informational inventory

[Answer](report.md), [exact paths](native-and-ui.md), [reuse](reuse-and-gaps.md).
Scope: both supplied 1920x1080 images. Native addresses are preferred static VAs
in the pinned 1.16.244.0 image, base 140000000; +offsets are hexadecimal object
offsets. `mNNN` is a decimal ABC method in the inherited SD3 LocationsPage
disassembly. `nNNN` is this task's native/NNN.request.tsv. Source hashes and export
limits are in [registers](sources.csv). No address below is a live/save address.

Refresh keys: **O** = entry collection 141360e80, queued delivery 14136ac90 ->
14136dc00 ->141361c10, then m1261/m1279; **S** = m1270 paints selected copied
entry; **B** = selection m1268 sends uBodyID ->14135e270 ->14135f0e0, then queued
141369b80 ->14136dc40 ->14135fcc0; **G** = entry-built galaxy markers,
141362bc0/1413630c0, selected system crosshair updated by m1268. These are
distinct epochs. O/S do not establish settled underlying state.

| Informational field / meaningful graphic | Source -> calculation or predicate | Native payload -> compiled consumer -> display | State / refresh | Coverage/provenance |
|---|---|---|---|---|
| Outpost list name | ExtraWorkshop+70 cached name from Workshop name/update machinery | 141360e80 -> row+0; 141361c10/14136c980 sName -> list InitializeEntries m1279, SystemBodyListEntry.SetEntryText m1005 | MIXED saved/current source, transient copy; O | Inherited SD3 + BM2 name producer; new exact compiled list edge |
| Selected detail name | Same entry sName; no distinct rename computation | m1270 byte 14..40 -> OutpostView.Title.Text_tf, SetText with outpostNameTruncateLength | O then S; no per-selection rename reread | TRACED; historical rename timing unknown |
| Planet subtitle | ExtraPlanetContent81+28 body ID if nonzero, else reference body-context 140910690; name lookup 1405e3fb0 | row+8 -> sBodyName -> m1270 byte 44..64 Subtitle.Text_tf | MIXED definition/context -> transient snapshot; O/S | TRACED ordinary source; exact metadata lookup described in native/UI |
| SYSTEM / DESIGNATION name | Entry uBodyID -> system-root 14231f860; localized name 1405e3fb0 | 1416cf8f0 ->1416b6310 sSystemName, LocationsBodyInfoData -> m1285 SystemName_tf | DEFINITION-DERIVED/context copy; B | TRACED; system ID is not a FormID |
| PLANET name | Selected body ID name 1405e3fb0, separately from entry subtitle snapshot | same body provider sBodyName -> m1285 PlanetName_tf | B | TRACED; subtitle and panel need not share epoch |
| OUTPOSTS BUILT numerator | Registry resolved rows, exclusion keyword absent, ACTI/Workshop keyword/ExtraBC required; no UI favorites filter in Outpost view | aOutpostListA ->m1261 ->m1279 null filter/InitializeEntries -> ListEntries.entryCount -> count text | RECONSTRUCTED collection; O | TRACED native screen population; exceptional registration/control and global saved completeness not asserted |
| OUTPOSTS BUILT denominator | Valid AV default 145f0c570 -> player AV owner base getter 141976dc0; truncating integer conversion; absent/wrong type default yields 0 | command aggregate+18 ->141361c10 -> iMaxOutposts ->m1261 MaxOutposts ->m1279 count + '/' + maximum | Base capability snapshot; O | TRACED; reused L1 ordinary base progression, distinct effective remaining getter |
| Cargo Links integer | Reuse BM2 active local endpoint predicate, summary ExtraBC+88 | row+18 -> iCargoLinks ->m1270 CargoLinks.text_tf | RECONSTRUCTED summary cache copied O/S; E1 request mask 4 | INHERITED computation, TRACED Locations adapter; no route/freight reinterpretation |
| Crew integer | Reuse BM2 CrewExtraData E2+18 handle-list count, zero without extra | row+1c -> iCrewCount ->m1270 Crew.text_tf | RECONSTRUCTED cache O/S; request mask 8 | INHERITED; no fresh actor resolution/capacity/presence test; robot membership follows assignment list |
| Needed Power | Reuse P1/E1 cached required lane ExtraBC+80 | row+14 -> iPowerRequired ->m1270 NeededPower.text_tf | RECONSTRUCTED cache O/S; request mask 1 | INHERITED computation; direct SetText, no new power calculation |
| Total Power | Reuse P1/E1 cached generated lane ExtraBC+7c | row+10 -> iPowerGenerated ->m1270 TotalPower.text_tf | Same as required power | INHERITED; display integer, no per-selection graph traversal |
| Production and /MIN | Reuse E1/BM2 nominal registered eligible producer sum ExtraBC+84 | row+20 -> fProductionPerMin ->m1270 RoundDecimalToFixedString(value,2) + '/MIN' | RECONSTRUCTED cache O/S; request mask 2 | INHERITED arithmetic/rounding; not realized throughput |
| Build Limit bar | Reuse L2 usage/allowance ratio ExtraBC+90, zero-denominator handling | row+24 -> fBuildLimit ->m1270 byte 164..196 Math.round(framesLoaded*ratio), gotoAndStop | RECONSTRUCTED cache O/S; request mask 10 | NEW Locations binding: sprite 149 has 100 frames. No clamp in handler; L2 scalar model retained |
| Stored resource name | Reuse SD3 eligible inventories, shared substitution/dedup and IRES grouping/sorting | aResourceListA ->m1271 ->m1288 sResourceName | Collected O, repainted S | INHERITED SD3; no new census |
| Stored resource quantity | Reuse SD3 unit aggregation and same-index sorted counts | aResourceListCountA ->m1271 ->m1288 count.toString() | O/S, no selected-item inventory request | INHERITED; no weight conversion or freshness guarantee |
| Resource icon, background, symbol, rarity marks | Reuse SD3 IRES inorganic symbol/color; named organic GNAM asset selector | ResourceEntry ->m1288, imported PlanetInfoCard ResourceIcon and OrganicIcons classes | Definition-derived icon metadata in O/S | INHERITED [SD3 icons](../stored-resources/icons.md); ordinary mapped variants only |
| Faction name / NONE | System location owner walk 140aba950; prefer +d8 then+a0; require FACT 0d; FACT full name virtual+60; missing => $NONE | 14135d890 -> sFactionName ->m1285 FactionName.Text_tf | MIXED definitions/effective owner pointers; B | NEW bounded causal selection; no outpost ownership/jurisdiction equivalence |
| Faction emblem | FACT+158 faction-type keyword ->14172bc70 fixed DFOB keyword matches or extension array; absent=>-1 | iFactionType ->m190 GetFactionIconLabel ->m1285 FactionIcon.gotoAndStop(label) | B; installed art in LocationsPage | NEW: seven actual frame labels; helper has more labels, so unsupported enum rendering remains unknown |
| LEVEL number | System location via 140786690's parent+c0 or140910af0 fallback; byte+a9, default 0 | uSystemMinLevel ->m1285 LevelState.UseNum.UseNum_tf SetText | DEFINITION-DERIVED/effective location snapshot; B | NEW: LCTN DATA byte 5; Narion 1, Schrodinger 65 physical controls, no player-level formula |
| LEVEL color block | Level compared against configured 11/21/31/51 defaults ->challenge 0..4 | uSystemChallengeLevel ->m1286 timeline labels Level 1-10/11-20/21-30/31-50/51-75 | B; effective settings may override defaults | NEW; top label does not prove a maximum level 75 |
| Upper starfield / dots | Component system-position data ->1413630c0 projection, clamp and rectangle mapping | LocationsMap2DMarkerData.aMarker2DDataA with uBodyID/fCoordsX/Y ->m1263/m1173 marker instances | TRANSIENT, entry-built G | NEW generated marker map, no per-outpost starfield texture selection |
| Upper crosshairs | Selected entry uSystemID matched against marker uBodyID | m1268 SetHoveredSystem ->m1175/m1171 places lines at matched marker | G plus selection | NEW selected-system marker, not beacon latitude/longitude; UI hides player-ship icon here |
| Orbital/system diagram | Root/body name/IDs, child hierarchy, component color, radius/size metadata, scan state ->StarMap::SystemInfoToUI | LocationsSystemBodyInfoData ->m1264 ->m859/m726 nested SystemView/PlanetView/MoonView and Body_mc | Definition/reconstructed hierarchy plus effective scan; B rebuilds on root-ID change; same-root update selects highlight | NEW schematic asset/data mapping; internal tween/drawing and exact pixel equivalence excluded |
| Selected-body marker/highlight | focusedBodyID carries selected body ID; recursive bodyID equality | m1264 SetBodyHighlight ->m862/m741/m742 ->m586 Highlight rollOver/off | B; symbol 16 visited/unvisited, highlight 14 | NEW ID-selected schematic symbol. No separate photographic planet image in mapped visible Overview panel |
| Caption text and metric pictograms | Installed localized UI captions and fixed timeline art | m1257 sets $CARGO LINKS/$CREW/$NEEDED POWER/$TOTAL POWER/$PRODUCTION; Overview/Outpost timeline captions BUILD LIMIT/STORED RESOURCES/SYSTEM/DESIGNATION/LEVEL/PLANET/FACTION and Count OUTPOSTS BUILT | Definition/static art, initialized with view | TRACED caption/instance provenance; no dynamic cargo/crew/power state encoded by the fixed pictograms. Translation/rendering outside supplied English witnesses not generalized |

LOCATIONS and OUTPOST identify the active view. Other tabs, category arrows,
selection-row decoration, CLOSE, sort/distance, stored-resource paging and key
hints are navigation/control context, explicitly excluded by the brief. Survey,
POI, favorite and body-card fields hidden in this Outpost overview are not added
as visible fields. No arbitrary Database/Almanac Workshop or Build Mode field is
silently substituted for a Locations binding.
