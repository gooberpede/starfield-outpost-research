# D5AP complete recorded competitor chronology

2026-11-04, Australia/Sydney. All 392 positively selected target tasks are
included. This is the complete relevant recorded ordinary-path scope, subject
to the [D5AM receiver census](d5am-owner-lock-census.md) and N2's authenticated
coverage. It does not enumerate arbitrary injected or replacement clients.
GC-10/D5R remain OPEN. See [report](d5ap-report.md) for claim qualifications.

The searchable local table is `.local-work/d5ap/analysis04/contenders.csv`.
Its 392 rows carry task allocation, family, original signed request, invocation,
selection, thread, source allocation, outcome, exact stage sequences and QPC.
`contenders.json` retains every copied scheduler field, dependency transition,
core event and causal event for those rows, including node/owner/frame runtime
identities. Native QPC frequency is 10,000,000 ticks/second. These are callback
stamps; sequence numbers identify channel records, not cross-thread atomics.

## Membership and exclusion proof

Eight births have the geographic target key: core 898/902/906/932/1278/1692/1696/
2082, allocations 387/388/389/397/569/749/750/932. Equal addresses recur for
387–389 and 749–750. Latest source birth/publication, not geographic key or
pointer equality, determines membership. Complete core extraction finds zero
selections in the seven earlier lifetimes and 392 in allocation 932, birth/
publication 2082/2083. No earlier lifetime is silently merged into this cohort.
Fresh D5AJ source/owning-Grid/frame/content qualification reproduces N2's
continuity through the later disjoint Grid clears.

Each target selection joins a unique typed provider on native thread and core
invocation, then `(node runtime VA, task allocation)` and matching original
request. The original scheduler validates publication/key/family identity,
retirement and per-task histories. All twelve stage kinds occur for every target
allocation. No ambiguous identity, source hazard or task-history issue is
accepted. Source allocation, task allocation, selection and ready serial are
distinct domains.

The full scheduler publication census also contains exactly these 392 typed
tasks with request coordinates in the target's native support rectangle
[-2, 11] in each axis. There is no additional coordinate-compatible published
task hidden by filtering on a later source selection. Other published requests
remain in the complete scheduler derivative; their actual source work and all
same-owner lock operations remain available independently of target membership.

| At the winner's protected miss, core 3959 | Tasks | Positive reason for exclusion from an earlier target miss |
| --- | ---: | --- |
| Constructor 1211 / density / (-2, 11) | 1 | Unvisited, exclusive acquisition and protected miss are observed. |
| Density providers 1283 / (-2, 10) and 1284 / (-1, 11) | 2 | Already in providers, but preceding source traversal is positively recorded; target selections 3999/3990 occur after store 3972. |
| Other density tasks | 193 | Their provider-entry callback is later than the miss. Native typed provider/core program order prevents a target selection before this entry. |
| Layer tasks | 196 | Their ready-tree approach is later than the miss; all also have later provider entries. Copied dependency/state transitions explain conditional readiness rather than treating publication as runnable work. |

All 392 are published and activated before authority; only the 196 density tasks
have a ready-tree approach/dispatch before it. The layer counterpart with the
same request, allocation 1237, last records seven outstanding dependencies before
authority at scheduler 40741; readiness approach 64906 occurs later. This
positive example is not substituted for the full 196-row table.

## Winner lead and nearest competitors

The winner is earliest by callback stamp at each named stage, with no tie.
Same-thread order supplies its own stage edges. Across threads these are
observations of bounded progress, not a total order of preceding native actions.

| Boundary | Winner witness | Nearest subsequent task / request | Stamp difference |
| --- | ---: | --- | ---: |
| Publication | Scheduler 3986 | 1237 / (-2, 11), layer | 6,178 ticks |
| Activation | 6198 | 1237 / (-2, 11), layer | 3,514 ticks |
| Ready-tree approach | 23318 | 1283 / (-2, 10) | 432 ticks |
| Dispatch | 33773 | 1283 / (-2, 10) | 599 ticks |
| Claim return | 41255 | 1283 / (-2, 10) | 38,174 ticks |
| Provider entry | 41257 | 1283 / (-2, 10) | 38,219 ticks |

Winner dependency updates are 7857–23316; consumed ready serial is 970, later
dispatch serial 970/rank zero and actual R8 byte 1. Queue snapshots 33775/33776
do not identify the successful claim route. Callback begins at 41256, ends at
41370 and retires at 41371. Claim CAS, exact ready insertion, callback return
from individual recorder probes and OS motives are NOT-OBSERVED.

## Already executing competitors and owner-wide interference

Winner invocation 1793 traverses three previously visited sources at core
3925/3930/3933 before selecting the target at 3942. Peer invocation 1804
enters at 3945 and checks its first source at 3957, then selects its second
at 3967 and third at 3988 before target 3999. Peer 1808 enters at 3949,
checks its first at 3955, selects second/third at 3965/3979, then target 3990.
Their provider starts therefore do not mean target lock eligibility.

The complete owner table is
`.local-work/d5ap/competition05/owner-participants.csv`: all 518 writer and
23,194 reader triples, owner runtime VA/generation, thread, context, source,
task when joined, event sequences and stamps. Generic clients with no provider
scope are included as OBSERVED owner participants with source/task NOT-OBSERVED;
their unknown allocation is not a target join and does not erase their blocking
effect. No recursive acquisition occurs in N2; recursive paths remain covered
by native semantics and adverse controls.

The callback envelope from winner provider entry to miss intersects ten reader
and two writer triples, including the winner. This deliberately inclusive set
is retained in `competition.json`; it is not an assertion that all were
simultaneously held. Foreign writer invocation 1799/selection 1800, source runtime
VA 0x16a9e027a00, acquires at causal 2925 and releases at 2932. The target reader
registers at 2927 against 0x401000; four other-source readers register at
2928–2931. Foreign release sees 0x401005. Reader releases reconstruct the unique
operand chain 2935 → 2937 → 2941 → 2940 → 2942, draining five to zero.
Events 2940/2941 have equal ticks and inverted reservation order relative to
their operand order. The independent native oracle proves this chain without
sorting atomics by timestamp or record number.

Winner visited-done/approach/pending/acquired are 2947/2948/2949/2950. Pending
sees 0 → 0x1000; acquired sees 0x1000 → 0x401000. The foreign writer and shared
cohort delay progress, but there is no other target pending writer to overtake.
All other target paths observe visited=1 and have no exclusive target approach.

## Stage qualification and queryable graph

| Stage class | Qualification for each target row |
| --- | --- |
| Publication, activation, dependency snapshots, ready approach, dispatch, queue bounds, claim return, callback/provider/end/retirement | OBSERVED, with all matching event rows retained. Readiness completion/insertion between probes is NATIVE-INFERRED only where the native predicate applies. |
| Source selection, visited result | OBSERVED for all 392; birth/publication plus allocation qualify identity. |
| Exclusive approach/pending/acquired/return/release and protected miss/generation/sample/store | OBSERVED for task 1211. For 391 visited bypasses these stages are NOT-APPLICABLE under the native branch, with positive visited=1 evidence. |
| Exact successful claim CAS, selected queue route, OS reason, uninstrumented winner | NOT-OBSERVED. No missing array is interpreted as absence. |
| Unsupported or ambiguous lifetime | UNQUALIFIED if encountered; none accepted in the target cohort. Generic unknown source/task fields remain explicit. |

`competition05/graph.json` stores per-thread causal program-order chains,
every reader/writer interval and the named native edges. Full original causal
rows and the compact index retain reset boundaries and uncertainty. Graph edges
never arise from global stream order. Owner registration is causal 1, zero
baseline, generation 1; later resets remain lifecycle invalidators for pair
queries that cross them. The [method](d5ap-analysis-method.md) describes lazy
witness expansion and qualification.
