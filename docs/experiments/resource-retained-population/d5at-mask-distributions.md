# D5AT source distributions

The [fixed Grid registration trace](d5at-grid-trace.md) is a separate input
contract. Its [table](d5at/grid-registration.csv) separates source support,
density and layer registrations. VI-b's leading split is unchanged within
this scenario. Twenty density cohorts are narrower than the corresponding
support, so the original ranking continues to label its fractions by domain.

The [saved-angle replay](d5at-activation-trace.md) uses saved site inputs to derive conditional manager and focus cells for 17 sites. VI-b has 108/46 density and 96/44 layer candidates at masks `0x0`/`0x8`, leading both family rankings. U20 retains 28/168 in both families. The [activation rows](d5at/activation-requests.csv) cover all 77 installed matches and preserve separate windows for the one site with different manager and focus cells. The [family distributions](d5at/activation-distributions.csv) record counts, shares and balance for each window. These cohorts are conditional on ordinary Grid selection and successful cold preparation in the named window.

The modeled census contains 142 source keys on 16 bodies, with 133 single-mask
and nine two-mask sources. The 130 smaller domains contain 196 coordinates
each. The 12 larger domains contain 676 each. All 33,592 coordinates have
an atlas result within their own contract. This leaves 141 source-level
uncertainties about the actual native cohort and effective descriptor.

| Source-at-outpost | Counts | Contract |
| --- | --- | --- |
| VI-b `D2-81bf2a`, source `0:29568:10944:0006ce56` | 144 mask 0, 52 mask 8 | Modeled insertion attempts |
| VIII-b `D2-844cc6`, five candidate keys | 28 mask 0, 168 mask 3 each | Modeled insertion attempts, with competing selections |
| V Cu IL F `D2-84e101`, two other keys | 28 mask 0, 168 mask 3 each | Modeled insertion attempts |
| V Cu IL F `D2-84e101`, source `0:37536:20928:0029d20e` | 28 mask 0, 168 mask 3 | Authenticated D5AQ-C1 coordinates under fixed inputs |

For D5AQ-C1, the exact N2 cohort supplies all coordinates. One row at
`(-2,11)` is the direct N2 mask sample. The other 195 samples under C1 and
the 33,396 insertion-attempt rows are conditional. For
`D5AT-INSERTION-ATTEMPT`, width and height come from each source block and
the owned D5H pad-two insertion model. The explicitly hypothesized descriptor
starts at the source anchor with zero fine phase. A change in owner, effective
descriptor, dimensions, atlas, chart or completed request preparation can
change the result. The source-specific raster is the authenticated installed
PlanetData member for that body.
Five exact keys also match the lower and interior witness queries in
[D5I QS1](../resource-query-variability/proofs.md). These are source-specific
conditional successful-miss witnesses. Their broader request cohorts remain open.

The arithmetic crosses both D5AQ projection branches with the independent
rationalized sampler, comparing face, column, row and byte. A third check
uses direct interior integer pixel indexing. The archived 392 native results
agree at all C1 coordinates. Face crossings and unsupported charts are refused.
The completed survey contains both charts and does not need to extrapolate
across a face. A one-cell descriptor phase change in C1 changes 14 mask results.

The [full counts](d5at/source-distributions.csv), [coordinate CSV](d5at/request-masks.csv)
and [mask grids](d5at/mask-grids.json) preserve each source separately.
Grid strings advance in increasing X and the list advances in increasing Y.
The [ranking](d5at/candidate-ranking.csv) puts complete two-class rows first,
ordered by smaller largest-class share. It then sorts higher class counts by
effective classes, followed by single-class rows and unranked placeholders.
Ties use outpost and source ID. Effective classes are two raised to the Shannon
entropy in bits over all sampled classes. It uses the full distribution
without renormalizing only the two largest classes. No associated modeled
distribution had three or more masks. The out-of-association D5U
U26 control reproduced 24 mask-0, four mask-1 and 168 mask-3 samples, and
three distinct complete geometry outcomes. D5U-C1 assigns it no outpost or
research disk. A synthetic three-class control also retained every class.
