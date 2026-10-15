# Native branch coverage and independent comparison

[Boundary/operand contract](boundary.md), [value decision](value-risk.md).
All existing native comparison counts for the rows below are **zero qualified
pairs: NOT TESTED**. Static instructions and synthetic tests support a
transcription; neither is an independently observed native execution oracle.

| Branch / primary static VA | Plausible natural discriminating input | Captured native outcome / independent replay | Limits |
|---|---|---|---|
| XY broadphase; P16 1421e1119..1154 | Query motion toward/away from resident region bounds; both sides of reach | Actual reject edge or passing branch witness; replay separate f32 subtraction/products/addition and strict greater comparison | Exact tangency may never occur naturally. An accepted final resource does not identify a passing region. |
| Point count zero / one; same window | A resident empty-point descriptor or single-point generated region, if such objects occur | Zero rejects after passing broadphase; one accepts directly; replay qualified count without point data | Natural occurrence is unestablished, particularly count zero. A rejected broadphase never tests the count rule. |
| Consecutive tapered strips; P16 1180..1391 | Multi-point generated vein with unequal endpoint widths and nonzero XYZ delta | Complete point sequence → independent normalization, fixed native polynomial rotation and ordered quads; pair with actual region verdict | Native generated population/point distribution absent in current capture; no promised coverage. Partial quad-only capture tests a reduced polygon predicate, not the strip reconstruction. |
| XY containment; P16 13fe..1460 | Proposed beacon center inside a strip; different heights may accompany movement | Four nonpositive cross witnesses lead to native acceptance; replay identical ordered crosses | This branch ignores Z. Naturally occurring height contrast is opportunistic, not a controlled vertical manipulation. |
| Vertex XY radius and absolute upper; P16 148b..14ec / P17 ac50..acf5 | Query outside containment but near a vertex, varying XY and vertex height relative to upper | Actual AL after each helper call, vertex ordinal and consumed inputs; combine in native short-circuit order | False vertex call is only helper rejection; an edge or later strip may still accept region. One true call is sufficient acceptance. |
| Quad edge distance; P16 152d..1714 / PS 141116580..66e0 | Query outside containment near quad edge, with vertex tests failing; height affects full XYZ distance | Native returned distance bits plus the caller's actual JBE outcome; replay endpoints/interior with f32 order | Helper distance alone is not the Boolean oracle. Upper scalar is not applied on this edge path. |
| Segment start/end/interior; PS 141116580..66e0 | Projection outside/inside segment range when edge branch is reached | Actual branch witness and native distance; independent branch arithmetic | These are sub-branch comparisons, separately counted from region-level verdicts. No naturally exact projection endpoint guaranteed. |
| First strip fails, later strip accepts; P16 171f..175c and 1772 | Long multi-point vein and query near a later strip | Ordered strip witnesses and complete array; exactly one region verdict | Earlier strip failure is not region false; a later region skipped after success is NOT EVALUATED. |
| All strips fail; P16 1741..175c | Broadphase admits coarse circle but query lies outside every tapered strip | Actual region reject edge after loop exhaustion; replay every consecutive pair | Need complete array and confirmed loop completion. Source callback exit/final absence cannot stand in for this observation. |
| Repeated-point/zero-length strip | Duplicate neighboring points, if native generation produces them | Native mask/containment path and outcome; replay existing degenerate case | Existing synthetic degeneracy control is useful; occurrence and numeric intermediate qualification are unknown. |
| Tangency, signed zero, rounding / polynomial residual | Naturally close boundaries and ordinary f32 inputs | Preserve input bits, MXCSR and native branch; replay ties-to-even and native fixed-angle constants | No promise of exact ULP/tie cases. Nonfinite, subnormal and unqualified modes stay UNKNOWN, not PASS or false. Native instructions may handle them differently. |

## Pair admission and result accounting

Freeze the independent evaluator source hash and its numeric-domain rules before
examining future verdicts. Decode native inputs and outcomes independently; never
fit widths, translation, tolerances, constants or branch selection to make a
native verdict agree. Run the existing `evaluate_region` directly on captured
complete inputs. Preserve native path witnesses separately from replay's
diagnostic branch label: different true paths can produce the same Boolean.

Use `(session, updater invocation, source callback invocation, thread, nesting,
resource slot, region ordinal)` for pairing, with the relevant native pointer
identities and captured content hashes. Increment a token for every evaluation;
never pair by closest timestamp, pointer reuse, final set membership or record
write order. Native helper calls need strip/vertex/edge ordinals within that
token. Simultaneous invocations cannot share a single mutable pending-region slot.

An admissible pair has complete operand bytes, a native decision edge, correct
ancestry and lifetime, no unqualified mutation, known numeric domain, and complete
transport through durable archival. For multi-point replay, native repeated query
resolutions must agree or a stability proof must apply; otherwise keep all
evidence and mark the single-query comparison UNQUALIFIED. Such a record may
contradict a capture assumption without contradicting the evaluator. Failed reads,
missing edges, overflow, unwind and incomplete STOP groups are explicit integrity
failures or incomplete pairs, never geometric rejections.

Deduplicate *coverage* using exact operand bits, ordered point bytes/count and
numeric environment. Keep identity/frame provenance separately, so identical
geometry from two regions can be reported both as repeated arithmetic and as
different native objects. Report unique configurations and true/false coverage
by executed branch, plus repeat counts, skipped regions and unqualified reasons.
Do not count 20 identical callbacks as 20 independent geometric cases.

Retain every disagreement with original bytes and native decision/path. Re-run
the frozen implementation and first audit pairing, numeric mode and translation
coherence; do not discard a genuine mismatch or revise the model silently. A
confirmed qualified disagreement falsifies equivalence for that configuration.
Agreement supports only sampled branches/configurations, never all geographic
resources or all IEEE-754 behavior. Zero qualified pairs, or a branch lacking
qualified discriminating inputs, is **NOT TESTED**. Repeated all-true containment
does not validate vertex/height/edge rejection.

## Existing offline evidence

The [0.7.0 report](../continuous-beacon-preview/live-scientific-report.md) records
35,574 evaluations and 346 final UI folds; its capture source lacks the region
arrays and paired decision edges. The
[Milestone B ledger](../resource-availability-milestone-b/native-provenance.md)
identifies the precise missing pointees. The
[0.8.0 reassessment](../local-readiness/scientific-value-reassessment.md) confirms
that its source callback result is traversal status and its fields do not repair
the gap. No existing branch has a complete native input/verdict pair, including
the tempting count-one shortcut. Existing synthetic tests and fixed-angle scalar
reproduction remain valuable offline controls and should not be repeated live
merely to increase telemetry. A fresh full-capture replay was not run here because
its documented capture schema cannot contain the missing operands.
