# D5AB native hook and synchronization map, version 1

**Working candidate, not an accepted lifetime-completeness proof.** The
[handoff](d5ab-report.md) records unfinished native coverage and final review.
This checkpoint authorizes no further native analysis.

2026-10-31, Australia/Sydney. Candidate schema `sor-d5x/3`, observer 0.3.0.
The [original contract](../../implementation-briefs/README.md#archive-lookup) (`implementation-briefs.zip :: docs/implementation-briefs/CODEX_BRIEF_SOR_RG2_D5AB_observer_remediation_live_readiness.md`)
and [active ledger](d5ab-investigation-ledger.md) govern qualification.
All locations below are **RVAs** for image base `0x140000000` and executable
SHA-256 `7e9adb1414a8e1b325e5e1f097b9b17b78deb7eebeda37a333351a43a60f9d28`.
Runtime VAs add the freshly verified module base. No cross-build transfer is allowed.

## Retained and added sites

| Index | RVA | Displaced bytes | Contract and synchronization |
|---|---|---:|---|
| 0 | `0x79f860` | 7 | Provider entry/return; original Int2, thread and parent invocation. |
| 1 | `0x79fa90` | 8 | Replay cursor load and stack store; record pointer without following it. |
| 2 | `0x79fca3` | 9 | Preserve TEST/JNZ and both destinations; record SIL and consumed RDI token. No source dereference. |
| 3 | `0x79fccb` | 5 | Original pointer-map CALL and result under ProcGen exclusive protection; bounded source copy only when lifecycle context remains valid. |
| 4 | `0x79feaf` | 5 | Original converter CALL and per-thread conversion scope. |
| 5 | `0x79ff18` | 5 | Original generator CALL and all six arguments; returned generation is not geometry success. |
| 6 | `0x79b8e8` | 5 | Original ordinary sampler CALL and actual AL; no guessed mask. |
| 7 | `0x79ddf0` | 5 | Broad reset entry/end; global hazard and epoch. |
| 8 | `0x79d910` | 5 | ProcGen destruction entry/end; invalidates affected continuity. |
| 9 | `0x975030` | 8 | Map erase entry/end; conservative global invalidation. |
| 10 | `0x9829b0` | 5 | Bulk Grid clear covers frees at `0x982af8`; no container scan. |
| 11 | `0x982b70` | 5 | Standalone retirement covers erase, unlock and free at `0x982c32`. |
| 12 | `0x79dec4` | 5 | Reset unlock CALL after both stores clear while exclusive protection remains held. |
| 13 | `0x78d6f4` | 5 | Original normalizer CALL receives actual engine-local descriptor and Int2 copy. |
| 14 | `0x9830cd` | 12 | Constructor-private R14 allocation after geographic fields and token initialization; copy bounded prefix, then replay two LEAs. |
| 15 | `0x983177` | 11 | Replay index conversion, backing pointer load and actual source-pointer publication store before witness. |
| 16 | `0x79ff3e` | 5 | Original visited reserve CALL; preserve all operands and result, including `0xffffffff`; record before/after count/capacity and resulting data pointer. |
| 17 | `0x79ff59` | 11 | Replay index conversion, backing pointer load and token store before witness; failure branch bypasses the entire site. |

Exact original bytes, 32-byte guards, CALL destinations and guard hashes belong
in the local native-site receipt. The build authenticates the entire installed
image and all fourteen inherited site pins before deriving the four new guards.
Each fixture package retains its own site guards; fixture VAs are not retail VAs.

## Identity and lifetime proof boundary

The native source constructor is `0x140982d90`, not a universal birth function:
its dedup branches return an existing allocation. The new-allocation branch
allocates `0x1a0` bytes at `0x140983001`, checks null, initializes SFBK and
geographic ancestry, and writes the token at `0x1409830c9`. At the birth site,
R14 is private to construction and has not reached the vector store at
`0x14098317e`. Grid `+0x5c` protection surrounds this constructor. The witness
does not acquire another engine/observer lock or traverse backing storage.

Only initialized semantic fields define identity: SFBK `+0x00..+0x03`,
geographic/ancestry `+0x38..+0x63`, and token `+0x68..+0x6f`. Padding
`+0x64..+0x67` is preserved as raw prefix data and ignored semantically. Bounds
at `+0x18` are completed later; the string at `+0x70` is not constructed yet.
The prefix is not a complete object, generator-origin snapshot or allocation lease.

Allocation failure bypasses birth. String-construction failure can leave birth
without publication; reserve failure can return a nonnull R14 without vector
publication. These are unqualified lifetimes. The candidate conservatively
requires a successful publication witness. Source-acquire callers may pass a
nonnull returned pointer to cells even when vector publication failed; that
possibility is not treated as successful publication or absence of selection.
Dedup can reuse a previously witnessed lifetime; it does not create a new birth.

At the visited branch, RDI is the token already read by native instruction
`0x14079fc37`, before the visited reader acquire at `0x14079fc45`. Neither the
visited lock nor Grid retention proves source lifetime there: the
[D5S detached-density counterexample](d5s-report.md) still applies. The observer
passes RDI by value and joins it offline to the birth/publication witnesses.
It never rereads the selected source at this boundary.

The join requires birth/publication before provider entry, the same pointer and
consumed token, no intervening rebirth or non-reset lifecycle fence, unchanged
birth-to-visited/store loss generation and valid invocation context. A broad
reset clears visited membership but does not establish a new source lifetime.
Any unknown birth, lost lifetime interval, pointer reuse, collision or ambiguous
publication refuses qualification. Raw pointer, eight-byte token, geographic
key, observer allocation ID, ProcGen epoch and loss generation remain separate.
Conservative global invalidation may reject an unaffected source; it never
certifies one by geographical plausibility.

## Append semantics and callback cost

The reserve helper at `0x1422cc0d0` returns an index and increments count on
success. Allocation/growth failure returns `0xffffffff`. The provider compares
that sentinel at `0x14079ff54` and jumps to `0x14079ff64`, skipping the store.
The store bridge starts at `0x14079ff59`, replays all eleven bytes including
the write at `0x14079ff60`, and only then calls its observer. The reducer checks
index/count/capacity, actual destination, token, thread, invocation, source and
epoch. Reserve success alone and later bypass alone cannot establish insertion.
None of these witnesses proves nonempty or complete generated geometry.

Callbacks use fixed-size records and bounded reads only at the specified owned
boundaries. No hook performs file I/O, hashes the image, allocates a variable
buffer, acquires a new lock, scans Grid members or calls an identity helper.
Queue reservation is bounded to 32 retries. Diagnostics run in the worker.
Original calls forward arguments/results; reserve exceptions are recorded then
rethrown. Observation adds execution time, including within native protection.

The five inline bridges preserve flags, volatile integer registers and XMM0–5.
Constructor sites have no later live upper-YMM consumer; provider allocation
uses YMM0 followed by VZEROUPPER before later CALLs and append. The new store
site has no live upper-YMM consumer. Ordinary x64 ABI calls already treat those
upper lanes as volatile. General asynchronous exception unwinding through
emitted bridges/trampolines remains unqualified; no universal unwind-safety or
retail behavioral claim follows from disposable tests. STOP leaves resident
wrappers forwarding originals; hot unloading and hot unpatching are unsupported.

Rejected alternatives are rereading selected source memory, scanning a moving
Grid vector, assuming Grid retention protects each source, joining by token
alone, marking a reserve return as a store, filtering guessed target pointers,
and treating an operator arrival checkpoint as an engine-native instant.
Additional travel/loading hooks are unnecessary for this bounded construction
question; operator checkpoints supply intervals only. Native visual-arrival
ordering remains unknown and is excluded from B2 success claims.
