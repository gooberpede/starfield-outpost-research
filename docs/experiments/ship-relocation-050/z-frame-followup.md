# Existing-capture Z and frame investigation

2026-10-13, Australia/Sydney. SOR-EXP-0031 / SOR-EV-0039 continuation.
[Authorized follow-up](../../implementation-briefs/README.md#archive-lookup) (`implementation-briefs.zip :: docs/implementation-briefs/CODEX_BRIEF_SOR_observer050_existing_capture_z_frame_followup.md`),
[prior live report](live-attempt-01.md), [40 audited cases](z-frame-followup-cases.csv),
[source/evidence hashes](z-frame-followup-sources.csv), [review](z-frame-followup-review.md).
Authored interpretation REVIEW-REQUIRED; raw/static/private artifacts LOCAL-ONLY.

| Element | Answer |
|---|---|
| Question | Can existing capture and static evidence resolve the Z discrepancy and missing loaded-frame provenance without another live run? |
| Best-supported answer | **Partly. The 2D query/grid source-frame provenance is recoverable.** All 40 ordinary Workshop grids have real Q→E→callback ancestry, an enclosing world key exactly matching the frozen saved descriptor, and matching source-descriptor bytes at enumeration/callback/grid-copy stages. The missing own-cell/world fields are genuine sampled nulls, not a demonstrated offset error. The native Z values are genuine reference/center outputs; their exact causal difference from saved Z remains unresolved because the relevant reference flag and selected 3D restoration/height edge were not sampled. |
| Confidence | PROVEN / RUNTIME+STATIC for field bytes, helper data flow and observed 2D source-frame chain; CROSS-VALIDATED numeric source-key correspondence with the existing frozen saved extraction. No full own-parent, 3D loaded-frame or restoration-equivalence claim. |
| Coverage |40 operations, two Workshop identities, 20 repeats each in one producer; all 1,194 events and 11,375 successful blob extents audited for alternative capture coverage. Eight retained native exports hash-matched to earlier ledgers. |
| Evidence | Original 60-file seal reverified; exact approved 41 source pins, executable/build and frozen inputs preserved; selected CSV includes raw-file offsets, Q/E/callback identities, world keys and Z/translation checks. |
| Limits | Null own-cell cannot prove loaded/unloaded status. A source-world frame is not automatically the reference's own restored parent. Ref+d3 and the selected restoration component/validity/height remain outside captured evidence. |
| Next step | Use the recovered 2D provenance for this scoped grid comparison. Keep Z/full restoration unresolved; any proposed future acquisition should target the specific missing flag/edge/height, rather than repeat this sequence. No new live run is needed for the conclusions here or authorized by them. |

## Native Z: actual output, not a decoding artifact

All native addresses here are static VAs for retail 1.16.244.0, preferred base
140000000, executable SHA256
`7e9adb1414a8e1b325e5e1f097b9b17b78deb7eebeda37a333351a43a60f9d28`.
Runtime VAs and raw-file offsets are explicitly labelled in the case CSV.

`workshop-origin-04.tsv` lines 6–96, function 140f4ab80, copies reference+8c/+90/+94
to output XYZ and conditionally adds concrete ExtraWorkshop+60/+64/+68. In all 40
cases, captured reference+8c..97 is exactly equal to captured native center bytes,
and the compensation vector is exactly zero. The center wrapper reads the
native output buffer after the actual call, with the verified reference argument.
This rejects a simple center-field offset, return-buffer or compensation mismatch
as the cause in these samples; it does not prove every possible observer behavior.

| Identity | Native reference/center Z | Frozen Save25/26 Z | Required additive difference (diagnostic hypothesis) |
|---|---|---|---|
| SOR-002 f1517de43e171745 |3.6431474685668945|18.352506637573242|+14.709359169006348|
| SOR-003 0efca066ee4c7b9b |-9.51641845703125|-31.89084243774414|-22.37442398071289|

Each difference, added in binary32, exactly yields the corresponding frozen Z.
These are calculated differences, **not captured native offsets**. Their opposite
signs reject one common additive Z translation for both simultaneous geometries.
They do not reject per-site height/frame transformations or different restoration
state. The previously checked settled captures in
[the Workshop persistence report](../workshop-origin-beacon-relocation-persistence.md)
record the frozen centers; they are prior evidence, not another new live control.

The sampled translation is **two floats**, not a three-component vector.
`engine-oracle-02.tsv` 140ad0a42–140ad0ab5 creates only XY from integer grid
displacement; stores at 140ad0a64 and 140ad0ab0 initialize eight bytes. The observer
copies 12 bytes from that address. Its third word is `2087902a` for SOR-002 and
`e086902a` for SOR-003; across all 40 records these equal the low 32 bits of the
enclosing query candidate pointer (respectively1fc2a908720/1fc2a9086e0).
Those bytes lie beyond the two-float object in adjacent stack storage. They
are not evidence of an initialized Z translation. No plugin/source change was
needed to establish this semantic boundary; the earlier report correctly left
the word unassigned, and this investigation narrows its explanation.

The callback's actual grid preparation, 140ad0c3b–140ad0d36 in
`engine-oracle-01.tsv`, consumes compensated center XY and translation XY,
computes the floor and calls 96f5c0. Center Z does not feed this grid calculation.
Consequently the Z discrepancy is material to a complete XYZ claim, but does
not invalidate the already observed native 2D nonzero/carry results.

## Recovered 2D query/grid source-frame provenance

This chain uses native scope ancestry and pointer-owned captured bytes, not
time proximity or matching output alone:

1. Grid sequence 96, callback 49 → enumeration 47 → query 46; grid 112, callback 55 →
   enumeration 51 → query 50. The same checks hold for all 20 repeats per identity.
2. Query context+10 points to runtime world 1f7cdb10340, FormID FF0147D2. Its captured
   +310 key bytes are `e0288052790eb202`, little-endian uint64
   `02b20e79528028e0`. The frozen Save25 and Save26 inputs for both Workshop IDs
   identify this exact descriptor key through their saved secondary world joins.
3. The independently qualified key decoder yields tag 1, X10464, Y21120,
   system 88327/body-index 15, reserved0. The callback landscape identifies Kreet
   0003F59F. This is a typed descriptor-key correspondence, not a runtime FormID
   equated with a saved token.
4. Retained query instructions 140ad096f–140ad0986 read source-world+310 and unpack
   it. Instructions 140ad0a85–140ad0a91 bind the source descriptor and XY translation
   to enumeration's callback context. Captured E and callback context+18 point
   to the same source bytes at runtime 7b058fd3c0.
5. Enumeration source 44 bytes, callback source 44 bytes and grid input 44 bytes
   match exactly. The grid input is a **different local copy** at 7b058fd1e0, as
   the native copies 140ad0cd5–140ad0d33 require; pointer equality is neither
   expected nor fabricated. The decoded input is (1,10464,21120).

Together this supplies observed **2D query/grid source-frame provenance** that
was not extracted in the first scientific report. It strengthens the conditional
comparison to frozen cells and translated XY. It does not reconstruct a beacon's
own parent, infer a saved-token remap, or observe a completed load/restoration edge.

The enclosing query requests distinct site-world FormIDs FF01763F for SOR-002
and FF01CB2E for SOR-003, with angular pairs respectively
(-0.2211059435912563,-0.5113105421317372) and
(-0.2197651008318516,-0.5116409319889974). The saved-parent angular association
was previously recorded in [the matching-source investigation](../matching-source-qualification.md).
The full objects for these two requested site worlds were not captured here.
The source world's persistent-cell pointer is 1fc1fae7540; the enumerated cells
are 1fc20083e00/1fc20082000. This concrete inequality prevents treating the source
world as the callbacks' own parent merely because its key matches the origin.

## Own-cell/world absence and alternative retained paths

All 40 complete Workshop grids sample reference+b0 as zero. The retained getter
142116840 (`workshop-origin-04.tsv` lines 160 onward) independently reads+b0;
it has other branches/global fallback when the direct cell is unavailable.
Thus the evidence supports the observer's direct-cell offset. A null direct
field does not establish the native getter's eventual result or object loading
state. Its fallback globals 1461fae90 and 145e60380 and the getter result were not captured.

We inspected all 11,375 successful blob extents, including fields with overloaded
names in other event kinds. For each ordinary reference, 100 views cover+b0;
none cover+d0 or+d3. The observer's normal reference copy ends at+cf. The known
native frame-flag byte+d3 is therefore absent both from its own snapshots and
from every other captured interval, not merely hidden under another field name.

| Retained alternative | What it supplies | Why it does not supply the missing own-parent/Z edge |
|---|---|---|
|14 readable `cell` blobs|Marker cells FF02F099/FF03608A; their+110 pointers link to marker worlds.|They are selected landing-marker contexts, not the ordinary refs whose+b0 is zero. No cross-object parent substitution is justified.|
|Query-world snapshots|World FF02F094 for the new landing, FF0147D2 for the return, readable packed keys.|The return key supplies the positive source-frame chain above; it is not a sampled own-cell or selected 3D restoration record.|
|Marker command worlds and route `center` world views|FF02F098/FF036089, keyffffffffffffffff, nonnull+388 component pointers.|These are marker worlds. The pointed-to component/selected edge bytes are not captured; they cannot be borrowed for a different ordinary reference.|
|Other nominal `world` views|Route fields copied from an overloaded address, not a validated type 56 world object.|Names alone do not supply WRLD semantics or a replacement own-parent join.|
|Enumeration cell 0x90 snapshots|Cell FormIDs FF01C699/FF018550 and the actual callback source context.|Their full+110 world links and the requested site-world objects are outside these views. Enumeration B1E190 explicitly permits callbacks on references with null+b0.|
|Saved world-component table|Typed secondary/source-world links, body/system, flags and bounds in the earlier qualified extraction.|It is a separate component type from the runtime ActivatedOverlayProperty edge; its fields do not supply the event's selected edge/validity/Z.|

The complete local interval/view inventory is retained in `audit-02/coverage.json`.
This corrects any broad reading of “missing provenance” as “no world evidence
anywhere”: useful source-world evidence exists, while the own-parent/3D edge is
still missing. No pointer was dereferenced after capture or transferred between
processes/builds to fill a gap.

## What remains underdetermined about Z

The retained frame preparation 141856d10 in `durable-center-02.tsv` tests
reference+d3 bit 02 at 141856fa8, world kind/context gates and ADA760 validity/status,
then obtains ADA3A0's selected XYZ and conditionally subtracts it at
141857055–141857080. `exact-beacon-11.tsv` 140ada4a8–140ada4f4 shows edge validity
+35, XY=100×integer components and Z from the selected record+30. These are
source-supported transformations that can affect Z independently of Workshop
compensation. They are **not evidence that this particular event took that branch**.

The prior [save/frame trace](../static-exhaustion/call-and-dataflow.md) also separates
typed saved world links from runtime activated edges, height production and
created-reference conversion. Frozen saved frame 0b is not a measurement of the
later reference+d3, manager epoch or selected edge height. No existing captured
view contains the actual flag or resolved height/validity record needed to choose
between a per-site frame/height transformation, different restoration state, or
other native reference-position updates before enumeration. The reference/center snapshots observe their resulting position; prior position-writer execution and operands were not captured, so causal history is not reconstructed.

An exact four-byte search for the two required additions and their negatives
finds zero occurrences in successful captured payloads. This is only a diagnostic:
an unrecorded or computed/rounded transform need not appear as those literal
words. Negative closure rests on absent typed operands/branch state and the
surviving alternative paths, not that byte search or a failed decoder. No fitted
per-outpost Z constants are substituted into the model. This is a bounded
unresolved result for the retained evidence, not proof that every possible future
offline investigation must fail.

## Checks, preservation and review

The original 60-file seal, 1,194 journal/raw events, approved 41 source pins, exact
build manifest/executable and both frozen hashes were checked. Eight native
exports match hashes in prior source ledgers and carry the pinned executable
identity. The audit checks all 40 cases and all captured interval alternatives;
the reviewer independently challenges the arithmetic, layouts and claimed joins.
The first new audit stopped on an erroneous source-pointer/local-copy equality
assertion. Failed source/receipt remain in `audit-01`; `audit-02` correctly compares
the copied bytes while retaining different address domains. No original evidence
or frozen expected result was changed to repair that assertion.

New local derivatives/scripts are under `.local-work/ship-relocation-050-z-frame/`;
the source ledger pins originals and derivatives. Source/card/build/old reports,
seals and captures remain unchanged. No native execution, new live run, deployment,
save/config/database mutation, new dependency/network disclosure, staging, commit
or push occurred. The linked review records criteria Z1–Z5, actual reviewer return,
complete/task-only diffs, inclusion/exclusion manifests and replay checks.
