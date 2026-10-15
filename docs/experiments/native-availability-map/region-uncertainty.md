# Evidence boundaries and discriminating observations

[Answer](region-dependencies.md), [lifecycle evidence](region-lifecycle.md).
These questions are not permission to implement or perform experiments.

| Local key | What is supported / what remains unknown | Why archived evidence cannot decide / discriminator |
|---|---|---|
| RD01 | Current source index bounds and null out-of-range lookup are STATIC. Coverage of a specified radius by resident source maps remains unknown. | 070 omits source descriptors/index extent and complete maps. Need same-epoch requested area, index origin/dimensions, selected sources and generated geometry coverage; distinguishes a true empty region from unprepared sources. |
| RD02 | Source miss synchronously attempts construction under exclusive lock. A map hit or visited key does not certify success/completeness. | Need actual component lookup result, BiomeMapDB entry state, selected descriptors and producer outputs for that source epoch. Distinguishes legitimate empty geometry from prerequisite exit and later cache reuse. No quota of UI repetitions supplies these. |
| RD03 | Reset/destruction clears region caches and visited state; explicit DB waits/publication exist. Exact reset/source-replacement timing versus availability refresh remains unknown. | Need epoch linkage among source object lifetime, reset, task execution/publication and availability scan. Pointer equality or a published aggregate alone cannot establish this join. Static indirect method location does not identify a particular travel event. |
| RD04 | Indexed query position can differ from player XYZ in the mapped consumer; current global context is a real dependency. Loaded no-player-at-center sufficiency remains untested. | Need independently qualified resident coverage/epoch and query/acceptance while player is elsewhere, without changing required context. Failure accompanied by eviction would test residency, not presence itself. Existing preview capture does not isolate the variable. |
| RD05 | Substituting only ProcGen cannot remove global manager reads. Native preparation of a separate planetary context remains unknown. | Need evidence of actual alternative-context creation/selection and the source index, BIOM/component store and task lifetimes it establishes, or a concrete branch rejecting such context. Current-manager code does not prove no other entry exists. No mod/API design is proposed. |
| RD06 | Complete spatial replay and preview/established runtime equality remain NOT TESTED. | Need same-evaluation region arrays/ordered XYZ-width points, translation table, query/scalars, prior query cache, independently observed accept/reject or insertion and resulting set. Established and preview need separately qualified epochs. Final fold agreement is downstream and cannot reconstruct these. |
| RD07 | Runtime caches are constructed/cleared in code; saved-location and producer lists are distinct. Exact seed/key persistence and cache restoration authority remain UNCLASSIFIED. | Existing captures omit component/database keys and source lifetimes. A save-value coincidence would need loader-to-selected-runtime mapping before it supplied the missing context. No new save parsing or modification is performed here. |

## Routes pursued and terminal scope

The provider and producer were reread in full existing exports; direct xrefs
identify two provider callers and one constructor caller. Both provider callers,
their parent task wrappers, neighbor preparation/request, current-key admission,
current-manager context resolution, bounded index/origin, component lookup,
descriptor alternatives, source cell iteration and generator/competition paths
are covered. Existing ownership construction/destruction/reset was followed;
focused new exports cover database acquisition and wait transitions, task
construction/registration and dependency gathering. References and vtables are
reported as indirect evidence, never silently converted into direct runtime calls.

Remaining generic resource-server dispatch internals and every terrain-source
polymorphic implementation are not reconstructed. They are not needed to infer
the **scoped positive dependencies** above, but their unobserved context/lifetime
states prevent a universal minimum-sufficiency account. No whole-engine static
exhaustion or remote impossibility is claimed. RD01–RD06 identify the particular
missing state that bounds runtime conclusions; further synthetic generation
would be self-derived evidence rather than the needed oracle.

Atmosphere, water selection, X-Tech and retained operation state remain separate
branches, as detailed in [dataflow](dataflow.md). Even complete spatial geometry
alone would not supply a complete displayed set without these qualifications.
