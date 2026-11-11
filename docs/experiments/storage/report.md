# S1: outpost storage and output-link eligibility

2026-10-17, Australia/Sydney. SOR-EXP-0042 / SOR-EV-0050.
[Invoked brief](../../implementation-briefs/README.md#archive-lookup) (`implementation-briefs.zip :: docs/implementation-briefs/CODEX_BRIEF_SOR_S1_storage_inventory_eligibility_runtime_save.md`),
[native contracts](native.md), [saved examples](saves.md), [review](review.md).
Authored interpretation REVIEW-REQUIRED; underlying game/native/save material LOCAL-ONLY.

| Element | Answer |
|---|---|
| Question | Which ordinary outpost objects hold inventory, what admits items and limits capacity, which references can be output-link endpoints, and what is saved? |
| Best-supported answer | Dedicated Solid, Liquid, Gas and Warehouse stores use item-category filters and weight capacity, with small/medium/large base capacities **75/150/300**. They can hold multiple different matching items. Extractors and builders have their own small output inventories. Recipe ingredients and generator/pad fuel are obtained from incoming source references; a recipe is not a second physical input inventory. Directed links connect **references**, separately from the reference's item stacks. |
| Confidence | Proposed STRONG / STATIC and SAVE for the bounded ordinary model; exact definition rereads and hash checks are mechanical observations. No new RUNTIME evidence. Independent assignment disposition is controlled by review.md. |
| Coverage | Installed retail 1.16.244.0/main ESM; all 225 quick-menu CONT definitions plus 16 construction-list chest comparisons; selected cargo/generator pack-in cells; four distinct historical originals; supported inline-base records and empty stack-extra inventory grammar. Main ESM is not a winning load-order merger. |
| Evidence | [Catalogue](catalogue.csv), [function register](functions.csv), [native](native.md), [object-level saved joins](saves.md), local census02/assemblies01/saved03-06 receipts and source metadata. |
| Limits | No current loaded stocks, effective overrides, actual menu interactions or transition measurements. Nonempty stack extras and leading unknown extras remain explicit gaps. No universal construction/Workshop population or cross-version layout claim. Transfer Container and ordinary chest saved instances are not established by this subset. |
| Next step | Critical review against the frozen S1 contract. S2 concerns movement/scheduling and requires its own brief; the deferred questions below confer no execution authority. |

Ordinary decorative chests have both incoming and outgoing link prohibitions set.
The native add-link validator checks those values, so their exclusion is more than
an absent UI button. A hypothetical container with those prohibitions removed is
a different case: a TESContainer component can satisfy the generic source test.
Neither class name nor the OutpostBuildContainer property alone decides eligibility.

The Transfer Container is a **200-weight local inventory**, with both local-link
directions available subject to ordinary pair validation. Its special keyword
supports the ship-access path; the attached installed source also requests local
redistribution on relevant player inventory/menu events. This does not establish
automatic periodic ship-to-container or container-to-ship loading.

Cargo-pad incoming and outgoing inventories are **different child references**.
The ordinary and fueled construction templates inspected here both use the
300-capacity `New_Basic` container bases. Incoming containers prohibit incoming
local links and can be senders; outgoing containers accept compatible local links
and can also qualify as senders. Those direction capabilities do not establish
reverse freight flow. The fueled pad's marker is a distinct recipe-bearing fuel
endpoint; its He-3 supply is the incoming graph's inventories, not an independently
demonstrated He-3 stack on that ACTI. Names containing `InterSystem` are not proof
that a template uses those alternative definitions.

## Runtime and persistence correspondence

All capacities below are **definition fallback values**, in item-weight units,
not item/stack counts or observed current effective capacity. Native effective
CarryWeight can include explicit bases and modifiers. Filters refer to item
keywords, not merely the player's UI tabs. Multiple matching forms are allowed;
different weights use different numbers of units to fill the same capacity.
ONAM absent, present-empty and populated are distinct native cases.
Category admission here is established for the mapped ordinary output-link/product
paths. Manual ContainerMenu item admission and forced/script insertion are not
claimed to share every restriction; the exact remaining boundary is in native.md.

| Class / variant | Role and admission / local directions | Base capacity | Runtime owner / path | Saved representation / sample | Cross-layer strength and limits |
|---|---|---|---|---|---|
| Solid, 3 sizes | Matching solid keyword; sender and receiver | 75 / 150 / 300 | CONT reference inventory; effective CarryWeight; ONAM filter | REFR inventory tail; H36 ff018b64; owner Extra4C | STRONG for sampled small store; medium/large definitions established, stocks not sampled |
| Liquid, 3 sizes | Matching liquid keyword; both | 75 / 150 / 300 | Same owner, separate item rows | H36 ff018b61 | STRONG small join; other size stocks unobserved |
| Gas, 3 sizes | Matching gas keyword; both | 75 / 150 / 300 | Same | H36 ff018b66; large examples include unsupported stack extras | STRONG small join; large association positive, full stocks unresolved |
| Warehouse, 3 sizes | Manufactured-resource keyword; both | 75 / 150 / 300 | Same | H36 ff02c339 contains two item types | STRONG mixed-content small example; no universal content census |
| Ordinary solid/gas/liquid extractor | Own output buffer; incoming link blocked; sender | Solid 10/15/20; gas 5/7.5/10; liquid 6/9/12 | CONT inventory; producer registration is separate | H77 ff0294fd Iron x17; producer-map joins reused from E1 | STRONG saved product-buffer join; no measured output or refill guarantee |
| Atmospheric extractors | Output buffer; sender, incoming blocked | Ordinary atmosphere 10; two He-3 bases 3.75 | Same reference inventory | H36 ff01a4fb Water x20 | STRONG example; exact 19-base exceptions retained in catalogue |
| Greenhouse / husbandry, 3 ranks each | Own output inventory; recipe-compatible input sources, compatible output targets | 3.75 each | CONT output inventory; common builder ingredient walker totals upstream stocks | H36 ff01a5c5 greenhouse product x15; configuration/producer rows separate | STRONG greenhouse join; husbandry save-instance gap retained from E2 |
| Fabricators, 3 families | Own output; compatible recipe inputs from incoming sources; both subject to pair tests | 15 ordinary; 14 retained cut/test presets are 5 | CONT inventory; no separate local ingredient store established in mapped consumption path | H36 ff0382cf output x4; BF configuration and producer map separate | STRONG sampled output join; 30 ordinary construction presets versus 45 classified bases |
| Fueled generator | Recipe-bearing receiving endpoint; excluded as sender | No own capacity/store established | ACTI plus upstream He-3 sources; charge/AV and electrical state separate | P1 source-consumption/producer and powered-state channels reused; no new physical stock join | STRONG upstream-input mechanism; own stock absence bounded to inspected definition/native path |
| Transfer Container | General local store; both directions | 200 | CONT plus special ship-access keyword; menu/event handoff | Generic serialization path identified; no sampled instance | STRONG static mechanism; SAVE correspondence conditional, actual instance unresolved |
| Cargo incoming child | Local source; incoming links blocked; no ONAM filter | 300 ordinary templates; 200 retained mission bases | Separate CONT reference | H36 ff01ca38 mixed historical stocks; empty comparison ff01ac54 | STRONG object/quantity join; historical cargo arrival mechanism deferred |
| Cargo outgoing child | Filtered local destination; generic source permitted | 300 ordinary templates; 200 mission bases | Separate CONT reference; cargo filter admits several resource keywords | H36 ff018b73 output stock; template linked-reference keys separate | STRONG local store join; does not imply S2 reverse-flow behavior |
| Fueled pad marker | Logical fuel receiving endpoint; recipe validation | No physical store established | ACTI marker and transitive source inventories | H36 ff018b69 has no inventory-change branch; marker/pad role derived separately | STRONG fuel-boundary model, not proof of universal inventory absence |
| Ordinary decorative chest comparison | Both directions prohibited by effective AV gates | Outside S1 general chest research | TESContainer capability alone is insufficient | Definition/list and native comparison; no identified chest in sampled inline subset | STRONG native exclusion for examined defaults; UI-only exclusion hypothesis contradicted |

Base capacity is DEFINITION-DERIVED; reference AV overrides/modifiers are MIXED;
item identities/counts and explicit owner/link relationships are PERSISTED;
resolved pointers, handles, lookup hash tables and component caches are
RECONSTRUCTED/TRANSIENT. An omitted inventory-change branch is not an empty-stock
finding. A decoded zero item count is the narrower positive empty serialized-list
observation. Save restoration does not certify the settled loaded value.

## Bounded census and falsifiers

The 225 main-ESM CONTs bearing `OutpostShowQuickMenu` partition into 154 extractor,
45 manufactured-builder, six organic-builder, twelve dedicated storage, six cargo
container, one Transfer Container and one mission-supply definition. All selected
records and direct classification/property/filter records were physically reread:
573 records. The ordinary construction families retain E1/E2/E3's exclusions rather
than calling cut presets available gameplay variants. The mission supply builder
has capacity 50,000 and is excluded from the ordinary catalogue model.

Sixteen ordinary decorative containers come from three actual construction FLSTs,
independent of the quick-menu predicate. All set both link-blocking AVs to 1.
Their general contents, display mechanics and chest persistence are out of scope.
All twelve dedicated storage bases have construction COBJ joins; cargo pack-ins
are checked through their actual cell children, not guessed labels.

An ordinary matching item rejected by the traced filter with the same operands,
a chest accepted despite its effective prohibitions being 1, or inventory counts
that disagree with native writer/loader framing would reopen the corresponding
claim. A current override would change a particular reference's effective state,
not falsify its base definition. Historical inventory can contain items not
admissible under current definitions; no current-load equivalence is assumed.

## S2 and deferred questions

S2 should use the reference graph and inventory interfaces mapped here to study
directional movement, trigger ordering, partial insertion, full destinations,
multi-hop routing, cycles, batching and backpressure. No such algorithm or
throughput prediction is implemented by S1. The partial-fit helper is documented
only to explain why free weight can admit fewer items than requested.

Defer ship scheduling, remote freight/return handling, remote saturation and voyage
He-3 consumption. Preserve the user's possible outgoing-to-incoming cargo spillover
as an unresolved transport hypothesis, without assigning a cause. Defer general
chests/displays, Shared Outpost Storage cross-outpost access and crafting sourcing.
The supplied Schrod II Ad screenshot does not establish where **Stored Resources**
quantities come from, including whether Shared Outpost Storage contributes.
No database-aggregation claim follows from these local inventory findings.

No new live observation is required to state this bounded mechanism. If a later
question turns on actual current overrides, one separately authorized reference-
matched native query/menu comparison would discriminate; S1 does not build it.
