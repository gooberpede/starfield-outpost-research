# Versioned bridge and comparison contracts

Authoritative validators live in [bridge.py](../../../research/blinded-outpost-validation/bridge.py),
[compare.py](../../../research/blinded-outpost-validation/compare.py) and
[gate.py](../../../research/blinded-outpost-validation/gate.py).
These strict, versioned Python schemas reject unrecognized fields. JSON is UTF-8;
duplicate keys and NaN/Infinity are rejected. Canonical project JSON uses CPython
sorted keys, compact separators, `allow_nan=False` and one final LF. Freeze hashes
bind literal file bytes, independently of payload interpretation.

## Location-only transfer: `sor-blind-location/1`

| Field | Exact domain and meaning |
|---|---|
| `schema` | Literal version above |
| `trial` | 32 lowercase hexadecimal characters; independently assigned trial identity |
| `body` / `body_formid` | Kreet/Vectera/Jemison and exact observed installed PNDT FormID, eight lowercase hex digits; not a runtime pointer |
| `workshop` | Eight saved Workshop identity bytes, 16 lowercase hex characters; not a native address |
| `beacon_token` | Three-byte saved reference token, six lowercase hex characters; not a FormID or handle |
| `position_le` | Raw saved XYZ, 12 little-endian binary32 bytes encoded as 24 lowercase hex characters; native local units |
| `compensation_le` | Raw saved Workshop compensation XYZ in the same encoding; separate from raw reference position |
| `frame` | Integer saved frame `0x0b` or `0x2b`; the JSON value is decimal 11 or 43 |
| `chart` / `descriptor` | Interior chart 0/1 and two integer fine-grid base coordinates in [0,49151], divisible by 96; conditional saved source/site base, not an observed loaded-frame transform |
| `effective` | Literal `UNKNOWN`; asserting effective native qualification is rejected in this version |
| `receipt` | SHA-256 of the custodian's exact operand/provenance receipt; no raw path, name or arbitrary text |

The custodian retains decoded-stream offsets, parent/world joins, source hashes,
qualification and full reconstruction privately. Only the filtered location is
released. `saved_adapter.py` delegates branch-aware reconstruction to unchanged
`durable_position_v2.py`; duplicate Workshop matches, missing qualified site,
unsupported chart/frame/body and ambiguous operands fail explicitly. The table
adapter also checks installed EXE/ESM/PlanetData identities. Neither adapter reads
a new raw save or proves future engine authority. Float bits retain signed zero
and precision; subnormal/effective arithmetic inherits the existing reproducer's
restricted domain. No fitted resource-derived coordinate is admissible.

## Prediction and truth

`sor-blind-prediction/1` is the current candidate runner's explicit unsupported
result. It retains the exact location, reason and empty source/presence maps,
`scope_complete=false`, with Special helium-3, terrestrial Water and atmosphere
UNKNOWN. Empty maps never mean no resources.

`sor-blind-comparable/1` represents qualified source-context comparisons. It binds
trial, body, installed body identity, Workshop, session and evaluation-context
token, scope completeness and unique source keys. A source key is
`chart:anchorX:anchorY:SFBK`, with explicitly scoped fine-grid coordinates and a
main-file SFBK FormID. It is not a source pointer or native lifetime witness.
Each source retains sorted unique mask alternatives with ordered region arrays
and unique ordinary admission resource identities. `conditional.py` additionally
retains exact ordinary weight bytes, full modeled paths, area intersections and
separate spatial admission calculations. External source-support qualification
is required; mask alternatives are never chosen from the beacon's tile alone.

`sor-blind-truth/1` binds the same identities plus oracle and completeness. Only
synthetic Workshop truth may claim complete coverage in this revision. Native
ordinary Workshop evidence must have `complete=false`; native complete claims
are rejected. Saved equipment, screenshots and X-Tech are rejected as exhaustive
oracles. Every region carries IRES identity, complete ordered little-endian XYZW
point/width bytes and four binary32 native bound words. Complete synthetic
sequences compare order, counts, identities and all bytes, including signed zero.

Native selected positives compare each observed region against every retained
alternative and report exact predicted ordinals. This is useful partial
correspondence; missing regions/resources and source census remain UNKNOWN.
Each alternative separately reports observed positive resources admitted or
unpredicted by its admission model. Per-resource modeling is all/some/none within
qualified complete scope, or UNKNOWN; unobserved resources remain UNKNOWN in
partial truth. Matching geometry never hides a modeled admission disagreement.
The independent full-journal adapter's `sor-blind-positive/1` retains ACK ordering,
query/radius/upper bits, source/Workshop joins and positive controls, with
`complete=false` and native lifetime epoch UNKNOWN. Evaluation-context tokens
are observer bookkeeping, not engine generation epochs. Incomplete or inconsistent
Workshop/session/context acquisition cannot become a scientific negative.
Its `gaps` diagnostic sums invalidations across resource replays; it is not a
unique engine-event or native-lifetime count. Accepted truth regions must have
nonempty point arrays and their resource must occur in positive presence.

## Freeze and revelation

`sor-blind-protocol/1` binds exact eligibility, transforms, comparison, collector,
installed-input, corpus, dependency and method artifacts. Actual worker, the
participating inference/gate/collector methods, unchanged owned modules and exact
runtime contents are mandatory dependencies. A synthetic fixture runtime is
explicitly nonexecutable and cannot freeze a candidate-body prediction. The
AppContainer mode accepts only this version's unsupported location runner.

The independent gate compares an externally supplied inventory digest before
exclusive trial creation, copies a sealed snapshot, fsyncs exact files and records
host time. Its freeze hash must be independently retained before any reveal.
Reveal rechecks live method/dependency bytes, original and sealed bundle
inventories, runtime files and independently expected truth bytes. It reserves
one revelation directory; a crash leaves an incomplete trial. Revised tools or
predictions cannot overwrite the original trial or backdate a client-supplied
timestamp. A trusted custodian/admin can still tamper with its own storage; the
external witness and access separation are essential parts of the contract.
