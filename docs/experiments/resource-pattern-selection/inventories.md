# Before and after source and cell coverage

The before state is the preserved C2C inventory: Carinae's five witnessed-pattern
sources with 48 unresolved cells, and Feynman's six conditional regenerated-tree
sources. C2C also preserves the still earlier four-source Carinae freeze and
[its exclusions](../resource-source-enumeration/inventories.md). No earlier file
or classification is overwritten.

| Site | Cell inventory | Source inventory | Scoped result |
|---|---|---|---|
| Carinae | [272 rows](carinae-cells-v1.csv) | [Six identity rows](carinae-sources-v1.csv) | Five prior identities retained; one added through the typed-block rule. All 48 prior resolver failures become valid single-backlink results. No default fallback is taken. |
| Feynman | [484 rows](feynman-cells-v1.csv) | [Nine union rows](feynman-sources-v1.csv) | Three old identities retained, three excluded and three added; six selected sources. The linked SFTR changes coarse cell (130, 169), while all 156 generated path geometries remain equal. |

Every cell row retains old status/source, new status/source, predicted pattern,
initial entry/flags, resolved flags and lookup rule. Empty old source fields are
documented resolver failures, not predicted empty cells. Source identity is
`chart:geographic-X:geographic-Y:SFBK`. Source coordinates are fine-grid cells;
nominal dimensions exclude padding. Pattern/FormID/flag fields use `0x` notation.

Source rows give inclusion/exclusion reasons and masks over the source footprint
plus the inherited conservative four-cell margin. All examined Carinae margins
have ordinary mask 4; Feynman margins have mask 8. These checks qualify the
unchanged installed resource requests used for complete-source generation.
The local validation receipt retains full source-frame and raw-dimension data.

The single added Carinae source is derived at (21384, 15624), SFBK
`0x002493ea`, resolved flags `0x10`. Forty-eight fine cells share initial slot
(6, 7), entry `0x002493e8` / `0x40`, and translated slot (6, 6). A recursive
resolver would continue to another entry and give a different source; the
native single-translation test explicitly rejects that alternative.

Coverage is complete for execution of this bounded interior/raw-pattern resolver
over the two specified halos. It is not completeness of native contributor
lists, edge/corner behavior, overlay sources, seams, cached historical sources,
planetary populations or accepted UI regions. Feynman pattern/source predictions
remain DERIVED/STATIC despite exact native path correspondence. Carinae's
consumed `0:21396:15636:002493cf` remains the separately witnessed source; the
other five predicted sources are not promoted to native observations.
