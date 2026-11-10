# B2 projection schema

`sor-d5bo-b2/1` is a fixed attempt-002 schema. The ZIP contains
`manifest.json` and `events.json` in that order. Each is ASCII JSON with LF
termination. The manifest contains the package tier, original and method
context, member size/digest, record and omission counts, original transport
attestation and claim limits. The container digest is external to the ZIP.
The builder pins the exact original reader, reducer, decoder and observer.

The array in `events.json` is in admission order and includes one row per
frame. In order, the common columns are sequence, kind, native QPC ticks,
thread alias, epoch, hazards, status, invocation, parent invocation,
selection/allocation, receiver alias, source alias, frame alias, signed
request X and signed request Y. QPC frequency is 10 MHz. Same-thread
admission order can break a QPC tie. Common request fields outside provider
context do not identify a geographic request.

| Kind | Additional columns in order |
| --- | --- |
| 1 Entry | Loss generation |
| 2 Selected | None |
| 3 Visited | Decision byte, token alias, loss generation |
| 4 Lookup | Slot, capacity, key alias, current epoch, source copy all zero flag |
| 5 Descriptor | Signed consumed-input minus conversion-manager delta |
| 6 Generating | Body FormID, geographic argument alias |
| 7 Sample | Mask, geographic argument alias |
| 8 Generated, 9 Returned | None |
| 10 FenceBegin, 11 FenceEnd | Fence reason, where 0 is ProcGen reset, 1 destructor, 2 map erase, 3 Grid clear and 4 source retirement |
| 12 Cold | Visited control word, visited data present flag, loss generation |
| 13 Ready | None |
| 14 Birth | Grid alias, consumed token alias, copied token alias, loss generation, geographic identity alias, target parts or null |
| 15 Published | Grid alias, destination at least `0x10000` flag, Grid index |
| 16 Reserve | Index, packed before control, packed after control |
| 17 Stored | Token alias, loss generation, signed destination minus paired reserve data base |

Alias zero preserves null. Nonzero aliases use first occurrence in each
domain in admission order. Lookup key and selected/born/published source
share a domain. A fence's receiver uses the domain for its reason. A
Grid alias therefore has no ProcGen meaning. Token, native frame,
geographic argument, thread and geographic identity each use their own
domain. Domain labels preserve equality within this session only. Flags
retain the indicated raw predicate and do not expose the operand.

Target parts are mode/face byte, world/FormID, signed coarse X/Y, signed
subtile X/Y and signed fine X/Y from the constructor copy. The original
copy starts at payload offset 152. The selected offsets within it are
`0x38`, `0x0`, `0x3c/40`, `0x4c/50` and `0x5c/60`. The geographic
key is `mode:(coarse_x×192+sub_x×12+fine_x):(coarse_y×192+sub_y×12+fine_y):FormID`.
The copied token is the u64 at `0x68`. Geography aliases derive from all
birth tuples. Only tuples matching the target key retain their parts.
The two store controls are packed native u64s, count in the low word and
capacity in the high word, each 32 bits. Deltas preserve only the pointer
relationships needed for the comparison.

The exact [builder](../../../research/resource-retained-population/d5bo_build.py),
[verifier](../../../research/resource-retained-population/d5bo_verify.py)
and [matrix](b2-matrix.json) control the remaining field and trust boundaries.
