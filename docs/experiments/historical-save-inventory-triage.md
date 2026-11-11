# SOR-EXP-0007 — Historical save inventory and outpost triage

2026-10-09, Australia/Sydney. ANALYZED; critical review pending. SOR-EV-0013 / SOR-F-0013 / SOR-D-0023. SAVE basis. Authored summaries, selected numeric manifest and helpers REVIEW-REQUIRED; originals, archives, personal filenames, complete string/window extractions and local receipts LOCAL-ONLY. No publication/integration approval.

## Result and coverage

All **278** `.sfs` files in the authorized Saves directory were enumerated and hashed; all have distinct content hashes. Physical sizes total **3,075,600,192 bytes**, range **1,054,720–49,283,616**, median **11,370,632**. Filename order is solely a deterministic catalog order, never a gameplay timeline. `HIST-` labels are immutable within this frozen inventory, resolved by SHA-256, not new controlled SOR-SAMPLE identities. The full local manifest retains exact paths, creation/modification nanoseconds and UTC times, hashes, character/header fields and archives; the [durable-safe manifest](historical-save-inventory/inventory.json) omits personal names/paths and retains per-file provenance and selected numeric fingerprints.

All 278 have physically closed BCPS version-1/ZIP length tables with 262,144-byte decoded blocks. **275** were fully transformed and fingerprinted within 64 MiB; all 275 yielded a unique directory, counted shared strings and a successor-framed `0x79` payload consumed exactly by the existing reference/count grammar. This demonstrates structural applicability, not complete save decoding. **196 SUPPORTED / 82 PARTIAL**: 79 partial cases have unresolved name/index or collection-to-window correspondence; three have declared decoded sizes beyond the resource limit. No UNSUPPORTED, MALFORMED_CONFIRMED or UNDETERMINED files were observed; unsupported/failure handling is nevertheless tested. SUPPORTED means supported by these bounded probes, not every subsystem or historical version is understood.

| First header version string | Files | Full fingerprints | SUPPORTED / PARTIAL | Exact relationship grammar |
|---|---:|---:|---:|---:|
| 1.12.32.0 | 2 | 1 | 1 / 1 | 1 |
| 1.12.36.0 | 3 | 3 | 1 / 2 | 3 |
| 1.14.74.0 | 18 | 18 | 17 / 1 | 18 |
| 1.15.222.0 | 71 | 71 | 40 / 31 | 71 |
| 1.16.242.0 | 2 | 2 | 2 / 0 | 2 |
| 1.16.244.0 | 182 | 180 | 135 / 47 | 180 |

[Version ledger](historical-save-inventory/versions.csv). Both adjacent uint16-length-prefixed header version strings are recorded separately; **their roles are UNKNOWN**. They sometimes differ (for example 1.15.222.0 / 1.14.74.0, or 1.12.32.0 / 1.8.88.0). Neither is a verified originating executable. Header word +16 is 27 in these inputs; its semantic role/save-format-version meaning is UNKNOWN. Container version 1 is independently encoded in the physical signature. Level is a candidate uint32 immediately after the character-name field; save location/playtime/race are observed length-prefixed strings. Save type and character identity are not inferred from filename tokens. Filesystem timestamps are not game-session chronology.

## Authority, plan and provenance

The user invoked the [historical inventory brief](../implementation-briefs/README.md#archive-lookup) (`implementation-briefs.zip :: docs/implementation-briefs/CODEX_RESEARCH_BRIEF_historical_save_inventory_triage.md`), additionally requested outpost planet/coordinate recovery leads, and prohibited commit/push. SOR-D-0023 records acceptance. Allowed operations: read authorized Saves originals, hash/stat, bounded offline transforms and outpost fingerprints, verify existing local archives/research, copy useful shortlisted originals exclusively into ignored storage, author this review package. No Starfield launch/load, SFSE/debugger, configuration/cloud/database changes, original edits, dependency acquisition, external contact/disclosure, staging, commit or push occurred. Earlier session attempts could not start the filesystem runtime and made no changes; work became executable after the user's desktop rollback. Initial Git status contained only the supplied untracked brief, preserved byte-for-byte.

Plan: catalog every candidate in lexical filename order; preserve a flushed per-file receipt; validate physical bounds before transforming; inspect all saves within a fixed decoded limit; calibrate on Save3/S0 and known positives, preserving the empty-collection counterexample; freeze inventory before the separate location-name fallback; select five distinct profiles; hash-verify copies and originals; return for critical review. Stop on preservation failure, ambiguous essential bounds, changed directory/input set, unsafe free space or resource limits. A per-file decoding/model failure is recorded and does not assert corruption/absence. No cleanup deletes originals or failed evidence; all intermediate runs remain local.

Tooling: installed CPython 3.14.3 and stdlib zlib, SOR-S-0113; exact executable/runtime/script/brief hashes in `scan-04/provenance.json`. [Inventory helper](../../save-analysis/scripts/inventory_historical_saves.py) directly imports this project's SOR-EXP-0006 directory/envelope/pool/count methods. Window/name/marker methods are source-informed by SOR-EXP-0003/0005/0006 and SOR-S-0124; no outside parser/code/dependency was incorporated. Definition comparisons retain SOR-S-0103/0104 attribution. The preserved offbook decoder was read as methodological context, not imported by the new inventory helper. Full originals, including historical files outside previous controlled scopes, are read under this brief's whole-directory authority; none are modified.

Limits: 128 MiB physical input, 64 MiB full decoded input, first decoded block only above that limit, at most 1 GiB declared size accepted for physical framing, 128 MiB run-output guard, 1,800-second cooperative outer-loop time bound. C: and D: free space must each remain at least 40,000,000,000 bytes before artifact creation and between files. Time/output guards are cooperative, not OS-enforced per-file CPU/memory quotas; one bounded decode may finish before the next time check. No decoded blob is written. Scan-04 processes one original at a time; receipts are flushed/fsynced per save and `--resume` requires unchanged sources/tooling. It completed far below the runtime bound. Scope and layout failures are PARTIAL/UNSUPPORTED, never automatically MALFORMED_CONFIRMED.

## Presence and absence

The [278-row indicator matrix](historical-save-inventory/presence-matrix.csv) retains each save's analysis depth, grammar, counts, animation evidence, errors and limits. Its categories describe **detected saved state**, not verified runtime activity:

| Classification | Files | Meaning here |
|---|---:|---|
| OUTPOSTS_CONFIRMED_PRESENT | 105 | A recognizable beacon window has a resolved nonempty name/index link. Saved outpost state is convincing; current active membership may still be residual. |
| POSSIBLE_RESIDUAL_OR_INACTIVE_STATE | 79 | Beacon/marker/collection evidence exists but current bounded name/identity coverage is insufficient. This does not claim those outposts are inactive. |
| NO_ACTIVE_OUTPOSTS_SUPPORTED | 20 | Multiple applicable indicators support a provisional absence interpretation under the current model. Ten mature candidates and ten low-level/control-profile files. |
| INDETERMINATE | 74 | Older-version negatives, unexplained nonempty relationship groups, or limited decoding do not justify exclusion. |
| NO_OUTPOST_STATE_SUPPORTED | 0 | Full residual-state coverage has not been established. |

Negative-evidence gate: full decode/checksum/EOF coverage; unique bounded directory and counted string collection; exact framed relationship grammar; **zero collection beacons, zero beacon windows, zero cargo marker windows, zero exact beacon-animation entries**; either no keyed groups/endpoints or the no-outpost control's one-group/one-endpoint cardinalities; both version strings equal 1.16.244.0; no model errors. These independent neighborhoods provide corroboration, but known-definition signatures, partial object framing and an incomplete semantic model limit exclusion. No exhaustive outpost-definition/mod coverage, active-state bit, loader authority or proof of absence of arbitrary residual state exists. Classification is PROVISIONAL, not a validated no-outpost detector. Any known outpost-bearing sample satisfying this entire gate would falsify it.

The ten mature candidates are **HIST-0025, 0067, 0109, 0152, 0198, 0254, 0258, 0260, 0261, 0265**. Their header level candidates are 306–318. All ten have zero detected collection beacons, windows, cargo markers, animation entries, keyed groups and endpoints, full structural coverage and no parser errors; this is their auditable negative checklist, with per-file hashes/region sizes in the manifest. Their unknowns are active membership, arbitrary residual objects, gameplay/Unity history and cross-version negative-control applicability beyond the specified version. They are distinct bytes, not ten independent controlled repetitions. The shortlist uses HIST-0265 as a representative, not proof of a new universe or a reset.

Save3 / HIST-0253 and S0/S0C pass the negative gate. **S1/S1C/S2/S2C remain positive even with zero collection beacons**, because the named beacon window and animation entries survive. S7/S7C retain that same saved-state evidence after the controlled deletion stage: named-window presence is not activity proof. No universal active-index interpretation is restored. Older all-zero profiles (including HIST-0263, first version 1.12.32.0) remain INDETERMINATE because matching negative controls across those versions are absent. HIST-0017 and its analogous mature profiles have zero beacon/marker/animation evidence but unexplained nonempty groups; they remain INDETERMINATE rather than being silently included as absent.

## Structural contrasts and five-save shortlist

Priority is question value and diversity, not size or level. Raw originals/copies remain local. Four exclusive new copies total **80,590,416 bytes**; HIST-0267 reuses its already preserved hash-identical mature archive. Exact filenames/source paths and source/copy/source receipts are in `scan-04/shortlist-archives.json`.

| Priority / ID | Profile and exact bounded observations | Research value / uncertainty | Archive |
|---|---|---|---|
| 1 / HIST-0267 | Mature baseline: 17 collection references, 19 beacon windows, 199 keyed groups/246 endpoints, 61 marker windows, 24 reciprocal pairs | Reproduce rich topology and parallel connections; 53 member-associated markers, eight unassociated; two nonmember beacons. Current activity/UUID authority unresolved. | Existing verified archive reused |
| 2 / HIST-0265 | Mature negative candidate: 1.16.244.0 / 1.16.244.0; zero all six indicator counts; 2-byte empty relationship payload | Test exclusion against rich-network evidence without assuming a Unity transition. NO_ACTIVE_OUTPOSTS_SUPPORTED, PROVISIONAL; residual-state exclusion unavailable. | Verified exclusive copy |
| 3 / HIST-0268 | Older small profile: 1.12.36.0 / 1.12.32.0; one collection beacon/window, three groups/12 endpoints, one regular and one interstellar marker, zero reciprocal pairs | Explore older name subunit and small topology; candidate Porrima II-b name link recovered separately. Inventory stays PARTIAL; absence not supported. | Verified exclusive copy |
| 4 / HIST-0250 | 1.16.244.0 / 1.16.242.0; 11 collection references vs 15 windows, 26 groups/37 endpoints, 12 markers (8 regular/4 interstellar), six reciprocal pairs | Resolve missing collection-window correspondences and possible retained state. Fifteen name candidates recovered by separate exploratory fallback; not fed back into classification. | Verified exclusive copy |
| 5 / HIST-0252 | 1.12.32.0 / 1.8.88.0; 49,283,616 physical bytes, 129,062,006 declared decoded bytes, 493 framed streams | Deliberate resource/compatibility boundary candidate. First stream only; outpost metrics UNCHECKED. Any larger decode needs a separately reviewed resource plan. | Verified exclusive copy |

The complete selected region sizes are in the manifest, not inferred from file size. For comparison, HIST-0267 has R2/R3/reference-table/shared-string sizes **54,425 / 23,219,642 / 5,501,288 / 54,275** bytes; HIST-0265 **13,141 / 914,188 / 5,483,920 / 12,124**; HIST-0268 **68,263 / 16,878,815 / 3,805,280 / 52,383**. Region labels are structural hypotheses, not exclusive outpost containers. Whole-playthrough variation prevents a complexity-growth law.

HIST-0256/0257 also exceed 64 MiB (their declared sizes are in the manifest); they are retained as header-only PARTIAL/INDETERMINATE, not rejected as corrupt. No unpaired/ambiguous cargo references were found by the narrow marker-keyword extractor in the 275 inspected files; self-reference occurrences are retained separately in the manifest. Missing/alternative keyword layouts remain possible. Marker counts and reciprocal saved references do not establish transport direction, inventory, timing or load behavior.

## Outpost location follow-up

There is a useful recovery path for **name-associated local coordinate candidates**, but no authoritative planet/body identifier or planetary latitude/longitude mapping is decoded here. Keep these domains separate:

1. Header save-display location can describe the player. HIST-0267 says `Jemison - The Lodge` while its network names refer to many other bodies. HIST-0268 says `Jemison - Jemison`, yet a beacon-window index pair points to `Porrima II-b Outpost 1` and the beacon animation. The header cannot locate all outposts.
2. Resolved outpost names provide body-name leads, including default-looking `Porrima II-b`, `Ursa Major II` and custom abbreviations in the mature baseline. Names are mutable and may be stale; no automatic mapping to an engine planet ID or even a verified planet-versus-moon classification follows.
3. A name/animation index subunit followed by five bytes and three float32 little-endian values reproduces the prior controlled beacon tuple. In S1 the index triple begins at decoded **1,295,831**; its end +5 is **1,295,842**, the exact prior `(122.692116, 277.254395, 18.351772)` candidate. This is a variable-position method, not a fixed offset from the beacon window.

The [narrow location helper](../../save-analysis/scripts/probe_inventory_locations.py) uses known name subunits first; a separate exploratory animation-predecessor index fallback recovers 17 additional names in HIST-0268/0259/0250. It preserves ambiguous alternatives and never changes the frozen inventory classifications. Four inspected saves yield **36 finite triples**: 19 mature baseline, one old small save, one current small save, 15 anomalous-save candidates. Exact tokens, name/index/string offsets, tuple offsets and source/decoded hashes are in local `location-final.json`; selected hops are in [location candidates](historical-save-inventory/location-candidates.csv). Index pairs and plausible floats alone do not prove record ownership or transform semantics.

Examples (all offsets are **decompressed logical stream offsets**, tokens save-local):

| Save / token | Name and name-index offset | Float candidate offset | Float32 interpretation |
|---|---|---:|---|
| HIST-0267 / 81a75b | Arch III W H2O Lub / 2,924,628 | 2,924,639 | (57.345551, 99.476166, 2.938312) |
| HIST-0268 / 80c301 | Porrima II-b Outpost 1 / 3,185,709 | 3,185,718 | (47.023254, 78.879387, 4.803261) |
| HIST-0259 / 9a461d | Feynman IV Al He-3 Fib / 2,580,296 | 2,580,305 | (31.286621, 48.221863, 0.152619) |

For HIST-0268, indices 1814/1815 point respectively to the name at decoded **26,550,875** and the animation entry; the five bytes after the pair differ from the mature terminator. This is a specific older-layout lead, not grounds to require the mature literal everywhere. The prior control's second component exceeds 180, so directly calling this universal tuple latitude/longitude in degrees is unsupported. Alternative interpretations include local Cartesian positions, related frame coordinates, child transforms or unrelated variable subunits. Units, axes, reference identity, planetary origin and loader authority remain UNKNOWN. No coordinate conversion, game-map restoration or safe mod interface is established. Literal latitude/longitude probes are recorded as bounded negative searches, never proof that numeric coordinates are absent.

## Version opportunities and future work

Physical framing, directory closure, shared string bounds and relationship grammar are preserved across every fully inspected version stratum. Exact name/animation terminators and collection-to-window matching are less portable. Neither version-string differences nor signature differences prove an upgrade caused the difference: gameplay, custom naming, loaded state, accumulated residue and Unity history are uncontrolled.

Proposed only: compare preserved HIST-0268 with a distinct current-game load/new manual save after separate live authorization; use a current-version no-action resave control and the same immutable source/copy identity checks. Establish compatibility and cloud safeguards before loading, never overwrite originals, and avoid inferring causality from a different playthrough. HIST-0250 is a second candidate for correspondence/remapping questions. HIST-0252 first requires a reviewed higher-resource offline plan; it should not be loaded or fully decoded merely to bypass the present limit. No migration, new live experiment, importer or general parser was executed.

## Validation and handoff

[Validation, complete file inventory and review package](historical-save-inventory/validation.md). Twenty-five control labels (including the incidental manual exit and L0/S4C alias) retain original manifest and prior decoded hashes. Save3/S0 negatives, S1+ positives and S7 retained-state counterexamples pass. The mature baseline independently matches prior frozen decoded hash, directory, all 19 resolved names and exact 24 reciprocal pairs; associated pad counts remain 25 regular / 28 interstellar. All originals were rehashed after inventory; four new copies and reused mature archive match source hashes. No raw/decoded save is tracked. No semantic promotion, publication, staging, commit or push follows this handoff.

Suggested commit after review only: `research: inventory historical saves and triage outpost location evidence`.
