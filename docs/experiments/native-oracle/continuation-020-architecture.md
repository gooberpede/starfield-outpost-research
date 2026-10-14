# Native-oracle 0.2.0 architecture and reachability ledger

2026-10-12. SOR-EXP-0031 / SOR-EV-0039. **Offline engineering and STATIC analysis;
actual game reachability NOT TESTED.** The unchanged 0.1.0 run observed zero native
records; responsive gameplay and clean retirement did not identify a blocking gate.
The new observer distinguishes absence at the two upstream instrumented boundaries
from downstream non-dispatch, conditional on qualified linked evidence.

## Native boundary and branch evidence

Pinned retail 1.16.244.0: preferred image base 0x140000000. Listed addresses below
are RVAs; runtime VA is recorded loaded base + RVA. PE file offsets are separate.
All four complete E8 instructions are freshly decoded by build.py; 11 independent
32-byte guards and exact six edit preimages are retained in build.json. Vtable
pointers are validated after relocation, not compared with unrelocated disk bytes.

| Boundary | RVA and natural contract | Primary local export / meaning |
|---|---|---|
| Q | AD93FA → AD08D0; RCX query context, RDX candidate; full EAX result | engine-oracle-04.tsv: 32–69 and engine-oracle-02.tsv: 48–164. AD93FF compares EAX, 1; query exit XOR EAX/EAX, CMP output byte, SETNZ AL. Preserve uint32 result. |
| E | AD0AB5 → B1E190; RCX collection, RDX callback object, R8B option (natural caller 0); full EAX | exp0002-selection-sites.tsv: 827–915; fresh pinned PE B1E1A4/1A8/1AB consume R8B/RDX/RCX; B1E370 MOV EAX,R14D. No consumed R9/stack arguments identified. |
| C | slots 4B916F0/4B916F8 → AD8EC0 → AD0B90; RCX object, RDX reference-slot, R8 argument | Existing architecture/source ledger; B1E33C indirect [vtable+10] dispatch. Return uint64 preserved and recorded. |
| Center | AD0C36 → F4AB80; actual returned center inside C | Retained 0.1.0 contract/schema and engine-oracle-01.tsv. |
| Grid | AD0D36 → 96F5C0; native input/output hierarchy inside C | Retained 0.1.0 contract/schema; no offline model output enters game. |

Q and E original bytes: `E8 D1 74 FF FF` at PE file offset AD89FA and
`E8 D6 D6 04 00` at AD00B5. Four CALL edits use near rel32 to leaf FF25 absolute
jump islands; two eight-byte vtable edits share the retained callback wrapper.
No stolen instruction, entry/prologue detour or forced engine invocation.
Original project-authored source-informed implementation; no clean-room claim.

Existing-reference search can satisfy a request before fallback Q. Q→E also
requires candidate/overlay data, an active landscape, hierarchy comparisons and
overlay+20 bit 0. E→C depends on collection population and reference flags/base
filters. C may return early before center/grid. Therefore a complete Q with no E
shows only no linked instrumented E, not which sampled gate caused it. A complete
E with no C shows no linked callback, not a proven empty collection or bad hook.
Raw snapshots can support narrower interpretations only when actual bytes allow.

## Natural acquisition design

Save25/26 existing 003→002→003 travel/build-open controls compare the historical
zero-event route with new diagnostics. They are not Q-positive controls.
The separately approved conditional N1 scenario selects one genuinely new,
ordinary landable Kreet point from a protected Save26 descendant. STATIC chain:
`78B030 → 77FC20` at 78B877 (exact-beacon-05.tsv: 1695); 77FC20 searches existing
77F900 at 7801B3, fallback 780264→77E350 (durable-center-04.tsv: 1994,2038,2212–2245);
77E350→AD92E0 at 77E81F (static-exhaustion-04.tsv: 1412), then Q's AD93FA.
These exports are pinned in [continuation sources](continuation-020-sources.csv).

A new landing has a defensible opportunity to bypass existing-reference success,
not a guaranteed bypass. A virgin location may produce Q/E but no Workshop C.
No new outpost is required by N1, so the low-level eight-outpost cap is respected.
A populated new-site/beacon scenario or mature Save52 route needs a separate
specific design/approval; it is not an automatic fallback. New-site captures are
diagnostic holdouts, never silently appended to the frozen 23 validation corpus.

## Schema 2, linkage and health

Raw Event remains 17,768 bytes: 11 uint64 header values and 17×1040-byte Blobs in the
[original schema order](schema.md). New kinds 7/8/9 Q begin/normal/unwind;
10/11/12 E begin/normal/unwind. Existing kinds 1–6 retain their meanings; C normal
end additionally carries uint64 native return in result. Q/E result is uint32.
SEH and C++ exceptions propagate; abnormal completions have no invented result.

Q/E header `reference/context` are raw argument 1/argument 2 aliases, **not reference
identity**. input_hierarchy contains the raw argument tuple (24 bytes). Q captures
context 40, candidate 24, output-byte 1, bounds 16, optional world/source prefixes;
E captures collection0x90, object 16 and object+8 context 48 plus candidate/source 44,
translation 12 and landscape 0x58. These overloaded schema 2 diagnostic fields are
raw evidence, not C's hierarchy/reference meaning. See exact capture extents in
core.h. Each Blob preserves runtime address, length and independent success.
Unreadable optional data is unknown, never zero or a health failure by itself.
C retains rich ref/base/Workshop/cell/world/terrain/center/floor/grid snapshots.

TLS32 stack binds each admitted scope to its actual current parent and thread;
rejected nested admission is suppressed rather than inheriting an outer identity.
Stage active/entered atomics are independent counters. Sequence reservation may
precede concurrent publication, so journal order across threads need not sort by
sequence; per-scope order/containment must agree. MPSC4096 queue saturation,
excessive TLS depth and writer/guard faults stop admission and disclose loss.

A dedicated worker, independent of all native hits, flushes health.jsonl at a
one-second nominal cadence. Identity includes PID/creation FILETIME, DLL/game/SFSE,
module base, schema and QPC frequency. Health carries sequence/UTC/QPC, queue,
flushed event/offset counts, loss/depth/watchdog counters, Q/E/C active/entered and
nonce. Unique requests are flushed under .pending then atomically renamed to
.request; only complete final requests are scanned. ACK is emitted once after
worker flush. No nonce invokes engine code. 15-second deadline is operational,
not a scientific capture quota. Durable health success alone refreshes admission's
monotonic tick; stale tick closes later producer admission. Operator monitoring
also detects zero-native stalls/recovered heartbeat gaps.

Raw record flush precedes journal hash-receipt flush. Only complete referenced
records count. A raw tail or partial journal is retained and disqualifies negative
diagnosis. Inspector reconciles final entered counters, terminal counts/offsets,
queue/active 0 and fresh retirement clocks. Orphans remain literal observations
but cannot qualify chain negatives; grid attempts missing center/pre/result order
are incomplete. Synthetic fixtures are explicitly marked and never native proof.

## Admission, overlays and residual risk

Normal gameoverlayrenderer64/nvspcap64/nvppex are accepted provenance roles.
Unknown modules are recorded, not rejected for unfamiliarity. A specific known
conflicting instrument or unexpected owned-site bytes is a hard stop. Startup
records module path/base/size/SHA before edits, checks original guards and exactly
one observed thread (at most 120-second wait), writes admission then repeats the
sole-thread/all-preimage transaction. No worker exists before edits. New module
sets trigger fresh inventories; owned edits/untouched target entry guards remain
checked while draining and idle; CALL-window guards normalize the owned first 5
bytes and still verify surrounding bytes. Four relay byte/target/RX guards and
actual relay addresses/hashes/protections are recorded in patches.json. Module enumeration failure fails closed. Optional module hash failures are explicitly
UNREADABLE_ASSESS_SPECIFIC_RISK, never presented as valid hashes or an automatic
unknown-module exclusion; evaluate concrete interference. Mandatory game/SFSE/owned
site/relay identity failures remain hard stops.

Snapshots cannot prove thread-creation exclusion or universal patch compatibility.
The sole-thread observation and adjacent byte guards bound a research assumption;
actual accepted-overlay startup and game survival remain live NOT TESTED. No
suspension, weaker gate, hot-unhook or safe-mod-interface claim follows.
STOP is disk-floor-independent tiny exclusive control; worker drains admitted
scopes, flushes final health/retirement and retains inert patches/islands/DLL until
normal exit. Disk failure/stuck call/crash may prevent retirement. Preserve durable
prefix and separate target survival from evidence/science. No forced kill/attach.
