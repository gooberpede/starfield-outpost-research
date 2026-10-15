# Scientific value reassessment — SOR-EXP-0036

**Decision: NO-GO for the existing 0.8.0 observer and first-session run card.**
2026-10-15, Australia/Sydney. [Correction brief](../../implementation-briefs/CODEX_BRIEF_SOR_080_prose_correction_scientific_go_nogo.md),
[original brief](../../implementation-briefs/CODEX_BRIEF_SOR_local_readiness_native_observation.md),
[prose audit](prose-correction-audit.md), [independent reassessment](reassessment-review.md).

| Element | Evidence-based answer |
|---|---|
| Material question | What minimum state and inputs support a correct, complete and current inorganic availability determination? |
| Best-supported answer | Even perfect capture by this immutable candidate cannot distinguish materially different readiness/coverage histories. Its new source/provider boundary events lack the geometry, native admission decisions and lifecycle evidence needed to resolve that question. The actual first card controls only unplaced-preview movement. |
| Basis and confidence | STATIC contracts and retained 0.7.0 runtime conclusions support a strong, scoped experiment-design judgment. This is a recommendation about this experiment, not a new engine finding or a universal impossibility result. |
| Coverage | Exact thirteen-hook candidate, schema 8 and the proposed first Save3 Kreet A/B/C preview. Established-Workshop and player-displacement scenarios are explicitly omitted by that card. No new runtime evidence was acquired. |
| Consequence | Preserve the offline-qualified observer, DLL, ZIP, qualifications, previous review and proposed procedure as an unadopted historical candidate. Supersede the earlier ACCEPT as a basis for committing or going live. No follow-on instrumentation project is proposed or implied. |

## Evidence and actual measurement boundary

The [native map](native-map.md) and immutable `runtime/local-readiness-080/capture.h`
establish the following surfaces. All addresses below are module-relative RVAs
for the pinned executable in [release.md](release.md); they are not runtime VAs.

- Tag 101 observes calls from `0x021b26bc`, `0x021b42e3` and `0x021b6931` to
  updater `0x021e07d0`. `args[0]` is operation state, `args[1]` the indexed
  descriptor pointer, and `args[2:4]` contain radius/upper-scalar bits. Blob `ref`
  copies the 24-byte descriptor, `base` copies 0x68 bytes of state, and tags
  108/109 copy the three population headers/members before and after. AL is
  recorded as `result`. Domain/reference headers and observed writer-overlap
  status do not supply source lifetimes or an authoritative cache epoch.
- Tag 111 observes `0x021e0a46 → 0x021e0f50`. `ref` copies the 0x18-byte
  closure, `operand` the 8-byte source-value slot, `reference` the pointed source,
  and `base` its 0x40-byte header. It captures neither resource-map contents nor
  ordered regions/points or actual native accept/reject decisions. `result` is
  the callback continuation result, not a region verdict.
- Tag 112 observes `0x007b526a` and `0x007a1a3c → 0x0079f860`. It copies the
  Int2 input in `ref`, the 0x78-byte ProcGen header in `base`, and the 8-byte
  aggregate output pointer slot in `output`. It does not observe the constructor
  at `0x0079b520`, its prerequisite exits, visited/source hit-miss decisions,
  coverage, reset/destruction or a publication/completion epoch. Provider headers
  are sampled outside its internal exclusive interval.
- Tags 102–110 observe command/UI consumption, union/selected-water inputs,
  row construction and final census. These support a final-fold comparison.
  TLS `parent` relates same-thread nested invocations; it does not bridge an
  asynchronous dispatch to an originating evaluation. A command pointer,
  matching populations or nearby QPC timestamps cannot supply that missing edge.

The [committed dataflow](../native-availability-map/dataflow.md),
[lifecycle](../native-availability-map/region-lifecycle.md),
[requirements](../native-availability-map/region-requirements.md) and
[RD01–RD07 uncertainty matrix](../native-availability-map/region-uncertainty.md)
already distinguish resident maps, attempted generation, retained populations
and completeness. The [Milestone B specification](../resource-availability-milestone-b/specification.md)
requires real geometry, actual translations and independently observed decisions
for spatial validation. The 0.8.0 additions do not supply those operands.

## Hypothesis decision matrix

Each row below assesses the actual first card, not a hypothetical expanded run.
Proof categories concern the stated proposition, not whether engineering works.

### H1 — Does every updater call scan source maps?

| Decision dimension | Assessment |
|---|---|
| Materiality / prior knowledge | Separating a retained result from a fresh scan matters to interpreting availability, but the refresh guard is already STATIC at updater `0x021e080f..0x021e0952`. The 0.7.0 report records 35,228 zero-refresh evaluations with unchanged populations. The exact per-call scan child would be an incremental runtime observation, not a newly identified prerequisite. |
| Competing explanations | A call may retain spatial results, scan an empty resident map, or scan populated maps without changing the result. Similar final populations can accompany different source readiness and previous cache histories. |
| Captured / missing | Tags 101/111, parent/thread/phases, descriptor/scalars and populations can identify an observed child. No explicit branch-reason event, complete map census, initialization/reset history or coverage certificate is captured. |
| Actual action | Load Save3; open unplaced-beacon preview; move the proposed beacon, seeking A/B/C if convenient. No controlled reset, source eviction or provider miss is required. |
| Outcomes / controls | A complete updater scope without a child refutes universal source-callback traversal on the covered path, but does not by itself distinguish retention from an empty scan. A child proves visitation; all calls having children cannot prove universality. Missing phases, admission closure or overflow invalidate an absence claim. Synthetic cached/child controls qualify detection only. |
| Proof category / payoff | **Bounded falsification only.** This is a valid possible narrow finding, but static guard evidence already supplies a lower-cost explanation. It does not establish correct/current coverage or minimum sufficient state. Thirteen hooks and another player session are disproportionate to this increment. |

### H2 — Does provider return certify completed geometry?

| Decision dimension | Assessment |
|---|---|
| Materiality / prior knowledge | This would be consequential if a genuine completeness certificate could be identified. Existing provider/constructor analysis already shows cache hits/visited skips and prerequisite exits that make return alone insufficient as a certificate; see lifecycle VA `0x14079fed3..0x14079ff60` and constructor exits in the existing source ledger. |
| Competing explanations | Successful production, previously cached maps, an attempted construction that exited, a visited skip, partial coverage or an earlier epoch can produce similar headers and aggregate output pointers. |
| Captured / missing | Tag 112 provides raw input/output slots and ProcGen headers, not branch results, geometry contents, constructor status, source coverage or lifecycle linkage. Provider-to-updater timing does not join asynchronous task epochs. |
| Actual action | Save3 loading may naturally generate provider calls; preview motion does not deliberately force or independently verify a provider miss, failed prerequisite or completed-source control. Provider occurrence is opportunistic. |
| Outcomes / controls | A return with empty/unchanged headers can mean legitimate emptiness or failed/unattempted generation. Nonempty/changed headers do not prove complete geometry. No return observed is a reachability result only. Malformed/partial reads and capacity failures yield unavailable evidence, not a native negative. |
| Proof category / payoff | **Not testable** as completeness certification. More boundary samples cannot separate the alternatives. Runtime reachability is a possible increment but is not the core scientific result; the static counterexample route is already cheaper. |

### H3 — Does source visitation mean spatial acceptance?

| Decision dimension | Assessment |
|---|---|
| Materiality / prior knowledge | Native admission is central to spatial equivalence. Existing `0x021e0f50` analysis resolves IRES and applies broadphase/strip/height/edge predicates; visiting a source precedes and is distinct from accepting a region. Milestone B already describes this distinction. |
| Competing explanations | One visited source may contain zero valid candidates, all rejected candidates, or one/many accepted regions; another source or retained atmosphere/biome contributions may explain the final set. |
| Captured / missing | Tag 111 contains closure/source headers and continuation `result`. Ordered candidate identities, complete points/widths/transforms, actual translation operands and candidate-level accept/reject branches are absent. Final spatial population does not identify which source/region admitted a resource. |
| Actual action | Beacon movement changes query operands and may produce source visits. The card supplies no independently qualified accepted and rejected region controls. |
| Outcomes / controls | Visits with changed or unchanged final sets cannot identify a region verdict. Even an apparently empty spatial result after visits lacks a complete candidate census and cannot prove every visited region rejected. A continuation return of 1 is not acceptance. Integrity/overflow failure further removes any exhaustive-negative interpretation. |
| Proof category / payoff | **Not testable** for native candidate acceptance. Runtime visitation could illustrate the known path; it cannot independently replay or validate spatial predicates. This increment does not justify the instrument/session burden. |

### H4 — Does refresh imply a changed resource set?

| Decision dimension | Assessment |
|---|---|
| Materiality / prior knowledge | Refresh semantics help interpret traces, but this is already answered directly by the [0.7.0 scientific report](../continuous-beacon-preview/live-scientific-report.md#actual-argument-source-populations-and-native-rows): 346 refresh=1 evaluations, five population changes and 341 unchanged populations, including initial delivery. The preliminary description of a potentially new minor clarification understates the existing evidence. |
| Competing explanations | Recomputing a scan can yield the same set; atmosphere/biome identity retention can also preserve populations. Identical results do not identify which source state or history was sufficient/current. |
| Captured / missing | Tag 101 AL and before/after tags 108/109 support the source-preserving `within_invocation_population_change` comparison. The repaired decoder separates it from `prior_observation_signature_change`. Missing reads/unknown IDs/overlap must remain unqualified; no full epoch or global writer coverage is added. |
| Actual action | A/B/C beacon motion can yield refreshed changed or unchanged populations; repeated evaluations require no extra scenario. |
| Outcomes / controls | A qualified refresh=1 with unchanged populations refutes the implication again. All sampled refreshes changing populations would not contradict the earlier counterexamples or prove universality. Zero-refresh samples or no refresh provide no new test. Complete unchanged/changed fixtures support detection, not the engine claim. |
| Proof category / payoff | **Illustrative/confirmatory.** The new within-call representation improves attribution discipline, but it does not make the already refuted universal proposition a consequential unresolved question. Another live session is unnecessary to answer H4. |

### H5 — Does the UI consume the originating evaluation snapshot?

| Decision dimension | Assessment |
|---|---|
| Materiality / prior knowledge | Causal ancestry would matter when associating readiness with displayed results. Static UI/queue analysis already shows a snapshot-free command consuming shared populations. The 0.7.0 report validates all 346 final folds while retaining unresolved unique ancestry; candidate producer matches range from one to 18,487. |
| Competing explanations | The UI may consume populations from a later evaluation, retained state or another relevant writer. Equal sets across many evaluations can fit all these histories. |
| Captured / missing | Tags 102–110 capture actual command/consumer/row identities. They do not carry an immutable originating descriptor/population snapshot or a qualified producer-to-dispatch epoch. Same-thread `parent` cannot fill this asynchronous gap. |
| Actual action | A/B/C preview reports provide label intervals, not an exact render event or controlled dispatch-order experiment. No delay injection, queue manipulation or isolated writer scenario is authorized. |
| Outcomes / controls | Input/row agreement validates aggregation at consumption again. A content/timing discrepancy may expose an association error or motivate investigation, but cannot identify the true originating evaluation from these fields. No discrepancy does not establish snapshot semantics. Missing rows/reads/overflow yield incomplete evidence. |
| Proof category / payoff | **Illustrative/confirmatory** for the final fold; **not testable** for unique originating ancestry. Repeating downstream agreement does not close upstream readiness. The retained static and runtime evidence is the lower-cost answer. |

### H6 — Are preview and established descriptors equivalent?

| Decision dimension | Assessment |
|---|---|
| Materiality / prior knowledge | Equality could constrain input sufficiency, but only for actual matched descriptors/context/cache. Static callers converge on the updater through distinct preview helper `0x00b4cee0` and established builder `0x00f4a140`; vertical bounds may differ. |
| Competing explanations | Nearby preview/Workshop contexts may differ in center/index/domain, radius, upper scalar, initialization and retained cache state. Even equal recorded operands need not establish equal coverage/currentness. |
| Captured / missing | Tag 101 records callsite, descriptor and scalar bits. It does not independently certify an incidental initialization call as an established player Workshop or capture full material cache epochs. |
| Actual action | The first card explicitly omits the established-Workshop scenario. It neither requires visiting an existing Workshop nor matches it to the preview. Incidental init/operation events are opportunistic, not the missing controlled scenario. |
| Outcomes / controls | Preview-only records cannot compare the paths. Incidental differing/equal descriptors do not qualify ownership and matched context/cache. No established event says nothing universal about that path. Loss/missing identities invalidate even an opportunistic comparison. |
| Proof category / payoff | **Not testable by the actual first card.** It cannot be counted as payoff without expanding the experiment. No such expansion is implemented or proposed here. |

## Primary-objective gate and strongest case for GO

| Core objective | What perfect planned capture could add | Why it would not settle the uncertainty |
|---|---|---|
| Sufficient readiness / complete current region data | Source-visit observations, header identities/capacities and opportunistic provider boundaries | Complete-generation and prerequisite-exit histories remain compatible with those samples. No expected source census, completion certificate, qualified reset epoch or geometry ground truth. |
| Native spatial equivalence / concrete query inputs | Actual indexed descriptor/scalars and final populations, already observed by 0.7.0, plus new source headers | Region geometry, actual translation table, FP qualification and paired accepted/rejected candidates remain absent. Final populations cannot invert the missing candidate decisions. |
| Preview/Workshop convergence and player-position requirements | Preview operands and incidental callsite classifications | No deliberate established scenario, no matched context/cache control, and no independent player-position measurement or displacement scenario. A moved preview is not evidence of an independent callable contract. |

The strongest GO argument is that live source/provider events could validate
reachability and correlate header changes with refresh and UI transitions.
Those are real potential observations. A surprising pattern might challenge a
static interpretation and justify a later question. However, no specified
attainable pattern supplies the missing completion/coverage/decision oracle.
Unexpected corruption or an unexplained contradiction is not a predeclared,
decisive test of sufficient state. It cannot justify thirteen hooks solely on
the possibility that something surprising happens.

For example, the same observed empty/unchanged source headers and final set can
fit a complete context with no additional eligible regions or an incomplete
context whose missing sources would have added resources. The same visited
source header can hide different region/point contents. Matching nonempty final
populations similarly cannot exclude an omitted resource elsewhere. These are
specific unmeasured distinctions in the traced dependency graph, not demands
for reconstructing every engine exception.

There is no mandatory controlled comparison of readiness states in the card.
Loading Save3 and moving the preview can change geometry selection, lifecycle
state and retained cache together. Temporal association of provider/scan/UI
events cannot isolate those changes. More A/B/C repetitions do not resolve the
unobserved variables. Any loss or failed capacity guard yields less evidence;
it cannot strengthen absence, freshness or completeness claims.

## Disposition and cost

The existing thirteen-hook capture adds timing and memory-read risks, possible
capacity loss, player setup/gameplay/exit time, raw evidence volume, full
postflight processing and independent review. No new cost benchmark was run.
The earlier 0.7.0 capture's 611,926 records occupied 2,036,489,728 raw bytes;
that is historical context, not a prediction or quota for 0.8.0. Sunk build and
qualification work contributes no scientific benefit to the decision to run.

**NO-GO**, rather than GO or REVISE: useful preparatory knowledge survives, but
there is no proportionate, specified first-session test that resolves the stated
core uncertainty with the current fields and controls. Closing spatial or
readiness gaps would require a separately justified design, new observables and
validation; its safety/cost and decisive oracle are not established here.
No minimal revision has been demonstrated to warrant intervention now, so this
assessment does not turn the gap into an automatic new instrumentation project.

Engineering qualification remains historical evidence about the built candidate;
it is neither disproved nor a reason to adopt it. The earlier review failed to
catch malformed prose and did not adequately distinguish engineering acceptance
from a consequential scientific test. Its actual returned text is preserved in
[the historical review](independent-review.md), with explicit supersession.

This reassessment changes the recommendation and documentation, not native
findings, confidence classifications, schema bytes, code, saves or protected
evidence. No observer rebuild/test, DLL/ZIP change, deployment, game launch,
native invocation, staging, commit or push was performed. Stop here for
ChatGPT/user critical review; there is no implied next capture or redesign.
