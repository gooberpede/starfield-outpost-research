# Resource-region dependencies and minimum runtime conditions

2026-10-15, Australia/Sydney. SOR-EXP-0034 / SOR-EV-0042 continuation.
[Brief](../../implementation-briefs/README.md#archive-lookup) (`implementation-briefs.zip :: docs/implementation-briefs/CODEX_BRIEF_SOR_resource_region_dependencies_minimum_requirements.md`),
[frozen contract](region-contract.md), [review package](region-review.md).
Authored interpretation REVIEW-REQUIRED; native/raw evidence LOCAL-ONLY.

| Element | Evidence-supported account |
|---|---|
| Research question | Which native states supply inorganic regions for a specified planetary area, and what is the smallest supported valid evaluation context? |
| Best-supported answer | The availability updater consumes the current manager's resident ProcGen source/resource maps. A separate provider selects sources through that manager's spatial source index, caches by source pointer and attempts synchronous region construction on a miss. A specified indexed center, radius and upper scalar plus initialized operation state are the explicit updater operands; complete, current geometry/definitions/translations and valid lifetime/freshness are additional conditions. |
| Confidence | STATIC, instruction-backed scoped account; STRONG interpretation proposed for user review. Existing runtime support concerns the natural loaded preview and final UI fold only. |
| Coverage | Pinned retail 1.16.244.0. Provider, producer, two direct provider consumers, component/descriptor selection, ProcGen ownership/reset and availability/UI branches. This is a bounded dependency graph, not every terrain generator or engine caller. |
| Sufficiency | Natural loaded preview execution and 346 UI folds are demonstrated. Static contracts do not establish standalone arbitrary-location sufficiency. Neither mandatory player travel nor independently prepared remote-context sufficiency is established. |
| Evidence | [Existing source pins](sources.csv), [additional pins](region-sources.csv), [native register](functions.csv), [lifecycle map](region-lifecycle.md), [requirements matrix](region-requirements.md). |
| Limitations | Captures omit source/resource maps, region points, actual translations and producer completion/cache epochs. Cache existence and task publication do not establish complete natural availability. |
| Next discriminator | Same-context source/component readiness, completed region operands and independently observed native spatial admission; separate-world versus current-manager selection needs its own lifecycle evidence. [Specific unknowns](region-uncertainty.md); no live experiment is authorized. |

## Method and provenance

All VAs are **preferred static VAs**, base `0x140000000`; RVA is VA minus that
base. Hexadecimal field offsets are relative to their expressly named object.
Executable SHA256:
`7e9adb1414a8e1b325e5e1f097b9b17b78deb7eebeda37a333351a43a60f9d28`.
No runtime base/address, pointer, FormID, source key or saved identifier is
interchanged. Original `FUN_` labels are analysis names; aliases are descriptive.

The investigation starts with the prior [native map](report.md) and
[Milestone B producer ledger](../resource-availability-milestone-b/native-provenance.md).
It rereads primary instruction/decompilation exports, then follows identified
missing source-index, pre-provider, task-publication and reset callers through
bounded existing-analysis exports. Ghidra runs read-only/no-analysis; neither
native code nor a game process is executed. Exact commands, tool identities,
export hashes, before/after protected pins and checks are retained in
[qualification](region-validation.md). A 600-instruction display cap is not a
complete instruction census; full decompilation and targeted instruction windows
are distinguished. No new third-party implementation is incorporated.

## Provider is a current-context producer, not a radius query

At RVA `0079f860`, explicit RCX is ProcGen, RDX a discrete Int2, R8 an output
aggregate wrapper. The function still reads singleton `145fd9c30`, asks
`14078c4e0` for current context, retains manager+120→+10, selects an index entry
through `140985870`, and invokes its virtual +10 enumerator. Decisive provider
windows: `14079f8d6..f937`, `14079f9bd..f9ca` in
`resource-milestone-b-producers-01.tsv`. Multiple source descriptors may be
enumerated. This is finer than a planet definition, but neither its Int2 nor its
cache key is a demonstrated universal planet/landing/cell identity.

For each selected source, provider resolves BIOM (`14079fb16`), derives source
origin/frame operands and uses two distinct bookkeeping keys. The visited array
ProcGen+48/+50 records source+68 (`14079fc37..fca6`). The source hash at ProcGen+10
uses the **source pointer** (`14079fcc2..fcd4`, `14079fe0f..fe18`). These are
separate keys with different lifetimes; neither is a persistent save identity.

On a miss it allocates a refcounted 0x40 wrapper and initializes its resource map,
inserts the source/value pair, invokes `14079b520` synchronously, and appends the
visited key. It holds ProcGen+40 exclusively through this work
(`14079fcb3..14079ffa5`); availability scans under the same lock. Insertion before
construction therefore does **not** demonstrate that a concurrent area scan sees
partially written construction. It does demonstrate that a stored entry is not
an independent success certificate: the void construction call has early exits
and no success value is checked before visited bookkeeping. A visited source can
also skip work; a source-hash hit reuses existing geometry. The provider's RAX
cleanup value is not established as a semantic success flag.

## Construction depends on more than biome and seed

At RVA `0079b520`, the arguments are a source-descriptor pointer, transformed
integer origin, a coordinate representation, manager+80 key/discriminator, BIOM
pointer, and output wrapper. The first argument is **not simply an owner key**;
source bounds and flags remain relevant. Component lookup `140771f30` reads
current component storage and matches the manager key plus BIOM FormID; false
branches from `14079b6e4` to cleanup. A separate retrieval at `14079b72b`
(`140478a30`) and state check `14079b750..b794` admit statuses 0/6 to further
work. Numeric status values are observations, not named engine enums here.

Resource descriptors come from component-selected RSGDs, the current BIOM and
alternate matching BIOM paths (`14079c540` / `14079c5e0`). Rarity sorting
`1407af470` precedes source-bounded cell traversal `14079c470`, then
`14079a330`. CRC/MT state, selected descriptor chance/weight, source frame and
clipping, resource order and earlier different-resource geometry affect accepted
points (`1407af1a0` / `14079b020`). This confirms concrete dependencies; no new
generation implementation or seed-only sufficiency is claimed.

The provider has no query radius or upper scalar. It prepares reusable source
geometry; those query bounds appear later in availability's callback. The related
raster path `1407a0820` and four-level aggregate are distinct products, not
substitutes for the source/resource regions consumed by availability.

## Requests, completion and invalidation

New export01 identifies context gate `14078c4e0`: it resolves manager+78's
state-qualified object to +98, then existing context+e0 or the flagged parent
chain. Its call to `140bbd270` passes false. Export04 shows that helper can
create a missing context only when its second argument is true; this provider
gate does not request creation. Other context-initialization entries remain open.

`140985870` subtracts origin supplied by `1409870d0`, checks nonnegative XY and
index dimensions +48/+4c, then returns the slot at index+20. Out-of-range returns
null. The origin uses stored +64/+68 or parent virtual +80/+88 geometry. This is
bounded retrieval from an existing source index. The source-pointer cache does
not establish universal per-cell, per-world or per-landing scope.

The provider callers are resource task workers. Wrappers `1407b5850` and
`14076d140` occupy identified functor vtable slots. Layer request `1407b5a00`
builds a key through `1407c07b0`, acquires a ProcGenLayersDB entry, records a
dependency node and invokes `1407b4bb0`. That preparation gathers base-resource
and bounded neighboring layer dependencies; `1407b55b0` registers a
`1407b58a0` functor with dependency keys. Virtual dispatch reaches `1407b5160`,
which runs neighbor preparation and the provider before publishing task+20.

Alternate resource request `1407a1260` gathers density dependencies through
`1407a8d30` and creates a task through `14076cd40`; dependency constructor
`14076d1c0` retains DensityMapDB handles. Its wrapper dispatches `14076c560`,
which samples four levels using a shared aggregate. Requests can be asynchronous
and cache-mediated; returning from a request does not guarantee the worker
already executed. Actual worker thread/epoch and scheduler behavior in the
captured session remain unobserved. This scheduling evidence is explicit task
construction/registration and virtual dispatch, not an inference from locks.

Entry helpers `1427d4ae0` / `1427d4be0` perform atomic transitions and may use
`WaitOnAddress` with indefinite timeout. Numeric results 0/1/6 distinguish entry
states, not complete geometry. Worker admission `1407c0720` requires a nonzero
discriminator equal to global `145903184` under lock. Key builder `1407c07b0`
requires valid global rectangle/discriminator state and packs coordinate words
with settings. These are concrete initialized-state/epoch dependencies beyond
world identity.

`14079ddf0` clears source-map values and visited entries under the ProcGen lock,
clears related caches and calls resource DB cleanup `1407b4770(1)`. New exports
follow the clear helper and DB cleanup; reset remains an indirect vtable method
through `14079df60`, not independently bound to a particular travel event.
Destruction through `14079d910` is distinct. Neither path establishes a
whole-engine invalidation guarantee or a requirement for player travel.

## Consumption, validity and persistence

Updater RVA `021e07d0` receives initialized state, indexed XYZ/index/domain,
horizontal radius and **separate upper-coordinate scalar**. It internally scans
occupied ProcGen maps and invokes `021e0f50`. The scalar applies to the vertex
branch as vertex Z <= upper; containment and edge branches differ. It is not a
symmetric height bound. [Prior arithmetic specification](dataflow.md) remains
unchanged and spatial native equivalence remains NOT TESTED.

State and prior query history matter. Spatial refresh uses context/displacement;
the mapped guard does not separately compare radius/upper. Missing/unchanged
ATMO or BIOM resolution retains prior collections. Freshly empty geometry,
incomplete producer output, stale caches and retained results can yield different
meanings despite identical final lists. AL means refresh activity, not certified
completeness. Atmosphere is independently resolved from world context; BIOM
contributions are filtered to selected water by the UI. X-Tech's separate
harvester bypass and saved extractor/producer registry are not natural resource
availability oracles.

ProcGen region maps, pointer keys, visited records and operation vectors are
**TRANSIENT runtime state in the inspected ownership path**; the geometry is
computed from definitions/context, so its informational provenance is
**RECONSTRUCTED / DEFINITION-DERIVED**. This does not establish that equivalent
data are absent from every save representation. Seed/key persistence and
authoritative restoration of this cache remain UNCLASSIFIED. Saved location or
extractor lists alone do not supply the demonstrated runtime prerequisites.

## Player presence and the supported boundary

The mapped inner updater accepts a query position rather than substituting
player XYZ. The provider requires current manager context and resident mappings;
the inspected chain does not establish a direct player-presence requirement.
That separates **specified location**, **player location**, **active world**,
**loaded source maps**, **producer readiness** and **availability freshness**.
It does not prove that the engine can initialize another planetary context
independently, or that current-manager state can be replaced by a body ID.

The smallest evidence-supported account is boundary-specific: explicit updater
operands plus valid initialized state, correct resident map/definition/frame
context, and qualified refresh/completion. Natural preview satisfies enough of
this context to produce observed sets; the corpus cannot certify its complete
upstream geometry. Established Workshop setup statically converges on the same
updater, but runtime equality remains untested. An arbitrary center in loaded
geometry is statically expressible, with coverage and freshness still needing
qualification. Separate-context and unloaded-area sufficiency are UNKNOWN.

Outcome B is independently ACCEPTED after documented rework: the positive native dependency
account is useful, while missing lifecycle/geometry epochs prevent a runtime
sufficiency theorem. The [uncertainty register](region-uncertainty.md) names
specific discriminators, rather than treating failed remote demonstration as
failure or claiming that travel is necessary. No live action, game launch,
deployment, save mutation, staging, commit, push or external disclosure follows.
