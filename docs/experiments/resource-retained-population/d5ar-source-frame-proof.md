# D5AR native source-planar comparison basis

2026-11-05, Australia/Sydney. **The represented region headers and ordered points
have a recoverable source-local native planar basis.** This is a proposed positive
STATIC result within the pinned ordinary ownership/writer graph, supported by
original-instruction controls and authenticated A0 bytes. Independent review and
the integrated capture's current-map/source-lifetime qualification remain required.
It does not establish the current outpost's physical area or historical sampled
mask. D5AR-Q2/Q4 and D5R are not closed by this proof.

All addresses below are preferred static VAs, image base `0x140000000`, retail
1.16.244.0 executable SHA-256
`7e9adb1414a8e1b325e5e1f097b9b17b78deb7eebeda37a333351a43a60f9d28`.
Offsets are hexadecimal bytes. Authored synthesis/methods are REVIEW-REQUIRED;
original instruction exports, raw birth and full receipts remain LOCAL-ONLY.

## Theorem and scope

For a live source in the qualified current ProcGen map, admitted by the complete
[startup ending history and gated-copy method](d5ar-source-ending-proof.md)
rather than map membership alone, whose allocation belongs
to the examined original Grid/source graph and whose retained collection was
constructed/copied by the mapped native region writers, the native numeric
coordinate basis is fixed by its four origin-input words at `+0x10/+0x14/+0x20/+0x24`.
The source's 44-byte geographic descriptor at `+0x38` additionally identifies its
source coordinate convention; its semantic 41-byte projection excludes only the
three padding bytes immediately following the chart byte. Body/current-map
binding, terrain FormID and this complete descriptor remain separate required
identity premises. No inverse planetary/chart transform is needed when comparing
two exactly equal complete basis records.

The source-origin provider computes signed 32-bit differences and multiplication
by 100, converts to binary32, floors/converts and supplies an Int2 to generation.
This contract preserves the input words and original arithmetic; it does not
replace those operations with unbounded integer arithmetic. For the admitted A0
and fixed controls the words are `[0,0,2,2]`, giving exactly `[-200,-200]`.
Initial points are source-origin + cell*100 + local random XY, with Z=positive
zero. Subsequent finite point steps preserve the same XY axes and planar zero Z.
The descriptor-dependent key/seed can change the represented shape without
changing this numeric basis. Historical query, effective mask, selected settings
and generation causation remain separate questions.

This proof concerns raw represented geometry. It does not equate that plane with
a current indexed Workshop query, a physically placed beacon, terrain height,
saved world XYZ or a unique planetary embedding. The global indexed translation
investigation therefore remains INCOMPLETE for physical area mapping, while it
is unnecessary for this narrower equality of source-planar representations.

## Positive native chain and writer closure

| Premise | Original evidence and consequence |
| --- | --- |
| Source construction | `0x14098303f/0x140983046` copy source anchor from incoming R8; `0x14098305a/0x140983061` copy incoming R9 padding pair. `0x140983085..0x1409830c5` copy the complete descriptor's initialized words. Source `+0x18/+0x1c` dimensions are distinct. P1 export01 lines 324–762, hash below. |
| Actual caller meaning | `0x140785490` builds the anchor, takes padding from setting `0x145f60a90`, copies current/pending manager descriptor and calls `0x14096f5c0` on the copy before `0x140982d90`. The source descriptor is therefore source-anchor transformed, not automatically the manager descriptor. Equal full records avoid an invented inverse of this chart conversion. Fresh origin-sender01 lines 3273–3509. |
| Post-return stores | The three bound constructor callers are `0x140849670`, `0x140785490`, `0x1407862a0`. The former discards the returned pointer; the latter returns without a source store; `0x140785490` writes only source `+0x178` at `0x1407855e9`. P1 specialist-export01 and its complete caller census retain these exact flows. |
| Source aliases | P1 L05/L06/L18 source-rooted receivers distinguish cells, cursor/auxiliary records, Grid getters and GridFillFile's raw source alias. Their writes are to those objects and outputs, not these origin or descriptor fields. `0x1409832e0` reads source in R14 with no direct source store; `0x140983880` reads source anchor/padding and passes its dimension pair as inputs, publishing its raw pointer into GridFillFile `+0x278`. Field meaning is not transferred between Grid/cell/source receivers merely by equal offsets. |
| Actual adverse source writer | Grid shift `0x140986da0` can subtract a nonzero third-argument rebase from each source anchor at `0x140987048/0x14098704c`, before retirement filtering. A claim that the primitive never changes source anchor is false. Fresh origin-event01 lines 969–1821, especially 1366/1368. |
| Ordinary zero-rebase caller | Its only defined code callers are `0x14078572e/0x140785746`, both in `0x1407856b0`, passing current manager `+0x1ec/+0x1f0` as rebase. Fresh origin-sender01 lines 3510 onward; loads at line 3539, calls at 3571/3583. The mapped manager constructor stores zero at `0x140787ab4/0x140787abb`; `0x14078c290`, `0x14078c3a0` and `0x14078c5f0` copy the same file-backed zero triple `0x144da97a8..0x144da97b3`. The sole nearby RBP+0x1ec address formation in `0x14078b030` is a stack local. No nonzero manager rebase writer or escape is established in this bounded receiver family. |
| Ordinary mutation scope | Under that actual zero-rebase caller graph, ordinary Grid shifting/filtering preserves the source origin words while sources remain allocated. Dimensions, source metadata, membership and allocation lifetime have their own operations. The nonzero primitive controls below are retained outside this zero-argument ordinary contract. No claim excludes arbitrary replacement vtables, injected writers or other builds. |
| Consumed origin | Provider `0x14079fab8..0x14079fad6` reads the four origin words; `0x14079feda..0x14079fefb` performs the final conversion; `0x14079ff0f/0x14079ff18` pass the Int2. Constructor retains its pointer at `0x14079b86f`; traversal passes it as R8 at `0x14079c4e0`. Original Q export01 lines 125–151, 378–410, 3535–3574, 6682–6741. |
| First point and basis | Generator `0x14079a330`: source origin is reloaded into R13 at `0x14079a72a`; `0x14079a7c5..0x14079a848` construct XY from that origin and cell/random terms; `0x14079a84e` stores zero Z. Fresh geometry-basis01 lines 1509 onward, first-point lines 2004–2058. |
| Later point and basis | At `0x14079a8dc..0x14079a8f2`, VEX scalar sin/cos loads zero upper lanes and create an XY direction with zero third component. `0x14079a954` adds distance times that zero to previous Z. This is a finite-input planar recurrence, not a terrain-height read. Candidate XYZ-width is copied into the ordered vector at `0x14079ab21` (line 2356). |
| Collision is a filter | `0x1407af1a0` reads candidate XYZ/width, builds nine local corner copies and calls `0x14079b020`. That callback writes only its caller-provided bool flag at `0x14079b43a`; it does not receive writable original candidate XYZ. Trigonometric callees receive register arithmetic, not source-coordinate pointers. Fresh geometry-basis01 lines 2–1250, flag line 433. |
| Header formation | `0x142bf4850` derives a center/radius from the supplied point bounds by local arithmetic. It reads no current descriptor or global frame and does not convert coordinate axes. Fresh geometry-basis01 lines 1251–1508. |
| Retained copy | Generator calls `0x1407ac2f0` at `0x14079aced`. The latter copies XYZ/radius and meaningful resource/type header fields directly, then `0x1407ac0d0` deep-copies ordered 16-byte points. Allocation failure can omit data; it cannot supply a completeness certificate from return AL alone. Fresh geometry-basis01 lines 3665 onward, header/point-copy call at 3736–3748. |
| Later ownership operations | The D5AH/D5AI ordinary holder/collection graph transfers, retains, releases or frees these buffers; it establishes no later coordinate rebasing of the represented map. Source retirement erases the current-map entry before source free. Old-map residence and checked readable bytes alone do not qualify source allocation or this basis; the integrated current-map/lifetime premise is mandatory. |

The source-rooted and manager receiver coverage above is the scoped ordinary
native graph already used by P1/D5AI, extended to these exact bytes and the actual
rebase counterexample. It is not a whole-executable arbitrary-memory nonmutation
theorem. The source array's ownership and current-map relation must survive the
entire admitted copy; present repeated equality alone cannot replace them.

## Executed controls and authenticated A0

`origin-shift07.json` and its qualification receipt execute six controls with
the pinned original instructions. Complete `0x14078c3a0/0x14078c290` functions and
explicitly isolated, ABI-wrapped constructor/threshold write blocks each start
from a nonzero owned manager triple, write zero, and run the original
`0x1407856b0 -> 0x140986da0 -> 0x140988100` path. The source remains resident and its
words remain `[0,0,2,2]`. Population-tail `0x140785190` is a recording return;
unreached retirement records only; an unrelated mutable reset-AABB template is
supplied as owned zero bytes. These substitutions are declared in the receipt.
The complete constructor and threshold functions were not executed. Two separate
original-primitive controls explicitly supply nonzero rebase, observe anchor
`[-3,2,2,2]`, then restore `[0,0,2,2]`. They expose the writer and equality/ABA
hazard without claiming that nonzero argument occurs in the ordinary caller.
Failed fixture versions 01–04 and passing versions 05/06 remain local; version 07
binds the final driver and six-control scope.

`source-frame01.json`, produced by the owned
[A0 source-frame control](../../../research/resource-retained-population/d5ar_source_frame_controls.py),
reauthenticates the D5AL original/archive anchors, complete resident census,
original A0 normalized bytes and acknowledged event prefix. It independently
checks the exact 328-byte frame at sequence 2082: magic, length, sequence, kind 14,
CRC and allocation 932. Birth copying really captured all source `0x70` bytes;
the earlier semantic projection was not a sparse raw capture. That actual birth
has origin words `[0,0,2,2]`. Its full source descriptor's semantic 41 bytes equal
the independently qualified actual consumed generation descriptor in A0's original
certificate. Thus the new basis has positive archived operands, not inferred
zeros or a label chosen because the geometry happened to match.

The same receipt authenticates D5AQ geometry01/02 and their complete independent
point/bound checks. Their fixed original native origin is exactly `[-200,-200]`;
all actual A0 and fixed output point/header Z words are positive zero. Fixed mask 0
has 74 regions/193 points and differs from A0; fixed mask 3 and its independent
repeat have 78/180 and equal A0's represented meaningful bytes. These are
comparison results in this proposed source-planar basis. They do not identify
the historical sampled mask or prove all hidden generation inputs equal.

## Proposed normalization and refusals

Use a new explicit basis name such as `native-source-planar-v1`, separate from
the historical `consumed-descriptor-v1` contract. The frame record must bind the
executable hash, qualified body FormID/current-map source relation, source terrain
FormID, complete source descriptor semantic41, and all four raw little-endian
origin-input words16. Preserve raw44 separately. Do not substitute the combined
geographic key for its complete descriptor decomposition, or omit non-geographic
descriptor words because their meaning is unknown. Do not include allocation
addresses, map order, source visited token, user labels or operation markers in
this coordinate-basis equality record.

Compare complete canonical represented geometry only after those frame records
match exactly: resource identities, resource/region counts, every meaningful
21-byte region header and every ordered 16-byte point. Preserve native order and
all meaningful bits, including signed zero; exclude only independently established
padding. No fitting, inferred rigid transform or count-only match is permitted.
The existing A0 archived normalization remains immutable; any new normalization
is a separately versioned derivative with its original input pins.

Refuse a qualified comparison when source/current-map lifetime is unqualified;
any required diagnostic read fails; source/body/descriptor/origin inputs disagree;
source-frame projection disagrees with independently copied geography; output is
partial/truncated; an unsupported writer/rebase path applies; numeric/finite/planar
premises fail; or required provenance is missing. A byte-identical population
cannot override a failed frame premise. Diagnostic helper statuses remain
SOURCE_BYTES_UNQUALIFIED, SOURCE_ORIGIN_WORDS_UNQUALIFIED and
SOURCE_DESCRIPTOR_UNQUALIFIED until the separate integrated premises qualify.
Current-outpost reference and physical area membership remain separate contracts.

Old D5AI historical-frame verdicts and its P -> Q -> P counterexample are unchanged.
The new theorem allows different hidden seed/mask histories to produce different
shapes in one source-planar representation; it does not recover their historical
geographic sampling frame. Independent review must challenge both this narrower
theorem and its integrated admission, rather than treating the new name as proof.

## Primary pins

| Local original evidence | SHA-256 |
| --- | --- |
| `.local-work/d5q/export01/native.tsv` | `60cc949338e9e0211b87f56c376e1a057d8b7af2da6f9e34a4ae3e84339f8fcd` |
| `.local-work/d5ab/p1-export01/native.tsv` | `27fe3e554236d1d03acddee2b26df26bcc0c976b1510fb60b54154fce29656a6` |
| `.local-work/d5ab/p1-specialist-export01/native.tsv` | `47451aca5d77cc8a7a6ae6b698dd7fa6d9fb4a05cf260559b178a52ae8f37132` |
| `.local-work/d5ai-ownership/owner-census01/native.tsv` | `6cc620abbc789284f60c62e18b6a62a13f61c88e899e14a9bb1ff55722d21914` |
| `.local-work/d5am/d5ar-origin-event01/native.tsv` | `afeeb65b60b54b0bc7f2f12ac233595935065131cd90f9f4394ff02b0c6eb4e4` |
| `.local-work/d5am/d5ar-origin-sender01/native.tsv` | `44472ae41c61b6eb5e8be38baf02852f24b44ebaa7fcc07e560420a2797dde90` |
| `.local-work/d5am/d5ar-geometry-basis01/native.tsv` | `92208bc5abab4a490ad371f4844fcb136b9bad457bbd4a4e0806fc01c57a1adf` |
| `.local-work/d5ar/source-frame02.json` | `900e501361b4ab1370af94d6231f41cd93d35259fa926f0452139b67fccfe5b5` |
| `.local-work/d5ar/source-frame03.json` | `1f4573f760ac6ea96c701690cb2f98e5ed22cfd1da4155d4efef38d2ac960cb1` |
| `.local-work/d5ar/origin-shift07.json` | `50f9fdac13762cf697dab022101a977bafdcd862e03e5f9a53641e2b372fed2b` |

Fresh copied-database exports retain readOnly/no-analysis commands and all fifteen
copied-core hashes before/after. The source-frame receipt pins every original A0
anchor and fixed output it reads; origin-shift qualification pins its owned
driver, inherited loader, generated method and original function/write-block
bytes. SOR-P-0002 covers those project-owned adaptations; no new third-party
implementation or permission basis was introduced.


## Admission repair and fixed-input authentication

The first frozen native build19 does not supply the interval premise above.
Before/after manager/ProcGen equality can miss constructor early publication,
ProcGen replacement and caller final republication. The new owned publication
control executes unchanged original `0x141881f3d..0x141881f5c` instructions and
exhibits that counterexample. Its whole-phase admission model rejects the
intervening states; production implementation requires separate qualification.
The repair under review spans initializer `0x141881660`, manager destructor
`0x140788bc0`, installer `0x140789ce0` and true reset `0x140788e70`, in addition
to the existing inner ProcGen destruction epoch. Startup must reject an already
active phase ancestor, including parsed cleanup/funclet ownership, and must
refuse missing unwind metadata. The exact method registry must admit only the
reviewed new source lock, never a caller-supplied qualification boolean.

Body attribution also needs the ordinary work-drain ordering. True reset calls
`0x14078f0b0` at `0x140788e8c`, before manager lock `+0x24`, ProcGen clear and
late body-zero store `0x14078936d`. Ordinary B030 calls the same drain at
`0x14078b077`, before exclusive manager admission `0x14078b080`, installer
`0x14078b3f4` and later Grid/source construction `0x14078b936`. The drain snapshots
tracked generation under its lock, sends completion command `0x1407906e0` at
`0x14078f228..0x14078f25e`, waits completion at `0x14078f263..0x14078f2a2`, then
waits the generation job site through `0x1427eef10` at `0x14078f2b3`. Active
ordinary layer provider work holds manager shared admission around provider dispatch
(`0x1407b5235..0x1407b526a`). Detached density has no such inherited preparation
reader; `a0-provider-family03.json` now identifies actual A0 as Density within
the examined two-caller graph. Its complete tracked-job/drain relation must be
checked separately rather than borrowing Layer admission. Generation itself loads the then-bound body at
`0x14079fed3`, immediately before the native generator. This is a positive
bounded ordinary-path argument; independent review must challenge tracked-work
coverage and source publication after reset. A mere current body read is not
historical body provenance by itself.

`source-frame02.json` strengthens the reference bridge (source-frame03 repeats the source-bound checks after the descriptive docstring correction): the original fixed request
metadata hash must equal
`9594ab2aa34856bcc3b8ecb249b46b0063ef4b5d1af80d4e557542f2d6657ccf`,
both independently pinned fixed controls must authenticate that exact hash in
`model_input_sha256`, both child copies must hash identically, and both execution
receipts must record successful exit and that exact original input hash. The
fixed fixture supplies only native numeric planar origin `[-200,-200]`; it does
not supply A0's full descriptor or four source words. Numeric basis equivalence
follows the original coordinate writer theorem. No A0 identity metadata is
assigned to fixed output because its shape matches.

Generic plane validation admits both IEEE signed zero encodings in Z, preserves
every bit in comparison and uses no tolerance. Unsupported nonzero/nonfinite Z
refuses this basis. An exact admitted producer's complete empty resource-map
traversal can derive an empty represented population; absent holders, failed
reads or arbitrary `EMPTY` labels cannot. This says nothing about geographical
absence. The indexed physical area frame remains a separate unqualified branch.


## Separate effective-input gate

[The effective-input investigation](d5ar-effective-input-gate.md) preserves the
mandatory limit: this numeric representation theorem does not establish full
non-mask generation-input equivalence with fixed C1. Positive native reconstruction
now recovers A0's final dimensions `[10,10]` from all three ordinary constructor
caller families and its authenticated birth `[14,14]`/padding `[2,2]` operands.
The read-only overlap predicate does not clip the nominal argument. All 23 pinned
config files contain no stitching keys; original merge-zone initialization is 2.
All 39 definition files contain no overrides in the 339-record Feynman resource
dependency set. The generic GameSetting reset is followed by definition reload
on every examined normal return path, so finding EXE default `.01` alone does
not establish an actual alternative to DATA `.05`. Missing per-use event fields
do not defeat these positive reconstruction routes by themselves.

Source-map membership alone failed to exclude late publication of a source
selected before retirement. The final [lifetime admission](d5ar-lifetime-admission.md)
adds the ending history and synchronization independently of the owner phase
fences. The exact native profile now has bounded technical admission for its
protected source reads and represented-content comparison. Q3 and AC05 remain
open at the distinct effective-input gate, including historical settings and
runtime component evidence. This profile does not independently qualify an
arbitrary future resident snapshot for the series.
