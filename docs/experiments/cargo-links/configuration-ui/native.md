# C1 native, script and compiled UI contract

Reader notation: [vtable versus object offsets](../../../reference/notation.md#native-prose-at-first-use);
[experiment-local export namespaces and lookup](../../../reference/native-export-ids.md).
These guide the existing local address/offset declarations; they do not make
export labels global symbols or raw exports available in a checkout.

[Report](report.md), [Save52](save52.md), [function locators](functions.csv),
[pins](sources.csv). Retail 1.16.244.0 / image base 0x140000000. Native addresses
below are static-analysis VAs, not live pointers. Local `nNN` means
`.local-work/c1-cargo/native/NNN.request.tsv`; `dNN` means
`.local-work/recon/c1-cargo-NN.tsv`. Each FUNCTION section includes original name,
existing address/body, instructions and decompilation. Use instructions where
decompiler propagated pointer types or floating return types poorly. Aliases here
are analyst descriptions; none qualifies an invocation ABI or mod integration.

## Terminal, eligibility and pairing

Installed ESM ordinary PKIN 2191a0 contains marker REFR 21916c/base ACTI 2a6c3f,
incoming 219172/base CONT 219173 and outgoing 219170/base CONT 219171.
Two menu activators 218230/21916d use ACTI 2508aa; their XLKR key 2a6c3e
points to 21916c. Source `OutpostCargoLinkMenuScript.OnActivate` checks player,
resolves that marker, then requests ShowWorkshopTargetMenu with same-system=true,
same-system keyword=None, intersystem=RequiresFuel and the optional marker menu
keyword for the other-system branch. Fueled marker source/VMAD supplies its
separate fuel/compatibility configuration. These are installed development-source
facts; identical execution of shipped PEX is not claimed. Four source files were
byte-compared with installed ContentResources.zip, not copied into Git.

Native `1417216e0` (n003) resolves the source from the open-message handle and
calls `1417219c0`. The latter obtains the source's current target via the reserved-target
default-object key, source system and owning Workshop; it walks registered
Workshops at `145f0ba80` and supplemental references at `145f0ba98`.
Do not confuse the constructor object address with its value: registrations
`140126ce0/d60/da0/de0` (n008) create BGSDefaultObject objects; their value slot
is +48, as `1409e6c20` initializes (n009). Thus:

| Runtime default value slot | Installed DFOB -> actual keyword |
|---|---|
| 145ef9c00 | Target_DO 21c77d -> CargoLinkKeyword 255c9c |
| 145ef9c58 | ReservedTarget_DO 21c77c -> LinkActive 255cc8 |
| 145ef9cb0 | Incoming_DO 21c200 -> Incoming 2a6c46 |
| 145ef9d08 | Outgoing_DO 21c201 -> Outgoing 2a6c45 |
| 145ef9d60 | CargoShip_DO 21a7e4 -> LinkShip 255cc7 |

Candidates require current resolution, eligible Workshop (`140f386a0`), exclusion
of source owner, and the enabled same/different-system branch. Per-pad enumeration
`1417278b0` (n005) follows reverse linked references for the target keyword,
excludes the source, retains the current linked target or an endpoint not already
occupied under `1421a98b0`, and checks the supplied required keyword when present.
The supplemental branch also excludes disabled references and groups by location.
It retains the current peer. Therefore Available Outposts means available **to
this source/menu request**, including its current link; not every player outpost
and not evidence that all pads are unpaired. No independent same-type Boolean is
invented beyond the script request, actual required keyword and occupancy gates.

`141722e90` resolves grouped target handles, obtains reference names, sets
`bCurrentTarget` against current peer, and ORs that into outpost `bCurrentLink`.
Native append/iteration order feeds SWF list filtering; neither distance nor
alphabetical sorting is requested in the mapped menu constructor/InitializeEntries.
Runtime hash iteration precludes stable ordering from the save.

The compiled SWF's OnSelect opens a create/change confirmation only for a child
other than current target. OnPopupConfirmed sends WorkshopTargetMenu_TargetPicked
with that child's uHandle; removal sends 0. The picked sink `141724a00` stores
pending target +690 and requests data refresh. Close-message case 2 in
`1417216e0` applies only a changed selection: clear old pair on both references,
remove pairing keyword state and add reciprocal `140ba0d40` linked references
under LinkActive, then dispatch the Workshop change event. Selection is not
itself a transaction. Installed marker source forwards old/new targets to the
quest; ship creation can fail and cause ClearCargoLink. Success sets both marker
ship links and per-endpoint ship references. Endpoint01/02 are creation orientation,
not one-way permission: the source contract includes each end's incoming/outgoing
references. Freight movement and creation retries' timing are C2, not traced here.

## Resource providers and the decisive direct-edge boundary

`141723c80` (n003) clears TargetData +68 needs and +e0 outgoing arrays. Incoming
lookup uses `145ef9cb0`; outgoing uses `145ef9d08`. With an incoming ref it calls
`140f80af0` (n005). That helper scans destination-keyed local-link map 145916580,
tests each destination's **direct source entries** against the given incoming
reference handle, and appends matching destination handles. It does not recurse.
This is different from S2 transitive `140f82c30` storage selection.

Only resolved destinations satisfying `140f7cab0` or `140f7d030` enter
`140f7fd50`. Those are builder/recipe-consuming classes, not passive Warehouse
stores; native/definition class evidence follows S1/E3. The helper collects
currently selected/nonzero recipe ingredients plus available-input counts using
upstream supply lookup. UI emits each resulting resource identity/name/icon/
tracking row; it does not enumerate every construction recipe in the outpost.
The outer direct edge remains restrictive even though ingredient stock lookup
inside the recipe helper can traverse upstream sources. Needs are neither a
whole-network demand aggregate nor proof that a producer is currently eligible.

Outgoing rows come from outgoing reference +a0's inventory item list, protected
under its lock, invoking `141724330` for each inventory entry. If there is no
inventory object, `1417283e0` uses base-container content entries. This does not
read the incoming inventory, ship manifest, transport history or declared exports.
Names/tracking/resource icons are filled per form; rows are resource types rather
than a displayed quantity ledger. S1 inventory serialization remains separate.

`141724670` (n004) compares each needs form ID with the opposite end's outgoing
form IDs and vice versa, setting `bNeeded`. It does not erase unmatched resource
rows. Thus a lack of complementary stock does not itself explain an empty list.

## Exact UI binding and rendering

Native maps `141720ef0/f60/db0/e40/d40` (n001/n003) register:

| Provider / nested object | Fields |
|---|---|
| WorkshopTargetData | sLinkedOutpostName; fCargoShipWeight; fCargoShipMaxWeight; aOutposts |
| WorkshopTargetSourceData | SourceOutpost; SourceRef |
| OutpostData | sSystem; sPlanet; sName; fDistanceInLY; uHandle; bCurrentLink; aTargets |
| TargetData | sName; uHandle; bCurrentTarget; aResourcesNeeded; aOutgoingResources |
| ResourceData | sName; bNeeded; bTracking; resourceInfo |

Installed Interface.ba2 member `interface/workshoptargetmenu.swf` was extracted
locally and its own DoABC parsed without running ActionScript. Receipt
`menuabc03.json` retains 100 selected bodies, their ABC method IDs and bytecode
offsets; framing closes and no selected opcode stops remain. This is a bounded
symbolic inspection, not runtime execution or a general decompiler.

- Method 970 OnSourceDataUpdate: bytecode 64..102 passes SourceRef needs/outgoing
  into CurrentNeedList/CurrentOutgoingList.SetResources.
- Method 971 OnSelectionChange: 91..176 displays selected **child** arrays and
  sends TargetHovered with parent/child handles. 180..220 intentionally hides
  target lists and source comparison checkmarks for a selected parent.
- Method 579 SetResources: iterates provided rows up to MAX_RESOURCES=8 (method
  575); displays existing rows and hides unused clips. Overflow uses a continuation
  indicator. It does not require bNeeded=true. Method 531 sets name/icon/check/
  tracking from each row. Empty arrays therefore intentionally render no rows.
- Method 969 OnTargetDataUpdate: linked name drives footer/ship-meter visibility;
  bytecode 88..130 uses Math.round on current/max weight. It initializes parent
  entries and selects the existing linked child once (method 1027), otherwise first
  entry as appropriate. Method 1029 retains supplied order when expanding children.
- Method 516 builds name, planet + comma + system, formats LY with precision argument 1 (OutpostEntry trait int-pool[5]) and
  applies current-link flag. Method 515 chooses linked/unlinked and selected/
  unselected frames separately. Green arrows are link indicators, not activity.

Native `1417239e0` (n010) produces geography/name fields, using Workshop/location
fallbacks and system displacement `142334600`, norm and LY scale. Same-system
display 0 LY does not measure planet-to-planet distance.

## Refresh, caches and persistence

Opening builds candidates then queues `1417290f0 -> 1417227b0`: source metadata
and SourceRef resource arrays are populated once, then target refresh is requested
through `141722990`. Hover `141724af0 -> 141724be0 -> 141729010 -> 141724cd0`
updates source checkmarks against cached target data. The picked handler requests
`141722a70` via the UI service; it resolves pending target +690, updates linked name, weight,
and rebuilds target rows through `141722e90`, including `141723c80` resource calls.
Data locks and UIValue invalidation notify Flash; invalidation is not inventory
transport. Methods receive/queue work across service contexts, not an atomic live
snapshot of both ends.

The mapped constructor registers hover/pick events, not a cargo/container-change
sink. Exact xrefs to source/target population and menu-local existing functions
were inspected: no periodic resource repopulation or freight-event subscription
was found in that coverage. Consequently **ordinary source and target rows retain opening
contents during navigation; a confirmed pick can resample target stocks/weight**. This is a scoped
menu contract, not a universal claim that no script/mod could reopen/replace it.
Underlying inventory/ship events can change state without these arrays being
rebuilt. Screenshot-specific staleness was not observed. Reopening repopulates.

`141722a70` calls `140b69760` for current ship weight only when pending target == initial
current target and LinkShip resolves; otherwise writes 0. Max uses `14211b700`
on ship in that branch and source marker otherwise. Effective capacity is not a
hard-coded UI 300; marker source OnInit sets CarryWeight from default 300.
Ship/base/current overrides remain separate from the photographed rounded 300.

Pair/child/owner identities use counted Extra4C key/mode/target entries, with
`140562ef0` restoration and S1's writer contract. Mode distinguishes reconstruction
behavior, not transport direction. FormIDs are remapped and reverse links rebuilt;
save tokens are not runtime handles. Inventory writer/loader are S1
`1406447c0/1406448b0`; local graph writer/loader `140f7e6f0/140f7ea10` are n010.
UI arrays/selection/candidate handles are reconstructed/transient, not that graph.
The [field mapping](save52.md#field-by-field-correspondence) separates each layer.

Preserved gaps/nonmatches: d002 symbol scans capped at 256; later exact vtable/
xref/function-range queries supplied the relevant positive paths. n001 guessed
141725cc0, n007 140404d20 and n010 1409e6d90/1405630a0 are not function entries;
none is absence evidence. Large instruction listings may cap; full decompilation,
existing function bodies and targeted paths remain retained. No ship-flight,
unload/return or general mod-instance decoder was commissioned.
