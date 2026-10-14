# Record-level cross-session comparison

[Scientific report](report.md), [ten selected raw records](ledger.csv),
[source hashes](sources.csv), [all patched-site coverage](coverage.csv).
The complete forty historical returns and eight selected later records are
retained locally as `verification-03/ledger.json` under
`.local-work/cross-session-center/`. All fields are re-decoded from originals,
not copied from earlier report tables.

## Exact observations

| Workshop / boundary | Version | Sequence(s) | CALL RVA / return RVA | Raw file offset(s), decimal |
|---|---|---|---|---|
| SOR-002 historical center return | 050 | 94 | AD0C36 / AD0C3B | 1,652,424 |
| SOR-003 historical center return | 050 | 110 | AD0C36 / AD0C3B | 1,936,712 |
| SOR-002 initial setter before/after | 060 | 190897 / 190898 | 5A14DA / 5A14DF | 635,301,888 / 635,305,216 |
| SOR-003 initial setter before/after | 060 | 194235 / 194236 | 5A14DA / 5A14DF | 646,410,752 / 646,414,080 |
| SOR-003 first center return | 060 | 204750 | F4A1D4 / F4A1D9 | 681,404,672 |
| SOR-003 alternate caller center | 060 | 305746 | F498F1 / F498F6 | 1,017,519,360 |
| SOR-002 first center return | 060 | 321078 | F4A1D4 / F4A1D9 | 1,068,544,256 |
| SOR-002 alternate caller center | 060 | 372290 | F498F1 / F498F6 | 1,238,977,792 |

Five-byte CALL return addresses are distinct from the patched CALL instruction
addresses, native calleeF4AB80/B4E410 addresses and captured output pointers.
050 first grid records 96/112 used by earlier tables are downstream of actual
center records 94/110; this ledger deliberately names the native-return boundary.
The CSV records per-record SHA256, raw source path, invocation/parent, TID/QPC,
full binary32 XYZ bits, own pointers, flags and exact identity qualifiers.

| Field | SOR-002 050 / 060 | SOR-003 050 / 060 |
|---|---|---|
| ExtraWorkshop ID bytes | `f1517de43e171745` / same | `0efca066ee4c7b9b` / same |
| Reference runtime VA | `0x1fc2cb23340` / `0x1f7e3ea0000` | `0x1fc2cbaeee0` / `0x1f7e3f55b20` |
| Runtime FormID | FF01AB50 / FF01AA50 | FF01AB8F / FF01AA8F |
| Raw Z / actual center output bits | `54296940` / `efd19241` | `404318c1` / `7220ffc1` |
| Compensation XYZ | twelve zero bytes / same | twelve zero bytes / same |
| Own+B0 at centers | zero / `0x1f7d4126140` | zero / `0x1f7d432f040` |
| Own world sampled at centers | unavailable / `0x1f381b90260` | unavailable / `0x1f381b90260` |
| D3 at centers | NOT CAPTURED / 2 | NOT CAPTURED / 2 |
| 050 query source key | `02b20e79528028e0` | same |

050 key bytes appear little-endian as `e0288052790eb202`; key and byte-string
domains are explicit. Its enclosing query source is not the reference's own
parent. 060 world blobs end at+180 and cannot supply that+310 key. No identity
or frame join is inferred from numerical equality of differently typed IDs.

Save25 decompressed XYZ stream offsets are 1,344,574 /1,474,225; compensation
offsets 1,344,620 /1,474,271. They are not offsets into the compressed original.
Saved reference tokens 822821 /84B985 are not runtime FormIDs. Both setters have
zero before XYZ, input=exact saved XYZ, afterXYZ=input, D3=0 at both ends; no
Workshop extra or own parent is available there. Later base/FormID/pointer and
exact ExtraWorkshop ID support a retrospective candidate association. They do
not prove allocation birth, destruction absence or saved-token remapping.

## Integrity and interpretation

Original raw file hashes:

- 050: `751cc142fd1ff4fece4f24e2f878792c1e48fba12ab986b01cc70af1ce2cdd43`, 21,214,992 bytes.
- 060: `b44b345d8d47628c74b5c4df0eee998cdf7ae85e046cd4205a7bcddb61ed0f75`, 1,871,420,928 bytes.

050 offset=(sequence−1)×17768; 060 offset=(sequence−1)×3328. Every original
journal hash/extent and sequence is checked before interpreting selected fields.
060 before-output contents are never treated as native returns. All 40 historical
reference triples equal output, zero compensation; all 16,826 later output triples
equal respective Save25 triples. Four incoherent pairs are quarantined from
coherent identity/arithmetic claims as explained in the report.

The raw journal orders emission. Independent scan detects 60,264 adjacent
cross-thread QPC inversions in the complete 060 corpus. This does not imply
transport corruption or a total native store order. TLS ancestry is same-thread;
050 Q/E joins are validated with actual parent/thread/kind/begin sequence,
separately from any hypothetical cross-thread producer generation.

Confidence is direct for bytes and scoped center arithmetic, cross-validated
for saved numeric agreement, and qualified for retrospective continuity. The
selected initial setters have an explicitly inferred later Workshop association.
Their CSV `identity_scope` must not be read as direct ExtraWorkshop identity at
the early setter. No sampled address is dereferenced by this offline analysis.
