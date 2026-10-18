# C3 inter-system fuel and skipped-time transport

2026-10-18, Australia/Sydney. SOR-EXP-0046 / SOR-EV-0054.
[Authority](contract.md), [native derivation](native.md),
[endpoint stages](stages.md), [saved cases](saves.md),
[clock examples](time.md), [review](review.md).

| Question | Answer | Status / source | Meaningful limit |
|---|---|---|---|
| Quantity and consumption event | The installed recipe withdraws **five He-3 units per accepted fuel-production cycle**. Its base interval is **108 engine scheduler seconds**, modified through the shared interval machinery. Withdrawal occurs in native producer work, independently of ship departures, legs or round trips | Established STATIC definition and concrete removal path | Five is the ordinary recipe amount per cycle; observed runtime deltas, races and mod overrides were not measured |
| Physical fuel source | Transitive incoming resource-transfer sources supply ingredients directly. The pad marker is the logical recipe consumer; no independent fuel-container inventory is required | Established STATIC, corroborated by SAVE source graphs and real He-3 stacks | Adjacency, a ship hold or an outgoing bay alone does not supply fuel. A cargo child can participate through a qualifying local graph |
| Admission threshold | An uncharged eligible pad needs a complete five-unit recipe, potentially split across sources. A charged pad's ordinary mode-0 readiness query bypasses that ingredient recheck until native producer work updates the charge | Established STATIC mode/charge branch | Current charge, halt, reference resolution and other production reasons remain necessary inputs; saved stock alone cannot decide readiness |
| Departure, receipt and return | Arrival unloads before fuel checking. Either linked non-mission pad passing readiness admits the shared ship's next load/departure sequence at either end, including reverse freight from an unfueled receiver | Established shipped PEX plus native readiness wrapper | A load/departure already admitted is not continuously gated. A mission endpoint is deliberately excluded from supplying readiness |
| Retry and recovery | Neither-ready arrival arms timer 2. Its next callback repeats unload, redistribution and the either-pad query. Replenishing either side can resume the route on polling; no direct stock-change wake-up appears in the complete ship/quest handlers | Established PEX, STATIC timer and input paths | A retry may unload retained freight into newly freed space. Fuel consumption can independently occur during the retry delay |
| Distance and perks | No distance or per-leg term enters the recipe withdrawal. Interval modifiers, effective HarvesterRateMult, registration quantity, pause/halt and available inputs change aggregate fuel use; cargo capacity perks affect freight separately | Strongly supported bounded definition/native/PEX review | Effective player/crew context and runtime settings were not sampled; no universal fixed fuel-per-wall-minute or fuel-per-trip claim |
| Wait/sleep mismatch | Elapsed producer work can make freight and He-3, consume fuel and fill stores while game-time freight dispatch is suppressed. On resumption one due event runs, then rearms from its actual current time; missed voyages are not enumerated | Established STATIC interfaces, conditional worked arithmetic | Net He-3 buildup requires supply exceeding consumption. Capacity, eligibility, update ordering and reference resolution can instead stop accumulation |

The user's observation that a fueled sending pad can deliver to an unfueled
receiver is supported. The mechanism is broader: “origin” is not a permanent
fuel-paying role. One eligible fueled endpoint can also permit return loading
and travel, and can release a retrying ship at the other endpoint. Both fueled
pads can consume their own periodic recipe inputs even though only one needs
to pass the ship's readiness query. This is a native-derived ordinary mechanism,
not a reconstructed historical voyage.

The charge state is consequential. The native query used by Papyrus passes
mode 0; the producer scheduler passes mode 1. For this pad category, charged
mode 0 can pass without five units currently in the source inventory. On the
next due producer check, insufficient inputs give reason 7 and change charged
to uncharged. Conversely, an uncharged pad with five reachable units can pass
the query before its next scheduled withdrawal. There is no atomic “pay five
to depart” transaction in the mapped route.

Confidence is **STRONG / STATIC**, with instance-level SAVE corroboration and
exact byte/check results scoped separately. Coverage is retail 1.16.244.0,
main ESM, five freshly matched shipped PEX/source members, existing read-only
analysis and the protected Save52 corpus sample. Four endpoints across two
stocked inter-system routes have explicit marker, owner, bays, ship, incoming
graph and producer-row joins. These cases answer the ordinary mechanism without
expanding into a generic parser or requiring another historical save merely to
increase sample count. Unsupported VM/timer and extra fields stay explicit.

The scientific model is complete for this bounded assignment, subject to the
[independent disposition](review.md). Particular historical consumption epochs,
current effective inputs and exact runtime shipment rates remain unmeasured.
No consequential unresolved mechanism requires a live experiment here. A
contrary concrete callback/removal or endpoint predicate would reopen the
specific claim; a snapshot with low fuel does not by itself contradict charge
or asynchronous readiness.

Authored interpretations remain REVIEW-REQUIRED; proprietary native/script/save
payloads remain LOCAL-ONLY. Scientific confidence, task acceptance, safe mod
integration and publication eligibility are separate. The requested
[time-skip reconciliation backlog](../../../BACKLOG.md#cargo-link-time-skip-reconciliation)
is a future design question. No mod, game launch, save alteration, staging,
commit, push or publication was performed or authorized.
