# What Game.GetPlayer().GetCurrentLocation() returns

2026-10-20. SOR-EV-0066. [Source pins](sources.csv), [methods and primary locators](evidence.md).

**It returns a Papyrus `Location` object (native BGSLocation / LCTN), with no longitude or latitude.** `Game.GetPlayer()` returns the player Actor; Actor inherits ObjectReference, whose native `GetCurrentLocation()` supplies the Location. It does not return a numeric coordinate, cell, worldspace, reference handle or the player's Actor reference.

Exact installed source signatures: `Actor Function GetPlayer() native global` in Game.psc; `Location Function GetCurrentLocation() native` in ObjectReference.psc. Actor.psc declares `Actor extends ObjectReference`; Location.psc declares `Location extends Form`. Source archive member hashes are recorded separately from the archive hash; no proprietary script text is copied into the authored package.

## Registration and dispatch

All addresses here are static VAs in executable SHA256 `7e9adb1414a8e1b325e5e1f097b9b17b78deb7eebeda37a333351a43a60f9d28`, image base `140000000`. Native member offsets are hexadecimal; they are not save offsets.

| Link | Primary evidence / exact behavior |
|---|---|
| Game registration | `142010740`, window `1420118be..1420118e4`: name GetPlayer, callback `14177a1f0`, constructor `1420188d0`, VM registration virtual+f0. Constructor uses `NativeFunction0<StaticFunctionTag,Actor*>`; result type registration uses form category 0x4b. |
| Player getter | `14177a1f0`: returns global player singleton `145f43230`. This is a native Actor pointer internally, wrapped as the Papyrus Actor return. |
| Inherited location registration | `142085050`, window `142086ccd..142086cfa`: ObjectReference class, GetCurrentLocation name, callback `14208b8f0`, constructor `14209ec60`. Constructor uses `NativeFunction0<TESObjectREFR,BGSLocation*>`, result type category 0x75. |
| Callback | Existing instruction thunk at `14208b8f0` moves receiver R8 to RCX and tail-jumps `140b4e650`. No new Ghidra function was created to label the thunk. |
| Player-specific lookup | `140b4e682..140b4e69a` tests reference FormID 0x14 and selects player singleton+f38. The decompiled complete body confirms this shortcut. No coordinate projection occurs in this player branch. |

Sources and native registration independently agree about return category. Papyrus exposes an object identity, not the raw native pointer. A Location can have a name, parent links, keywords and a planet association; none of those makes its optional name a geographic coordinate.

## General reference lookup and priority

The complete `140b4e650` body has further branches for non-player references. With a parent cell, `1421190b0` can resolve a containing reference's cell/world location first, then `140af4c50` obtains the cell's own ExtraLocation or selects a world/cell association. `140af4c50` first consults ExtraLocation via `14051b2b0`; on the eligible exterior branch it can select an overlay through `140ad3240`, prefer that world's+2b0 location and otherwise use the world's+2b0 value. Interior/flag branches differ. With no parent cell, `140b4eb40/140bc17b0` can perform world/position lookup, or ExtraLocation supplies the fallback. `14051b2b0` returns ExtraLocation type 0x81 field+38, not its separate angular fields.

Special containment/space-reference branches use `140b58d50/142116840` and component lookup; the final null-result path can consult `140911600` or enumerate a component association. These are genuine priority/loaded-context exceptions, not proof that all objects return their cell's immediate location. The inspected getter does **not** simply walk every LCTN parent and return a planet. Player cache population and its event/update ordering are not fully traced here; the narrow next trace for an exact player return is writers of player+f38 and the corresponding cached/saved Location identity.

Location.psc separately exposes `Planet Function GetCurrentPlanet() native`, `Location[] Function GetParentLocations(Keyword apKeyword = None) native`, and `bool Function IsChild(Location akOther) native`. Thus parent traversal is a distinct query; the plural API and keyword filter preclude assuming one universal linear parent chain. Their complete native implementations are not claimed in this bounded GetCurrentLocation trace. A known returned Location can help classify a named POI or join to a planet through those relationships, but its precision and association depend on the returned object and content. It does not directly identify a terrain cell or guarantee a biome/outpost-site identity.

## Supported fixture contrasts

| Fixture | Supported evidence | Actual GetCurrentLocation result |
|---|---|---|
| Lab / Save37 | Player parent resolves to installed exterior WRLD 00325868; its XLCN is LCTN 00028A08, with parent 0001B1D4 | **NOT MEASURED.** World XLCN is a definition association; the player getter selects cached+f38. |
| Save38 preconstruction | Player parent is generated source world 81482d; Kreet descriptor is present; no detected ordinary beacon | **NOT MEASURED.** No name or assumed biome is substituted. |
| Save39 new outpost | Player and beacon share site parent 839160; typed world/body/Workshop joins are positive | **NOT MEASURED.** Creating a site does not prove cache retargeting or that the return is a newly named outpost Location. |

This answers the API's type and static selection behavior without invoking Papyrus, compiling/deploying a plugin, or pretending save parent identity is the live return. No new biome identification is claimed. The useful shared prerequisite for later POI/biome work is an identity-qualified Location return plus its definition/parent/planet joins, separate from the geographic grid address.
