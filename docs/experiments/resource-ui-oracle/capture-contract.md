# Minimum native resource receipt: sor-resource-oracle/1

[Method](methods.md), [dataflow](dataflow.md), [scientific interpretation](pilot-plan.md).
Design contract; only its synthetic transport subset is implemented.

Every value has OBSERVED / UNOBSERVED / INVALID / NOT_EVALUATED status and domain.
Observed empty is a complete zero-count read, never a failed or skipped read.
Each native event is its own immutable external byte copy. The collector never
queues native pointers for later dereferencing.

| Group | Minimum evidence and claim boundary |
|---|---|
| Session | Schema; nonce; executable/hash/version and measured module base; instruction-byte guard digest at each breakpoint; collector/build/load-map/config hashes; protected Save52 master and disposable input SHA256; monotonic clock frequency plus diagnostic wall time; platform/debug intervention and freeze periods. |
| Event | Process/thread IDs plus lifetime token, per-thread sequence/nesting and call-return stack, site RVA, original register snapshot, begin/end/read/LOSS status. No pointer reused as a permanent identity. |
| Workshop context | Saved PNDT/Workshop bytes/beacon/parent/extractor/base/IRES joins from cases; separate resolved runtime references, handles, FormIDs and plugin-qualified identities; witness/lookup result for owner relation and current selected Workshop. Decode saved tokens with the qualified load remapping, never substitute them for runtime IDs. A screenshot/name/coordinate-only association is SITE_ONLY, not BOUND. |
| Updater | RCX=S, RDX descriptor24 bytes with XYZ raw f32 bits/index/domain, XMM2 radius/XMM3 upper raw words; O=S-520 only after caller/identity validation. Established caller reference and descriptor provenance; per-list branch history, last ATMO/BIOM IDs and retained indexed XYZ/domain. Capture scalar values without assigning unverified units. |
| Populations | Spatial/atmosphere/raw-biome source tag; header begin/end/capacity; complete ordered member pointer tokens copied now; each resource header FormID+28/type+2e and load-map-qualified IRES identity. Keep duplicate entries and pointer identity separately from numeric IDs. Bounds, read length, error, captured count, claimed count and payload digest per list. Resource type must be 9f for this IRES claim. |
| Freshness | For each list THIS_REFRESH_REPLACED / RETAINED_UNCHANGED_ID / RETAINED_MISSING_PROVIDER / RETAINED_SPATIAL_GUARD / UNKNOWN; actual executed branch RVAs and updater token. Begin/return plus AL alone yields UNKNOWN. Last ATMO/BIOM ID equality is not branch observation. Current list refresh and underlying map generation age are separate fields; latter UNKNOWN absent producer/lifecycle proof. |
| Catalogue | Builder invocation/category ID/node identity; at `1421f6b58` selected header RCX, produced range from frame; property branch trace, default/property identity and presence, exact intersection if reached, return AL at caller `1415796fc`. Node→concrete leaf/base/recipe mapping observed at constructor, append outcome and later condition results separately. Nonexecuted selector is BYPASS/NOT_EVALUATED, not an empty list. |
| Fold and rows | Ordered pointer-union of first two copied lists and Water-only append may be DERIVED_EXPECTED_FOLD. Actual `141578500` input/return/row constructor events are OBSERVED only if separately collected; raw biome membership is not automatically displayed. Record actual water operand. Actual catalogue and area typed rows have separate census/epoch fields. Unobserved census is null/UNOBSERVED, never derived as observed. |
| Relations | Explicit SAME_SYNCHRONOUS_CALL / COMPLETE_WRITER_INTERVAL / CORRESPONDENCE_ONLY / UNKNOWN links. Equal sets, header rereads, same pointer or close times never certify cross-event ancestry, absence of ABA or no resets. |
| Terminal | Numbered frames, schema/length and SHA256; END and sticky LOSS/partial state; raw file byte count/digest, close+OS flush result and independent full readback ACK. Capture process outcome separately. ACK is OS-flushed/readback evidence, not immunity to hardware/power failure. |

Live decoder must require session/build/identity and member type/load-map
validation before binding scientific claims. The prototype tests accounting with
invented fixture IDs; it does not implement those native validation checks.

Copy policy: verify unsigned 64-bit arithmetic, `begin<=end<=cap`, eight-byte
alignment and exact byte count, readable committed ranges via external guarded
reads. Null/all-zero header may represent known empty only in an initialized,
validated operation. Copy header, bounded pointer bytes and each resource header
while the debug event holds execution; preserve the raw evidence locally.
External read failure does not dereference memory inside Starfield. OS-readable
bytes still require semantic validation: a freed/reused object is INVALID or
UNKNOWN, never valid merely because its page is readable. Quiescence prevents
concurrent writes during the stop, not pre-stop dangling pointers or past ABA.

Prototype limits 4,096 pointers/list and 1 MiB/frame are transport budgets,
**not** game maxima or scientific event quotas. Overflow emits LOSS/refuses the
complete claim; qualify a larger transport offline if required. No silent
truncation, count clamping or fabricated absence. For a positive single member,
a fully validated observed prefix may support that positive only; this prototype
conservatively refuses classification if any list is incomplete.

Separate an invocation's witnessed replacement path from the ancestry of a shared
snapshot at its return: other writers can run between debug stops. Prefer the
SPATIAL_REFRESH_PAYLOAD copy at `1421e0bf4`, RDX stack-local vector header, for
direct scan-output attribution; it does not certify a later shared vector's age.
No all-thread single-stepping/exclusion is implied by Windows all-stop events.

After resuming, do not claim the three lists remain coherent or still feed the
later consumer. A complete stopped sample supports that instant. An updater
refresh receipt supports its own descriptor; a later gate receipt supports its
own selected input. Fully joined freshness at the gate requires uninterrupted
coverage of every relevant writer/reset/owner transition, not currently proven.
The primary spatial probe remains useful without that stronger join.

Loss/unknown rules: bad framing/digest/sequence, missing END, failed flush,
unwitnessed identity, out-of-budget list, unreadable resource, unexpected exit,
unmatched return or conflicting writer invalidates the affected claim. Preserve
intact independent groups and the failure. No successful-capture status is
awarded for another screenshot or a receipt with population origin unbound.
