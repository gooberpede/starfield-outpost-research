# D4E component-slot producer ledger

2026-10-25, Australia/Sydney. [Contract](contract.md), [result](report.md),
[source pins](sources.csv). All instruction addresses are preferred static VAs
for Starfield.exe 1.16.244.0, image base `0x140000000`, SHA-256
`7e9adb1414a8e1b325e5e1f097b9b17b78deb7eebeda37a333351a43a60f9d28`.
Subtract that base for RVAs. These are not relocated runtime addresses.

## Sixth-slot producer

**STATIC:** `FUN_140779760` supplies payload `+0x68` from the first rarity-6
IRES encountered through the component BIOM's own RNAM descriptor lists. It does
not draw a Water resource by name, read its DNAM chance, or use the component's
PNDT RSGD override for this scan. The prior conditional model omitted this field.

| Boundary | Exact instructions | Semantics and domains |
|---|---|---|
| Clear initialized resources | `0x140779af5–0x140779b2e` | R14 is the component payload. Clear payload `+0x50..+0x6b`, including root and all six uint32 slots. Both vector/scalar branches have the same result. |
| Resolve BIOM | `0x140779b32–0x140779b48` | Read payload BIOM FormID at `+0x40`; resolve and require form type `0xa0`. |
| Traverse BIOM references | `0x140779b4e–0x140779b85` | BIOM count/pointer `+0x308/+0x310` supply ordered RSGD pointers. RSGD count/pointer `+0x38/+0x40` supply descriptors of byte stride `0x238`. Serialized BIOM RNAM and RSGD RNAM order supply the independently extracted inputs. |
| Qualify and store | `0x140779b90–0x140779bb8` | Descriptor first pointer is IRES. Compare IRES rarity byte `+0x110` with 6; read its uint32 FormID at `+0x28`; write payload `+0x68` at `0x140779b9f`. Add the identity to shared occupancy separately. |
| First match | `0x140779bbd–0x140779bde` | A nonzero stored word exits both nested searches. No match preserves zero. No chance-field read or RNG call occurs on this scan. |
| Next phase | `0x140779c30–0x140779c86` | Only after the prepass, run per-component Special/Common selection. Its effective-RSGD route is distinct from the sixth-slot BIOM scan. |

`resource-availability-ui-28.tsv` already contained the complete writer. The new
`d4e-slots03.tsv` independently exports its full instructions/decompilation and
the next selection stage. `d4e-descendants04.tsv` exports descendant writes and
the descriptor/fallback helpers. Exports require matching EXE/base headers, END,
and an error-free script log. `d4e-slotrefs01.tsv` is a preserved partial failure:
the final requested address was not a function entry. It has no END and is not
used as a completed producer proof. The corrected containing-function export is
in `d4e-producers02.tsv`.

## All six slots and transformation boundaries

| Slot | Payload / node byte offset | STATIC writer and rule |
|---|---|---|
| 0 | `+0x54 / +0x74` | `0x140778123` clears and `0x1407781f9` conditionally writes at payload `+0x50 + rarity*4`, with rarity 1. |
| 1 | `+0x58 / +0x78` | Same indexed descendant writer, rarity 2. |
| 2 | `+0x5c / +0x7c` | Same indexed descendant writer, rarity 3. |
| 3 | `+0x60 / +0x80` | Same indexed descendant writer, rarity 4. |
| 4 | `+0x64 / +0x84` | `0x140777949–0x140777981`: category-5 selection, shared occupancy guard below eight, nonnull selected IRES and descriptor, then uint32 write at `0x140777971`. This is Special, not a fifth ordinary descendant. |
| 5 | `+0x68 / +0x88` | First BIOM-local rarity-6 prepass writer `0x140779b9f`, above. |

`0x140777a26–0x140777a5d` calls the descendant helper for rarities 1 through 4
in order. Its capacity gate, RNG/chance and child traversal remain the pinned
owned planetary selection model's upstream dependencies. A newly assigned root
is written to payload `+0x50` at `0x1407779fc`. A cache hit copies root and four
descendant words at `0x140777ad1–0x140777aea`; guarded fallback copies the same
five words at `0x140777b7c–0x140777b96`. Neither copy includes Special or
Everywhere. Zero roots, rejected descendant draws and duplicate resource
occurrences therefore have distinct meanings.

**STATIC, serialized versus initialized:** the existing PNDT PPBD loader and
queued-creation exports initialize these resource words to zero, with BIOM,
chance, seed and override inputs. The later selection pass populates resources;
the raw PPBD record is not a serialized six-slot runtime image. Copy constructor
`0x14076e7d9–0x14076e7f2` and assignment
`0x14076e86a–0x14076e886` preserve the initialized root/slot block, including
the sixth word. Existing node-copy evidence places payload at node `+0x20`.
This establishes the inspected definition-initialization route, not a save
serialization schema or post-load authority for every component.

**INSTALLED:** fresh pinned ESM extraction reads PNDT RSCS/PPBD, BIOM RNAM,
ordered RSGD RNAM/DNAM, IRES SNAM/CNAM and record headers. No resource is selected
by an expected label. **DERIVED:** the owned selection model supplies assignments;
the new projection supplies slots and the owner-map evaluator supplies displaced
arrays. BIOM-key sorting follows the existing queued-creation and unsigned
container-order instructions in the [D4C ledger](../resource-owner-root/native.md).
This remains conditional on that creation route and main-file input state.

**RUNTIME-WITNESS:** only after the D4E freeze, original D4D captures 358–374
qualify the eight visits, slot words, map/staging boundaries and calls. All 48
uint32 slot identities and all eight second keys match. The runtime-registered
type `0x00d2` is witnessed, not an installed-data prediction. Observed first keys
are `0x0005de4c000100d2`; owner, type registration and container flags are distinct
operands. The comparator checks the existing guarded chain but makes no new
whole-session durability claim. D4D's full-session audit remains its own evidence.

The same general slot rule predicts seven nonzero sixth words and component 6's
zero. The writer explains the initialized representation without proving which
historical initialization event produced a later consumed cache. No new live
experiment is necessary to close this scoped discrepancy. Effective overrides,
alternate creation routes, atmosphere occupancy differences and historical epochs
remain separate limitations of wider reconstruction.

## Bounded rarity-tie refinement

The inherited `resource-availability-ui-29.tsv` contains the complete native sort.
At `0x1407af4a9`, a pointer-span size no greater than `0x100` bytes branches to
`0x1407af569`, bypassing partition/heap paths. For at most 32 resolved pointers,
`0x1407af590–0x1407af597` and `0x1407af72e–0x1407af75d` move an entry only
when its rarity is strictly greater than a predecessor's. Equal rarities retain
encounter order. This source-backed stable insertion rule resolves the small
different-identity tie exposed by the full Save52 regression. It does not infer
stable behavior for larger lists. The original D4E target freeze already has
no different-identity tie; its prediction remains unchanged. The separate local
`candidate-freeze-v2.json` retains this general ordering refinement before the
second corpus's geometry predictions are computed.
