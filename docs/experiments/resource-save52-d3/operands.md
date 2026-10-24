# Native operands, corpus amendments and provenance

2026-10-24, Australia/Sydney. Preferred static image base `0x140000000`;
all VAs here apply only to EXE SHA-256
`7e9adb1414a8e1b325e5e1f097b9b17b78deb7eebeda37a333351a43a60f9d28`,
retail 1.16.244.0. RVA = static VA minus that base. No runtime base or pointer
is inferred. [Sources](sources.csv) pin the exact local exports, installed
ESM/PlanetData, Save52, screenshots and owned selection modules.

| Boundary / preferred static VA | Exact primary location and result |
|---|---|
| Source BIOM and construction query | `resource-milestone-b-producers-01.tsv`, full `FUN_14079f860`: `FUN_14078ee90` receives source anchor `source+0x10`; `FUN_14078d660` receives the triggering query `param_2`, converts it to geographic coordinates, then calls `FUN_14079b520`. These two geographic positions are not interchangeable. |
| BIOM map lookup, `0x14078ee90` | `resource-availability-ui-34.tsv`, full function: manager map and converted chart coordinates select a FormID, resolved with type `0xa0`. This supports the installed-map/source-anchor route, not historical effective-map identity. |
| Per-biome component, `0x140771f30` | `resource-availability-cont-05.tsv`: keyed owner and BIOM, compare stored component `+0x40`, copy through `0x14076e810`. That copy preserves scalars at `+0x40..+0x4c`, qwords `+0x50/+0x58/+0x60` and final scalar `+0x68`. |
| Ordinary selected root | `resource-availability-cont-01.tsv`, `FUN_14079b520` full decompilation, `local_1a8` low uint: resolved IRES enters the family map from `0x1407bc300`; descendants are appended and rarity-sorted. This is the consumer-defined family key. Native component `+0x70` in the container corresponds to copied payload `+0x50`, rather than a different rarity mask or saved FormID namespace. |
| Descriptor precedence, `0x14079c540` | `resource-availability-cont-11.tsv`, complete instructions/decompilation: effective component RSGD first, then current BIOM `+0x308` count / `+0x310` ordered RSGD pointers. Entry stride `0x238`, descriptor at entry `+0x08`; match the root IRES pointer. |
| Alternate components, `0x14079c5e0` | Same export: iterate the owner's component range; exclude current BIOM at container-record `+0x60`, compare root at `+0x70`; search current RSGD then alternate BIOM RNAM. First successful descriptor wins. Native traversal order is not planetary shuffle order. |
| Final ordinary fallback | `cont-01`, instructions `0x14079bb23..0x14079bb73`: after alternate lookup fails, first nonempty current BIOM RSGD contributes its first descriptor, even if that descriptor's resource differs from the assigned family root. No fallback to arbitrary geometry operands. |
| Ordinary mask | `cont-01`, `FUN_142339340` called before resource traversal; `0x14079bdad..0x14079be20`: low nibble 8 or low nibble below resource rarity selects the inactive setting. Otherwise multiplier 1. One multiplier applies to the complete source/resource X/Y loop. |
| Special | `cont-01`, full continuation at label `0x14079bf06`: selected Special IRES searches effective/current BIOM descriptors, converts the same construction query, then tests the raw map byte's high nibble. Nonzero → 1; zero → Special inactive setting. Calls `0x14079c470` after ordinary resources, preserving predecessor regions. |
| BIOM RNAM representation | `resource-availability-ui-35.tsv`, `0x1409df850`, RNAM case `0x4d414e52`: append reference at object `+0x308/+0x310`; `0x1409e1640` resolves it. Main installed selection adapter currently permits one RNAM per BIOM; ambiguous multiplicity remains rejected upstream. |
| Component lookup ordering boundary | `cont-05`, full `0x1405f7a80`: builds a bounded owner/type-key range and performs native container lower-bound/iteration. D3 does not invent the remaining component-key ordering for the distinct Feynman III descriptors. |

The payload's assigned-family key is projected from the maintained planetary
reproducer's `common_assignment.family`, including guard fallback. Native
consumer/copy evidence establishes the compared key's role. The equivalence
between those projected initialized components and actual loaded components is
still an explicit conditional model assumption. No new component writer,
byte-stream schema, loaded override map or historical component sequence was
captured. The owned module revision/pins and prior qualifications are in
[D1 provenance](../resource-standalone/sources.csv) and the current source ledger;
no sibling catalogue CSV or new third-party implementation was used.

## Versioned schema and algorithm

`predictor_d3.py` uses corpus schema `sor-d3-corpus/1` and response schema
`sor-d3-response/1`; the geographic request schema remains `sor-d1-request/1`.
The original files, schemas, copied bundles and blind outputs remain unchanged.
The new predictor is an adaptation of the committed D1 predictor; the new
builder adapts committed D2 extraction. Final delivery hashes identify new code;
the original model hashes remain in the frozen baseline/source manifests.

Changes to the retained corpus are limited to full raw mask bytes in tile slot
3 (0–255 rather than low nibble only), assigned-family descriptor projection,
and an optional final resource row with `branch: special`, rarity 5 and its own
eight-float generation block. Qualified projections use status
`ORDINARY_AND_SPECIAL`. Order, block references and Special rarity are validated.
Missing operands retain explicit failure states; neither a missing family nor
an unknown descriptor becomes an empty resource set.

At inference, ordinary masks are the low nibble over the established conservative
source neighborhood. They must be uniform for the current implementation. A
Special pass additionally requires invariant high-nibble zero/nonzero state.
Mixed state does not supply the historical first construction query. The model
conservatively omits that source; other supported source positives survive.
It does not average masks or independently vary masks between resource cells.

The six installed inactive settings and unchanged ordinary generator remain
those documented in [C1G](../resource-selection-operands/native.md). Special uses
its own rarity-5 block at serialized DNAM byte offset `40*(5+7)`, then the same
cell generator. Everywhere omission still requires a zero own-rarity cell
chance at byte offset `40*13+28`. No nonzero Everywhere implementation is claimed.

`build-v6/normalized.json` is 738,975 bytes across 16 bodies/204 tile projections;
its SHA-256 is
`d6fe11c89656f5a928d30e49e99e1ad7fb18dedbedad65ba8b4ef3f626a3ee12`.
The raw payload remains ignored. Final inference uses a byte-identical copy in
`revision06/build-v1/`; that directory name is an adapter convention, not D1
schema or scientific version. Exact code copies and input freeze are local.

## Exact unresolved descriptor operands

Feynman III current BIOM `0x000fd00a` has assigned Uranium root `0x000057eb`.
Its two qualified alternate candidates differ:

| Alternate BIOM / RSGD | Original ESM record-header file offset, decimal | Full 560-byte DNAM SHA-256 |
|---|---:|---|
| `0x0008ae7b` / `0x000083ea` | 1307821688 | `f54b36484361b425e45c2d0f6fb6abe66940f5eeffd21745b870dcfa83b81757` |
| `0x00095092` / `0x000083dd` | 1307812746 | `2d36af577ee5912fadb336f021b2c996b35192ca2ac9178f922db0568af2ec3d` |

Neither descriptor was selected through outcome comparison. Inspecting the
actual selected DNAM at the ordinary CALL would falsifiably distinguish them;
an unmatched third descriptor would instead reject this finite candidate model.
The full local `descriptor-ledger.json` retains other biome assignments,
successful routes and original header metadata.

Water's UI/harvester route is separate: [native availability](../resource-availability/native.md)
describes the selected-BIOM Water contribution and atmosphere collection.
Property presence, not numeric positivity, selects the harvester collection.
The screenshot's terrestrial and atmospheric labels do not supply current
ATMO/component identities or convert Water into an ordinary geometric control.
