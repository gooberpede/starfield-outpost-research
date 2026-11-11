# D5AB P2 controller, transport and consumer qualification

2026-11-01, Australia/Sydney. **P2 COMPLETE / ACCEPT for offline engineering.
D5AB INCOMPLETE / REWORK; D5R OPEN; B2 NOT AUTHORIZED.**
[Contract](../../implementation-briefs/README.md#archive-lookup) (`implementation-briefs.zip :: docs/implementation-briefs/CODEX_BRIEF_SOR_RG2_D5AB_P2_controller_reducer_transport_qualification.md`),
[active ledger](d5ab-p2-investigation-ledger.md),
[parent mapping](d5ab-p2-parent-mapping.md), [provenance](d5ab-p2-provenance.md),
[review](d5ab-p2-review.md).

| Element | Answer and scope |
|---|---|
| Question | Do the exact final recorder, controller and consumers meet the four frozen P2 engineering questions? |
| Best-supported result | The exact final disposable recorder/controller retains all admitted records in declared lossless workloads, distinguishes actual worker failure from delay and refuses damaged, incomplete, ambiguous or loss-contaminated finalized claims. |
| Evidence basis | Native06's 61 cases, an identical-DLL rebuild with two controls, 26 controller cases, one deterministic actual-worker sharing control, 202 consumer checks, 54 legacy semantic regressions and nine queue runs all pass. Independent Review03 accepts the scoped result. |
| Coverage | Existing eighteen-site observer and seventeen event kinds, three queue capacities, ordinary finite competing workloads, deliberate faults and damaged derivatives. No retail observation or new source-lifetime proof. |
| Limitations | P1/P3 ownership, initialization, alternate cleanup, detached reuse and actual engine schedules remain unqualified. No finite offline workload proves universal zero loss or complete native coverage. |
| Publication | Authored code/summaries REVIEW-REQUIRED; native bytes, binaries, raw captures and private receipts LOCAL-ONLY. No release or publication authority. |

## Architecture and operational boundary

Production queue/hook layout, source operand acquisition and assembly sites remain
unchanged. The recorder adds disposable fault branches for unexpected worker exit,
guard refusal and omitted terminal output; existing writer/flush/ACK/disk controls
remain. The guarded fixture accepts a controller-host scenario and small commands
only inside its own output directory. These branches neither discover new engine
sites nor prove native lifetime safety.

`runtime/construction-winner/controller.py` is the actual controller exercised by
the P2 tests. It retains a query/synchronization handle for READY's worker TID and
creation FILETIME, verifies process birth, expected session identity and DLL hash,
and holds an exclusive Windows file lock. Its challenge response must authenticate
the exact raw/ACK prefix and current worker identity. A live thread with a pending
ACK remains `ALIVE_ACK_PENDING`; elapsed time alone never becomes worker death.
Counted losses remain visible as `ALIVE_LOSS` while safe capture continues.

STOP contains the controller owner, session-identity digest and unique nonce.
Successful closeout requires those exact STOP bytes, actual worker exit, matching
terminal identity/counts and independent closed raw/ACK readback. A foreign STOP,
unexpected exit, output/guard fault or absent/damaged finalization has a distinct
failure/uncertainty state. Controller disconnect or process death releases the
lock; reconnect binds the worker anew and requires a fresh challenge. It does not
inherit another controller's successful STOP ownership.

The controller accepts disposable sessions only. The older `worker_health.py
--watch` loop remains an unqualified future helper and is not used for P2's STOP
classification. Retail admission, deployment and operational integration remain
separate P4/maintainer gates. No process is attached, paused, killed or unloaded by
the controller. Resident observer wrappers remain inert after shutdown.

Schema-3 consumers retain authenticated `candidate_chains` and diagnostics when
session damage, incomplete finalization or loss prevents final chain claims.
Malformed, duplicated or regressing ACKs and inconsistent loss/terminal totals
are rejected. Duplicate invocation/selection identities and reversed native clocks
refuse chronology. A first construction does not require an artificial later
bypass. The new output explicitly sets native-source-lifetime and scientific
firstness qualification to false: passing witness logic is conditional on the
still-open P1/P3 observation premise. Schema-2 B1 retains its historical result.

## Workload rationale and measurements

B1's 19,780 admitted records and 9,957 untimed lost attempts cannot reconstruct
an arrival stream or prescribe a sufficient queue. P2 therefore declares separate
engineering envelopes: a 32,000-offer held burst; 96,000 unpaced competing offers;
76,800 hot-round offers; and 16,000 paced concurrent offers. Exact successful
producer IDs and order are compared with consumed records. The paced workload
qualifies only its measured envelope; it is not a maximum writer service rate.
The native representative case independently exercises all seventeen categories
under a three-second raw-flush pause. Intentional overload must count losses and
refuse stronger firstness claims rather than masquerade as lossless capture.

Cells measure 320 bytes for a 312-byte event. Queue allocations are 327,680,
2,621,440 and 10,485,760 bytes at 1,024, 8,192 and 32,768 cells. Whole-process
working set includes test data/runtime overhead and is reported separately in
the primary receipts. Hot competing producers can exhaust the 32-retry bound
without filling the queue; increasing capacity alone cannot cure that mode.

The final queue suite has nine passing runs with unchanged source. All nine
16,000-offer paced workloads lose zero events, at measured 830.43–1,303.70
records/s and sampled high-water lower bounds of 16–36. These are offered-load
measurements under competing local tests, not maximum recorder service rates.

| Cells | Held 32,000-offer losses, each repeat | Hot-round contention loss range | Unpaced loss range |
|---:|---:|---:|---:|
| 1,024 | 30,976 | 20–41 | 48,288–53,643 |
| 8,192 | 23,808 | 17–56 | 9,551–55,618 |
| 32,768 | 0 | 32–71 | 9,495–23,635 |

The held burst is qualified lossless only at 32,768 cells. Smaller held bursts,
all hot-round workloads and all unpaced workloads are intentional loss controls;
they must not receive a zero-loss verdict. Queue working-set ranges, actual
cause totals, per-repeat results and original failures are in the transport notes
and `.local-work/d5ab/p2-queue06/receipt.json`.

## Final tests and frozen P2 accounting

All final source, receipt and DLL pins are in the selected
[test summary](d5ab-p2-test-results.json). The reproducible verification script is
`research/resource-retained-population/d5ab_p2_provenance.py`; its final receipt
is `.local-work/d5ab/p2-provenance02/receipt.json`.

| Final suite | Result | Exact local primary receipt |
|---|---|---|
| Compiled DLL and existing native cases | 61/61 expected exits; source unchanged; no unexpected failure. Declared crash cases retain their expected exits. | `.local-work/d5x/p2-native06/build.json` |
| Same-input DLL reproduction | Identical DLL bytes; 2/2 additional controls; source unchanged. | `.local-work/d5x/p2-repro01/build.json` |
| Actual recorder/controller | 26/26 cases; source unchanged; positive/impairment/STOP/readback and six ACK loss controls. | `.local-work/d5ab/p2-controller07/receipt.json` and its per-case receipts |
| File-sharing interoperability | 1/1 actual-worker control; actual old-policy error 32; final held-handle command, loss and STOP reconcile. | `.local-work/d5ab/p2-sharing01/receipt.json` |
| Final producer/consumer pair | 202/202 checks; final packaged-consumer hashes match; schema-2 B1 full result unchanged. | `.local-work/d5ab/p2-reader-final02/receipt.json` |
| Original collision/order semantic regressions | 54/54 original explicit fixture oracles, including equal token/different source, different token/same geography, altered ancestry, shuffled arrival and fresh-boundary recovery. | `.local-work/d5ab/p2-legacy-semantics01/receipt.json` |
| Three queue capacities, three repeats | 9/9 executable runs; exact admitted IDs/order; qualified envelopes lose zero; overload losses accounted. | `.local-work/d5ab/p2-queue06/receipt.json` |
| Historical evidence preservation | 826 existing local files/absence records match the C2 preservation pins. | `.local-work/d5ab/p2-provenance02/preservation.json` |

The native representative fixture retains all 21,061 admitted records with zero
drops/output faults and identical written/flushed/acknowledged totals. Its sampled
queue high-water lower bound is 11,338 cells; peak process working set is
15,294,464 bytes. The raw-flush phase maximum is 3.1150391 seconds, including the
injected three-second pause. Legacy in-call flush timing excludes that injected
sleep and must not substitute for the phase measurement. This qualifies the
declared transport envelope, not complete native-event observation or retail.

| Frozen question | Independently reviewed outcome | Evidence and scope |
|---|---|---|
| P2-Q1 | COMPLETE | Queue06, Native06 representative/fault/STOP cases, Controller07 and authenticated readback establish the stated finite envelopes and honest overload accounting. |
| P2-Q2 | COMPLETE | Actual retained DLL worker handle, delayed flush, worker exit/fault, controller death/restart, stale identity/ACK and owned/foreign STOP controls. |
| P2-Q3 | COMPLETE | Final02's 202 checks and 54 original semantic regressions bind producer/consumers, preserve B1 and reject session/identity/collision/loss/native-order counterexamples. Native lifetime remains unqualified. |
| P2-Q4 | COMPLETE | Review03 accepts exact component lineage, source/evidence/delivery snapshot, parent mapping and editorial quality. The review record governs final closure verification. |

| Mandatory criterion | Final result | Exact evidence and scope |
|---|---|---|
| P2-AC01 | PASS | Admission HEAD/permission ledger, build identity checks and unchanged observer/assembly/acquisition-source hashes. |
| P2-AC02 | PASS | Queue06, Native06 and Controller07; measured lossless/overload/flush/wrap/publication/fault and STOP controls. |
| P2-AC03 | PASS | Controller07's real worker/controller cases plus Sharing01; no Python-thread substitution. |
| P2-AC04 | PASS | Reader Final02 plus 54 unchanged original semantic fixtures, exact packaged hashes and preserved Build08 mismatch; collision/order/loss controls and B1 regression. |
| P2-AC05 | PASS | Actual DLL in disposable hosts, 61 cases, repeated identical DLL build and combined current-source tests; failures retained. |
| P2-AC06 | PASS | All four P2 questions, five parent questions and twelve parent criteria mapped without P1/P3 closure or B2 authority. |
| P2-AC07 | PASS | Independent Review03 accepts exact-snapshot engineering/completeness and editorial quality; all material challenges were corrected and requalified. |
| P2-AC08 | PASS | Review03 verifies both patches, all 26 changed/supplied text paths, exact forward/reverse bytes, exclusions and unchanged HEAD/index. Final closure uses the same checks. No prohibited operation. |

Engineering tests and evidence integrity pass at their declared scope. Scientific
retail readiness remains unqualified; the full parent remains INCOMPLETE / REWORK.
Editorial and independent completion dispositions are supplied in the review
record. These separate outcomes must not be collapsed into B2 readiness.

## Failures preserved and limits

The first controller test used a 20-second finite engineering admission wait and
expired before the host's sole-thread admission completed. Its STOP cleanup and
eventual closeout remain in `p2-controller01`; no target was terminated. The test
wait was increased to distinguish host startup from worker death. The controller
itself has no such retirement timer. A broad process-inventory diagnostic returned
Windows `Access denied`; that broad CIM query was not repeated or escalated.

Early queue proposals treated hot contention as lossless and failed; those are
preserved as counterexamples. Later hot workloads intentionally measure retry
losses, while the independently declared paced envelope must lose zero events.
Intermediate build/queue runs overlapping consumer/test-source edits explicitly
fail final source-identity checks and are not final combined qualification.
Native01–Native04 each complete 61 expected-exit cases but are not final combined
source qualification. Controller02 passes 16 development cases; Controller03
passes 16/17 and Controller04 passes 19/20, each preserving one intermittent
fixture text-read failure. The bounded Windows command-reader correction passes
all twenty Controller05 cases. Controller06 adds six loss-telemetry controls
and snapshots its exact controller/consumer/test source before execution, but
passes only 25/26: its loss-denial host fails while opening the command file.
The failed line is recorded; its original Win32 error and exact cause are UNKNOWN.

The final fixture matches the production request reader's read/write/delete
sharing contract and logs open errors immediately. It retries only sharing or
lock violations for finite offline command admission; other errors fail directly.
A separate actual-worker interoperability control deterministically holds DELETE
access during command publication. The old share-read-only policy returns actual
Windows error 32, while the final fixture consumes the same command under the
held publication handle and reconciles the resulting loss and owned STOP. This
supports the sharing correction without retroactively proving the historical
failure's cause. Final qualification uses Native06 and Controller07; the separate
same-input Repro01 build produces identical DLL bytes and passes two controls.

Independent review reproduced missing READY, contradictory terminal faults,
nine Generated-event context errors and two adverse native-time/admission-order
cases that the earlier consumer accepted. The baseline failures, remedies and
202-check development rerun are preserved in the reader notes. The final reader
also requires READY and clean output-fault telemetry and validates Generated
context through append. A birth-through-store partial-order fence check rejects
delayed publication and unordered cross-thread ties while allowing a lifecycle
entirely after store. Those schedule fixtures test conditional interpretation;
they do not prove that exact native producer schedule occurs.

The controller now reconciles typed loss/cause totals with the authenticated
durable prefix and prior challenges. Its monotonic-counter negative explicitly
models a prior larger counter in controller state while the real worker continues;
it is not reported as an observed native counter regression.

The final review found that the new 202-check driver had omitted several original
collision controls. A separate adapter executes only the unchanged owned
`d5ab_qualify.py` semantic AST block, lines 105–230, with the exact final packaged
consumers. All 54 explicit oracles pass. The selected source, original full source
snapshot, line bounds, fixture hashes and results are retained. Historical
native-session prefix-chain expectations are intentionally outside this adapter;
the stronger new finalized-session behavior is tested by Final02. No old receipt
or oracle is rewritten, and no native rebuild is needed for this pure regression.

The reader specialist's first JSONL mutation harness incorrectly parsed a whole
JSONL stream as one object; its failure remains preserved. Historical Build08
ACK/prefix comparisons and later consumer versions remain distinct. The exact
final source/build lineage must resolve the mismatch through new qualification,
never by editing historical receipts. See the specialist
[transport notes](d5ab-p2-transport-notes.md) and [reader notes](d5ab-p2-reader-notes.md).

No gameplay checklist item changes. Offline fixture output is not an observed
historical target construction, source lease, generated geometry or retail winner.
No protected save, configuration, analysis database or deployment is modified.
