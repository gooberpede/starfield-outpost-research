# D5AE eligibility and readiness

2026-11-02. All addresses are preferred static VAs for Starfield 1.16.244.0,
image base `0x140000000`; RVA is VA minus that base. Member offsets are bytes.
[Sources](d5ae-sources.csv), [inherited input provenance](d5ad-input-provenance.md),
[saved-state matrix](d5ad-save-state-matrix.md), [load chronology](d5ad-load-chronology.md).

**A request needs several kinds of readiness. Source metadata at the Lodge
does not establish that every destination task or raster is ready.** Startup
admission and protected context installation order their own writes; later
task dependencies can still make one competing request runnable before another.

| Boundary | Native predicate/order | Effect on competition |
|---|---|---|
| Startup definitions | `0x141893ee0 → 0x141883440 → 0x1405994a0`, postlink `0x14059ac20`; counted jobs and final graph wait precede module setup. | Ordinary admission cannot treat merely submitted definition jobs as complete. Effective overrides/settings remain inputs. |
| Resource-slot population | Module `0x14094e3d0`, enumeration call `0x14094ef57`, callback `0x14077c470 → 0x140779610`, direct initializer call `0x1407796d2 → 0x140779760`. | CTPerBiomeData root/slots are initialized through this startup path; they are distinct from queued saved-world scalar components. |
| Startup admission | Worker `0x14187f9d0` calls initialization at `0x14187fa0f`, signals event at `0x14187fb52`; ordinary pending-load wrapper `0x141898210` calls event wait `0x14187fbd0` at `0x141898237`. | This is a real ready-before-admission edge. The already-completed guard and full-reset path retain their predicates. |
| Context/owner/descriptor | `0x14078b030` drains prior work, takes manager `+0x24` exclusive and uses mode `+0x20 = 1` during owner/landscape installation. `0x14078af30` drains service work and calls `0x14078bc30`. | Ordinary AcquireHandles requires manager reader admission and mode 2; half-installed context is not an eligible prewarm state. |
| Demand admission | `0x1407b2390`: global `0x145e903a8` enabled, false `0x1403473a0` state test, manager reader admission, mode 2, nonnull `0x14078c4e0` context, resolved owner form-type admission and terrain focus-valid `+0xe0`. | A focus write or interior residency alone cannot create eligible resource work. |
| Source/Grid | `0x1407847b0 → 0x140785190`, finalization `0x140983270`; source creation `0x140982d90`. Provider locates actual cell/contributors and requires source BIOM. | Failed setup can suppress target selection; source publication alone does not construct a population. Different source/owner allocations change identity. |
| Preparation and files | Rectangle preparation, layer preparation, file handles and density dependencies feed registration `0x14076cd40`. Pending dependencies and node states gate activation. | Real overlapping readiness can change which request reaches arbitration first. A parent wait does not order all density jobs. |
| Discriminator and aggregate | Density worker `0x14076c560` validates work and uses the entry's current aggregate; `0x1407a1940` calls provider for level zero. | Stale work may cancel; a populated aggregate bypasses provider entirely. Warm request keys deduplicate rather than create independent trials. |
| Visit and map | Source token `+0x68` is tested under shared ProcGen `+0x40`, then exclusive pointer-map lookup occurs without a second visited check. | Several requests may already have passed visited. First protected constructing miss determines authority. |
| Generator metadata | `0x140771f30` tests body/keyed range/BIOM match; `0x14079b6e4` branches out on failure. | This is after holder insertion: failure can produce an empty attempt, not transfer authority to a waiter. |
| Raster | `0x140478a30` entry acquisition; `0x1427d4be0` waits/claims; generator calls loader at `0x14079b770`, updates state/wakes, then samples at `0x14079b8e8`. | Deferred synchronous loading is permitted after authority. It delays the owner and waiting requests. Ready or claimed-load results permit continuation; refusal/fallback has its documented scope. |
| Definitions at use | Resource resolution `0x1405de3b0`, IRES/RSGD types, derived dictionary and effective rarity settings feed generation. | Missing/invalid definitions and unsuccessful geometry remain distinct from scheduling authority. No unsafe half-initialized object is treated as a normal fixture. |

## D5AD handoff and contrary cases

D5AD's saved type-3 PlanetWorldSpaceData/GameDaysPassed restoration is queued;
its finish command does not wait for every component command. That fact does
not prove a resource-slot initialization race: the component types and owners
are different. The storage reader `0x142404230` supplies phase consistency,
not a blanket queued-command drain. PCM's persisted seed/content/placements
can affect preparation through their own consumer gates; they are not restored
ProcGen holders or visited tokens.

For ordinary startup, initial definition/module work is separated from later
per-request file/placement/density work. A delayed prerequisite before dispatch
can allow B to reach arbitration while A remains pending. Delaying raster
loading inside A's already-held exclusive interval cannot do that: B may have
passed visited but cannot decide the same map until A unlocks. If A returns
without geometry and successfully appends the token, a new B can bypass visited;
an already-passed B instead reaches a map hit. These are explicit compiled
branches, with separately labelled native helper and synthetic controls.

Historical B2 loader timing remains unmeasured. Its Lodge prefix has 383
source births/publications and zero provider records, followed by a second
reset and further Grid work. This supplies no all-input readiness snapshot.

Fresh D5AE export02 closes the enumeration question: `0x140593280` holds the typed form-list reader, synchronously calls callback virtual `+0x10` at `0x1405932ef` for each nonnull form, and returns only after that loop and unlock. The PNDT callback returns one after direct initialization, so it does not terminate this enumeration early. Component maintenance `0x1407873d0` precedes it in module setup and is not substituted for resource-slot population. Together with the startup event wait, this proves the pertinent ordinary initial slot-population-before-load-admission edge. It does not certify later file/raster readiness.
