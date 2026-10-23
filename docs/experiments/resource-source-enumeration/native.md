# Native enumeration and coordinate-frame ledger

All addresses below are preferred static VAs for Starfield 1.16.244.0, image
base `0x140000000`, EXE SHA-256
`7e9adb1414a8e1b325e5e1f097b9b17b78deb7eebeda37a333351a43a60f9d28`.
Object offsets are bytes. [Exact export and method pins](sources.csv).
Existing native exports were read; no Ghidra process or analysis state changed.

| Boundary | Exact local export / source pin | Supported rule and scope |
|---|---|---|
| Surface-pattern selection | `.local-work/recon/exact-beacon-05.tsv`, `FUN_14096e060`; seed setup `0x14096e0a4..0x14096e0c3`, selection/store `0x14096e70d..0x14096e744` | Surface seed plus system/body initializes MT. Native registry at global data handler `+0x1178/+0x1180` supplies style-compatible candidates in its actual iteration order. More than one candidate consumes a draw; one selects index zero. Installed definition-file order is a reconstruction input, not captured registry order. |
| Pattern slot lookup | `.local-work/resource-geometry/native/011.request.tsv`, `0x14096be70..0x14096bef9` | Slot index is X times 16 plus Y. Flags below `0x20`, or disabled block orientation, use raw slots; otherwise whole-footprint remapping applies. Carinae retained coarse flags 8 take the raw route, eliminating orientation as a necessary correction for this source. |
| Pattern remapping | Same export, `0x14096bba0..0x14096be65` | Derives block footprint from raw dimensions, merge and stride; moves complete footprints and preserves underlying slot words. Pattern orientation and per-block flags are separate operands. |
| Base-source construction | `005.request.tsv`, `FUN_140785190`; `006.request.tsv`, `FUN_140784c40` | Manager mode chooses descriptor `+0xc8`, or `+0x1c0` in mode 3. Traverses stride-sized base blocks; nonanchor flags relocate toward an anchor. Invalid block lookup can fall back to global `0x145ea68a0`. Overlay callback is a separate route; neither absence nor completeness is inferred for it. |
| Padding and copied selector ancestry | `011.request.tsv`, `0x1407862b1..0x140786382`; `013.request.tsv`, full `FUN_140982d90` constructor | Callback subtracts twice padding from raw dimensions. Constructor stores SFBK FormID from block `+0x28` into source `+0x00`, local anchor at `+0x10/+0x14`, padding `+0x20/+0x24`, raw dimensions `+0x28/+0x2c`. It copies the geographic descriptor fields at `+0x38..+0x64`; details below. |
| Contributing-source index | `001.request.tsv`, `FUN_140985870`; `003.request.tsv`, `FUN_140985900`, `FUN_140985c50`, `FUN_140986080` | Bounded lookup subtracts native grid origin and checks dimensions. Cell, edge and corner objects retain/enumerate contributors. Resolving owner cells is a bounded analytical coverage method, not a claim that these virtual contributor lists were captured. |
| Provider and cache | `.local-work/recon/resource-milestone-b-producers-01.tsv`, `0x14079f8d6..0x14079f937`, `0x14079fc37..0x14079ffa5` | Provider gets source index via manager `+0x120`; virtual enumeration yields source pointers. Visited test uses source `+0x68`; ProcGen map uses source pointer. Miss inserts and attempts construction under lock; visit marking is not a success or freshness certificate. |
| Generator frame | Same export, `0x14079fe81..0x14079ff18`, `FUN_14078d7b0`; [inherited native ledger](../resource-geometry/native.md) | Origin is 100 times (local anchor minus padding). Source-origin native units enter the packed-cell transform without dividing by 100. Manager owner is the separate CRC suffix; source pointer/ordinal are not seed inputs. |
| Consumer | `.local-work/recon/resource-availability-ui-15.tsv`, `0x1421e09d4..0x1421e0a77`; `resource-availability-ui-16.tsv`, `FUN_1421e0f50` | Scans occupied ProcGen source maps under shared lock; evaluates regions and short-circuits after resource acceptance. Consumed resident maps do not certify an exhaustive historical producer population. |

## Retained source descriptor decoded anew

The C2B independent SRO1 parser reads captures 84, 94 and 115. All three source
prefix hashes equal
`01ab34593269583b7e6d8fc5b95b78135c23f6ef382502ce15cef2a57a8bc654`.
The previous [Phase B audit](../resource-carinae-source-context/phase-b.md)
establishes their same-invocation transfer join and prior geometry equality.
Current decoding is checked against constructor copy assignments, not inferred
solely from matching numeric values.

| Source offset | Constructor input | Current value / domain |
|---|---|---|
| `+0x00` | SFBK object `+0x28` | FormID `0x002493cf`, matching separately retained selector `+0x54` |
| `+0x10/+0x14` | Local callback anchor | (-12, -12), source-grid cells |
| `+0x20/+0x24` | Grid padding | (2, 2), cells |
| `+0x28/+0x2c` | Raw SFBK dimensions | (14, 14), cells |
| `+0x38` | Geographic descriptor `+0x00` | Chart 0 |
| `+0x3c/+0x40` | Descriptor `+0x04/+0x08` | Coarse cell (111, 81) |
| `+0x44/+0x48` | Descriptor `+0x0c` eight-byte pattern slot | SFPT FormID `0x00212e16`; meaningful flag byte 8. Other copied bytes are not promoted as independent flags. |
| `+0x4c/+0x50` | Descriptor `+0x14/+0x18` | Pattern subindices (7, 7) |
| `+0x54/+0x58` | Descriptor `+0x1c` eight-byte block slot | SFBK FormID `0x002493cf`; meaningful flag byte `0xe8` |
| `+0x68` | Constructor-generated visited/cache key | Separate from source-pointer map key and packed vein cell; no epoch inferred |

Coarse/sub/fine arithmetic gives the source geographic fine-cell anchor
(111 times 192 plus 7 times 12, 81 times 192 plus 7 times 12) = (21396, 15636).
The current manager descriptor instead has subindices (8, 8), giving
(21408, 15648). Subtraction agrees with the copied local anchor. Generator
origin (-1400, -1400) uses 100 times (local anchor minus padding); it is neither
that geographic anchor nor the saved site's coordinate.

The runtime source pointer, wrapper and slot ordinal 27 belong to one consumer
invocation. SFBK/SFPT FormIDs describe definitions, not source lifetime; identical
definitions can occur at many geographic anchors. Source identity in the CSVs
therefore combines chart, geographic anchor and SFBK, while pattern is retained
as a separate selection dimension. Feynman candidates can share a source ID
under multiple SFPTs; those pattern/source combinations are not deduplicated into
one native selection claim.

The copied source's nominal words `+0x18/+0x1c` are not used as a fresh runtime
dimension oracle. Nominal dimensions are derived from raw dimensions minus
twice padding, independently through the callback. Runtime state, historical
generation state and installed definition reconstruction remain distinguished.
