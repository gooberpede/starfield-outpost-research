# D5AG lifecycle consistency

**Retention stabilizes an existing population only while its holder and relevant
owner state survive. Rebuilding the same source metadata is a weaker property
than rebuilding identical resource geometry.** A restored PCM seed/content map
constrains preparation, but is not a restored ProcGen point collection.

| Element | Scope |
|---|---|
| Question | D5AG-Q3: continued identity across movement, retirement, reset, load and return. |
| Confidence / basis | STATIC, with inherited executed shift and geometry controls; high confidence in the named conditional paths. Actual return/reconstruction of a complete retail population remains unmeasured. |
| Coverage | Starfield 1.16.244.0 ordinary source/ProcGen graph and protected Save52's previously decoded fields. No new save load or retail action. |
| Evidence | [D5V primary lifecycle map](d5v-lifecycle-consumer-map.md), [D5AD persisted/reconstructed state](d5ad-save-state-matrix.md), authenticated windows in [D5AG sources](d5ag-sources.csv). |
| Limit | No complete before/after retail population with effective source/frame/definitions and lifecycle observations. D5AG-Q3 remains BLOCKED for that empirical part; native conditional conclusions remain usable. |

All native addresses are preferred static VAs, base `0x140000000`; member
offsets are bytes. Pointer identity, source content identity, token equality,
retained collection identity and geometric equality are separate properties.

| Transition | State that can survive | State removed/recomputed | Complete-geometry implication |
|---|---|---|---|
| First cold construction | Source descriptor/content and effective owner/component exist before resource output. | An eligible unvisited pointer-map miss inserts a holder and attempts synchronous generation. | Geometry depends on the successful effective query, weights, seeds, source frame/clip, definitions/order and extra passes. Publication alone does not fix it. |
| Repeated same-session demand | Existing map holder and retained nested collections; density aggregate can bypass the provider. | Visited hit bypasses construction without fetching a holder; a previously unvisited contender can instead hit the map. | Map reuse preserves represented geometry. Visited alone does not establish its existence or completeness. |
| Small movement without shift | Same live owner and source stores, subject to other transitions. | Newly demanded sources can still construct. | No regeneration is required for the existing source by this movement branch. |
| Shift with source still overlapping coverage | Qualifying overlapping source allocations and populations can remain. | Grid slots/origin change; other sources may retire. | Retention is conditional on actual overlap and no independent reset. Shift is not automatic regeneration. |
| Source retirement | Source token can remain in the owner's visited array. Other references may retain copied collections. | `0x140982b70` erases a present source-pointer map entry under ProcGen `+0x40`, releases the source's shared definition/path reference and frees source storage. | A later allocation with equal token can bypass construction despite missing map geometry. This is a compiled state, not an observed missing-deposit bug. |
| Return without broad reset | Content-derived equal token can compare equal even with a new source pointer. | Reappearance reconstructs source metadata; it does not restore the erased map holder. | Distinguish retained geometry from visited suppression. No automatic fresh generation follows from pointer change. |
| World/component change with reset predicate | Persistent definitions, saved selections and outpost/reference data remain separate. | Registered ProcGen clear `0x14079ddf0` frees map holders and visited array; landscape clear releases Grids. | A subsequent successful demand competes anew. Same source metadata does not force the same effective request. |
| Save/load under ordinary full-load graph | Type-3 descriptors/context and type-7 PCM seed/content/placements restore through distinct readers. | Complementary reset branches clear transient ProcGen stores; world/source and queued component state reconstruct. | Saved outpost existence and PCM restoration do not restore old resource point arrays or certify load-time generation. |
| Return after reset/load | Reconstructed inputs may be equivalent when their full contract matches. | New source selection, demand readiness and map arbitration choose construction. | Fixed-input regeneration can reproduce complete geometry; independent retail equivalence needs measured inputs and outputs. |

The primary instructions independently reread for D5AG distinguish retirement
from reset: [V-S030](d5v-sources.csv) lines 4562–4654 erase the map and free the
source without writing ProcGen `+0x48/+0x50`; [V-S021](d5v-sources.csv) lines
1900–2059 clear the map and explicitly free/zero that visited storage at
`0x14079de9e..0x14079deb8`. This is a positive store/lifetime distinction.
D5S's inherited 38-step retirement control retains its raw-source lifetime
counterexample; Grid retention alone cannot certify each selected source.

There is also a positive conditional protection path. Terrain height nodes hold
the same manager reader while their pending-height helper can execute queued
callbacks. A resource invocation nested inside that interval is protected
against another thread's ordinary exclusive context shift until the outer reader
is released. Same-thread preheld exclusive ownership/recursion is a separate
case. This ambient reader does not become a source reference, cannot protect
work after its destruction and is not evidence that B2 actually used this route.
The [terrain map](d5ag-terrain-resource-map.md#preparation-terrain-work-and-conditional-protection)
records the native wait/claim and shift-admission joins. This qualifies the
detached-density gap without silently discarding its independently valid
unprotected continuation.

## What the saved preparation state actually constrains

PCM reader `0x1418b22c0` restores seed `+0x420`, PNDT content map `+0x360` and
world placement map `+0x3e0`. Save52's qualified type-7 frame contains seed
1008349248 and populated content/placement records; the prior complete reader
and installed PNDT joins are in D5AD. D5AG authenticates the primary reader
window but does not claim a new full save decoding or live restoration test.

The relationship to resource preparation is concrete. `0x14079da80` calls
`0x1418aa1c0` at `0x14079db11`, filters returned objects by type, obtains their
definition data and builds 96-byte preparation records with coordinates and IDs.
`0x1407b5bd0` calls that helper at `0x1407b5c78`, then four preparation subpasses
and publishes the resulting request collection at `+0x20` only after claiming
the owning entry. The primary windows are D5AD-SV137 and D5AD-SV146 in
[the authenticated source list](d5ag-sources.csv). This is a real connection
from persisted data to preparation; it cannot be dismissed as unrelated content
management.

Conversely, `0x1418aa1c0` can reuse existing placement state, compare its day
value against current GameDaysPassed/settings, prune/refresh and fill residual
demand. D5AD-SV134's body, including `0x1418aa730`, positively shows that fixed
PCM seed and cell do not by themselves freeze all subsequent preparation state.
The four subpasses' relationship to resource requests is separately traced in
the terrain map. No saved seed is substituted for the later per-cell/resource
CRC seed or for a resource population image.

## Outposts and extractors

The mapped area and point consumers traverse resident collections under shared
ProcGen protection. Natural extractor placement additionally intersects its
point-admitted resources with effective produced-resource definitions. Neither
consumer path calls the resource generator or supplies a source-preservation
pin. Their mappings support conditional admission against resident geometry;
they do not prove outpost-specific retention through reset or regeneration.
See [the exact consumer sites](d5v-lifecycle-consumer-map.md#native-geometry--area-catalogue-and-extractor-decisions).

A placed extractor's saved association, continued production and a later placement
point recheck are different questions. This work establishes no actual gameplay
bug and no guarantee that an existing machine revalidates every later geometry
change. A feedback path from restored extractor identity to canonical source
construction has not been demonstrated. The discriminator must observe the
actual population and transition, rather than infer them from production alone.
