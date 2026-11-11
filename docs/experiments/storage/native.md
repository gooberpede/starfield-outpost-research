# Native storage and endpoint contracts

Reader notation: [vtable versus object offsets](../../reference/notation.md#native-prose-at-first-use);
[experiment-local export namespaces and lookup](../../reference/native-export-ids.md).
These guide the existing local address/offset declarations; they do not make
export labels global symbols or raw exports available in a checkout.

[Answer-first report](report.md), [saved joins](saves.md), [register](functions.csv).
All hexadecimal addresses are preferred static VAs, image base `140000000`;
RVA = VA minus base. Object offsets are hexadecimal. Fresh executable version
1.16.244.0, SHA-256
`7e9adb1414a8e1b325e5e1f097b9b17b78deb7eebeda37a333351a43a60f9d28`;
main ESM SHA-256
`1dabed00c3f4282dd3bb54d2e9601e40b577d8742d078b7ccef203adbfef0da7`.
No address is a runtime pointer. Aliases are analyst-assigned,
OBSERVED-INTERNAL; no safe ABI or mod integration point is qualified.

`sNNN` denotes `.local-work/s1-storage/native/NNN.request.tsv`; prior `aNN`
denotes `.local-work/recon/e1-arithmetic-NN.tsv`. Full exports remain LOCAL-ONLY.
Decompiler types and return types are not authoritative; instructions and consumers
control argument direction and floating-point results.

## Owner, weight and capacity

`140b24ca0` (s003) queries the reference's base at +98 through `140b756c0`.
That helper uses component lookup `1405ddbd0`; `1405da040` (s005) positively names
`TESContainer_Component`. Capability is distinct from stock. Reference +a0 is the
inventory-list object reached by `140b29990`'s inventory restoration branch.
`1406448b0` reads its item array (count +28, data +30, stride 28), resolving the
owner handle at +38. These are runtime offsets, not on-disk offsets.

`140f7c210` (s001) returns capacity <= current weight. Non-actors read effective
CarryWeight from reference +70 virtual +8, with the AV singleton's +80 binding;
current weight comes from `140b69760`. Actors have a distinct capacity route.
The existing [effective AV contract](../inorganic-extractors/arithmetic-production.md#effective-interval-and-av-provenance)
traces `140b6ce20`, `140b6cfa0`, ExtraBF base overrides and modifier slots,
ExtraE1 and base-sheet fallback. PRPS alone is not an effective runtime value.

`140b70a80` (s001/a10) limits ordinary positive-weight insertion to
trunc((capacity-currentWeight)/itemWeight) when requested mass would exceed a
positive capacity; no remaining space yields zero. Item weight is clamped at least
zero. Its conditions include a player exception, and nonpositive capacity does not
enter this positive-capacity clamp. Consequently it is wrong to interpret zero as
universally zero available storage. Do not extrapolate exceptional float inputs.
`140b64fc0` (a10) calls this helper and performs ordinary mutation/count splitting;
requested count is not an independently measured accepted delta.

No shared one-item/one-stack limit appears in this representation: native arrays
and saved mixed-content examples support multiple forms. Capacity is weight, not
number of forms or stacks. The array/count structure alone does not establish
arbitrary engine-wide unboundedness.

## Separate source and pair gates

`140f83f60` (s002) is the source predicate. A nonzero effective
OutpostNoOutgoingTransferLink rejects. Otherwise harvester, builder, non-actor
TESContainer capability, or fueled-input category can qualify, but the fueled
generator predicate excludes generators as senders. This is not the test
`OutpostBuildContainer != 0`.

Default bindings are positive initialization evidence: `140156fc0` binds
OutpostNoOutgoingTransferLinkAV_DO, `140156f80` incoming, `140156980` harvesters,
`140157730` Workshop (s012). DFOB targets are AVIF `0313eb` and `2192d5`;
their ordinary default is zero. The initialized object's resolved pointer at +48
is the pointer consumed at `145f0aa28` / `145f0a9d0`. The sixteen decorative
container definitions override both to 1. `OutpostBuildContainer` is `00f65a`;
the chest definitions also set it to 1, an explicit counterexample to using it as
the sole link-capability classifier.

`140f84470` (s001) validates the **ordered source,destination pair**, returning
zero on success and a nonzero reason otherwise. It rejects self/same compound
identity, actor destination, harvester destination, Workshop destination and
nonzero incoming prohibition, then requires the source predicate. Builder source
compatibility and ordinary container-source compatibility take different branches.
Builders test their catalogue against destination filters; recipe-bearing receivers
test ingredient compatibility. Ordinary container pairs compare their filter lists
and topology rather than proving that every current stored item can move.

`140f841c0` ([E3 contract](../fabricators/native.md#connections-and-upstream-input-contract))
normalizes recipe products, requires destination CONT and reads base +258 ONAM
list: null accepts; present-empty rejects; populated accepts exact forms or item
keyword matches, across the candidate catalogue. This is catalogue compatibility,
not current stock, quantity, free space or guaranteed ongoing supply.
Fresh CONT loader `140a84810` (s026), instructions `140a85031..140a850de`,
binds ONAM (`4d414e4f`) to base +258; `140a84690` fixes the definition identity
into the resolved form pointer. This independently grounds that field.
`140f84020` (s002) supplies the related ingredient/source-container compatibility.
`140f843e0` delegates the topology guard to `140f894c0`; S1 does not simulate it.

`140f85760` (existing E1 e1-native-09) calls `140f84470` and invokes insertion
`140f81200` only for result zero. The ObjectReference AddTransferLink binding
`142068a10` (s002) additionally runs the source test, emits explicit diagnostic
reasons, then uses the same validated add. Therefore ordinary API/UI exclusion is
native-enforced. Low-level map insertion is a separate internal mutator; bypassing
the validated wrapper has not been invoked, qualified or shown safe.

Workshop action-mask producer `141589840` (s006) uses `140f83f60` to add bit 80
for the relevant selected reference/compound context. Destination highlighting
`1421c3bf0` and nearest eligible target selection `1421e7e20` (s004) call
`140f84470`. Final UI command `140f65870` resolves source/target handles from
context +5fc/+600 and calls `140f85760`. These positively connect source selection,
target selection and final mutation. No actual button visibility was captured.

Manual ContainerMenu's item-row enable/transfer check is a distinct unresolved
boundary. The complete literal +258 locator (s013: 14,392,060 instructions,
969 untyped candidates, not cancelled) led to the loader, known link consumers
and `14173ae90` (s016). The latter classifies a CONT's filter keywords for UI
category display; it is not a per-item insertion rejection. Generic insertion
`140b64fc0`/fit helper and the existing link/product paths do not establish a
universal manual/script admission invariant. Other literal matches were inspected
and rejected where they operated on unrelated structures (s018/s021/s023).
The actual manual command was then traced: ContainerMenu's TransferItem sink
at object offset 138 dispatches through vtable `144d07dd8` to `141eaf900`
(s028-s031). The handler runs or queues `141eaf9e0` (s033), which finds the
inventory item and reaches `141eb7950` -> `141eafe00` (s035-s036). That path
first calls `141eaf090` (s037): the item-interface predicate at vtable byte offset `0x130` **and** the invocation's
callable held at menu object + `0x4C8` must accept. It then applies direction/take-give state,
actor-specific capacity checks and the shared transfer operation `141eb01a0`.
That operation also reaches the ordinary fit/insertion helpers; it is not a
single unconditional item-copy operation.

The remaining narrow gap is the particular bound callable's target/captured
filter, not the identity of the manual transfer command. Menu constructor
`141eab810` (s039) initializes separate ContainerInventoryData and
PlayerShipContainerInventoryData models through `14146ba60` (s042); that helper
initializes callable storage at relative +338 to null. Refresh/setup paths
`141eaca10` / `141eac0e0` (s040/s044) and two scoped literal-use locators
(`native-menu/fields.tsv`, `native-final/*-fields.tsv`) do not resolve the
indirect assignment/captured operand. Literal coverage is not alias closure.
Thus no universal manual/script admission invariant is asserted from these
routes. A matched callable target/captured filter at `141eaf090`, or its proven
assignment ancestry, would close that specific boundary. Ordinary native
output-link/product category admission remains established independently.

## Transfer Container and ship-access boundary

`140126ca0` (s015) binds KeywordOutpostTransferContainer_DO; DFOB `2b207a`
targets KYWD `2b207b`, consumed through pointer `145ef9ba8`. `1416d47e0`
(s021) searches the Workshop reference's Extra4D relationships; callback
`1416d7a00` (s019) requires the Workshop relationship key and the special
Transfer Container keyword before returning the reference. Alternate finder
`141ee7130` -> `141ee80e0` -> `141ee8d20` additionally selects a spatially
qualified candidate; exact distance measurement is deferred.

UI handoff `1416bd210` (s024) obtains that Transfer Container reference and
another resolved inventory endpoint from handle global `145e88644`, applies its
access/range checks, and prepares separate handles in an event payload. It
dispatches through `14146d800`, positively identified in s025 as
`BSTGlobalEvent::EventSource<OpenContainerMenuEventData>`. This is a menu-access
handoff between references, not a copy of ship cargo into a shared outpost pool.
The exact active/home-ship selection of that global and every access-state branch
remain unqualified; the report does not generalize broader ship inventory behavior.

The installed `OutpostContainerScript.psc` attaches by VMAD to CONT `2ce194`.
Its ready-state player-origin item add/remove handlers and busy-state menu-close
handler call MoveContainerContentToUnfilledContainers. This is SOURCE-REPORTED
installed development source, not proof that the shipped PEX executes identically.
It supports a menu/event trigger distinction; periodic automatic loading of the
ship is not established. Redistribution internals and timing remain S2.

## Cargo compartment definition joins

`assemblies01.json` independently walks group/header boundaries for cargo PKIN
cells. Ordinary PKIN `2191a0` has incoming child REFR `219172` -> CONT `219173`
and outgoing `219170` -> CONT `219171`. Fueled PKIN `21903f` has incoming
`0d4d7d` -> `219173`, outgoing `0d556f` -> `219171`, and marker `219031` ->
ACTI `219523`. Child XLKR fields preserve role/marker relationships; exact raw
fields and offsets stay in that receipt. Both child CONT bases carry capacity 300;
incoming has NoIncoming = 1 and no ONAM; outgoing uses FLST `22b93c`, whose five
keywords are manufactured, organic, solid, liquid and gas. These are local stores.

Alternative CONT `100b62/100b63` named New_InterSystem also have capacity 300,
but those names do not replace the actual ordinary template joins. Mission
PKINs retain CONT `2a6c3a/2a6c3b` with capacity 200 and remain explicit exceptions.
The fueled marker and generator lack a TESContainer component in the inspected
definition records. Their common ingredient traversal establishes a logical input
role. No voyage consumption, shipment or spillover mechanism is assigned here.

## Link and inventory persistence are separate

Use [E1's writer/loader](../inorganic-extractors/links.md): `140f7e6f0` writes
destination then incoming source list; `140f7ea10` resolves saved references back
into the destination-keyed map `145916580` under lock `1459165d0`, and schedules
cache rebuilding. Edges are between reference identities, not inventory-port IDs
or resource-keyed producer rows. Distinct cargo compartments are distinct references.
Power ExtraCB and WorkshopItem Extra4C are other relationships.

Inventory writer `1406447c0` (s009) writes compact item count then each
`140641180` row (s010). A row writes the item FormID through `141868de0`, compact
stack count, each stack's ExtraDataList through `14051ea30` followed by signed
four-byte quantity, then four-byte bookkeeping and a byte. Loader `1406448b0`
(s006) -> `140641320` (s007) -> `140642a00` (s008) corroborates the order. It
resolves item identities, allocates stack extra lists and restores quantities.
Item FormIDs are remapped via the save's identity machinery, not raw pointers.

Reference loader `140b29990` (s005) reaches inventory when mask `08000020` is
present; inventory is after supported counted reference extras, not inside the
producer map or the base property sheet. The bounded reader recognizes empty
stack extra lists only. It stops explicitly at nonempty lists. Reference records
have additional trailing channels; inventory subgrammar closure does not mean
full record-body closure. `saves.md` reports exact offsets and queue consumption.
Reference saver `140b29700` (s034), especially `140b29807..140b29836`, tests
the same mask, obtains reference +a0 under protection and calls `1406447c0`.
This independently corroborates the reference-level wire boundary.

Definition content and explicit saved inventory changes are distinct; omitted
changes do not prove empty. Capacity/filter configuration normally comes from
base definitions; ExtraBF can persist explicit AV overrides/modifiers. The sampled
stock-bearing small store has explicit Workshop owner and inventory counts without
an explicit saved CarryWeight value. Load resolution/recalculation can change
effective values; no saved value is asserted authoritative after settling.

## Production input and lifecycle boundary

E1/E2/E3 and [P1 fuel](../power/fuel.md) remain the primary evidence for
`140f7f6f0`: current recipe ingredients are counted across transitive incoming
references (`140f881c0`), then prepared removals are sent to source virtual +458.
Production insertion uses the producer or an eligible destination. Recipe ingredient
definitions do not establish physically co-located input stacks. Generator ACTI
`2b063a` lacks a TESContainer component/capacity in the inspected definition;
fueled pad ACTI `219523` is likewise a recipe/fuel endpoint. No independent input
store on either ACTI is demonstrated by those paths.

Power and halt predicates control production separately from item serialization.
The inventory writer/loader does not require current power or loaded 3D. This
supports persistence independent of those predicates, but is not a measured
power-loss/disable/unload transition and does not exclude another lifecycle script
changing contents. The sampled no-inventory-change fuel marker is not proof that
every marker representation has no inventory. Disable survival and complete
unloaded simulation remain unmeasured; save/reload has a positive reconstruction
mechanism, with actual post-load equality NOT TESTED.
