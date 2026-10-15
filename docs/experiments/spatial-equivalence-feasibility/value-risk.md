# Scientific value, safety and minimum revision

[Report](report.md), [exact boundaries](boundary.md), [coverage](coverage.md).
This is an assessment of a proposed observation, not a run card or integration
recipe. Hooks alter instruction execution and timing even when they intentionally
change no gameplay state. No future hooked observation is called non-invasive.

## Value threshold before any observer build

A worthwhile design must pair complete multi-point region inputs with native
acceptance **and rejection**, together with enough path evidence to distinguish
containment from vertex/height and 3D-edge outcomes. These are unresolved and
material assertions in the reconstructed evaluator: direction normalization,
native polynomial rotation, tapered widths, height-independent containment,
absolute upper test, open point-path traversal and closed 3D quad edges. Perfect
capture could contradict or support those assertions within observed coverage.
It would not establish generated-source completeness, remote querying, extractor
placement, save persistence or even coverage of an unexecuted native branch.

Conditional single-region replay needs no global cache epoch, complete source
census or final UI telemetry. Adding those would increase burden without making
this comparison more independent. A narrow broadphase/count-only experiment is
possible in principle with fewer operands, but mostly confirms strongly supported
static transcription and leaves the consequential multi-point reconstruction
untouched. It is not the recommended substitute for Experiment A. Helper-only
wrappers can test vertex or segment arithmetic at ordinary CALL boundaries, but
cannot validate normalization, rotation or the full region decision. No native
inputs currently demonstrate those helpers would provide a proportionate stand-alone
scientific payoff.

## Engineering evidence and unresolved risks

| Issue | Existing evidence / consequence |
|---|---|
| Instruction/ABI integrity | 0.8.0 `patch.h` qualifies guarded five-byte CALL replacement, not arbitrary inline branches. P16 region entry/accept/reject sites are internal blocks; ordinary four-channel wrappers may clobber live volatile registers and flags. Full live state, RIP-relative relocation, incoming control flow, unwind and continuation must be explicitly qualified before use. No exact patch length/byte guard is proposed here. |
| SIMD/FP state | `history.h` Environment uses FXSAVE/FXRSTOR and LastError preservation. This is not proof of all AVX upper-lane or flags preservation at a new internal site. P16 uses many XMM registers and AVX instructions. Required preservation must come from site liveness, not an ABI assumption imported from a CALL boundary. |
| Native object validity | The updater's shared ProcGen+40 interval excludes mapped exclusive provider/reset writers. Capture must stay inside that interval and own geometry before release. Other point writers and query/table stability are not established by this lock. Safe read failure is unavailable evidence; it does not validate a stale successful copy. |
| Variable-length data | 0.8.0 owns 3328-byte events with eight Blob fields, each payload at most 0x180 bytes; queue has 4096 nodes. Those are historical engineering capacities, not proposed scientific quotas. Complete count×16 point arrays need a separately qualified admission/copy/commit protocol. Header snapshots alone fail. |
| Callback workload | Existing SLIST emission avoids synchronous heap allocation, file I/O and waiting locks; worker performs hashing/writes/flush. A geometry design could reserve preallocated owned chunks, copy under valid lifetime and commit a complete group. Cost scales with native count; existing tests do not bound that new critical-section time. Reading an unconsumed array tail itself adds target timing/read effects. |
| Nesting/concurrency | Existing TLS parent tokens help normal CALL ancestry; concurrent regions and repeated addresses require per-invocation tokens plus independent pending groups. Source visitation and pointer equality do not prove object identity across lifetimes. Repeated native query reductions require per-use capture or a proven stable interval. |
| Overflow/retirement | Current sticky overflow marks instrumentation failure; preserve this principle. Geometry fragments need declared length/count, completion marker and independently verifiable durable group boundaries. STOP must cease new admission, finish or explicitly invalidate admitted groups, drain and flush, then retire only after no thread can enter an inline continuation. CALL retirement tests do not establish that property for a new internal probe. |
| Operator burden | One natural unplaced-beacon preview with ordinary movement near visible transitions is plausible from 0.7.0; no construction or forced invocation is needed. Native multi-point/negative/height/edge coverage remains opportunistic. Avoid a new game session until offline engineering is qualified; repeated trips or artificial edge forcing are not part of this proposal. |

The useful 0.8.0 inheritance is a set of owned design precedents: same-thread
ancestry, fixed owned snapshots, sticky loss, worker-only persistence and shared
session checks. Its observer, hooks, schema, release and NO-GO card remain
historical; no rehabilitation, rebuild or reuse is required. No new third-party
code, dependency or runtime tool is selected by this assessment.

## Minimum prerequisite and finite exit

The remaining gate is **a disposable offline qualification showing that one
region-entry → accept/reject probe can preserve live state and transport complete
owned variable geometry as an atomic evidence group**. Group atomicity means
completion/transport validity; coherent copying of native memory remains a
separate requirement. The qualification is narrower than a
new observer: no Starfield loading, SFSE DLL, Vortex package, real hooks or live
tooling. It would require a separately authorized offline harness/implementation
because this brief explicitly prohibits observer implementation. This task
inspects the existing source and exports; it does not build that harness.

The prerequisite must establish these concrete facts together:

1. A pinned instruction-byte/site-liveness analysis and disposable equivalent
   control-flow fixture preserve every live GPR, flags, required SIMD/FP state,
   stack alignment and continuation on both region outcomes, including nesting
   and unwind. Test direct count-one acceptance as well as acceptance after
   cleanup, and rejection before RBX advances. Merely finding E8 CALL bytes
   elsewhere is insufficient.
2. A preallocated owned-chunk protocol captures an entire supplied point array
   and matching verdict under simultaneous/nested fixtures without callback
   allocation, I/O, waiting locks or worker dereference of native pointers.
   Corrupt count/pointer arithmetic, failed reads, queue exhaustion and STOP
   mid-group must produce explicit incomplete evidence and retain prior flushed
   complete groups. A fragment prefix must never be accepted as a complete array.
3. The design records actual reduced query/scalar operands at their native uses,
   or supplies a bounded evidence-backed stability argument. A deliberately
   changing synthetic descriptor/table must not produce a falsely qualified
   single-query pair. Inspecting query-header equality twice is insufficient.

These are engineering facts with binary exit criteria, not a request for a
whole-engine reverse-engineering campaign. If any cannot be qualified at these
specific sites with bounded callback ownership and retirement, abstain from the
full experiment and report that failure; do not widen to more source/header/UI
hooks. New observer design/live work would still require separate review after
this prerequisite. No runtime duration, event-count or byte quota is invented.
Memory capacity is an integrity safeguard to be justified against measured
copy/transport costs, not a scientific stopping rule.

## Conditional future scientific boundary

Only after that qualification could a separately approved natural preview run
seek distinct complete region configurations as the proposed bounded experiment.
Scientific stopping is coverage-based: accepted and rejected multi-point pairs
and whichever containment/vertex/edge branches actually execute, or an explicit
insufficient-coverage result when the authorized natural scenario is exhausted.
No promise is made that exact tangency, repeated points, count zero or every height
case will occur. A healthy run is not stopped solely for elapsed time, evidence
volume or a late operator action. Operator STOP and integrity failures remain
binding; partial durable evidence is retained and overload disclosed.

A future card must reference the shared [phase-aware preflight/ACK/STOP/postflight
infrastructure](../../../runtime/session-tools/README.md) and
[lossless archival qualification](../session-infrastructure/report.md), verify
build/instruction identities, protect saves, retain the 40,000,000,000-byte free-space
guard on C: and D:, and disclose timing/patch interventions. None was operated
here. The result may remain NOT TESTED even after a healthy session.

**Recommendation: REVISE.** A real and valuable native decision boundary exists;
applicable full-pair capture qualification does not. Preserve the design and
abstain from an observer build or live session pending the finite offline gate.
