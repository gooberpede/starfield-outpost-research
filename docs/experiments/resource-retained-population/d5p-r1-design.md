# D5P-R1 evidence and continuity contract

2026-10-29, Australia/Sydney. [Pre-repair diagnosis](d5p-r1-diagnosis.md) and
[frozen brief](../../implementation-briefs/CODEX_BRIEF_SOR_RG2_D5P_R1_observer_resilience_context_repair.md).
This is an offline research observer contract, not retail approval.

## Context diagnostics

The first failed predicate receives a stable reason. Zero means all selected
context predicates passed. The suffix records actual read address, requested
and returned byte counts, immediate Win32 error, and successfully reached
operands. A failed or unreached operand is unavailable; its initialized zero is
never an observed null. Later fields are interpreted only along the reached
predicate path. Diagnostic runtime addresses qualify inspection provenance,
not persistent or scientific source identity.

| Reason | Predicate or failed read |
|---|---|
| 1–3 | Singleton, source-pointer slot, original-query-pointer slot read. |
| 4–6 | Current ProcGen read, ProcGen mismatch, mode read. |
| 7–10 | Source bytes, original query words, owner, effective descriptor read. |
| 11–12 | ProcGen type read or mismatch. |
| 13–16 | Source-index read, ordinary Grid pointer read, Grid type read or mismatch. |
| 17–20 | Grid count read, capacity read, count exceeds capacity, data-pointer read. |
| 21–23 | Member slot read, source not a member, overlapping lifetime activity. |
| 24 | Structurally admissible Grid exceeds the 256-member observer inspection bound. |
| 25–26 | Retained invocation Grid read or disagreement with current manager Grid. |

The provider retains its Grid at W+`0x100`; the current manager's Grid alone
cannot establish invocation membership. R1 rejects disagreement rather than
guessing which allocation supplies a valid lifetime. Independent review found
this missing distinction during repair; it is not a verified historical cause.
The vector bound is an explicit engineering coverage limit, not a native type
invariant. The inspected ordinary context is not an exhaustive alternate-type
contract. Unsupported contexts remain diagnostic observations.

## Ordinary loss and scientific joins

The 1,024-cell MPSC queue remains bounded. Producers try at most 32 reservation
iterations. Capacity failure and bounded retry exhaustion count separately;
neither disables wrappers or stops the writer. A loss advances the same global
observer epoch used by conservative lifetime invalidation. In-flight context
epochs become stale. Later complete invocations can recover in a new epoch.
Every retained ownership/reuse join requires equal epochs and no active hazard.
No pointer, geographic key or source inequality exempts a chain from loss.

A complete source-demand/query/mask/copy/ownership/reuse chain entirely after
a quiescent loss boundary may qualify within the existing eleven-hook scope.
That is a new witnessed construction, not a continuity certificate bridging
the gap, a first-ever construction or proof of whole-session completeness.
The recorder never reconstructs missing decisive events. A failed append may
coexist with a separately witnessed good region; contradictory and orphan
payloads remain available. Session health, record authentication, causal
qualification and target survival remain separate outcomes.

Admission sequences count successful reservations only. They do not count
dropped events. The cause counters provide known ordinary losses while enabled;
fatal deactivation or a missing terminal leaves later unobserved totals UNKNOWN.
First/last sampled admission watermarks are concurrent diagnostic samples, not
precise temporal bounds. The epoch comparison supplies the conservative join
rule. Queue high-water is a measured lower bound because its update is bounded.
Counter overflow or exhaustion of the signed ticket representation is a fatal
representation failure, not a scientific event quota.

## Evidence version and durability

The plugin version is 0.2.0; identities use `sor-d5p/2`. The original 1,416-byte
schema remains readable as historical `sor-d5p/1`. Schema 2 appends fourteen
little-endian u64 diagnostics at payload offset 1,416, for 1,528 bytes total.
Original meaningful geometry offsets remain unchanged. Frame sequence headers
contain the low 32 bits; the payload retains the full sequence. Bytes, admitted,
written, raw-flushed and independently acknowledged records are distinct.

The worker writes batches of at most 64 framed records, bounded by an enqueue
snapshot. It flushes raw bytes before writing and flushing the identity-bound
acknowledgment. Continuous producers cannot extend a drain indefinitely.
The 40,000,000,000-byte caller-available floor remains mandatory on C: and D:,
including the next snapshot's write reserve. Output and disk failures are fatal
transport failures; hook guard failure requires safe resident deactivation.
Ordinary admission loss remains recoverable.

The runtime writes one append-only file; no filesystem reliability evidence
requires rotation. The reader also accepts a lossless offline segmented
derivative, with exact offsets, predecessor SHA-256, per-part SHA-256 and the
original identity/flush bindings. It does not invent continuity between separate
sessions. A torn tail preserves an earlier authenticated acknowledged prefix.
Unacknowledged bytes remain provisional observations and cannot establish a
qualified chain. Damaged bytes never establish source absence.

The development build01 used a transitional 1,520-byte schema-2 payload before
the retained-Grid operand was added. It is not a released format or candidate.
Its original qualification receipt remains historical; the final reader rejects
that transitional size rather than silently interpreting it as the final schema.
