# D1 hypothesis and falsification ledger

[Report](report.md), [native windows](native.md), [save/control rows](sites.csv).
Identifiers D1-H1–H4 are local to SOR-EXP-0037. A falsifier addresses the stated
mechanism and measured incident, not every conceivable variation of the bug.
No historical snapshot has an independent failure/recovery label.

## D1-H1 — saved site displacement

| Required element | Evidence / test |
|---|---|
| Mechanism | A changed saved site pair, compensated beacon center or Workshop delta moves the established query relative to otherwise fixed generated veins. PERSISTED inputs feed native descriptor N05 and spatial translation in N07. |
| Distinct prediction | The matched site's saved fields differ across a pair enclosing the displacement. Extractor resource definitions could remain stable. |
| Falsifier | Bit-identical pair, center and delta at the same Workshop identity across the claimed displacement interval. |
| Offline test / actual result | Save38→39 Decaran II/VII-b and Save51→52 Feynman VIII-b: equal Workshop identifiers, body, 16 pair bytes, compensated binary32 center and zero 12-byte delta. Tokens remap and names/equipment may change. Comparisons are in local comparisons.json and sites.csv. |
| Disposition / confidence | **Falsified within the tested snapshot intervals**, PROVEN / SAVE equality. These are not independently labelled incident intervals; a broader explanation of an unobserved earlier/later incident remains untested. |
| Minimum further falsification | For the actual incident, compare the same fields in an already existing, independently labelled immediately-before/after pair. Modest decoding cost using these readers; currently no such labelled pair is supplied. Do not load/resave old inputs under D1. If the saved fields are equal, that actual-interval displacement explanation is ruled out. |

## D1-H2 — failed construction retained as visited

| Required element | Evidence / test |
|---|---|
| Mechanism | N15 inserts a source-pointer entry, synchronously calls void constructor N16, then appends source+68 to visited bookkeeping. N16 has prerequisite early exits. An attempted but incomplete construction can therefore be retained and skipped until reset/replacement. ProcGen/visited data are TRANSIENT in this ownership path; exact seed persistence is UNCLASSIFIED. |
| Distinct prediction | Loss follows a failed prerequisite attempt for the relevant spatial source and persists while the visited/cache entry suppresses a successful retry. Installed extractor configuration remains available. This restricted mechanism predicts loss; it does not itself assign Copper to a former Gold region. |
| Falsifier | For the source implicated by a reproducible loss, establish successful construction before first affected consumption, with no intervening reset/source replacement/failed reconstruction. That contradicts failed construction as the cause of this incident. |
| Offline test / actual result | Primary provider/constructor exports show early exits and unconditional post-attempt bookkeeping, so code does not rule it out. N15's exclusive +40 lock spans construction; N01/N71 traverse under the shared lock. The partial-write race explanation under that same lock is rejected. No saved/native receipt records the affected construction outcome. Decaran II He-3 recognition only controls equipment decoding. |
| Disposition / confidence | **Remains possible with positive STATIC mechanism support; incident occurrence unresolved.** No probability or confirmed cache bug is assigned. |
| Minimum further falsification | First, bounded read-only analysis can trace constructor prerequisite guarantees and all consumer-before-retry paths for the known task callers N25/N38; a proof that a failed attempt cannot reach affected consumption would falsify the mechanism as stated. Existing read-only export tooling makes this feasible, but asynchronous dependency/indirect dispatch closure may require several functions and yield a qualified negative. If static guarantees cannot close it, a separately designed observation of constructor exit branch and subsequent source-key consumption is needed; it needs lifetime/thread qualification and is substantially costlier. No complete geometry snapshot or arbitrary native invocation is assumed. |

## D1-H3 — retained operation list

| Required element | Evidence / test |
|---|---|
| Mechanism | N01 can retain spatial results under its domain/displacement guard and retain atmosphere/biome lists on null or unchanged definition resolution. N31 folds current lists; N34 tests produced-resource intersection with a property-selected list. A wrong retained list could change displayed/build-menu eligibility without changing underlying ground geometry. These are TRANSIENT operation caches, separate from ProcGen source maps. |
| Distinct prediction | For the restricted **list-only** explanation, the ground resource remains at the same point while Available Resources or category eligibility disagrees. Ordinary gas/solid bases in the curated controls have no special source/bypass keys. Installed definitions can remain unchanged. |
| Falsifier | At a reproduced failure, the required ordinary resource is correctly present in the consumed area list and ordinary category remains available, while the fixed ground location's scanner identity/placement eligibility changes. That rules out missing/retained area-list membership as the sole cause. |
| Offline test / actual result | Guard/retention edges and selected-list gate are directly present in exports. All 22 curated bases select the ordinary spatial branch under the resolved-property contract. Existing 070 final-fold agreement concerns Kreet unplaced preview, not these mature failures; it does not falsify stale upstream values. No affected UI/ground pair exists offline. |
| Disposition / confidence | **Remains possible with positive STATIC mechanism support; affected execution unresolved.** Cannot explain a verified changed ground type by itself. |
| Minimum further falsification | A separately authorized ordinary game procedure at one current, matched site: record area list, continued build-menu eligibility of the same ordinary solid extractor, a fixed ground scanner point and an unplaced extractor preview; repeat at the same landmarks after loss. Prefer Gold/Copper, with a nearby stable mineral point; record He-3 separately because a merged atmospheric entry cannot certify spatial gas membership. Continued eligibility of the same ordinary solid type plus changed local ground/placement behavior challenges the list-only model at low cost. If menu behavior cannot establish that the same N34 branch passed, the decisive native version needs a separately qualified scalar observation of that gate's resolved source and return at the failing placement. Existing exports identify those operands; no complete region capture is needed, but new observation still requires engineering/review and approval. A nonreproducing attempt decides nothing; screenshots alone do not prove map equality or the native branch. |

## D1-H4 — changed generation inputs

| Required element | Evidence / test |
|---|---|
| Mechanism | Restricted candidate: N16/N18/N19 select a different component/BIOM/RSGD descriptor chain or ordered resource candidates on reconstruction, changing local type allocation. N20/N21 consume these choices before point generation and competing-resource rejection. Geometry is RECONSTRUCTED / DEFINITION-DERIVED; descriptor-selection persistence is not established. Other key/frame/bounds changes are acknowledged alternatives, not folded into an unfalsifiable catch-all. |
| Distinct prediction | The consumed BIOM/RSGD selection or ordered resource descriptors differ across successful constructions associated with changed local resource type. Installed extractor identity need not change. |
| Falsifier | The actual selected descriptor identities, values and candidate order are equal across successful constructions for the corresponding source while independently observed ground type changes. That rules out descriptor-selection change as this incident's cause, even if other generator operands differ. |
| Offline test / actual result | Saved pair/center equality eliminates those changed inputs within sampled intervals, but does not cover source selection, descriptor order or runtime translation. Existing generation exports explicitly show the additional dependencies. The archived-input boundary lacks a joined affected construction. Feynman has Copper and Gold equipment in both saves; this is no geometry/type-transition oracle. |
| Disposition / confidence | **Unresolved due to unavailable evidence**, with a concrete STATIC dependency mechanism. No evidence of actual reseeding, shuffled type assignment or different historical descriptor choices. |
| Minimum further falsification | After ordinary gameplay reproduces the discrepancy, a separately qualified scalar/identity observation of natural N18/N19 selection and N20 traversal can compare selected BIOM/RSGD/resource IDs, consumed descriptor scalar values and candidate order for the same source coordinates before/after reconstruction. Include completion/early-exit branch records and a nearby resource point that stays stable; independently record changed ground type at fixed landmarks. These boundaries and descriptor layouts already exist in exports; copying numeric IDs/scalars at their natural uses avoids retaining region point arrays or rebuilding the game. It still needs new thread/lifetime/source-pairing qualification and observer approval, so feasibility is a concrete engineering route, not a ready or proven-safe instrument. Moderate-to-high cost; do not commission until a reproducible manual case exists. This test need not capture every geometry operand, and cannot settle other generator variants. |

Discarded as unmotivated causal claims: depletion without a native depletion path;
power cycling as a remedy without a controlled native power→region dependency;
shader Pipeline.cache deletion as a ProcGen reset; universal random seed replacement;
and “all lists equal visible vein geometry.” Public suggestions supply no such
native link. Production/placement separation is a supported architectural
distinction, not an independently established root cause.
