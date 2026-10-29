# D5P-R2 unchanged-R1 adequacy decision

2026-10-29, Australia/Sydney. The initial REUSE UNCHANGED decision and matrix were
written before R2 implementation. Image-base and wrapper clarifications were
added during qualification without changing that decision. The
[invoked brief](../../implementation-briefs/CODEX_BRIEF_SOR_RG2_D5P_R2_retail_context_diagnostic_preparation.md)
freezes R2-AC1–R2-AC8 unchanged. Offline work only; retail is NOT AUTHORIZED.

**REUSE UNCHANGED.** The final R1 DLL/schema can identify the next admitted
source-demand validator's first failed predicate. It cannot recover the original
retail operands or uniquely explain every deeper native cause. Add a separate
offline decoder and native qualification, not a new observer profile or binary.
The existing full eleven-hook profile remains the diagnostic acquisition profile.
This decision concerns diagnostic adequacy, not the failed scientific hypothesis.

## Discrimination matrix and validity contract

Authority: actual `source_context`, `context_read` and `capture_visited` in
[observer.h](../../../runtime/retained-population/observer.h), decoded layout in
[read_capture.py](../../../runtime/retained-population/read_capture.py), and
[R1 contract](d5p-r1-design.md). Predicate order is
`1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,24,20,21,22,25,26,23`.
It is **not numeric reason order**. Each nonzero reason terminates this path.

All field offsets below are little-endian payload-relative byte offsets, unless
identified as object/frame offsets. The payload is 1,528 bytes. Common fields:
sequence/invocation/parent/thread/epoch/hazards/status at `0x0`/`0x10`/`0x18`/
`0x20`/`0x28`/`0x30`/`0x38`; frame/manager/ProcGen/source at `0x40`/`0x48`/
`0x50`/`0x58`; query words at `0x80`; mode at `0xa0`; owner at `0xb4`;
source bytes at `0xb8`, length `0x70`; effective descriptor at `0x128`, length
`0x2c`. Schema-2 fourteen-u64 suffix starts at `0x588` in declaration order:
reason, failed-read address/requested/returned/error, actual ProcGen, ProcGen
type, source index, Grid, Grid type, member-array pointer, count, capacity,
retained invocation Grid. Runtime VAs are diagnostic addresses, not stable IDs.

| Reason | First failed predicate / expected value | Discriminator retained; remaining ambiguity |
|---|---|---|
| 1 | Singleton read at image base + `0x5fd9c30` | Read address, size 8, returned count/error. Manager unavailable. |
| 2 | Source pointer at W + `0x38` | Failed-read tuple, valid manager. Source unavailable. |
| 3 | Query pointer at W + `0x3d8` | Failed-read tuple, valid source pointer. Query pointer not retained. |
| 4 | Current ProcGen at manager + `0x130` | Failed-read tuple; actual ProcGen unavailable. |
| 5 | Current ProcGen equals invocation ProcGen | Both VAs. Different objects are not automatically malformed. |
| 6 | Mode byte at manager + `0x20` | Failed-read tuple. Mode unavailable. |
| 7 | Source bytes, `0x70` bytes | Failed-read tuple. Partial destination bytes are unavailable as identity. |
| 8 | Original query, 8 bytes | Failed-read tuple. Query pointer recoverable from read address only here. |
| 9 | Owner at manager + `0x80`, 4 bytes | Failed-read tuple. Owner unavailable. |
| 10 | Effective descriptor, `0x2c` bytes | Failed-read address distinguishes mode-3 offset `0x1c0` from other-mode `0xc8`; descriptor unavailable. |
| 11 | ProcGen type word read | Failed-read tuple; type unavailable. |
| 12 | ProcGen type equals image base + `0x4b3f3a8` | Observed type and expected RVA; absolute expected VA needs an independently recorded image base. Different type is not a proven bad object. |
| 13 | Source index at manager + `0x120` | Failed-read tuple; index unavailable. |
| 14 | Current Grid at source index + `0x10` | Failed-read tuple; source-index VA valid, Grid unavailable. |
| 15 | Grid type word read | Failed-read tuple; Grid VA valid, type unavailable. |
| 16 | Grid type equals image base + `0x4b67f48` | Observed type and expected RVA; absolute expected VA needs independent image-base provenance. |
| 17 | Grid count at Grid + `0x10`, 4 bytes | Failed-read tuple; count unavailable. |
| 18 | Grid capacity at Grid + `0x14`, 4 bytes | Count valid; capacity unavailable. |
| 19 | Count <= capacity | Both read-valid values; malformed extent under this model. |
| 24 | Count <= 256 | Both values, native extent already passed. Observer coverage limit, not malformed extent. |
| 20 | Member-array pointer at Grid + `0x18` | Failed-read tuple; pointer unavailable. |
| 21 | Each member slot, 8 bytes | Address, array pointer and count identify failing slot. Earlier member values/matches are not retained. |
| 22 | Source belongs to inspected member array | Successful full bounded traversal with no equality, including empty array. Array contents are intentionally not retained. |
| 25 | Invocation Grid at W + `0x100` | Failed-read tuple. Invocation Grid unavailable. |
| 26 | Invocation Grid equals current Grid | Both read-valid VAs; pointer disagreement only, not allocation lineage. |
| 23 | No starting/current hazard, unchanged epoch, recorder not broken | Starting hazard/epoch retained. Current hazard/epoch/broken state not retained; exact subcause UNRESOLVED. |
| 0 | All predicates passed | Read-valid ordinary context; not proof of selected geographic identity or complete lifetime coverage. |

Read-validity is derived from the reached path, not a stored bitmap. A field is
valid only if its read precedes the failed predicate; the failed read's output
and all later outputs are unavailable. The failed-read tuple itself is meaningful
only for a read reason. Mode is assigned to `args[4]` even after an earlier failure;
initialized zero is not evidence. The visited hook overwrites `args[1]` with the
saved RSI low byte; only `args[0]` holds the original two packed query words.
Later hooks can overwrite argument/descriptor fields, so first-failure decoding
uses demand records only. A direct `context_read` fixture record is not a complete
source-context invocation and must be identified separately.

An address rejected before `ReadProcessMemory` has returned count/error zero;
this is a range refusal, not an observed Win32 read error. A null pointer is an
observed absent pointer only when its own slot read passed. Partial read contents
do not qualify. Type differences, malformed extents, inspection limits, missing
membership and unreadability remain separate outcomes.

R1 identity does not retain the relocated image base. The type comparison can
still be identified by reason and interpreted using its expected image-relative
offset. A later proposed READY receipt must capture module base independently
through read-only process metadata to supply the absolute expected VA. The reader
leaves that VA unavailable when base provenance is missing; it never derives a
base from the rejected type pointer.

## Invocation, source and lifetime limits

`capture_visited` allocates per-invocation tokens and records parent/thread plus
global conservative epoch/hazards. No source/geographic/owner/mask pre-filter
exists. Legitimate non-target contexts remain recorded. Missing demand admission
produces no demand record; ordinary losses advance the global epoch. Disabled
wrappers, upstream paths that never reach the site, fatal output failure and
unflushed tails also prevent usable diagnostics. No admitted target is not absence.

The generator fifth argument is a definition object, not a Grid. Native getter
and forwarding evidence cited in [R1 diagnosis](d5p-r1-diagnosis.md) establishes
that distinction statically. Completion `args[3]` retains it, but demand records
do not. It is not part of the source-context validator. No new speculative
definition dereference or hook is necessary to identify its first failure.
No broad memory dump or complete membership array is retained. Geographic
interpretation requires separately supported source and manager-frame decoding;
an invalid context never becomes a certified selected-source identity.

Reason 23's subcauses, earlier matching members before reason 21, simultaneous
later failures and upstream contexts producing no record remain indistinguishable.
These ambiguities do not hide which validator predicate first rejected a recorded
invocation. The diagnostic result must stop at that predicate when operands cannot
explain more. Historical root cause remains UNKNOWN.

## Chronology and architecture choice

The original Phase B records contain admission sequence but no event clock.
Fresh pre-load READY authenticates only startup. Arrival health finds the terminal
already failed; no intervening load/travel checkpoint establishes where the first
invalid demand occurred. Inspect original nonce/terminal/milestone receipts in R2
qualification before finalizing the card. Pending that inspection, retain ordinary
Save52 load and travel to second Feynman V; do not shorten to load alone.

Alternatives considered: reuse unchanged with explicit decoding (selected);
selectable low-volume profile (unnecessary binary change without demonstrated
discrimination benefit); new hooks/architecture (no missing first-predicate
boundary demonstrated). Full profile has existing bounded traversal/queue costs
and potentially high geometry traffic. Requalify ordinary-loss resilience and
measure current native activity; do not label the full profile low-volume or
retail-safe from synthetic means. Existing R1 DLL SHA-256:
`503464d3670ff00422303c10652b036cd0bc891d3f8f7cba9a22d9d396fb5667`.
No new DLL or deployment ZIP is to be represented as an R2 build. R1 issued no
deployment ZIP. R2 may supply a clearly labelled distribution wrapper containing
those exact unchanged DLL bytes and existing notices, separately hash-bound to
its reader/card and qualification. That is packaging, not a new observer build,
profile or retail qualification.
