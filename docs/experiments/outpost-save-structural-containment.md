# SOR-EXP-0005 — Structural containment of outpost save candidates

**Later independent work, 2026-10-08:** [SOR-EXP-0006](mature-save-outpost-validation.md) validates the count/reference grammar in a mature save and all small envelopes, including nine-byte zero-beacon cases outside this experiment's narrow predicate. Its small-corpus membership counterexample and cargo topology are recorded separately; this historical report and its observations are preserved.

2026-10-08, Australia/Sydney. SOR-EV-0011 / SOR-F-0011. Offline bounded pass complete; critical review pending. SAVE basis. Authored scripts, documentation and selected metrics REVIEW-REQUIRED; original saves, decoded blobs, bulk JSON and exploratory probes LOCAL-ONLY. No publication or integration approval.

## Result

**OBSERVED:** the known candidates occupy three separated logical neighborhoods: a length-framed relationship payload in R2, all four main object-window candidates in R3, and an indexed, counted string collection in the late region. A repeatable early directory points to the containing broad regions. An additional early pointer reaches the counted string collection. Consecutive uint16 values inside the beacon candidate match the outpost-name and two neighboring beacon-animation string indices in every beacon-bearing sample, including remapped/reordered reload samples.

**INFERRED:** Model C, distributed candidate state tied by compact references and string indices, best fits the observed footprint. This is a structural association, not a complete change-record schema or resolved workshop owner. Model B remains a possible semantic organization beneath this representation. A monolithic, exclusive outpost region is not supported. Exact individual placed-object record boundaries and a complete minimal serialization footprint remain UNKNOWN.

**HYPOTHESIZED:** the broad R3 region contains a general changed/persistent-object family; tagged compact tokens distinguish direct base identities from dynamic/reference identities; the late uint32/pair structures support identifier resolution or bookkeeping. New-session counterexamples reject treating one simple arithmetic mapping as a universal token-to-stable-identity bridge.

The pass establishes a bounded string collection and repeatable cross-save string-index mechanism, plus a directory-backed distributed containment map. It stops at the unresolved object framing/ownership boundary rather than decoding unrelated adjacent systems. The complete lower-level outpost schema is not claimed solved.

## Authority, inputs, safety and provenance

The user explicitly invoked the [structural-containment brief](../implementation-briefs/CODEX_RESEARCH_BRIEF_outpost_save_structural_containment.md). Allowed: read existing corpus records and manifests; hash originals for preservation; analyze verified existing archived copies offline; create narrow original standard-library scripts, local derivatives and review summaries. Prohibited: game launch, SFSE deployment, debugger, original-save edits, configuration or analysis-database mutation, third-party tool/code acquisition, staging, commit, push and disclosure.

Inputs: all requested S0/S0C through S7/S7C and L0/L0C/L1/L1C/L2/L2C labels. **22 labels represent 21 unique saves**, because L0 is immutable S4C / SOR-SAMPLE-0015. No incidental exit sample was analyzed. No raw save or decoded blob was copied. Exact source/copy paths remain in the unchanged prior local manifests; selected [directory metrics](structural-containment/directory.csv) use neutral labels/sample IDs.

Authoritative prior candidate definitions: [SOR-EXP-0003](manual-save-corpus-S0-S7C.md), SOR-ST-0010–0013; [SOR-EXP-0004](output-link-validation-L0-L2C.md), SOR-F-0010 / SOR-EV-0010. Role assignments retain their existing limits. The brief's STRONG output-link terminology is used as the scoped semantic association; this pass does not silently change the previous register's pending-review confidence. Internal container schema remains unresolved. Prefer **relationship/collection region**, not a proven list.

Original `analyze_structural_containment.py` imports the existing project-authored decoder, hash/search utilities, candidate constants and base-like anchors. Installed CPython 3.14.3, executable SHA-256 `cce21c0e8710e304273e98ac4b2b0f5aceb639acbcd2343cbaa5c4e81619c45b`, standard-library zlib runtime `1.3.1.zlib-ng`; source/tool credit SOR-S-0113. Source-informed definition comparisons use prior SOR-F-0004 / SOR-S-0103, not a newly executed xEdit or ESM parser. No outside implementation or new dependency was consulted/incorporated.

Every archive was freshly hashed against its existing manifest before decoding. The decoder's concatenated output hash matches the prior derivative hash. Original hashes/sizes and observed mtimes were checked before/after. Save headers again contain the recorded build strings; this is existing save metadata, not a freshly measured originating executable/profile. No build generalization.

Risks: compressed/logical offset confusion, accidental matches, unstable indices/tokens, overly broad directory naming, positional-diff inflation and cached-state interpretations. Stops: missing input, hash/bounds/transform failure, nonunique directory/object/name-index correspondence. Missing exploratory token mappings are negative evidence, not corruption or an excuse to invent identities. Cleanup: retain originals and previous artifacts; fresh output roots only; no live-save cleanup.

## A–D structural map and framing

A = raw `.sfs` physical offsets; B = compressed stream bounds; C = concatenated decoded logical offsets; D = cross-record references. All ranges are zero-based and half-open. A decoded offset is not an exact byte location within a compressed stream.

**A/B — OBSERVED corpus framing:** BCPS header occupies physical [0,72); version word +4 = 1; uint64 +8 = 72; +24 = 160; +32 = concatenated decoded length; +48 = 262144; +68 reads `ZIP `. The compressed-size table is [72,160), 22 little-endian uint32 lengths. Streams begin at physical 160 and each subsequent 16-byte aligned boundary. Table sizes delimit zlib input; each stream has checksum/EOF/input-consumption checks and expands to 262144 bytes except the final partial stream. 484 label-stream checks / 462 unique-save streams passed. Padding is separate from compressed size. [Every physical stream bound, compressed/decoded size and hash](structural-containment/chunks.csv). No additional game-record checksum has been demonstrated.

**C — OBSERVED repeatable directory hypothesis:** a unique early run of ten little-endian uint32 words is at decoded 2995 for S0/S0C and 2997 thereafter. First six values partition the save as shown below; following words are 17, 21, 9 and a variable roughly 20,700-valued word. Their interpretation as particular record counts/type families remains HYPOTHESIZED. Directory discovery requires ordered bounds and the independently closed uint32 table; it does not name sections from an outside parser.

Representative **S5** map:

| Unit | Decoded range | Size | Observed outpost relevance / boundary evidence |
|---|---|---:|---|
| Early metadata | [0,3097) | 3097 | `SFS_SAVEGAME`, metadata/plugin strings and directory at 2997; not an outpost-specific header |
| R1 | [3097,409713) | 406616 | At R1+4, uint32 5179132 points to counted string collection; R1's first word is 0; full schema unknown |
| R2 | [409713,427149) | 17436 | Relationship marker at 427039; declared payload [427047,427066) |
| R3 | [427149,3907197) | 3480048 | All four matched main object windows; full record framing unresolved |
| R4 | [3907197,4983947) | 1076750 | No assigned outpost ownership; mapped only to delimit neighboring regions |
| uint32 reference candidate | [4983947,5179059) | 195112 | uint32 count 48777 + exactly 48777 four-byte entries; next directory pointer is exact end |
| Late region | [5179059,5631712) | 452653 | Contains bounded shared string collection and candidate tail pairs |
| String collection, subregion | [5179132,5195776) | 16644 | uint16 count 880; 880 successive uint16 byte lengths and byte strings consume this interval |
| Tail-pair candidate, subregion | [5615588,5631712) | 16124 | uint32 count 2015 + 2015 pairs of uint32 values; exact EOF, ascending FF-prefixed first values |

The directory words for S5 are `4983947, 5179059, 3097, 409713, 427149, 3907197, 17, 21, 9, 20769`. Auxiliary word at directory+44 is 5179067, eight bytes into the late region; deeper semantics UNKNOWN. [All labels and pointer/count values](structural-containment/directory.csv).

**D — observed reference correlations:** the early string-collection pointer, beacon string-index triple, repeated candidate tokens between object windows and the relationship payload, and historical compact/full-width tail correspondences. Runtime pointers, handles, loaded FormIDs and stable serialized identity are not conflated with any of these values.

These broad directory regions have repeatable numerical boundaries, but their engine type names and exclusive ownership are not established. The attempted assumption that each region is uniformly `[uint32 tag][uint32 length][payload]` fails near the beginning of R1 and after the first R2 unit; retained local probes document that failure. Do not transfer the relationship envelope framing to the whole save.

## Anchor containment and logical identity

[Complete containment ledger](structural-containment/anchors.csv): every present anchor, decoded offset, extent type, broad parent, chunk number, physical compressed stream bounds, compressed size, decoded chunk size and token. Absent candidates retain the prior lifecycles rather than being redefined. Chunk numbering is zero-based.

S5 representative offsets:

| Anchor | Decoded offset | Immediate enclosing evidence | Broad parent / chunk | Physical stream range | Compressed / decoded stream bytes | Cross-save identity basis |
|---|---:|---|---|---|---:|---|
| SOR-001 | 5191160 text; field 5191158 | uint16 length 7; indexed string entry 667 in bounded counted collection | late region / 19 | [1690480,1846755) | 156275 / 262144 | old/new name field, neighboring animations and beacon's matching string-index triple |
| Beacon B | 1299772 | repeated `3a`/token/base-like framing; 512-byte analysis window | R3 / 4 | [463840,582186) | 118346 / 262144 | original signature, base-like bytes, repeated token, prior position tuple and string indices |
| Storage T | 1300898 | same candidate matching method; record boundary UNKNOWN | R3 / 4 | [463840,582186) | 118346 / 262144 | prior creation lifecycle, independent framing/base-like/token match |
| Extractor E | 1301439 | same candidate matching method; record boundary UNKNOWN | R3 / 4 | [463840,582186) | 118346 / 262144 | prior deletion lifecycle, independent framing/base-like/token match |
| Solar P | 1302007 | same candidate matching method; record boundary UNKNOWN | R3 / 4 | [463840,582186) | 118346 / 262144 | prior move tuple/deletion discrimination, independent framing/base-like/token match |
| Output relationship | 427039 marker; payload 427047 | marker 0x79, uint32 length 19, payload, then next marker 0x7a / value 40 | R2 / 1 | [179072,290302) | 111230 / 262144 | independently matched endpoint tokens; returning pair; control-preserved lengths/payloads |

Exact physical anchor offsets are **UNRESOLVED WITHIN THE COMPRESSED STREAM**; stream offsets are the meaningful A/B containment result. A 512-byte window is neither a complete object record nor its size. Parent outpost/workshop ownership remains UNKNOWN. Type/version/flags/count/checksum meanings within object headers remain UNKNOWN. The repeated main-window family is recognizable; no complete placed-object record-family decoder was validated.

All main windows remain in decoded chunk 4, the name in chunk 19, and matched relationship envelope in chunk 1. L0C's B/T/E/P main offsets are 1248327/1253622/1257727/1258295; remapped tokens and different spacing preserve structural correspondence, not literal original bytes. [Window changes](structural-containment/candidate-changes.csv) count positional differences in candidates, not changed game records. Number of complete candidate records changed is UNKNOWN.

## Name-containing collection and new index bridge

**OBSERVED / PROVEN within these samples:** the uint32 at R1+4 reaches a uint16 count followed by exactly that many uint16-length byte strings. No requirement that all strings are ASCII is imposed; only the selected name/animation anchors are interpreted as ASCII. Bounded count/length parsing succeeds on all 22 labels. It recovers every existing old/new rename offset without searching for a convenient replacement candidate.

In every one of the **20 beacon-bearing labels**, the name entry is followed by `OBJ_Outpost_Beacon_Deploy` and `OBJ_Outpost_Beacon_On_LP`. The three consecutive little-endian uint16 indices occur exactly once globally and exactly once in the beacon's first 512 bytes:

| Label | Name index | Beacon-relative triple offset | Name field offset | Counted collection range |
|---|---:|---:|---:|---|
| S1 | 661 | 66 | 5091202 | [5079285,5093911) |
| S4C / L0 | 666 | 93 | 5148238 | [5136220,5152583) |
| S5 | 667 | 93 | 5191158 | [5179132,5195776) |
| S7C | 667 | 81 | 5133942 | [5121916,5136819) |
| L0C | 660 | 93 | 5155950 | [5144051,5160433) |
| L1 | 661 | 93 | 5152717 | [5140810,5157159) |
| L1C / L2 / L2C | 664 | 93 | 5147142 / 5151436 / 5151006 | see directory ledger |

**INFERRED / STRONG structural association proposed for review:** these are references from the beacon candidate into the shared string collection. Independent changes in index and window offset, while the referenced three strings retain their relationship, support the association. Consumer/authority, name-field ownership versus related child references and a runtime API remain UNKNOWN. This is a bridge through **two-byte string indices**, distinct from three-byte object tokens. The collection is shared and contains unrelated strings; it is not an exclusive outpost record.

**Correction to SOR-EXP-0003, preserved history:** the old report says the S4C uint16 name length is 14. Direct re-reading at 5148238 yields **15**, bytes `0f00`, followed by the 15 bytes of `Kreet Outpost 1`; the whole field is 17 bytes. S5 length is 7 and whole field 9 bytes. The full field shrinks by 8 bytes. The old rename positions/lifecycle remain correct. The original report is retained with a follow-up notice; no raw bytes were changed. Name identity was not redefined.

## Relationship-region containment

The existing 0x79/uint32-length/payload/0x7a framing is confirmed in R2. Matched payloads are 12 bytes in S3/S3C, 19 in S4–S6C, and 19/19/12/12/19/19 in L0/L0C/L1/L1C/L2/L2C. The narrow scanner finds no such envelope in S1/S1C/S2/S2C/S7/S7C; that is absence of this framing predicate, not absence of all relationship state. S0/S0C have no beacon candidate. No additional early-state envelope was invented.

The 19→12→19 transitions remove/return the same seven-byte endpoint-pair group under independently matched tokens. Linked and unlinked adjacent controls preserve exact payload bytes. Entry order changes across reserialization. A beacon-like token is in the payload, but this cannot determine whether the logical owner is beacon/workshop, endpoint, independent table, cache or mirror. The immediate boundary is the length-delimited envelope; its parent is R2 at directory level. Count/discriminator encoding is still provisional. No list schema or authoritative loader consumption was established.

## Compact identifiers, reference tables and static identities

[Full tested arithmetic and negative results](structural-containment/token-mapping.csv).

**OBSERVED:** the directory-delimited uint32 table has count **48777** and span **195112 bytes** in every sample. It is byte-identical in action/control comparisons; the full run's hashes also test reload correspondence. It is a reference/index candidate by structure, not a decoded resolver. Its entries were not attributed to runtime types or inspected beyond outpost correlation needs.

Historical S1–S7C and L0 show exact tail matches for present object candidates under this arithmetic hypothesis:

```text
three token bytes interpreted big-endian
    -> low 22 bits
    -> OR FF000000
    -> a little-endian uint32 in the EOF pair candidate
```

For S5: `822c5d -> FF022C5D` at decoded 5631496, `822d48 -> FF022D48` at 5631576, `822da9 -> FF022DA9` at 5631608, `822dba -> FF022DBA` at 5631616. Associated uint32 values are 4/1/3/1; they are **not** declared object counts, owners or reference counts. Tail framing is a maximal, sorted FF-valued pair-sequence hypothesis ending exactly at EOF. Shorter suffixes can satisfy length closure too; selecting the maximal sequence avoids one known ambiguity, not all possible schemas.

**Counterexamples:** L0C–L2C B token `81a650` has a matching arithmetic full-width value `FF01A650`, with associated value 334. T/E/P tokens `81a7a3`, `81a947`, `81a94a` have **zero occurrences** of `FF01A7A3`, `FF01A947`, `FF01A94A` anywhere in each decoded save, and no tail matches. 53 of 68 present-candidate label mappings match; 15 do not. Therefore the tail cannot supply a universal stable-object bridge on this evidence. Corresponding candidate identity after reload relies on structural/lifecycle/string invariants, not this arithmetic alone. Other tag interpretations, serialization-local indices and a different created/reference table remain alternatives.

Base-like anchors: interpreting `6c60e9` and `63aed9` big-endian and masking low 22 bits yields **002C60E9** and **0023AED9**, the independently established beacon ACTI and storage CONT definitions (SOR-F-0004). This is **OBSERVED arithmetic plus INFERRED base association**, supported by creation lifecycles; no table/tag specification was adopted. Extractor/solar anchors yield 0005EF19/002031E1 by the same arithmetic, but their static definition types/names are not newly verified. A base-object association is different from this particular placed instance. No runtime handle/FormID or immutable serialized identity has been resolved across sessions.

## Growth and change density

[Full 22-label growth table](structural-containment/growth.csv); [per-stream sizes](structural-containment/chunks.csv); [action/reload compressed and decoded chunk differences](structural-containment/chunk-density.csv); [all region action/control comparisons](structural-containment/region-density.csv); [control/action ranges](structural-containment/density-summary.csv).

Measurement definition: after aligning **region starts by the directory**, compare equal-index bytes, count unequal paired bytes plus any unmatched tail, and divide by maximum before/after size. Chunk comparisons align compressed stream ordinal or decoded chunk ordinal. These are exact **positional mismatch counts**, inflated by internal shifts/reordering. They are not edit distance, changed-field counts or proof of semantic change. Prior shift-tolerant analysis in SOR-EXP-0003/0004 supplies complementary background-churn context. No subtraction of controls or statistical attribution.

| Label | R2 bytes | R3 bytes | String collection bytes |
|---|---:|---:|---:|
| S0 | 15211 | 3407958 | 14602 |
| S0C | 15211 | 3403118 | 14629 |
| S1 | 15179 | 3383991 | 14626 |
| S1C | 15179 | 3397401 | 14626 |
| S2 | 15580 | 3508846 | 16167 |
| S2C | 15190 | 3460860 | 14626 |
| S3 | 15232 | 3444598 | 14801 |
| S3C | 17280 | 3423078 | 16422 |
| S4 | 15816 | 3403360 | 16284 |
| S4C / L0 | 16062 | 3438620 | 16363 |
| S5 | 17436 | 3480048 | 16644 |
| S5C | 15797 | 3462326 | 16259 |
| S6 | 17213 | 3508047 | 16479 |
| S6C | 17066 | 3482444 | 16359 |
| S7 | 15194 | 3478303 | 14903 |
| S7C | 15194 | 3425190 | 14903 |
| L0C | 15837 | 3445988 | 16382 |
| L1 | 15833 | 3442974 | 16349 |
| L1C | 15833 | 3437087 | 16349 |
| L2 | 17160 | 3440101 | 16385 |
| L2C | 17156 | 3439618 | 16174 |

| Action | R2 size delta | R3 size delta | R3 positional mismatch density |
|---|---:|---:|---:|
| S0C→S1 beacon | -32 | -19127 | 81.10% |
| S1C→S2 storage | +401 | +111445 | 80.20% |
| S2C→S3 extractor + solar | +42 | -16262 | 78.68% |
| S3C→S4 link | -1464 | -19718 | 79.45% |
| S4C→S5 rename + player move | +1374 | +41428 | 80.61% |
| S5C→S6 solar move | +1416 | +45721 | 80.30% |
| S6C→S7 delete/cleanup | -1872 | -4141 | 80.02% |
| L0C→L1 unlink | -4 | -3014 | 80.35% |
| L1C→L2 relink | +1327 | +3014 | 60.68% |

R3 is the largest directory interval (about 3.38–3.51 MB), remains large through controls and reload, and contains all main object candidates. However beacon creation and extractor/solar creation **decrease** its size, storage increases it, and controls move it by tens of thousands of bytes. Deletion decreases it by 4141 bytes while its next control decreases it another 53113. Thus no reliable outpost-complexity growth law is demonstrated. The tiny relationship payload's ±7-byte response is hidden within unrelated R2 changes. Its payload state persists in controls even though broad region size/density does not isolate the action.

R3 action positional densities span 60.68–81.10%, control 59.21–80.43%; R2 action 53.92–67.91%, control 0.49–65.23%. R4 and the late region also churn; the uint32 reference candidate is unchanged. Highest broad diff density is not evidence of exclusive outpost ownership. No region is assigned to ships; that comparison hypothesis was not tested or pursued.

## Sparse state, model choice and bounded-region answer

Known windows combine compact candidate/base-like identity bytes, local float tuples, relationship-associated tokens and name/animation indices. This is consistent with persisted reference/change state plus inherited definitions. It does **not** demonstrate all objects use sparse deltas, decode complete definitions or identify every changed field. Saved bytes can be a cache or reconstructed derivative. No claim of authoritative state after load or safe mod integration follows.

**Direct answer:** there is no demonstrated bounded, exclusive, logically contiguous region reasonably identifiable as all “the outpost data.” The known anchors need at least **R2's relationship envelope, R3's four object neighborhoods, and the late counted string collection**, with early directory/string-pointer metadata to find them. This is the smallest **demonstrated linked support set for the known anchors**, not a proven minimal complete representation of an outpost. Reference/tail structures are additional identity leads; unresolved dependencies could require more regions.

S5's single enclosing interval from relationship marker to end of name field is [427039,5191167), roughly 4.76 MB and includes broad unrelated regions. Calling that “the outpost region” would not establish meaningful exclusivity. The name pool and uint32 table are shared; R3 is much larger than the studied objects. Model A is unsupported at this granularity. Model B could describe a deeper owner/header/object/relationship structure, but no dedicated outpost/workshop header was found. **Model C is the best-supported inferred structural model; individual change-record schema and owner remain unresolved (Model D at that lower level).**

Strongest current interpretation: separately serialized relationship state and object-reference neighborhoods share object-like tokens; the beacon neighborhood refers into a counted shared name/animation collection through remappable two-byte indices. It remains recognizable as offsets, tokens and string indices move. This is substantial logical continuity without a fully stable serialized ID.

Alternatives: cached/VM/event representations may mirror authoritative state elsewhere; the candidate main windows may be children rather than principal objects; early directory/count words could frame differently typed tables; arithmetic token matches can be a subset-specific encoding or coincidence. Additional outposts/links were not supplied, so exclusive ownership, cardinality encoding and generality are untested.

Smallest proposed next analysis, **not begun**: use these same archived samples to frame only the beacon candidate and its name-index-bearing subunit, starting at the R3 boundary and requiring record-end closure against multiple controls. Resolve the containing owner and test whether its token representation indexes the unchanged uint32 table before asserting stable identity. Stop at those candidates; no new save-format project or live experiment is implied. Additional controlled link cardinalities would require a separate live brief.

## Review package and validation

[Checks, exact new/modified file inventory, limits and review export](structural-containment/validation.md). Local root `.local-work/structural-containment/` retains failed/narrow exploratory probes, partial analysis-01–03 roots, completed analysis-04 (pre-string-pool extension), final analysis-06, local helper scripts, run log, final preservation/independent-check/validation JSON, artifact inventory, Git status and **tracked-plus-untracked review.diff**. Empty partial roots are retained, not rewritten as success. Final analysis has fresh source/tool/brief/manifest/decoded hashes. No original/decoded input is rewritten or duplicated.

The pre-existing untracked supplied brief is byte-preserved and included as an identified input in the local review package. No staging, commit, push, contact, upload or publication occurred. No new third-party permission blocker arose. Remaining limits are scientific framing/ownership/identity gaps, publication review of selected evidence and critical integration review.

Suggested later commit: `research: map structural containment of outpost save data`. Optional split: `research: add bounded outpost containment analysis` and `docs: record distributed outpost serialization evidence`. These are suggestions, not approval to commit.
