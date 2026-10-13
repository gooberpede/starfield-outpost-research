# Schema 6 — native position-write history

Retail1.16.244.0 preferred base `0x140000000`; actual module base and hashes are
session fields. Scientific addresses are RVAs in `site`, runtime VAs in arguments
and Blob addresses. FormID, Workshop ID, command generation, saved token and
pointer are distinct domains. Every session/process creation supplies a separate
epoch; no cross-session pointer association is allowed.

Workshop IDs use the established raw-byte hexadecimal convention, not a uint64
numeric spelling. Prior050 bytes at extra+98 are `f1517de43e171745` and
`0efca066ee4c7b9b`; their little-endian uint64 spellings would instead be
`4517173ee47d51f1` and `9b7b4cee66a0fc0e`. Literal run-card-ID fixtures verify
this domain without deriving the expected IDs from the decoder itself.

An Event is3328 bytes, little endian, with16 unsigned64-bit header words:

`sequence, invocation, parent, thread, qpc, site, kind, phase, reference, command,
result, status, arg0, arg1, arg2, arg3`.

Then eight400-byte Blobs, ordered `ref, base, extra, cell, world, operand, aux,
output`. Each has runtime address uint64, requested length uint32, successful
read flag uint32,384 owned bytes. `ok=false` means unavailable, never zero-valued
native evidence. Unused bytes are zero padding; only requested successful bytes
have semantic standing. Decode floats from exact raw little-endian binary32
bytes; unusual/nonfinite values do not terminate healthy acquisition.

| Field | Source / use |
|---|---|
| sequence | Serialized file-write order under spool lock, starting1. QPC is sampled earlier and may have a different cross-thread order. Not a global engine causal clock. |
| invocation/parent | Global observer invocation number and actual enclosing TLS invocation; cross-thread deferred application has its own parent, never a fabricated TLS ancestor. |
| kind/phase | replacement1; conversion2; scalar XYZ application3; immediate producer4; queued producer5; reserved submission6; deferred application7; center8; command allocation9; initial-restoration setter10 at5A14DA. The latter distinguishes the saved construction/rework path without claiming allocation birth. Phases: before1, after2, unwind3. Submission6 is reserved and not emitted by native hooks. |
| result | Actual RAX after return; unspecified for native void functions. Only command allocator return has the evidenced pointer interpretation. |
| ref | Reference prefix0xD8; XYZ+8C/+90/+94, FormID+28, base+98, own cell+B0, extra-list+C8, frame byte+D3. Raw +24 is not relabelled a handle. No native handle resolver is called; legitimate handle is UNAVAILABLE. |
| extra | TypeBC node0xA0; compensation+60/+64/+68 and stable observed Workshop identity bytes+98..9F. Bounded walk statuses: cycle1, unreadable2, traversal bound4. These are optional-field limits, not event quotas. |
| cell/world | Own cell prefix0x118 and exterior world prefix0x180, if available. Null own cell is retained; no guessed resolver fallback or query-source-world substitution. World body/geography resolver is UNAVAILABLE here. |
| operand | Original pointer XYZ12 for setters/converter/producers; scalar application copies16 including integer mode at+C. Original pointers, not snapshot replacements, are forwarded. |
| aux/command | Application at18CE315 uses native R8−10 command pointer; copies command0x30 (XYZ+10, reference+20, parent+28). Allocation after-event stores real RAX as command, enclosing queued producer as TLS parent. Allocation occurs before payload construction/publication; it is not evidence of successful enqueue. |
| output | Center caller output12 from original RDX; only after-phase is returned center. Allocator after-phase captures returned allocation prefix, still uninitialized payload. |
| status | Bit8 means reference prefix changed during snapshot. Raw bytes remain available, but all identity binding from nonzero-status events is quarantined. Sampling is non-atomic; a zero status detects no sampled change, not a proof of atomicity. |

`events.bin` owns unmodified records; `records.jsonl` supplies sequence, byte
offset, fixed length and SHA256 per accepted raw record. Both use cached serialized
WriteFile; worker FlushFileBuffers(raw), FlushFileBuffers(journal), then writes
health/ACK evidence. Counters: attempted record emissions, captured raw+journal
writes, last durable sequence after both flushes, failed operations and active
invocations. Write/flush failure closes admission and retains partial tails.
No data rewriting or zero-fill repair occurs. An unjournaled raw tail is located
and counted separately; a one-record preview is diagnostic, not the entire tail.

`session.json`, `admission.json`, `patches.json`, initial/final module inventories,
`ready.json`, append-only `health.jsonl`, nonce ACKs and retired/failure receipts
support identity/health/retirement. `operator-stop.flag` is a four-byte preallocated
mutable control (`RUN\n`→`STOP`). `emergency-status.json` is a4096-byte preallocated
mutable failure-only page: initially `{}` padded with spaces, overwritten after
actual failure without growing the file, including failed disk queries/terminal
receipt writes. It never replaces or rewrites raw events. If even its write fails,
missing terminal is an integrity/retirement gap, never normal retirement.

Inspector states are independent: committed-prefix integrity, terminal/retirement,
paired/unfinished invocations, observational history and scientific equivalence.
No records means UNUSABLE_OR_MISSING_EVIDENCE, not a scientific negative. Captured
segments are PARTIAL_OBSERVED_HISTORY; allocations/destructions, inlined writers
and save remapping remain uncovered. Observed identity changes split pointer
segments; earlier unknown-ID records are candidate late binding, with lifetime
UNPROVEN. Same-ID reuse cannot be excluded. Command links similarly remain
observed address-generation candidates with other-allocator/reuse uncertainty.

COMPLETE_WITHIN_COVERED_WRITER_SET_AND_LIFETIME requires independent evidence for
both coverage and lifetime; this observer does not certify either from hook
counts. SCOPED_NO_WRITE requires a proven interval/branch/ownership argument;
equal snapshots or a compatible d3 gate do not establish it. The inspector keeps
unchanged/gate-compatible candidates separate and emits NOT_ESTABLISHED for
no-write. Full restored XYZ equivalence remains NOT_TESTED until independently
associated native/saved frame and history evidence supports it.
