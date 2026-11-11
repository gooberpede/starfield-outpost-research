# Manual observation matrix

2026-10-13. Source: section 2 of the [invoked brief](../../implementation-briefs/README.md#archive-lookup) (`implementation-briefs.zip :: docs/implementation-briefs/CODEX_BRIEF_SOR_ship_relocation_landing_selection_grid_oracle.md`),
two operator-reported sequences, including restart/reload of original Save25.
These are SOURCE-REPORTED gameplay observations, not independently recorded native
traces. They were supplied for this investigation; no new gameplay was performed.
Approximate distances are reported metres; no native-unit conversion is inferred.

| ID | Reported condition/action | Player arrival | Ship observation | What it establishes / does not establish |
|---|---|---|---|---|
| M01 | Save25 at SOR-003, no SFSE | At SOR-003 | At LZ1, original Save3 landing near SOR-002 (~230 m), >2 km from SOR-003 | Initial separation reported; no runtime identity/frame/grid. |
| M02 | Local SOR-002 ↔ SOR-003 travel, often | At chosen outpost | Remains at existing LZ1, or LZ3 after a different arrival | Player and ship destinations can differ observationally; no proof of omitted native route or selection. "Often" is not a frequency estimate. |
| M03 | LZ2 or LZ4 → SOR-003 | At SOR-003 | Relocates to LZ3 (~450 m from SOR-003) | A useful relocating contrast; lookup/reuse/generation are not distinguished. |
| M04 | LZ2 or LZ4 → SOR-002 | At SOR-002 | Relocates to LZ1 | Destination-dependent placement reported; neither closest-marker nor exclusion rule proved. |
| M05 | Travel to separate POI with conventional pad | At POI | Pad remains empty; ship need not move | Conventional pad presence alone does not predict ship movement in this sequence. No constructed-pad retest needed. |
| M06 | First arrival at a new landing area | In front of ship ramp | Ship at landing area | Player-arrival mode differs from repeat travel; no newly allocated marker proof. |
| M07 | Repeat travel to that landing area | Elsewhere near landing area | No separate exact identity observation | Arrival marker/offset/cached context can explain this; branch unknown. |
| M08 | Restart and original Save25 reload; LZ4→003 and LZ4→002 | At chosen outpost | LZ3 and LZ1 respectively reproduced | Strengthens reported reproducibility across restart. Not two independently instrumented native trials. |
| H01 | Player experience: natural landing partly overlapping boundary excluded without suitable built pad | Not a controlled action here | Hypothesized exclusion | PROVISIONAL hypothesis only. 150 native-unit ordinary Workshop radius and marker's `80m` name do not establish an exclusion radius or units. |

LZ1-LZ4 are the operator's contextual labels. Their identities, selectable UI
entries and persistence across reload are unqualified. Save28's earlier
instrumented travel is a different evidence sequence; it must not be silently
renamed LZ4 or treated as a trace of M03/M08. Local and remote travel contrasts
remain consistent with request flags, resident-world reuse, distance/eligibility,
cached placement or distinct travel dispatch; the [dependency ledger](dependencies.md)
and [design](acquisition.md) give discriminators.
