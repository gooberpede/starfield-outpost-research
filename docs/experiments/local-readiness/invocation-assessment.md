# Controlled invocation — assessment only

**Current disposition: NO-GO for the proposed passive live session.** [Reassessment](scientific-value-reassessment.md) is separate from the unchanged recommendation below that controlled invocation is premature. No invocation or redesign follows from either assessment.

Recommendation: **premature** for all three boundaries. No invocation interface,
synthetic target submission or native calls were implemented or executed.
[Native register](../native-availability-map/functions.csv),
[requirements](../native-availability-map/region-requirements.md) and
[exact lifecycle evidence](../native-availability-map/region-lifecycle.md) control
the build-specific claims below. ABI spellings are internal observations, not
validated standalone contracts.

| Boundary | Possible scientific gain | Known prerequisites / unknowns and risks | Smallest useful later test / recommendation |
|---|---|---|---|
| 021e07d0 updater | Separate actual query-position dependence from natural caller selection | Four explicit channels include two floats and initialized mutable cache; hidden current manager/ProcGen, translations, ATMO/BIOM, allocation and locks. Thread affinity, safe owned state creation/destruction, full coverage/epoch and standalone effects UNKNOWN. Mutates state, may retain results; calling it is intervention. | First qualify an independently owned initialized state, actual resident inputs/epoch and an independently observed natural result at a matched descriptor; only then propose one matched-descriptor comparison with explicit side effects/failure categories. Premature: the current final UI fold cannot serve as an oracle for missing geometry or freshness. |
| 00f4a140 descriptor builder | Determine how an existing Workshop produces its center/radius/upper bound when natural refresh is hard to trigger | RCX initialized output, RDX resolved Workshop; reference lifetime, components/settings and early-status paths. Ownership of initialized output and any retained references, valid calling thread and off-natural-sequence preconditions not qualified. Global resolution may change outcomes. | Observe natural builder status/output/lifetimes first; later a matched existing Workshop descriptor could have an independent natural oracle. Premature: current observer only samples downstream actual updater arguments. |
| 0079f860 provider /0079b520 construction | Distinguish source prerequisites from generation/cache reuse, possibly prepare a specified resident source | Provider's ProcGen/Int2/output wrapper still reads global current context/index and databases; constructs geometry, inserts caches/visited keys, waits and affects task state. Constructor takes additional coordinate/key/BIOM/ownership arguments, not four generic integers. Side effects, threading/scheduler and reset discipline unresolved. | Natural miss→prerequisite branch→produced region evidence and coherent epoch first. Then a separately approved isolated copied-state experiment, if isolation can be established. Premature: provider return/empty aggregate offers no independent completeness oracle; direct invocation risks changing the phenomenon. |

Independent oracle categories would need qualified matched natural result,
contradictory result, unavailable prerequisites, retained state, incomplete
coverage and instrumentation failure. A successful indirect call or decompiler
signature cannot collapse them into success/failure. The expected immediate gain
does not justify intervening before the passive source/readiness boundaries are
better measured. This is a recommendation for later discussion, not a request
to broaden this assignment or proof that independent invocation is impossible.
