# SOR-EXP-0009 — Active outpost identification: record framing and membership obstruction

2026-10-09. SOR-EV-0015 / SOR-F-0014 / SOR-ST-0017 / SOR-H-0006. Offline SAVE and STATIC research; ANALYZED, critical review pending. Authored summaries/code/numeric ledgers REVIEW-REQUIRED; saves, paths, full fingerprints, executable text and analysis exports LOCAL-ONLY. The invoked [brief](../implementation-briefs/README.md#archive-lookup) (`implementation-briefs.zip :: docs/implementation-briefs/CODEX_RESEARCH_BRIEF_active_outpost_identification.md`) authorizes this work under SOR-D-0025. No live execution, staging, commit, sync or publication.

## Result and milestone disposition

**A complete active-player-outpost classifier is not established. The obstruction is specific:** a complete change-record scan can recover inline beacon bases and saved disabled flags, but the loader also supports records whose base is supplied through another reconstruction path. Independently, Almanac—an internal engine/UI subsystem, distinct from external reference websites—enumerates a reconstructed workshop-handle registry and applies keyword, base-type and extra-data predicates in the inspected native code. This observed list has not been independently verified as a gameplay-facing registry of active player-owned outposts. Neither the inline base nor the promotion bit substitutes for those predicates. Existing operator labels contain no controlled beacon-removal or ownership-discrimination transition. The available observations therefore do not adjudicate the competing membership rules below.

This is an obstruction to a warranted result from the **current evidence and implemented reconstruction**, not a claim that the save lacks the information, that offline recovery is impossible, or that every static avenue has been exhausted. The new static paths make the missing work concrete. Further ordinary byte-pattern searches cannot supply the missing reconstruction/semantic proof. No effort or resource budget is offered as the reason for the semantic stop; the three size-limited files are a separate coverage limitation.

| Milestone | Outcome |
|---|---|
| A: positive identification | Structural/semantic partial advance: controlled positives contain one inline created-beacon record with restored disabled bit clear; controlled negatives contain none. An active **player-owned membership** rule remains unvalidated. |
| B: conclusive zero | Not achieved. No new `NO_ACTIVE_OUTPOSTS` result. Complete R3 byte consumption is not complete reconstruction of every workshop/base/owner. |
| C: broader validation | Mechanical validation completed on 409 bounded saves; 412 labels / 389 distinct source hashes overall. Feature predictions were frozen before per-file comparison, but this was **partially blinded**, not a fresh blind study. Historical/donor gameplay truth remains unavailable. |

Every new tool result is `INDETERMINATE` for active membership, with either a size-bound reason or unresolved alternate-base/registration/ownership reason. This does not relabel the operator's known zero/one controls as unknown gameplay states: it distinguishes their ground truth from what this algorithm proves. Earlier historical triage classifications and their limitations remain preserved.

## Inputs, ground truth and preservation

[Selected manifest](active-outpost-identification/manifest.csv) records all 412 labels, exact source/decoded SHA-256, physical size, measured framing counts, first embedded version field and qualified ground truth. Absolute paths and personal character/save names remain in ignored receipts. Exact original/archive locators come from existing manifests, never guessed filenames:

| Input | Existing authority/provenance | Role here |
|---|---|---|
| Save3 / SOR-SAMPLE-0001 | `.local-work/exp0002/integrity-before.json`: `original` and `backup`; [provenance](../PROVENANCE.md) | Operator's pristine pre-beacon zero. Separate from later mature discovery. |
| S0/S0C, S1/S1C | `.local-work/manual-S0-S7C/manifest.json`; [manual experiment](manual-save-corpus-S0-S7C.md), SOR-SAMPLE-0006–0009 | Operator zero/no-action and one placed beacon/no-action controls. |
| S2–S7C, L0–L2C | Same manual manifest and `.local-work/output-link-L0-L2C/manifest.json`; [independent link series](output-link-validation-L0-L2C.md) | One retained outpost through construction, rename, movement, extractor deletion and reload/resave. L0 reuses S4C; not independent bytes. |
| Save52 / HIST-0267 / SOR-SAMPLE-0029 | Frozen HIST inventory plus [mature archive/JSON provenance](mature-save-outpost-validation.md) | 17 manually documented outposts; two additional retained beacon records. JSON was already consulted in prior work, so the count is not a blind oracle here. |
| HIST-0001–0278 | Frozen `.local-work/historical-inventory/scan-04/inventory.json` | Historical observations, not parser-derived gameplay truth. |
| TDX1798-0001–0111 | Frozen `.local-work/third-party/the-daily-xperience-1798/scan-03/inventory.json`; [donor intake](launch-era-third-party-save-corpus.md), SOR-S-0125 / SOR-P-0003 | Separate launch-era observations. Original archive and full extracts remain local; no redistribution or new permission basis. |

The runner verifies expected size/hash before reading, hashes the bytes read, and compares complete source identities after analysis. Final flags-03 receipt records **411 distinct original/archive paths unchanged**, including repeated labels and corpus overlap. There are 389 distinct source contents; 412 labels are not 412 independent observations. Incidental rotated exit saves are deliberately excluded from this research set. No new source copy or decompressed blob was written.

The inspected retail executable is the existing SOR-ENV-0001 pinned copy, SHA-256 `7e9adb1414a8e1b325e5e1f097b9b17b78deb7eebeda37a333351a43a60f9d28`, preferred image base `0x140000000`, installed game version 1.16.244.0. All native addresses below are **static-analysis virtual addresses**, not live pointers or file offsets. Originating executables for the saves were not measured; embedded versions do not transfer this native layout to older engines.

## New structural evidence

The original parser [outpost_record_framing.py](../../save-analysis/scripts/outpost_record_framing.py) follows installed instructions at `0x14185e180` and count reader `0x141809400`. For each R3 record:

1. Read one header tag; optional type byte when bit 0 is set; three-byte reference token.
2. Read LE uint32 change flags when bit 1 is set; otherwise use engine default `0x80008000`.
3. Read tagged reference count, string-index count and body length when bits 3, 4 and 5 are set. Low two count bits select 1/2/4 bytes; value is little-endian integer shifted right two.
4. Consume exactly `3 × reference count`, then `2 × string count`, then the declared body length.
5. Require exactly the directory-declared number of records and exact R3 end closure. Unknown high header bits and count tag 3 are unsupported and rejected. Header bit 2 is retained without assigning semantics. An absent type is inherited from engine context, **not guessed by the parser**.

The native buffer builders `0x141863e00` and `0x14186c250` independently show ordered resolved-reference queues, uint16 string queues and a separate body. Native `0x1418650d0` consumes queued references without advancing the body cursor; `0x141865960` consumes queued string indices on modern versions. A reference occurring in a record is therefore not automatically its base. For example, the mature QUST token `6a6c44` references a beacon and the beacon base but is not a created beacon record.

All 409 decoded inputs close exactly: **48,863,625 records**. This verifies boundaries/counts within sampled layouts, not every payload's semantics. Two saves (HIST-0248/0274) include explicit record types; the remainder use inherited types. [Version ledger](active-outpost-identification/versions.csv) separates seven embedded-version strata. HIST-0252/0256/0257 exceed the 64 MiB decoded guard and remain size-indeterminate; absence was never inferred from their skipped content.

## Initial data, base identity and saved state

The engine selector `0x141832f00` chooses initial-data type 5 for dynamic FF-domain references in the REFR family (`0x4a`–`0x55`, confirmed by `0x140b36310`) when change bit `0x8000` is clear. Other flag combinations choose types 4, 6 or 7. Token resolution at `0x1418599a0` first interprets the three-byte **big-endian tagged token**, then consults remapping at `0x14180b410`; the resulting load-time FormID is not a timeless identity.

For type 5, `0x141835610` / `0x141835c20` consume the parent-cell reference and transform, followed by the base reference. The transform body contains one shape byte, three float32 coordinates, conditional rotation floats for low bits 0–2, and a conditional packed byte. `0x1405dfa40`, called by REFR LoadGame at `0x140b29990`, discards the next queued reference and reads saved form flags (uint32) plus auxiliary flags (uint16) when change bit 0 is set. It restores form flags with mask `0x00d12960` for REFR objects and auxiliary flags with mask `0x443f`.

The named Papyrus registration for `IsDisabled` at `0x142088956` points to callback `0x14208bab0`, which tests runtime form flags bit 11 (`0x800`). `IsDeleted` at `0x1420888a6` points to `0x14208ba90`, testing bit 5 (`0x20`). These bits are included in the loader mask. This is a specific STATIC mapping of saved flags to named runtime predicates; no function was called live.

The diagnostic decoder checks token tag, change-bit preconditions, second queued reference `6c60e9` and repeated self token. The comparison with installed ACTI `002C60E9` comes from prior xEdit definition evidence, not an invented universal base-token rule. Actual inherited form type, remapping and membership are separate obligations. [Record ledger](active-outpost-identification/record-ledger.csv) contains exact decoded offsets and fields, without raw payloads or names.

| Sample | Inline case-5 beacons | Disabled clear / set | Promotion set / clear | Known gameplay |
|---|---:|---:|---:|---|
| Save3, S0, S0C | 0 each | 0 / 0 | 0 / 0 | Zero |
| S1, S1C | 1 each | 1 / 0 | 1 / 0 | One |
| S2–S7C and L0–L2C | 1 each | 1 / 0 | 1 / 0 | One |
| Save52 / HIST-0267 | 19 | 17 / 2 | 17 / 2 | 17 documented |
| HIST-0083 | 20 | 18 / 2 | 18 / 2 | Unlabelled; relationship collection has 17 |
| HIST-0016 | 2 | 1 / 1 | 1 / 1 | Unlabelled; relationship collection has 3 |

S1 record `[1295765,1296100)` has 18 references, five string indices and a 259-byte body at 1295841. Saved flags at body +14 are `0x00400409`, auxiliary flags `0x0040`; S1C matches these fields. Save52's 17 clear-disabled records carry `0x00400408`/`0x0040`; its two set-disabled records carry `0x00400c08`/`0x0041`. The saved deleted bit is clear in both sets. Thus “these two extras are marked deleted” is **not** supported; “these two load a disabled flag” is supported within the stated path.

Across 409 saves, 1,804 diagnostic records split into 1,717 disabled-clear/promoted/auxiliary `0x40` and 87 disabled-set/not-promoted/auxiliary `0x41`. These are record occurrences across repeated/correlated saves, not independent deletion experiments. Another 130 reference-containing records fail the narrow inline case-5 diagnostic; they must not be silently classified as beacons or discarded as irrelevant.

## Competing rules, predictions and falsification

The original `.local-work/active-outpost/predictions.json` predates per-file HIST/donor comparison. It predicts zero for Save3/S0/S0C, one for S1 onward/L controls, and 17 for Save52, using bit `0x02000000` in the old windows. Mature labels and prior aggregate summaries had already been seen. The disabled/auxiliary rule was discovered later and has **no independent preregistration**; its agreement is exploratory corroboration.

| Rule/mechanism | Test and result | Disposition / missing discriminator |
|---|---|---|
| Any beacon-like window means active | Mature 19 versus documented 17 | Rejected as an active count. Retained objects require state interpretation. |
| Relationship collection is all active beacons | S1/S1C, S2/S2C and S7/S7C have empty collections while one outpost remains | Falsified. Preserve SOR-H-0005 subset alternatives. |
| Any record referencing the beacon base is a beacon | Mature quest record references base/beacon; ordered queues separate base use from other uses | Falsified. Reference occurrence is not identity. |
| Promotion bit directly means active | Native `0x141803ba0` names it `CHANGE_REFR_PROMOTED`; loader uses it in initial cell/restoration handling | Direct active-bit interpretation rejected. Correlation survives but does not establish authority. |
| Inline base plus disabled-clear identifies every active outpost | Engine supports alternate initial-data paths; HIST-0016 has three collection-member records lacking the inline base | Completeness unproved and mechanically unsafe. Those members are not independently labelled active beacons. Resolve their actual bases before calling them false negatives. |
| Disabled-clear plus auxiliary bit 0 clear is sufficient player membership | All 1,804 diagnostics co-vary; no controlled removed/non-player workshop case separates the policies | Provisional. Engine registration predicates below are additional obligations. |
| Empty decoded R3/base search proves zero | Byte closure does not resolve inherited types, external/static bases, extra restoration, keywords or registry population | Rejected as an absence proof. |
| Names, animations or compact arithmetic identify membership | Prior cross-session remapping failures; shared strings and retained records | Corroboration only; no identity/authority shortcut. |

HIST-0016 is an exact alternate-representation challenge: collection tokens `82c210`, `8163c8`, `81be60` have R3 records at decoded 3875017, 3294780 and 3448919, each flags `0x92018200`. Their second reference repeats a cell-like token rather than `6c60e9`. Their change bit `0x8000` disqualifies the type-5 decoder, and the native selector has another path. The inline-base method cannot tell whether these are alternative beacon records, other workshops or unrelated collection members. Do not convert the previous collection label into ground truth to settle that question.

## Independent native membership route and exact obstruction

Tracing the `aOutpostListA` binding through Almanac owner construction and initialization reaches `0x141360e80`. It iterates handles from static globals `0x145f0ba80` / count `0x145f0ba78`, resolves references, applies an exclusion keyword query `0x140f3bfc0` via global `0x145f0c6d0`, checks base form type ACTI (`0x1e`), checks another keyword through `0x14047fce0` / `0x145f0b380`, and requires extra type `0xbc` (ExtraWorkshop). The list is sent through `0x14136ac90` → `0x14136dc00` → `0x141361c10` to the outpost UI data.

Registry insertion `0x140f3b300` suppresses references with runtime auxiliary bit 0, a particular parent-cell/worldspace condition, wrong base type, or a missing keyword, then deduplicates handles. Removal is `0x140f3b500`. Registration is reachable from reference setup (`0x140b270a4`), a build path (`0x14133515f`) and extra-data restoration (`0x14052701c`). These are direct static observations, not a complete list of all writers: xref queries have documented limits.

The extra-data loader `0x140521620` dispatches type `0xbc` to `0x140f50880`. That reader consumes resource/assignment data, reference and string queues, a name and transform-related fields, with a version-dependent branch clearing fields for versions below `0x89`. There is no fixed “outpost active byte” at a universal body offset. Full decompilation was exported locally after the initial 50,000-character cap truncated this dispatch; this truncation was not mistaken for absence.

The missing proof has two precise parts:

1. **Reconstruction coverage:** resolve inherited form types and bases for alternate initial-data records, and reconstruct ExtraWorkshop/keyword/parent predicates for all registration candidates. Current R3 framing establishes none of those by itself. The three HIST-0016 records provide fixed test locations for this gap; the type-5 parser explicitly refuses them.
2. **Player-active semantics:** establish that the reconstructed registry/UI predicate equals the requested active player-owned state, including retained disabled objects, removal and excluded/non-player workshops. Controlled fixtures do not discriminate this from enabled-beacon presence, and observational JSON only covers one mature network. A native UI consumer is stronger evidence than a pattern, but its completeness and gameplay equivalence still require validation.

There is no proof that two full saves with different active states are information-identical, and no such claim is made. The obstacle is underdetermination of the tested rules by the labelled corpus plus unfinished reconstruction of the engine's actual predicates. Wider feature scanning cannot resolve that underdetermination. A subsequent offline reconstruction can overcome part 1; a targeted causal checkpoint can discriminate part 2. They are distinct requirements.

## Smallest targeted follow-up

For A, separately authorize an operator-controlled **beacon-only present → removed → reload** sequence on an isolated copy of the known one-outpost save. Record an independent in-game outpost count/list at each settled checkpoint, manually create a new save and a no-action control, and confirm the post-reload count. Compare full framed records, restored form/auxiliary flags and actual ExtraWorkshop/registration inputs. Preserve originals; no debugger, SFSE, injection or save-byte editing is needed. Stop on unexpected load/content mismatch or source-save changes. Do not run this proposal under the current brief.

This discriminates whether removed outposts disappear, remain disabled, retain promotion, or lose registration separately. It **cannot** alone prove B. B additionally needs the offline alternate-base/registry reconstruction above and a stated content/version scope. A non-player/excluded workshop control is needed before claiming player-ownership equivalence. No broad live survey or native-save automation retry is proposed.

## Reproduction, failures and limits

Run from the repository with the already installed Python; output directories must be new:

```powershell
& 'C:/Users/User/AppData/Local/Python/pythoncore-3.14-64/python.exe' save-analysis/scripts/test_outpost_record_framing.py
& 'C:/Users/User/AppData/Local/Python/pythoncore-3.14-64/python.exe' save-analysis/scripts/test_outpost_record_framing.py --corpus --run review-new-name
& 'C:/Users/User/AppData/Local/Python/pythoncore-3.14-64/python.exe' save-analysis/scripts/investigate_active_outposts.py --run review-new-name
```

The synthetic suite has six test methods covering count widths, explicit/default headers, table/body boundaries, exact closure, truncation, transform-conditioned offsets and reference decoys. `--corpus` additionally compares an independently implemented arithmetic walker on 11 selected verified saves / 874,242 records; its receipt path is exclusive, so use a fresh `--run` name when repeating. It uses no production cursor/count code. Independence is implementation-level; both walkers derive from the same native format evidence and shared physical decoder.

Fresh corpus runs should reproduce 409 full framings / three size limits, all 23 controlled labels' zero/one inline observations, and the selected mature/historical metrics. They should not produce active membership classifications. Safeguards: physical ≤128 MiB, decoded ≤64 MiB, individual decoded blocks ≤262,144 bytes, existing disk guards ≥40 GB on C/D. Originals/copies are read in memory; raw decoded bytes are not saved. Fresh JSON receipts are ignored and may contain personal paths/strings. No dependency installation or outside parser is involved.

Failures preserved locally: flag-01 included an incidental exit-save locator that had rotated and aborted; filtering to the authorized S/L labels fixed intake. Early ad-hoc fixed/shifted-header probes failed before the complete queue/count model; preserved probe scripts document these abandoned assumptions. The first constant search matched substrings and hit 3,000 entries before relevant code; exact constant matching replaced it. Some large function exports hit instruction/decompilation caps; a bounded `full:` export (250,000 characters) recovered the needed ExtraWorkshop dispatch. No capped scan is called exhaustive.

Final frozen features: flags-03 SHA-256 `91aefdc09432cb6284fa337ccdd5a721ba025d300e5eda72c2f0089985460acc`; earlier framing-01 `05df0d0ce8a08d9acf5ce564de0fc0d2e700d212bfe472934e0706a6ba2f41c4`; original flag-02 `9f9939dc83e6ec82bba8a8cdefc7fb50cf6ccd3098a44b61dad0c9c41e6aabd2`. Selected CSVs were authored after freezing, not classifier inputs. Historical classifications/JSON were not read by feature extraction; pre-existing familiarity prevents a full blindness claim. The final diagnostic reason wording changed after flags-03, without changing feature logic; final code hashes are retained separately.

Ghidra 12.1.2 ran only with `-readOnly -noanalysis`; no symbols/types/comments/imports were changed. A contemporaneous database hash snapshot was unfortunately not taken before the first exports. Existing earlier snapshots and a mid-run/final comparison can detect differences, but cannot replace that missing initial baseline. This limitation is retained in [validation](active-outpost-identification/validation.md). Full static exports 01–32, constant-search exports 01–04, failed probes and private preservation manifests remain under ignored `.local-work/`.

## Review package and provenance

[Validation and exact inventory](active-outpost-identification/validation.md) records actual checks, local diff location and remaining risks. New tools are original project work informed by installed Bethesda instructions and existing project methods (SOR-S-0124), not clean-room work or outside parser reuse. Separate tool credits: SOR-S-0113 Python/stdlib; existing Ghidra/JDK provenance; SOR-S-0103/0104 definition/script evidence; SOR-S-0127 installed native evidence; donor data SOR-S-0125 under unchanged SOR-P-0003. No third-party implementation, new dependency, fork, upstream contact or PR was incorporated/created. Scientific confidence does not clear publication. Await critical review; this report is not approval to integrate or expand scope.
