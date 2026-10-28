# D5L Phase B post-mortem and prevention plan

2026-10-28, Australia/Sydney. Requested by the maintainer during finalization.
[Observed run and limits](phase-b.md), [authority](phase-b-authorization.md),
[source pins](phase-b-sources.csv).

**Keep the ordinary-user launch correction, repair the confirmed handle-ownership
defect, and qualify the Grid-clear breakpoint path with better exception and
continuation evidence before another live attempt.** This is a proposed
engineering plan, not an implemented or validated prevention guarantee.

## What the preserved evidence establishes

The initial attachment was denied under the sandbox account. The unchanged
binary attached and armed successfully under the ordinary user after a fresh
authorized preflight. Treat caller/target account identity as a pre-admission
requirement in the next operational revision; no blanket administrator or
security-setting change is justified by this evidence.

The later premature exit is a separate failure. WER reports `0x80000003` at the
exact armed Grid-clear site, module-relative `0x9829b0`, for the correct process
lifetime. Attribution is **STRONG observer-associated breakpoint failure**.
The exact exception-delivery, rearm or continuation mechanism remains UNKNOWN.
The journal has no faulting exception context or per-event continuation trail.
Its final sample is source initialization, not Grid-clear. Preserved receipt
integrity and passing postflight do not establish execution safety.

Independent static review also found a concrete defect in
[controller-tail.inc](../../../research/resource-retained-population/controller-tail.inc):
the controller stores thread handles received in CREATE debug events directly,
then manually closes them on thread exit, in dead-peer cleanup and after process
exit continuation. Windows owns these event handles and closes them when exit
events are continued. The controller needs explicitly duplicated owned handles
where it requires independent ownership, with one close owner for each handle.
[Microsoft Debugging Events](https://learn.microsoft.com/en-us/windows/win32/debug/debugging-events)
and [ContinueDebugEvent](https://learn.microsoft.com/en-us/windows/win32/api/debugapi/nf-debugapi-continuedebugevent)
document this lifecycle.

**That defect is not the demonstrated initiating cause.** Two thread exits occur
after the arming barrier and before sample 1: journal lines 95–96, TIDs 21752 and
22888, lifetimes 93 and 89. There are no exits between samples 1 and 492; the
remaining 90 exits follow sample 492. There are no DEAD_PEER events. The defective
close path therefore executed before the first native sample and cannot be
dismissed as post-crash cleanup. Handle values, close results and a causal link
to the later breakpoint failure were not recorded. Repair is necessary, but is
not by itself a validated prevention guarantee.

The initial technical review incorrectly generalized a suffix of the journal
to all 92 exits. Final review found the two early counterexamples and required
REWORK. A full-row enumeration and the technical reviewer's correction supersede
that earlier ordering and causal exclusion; the original return is retained
unchanged and labelled superseded in the receipt ledger.

## Proposed prevention and diagnosis sequence

1. **Make launch identity explicit.** Record the actual collector and target
   owners before consuming admission; refuse an unintended sandbox-account
   launch. Retain actual attachment and READY as the decisive live gates.
2. **Correct handle ownership.** Distinguish operating-system-owned debug-event
   handles, independently opened handles and explicit duplicates. Stress thread
   creation/exit and handle-value reuse in disposable targets, including early
   post-attach exits before the first sample followed by continuing traffic.
   Use independent retirement checks. Do not remove existing identity or
   peer-fencing guards.
3. **Persist the missing control evidence.** Before specialized exception
   handling, record event sequence, PID/TID and lifetime, exception code/address
   and first/last chance, current site/step owner and chosen disposition. Record
   ContinueDebugEvent success/error after each call, together with handle
   identity, ownership and close results. Separately record restore,
   owned step, rearm/readback and peer suspend/resume transitions. Flush the
   exception metadata before continuation so a failure leaves diagnostic evidence.
   These are proposed additions, not fields recovered from this run.
4. **Qualify the suspected path under concurrency.** Exercise rapid Grid-clear
   and source-init traffic, same/different-site queued traps, and thread
   creation/exit during rearm in real disposable processes. Inject failed/missing
   continuation and handle errors to verify useful failure evidence and safe
   teardown. Keep scientific receipts separate from control diagnostics.
5. **Preserve the scientific contract when choosing a repair.** Grid-clear is a
   lifetime fence. Removing it, delaying arming or rotating fourteen permanent
   observations through four hardware slots would require proof of equivalent
   ancestry coverage. If safe breakpoint delivery cannot be established, assess
   a different observation mechanism for that fence under a separate reviewed
   implementation and qualification scope.
6. **Authorize a fresh live check only after review.** Bind the repaired build,
   evidence contract and disposable qualification to a new card/GO, retain the
   protected Save52 and backup checks, and arm before load again. No additional
   game run follows from this post-mortem.

This sequence follows the Windows exception model: the debugger receives
exception notifications and chooses a handled or unhandled continuation; an
unhandled last-chance exception terminates the target.
[Microsoft debugger exception handling](https://learn.microsoft.com/en-us/windows/win32/debug/debugger-exception-handling)
explains those semantics. The existing trace does not show which delivery or
disposition path preceded this specific failure, so a diagnosis must not be
selected merely because it is plausible.

An existing WER crash dump, if available and explicitly brought into a future
read-only analysis scope, could identify the faulting thread/context and narrow
that uncertainty before new instrumentation is added. No dump was opened here.
The suggestions do not authorize exception suppression, security-setting
changes, forced regeneration, save modification or removal of evidence gates.

The corrected independent technical assessment accepts the scoped attribution
and recommends REWORK before observer reuse. Both the superseded initial return
and the explicit correction are retained outside the sealed capture in
`.local-work/d5l-phase-b-final/`; the receipt ledger identifies their separate
hashes and dispositions. Final delivery review remains separate from engineering
qualification and live GO.
