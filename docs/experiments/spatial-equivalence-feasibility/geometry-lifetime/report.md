# Experiment A: native geometry lifetime and consumed operands

2026-10-16, Australia/Sydney. SOR-EXP-0034 / SOR-EV-0042 continuation.
[Invoked brief](../../../implementation-briefs/README.md#archive-lookup) (`implementation-briefs.zip :: docs/implementation-briefs/CODEX_BRIEF_SOR_experiment_A_geometry_lifetime_operand_capture.md`).
Authored interpretation REVIEW-REQUIRED; native exports and receipts LOCAL-ONLY.

| Element | Scoped result |
|---|---|
| Question | Can complete native region geometry and every consumed spatial operand be copied coherently and paired with real region verdicts? |
| Answer | **NO-GO, evidence-bounded inconclusive capture feasibility.** Useful ownership and operand paths are established statically, but the native owner lifetime and payload stability needed for a full snapshot are not established. No live development is approved. |
| G, judged separately | **UNKNOWN / design gate not met.** Append deep-copies ordered points; mapped construction and reset are excluded by the consumer's shared lock. ProcGen destruction has no local acquisition of that lock; callback neither retains ProcGen nor acquires its own source/collection references. The owner destruction fence and alias mutation scope remain unresolved. |
| O, judged separately | **Static source-to-consumer map established; coherent capture design not qualified.** All mapped branches have candidate consumed-value boundaries, including repeated query and radius reads. One entry query/scalar snapshot is insufficient without stability evidence. New inline sites/storage and their ancestry/retirement are not qualified by the terminal-only fixture. |
| Confidence / coverage | STATIC instruction-backed layout/call findings, STRONG scoped ownership interpretation proposed for review. Bounded mapped provider, consumer, copy/free and reference-transfer paths in retail 1.16.244.0; no whole-engine writer census or game execution. |
| Evidence | [Ownership and windows](ownership.md), [branch operand map](operands.md), [correlation/admission contract](capture-contract.md), [verification and independent review](review.md), [exact source pins](sources.csv). |
| Limits | Zero qualified real native operand/verdict pairs. Retail safety and native spatial equivalence remain **NOT TESTED**. A coherent conditional dataflow is distinct from permission or implementation readiness. |
| Next step | Retain the conditional contract for maintainer review. No synthetic test can establish the missing native lifetime fence. Reopening requires concrete native ownership/alias evidence and a separately reviewed acquisition decision; no automatic fixture, observer or live continuation. |

## Decision and alternatives assessed

The strongest positive result is that the region is an owned, deep-copied object,
not a borrowed alias of the generator's temporary points. Its entire point array
is destroyed with its collection. The same ProcGen lock spans the synchronous
consumer and the mapped producer/reset. This supports a **conditional** snapshot
inside the native callback against those paths. It does not supply the missing
owner destruction fence or prove that every reference-bearing collection helper
operates under this lock. No actual concurrent destruction or mutation was seen;
the result concerns missing proof, not an observed unsafe retail race.

The second positive result is a branch-specific consumed-value plan: resolved
broadphase XYZ, per-strip containment XY, per-call vertex XY/radius/upper, and
per-strip edge XYZ/radius. Capturing those would remove the need to assume global
translation-table stability. It requires more internal observations than the two
previously qualified terminals, with invocation-owned storage and distinct helper
ancestry. Static locations alone do not qualify that mechanism.

Borrowing pointers for worker copying fails the required lifetime condition.
Taking an additional engine lock or reference would change the intervention and
does not establish immutability. Re-reading headers or matching two copies cannot
exclude unversioned in-place writes or ABA; the mapped arrays have no established
version protocol. Copying only visited segments avoids unread tails but cannot
supply the complete ordered geometry required to test the frozen full-region
reconstruction independently. Derived quad/helper captures alone remain useful
component tests, with narrower claims. They cannot earn this brief's PASS.

**NO-GO is appropriate rather than REVISE:** the remaining dependencies are not
one finite synthetic proposition. They include native owner/alias protection,
safe complete-copy cost/storage and qualification at multiple real use sites.
An engine-wide writer campaign or enlarged observer would displace the question.
This is neither a universal impossibility finding nor a rejection of the earlier
synthetic/x87 PASS. Historical reports and the unapproved 0.8.0 source are intact.

## Static first gate and fixture disposition

No new synthetic/native-equivalent fixture was implemented or run. A cooperative
ownership stressor would certify its authored lease, not Starfield's owner fence.
A changing-query fixture already detects invalid single-query admission in the
accepted offline qualification. Another correlation/STOP fixture would not
qualify the new native sites or demonstrate real engine lifetime. Each candidate
therefore fails this brief's evidence-triggered information-gain test. There are
no new fixture outputs or negative fixture cases to hash. Existing source and
accepted corrected/uncorrected evidence were preserved and rehashed instead.
No preservation, exception, decoder or evaluator pathway was changed, so their
conditional rerun requirement was not triggered. Verification here is static
evidence, document and patch checking, not fresh state-preservation execution.

## Scientific consequence

A correctly implemented, separately qualified and authorized future live
experiment **could conclusively falsify the frozen spatial evaluator for a
particular admitted native input configuration** by pairing complete coherent
operands with that region's real ACCEPT or REJECT edge. Agreement could establish
agreement for the sampled configurations and executed branches, including negative
candidates and loop exhaustion. Natural scenario exhaustion could also establish
insufficient coverage for this experiment, without calling missing branches false.

It **could not** establish universal spatial equivalence, unexecuted count/strip/
height/numeric branches, all-region or planet-wide availability, source freshness,
generation completeness, persistence or load authority, supported mod integration,
or retail safety from synthetic qualification. The current task supplies no such
native comparison and approves no live observer development.
