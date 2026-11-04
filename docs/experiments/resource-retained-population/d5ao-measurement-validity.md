# D5AO measurement validity

2026-11-04, Australia/Sydney. Offline measurement qualification; parent GC-10 /
D5R remains OPEN. Authored interpretation is REVIEW-REQUIRED; raw native outputs
and binaries are LOCAL-ONLY.

| Element | Answer and scope |
| --- | --- |
| Question | Can a GC-10 instrument record a winner without certifying an unobserved winner or a usual preference? |
| Best-supported answer | A complete, authenticated record can establish the winner of the instrumented execution. Delaying an observer counter can change relative arrival at the native ownership CAS. Removing counter sleeps removes that mechanism, while atomic retries and all other hooks still influence execution. |
| Confidence | STATIC proof for the changed helper and native ownership intervals; controlled native-fixture evidence is reported separately in the interference controls. No retail frequency estimate. |
| Coverage | Exact qualified candidate, same-target owned native lock pages, deterministic collision seams, real concurrent participants and stated operational substitutions. |
| Limitations | Counterfactual uninstrumented execution cannot be replayed with identical OS scheduling. Fixture timing does not bound retail delays or establish exhaustive ingress/OS causality. |
| Next decision | Consider the separately bound NOT AUTHORIZED N2 proposal only after independent exact-snapshot review; actual live approval remains separate. |

## Threat model and claim tiers

The native owner lock is shared by requests for different sources. Its writer
pending count is not a ticket. Readers can enter while only pending writers
exist. A later running writer can win the ownership CAS before an earlier
registered writer. See [D5AF native instructions](d5af-prelock-causality.md) and
the [receiver/call-site census](d5ao-counter-critical-path-matrix.md).

| Claim tier | Positive support required | Defensible conclusion | Excluded inference |
| --- | --- | --- | --- |
| Historical event observation | Exact producer/site/source pins; complete relevant byte/CRC/sequence/flush accounting; stable source allocation and owner; protected miss, direct sample and successful store joined to one invocation | This request constructed in this instrumented execution, using the directly copied mask/input. A narrower direct sample may survive unrelated gaps. | No assertion that this request would win without instrumentation; no absent-competitor claim from absent events. |
| Causal ordering | Qualified task allocations, callback/provider joins, owner baseline/generation, all relevant reader/writer/releases and sound before/after interval bounds | Recorded partial orders and witnessed overtaking constrain how the actual instrumented winner progressed. Unknown overlap remains UNKNOWN. | QPC stamp order is not cross-thread atomic order. Claim-return is not claim-CAS time. Pending registration is not ownership. A visited stamp is not exclusive approach. |
| Normal preference or consistency | Repeated independently admitted ordinary retail trials, predeclared eligibility and denominator, contrary outcomes retained, route/context qualification and assessed observer-effect envelope | At most a scope-limited descriptive recurrence, with uncertainty and intervention limitations stated; a causal preference needs discriminating conditions. | No usual winner, probability, universal coordinate preference or unchanged uninstrumented distribution from a fixture or a single ordinary observation. |

Event integrity and measurement validity are separate. A truthful failed
terminal refuses completeness even when all stored frames pass CRC. Conversely,
a complete record can be an accurate history of an observer-influenced winner.
The latter is useful evidence when the intervention and claimed tier are explicit.

## Version-specific fitness

| Version | Counter behavior | Measurement consequence |
| --- | --- | --- |
| 0.9.1 | Thirty-two CAS attempts can refuse a legitimate contended admission. Separate queue reservation quotas can also lose events. | Failure may prevent useful observation; no unique N1 initiating producer can be recovered. Incomplete acquisition cannot establish absence, winner or consistency. |
| 0.9.2 | Checked strong CAS retries call Sleep(1) after interference, including checked exit. | Improves counter admission liveness relative to a quota but can voluntarily deschedule a requester while it owns native or observer gates. Requested sleep duration has no upper scheduling bound. |
| 0.9.3 D5AO | Checked strong CAS retries without OS sleep/yield, preserving saturation/underflow and diagnostics. | Removes voluntary descheduling from these helpers. Cache traffic, retry work, native preemption and other observer work remain. Per-thread progress is not wait-free or latency-bounded. |

These are design/coverage distinctions, not comparable retail failure rates.
The historical bounded comparator is an explicitly identified algorithm control
inside the modern integrated envelope, not an untouched 0.9.1 recording.

## Residual bias register

| Mechanism | Relevant interval and consequence | Admission or interpretation control |
| --- | --- | --- |
| Shared atomic cache line and retries | Core/bridge/producer entry and exit can change relative task progress before or during ownership. A preempted contender may repeatedly lose CAS. | Report observed retries/controlled collision limits. No starvation or fairness bound; no inference of unchanged arbitration. |
| Hook CALL/relay and ABI saves | Extra branches, stack/vector saves and restoration bracket native operations, including releases. | Exact site/guard/ABI qualification prevents semantic corruption; it cannot remove execution cost. |
| Event copying and timestamps | QPC, native field reads and reservation/publication occur before native continuation or under native ownership. | Interpret stamps as callback bounds. Do not subtract fixture means to manufacture retail acquisition times. |
| Queue reservation and storage | Existing finite capacity, bounded reservation attempts and cache traffic can fail or delay a producer. | Any actual loss is explicit and refuses affected completeness; no silent drop allowance or invented healthy threshold. |
| Registry and token publication | Odd serial or registering flag windows can extend uncertainty; identity ABA can defeat a naive pointer join. | Stable allocation/generation/serial joins, guarded provenance and refusal of ambiguous histories. |
| Periodic worker draining and guards | Worker CPU, memory traffic, hash checks and filesystem flushing compete for resources even outside a callback. | Qualify all-channel health and retain unknown OS effects. Observation-off fixture is a control, not an identical uninstrumented scheduler. |
| Other native lock users | Readers, other-source writers, recursive owners and separate manager locks affect progress. | Use actual receiver aliases and all relevant release edges. Do not equate manager `+0x130`, ProcGen `+0x130`, `+0xd0` or unrelated global-helper users. |
| Measurement seam and timers | Controlled event waits and busy waiting intentionally set contender offsets; QPC perturbs measured code. | Shared paired inputs, batch timing and repeated controls; no ordinary scheduling-frequency interpretation. |

The acquisition decision is therefore conditional suitability for qualified
instrumented event history, rather than a zero-effect certificate. Any future
N2 adjudication must distinguish a witnessed causal order from the reason a
thread ran first. The latter may remain inseparable from observer work.

## Prospective prediction and interpretation

Retain D5AM-PRED-01, the N0 outcome and N1 PRED-02 text/oracles unchanged. Both
failed attempts lack target observations and remain INCONCLUSIVE. A new package
or eligible trial requires a separately identified reviewed prospective forecast
and freeze before any future observation. The [N2 card](run-card-d5ao-n2-proposal.md)
does not issue that forecast or live permission.

Scientific uncertainty suspends only dependent inference/actions. Healthy
authorized recording need not stop because a causal comparison is inconclusive.
Actual integrity/safety failures retain protective refusal. No matching-mask,
chosen-request or equal-geometry prerequisite may filter a prediction testing
their variability. A contrary result remains evidence.
