# Native position oracle 0.3.0 / schema 3

Only the pinned retail 1.16.244.0 executable SHA256
`7e9adb1414a8e1b325e5e1f097b9b17b78deb7eebeda37a333351a43a60f9d28`.
Addresses below are module-relative RVAs. Event byte layout remains 17,768 bytes,
little-endian: eleven uint64 header values followed by seventeen 1,040-byte blobs
`<QII1024s>`. Blob address is the sampled runtime VA, length requested bytes,
ok is exact ReadProcessMemory success. Failed reads never mean zero. Unused blobs
have zero length/ok. Raw pointers are process-local and not serialized identities.

Header fields: sequence, invocation, parent, QPC, reference, context, thread,
kind, status, MXCSR, LastError. For Q records reference/context preserve Q's
RCX/RDX arguments (query context / candidate descriptor); additional helpers use
the owning Q's identity, not a new invocation. Parent remains Q's parent; events
are ordered by sequence with QPC/thread corroboration. Nested scopes and E/C
retain their distinct invocation IDs. No proximity joins.

Kinds 1–12 preserve 0.2.0 C/center/grid/Q/E layouts except **Q kinds 7–9**:
source now reads context[4]'s 24-byte angular descriptor; floor_xy reads the eight
bytes at world+310 **as a packed value**. World prefix still preserves those bits.
center remains the latch byte, translation the 16-byte query rectangle,
context_raw the five pointers/40 bytes, candidate the 24-byte Q descriptor.
Normal Q result is four EAX bytes; abnormal completion has no result.
Use schema3 reader; never reinterpret original schema2 captures in place.

| Kind / complete CALL | Natural ABI input | Completion-specific blobs |
|---|---|---|
|13 resolver AD08F2→AD5760|RCX world, EDX candidate key, R8 descriptor|ref returned form prefix 0x30 (type +2E)|
|14 fallback AD0903→5DE3B0|ECX key|ref returned form prefix 0x30|
|15 overlay AD092C→ACCAD0|RCX pointer-to-owner slot, RDX resolved form|extra returned overlay prefix 0x34: flags +20, four signed rectangle dwords +24..30|
|16 A AD0976→96EFB0|RCX landscape, RDX output, R8 angular descriptor|candidate 44-byte A; retain its stack pointer within Q only|
|17 B AD0986→96FB40|RCX landscape, RDX output, R8 packed value|candidate recopy of A and source B, both 44 bytes after B returns|
|18 final source AD0AE5→96EB90|RCX landscape, RDX output, R8 source descriptor|center actual 24-byte source pointee; source 44-byte converted output|
|19 final delta AD0B08→96F940|RCX landscape, RDX output, R8 source hierarchy, R9 candidate hierarchy|translation eight-byte signed XY delta; source/candidate 44-byte actual inputs|
|20 E entry AD0AB5→B1E190|RCX collection, RDX callback object, R8B option|actual entry marker before optional E diagnostic admission; no return blob|
|21 helper abnormal completion|status identifies helper kind13–19|arguments and shared samples only; no return/output inference|

Kinds13–21 input_hierarchy contains four uint64 argument slots (32 bytes; unused
slots zero). result contains eight RAX bytes on normal helper completion; these
are transport bits, not an invented return semantic. Resolver/key upper halves
are the actual zero-extended argument values passed by the native caller.
Common blobs: context_raw40, world0x390, floor_xy8 packed-key sample, block/merge/
scale4 each, extra0x34 overlay when known, landscape0x58 when known (resolution
+50/body +54). The landscape VA comes from actual A RCX, not guessed global
state. A absent on normal nonnull-overlay path identifies the null-landscape
static path; no unsafe global-chain traversal is added solely to sample null.

Ordered hierarchy tests are byte0,dword4,dword8,byte10,dwordC,dword14,dword18,
byte20,dword1C,dword24,dword28, hexadecimal offsets. Padding is not compared.
`branch_inspect.py` uses full private output snapshots, helper argument linkage,
Q result/latch, normal completion, journal/ancestry and worker health. An actual
E-entry marker discriminates E entry even if STOP rejects its separate diagnostic
lease. Admitted Q helpers continue after STOP, then normal retirement drains Q.

Shared overlay/landscape/settings/key/context source contents are samples, not
an atomic snapshot or exact tested machine registers. Structured disagreements
remain visible. Equal hierarchy with no E can identify the pinned static flag
skip under a complete healthy normal Q; it does not assert the sampled flag was
the byte tested. Delta proves that final geometry was reached; the rectangle
loaded earlier into XMM6 is **not** claimed captured at its actual load. No exact
final rectangle arithmetic equivalence is asserted from shared rectangle samples.
An incomplete/unhealthy/unwound/contradictory chain is UNQUALIFIED. Missing reads
needed for path inference also prevent that inference. Synthetic records always
remain qualification only; this schema supplies no saved/runtime identity join.
