# D5AT table schema

These derived tables are REVIEW-REQUIRED and keyed to the [survey](../d5at-report.md).
The source key combines the body FormID, chart, two geographic fine-grid
coordinates and SFBK FormID. Saved IDs, runtime allocations and geographic IDs
occupy separate domains.

| File | Key | Fields |
| --- | --- | --- |
| outposts.csv | outpost | Save-side reference token, decoded stream byte offset, label, state, body, frame, parent, Workshop identifier, registration and local/site coordinates. |
| outpost-source-joins.csv | outpost, source_id, qualification, related_saved_identity | Modeled association, qualified research-disk result, resident observation or unresolved historical Hab ownership, with provenance. |
| request-masks.csv | source_id, x, y | Contract, original coordinate or modeled offset, sampled atlas face/column/row, byte and low nibble, sample class and unresolved reason. |
| source-distributions.csv | source_id | Installed selection inputs, source dimensions and descriptor, counts/shares by mask, cohort size, prior witness IDs, coverage and balance statistics. |
| candidate-ranking.csv | outpost, source_id, qualification, related_saved_identity | Insertion-support summary plus join qualification, ranking and unresolved placeholders. |
| unresolved.csv | outpost, source_id, reason, related_saved_identity | Remaining input or coverage gaps and affected count where known. |
| grid-registration.csv | outpost, source_id | Exact installed-main comparison, scenario descriptor anchor, and separate retained Grid, density and layer counts and mask histograms under `D5AT-GRID-PREWARM-0`. |
| activation-requests.csv | outpost, source, trigger, x, y | Retained Grid pairs under `D5AT-SAVED-ANGLE-PREWARM`, with original signed XY, decimal mask, hexadecimal packed coordinate word and density/layer candidacy. Trigger is `both` when manager and focus bounds agree, otherwise each preparation window has its own rows. |
| activation-distributions.csv | family, outpost, source, trigger | Rank within the density or layer family, inclusive window bounds, retained Grid and family candidate counts, mask shares, balance and qualification. Actual completion is unknown. |
| mask-grids.json | source_id | First X and Y, plus ascending-Y mask rows. Each character is one hexadecimal mask or `?`. |

Atlas coordinates are zero-based. Counts use decimal. Shares range from zero
to one. The modeled source dimensions and anchor are in fine cells. Local
XYZ values are native-frame units. Descriptor is the chart followed by coarse,
sub and fine XY pairs. `UNKNOWN` marks missing or unqualified fields.
Ranking uses all observed mask classes and preserves unranked coverage rows.
