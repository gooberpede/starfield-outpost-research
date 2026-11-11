# Workshop caller semantics and the idle-camera hypothesis

2026-10-13, Australia/Sydney. SOR-EXP-0031 / SOR-EV-0039 continuation.
[Authorized brief](../../implementation-briefs/README.md#archive-lookup) (`implementation-briefs.zip :: docs/implementation-briefs/CODEX_BRIEF_SOR_workshop_center_caller_semantics_idle_camera.md`).
Authored interpretation REVIEW-REQUIRED; native exports, raw captures and private receipts LOCAL-ONLY.

**B — completed evidence-bound result, independently ACCEPTED in [review](review.md).** The high
count is dominated by multithreaded bursts of descriptor construction, with sparse
calls between bursts. A regular idle-camera update is not established. Native
consumers explicitly distinguish reference center, indexed descriptor translation
and terrain-query XY translation; neither capture supplies a complete common
three-dimensional frame or the historical writer transition.

| Element | Result |
|---|---|
| Question | What do AD0C36, F4A1D4 and F498F1 consume, and does idle camera explain their contrasting coordinates/frequency? |
| Answer | The shared helper reads current reference XYZ and optional Workshop compensation. The callers use this result for different spatial operations. Captured frequency is bursty and multithreaded; camera activation and camera-induced reference mutation remain unobserved. |
| Confidence | PROVEN / RUNTIME for checked records, counts and sample intervals; STATIC for recovered consumer contracts. Causal history and idle-camera activation OPEN. |
| Coverage | Pinned retail 1.16.244.0; two identities, one 050 new-landing/return and one 060 local-travel session. Complete captured center census, partial lifetime/writer/frame coverage. |
| Evidence | [Native ledger](native-ledger.md), [chronology](chronology.md), [matched-state audit](state-and-acquisition.md), fresh raw/save replay and [review matrix](review.md). |
| Limits | Missing 050 D3/own-parent/producing edge; missing 060 equivalent query activation; no input inactivity/camera-state trace; no full native XYZ equivalence. |
| Next decision | A narrowly targeted same-trigger/same-boundary capture would improve validation; broad repeated descriptor logging would not identify the missing producer. No new observer commissioned. |

## Actual raw result and native meaning

Both original schemas were freshly decoded using the independent project
cross-session verifier, separately from the observer's production decoder.
The chronology composes that pinned decoder; it is a new timing analysis, not a
second independently implemented binary parser. Every 1,194050 and 562,326060
record's journal extent, sequence and SHA256 passes. The original 81 sealed
files, 61 observer build-source pins, executable and archived Save25/26 selected
fields were freshly checked. Existing save decompression is explicitly reused.
Exact input/output hashes are in local `replay-01/pins.json` and
`chronology-02/summary.json`, with a curated [source ledger](sources.csv).

| Observation | 050 | 060 |
|---|---|---|
| Actual returned centers | 40 at AD0C36,20 per identity | 16,824 at F4A1D4; two at F498F1 |
| SOR-002 XYZ | (22.7004547,73.0462341,3.64314747) | (122.7004547,273.0462341,18.3525066) |
| SOR-003 XYZ | (56.8204041,59.0585938,-9.51641846) | (356.8204041,2459.0585938,-31.8908424) |
| Compensation | All twelve bytes zero | All readable selected compensation vectors zero |
| Own+B0 / D3 | Null / NOT CAPTURED | Own cell available / sampled 2 at centers |
| Query ancestry | Actual Q→E→callback, source key 02b20e79528028e0 | Not instrumented; AD0C36 patched but zero events |
| Coherence qualification | Identity recheck excludes coordinate bytes | Four pairs quarantined from coherent before/after claims; all returned output bits retained |

F4AB80 has no caller-selected height mode and does not inspect D3. It writes
its output, without replacing reference XYZ. Checked outputs equal sampled
reference XYZ because compensation is zero. Saved 25 XYZ equals all 060 returned
triples, including retained outputs from the incoherent records; those records
cannot certify sampled identity or arithmetic. Exact offsets/bytes and prior
source-informed interpretation are preserved in the [previous ledger](../cross-session-center/ledger.md).

The 060 sites have distinct purposes: F4A1D4 constructs a shared Workshop
geometry descriptor used by geometric membership, collision, placement and
border paths; F498F1 constructs circular border geometry, whose downstream
builder samples 36 angles. AD0C36 contributes a terrain-query exclusion
rectangle. These are supported spatial consumers, not a unique cadence-owning
camera operation. Which dynamic ancestor generated each 060 burst is unrecorded.

AD0C36 translates only X/Y for the terrain hierarchy operation. Adding captured
(100,200) or (300,2400) reproduces saved 25 X/Y exactly in binary32. No third
translation word is consumed as Z. F4A1D4 builds a descriptor that can encode a
frame index, and F4AC50 conditionally translates descriptor XYZ from that index.
This is an actual native representation contract; the relevant runtime table
and selected descriptor were not captured. It cannot supply the historical Z
operand. F498F1 supplies a separate descriptor/consumer path. The complete
gates, callers, purposes and uncertainty are in the native ledger.

## Idle/free-camera verdict

**Not distinguishable for actual automatic idle-camera activation or a causal
effect on these centers.** The narrower inference that these events form a uniform,
single-thread, one-call-per-camera-update loop is contradicted by the observed
burst/thread pattern.
Neither an operator's settled checkpoint nor time between chat messages measures
input inactivity. No captured camera activation flag, input-idle timer or
camera-linked reference writer exists in these sessions.

The 050 terrain callback is a repeated query enumeration, with forty 050
centers inside approximately 13.46 ms on one thread; this illustrates why a high
instantaneous rate does not imply one camera frame per event. The 060 descriptor
calls span 20/21 threads per coherent identity with submillisecond pooled median
gaps, large inter-burst gaps and sparse background samples. A sampled root
parent 0 means no enclosing *instrumented* TLS scope, not no native caller or job
ancestry. No OS thread role is inferred from its numeric TID.

Static camera ancestry and its counterexamples are audited in the native ledger.
The actual AutoVanityState update and target/collision dependencies were traced,
as was the distinct DebugFreeCamera update. No direct center call or reference XYZ
write was established on those inspected chains; shared generic physics services
do not establish a historical join to the descriptor-collision route.
A camera clamp using a Workshop boundary elsewhere would not establish that
the captured F4A1D4 calls originated from automatic vanity camera, or that camera
operations wrote the reference position. Camera presentation and physical
placement are separate claims requiring their own dataflow.

## Physical stability and numerical state

The user's observation that outposts and surrounding terrain/resources remain
physically stable is a constraint on an explanation. Stable physical placement
can coexist with distinct numeric representations when a proven transform joins
them. Here native XY translation preserves the checked terrain-grid relationship.
The native indexed descriptor mechanism provides another specific frame-aware
consumer contract, with unavailable invocation operands. These facts justify
investigating frame state, but do not prove a shared 3D mapping or terrain height.

The required Z shifts are +14.709359169006348 and -22.37442398071289. Opposite,
unequal differences exclude a common constant correction for these pairs. They
do not exclude per-edge translation, replacement or different reference epochs.
No fitted per-outpost offsets are offered as a native transformation. The saved
controls and 23 frozen predictions remain unchanged; physical stability is not a
substitute for recovering frame identity, native authority or geographic position.

## Evidence boundary

The authorized investigation follows actual consumer, caller, conversion,
restoration, edge-height and observer dependencies to specific unavailable
invocation state, rather than ending at a vague architectural story. Its
[matched-state assessment](state-and-acquisition.md) states what each next
observation would distinguish. No decoder defect, shared compensation shift or
caller-selected F4AB80 Z calculation explains the checked samples. Sampling
selection is demonstrated; scheduling perturbation is mechanically supported;
semantic instrumentation interference and the historical producer remain unknown.
Full native XYZ equivalence is **NOT TESTED**. This scope does not claim an
exhaustive engine writer census, camera impossibility, or programme completion.
