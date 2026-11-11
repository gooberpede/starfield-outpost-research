# P3 recorder, controller and workload qualification

2026-11-01, Australia/Sydney. Offline results; final independent disposition
remains separate. D5AB INCOMPLETE / REWORK; D5R OPEN; P4/B2 NOT AUTHORIZED.
[Contract](../../implementation-briefs/README.md#archive-lookup) (`implementation-briefs.zip :: docs/implementation-briefs/CODEX_BRIEF_SOR_RG2_D5AB_P3_native_integration_qualification.md`),
[ledger](d5ab-p3-investigation-ledger.md), [provenance](d5ab-p3-provenance.md).

## Complete-producer envelopes

The actual final DLL emits 21,061 events in the representative workload and
12,018 in the burst workload without loss at 32,768 cells. These are declared
finite host envelopes, not a universal retail rate. The representative host
uses four producers with 500 calls each, actual callbacks and a deliberately
paused raw flush. It includes all seventeen categories, five births/publications,
2,001 reserve attempts and 1,025 executed stores. Four host arrays each permit
256 stores before reserve failure; the baseline supplies the remaining store.
A sampled mask or a reserve attempt does not imply successful geometry/store.
The burst adds 12,000 READY offers plus trigger/baseline lifecycle evidence.

Independent host actions count attempted categories without interpreting the
observer stream. The capacity driver independently expects those totals and
requires attempted = admitted + losses; it verifies per-category admission bounds,
raw CRC/sequence, ACK-prefix bytes and stable terminal accounting. The smaller
queues are counterexamples to universal losslessness, not failed target science.

| Cells | Scenario | Independent offers | Admitted | Capacity losses | Retry losses | Sampled queue high-water lower bound |
|---:|---|---:|---:|---:|---:|---:|
| 1,024 | Representative | 21,061 | 10,880 | 10,181 | 0 | 1,024 |
| 1,024 | Burst | 12,018 | 6,972 | 5,046 | 0 | 1,024 |
| 8,192 | Representative | 21,061 | 18,707 | 2,354 | 0 | 8,192 |
| 8,192 | Burst | 12,018 | 12,018 | 0 | 0 | 5,716 |
| 32,768 | Representative | 21,061 | 21,061 | 0 | 0 | 11,292 |
| 32,768 | Burst | 12,018 | 12,018 | 0 | 0 | 6,160 |

The normal 17-record scenario also passes at all three capacities. All nine
scenario/capacity combinations authenticate their complete admitted byte prefix.
Lossy sessions cannot promote whole-session firstness. A complete admitted prefix
does not mean native-event capture completeness. The 32,768-cell candidate has
measured headroom in these envelopes; no optimum or general lossless capacity
is proved. Final receipts are under `p3-capacity-final02`, including exact source,
binary and packaged-consumer identities.

## Independent queue controls

The production queue itself is unchanged. Queue01 compiles it at each capacity
and runs three repeats, comparing every offered ID, successful admission and
per-producer order with consumption. Each paced 16,000-offer workload loses zero.
The held 32,000-offer workload begins consumption after the stall and producer
joins; it must not be described as 32,000 events produced in exactly three seconds.

| Cells | Queue allocation bytes | Held-burst losses in three repeats | Hot contention losses | Unpaced overload losses | Paced retained records/s range |
|---:|---:|---|---|---|---|
| 1,024 | 327,680 | 30,976 / 30,976 / 30,976 | 77 / 31 / 56 | 51,831 / 53,818 / 61,423 | 1,293–1,305 |
| 8,192 | 2,621,440 | 23,808 / 23,808 / 23,808 | 52 / 44 / 49 | 51,273 / 38,799 / 53,232 | 1,306–1,313 |
| 32,768 | 10,485,760 | 0 / 0 / 0 | 44 / 87 / 111 | 14,353 / 22,010 / 12,704 | 1,294–1,305 |

Pacing is four offers followed by a Windows yield per producer; actual elapsed
time is measured rather than assuming a one-millisecond yield. Hot contention
can lose records at every capacity because reservation has a 32-retry bound.
Independent controls also cover delayed reserved heads, wrap, recursion,
uncertain loss bounds, overflow refusal and STOP with a reserved producer.
Neither these finite trials nor B1's untimed cumulative losses identify a
universal service limit or timestamps for the historical 9,957 lost events.

## Worker phases and evidence conservation

The final 32,768-cell representative event span is 8.755 seconds and its retained
rate about 2,406 records/s; the burst span is 8.491 seconds and about 1,415 records/s.
These include deliberate pauses, OS scheduling, file I/O and competing local
tests. They are retained rates over observed QPC spans, not offered peak rates.

| Worker measurement | Representative max milliseconds | Burst max milliseconds |
|---|---:|---:|
| Wake interval | 3,197.655 | 3,241.420 |
| Drain scope | 3,172.429 | 3,165.486 |
| Write call | 43.809 | 116.712 |
| Raw-flush scope | 3,064.279 | 3,081.626 |
| ACK flush | 332.249 | 132.379 |
| Guard check | 0.202 | 0.169 |
| Disk guard | 25.806 | 40.985 |
| Shutdown scope | 0.133 | 0.110 |

The raw-flush scope includes an injected three-second pause. Drain contains
nested disk/write/flush work and wake is an interval; these phase totals overlap
and must not be added as independent elapsed costs. Receipts retain every count,
total and maximum in QPC ticks, with the actual frequency. Queue high-water is
a sampled lower bound, not an exact global maximum. Timing alone does not show
what caused B1's loss.

The independent final audit authenticates 216,979 frames and 413 ACK prefixes
across 88 recorded native sessions. The other two build cases are guard refusal
and metadata-only unwind probes. Stable terminal cause/generation totals
reconcile; failed I/O/flush/worker/crash cases preserve their available prefixes
without claiming successful closeout. Raw bytes precede raw flush, then ACK
write/flush; acknowledged count never exceeds the independently authenticated
written prefix in these cases.

One deliberate overloaded STOP case exposes a real sampled counter inconsistency
in ACK line three. Loss-generation and cause fields are separate atomic loads,
not an atomic tuple. Its 65,553 admitted frames and four byte-authenticated ACK
prefixes survive; final terminal drops total 21,827,946. The reader preserves all
durable records while reporting `LOSS_TELEMETRY_INCOMPLETE_OR_CONTRADICTORY` and
refusing complete-session and reset-scoped scientific qualification. This is
metadata inconsistency, not observed byte/CRC corruption. The independent audit
and final consumer counterexamples separately verify those dimensions.

A related synthetic cause-sum inconsistency originally truncated reported
durability before a later valid ACK. The preserved Baseline11 fails that control.
The corrected schema-4 path separates byte authentication from sampled metadata,
retains the later prefix and keeps the scientific refusal. Old schema-3 behavior
and original receipts remain unchanged. No coherent-snapshot guarantee is claimed.

## Controller and operational safeguards

The unchanged P2 controller is tested against the actual final recorder worker,
with fresh READY/challenge, retained process/thread identity, exclusive ownership,
delay, disconnect/reconnect and controller death, actual worker early exit,
I/O/raw-flush/ACK-flush/guard/disk faults, missing terminal, stale/foreign STOP,
loss accounting, damaged evidence and owned operator STOP. The 26-case final
receipt and sharing control must pass with exact source and consumer pins.
Slow ACK remains alive/pending; controller state has no elapsed-time retirement
policy. Offline engineering admission waits are not future live-session cutoffs.
STOP leaves resident inert wrappers; hot unload/unpatch is unsupported.

Both C: and D: retain the 40,000,000,000 caller-available byte guard. Installed
identity, original site/target/relay guards, source protection and failure signals
remain separate. Sixteen disposable policy/content/backup/disk tests demonstrate
the matching guard behavior without reading or modifying an active playthrough.
This is not B2 preflight. The controller deliberately refuses retail sessions;
P4 must qualify a suitable operational adapter and bind the full protected-input,
health, STOP, postflight and archive plan before a separate B2 decision. The
[draft B2 card](run-card-d5x-b2.md) remains NOT AUTHORIZED at every live step.
