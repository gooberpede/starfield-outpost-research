# D5E event and continuous-coverage specification

[Native contract](native.md), [qualification](qualification.md),
[machine envelope](../../../research/resource-source-decisions/event.schema.json).

## Acquisition and durable order

The existing D5B Windows debugger utilities are reused by a generated translation
unit. The new tail keeps four execution-breakpoint addresses fixed on every
thread. At process creation it verifies the image path/hash and 16 instruction
bytes at each mapped-image RVA. New threads are armed before their debug event
is continued. Startup reconciles all known threads with DR readback, emits
ARM_BARRIER and waits for a durable ARM_ACK before releasing the fixture gate.
The future native transport publishes READY before the operator is allowed to
load Save52. No consumer phase, slot rotation or automatic mode switch exists.

Each owned trap verifies RIP, DR0–DR3, DR6 ownership, DR7 enables and instruction
bytes. Only owned DR state and RF are changed to resume; general registers,
floating-point state and material flag bits are read back for preservation.
This affects execution through attachment, all-stop pauses and breakpoint/RF
control. It is not non-invasive. No target bytes or gameplay operands are patched.

SESSION binds PID, image hash, module base, schema and synthetic/native domain.
SAMPLE binds monotonic capture number, TID/thread lifetime, site, runtime RIP/RSP,
UTC FILETIME ticks, full raw CONTEXT and exact copied operands. Native records
retain raw source/manager/query bytes with addresses/read status and repeat
copies; fixture records retain a `0x78`-byte little-endian packet. The packet's
manager/source epochs, invocation and parent are **fixture-only oracle fields**,
never decoded as native engine members. Thread lifetime is an observer token.

The transport journals events, flushes with fsync, creates SRO1 frames with body
SHA-256, reads them back and independently decodes them before sending the
numbered ACK. Its queue holds at most 32 rows; the controller blocks for each
sample ACK, bounding outstanding sample memory. Native map reads cap capacity at
4096, with inherited 65,536-byte per-read and 1,048,576-byte per-stop bounds.
Oversized reads fail explicitly; they cannot silently become complete evidence.
No arbitrary healthy-session duration/event-volume limit is added.

ARM_BARRIER, THREAD_ARMED, GAP, STOP_COMMITTED, TERMINAL_EVENT, FAILURE_CLEANUP and
EXIT remain in the durable journal. The schema file validates only the outer
envelope; reducers enforce session, identity, order and scientific predicates.
It is not claimed as a complete JSON validator of every raw native member.

## Coverage and rejection

Coverage opens only at the all-thread readback barrier. A newly created thread
is stopped and armed before execution. Unrelated calls do not disarm any site.
Failed instruction/context/slot checks or unowned exceptions emit GAP. A capture
sequence discontinuity closes reduction coverage until a fresh arm barrier.
STOP commits terminal intent before disposal; queued terminal events are drained
without rearming or sampling. Native ABI/lifecycle coverage differs from probe
coverage: continuous probes do not establish complete lifecycle observation.

The native reducer preserves session identity and coverage intervals, refuses
concatenated or unpinned sessions, and records capture/site/frame plus a named
rejection reason. Failed source/manager identity reads reject association.
A valid branch with an incomplete original query remains C with the exact missing
query named. Mask/query-only snapshots are D until a provider decision exists;
they are retained as unjoined operands. Lost coverage never means a map hit.

## Scientific tiers and lifetime handling

| Tier | Required evidence and scope |
|---|---|
| A | Fixture-qualified miss, original query, sampled mask, actual target-memory construction/insertion and completion, with explicit oracle lifetime. Native A is blocked by unobserved completion/lifetime/provenance fields. |
| B | Fixture-qualified explicit map hit or visited bypass, labelled distinctly with oracle manager/source lifetimes. A bypass need not have complete population; a hit need not have an observed historical constructor. |
| C | Qualified decision with named missing necessary operand. Native branch records retain unknown lifetime, associated definition-file identity and completed construction event. Fixture partial/stale/failed insertion cases remain C. |
| D | No qualified provider decision, including consumer-only or unjoined mask/query evidence. No resolution of source construction history. |

Fixture decisions preserve encounter order using first captured decision order,
not completion order. Concurrent and nested contexts use TID, thread lifetime
and explicit fixture invocation/parent; contradictory masks and replacement
epochs remain separate. Native frames are not promoted to equivalent epochs.
Every output states first-observed separately from first-ever; first-ever remains
UNKNOWN even across a fresh-process/pre-load barrier. Raw packets and snapshots
remain available for a competing reducer. No reduction relabels D5B geometry,
predicts an unknown query, or closes the seven indeterminate associations.
