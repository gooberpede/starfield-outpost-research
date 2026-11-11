# SOR-EXP-0008 — Launch-era supplemental third-party save corpus

2026-10-09, Australia/Sydney. ANALYZED; critical review pending. SOR-EV-0014; SAVE basis. Authored code, numeric tables and prose REVIEW-REQUIRED. Original archive, saves, private locators, full receipts and extracted content LOCAL-ONLY. No confidence promotion or publication/integration approval.

## Result

The operator-supplied TheDailyXPerience package contains **111 distinct saves**, not a new tranche of the frozen 278-save HIST inventory. All 111 pass the existing bounded physical transform, directory/string checks and successor-framed `0x79` grammar. Both separately recorded header version strings are **1.7.23.0** in every save. These are embedded metadata, not measured originating executable identities. Physical container version is 1; header word at decoded +16 is 27, meaning UNKNOWN.

No known beacon window, exact beacon animation string, cargo-marker window, collection beacon or reciprocal cargo connection was detected in any file. **15 NO_ACTIVE_OUTPOST_INDICATORS_DETECTED / 96 INCONCLUSIVE / 0 OUTPOST_EVIDENCE_PRESENT**. Fourteen relationship payloads are genuinely empty two-byte units; one additional negative candidate has one group/one endpoint. The other 96 have unexplained groups/endpoints. Their syntax is compatible, but their outpost semantics are unestablished. No save is certified outpost-free, vanilla, corrupt or migration-compatible.

The [111-row numeric manifest](launch-era-third-party-corpus/manifest.csv) retains hashes, sizes, decoded identities, version fields, region/payload bounds, exact-consumption counts and detection metrics without donor filenames or character names. [Ranked shortlist](launch-era-third-party-corpus/shortlist.csv) contains full source hashes. Local receipts map immutable `TDX1798-*` IDs to archive members; lexical member order is catalog order only.

## Authority, source and intake

The user invoked the [retained brief](../implementation-briefs/README.md#archive-lookup) (`implementation-briefs.zip :: docs/implementation-briefs/CODEX_RESEARCH_BRIEF_launch_era_third_party_save_corpus.md`), requested commit suggestions, and prohibited commit/push. Allowed: read/list/hash the exact supplied archive; execute available installed 7z for safe local extraction; bounded offline outpost compatibility/triage; independently authored scripts and review records. No game launch/load/resave, SFSE, debugger, original modifications, live-save writes, new software/dependencies, external contact/disclosure, Git staging/commit/push or unrelated system decoding occurred. SOR-D-0024 records authority.

Author/uploader **TheDailyXPerience**, [Nexus listing 1798](https://www.nexusmods.com/starfield/mods/1798), SOR-S-0125 / SOR-P-0003. Listing metadata reports a September 2023 upload; the [files tab](https://www.nexusmods.com/starfield/mods/1798?tab=files) distinguishes the large first-playthrough package from a later small package. This is source-reported provenance, not per-save build certification. Author endorsement is not implied.

| Original archive identity | Observation |
|---|---|
| Filename | `Over 110 saves-1798-1-1694378623.7z` |
| SHA-256, before and after | `9b8bd55553c8e21f97a88d201a06aa870dd77a476f76cef69041176cf71b9093` |
| Physical bytes | 867,429,978 |
| Local creation UTC | 2026-10-08T21:42:59.194164+00:00 |
| Local modification UTC | 2026-10-08T21:45:37.896598+00:00 |
| Archive format | 7z, LZMA2:24, solid, one block, 2,632 header bytes |
| Members | 111 `.sfs` files + one directory; 900,829,296 expanded bytes |

Installed **7-Zip 22.01 x64**, Igor Pavlov/contributors, SOR-S-0126, was used as a separate tool. No implementation was copied. Member validation precedes extraction: reject rooted/traversal/drive/alternate-stream/device paths, case-insensitive collisions, unsupported attributes, links/reparse metadata, encryption, non-save content and excessive sizes/counts. Observed attributes were only A/D. Post-extraction member set, sizes, archive CRC32 values and reparse checks all passed. Every extracted file has a SHA-256 and unchanged final identity. CRC verifies archive-member integrity; it is not an archive-provided cryptographic hash or semantic validation.

Extraction is retained under `.local-work/third-party/the-daily-xperience-1798/extracted/`; no shortlist duplication or repackaging. The original archive was never moved, renamed, edited or deleted. Absolute original/member locators, timestamps and character fields stay in ignored receipts. Access-time behavior is uncontrolled. Member times span 2023-09-01 through 2023-09-11; 7z displayed them without a timezone, so they are not labelled UTC.

Resource plan: <=256 members including directories; <=128 MiB individual physical file; <=4 GiB total expanded intake; <=64 MiB decoded per save; <=128 MiB analytical receipts per scan; 300-second extraction deadline; 1,800-second cooperative scan bound. C: and D: must each retain **40,000,000,000 free bytes**, checked before and during operations; projected expansion must also preserve that guard. No decoded blobs are written. Processing is sequential; CPU/time guards are cooperative between bounded files, not hard per-decode quotas. Final scan took about 31.5 seconds; free space remained about 89.8 GB C: / 142.9 GB D:.

The initial run extracted the corpus but stopped while writing its extraction receipt: the inherited 128 MiB output guard incorrectly included the extracted corpus. This was an accounting failure, not a space-guard failure. The correction places fresh scan receipts in separate subdirectories. Existing extracted bytes were reused unchanged and checked against every member size/CRC; all originals were rehashed. `scan-02` and final `scan-03` agree. A synthetic test also caught rejection missing for a root-relative path; `path.root` and empty-component rejection were added before final scan. Failed/earlier receipts remain preserved.

## Narrow compatibility matrix

| Structure | 1.7.23.0 / 1.7.23.0 result, 111 saves | Comparability and limits |
|---|---|---|
| BCPS v1 / ZIP physical framing | recognized, exact physical EOF and all 10,007 zlib streams verified | Same size-table/262,144-byte-block/16-byte alignment model as later corpus; no loader test |
| Directory and reference-table closure | recognized, unique bounded directory in 111 | Same ordered region and uint32 table closure constraints; region ownership remains provisional |
| Counted string collection | recognized and bounded in 111 | Same early pointer and uint16 count/length walk; not a full late-region decoder |
| `0x79` relationship unit | recognized, unique successor-framed unit, exact grammar consumption in 111 | Payloads 2–82 bytes; syntactic compatibility includes empty units |
| Beacon/reference collection | recognized, count zero in all 111 | Empty collection alone does not identify active-state absence |
| Known beacon/object windows | absent in successfully decoded R3 under existing signature model | No matching positive launch-era control; alternate layouts remain possible |
| Name/animation association | exact animation entries absent in bounded shared pool; association untested | No candidate beacon/name link to exercise positive semantic compatibility |
| Cargo markers/reciprocal signatures | known marker windows absent in successfully decoded R3; no extracted reciprocal pairs | Cargo absence outside these signatures is unproven |
| Location/body-name lead | ambiguous/unavailable for outposts | No linked outpost name; player display location cannot locate absent candidates; no float/coordinate workstream |

Physical sizes range **869,152–13,579,344 bytes**; decoded sizes **2,188,291–39,753,248**; stream counts **9–152**. All saves are within full bounded coverage, no header-only/unsupported/error cases. Decoded bytes processed per complete scan total 2,607,377,084, never stored as a combined blob. SUPPORTED means these probes succeeded, not that all records or semantics are understood.

The grammar is the existing SOR-EXP-0006 model: tagged count with widths 1/2/4 selected by low bits 0/1/2, value shifted right by two; beacon count then three-byte references; group count then three-byte group key, tagged endpoint count and three-byte references. Tag 3 is unsupported. Require exact payload consumption and the existing eight-byte `0x7a` successor with length 40. A separate direct walker verifies every payload without calling the original grammar/Cursor.

Exact examples below use **decompressed logical stream offsets**, zero-based and half-open, never physical compressed offsets or runtime addresses. All IDs resolve to source/decoded hashes in the manifest.

| ID | `0x79` header offset | Payload range | Length/consumed | Beacon/group/endpoint counts |
|---|---:|---|---:|---|
| TDX1798-0013 | 546703 | [546711,546713) | 2/2 | 0/0/0 |
| TDX1798-0014 | 3491000 | [3491008,3491064) | 56/56 | 0/3/14 |
| TDX1798-0024 | 337278 | [337286,337288) | 2/2 | 0/0/0 |
| TDX1798-0080 | 3227991 | [3227999,3228081) | 82/82 | 0/8/16 |
| TDX1798-0015 | 719986 | [719994,720003) | 9/9 | 0/1/1 |

Empty payloads consume two zero-valued tagged counts. The syntax does not imply these broad regions are exclusively outpost state. Nonempty relationship groups without any known outpost signatures are a useful specificity challenge, not proof of a new non-outpost subsystem. Nothing demonstrates that differences from later saves are version migrations rather than uncontrolled gameplay state.

## Detection, progression and shortlist

The 15 negative-detection candidates have full stream/checksum coverage, unique directory/pool, exact relationship grammar, zero beacon collection entries/windows, zero cargo marker windows and zero exact animation entries, with either zero groups/endpoints or one/one. This adopts the brief's **detection-only** label without adopting the historical inventory's current-version absence claim. Older-version positive/negative ground truth is missing; residual state and alternative definition/layout signatures remain unexcluded. Fourteen empty units include five level-41 candidates, so emptiness is not confined to early progression. The one/one case is TDX1798-0015 (level candidate 7), an observational cardinality match to the current no-outpost control, not proof of identical semantics.

The 96 other saves have zero known beacon/cargo/animation signatures but groups/endpoints beyond that narrow gate. They remain INCONCLUSIVE even though parsing succeeds. Existing controlled S1/S2 empty-beacon-collection positives and S7 retained-state examples remain counterexamples to registry/activity interpretations; this corpus does not replace them. No new controlled experiment was performed.

Character-name metadata has two distinct labels (110 files versus one), anonymized in the manifest. Names are not decoded persistent character identifiers. Shared name, embedded versions, level/playtime and nearby member timestamps support a **plausible related progression/branch comparison** for 0013/0014: both level 41, playtime candidates 2d14h14m/2d14h15m, nearby member times, but payloads 2/56 bytes and substantially different save sizes. The earlier 0011 also has 42 bytes before the empty cluster. A simple monotonic history is not supported. Unity transition, branch identity and exact chronology remain UNKNOWN; filename suffixes do not establish them.

Header plugin-name leads include the expected base/bonus-content strings, but **TDX1798-0001 and 0003 also contain `RicherMerchants.esp`**. These are bounded early-header string observations, not a complete validated load-order decoder or evidence that a module affected outpost state. They defeat assuming the package is uniformly mod-free. Absence of extra plugin strings cannot prove vanilla status.

Five selected cases, ranked by information value, with full hashes in [shortlist.csv](launch-era-third-party-corpus/shortlist.csv):

1. **0013:** advanced empty unit; strongest advanced negative-detection candidate and branch comparison anchor.
2. **0014:** nearby same-label/version/level nonempty unit (3 groups/14 endpoints); tests specificity and the progression interpretation. No outpost variation is demonstrated.
3. **0024:** distinct character-name label, level 1, empty unit; early observational calibration lead, not a controlled no-outpost baseline.
4. **0080:** largest group/endpoint profile (8/16) despite zero known outpost signatures; strongest relationship-specificity challenge.
5. **0001:** mod-name counterexample with one group/nine endpoints; tests future assumptions about corpus provenance. 0003 repeats that lead, not a separate distinct category.

No positive outpost-containing sample was found to select. Future launch-era positive-control acquisition or a focused read-only comparison may be useful, but is proposed only. Loading/resaving these historical saves still requires separate authorization and source/cloud protections.

## Evidence and publication boundaries

OBSERVED: hashes, bounds, version strings, empty/nonempty count profiles and signature searches. INFERRED: bounded syntactic compatibility with existing methods and possible related branches. HYPOTHESIZED/OPEN: active-state absence, group semantics, identity/Unity continuity and alternate older object layouts. No new PROVEN/STRONG semantic register entry is created.

The Nexus listing's permission panel restricts re-upload, modification and asset use, while descriptive prose offers broader testing/resource use. The retrieved references and their exact sections are retained locally in `permission-reference.json`; SOR-P-0003 records the brief's limited working interpretation for local examination and independent research. Web retrieval supplied cached pages (description approximately two weeks old, files approximately one month old), **not an independently preserved live-current permission snapshot**. Currentness and scope ambiguity remain a publication-review issue. No source saves/archive/substantial extracted payload may be published or re-uploaded; independent summaries also remain REVIEW-REQUIRED. No author contact was attempted.

[Validation and complete review package](launch-era-third-party-corpus/validation.md) records tooling, checks, errors, exact local paths, changed files and diffs. Older saves remain eligible observational research inputs; Save3 causality experiments, the owner's mature/historical corpus and this donor corpus remain distinct. Frozen HIST records were not modified.

Suggested commit after review only: `research: inventory launch-era third-party save corpus`.
