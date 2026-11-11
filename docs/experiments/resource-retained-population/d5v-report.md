# D5V population lifecycle, stability and gameplay consumption

2026-10-30, Australia/Sydney. [Frozen brief](../../implementation-briefs/README.md#archive-lookup) (`implementation-briefs.zip :: docs/implementation-briefs/CODEX_BRIEF_SOR_RG2_D5V_resource_population_stability_consumption_native_coordinates.md`),
[active ledger](d5v-investigation-ledger.md), [native map](d5v-lifecycle-consumer-map.md),
[coordinate contract](d5v-coordinate-contract.md), [sources](d5v-sources.csv),
[figures and data](d5v/README.md), [review](d5v-review.md).

**Coordinate presentation corrected under [D5V-C1](d5v-c1-report.md):** the
original figures had reversible centre-relative axes, which failed the requested
native-axis presentation despite prior acceptance. Current plots show absolute
historical native descriptor-frame X/Y, including centre/beacon labels and full
150-unit circles. This supersedes the old D5V-AC6/AC7 presentation acceptance;
native geometry and the lifecycle/consumer conclusions below are unchanged.

**Ordinary stability is conditional on several different contracts.** A source's
first eligible constructing miss fixes its retained geometry; later map hits and
visited bypasses do not rerun generation. Ordinary movement can preserve some
sources and retire others. Broad manager reset clears both the source map and
visited state, permitting reconstruction. Consumers then apply their own query,
refresh and filtering rules. Equal geometry therefore need not imply equal
player-visible answers, and different geometry need not change the available
resource identities.

## Answers to the frozen questions

| Question | Best-supported answer | Proposed status and coverage |
|---|---|---|
| **D5V-Q1 — Population lifecycle** | Cold initialized state admits construction on an unvisited map miss after source/BIOM/component/raster prerequisites. Hits retain output. A shift preserves overlapping sources and retires others; retirement removes the pointer-map entry without clearing visited identities. Broad reset dispatches the actual ProcGen reset and clears both stores; destruction releases their allocations. Return through retained context, source retirement, broad reset and a new process are distinct cases. | COMPLETE within the pinned ordinary compiled paths and explicit transition predicates below; final independent disposition controls acceptance. No claim identifies Save52's first construction or every exceptional gameplay script. |
| **D5V-Q2 — Gameplay consumption** | Area availability scans retained regions through `0x1421e0f50`, then maintains separate spatial/atmosphere/biome lists. Catalogue filters and UI rows use those lists differently. Natural extractor placement instead uses `0x14079df70 → 0x1407affb0 → 0x142346b30` at candidate raw XYZ, then intersects the accepted resource pointers with the candidate's produced resources. Fixed geometry can give different results through query, translation, cache or filter changes. | COMPLETE for these native consumers; static branch semantics plus executed per-region controls. Physical collision, production rate and a complete scanner-renderer reconstruction are separate operations. |
| **D5V-Q3 — Stability mechanisms** | Winner selection is order-sensitive under D5S's qualified cold contract. Generation is reproducible for fixed complete effective inputs, separately from retained ownership and consumer invariance. Retention avoids resampling. Reset permits a different winner without requiring different available identities: the second Feynman V model has the same Cu/F/IL area membership under both U25 alternatives. | COMPLETE as a conditional normal-system account, not a measured retail frequency or universal invariance guarantee. No reported missing/swapped-resource incident is attributed to any mechanism here. |
| **D5V-Q4 — Native spatial provenance** | Source-grid Int2, body-face cells, descriptor-frame geometry, saved site-local centre, indexed area operands and raw candidate XYZ are distinct native domains. The saved-frame join and reversible display transform are independently checked. Both outpost figures carry the full default 150-unit circle; current loaded frames and unobserved candidate positions are not superimposed. | COMPLETE for the documented native domains, qualified saved-frame models and explicit conditional consumer joins. Historical loaded index translations, terrain borders and physical compass orientation remain unobserved and are not plotted. |

Confidence is **PROVEN / STATIC** for the cited pinned instruction paths and
**PROVEN / executed fixture coverage** for the finite predicate controls.
Historical-frame deposit maps remain conditional models, not observed complete
populations. Operator checks are **OPERATOR OBSERVED** only. These proposed
question statuses do not replace the exact-snapshot independent review or
maintainer integration/publication gates.

## Construction, retention and return

The [native map](d5v-lifecycle-consumer-map.md) gives exact sites, field owners,
predicates and an action/state matrix. All addresses are preferred static VAs for
image base `0x140000000`, Starfield 1.16.244.0. RVAs subtract that base; they are
not relocated runtime pointers, FormIDs or save offsets.

The provider `0x14079f860` obtains the current source Grid, retains it for the
invocation, selects a cell from the original signed Int2, and enumerates its raw
source pointers. Source BIOM lookup precedes the shared visited check. An
unvisited source reaches exclusive ProcGen protection and full-pointer lookup.
Only the miss branch allocates/inserts a wrapper and calls the generator.
The lock serializes construction for that live pointer-map entry; it does not
choose a geographic minimum or promise the first registered request wins.

The ordinary query sample controls numeric rarity multipliers, not membership
bits. Source origin, source BIOM, owner/component, definitions, resource order,
seed operands, clipping and successful copying remain separate inputs.
The provider appends visited after the attempt without a complete-population
success test. Failed prerequisites or copies can therefore leave empty/partial
output without automatic retry. A visited marker, wrapper allocation, aggregate
result and successful geometry are different facts.

Manager construction installs ProcGen in its module list. Broad reset
`0x140788e70` first drains tracked generation, takes manager exclusive ownership,
dispatches module `+0x10`, then module `+0x18`. The landscape `+0x18` callback
releases its Grids; ProcGen `+0x18` resolves to `0x14079df60 → 0x14079ddf0`.
That reset clears retained wrappers and visited storage. The false-argument
variant `0x140789850` uses the same module reset slots. The manager object can
survive while these populations do not.

Ordinary focus movement is different. With manager mode 2 and no blocking
transition, `0x14078c5f0` compares displacement with the setting-derived threshold,
queues ShiftToTask on crossing, and enters mode 3. The default threshold is 250
native units under D5S's qualified settings. `0x14078ce00` takes manager exclusive
ownership and dispatches module `+0x50`, then `+0x58`. Landscape callbacks update
the origin and shift both Grids. ProcGen's corresponding slots are no-ops, so
this dispatch does not itself perform the broad ProcGen reset.

Retirement `0x140982b70` removes the pointer-map entry and frees the source after
unlocking. It does not remove the separate visited identity. Constructor
`0x140982d90` derives that identity from content/geographic and filename hashes;
the filename parser `0x1427d7580` is a CRC calculation, not an allocation counter.
Consequently, **if** a recreated source has the same identity and the visited
entry survives, the provider bypasses construction even when that source's new
pointer has no map entry. This is a conditional branch result, not evidence that
an ordinary retail return took that path or caused a reported defect.

Entering a new descriptor/owner context can reach `0x140789ce0`: zero owner resets;
changed owner resets an existing context before installation; the same-owner
branch distinguishes the current world's component from the incoming one and
uses the false reset or broad reset/re-entry branches. Source/visited retention
must not be inferred merely because the body FormID is unchanged. Worldspace
release `0x14078cf00` also resets when a nonzero current owner has a different
current world component from the supplied component.

Loading function `0x141815620` calls the generation drain. Engine phase dispatcher
`0x141827960`, case 3, conditionally calls `0x1407895a0 → 0x140788e70`; its guard
is the byte at `0x145e8fd70` being zero or the supplied phase flag being nonzero.
The independent world teardown path `0x141896280` drains and calls broad reset.
Neither a drain alone nor a load progress label proves a populated source.
After reset, source/index initialization and demand prerequisites reconstruct
the mapped generated representation. This does not certify completion at a
particular historical load boundary or exclude all alternate serialization.

## Consumers and supported stability

Area refresh is gated by domain and translated XY displacement, rather than
every invocation. Its local guard does not separately compare radius or upper
height. A refresh scans the current manager's occupied source map under shared
ProcGen protection. One passing region admits an IRES pointer to a deduplicated
temporary set. There is no exclusive overlap winner between resources on this
path: several resource identities can pass. Resource resolution, allocations,
store completeness and the separate cache state still matter.

The area predicate has XY broadphase, a special one-point acceptance branch,
tapered-strip planar containment, height-qualified vertices and 3D edge-distance
branches. It is different from the point predicate used by natural extractor
placement and from generation competition. The point query tests endpoint disks
and oriented segments after its own bound check; it consumes XY rather than an
area radius/upper-height operand. Its input comes directly from candidate
reference `+0x8c/+0x94`, with no indexed-position conversion at that edge.

Catalogue eligibility selects spatial, atmosphere or biome declaration lists
according to effective properties; PlaceAnywhere can bypass the resource gate.
The area UI unions spatial and atmosphere lists, then appends selected Water
from biome declarations. These are distinct native decisions. The queued UI
command reads mutable shared lists later and carries no immutable query/result
snapshot. A catalogue item, an area resource row, a valid resource position and
a successfully placed/producing extractor are not interchangeable observations.

With fixed complete region bytes, matching coordinate frame, query operands,
effective resource definitions and relevant cache/filter state, the mapped
membership computations are deterministic within their qualified arithmetic and
successful-allocation domain. Holding position alone does not meet that contract.
Moving a candidate, changing radius/translation, using a retained versus refreshed
list, changing produced-resource properties or reading a different asynchronous
list state can change a consumer answer without a geometry mutation. These are
code-supported possibilities; this assignment observes none of them in retail.

For **Feynman V Cu Co Ni IL**, the frozen historical-frame source models admit
one region each for Nickel/Cobalt/Copper/Ionic Liquids in the 150-unit area query.
For **Feynman V Cu IL F**, U25-M0 admits Cu/F/IL counts 3/2/1, while U25-M3 admits
2/3/4. Resource identities stay equal while shapes and path counts differ.
Other contributed layers admit none at this disk; independently variable U23
is omitted from the second figure rather than asserted to share U25's winner.
Both model beacon-centre point queries admit no region, illustrating why an
outpost-wide resource list does not certify a vein at the beacon itself.
These counts use the actual native predicates on supplied geometry, not pixels.

The maintainer's primary-site four-resource match with minor shape differences
and second-site preference for Mask 3 remain qualitative operator reports.
They do not establish a sampled mask, complete construction epoch, jointly
selected source outcomes, scanner predicate equality or a bug cause.

## Evidence, controls and limits

[Native method](../../../research/resource-retained-population/d5v_native.py)
executes original callback/predicate bytes only in a disposable offline process.
Its final local receipt is `.local-work/d5v/native05.json`. The 591 supplied
model regions plus 15 synthetic controls yield **606 area comparisons**, all
equal to the owned transcription, and **606 point-predicate evaluations**.
Positive first-point and changed-Z controls additionally exercise the original
point predicate. The receipt retains exact geometry, translations, branch
results and input hashes. The [check method](../../../research/resource-retained-population/d5v_checks.py)
authenticates the model geometry and independent centre tables and reproduces
the SVGs byte-for-byte.

All seven area-transcription branch categories occur: broadphase rejection,
one-point acceptance, empty points, planar containment, height-qualified vertex
acceptance, 3D edge acceptance and narrowphase rejection. Deliberate controls
include inclusive tangency, fixed-geometry near/far queries, area-versus-point
disagreement, translated multipoint input and vertex/edge height discriminators.
Each native case supplies one resource/one region and a preallocated one-slot
set. It does not qualify native multi-entry aggregation, overlap deduplication,
allocation failure, every boundary rounding case or a retail history.

D5S/D5T/D5U retain the evidence for feasible winner alternatives, fixed-input
generation and source lifetime limits. D5V does not rerun their complete
generation corpus or promote their prospective frames to historical replays.
The source-lifetime gap in detached density work remains a native-feasible
conditional counterexample, not a measured race or observed crash.

No indispensable unknown input with a supported serialized producer was found
for these conditional mechanism questions. AC8's targeted-save trigger therefore
did not fire. Existing authored saved-centre derivatives were read; no raw save
was parsed or changed. Persisted centre/producer rows do not prove persisted
region geometry. Save geometry/restoration authority remains UNRESOLVED beyond
the mapped reconstruction paths; it is not needed to identify the conditions
under which these paths construct, retain or consume their process-local data.

Falsifiers include a different compiled module-slot target, a qualified same-input
native predicate disagreement, a wrong saved-frame byte join, or evidence that a
claimed reset branch leaves these stores intact. Such evidence reopens the
affected claim. Unknown historical timings and exceptional paths outside the
documented contracts do not establish these falsifiers.

## Preservation and handoff

Fresh installed executable/ESM/PlanetData hashes match the brief. All 15 existing
analysis pins are verified before/after read-only exports. The exact source/tool
and final delivery manifests retain identities. Raw PE bytes, decompilation,
native fixtures/receipts and analysis databases stay local and excluded.
No game launch, attach, breakpoint, plugin/configuration/Vortex change, save
write, database edit, external disclosure, staging, commit, push or publication
was performed. D5P remains NO-GO and B6/publication ON HOLD.

The complete and task-only patches, unchanged HEAD/index checks, failures,
criteria matrix and independent scientific/engineering/editorial dispositions
are recorded in [the review](d5v-review.md). Research conclusions and integration
approval remain separate.
