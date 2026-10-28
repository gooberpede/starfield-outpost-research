# D5N minimal causal contract and method selection

2026-10-28, Australia/Sydney. The invoked [brief](../../implementation-briefs/CODEX_BRIEF_SOR_RG2_D5N_alternative_native_observation.md)
freezes AC1–AC8 without amendment. This is Phase A: offline inspection, builds
and disposable Windows qualification only. [Results](d5n-report.md) and the
[proposed card](run-card-d5n-v1.md) do not authorize Starfield execution.

## Required information and replacement tests

The [native register](native.md) gives the exact fields, stack frames, copy
semantics and inspected paths. Addresses below are module RVAs for the pinned
1.16.244.0 image, preferred base `0x140000000`; runtime addresses must use the
measured module base. The selected implementation retains all fourteen sites.
An information requirement is indispensable even where its current trap may
eventually be replaceable.

| Information | Current witness and indispensable content | Stopped snapshot alternative and current disposition |
|---|---|---|
| Qualified demand and first observed miss | Visited `0x79fca3` samples SIL and visited key; lookup `0x79fcd0` samples RAX against capacity. Process/thread lifetime, source membership, current manager/ProcGen/Grid and recovered invocation frame must agree. | Lookup already copies original query and descriptor bytes. A separate query stop is not intrinsically necessary if native dataflow proves equivalent caller/converter operands. The visited operand's survival at lookup is not established by its earlier existence. No merged replacement is qualified here. |
| Construction input | Query `0x79feaf` checks R8/R9 against effective descriptor and original Int2; mask `0x79b8ed` samples actual AL with recovered provider return/frame. | Query bytes at a later stop do not prove the actual sampled mask. D5H/D5I predictions cannot fill a missing mask. The direct mask is indispensable; no demonstrated snapshot reconstructs it after generation. |
| Completed copied region | Append `0x79acf2`: valid returned index, temporary/destination meaningful fields, nonempty count and all ordered point bytes agree. | Final nonempty output alone cannot exclude failed or incomplete point copying. The native false-success paths in native.md remain counterexamples. No final-only replacement is demonstrated. |
| Retained ownership | Complete `0x79ff1d`: generation has returned while ProcGen protection remains held. Actual source slot, wrapper, resource slot, referenced collection/data/index and copied region must agree with append. | This stopped snapshot is the implemented replacement for observing every internal ownership store. Insertion, wrapper allocation, visited marking and a true status are insufficient. It certifies the witnessed region, with surrounding failures retained. |
| Same-population reuse | Later lookup `0x79fcd0`: occupied map hit in the same observed lifetime and the same wrapper/resource/collection/index with identical actual region bytes. | A consumer callback or matching geographic label is unnecessary. A bypass is not a map hit. A hit preceding completion cannot borrow its future evidence. Different later queries remain visible. |
| Owner lifetime | Init `0x79d8b2`, protected post-clear reset `0x79de92`, destroy `0x79d910`, plus a changed current manager pointer. | A manager pointer alone is not a generation counter. An equal map/wrapper snapshot does not exclude destruction and reconstruction at the same addresses. No replacement epoch field is established. |
| Source/Grid lifetime | Related erase `0x975030`, Grid-clear `0x9829b0`, completed SourceInit `0x983140`, completed GridInit `0x9828d5`, standalone SourceRetire `0x982b70`. | Grid-clear's erase at static VA `0x140982a36` precedes free at `0x140982af8`; absent-map retirement and erase-to-free windows matter. The standalone retire path is separate. Later equal pointers/bytes cannot prove uninterrupted ancestry. Keep Grid-clear, implemented through DR0. |

Source/owner retirement poisons pending and retained joins until qualified birth;
reset invalidates them at the protected post-clear point. A miss invalidates a
previous retained join. Capture gaps, bad frames, incomplete reads and unknown
thread lifetimes disqualify subsequent joins. These are observer segments, not
invented native epoch fields. No first observed miss is called first-ever, and
no chain identifies Save52's historical construction or persisted authority.
The region claim needs neither a complete source census nor Workshop callback.

## Acquisition comparison before implementation

| Route | Scientific coverage, intervention and concrete burden | Decision |
|---|---|---|
| Hardware-first, four permanent sites | Windows x64 CONTEXT exposes DR0–DR3. The existing D5E four-decision method lacks completed copied geometry and continuous lifetime fences. Register/stack/memory snapshots are available while stopped; each real CREATE_THREAD must be armed and read back, rather than assumed to inherit coverage. | Not selected as a complete causal method. Four slots are a constraint, not an impossibility theorem. It would require new native dataflow proofs and a per-thread rotation protocol that fences nested/concurrent pending calls and all relevant lifetime events. |
| Hardware-first, adaptive sites or data watches | Query/visited/lookup information may be partly merged. Data watches might detect a selected slot update, but map replacement, in-place occupancy changes, absent-map frees and same-address reconstruction are distinct. Pausing all threads only during rotation does not observe events in the intervening running interval. | Plausible future alternative, not a demonstrated equivalent. No actual retained generation counter or sufficient common destruction/reset barrier was found in the inspected register/exports. Replacing missing witnesses with equal snapshots would weaken the claim. |
| Minimal hybrid | DR0 continuously observes Grid-clear; thirteen permanent INT3 sites retain all other witnesses. No site rotation or new target-side loader is needed. It reuses D5M ownership, all-stop reads, software rearm and durable transport. It still changes scheduling and target control/debug state. | Selected for disposable qualification because it removes the exact repeated fault-site byte patch with the smallest change to the existing complete reader. This is a scoped engineering choice, not proof of lowest possible retail crash probability. |
| More extensive hybrid | Moving three additional sites to DR1–DR3 could remove three further patches, while requiring more mixed-event ownership/queue cases. Remaining software sites and debugger delivery still matter. | Not justified by a site-specific failure or additional scientific information in this task. Reserve the slots; refuse foreign enabled/GD state rather than silently taking it. |
| In-process native observer | Synchronous protected-site copies could supply all fourteen witnesses without debugger exception delivery. It needs a qualified early loader/injection or plugin mechanism, safe instruction relocation, ABI/CPU preservation, hook admission with concurrent threads, copy ownership and durable external acknowledgements. A worker cannot safely dereference borrowed pointers later. | Viable design class, unimplemented here. Existing [geometry-lifetime study](../spatial-equivalence-feasibility/geometry-lifetime/report.md) did not qualify destruction/alias stability; [x87 correction](../spatial-equivalence-feasibility/x87-preservation/report.md) is scoped. Building a new loader/hook framework is disproportionate while a smaller complete hybrid can be tested. No retail deployment is authorized. |

The [earlier DR0 failures](../../audits/exp0002a-crash-dump-comparison.md)
are adverse evidence against any blanket hardware-safety claim: the same game
build faulted at an armed hardware site without corresponding recorded exception
delivery. They concern another subsystem/site and do not prove this hybrid will
fail. Equally, successful D5B hardware captures and disposable tests cannot prove
delivery on every retail thread. The D5M initiating mechanism stays UNKNOWN;
this task neither assigns a hidden-thread cause nor suppresses exceptions.

Microsoft's [debug-event semantics](https://learn.microsoft.com/en-us/windows/win32/debug/debugging-events),
[context API](https://learn.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-setthreadcontext)
and [x64 register declaration](https://learn.microsoft.com/en-us/windows/win32/api/winnt/ns-winnt-context)
support the all-stop/register design (SOR-S-0117, consulted 2026-10-28). API facts
are source-reported; the actual fixture journals test this implementation.
No Microsoft example implementation was copied.

## Frozen disposable experiment envelope

Inputs are original project-authored native-shaped fixtures, their exact build
and the existing owned transport/decoder. They contain no game generation
algorithm. Allowed actions are compilation with installed tools, creation and
debugger attachment to hash-bound sibling fixtures, thirteen software probes,
DR0 execution probes, bounded reads, owned RIP/TF/RF/debug-status writes,
peer suspension/resumption and intentional fixture crash/termination. Focused
queue/thread controls use the inherited fixture-only mechanisms, compiled out
of the retail controller. All scientific layout/region reads remain synchronous.

Outputs are fresh ignored build/source snapshots, raw contexts, control and
event journals, SRO1/ACK receipts, reductions and test results. Risks include
changed scheduling, fixture hangs/crashes and lost coverage. Stop or dispose on
identity/instruction/slot/receipt/worker/pipe failure, either drive falling below
40,000,000,000 caller-available bytes, explicit STOP or the fixture endpoint.
Diagnose test defects within this task; preserve decisive failed controls.
No healthy experiment ends solely because of elapsed time or receipt count.
Fixed synthetic loops define test traffic, not scientific-session quotas.
Cleanup verifies target absence and handle ownership; task-owned scratch may be
replaced. Originals, saves, backups, installed content and analysis state receive
no writes. The active archive-backed preservation method remains authoritative;
the historical four-ZIP discrepancy is neither repaired nor relabelled.
