# D5M Phase B post-mortem

2026-10-28, Australia/Sydney. Prepared after successful full postflight.
[Execution](d5m-phase-b.md), [authority](d5m-phase-b-authorization.md),
[exact evidence pins](d5m-phase-b-sources.csv), [historical D5L failure](phase-b-postmortem.md).

**The ownership repair held, but the retail process again faulted at the armed
Grid-clear breakpoint. The faulting main thread has no recorded exception debug
event. The complete recorded continuation trail and last observed Grid-clear
rearm do not explain that missing delivery. Initiating mechanism remains UNKNOWN;
another retail run with this observer is NO-GO.**

| Question | Best-supported result |
|---|---|
| Did the repaired handle paths fail again? | No such failure is observed. Ownership replay closes all 254 registered handles; zero registered/plain owners remain. |
| Did the target hit an observer breakpoint? | The qualified existing dump places TID 3864 at the armed Grid-clear RVA `0x9829b0`, with `0xcc` present and TF clear. Matching Windows records identify the same process/fault. |
| Did the debugger continue that fault unhandled? | Not demonstrated. No exception event from TID 3864 exists in the complete control journal; every recorded continuation used `DBG_CONTINUE` and succeeded. |
| Did the last observed Grid-clear rearm fail? | Its recorded byte/context/rearm/readback/continuation sequence completes successfully on a different thread. This does not establish unseen execution state. |
| Did the scientific test complete? | No. There is no selected-source decision, construction or reuse chain; reported travel did not reach arrival. |

## Dump and Windows identity

The pre-existing OS crash artifact `Starfield.exe.11600.dmp` was inspected read-only
under the ordinary user. No debugger was attached after exit, no new dump was
requested, and no ACL/security setting was changed. Its 152,519,251 bytes have
SHA-256 `01d4c34bd3fe72b64dfccc23d06d83bc895a4fcd4f01cd1ca0e4354c75194ec7`.
PID, creation Unix second 1793158432 and module base match the admitted session;
creation precision is one second, compared with exact READY FILETIME truncated
to seconds. Module version 1.16.244.0, PE timestamp 1780354072 and image size
144,449,536 bytes match the pinned installed EXE.

The runtime module base is `0x7ff615df0000`. Fault VA/RIP is
`0x7ff6167729b0`, module RVA `0x9829b0`; exception is `0x80000003`,
EFLAGS `0x200`, TF clear. Bytes at the site begin `0xcc`. These are dump
observations, not a reconstruction of the missing debugger delivery.

Application Error record 141493 at 03:43:36.772166 UTC binds PID `0x2d50`
(11600), exact creation FILETIME, executable, exception and fault offset.
WER record 141494 and its readable existing Report.wer share report identity
`12bd822a-3738-4a7f-88d4-8dab522a2920` and the same fault signature. The
bounded Windows query also returned three older records; the forensic method
excludes them by explicit UTC comparison and qualifies the current application
record by PID and exact creation identity. No older event is relabelled current.

## What the complete control trail establishes

The 142,604 control rows are contiguous. All 1,330 received debug events have
paired continuation intent/result records. Every recorded call succeeds with
error zero and disposition `DBG_CONTINUE` (`0x00010002`). No fatal-controller
diagnostic, collector failure or requested STOP is present. This excludes a
recorded unhandled disposition/API rejection as the immediate explanation; it
does not establish the state of an event never received by this observer.

Faulting TID 3864 is the CREATE-process thread, registered lifetime 1 and present
in the 89-thread barrier. Its last recorded ordinary event is LOAD_DLL at debug
sequence 246. **There is no exception debug event from this thread anywhere in
the journal**, before or during the fatal incident. The dump supplies its fault
context; the debugger journal supplies no corresponding first/second-chance,
trap classification, context readback or continuation for that incident.

The last observed Grid-clear trap instead belongs to TID 3640/lifetime 9,
debug sequence 579. Control rows 47463–47749 include the owned trap at site+1,
original-byte restoration (`0x48`), RIP rewind/TF ownership and successful
continuation; sequence 580 supplies the single step at site+5, `0xcc` rearm,
TF-clear readback, peer release and successful continuation. The last recorded
exception, sequence 1242, is a SourceInit single step on TID 3640. Thread exits
and unexpected process exit follow. Do not substitute that worker's successful
sequence for the unobserved faulting main-thread transition.

Ownership replay accounts for 160 image-file adoptions, one process duplicate,
93 thread duplicates and 254 successful registered closes. Borrowed event
process/thread handles remain unclosed by the observer. The known D5L defect
is repaired; fixing it was insufficient to establish retail reliability.

One peer-suspend error is preserved: control row 107830, debug sequence 999,
reports Windows error 5 for TID 23892/lifetime 2. The observer defers the SourceInit
trap without restoring an instruction or acknowledging a sample; sequence 1000
records that peer's EXIT and sequence 1001 retraps SourceInit. This handled
transition is not proof that all APIs succeeded, nor established cause of the
later fault on a different thread.

## Alternatives and next discriminating work

| Explanation | Current evidence and falsifiable requirement |
|---|---|
| Original borrowed-handle failure | Not reproduced by ownership replay. No equivalent invalid close is observed; causal history of D5L remains separate. |
| Recorded wrong continuation or failed last Grid-clear rearm | Contradicted within the recorded trail by successful owned continuations and rearm/readbacks. No conclusion about the missing main-thread delivery follows. |
| Thread-specific exception-delivery exclusion | Compatible with a breakpoint fault absent from the debugger's received-event stream; state and timing are NOT observed. This is a hypothesis, not a diagnosed hidden-thread flag. |
| Another routing/termination mechanism or unobserved control failure | Remains possible. Dump/WER and received-event logs do not reconstruct every target/OS routing action. |

A useful next bounded **offline disposable** test would contrast an ordinary
main-thread breakpoint with a deliberately excluded thread, recording identical
armed bytes, actual debugger delivery, thread identity, target outcome and dump
state. Reproducing this signature would demonstrate sufficiency in the fixture,
not occurrence in Starfield. Its precise intervention/oracle needs a separately
authorized experiment. No live retry or new instrumentation follows from this
post-mortem, and removing Grid-clear without an equivalent proven lifetime fence
would weaken the scientific instrument.

The existing dump lacks a qualified observation of the proposed delivery-exclusion
state. A plausible explanation is not promoted to root cause. The prior and current
fault signatures coincide, but the new control evidence cannot retrospectively
prove the old initiating mechanism. All D5L failure records remain unchanged.

## Reproduction and remaining boundary

The retained `review_capture.py` independently binds every journal barrier/sample
to its SRO1 and ACK before reduction. The new standalone
`research/resource-retained-population/postmortem_d5m.py` reads completed journals,
qualified dump/Windows/protection evidence and writes the forensic summary.
It performs no target operations and was authored after postflight; it is not an
input to the native observer. The [ledger](d5m-phase-b-sources.csv) pins the final
method and output plus the exact admission, protection and archive records.

The first local summary used the control action name for a deferred trap that is
actually journalled as an event; its zero count was a postprocessing error. The
corrected final summary counts the one event and explicitly preserves the suspend
error. Original journals and the superseded summary are retained. A premature
attempt to read a still-running reduction's absent output likewise produced no
scientific result; the completed review output is the one cited.

Evidence integrity and protection pass. Scientific acquisition is incomplete,
target survival failed, and retail instrumentation requires REWORK. Final
independent review assesses this account and its exact primary evidence; it does
not certify another run, integration, B6 or publication.
