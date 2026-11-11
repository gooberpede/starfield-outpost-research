# Outpost identity and the source-to-row contract

Reader notation: [vtable versus object offsets](../../reference/notation.md#native-prose-at-first-use);
[experiment-local export namespaces and lookup](../../reference/native-export-ids.md).
These guide the existing local address/offset declarations; they do not make
export labels global symbols or raw exports available in a checkout.

[Answer](report.md), [methods](methods.md). `nNNN` refers to the exact local
`native/NNN.request.tsv` export under `.local-work/sd3-stored/`.
Addresses are preferred static hexadecimal VAs at image base `140000000`;
object offsets are hexadecimal. These are not runtime addresses or saved IDs.

## Actual provider and a discriminating control

LocationsPage ABC method 1243 names **OutpostStaticData**; method 1257 subscribes
onOutpostDataUpdate. Native `14135dcb0` registers that provider at Locations
state+`a48` (n020), with `141364550/1413644b0` binding **iMaxOutposts** and
**aOutpostListA** (n023/n027). The state owns its provider and unregisters it on
destruction (`14135df40`, n019). The UI does not obtain these rows from a script
named Stored Resources or from a caption lookup.

**Non-provider control:** `141382c00` registers **AlmanacWorkshopStaticData** and
**AlmanacWorkshopDetailsData** for the separate Workshop tab (n003). Its recipe
and tracking functions were reconnaissance controls, not SD3 inventory evidence.
Likewise SD2's bench provider `1417f6fa0` does not feed these fields.

## Enumeration before selection

State entry **14135e120 -> 141360e80** (n019/n012) traverses global Workshop
handles at `145f0ba80`, count `145f0ba78`. Each handle is resolved through the
reference service. It skips a positive **140f3bfc0** exclusion query, requires a
base ACTI (`1e`), the **14047fce0 / 145f0b380** Workshop keyword predicate, and
ExtraWorkshop (`bc`). Missing/unresolvable/failed contexts contribute no entry in
that invocation. ExtraBC summary/name and body context supply the accompanying
outpost fields; the summary-refresh request/pump is separate from inventory sums.

The exclusion uses reference+68 virtual+8 and global **145f0c6d0**, not a proven
BlockPlayerActivation equivalence (n015). Its resolved FormID remains unresolved.
This preserves [earlier membership limits](../active-outpost-membership-completion.md)
and the [earlier exact provider lead](../active-outpost-identification.md#independent-native-membership-route-and-exact-obstruction).
An enabled ordinary saved beacon does not by itself prove registry membership,
player ownership or inclusion in a historical UI invocation.

For each qualifying Workshop, `141360e80` walks reverse ExtraLinkedRefChildren
(`4d`) entries keyed by **WorkshopItem / 145f0b3d8**. It calls **141368cf0** for
each matching handle (n014). The callback resolves a reference, obtains its
TESContainer capability through `140b24ca0`, requires effective AV global
`145f0a978` nonzero, substitutes a recognized shared reference, then deduplicates
by reference pointer. [Membership](membership.md) records the consequences.

## Source inventories to selected row

For each retained source, `141360e80` locks inventory access at reference+a8.
With an initialized inventory at +a0 it calls **14136be50**; otherwise
**14136c060 -> 141361ad0** visits the base-container entries through the generic
inventory machinery (n014/n016). [Aggregation](aggregation.md) maps both routes.
The report must not mistake the no-initialized-inventory branch for empty stock.

The temporary outpost aggregate contains its resource map at +38.
**14136ac90 -> queued 14136dc00 -> 141361c10** sends an owned aggregate to the UI
service (n019/n017/n012). The receiver rebuilds OutpostEntry objects, converts
each resource map to ResourceEntry, inserts resources by name with
**14136a980**, and inserts the corresponding count at the returned index with
**141369750**. Sorting therefore preserves resource/count alignment.

**14136c980** binds each OutpostEntry: sName, sBodyName, iPowerGenerated,
iPowerRequired, iCargoLinks, iCrewCount, fProductionPerMin, fBuildLimit,
uFormID, uBodyID, uSystemID, **aResourceListA**, **aResourceListCountA** (n006).
`uFormID` comes from the Workshop reference's form identity, not its process
pointer or registry handle. No new durable cross-session identity is inferred.

ABC 1261 retains aOutpostListA. Selection handler **1270** reads the actual
EntryObject and calls **1271 SetStoredResources** with it. The latter pairs
the arrays at the same index and passes the resource plus count to **1288**.
1288 writes `count.toString()` and `sResourceName`, then chooses the icon.
There is no native inventory request in this selection handler. Navigation,
paging controls, animations and layout were not interpreted as research subjects.
