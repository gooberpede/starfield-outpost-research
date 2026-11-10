# B2 candidate and standalone reader

**Local proposal, NOT CLEARED and unhosted.** The one proposed asset is
`SOR-D5BO-B2-projected-evidence-v1.zip` under `.local-work/d5bo/`.
It is 394,869 bytes, SHA-256
`098ddf7d67f6a23390932b3440faa489439235663bf315754697e40acf694224`.
The [schema](b2-schema.md) and [sufficiency review](b2-sufficiency.md)
describe what the projection retains.

| Member | Bytes | SHA-256 | Proposed file-specific scope |
| --- | ---: | --- | --- |
| `manifest.json` | 1,223 | `583b451e17f3b7b63d340063a422954ae9430cb0857d1ed46ee3418c883c85ba` | Authored metadata and minimum source fingerprints, schema and transport counters. No session nonce, private receipt payload, paths or PID. Rights/privacy review pending. |
| `events.json` | 2,043,258 | `652bf2ec70fd9bf241dcd423b06c3749d950d2445171e1fb82eab0688ca6adee` | First-party observer derivative. Frame timing, event context, limited game-derived operands and session-local equality labels. No raw frames, instructions, absolute runtime pointers, saves or geometry. Rights/privacy review pending. |

Exact QPC, invocation IDs, the target tuple/FormIDs and original requests
remain intentionally visible for the event check. This is a reduction of
the original disclosure surface. The exact member rights and privacy,
authorized transfer and retention, B6, hosting and hosted-byte checks
remain separate. The local directory and hash alone confer neither public
access nor independent backup custody.

With the exact candidate explicitly supplied, run this from a checkout
with standard-library CPython. No game or private originals are inputs.

```powershell
$asset = 'path-to-SOR-D5BO-B2-projected-evidence-v1.zip'
python -I -B research/resource-retained-population/d5bo_verify.py $asset --sha256 098ddf7d67f6a23390932b3440faa489439235663bf315754697e40acf694224
```

The reader computes the target allocation, both native decision orders,
miss/hit, mask and store, the repeated births, competing keys, 56 late
unqualified decisions, 390 later bypasses and reset/clear accounting.
It treats native insertion and transport/source authenticity as upstream
premises. To exercise the adverse controls, use `-E -B` with
`d5bo_controls.py` and the same arguments. Nineteen altered row tests,
one dropped-frame test, two claim promotion refusals and two package
identity refusals passed. Semantic tests bypass package identity to
reach their intended predicates. The initial late-token control used
the Grid column by mistake. Selecting the token by field name corrected
the test and demonstrated the intended refusal. The independent challenge
found three additional malformed return and map-key contexts. The revised
verifier checks the recorded last selection for each return and all lookup
keys against their selected source.

Local rebuild uses
`python -E -B research/resource-retained-population/d5bo_build.py <new-path.zip>`
under `.local-work/d5bo/`. The builder requires the actual pinned
attempt-002 session, original reader result and exact owned reader,
reducer, observer and decoder source. It pins the historical modules before
import and rechecks original framing and
reader equality before writing one new file exclusively. The ZIP uses
fixed order and timestamps and pinned-run DEFLATE compression. Use the
same CPython and compression runtime for exact byte rebuilds. Public
verification does not depend on rebuilding the private original.
