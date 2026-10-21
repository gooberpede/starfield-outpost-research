# Newly traced Locations edges and decisive locators

Reader notation: [vtable versus object offsets](../../audits/publication-readiness-b2/notation.md#native-prose-at-first-use);
[experiment-local export namespaces and lookup](../../audits/publication-readiness-b2/native-export-ids.md).
These guide the existing local address/offset declarations; they do not make
export labels global symbols or raw exports available in a checkout.

[Inventory](field-lineage.md), [methods/pins](methods.md). `nNNN` means local
`.local-work/lo1-locations/native/NNN.request.tsv`; `mNNN` means inherited
`.local-work/sd3-stored/02.json` ABC method number. VAs use preferred image
base 140000000, retail 1.16.244.0; object offsets are hexadecimal. Local raw exports
are not publication candidates. [functions.csv](functions.csv) records export
coverage, including incomplete instructions and failed entry guesses.

## Snapshot, numerator and maximum

SD3's provider distinctions are retained: **OutpostStaticData** is registered by
14135dcb0 at state+a48; LocationsBodyInfoData at+170, SystemBodyInfoData at+830
and Map2DMarkerData at+b38 (n002). AlmanacWorkshopStaticData is a different tab.
Entry 14135e120 first collects general body data, then 141360e80 outpost rows,
and builds galaxy markers if their stored context is absent (n001).

**141360e80** enumerates the handle registry 145f0ba80/count 145f0ba78. It resolves
each, rejects positive 140f3bfc0, requires ACTI 1e, Workshop keyword and ExtraBC,
then appends one 72-byte outpost aggregate. It requests summary refresh type 5 and
pumps 1421ba960 before copying lanes; that is not a guarantee that all pending
requests or inventories have settled. Existing SD3 inventory collection remains
the authority for resource rows. Missing/unresolvable/invalid references do not
produce a row in that invocation. There is no independent saved-beacon scan,
explicit ownership test or route/crew predicate in this row-admission branch.

**New exclusion identity:**140f3bfc0 queries the reference's keyword interface
at+68 virtual+8 using 145f0c6d0 (n012). Constructor 1401595f0 constructs default
object 145f0c688, value slot+48, with string 144c266e0
**WorkshopUseDecorateTextKeyword_DO** (n022/n023; pe-selected01).
Installed DFOB 003e4f4a DATA ->KYWD 003e4f4b physically confirms the identity
(controls02). It is not an inferred BlockPlayerActivation test. Exclusion is
conditional on that resolved default being a KYWD; exceptional/global registry
completeness and player control remain outside this native screen rule.

After enumeration,141360e80 initializes maximum 0. For a valid AVIF at 145f0c570
it calls **141976dc0(player 145f43230+70, AV)**, then truncates returned float to
integer. This is the base-value path with cache at AV-owner+1f0 (n003/n016/n027),
not 1419776f0, which composes base and modifiers for the effective getter.
L1's accepted [allowance](../limits/native.md#deployment-allowance-and-ordinary-beacon-operation)
maps DFOB 002a84f6 ->AVIF 002a84f7 and ordinary player base 8, rank stages setting
12/16/20/24; placement/removal use modifier 2 -1/+1. Thus an ordinary charged
deployment changes remaining allowance without subtracting from this displayed
maximum. Missing/wrong-type default gives 0; no clamp against numerator is shown.
Arbitrary fractional/nonfinite or modded states are not promised ordinary counts.

141363960/14136ac90 queue the vector and maximum. Receiver 141361c10 rebuilds
entries and transfers aggregate+18 to iMaxOutposts;141364550 binds it alongside
aOutpostListA (n001). **m1261** retains both. **m1279** explicitly clears the
list filter, initializes OutpostEntriesDataA, and writes
`ListEntries.entryCount + '/' + MaxOutposts` (bytes 48..77). Zero entries also hide
the detail/overview panels. This closes the native-to-displayed numerator rule,
without claiming an exhaustive general active-player-outpost importer.

## Common cache, names and residual meter

The inherited [BM2](../build-catalogue/ui.md#footer-gaps-investigated) endpoint
and assignment-length predicates were already independently accepted before LO1.
They are reused. Cargo mask 4's reverse WorkshopItem members require target and
active-link keywords and exclude disabled bit 20; Crew mask 8 reads CrewExtraData
E2+18 count, zero without E2. It does not resolve individual living/arrived
actors. [R1](../robots/lifecycle.md) shares E2 insertion for zero-human-slot-cost
robots: a handle-list count is not a weighted human-slot or Crew Station measure.
New Locations evidence is the **adapter**, not rediscovery of those computations.

141360e80 copies ExtraBC+7c..93 into row power+10/+14, cargo+18, crew+1c,
production+20 and budget+24; ExtraBC+70 supplies name. Receiver 141361c10 and
binder 14136c980 deliver sName/sBodyName/iPowerGenerated/iPowerRequired/
iCargoLinks/iCrewCount/fProductionPerMin/fBuildLimit/uFormID/uBodyID/uSystemID
(n001/n027, inherited SD3). **m1270** assigns title/subtitle and four integers
directly with SetText. Production's existing RoundDecimalToFixedString(value,2)
then `/MIN` is reused from [E1](../inorganic-extractors/arithmetic-ui.md).

The **Locations** budget consumer m1270 bytes 164..196 requests
`gotoAndStop(Math.round(BuildLimitMeter_mc.framesLoaded * entry.fBuildLimit))`.
Named placement at uncompressed SWF byte 16604 points from outpost sprite 152 to
meter sprite 149, definition byte 14089, **100 frames** (assets01). The same
ratio-to-frame algorithm is present here independently of L2's footer binding.
No clamp occurs in this handler; engine behavior for out-of-range requests is
not newly qualified. [L2](../build-budget/ui.md) controls underlying accounting.

Name display is two copied sName consumers: list m1005 and detail m1270.
The [BM2 name producer](../build-catalogue/ui.md) updates cached ExtraWorkshop
name in the ordinary Workshop-info path. This is the known update source;
Locations entry collection copies it, selection only repaints. No independent
rename notification/recollection guarantee is demonstrated for an already open
Locations snapshot.

Entry body ID prefers ExtraPlanetContent81+28 if nonzero; otherwise 140910690
obtains the reference's body context. **1405e3fb0 ->1405e40a0** resolves its name
from the current component database, using type key 145fdce50 via 140461f10 and
localized-name virtual+60; missing component/name yields the empty-string path
(n001/n003/n005/n014). Assembly 1405e40e6..4107 fixes the argument order which
the decompiler obscures. This is a localized metadata lookup, not sName parsing
or an assumption that the moon's parent must be displayed. Selected examples
PNDT 0003f59f FULL 0000a898 and PNDT 0005e0b5 FULL 0000a4a0 resolve Kreet and
Schrodinger II in the installed English string member. Component-store winning
overrides are not reconstructed from those physical source records alone.

## Selected body/system metadata, faction and level

**m1268** takes EntryObject.uSystemID to the galaxy hover marker, dispatches
Almanac_Locations_ChangeSelection with **uBodyID**, then paints outpost metrics.
Native **14135e270** decodes that ID and calls or queues **14135f0e0** (n006).
The latter builds selected body data using 1416cd320/1416cf0f0/1416cf8f0.
**14231f860** validates/resolves the containing root body from component-store
relationships (n009); it is a logical body/system ID, not a runtime pointer.
1416cf8f0 obtains names for selected body, root and optional parent through
1405e3fb0, populating body-name+28/system-name+48 in its temporary body model
(n007). Receiver 1416b6310 plus 14135d570 binds **sBodyName/sSystemName**;
**m1285** sends those to PlanetName_tf/SystemName_tf. STDT 0005e630 FULL 0000a9b2
and STDT 0005e5e8 FULL 0000a9ea supply installed Narion/Schrodinger name controls.
No comma-caption algorithm is needed in these separate fields.

In **14135f0e0**, the resolved system-root ID selects location with
**140786690** and then that object's parent+c0; if absent, **140910af0** supplies
the fallback location (n004/n005/n027). Both helpers resolve component-held form
IDs, then require runtime form type 75, BGSLocation; n026 exposes their distinct
component type keys 1461e1d88/1461dd80c. This is a current metadata/context lookup.
The full population/override construction of those maps is not a new LO1 claim.

**14135d890** starts with `$NONE` and type-1. For a location it calls
**140aba950**, which selects the first available owner context by +d8 or+a0,
otherwise climbs parent+c0 subject to its three keyword guards
145eacec8/145e8fb68/145e8fb10. If a guard stops inheritance or the chain has no
owner, it returns 0. In the returned context, **+d8 takes precedence over+a0**;
the selected owner must be FACT 0d. A non-FACT preferred pointer does not retry
the lower-priority owner in this helper. Its full-name virtual+60 supplies
sFactionName; FACT+158 supplies the **faction-type keyword** to14172bc70
(n005/n006). Owner-override writer/lifetime and all inheritance-guard identities
remain outside the established lineage; no universal jurisdiction rule follows.

The FACT definition owner at location+a0 comes from LCTN **DATA first u32**:
140ab8030 DATA case calls 140aab770 at+a0; that decoder places the following
four bytes at+a8..ab. Link fixup 140ab9f80 calls 1402b9480 for+a0 (n012/n016/n026).
Physical system-location controls are:

| LCTN / physical ESM byte | DATA / context | Selected result supported by definitions |
|---|---|---|
| 000615b0 SNarion /1293511210 | e53806000001000a; XNAM 00015907 | owner FACT 000638e5 CrimeFactionFreestar, level byte 5=1 |
| 00061547 SSchrodinger /1293495177 | 00000000004100ff; XNAM 0001575e | definition owner 0, level byte 5=65 |

The FACT 000638e5 localized FULL 00006d04 is **Freestar Collective**. Its faction
type is KYWD 000546df FactionTypeFreestarCollective, distinct from the FACT itself.
DFOB 00137e5c FactionFreestar_DO points to that keyword. Constructor 1401366a0
binds the default at 145eff100/value 145eff148 (n025/n027; direct string pin);
14172bc70's fixed keyword comparisons return enum 4 for it. A configured extension
array provides additional type indices; unresolved type isffff, null type-1.
This does not guarantee matching art for all extension indices.

Level takes **location+a9**, default 0 without location, into
uSystemMinLevel; comparison with 145e85bf8/5c18/5c38/5c58 produces challenge 0..4
(n004/n027). Constructors 1400255c0/5f0/620/650 set **11/21/31/51** for
iLevelChallengeThresholdEasy/Average/Challenging/Deadly:StarMap. Setter 1402d66a0
stores the setting's value at+8 (n022/n023, pe-selected01). Effective settings
can differ from compiled defaults. The Locations body binder is 141364930;
queued 141369b80 ->14136dc40 ->**14135fcc0** copies faction/level and body data.
**m1285** displays the unsigned level; **m1286** maps challenge 0..4 to timeline
labels Level 1-10, Level 11-20, Level 21-30, Level 31-50, Level 51-75. The last
label is an art selector, not evidence of a75 cap. No subtraction of player level
occurs in this Locations classification.

## Asset/data selection and technical boundary

**Faction:**m1285 passes iFactionType to shared **m190 GetFactionIconLabel**,
then gotoAndStop on FactionIcon_mc. Enum 4 selects **FreestarCollective**;
type-1 selects **None**. Locations sprite 154 (definition SWF byte 16924,
placed at 22101) has exactly seven labels: BlackFleet, FreestarCollective,
HouseVaruun, RyujinIndustries, UnitedColonies, Constellation, None (assets01).
The shared helper can also return TrackersAlliance/TerranArmada/Creations,
which are **not labels on that clip**. No fallback/render behavior for those
requests is claimed. Even a missing owner selects explicit None art; a recognized
FACT's text comes from the FACT name, not m191's generic faction-name table.

**Upper map:**141362bc0 obtains the display rectangle/context and calls
**1413630c0** (n007/n008). This enumerates system-component positions, projects
them with 142be45c0, clamps normalized coordinates and maps into the rectangle,
inverting vertical position. It produces 12-byte `{ID,X,Y}` rows; queued delivery
binds **LocationsMap2DMarkerData.aMarker2DDataA** (141364300), entry binder
**14136cf60** supplies uBodyID/fCoordsX/fCoordsY (n021).
**m1263 ->m1173 SetMapMarkers** applies those coordinates to marker instances.
**m1268/m1175/m1171** match selected entry uSystemID to marker uBodyID and place
the crosshairs there. The Locations adapter hides the map header and ship icon.
No per-outpost starfield bitmap, geographic beacon coordinate or planet terrain
texture is selected in this mapped overview path. Projection internals are a
renderer boundary, not a new geographic coordinate specification.

**System diagram/body symbol:**1416aac10/1416aacd0 derives the system-root
model, focused body, names and child hierarchy. It walks component relationships
and sorts child rows; **1416aa920** supplies body type, scan bit, color via
1416ceb20 (star component or planet type 23 color+48), and normalized display
size via 1416ceb90/142333270 (component type 1461dd7a4 field+0c; missing fallback 0).
1416d1c50 accumulates per-type size ranges; the display size path normalizes
against the parent, remaps through type-specific ranges/settings and clamps.
These are schematic sizes, not plotted orbital distance or a promise of physical
scale. Root display size is set to1.0. Relevant paths are n007–n010/n014/n018.

**14135fcc0 ->1416ab670** replaces LocationsSystemBodyInfoData;1416aab70 binds
focusedBodyID/focusedCelestialBodyID/name, systemName and childInfoA, with
1416aa880's bodyID/parentCelestialBodyID/bodyType/color/sunRadiusPercent/scanned
(n017/n021). **m1264** rebuilds the system view when root ID changes, focuses
the whole-system view and applies focusedBodyID highlight. **m859 ->m726**
creates nested SystemView/PlanetView/MoonView objects using childInfoA, clamped
size, scan state and color. **m741/m742** recursively match bodyID and request
highlight; **m586** selects rollOver/off on Highlight_mc.
Locations body art uses **sprite 16**, labels unvisited/visited, with highlight
**sprite 14**, labels off/rollOver (assets01). **m1247/m1248** bind the Overview
SystemView_mc and Galaxy2DMap_mc; these are the supplied panel's informational
schematics. The generic BodyInfoCard receives metadata too, but its hidden
survey/body-card fields are outside this visible Outpost inventory. No independent
terrain/photo preview needs to be invented from the phrase 'planet image'.

Internal drawing, tweening, art shapes and arbitrary scale variants are excluded.
Component metadata selectors are traced without certifying every override,
compiled fallback for malformed records or the screenshot's exact rendered art.

## Refresh boundaries

1. **Source updates:** inherited E1 masks/coalescing/pump update the common
   summary; inventory/name/assignment/owner/scan changes have independent sources.
2. **Outpost snapshot:** entry collection requests/pumps status and collects
   inventories, then queues replacement provider arrays. m1261/m1279 rebuild list.
3. **Selected metrics:** m1270 copies selected entry fields and resources only.
4. **Selected metadata:** m1268 sends bodyID;14135e270 calls or queues 14135f0e0;
   body and system providers are replaced, m1285/m1264 paint them. This is a
   demonstrable per-selection refresh that is distinct from inventory recollection.
5. **Other events:** inherited SD3 UI-service callback 14135e350 rebuilds general
   body data 14135eb10, not the outpost collector. Favorites have a separate flag
   update. No continuously maintained Locations metrics/inventory snapshot or
   synchronous cross-provider epoch is established. External re-entry remains
   possible; there was no live timing experiment.
