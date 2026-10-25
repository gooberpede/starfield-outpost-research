# Native construction demand register

[Report](report.md), [exact content pins](sources.csv). All VAs are preferred
static addresses on Starfield.exe 1.16.244.0, image base `0x140000000`, SHA-256
`7e9adb1414a8e1b325e5e1f097b9b17b78deb7eebeda37a333351a43a60f9d28`.
Subtract the base for RVA. Object/member offsets are bytes. Analysis `FUN_`
labels are not named engine interfaces. Raw exports remain LOCAL-ONLY.

Fresh exports are under `.local-work/workshop-population-rework/specialist/`,
named `d5d-demand01.tsv` through `d5d-demand05.tsv`. Each includes instructions,
complete decompilation for selected functions, requested xrefs and END. Xref
lists distinguish code calls from exception/unwind or packed data references;
an address appearing in data alone is not a caller. The exploratory data read
at `0x145499880` in export02 contains packed words, **not** a demonstrated vtable
or dispatch edge. The scoped register below does not use it.

| ID / operation | Caller → callee / decisive condition | Evidence and classification |
|---|---|---|
| N01 source lookup | Provider `0x14079f860`: BIOM required; shared visited check on source `+0x68`; exclusive ProcGen `+0x40`; call `0x1403499f0` at `0x14079fccb`; compare result/capacity at `0x14079fcd0`, branch `0x14079fcd4` | Inherited `resource-milestone-b-producers-01.tsv`, independently read here; [D5C](../resource-population-lifecycle/native.md). PROVEN STATIC: visited skip, map hit and miss are three distinct paths. |
| N02 construction/reuse | Miss target `0x14079fd02` allocates wrapper, inserts via `0x1407aa5f0`, converts original query and calls `0x14079b520` at `0x14079ff18`. Hit `0x14079fcd6..0x14079fcfd` retains slot holder and bypasses generation | Same primary export; [D5C ownership](../resource-population-lifecycle/native.md). PROVEN STATIC; producer prerequisite exits mean insertion/return is not successful nonempty geometry. No D5D retail branch observation. |
| N03 layer worker | `0x1407b5850` → `0x1407b5160`; latter prepares neighbors via `0x1407a0fa0` at `0x1407b524c`, calls provider at `0x1407b526a`, then publishes aggregate task payload | Export05 plus inherited `resource-availability-ui-32.tsv` and `resource-region-dependencies-02..06.tsv`. STATIC direct call plus registered functor dispatch. Construction is synchronous inside the provider, while the request-to-worker edge is task mediated. |
| N04 lower-level worker | `0x14076d140` → `0x14076c560`; four levels 0–3 call `0x1407a1940`; aggregate-absent branch calls provider at `0x1407a1a3c` | Export05, inherited `resource-availability-ui-31/32.tsv`. PROVEN STATIC conditional construction reachability; aggregate reuse is not a source-map hit. |
| N05 demand registration | `0x1407b5a00` acquires keyed layer entry; only acquisition result 1 calls `0x1407b4bb0` at `0x1407b5b4e`; latter requests base/neighbor resources and registers through `0x1407b55b0` at `0x1407b506a` | Export01/05. `0x1407b55b0` installs `0x1407b58a0` functor and dependency edges; table `0x144b406b8` method `+0x10` dispatches N03. Existing dependency ledger supplies that table pin. A request can reuse an entry without scheduling a new worker. |
| N06 dependency acquisition | `0x1403625e0` forms current-discriminator coordinate key, acquires entry, registers dependency only on result 1, requests N05 at `0x140362726`, links via `0x1407b5dd0` | Export01 complete body. Upstream coordinate demand can reach N03 without a Workshop argument. Server entry acquisition is distinct from ProcGen source-map lookup. |
| N07 rectangular demand | `0x1407a1580`, owner `manager+0x80 != 0`, registers/waits for preparation then loops inclusive XY rectangle and calls N06 at `0x1407a17c8` | Export02. This supplies a concrete demand operation beyond a function-pointer name. |
| N08 cell preparation route | `0x140aed020` outer guards: object `+0x48` bit 0 clear, global `0x145f60c10` zero, object `+0x20 & 0x2400` clear, and `0x140ad3410` false. Calls manager preparation `0x14078c940`; copies the original object `+0x58` coordinate pair (or default) at `0x140aed0a9..0x140aed0b1`; calls N07 at `0x140aed393` with that original pair as both min/max. The `0x14078d7b0` conversion feeds a separate CellRefDB key, not N07's coordinate | Export03 full body and export04 callers. STATIC coordinate extraction/request ordering; STRONG cell-preparation interpretation. No player Build Mode or Workshop requirement in this body. It also coordinates CellRefDB work. |
| N09 cell callers | `0x140afb220` calls N08 at `0x140afb6ed`; `0x140bbb170` calls N08 at `0x140bbc380`, then separately queues `DynamicNavMeshTaskStitchCellEvent` | Export03 xrefs/export04 full bodies. These are concrete cell/reference preparation operations, not evidence that every travel or save load takes them, nor a saved-outpost enumerator. Full surrounding streaming subsystem is outside scope. |
| N10 neighboring coordinate demand | `0x140363b80` → `0x140360120` at `0x140363bca`; builds 3×3 neighborhood, center → `0x140360310` at `0x14036021d`, eligible neighbors → `0x1403605e0` at `0x14036028e`; result-1/nonnegative flag routes → `0x1403615d0` → N06 at `0x140361615` | Exports02–05. PROVEN STATIC neighborhood/dependency route. Negative flag takes cancellation/release path rather than ordinary request; native packed neighbor eligibility and current discriminator are material guards. No remote outpost list is consumed here. |
| N11 bounded region task | `0x1407b1420` calls `0x14079d080` at `0x1407b1433`; descriptor/discriminator match `0x14079cd50` and nonzero owner gate `0x1407af970`; rectangle loop calls N06 at `0x1407af9d0` | Exports02–05. Table `0x144b3f1c8 +0x10` points to `0x1407b1420`. Task dispatch is STATIC indirect linkage; originating gameplay event remains unknown. Stale descriptor/discriminator fails the gate. |
| N12 density/neighbor preparation | N03 calls `0x1407a0fa0`, which requests four neighbors via `0x1407a1260` at `0x1407a1050`; N05 also calls it at `0x1407b4e8b`; density requests `0x1407a8d30` and registration `0x14076cd40` at `0x1407a141b` lead to N04 | Export01 and inherited dependency exports. DensityMapDB handles and resource-server dependencies are distinct stores. This is another path to provider construction, not a direct linear call stack through the scheduler. |
| N13 Workshop consumption | `0x1421e07d0`, occupied-source scan `0x1421e09d4..0x1421e0a77`, callback `0x1421e0f50`; query guard may reuse operation vector | Inherited `resource-availability-ui-15/16.tsv`. Independently read; shared ProcGen `+0x40` scan, no provider call in this scan. Workshop evaluation can consume populations made by earlier ordinary demand. |
| N14 load/bootstrap limits | Workshop loader `0x140f50880`; Main constructor `0x141881660`, singleton-null manager creation `0x141881f3d..0x141881f56`; owner constructor/destructor `0x140787830`/`0x140788bc0` | Inherited `d5c-load02.tsv`, `d5c-init03.tsv` and D5C native account. Loader rows are not a joined region restore; bootstrap creation is not population construction. No newly demonstrated saved-game → distant-outpost source request. |

N07/N08 make terrain/cell preparation a positive ordinary-demand candidate;
N10/N11 show coordinate neighborhoods and bounded background requests. Landing,
travel and worldspace transitions plausibly drive such preparation, but **their
exact event-to-request bindings are not proved here**. Current-manager fields
and source-index enumeration determine which live sources are eligible. These
operations do not imply that all outposts on the current or another planet are
visited, enumerated or generated.

The meaningful earliest native construction boundary is N01/N02 for a source
actually enumerated by a request. Source descriptor construction/index creation
precedes this, but does not allocate the generated resource population. The
manager is bootstrap-owned; its ProcGen reset `0x14079ddf0` and destruction
`0x14079d910` can end retention independently of pointer-value reuse. A new
request, aggregate state, visited identity, source pointer and manager lifetime
must therefore be recorded separately.

Save-load can prepare the player's loaded cell through ordinary mechanisms;
that is a conditional explanation, not an observed D5B sequence. Within the
bounded paths above there is no positive join from saved remote Workshop rows
to N07/N10/N11 requests for the selected Feynman source. Geometry deserialization
and alternate indirect demand remain unresolved. Neither a global absence proof
nor eager Save52 population follows from this finite trace. These mechanisms
are OBSERVED-INTERNAL, not validated mod integration points.
