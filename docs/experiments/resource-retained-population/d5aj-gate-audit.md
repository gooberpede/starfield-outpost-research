# D5AJ experimental gate audit

2026-11-03, Australia/Sydney. **Scientific non-qualification should hold the
dependent comparison action while preserving healthy acquisition and useful
evidence. It is not a machine safety failure.** A qualified baseline remains a
real prerequisite for an interpretable departure/return comparison. The approved
historical Episode A stopped correctly under its consumed card. These proposed
changes grant no new attempt, Episode B, deployment or controller operation.

| Element | Answer and scope |
|---|---|
| Frozen question | D5AJ-Q4: which admission, continuation and STOP gates protect safety/integrity or indispensable evidence, and which represent recoverable uncertainty? |
| Best answer | Retain all actual safety/integrity gates and finite operator actions. Replace blanket scientific retirement with explicit query/departure holds, source-specific qualification and evidence preservation. |
| Basis | Actual [card](run-card-d5ai-episode-a.md), [accepted amendment](../../implementation-briefs/CODEX_AMENDMENT_SOR_D5AI_EPISODE_A_live_2026-11-03.md), [command contract](d5ai-operator-commands.md), `d5ai_episode.py`, `d5ai_a_episode.py`, `d5ai_a_operations.py`, native controller and completed Episode A receipts. |
| Coverage | Offline design and pure policy controls; existing live helpers/cards are unchanged. All future live actions still require a separately approved plan and exact source/package lock. |
| Limit | The policy model is not a live controller qualification. No new process or future gameplay action is tested here. |

## Gate-by-gate disposition

Categories describe the failed observation's purpose, not whether useful data
already collected must be discarded. A gate may protect an indispensable
comparison without justifying a machine-wide STOP. Pending evidence is pending;
elapsed time alone does not prove failure.

| Gate / observed or hypothetical failure | Category | Necessary response | Evidence still useful / action limit |
|---|---|---|---|
| Operator STOP | SAFETY | Honor immediately through owned inert STOP where safely possible; operator owns exit. | Preserve all flushed evidence and partial/failure diagnostics. No termination or hot unload. |
| Protected contents, save classification, namespace or policy mismatch | SAFETY | Hold admission or stop affected experiment; preserve receipts and seek recovery decision. | Existing evidence can remain valid; never overwrite an original from backup. Transient classified autosave/exitsave churn stays diagnostic. |
| Independent Save52 backup/restoration-copy readiness absent | SAFETY | No launch admission. | Offline analysis remains possible; historical archive is not a substitute backup. |
| C: or D: caller-available query fails or is below 40,000,000,000 bytes | SAFETY | Stop affected writes/experiment; retain exact trigger. | Do not continue unbounded acquisition into failed capacity protection. Both drives remain mandatory. |
| Wrong executable, DLL, hook/site guard, session, process birth or source lock | INTEGRITY | No admission; if discovered during acquisition, preserve evidence and request owned STOP. | Earlier independently bounded data may be retained with its actual identity; do not silently rebind a process. |
| Controller/worker actually failed; native recorder failure; output fault/corruption | INTEGRITY | Stop affected capture and dependent actions, preserve partial data and diagnostics. | A complete already-flushed boundary is assessed separately; never invent a clean terminal. |
| Core loss, counter overflow, unexplained epoch, missing/contradictory invalidation | INTEGRITY | Refuse affected source/lifetime history and the dependent comparison; actual ongoing integrity failure triggers owned STOP. | Preserve structural snapshots and narrower qualified prefixes. No source continuity may cross unknown loss. |
| Lifetime journal loss, unlogged cutoff or absent indispensable coverage | INTEGRITY | Refuse affected content continuity and departure comparison. Stop an actually failed recorder. | Before-cutoff completed evidence remains assessable; current geometry bytes alone cannot repair history. |
| `GEOMETRY_ARMED` or fresh exact arm ACK absent | SCIENTIFIC PREREQUISITE | Hold the one permitted consumer action; keep a healthy pending challenge and lifecycle acquisition. | No second label or forced refresh. A natural already-consumed arm is inspected without another query. |
| `BASELINE_PREFIX_QUALIFIED` absent | SCIENTIFIC PREREQUISITE | Hold departure. Run the reviewed read-only prefix method; preserve actual errors. | Continue safe recording and offline interpretation within the approved action set; this alone is not STOP or permission for extra queries/travel. |
| Complete A0 missing, partial/unarmed/cached scan | SCIENTIFIC PREREQUISITE | No departure comparison without an adequate baseline. Do not force regeneration. | Partial geometry, cache behavior, lifecycle history and quality diagnostics retain value. No automatic retry. |
| Target source attribution fails solely on global epoch | RECOVERABLE SCIENTIFIC UNCERTAINTY | Apply reviewed typed source-Grid qualification. Hold departure until a qualified target exists. | All-map geometry and source history remain useful. Different field values alone do not prove unrelated native owners. |
| A source's own Grid clear, actual retirement, owner reset, ABA or unknown relevant fence | SCIENTIFIC PREREQUISITE | Refuse old identity/content continuity. Establish a genuinely new qualified boundary only if the approved finite action set permits it. | This can be an ordinary lifecycle outcome, not an engine defect or machine hazard. No manufactured regeneration. |
| Wrong consumer owner/frame, nonfinite query or incoherent scan | SCIENTIFIC PREREQUISITE | Hold comparison; refuse attribution/availability at that boundary. | Preserve exact bytes and native diagnostics. No guessing a transform or claiming absence. |
| Native generation output is represented but empty/partial; intended quality unknown | RECOVERABLE SCIENTIFIC UNCERTAINTY | Retain explicit UNKNOWN/native quality and actual full represented content. | Complete representation is useful even if intended construction succeeded only partially. Do not turn it into successful generation. |
| Unavailability at a qualified complete consumer boundary | RECOVERABLE SCIENTIFIC UNCERTAINTY | Report measured unavailability and prior storage separately. | A valid scientific outcome; not a reason to crash, force reset or discard evidence. |
| Healthy delayed ACK, operator response or routine poll | RECOVERABLE SCIENTIFIC UNCERTAINTY | Warn if useful and continue safely; request operator direction before any delay-only termination. | No elapsed-time, event-count, evidence-volume or routine-cadence scientific cutoff. |
| Timestamp differs, exact contents equal | RECOVERABLE SCIENTIFIC UNCERTAINTY | Record metadata change and rehash the specifically changed guard; accept equal bytes under the existing amendment. | Configuration retains full content checks. A content mismatch is SAFETY/INTEGRITY, not a timestamp waiver. |

The original card/controller already preserves operator STOP, healthy pending
ACKs, timestamp-content acceptance and both disk floors. The material design
change is the scientific response and versioned prefix predicate. The existing
controller does not automatically call the offline reducer or shut down on its
refusal: the historical hard stop came from the card's measurement rule and
operator decision. No production controller code needs changing to correct
that distinction. There is no justification for removing protective guards.

## Exact prospective amendments and tests

[Proposed replacement card](run-card-d5aj-episode-a-proposal.md) is a separate
full-text derivative of the frozen Episode A card. Its explicit design-only
notice and changed baseline/safeguard language retain the same finite itinerary,
query budget and operator ownership. It replaces scientific retirement with
dependent-action holds, requires the new reviewed checkpoint/source lock, and
preserves safety/integrity STOP. The final local delivery includes an exact
old-card-to-proposed-card diff under `.local-work/d5aj/proposals/episode-a.diff`.
That proposal diff is distinct from the task/complete repository patches.

The [policy oracle](../../../research/resource-retained-population/d5aj_gates.py)
returns proposed decisions only, with `permission_to_act: false` for every
case. Fifty-seven offline states exercise 19 gates at PASS/FAIL/PENDING;
the versioned source predicate separately tests actual qualified A0 and adverse
source/owner/content histories. These are fresh offline tests, not live helper
or gameplay execution. The original 0.7.0 package and consumed cards remain
immutable. A future approval must bind reviewed versioned sources and fresh
plan/source-lock paths; the old plan cannot silently select the new method.

## What may continue in a future equivalent situation

When target attribution is pending but the worker, transport, guards, protected
inputs and capacity remain healthy, lifecycle recording and already permitted
passive observation may continue. A reviewed offline analysis can qualify the
existing A0 without another query. Departure still waits for interpretable A0;
new geometry requests, extra travel or a retry require explicit scope. The
operator can always choose STOP and normal exit. These distinctions preserve
useful evidence without treating normal unrelated Grid housekeeping as a hazard.

GC-30 still needs an actual qualified before/after consumer comparison around
the approved ordinary departure/return, with continuity/reconstruction/availability
and prior storage history. GC-31 needs a separately authorized independent
fresh-process initialization and complete population comparison, with input,
frame and lifetime provenance. Recovering one A0 supplies neither observation.
