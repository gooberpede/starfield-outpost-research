# SOR-EXP-0003 — Manual save corpus S0–S7C

2026-10-07 (Australia/Sydney). Status: first pass complete, awaiting critical review; REVIEW-REQUIRED. Raw saves, decoded streams and bulk outputs are LOCAL-ONLY. Evidence bundle SOR-EV-0009; samples SOR-SAMPLE-0006–0022.

Authority: user invoked the [research brief](../implementation-briefs/CODEX_RESEARCH_BRIEF_manual_save_corpus_S0-S7C.md) and additionally requested star-system, planet and planetary-coordinate investigation, explicitly retaining actor/outpost ambiguity. No staging, commit or push. This record is the complete analysis/review entry point.

## Bounded experiment

Question: which saved byte structures correlate with beacon creation, placed objects, linking, rename, movement and deletion, beyond adjacent no-action churn? Can location evidence be tied specifically to the outpost?

Allowed actions: read metadata/hash the 17 named source saves, copy into a fresh ignored archive, verify source/copy/source hashes, then inspect only verified copies with narrow project-authored Python standard-library scripts. Read existing project research as hypotheses. Write local derived data and authored review summaries. No game/CK/third-party save-tool launch, debugger, configuration changes, save rewrite, external disclosure or new dependencies.

Inputs: the brief's exact S0–S7C and incidental exit filenames. Outputs: ignored `.local-work/savegames/manual-S0-S7C/` and `.local-work/manual-S0-S7C/`; authored report, selected manifest metrics and scripts. Existing copies are preserved. Risks: misinterpreting compressed bytes, unstable offset alignment, actor/location ambiguity, incidental simulation/combat changes, privacy of filenames and raw data. Stop on missing input, hash mismatch, conflicting destination, unsupported framing or bounds failure; preserve evidence and report limits. Cleanup: retain all originals/copies/derivatives, no live-save cleanup.

Success: narrow at least one action-correlated persistent candidate or document the exact opaque boundary. A matching string/hash or successful transform is not complete schema validation. Falsification: candidates changing similarly in controls, absent from following controls, or not matching independently repeated actions weaken semantic assignment. No reload occurs, so saved presence cannot establish authority after load.

User-reported conditions: one continuous session, no restart/reload, same general site, player stationary nearly throughout. S5 also includes movement toward the beacon. S3 adds extractor and solar together. Fauna attack likely after S3, before or after S3C uncertain; roughly 190+ to 100+ 7mm ammo. S7 can include output-link cleanup. No-action does not mean simulation stopped. Exit is `INCIDENTAL_TERMINAL_SAMPLE` only.

## Result and evidence classification

The corpus materially narrows saved outpost state. **OBSERVED:** four distinct byte signatures have the expected creation/deletion lifecycles; a three-token relationship motif appears at S4 and disappears at S7; a stable candidate identity has a three-float mutation only at S6; and the rename is an exact length-prefixed string replacement. **INFERRED:** these are respectively beacon, storage, extractor, solar, output-link and local-position candidates. **HYPOTHESIZED:** three-byte tokens encode saved identities and some nearby tokens encode base definitions. Neither full record framing nor runtime/serialized identity mapping is established.

These are SAVE observations scoped to this single continuous-session corpus, not independent repeated experiments. Byte facts are PROVEN within the listed inputs; role/field interpretations are PROVISIONAL. The candidates are stored in decoded save bytes, but their authority after load, reconstructed consumers and safe mod integration remain UNKNOWN. No native-save result is strengthened.

## Archive, manifest and timing

All 17 original/copy/original SHA-256 and size comparisons passed before analysis. A fresh archive was created at `.local-work/savegames/manual-S0-S7C/`; pre-existing copies directly in `.local-work/savegames/` were retained. The exact manifest is `.local-work/manual-S0-S7C/manifest.json`: exact source/copy paths and filenames, source-before/copy/source-after hashes, sizes, birth and modification timestamps, classification, tool/script/brief hashes. No semantic analysis read live originals. Copies have new filesystem timestamps; the manifest preserves the original timestamps separately.

The [selected manifest](manual-save-corpus/manifest.csv) preserves all 17 neutral sample IDs, descriptions, classifications, sizes, source/copy timestamps and hashes, decoded sizes/hashes and verification results. Exact names/paths stay in the local manifest because save filenames encode a personal character name. The supplied brief already contains those names and was an existing untracked input; it was not edited or cleared for publication.

Source modification times span **2026-10-07 08:23:16.120637–08:31:07.282402 UTC**, corresponding to **19:23:16–19:31:07 Australia/Sydney (UTC+11)**. Filename clock strings agree to about a second (S6 filename 08:29:34 versus mtime 08:29:35.035446). This supports a UTC filename-clock interpretation for this corpus; it does not prove the filename format generally. Filesystem times measure writes, not exact gameplay-action instants. Sequence length to S7C is 460.425 seconds; exit follows 10.737 seconds later. No missing checkpoint inferred from filenames.

Decoded headers in all samples contain two `1.16.244.0` strings. This is SAVE metadata evidence, not an independently hashed originating executable or confirmation of loaded modules. Master/plugin names are present in the header; exact strings remain local. The continuous-session baseline, no reload and gameplay actions are user reports, not independently observed runtime events.

## Container and analysis method

Empirical layout, validated on every sample: original-file bytes 0–3 `BCPS`, little-endian uint32 at +4 equals 1, uint64 at +8 equals 72 (size-table start), +24 equals 160 (first compressed chunk), +32 equals decoded length, +48 equals 262144 (full decoded chunk size), and bytes +68–71 read `ZIP `. There are 22 little-endian uint32 compressed lengths at +72. Each zlib stream expands to 262144 bytes except the final partial stream. Each next stream starts at the next 16-byte original-file boundary. The initial exploratory assumption of contiguous compressed chunks failed on chunk 2; 16-byte alignment explains the intervening padding. That failed assumption was discarded, not treated as corruption.

All **374 streams** passed zlib checksum/EOF, input-consumption and expected-output-length checks; all 17 containers consumed exactly to EOF and concatenated lengths equalled +32. Inner signature is `SFS_SAVEGAME`. Original sizes range 2,082,464–2,114,656 bytes; decoded sizes 5,528,591–5,658,954 bytes. No unsupported compression/library was installed. This validates the bounded container transform for these files, not every BCPS version or the inner schema. Header fields not used by the decoder retain unknown meanings.

Installed CPython 3.14.3 and standard-library zlib runtime `1.3.1.zlib-ng` supplied the separate execution/transform facilities (SOR-S-0113). Python executable SHA-256: `cce21c0e8710e304273e98ac4b2b0f5aceb639acbcd2343cbaa5c4e81619c45b`. No external parser/source implementation was copied or adapted. Existing definition research SOR-F-0004 / SOR-S-0103 and script research SOR-F-0001/0002 / SOR-S-0104 supplied explicitly labelled comparison leads, not save-format authority.

Shift-tolerant descriptive diff: partition decoded streams with a 32-byte rolling sum, minimum 64 and maximum 4096 bytes, boundary when low nine sum bits are zero; compare region SHA-256 sequences with `SequenceMatcher(autojunk=False)`, then trim equal byte edges. These are **analysis regions, not game records**. Unmatched sizes include unresolved alignments, reorderings and unchanged bytes inside coarse regions; they are not exact changed-byte counts. No mechanical background subtraction. Whole compressed-file positional diffs were not used to infer logical objects. Record/chunk additions and deletions below mean analysis edit operations unless specifically labelled container chunks; inner game-record counts remain UNKNOWN.

## Transition matrix and background churn

The [complete transition matrix](manual-save-corpus/transitions.csv) gives file/decoded deltas, timing, matching/unmatched bytes, insertion/deletion/replacement region counts and exact-following-control results. All eight primary controls and seven action transitions are included; exit is separated as incidental.

| Pair | Role | Elapsed seconds | File delta | Decoded delta | Unequal analysis regions | After-unmatched bytes |
|---|---|---:|---:|---:|---:|---:|
| S0 → S0C | Control | 20.481 | -2976 | -4764 | 941 | 1327115 |
| S0C → S1 | Beacon | 41.949 | -448 | -18654 | 996 | 1564005 |
| S1 → S1C | Control | 14.850 | 1056 | 13346 | 625 | 1500145 |
| S1C → S2 | Storage | 43.552 | 24192 | 114360 | 726 | 1632230 |
| S2 → S2C | Control | 18.206 | -9568 | -49997 | 903 | 1351455 |
| S2C → S3 | Extractor + solar | 45.135 | -12240 | -15642 | 833 | 1522618 |
| S3 → S3C | Control / possible combat | 31.345 | 14928 | -16590 | 834 | 1421461 |
| S3C → S4 | Output link | 54.496 | -5680 | -21379 | 839 | 1379573 |
| S4 → S4C | Control | 15.639 | 3728 | 35590 | 880 | 1396309 |
| S4C → S5 | Rename + player movement | 42.113 | 6240 | 43433 | 824 | 1560598 |
| S5 → S5C | Control | 14.932 | -9792 | -19920 | 970 | 1330771 |
| S5C → S6 | Solar move | 36.216 | 19328 | 47162 | 937 | 1480115 |
| S6 → S6C | Control | 16.105 | -7248 | -25901 | 919 | 1374851 |
| S6C → S7 | Delete + possible cleanup | 51.342 | 1328 | -7742 | 639 | 1602751 |
| S7 → S7C | Control | 14.064 | -9520 | -53032 | 924 | 1322569 |
| S7C → exit | Incidental | 10.737 | 3664 | 12415 | 759 | 1360091 |

Controls have 625–970 unequal analysis regions and 1,322,569–1,500,145 after-unmatched bytes, overlapping action results. About 1.22–1.42 MB of each control's unmatched regions lie in decoded offsets 1,000,000–2,999,999; the 4,000,000–4,999,999 bin has only 113–621 after-unmatched bytes under this alignment. Regions downstream move by tens of thousands of bytes even when their text is identical. Every indexed 256-KiB decoded container chunk changes in every pair, so chunk-level equality is too coarse to localize the actions.

Observed recurring churn includes header/session text and values, offset shifts, changes in the candidate object neighborhoods, and rearrangement of length-prefixed strings. For example, the helmet/light/attack-state string order changes at S6, unrelated to a claim of solar position. Numeric changes in storage neighborhoods after S4 are compatible with production/inventory simulation, but those fields are not decoded. Timestamp/counter, physics, actor/AI and serialization-order explanations remain alternatives, not established assignments of every changed region. Combat may contaminate S3/S3C.

Exact new-region matches in the following control number 101/42/37/17/41/30/25 for S1–S7. These counts are a triage tool, not a significance measure: some are reordered pre-existing data or nonunique patterns. The focused signatures below have the more discriminating cross-sequence lifecycles.

## Candidate identities and lifecycles

The [candidate ledger](manual-save-corpus/candidates.csv) provides each checkpoint's decoded-stream offsets, name/motif/string hits, three-byte token counts and float values. All offsets here are **zero-based decoded-stream byte offsets**. Prefix-relative offsets refer to the start of the specified byte signature, not a validated record boundary. No runtime address, FormID or handle is inferred from an offset.

| Candidate | Exact main-window signature | S0/S0C | S1/S1C | S2/S2C | S3–S6C | S7/S7C/exit |
|---|---|---|---|---|---|---|
| B / beacon | `3a 82 2c 5d 03 07 01 92` | Absent | Present | Present | Present | Present |
| T / storage | `3a 82 2d 48 6b 03 00 9a` | Absent | Absent | Present | Present | Present |
| E / extractor | `3a 82 2d a9 6b 03 00 9a` | Absent | Absent | Absent | Present | Absent |
| P / solar | `3a 82 2d ba 0f 03 00 92` | Absent | Absent | Absent | Present | Present |

Each main signature has exactly one occurrence when present. These signatures identify bounded windows; a general record header/length decoder was not implemented. Candidate saved tokens are B=`82 2c 5d`, T=`82 2d 48`, E=`82 2d a9`, P=`82 2d ba`. **Counterexample:** raw T bytes already occur once in S0/S0C/S1/S1C, whereas the longer T signature does not. A three-byte occurrence alone is not proof of identity. E has five occurrences from S3, six with the link at S4–S6C, and zero after deletion; P has four from S3 through exit. B token multiplicity changes with construction/deletion, consistent with relationships but not membership enumeration.

At S1, B main offset 1,295,765 includes `6c 60 e9` at +15, while S2 T main offset 1,298,897 includes `63 ae d9` at +15. Those are compatible with a tag-bit encoding of previously observed base definitions 002C60E9 / 0023AED9 (SOR-F-0004), but **the tag scheme is HYPOTHESIZED**, not a decoded FormID mapping. Literal 32-bit little-endian searches for the two definitions found no hits. B and T associations are independently supported by their exact creation stages; E and P are initially ambiguous at S3 and become distinguishable by S6/S7 behavior.

`outpostbeaconscript` and beacon animation strings appear at S1 and persist. Harvester and solar animation entries appear at S3. The harvester entry disappears at S7, while solar remains. S0 already contains many generic workshop/outpost script/event strings, including output-link event vocabulary; those generic names are not evidence of a built outpost or an actual link. String presence alone also cannot prove object liveness.

## S4 output-link and S7 cleanup

**OBSERVED:** the exact 12-byte motif `04 82 2c 5d 08 82 2d 48 04 82 2d a9` is absent S0–S3C, occurs once in every S4–S6C sample, and is absent S7/S7C/exit. It brings B, T and E candidate tokens together. Decoded offsets: S4 425499; S4C 425676; S5 427047; S5C 425408; S6 426827; S6C 426677. These are within container decoded chunk 1, far from the main object windows in chunk 4. This exact motif is a stronger relationship candidate than a broad S4 changed region.

**INFERRED:** persisted output-link state; disappearance at S7 is consistent with deletion cleanup. **UNKNOWN:** encoding of counts/flags, endpoint direction, whether this is the authoritative relationship or a cached/script/event representation, and whether the motif is inside a larger workshop table. Its storage-before-extractor byte order does not reverse or establish link direction. No link-only removal/recreation control exists.

E's main signature and all raw `82 2d a9` hits disappear at S7; the harvester animation string also disappears. B/T/P persist, and P's moved tuple persists. This supports a deletion lifecycle rather than a claim that the entire outpost vanished. We did not resolve tombstone flags or prove absence of every extractor-related record. The broad S7 transition remains deletion plus cleanup and background changes.

## S5 rename anchor

`SOR-001` occurs zero times in decoded S0–S4C, then exactly once in S5, S5C, S6, S6C, S7, S7C and exit. UTF-16LE searches find none in all 17 decoded streams; original compressed-byte searches are negative and are not meaningful absence evidence on their own. In S1–S4C, the same string neighborhood instead contains `Kreet Outpost 1`; that name is absent before S1 and from S5 onward.

S4C decoded offset **5148238** contains little-endian uint16 length 14 followed by `Kreet Outpost 1`. S5 offset **5191158** contains uint16 length 7 followed by `SOR-001`; text begins **5191160**. The next length-prefixed entry is `OBJ_Outpost_Beacon_Deploy`, followed by `OBJ_Outpost_Beacon_On_LP`, harvester/power and solar entries. These observations identify a string-pool-like neighborhood, not an embedded beacon name field with a resolved reference. The byte diff trims the common final `1`, yielding unequal ranges S4C `[5148238,5148254)` and S5 `[5191158,5191166)`; full fields include that unchanged final byte.

Rename text offsets: S5 5191160; S5C 5171665; S6 5218591; S6C 5192778; S7 5186932; S7C 5133944; exit 5146423. All are in decoded chunk 19. A string-table index/reference to B remains unresolved. S5 also contains player movement, so only this discriminating rename anchor is assigned to the rename; other S5 differences are not.

## S6 movement and location investigation

P's main signature and candidate token persist. At **main-prefix +50**, 12 bytes interpreted as three little-endian IEEE-754 float32s have this lifecycle:

| Samples | Raw 12 bytes | Candidate local XYZ tuple |
|---|---|---|
| S3–S5C | `ca d7 df 42 67 d0 86 43 86 fe 86 41` | (111.921463, 269.628143, 16.874279) |
| S6–exit | `fb 35 d7 42 be 66 78 43 f3 cf 7f 41` | (107.605431, 248.401337, 15.988269) |

Exact float offsets: S5C **1300418**, S6 **1302157**, S6C **1301740**, S7 **1299139**, S7C **1299096**. The same tuple also appears in a nearby P-token-associated window (for example S6 at 1302646). **INFERRED:** a transform/position-bearing solar candidate, separated from the extractor by movement and deletion behavior. Numeric plausibility alone is not the basis; the stable identity/matched action/control lifecycle is. Axis names, units, frame, reference-object versus child-object ownership and duplicated-field authority remain UNKNOWN. Animation/physics bytes elsewhere in the window continue changing in controls.

B has a stable 12-byte tuple `5d 62 f5 42 90 a0 8a 43 6e d0 92 41`, float interpretation **(122.692116, 277.254395, 18.351772)**, in its first 512-byte window from S1 through exit. The ledger locates it in every sample (S1 offset 1295842). **INFERRED:** beacon-local position candidate; it stays unchanged across the user's S5 actor movement and S6 solar movement. This is useful evidence against treating that particular tuple as the actor's changing position, but it does not validate planetary coordinates or a global origin.

### Offline comparison with earlier EXP0002 live player coordinates

Documentation/offline-only correction authorized by the user after the first-pass handoff; [correction audit](../audits/manual-corpus-coordinate-correction.md). Authoritative prior source: **SOR-EV-0004**, the [review14 evidence index](evidence/exp0002-review14-live/README.md), with the [run record](EXP0002-review14-run.md#captures-and-controls) as contextual corroboration. The actual archived observer JSON files were read and independently rehashed against the index, not reconstructed from the approximate values in the correction request:

| Capture | Local path under `.local-work/exp0002-review14-live/` | UTC | SHA-256 |
|---|---|---|---|
| A0 | `archive/observer/A0.json` | 2026-10-06T08:36:08.868Z | `27d89814a8a893603ce6a9f530e3fff9dbb08b20ea2856947ec7c2772c7fed34` |
| A0C | `archive/observer/A0C.json` | 2026-10-06T08:37:33.825Z | `f763441b19202f0277b422d6e4905dfc0231cfdbeda4edca45b113bbf675f015` |

In both files, JSON pointer `/player/coordinates/reference_xyz/value` is exactly **`[120.827057,270.736237,17.5202465]`** as serialized decimal values. A0 and A0C are identical at recorded precision: difference `(0,0,0)`, Euclidean distance **0**. No materially different captured position is observed. Extra precision not present in the capture is not invented. Both records identify `source=native_position_operands`, `units=UNKNOWN`, `frame=REFERENCE_QUERY_FRAME_UNQUALIFIED`, player FormID `00000014`, and `snapshot_atomic=false`. Their differing execution threads and existing acquisition limitations remain documented; this correction does not qualify the live query contract.

The save tuples were re-read as float32 little-endian from hash-verified decoded copies, using the existing candidate ledger offsets. Calculation: `d = sqrt(sum((candidate[i] - live[i])**2 for i in range(3)))`. The captured decimal live values and exact decoded float values below are the inputs; final distances are rounded to six decimals. Decimal arithmetic was checked against Python `math.dist` within 1e-12. Distances are **numerical coordinate differences, with no assigned physical unit**.

| Candidate / sample / decoded offset | Exact decoded float32 tuple used | Distance from either A0 or A0C |
|---|---|---:|
| Beacon / S1 / 1295842 | (122.69211578369140625, 277.25439453125, 18.351772308349609375) | 6.830539 |
| Solar before S6 / S5C / 1300418 | (111.9214630126953125, 269.628143310546875, 16.874279022216796875) | 8.997486 |
| Solar after S6 / S6 / 1302157 | (107.60543060302734375, 248.401336669921875, 15.98826885223388671875) | 26.000118 |

**OBSERVED:** the independently captured prior live tuple and save-derived candidate tuples are numerically close: distances approximately 6.83, 9.00 and 26.00, with the moved solar candidate farther from that prior reference. These are plausible local numerical separations for objects placed around the reported same player/outpost site; no numerical contradiction was found. “Plausible” describes compatibility with the placement account, not a calibrated physical-distance test.

**INFERRED (PROVISIONAL, SOR-H-0004):** the save-derived tuples may use the same or a closely related local Cartesian coordinate frame as the live runtime position. Numerical agreement strengthens that possibility, in addition to the S6 action/control lifecycle; it does not promote the candidates to authoritative object transforms or establish reference ownership.

**UNKNOWN:** frame origin, units, axis semantics, reference ownership, planetary/body-relative interpretation, conversion to latitude/longitude, and whether a frame offset or scaling exists. A0/A0C are earlier-session captures on 2026-10-06; the manual corpus is from 2026-10-07. The comparison relies on the reported same site, not a simultaneous runtime/save checkpoint or a proven cross-session frame/identity mapping. It does not reconstruct the player's actual position at S5/S6. Coincidental proximity, a related translated/scaled frame, or a different reference/child remain alternatives. Independent matched runtime/save observations would be needed to distinguish them and are not authorized here.

Local reproducibility: `.local-work/manual-corpus-coordinate-correction/compare_positions.py` reads the existing evidence/candidate files and writes only a new `comparison.json` with input hashes, offsets, exact tuples, component differences and unrounded results. It uses installed CPython/standard-library facilities already recorded as SOR-S-0113. No raw evidence or earlier manifests were rewritten.

Location hierarchy remains: **Kreet** supported as site/body label; **Narion** provisional script-name/system lead only; **local XYZ** provisional, now supported by numerical runtime/save compatibility; **planetary coordinates/lat-long** unresolved.

Location evidence:

- **OBSERVED:** a uint16-length-prefixed header field at decoded +44/+46 is `Kreet - Kreet` in S0/S0C and `Kreet - Outpost` from S1 through exit. It does not change to `SOR-001`; therefore it is not the same rename string. This looks like save-display/current-location metadata and can describe the actor's location.
- **OBSERVED:** `KreetPlanetWorld`, `Kreet`, and script-property name `::SNarionA_PAnselon_MKreet_var` occur even before placement. The latter supplies a **Narion / Anselon / Kreet naming lead**, not a decoded outpost-to-system relationship. Generic script state can retain locations other than the current one.
- **INFERRED:** the outpost is on the body labelled **Kreet**, supported jointly by the same-site user report, S1 default outpost name, header transition and stable beacon candidate. Whether the body is a planet or moon is not established by this save analysis. **Narion is only a provisional system-name lead**; no independent system identifier or authoritative association has been decoded.
- **UNKNOWN:** latitude, longitude, planetary map coordinates and conversion from the candidate local tuples. No literal `latitude`/`longitude` strings were found in the decoded streams. This negative search does not show coordinates are absent; they can be numeric, indexed or reconstructed. Prior static latitude/longitude naming evidence SOR-F-0005 supplies no validated saved offset or conversion. Actor/outpost location ambiguity remains explicit.

## Combat confound

**Combat window unresolved.** S3→S3C lasts 31.345 seconds and S3C→S4 54.496 seconds by source write times; either is compatible with the user's uncertainty. Neither delay proves the attack interval. No inventory schema or 7mm item/count mapping was already available. A raw case-insensitive `7mm` byte hit in S5C at 2255386 lies in otherwise opaque data and is not an inventory/name record. It was rejected as ammunition evidence. No ammo reverse-engineering expansion was undertaken. Combat/AI, ammunition, health and actor motion remain possible confounds around S3 and later state; control changes were retained intact.

## Alternatives, limits and smallest next step

The strongest current interpretation is a linked family of saved object/relationship candidates with independently informative rename, move and deletion anchors. They can still be cached, duplicated, script-facing or reconstruction inputs. Three-byte collisions, variable-length data, changed string ordering and coarse diff alignment prevent blanket schema claims. A single session does not test persistence through reload, identity stability across sessions, unloaded behavior or serialization on another build.

Smallest next **offline** analysis: bound the chunk-1 12-byte link motif's containing structure and cross-references to B/T/E using these existing copies; test candidate framing across all 17 samples before generalizing. Smallest new **experiment**, separately authorized: create/remove/recreate only the extractor→storage link with adjacent stationary no-action controls and no object deletion; predict motif presence/absence/presence while B/T/E/P windows remain. A later solar move-back/reload can validate the tuple and identity without expanding into a general parser. For location, a separately approved observation should record beacon versus actor position plus named body/system and map coordinates at the same checkpoint. None of these next steps was executed.

## Review package and validation

Scripts and reproducible commands are in [the script guide](../../save-analysis/scripts/README.md). Local output root `.local-work/manual-S0-S7C/` contains the exact manifest, `analysis-01/analysis.json`, `candidates.json`, all 17 decoded streams and ASCII string inventories, an exploratory `probe-S5.bin`, `identity-probes.json`, the selected-table generator, validation/inventory and complete review diff. `analysis.json` records source/output hashes, 374 chunk bounds/padding/hash records, full unequal ranges and exact following-control offsets. Exploratory command failures (unaligned second zlib stream; reading analysis.json before it finished; empty-list indexing when probing pre-storage samples) did not mutate inputs and were corrected in the final scripts.

Actual checks: five synthetic tests passed (multi-chunk round-trip fixture; corruption/truncation rejection; header/output bounds; trailing-byte rejection; insertion resynchronization). All 17 real container transforms passed the bounded checks. The candidate ledger checks every main signature for uniqueness and verifies every decoded input hash. These tests validate tool behavior, not game semantics or independent schema reproduction. Final original/copy preservation, ignore/tracked-save checks, Markdown-link checks, diff whitespace and full file inventory are recorded in the [validation record](manual-save-corpus/validation.md).

Files added: this report; three selected CSVs and validation record in `manual-save-corpus/`; four Python scripts. Files updated: root README, research state, known facts, state register, provenance, sources, credits, subsystem map, save-analysis README and script guide. The supplied brief remains an unchanged pre-existing untracked file. Exact changed/new lists and tracked/untracked-inclusive diff are in the local review package. No third-party permission blocker: existing CPython separate-tool use plus original project-authored scripts only; no parser reuse/dependency incorporation, external upload/contact, game launch, debugger, staging, commit or push. All authored findings/selected summaries await critical review and publication clearance.

Suggested single commit, only after review: `research: characterize manual outpost save corpus and location candidates`. Alternatively split tooling and research as `research: add bounded offline save corpus analysis tools` and `docs: record S0-S7C outpost persistence candidates`. This handoff does not approve integration or further execution.
