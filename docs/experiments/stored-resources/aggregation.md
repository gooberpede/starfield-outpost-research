# Resource identities, counts and freshness

Reader notation: [vtable versus object offsets](../../reference/notation.md#native-prose-at-first-use);
[experiment-local export namespaces and lookup](../../reference/native-export-ids.md).
These guide the existing local address/offset declarations; they do not make
export labels global symbols or raw exports available in a checkout.

[Provider](provider.md), [saved cases](saves.md), [icons](icons.md), [methods](methods.md).
Confidence is STRONG STATIC for the mapped ordinary pipeline; no loaded output
or historical UI total was measured.

## Item admission and grouping

Initialized inventory visitor **14136be50** (n014) admits a MISC (`28`) associated
through its component data at +238 with **exactly one entry** whose form is IRES
(`9f`). An IRES input takes its physical item through +108 then +88 before the
same check. **141350b10** and default visitor **141361ad0** implement the matching
association (n017/n016). This is a resource association, not a generic
ResourceType keyword search or arbitrary crafting decomposition.

For each admitted item, the visitor sums the 32-bit counts at stack entry+8,
stride 10, then calls **141351790** to construct resource metadata with that
quantity. **14136bbb0** inserts into a map keyed by the associated **IRES FormID**
at node+1c. A new node retains the quantity; an existing node adds it at +2c.
The visitor does not multiply units by the CVPA component amount, item weight,
production interval, rarity, available-to-craft amount or container capacity.
It does not subtract quest/tracked/stolen stock by a separate predicate here.

Installed `0055b1` Adhesive, `260db6` Adhesive Stalk and `260db7` Adhesive Seed
have the same sole CVPA resource `077828`. They can therefore merge into one
Adhesive row despite different physical item identities, names and masses.
Iron `00556e -> 0057c7` and Adaptive Frame `246b6a -> 245775` are different joins.
The native rule requires one component entry; a missing/multiple-entry or
non-IRES association is excluded by the mapped item path. Weapons/equipment do
not become resource stock merely because crafting can consume/decompose them.

Extra-data differences do not produce separate resource keys. The collector reads
stack quantities and resource association, not theft/modification ownership flags
as a reporting filter. This is not a claim that every exceptional modified form
or virtual inventory can reach the visitor; [save decoding limits](saves.md)
remain explicit. Mounted display references are not independently swept.

The initialized-inventory visitor has no positive-count guard before insertion, no generic
zero-row suppression and no saturating arithmetic. Zero stacks can produce zero
metadata; signed/negative internal sums cross into unsigned UI count storage.
The ordinary supported interpretation is positive resource units. Overflow,
negative/corrupt inventory and realized rendering of abnormal values are untested;
do not promise a nonnegative clamp that the inspected path does not implement.

## Default stock, ordering and names

`141360e80` chooses initialized source inventory when present, otherwise
**14136c060** obtains base-container entries and invokes **141361ad0** using the
ordinary inventory-entry machinery. At static VAs **14136c111–14136c12c**
(n014), the default path reads the base-entry count and prepares **1 for a zero
count**, preserving nonzero count bits, before passing it to **14063e4e0**.
This preparation is distinct from summing already initialized zero stack counts:
the latter visitor does not apply this zero-to-one substitution. The prepared
argument is not a measured displayed default quantity; the generic constructor's
full default/leveled/instance realization is not reconstructed in SD3.
It does not independently add default CNTO
again to an initialized list. Serialized inventory changes alone must not be
mistaken for a complete effective inventory. Many industrial definitions contain
default marker entries; [SD1 construction clearing](../containers-displays/native.md)
and item association remain separate from saved added resource stacks.

**141361c10** builds ResourceEntry fields from each resource-map node.
**14136a980** uses bytewise string ordering on resource-name data to insert the
resource; **141369750** inserts the count at that same position (n020/n028).
The order is based on the resolved resource label, not container order, quantity
or physical variant name. Equal-name tie ordering is not a promised stable API.
The native resource metadata uses the IRES full-name interface; localized string
resolution is retained. English examples are freshly resolved in localization01.
ABC **1288** writes count.toString and sResourceName without weight conversion.

## Three separate freshness boundaries

1. **Inventory changes:** producers, local redistribution, freight and player
   actions have their own eligibility, timing and mutation paths. S2's remote
   operation does not imply an immediate Locations repaint; C3 does not replay
   cargo voyages during a wait.
2. **Aggregate collection:** Locations entry **14135e120 -> 141360e80** resolves
   the registry and collects member inventories into temporary per-outpost maps.
   Source locks protect individual reads; no global multi-inventory atomic
   snapshot is demonstrated. The subsequent command owns a copy for UI delivery.
3. **Provider/repaint:** **14136ac90 -> 14136dc00 -> 141361c10** replaces the
   provider arrays asynchronously. ABC 1261 accepts them; 1270/1271/1288 paints
   the selected entry. Selection does not itself re-enumerate inventory.

The mapped Locations state subscribes to ChangeSelection, FavoriteSelection,
OutpostSelected and the UI-service event (n019/n021/n022/n023/n024).
ChangeSelection updates body context; favorites update their flag; the service
event calls **14135eb10**, which rebuilds body data, not **141360e80**.
The inspected lifecycle table supplies no independent periodic collector;
`1408817d0` forwards through slot+38 to the exit method (n029/n020).
The provider has an entry-built lifetime, not a demonstrated continuously
maintained resource cache.
No inventory-mutation subscription or per-selection recount occurs in this
bounded state/receiver/compiled-handler inspection. This scoped negative does
not prove that no external menu lifecycle can re-enter/rebuild the state.

Unloaded 3D and player distance are not direct collection operands: registered
Workshop and member **resolution**, capability and effective state govern access.
Missing registration/reference prevents contribution in that invocation.
Physical shared fixtures can expose the same backing stock even when the selected
outpost is distant. Offline code does not establish exactly which distant
references remain resident or how soon pending production/inventory work settles.

If realized freshness becomes consequential, the single proposed test is: on a
protected copy, establish one isolated producing resource and record settled
Locations count, leave the menu open while production advances, compare a
selection-only repaint, then leave/re-enter Locations and compare the isolated
inventory. Record time/load state and no-action control; protect source saves.
This is **not executed** and requires a separately authorized live card. It tests
snapshot repaint versus recollection, not cargo-voyage replay or all remote states.
