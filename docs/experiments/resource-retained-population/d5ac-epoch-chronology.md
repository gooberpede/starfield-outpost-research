# D5AC epoch chronology

**Every B2 observer increment is explained without equating it to a native
reset.** Two resets establish empty-state triads; 111 Grid clears account for
222 other increments. Parent D5R OPEN. [Report](d5ac-report.md),
[sources](d5ac-sources.md), [audit](d5ac-cold-certificate-audit.md).

## Counter rules and complete accounting

The observer starts at 1. Fence entry increments the global atomic counter.
Reset fence 0 exits without another increment; fences 1–4 increment on exit.
Reported loss independently increments the counter. Overflow disables recording
and marks it broken; no wrap or reported loss occurs here. Events copied from
an invocation retain its entry epoch; Lookup `d` records the current global
counter. An arbitrary event-to-event epoch difference is not an increment site.

| Native receiver and operation | Fence | Recorded calls | Increments |
|---|---:|---:|---:|
| ProcGen broad reset | 0 | 2 | 2 |
| ProcGen destructor | 1 | 0 | 0 |
| Map subobject erasure | 2 | 0 | 0 |
| Grid bulk clear | 3 | 111 | 222 |
| Geographic-source retirement | 4 | 0 | 0 |
| Reported recorder loss | Separate path | 0 | 0 |
| Total | | 113 fenced calls | 224; final counter 225 |

All 113 begins have matching ends on the same thread and receiver; the recorded
hazards are 1 on begin and 0 on end. Both Cold events have hazards 1, zero
visited control/data and status zero. No unmatched triad or event category is
hidden. All increment-causing records have strictly increasing native QPC and
consecutive before/after counters. Other event admissions include 97 adjacent
QPC inversions and must not be treated as a total causal clock.

| Boundaries | Counter transition | Native interpretation |
|---|---|---|
| 2 / 3 / 4 | 1 → 2 | Reset begin / protected empty unlock / reset end; first valid certificate. |
| Grid fences before 881 | 2 → 112 | 55 Grid clears, 110 increments; not 110 resets. |
| 881 / 882 / 883 | 112 → 113 | Second valid reset certificate for the same ProcGen used by target requests. |
| 892 / 893 through 1730 / 1731 | 113 → 207 | 47 Grid clears; 94 increments; no broad reset. |
| 2074 / 2075 | 207 unchanged | Target geographic source birth / publication, allocation 932. |
| 2470 / 2473 | 207 unchanged | First recorded provider entry / protected map decision in the entire capture. |
| 8006 / 8020 / 8091 / 8106 / 8339 | 207 unchanged | Competing target decisions, constructing miss/store, then other request's hit. |
| 31882 / 31883 onward | 207 → 225 | Nine later Grid clears; no new reset. |

This is a labelled causal milestone diagram, **not a duration-scaled axis**:

```mermaid
flowchart LR
  A[Reset triad 2-4: epoch 2] --> B[55 Grid clears: epoch 112]
  B --> C[Reset triad 881-883: epoch 113]
  C --> D[47 Grid clears: epoch 207]
  D --> E[Birth 2074; first provider 2470]
  E --> F[Target decisions and sample: epoch 207]
  F --> G[9 Grid clears: final epoch 225]
```

## Why the target has no same-epoch certificate

Grid clear's receiver is a Grid. Its schema field named `proc` is **not** a
ProcGen pointer at that site. Native clear may remove zero or more pointer-map
entries through the current manager's ProcGen, then free geographic sources.
It never clears the separate visited array. Even an already empty Grid advances
the observer epoch twice. Thus neither 47 calls nor 94 increments counts actual
map removals, ProcGen replacements or cold transitions.

Reset 113's direct empty witness is real. The unchanged consumer indexes cold
certificates by ProcGen and exact observer epoch; after Grid invalidations there
is no reset begin/unlock/end in epoch 207 to index. Healthy transport cannot
synthesize one. Conversely, zero reported loss cannot prove that arbitrary native
paths were instrumented. Here the reason for the missing certificate is supported
positively by the recorder rules and every intervening fence, rather than by
losslessness alone.

Under the audited ordinary mutation graph, reset end 883 also supports a
**separately derived carried-empty anchor** through the removal-only interval to
first provider entry 2470. Geographic source creation does not insert population
holders or visited tokens. No provider, append, destructor or other invalidation
is recorded in that interval. The same ProcGen is directly recorded at both
ends. This inference depends on ordinary mutator/lifetime coverage; it is neither
a direct snapshot in epoch 207 nor a production certificate. Once demand starts,
other sources populate the map before the target. This is not a claim that the
whole ProcGen remains empty at sequence 8091.

## Exact local tables and timing domains

`.local-work/d5ac/reconstruction05/events.csv` contains every event's sequence,
raw frame offset, kind, invocation/parent, thread, QPC, inherited epoch, hazards,
status, runtime operands, selection and request. `transitions.json` contains
all 224 increment-causing records, before/after counters and fence reason;
`resets.json` contains all six reset witnesses. `carried-empty-oracle.json`
records the separate continuity test. These derivatives are LOCAL-ONLY.

For sequence `s`, frame file offset is `(s - 1) × 328`; payload starts 16 bytes
later and is 312 bytes. QPC has 10,000,000 ticks per second. Reset end 883 is
QPC 3761440385432; last clear end 1731 is 3761442380446; first provider entry
2470 is 3761443830507. This distinguishes reset completion, removal interval and
demand without claiming operator-action times. Full pointers and exact per-call
threads/receivers stay in the local tables, bound by the delivery hashes.
