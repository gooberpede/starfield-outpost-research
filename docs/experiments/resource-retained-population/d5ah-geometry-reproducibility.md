# D5AH complete geometry reconstruction controls

**Fresh native hosts reproduce the complete fixed ordinary population. Mask 0
and mask 3 differ despite containing the same resource identities. A successful
outer region append does not guarantee a complete point copy.** These are
controlled offline results, not observed retail reconstruction beneath an outpost.

| Element | Scope |
|---|---|
| Question | D5AH-Q4: complete geometry equality/difference under explicit effective-input and copy-success contracts. |
| Confidence / basis | PROVEN for executed native stages and independently compared finite byte representations; STATIC composition supplies the qualified outer input factorization. |
| Coverage | Starfield 1.16.244.0; Feynman V source `0:37536:20928:0029d20e`, body `0x0005e0de`, BIOM `0x00145440`; three ordered ordinary resources, every represented region and point. |
| Primary receipts | `.local-work/d5ah/geometry01/control.json`, `geometry02/control.json`, `verify04/verification.json`, `copy02/copy.json`; [identity manifest](d5ah-sources.csv). |
| Limit | Supplied seed-cell conversion keys, resource getters and allocator callbacks; native per-cell and competition routines execute, whole generator/scheduler/retail do not. |

## Fixed effective-input contract

The source descriptor anchor is `(37536,20928)`. Native planar source origin
is `(-200,-200)`, clip centre `(300,300,0)` and half extent `(700,700,0)`.
These coordinates are distinct from original query Int2 and saved beacon
position. Preserve the native frame and descriptor orientation rather than
aligning pictures after generation. Each host constructs 144 cells per resource
in native resource/X/Y order, clearing the supplied collections between runs.

Hold owner key, all packed cell keys, effective source footprint/clip, ordered
resource definitions, rarity/DNAM blocks, weights, generation settings,
arithmetic/imports and successful allocation fixed. The query-to-raster step
uses the pinned atlas; the original queries below are supplied labels rather
than an execution of the outer provider. The [D5T factorization](d5t-report.md)
and [D5AF extra-pass exclusion](d5af-geometric-reproducibility.md) retain the
necessary premise: for this fixed main-file component, Special has no eligible
candidate and the Everywhere slot is zero. Equal ordinary masks alone do not
establish equality when other effective inputs or applicable extra passes differ.

## Complete results and independent oracle

| Original query | Raster / ordinary mask | Ionic Liquids / Fluorine / Copper regions | Total points | Result |
|---|---|---|---|---|
| `[4,-1]` | `0x00` / 0 | 2 / 15 / 57 | 193 | Complete population differs from mask 3. |
| `[4,1]` | `0x03` / 3 | 25 / 35 / 18 | 180 | Equal to the other mask-3 query in all represented bytes. |
| `[5,0]` | `0x03` / 3 | 25 / 35 / 18 | 180 | Same complete result in both fresh processes. |

The [native driver](../../../research/resource-retained-population/d5ah_controls.py)
adapts the owned D5AF method by namespace only. The
[independent verifier](../../../research/resource-retained-population/d5ah_verify.py)
compares every ordered resource key, 24-byte represented region header, point
count and ordered 16-byte point. It checks header/resource agreement, finite
coordinates, exact lengths and all cross-process representations; allocation
pointers and spare capacity are excluded. It performs no sorting, deduplication
or tolerance matching. Counts above summarize comparisons; they are not equality
oracles.

The verifier separately packs all expected binary32 points and bounds from
the owned planar model in D5S `geometry.json`, rather than trusting success flags
in the native receipt. It agrees with every resource in all three contrasts and
with both historical D5AG hosts. A single changed point with unchanged counts
is detected as unequal; a truncated point array is rejected. This validates the
comparison method against identity-only/count-only and partial-byte proxies.
The independent model and native methods share input definitions, as required
by the contrast; independence is in the geometric calculation/comparison.

## Actual native copy failures

The [copy control](../../../research/resource-retained-population/d5ah_copy.py)
executes native region append `0x1407ac2f0` and point copy `0x1407ac0d0`
with explicit owned allocator callbacks. Addresses are preferred static VAs,
image base `0x140000000`. Two synthetic points make every byte independently
checkable. Only the supplied source buffer is mutated in the deep-copy control.

| Supplied callback condition | Outer append result | Retained point count | Consequence |
|---|---|---|---|
| Successful allocation/copy | Index 0 | 2 | Exact source bytes copied to a different allocation; later source mutation does not alter them. |
| Outer append failure | `0xffffffff` | 0 | No outer region is admitted. |
| Outer vector preallocated, inner reserve failure | Index 0 | 0 | Outer success with empty geometry. |
| Outer vector preallocated, inner point append fails after first point | Index 0 | 1 | Outer success with partial geometry. |

The native outer function ignores the inner copy return before storing the
resource/header metadata. The controls positively exercise that distinction;
they do not report a retail allocation failure or estimate its likelihood.
Generator return, holder insertion, visited append and successful outer region
append cannot substitute for validating complete surviving geometry.

The first copy attempt failed before native mapping because its retained
`start` module was not on the import path. `.local-work/d5ah/copy01/` retains
the exception and nonzero exit. The correction adds only the task-local module
directory; fresh `copy02` passes. Failed output is not overwritten.

## Reproduction and claim boundary

Use the pinned installed x64 CPython with `-E -B`, authenticate inputs with
`d5ah_baseline.py --inputs NEW.json`, and choose fresh task-local output paths:

```text
d5ah_controls.py .local-work/d5ah/NEW-GEOMETRY .local-work/d5af/geometry-metadata
d5ah_copy.py NEW-COPY
d5ah_verify.py NEW-VERIFY
```

The verifier intentionally names the retained selected pair and `copy02`;
repointing it to a new pair is a documented method revision. Native fixtures
map selected installed PE pages only into disposable Python processes. No game,
debugger, save write or database opening occurs. Both caller-available drive
floors are checked; raw outputs and proprietary metadata remain LOCAL-ONLY.

The results establish a qualified fixed-input reconstruction contract and a
positive non-equivalence control. They do not establish that real independent
retail episodes select equivalent inputs, nor that an existing extractor's
world location remains on the same deposits. GC-25/31 and D5R stay OPEN.
