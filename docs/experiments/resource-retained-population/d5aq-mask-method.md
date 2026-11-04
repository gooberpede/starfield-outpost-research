# D5AQ census method and effective-input contract

2026-11-04, Australia/Sydney. **All 196 coordinates have a conditional mask;
none requires a guessed fill.** N2 supplies actual task identities and its one
direct sampled winner. It does not supply 196 successful constructing misses.
The [matrix](d5aq-mask-map.md), [CSV](d5aq-request-mask-map.csv) and
[ledger](d5aq-investigation-ledger.md) preserve that distinction.

## D5AQ-C1: exact scope

| Operand | Qualified value and evidence | Limit |
| --- | --- | --- |
| Build | Installed Starfield 1.16.244.0; EXE SHA-256 `7e9adb1414a8e1b325e5e1f097b9b17b78deb7eebeda37a333351a43a60f9d28`; preferred image base `0x140000000`. | Every native address here is a preferred static VA, not an N2 runtime VA. |
| Source | Feynman V `0x0005e0de`, source `0:37536:20928:0029d20e`, BIOM `0x00145440`, effective main-file RSGD `0x00258050`. | Source key is not a request, pointer or saved identifier. |
| Consumed descriptor | Chart 0; coarse `(195,109)`, sub `(8,0)`, fine `(0,0)`; anchor `(37536,20928)`. N2 core generation 3961 and sample 3962 contain these fields. | Padding, pointers and unrelated descriptor words are not fabricated from the fixture. Only coordinate-consumed fields are compared. |
| Coordinate constants | Base dimension 10 plus stitch 2; master dimension 256, giving 49,152 fine cells per face axis. | Main-file/compiled fixed contract; the 196 counterfactuals require the same qualified inputs, not merely equal source names. |
| Raster | Installed pinned PlanetData ordinary 256 by 256 two-face BIOM map for the body. | Resident valid raster at the selected generation; an absent or failed raster is not assigned a mask. |
| Task cohort | Exactly 196 family-1 density allocations paired with 196 distinct family-2 layer allocations at the same original coordinates. | Allocation IDs are N2 observer identities. Family equality does not imply simultaneous readiness or equal service. |
| Complete ordinary geometry | Fixed source origin `(-200,-200)`, clip center `(300,300,0)`, half extent `(700,700,0)`, 144 cells per resource, effective resource order, keys, owner, DNAM, settings and successful allocation. | These are the D5AG/D5AF stage premises. An ordinary mask alone does not bind them in every retail episode. |

Fresh unmodified [D5AP extraction](../../../research/resource-retained-population/d5ap_analyze.py)
at `.local-work/d5ap/d5aq-auth01/` authenticates the N2 seal/archive, all 174
retained payloads and 484 source pins, then reruns original wire/accounting,
typed-task and source/frame/lifetime readers. The original analyzer refuses an
output under `.local-work/d5aq`; the failed attempt writes no evidence. Its
required fresh D5AP namespace is used instead, with no original replacement.
The prior N2 and D5AP results remain unchanged.

The census independently requires a unique task allocation per family/cell,
all twelve instrumented task stage classes, and exact equality of each family's
coordinate set with `[-2,11]²`. Sorting actual density publication sequences
independently reproduces `(x-y,x)` ascending for every cell. The CSV includes
that rank, each density/layer identity and provider witness. Publication rank
is never used as the map's sampling input or as a construction guarantee.

## Compiled conversion and sampling

The density and layer routes preserve their original signed Int2. Provider
`0x14079f860` passes it through `0x14078d660`, which copies the actual descriptor,
calls `0x14096f5c0` with that Int2, and normalizes the recomposed coordinates.
For C1's interior domain the face cell is `anchor + original Int2`. Native
instructions `0x14078d6e5..0x14078d6f4` copy the two request words; recomposition
and floating arithmetic occupy `0x14078d6f9..0x14078d795`. No source-origin or
canonical query replaces the original request here. Source-origin-plus-cell
conversion `0x14078d7b0` supplies separate generation keys.

The geographic projection `0x142332410` and low-nibble sampler `0x142339340`
convert through the sphere and inverse chart. The sampler's final face table
and pixel index read one byte and apply `& 0xf`; ordinary rarity comparisons
are numeric. The actual raster column and row are persisted per candidate.
The native sine dispatch has separate FMA and non-FMA arithmetic; both are
evaluated, retaining explicit binary32 boundaries. Equal results do not imply
that the host selected both branches during N2.

[Census implementation](../../../research/resource-retained-population/d5aq_census.py)
reuses the owned D5H `roundtrip.py`/`native_sine.py` transcription and bounded
BA2 reader, with their provenance intact. It compares every result against the
new [independent oracle](../../../research/resource-retained-population/d5aq_oracle.py).
That oracle uses Decimal mixed-radix conversion with rounding at each native
binary64 operation, host scalar trigonometry and a rationalized inverse rather
than the primary polynomial or subtractive-root implementation. It compares
the complete atlas cell and sampled byte, not just the low mask.

A separate child replays D5T's original-instruction converter for all 196
coordinates. Its ten function ranges are checked against the installed PE and
pinned historical native hashes before execution. The child explicitly supplies
master/descriptor data, a null definition lookup after interior reconstruction,
and private storage. It does not execute the whole engine, full generator or
retail scheduler. Original local fixture support is copied into fresh scratch;
the original files and native exports are preserved. The fixture callbacks and
patched private import slots are disclosed substitutions, not game changes.

The separate guarded
[native startup/sampler host](../../../research/resource-retained-population/d5aq_startup.py)
then executes original converter → spherical projection → ordinary raster sample
for every coordinate under both original CPU arithmetic paths. Final receipt
`.local-work/d5aq/startup-native05/receipt.json` contains 392 actual native masks,
all agreeing with the separate C1 arithmetic census. It also executes native
projection, quantization, landing snap and center conversion for the initializer
preimage. The authentic atlas is supplied in private native-shaped face buffers;
the CPU dispatch thunk and scalar CRT imports are explicit substitutions. This
closes numerical sampling coverage, without executing the outer generator or
the engine's DB loader, whole initializer or retail scheduler.

## Verification and adverse inputs

`.local-work/d5aq/census04/census.json` retains all 196 detailed comparisons,
input/method identities, native function hashes and both drive floors. Final
`verification03.json` confirms the executed source identities. Earlier attempts
are retained:
`census01` refuses an unrelated unpinned export during an overly broad metadata
copy; `census02` exposes the oracle's initially missing intermediate binary64
rounding. Explicit operation rounding corrects that defect before `census03/04`
pass. Neither failed attempt is a scientific counterexample.

| Control | Actual result | Interpretation |
| --- | --- | --- |
| All 196 converter comparisons | Native chart, face cell and binary64 normalized coordinates agree exactly with the independent conversion. | Conversion is checked for every C1 query. |
| All 196 raster comparisons | Primary FMA and non-FMA branches agree with the independent oracle and retained D5T census at every atlas cell and mask. | 28 mask 0; 168 mask 3; zero unresolved C1 samples. |
| All 392 original native raster samples | Both native arithmetic paths agree with every independently calculated C1 mask. | Compiled conversion/projection/sampler are executed; supplied raster/owner state remains explicit. |
| Authentic D5AG labels `(4,-1)`, `(4,1)`, `(5,0)` | `0,3,3`, respectively, under the D5AG fixed coordinate contract. | These are supplied-stage controls; B2's losing query is not retrospectively sampled. |
| N2 direct winner | `(-2,11)` predicts 3; core 3962 directly records 3 under the consumed descriptor. | One actual retail corroboration; other providers bypass the visited target. |
| Fine Y phase `+1` | 14 mask 0; 182 mask 3; 14 changed cells. | Descriptor phase materially affects the conditional map. |
| Descriptor anchor Y `-192` / `+192` | All 196 mask 0 / all 196 mask 3. | Deliberate input perturbations, not feasible alternate ownership of the same source or ordinary winner forecasts. |
| Missing raster, unqualified chart, incompatible dimension 128 | Explicit refusal, no assigned mask. | Missing or changed owners need their own compatible source/frame/raster contract. |
| Failed append / allocation | Fresh D5S native replay reproduces `0xffffffff` append failure. | An empty/failed population is not substituted for a successful C1 ordinary outcome. Mask and successful output are distinct. |
| Fixed Special / Everywhere applicability | Fresh `extra-inputs01.json` resolves absent Special and no Everywhere entry; component slots end in two zeros. | Applicable extra passes are positively absent for fixed main-file C1, not assumed absent for all loaded components. |
| Complete ordinary stage | Fresh `geometry01/control.json` executes three resources at masks 0/3/3; every point/bound agrees with the independent planar model. | 74 regions / 193 points versus 78 / 180; same-mask complete stage outputs agree under fixed other inputs. |

`verification03.json` additionally compares both independent native geometry
processes (`geometry01/02`) with every retained D5AG population, joins all 392
native masks to the arithmetic census and authored CSV, and checks thirty early
optimization refusals across the ten final D5AQ Python entry points. These
checks do not replace the independent scientific review of startup feasibility.

Special uses the original geographic query again and high bits through its own
sampling branch (`0x14079bf06..0x14079c009`). A changed component enabling that
pass invalidates the complete-output equivalence contract even if `byte & 0xf`
is unchanged. Atmospheric and Water products are separate; the census does not
invent their geometry or infer global full-generator equivalence. The alternate
source in [D5U](d5u-report.md) remains a concrete three-mask counterexample to
a universal two-outcome bound.

## Reproduction and safety

Use pinned installed CPython 3.14.3 at
`C:/Users/User/AppData/Local/Python/pythoncore-3.14-64/python.exe`, SHA-256
`cce21c0e8710e304273e98ac4b2b0f5aceb639acbcd2343cbaa5c4e81619c45b`,
with `-E -B`. New entry points refuse optimization before project/sensitive
imports. Inputs are local and must already exist; no downloads occur.

```powershell
$py = 'C:/Users/User/AppData/Local/Python/pythoncore-3.14-64/python.exe'
& $py -E -B research/resource-retained-population/d5ap_analyze.py --out .local-work/d5ap/NEW-d5aq-auth
$hash = (Get-FileHash .local-work/d5ap/NEW-d5aq-auth/summary.json -Algorithm SHA256).Hash.ToLower()
& $py -E -B research/resource-retained-population/d5aq_census.py --analysis .local-work/d5ap/NEW-d5aq-auth --summary-sha256 $hash --out .local-work/d5aq/NEW-census
& $py -E -B research/resource-retained-population/d5aq_geometry.py .local-work/d5aq/NEW-geometry .local-work/d5af/geometry-metadata
& $py -E -B research/resource-retained-population/d5aq_extra_inputs.py NEW-extra.json
& $py -E -B research/resource-retained-population/d5aq_preserve.py --out .local-work/d5aq/NEW-preservation.json
```

Replace NEW names with unused names. `--publish-derived` additionally writes the
two authored map files; ordinary reruns write scratch only. Existing output
directories refuse replacement. All applicable outputs retain the separate
40,000,000,000-byte caller-available floor on C: and D:. Native faults stop the
disposable method and retain logs. Exiting the child frees its private mappings;
there is no target cleanup or save restoration. Proprietary raster/native/raw
payloads stay local. Authored methods and synthesis are REVIEW-REQUIRED.
