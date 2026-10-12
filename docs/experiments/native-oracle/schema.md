# Native capture and comparison schema

SorNativePositionOracle0.1.0; schema SOR native event1, little endian x64.
Raw Event is17,768 bytes. Header=11 unsigned64 values: sequence, invocation,
parent, QPC, reference VA, context VA, thread ID, kind, status bits, MXCSR,
LastError. Kind1 begin;2 center-return;6 grid-before;3 grid-after;4 normal-end;
5 abnormal-end. Sequence allocation can precede queue publication, so journal
order across threads need not equal sequence order. Invocation/parent IDs are
observer-local identifiers, never saved IDs/FormIDs/handles.

Seventeen Blob fields follow in exact order: ref, base, extra, cell, world,
context_raw, source, candidate, translation, landscape, center, input_hierarchy,
floor_xy, result, block, merge, scale. Each Blob is1040 bytes: runtime VA uint64,
requested length uint32, read-success uint32,1024-byte zero-padded buffer.
Only success1 authorizes using its first length bytes. Failed reads are unknown,
never zero-valued observations. Field extents are defined in core.h and backed by
the existing static contracts. Status bits:1 extra cycle;2 unreadable node;
4 bounded-chain exhaustion;8 repeated reference identity changed;16 center
reference mismatch;32 no associated center. No name/player testimony fills a gap.

Native fields include the actual center12, input/result hierarchy44, floorXY8,
translation12, landscape resolution+50/body+54, block/merge/scale globals,
reference/base/cell/world prefixes and concrete Workshop extra+60/+98. Opaque
hierarchy asset handles stay raw. Raw reference pointer, FormID, handle, stored
parent pointer, serialized tokens and Workshop identifier are separate domains.

Worker writes fixed records to events.bin and flushes each; records.jsonl then
records offset/length/SHA256/sequence/invocation/kind and is separately flushed.
Only complete journal-referenced hashes are classified. An incomplete final line
and unreferenced raw tail are retained and reported. A hash proves byte integrity,
not semantics or authenticity. Power-loss durability is not established merely
by a successful FlushFileBuffers. No orphan/truncated original is repaired in place.

READY pins component/version/game/SFSE/plugin/base/schema/session process identity.
retired.json reports observed event/loss/depth counts and resident inert patches;
failure/not-ready reports are independent. No marker promises game survival.

Offline inspector verifies frozen prediction SHA256, record integrity, unique
sequences, normal begin/end, same thread/reference/context, exactly one earlier
associated center and matching grid-before record. Scientific identity uses
ordinary base002C60E9, Workshop identifier and actual landscape body; it never
uses output equality to select a beacon. It reports native hierarchy and exact
center equality separately from conditional native-input replay.

With supported R256/B12/scale.01 and supported round-to-nearest normal inputs,
offline DERIVED translated bits/floor and signed hierarchy offsets are compared
exactly with actual floor/result. Subnormal/overflow/unknown FP domains remain
UNASSESSED. The saved→loaded source-frame/translation join is deliberately still
UNASSESSED until independent primary evidence reconciles it. Matching a native-input
replay is not end-to-end saved-position equivalence, arbitrary-angle validation,
blind holdout success or complete branch coverage. No expected output is read by
the DLL, injected into native inputs or retuned after capture.
