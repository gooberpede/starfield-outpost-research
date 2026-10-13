# Schema5 event and operational contract

0.5.0 retains the17768-byte Event layout and per-blob address/length/ok/raw fields.
All integers little-endian, runtime pointers are process VAs; module RVAs in
build.json are offsets from the pinned image base. FormIDs, native handles,
Workshop8-byte identities, pointers and saved tokens are separate domains.
The original [schema4 field contracts](../native-oracle-040/schema.md) apply to
route/selection/Q/E records; historical activation statements there do not apply
to050. Kinds1–6 ARE activated here through two guarded callback slots and
center/grid CALLs; they capture a separate Workshop oracle. Header reference is
the actual callback reference resolved by AD8EC0, not the marker or a base FormID.

| Kinds | Scope / blob contract |
|---|---|
|1/4/5,2,6/3|Workshop begin/end/unwind, natural center output, grid before/after; same callback invocation. result44bytes is actual in-place output; source and input_hierarchy44 are input descriptor copies; floor_xy8 is actual native input, translation12 and context_raw48 contain sampled operands/rectangle pointers. Callback end also snapshots context/latch. Center is linked only within actual callback/ref identity.|
|56|Workshop grid unwind: retains input, no invented output. Parent callback also unwinds5.|
|50/51/52|17DEC70 producing CALL17DEE5B begin/end/unwind, encloses existing77FC20 route when naturally reached. input_hierarchy=RCX/RDX/R8/R9 (32bytes); source=requestR9 (64bytes); candidate=outputRDX(40bytes); center=R13 original requested angles(16bytes); context_raw=RSI candidate reference(208bytes). ref/base/extra/cell/world are resolved RBX target samples, independent of chosen route marker.|
|53/54/55|CALL17DF168 handoff begin/end/unwind. source=RDX command(152bytes), candidate=RCX player+A08 state(152bytes); context_raw=RBX target208bytes; ref identity is R13 resolved route ref. Not asynchronously joined to50 by time/thread/values.|

For50–55 block contains12 little-endian u64 values: original caller return,
caller RBP, R14B decision (raw, not guaranteed move-ship flag), RBX target, R13,
RSI, R15, R12, caller param5 byte, caller param6 dword, prior-ship stack local,
actual instrumented CALL return. Unused/transient values remain raw, not guessed
structure fields. source preserves request+20/+28/+30/+38/+39 or command+8D/+8E.
Each scope has own invocation, real TLS parent, TID/QPC/order/FP mode. Command
parent0 after producer returns means UNASSOCIATED, not lost evidence. Optional
null/unreadable copies retain ok=false; zero-filled bytes never establish zero.
Status8 means a detected reference identity race, invalidating identity-bound
qualification. Optional list cycle/unreadable/bound bits remain disclosed.

Health entered counters group Q, E, and all callback/route/selection/travel scopes;
active counts must drain to0. Worker health/nonce challenge is independent of
callback reachability. Historical heartbeat delays are reported, not retroactive
failure. Current stale health requires a fresh ACK and assessment before action.
True writer/guard/disk/loss/depth failures stop admission. STOP drains admitted
work and writes retired.json; code stays resident. Abrupt exit before retirement
is partial evidence, not orderly completion. A crash cannot silently invent a
terminal receipt, but already flushed complete records remain preserved.

inspect_capture.py is the050 entrypoint. It validates schema identity, per-record
SHA256/extent/sequence, scope ancestry and phases, health and terminal counters.
Generic marker replay, ordinary Workshop center/grid replay, frozen center-byte
correspondence, and full durable equivalence stay distinct. It never promotes
full Workshop equivalence automatically. Radius/exclusion predicate, internal
marker creation branch and actual ship assignment remain UNKNOWN unless separate
qualified evidence establishes them; no hook was added solely for completeness.
