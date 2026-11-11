# D5AI complete represented geometry contract

2026-11-02, Australia/Sydney. Schema `sor-d5ai-geometry/1` is an offline
consumer contract. Qualification of a native producer is a separate obligation.
Parent D5R and gameplay GC-25/30/31 remain OPEN.

## Meaning and evidence boundary

A complete snapshot includes every occupied resource entry in the selected
resident holder, every region in each collection and every represented point.
Completeness of this traversal does not prove successful intended generation.
Native outer copy success can coexist with an empty or partial inner copy;
`generation_quality: UNKNOWN` preserves that distinction. Invalid, zero-length,
partial and failed populations must remain in raw evidence. A failed capture
cannot become a valid empty population.

The [normalizer and comparator](../../../research/resource-retained-population/d5ai_geometry.py)
read JSON files only. The separately qualified native sidecar must supply owned
bytes and independently justified capture, availability and lifetime certificates.
Hand-written `qualified: true` fields are fixture premises, not native proof.

## Fields and exact comparison

| Field | Contract |
|---|---|
| `schema` | Exact version string above. Historical B1 schema 2 and B2 schema 4 have no full geometry envelope; neither is upgraded by this schema. |
| `session_id`, `snapshot_id` | Nonempty observation identities. Lifetime certificates bind both observations. Continuous lifetime cannot cross sessions. |
| `source` | Geographic/content `key` and generator owner/body `body_formid`, eight lower-case hexadecimal digits. Neither is a runtime pointer or serialized reference. |
| `frame` | Fixed-stage fixtures use `basis: source-planar`, signed 32-bit `anchor_i32` and `origin_i32` pairs, plus four `clip_center_f32` and four `clip_half_f32` words. Each word is four original little-endian bytes in hexadecimal. Runtime captures instead use the descriptor contract below. Equal numbers in different frames are not a comparison. No translation is guessed. |
| `capture` | `complete`, `status`, occupied `resource_slots`, `region_total`, `point_total`. Counts must agree with full arrays. A complete capture requires `OK`; overflow, read failure, interruption and writer recursion are refusals. |
| `population` | All resource entries, each with eight-digit `resource` FormID and `regions`. Reject duplicate keys. Canonicalize resource keys by numeric FormID; resident hash-slot order is not construction order. |
| Region | Original 24-byte `header`, unsigned 32-bit point `count`, complete `points` bytes. Keep region order, duplicates and zero-length arrays. Header FormID at byte offset `0x10` must equal its resource key. |
| Point | All 16 original bytes, including the fourth binary32 word. Do not reduce a point to XYZ or discard unknown semantics. |
| `availability` | Qualified boundary, complete map scan, holder presence and actual consumer exposure are distinct fields. Query result membership is also distinct: an exposed population need not intersect the query point or area. |
| `loss` | Zero is required for a qualified comparison. This does not establish that all relevant native paths were instrumented. |
| `generation_quality` | Preserve known native failures or `UNKNOWN`; never derive successful intended geometry from a sampler, visited store or successful outer index. |

The native copy at preferred static VA `0x1407ac2f0`, image base
`0x140000000` on Starfield 1.16.244.0, writes header bytes `0x00..0x14`.
It does not initialize padding `0x15..0x17`. Preserve all raw bytes, compare
only the first 21 header bytes semantically, and retain all point bytes.
The [ownership map](d5ai-source-lifecycle-map.md) supplies exact native provenance.
Historical byte-equality findings remain historical; this prospective padding
rule does not rewrite their receipts.

No tolerance, rounding, sorting of regions/points, deduplication or polygon
rotation is applied. Signed zero remains distinct. NaN/infinity in typed point,
bound or fixed source-planar fixture frame floats refuse comparison while raw
evidence remains intact. Normalized bytes contain complete framed
content; SHA-256 is an integrity convenience, never the sole equality oracle.
Original envelope byte equality, normalized equality and population lifetime
continuity are separate results.

The runtime variant uses `basis: consumed-descriptor-v1`, `owner_formid`,
and 41 bytes of `descriptor_semantic`: original descriptor byte
`0x00` followed by bytes `0x04..0x2b`. Exclude only the three padding bytes
under the pinned native converter proof. The owner must agree with the source
body. Only the qualified chart-0 interior scope is accepted. Bind the actual
engine-consumed Descriptor event to Generating, its owner and output address
equal to captured holder plus `0x08`, then the normal Generated return. Require
qualified source allocation and uninterrupted holder lifetime through the scan.
This uses the construction's frame rather than inferring one from current
manager fields. Never substitute the fixed fixture frame or label holder
`+0x08` as an origin. Runtime generation clip/origin remains NOT_CAPTURED.
Different or absent consumed descriptor certificates refuse content comparison.
Descriptor payload words are integer coordinates and packed atlas/record data,
not ten binary32 coordinates. Preserve their exact bytes without interpreting
integer or packed bit patterns as NaN/infinity. The converter at preferred VA
`0x14078d660` uses integer arithmetic before conversion, and the descriptor
normalizer at `0x14096f5c0` uses integer quotient/remainder and packed-field
operations. Reviewed exports remain `.local-work/d5q/functions/14078d660-q.txt`
and `.local-work/d5u/native05/functions/14096f5c0.txt`; this clarification does
not change the measurement code.
A complete absent-map observation has no represented geometry frame; it carries
`frame: null` and can establish UNAVAILABLE without inventing construction or
comparing point coordinates. Current manager fields are retained as diagnostics.
The early current-descriptor double-read proposal is superseded: equal reads
alone do not exclude intervening mutation or ABA. The
[ownership map](d5ai-source-lifecycle-map.md#runtime-frame-certificate-and-rejected-current-state-shortcut) records
the native frame argument; exact represented points are compared without a
coordinate transformation.

## Qualified outcomes

First validate both complete representations and their source/frame contract.
A qualified consumer scan showing the expected holder is absent or unexposed
gives UNAVAILABLE at that boundary. Retained external storage does not by itself
establish exposure. Missing events, a cached area refresh, an unarmed recorder,
loss or unreadable geometry give INCONCLUSIVE, not absence.

For two exposed populations, independently establish CONTINUOUS or RECONSTRUCTED
lifetime from positively joined native history. Compare the full normalized
bytes. Continuous and equal gives RETAINED. Reconstructed and equal gives
REBUILT_IDENTICAL; reconstructed and different gives REBUILT_DIFFERENT. A
different complete representation during claimed continuous lifetime is a
contradiction requiring investigation. Equal pointers, visited tokens or resource
lists cannot establish the lifetime relation.

The integrated Raw2 reducer additionally requires the
[dedicated lifetime journal](d5ai-lifetime-schema.md) for retention. It binds
all baseline resource collections and their allocation shape, distinguishing
complete survival, partial survival, old content ending, null-empty continuity
and uncertainty. `prior_storage` is separate from the four consumer/content
outcomes: UNAVAILABLE can coexist with positively surviving external geometry.
Mutation alone cannot prove storage destruction. Frame attribution also refuses
relevant ending or mutation after the actual Generated return and before the
copied content; a stale construction descriptor cannot certify a reused holder.

The lineage JSON has `qualified`, `loss`, `relation`, and `before`/`after`
session/snapshot pairs. It is an interchange certificate requiring independent
native justification. This comparator alone does not generate that proof.

The current adapter deliberately requires each occupied holder's source birth
and publication to survive the same recorder epoch without intervening fences.
An unrelated Grid/source fence can therefore make a surviving holder unqualified;
an unidentified occupied holder also prevents unique geographic selection.
These are INCONCLUSIVE coverage limits, never native absence. The ordinary
initialization path creates new Landscape sources after the whole owner installer
returns, as traced in [the context proof](d5ai-owner-context-rework.md). The
authenticated historical B2 retry has 36 generation witnesses, all with preceding
same-epoch births and 36 distinct geographic keys in
`.local-work/d5ai/b2-birth-coverage02.json`. That supports a usable positive path;
it does not promise all future schedules or qualify a new retail capture.

Correct-body unavailability additionally requires an actual generation-owner
certificate for this ProcGen and a complete observed history without reasons
0, 1, 5 or 6. Owner-preserving reasons 2/3/4 must be fully paired and explain
every epoch increment. Missing fences, unexplained increments, an active context
transition or a fresh empty process without an owner anchor refuse attribution.
Whole installer/reset invalidators are necessary because the inner ProcGen clear
ends before the manager's late owner-zero store. Current manager values alone
cannot substitute for that history.

## Independent controls and reproduction

[Native controls](../../../research/resource-retained-population/d5ai_native_geometry.py)
adapt the owned D5AF method under SOR-P-0002, changing only task/output names.
Two fresh disposable hosts execute fixed ordinary native stages for the three
resource entries, with supplied keys, allocators and callbacks. The full generator,
retail scheduling and gameplay do not execute. Masks 0/3/3 produce respectively
74/78/78 regions and 193/180/180 points; these are summaries of full comparisons.

[Independent controls](../../../research/resource-retained-population/d5ai_geometry_controls.py)
check every represented point and bound against the separate pinned D5S planar
model, then challenge completeness, identity, frame, padding, ordering, flags,
unknown point words, signed zero, availability and lifetime certificates.
The complete raw fixtures and normalized bytes remain LOCAL-ONLY under
`.local-work/d5ai/comparison10/`; its current 286 checks pass. The retained
comparison07 receipt passes 282 checks on that earlier method revision.
Earlier comparison01 preserves the original conservative resource-order rule;
comparison02 corrects it from native hash-map evidence. Comparison03 adds
observation binding, comparison04 adds runtime descriptor-frame controls, and
comparison05 corrects a previously misbound continuity adversary and rejects
malformed frame types. Comparison06 adds the full independent resource-key
census; comparison07 uses the consumed construction frame and explicit no-frame
absence representation. None is claimed equivalent to a later method revision.

Use installed CPython with `-E -B`, repository cwd and fresh ignored output paths:

```text
research/resource-retained-population/d5ai_native_geometry.py .local-work/d5ai/NEW-HOST .local-work/d5af/geometry-metadata
research/resource-retained-population/d5ai_geometry_controls.py .local-work/d5ai/NEW-CONTROLS .local-work/d5ai/geometry01/control.json .local-work/d5ai/geometry02/control.json
research/resource-retained-population/d5ai_geometry.py BEFORE.json AFTER.json LINEAGE.json --out NEW-RESULT.json
```

The byte/oracle controls qualify a representation and comparator. Native lock,
snapshot ownership, transport, frame attribution and operational qualification
remain separate acceptance requirements of the [original brief](../../implementation-briefs/README.md#archive-lookup) (`implementation-briefs.zip :: docs/implementation-briefs/CODEX_BRIEF_SOR_RG2_D5AI_population_lifecycle_geometry_observer_readiness.md`).
