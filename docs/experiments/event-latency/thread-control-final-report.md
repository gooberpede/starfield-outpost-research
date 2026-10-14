# B — COMPLETE / ABANDON EXTERNAL DEBUGGER

2026-10-11 Australia/Sydney; SOR-EXP-0028 / SOR-EV-0036 / SOR-D-0048.
[Final authorized brief](../../implementation-briefs/CODEX_BRIEF_SOR_FINAL_THREAD_CONTROL_RECOVERY.md).
Authored analysis REVIEW-REQUIRED; raw/private receipts LOCAL-ONLY.

**ABANDON EXTERNAL DEBUGGER PATH.** The final bounded engineering attempt is
complete. No new acquisition candidate is issued, no exploratory Starfield
attachment is justified, and no further debugger implementation brief is proposed.
This closes this approach in this project; it does not establish that a different
Windows debugger could never implement correct replay/retirement.

| Question | Best-supported answer |
|---|---|
| R1: why can thread suspension fail? | Actual runs capture SuspendThread returning DWORD(-1)/error 5 despite measured suspension rights, while both same-handle and independently opened query handles return STILL_ACTIVE and a zero-time wait times out. Current successful-suspend-or-proven-exit handling cannot resolve this state. Separately, a real exited thread with only the documented minimum debug-handle rights reproduces suspension error 5 followed by query error 5. |
| R2: why can an owned trap appear foreign? | Multiple threads can already have trapped at an owned INT3 before its first event is serviced. The adapter restores that site's byte for one replay, marks it uninstalled, then rejects another queued trap at that same site as foreign. Actual exception addresses/RIP/TID/TF and site state demonstrate this mechanism. |
| Does a narrow repair solve both? | No. Explicit query-capable handles plus rewinding queued owned traps improve ordinary acquisition but still encounter R1. Stopping at queued replay repeatedly delivers outstanding owned traps to the application after clean-looking restoration/detach. |
| Confidence and scope | PROVEN for these instrumented disposable observations and source branches; original R1's exact handle/native state and original R2 address remain missing. New traces explain reproducible mechanisms, not retroactively captured historical details. |
| Safety decision | No fully qualified retirement protocol. Original bytes/debugger absence and fixture survival alone do not prove semantic restoration. Outcome A is blocked and is not offered. |

## Work performed and bounds

The repository requirements, active brief, original incident and startup/latency
reports/source/raw receipts were read. The unchanged 0.1.4 source SHA-256 is
`6606a9b77991d3f1333eda33b213cf5449c42fb4b1b67f15dae0da7b25578497`.
Project-owned baseline code was transformed only into new ignored diagnostic
sources/executables. The approved adapter, startup repair, writer, collector,
fixture, decoder, operational checker and shared helpers remain unchanged.
[Tool contract and original diagnostic source](../../../debugger/event-thread-control/README.md).

The experiment question was whether actual handle/lifetime and queued-trap state
could support a narrow, independently safe repair. Inputs were pinned project
fixtures/adapter source, installed MSVC/SDK/Python and protected inputs used only
for integrity hashing. Outputs were new ignored build/command/API/context/WAL/
postflight receipts. Permitted interventions were confined to owned disposable
processes, including native patch/TF/suspension changes and declared stop/failure
injections. Risks were altered timing, disposable crash/stall and partial evidence.
Orchestration timeouts and cooperative-stop/owned-handle cleanup bounded them.
No event quota or short scientific cap was added to acquisition.

Six trace workflows, five native API experiments and 26 additional adversarial/
repair workflows were completed: **32 target workflows total**, plus the separate
five API cases. All meaningful failures and pilots are retained. The final trial
ran a predetermined eight-case schedule, including three stop-at-queue cases;
passing repetitions do not erase failures. Independent read-only postflight ran
after failed adapter exits too. All surviving final-trial targets passed original
code/debugger-absence checks. The intentionally exiting target has an explicit
equivalence limit below.

## R1 — Precise API evidence and unresolved native state

Microsoft documents debug-event thread handles as granting get/set-context and
suspend/resume rights; query rights are a separate requirement. SuspendThread
returns the previous count or DWORD(-1), and GetExitCodeThread needs query access.
These contracts informed the original experiments; no example implementation was
copied. [CREATE_THREAD_DEBUG_INFO](https://learn.microsoft.com/en-us/windows/win32/api/minwinbase/ns-minwinbase-create_thread_debug_info),
[SuspendThread](https://learn.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-suspendthread),
[GetExitCodeThread](https://learn.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-getexitcodethread),
[NtQueryObject](https://learn.microsoft.com/en-us/windows/win32/api/winternl/nf-winternl-ntqueryobject);
SOR-S-0139. Installed SDK declarations are used, not vendored.

The five-case `api-probe-01/results.jsonl` directly measures:

| Handle/state | Suspend result/error | Exit query | Ownership check |
|---|---|---|---|
| Running, full rights |0 /0 | STILL_ACTIVE | Resume returns 1 |
| Running, minimum context/suspend rights |0 /0 | Fails/error 5 | Resume returns 1 |
| Running, pre-existing suspend increment |1 /0 | STILL_ACTIVE | Probe resume returns 2; outer resume returns 1 |
| Exited, full rights | DWORD(-1) /5 | Exit 23 succeeds | No resume issued |
| Exited, minimum context/suspend rights | DWORD(-1) /5 | Fails/error 5 | No resume issued |

The reduced handle's measured mask is `0x101A`; the full handle is `0x1FFFFF`.
This isolates a concrete liveness-query assumption and reproduces the original
error string's API combination. It **does not prove** that the historical R1
handle had that mask or that missing query rights were its cause.

The attempted repair opens explicit handles requesting get/set-context,
suspend/resume, query-limited and synchronization rights. Actual measured mask is
`0x10181A`. The trace captures each API result/error immediately, before secondary
calls, and queries granted access using ObjectBasicInformation. It records an
independent OpenThread/query/wait, plus owned increment count.

Three actual run failures remain:

| Run / trace lines | TID | Suspend | Same and independent query | Wait / owned increments |
|---|---|---|---|---|
| `repair-trial-01/00-exit-burst/adapter.log`:1326–1327 |15300 | DWORD(-1), error 5 | Both succeed, STILL_ACTIVE | WAIT_TIMEOUT258 /0 |
| `repair-trial-01/01-queue-burst/adapter.log`:510–511 |11168 | DWORD(-1), error 5 | Both succeed, STILL_ACTIVE | WAIT_TIMEOUT258 /0 |
| `repair-trial-02/01-queue-burst/adapter.log`:2328–2329 |3896 | DWORD(-1), error 5 | Both succeed, STILL_ACTIVE | WAIT_TIMEOUT258 /0 |

All three have successful object-information queries and suspension rights in
the granted mask. The original branch fails because the exit status remains 259;
the diagnostic resets/captures errors, so the resulting message is
`suspend_live_thread:0`, with the preceding **actual suspension error 5** retained.
The zero is not a successful suspension and is not the cause. This demonstrates
why the old single GetLastError string was insufficient.

A termination-in-progress/debug-event ordering state is a plausible explanation;
it is **not proven** by these API values. STILL_ACTIVE plus a non-signaled handle
does not establish that the thread can safely be ignored. No native termination
state or later same-object exit-event correlation was captured before detach.
Insufficient rights are excluded for the new suspension failures, but not for the
historical query. The exact kernel/lifetime reason remains unresolved. Skipping
the thread, repeatedly resuming it, or treating denial as exit would weaken the
existing safety claim. None is delivered as a fix.

## R2 — Queued owned traps and retirement debt

Windows debug-event handling stops the process while an event is handled; this
does not prove that no other thread already executed a trap before that stop.
[Debugging Events](https://learn.microsoft.com/en-us/windows/win32/debug/debugging-events)
and [ContinueDebugEvent](https://learn.microsoft.com/en-us/windows/win32/api/debugapi/nf-debugapi-continuedebugevent)
explain the continuation contract (SOR-S-0139). The project fixture's 32-thread
barrier drives actual simultaneous attempts; the trace establishes resulting
ordering rather than assuming it from scheduling.

`adversarial-original-01/01-queue-burst/adapter.log`:140–142 records a first-chance
`0x80000003` at runtime VA `0x7FF79C0D7560`, RIP `0x7FF79C0D7561`, thread 4668,
while replay of center_entry at the same address is pending on thread 2580.
EFlags514 has TF clear, DR6/DR7 are zero, the site matches center_entry but
`installed=0`. The site was previously guarded/armed; it is disarmed for another
thread's owned instruction replay. The source's `installed && address` search
rejects it. The event becomes NOT_HANDLED, sets stop, and teardown clears the
pending replay, restores code, resumes owned increments, continues the event as
foreign and detaches. That is the reproduced R2 causal chain.

The original diagnostic run retired after **one captured entry/zero exits**;
the fixture nevertheless completed 32 calls and received **six unexpected breakpoint
exceptions**. Original bytes and debugger absence passed independent postflight.
Adapter exit 0 and terminal RETIRED therefore conceal a semantic intervention.
The exiting-thread burst similarly received five unexpected breakpoints. No
foreign exception is silently suppressed by the diagnostic observer.

The repair trial recognizes a previously armed, address/RIP-matched queued trap
on another suspended thread with clear TF/hardware-debug state. It rewinds that
thread, retains exactly one owned suspension increment, continues the event and
lets it re-trap after the current instruction is replayed/rearmed. No scientific
capture is fabricated for the deferred event. This is an actual local
implementation trial, not an unexecuted suggestion.

Ordinary exit-burst in the final trial captures all 8 entries/exits, zero unexpected
exceptions and unchanged semantics. Queue-burst still fails on R1 after 15 entries/
14 exits; two outstanding debugger traps reach the application during teardown.
The three synchronized stop-at-queue controls expose the independent retirement
gap: each rewinds one known queued trap then stops with other queued events still
outstanding. The application receives **6,5,5 unexpected breakpoint exceptions**.
All 32 calls complete, bad 0/exit 0, all site bytes are original and no debugger is
present. These remain failed negative assertions despite survival/output matches.

The missing mechanism is a complete per-thread ledger and safe draining/replay of
all queued trap obligations across stop/failure/thread-exit states, including TF
ownership and suspension increments. Merely restoring bytes and rewinding the
current stepping thread does not settle undelivered exceptions. Consuming every
breakpoint or globally guessing RIP corrections would risk suppressing foreign
events or modifying unrelated context. The tested narrow repairs do not qualify
that broader protocol. This is the engineering stopping point, not a claim that
such a protocol is impossible in general.

## Complete result accounting

[Machine-readable matrix](../../../.local-work/thread-control/result-matrix.json)
records all 32 workflows, exits, counts, hashes, WAL health, independent postflight,
trace locations and diagnostic latency. All final eight cases use diagnostic SHA
`a67db04d9000896a69d482c7b34f715429cb2b5ef1ccc8028a70da3cb05561c8`
and fixture SHA
`e7322d66f81e580548515dda97ae7eb656c8908333305f6049371a4618fc7f57`.
These are **failed engineering-trial hashes, not a candidate**.

| Final repair trial control | Result | Adapter/fixture exit; decisive observation |
|---|---|---|
| Exit-burst | Diagnostic expectations met |0/0; 8 entries/8 exits, exceptions 0/bad 0; independent postflight |
| Queue-burst | FAIL |1/0; R1,15 entries/14 exits, unexpected exceptions 2; independent postflight |
| Stop-queued #1 | FAIL |0/0; unexpected exceptions 6; independent postflight |
| Stop-queued #2 | FAIL |0/0; unexpected exceptions 5; independent postflight |
| Stop-queued #3 | FAIL |0/0; unexpected exceptions 5; independent postflight |
| Foreign application DebugBreak | Diagnostic expectations met |0/0; one foreign exception reaches fixture handler, 1 entry/1 exit; independent postflight |
| Stop during owned replay | Diagnostic expectations met |0/0; intentional partial capture, fixture 42/41 plus original unwind; independent postflight |
| Target exit | Expected exit observed |0/27; durable target_exit27 and TARGET_EXIT; live code/debugger postflight impossible after exit, not marked restored |

The retained six **ordinary trace workflows** complete with full/center-only/
invalid-grid 42 entries/41 exits, zero no hits, active retirement 1 entry, and genuine
writer failure adapter 1. All six independently verify bytes/detach and fixture 0.
They supplement the historical established suite; the diagnostic collector does
not run every scientific inspector assertion and is not claimed as a new 6/6
qualified release. The original 0.1.4 five-pass/one-fail qualification remains
unchanged and cannot be waived by these passes.

The unchanged exact 0.1.4 executable additionally reruns **19/19 startup controls**;
the existing health executable passes **12/12 assertions**, and **11/11 Python
WAL/inspector tests** pass again. These cannot qualify the failed thread protocol.
The first and repeated health executions pass. Post-work offline protected-input
checks pass, including both-drive storage guard. All 32 retained WALs decode;
prefix/tail/terminal differences remain visible, never fabricated or repaired.

### Pilots and adverse cases retained

- `original-trace-01`: six completed ordinary workflows; actual independent checks,
  not proof that R1/R2 disappeared.
- `adversarial-original-01`: exit/queue bursts reproduce R2. Its foreign-break
  fixture handler failed to advance a still-present INT3 and looped. Cooperative
  STOP detached the observer; the original Popen-owned fixture required recorded
  termination after the declared timeout. This is a fixture pilot defect, not
  evidence that ordinary foreign exception propagation itself is broken.
- `adversarial-query-01`: explicit query handles do not fix R2. Its revised pilot
  handler advanced over restored owned code as well as INT3; exit/queue bursts
  produced bad 7/exit 3. Do not attribute that entire register failure to the adapter
  alone. The final fixture advances only over a still-present INT3, separating
  this pilot error from the reproducible extra-exception failure.
- `repair-trial-01`: actual queued rewind implementation, two captured R1 failures;
  stop-at-queue still fails. Its earlier handler accounts for bad 6/exit 3 there.
- `minimum-rights-01`: deliberately reduced duplicate handles; grid-guard ordinary
  workload completes, but this does not disprove the separate API/lifetime failures.
- `repair-trial-02`: final corrected handler and complete 8-case schedule above;
  four negative cases, no forced cleanup. All failures retained.
- Earlier target-exit pilots attempted unavailable live queries and recorded those
  errors. The final harness instead distinguishes target-exit evidence and an
  unavailable restoration check; the earlier errors remain in the matrix.
- Initial directory-command syntax and missing checker-output argument rejected
  before substantive execution; corrected orchestration receipts are retained.

Elapsed/handler timing is diagnostic only. Ordinary full/center/guard workflows
take 62.335/37.047/36.327 seconds; final exit/queue bursts take 10.279/17.249 seconds;
stop-at-queue cases take 0.861/1.000/0.897 seconds. Trace overhead, altered fixture
workloads and concurrent experiments prevent a controlled comparison with 0.1.3.
The matrix includes measured per-event handler totals/maxima with that limitation.
No latency improvement or acceptable live pause budget is claimed.

## Preservation, disposition and alternatives

The original 0.1.2 baseline/all six passing controls, approved 0.1.3 executable/ZIP,
failed live-attempt receipts and entire prior 0.1.4 diagnostic review/build trees
are hash-checked unchanged. The new starting snapshot covers 55 pre-existing
changed/untracked text files, including the supplied final brief. Private
preservation/diff inventories identify prior work separately from this assignment.
Protected Save25/26 originals/archives, frozen scientific inputs and shared helpers
pass read-only integrity checks. No target process remains from this experiment.

No Starfield launch/open/attach/memory access, deployment, SFSE/Vortex/save/config/
analysis-database edit, global security change, staging, commit, push or external
disclosure occurred. Primary diagnostics still precede fallible timing telemetry;
the accepted startup fix and per-record durable WAL/40-billion-byte guards remain
unchanged. No permission issue blocked this scope, and none is used as a reason
to return an unfinished engineering candidate.

Decommission recommendation: retain all packages/receipts as historical research,
mark this external acquisition route closed, and do not use the old cards or any
diagnostic executable for another attachment. There is no installed external
adapter payload to remove. No archive deletion, configuration change or deployment
is needed. The original scientific/static/save findings remain valuable.

Continue research through existing offline native/save analysis and frozen
coordinate predictions. A future alternative could use separately reviewed
engine-side observation at a natural callback boundary, but this task neither
implements nor authorizes it. It is a different research direction, not another
external-debugger recovery iteration. [Final review and frozen diagnosis archive](thread-control-final-review.md).
