# Versioned before, after and candidate inventories

All source inventories are bounded interpretations, REVIEW-REQUIRED. Original
[v2 freeze](../resource-geometry-mature-context/freeze-mature-v2.json) and
[installed prediction](../resource-installed-settings/predictions-installed-v1.json)
remain unchanged. Full generation requests and raw native selectors stay local.

| Site | Original inventory | Proposed inventory | Uncertainty envelope |
|---|---|---|---|
| Carinae | [before v1](carinae-before-v1.csv): four frozen sources | [after v1](carinae-after-v1.csv): five sources resolved using the retained coarse-pattern witness; 48 unresolved cells remain | [candidates v1](carinae-candidates-v1.csv): 23 identities over five compatible SFPTs |
| Feynman | [before v1](feynman-before-v1.csv): six frozen sources | [after v1](feynman-after-v1.csv): same six, still conditional on initialization selection | [candidates v1](feynman-candidates-v1.csv): 33 pattern/source combinations, 26 source IDs over eleven compatible SFPTs in two coarse cells |

The after rule receives only coarse cell, chart, SFPT and pattern flags from a
constructor-retained witness, then resolves every cell in the unchanged halo.
It accepts no observed local anchor. The candidate rule enumerates all pinned
main-file SFPTs whose style matches the installed BIOM at each halo cell; it receives no
runtime source or geometry input. Coarse rotation is held at the pre-existing
initialization setting for this envelope. It is not an envelope over all possible
surface seeds, rotated patterns, effective plugin registries or native fallbacks.

Carinae's four old identities are excluded from the five-source after set because
the selected pattern changes their blocks and/or anchors; the per-source
exclusions in [results v1](results-v1.json) preserve the reason. They remain
valid frozen model inputs and are not deleted from history. The observed
`0:21396:15636:002493cf` appears in both the independent candidate envelope and
the witnessed after set. Its definition/anchor/padding match the native prefix;
membership of the other four after rows is DERIVED, not separately OBSERVED.

Under SFPT `0x00212e16`, 48 of the 272 fine cells in Carinae's unchanged halo
raise `unqualified source anchor`. They are all retained with exact coordinates
in results v1. The existing helper raises where native code can fall back to a
default block. That unresolved branch and contributor edge/corner semantics
prevent calling the after set complete. No such error occurs in the examined
Feynman compatible-pattern envelope. That finite success does not prove a native
census or absence of overlay, cached or previously generated sources.

CSV coordinates distinguish geographic fine cells, descriptor-local cells and
generator native units. Dimensions are nominal; raw dimensions are nominal plus
twice padding. Flags and definition FormIDs have `0x` prefixes. `in_before` and
`in_after` compare source identities, not pointer/slot ordinals or historical
lifetimes. Every row states inclusion rationale and evidence classification.
