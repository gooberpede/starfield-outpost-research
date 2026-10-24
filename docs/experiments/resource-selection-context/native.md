# Native producer and operand contract

[Report](report.md), [exact source pins](sources.csv). Existing read-only Ghidra
exports were inspected; no Ghidra process or database mutation was needed.
All addresses below are preferred static VAs for Starfield 1.16.244.0, EXE
SHA-256 `7e9adb1414a8e1b325e5e1f097b9b17b78deb7eebeda37a333351a43a60f9d28`.
Preferred image base is `0x140000000`. Subtract it for RVA; add the measured
runtime module base for runtime VA. Members and stack displacements are bytes.

| Stop / source | Captured operand and lifetime |
|---|---|
| `0x14079f860`, producers-01 | Provider entry RSP P; record a fresh thread-local provider token and original query, clear pending observations and reset the BIOM stage. The BIOM-selection working RSP must be P−`0x3c8`; generator entry E must be P−`0x3d0`. Cached/no-generation returns cannot lend pending observations to the next observed provider entry. |
| `0x14079fb1b`, producers-01 instructions `0x14079fa90..0x14079fb1e` | Before MOV R15,RAX: RAX is the BIOM returned by source-anchor lookup `0x14078ee90`. Source pointer is `[RSP+0x38]`; original query pointer is `[RBP+0x2d8]`. Copy source `0x70`, BIOM prefix and two signed query integers. Preserve associated-file provenance separately from numeric FormID. |
| `0x14079feaf`, producers-01 | Before conversion call `0x14078d660`: R9 is the same original query; R8 is manager descriptor `+0xc8` or `+0x1c0`. Copy 8 query bytes and `0x2c` descriptor bytes. Require provider RSP and query pointer equality with the preceding BIOM observation. |
| `0x14079b520`, cont-01 and producers-01 | Entry RSP E; RCX source, RDX integer source origin, R8 converted geographic query, R9D owner, `[E+0x28]` BIOM and `[E+0x30]` output map. Return must be relocated `0x14079ff1d`; provider working RSP must equal E+8 (provider entry P is E+`0x3d0`) and source/BIOM must equal the observed upstream selection. Retain upstream capture numbers. |
| `0x14079b6a5`, cont-01, producers-01 `0x140771f30` | Working frame F=E−`0x2d8`; AL is component lookup success. Copy F+`0xe0`, length `0x68`. Producer uses owner/type range and BIOM comparison, then copy `0x14076e810`; payload +`0x50` supplies the assigned ordinary family key. |
| `0x14079b8e8` and `0x14079b8ed`, cont-01 | Before/after ordinary sampler call `0x142339340`: capture its actual RDX geographic-position operand (`0x18` bytes), RCX sampler pointer and returned AL. This is the ordinary sampled return byte, not an observed full underlying raster byte or a Special high-nibble sample. |
| `0x14079c642`, cont-11 | Each actually visited alternate candidate: RBX iterator (`0x38`), RDI lookup context (`0x28`); node=`[RBX+0x18]`, index=`[RBX+0x20]`, record=node+u16(node+index×4+`0x12`). Record BIOM +`0x60`, family +`0x70`. Current BIOM exclusion and family equality are labelled derived static predicates. |
| `0x14079c674`, cont-11 | Eligible candidate's resolved BIOM is RAX after `0x1405de3b0`. Copy BIOM through +`0x318`, ordered RNAM array and each RSGD header/ordered entry array, including current effective RSGD. These are snapshots of candidates before descriptor search, not a branch trace of every comparison. |
| `0x14079be20`, cont-01 / ui-29 | Ordinary resource CALL: RDX IRES, R8 chosen DNAM, XMM3 low word effective multiplier, DIL mask; F+`0x58` assigned family, F+`0x80` effective RSGD, F+`0x68` DNAM. Copy complete `0x238`-stride candidate entries, selected 560-byte DNAM, ordered resource pointers/prefixes, current BIOM RNAM, six setting payloads and actual order slot/ordinal. |
| `0x14079ff1d`, producers-01 | Require RSP=E+8; copy source and output prefix before visited append. This is a witnessed synchronous return, including possible early exits, not successful source population or accepted region transfer. |

The alternate routine has one push and `0x60` allocation in addition to the CALL:
candidate RSP +`0x70` equals F. This is distinct from the cell-frame relationships
in C1G; D4 does not arm the cell chance breakpoint. Its fixed sites are generation
entry and ordinary CALL; DR2 rotates through the seven selection stages. DR3 watches provider entry outside generation and
the provider continuation during generation. Pending and generation records must
share the observed provider token; unexpected exceptions invalidate pending state.
A skipped/early-return/nested stage cannot be supplied from
another thread or an earlier invocation. Stage bits, read validity and upstream
binding are separate from raw-copy completeness.

The original query is an integer fine-cell XY passed to the provider, with 100
native units per fine cell. Producers-01 multiplies it by 100 while deriving the
source-local origin/frame. `0x14078d660` consumes that XY with the selected manager
descriptor and emits chart/angular geographic bytes; D4 preserves the bytes
without pretending they are saved world XYZ. Source anchor, source origin,
manager descriptor, converted geographic query and later per-cell XY are separate
operands. Exact current world-to-saved-frame equivalence is still unobserved.

Descriptor precedence follows cont-11 `0x14079c540`: effective component RSGD,
then ordered current BIOM RNAM, matching root IRES pointers. Alternate lookup
`0x14079c5e0` visits native owner-range order, excludes current BIOM and checks
assigned family. Its first successful descriptor terminates the search.
Cont-01 `0x14079bb23..0x14079bb73` then supplies the first-descriptor fallback
if alternate lookup fails. D4 observes visited ordering and the selected final
DNAM; unvisited candidates remain UNKNOWN. A complete winner explanation requires
matching these snapshots and the final pointer within that witnessed invocation.

Entry manager owner equality is qualified numerically against captured manager
+`0x80`; file-associated identities are retained separately. No permanent source
ID, source ABA exclusion, initialization epoch or historical cache identity is
inferred. Save52's saved Workshop bytes and beacon token cannot identify a native
pointer. Existing consumer captures elsewhere bind Workshop → updater → accepted
region → transfer, but they do not complete the Archimedes producer edge.
