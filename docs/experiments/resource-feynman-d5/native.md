# D5 construction-mask and descriptor lineage

2026-10-25, Australia/Sydney. [Contract](contract.md), [report](report.md),
[source pins](sources.csv). All addresses are preferred static VAs, image base
`0x140000000`, Starfield.exe 1.16.244.0, SHA-256
`7e9adb1414a8e1b325e5e1f097b9b17b78deb7eebeda37a333351a43a60f9d28`.
Subtract the image base for RVA. Object and stack displacements are byte offsets.
No relocated address, saved identity or historical cache epoch is inferred.

## First construction query

**STATIC: the ordinary mask depends on the caller's first cache-miss query,
not solely on the selected source.** The earliest missing operand is the two
signed integers passed as provider argument RDX, qualified by cache state and
the effective manager descriptor at that invocation. Existing saved geographic
context locates the outpost; it does not record which request first populated
each source. No unique historical query or sampled byte is reconstructed here.

| Stage | Exact evidence | Supported operation |
|---|---|---|
| Caller | `resource-availability-cont-01.tsv`, `0x1407a1a3c` and `0x1407b526a` | Two caller routes supply a fine-cell query to `0x14079f860`. The latter passes its own input Int2 after manager cleanup. A static call graph does not identify the first historical caller. |
| Source versus query | `resource-milestone-b-producers-01.tsv`, `0x14079fa90–0x14079fb1e` | Source-local frame derives from source anchor/delta fields and integer query multiplied by 100, converted to binary32; rounded differences supply later local calculations. BIOM lookup receives source `+0x10`, independently of original query. |
| Visited/cache gate | Same, `0x14079fc37–0x14079fd02` | Visited key is source `+0x68`. A visited hit skips construction. Under the lock, source-pointer cache hit also bypasses new generation; insertion follows a miss. Neither cache identity is a saved Workshop handle. |
| Descriptor choice | Same, `0x14079fe81–0x14079feaf` | Manager mode byte `+0x20 == 3` selects descriptor `+0x1c0`; otherwise `+0xc8`. Original query pointer is restored from provider RBP `+0x2d8`. |
| Fine-cell conversion | `cont-01`, `0x14078d660–0x14078d7a7`; `activated-grid-01.tsv`, `0x14096f5c0–0x14096f935` | Copy the 0x2c-byte descriptor, apply signed remainder and chart/seam conversion to the original Int2. Coarse, subcell and residual coordinates are recomposed with the stitch-setting sum. Binary64 division and arithmetic yield chart coordinates at output `+0x08/+0x10`, chart byte at `+0x00`. |
| Geographic conversion | `surface-projection-14.tsv`, `0x142332410–0x14233256d` | Chart coordinates undergo doubled-coordinate square-root projection, clamping, chart sign changes and atan2. The horizontal magnitude has an explicit binary32 conversion/square root before promotion to binary64. This is not an interchangeable saved XYZ. |
| Generator entry | `producers-01`, `0x14079fec8–0x14079ff18` | Source-relative origin is rounded separately; converted query goes in R8 to `0x14079b520`, source in RCX, origin Int2 in RDX, manager owner in R9D and BIOM on stack. |
| Ordinary sample | `cont-01`, `0x14079b8dd–0x14079b8ed` | Fetch the original geographic query argument, call `0x142339340`, retain AL before resource loops. |
| Chart/raster conversion | `d5-mask01.tsv`, `0x142339340–0x14233942f` | Cosine and trigonometric helper form a vector; `0x1423321f0` converts back to chart coordinates. Charts 2/3 fold to 0/1 with sign changes; select sampler descriptor at sampler `+0x18 + chart*0x30`. |
| Final cell | `d5-raster02.tsv`, `0x1423390f0–0x1423391ce` | Binary64: clamp `0.5+x` and `0.5+y` to [0,1], floor width times X and height times inverted Y, clamp indices to dimensions minus one. Return column + width*row. Raster byte comes through descriptor `+0x20`; AND AL with `0x0f` at `0x142339428`. |
| Admission | `cont-01`, `0x14079bdad–0x14079be20` | Low nibble 8 or less than current rarity uses its inactive multiplier; otherwise 1. The same multiplier reaches the whole resource/cell traversal. Later per-cell queries cannot retroactively choose this mask. |

The pure [final-stage sampler](../../../research/resource-feynman-d5/mask.py)
tests opposite masks, inverted Y, exact boundaries, clamping and asymmetric
dimensions. It deliberately does not implement the whole geographic round trip:
there is no qualified first query to feed it. The research predictor retains
its conservative uniform-neighbourhood gate. Representative neighbour cells in
`inputs-v2.json` demonstrate spatial variability; they are not asserted to be
the historical construction query or a complete reachable-query census.

The new Ghidra exports use the existing owned launcher/exporter with
`-readOnly -noanalysis`. Both exports end with END and their logs have no script
error. Exported instructions and decompilation remain LOCAL-ONLY. No analysis
symbols, comments, types, settings or executable bytes were edited.

## Feynman III first successful alternate

**STATIC and DERIVED: the supported BIOM-key creation route visits
`0x0008ae7b` before `0x00095092`.** It finds the Uranium root descriptor in the
former's BIOM RNAM RSGD `0x000083ea`; that first success terminates traversal.
This is conditional on the same installed-main initialized population as D4E,
not a newly observed historical/live component population.

The [D4C key ancestry](../resource-owner-root/native.md) supplies the ordering
proof: queued creation uses BIOM as the second unsigned key, and native range
iteration is lexicographic. The [D4E initializer](../resource-slot-provenance/native.md)
supplies initialized roots/slots independently of screenshots. The builder
recomputes and checks every component against the frozen D4E projection.

For current BIOM `0x000fd00a`, root `0x000057eb`, effective RSGD `0x000083f0`:

1. `0x14079c540` searches the current effective RSGD, then current BIOM RNAM.
   Neither contains the assigned Uranium-root descriptor.
2. `0x14079c5e0`, instructions `0x14079c642–0x14079c71f`, walks the owner range.
   BIOM `0x0007d722` has root zero and is bypassed. BIOM `0x0008ae7b` has the
   matching root and is eligible.
3. The alternate search reuses the **current** effective-RSGD context, then
   searches the eligible alternate BIOM's ordered RNAM. It does not substitute
   the alternate's own PNDT effective override. Here the repeated effective
   search fails; BIOM-local `0x000083ea` succeeds.
4. DNAM SHA-256 is
   `f54b36484361b425e45c2d0f6fb6abe66940f5eeffd21745b870dcfa83b81757`.
   `0x14079c71f–0x14079c72e` stores the descriptor and returns success. BIOM
   `0x00095092` / RSGD `0x000083dd` is not visited on this modeled successful
   path. Its different descriptor remains a counterfactual, not a fitted choice.
5. If a candidate lacks the root descriptor, traversal continues. Only complete
   alternate failure reaches the first-nonempty current BIOM descriptor fallback
   at `0x14079bb23–0x14079bb73`. Tests discriminate those branches.

The descriptor chooses generation parameters; it does not create the owner-root
candidate array. D4E's map reconstruction and stable small-list rarity sort
remain unchanged. Rarity-6 occurrences, Special, biome Water and atmospheric
admission keep their separate meanings.

`build04/preparation.json` preserves every actually modeled descriptor comparison,
rejection, bypass and selected entry for every represented BIOM. Missing native
component lookup or unresolved form prerequisites remain an acquisition failure;
the analytical initialized-population model does not claim to simulate invalid
native pointers, allocation failures or all alternate creation routes.

The builder preserves D3/D4E's separate `NONZERO_EVERYWHERE` rejection: an
effective-RSGD rarity-6 descriptor with nonzero own-rarity chance remains outside
this finite-vein model. The descriptor refactor initially omitted that guard;
final code audit restored it and added a zero/nonzero synthetic discriminator.
The qualified cohort's corpus bytes remain identical after restoration.
