# D5E native decision contract

2026-10-25, Australia/Sydney. [Report](report.md), [coverage/schema](schema.md),
[source pins](sources.csv). All native addresses below are preferred static VAs,
image base `0x140000000`, Starfield 1.16.244.0, executable SHA-256
`7e9adb1414a8e1b325e5e1f097b9b17b78deb7eebeda37a333351a43a60f9d28`.
Runtime VA adds the measured module base to the RVA. Offsets are byte offsets.
These are observed internal mechanisms, not validated mod interfaces.

## Four permanent observation sites

The original provider export is
`.local-work/recon/resource-milestone-b-producers-01.tsv`; the generator export
is `.local-work/recon/resource-availability-cont-01.tsv`. Both are pinned in
the source ledger and inherited [D5C evidence](../resource-population-lifecycle/native.md).
This assignment rereads existing exports; it makes no Ghidra change or new export.

| Static VA / RVA | Instruction and decision | Synchronous operands and limitations |
|---|---|---|
| `0x14079fca3` / `0x0079fca3` | `TEST SIL,SIL`; subsequent `JNZ 0x14079ffaa` is the visited bypass | Low RSI byte is the previously computed visited result. RDI contains the visited identity loaded from source `+0x68`, not the source pointer. Shared-lock release has already occurred; the captured branch operand remains thread-local. A zero result is not a map miss. |
| `0x14079fcd0` / `0x0079fcd0` | `CMP RAX,[R13+0x28]`; equality branches to miss at `0x14079fd02` | RAX is the lookup result, R13 the ProcGen object, capacity at `+0x28`. Result below capacity is hit. Slots at `+0x20`, stride `0x18`: key `+0`, wrapper `+8`, occupancy `+0x10`. Require exact pointer key and occupied slot on hit. Null wrapper remains a named incomplete operand. |
| `0x14079b8ed` / `0x0079b8ed` | `MOV [RSP+0x30],AL` after sampler call at `0x14079b8e8` | AL is the directly sampled ordinary low nibble, not geometry-inferred mask 3. Geographic argument pointer is saved at generator working RSP `+0x2f0`. Require return address at `+0x2d8` to be relocated `0x0079ff1d`. Values outside 0–15 are rejected. |
| `0x14079feaf` / `0x0079feaf` | Call to coordinate converter `0x14078d660` | R9 is the original query pointer and R8 the selected `0x2c` descriptor. Copy both before the call; compare query with the saved original pointer's Int2. The retained source map is already updated at this point. This is not the later generation-cell query. |

Let P be provider entry RSP and W its working RSP. Provider pushes `0x40`
and allocates `0x388`, so W = P minus `0x3c8`; provider RBP = W plus `0x100`.
Original RCX and RDX pointers were saved at P `+8/+0x10`, hence W
`+0x3d0/+0x3d8`. The enumerated source pointer is W `+0x38`.
Generator call pushes eight more bytes; its prologue pushes `0x38` and allocates
`0x2a0`. Thus W = generator working RSP plus `0x2e0`.
These are instruction-backed stack relationships, not guessed object offsets.
The native adapter validates provider R13 against the saved ProcGen and current
manager `+0x130`; it copies the source, query and manager again at the same stop.
Equal copies establish stop-local consistency only.

Provider entry `0x14079f860` is validated as the origin of saved arguments, but
is not armed. BIOM-null paths bypass these sites. Therefore this instrument
does not claim a census of provider entries, sources lacking BIOM or every
possible request. It continuously covers the inspected visited/map decisions
that actually reach these permanent boundaries after arming.

## Lock, ownership and lifetime interpretation

The visited guard acquires shared ProcGen `+0x40` at `0x14079fc45`, compares
eight-byte source `+0x68` against visited count/data `+0x48/+0x50`, then releases
before testing SIL. The exclusive lock acquired at `0x14079fcb3` spans the map
lookup, insertion and synchronous generation through `0x14079ffa5`. Two threads
can both pass the earlier guard; the later exclusive lookup can then hit a
population constructed by the first. Debugger all-stop order is observation
order, not a claim about scheduler fairness or the original historical winner.

Insertion call `0x14079fdf9` returns new/existing status in AL. The new-slot
stores at `0x14079fe14/18` retain the wrapper before generation at `0x14079ff18`.
The existing-slot branch assigns/references/releases separately. The permanent
conversion site can preserve retained slots but does not observe the insertion
return or a completed generator outcome. Generation has prerequisite exits;
visited append at `0x14079ff60` is not a completeness certificate.

Reset `0x14079ddf0` acquires exclusive protection at `0x14079de83`, clears source
holders at `0x14079de8d` and resets visited storage. Destructor `0x14079d910`
clears/frees the same stores without a demonstrated local lock; manager cleanup
`0x140788d4f..0x140788d66` destroys/frees ProcGen. Source-index replacement and
all aliases are not exhaustively fenced. None of these lifecycle sites is armed.
Four fixed decision/query/mask slots cannot additionally establish those fences.
Between-stop reset or same-address reallocation can reproduce identical bytes.

Consequently native stops are **UNJOINED_STOPS** with unknown manager/source
lifetimes. The adapter/reducer does not merge them into population epochs, even
when thread, stack, pointer, geographic key and bytes agree. It records frame
coordinates as correlation candidates only. Native tier A/B is unavailable;
observed branch operands remain tier C with the missing lifetime fence named.
This is an explicit AC4 technical blocker, not a claim of native impossibility.
The smallest completion discriminator is a same-invocation generator terminal
with explicit outcome; a separate complete lifecycle fence is still required
before joining requests across reset/replacement. Adding either probe must first
resolve the four-slot budget without suspending visited/map coverage.

## Geographic association and scientific limits

The [owned D5B geographic decoder](../../../research/resource-combined-acquisition/reduce.py)
is reused unchanged: qualified chart 0, descriptor coarse coordinates times 192,
subindices times 12, residuals, plus source anchor. Mode `+0x20 == 3` selects
manager descriptor `+0x1c0`, otherwise `+0xc8`. Require exact source key
`0:37536:20928:0029d20e` and owner `0x0005e0de`. Unsupported charts, other sources,
incoherent source bytes, invalid frame or incomplete identity reads are rejected.

This is **INTERIOR_FRAME_AND_OWNER_ONLY** association. The source's SFBK numeric
identity alone does not prove associated definition-file provenance. That is a
separate named missing field. A future reader can preserve an explicit hit/miss
or bypass operand while refusing a fully qualified historical source association.
No resource-name match, Workshop token, source pointer or timestamp supplies
missing ancestry. Seven indeterminate Save52 associations remain unchanged.

Direct mask comparisons retain both frozen alternatives 0 and 3 and any other
observed value. Matching mask 3 is not deduced from the D5B geometry matches.
A miss during a Save52 load interval needs actor/call-path context before any
claim about ordinary distant-source eager generation. A hit/bypass says nothing
about the population's first-ever construction, serialization or success.
