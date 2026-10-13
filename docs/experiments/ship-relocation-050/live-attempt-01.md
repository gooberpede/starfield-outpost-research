# Observer 0.5.0 live attempt 01 — scientific report

2026-10-13, Australia/Sydney. SOR-EXP-0031 / SOR-EV-0039 continuation.
[Approved procedure](run-card.md), [native design](design.md),
[acceptance and independent review](live-attempt-01-review.md),
[selected native samples](live-attempt-01-workshop.csv),
[exact evidence/source hashes](live-attempt-01-sources.csv).
Authored results REVIEW-REQUIRED; original memory, save and binary evidence LOCAL-ONLY.

| Element | Result |
|---|---|
| Question | Does the approved local-control/new-Kreet-landing contrast naturally reach identity-bound native marker and ordinary Workshop positioning, and what agrees with the frozen predictions? |
| Best-supported answer | **Yes, for the sampled native components.** Local control recorded no instrumented native events. The new landing and return recorded two complete travel/marker/grid chains. The return additionally reached 40 ordinary Workshop center/grid operations: 20 repeats each for SOR-002 and SOR-003. All 40 actual native floors and numeric hierarchy outputs match replay of captured operands. SOR-003 demonstrates a radix-12 fine-to-middle Y carry. Translated XY and final cells also match the unchanged Save25/26 numeric candidates for both identities. |
| Confidence | PROVEN / RUNTIME for these recorded input/output bytes, ancestry and scoped numeric comparisons. The saved-to-loaded frame/restoration join remains UNASSESSED; full durable Workshop equivalence is **NOT TESTED**. New scoped interpretations await maintainer review. |
| Coverage | One Save25 session, one local control, one new Kreet landing and one return. Two ordinary Workshop identities and two distinct Workshop operand geometries, repeated 20 times each within one return producer. No negative floors, coarse carry or face/tag transition observed. |
| Evidence | 1,194 hash-validated records; complete schema-5 scopes/retirement; 40 selected grid rows with original journal lines and raw-file offsets; 60-file seal. Independent review is recorded separately. |
| Limits | Captured Workshop cell/world pointers are null/unreadable. Native center XYZ differs from frozen center XYZ; translated XY agrees but Z does not. No complete current-frame, saved-parent or restoration-edge proof. Marker creation and applied ship-assignment identity remain UNKNOWN. |
| Next step | Analyze the retained loaded-frame/Z/restoration dependencies offline before proposing any new capture. No further live session, extra trip, save, deployment or integration follows from this report. |

## Authority, sequence and control

The maintainer approved the exact plugin and run card in this chat, deployed
the ZIP in Vortex profile `Starfield - SFSE`, and started the game after machine
preflight clearance. The maintainer controlled all gameplay. Codex read receipts,
issued fresh worker challenges and operator marks, then requested STOP. The
approved hooks alter execution/timing; this was an instrumented experiment.
No debugger attachment, synthetic trigger, console call or new hook was used.

| Phase | Operator testimony | Native records observed within marked action interval |
|---|---|---|
| Save25 load | At SOR-003, ship scanner distance 2,427 m. Initial SOR-002 wording was immediately corrected by the maintainer. | 0 |
| SOR-003 → SOR-002 | Ship appeared at its original landing location; no movement noticed; scanner 233 m. | 0 |
| SOR-002 → SOR-003 | Surface-map ship position unchanged; scanner 2,427 m. | 0 |
| One new, previously unvisited accessible Kreet landing | Player stood in front of ship entry ramp after arrival. | Sequences 1–52: one producer/route/grid and one command handoff. |
| LZ-new → SOR-003 | Scanner 435 m; surface map showed ship relocated to a much closer spot. | Sequences 53–1,194: second producer/route/grid and command; all 40 Workshop grids. |

These distances are scanner readings supplied by the maintainer, not a calibrated
native-distance conversion. The contrast supports visible ship relocation on
the experimental return and observed stability during the local control. It
does not establish physical LZ1 identity, a universal relocation rule or which
native operation created a marker. Zero control events are a scoped reachability
result with a healthy worker, not proof that no game code ran or no ship state
changed. No optional checkpoint was made; no additional trip/session occurred.

## Native travel, marker and grid chain

Pinned retail 1.16.244.0 executable SHA256
`7e9adb1414a8e1b325e5e1f097b9b17b78deb7eebeda37a333351a43a60f9d28`;
runtime module base `0x00007ff7a4950000`, PID 17008, process creation FILETIME
134363351123063612, native event thread 36728. Addresses in [design](design.md)
are module RVAs; reference addresses below are runtime VAs, not handles or saved
tokens. Exact SFSE/DLL/tool hashes remain in the approved build and source ledger.

Both request-producing scopes (invocations 1 and 27, kinds 50/51) enclose actual
78B030→77FC20 route scopes (2 and 28). Both routes took the observed
`FALLBACK_REFERENCE` branch after eligibility/search, produced a fresh descriptor,
and called the shared grid at RVA 96F5C0 with paired before/after native bytes.
This is observed fallback selection; allocation/creation inside it is not proved.

| Native marker component | New landing | Return to SOR-003 |
|---|---|---|
| Route/grid invocation | 2 / 25 | 28 / 516 |
| Grid before/after record sequence | 47 / 48 | 1189 / 1190 |
| Chosen marker runtime VA | 0x1fbfab9ae00 | 0x1fbfab9ab60 |
| Sampled marker base FormID | 00007145 | 00007145 |
| Native floor XY | (0, 0) | (0, 0) |
| Native numeric hierarchy (tag, X, Y) | (0, 40320, 20736) | (1, 10464, 21141) |
| Actual output versus captured-input replay | Equal | Equal |

The marker base is the previously identified ship landing marker, distinct from
ordinary Workshop base 002C60E9. Both generic grid outputs are independently
bound to their selected marker and fresh descriptor, not to a Workshop merely
because they share a grid routine. The older alternate-selection helper reports
`selected_reference_bound=false` for these new producer kinds; this is not an
absent producer or absent chosen-marker binding. Producer ancestry and the
generic chosen-reference checks are separately retained in the schema-5 analysis.

Raw R14B decision is 0 in both producer captures. Command invocations 26 and 517
(53/54) each record command +8D=0, +8E=1, and the corresponding captured marker
VA. The commands execute after their producer has returned, with parent 0.
Equal marker addresses/raw values are observations, not a fabricated asynchronous
parent or proof that a downstream ship-assignment consumer applied the command.
The observed flags alone do not classify visible relocation.

## Ordinary Workshop center/grid results

The return producer contains 40 enumeration scopes and 120 callback scopes:
40 ordinary Workshop callbacks execute center→grid-before→grid-after, and 80
other callbacks return early. Thus 120 callbacks do **not** mean 120 Workshops.
All 40 complete grid samples have base 002C60E9, readable concrete ExtraWorkshop
identity bytes, Kreet body 0003F59F, status 0 and stable sampled ref identity
within their callback. The center comes from the actual F4AB80 return; grid output
comes from the actual in-place 96F5C0 result. Neither is synthesized by replay.

| Field | SOR-002 identity f1517de43e171745 | SOR-003 identity 0efca066ee4c7b9b |
|---|---|---|
| Runtime reference VA | 0x1fc2cb23340 | 0x1fc2cbaeee0 |
| First grid invocation / sequence | 49 / 96 | 55 / 112 |
| First record raw-file offset (decimal) | 1687960 | 1972248 |
| Native compensated center XYZ | (22.700454711914062, 73.04623413085938, 3.6431474685668945) | (56.820404052734375, 59.05859375, -9.51641845703125) |
| Captured native translation XY | (100, 200) | (300, 2400) |
| Derived binary32 center+translation XY | (122.70045471191406, 273.0462341308594) | (356.8204040527344, 2459.05859375) |
| Actual native floor XY | (1, 2) | (3, 24) |
| Native input hierarchy (tag, X, Y) | (1, 10464, 21120) | (1, 10464, 21120) |
| Native output hierarchy (tag, X, Y) | (1, 10465, 21122) | (1, 10467, 21144) |
| Samples | 20, identical reported operands/output | 20, identical reported operands/output |

For SOR-003, input middleY at descriptor +0x18 is 0 and fineY at +0x28 is 0;
adding floorY 24 produces middleY 2, fineY 0. This is a directly encountered
fine-to-middle radix-12 carry, supported by actual result bytes, not only a
prediction. CoarseY remains 110 and tag remains 1. Opaque neighboring handle
fields also change, but numeric equality does not validate their semantics.
SOR-002 has no such carry. These are two distinct geometries within one producer,
not 40 independent blind holdouts or 20 independent gameplay repetitions.

The original audit independently checks binary32 addition/scale/floor and scalar
192/12 hierarchy additions for this no-face-crossing domain; the reviewer also
checks raw arithmetic without the production `offset()` helper. The selected
CSV preserves all 40 cases and exact raw/journal offset domains. No translated
register value was captured: translated XY is explicitly DERIVED from captured
operands. The third sampled translation word has no assigned Z semantics.

## Unchanged frozen predictions: agreement and counterexamples

The 23 frozen predictions remain SHA256
`a8a7402697ed866a3410d4bd58796de513c7ca11f89e770a80deb5a8651a0487`;
their inputs remain `9fe2924ff7bc444714fbab685893b8d8e0572dc2c7aad96cbd06de8aac93ad91`.
Candidates were selected by independently captured Workshop identifier, ordinary
base and body, not by a numerically nearest output. Each identity selects the
Save25 and Save26 entries; only Save25 was loaded in this experiment.

All 40 native result cells equal those candidates' numeric cells. Derived
translated XY also equals their frozen center XY bit-for-bit: SOR-002
`a266f542eb858843`, SOR-003 `0369b243f0b01945`. This is a positive conditional
numeric correspondence for two outposts/four existing prediction rows. The
other 19 frozen rows received no native comparison, and Save26 received no
separate load test.

Raw native compensated-center XYZ is **not** equal to frozen compensated-center
XYZ in any of the 40 samples. XY differs by the captured translation. Z remains
3.6431474685668945 versus frozen 18.352506637573242 for SOR-002, and
-9.51641845703125 versus frozen -31.89084243774414 for SOR-003. ExtraWorkshop
+0x60 compensation is zero in both sampled live identities. These observations
reject an unqualified same-XYZ/same-frame equality claim. They do not falsify the
durable model's conditional saved-frame prediction: captured cell/world pointers
are null/unreadable in all 40 grid records, so the full loaded-parent/frame and
restoration join cannot be independently completed from these sampled fields.
No rebase or height explanation is promoted from numerical agreement alone.

Generic terrain-grid agreement, marker identity, ordinary Workshop center/grid
agreement and full durable equivalence are separate results. Full Workshop
equivalence, native Z restoration, opaque handle reconstruction, marker creation
and actual applied ship assignment remain NOT TESTED/UNKNOWN. No radius, visible
border or metre conversion is inferred from these operations.

## Integrity, cleanup and retained corrections

Preflight passed 6,294 checks; postflight passed 6,291. Both verified 6,241
protected paths, including prior captures, save inputs, old observers and frozen
predictions. All 21 patch receipts and 19 RX relays were checked at admission.
Independent fresh worker ACKs preceded save load and each action. The worker
recorded 742 health rows, maximum QPC gap 4.1601449 s; final entered counts are
(341, 40, 126), active/queue/lost/depth/health-failure counts zero. There was no
arbitrary event/time/cadence cutoff. External checks were at action boundaries;
continuous one-second external monitoring is not claimed.

All 1,194 records have validated hashes/sequence/extents and normal schema-5
scopes. Raw size is 21,214,992 bytes, no unjournaled or incomplete tail. STOP
drained to clean retirement with code resident/inert until exit. Maintainer
reported normal exit and completed Steam sync; machine checks confirm process
absence and deployed DLL removal. Save inventory: 260 files byte-unchanged,
one ExitSave removed and one new ExitSave added, no changed retained file.
No save was restored/edited and no manual checkpoint created. Source, approved
build, HEAD and index remain unchanged.

The original 60-file seal SHA256 is
`e73dbe60db556b3654831a966aababe7026fc098e158674ea556cc97e02d16a3`.
The scientific audit independently rehashed all 60 files and exactly reproduced
the stored schema-5 analysis. Sealed originals are not edited to add this report.

Two corrections are retained explicitly. First, earlier postflight delivery
omitted this required scientific report; the seal/automated analysis was not its
completion. Second, sealed `postflight-closure.json` incorrectly describes 40
legacy `incomplete_diagnostics` as lacking helper detail. These are legal
query scopes with kinds [7,20,8], all normal-complete and status 0. The older
route helper's two-record `pair()` check causes the diagnostic label; no raw
events are missing. This report supersedes that explanation while preserving
the original sealed bytes and approved helper unchanged. The new audit's first
comparison attempt failed on integer-versus-JSON-string scope keys; a JSON
round-trip fixes only representation equality. The failed attempt note remains
local; no raw/frozen result was adjusted.

Evidence roots are repository-relative: original run
`.local-work/ship-relocation-050/live-20261013T031605991759Z/`, raw session
`.local-work/native-oracle-live/session-17008-144157125/`, new audit/review
`.local-work/ship-relocation-050-scientific/`. The source ledger pins individual
files and the audit script. See the linked review for actual independent checks,
criterion matrix, prior-work/task-only diffs and publication exclusions. No new
live action, source/build modification, staging, commit, push or disclosure was
performed while completing this report.
