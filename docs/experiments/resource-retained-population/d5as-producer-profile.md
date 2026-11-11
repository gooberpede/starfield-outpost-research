# D5AS producer profile and Feynman comparison

2026-11-06, Australia/Sydney. D5AS-Q1 and AC02–AC03 implementation evidence.
Authored analysis and code are REVIEW-REQUIRED. Raw snapshots, native control
outputs and historical archives are LOCAL-ONLY. GC-10, GC-31 and D5R remain OPEN.

| Question | Offline result |
| --- | --- |
| Does exact 0.2.0 supply a comparable target observation? | The retained Pilot04 file passes the prospective `sor-d5as-feynman-source-geometry/1` source and frame checks. One of 36 readable resident entries, `map-entry-6`, binds to the authenticated Feynman source. The geometry gate is separate from aggregate attempt admission and Pilot04 is excluded from the roster. |
| What did Pilot04 represent? | Its complete 4,858-byte canonical body equals actual A0 and the fixed mask-3 body byte for byte. The 4,966-byte fixed mask-0 body differs. This is a STRONG scoped source and frame attribution supported by static analysis, owned controls and one authenticated retail pilot. Exact equality in the stated byte domain is directly reproducible. |
| What does the old method say? | `sor-d5ar-source-planar/1` still returns `UNAVAILABLE/INCONCLUSIVE` with `Producer interval profile not admitted`. It rejects the exact 0.2.0 producer before evaluating source or shape. |
| What remains unknown? | Physical outpost area, historical sampled mask, full effective generation input equality, future retail performance, load-set identity and the representativeness of eligible attempts. Independent review of this D5AS profile and aggregate procedure is a separate acceptance requirement. |

[Frozen D5AS contract](../../implementation-briefs/README.md#archive-lookup) (`implementation-briefs.zip :: docs/implementation-briefs/CODEX_BRIEF_SOR_RG2_D5AS_Feynman_30_sample_series_preparation.md`) ·
[Pilot04 offline findings](d5ar-pilot04-offline-findings.md) ·
[D5AR effective input gate](d5ar-effective-input-gate.md)

## Exact producer and admission

The previous `d5ar_source_frames.derive` tests the complete build dictionary
before interpreting native diagnostics. The original native profile specifies
DLL SHA-256 `8fadade8fde699238af1eadd06065b4dd92f161471499cf03961166639270fe0`
and source lock `1470a6368cec252ae5ac8d3a8bcb8f2291249177a8fd4d53e6145dc0d47bf1f5`.
Pilot04 instead supplies the direct 0.2.0 DLL
`207ff49ee06ab52b6cc5978247c4f45b09a41a676ab55b491fa8d7ace1acd401` and
source lock `063117f8149060b0347ef475145c9306b49b924cf7d29fcef05216cdadb8eb24`.
Both methods bind game version 1.16.244.0, executable
`7e9adb1414a8e1b325e5e1f097b9b17b78deb7eebeda37a333351a43a60f9d28`
and SFSE runtime
`28c5bda41d9959c885efcb6e889de69e92767c80a1a66842d711d215f722f82b`.
The D5AS method has a separate identifier and leaves the older classifier
and Pilot04's raw evidence basis unchanged.
[D5AR classifier](../../../research/resource-retained-population/d5ar_source_frames.py) ·
[D5AS geometry admission](../../../research/resource-retained-population/d5as_geometry.py)

The 0.2.0 preload verifies the executable and SFSE hashes, private sidecar,
drive floors, sole-thread and empty-owner conditions, startup ancestor and
seven guarded sites. Five entry sites protect ProcGen destruction and owner
lifecycle. The two source-ending call sites record retired addresses before
original free. Complete diagnostic group reads share that source-ending
barrier, so later reuse of a recorded address cannot pass as a new source.
The source-bearing geometry copy does not establish that an allocation
survives publication.
[Preload history](d5ar-preload-history.md) ·
[Source-ending proof](d5ar-source-ending-proof.md) ·
[Exact producer source](../../../runtime/outpost-geometry-snapshot/plugin.cpp)

The direct worker takes an observer lifetime lease before reading the current
manager, claims an idle ProcGen reader word by CAS from 0 to 1 at object-relative
offset `+0x44`, then verifies the complete owner binding again. It reads under
both protections and compares the manager, attached ProcGen, owner FormID, mode
and all 44 current descriptor bytes again before releasing either lease.
The copied reader word may include an additional reader or queued writer. It
must retain a nonzero reader count and no exclusive bits. The release wakes the
original waiting writer when appropriate. Original phase unwinding, STOP
and copy refusal suppress qualifying publication. Startup receipt correlation
belongs to aggregate analysis. Endpoint diagnostics alone do not establish
lease or source history.
[Direct worker integration and exact controls](d5ar-pilot03-trigger-followup.md#pilot04-implementation-and-offline-acceptance-scope) ·
[Native reader claim and release](../../../runtime/outpost-geometry-snapshot/direct_reader.h)

The profile verifies the exact raw schema and both integrity hash levels.
It requires a successful direct copy, equal nonzero epochs, admissible reader
word, present copy clocks, complete equal owner records, valid owner and copy
ProcGen pointer tokens, Feynman body `0x0005e0de` and mode 2. Clock reversal
is diagnostic. It checks direct producer map-slot ordering and source and
geometry dispositions, including the lack of an area-operation observation.
Every resident entry must supply a readable geographic key so an unidentified
entry cannot conceal a second target. The sole target must have valid
source/holder tokens, a coherent frame and nonempty complete copied geometry.
The native reserve census must agree with all serialized rows using the
exact x64 strides of 224 bytes per holder, 32 per resource, 56 per region and
16 per point. Pilot04 gives 296,384 bytes from 36 holders, 102 resources,
2,984 regions and 7,372 points. The raw representation retains other resident
entries and the native DLL contains no Feynman target selection.
[Copier](../../../runtime/outpost-geometry-snapshot/capture.h) ·
[Writer](../../../runtime/outpost-geometry-snapshot/writer.cpp) ·
[Raw schema](d5ar-snapshot-schema.md)

The direct worker lacks the older established-operation and reference capture
hooks. That difference makes it unsuitable as evidence for an outpost selection
lease. The target-source profile instead verifies the serialized source bytes
from the protected current-map interval. It tests the source-derived coordinate
basis against A0, while current owner descriptor equality checks the integrity
of each copy interval. The current owner descriptor can vary across attempts.
The profile grants a conditional interpretation of immutable acquired bytes.
Checksums and self-reported build strings cannot authenticate a fabricated or
replaced acquisition. The tested lease and preload premises apply within the
pinned ordinary native graph and load-set assumptions.
[Owner/source lifetime](d5ar-lifetime-admission.md) ·
[Source-planar proof and ordinary zero-rebase scope](d5ar-source-frame-proof.md)

## Pilot and byte domains

The comparison authenticates the final Pilot04 snapshot
`224f82e69a4a59f7758328e2ee029b450c7cca9cdf830ac5022e077a131a559e`
against sealed archive
`fe3a7a07f9c48e60e25ce6496f88bab77280789afb41e9eccbf5b5c15363a504`,
all 27 inventory members and the linked process, session, command, package and
postflight records. The separately authored previous reviewer receipt is
`.local-work/d5ar/review-pilot04-feynman-comparison01.json`, SHA-256
`3b1d72edede5d3b3c054d1f1e383e6a4e8efd1f6c9f24640081cc82aafe6f6cc`.
That receipt independently reaches the same target entry, frame and body
digest under its diagnostic scope. No historical outcome is promoted.
[Pilot04 record](d5ar-pilot04-offline-findings.md)

The target's original little-endian terrain and six signed source coordinate
words plus chart decode to `0:37536:20928:0029d20e`. The 29-byte diagnostic must
agree with its projection from the terrain word and full 44-byte source
descriptor. The basis compares the semantic 41 descriptor bytes, excluding
the three chart padding bytes, plus the executable, owner/body, terrain and
four exact origin inputs. The inputs `[0,0,2,2]` yield the source-plane
origin `[-200,-200]`. The historical A0 receipt binds the same source basis
to allocation 932 and its acknowledged native birth frame at sequence 2082.
The two fixed original native hosts agree on source, body, origin and fixed
coordinate context. Their reference bridge uses the pinned request model and
repeated point/bounds controls. It does not reconstruct the whole source object
or effective inputs of historical generation.
[A0 and source basis proof](d5ar-source-frame-proof.md#executed-controls-and-authenticated-a0) ·
[Fixed reference provenance](d5aq-report.md)

Both primary D5AG original-instruction control outputs independently reproduce
the D5AQ fixed-reference bodies across the three query cases `[4,-1]`,
`[4,1]` and `[5,0]`. D5AS checks their exact recorded files against the pinned
D5AG verifier, compares all six canonical bodies byte for byte, and repeats
that comparison with the separate field serializer.
[D5AG complete geometry controls](d5ag-geometry-controls.md)

The body starts with a little-endian u32 resource count. It writes ascending
eight-hex-digit resource identities as four bytes in display order, each
followed by its little-endian u32 region count. For each region in native
order it writes the first 21 raw header bytes, little-endian u32 point count
and every original 16-byte point in order, including the fourth word.
Header bytes `0x15..0x17` are the only excluded geometry padding. Complete
arrays must agree with represented counts, FormIDs and hashes. Header and
point float words must be finite, with planar signed zero for the third
word. No transforms or rounding enter the comparison.
[Raw schema and normalization](d5ar-snapshot-schema.md) ·
[Source-planar normalizer](../../../research/resource-retained-population/d5ar_source_frames.py)

| Artifact | Comparison domain | Bytes | SHA-256 |
| --- | --- | ---: | --- |
| Historical A0 | Original envelope-inclusive D5AI normalization | 5,090 | `0c05d4a4c458b533d1ec7ae3acc8b34698ac48b91ff2965224e5c37ca055da96` |
| A0 derivative, Pilot04 and fixed mask 3 | Exact canonical body | 4,858 | `7b66c2cce4b0c4c2d52a91a41d02997f12632d0c197681fcf4f21cb87bdbf653` |
| Fixed mask 0 | Exact canonical body | 4,966 | `bba4c877bc14d8abd3cfe36313e4cd62fd98e510dbf18441b250eacb57b942c4` |

The A0 original wire has two u32 length-prefixed canonical JSON values for
source and frame. They occupy 232 bytes together with their prefixes.
Independent extraction at byte offset 232 yields the same 4,858-byte body
as the independent field serializer and the unchanged D5AR body builder.
The first fixed mask-0 difference is the region count for FormID `0x000057cf`
(18 versus 57). The difference locator is diagnostic. Classification uses all
body bytes. A synthetic same-count fourth-point-word change remains eligible
as `OTHER_QUALIFIED_GEOMETRY`; it is not classified by matching counts or
treated as a failure because of its novelty.
[Offline geometry controls](../../../research/resource-retained-population/d5as_geometry_controls.py)

The C1 request census counts 28 mask-0 and 168 mask-3 candidates over 196
coordinates under its conditional model. It includes 195 conditional rows
and the separate directly sampled N2 constructor at `(-2,11)`, mask 3.
The planned `p=1/7` null requires separate sampling assumptions.
Reference-equivalent geometry is the observable proxy. The generating mask
for Pilot04 and future direct snapshots stays UNKNOWN.
[C1 map](d5aq-request-mask-map.csv) ·
[Original statistical limits](d5aq-statistical-limits.md)

## Reproduction and limits

Run `d5as_geometry_controls.py` with the pinned local Python using `-E -B`.
The test reads only existing local evidence, exact source and reference
inputs, and emits a JSON receipt to stdout. The receipt records tested cases,
interpreter and method hashes, both disk floors and input pins. Synthetic
controls carry an explicit synthetic role and are never retail observations.
The owned method reuses D5AR raw decoding, D5AL archive authentication and
D5AQ fixed native evidence under SOR-P-0002. The old raw decoder and frame
method are pinned by exact bytes. No additional third-party code or native
binary execution enters this comparison.

The final implementation receipt records **53 passing checks** in
`.local-work/d5as/geometry-qualification03.json`, SHA-256
`855735a595dc554997aba2ba4831c6aec45497c46506abc01fbb14dd4e80e732`.
Earlier 45- and 51-check runs passed before all frame, census and D5AG
controls were in place.
The first expanded control incorrectly expected all C1 rows to say
`CONDITIONAL`. Reading the pinned CSV revealed the explicit proven N2 row,
and the corrected control tests both groups and the 28/168 aggregate.

The native safety evidence remains the exact previously qualified 0.2.0
controls, including the original writer handoff, adverse binding replacement,
source-address reuse, native reader contention, STOP before publication, and
C++ and SEH cleanup. The original 11-case lock receipt is
`.local-work/d5ar/trigger-lock03.json` at SHA-256
`39ea60b0659ef728f2b2da5da43717a414feebbcc516d5898c54695fb861ffbd`.
The exact direct build control receipt is
`.local-work/d5ar/direct-worker-rework04/build.json` at SHA-256
`fda5bbd088a31f2b4d5aae993a53fbf5e25b8d8a41f7869785ce97649d22327b`.
Those are historical owned-host and original-instruction controls. The D5AS
decoder tests check acceptance, exact representation and adverse input
rejection. Future retail success and effective deployment remain open until
observable under separately authorized collection.

A separate read-only check matched the compiled census byte accounting in
all six retained complete direct-worker fixture outputs. Their SHA-256 values
agree with the final build receipt. Modes 62, 72, 75, 76 and 77 each give
328 bytes; mode 80's empty holder gives 224. This checks the serialized counts
and exact ABI formula on the retained bytes. The reviewed copier source
explains the occupied-record stride accounting.
