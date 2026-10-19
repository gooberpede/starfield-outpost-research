# Six protected Kreet checkpoints

[Exact sample hashes](samples.csv), [positive roots/positions](roots.csv),
[bulldozing channel rows](bulldozed.csv), [native correspondence](native.md).
All offsets in these tables are **decoded logical-stream** offsets; identities
are saved IDs resolved through each save's own tables, not runtime handles.

Six complete filenames were resolved in the actual user Documents save directory
and protected before decoding. `.local-work/l3-placement/baseline.json` binds
original paths/hashes to read-only copies. BCPS1/ZIP framing, all compressed
stream boundaries/EOF and zlib lengths/checksums were validated. Decoded hashes
and counts are in samples.csv. All six contain build string 1.16.244.0, format 27,
and buffer version 153. Filename dates do not establish a single linear chronology; the user
supplies the two scenario/action sequences. There is intentionally no Save32.

| Scenario | Baseline → beacon → completed | Supported roots | Bulldozed-channel REFR rows | Positive saved beacon / parent |
|---|---|---|---|---|
| SOR-004 / POI | Save30→31→33 | 0→1→3 | 0→1→4 | ff029ab6 / ff0193af |
| SOR-005 / clutter | Save34→35→36 | 0→1→3 | 0→1→12 | ff041cc1 / ff0327f4 |

The one initial root is the beacon PackIn's representative, not the activator
alone and not every generated child. Its base `015804` and construction
definition `29a8c6` reproduce the established
[native construction-root projection](../workshop-membership/schema.md).
Each completed input adds one single-root ACTI `2031e1` (OutpostPowerSolarArray03)
and one single-root base `05ef19` (Iron extractor, corroborated by established
extractor records and this user-described acquisition). The beacon and solar
physical definition fields/source offsets are retained in definition-details01.json.
The extractor's precise existing provenance is [E1 arithmetic/production](../inorganic-extractors/arithmetic-production.md):
CONT `0005ef19` at physical ESM byte offset 5,403,487, also in the [E1 definition table](../inorganic-extractors/definitions.md).
That earlier research uses the same freshly hash-pinned installed ESM. The beacon,
its dummy root and generated members must not be counted as separate buildings.

SOR-004 beacon position remains
`(23.853296279907227, -96.75476837158203, -2.5808780193328857)` in Save31/33;
SOR-005 remains
`(140.3616485595703, 318.734619140625, 19.341909408569336)` in Save35/36.
The two actual completed solar IDs are ff03aaa6 and ff042cdc; extractor IDs
are ff03aabe and ff042f7c. roots.csv preserves each raw representative XYZ, direct
owner, record span and saved disabled/deleted flags. All eight supported root
rows have both flags clear. This is positive saved state, not complete active
membership or guaranteed post-load semantics.

Each beacon's counted extras closes at its declared count. ExtraBC and owned
reader provenance are retained; resource registration goes from 0 to 1, and BF
budget AV `00000399` goes from 7 to 9 in both pairs, consistent with earlier L2.
No new L2 finding or quota test is implied. No explicit BF radius override for
AV `00063fc5` was decoded; the physical beacon definition supplies 150. Missing explicit saved radius is
not an absent effective radius.

The fresh independent arithmetic record walk agrees with the full framed-record
inventory in every save. Positive roots are supported under the existing
projection; complete constructed population remains false. The underlying
inventory records 167/167/167 and 165/166/166 prefix errors, other representations
and unresolved member roles. These are retained in each SaveNN.json, never
silently treated as absent objects. The targeted typed beacon scan has its own
prefix-gap ledger. No arbitrary parser error establishes absence of all outposts,
clipping data or suppression mechanisms.

Whole-save differential receipts compare resolved IDs plus body hash, reference
queues and change masks, not raw compressed offsets. Many unrelated records
change; there is no no-action save pair in this new acquisition. The useful
conclusion is the positive retained beacon/owner/position and added construction
and bulldozing representations, not that only those objects changed.

The mask `0x01000000` is native-named Workshop Bulldozed and is restored to
mask `0x04` at reference offset `0xd3` in the inspected loader. Most positive rows
are conditional case 7 with no inline base or XYZ; their one-byte body containing
`00` is not a Boolean clearing
flag. Disabled/deleted fields remain UNKNOWN where not saved. No positive row
is identified as the pictured boulder, shrub, gas vent, animal or rejected
candidate. Full rows and unsupported fields stay in the local channel receipt;
the authored metadata table retains only identity, span, mask and qualification.

Original hashes were checked after analysis and again by the final verifier;
copies were not modified. Temporary decoded scratch is closed/removed by the
existing streaming context. No save was loaded in Starfield, created or edited.
