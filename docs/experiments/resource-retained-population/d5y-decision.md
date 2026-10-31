# D5Y remedy decision before native changes

2026-10-31, Australia/Sydney. [Contract](../../implementation-briefs/CODEX_BRIEF_SOR_RG2_D5Y_B1_capture_forensics_recorder_performance.md),
[analysis](d5y-report.md), [active ledger](d5y-investigation-ledger.md).
Decision: retain the exact reviewed observer, recorder, scientific reader and
B1 reporter. This is a completed offline remedy selection, not retail readiness.

The 1,024-cell queue reached capacity. Recorded flush latency is long enough
to make service availability a plausible contributor, and admitted traffic is
bursty. There is no measured placement of individual flush calls, worker wakes,
guard work or dropped attempts. Neither a unique bottleneck nor a defective
implementation follows. All admitted records finalized; ordinary loss advanced
epochs and did not stop acquisition. The intended conservative behavior held.

| Alternative | Evidence and decision |
|---|---|
| No code change; improve interpretation and targeting | SELECTED. Report conditional spatial bypass evidence alongside missing direct identity. Do not repeat the visit on the assumption that nineteen other paths imply target coverage. |
| Increase queue/retries or reduce polling delay | NOT JUSTIFIED. The existing trace does not establish a sufficient queue size, dominant service interval or benefit under uncensored arrivals. Serial replay changes materially with drain phase. More retries cannot cure capacity loss and contention exhaustion was zero. |
| Drain/batch/flush repair | NO PROVEN DEFECT. The actual worker snapshots admission, batches up to 64 frames and flushes raw before its cumulative ACK. Continuous arrivals cannot starve that snapshot's closeout. Altering durability or scheduling requires separate binary identity and qualification. |
| Bounded diagnostic enhancement | JUSTIFIED FUTURE DESIGN, not implemented. Retained evidence already suffices for this task's scoped uncertainty/no-change answer. Worker operation timing would discriminate future causes, but cannot recover B1 history; adding an otherwise unnecessary candidate would incur qualification without resolving that history. |
| Target-only filtering | REJECTED. Before a source copy, P20 is only conditionally identified. Filtering other accesses, unknown selections, resets, lifetime fences or losses can manufacture cold-first attribution. No independent global-coverage channel has been qualified. |
| Copy source bytes directly at visited/selection | REJECTED AS AN UNQUALIFIED SHORTCUT. These boundaries do not hold the lookup's native exclusive protection. Readable bytes alone would not establish coherent source identity/lifetime. A new safe identity boundary requires its own proof and native controls. |

The smallest useful **writer diagnostic proposal** records QPC start/end and
operation kind for raw write, raw flush, ACK write/flush, guards/disk checks,
snapshot begin/end and wake/STOP handling, with snapshot admission/dequeue
bounds and cumulative cause-specific losses before/after each operation.
Keep it on the worker, in a bounded fixed-state summary or separately framed
diagnostic channel; do not recursively enqueue it through a full scientific
queue. Specify overflow/failure semantics and exclude its incomplete tail from
scientific completeness. Per-operation timing would localize delays to I/O-call
intervals versus between-call, guard and sleep intervals. Device latency and
in-call scheduling would remain inseparable without another independent witness;
the proposal would not recover dropped types or isolated producer hot-path cost.

For target attribution, independently qualify a lifetime-protected source/frame
identity witness for bypass-only paths. Preserve every global invalidation,
unknown prior access and loss epoch. A source identity read cannot borrow the
historical descriptor or become safe simply because its payload is small.
No revised native candidate or retail package is produced here. Any implemented
diagnostic must receive new source/binary/schema identities where appropriate,
actual compiled native adverse controls and separate retail authorization.

All fourteen hook identities, schema `sor-d5x/2`, DLL/package pins and original
39-case B1 audit behavior remain unchanged. Conditional native repair/regression
requirements therefore do not apply to a new candidate in this assignment.
The new offline forensic and visualization scripts receive independent arithmetic,
primary-evidence, determinism and editorial checks. Historical failed captures
and original verdicts remain intact; B1 retry, B2 and publication remain gated.
