# D5B proposition reconciliation

[Report](report.md), [native evidence](native.md), [pins](sources.csv).
DEMONSTRATED means direct code or qualified observation proves the stated scoped
proposition. CONTRADICTED requires decisive incompatible evidence in that scope.
PLAUSIBLE-BUT-UNPROVEN has a concrete compatible mechanism with an unobserved
premise. UNRESOLVED has no decisive support or refutation in the inspected paths.
These categories describe claims, not publication clearance or complete coverage.

| Proposition | Disposition and evidence | Falsifier or missing discriminator |
|---|---|---|
| Collection retains region populations beyond the initiating provider call | DEMONSTRATED / STATIC for the mapped source slot, nested retained collections and deep point copy. [N03, N07, N08, N12, N13](native.csv). | A different actual ownership chain or a release removing map ownership would contradict this scoped transcription. Other owners are outside the claim. |
| An existing population can be reused without rerunning the generator | DEMONSTRATED / STATIC: provider hit bypasses construction; consumer scans resident map directly. [N01, N03, N04](native.csv). | Show a mandatory generator call on that hit/scan path, or that the consumer accesses a different map. |
| The collection key fully identifies population contents | CONTRADICTED if this means an explicit complete recipe key: the hash/equality key is only source pointer. UNRESOLVED if it means source lifetime implicitly guarantees immutable recipe/contents. [N03–N05, N15](native.csv). | Establish source-lifetime/context invariants, or observe one source epoch with differing populations. Query/mask omission alone does not prove a retail collision or mutation. |
| Selected population is present when Save52 load completes | UNRESOLVED. D5B consumption is later; [Phase B](../resource-combined-acquisition/phase-b.md) lacks a native load-completion timestamp and population read there. | Qualified load-completion boundary plus coherent target-source presence or absence, before travel. |
| Selected construction occurs during Save52 load | UNRESOLVED. Task-to-provider calls are STATIC; load-to-selected-task execution is unjoined. [N11](native.csv). | Source/owner/lifetime-bound construction between qualified load begin and end; distinguish earlier process state and later demand. |
| Generated geometry is serialized | UNRESOLVED. [Targeted search](native.md#save-and-initialization-scope) finds Workshop object rows, not a joined region serializer. | Stream operations reading/writing actual population arrays with a restoration join; a failed search or matching regenerated output is insufficient. |
| D5B consumed a previously retained source | DEMONSTRATED only in the immediate sense that the callback reads a stored map holder. PLAUSIBLE-BUT-UNPROVEN for reuse from an earlier provider invocation/load/travel epoch. [N01–N03](native.csv), D5B ACCEPTs 12901/12906/12907. | Observe insert/construction/return and uninterrupted population lifetime to consumption, or observe a different restoration/replacement path. No minimum age follows from a stored holder. |
| D5B's historical construction sampled mask 3 | PLAUSIBLE-BUT-UNPROVEN. [Three exact comparisons](../resource-combined-acquisition/phase-b.md) match mask 3, but the constructor query and sampler return were not captured for this source. | Capture historical invocation or an adequately witnessed new construction; current output equality cannot recover an unobserved historical argument. |
| Two initial queries can yield different retained geometry for the same source | PLAUSIBLE-BUT-UNPROVEN for retail. Native query-dependent construction plus retained pointer-key map and [D5A alternatives](../resource-construction-mask-selection/report.md) support the conditional mechanism. D5B fixtures are synthetic engineering evidence only. | Demonstrate two reachable first queries selecting the same live source identity in separate controlled epochs and differing completed native outputs, with controls against context/definition changes. |
| Cache/retention could explain VIII-b substitution | PLAUSIBLE-BUT-UNPROVEN. Reset/reconstruction is a concrete candidate; the [historical account](../disappearing-deposits/report.md) does not bind its initiating event or population epoch. | Observe stable versus changed source/recipe/geometry across a specific transition; distinguish overlay retention, source change and definition change. No bug reproduction occurred. |
| Every area query necessarily constructs the population afresh | CONTRADICTED / STATIC for the inspected callback: it scans the resident map and does not call the provider. [N01, N02](native.csv). | A mandatory construction edge in this actual scan would refute the scoped conclusion. Separate earlier construction is compatible. |

The complete supported range for Feynman V includes population creation before
load completion, during later travel/demand, or in a missed construction window;
restoration/reconstruction through an unjoined path; and replacement before the
accepted scan. Retention may span provider calls, but its historical duration
here is unknown. The native code excludes a requirement to generate inside each
area callback; it does not exclude a freshly constructed population being read.

D5B's 36 generation entries, 108 resource calls and 36 provider returns are
sampled observations, not a complete selected-source chronology. Its zero
qualified target-source construction chains are an acquisition non-hit, not an
observed native miss, hit, absent construction or absent population. The two
explicit schedule changes leave lifetime coverage gaps even with zero transport
LOSS records. Native sampled mask, first query, population epoch and prior cache
state remain UNKNOWN. The seven indeterminate Save52 associations are unchanged.

The [next-run draft](next-run-draft.md) separates presence-at-load, constructor
timing and geometry persistence. They require different evidence and cannot be
collapsed into one successful consumer observation.
