# D5AR resident snapshot interchange, version 1

2026-11-05, Australia/Sydney. **Raw representation and offline native producer
controls implemented; scientific qualification is separate.** The [decoder/comparator](../../../research/resource-retained-population/d5ar_snapshot.py)
reads explicit files only. It cannot read Starfield memory or certify a command,
current outpost, native lifetime, geographic completeness or historical mask.
The [controls](../../../research/resource-retained-population/d5ar_qualify.py)
use owned synthetic inputs. Authored code/specification is REVIEW-REQUIRED;
raw reference/session/native material remains LOCAL-ONLY.

## Meaning and qualification

Schema is `sor-d5ar-resident-snapshot/1`; method is `sor-d5ar-offline/0.1.0`.
Scope is exactly `RESIDENT_MAP_CENSUS_AREA_ASSOCIATION_UNKNOWN`. Evidence basis
is `SYNTHETIC` or `UNQUALIFIED_NATIVE`. Version 1 deliberately cannot accept
`QUALIFIED_NATIVE`. A separately versioned derivation method must authenticate
the exact producer contract and required source/frame premises; a hand-written
field cannot supply that proof. The [source-planar proof](d5ar-source-frame-proof.md)
does not change this frozen raw schema or historical D5AI contracts.

This format can preserve a copied resident-map census, including raw geometry
whose source/frame is unknown. It does not establish that a producer actually
enumerated the map. Owned fixtures and exact-DLL controls are distinct from retail
observations; no D5AR retail capture exists. A map census cannot
be called an outpost census or a resource-absence certificate.

## Canonical envelope and raw preservation

UTF-8 JSON has unique field names. Writers emit sorted keys, ASCII escaping,
compact separators, no nonfinite JSON literals and one terminal LF. Readers
reject duplicate JSON fields, unsupported schema/method, incomplete arrays,
duplicate map entries/allocation IDs and unknown schema fields. Geometry floats
are stored as original hexadecimal byte strings, preserving signed zero, unknown
fourth point words and nonfinite bit patterns. Typed fixture frames must be valid.

| Field | Representation and validation |
| --- | --- |
| `schema`, `method` | Exact strings above; unknown semantic fields require revision. |
| `capture_id`, `session_id` | Canonical UUID strings. UUID is distinct from PID, runtime pointer and saved identity. |
| `utc` | Accepted invocation UTC `YYYY-MM-DDTHH:MM:SS.ffffffZ`, exactly six subsecond digits. The actual callback may occur later. |
| `process` | Positive u32 `pid`, positive u64 `creation_filetime`; both required. Synthetic values are fixture premises, not observed process certificates. |
| `build` | Exact `game_version` 1.16.244.0 and four 32-byte lowercase hex hashes: `game_exe_sha256`, `sfse_sha256`, `plugin_sha256`, `source_lock_sha256`. Hash-shaped strings alone authenticate no producer. |
| `scope`, `evidence_basis` | Restricted values above. No full-outpost coverage claim is accepted. |
| `outpost` | `status`: UNKNOWN, ABSENT_UNPROVEN, AMBIGUOUS, SOURCE_REPORTED or ACTIVE_ESTABLISHED_OPERATION_REFERENCE; `reference`: diagnostic string or null; `area_context`: diagnostic object. No status proves unique player membership or absence. |
| `status` | COPIED_UNQUALIFIED or REFUSED. REFUSED never participates in represented-content equality. |
| `capture_diagnostics` | Original `copy_status`, u64 `copy_begin_filetime`, `copy_end_filetime`, `epoch_begin`, `epoch_end`, `lock_state`, `required_bytes` and diagnostic `proc_identity_token` string/null. Zero copy FILETIME means unobserved; otherwise preserve actual UTC copy window independently of invocation time. Wall-clock adjustment is diagnostic, not geometric corruption. Preserve actual refusal code; copied status must agree. Epoch/lock integers are diagnostics, not independent native proof. |
| `owner_context` | Separate `before`/`after` observations, each with `status`, `complete`, `manager_pointer_token`, `attached_proc_token`, raw little-endian `owner_formid_word`, `mode`, and `current_descriptor_bytes`. Complete OBSERVED_UNQUALIFIED observations preserve all 44 descriptor bytes; NOT_CAPTURED/NO_MANAGER/READ_FAILED/READ_EXCEPTION retain null payloads. Repeated equal observations alone are not a lease or ABA exclusion. |
| `sources` | Ordered array preserving every reported map-entry disposition. Each entry has the fields below. |
| `payload_sha256` | SHA-256 over the canonical encoding of all other envelope fields. This is an integrity checksum, not an origin signature or semantic proof. |

Each source contains separate `allocation_id`, `map_entry_id`, `holder_id` and
`owning_grid` domains: nonempty strings or null, with a required unique map entry.
They are diagnostic/invocation-local tokens until native proof qualifies them;
their spelling cannot turn an address into a lease. `source_disposition` is
IDENTIFIED, ALLOCATION_UNKNOWN, EMPTY, MALFORMED or COPY_FAILED.
`area_association` is exactly UNKNOWN. `geometry` is null or the complete owned
payload below. `geometry_sha256` hashes that payload's canonical JSON, or is
null when payload is absent. Failed/empty dispositions cannot carry comparable
geometry. An ALLOCATION_UNKNOWN entry may preserve healthy raw arrays with a
null geographic source; this does not discard unknown resident populations.

`source_diagnostics` preserves `status`, `semantic_bytes`, `visited_token`.
NOT_CAPTURED or READ_FAILED carries null payloads. SOURCE_BYTES_UNQUALIFIED
contains 29 raw bytes concatenating terrain FormID, chart byte and the six
original coordinate words at source offsets `0x00`, `0x38`, `0x3c`, `0x40`,
`0x4c`, `0x50`, `0x5c`, `0x60`; the separate u64 token comes from `0x68`.
These checked raw reads are diagnostics, never an allocation lease, geographic
source certificate or sampled mask. Padding and mutable dimensions are excluded
from this selected diagnostic; it does not claim a whole-source memory dump.

The same diagnostic separately preserves `origin_status` and `origin_input_words`:
16 original bytes from source `0x10`, `0x14`, `0x20`, `0x24`, with
SOURCE_ORIGIN_WORDS_UNQUALIFIED or null payload for NOT_CAPTURED/READ_FAILED.
The provider consumes these words to form the ordinary generator origin, but
their observation does not itself prove source lifetime, immutability or historical
construction inputs. Geographic/token and origin-read failures remain separate;
neither failure discards successfully copied resource geometry.

`descriptor_status` and `source_descriptor_bytes` separately preserve the full
44 source bytes at `+0x38`: SOURCE_DESCRIPTOR_UNQUALIFIED, or null for
NOT_CAPTURED/READ_FAILED. These include fields absent from the selected 29-byte
geographic diagnostic and all three padding bytes. The separately versioned
source-planar derivation can exclude only the proved three padding bytes after
the chart byte. It requires the remaining complete 41-byte descriptor, terrain,
body and four origin words, plus the current-map/source-lifetime proof. Failure
of this diagnostic preserves otherwise healthy geometry with UNKNOWN comparison.

## Nested geometry and normalization

Owned geometry follows the [D5AI contract](d5ai-geometry-schema.md) and its
[native ownership proof](d5ai-source-lifecycle-map.md), reused under SOR-P-0002.
Its exact fields are `schema`, `session_id`, `snapshot_id`, `source`, `frame`,
`capture`, `population`, `loss`, `generation_quality`. Session/capture identities
must bind the envelope. `capture` has exactly `complete`, `status`,
`resource_slots`, `region_total`, `point_total`; require complete/OK/zero loss.
This means traversal completeness as supplied, not intended generation success.
`generation_quality` preserves UNKNOWN, KNOWN_PARTIAL or SOURCE_REPORTED_SUCCESS.

`source` is null or exactly geographic `key` and eight-digit `body_formid`.
`frame` is null or the existing source-planar/consumed-descriptor-v1 contract.
A consumed descriptor's owner must agree with the source body. Unknown fields,
chart/seam scope or fabricated frame transforms are not silently accepted.

Source-ending admission adds two explicit refusal statuses without adding raw
payload fields: `SOURCE_LIFETIME_RETIRED` and `SOURCE_RECORDER_UNAVAILABLE`.
Either applies to all three source diagnostic groups together, with null
geography/visited, origin and descriptor payloads. The first includes permanent
conservative refusal of an address reused after retirement; the second includes
lost recorder coverage or insertion failure. Healthy holder geometry remains
losslessly available. These statuses never mean geographical resource absence.
The producer must synchronize the complete fixed source group against pre-free
address recording; checked RPM and a later epoch rejection alone are insufficient.
Copied source bytes concern that protected group-read interval and do not certify
continued source allocation lifetime afterward.
Current manager equality cannot manufacture a consumed construction descriptor.

For an actual established-operation call, the native producer additionally retains
owned area diagnostics: exact caller-live 24-byte indexed input, radius/upper
words, module-owned translation header count/pointer, index and caller/reference/
domain pointer values. It never follows the unleased reference/base/cell or
translation-vector pointers. Legacy reference/base/cell identity fields and
translation vector/application values are null; `translation_application_status`
is UNKNOWN_NOT_OBSERVED. HEADER_ONLY_UNQUALIFIED does not certify later vector
binding or predicate consumption. ACTIVE_ESTABLISHED_OPERATION_REFERENCE
identifies the original established operation's selected reference at native
return site at preferred static VA `0x1421b26c1`, image base `0x140000000`; it is not a native reference lease
or unique current player-outpost certificate. The reference field remains an
explicit runtime-pointer diagnostic. The retained header scalars supply no ABA
exclusion or actual later predicate-consumption proof.
Preview/other call sites cannot inherit this established-operation status.

The integrated producer also retains `area_context.selected_reference`. Its exact
fields are `status`, `invocation`, `command`, `epoch`, `reference_pointer_token`,
`formid_word`, `type`, `observations`, `active`, `copied`, `ambiguous`, `linked`,
`identity_time` and `post_release_allocation_continuity`. FormID is four original
little-endian bytes or null, type is an uninterpreted u8, and all flags are booleans.
Invocation/command/epoch are separate u64 domains. `active` and `linked` describe
the recorded observation, not a live lease when the file is read. The exact
native pre-release hook copies FormID/type under the original local reference
lease and links the same established-operation invocation/command/epoch/R14
operand. It neither adds nor retains an engine reference. The time claim is
NATIVE_RESOLVED_REFERENCE_LEASE_BEFORE_RELEASE; later allocation continuity stays
UNKNOWN, including equal-pointer/equal-FormID recycling. This is logical identity
at selection time, without unique player ownership or physical-area membership.

Each unique resource FormID carries its ordered regions. Each region preserves
all 24 original header bytes, u32 point count and all `count * 16` point bytes.
Header FormID at byte offset `0x10` must equal the resource key. Counts must match
the full arrays. No point rounding, region rotation, deduplication, coordinate
alignment or region/point reordering occurs. Raw hashes include padding.

Semantic normalization uses the existing owned D5AI method: sort unique resource
FormIDs because native resource-map slot order changes under rehash; preserve
region/point order. Compare header bytes `0x00..0x14` and every point byte.
Only header padding `0x15..0x17` is excluded under native copy proof at preferred
static VA `0x1407ac2f0`, image base `0x140000000`, Starfield 1.16.244.0.
Raw input still retains it. Nonfinite geometry can be stored but receives
RAW_GEOMETRY_NOT_COMPARABLE; no semantic equality is forced.

## Atomic publication and failures

`publish` is an **offline owned-file writer**, not plugin IO qualification. It
checks both caller-available drive floors, validates data, exclusively creates a
fresh `.partial`, writes, flushes and fsyncs it, rereads every byte and calls Windows
`MoveFileExW` with WRITE_THROUGH and without REPLACE_EXISTING. Existing output,
partial, missing directory or IO failure refuses; no file is overwritten,
deleted or recycled. A failed flush retains an identifiable partial. Both file
analysis entry points refuse `.partial` input even when all serialized bytes
and hashes are structurally valid. Renaming a partial cannot prove publication;
study admission also needs the original immutable file and attempt records. This is
atomic rename support on the tested Windows filesystem, not a guarantee against
all hardware/power failures. The native producer independently preflights headers
and point ranges before count-driven allocation, measures occupied holder/resource
and actual region/point capacity, and refuses genuine insufficient memory. Unused
native vector capacity is not a healthy-data quota. The [native record](d5ar-native-investigation.md)
documents the actual worker, read, cancellation and publication controls.

Names are sortable `YYYYMMDDTHHMMSS.ffffffZ_<session-uuid>_<capture-uuid>.snapshot.json`.
Timestamp is not the uniqueness key. Readers derive provenance from contents.
The compare call rejects duplicate capture UUIDs; the future series admission
must also reject duplicate attempts/process/session identities under its roster.
Repeated comparisons within one session are allowed outside a cold-start roster.

## Comparison outputs and reproduction

The comparator validates both entire files. It matches known geographic keys
only after rejecting ambiguous duplicate geographic identities, checks source,
owner, frame and build equality, then compares all normalized bytes. It reports
the first different normalized byte as a diagnostic. A hash is never the sole
equality test. Every unknown/failed/missing holder receives a disposition row;
it cannot disappear from output. Missing frame, source/build mismatch, REFUSED
or missing population gives UNAVAILABLE_INCOMPARABLE. Output always states
UNQUALIFIED_NO_NATIVE_CERTIFICATE and historical mask UNKNOWN.

EQUAL_REPRESENTED_BYTES and DIFFERENT_REPRESENTED_BYTES describe only the owned
representation. They do not assert native safety, intended generation success,
current outpost membership, complete geographic coverage, effective-input
equivalence or a sampled mask. The reference verifier separately authenticates
actual A0 against its independent raw-wire oracle and fixed-native controls;
it refuses to promote content-only equality across distinct unqualified frames.

The decoder's `--feynman` option selects raw diagnostic candidates for
`0:37536:20928:0029d20e` only offline. Its key arithmetic follows owned
`read_capture.py`: each signed axis combines coarse, intermediate and fine words
as `coarse * 192 + intermediate * 12 + fine`. A matching diagnostic is not a
native source/frame/outpost certificate. All version-1 diagnostic selections
remain UNAVAILABLE/INCONCLUSIVE with sampled mask UNKNOWN; absent or unreadable
candidates prove no geographic resource absence. The producer embeds no Feynman
key, resource list or target population count.

## Separate represented source-planar method

[d5ar_source_frames.py](../../../research/resource-retained-population/d5ar_source_frames.py)
implements `sor-d5ar-source-planar/1`, independently of the frozen raw comparator.
It admits only its exact pinned producer build/source-lock profile and the
reviewed ordinary lifecycle graph, synchronized owner/map admission and complete
source-ending history, stable foreign-reader/current-map/body premises, complete
source diagnostics and established owner mode 2. Older producer checkpoints are
refused. The exact lifecycle-gated `NATIVE_BUILD` profile remains REVIEW-REQUIRED;
synthetic controls do not establish retail acquisition provenance.
Checksums are not signatures: authenticated acquisition
provenance and the external pilot/roster gates are still required. Synthetic
premises and owned exact-DLL outputs retain SYNTHETIC_ONLY role.

The separate basis record contains `basis` = native-source-planar-v1,
`game_exe_sha256`, `geographic_key`, `body_formid`, `terrain_formid`, full
`descriptor_semantic41`, all `origin_input_words16` and derived `native_origin_i32`.
The selected 29-byte geography must agree with the complete descriptor. Native
signed-dword arithmetic is modeled explicitly; origin conversion is admitted
only when its integer is exactly representable as binary32, avoiding an invented
MXCSR rounding mode. Other healthy raw captures remain preserved with an
unqualified basis. No region/point data is truncated.

The versioned normalized stream is prefix `SOR-D5AR-SOURCE-PLANAR`, bytes 0 and 1,
u32 little-endian canonical-frame-JSON length, that ASCII JSON, then u32
little-endian resource count. Each numerically sorted resource has its u32
big-endian FormID and u32 little-endian region count. Each ordered region has
the original meaningful 21 header bytes, u32 little-endian point count, and all
original ordered 16-byte points. The big-endian resource key is an explicit
canonical encoding; native headers/points are copied unchanged. Both IEEE zero
signs in planar Z are admissible and remain different bits. Nonfinite/nonplanar
data remains raw and incomparable. An exact producer's completed EMPTY traversal
derives a zero-resource representation, without a geographical absence claim.

The reference path reauthenticates actual A0/allocation 932/Birth sequence 2082,
the original 5,090-byte normalization and both pinned fixed-native hosts with
their original/copied model inputs and successful execution receipts. Fixed
fixtures consume numeric origin only; no A0 descriptor is stamped onto them.
The original native writer theorem bridges their numeric plane to actual A0.
Classification additionally requires the captured complete source basis to equal
actual A0's, not just its combined key or geometry hash. Source identity, all
meaningful headers and every point word participate. Mask-dependent resource
weights may differ; hidden effective generation-input equivalence and historical
sampled mask remain UNKNOWN. The new derivative has its own digest and never
substitutes for the frozen historical normalization.

Output classes are MATCH_MASK0_REFERENCE, MATCH_MASK3_REFERENCE,
OTHER_QUALIFIED_GEOMETRY and UNAVAILABLE/INCONCLUSIVE. Missing/duplicate targets,
unidentified residents that could hide another target, wrong owner/frame and
unproved native profiles cannot match by content alone. Complete novel and empty
representations remain qualified geometry results. Geometry classification does
not itself adjudicate cold-study eligibility, outpost membership or authorization.

With the same pinned interpreter and `-E -B`, separate CLI forms are:

```text
research/resource-retained-population/d5ar_source_frames.py references .local-work/d5ar/FRESH-REFERENCES.json
research/resource-retained-population/d5ar_source_frames.py classify SNAPSHOT.json .local-work/d5ar/FRESH-RESULT.json
research/resource-retained-population/d5ar_source_frames.py compare LEFT.json RIGHT.json .local-work/d5ar/FRESH-RESULT.json
```

The classify command authenticates primary references itself; it accepts no
caller-supplied qualified flag or reference replacement. The
[adversarial controls](../../../research/resource-retained-population/d5ar_source_frame_qualify.py)
independently construct the normalized stream and challenge every premise.
CLI outputs must be fresh plain files in the ignored D5AR namespace because
reference bundles and derivation rows contain local-only raw geometry. A supplied
legacy frame overlay is outside this exact producer contract; it cannot replace
the independently derived basis or silently join a different historical frame.

With repository cwd and installed pinned CPython 3.14.3, use `-E -B`:

```text
research/resource-retained-population/d5ar_qualify.py .local-work/d5ar/FRESH-CONTROLS
research/resource-retained-population/d5ar_snapshot.py LEFT.json RIGHT.json --out FRESH-RESULT.json
research/resource-retained-population/d5ar_references.py .local-work/d5ar/FRESH-REFERENCES.json
```

The CLI writes an exclusive result and refuses optimized or inherited-optimized
execution before sensitive imports. Source docstrings declare inputs/outputs and
effects. No command here deploys a plugin or touches a game process.
