# B2 original event sufficiency

**A reduced row for each of 32,141 original frames supports the bounded
recorded chronology and its negative controls.** The original is present
and authenticated. The scope is the recorded attempt-002 history under the
pinned observer and ordinary native mutation graph. Complete native
instrumentation coverage, exact scheduler cause and population geometry
remain unknown. [Original D5AC report](../../experiments/resource-retained-population/d5ac-report.md) ·
[Machine-readable evidence and omission matrix](b2-matrix.json)

| Claim | Records or premises and disposition |
| --- | --- |
| Provenance | Schema `sor-d5x/4`, attempt 002, Starfield 1.16.244.0. Capture 10,542,248 bytes. Fixed-offset framing checks magic, 312-byte payload, header and payload sequence, CRC and the stream SHA-256. Historical reader equality includes all 56 cumulative ACKs, terminal accounting, zero reported drops/faults and zero qualified firstness chains. These are original-side checks. |
| Historical sample | The maintainer reported one Save52 load at the Lodge and direct travel to Feynman V Cu IL F. The protected Save52 copy is 16,411,136 bytes, SHA-256 `6b4a10084c7e752c31fd2de121a00850aaa2bf1decd700b437d7dccfcdbc82e8`. D5BO rehashed that copy against the original run card. The report of game actions is separate from native clock evidence. [B2 card](../../experiments/resource-retained-population/run-card-d5x-b2.md) |
| Allocation and source | Private birth 2074, publication 2075, allocation 932, geographic identity `0:37536:20928:0029d20e`. Source pointer equality, ProcGen receiver equality, Grid receiver equality, token equality, and constructor allocation ID are separate domains. Seven earlier births share the target tuple and token but precede allocation 932 in separate epochs, with intervening Grid fences. One shares its Grid receiver. |
| Decisions | Entry 8004, selection 8005 and unvisited 8006 belong to invocation 3837, query `[4,-1]`. Entry 8018, selection 8019 and unvisited 8020 belong to 3844, query `[5,0]`. Both joins reach the same live source and ProcGen at epoch 207. The original request is a signed Int2. |
| Protected order | Lookup 8091 records slot/capacity 64/64, a miss. Lookup 8339 records 18/64, a hit. Both carry the same full source pointer as map key and current epoch 207. The alias preserves pointer-key equality without including pointer values. No other recorded lookup has that key. Native QPC is captured before enqueue, and 97 adjacent sequence/QPC inversions rule out sequence as a universal clock. Across-thread QPC ties remain unordered. |
| Construction and alternative | Descriptor delta 8092 is `0xc8` from the conversion manager. Generator 8093 has body FormID `0x0005e0de` and the same geographic argument as sample 8094. Generated 8104 precedes reserve 8105 and matching token store 8106. Reserve index 21 advances count 21→22 at capacity 32 and destination delta is 168. Return 8110 follows. Invocation 3837 later selects a different source at 8340, bypasses at 8341 and returns at 8345. There are 46 other-key protected lookups. |
| Compiled constraint | Preferred VA `0x14079fccb` calls lookup after exclusive acquisition. The miss branch requires insertion at `0x14079fdf9` and key/wrapper writes at `0x14079fe14/18` before generation. Store at `0x14079ff60` precedes exclusive unlock at `0x14079ffa5`. The hit skips generation and append. Insertion is native-required and lacks a separate record. QPC intervals cannot distinguish pre-admission delay from lock waiting. |
| Fences and firstness | Both reset triads and all 111 Grid-clear pairs yield 224 increments. Reset end 883 is epoch 113. The 47 intervening Grid calls add 94 increments before first provider entry 2470 in epoch 207. There is no epoch-207 reset triad. Grid clear is a removal-only native premise and its receiver is a Grid. The carried-empty interpretation depends on that ordinary mutation graph. The earlier eligible decision 8006 independently defeats constructing-first attribution even under that interpretation. |
| Remaining history | 390 target bypasses follow the store in native time. The projected lifetime checks flag 56 late other-source bypasses whose births cannot certify the decision epoch. They do not disappear from the census. Original reader and projection agree on those sequences. Exact callback return and acquisition timestamps, uninstrumented callers, cold-first, retail frequency and complete geometry remain unproved. |

## Omission screen and trust boundary

For sequence `s`, the original frame offset is `328 × (s − 1)`. The payload
starts 16 bytes later. No original frame was excluded. The allowlist omits
unneeded payload fields, opaque descriptor/source bytes, padding, raw process
and runtime identifiers, private receipt contents and archive members. The
[schema](b2-schema.md) maps the per-kind retention rules. All births and
publications remain visible, including the seven historical repeats. All
selected/visited rows, lookups, entries, returns, append boundaries, Ready
and fence rows are available to test unknowns, competitors and replacement.
Birth-derived equality aliases preserve collisions without publishing
unrelated geographic operands. Descriptive intervals exclude observed
invalidations within the stated recorded history. Absence of uninstrumented
writers depends on the historical ordinary native contract.

The standalone reader recalculates joins and chronology from the projected
operands. An exact package hash checks identity against the published digest.
It cannot authenticate original CRCs, loss telemetry, discarded fields,
alias assignments or original-to-projected fidelity without the private
input. It also does not re-evaluate native instructions or prove the
historical instrumentation's coverage. [Original source and static premises](../../experiments/resource-retained-population/d5ac-sources.md) ·
[Conservative predicate](../../experiments/resource-retained-population/d5ac-cold-certificate-audit.md)

## Local original-to-projection checks

Specialist A decoded original bytes by fixed offset without importing the
builder, verifier or historical decoder. It recomputed original stream and
frame integrity, all typed aliases and derived operands, and matched
32,141 rows and 525,369 positional fields to the exact candidate digest.
It also streamed all 85 sealed payloads in the 34,401,743-byte attempt-002
archive, matched the embedded seal and compared all 12 archived session
payloads with the loose session. The archive SHA-256 is
`f472f69b85e37a4715c1d713e91387e80d20d3518fc66a5b42b9709e0e733d88`.
These checks are local. The [independent review record](review.md) separately
accounts for non-implementer checks after both specialists finish.
The local `selected-originals.json` binds 27 checked original/source/tool
identities and disk readings, including the protected Save52 copy and the
retained native windows. This is a selected identity check and does not
revalidate the active save set or launch posture.
