# SOR-EXP-0004 — Output-link remove/recreate validation

2026-10-07 (Australia/Sydney). Offline analysis complete; critical review pending. Evidence SOR-EV-0010; finding SOR-F-0010; relationship candidate SOR-ST-0011. Authored summaries REVIEW-REQUIRED; raw/decoded saves and bulk probes LOCAL-ONLY.

## Result

**OBSERVED:** the original literal 12-byte motif is present only in historical L0. Its original object tokens are not stable across the reported reload. Independent object-window matching finds replacement tokens; a bounded relationship payload containing those endpoint tokens follows **present / present / absent / absent / present / present** across L0/L0C/L1/L1C/L2/L2C. Both controls preserve the payload state. All four object-window candidates persist under the new tokens.

**INFERRED:** the bounded payload strongly supports persisted extractor/storage output-relationship state. Recommend **promote the scoped semantic association to STRONG after critical review**, not PROVEN engine semantics. No automatic promotion is made by this report. Cross-session logical correspondence, exact ownership, direction encoding, identity resolution and authoritative load consumers remain provisional/unknown. The failed literal prediction and post-preregistration method change are preserved below.

## Authority, plan and conditions

The user invoked the [L0–L2C brief](../implementation-briefs/CODEX_RESEARCH_BRIEF_output_link_validation_L0-L2C.md). Allowed: copy/hash the six new named originals, reuse verified S4C, analyze local copies with existing project-authored tooling and narrow additions, author review records. No live gameplay, debugger, SFSE, save edits, configuration/database changes, network, staging, commit or push. No third-party parser or dependency introduced.

Question/prediction: does the prior S4 motif reverse on unlink/relink while endpoint candidates persist? Before new-save analysis, `.local-work/output-link-L0-L2C/preregistration.json` pinned the existing exact motif, four main signatures, tokens, prior report/candidate hashes, brief and script hashes. Controls and falsifiers: the linked baseline must support the candidate; unlink and relink must change it oppositely; unlinked/relinked no-action samples must preserve state; unexpected endpoint loss or remapping must be investigated before assigning link semantics.

Inputs/outputs: exact seven source filenames from the brief; existing L0 archive, fresh six-save archive `.local-work/savegames/output-link-L0-L2C/`, and fresh local analysis root `.local-work/output-link-L0-L2C/`. Risks: copy race, unsupported compression, remapped token collisions, reordered serialization, simulation/production and action-account confounds. Stop on missing input, hash/size/mtime mismatch, ambiguous structural matching or unsupported container bounds. Preserve failed outputs; no original cleanup. These are completed offline observations of saves supplied by the user, not independently observed game actions. Reload, unlink/relink and no-action descriptions are user-reported. No-action does not freeze simulation; production state, actor movement, loading/timing and runtime inventory were not independently measured.

**L0 → L0C is cross-session/reload/elapsed-time churn, not a same-session no-action control and not an action validation transition.** L0C is the new-session linked baseline. Exit is `INCIDENTAL_TERMINAL_SAMPLE`; it is not an additional control or validation action.

## Archive and provenance

Six new source/copy/source comparisons passed before analysis. Historical L0 also passed a fresh live-original/archive comparison. Seven final source/archive hashes and original modification times were rechecked; [validation](output-link-validation/validation.md). Exact filenames, absolute source/copy paths, descriptions, classifications, SHA-256, size and creation/modification times for every sample are in the local `manifest.json`. The [selected manifest](output-link-validation/manifest.csv) omits personal filenames/absolute paths while retaining verification data. Access times were not controlled.

L0 is S4C / Save13 / **SOR-SAMPLE-0015**, not a new independent sample. Existing archive `.local-work/savegames/manual-S0-S7C/` was reused without duplication. Size **2,098,880 bytes**, SHA-256 **`5dcf2549a19dbf6b2bdd5573762c67e66f256e05a7db6faa772d616bd35401fd`**; decoded size **5,588,279 bytes**, decoded hash agrees with the prior analysis. Prior source: SOR-EXP-0003 / SOR-EV-0009, [report and exact candidate definitions](manual-save-corpus-S0-S7C.md#s4-output-link-and-s7-cleanup). The new manifest pins the old manifest hash and matches its S4C filename/hash/sample ID.

New IDs: L0C=**SOR-SAMPLE-0023**, L1=0024, L1C=0025, L2=0026, L2C=0027, exit=0028. All seven decoded headers contain `1.16.244.0` at decoded offsets 142 and 154. This is save metadata, not a newly verified originating executable hash, module profile or plugin equivalence. Build generalization remains untested.

Installed CPython **3.14.3**, executable SHA-256 `cce21c0e8710e304273e98ac4b2b0f5aceb639acbcd2343cbaa5c4e81619c45b`, standard-library zlib runtime **1.3.1.zlib-ng** (SOR-S-0113) reused the project's bounded BCPS decoder. Seven saves / **154 chunks** passed checksum, EOF, expected decoded length, input-consumption, alignment and full-file bounds. Prior S3C/S4/S4C decoded files were rehashed for historical structural comparison. No second decoder or general save schema was established.

## Transition metrics

[Complete CSV](output-link-validation/transitions.csv). Seconds derive from source filesystem modification times, not exact gameplay event times. Region partition/alignment is the unchanged [manual-corpus method](manual-save-corpus-S0-S7C.md#container-and-analysis-method). Unequal regions are analysis units, not game records; unmatched bytes include unresolved alignment/reordering and are not exact changed-byte counts.

| Transition | Classification | Seconds | File delta | Decoded delta | Unequal regions | After-unmatched bytes |
|---|---|---:|---:|---:|---:|---:|
| L0 → L0C | Cross-session/reload/elapsed-time | 5986.044 | -7120 | -3446 | 961 | 3757465 |
| L0C → L1 | Unlink | 40.047 | -7856 | -3290 | 1095 | 1568952 |
| L1 → L1C | Unlinked no-action control | 13.521 | +2528 | -5639 | 996 | 1275728 |
| L1C → L2 | Relink | 19.524 | +2480 | +4350 | 1008 | 1292885 |
| L2 → L2C | Relinked no-action control | 20.037 | +4240 | -641 | 1010 | 1279729 |
| L2C → exit | Incidental terminal | 10.228 | +1104 | +3164 | 1007 | 1283947 |

Cross-session unmatched extent is much larger than within-session extent under this alignment, despite similar total sizes. Remapped tokens/reordered data account for observable churn; this does not isolate how much is specifically caused by reload versus elapsed time. Within-session action/control region counts overlap, so broad diff volume does not establish link semantics.

## Preregistered literal result and bounded follow-up

The exact prior motif is `04 82 2c 5d 08 82 2d 48 04 82 2d a9`. Its exact-byte result is **PRESENT, ABSENT, ABSENT, ABSENT, ABSENT, ABSENT**. Initial analysis stopped at the first missing old beacon signature in L0C after archiving all inputs. Root-level L0/L0C decoded derivatives and original preregistration remain as partial-run artifacts. A fresh `analysis-01/` run retained missing old signatures as observations rather than erasing the failure. The original literal is not a build/session-independent detector.

Old B/E/P three-byte tokens have no occurrences in L0C–L2C; old T has one unrelated occurrence in each, the already-known collision class. Exit has an incidental old E byte occurrence outside the object neighborhood; no old E main signature. Raw token occurrence alone is not object identity.

**Post-preregistration exploratory matching**, explicitly not a retroactively registered test: find the prior role's base-like three bytes at main-prefix +15, require `3a` at prefix +0, the old four bytes at +4…+7, and the same candidate token at +1…+3 and +18…+20. This yields one match per role per sample, independently of whether the relationship payload is linked. Base-like bytes are B=`6c60e9`, T=`63aed9`, E=`45ef19`, P=`6031e1`; they are byte anchors, not newly decoded FormIDs. B's prior tuple remains at +104 and P's pre-move tuple remains at +50, corroborating correspondence. Prior and new relationship-adjacent tokens then correlate with those independently matched windows.

| Role candidate | L0 token | L0C–exit token | Matching result |
|---|---|---|---|
| B / beacon | `822c5d` | `81a650` | Unique window; prior B tuple retained |
| T / storage | `822d48` | `81a7a3` | Unique window throughout |
| E / extractor | `822da9` | `81a947` | Unique window throughout |
| P / solar | `822dba` | `81a94a` | Unique window; prior pre-move P tuple retained |

**OBSERVED:** token substitution between structurally corresponding windows. **INFERRED:** same logical objects across the reported reload. **HYPOTHESIZED:** a save-local reference index/remapping scheme; no index table has been decoded, and these are not proven runtime handles/FormIDs. Cross-session mapping is narrower evidence than resolved identity.

## Lifecycle and exact locations

All locations below and in the [candidate ledger](output-link-validation/candidates.csv) are **zero-based decoded-stream byte offsets**, never compressed-file offsets or runtime addresses. The envelope marker is `79 00 00 00`, followed by a little-endian uint32 candidate payload length, then the payload. At its computed end is `7a 00 00 00 28 00 00 00`. Marker values are not asserted to be schema/type IDs.

| Sample | Original literal | Token-substituted 12-byte literal | Corresponding endpoint pair in payload | Payload offset | Length | Discriminator byte | Pair offset |
|---|---|---|---|---:|---:|---:|---:|
| S3C historical | Absent | Absent | Absent | 426970 | 12 | `04` | — |
| S4 historical | Present | Present | Present | 425499 | 19 | `08` | 425504 |
| L0 = S4C | Present | Present | Present | 425676 | 19 | `08` | 425681 |
| L0C | Absent | Absent (entry order differs) | Present | 425510 | 19 | `08` | 425522 |
| L1 | Absent | Absent | Absent | 425510 | 12 | `04` | — |
| L1C | Absent | Absent | Absent | 425510 | 12 | `04` | — |
| L2 | Absent | Present | Present | 426830 | 19 | `08` | 426835 |
| L2C | Absent | Present | Present | 426826 | 19 | `08` | 426831 |
| exit incidental | Absent | Present | Present | 425248 | 19 | `08` | 425253 |

The original logical candidate is therefore **changed/remapped/reordered at L0C**, absent as an endpoint-pair entry in L1/L1C, and restored under the new tokens in L2/L2C. It is incorrect to report the exact prior literal as present throughout linked states.

Bounded payload observations, grouped for readability (grouping is an inferred entry interpretation):

```text
S3C: 04 822c5d 04 | 000000 04 679bc3
S4:  04 822c5d 08 | 822d48 04 822da9 | 000000 04 679bc3
L0:  04 822c5d 08 | 822d48 04 822da9 | 000000 04 679bc3
L0C: 04 81a650 08 | 000000 04 679bc3 | 81a7a3 04 81a947
L1:  04 81a650 04 | 000000 04 679bc3
L1C: 04 81a650 04 | 000000 04 679bc3
L2:  04 81a650 08 | 81a7a3 04 81a947 | 000000 04 679bc3
L2C: 04 81a650 08 | 81a7a3 04 81a947 | 000000 04 679bc3
```

The L0C/L1 envelope starts at the same offset. Unlink reduces the adjacent length from 19 to 12, changes payload +4 from `08` to `04`, and removes exactly `81 a7 a3 04 81 a9 47`; the other seven-byte group is unchanged. L1C → L2 reverses these changes, with the returning group before the retained group. L1/L1C payloads are byte-identical; L2/L2C payloads are byte-identical. Substituting role tokens and ignoring the order of the two seven-byte groups makes S4/L0/L0C/L2/L2C comparable; this is a stated normalization hypothesis, not evidence that all serialized ordering is irrelevant. S3C → S4 has the same 12→19 length and `04`→`08` discriminator transition and adds the corresponding historical endpoint pair.

**Cross-session result:** the logical pair survives in the corresponding bounded payload under changed tokens/order. The literal motif does not survive. This supports persisted relationship association across the reported reload, but cannot distinguish authoritative load input from a cached or reconstructed representation saved again.

## Endpoint persistence and background state

All four new tokens and matched main windows persist L0C–exit. [Exact offsets, token multiplicities and window hashes](output-link-validation/candidates.csv) preserve the independent checks. B occurs 26 times and P four times throughout. Within the new session, T counts **4/3/3/4/4** and E counts **6/5/5/6/6** across L0C/L1/L1C/L2/L2C: each loses exactly one occurrence at unlink and regains one at relink, while its main window remains. Historical T count five includes the old collision and is not directly comparable to the new token count. This is relationship change with endpoint-candidate persistence, not the S7 endpoint-deletion confound.

Fixed 512-byte windows anchored at the matched main prefix provide descriptive secondary checks, **not decoded record boundaries**. [Window comparison CSV](output-link-validation/endpoint-windows.csv):

| Transition | B unequal positions | T | E | P |
|---|---:|---:|---:|---:|
| Unlink | 16 | 0 | 337 | 27 |
| Unlinked control | 16 | 0 | 11 | 27 |
| Relink | 12 | 7 | 340 | 23 |
| Relinked control | 13 | 0 | 8 | 20 |

Extractor-window changes are larger in actions than controls, but internal shifts inflate positional differences: E-to-P main-prefix spacing is 568 bytes linked and 582 unlinked. This does not establish a 14-byte field or one complete extractor record. E header-adjacent bytes also reverse, while other bytes vary in controls. Storage's first 512 bytes are identical on unlink and both controls; seven positions change on relink, including +103. No resource/count/timer schema was decoded, so these remain possible production, transfer or inventory confounds. The separate bounded relationship payload reverses cleanly and remains exact in controls despite these continuing window changes. No claim that every action difference encodes the output link is supported.

## Representation, confidence and alternatives

Best-supported description: **a separate serialized relationship/collection candidate region containing a beacon-like token and an entry pairing storage/extractor-like tokens**. It is far from the matched main object windows (decoded chunk 1 versus chunk 4), and its length/entry/discriminator changes reverse with the link. This favors a separate relationship/list representation over finding the motif exclusively within either main endpoint window. Physical separation does **not** establish logical ownership or absence of mirrors elsewhere.

- **OBSERVED / PROVEN within these inputs / SAVE:** byte locations, repeated framing, literal mismatch, remapped candidate windows, seven-byte removal/reappearance, length/discriminator transitions, control equality and historical comparison.
- **INFERRED / proposed STRONG association, pending review:** saved local output-link relationship state. Original creation, link-only removal/recreation, endpoint persistence and steady controls support it; ordinary no-action churn does not explain this repeated pattern.
- **HYPOTHESIZED / PROVISIONAL:** token remapping denotes the same objects; `04`/`08` encodes one/two seven-byte entries (possibly a shifted/variable-length count); beacon ownership of the list; the retained `000000 04 679bc3` group's purpose. Count encoding needs more cardinalities. Storage-before-extractor byte order does not establish runtime direction.
- **UNKNOWN:** extractor-owned, storage-owned, mirrored, workshop-owned, or independent logical owner; consumers and authoritative state after load; cached/event/script versus primary relationship representation; full record framing; runtime identity map; production semantics; safe integration. No live function/field is qualified.

Alternatives retained: a cache or link-event-derived structure can follow the same actions; reload may regenerate this representation from another authority; corresponding windows could be related references/children instead of principal objects; additional copies may exist outside searched windows. A coincident production representation is less persuasive given the exact returning endpoint-pair group, unchanged endpoint windows and stable controls, but is not categorically excluded. A strict byte-signature hypothesis is rejected across sessions; the broader output-link hypothesis is strengthened, not rejected.

Recommendation: **PROMOTE for review** only the bounded output-relationship semantic association; retain provisional ownership/count/identity details. Smallest next step, proposed only: use these same archived samples to examine the containing region's boundary/reference-table mapping, testing token resolution independently of this motif before asserting owner or direction. A separate additional-link cardinality experiment would be needed to test the count hypothesis; no live experiment is authorized or begun here. Broad parsing infrastructure is unnecessary.

## Review package

[Validation and complete file inventory](output-link-validation/validation.md); [script usage and effects](../../save-analysis/scripts/README.md). Local evidence root contains the exact manifest/preregistration; initial partial derivatives; seven final decoded streams and `analysis-01/analysis.json`; `structure.json`; `build_review_tables.py`; `validate_review.py`; final preservation/check results, artifact inventory, Git status and **tracked-plus-untracked `review.diff`**. No source/decoded blob or bulk window dump is included in the authored review diff. Selected CSVs and short payload observations still require publication review. The pre-existing supplied brief contains personal filenames and remains unchanged/unreviewed for publication.

Sources: project's SOR-EXP-0003 candidate discovery and existing project-authored decoder/diff; installed CPython/zlib facilities SOR-S-0113; Bethesda locally owned save inputs (SOR-S-0104 provenance). No third-party code reuse, new dependency, outside contact or permission blocker arose. No staging, commit, push or live-save cleanup occurred. This completion is not approval to integrate or widen scope.

Suggested commit message, only if later approved: `research: validate outpost output-link serialization`.
