# SOR-EXP-0034 — Inorganic resource availability

2026-10-14, Australia/Sydney. SOR-EV-0042 / SOR-F-0033 / SOR-ST-0031.
[Authority](../../implementation-briefs/CODEX_BRIEF_SOR_inorganic_resource_availability_runtime_serialization.md),
[frozen acceptance](contract.md), [executable contract](schema.md).
Authored research REVIEW-REQUIRED; original screenshots/saves/native exports and
bulk derivatives LOCAL-ONLY. Independent final disposition is in [review](review.md).

| Element | Best-supported scoped answer |
|---|---|
| Question | What produces a site's inorganic resource set, how does the UI relate to extractor eligibility, and what persists? |
| Answer | The native area UI aggregates generated resource regions, a world-linked ATMO definition list and spatially selected BIOM→RSGD resource definitions. Its third collection is filtered to water. A distinct harvester resource gate selects a collection by property presence or bypasses the test. The saved Workshop map instead groups producer objects; it is not a prospective availability list. |
| Confidence | Exact sampled bytes and selected instruction/data-flow links PROVEN within SAVE/STATIC scopes. Mechanism interpretation is a scoped STRONG proposal for review. Actual live invocation, freshness and existential placement coverage remain unvalidated. |
| Coverage | Pinned retail 1.16.244.0, 29 save labels including beacon-only stages and Save25–28/52; 38 installed ESMs, including 434 BIOM/599 ATMO/32 RSGD records; 848 supported roots and all 63 recognized extractors as positive controls; four static X-Tech variants; supplied prospective UI screenshot. |
| Evidence | [Validation ledger](validation.md), [native routes](native.md), [source hashes](sources.csv). Independently replayed 29 labels and 63 joins; executable conditional UI, callback, harvester gate, RNAM and generation first-gate calculations. |
| Limits | No archived same-invocation terrain arrays/UI/placement oracle; no independently evaluated complete site set. Source generation/identity/frame/cache inputs are not supplied merely by a saved beacon/body/site or planet/biome allocation. Whole-save absence and fundamental impossibility are not claimed. |
| Next step | [Minimal acquisition assessment](acquisition.md) separates UI equality/cache behavior from actual resource-location/footprint checks. Proposal only; no observer implementation or live authority. |

## Definitions and independent evidence channels

Operational local availability means that an appropriate inorganic extractor
could be validly placed somewhere in the effective area under resource-location
rules, with materials, power, unlocks and unrelated build requirements abstracted
away. An intersecting patch qualifies only if it supports placement; visual patch
presence or a coarse geometric overlap alone does not establish that property.
Planet-wide population, biome allocation, UI listing, craft-menu filtering,
point/footprint placement and existing producer objects are distinct quantities.

The supplied screenshot shows **Iron, Alkanes and Helium-3** under Available
Resources with an unconfirmed beacon preview and Confirm/Cancel controls. It
independently establishes a three-label prospective UI observation before
confirmation. Its pixels supply no qualified body/site/position, executable build,
timestamp of gameplay or archived-save association. It proves neither full
extractor-placement eligibility nor the native contents for Save25 or S1.
The original image remains local with SHA256
`391ef66c47b22f79716564e7ce7c8c4d8c0c661a28caddaddf6f3c27ea532fc8`.

Installed IRES definitions provide identity candidates Iron
`Starfield.esm:0057c7`, Alkanes `0057c9`, Helium-3 `0057f5`; these are definition
identities, not resource IDs read from the screenshot. The screenshot has no
runtime FormID channel. No expected availability list was manufactured from
extractors, those labels or a planetary allocation oracle. Current set equality,
false positives and false negatives are **NOT TESTED**, with null results.

## Runtime producer and preview/established distinction

The [native route ledger](native.md) preserves exact original function names,
static VA/RVA and decisive sites. Preferred image base is `0x140000000`; these
addresses apply only to executable SHA256
`7e9adb1414a8e1b325e5e1f097b9b17b78deb7eebeda37a333351a43a60f9d28`.
Runtime VAs, pointer identity, runtime FormIDs, saved tokens and file offsets are
separate domains. No function was called in the game by this task.

`FUN_141578250` creates the typed `WorkshopAreaResourcesDataModel`; embedded
constructor `FUN_14157d570` binds `aAreaResources` and `bSearchedResources`.
The event-shuttle/model chain reaches `FUN_141578500`, which clears/repopulates
typed `WorkshopAreaResourcesData::AreaResource` rows. This identification is
supported by constructors, callback ownership and typed row constructors, rather
than adjacency to the distinct category-bar model. The binder supplies name,
resource type, tracking and resource-info fields. UI transport is a native data
model feeding Flash; a Papyrus set-returning API is not established.

The final fold unions globals `145f5d800..808` and `145f5d818..820` by **pointer
identity**, retaining first occurrences. It then appends entries from
`145f5d830..838` whose runtime FormID matches `145efb1f0`'s selected form.
The independently resolved default is `WaterResource_DO` → IRES `0083ec`.
That special append does not use the union's deduplication. Null common pointers
are skipped; null special entries would be dereferenced by the filter. Successful
allocation is a precondition; failing allocation is not an observed empty set.

`FUN_1421e07d0` fills the collections through the operation-context object
`145f5d2e0 +0x520`. It uses an indexed-center descriptor and two separate float
arguments: **XMM2 radius** and **XMM3 an additional geometry operand**. The
established path reads descriptor +0x28/+0x2c respectively (context +0x360/+0x364).
The Ghidra decompiler's inferred pointer-shaped signature is not the ABI proof.

The ordinary-region callback `FUN_1421e0f50` resolves a resource form and checks
type byte `0x9f`, then tests same-frame XY distance against the squared sum of
region and query radii. One-point regions can qualify directly; zero-point
regions do not; multiple-point regions follow descriptor containment and
interpolated segment checks. This is a resource-region candidate predicate,
not a complete placement-footprint or collision test. The partial calculator
reproduces only its supported scalar branch and leaves segment decisions unknown.

The source types are independently identified by exact native concrete form
factories: IRES/BGSResource=159, BIOM/BGSBiome=160,
RSGD/BGSResourceGenerationData=171, ATMO/BGSAtmosphere=173 and
AVIF/ActorValueInfo=109. The second collection copies ATMO +0xf8/+0x100 after
resolving a world-component identity; it is an atmosphere-resource population,
not terrain intersection geometry. The third follows the indexed BIOM +0x308/
+0x310 RNAM list, then each RSGD's resource descriptors at +0x38/+0x40. Those
are **BIOM definition inputs**, not a saved TESObjectCELL resource array.
The BIOM loader's RNAM append and fixup independently establish that edge.

Fresh installed walks recover 434 BIOM, 599 ATMO and 32 RSGD records. The
conditional BIOM→RSGD→IRES RNAM calculation resolves 432 BIOM definitions
without conflicting projected overrides; 202 of those declared lists include
water `0083ec`. Two missing-RNAM BIOM definitions remain UNKNOWN rather than
being called empty terrain. This is reproducible definition-level information,
not 432 evaluated local sites. The spatial lookup selecting the actual BIOM,
ATMO inheritance/context and current native cache remain separate prerequisites.
The third-list operation does not apply the sibling planetary-family RNG or a
PNDT override merely because it traverses the same record types.

Established initialization and prospective placement/movement have distinct
callers reaching this shared producer. The producer maintains cached reference,
indexed center/frame and identity keys for the other two domains. A shared
function does not establish equal inputs, equally fresh results or equivalent
area semantics in preview and established states. The native ledger records the
exact cache branches and update-event path; no actual A→B→A preview movement was
performed. Beacon relocation versus the compensated durable Workshop center
retains its earlier [position qualification](../workshop-origin-beacon-relocation-persistence.md).
The ordinary definition's 150-unit radius is not substituted for the selected
effective descriptor/radius in this task.

## Resource gate and X-Tech

`FUN_1421f68f0` is a separate selected-harvester resource gate. After resolving
the qualified category/base/produced resources and property context, it consults
AVIF **key presence** through `FUN_14044b610`; this helper does not read the
numeric property value. Place-anywhere presence bypasses resource overlap.
Otherwise skip-vein presence selects the third collection; atmosphere presence
selects the second; the ordinary branch selects the first. The gate requires
at least one pointer overlap with the produced resource list, not all resources.
The third collection is not water-filtered here. Other native placement rules
remain separate. This proves that UI presentation and this resource gate do not
apply the same filter; it does not claim an observed retail false negative.

Fresh installed default-object and exact type joins establish:

| Default / target | Type | Meaning established here |
|---|---|---|
| OutpostCategoryHarvesters_DO → `008406` | KYWD | Category identity, not an AVIF. |
| HarvesterAtmosphere → `0083ff` | AVIF | Presence selects the second resource collection. |
| OutpostSkipResourceVeinCheck_DO → `271128` | AVIF | Presence selects the third collection. |
| OutpostHarvesterPlaceAnywhere_DO → `31986f` | AVIF | Presence bypasses this resource gate. |
| WaterResource_DO → `0083ec` | IRES | Special collection's UI filter identity. |

Both skip-vein and place-anywhere are **AVIF properties**, not keywords; the
native default-type byte `0x6d` must not be mislabelled KYWD. The four X-Tech
extractor bases `SFBGS050.esm:01662c`, `07e613`, `07e614`, `07e615` contain both
property keys (values 1.0 in these definitions). Their produced-resource identity
is `SFBGS00D.esm:033e3f`. This supports a static place-anywhere bypass in the
qualified native property branch, independently of a vein intersection or the
third collection's UI filter. It is not evidence that a placed X-Tech extractor
ran, that every site satisfies unrelated placement conditions, or that the UI
lists X-Tech. Placement remains NOT_OBSERVED_IN_SAVE_CORPUS.

The Terran Armada power-core build requirement is a separate COBJ recipe
relationship retained in [EXP0029](../extractor-resource-association.md#x-tech-exception-and-source-claims).
It must not become a terrain prerequisite or availability proxy. No new core
refund or production claim is made.

## What the saves actually serialize

The concrete `Workshop::ExtraData +0x20` map is serialized by
`FUN_140f50660` through `FUN_140f515a0`, restored through the corresponding
loader path, and contains outer resource keys with object rows. The native
row's handle and form-ID fields use separate queue helpers; four u32 words and
one byte contribute 17 body bytes. The new bounded decoder retains exact
decompressed-stream offsets, queued reference identities and raw payloads locally.
It does not assign operating-state semantics to those body words.

Controlled beacon-only S1/S1C and storage-only S2/S2C have **zero** groups. Iron
extractor construction at S3/S3C introduces one IRES `0057c7` group whose row
resolves the constructed extractor `ff022da9` and base `05ef19`; subsequent
no-action/solar movement/link controls retain it. Extractor deletion at S7/S7C
removes the group while the beacon remains. These actions were independently
recorded in the [manual-corpus brief](../../implementation-briefs/CODEX_RESEARCH_BRIEF_manual_save_corpus_S0-S7C.md).
They are not names inferred by the new scanner.

Save25/26/27/28 each have two sampled beacon prefixes and zero groups. Mature
Save52 has 19 sampled beacon prefixes, **80 groups / 114 rows**. Groups include
organic lubricant, manufactured drilling rigs and intersystem cargo links,
as well as ordinary inorganic resources. All **63 recognized inorganic
extractors** join uniquely by instance, base and produced resource to one row,
the same explicit saved owner and one of the **848 supported construction
roots**. This advances the producer-registry interpretation; it never expands
63 into a complete availability population. Two historical beacon prefixes have
zero groups, which is not total terrain-resource absence.

This is a decisive rejection of interpreting this sampled map as the whole
Available Resources list. It does **not** prove that no other save/global,
definition or generated representation preserves sufficient availability inputs.
The decoder covers the Workshop prefix, not every extra, version or restoration
branch. All current original/decoded hashes are in the local before/after
receipts; all 29 samples were replayed for deterministic output.

## Deterministic regeneration is a separate investigated lead

Maintainer-owned `starfield-resource-research` at
`a23e1c337bc369232d6ce463552a53617bb918e2` and
`starfield-resource-reproducer` at
`a8ff1c788bca415f571f06769ab3e712fa674f75` remain useful prior knowledge under
SOR-P-0002 / SOR-S-0133. Their actual README, v1 baseline and hypotheses were
read at those local revisions, not assumed from another session. They reconstruct
PNDT/BIOM/effective-RSGD/RSCS allocation, IRES families and atmosphere membership.
They explicitly exclude vein geometry and extractor placement; their validation
totals are source reports, not rerun or transferred to this site question.

A body seed and biome resource identity can identify a candidate generation
population, but do not by themselves identify each loaded region's center/radius,
point sequence, selected descriptor/frame or cached temporal state. Two sites
on one body need not have identical intersections. Even exact agreement with
the sibling planetary algorithm therefore would not independently test this
local predicate. No sibling oracle was used to populate expected local sets.

The native route ledger pursues the region/spatial descriptor producer and
definition/serialization leads directly rather than dismissing deterministic
regeneration because the Workshop map is different. Recovered dynamic operands
and unresolved operations are explicitly separated in that ledger. A possible
future complete offline terrain reconstruction is not disproved by this result.

## Deliverable and completion boundary

The executable deliverable is a **partial reconstruction**, comprising the
native UI identity fold, conditional BIOM RNAM identity projection, binary32
region broadphase, selected harvester resource-overlap gate, CRC/MT first
stochastic gate, saved registry audit and independent corpus checks.
No resource list is guessed. [Validation](validation.md) separates synthetic
mechanism checks, genuine saved controls, screenshot testimony and absent live
set/placement controls. [Acquisition](acquisition.md) defines the shortest
remaining discriminators without implementing instrumentation.

The original Outcome A is not demonstrated. The independent reviewer accepts
evidence-bound Outcome B for scientific criterion 6; exact package disposition
is recorded separately in review.md. It is not a universal impossibility proof or a claim that all future
native regeneration research is exhausted. The broader operational availability
question remains open where independent point/footprint evidence is missing.
Deferred XYZ/Z/continuous geography and the separate removed-outpost Hab control
remain discoverable in [BACKLOG](../../BACKLOG.md), without reopening them here.
