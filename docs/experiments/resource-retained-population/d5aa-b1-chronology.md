# D5AA retained B1 chronology

2026-10-31, Australia/Sydney. [Report](d5aa-report.md),
[source ledger](d5aa-sources.csv), [machine data](d5aa/README.md),
[chronology figure](d5aa/chronology.svg).

**B1 retains two empty-state boundaries followed by non-target construction and
conditional target-compatible visited bypasses. It does not retain the target's
first query, sample or successful visited append.** No complete authenticated
source first→append→later-bypass chain exists in this observation schema,
including the non-target controls. The missing append witness is a positive
coverage limitation of the fourteen installed hooks, not a failed text search.

## Clock and phase boundaries

The raw stream has 19,780 frames of 328 bytes. Frame `n` starts at raw-file byte
offset `328 × (n−1)`; its 312-byte payload begins 16 bytes later. The unchanged
decoder and D5Y authenticator check framing, sequence/payload CRCs and 39 durable
prefix ACKs against the exact identity/archive pins. Raw SHA-256 is
`cd4762095a422fb537844546e923fff667e894a63b082b0205f3107786f49a5c`.
The full local sanitized ledger is `.local-work/d5aa/chronology04/events.csv`;
the tracked [451-event selection](d5aa/events.csv) includes every map-path
record, all conditional target pairs, selected reset/loss/phase boundaries and
first/last pointer-compatible later bypasses. It is not the complete stream.

QPC frequency is 10,000,000 ticks/s; origin is first retained READY tick
2,619,875,036,404. Absolute QPC values and relative seconds are in each row.
Checkpoint files additionally pair UTC and QPC; raw events have no UTC capture.
Their conversion would be calibrated wall time, not an independently measured
UTC instant. Collection times are intervals around external challenge handling,
not exact load, travel, visual arrival or loading-screen transitions.

| External checkpoint | Request → collection ACK, seconds after READY | Admitted watermark / counted losses |
|---|---|---|
| Main menu | 53.0658791 → 57.4424402 | 1 / 0 |
| Save52 loaded, not travelled | 159.6000001 → 165.1588306 | 110 / 0 |
| First arrival reported | 245.0536603 → 249.9573088 | 19,780 / 9,957 |
| Operator STOP write | 250.1425311 | No new native event instant follows from the annotation. |

The owner places the PC in the Lodge during the load checkpoint and reports
direct ordinary travel to Feynman V Cu IL F. This is operator evidence, not a
native transition clock. Recorded native events stop before the arrival-request
annotation; arrival may already have happened when that request was collected.
No event can be assigned to a loading-screen frame or subsequent player movement.

## Exact retained boundaries

| Sequence / event | Relative QPC seconds | Supported order / meaning |
|---|---:|---|
| 1 READY | 0.0000000 | Installation/startup witness; no coldness claim. |
| 2 / 3 / 4 reset begin/unlock/end | 125.9728231 / 125.9728299 / 125.9728316 | Same ProcGen, observer epoch 2, qualified empty-state certificate; caller unknown. |
| 110 last pre-travel prefix record | 128.4452000 | Prefix contains READY 1, reset/Grid fence begin 54, fence end 54, cold 1; no provider record. |
| 115 / 116 / 117 second reset | 221.1232376 / 221.1232464 / 221.1232486 | Same ProcGen, observer epoch 113, second qualified empty-state certificate after pre-travel ACK. |
| 215 first retained copied-key map miss | 221.4626961 | Non-target `0:37524:20928:00257f37`, query `(-7,4)`, sample 218 / mask 3. |
| 1236 first sampled loss admission boundary | 221.5290664 | Counter samples next admission after loss; this event's time is not a lost event timestamp. |
| 3297 first conditional target selection | 221.6887695 | Selection/bypass pair; identity conditional on installed frame/content/Grid support. |
| 10445 last conditional target selection | 223.2743616 | Same conditional class; no copied positive target identity. |
| 19780 last admission | 230.9878599 | All admitted records eventually durable; losses remain unplaced. |

All 19 sampler paths and all 24 copied map decisions lie between the pre-travel
ACK and the arrival-request collection. Their owner is `0x0005e0de` (Feynman V).
The prefix has no copied Jemison or Feynman source because it contains no source
selection/provider boundary. This is not a general assertion that no exterior
file, cell, context, uninstrumented producer or source was loaded.

## Activation, flush and loss audit

The unchanged plugin enables capture before installing hooks and emits READY
before the main-menu challenge. `provider_hook` emits entry whenever enabled;
it does not filter by target, geographic owner, source count or firstness.
Request-read failure still emits status. Selected/visited hooks also do not
filter source identity. Descriptor emission has a narrower converter-scope guard.
The 110-record ACK reports active capture, intact hooks, enqueued/dequeued/
acknowledged all 110, zero loss/counter overflow/output faults. Thus the retained
prefix contains no admitted provider execution under this recorder contract.
It is a bounded hook-path result, not proof against bypassed hooks, another
unexamined engine route, or arbitrary corruption. No positive Jemison demand
should be inferred from the first reset alone.

Native QPC sampling precedes queue reservation. There are 13 adjacent admission
inversions; a higher successful-admission sequence may have an earlier sampled
tick. No universal total engine order follows from the file order. The path
joins use invocation/selection/thread/request/source/frame and actual decision
epoch, with status/hazard checks inherited from the unchanged path reporter.
Each displayed map path has nondecreasing local QPC; same-thread control flow
supports its boundary order. Cross-thread map misses/hits additionally have the
native exclusive-lock order. Checkpoint relations give only interval order.

The writer flushes raw bytes, then an identity-bound cumulative ACK. Raw event
ticks bound event sampling, not actual write/flush completion. Cumulative writer
ACKs have no individual QPC timestamps. Final raw/ACK/terminal watermarks agree
at 19,780 with zero output faults. Known 9,957 capacity losses and zero
contention-exhausted losses are not assigned to sites, sources or invented times.
Loss advances observer epochs, as do lifecycle invalidators; an observer epoch
is not the native visited-store epoch. The first conditional target pair follows
the loss boundary. Both reset certificates therefore fail to supply an
uninterrupted target identity/writer history.

## Every map decision and partial source controls

[paths.csv](d5aa/paths.csv) individually records 19 misses with direct ordinary
samples and five hits without resampling. It gives each source key, original
query, thread, invocation/selection, epoch, exact lookup/sample sequences and
QPC. Seven miss paths start before the first sampled loss admission; the other
twelve and all five hits are exposed to prior loss. None has the target key.
Missing generator closeout or returned records remain missing rather than
invented. A complete sampler prefix is not a complete population.

[partial-chains.csv](d5aa/partial-chains.csv) enumerates later valid visited hits
with matching source pointer, ProcGen and observer epoch for **23 of 24** decisions;
all 24 are audited. Lookup 1227, key `0:37560:20952:00257f33`, epoch 207, has
zero such later bypasses. Its first later pointer-compatible bypass is 3907,
epoch 4974; accepting it would silently cross a loss/invalidator boundary.
For example lookup 215 is followed by pointer-compatible bypasses starting 237;
lookup 224 is followed by bypass 308. These pre-loss controls are stronger than
an unrelated later event, but bypasses lack copied identity and no allocation
lifetime or append-success record closes the chain. Alias labels preserve
numeric equality only and cannot transfer source identity across retirement,
reset or allocation reuse. The unchanged cold reducer qualifies zero chains.

The copied key `0:37536:20952:0024ef52` has a miss at 1308 and later map hits
1327/1328. Key `0:37548:20892:00257f30` has miss 16370 then hits 16401/16402.
The respective selections/visited checks overlap the generating invocation;
the hits reached the map only after their earlier unvisited checks. This is
consistent with the verified shared-lock release/exclusive reacquisition and
absence of a second visited check. It does not expose exact lock acquisition
timestamps or prove that every later request saw an appended token.

The 119 [conditional pairs](d5aa/conditional.csv) span selection sequences
3297–10445 at 97 singleton-support cells. D5Y recomputes their installed-support
uniqueness. The actual selected/visited hooks copy no source descriptor or positive
target identity; protected source copying occurs later at map lookup, which a
visited hit bypasses. No target descriptor can be recovered from this path's
zero-filled source buffer. Retrospective pointer aliases, equal owner and nearby
non-target samples cannot replace that missing observation.
