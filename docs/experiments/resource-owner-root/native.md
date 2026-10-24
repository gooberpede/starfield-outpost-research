# Native semantics and provenance

All addresses are preferred static VAs for Starfield.exe 1.16.244.0, image base `0x140000000`, SHA-256 `7e9adb1414a8e1b325e5e1f097b9b17b78deb7eebeda37a333351a43a60f9d28`. RVA equals VA minus that base. Node, payload, map and stack offsets below are byte offsets in different named objects. No runtime address is inferred. [Pins](sources.csv) identify every excerpt/export; raw instructions/decompilation remain local-only.

| Operation | Instruction evidence | Supported semantics |
|---|---|---|
| Owner/store entry | `cont-11`, `0x1407bc31d–0x1407bc36f` | Global context `+0x8b0`, store `+0x238`, retained reader context, explicit owner argument and caller-owned output map reach `0x1407bc3d0`. |
| Range construction | `d4c-range01`, `0x1405f7a8d–0x1405f7aec` | First key word is `(uint64(owner)<<32) OR uint16(type word at 0x1461dfa4c) OR 0x10000`. Second key bounds are zero through `0xffffffffffff`. Type word is runtime-registered; its zero static bytes are not its live value. |
| Native order | `d4c-range01`, `0x1405f7b33–0x1405f7b6d`, `0x1403a4250–0x1403a42cf` | Unsigned lexicographic key comparison at node `+0x10/+0x18`, lower-bound initialization and successive page/slot traversal. Node address = page + uint16 at page `+0x12 + ordinal*4`. Native container order is not PNDT authoring or shuffle order. |
| Creation-key ancestry | `d4c-writers01`, `0x140773194–0x140773204` and `0x140773bf4–0x140773c64`; `d4c-initialization01`, `0x14234101e–0x14234103a` | Queued creation copies owner/type as first key and uint32 third argument as second key. Postprocessor passes payload BIOM at `+0x40` as that third argument. This supports BIOM-key order for this route, conditional on actual population/creation provenance. |
| Payload relation | `resource-milestone-b-producers-01`, `0x140771fa2–0x14077200d`; `d4c-producerrefs01`, `0x14076e73d–0x14076e7f2` | Payload starts at node `+0x20`. Node BIOM `+0x60` corresponds to payload `+0x40`; node root `+0x70` to payload `+0x50`; six words `+0x74..+0x88` to payload `+0x54..+0x68`. Copy preserves them; it does not explain their producer. |
| Staging initialization | `d4b-owner-map01`, `0x1407bc3f2–0x1407bc404` | One array initialized before the range loop. No per-record reset. Logical header is count/capacity/pointer at stack `+0x20/+0x24/+0x28`. |
| Append order | Same, `0x1407bc480–0x1407bc666` | Test six uint32 words in ascending field offset; nonzero words request append and are written on success. No identity/rarity filter or deduplication here. |
| Append refusal | `d4c-range01`, `0x1422cc0d0–0x1422cc150`; six caller checks | If capacity suffices, increment count and return old index. Otherwise allocate/grow; false returns `0xffffffff`, caller skips that write and continues. No guaranteed successful allocation is claimed. |
| Key/create/exchange | `d4b-owner-map01`, `0x1407bc669–0x1407bc6fa`; `d4c-range01`, `0x1405ed1b0` | Nonzero root looks up/inserts a map entry, initializes a new array empty, then exchanges count, pointer and capacity. Existing destination contents become staging for the next record. Zero root leaves staging alone. |
| Cleanup | `d4b-owner-map01`, `0x1407bc745–0x1407bc9eb` | After range end, remaining staging allocation is released through allocator-specific branches. It is not appended to every root or merged back. Capacity management is not modeled by the logical evaluator. |
| Selected-root lookup | `cont-01`, `0x14079b947–0x14079ba11`, `0x14079bb8e–0x14079bd17` | Resolve assigned root, type check `0x9f`, append root pointer; find exact root map key and append each resolving type-`0x9f` supplemental FormID in array order. Missing map key exits the ordinary path. |
| Descriptor alternatives | `cont-11` / `d4c-alternates01`, `0x14079c540`, `0x14079c5e0`; `cont-01`, `0x14079ba15–0x14079bb75` | Current component RSGD, current BIOM descriptors, then other same-root components; first successful alternate wins, otherwise first nonempty current BIOM descriptor fallback. These choices supply DNAM, not new resource candidates. |
| Sort and weights | `ui-29`, `0x1407af57f–0x1407af76c`; `cont-01`, `0x14079bd3f–0x14079be20` | Descending rarity after map lookup; no deduplication. Ordinary low mask controls inactive multiplier. Everywhere rarity 6 takes zero weight on the sampled inactive branch; Special has a separate later path. Distinct equal-rarity order is not generalized by the evaluator. |

`cont-*` and `ui-29` are the existing `resource-availability-*` exports. New `d4c-*` exports reside in `.local-work/workshop-population-rework/specialist/`. Ghidra 12.1.2 with the existing JDK 21 launcher ran only `-readOnly -noanalysis` and the owned `ReadSpecialist.java`; no bytes, symbols, types, comments or analysis settings were changed. Cache/log writes are separate from analysis content. Export completion requires its `END` marker, pinned executable/base and a log without script error. `d4c-creationrefs01` is a preserved partial failure at a nonexistent function entry, not a successful full export.

## Logical transition table

Authored numeric examples below are synthetic identifiers, not game FormIDs. They discriminate models rather than merely restating implementation code.

| Input in order | Map after completion | Final discarded staging | Discriminator |
|---|---|---|---|
| Root 10 / slots [11]; root 10 / [12]; root 20 / [21] | 10 → [12]; 20 → [11,21] | [] | Displaced array crosses root boundaries. |
| Root 0 / [11,11]; root 10 / [12] | 10 → [11,11,12] | [] | Zero root retains staging; duplicates survive. |
| Root 10 / [11]; root 10 / [] | 10 → [] | [11] | Empty replacement does not retain the old value. |
| Five zero-root records each with six copies of 11; then root 10 / [] | 10 → 30 copies of 11 | [] | No same-resource occurrence cap in this logical path. |

Allocation-failure injection is an explicit synthetic input, not a resource fallback. The evaluator does not model heap corruption, map-insertion allocation failure, native sort ties between different identities or arbitrary native ABI objects. Its contract is successful-map-storage logical contents plus individually refused appends.

The earliest supported D3 divergence is its projection of `family.emitted_form_ids`, before the native supplemental append at `0x14079bc50`. Source lookup, descriptor selection, geometry and later competition cannot insert an absent predictor candidate. The [conditional trace](candidate-trace.md) tests one possible installed assignment-to-slot mapping; it is not the missing native producer evidence.
