# D5V native lifecycle and consumer map

[Report](d5v-report.md), [coordinate contract](d5v-coordinate-contract.md),
[function/export hashes and exact line ranges](d5v-sources.csv),
[lifecycle figure](d5v/lifecycle.svg). All VAs are preferred static image addresses
for 1.16.244.0, image base `0x140000000`; member offsets are bytes. Semantic names
are research aliases unless an original symbol is explicitly identified.

## Construction and ownership

| Edge | Native operation and decisive sites | Conditions, ownership and consequence |
|---|---|---|
| Current manager → ProcGen | Constructor `0x140787830`, stores/registration `0x1407886e4..0x140788766` | ProcGen pointer at manager `+0x130` is also appended to module vector `+0x170/+0x178`. This joins indirect reset dispatch to the actual population owner. |
| Initialization → request | `0x14078b030` drains at `0x14078b077`; creates landscape at `0x14078b936`; completion `0x14078bc30` dispatches module `+0x40/+0x48` | Descriptor/owner setup and valid streaming/component/file state precede demands. RuntimeService `+0x48 = 0x1407b2370`; `+0x70 = 0x1407b1fe0`; both reach handle acquisition. Exact registration/queue prerequisites remain [D5S](d5s-query-winner-model.md). |
| Worker → provider | Layer `0x1407b5160`, call `0x1407b526a`; density builder `0x1407a1940`, call `0x1407a1a3c` | Layer prepares neighbors first and holds manager reader; density aggregate `+0x08` reuse skips provider. Detached density does not inherit that reader. |
| Provider → selected source | `0x14079f860`, cell lookup `0x14079f92c`, emitter call `0x14079f9ca`, selected pointer `0x14079fa90` | Invocation retains Grid; emitted entries/chunks contain raw source pointers. Retaining Grid is not retaining each source through retirement. |
| Selected source → visit/lookup | `0x14079fc37..0x14079fcd4` | Source BIOM nonnull; shared visited array compares source `+0x68`. Visited false leads to exclusive ProcGen `+0x40` and full source-pointer lookup. |
| Miss → generation | Insert `0x14079fdf9`; generator `0x14079ff18`; visited append `0x14079ff3e`; unlock `0x14079ffa5` | Exclusive interval includes synchronous generation. Hit skips it. Visit marking does not check complete geometry success. |
| Wrapper → copied regions | Wrapper resource slots `+0x20`, capacity `+0x28`, stride `0x18`; region append `0x1407ac2f0`; point copy `0x1407ac0d0` | Resource key is u32 FormID; slot `+0x08` retains 24-byte collection. Collection `+0x08/+0x0c/+0x10` gives count/capacity/data; 48-byte regions own 16-byte points. Temporary generation storage is separate. |
| Retained holders → teardown | `0x14079ddf0`, `0x14079d910`, `0x1407aa8a0`, `0x1407aab10`, `0x1407ac260` | Reset/destruction releases wrappers; final references release collections and nested arrays. Rehash can move slots without regenerating region content. |

## Action/state transition matrix

"Can" means the branch permits that effect; "must" is conditional on every
listed predicate, not a measured gameplay frequency. A completed demand still
requires valid inputs and successful allocations/copies.

| Ordinary action/state contract | Native edge and predicate | Population effect / regeneration implication |
|---|---|---|
| First demand after empty initialization | Provider: valid Grid/source/BIOM, visited false and source-pointer map miss; generator component/raster prerequisites pass | Must attempt generator under exclusive protection. Successful nonempty population is a separate outcome. |
| Same source selected again, visited hit | Source `+0x68` present in ProcGen count/data `+0x48/+0x50` | Must bypass this construction block. Does not establish successful old geometry or even retrieve a wrapper. |
| Unvisited lookup hit | Existing pointer-map slot under exclusive lock | Must retain/release existing wrapper locally; no generator in that branch. Empty/partial holders are also hits. |
| Subsequent aggregate level | Density aggregate `+0x08` already nonnull | Skips provider entirely; different from source-map lookup. |
| Focus moves below shift threshold | `0x14078c5f0`: mode 2, no active blocking transition, both absolute displacements below setting-derived threshold | This movement branch does not shift/reset the source map. Separate new demands can construct previously unvisited sources. |
| Focus crosses threshold | `0x14078c5f0 → 0x14078c060 → ShiftToTask 0x14078ce00`; exclusive manager ownership; module `+0x50/+0x58` | Landscape shifts ordinary/overlay Grids. ProcGen shift slots are no-ops. Overlapping source populations can remain; no blanket regenerate-on-movement rule. |
| Source exits shifted Grid coverage | `0x140986da0 → 0x140988100 → 0x140982b70`; retirement predicate `0x140987080` negates overlap | Must remove a present source-pointer map entry and release source. Does not clear visited array. New generation is not implied. |
| Same content source reappears without broad reset | New source from `0x140982d90`, content-derived `+0x68`; old visited identity still present | Must bypass construction if the identity compares equal. Different pointer alone does not force generation. This is conditional native semantics, not a claimed observed return. |
| Broad manager reset / context departure | `0x140788e70`: drain, manager exclusive, module `+0x10`, then `+0x18`; false variant `0x140789850` uses same reset slots | Landscape `+0x18 = 0x1407846d0` releases Grids. Registered ProcGen `+0x18 = 0x14079df60 → 0x14079ddf0` clears map and visited. Subsequent qualified demand can construct afresh. |
| World component release | `0x14078cf00`: current owner nonzero and qualifying current world's component differs from supplied component | Calls broad reset. Without that predicate, cleans retained world references instead; do not infer reset from every call. |
| Owner/descriptor installation | `0x140789ce0`: zero owner resets; changed owner resets existing nonzero context; same owner tests current component versus incoming descriptor component | Reset/reinitialization branch is selected by real owner/component inputs, not just body/name equality. Entry via `0x14078b030` rebuilds landscape. |
| Loading/reloading | Load `0x141815620` calls drain; phase dispatcher `0x141827960`, case 3, guard `!byte[0x145e8fd70] || phase_flag`, calls `0x1407895a0 → reset`; world teardown `0x141896280` separately drains/resets | Drain alone means work completion, not population readiness. A taken reset clears stores. Existing outpost centre/producer restoration does not prove geometry is already present at load completion. |
| Manager replacement/new process | Manager destructor `0x140788bc0`, call ProcGen destruction `0x140788d5e`; bootstrap constructor is conditional on singleton absence | Old process allocations do not persist as pointers. New manager initializes empty stores; reconstruction from inputs is separate from any unjoined alternate serializer. |
| Workshop area refresh / selected candidate movement | `0x1421e07d0` versus `0x140f7c290` | Recompute consumer answers from resident geometry; neither inspected scan calls the generator. These operations alone do not invalidate source geometry. |

Grid destructor `0x140982930` reaches clear `0x1409829b0`; the extra derived
deleting destructor is not an arbitrary standalone clear caller. Clear removes
map entries and frees sources without locally clearing visited. Source retirement
and generic clear are therefore separated from broad reset. D5S's detached-density
counterexample remains: ordinary movement can retire a raw selected source before
that invocation's later map lock. This bounds lifetime guarantees without claiming
a retail race, current use-after-free or missing-resource bug.

## Native geometry → area, catalogue and extractor decisions

| Consumer | Exact data/control path | Semantics and independent dependencies |
|---|---|---|
| Area query setup | Preview `0x1421b41f0 → 0x140b4cee0`; established `0x1421b2570 → 0x140f4a140`; both call updater `0x1421e07d0` | Indexed XYZ/domain plus radius and upper scalar; preview and established setup differ. Existing captures do not make every established descriptor observed. |
| Spatial refresh | `0x1421e080f..0x1421e0960`; scan `0x1421e09d4..0x1421e0aa5` | Domain/translated displacement guard; radius and upper not separately compared locally. Shared ProcGen lock, occupied source slots. No provider/generator call. |
| Source/region area callback | `0x1421e0f50`: typed IRES resolution `0x1421e1012..0x1421e1027`; translation `0x1421e1091..0x1421e10fb`; acceptance/set insertion `0x1421e1772..0x1421e18b3` | Every passing resource can be inserted; pointer deduplication, not single-resource priority. Broadphase/count/strip/vertex/edge branches differ. Invalid form resolution skips the entry. |
| Atmosphere/biome caches | Updater `0x1421e0c61..0x1421e0eff` | Nonnull changed identity replaces relevant list; null/unchanged can retain it. Biome declarations are not generated vein membership. |
| UI area rows | `0x141578500`, union `0x1421f8120`; selected Water filter | Spatial + atmosphere union; selected biome Water appended separately. Queued model command reads then-current ranges, without an immutable producer snapshot. |
| Catalogue eligibility | `0x1415796f1..0x141579716 → 0x1421f68f0`; property selectors `0x1421f6ad0..0x1421f6b9a` | PlaceAnywhere bypass; SkipVein selects biome declaration list; atmosphere selects atmosphere; ordinary selects spatial. Further organic/recipe/category conditions remain. [Prior primary ledger](../resource-ui-oracle/dataflow.md). |
| Natural extractor location | Final placement `0x140f3f9a0`: qualifying `0x140f7c9f0`, excluding relevant bypass properties, calls `0x140f7c290` at `0x140f3fd5f`; empty intersection sets status `0x17` | A catalogue entry does not prove location admission. Territory/collision/support and later status assignments still apply. |
| Candidate resource query | `0x140f7c290`: atmosphere property branch copies ATMO; ordinary copies reference `+0x8c/+0x94`, calls `0x14079df70` at `0x140f7c408` | This is a point query, not a 150-unit area query. Current valid exterior world context is required. |
| Point traversal/predicate | `0x14079df70`, call `0x14079dff2 → 0x1407affb0`; call `0x1407b00db → 0x142346b30` | Shared ProcGen protection; resource collections retained during traversal; typed resource resolves. Any passing region appends that resource if absent. No winner priority excluding another matching resource. |
| Produced-resource association | `0x140f7c421 → 0x1409e8700 → callback 0x1409ea530 → 0x1409e8950` | Enumerates AVIF forms of property class 9, excludes disabled property flag, requires resource pointer `AVIF+0x148`; checks reference/instance/base property lists and value/default/keyword conditions. Candidate effective state, not name, selects produced resources. |
| Final resource intersection | `0x140f7c443..0x140f7c4b6` | Sort both pointer vectors, append equal pointers. One overlap suffices for nonempty result; there is no resource abundance estimate here. Unit production and power/time/storage gates are downstream and separately documented in [inorganic production](../inorganic-extractors/native.md). |

The default-property names in the catalogue/placement discussion inherit the
existing native/default-object evidence, not string guesses. Numeric globals
`0x145f0a6b8` (PlaceAnywhere), `0x145f0a710` (SkipVein) and `0x145f0a3a0`
(atmosphere selector) are build-bound slots. Their selected effective AVIFs and
candidate values can change without changing source geometry. The produced
resource association is an AVIF relationship, not evidence that a placed machine
is running, powered or currently generating inventory.

## Stability contracts and discriminating controls

| Mechanism | Sufficient scoped stability contract | Counterexample / limitation |
|---|---|---|
| Construction winner | Same actual admitted constructing query, source/owner epoch and prerequisite order | D5S native queue continuations produce different eligible first queries. Registration order alone is insufficient. |
| Generation | Same complete effective definitions, query sample, seed/frame/order/geometry/allocator premises | D5T/U show different fixed-domain populations for reachable alternatives; equal weights suffice only with other inputs fixed. |
| Retention | Same live owner/map holder, no erasure/reset/replacement, valid lifetime | Broad reset releases it; retirement differs from clearing visited. Pointer equality after teardown is not continuity. |
| Area membership | Same complete resident regions, translated query, radius/upper, effective definitions and actual refresh state | Fixed one-point region: query at X=3 rejects at radius 0 and accepts at radius 150. The point gate rejects there. Original instructions verify this finite control. |
| UI/catalogue/placement | Same relevant operation cache, properties, produced resources, asynchronous observation and additional admission gates | Area rows, catalogue membership and point placement use different native rules. Equal available identities can coexist with different geometry. |

No measured probability, schedule frequency, universal return invariance or bug
attribution follows from these contracts. The two Feynman V figures test the
area-membership implication directly; they do not select historical winners.
