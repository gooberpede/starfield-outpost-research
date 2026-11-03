# D5AM causal sidecar contract

2026-11-03, Australia/Sydney. **OFFLINE CANDIDATE / NOT AUTHORIZED.**
This versioned sidecar extends observation; it does not replace the unchanged
schema-4 core, Raw2 geometry or lifetime channels. Exact final producer/reader
source locks and independent qualification control admission. Successful parsing
alone does not establish native coverage, source attribution or readiness.

## Wire representation and identity

`causal.bin` starts with a 96-byte little-endian header: four unsigned 64-bit
words (magic `0x31434c4d41354453`, version 1, event size 128, reserved zero),
followed by the 64 ASCII hexadecimal characters of SHA-256 over the session's
exact `identity.json` bytes. Identity declares `sor-d5am-causal/1`, the actual
DLL/process/birth/nonce and installed causal sites. A filename is not provenance.
Final native admission additionally declares
`causal_bridge_admission_schema=sor-d5am-causal-bridge/1`. Earlier milestone
journals without that declaration retain their narrower byte-accounting scope.

Each subsequent frame has an unsigned 32-bit length (128), an unsigned 32-bit
CRC32 over the payload and the 128-byte payload. There is no frame padding.
The payload is fifteen unsigned 64-bit words followed by two signed 32-bit
original-request coordinates, in this exact order:

```text
sequence kind thread ticks lock generation invocation selection source
epoch hazards old_state new_state status site request_x request_y
```

Sequence starts at 1 and counts admitted causal records. Thread ID is decimal;
ticks use the identity's QPC frequency. Lock and source are runtime pointers;
generation is an observer owner-lifetime identity. It is distinct from source
allocation, global observer epoch, saved identity and actual reset count.
Invocation/selection join the schema-4 provider context where one exists.
Zero context identifies an unscoped lock user, not an absent participant. Site
attribution must be interpreted against the exact candidate's guarded mapping;
early candidates with reserved zero values do not supply per-site observations.

CRC detects damage and the header binds identity bytes. Neither is a signature
or independent source-authentication proof. Retained external manifests, exact
candidate hashes and original-source/site provenance remain mandatory.

## Events and native meaning

| Kind | Event | Native meaning and limitation |
| --- | --- | --- |
| 1 | Register | Publishes a watched owner-lock lifetime and immediately copies initial packed state/owner. A nonzero or unreadable baseline refuses earlier-holder completeness. The native gate can admit a probe before this record is enqueued. |
| 2 | Pending | Copies the actual old operand of writer XADD `+0x1000`. New packed state is old plus that amount modulo 32 bits. It is a count, not a ticket. |
| 3 | Acquired | Success-only ownership path, after native CAS and owner publication. Old packed state excludes readers/exclusive bits and includes a pending writer. New state adds `0x00400000`. Callback time is later than CAS. |
| 4 | Recursive | Current-owner path adds exclusive depth. It is not a new nonowner contender. |
| 5 | Reader registered | Actual reader XADD old state; new state adds one. Registration is not necessarily completed reader admission while a foreign writer holds ownership. |
| 6 | Reader release | Actual decrement old state; new state subtracts one. The typed provider, point and area sites require separate installed-site coverage. |
| 7 | Final writer release | Native final-depth decrement subtracts `0x00401000`; owner clearing and wake behavior remain separately ordered original instructions. |
| 8 | Recursive writer release | Removes one `0x00400000` depth, without claiming final release. |
| 9 | Exclusive approach | Provider's call boundary before entering the native helper. It is neither pending registration nor acquired ownership. |
| 10 | Exclusive helper return | Helper has returned; it does not timestamp the earlier successful CAS. |
| 11 | Visited observer completion | Tail of the visited observer's copied event path. Native restoration/continuation still follows; this is not an exact exclusive-attempt timestamp. |
| 12 / 13 | Owner reset begin / end | Scoped owner lifecycle boundaries. Do not equate the process-global observer epoch with a reset count or treat unrelated owning-Grid housekeeping as this event. |
| 14 | Retire | Ends a watched owner lifetime before same-address registration can create a new generation. In-flight generation/serial uncertainty remains explicit. |
| 15 | Reader admitted | Native shared helper's completed admission path. It is separate from kind 5. Same-thread exclusive recursion remains a distinct case. |

Original native sites and predicates are in the
[coverage audit](d5am-observer-coverage.md) and
[causality map](d5am-native-winner-causality.md). Those are STATIC premises;
executed native-copy controls and runtime records have separate evidence labels.

## Ordering and uncertainty

The producer uses bounded preallocated copying and queue admission. Queue
sequence is recorder reservation order, not cross-thread atomic order. Native
callback QPC is sampled after the displaced atomic where applicable. A paused
thread can publish a stamp after another thread has progressed. Do not sort the
whole history by one clock and infer a cause.

Disjoint bounds can be useful. A's Pending stamp is after A's registration;
B's Approach stamp is before B enters the helper. A Pending stamp strictly
before B Approach proves A registered before B's later acquisition opportunity.
Conversely, B's acquired callback strictly before A Approach proves B already
held ownership before A entered that helper. Overlapping brackets remain
UNKNOWN. Same-owner mutual exclusion and qualified lifetimes are necessary
premises; the core protected miss still identifies the actual constructor.

Probes can change progress in precisely these intervals. The offline controlled
pending-callback hold demonstrates observer-induced overtaking. A measured
instrumented order is not automatically the uninstrumented order or a normal
retail distribution.

Registry generations and serials must be captured coherently around the native
operation. Status bit `0x08` records uncertain retirement/re-registration rather
than silently assigning an old in-flight event to a new owner. Initial-state,
read and unsupported-event status bits remain refusals. Unknown baseline,
multiple owners, relevant lifecycle overlap, missed context, source/task ABA and
loss cannot be repaired by equal pointers or a plausible final map.

The final bridge snapshots registry identity before the displaced operation and
checks the watched receiver afterward. This detects a user that crosses initial
watch publication; a zero baseline alone cannot exclude a user paused after an
earlier unmatched filter. The bridge saves state and admits native activity on
unrelated locks too, adding observable work even without a C++ callback. Actual
crossing-user, flags/register and unwind controls must qualify these final bytes.
A crossing operation may retain its original zero generation only with status
`0x8` on the affected native-operation record. That authentic uncertain operand
is preserved, never assigned a later owner's generation. Other zero-generation
records and unknown status bits are refused. Registry uncertainty can coexist
with intact byte and native-producer accounting.

## Durable accounting and independent reader

Terminal and core ACK receipts carry causal written/enqueued/active counts,
drops, reentrancy, failed state, unknown baseline, multiple-owner and registry-
uncertainty counts. The terminal must bind every identity field and agree with
the complete sidecar count. Counters and failure histories cannot regress across
ACKs or disappear in the terminal. Exact final worker/flush tests must establish
that declared counts correspond to flushed bytes. A clean terminal alone is
insufficient; interrupted output remains incomplete evidence.

For the declared native-admission feature, every ACK and terminal must include
unsigned `causal_bridge_active` and `causal_native_counter_faults`. The terminal
bridge count must be zero. The fault word has sticky mask `0x1` for overflow and
mask `0x2` for bounded admission-counter contention; bits cannot disappear across ACKs
or at terminal. Any such fault must also set `causal_failed`. STOP must wait for
native admission beginning before the displaced operation, including the gap
before C++ producer admission. The reader separately reports
`native_bridge_accounting_complete`; older byte-valid journals cannot supply
this stronger proof merely by retaining wire version 1.

The [independent reader](../../../runtime/construction-winner/d5am_read_causal.py)
validates wire fields, CRC/sequence, full identity and typed accounting. It
consumes each pending witness once and preserves foreign/unscoped users.
Its conditional interval witnesses distinguish disjoint bounds from overlap;
full causal completeness remains INCONCLUSIVE until all core/source/task,
coverage and native-method prerequisites qualify. It performs no raw repair,
late pointer traversal, live operation or automatic STOP.

[Parser controls](../../../research/resource-retained-population/d5am_causal_controls.py)
use explicitly synthetic wire and interval schedules, with corrupt/missing/
contradictory alternatives and optimization refusals. They do not execute the
producer or prove its bridge semantics. Actual native-helper recordings must
be independently replayed in addition to those parser tests.
