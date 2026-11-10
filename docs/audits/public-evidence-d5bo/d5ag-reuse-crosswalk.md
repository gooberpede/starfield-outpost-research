# D5AG fixed ordinary geometry reuse crosswalk

**The unchanged, previously qualified D5BJ geometry entry point covers the
three D5AG requests.** It recomputes each mask with two original branches,
executes the ordinary per-cell geometry for each query in full, checks the
planar model and D5AS bytes, and compares the complete repeated-mask native
population. D5BO performs offline comparisons of retained evidence. The
supporting native qualification is inherited at its exact component tier.
[D5AG original controls](../../experiments/resource-retained-population/d5ag-geometry-controls.md) ·
[D5BJ qualification](../evidence-reproduction-d5bj/qualification.md)

| Operand / domain | Original and reusable qualification |
| --- | --- |
| Build and inputs | Starfield 1.16.244.0, preferred image base `0x140000000`. D5BO rehashed EXE (102,476,200 bytes) `7e9adb1414a8e1b325e5e1f097b9b17b78deb7eebeda37a333351a43a60f9d28`, ESM (1,457,098,709) `1dabed00c3f4282dd3bb54d2e9601e40b577d8742d078b7ccef203adbfef0da7`, PlanetData BA2 (22,468,821) `2fb1fff5d8fc074718bf05022c099f3c87ef70e00050229b368ae7d680fbe5d5`. D5BJ requires these bytes and a pinned Windows x64 host. These pins identify the main-file fixture. Effective retail overrides require separate evidence. |
| Body, source and hierarchy | Feynman V body `0x0005e0de`, system 86469, body index 5, BIOM `0x00145440`, RSGD `0x00258050`. SFTR `0x00168814` → SFPT `0x0023ddf3` (flags 8) → SFBK `0x0029d20e` (flags 136 and DNAM 14×14). Source `0:37536:20928:0029d20e` has chart 0, coarse (195,109), sub (8,0), fine (0,0), anchor (37536,20928) and C1 fine axis 49152. D5BJ supplies the fixed frame selectors and checks the corresponding main-file records and identities. |
| Raster and request | Exact BA2 member `planetdata/biomemaps/feynman v.biom`, 655,414 bytes, SHA-256 `bd06d24e8ca1788481f6a4388c0e262b863b8b376a521752cf3d286c69f23863`. Version 5, two 256² faces. D5AF/D5AG provide original signed request cases. D5AQ maps independent atlas arithmetic and reachability. D5BJ exercises both native conversion/sampler branches at preferred VAs `0x14078d660`, `0x14096f5c0`, `0x142332410` and `0x142339340`. Recompute below from the fixed source, with no substitution of the anchor for Int2. |
| Frame and clipping | Ordinary per-cell geometry uses origin (−200,−200), centre (300,300,0), half extent (700,700,0) and cells `[1,13)²` in native resource/X/Y order. Origin, seed-cell position, anchor, signed provider Int2 and geographic raster coordinates are separate operands. D5AF, D5AG and D5AQ carry this fixture frame. |
| Effective family | Ionic Liquids, Fluorine and Copper in native order `0x57d4/0x57d0/0x57cf`, rarities 3/1/0. Mask-0 binary32 weights 0.05000000074505806, 0.20000000298023224, 1. Mask-3 weights 1, 1, 1. D5T establishes the bounded factorization. Changing earlier resource weights can affect later retained geometry. |
| DNAM and settings | Copper RSGD DNAM 560 bytes. Rarity row offset `40 × (rarity + 7)` gives 400/320/280, eight definition words plus two supplied zeros. Six effective GMSTs `0x2d40c0/0x226b0c/0x226b0e/0x226b0d/0x2f031c/0x2d40ce` are read and checked from the main ESM. [Geometry loader](../../../research/resource-retained-population/d5bj_geometry.py) |
| Cell key, CRC and seed | Native `0x14078d7b0` produces 144 packed u64 cell keys, checked independently. Geometry folds each little-endian u64 key plus manager `+0x80` owner u32 into reflected CRC `0xedb88320`, initial zero and no final XOR, then uses original MT generation. No derivation from the incoming Int2 alone. |
| Original native stage and ABI | At preferred VA `0x14079a330`, the Windows x64 stage takes pointers to IRES, cell, origin, clip and DNAM, followed by a binary32 weight and an output pointer. Native append/copy `0x1407ac2f0` and competition `0x14079b020` exercise caller-owned collections. D5BJ retains private allocator/getter callbacks, UCRT math imports and writable private RNG state with an exact page allowlist. The harness runs in a fresh disposable process and supplies successful allocation. Separate controls test failed allocation, failed append and deep copy. This scope starts at the ordinary stage and does not execute the whole retail generator. |
| Extra passes | D5AF/D5AQ check initialized Special/Everywhere exclusions for this family, including slots `[0x57d0,0,0x57d4,0,0,0]`. D5BJ checks relevant main-file entries and no PNDT override, then supplies the family. The geometry command does not rerun component initialization. Special may otherwise reuse original Int2 and high bits. D5U's other source (masks 0/1/3 with 69/77/75 regions) and D5AQ different-mask controls bound the claim. |
| Output and independent checks | Every ordered native resource FormID, region header (24 bytes), point count and point (16 bytes). Native same-mask repeat compares the complete population dictionaries, including all header bytes. Planar oracle packs and checks points and bounds, including finite binary32 fields. No region/point sorting, deduplication, rounding or tolerance. |
| D5AS byte domain | Canonical comparison sorts the resource records by FormID as specified by D5AS, retains region and point order within each resource, and encodes the 21 meaningful header bytes, explicit count and all ordered 16-byte points. Header bytes `0x15..0x17` are padding omitted by the canonical encoding. The canonical comparison covers represented geometry and excludes native pointers, spare capacity and padding. The raw same-mask comparison covers padding within the native tier. [D5AS representation](../evidence-access-d5be/d5as.md) |

| Original signed Int2 | Face-0 geographic coordinate | Raster pixel | Native mask | Complete fixed geometry |
| --- | --- | --- | ---: | --- |
| `[4,-1]` | (37540,20927) | (195,147) | 0 | 74 regions / 193 points, 2/15/57 regions by resource |
| `[4,1]` | (37540,20929) | (195,146) | 3 | 78 regions / 180 points, 25/35/18 regions |
| `[5,0]` | (37541,20928) | (195,146) | 3 | Exact full represented native equality to `[4,1]` |

The specialist compared all 18 query populations across D5AF
`geometry08/09`, D5AG `geometry01/02` and D5AQ `geometry01/02`. Corresponding
raw populations agreed, every point and bound was finite, and each complete
normalized body matched the exact D5AS reference bytes. The original
24-byte headers in these receipts had zero padding. Original D5AG
`verify03` primary source locators (14) authenticated. Local receipt
locators remain private. [Original source ledger](../../experiments/resource-retained-population/d5ag-sources.csv) ·
[D5AF geometry](../../experiments/resource-retained-population/d5af-geometric-reproducibility.md) ·
[D5AQ mask method](../../experiments/resource-retained-population/d5aq-mask-method.md)

The unchanged D5BJ geometry and sampler sources hash to
`cdd9f268751bc9e99a7b6f549d3d6f05cb65fd053fee070cb1088fc6b89a97b3` and
`ffb9b40e85d48489b15493fc4db2635c2e9341e7f12813ead3b7c0268db46631`.
The specialist rehashed the five D5BJ entry points and all 30 isolated04
streams. Geometry and fresh repeat each exited zero with the same
996-byte stdout SHA-256
`7c6c0a8c355a701ff9ae0565694a9e5d58778870e26109a773879b332b9269c9`.
The isolated receipt SHA-256 is
`0b5d41d95cd12ecd9c9fe28acc9f057b2cd2445605ff3d1b77b436f772c12900`.
The earlier D5BJ final02 independent reviewer separately reran that
isolated method. Its retained review SHA-256 is
`9a8443e847f5e1b5db1935475c2d2047720fdafa7c03f595f56e46039358cada`.

The geometry component requires the D5AS reference ZIP as supplied input.
It requires no D5BI derivative, integrated initialization, worker or
ContentManager continuation. There is no missing native geometry component
within this selected contract. Access to the exact ZIP, lawful pinned
files and the supported host remains conditional. [Reader](d5ag-reader.md)
