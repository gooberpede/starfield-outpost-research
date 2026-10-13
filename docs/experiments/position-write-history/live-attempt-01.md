# Position-write history: approved live attempt 01

2026-10-13 (Australia/Sydney), SOR-EXP-0031 / SOR-EV-0039 continuation.
**The previous Z discrepancy was not reproduced.** Both candidate initial-load
setters receive exact Save25 XYZ and the subsequent sampled native centers retain
those bytes. This is a positive Cartesian value match in this run, with partial
writer/identity history; the cause of the different 0.5.0 Z remains unknown.
This report supplements the historical [offline
qualification](report.md); it does not rewrite that assignment's authority.

## Authority, actions and provenance

The maintainer explicitly approved the plugin and [integrated card](run-card.md),
reported deployment of the exact 0.6.0 ZIP to Vortex profile `Starfield - SFSE`,
and authorized preflight. Following verified clearance, the operator launched
normally, reached the responsive main menu, loaded **Attila Kiraly Save25 —
Kreet - Outpost, 10/9/26 at 9:22:22 PM (Level 4)**, settled at SOR-003, traveled
normally to SOR-002 and returned to SOR-003. Each checkpoint was operator-reported
without issues and corroborated by fresh observer nonce ACKs. No fresh landing,
construction, beacon movement, console action or manual new save was requested.

The finite scientific action scope completed; Codex requested the card's STOP
and independently verified retirement. The operator then reported normal exit,
completed Steam sync and observer disablement. Postflight independently confirms
the original process exited and the deployed DLL is absent. Sync and subjective
responsiveness remain operator reports, not machine measurements.

Local receipt root: `.local-work/position-write-history/run-20261013T085008190141Z/`.
Original session: `.local-work/position-write-history/live/session-40616-164222546/`.
Raw evidence and all private save/module/process paths remain ignored, local-only.
Original session files are sealed before final analysis; derivatives are outside
that directory. [Live sources](live-attempt-01-sources.csv) pin actual inputs and
outputs. Existing [build pins](review.md#exact-selected-artifacts) remain unchanged.

The game is pinned retail 1.16.244.0, SFSE reports 131408 (0.2.21), observer 0.6.0
schema 6. Process PID 40616 has creation FILETIME 134363551777466124; module base
`0x00007ff7593a0000`, QPC frequency 10,000,000. Native sites are module-relative
RVAs; captured pointers are runtime addresses, not saved reference tokens.
Admission observed a sole thread, verified 129 owned sites and waited 59,203ms.
Natural CALL/slot replacements, snapshots, synchronous spooling and group flushes
affect timing. This hooked experiment is not described as non-invasive.

## Operational outcome and actual matrix

| Mandatory live criterion | Actual result and primary receipt |
|---|---|
| Exact reviewed package/deployment/loader and source pins | PASS: `preflight.json`, loader/deployed inventory; DLL-only payload matches qualification-11. |
| Both caller-available disk guards | PASS: preflight, checkpoints, retirement and postflight exceed 40,000,000,000 bytes independently on C: and D:. |
| Sole-thread admission, owned guards and fresh ACK | PASS: session admission/patch receipts and fresh menu/three phase nonce ACKs. |
| Approved Save25 and finite 003→002→003 actions | PASS: operator reports and phase receipts; load selection is operator-attested. |
| Generic capture and full committed integrity | PASS: `postflight.json` verifies 562,326 records / 281,163 completed pairs, zero unfinished invocations or uncommitted tail. |
| Retirement and explicit failure accounting | PASS: `retired.json`, attempted=captured=durable=562,326; failed=active=0; no integrity error. Hooks remained inert until exit. |
| Original process exit and DLL removal | PASS: `postflight.json`, original process state EXITED and deployed DLL absent; operator reports normal exit/sync/disable. |
| Protected original inputs | PASS: all 6,563 protected hashes match postflight; canonical saves, old sessions and frozen models preserved. |
| Save-directory changes explained | PASS: `saves-after.json`: 260 unchanged, no modified same-path files, one removed old ExitSave and one new ExitSave at normal exit. No manual save requested. |
| Native history and saved-to-loaded reconciliation | See scientific account below; transport PASS does not establish semantics. |
| Complete lifetime / exhaustive writers / scoped no-write | NOT TESTED / NOT ESTABLISHED: direct stores and allocation/destruction/remapping are not fully observed. |
| Independent scientific review and review patches | See [live review](live-attempt-01-review.md). |

Raw length is 1,871,420,928 bytes. Raw SHA256:
`b44b345d8d47628c74b5c4df0eee998cdf7ae85e046cd4205a7bcddb61ed0f75`.
Journal SHA256:
`5fceef37b31c1ff7c829c8ec315bdcc71841d75610fe444556b2d22fc84ab17e`.
Postflight confirms `PASS_TRANSPORT_POSTFLIGHT` and `PASS_COMMITTED_PREFIX`.
Clean engineering capture, scientific completeness and target survival are
separate outcomes; this run has clean retirement and reported normal survival.

## Retained operational correction

At the initial SOR-003 ACK, an ephemeral checkpoint assertion incorrectly
required captured=durable at the instant of ACK. The legitimate group-flush lag
was 28 records (264,112 captured, 264,084 durable), with zero failures. No STOP,
native patch or gameplay action followed that assertion. Subsequent durable
progress to 278,166 and 300,480 established health. The corrected checkpoint
requires attempted=captured, durable≤captured, zero failures and later durable
progress beyond the ACK's captured sequence. Original ACK, assertion explanation
and correction are retained in `phase-control-check-correction.json`; source,
DLL, guards and scientific records were unchanged. Phase controls used the
approved nonce mechanism with source/deployment/process/guard/disk checks;
the full protected audit was performed at preflight/menu and postflight.

## Scientific reconciliation

The original verified trace was traversed twice, first to identify coherent
Workshop candidates, then to retain **all earlier events for those pointers**.
The primary and authorized specialist independently reconstruct 33,656 selected
records: two initial setter pairs and 16,826 center pairs. The shared fixed-schema
decoder verifies each original journal hash and sequence; separate derivations
agree. `reconciliation.json` additionally re-decodes the unchanged archived
Save25/26 with the existing BCPS reader, verifies source and decoded hashes and
rechecks exact XYZ/compensation offsets. [Selected cases](live-attempt-01-cases.csv)
give invocation, site, sequence, original raw offset and all three component bytes.
Offset domains are distinct: native record offset=(sequence−1)×3328; saved
offsets below refer to the decompressed save stream, not physical compressed bytes.

| Candidate | Saved / setter / sampled center XYZ bytes | Initial setter pair | Center pairs (both ends coherent) | First / last center pairs |
|---|---|---|---|---|
| SOR-002, raw ID `f1517de43e171745` | `a266f542eb858843efd19241` | 190897→190898 | 5,282 (5,280) | 321077→321078 / 372699→372700 |
| SOR-003, raw ID `0efca066ee4c7b9b` | `0369b243f0b019457220ffc1` | 194235→194236 | 11,544 (11,542) | 204749→204750 / 561983→561984 |

SOR-002 XYZ is `[122.70045471191406, 273.0462341308594, 18.352506637573242]`;
SOR-003 is `[356.8204040527344, 2459.05859375, −31.89084243774414]`.
Save25 XYZ starts at 1,344,574 / 1,474,225 respectively; compensation starts at
1,344,620 / 1,474,271, all twelve zero bytes. Both setters at RVA `5A14DA→B4E410`
have before-XYZ twelve zero bytes, operand equal to saved XYZ, after-XYZ equal
to operand, and d3=0 before/after. They are the earliest **captured** setters,
not demonstrated allocation births. Their measured Z effects are respectively
+18.352506637573242 and −31.89084243774414, ordinary replacement from zero,
not signed conversion operands or corrections to historical centers.

At those setters, Workshop extra identity and own-cell/world are unavailable;
ordinary base `002C60E9` and runtime FormIDs are present. Later coherent samples
bind pointers `0x1f7e3ea0000` / `0x1f7e3f55b20` and FormIDs `FF01AA50` /
`FF01AA8F` to the raw Workshop IDs. No conflicting nonzero identity is observed.
Same pointer/form/base plus matching saved XYZ supports the retrospective
association, but save tokens `822821` / `84b985` are **not** those runtime FormIDs.
Allocation/destruction and saved-token remapping were not captured; same-ID
unseen reuse and incomplete epochs remain possible. Confidence is direct
observation for bytes/operations, cross-validated for the saved-value match,
and qualified candidate inference for continuity to the later Workshop.

All 16,826 returned center byte triples equal their respective Save25 XYZ.
Exclude four invocation pairs from coherent before/after identity and arithmetic
claims: SOR-003 206090→206095 and 401602→401603, SOR-002 321083→321086 and
330832→330833. Status8 occurs at records 206095, 321083, 330833, 401602:
the double-read reference prefix changed. It does not identify which field
changed or establish reuse. The output bytes remain retained; this is sampling
incoherence, not transport loss. For all 16,822 remaining pairs, before/after
XYZ are identical, compensation is twelve zero bytes, and actual returned output
equals independently rounded binary32 reference+compensation on all axes.
Center output is interpreted only after native return, never its before buffer.

No later kind1 replacement, kind2 outer conversion, kind3 XYZ application or
producer/deferred application appears for either selected pointer within the
hooked population. Those paths did execute elsewhere: 4,699 outer converter,
4,670 XYZ application and six each queued-producer/allocation/deferred-application
pairs. The initial setter is therefore the last **demonstrated captured** XYZ
writer before each selected center. This is not proof it was the last actual
writer: the [static audit](static-audit.md) retains bypass stores and other
dispatch routes. No selected signed-conversion arithmetic/mode or cross-thread
producer relationship can be validated from absent selected events.

By each first coherent center, d3=2, despite no selected captured converter.
Thus the d3 bit-writing path is a concrete missing interval; a set bit alone
does not establish an XYZ translation. Current centers at caller RVA `F4A1D4`
have available own cells (different for the two references) and a common sampled
world pointer, whereas the historical 0.5.0 query-associated caller `AD0C36` had
null own cells. Current world snapshots stop at +0x180 and do not include the
historical query's +0x310 descriptor key. There is no independently demonstrated
same loaded parent/body/3D frame across the two captures, and availability alone
does not identify the activation state or a geographic height datum.

SOR-003's last center and 143 outputs beyond the return checkpoint's diagnostic
prefix retain saved XYZ; SOR-002 has no sampled centers after that return marker.
The actual return ACK captured sequence is 476,992, with 144 subsequent center
outputs; the later diagnostic survey uses 477,380. Review corrected an initial
derivative field that mislabeled the survey cutoff as ACK; the original derivative
and `return-count-label-correction.json` are retained. No measured bytes changed.
The unchanged historical 0.5.0 Z outputs remain `54296940` (+3.6431474685668945)
and `404318c1` (−9.51641845703125). Their signed differences in the old
[comparison ledger](../workshop-z-restoration/comparisons.csv) remain diagnostic,
not correction vectors. Save26 was rechecked offline only: SOR-003 raw XYZ and
nonzero compensation differ from Save25; it was not loaded in this run and is
not a new native validation control. The frozen 23 predictions are unchanged.

Ordering is bounded by genuine invocation pairs, same-thread ancestry and sample
intervals. Journal sequence orders serialized emission, not a total native store
order: seq204767/thread40180/QPC1648406689521 precedes seq204768/thread49440/
QPC1648406686623 despite the later timestamp. The selected streams have 2,801 /
5,773 adjacent sequence QPC inversions. Stable sampled XYZ cannot exclude
unobserved intermediate writes that return to the same bytes.

**Scientific disposition:** direct saved-value input→native replacement→later
sampled Cartesian center agreement is supported for these two ordinary
candidates in this Save25 run. No selected Z discrepancy needs reconciling here;
the historical altered-center producing epoch is still missing. Complete
restoration/lifetime, exhaustive writer coverage, interval-wide no-write and
full saved-to-loaded geographic/grid-frame equivalence are NOT ESTABLISHED.
This is a completed scoped result with explicit missing history, not a claim
that 0.5.0 was wrong or that height conversion cannot occur. No model fitting,
terrain reconstruction or additional trip was introduced.

No staging, commit, push, upstream contact, database edit, new dependency,
publication or follow-on game run is authorized by completion. Publication
eligibility remains REVIEW-REQUIRED independently of scientific confidence.

After analysis all 21 sealed file lengths/hashes and 20 selected-build source
inputs match (`post-analysis-verification.json`). Recorded module inventories
contain 62 pre-edit and 161 final modules; path review identifies expected
Windows/security/graphics/input/audio/network components and Steam/NVIDIA
overlays, with no credible conflicting instrumentation identified. This inventory
review does not prove absence of all unrecorded instrumentation. No permission
issue or external rights expansion occurred.
