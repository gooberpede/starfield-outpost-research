# P3 native integration qualification

2026-11-01, Australia/Sydney. **P3 COMPLETE / ACCEPT within its offline
integration scope. Independent technical/scientific and editorial review accepts
all five questions and eight criteria. D5AB INCOMPLETE / REWORK; D5R OPEN;
P4/B2 NOT AUTHORIZED.**

The compiled schema-4 observer now supports a positively source-qualified first
processing chain and a separately verified later bypass in disposable native
hosts. Independent state/operand oracles verify the actual publication and token
writes. Concurrency, retirement, reuse, collisions, owner replacement, native
exceptions, store failure, transport faults and incomplete histories produce
appropriate partial evidence or conservative refusals. This is offline instrument
qualification; it is not a retail target event, historical B1 reconstruction,
complete game-generator execution or permission for B2.

[Original P3 contract](../../implementation-briefs/CODEX_BRIEF_SOR_RG2_D5AB_P3_native_integration_qualification.md),
[active ledger](d5ab-p3-investigation-ledger.md), [scenario/oracle matrix](d5ab-p3-scenarios.md),
[transport/controller qualification](d5ab-p3-transport.md),
[source and reproduction provenance](d5ab-p3-provenance.md),
[parent mapping](d5ab-p3-parent-mapping.md), [review record](d5ab-p3-review.md).

## Answers to the frozen questions

| Question | Implementation outcome | Supported answer and remaining qualification |
|---|---|---|
| P3-Q1: integrated native lifecycle | COMPLETE | The final compiled producer records birth/publication, selected/visited, protected lookup, consumed descriptor, generator/sample, reserve and actual store. A no-bypass first chain and a later membership-derived bypass both qualify under independent host oracles. Reset/retirement and alternatives remain visible. Engine provider/generation policy is emulated where documented; native instruction and ABI equivalence is separately pinned. |
| P3-Q2: concurrency and adverse identity | COMPLETE | Four competing unvisited requests produce one protected miss and three waiting hits without inventing first-request order. Detached retirement, real same-address reuse, equal tokens, distinct owners, publication gaps and installed-owner replacement refuse false continuity. P1's native ordinary lifetime graph remains the ownership premise; callbacks do not acquire a fictitious lease or reread a selected source. |
| P3-Q3: integrated recorder/controller | COMPLETE | The actual producer, worker, controller and reader pass declared lossless workloads and independently accounted overload/fault/STOP cases. Sampled loss tuples can be incoherent; this is reported separately from authenticated durable bytes and scientific qualification. All recoverable admitted evidence remains local. Operational retail adaptation remains P4 work. |
| P3-Q4: chronology correctness | COMPLETE | The final reducer distinguishes first processing, direct mask, successful/failed reserve/store and later bypass; rejects incomplete, duplicated, contradictory, reused or ambiguous histories; and preserves partial/reset-scoped evidence without silently promoting lossy sessions. Schema-2 B1 and accepted schema-3 result comparisons remain equal. |
| P3-Q5: offline deliverable integrity | COMPLETE | Independent Review01 accepts the exact source/build/schema/fixture/consumer/controller bundle, identical-DLL reproduction, requirement mapping, primary evidence and verified delivery artifacts. P4 readiness and retail execution remain open. |

Confidence is high in the pinned STATIC dataflow/ownership premises and decisive
finite disposable-host observations. Coverage is the enumerated ordinary native
graph, exact compiled paths and declared workloads. It is not a census of every
engine scheduler, allocator, content override, corrupted object or retail state.
The frozen P3 questions concern that offline integration scope; the broader
historical/retail D5R question remains OPEN.

## Corrections and actual tested layers

P1 removed the unsafe source read at lookup. P3 preserves its constructor-private
semantic snapshot and allocation/publication/epoch/order checks. A runtime address,
visited token, source allocation serial, geographic key and owner are distinct.
Observed invalidation or missing continuity refuses the join. Actual host
deallocation/reallocation and owner-slot changes test those refusals. The full
engine owner replacement and generator remain emulated where documented.

P3 replaces the five naked midfunction JMP bridges with CALL-entered RBP-framed
helpers. Normal return preserves a real original-image PC. The visited window
widens to thirteen guarded bytes, keeping its conditional branch in the original
image and replaying the displaced stack store only on non-bypass. No return
address is rewritten. The erase trampoline registers partial-prologue unwind
metadata and uses a guarded RAX-dead register tail. These choices follow the
platform constraints in Microsoft's [x64 unwind documentation](https://learn.microsoft.com/en-us/cpp/build/exception-handling-x64),
[prologue/epilogue rules](https://learn.microsoft.com/en-us/cpp/build/prolog-and-epilog)
and [shadow-stack policy](https://learn.microsoft.com/en-us/windows/win32/api/winnt/ns-winnt-process_mitigation_user_shadow_stack_policy).
They are independently tested, not justified solely by those references.

All 226 declared instruction/frame contexts recover the expected caller state
through actual RtlVirtualUnwind. A separate exact-object caller with deliberately
clobbering callback stubs passes thirteen register/flags/stack/store checks,
including birth's output RCX/RDX and visited's displaced store/bypass. Actual
generator/reserve C++ throws restore observer state. A deliberately inaccessible
store destination produces the expected unhandled host access violation, with
the flushed pre-store prefix preserved and no fabricated Stored event. Host
survival fails in that declared fault control; evidence completeness is separate.
The observed Windows/ntdll implementation and platform limits are recorded in
the provenance. Arbitrary corruption and universal exception safety are not claimed.

The query join uses more than pointer proximity. Twenty-three exact retained
native instruction facts connect the original Int2 and consumed descriptor to
projection, generator geographic argument and the direct sampler. Source-origin
Int2 and geographic doubles are separate operands. The native host independently
checks distinct buffers and recorded query/source/owner associations. This does
not execute the complete engine projection/generator or establish retail geometry.

The consumer now rejects malformed reset native order, duplicate/late-duplicate
boundaries, late publication contradictions and observed early/duplicate return.
It separates byte-prefix authentication from sampled loss metadata. Missing or
contradictory bounds/generation cannot qualify a reset scope; a sampled bad tuple
cannot discard a later valid byte-authenticated prefix. A complete later empty
reset and fresh source lifetime can support a conditional recovered witness.
Global retail/whole-session firstness flags remain conservative. Sample/store
alone never proves nonempty or complete geometry.

## Exact qualification inventory

Final candidate DLL SHA-256:
`9d2f0bab159f3ec23186426fb4833eb645578d2a43612bb2e8def6b1af455dcc`.
Final04 and Repro02 have identical DLL bytes and exact packaged consumers.
The [provenance recipe](d5ab-p3-provenance.md) lists every actual command and local
receipt. `d5ab-p3-test-results.json` binds final source/component/receipt hashes.

| Check | Actual final result / limit |
|---|---|
| Native build | 90/90 expected exits; includes four declared host-crash exits, not 90 surviving targets. |
| Native independent oracles | 257/257 checks, all 24 P3 families; includes 226 unwind contexts. |
| Reproduction / bridge ABI | Four same-input controls; identical DLL; thirteen exact-object ABI checks. |
| P3 consumer / P1 full regression | 133/133 and 316/316; exact packaged consumers and historical result equality. |
| Actual worker/controller / sharing | 26 controller cases and one held-publication sharing control. |
| Full producer capacities | Nine scenario/capacity combinations; 32,768-cell representative/burst lossless at 21,061/12,018 offers; smaller queues expose measured losses. |
| Queue alone | Nine executable runs; all paced 16,000-offer workloads lossless; held 32,000-offer bursts lossless at 32,768 only; hot/unpaced loss retained. |
| Independent raw/ACK audit | 216,979 frames and 413 prefixes across 88 sessions; stable terminal reconciliation; one reported sampled-telemetry inconsistency. |
| Original native / legacy semantics / worker lease | Eleven original-instruction controls; 54 original semantic oracles; nine own-thread identity/death controls. |
| Disposable protection / static query join | Sixteen policy/content/backup/disk checks; 23 pinned dataflow facts; no actual B2 preflight. |
| Combined provenance | Exact final inputs/outputs/consumers/receipts, seventeen original P1 exports, 826 historical preservation records and unchanged HEAD/index required. |

The 32,768-cell queue is justified by finite measured headroom, not declared
optimal. Retained-event rates, occupancy, writer phases and losses are in the
transport report. Its phase scopes overlap and include deliberate pauses and
competing local work; no B1 lost-event timestamps or universal lossless rate are
invented. The full native producer remains distinct from the queue-only harness.

## Mandatory acceptance matrix

| Criterion | Current outcome | Primary evidence and limit |
|---|---|---|
| P3-AC01 | PASS | Baseline/brief/identity pins, actual authorized offline operations and ledger; no retail deployment/launch/save mutation or Git integration. |
| P3-AC02 | PASS | Final04 compiled lifecycle and independent operation/memory oracles; normal first chain, later bypass and all required alternatives. Host/retail distinctions explicit. |
| P3-AC03 | PASS | Native competing/retirement/reuse/token/owner cases, P1 lifetime graph, 226 unwind probes and thirteen object ABI checks with exact guards/width. |
| P3-AC04 | PASS | Final worker/controller/sharing, complete-producer capacity/oracle, queue and raw/ACK audit receipts; truthful loss/fault/refusal and guard behavior. |
| P3-AC05 | PASS | Exact final packaged consumers pass native positives, 133 new counterexamples, 316 original controls and full B1/schema-3 result equality; partial evidence retained. |
| P3-AC06 | PASS | Final04/Repro02 exact identities, all affected regressions, preserved original failures and version correspondence; final provenance receipt controls the claim. |
| P3-AC07 | PASS | All AB-Q1–Q5 and AB-AC01–AC12 mapped; B1/D5AA/D5R and publication status unchanged; draft card remains NOT AUTHORIZED and controller refuses retail. |
| P3-AC08 | PASS | Independent Review01 accepts the exact tree, primary evidence, failed controls, complete prose and verified complete/task-only patches. The review record preserves the actual return and closing delta verification. |

## Failures, residual work and authority

The ledger and provenance preserve the failed initial unwind, late-duplicate/
return/reset/telemetry/prefix counterexamples, ABI linker failure, source-overlap
builds and valid superseded combinations. New tests and fixes were requalified
without rewriting earlier evidence. The first full-package freezes were violated
by later in-scope reader changes; those runs are explicitly excluded from final
correspondence. Final04 is the exact later combination.

Independent review challenges the frozen brief and primary evidence and finds
no material mandatory P3 branch unresolved. All five questions are COMPLETE
within the declared offline scope; no engineering branch is deferred as optional.
P4 must reconcile the full parent bundle, retail-capable operational adapter,
protected preflight/health/STOP/postflight/archive plan and exact readiness review;
no P4 work or B2 action follows automatically. Full protected-input checks apply
only to a separately approved future retail run; P3's disposable parity checks
cannot stand in for them. The gameplay checklist is unchanged.

Implementation evidence and scientific witness logic pass at the declared
offline scope; target survival is not applicable to any retail game, and declared
disposable crashes remain failures of host survival. Publication remains ON HOLD;
raw/native/private artifacts stay LOCAL-ONLY and authored work REVIEW-REQUIRED.
No new third-party incorporation, permission exception, external disclosure,
deployment, protected-save change, staging, commit or push occurs.
