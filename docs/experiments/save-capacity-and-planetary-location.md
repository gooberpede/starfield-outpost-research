# SOR-EXP-0012 — Save capacity and planetary location

2026-10-09, Australia/Sydney. SOR-EV-0018 / SOR-F-0017 / SOR-ST-0019 / SOR-H-0008. Offline analysis complete within the results below; critical review pending. Authored code, report and selected ledgers REVIEW-REQUIRED. Source saves, private JSON, ESM extraction and native exports LOCAL-ONLY. No semantic promotion, integration or publication approval follows.

## Answer first

| Question | Best-supported answer | Confidence / coverage / limits |
|---|---|---|
| A: formerly size-excluded saves | All three decode, validate every zlib stream and close R3 exactly. New mapped decoder and ordinary-beacon CLI have no arbitrary aggregate decoded-size cap. | PROVEN for tested byte accounting; 11 capacity/regression inputs, including three large saves and two donor saves. Operational disk/time/queue budgets remain. Older frozen experiment runners retain their explicitly documented historical limits. |
| B: S1 body | **Kreet**, planet-data FormID **0003F59F**, system identifier **88327**, body index **15**; the matching STDT is `NarionStar`, **0005E630**. | STRONG scoped association proposed; SAVE + installed ESM + controlled gameplay. S1C repeats, and L2C retains body and spatial pair after beacon/parent/source-world tokens remap. No outpost-name inference. |
| B: mature network | All **17** disabled-clear candidates resolve independently to bodies and systems matching the JSON. The two disabled-set candidates also have body-cache resolutions, but lack the second spatial association and JSON counterparts. | STRONG proposed for the 17 with concordant independent associations; PROVISIONAL for the two cache-only records. Correspondence to individual JSON rows uses unique name equality; UUID mapping remains unknown. No completeness or ownership claim. |
| B: planetary surface | A separate body-associated pair of doubles is reproducible for S1/S1C/L2C and all 17 mature clear candidates. This is a useful surface-placement lead beyond local XYZ. | PROVISIONAL angular/surface interpretation. Order, radians versus another convention, axes/origin and overlay anchor versus precise beacon point remain unvalidated. **No latitude/longitude conversion is claimed.** |

## Authority, plan and safety

The maintainer invoked the [retained brief](../implementation-briefs/CODEX_BRIEF_SOR_save_capacity_and_outpost_planetary_location.md); SOR-D-0029 records authority. Allowed actions: manifest discovery, hashing, offline save/installed-data reads, bounded original stdlib tooling, existing read-only Ghidra exports and local documentation. No game launch, load/resave, debugger, deployment, configuration/save/ESM/database edits, external contact, dependency acquisition, staging, commit or push occurred.

Plan: diagnose aggregate limits; validate a bounded decoder on synthetic and actual saves; start from the beacon reader's structural parent; challenge competing identity representations; freeze save-derived associations before per-row JSON comparison; distinguish body identification from surface interpretation. Stop on hash mismatch, corrupt framing, resource guard or ambiguous essential association. Scratch is exclusive and removed on success/failure; evidence and failed runs are retained. Main risks are false component matches, save-era content mismatch and confusing tagged saved identities with runtime IDs. C:/D: retain the 40,000,000,000-byte free-space guard.

## A: diagnosis and implementation

`inventory_historical_saves.py` applies 64 MiB to **aggregate declared decoded size**, selecting first-stream-only inspection above it. Its framing helper also rejects totals above 1 GiB. `analyze_manual_corpus.decode` has a 64 MiB aggregate bound and the older exact-table-start rule. These were deliberate corpus/resource restrictions, not established format limits. The in-memory transforms retain chunk lists and join a second full output; merely raising the limits would increase memory pressure.

[stream_save.py](../../save-analysis/scripts/stream_save.py) validates physical feasibility before scratch creation, iterates the size table, reads compressed data in at most 65,536-byte buffers, and bounds each decoded allocation to the remaining 262,144-byte chunk plus one expansion-detection byte. Checks include signature/profile, table feasibility/alignment, positive compressed lengths, padding/end accounting, each zlib checksum/EOF/input consumption and exact decoded lengths. No separately defined container checksum is assumed. Huge false total declarations fail physical feasibility before allocation. Large valid declarations face an explicit resource decision rather than semantic rejection.

Decoded output goes to an exclusive temporary file and is exposed through a read-only mapping. One save occupies scratch at a time; free-space reservation includes the outstanding write. Optional `--scratch-budget` and `--decode-seconds` report `SCAN_RESOURCE_FAILURE`, distinct from structural `SCAN_UNSUPPORTED`. OS/allocation failures also report resource failure. There is no default aggregate scratch-size cap; free space is finite. The decoder requires enough virtual address space and disk, and clients must not retain the mapping after context exit. Scratch is not retained as evidence; decoded SHA-256 is.

The existing ordinary-beacon CLI now uses this path, preserving existing label/definition/archive arguments and semantic result schema while adding operational options. Its classifier iterates records and accesses the uint32 form array lazily. `records()` remains a compatibility list wrapper; `iter_records()` skips body bytes without copying and checks final closure when exhausted. A configurable per-record queue working-memory estimate defaults to 16 MiB and yields a resource exception after combined structural bounds checks. This is an individual working allocation guard, not a save-size limit. Legacy frozen inventory/experimental CLIs are not silently rerun or reclassified; use the new decoder/CLI for large-save work.

### Formerly excluded dispositions

| Input | Header version strings | Physical bytes | Decoded bytes | Streams | R3 records | Ordinary clear / set |
|---|---|---:|---:|---:|---:|---:|
| HIST-0252 | 1.12.32.0 / 1.8.88.0 | 49,283,616 | 129,062,006 | 493 | 739,330 | 20 / 8 |
| HIST-0256 | 1.16.244.0 / 1.16.244.0 | 27,854,992 | 72,878,818 | 279 | 404,025 | 16 / 1 |
| HIST-0257 | 1.16.244.0 / 1.16.244.0 | 33,343,504 | 89,499,141 | 342 | 549,915 | 20 / 2 |

All three complete without remaining framing/decompression errors. These counts describe the ordinary detector, not active player membership; historical content mapping is not newly certified. Frozen HIST classifications remain unchanged.

[Capacity ledger](save-capacity-location/capacity.csv) includes exact input/decoded hashes, versions, sizes, streams, record counts and measured Python peaks for Save3, S1/S1C, Save2/HIST-0245, Save52/HIST-0267, HIST-0268 and two TDX1798 samples as well as the three large saves. Save52 decoded SHA-256 reproduces `e3c0dc34cbbdcd26bb85d212fc458378b44404b37a5f54b635070e03e1565b93`. Primary CLI reproduces zero in Save3, one clear in S1/S1C and 19 split 17 clear/two set in Save52; donor challenges remain zero ordinary detections.

Measured `tracemalloc` peaks for the large research scans are 11,616,057 / 10,418,871 / 12,431,461 bytes respectively, including selected output accumulation. Maximum actual scratch is 129,062,006 bytes, removed after each context. Decoder input/output buffers have a combined 327,681-byte bound, **excluding** zlib internals, temporary Python object overhead, mapped resident pages and consumer outputs. The synthetic 65 MiB + 1-byte case measures less than 2 MiB of Python allocations. These are Python allocation measurements, not whole-process RSS; OS mapping residency can grow as pages are read. No claim that mapped pages consume zero RAM is made.

## B: save-derived identity chain

S1's recognized ordinary beacon is record **[1295765,1296100)**, token **822c5d**. Its first queued reference at **1295777** is **822c8d**; the next is direct base **6c60e9** and the next repeats self. The existing conditional case-5 reader supplies the parent and local XYZ independently of names. Native prefix basis remains SOR-S-0127 (`141835610` / `141835c20`, preferred VAs in the pinned image).

Initial searches found no R3 record for parent 822c8d, and only template/clone occurrences of its three-byte big-endian encoding in R1. **That negative was representation-limited:** the same tagged saved value also appears little-endian in four bytes, **8d2c8200**. It is not little-endian FF022C8D, a runtime pointer, handle or proven loaded FormID.

The new reader validates a unique length-closed R1 suffix of units 4..16, ending at R1's directory boundary. In S1 unit 6 is **[199923,297569)**. This suffix is empirical structural framing, not a full component-database decoder. Two independent associations within that bounded unit then agree:

1. At **279038**, five little-endian uint32 values are **00822C8D, 00000000, 00015907, 0000000F, 008147FC**. The middle pair (88327,15) uniquely matches the first/third uint32 values in installed PNDT `KreetPlanetData` GNAM. The last value is a source-world token lead, not the same identity as the overlay.
2. At **216019**, direct PNDT token **0043F59F** precedes the same parent at **216023**, two observed kind bytes `0200`, two doubles at **216029** and **216037**, then repeated parent at **216045**. Masking the direct static PNDT tag yields **0003F59F**, independently agreeing with association 1. This is an identity relationship plus repeated key, not a planet-name proximity search.

S1C repeats the body/cache/spatial values and offsets. L2C changes beacon **822c5d→81a650**, parent **822c8d→816f39** and source world **8147fc→8147e1**, yet resolves the same Kreet PNDT and exact double pair. This challenges literal identity persistence independently of JSON. Save3 has zero ordinary candidates. Controlled gameplay independently places S1 on Kreet; no outpost name supplies that validation.

Installed PNDT GNAM is treated as an observed three-uint32 identity tuple; field-role interpretation is supported by independent WRLD component pairs and STDT DNAM, not guessed FormIDs. `NarionStar` STDT 0005E630 DNAM equals 88327. The system identifier **88327 is not that STDT FormID**. Parent, direct PNDT token, PNDT FormID, body index, system identifier and STDT FormID remain distinct domains.

## Save2 and fixed ESM anchors

Save2 is frozen **HIST-0245**, located through scan-04 inventory; source and exact hashes are in the capacity/local provenance. It has a player record at **1519861**, first queued parent **41251b**, resolving to installed WRLD **0001251B NewAtlantis**. This is a player-location control, not a beacon decoder. The user supplies the near-Lodge-doors condition; precise doorstep distance/cell identity is not independently validated.

| Verified WRLD | Overlay SNAM / PNAM observed values | Uniquely matching PNDT |
|---|---|---|
| NewAtlantis 0001251B | 71456 / 3 | JemisonPlanetData 0003F5A1 |
| akilacity 0027CFA2 | 72432 / 2 | AkilaPlanetData 0005E2B6 |
| CydoniaCity 002CFC4A | 0 / 4 | MarsPlanetData 0003F59A |

The records explicitly contain `BGSWorldSpaceOverlay_Component`; the original read-only ESM walker verifies group/record/subrecord bounds. It exports only selected small fields locally, retaining last repeated subrecords rather than merging components. No xEdit run occurred in this task, no ESM mutation or historical content identity is implied. These are verified installed records and cross-correlations, with second-parser validation still absent.

Save2 also carries Jemison PNDT/parent/double-pair linkage at parent offset **271653**, pair **(2.2810355988151545, 0.7111154993616507)**, kind `0000`. Its component-pair body agrees with the independent fixed WRLD tuple. It lacks the outpost cache pattern; the two paths are not assumed identical.

## Save52 comparison

[Complete 19-row matrix](save-capacity-location/save52-location.csv) includes saved beacon/parent tokens, body FormID/system, JSON values, exact cache/point decoded offsets, double pairs, disabled state and concordance. All 17 JSON-corresponding rows have **body_match=True and system_match=True**. Both excluded rows are reported separately, not forced into the comparison.

The body rule was derived from S1. Initial save-only parent extraction and body/spatial receipts precede per-outpost expected-value comparison. The JSON was first inspected after initial save-derived candidates, but prior research/name/topology knowledge and subsequent repeat runs prevent a fully blind-study claim. Final `save-derived.json` is closed and hashed before its comparison phase. No parsing rule was adjusted to obtain 17/17.

JSON `bodyId` values resolve to installed PNDT FormIDs; its decimal `systemId` values match the associated PNDT GNAM first word. They are not uniformly game FormIDs: Narion's numeric system key and its STDT FormID differ. JSON UUIDs remain application identities. Individual row alignment uses unique manually chosen name equality. Independent **body evidence** is the saved overlay key plus two agreeing identity structures; earlier cargo topology is aggregate corroboration of the network, not a newly established per-outpost UUID bridge. Uncertainty in that correspondence is disclosed rather than erased by agreement.

Different Feynman bodies—including I, II, III, V, VI-b, VII-b, VIII-b and IX—resolve within the same system key. Both Feynman V sites share PNDT **0005E0DE** but have different overlay parents and double pairs. This distinguishes body identity from system-only resolution and site identity from body identity. The two historical disabled-set records resolve provisionally to Feynman VII-b and II; their point associations are absent under this predicate. Absence of those points does not prove deletion or total absence of residual geographical state.

## Surface placement and falsified alternatives

S1/S1C/L2C preserve **(-0.2211059435912563, -0.5113105421317372)** for the body-associated overlay pair despite local/reference remapping. All 17 mature clear rows have finite pairs in angular-compatible ranges; first values span roughly ±3, second roughly ±1. The same PNDT can have different pairs for different sites. Together with fixed New Atlantis/Jemison's analogous pair, this supports a body-specific surface-anchor interpretation. Numerical ranges alone do not prove radians, longitude-first order, a conventional prime meridian or north-positive orientation. Kind `0300` appears in three mature records; no forced uniform two-entry grammar or semantic kind meaning is introduced.

Local S1 XYZ **(122.6921157836914,277.25439453125,18.35177230834961)** remains separate from this pair. Earlier A0/A0C player coordinates and distances in SOR-H-0004 are contextual numerical evidence only; they do not define an angular conversion. No transform from local Cartesian beacon/player offsets to the planet's surface frame is established.

Rejected routes: treating the three-byte parent search as exhaustive; mapping the parent as a full little-endian FF FormID; expecting a standalone R3 record for every generated parent; inferring body from outpost names; interpreting system IDs as STDT FormIDs; equating local XYZ with planetary coordinates. Cache-only identity is explicitly weaker than concordant two-structure identity. Ambiguous ESM body pairs are retained as alternatives, not overwritten.

The exact remaining surface obligation is to identify the consumer/serializer of unit 6's body/overlay-keyed double pair, validate its axes/units and whether it locates the overlay/site anchor or the beacon itself, then relate source-world/tile placement and local XYZ if needed. Existing offline native exports establish overlay lookup/restoration candidates (`140ad31a0`, `140ad7200`, `140ada3a0`, `140ada760`, `141805090`) but do not prove these doubles' semantics. **Smallest high-value next step:** a targeted offline read of the landing-marker/overlay pair serializer and one fixed-world anchor consumer; if that cannot establish frame semantics, separately brief one matched in-game surface-map marker observation. No live follow-up is authorized or performed.

## Provenance, reproduction and review

Sources: Bethesda installed saves/content/native instructions (SOR-S-0127/0128 extension), project methods (SOR-S-0124), installed CPython 3.14.3/stdlib zlib/mmap (SOR-S-0113), Ghidra/JDK separate tools (SOR-S-0105), and two existing TheDailyXPerience donor saves (SOR-S-0125 / SOR-P-0003). No external parser/source code or new dependency incorporated. [Credits](../../CREDITS.md) and [source register](../SOURCES.md) retain attribution.

Local root `.local-work/save-capacity-location/` retains controls-01, mature-lodge-02, capacity-final, catalog/fixed anchors, initial blind receipts, body-final-01/body-final-02/body-final-03, native/database preservation and failed mature-lodge-01 (unknown label; no save processed). Capacity runner used manifest originals for historical inputs; final body runner uses the existing Save52 archive. Both originals and archives actually consumed were hashed against frozen manifests and before/after. No original was modified or overwritten. Header strings describe saves; originating executable/module profiles are unknown. Current installed ESM hash is `1dabed00c3f4282dd3bb54d2e9601e40b577d8742d078b7ccef203adbfef0da7`; pinned executable hash remains `7e9adb1414a8e1b325e5e1f097b9b17b78deb7eebeda37a333351a43a60f9d28`. New location semantics are tested on the 1.16.244.0 controlled/mature inputs, not transferred to older versions.

Use the installed Python executable with `-B`. Fresh runs require fresh names:

```powershell
python -B save-analysis/scripts/research_save_location.py --run <fresh> --labels Save3,S1,S1C,HIST-0252,HIST-0256,HIST-0257
python -B save-analysis/scripts/detect_ordinary_outpost_beacons.py --run <fresh> --labels Save3,S1,S1C,HIST-0267,HIST-0252,HIST-0256,HIST-0257
python -B save-analysis/scripts/inspect_spatial_definitions.py <installed-Starfield.esm> <fresh-ignored-catalog.json>
python -B save-analysis/scripts/run_planetary_location.py --run <fresh> --catalog <catalog.json> --network <existing-private-network.json>
python -B -m unittest discover -s save-analysis/scripts -p 'test_*.py'
```

The WindowsApps `python` alias was inaccessible on this workstation; actual calls used `C:/Users/User/AppData/Local/Python/pythoncore-3.14-64/python.exe`. [Validation and exact file inventory](save-capacity-location/validation.md) describes final checks, local tracked-plus-untracked review diff and limits. Await critical review. Suggested later commits: `research: stream large saves with bounded working allocations` and `research: resolve saved outpost bodies and surface-anchor candidates`.
