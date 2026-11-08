# D5AS geometry evidence access

The local candidate reproduces all 30 qualified full-body comparisons at the
Feynman V source on the Starfield 1.16.244.0 research baseline. Qualified
positions 7 and 13 match the fixed mask-0 geometry. The other 28 match fixed
mask 3. No qualified body differs from both references. The candidate asset is **PENDING
SPECIFIC APPROVAL** and currently **LOCAL-ONLY**. Public access to the complete
body comparisons depends on an approved asset or an approved scope change.
[Exact candidate and source index](d5as-manifest.json) ·
[Original series closeout](../../experiments/resource-retained-population/d5as-series-closeout.md).

The comparable source is `0:37536:20928:0029d20e`, on body FormID
`0x0005e0de` with a source-planar origin of `(-200,-200)`. The historical
capture census includes 31 snapshots and 99 startup receipts for 33 process
sessions. Two sessions have startup receipts only. Attempt 6, UUID
`7edfc207-4f95-4cdc-9617-ce847107c49c`, was excluded before classification.
The `SOURCE_LIFETIME_RETIRED` diagnostic for `map-entry-56` leaves one
resident entry unidentified, so the entry could conceal a competing target.
The initial 30 attempts yielded 29 qualified captures. Attempt 31 added the
replacement and three startup receipts, leaving all 126 initial artifacts
byte-identical. Pilot04 is a prior producer control outside this series.
[Prespecified eligibility and ordering](../../experiments/resource-retained-population/d5as-analysis-protocol.md) ·
[Producer and reference profile](../../experiments/resource-retained-population/d5as-producer-profile.md).

Full-body equality establishes a geometry proxy. The generating raster mask,
request winner, full effective-input equality and physical outpost association
remain unresolved. The fixed C1 census of 28 mask-0 and 168 mask-3 candidates
describes eligible request coordinates under its conditional model. Winner
probabilities remain unmeasured. Separate process starts and the operator's
reported route, save and deployment adherence have different evidence bases.
The observations do not establish IID. The version pin does not identify the
original save creation build or effective load order.
[Original acquisition and limits](../../experiments/resource-retained-population/d5as-series-closeout.md) ·
[Fixed request map](../../experiments/resource-retained-population/d5aq-request-mask-map.csv).

## Reader comparison

Use CPython 3.9 or later and the [standalone verifier](../../../research/evidence-access/d5be/d5as_verify.py).
From the checkout root, supply the ZIP explicitly and use the hash in the
[index](d5as-manifest.json). The file name below is a candidate basename, and
the command needs a separately supplied copy of that exact asset.

```text
python -I -B research/evidence-access/d5be/d5as_verify.py d5as-feynman-geometry-v1.zip --sha256 d0d35ed2193527dd8215a647178614a5403e814bf14c3f9d1f0a448c53a1043c --negative-controls
```

The verifier reads the ZIP without extraction and writes its result to stdout.
It needs the Python standard library and the explicit ZIP. An absent asset
fails the command. The tracked text alone explains
the method and pins the candidate but cannot reproduce the comparisons. The
output lists all 30 classifications and the count, fraction and marginal
95% binomial interval for each class. The conditional IID null with mask-0
proxy probability `1/7` gives inclusive tails of 0.177368 and 0.941150,
probability-ordered two-sided p-value 0.303654 and all-mask-3 probability
0.00980836. The three equal-tailed exact marginal intervals are 0.82–22.07%,
77.93–99.18% and 0–11.57% in the order mask 0, mask 3, other. They have no
simultaneous coverage or allowance for dependence or acquisition failures.
[Prespecified analysis and assumptions](../../experiments/resource-retained-population/d5as-analysis-protocol.md#prespecified-analysis).

The ZIP uses stored members with fixed metadata. Its UTF-8 `manifest.json`
declares schema `sor-d5be-d5as-geometry/1`, frame, original snapshot pins,
reference and sample member pins, chronological attempt ordinal, capture UUID,
qualified position, recorded class and the exclusion and replacement trace.
Process creation FILETIME, invocation UTC, session UUID and capture UUID were
the historical ordering keys. The candidate carries their resulting ordinals.
Original timing keys, startup IDs and process details stay in local custody.
The two reference members are `references/mask0.bin` and `references/mask3.bin`.
The qualified bodies occupy `samples/01.bin` through `samples/30.bin`, one
complete body per capture even when the bytes repeat. The excluded attempt has
an original snapshot pin and its reason, with no body or class.

| Field | Encoding |
| --- | --- |
| Body start | Little-endian unsigned 32-bit count of resources. |
| Resource record | Four FormID bytes in display order, followed by a little-endian unsigned 32-bit region count. Resource records appear in ascending numeric FormID order. |
| Region record | First 21 original header bytes in native order, then a little-endian unsigned 32-bit point count. The four-byte FormID embedded at header offset `0x10` is little-endian. Header bytes at offsets `0x15` through `0x17` are the excluded padding. |
| Point record | Every original 16-byte point in native order. Admission requires finite binary32 words in the four-word header group and each point. The third word in each group accepts either sign of zero. Fourth words are retained without assigning a semantic role. |

There is no coordinate transformation or rounding in body construction. The
verifier consumes every byte, checks the structure and member pins and compares
each complete body to both pinned reference bodies. The mask-0 body is 4,966
bytes and mask 3 is 4,858. The historical D5AK A0 normalization has two
length-prefixed JSON values followed by its body. Its 5,090-byte envelope and
the D5AR source-planar envelope occupy different byte domains. Byte offset 232
in the original A0 normalization is the start of the same 4,858-byte body as
fixed mask 3. The candidate domain is
`sor-d5as-feynman-source-geometry/1:canonical-body`.
[Original normalization and wire rules](../../experiments/resource-retained-population/d5as-producer-profile.md#pilot-and-byte-domains) ·
[Original snapshot schema](../../experiments/resource-retained-population/d5ar-snapshot-schema.md).

The optional negative controls change one bit in a point's fourth word while
updating the row hash, substitute a wrong domain and a synthetic envelope
prefix, remove a sample, duplicate a capture UUID and flip a recorded class.
Each control must fail at its intended structural or equality check. The
negative cases use in-memory copies and do not generate publication fixtures.
The package SHA-256 provides the separate whole-asset identity check.

## Local custody and derivation

The [local builder](../../../research/evidence-access/d5be/d5as_build.py) uses
the already authorized historical offline Python methods and retained evidence
under SOR-P-0002. It requires the existing Windows historical layout and
CPython 3.14.3 with `-E -B`. A fresh immediate child of the ignored staging
namespace receives the ZIP and local custody JSON. The builder stops on a
missing or changed input, archive inconsistency, wrong output location or a
disk-floor failure. It opens source evidence and protected Save52 witnesses
read-only. It does not extract original archive members to disk.

```text
python -E -B research/evidence-access/d5be/d5as_build.py .local-work/d5be/d5as-rebuild
```

The closeout ZIP has 15 payloads and an internal manifest. Its corpus member
and the loose ZIP agree, and each of the 130 corpus members matches the frozen
ledger pin and the corresponding loose file. The original pre-freeze review
pins the archive, eligibility ledger, authorization and before/after
protection receipts. The builder verifies those joins, replays the historical
eligibility method, and directly checks the original, loose backup and
restoration rehearsal for the recorded Save52 pin. The historical protection
receipts cover the wider protected population. D5BE's source guard hashes its
selected inputs before and after building. It does not rerun the broad
historical postflight or claim a new observation about other saves.
[Original custody and review pointers](../../experiments/resource-retained-population/d5as-series-closeout.md#protection-and-archive).

For each qualified row the builder independently decodes the geographic key
from each raw source diagnostic, selects the unique target and serializes the
selected native population with the field rules above. It compares the result
to the body stored in the frozen manifest. For the fixed bodies, the builder
checks four D5AQ/D5AG native outputs and the source/frame provenance using the
historical code. It serializes their population fields and checks all repeated
mask-3 cases. It validates 164 D5AK A0 archive payloads and the internal
manifest, checks exact loose counterparts for the decisive A0 inputs and
cross-checks the A0 geometry against the archived envelope's body. The fixed
hosts do not reproduce every historical effective generation input. The
custody receipt maps each original snapshot and startup-member set to its
attempt and derived body, and records exact source/member sizes and hashes.
[Fixed-reference evidence](../../experiments/resource-retained-population/d5aq-report.md) ·
[D5AG repeated geometry controls](../../experiments/resource-retained-population/d5ag-geometry-controls.md).

An earlier independent historical closeout reviewer also reconstructed every
body from the sealed captures and reproduced the statistics. D5BE's exact
snapshot requires a new independent review. The reader package permits a
separate check of its equality and statistical claims. Checking the upstream
custody chain, historical qualification and source-to-derivative fidelity
requires authorized access to the original witnesses and local receipt.

## Access decisions

The proposed tracked files are authored method, explanatory text and a hash
index under the project licence. The candidate contains full game-derived
geometry, FormIDs, capture UUIDs and original snapshot hashes. Those bytes
remain in controlled staging pending asset-specific rights, privacy and
maintainer selection. The proposed ZIP contains no raw snapshot JSON, game
binaries, save bytes, raw pointer or process tokens, private filesystem
paths, startup receipts, or operator notes. Historical original evidence and
the detailed custody receipt remain local-only. This removes those diagnostics
from public reader scope and keeps their relation to the original evidence
auditable by an authorized reviewer. There is no hosted asset URL.
[Project publication gate](../../PUBLICATION.md) ·
[Third-party policy](../../../THIRD_PARTY_POLICY.md).
