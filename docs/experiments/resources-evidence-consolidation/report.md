# Resources, production and power evidence consolidation

**Historical preparation checkpoint.** The separately authorized
[execution and postflight](execution.md) supersede the pending-GO status below;
original preparation measurements and limits remain unchanged.

The real consolidated archive contains **134,131 files / 7,998,429,154 logical
bytes**. Independent archive and physical-restore checks passed for every member.
The exact original-retirement plan is prepared; **originals retired: 0; actual
historical pins removed: 0; replacement baseline: inactive**. The
[separate GO card](execution-card.md) governs the remaining migration. This is a
preparation result, not completion of physical retirement. See [review](review.md)
for the exact independent acceptance boundary.

## Scope and identities

The [invoked brief](../../implementation-briefs/CODEX_BRIEF_SOR_resources_production_power_evidence_consolidation.md)
retains AC1–AC8. [Subareas](subareas.csv) enumerate all 58 current system roots,
not 58 archives. The owner is `resources-production`; original relative paths
remain member locators. The current eligible roster matches the Stage A scoped
ownership set exactly: no additions or missing files.

| Population | Files | Logical bytes | Disposition |
|---|---:|---:|---|
| Current eligible system | 134,140 | 8,002,753,894 | Exact frozen roster |
| Consolidated and proposed for retirement | 134,131 | 7,998,429,154 | Every original still present |
| Eligible loose holds | 9 | 4,324,740 | Outside archive and retirement plan |
| Protected/opaque/save exclusions | 969 | 10,305,652,112 | Metadata only; no new saved-payload hashing |

Seven holds preserve current export scripts whose historical expected versions
conflict: `.local-work/{e1-arithmetic,e1-intervals,e1-production,e2-organic,e3-fabricators,p1-load,p1-order}/export.py`.
The other two are active preservation inputs:
`.local-work/resource-carinae/sync-paths-preflight02.json` and
`.local-work/resource-carinae-source-context/protected-before.json`.
None of these nine occurs in the actual 93,334-pin historical inventory.
No save stream or analysis database suffix was admitted. The separate protected
manifest has 12,974 rows; 12,058 overlap archived identities, with no digest
conflict. This does not alter the prospective save-protection policy.

The primary authority anchors are the committed Stage A source ledger
`docs/experiments/evidence-archive-discovery/sources.csv`: EAD-S022 inventory03
SHA-256 `4bd07ae2906d1aaec146b254b3bd833de81458bacae2c7244a485d0f670ff462`
and EAD-S028 scoped-owner database SHA-256
`b57c2101acf51fda2e17b478a15b885f9725a7ef0c128043ec4f96aae3bc62fc`.
Local `source-selection-qualification.json` checks that normalized working ledger
content equals HEAD and that current paths equal the scoped owner set. Current
source hashes are checked against established historical pins where available;
newly admitted current digests are identified separately in local admission data.

| Object | Bytes | SHA-256 |
|---|---:|---|
| `resources-production-preparation01/resources-production.tar.zst` | 351,425,006 | `2df3244872961232c87067ca60e2c59e54ab66d7c2c858031db2649cc86ed8a5` |
| Embedded inventory | Included | `de8b2aa5f2fe89878ef8d8a1f4708952302250f955cdddfab1b4e7eaf1c8d8d1` |
| `index-resources-merged-proposed01.json` | 38,249,694 | `268f8c2c188dc640091d0ddc041ee547db5f9fb9e1f592031e24452fcd2e1995` |

These objects are below ignored `.local-work/research-archives/`. The combined
proposed index preserves the existing Cargo entry and cross-references exactly.
The old Cargo `index.json` remains its immutable committed compatibility root,
SHA-256 `5500892dbc247c642b83336ee619ca34d40fae8967ccfda95c5394e7ceff7e3b`;
Cargo archive SHA-256 remains
`ebda740f0092b93f1dc9f32120db365223f465a6d374ce8e98933e8041eb1da7`.
Only the combined version would become the central current index after GO.
There is one new owning archive, not a payload archive per experiment.

## Consumers and routine work

| Consumer or dependency | Current treatment and evidence |
|---|---|
| Maintained Carinae and tungsten preservation readers | Share authenticated selected-archive substitution after activation; retain exact old expected digests, survivor hashes and protected-save policy. Before activation they retain their original checks. Both readers passed selection/control/index/journal tamper cases. |
| Historical D4E corpus reader | Unchanged `research/resource-standalone/isolate.py`, five restored historical modules, two corpora and original request; fresh empty directories, `-I -S -B`, full stdout equality and read-audit checks. |
| Shared E2 inventory | `research/{c1-cargo/sources,s1-storage/catalog,p1-power/definitions,e3-fabricators/catalog}.py` reference `.local-work/e2-organic/inventory02.json`. One original-path locator under the resources owner supplies a bounded authenticated restore; no duplicate owning archive. |
| Other historical acquisition/admission methods | Closed prerequisites remain in force. The dependency ledger records 297 tracked Python candidate/read-site records, not 297 universally qualified runnable consumers. Broader save/ESM/historical prerequisites are neither replayed nor relaxed. |

The two replayed stdout bodies are each 90,228 bytes, with hashes
`898faffea1ccfc87df2fdd6864c89704585ea8770b9610d4a741ca6134436ce7`
(normalized) and
`af4d8d81c6aef79882ad61ddc80aac644d610ca5850b15af58b768da7080a12f`
(expanded). Each denied eight guard probes, reported no forbidden inference
and read only restored inference inputs plus interpreter runtime. This proves
those complete reader outputs, not every historical script or scientific claim.
`dependencies-final.json` preserves the candidate limitations; unknown external
or dynamically constructed consumers are not ruled out.

Both actual historical audit files contain **93,334 pins**, SHA-256
`a243c67c0e451aac21cbb5fcb671c9e94ad2b3806406d0fdec1b2626f153ab9b`.
Exactly **91,933** overlap archived originals, all checked against actual bytes:
2,608,506,655 bytes read in 645.396 seconds. The future historical boundary has
**1,401 loose pins + 2 archive/index objects = 1,403 payload objects**; adding
the nine new loose holds gives **1,412 unique payload objects**. The 42,198
archived files outside those old pins receive no historical pin-relief credit.
The proposed 98.5% historical object reduction materially advances the programme's
≥80% aim, but the actual current reduction is zero. Control, journal, baseline,
namespace and protected-save work are additional to these payload counts.

The archive/index-only sample read 389,674,700 bytes in 8.772 seconds with zero
member payload hashes. This is not a full after-routine benchmark. The complete
activated routine, surviving-file cost and actual postflight remain **NOT TESTED**
before GO. The earlier preservation-optimization AC4 remains **FAIL / REWORK**.

## Restoration, safety and provenance

The real build took 747.152 seconds and initial archive verification 31.549
seconds. An independent stdlib tar/hash pass checked all 134,132 entries,
including the embedded inventory, in 60.316 seconds. A complete C: restore was
then independently reread: all 134,131 payload files, 134,132 namespace files
including LEASE, 4,724 directories and distinct single-link regular file objects;
all hashes and final lease/index identities matched in 127.490 seconds.

C: temporary staging was justified by the measured 100-file durable-write probe
(D: 7.855 seconds; C: 0.174 seconds). It held a disposable restore only, never an
archive replica. After complete independent C: proof, the earlier healthy D:
worker was deliberately superseded using verified process creation/image/command
identity. Native exit 75 was normalized by the tool session to exit 1; it was not
an unexplained evidence failure. The D: subset contained 89,263 verified complete
files / 6,197,589,062 bytes. One 3,145,728-byte matching incomplete prefix remains
in ignored `superseded-d-diagnostics01`, SHA-256
`d9b55907a75b91ba16126e6bde904b6a3fdece267cd6ff180abb0357820608e3`.
Both authenticated temporary leases were cleaned only after proof; these removals
are not original-evidence retirement. C: staging contains no remaining files.

Both volumes retain the 40,000,000,000-byte free-space guard. Material writes
reserve capacity on their actual destination, including C: when staging.
The following are capacity envelopes, not measured compression or peak samples.

| Phase | Additional write reserve | Available before minus reserve |
|---|---:|---:|
| Build on D: | 36,422,475,656 bytes: four times source bytes + 32 KiB/member + 32 MiB | D: 82,128,654,336 − reserve = 45,706,178,680 bytes; C: 92,043,104,256 bytes |
| Full D: restore after build | 12,427,188,194 bytes: payload + 32 KiB/member + 32 MiB | D: build-completion checkpoint 81,739,661,312 − reserve = 69,312,473,118 bytes; actual write guard rechecked before restore |
| C: alternate, while D: partial existed | 12,427,188,194 bytes on C: | C: 91,905,802,240 − reserve = 79,478,614,046 bytes; observed D: 75,767,345,152 bytes still exceeded floor and remaining D: payload need |
| Pending original migration | 536,870,912 bytes for journal/metadata/review | Both volumes remeasured immediately before GO; no full restore copy required |

The temporary payload high-water set held the complete 7,998,429,154-byte C:
restore plus 6,197,589,062 complete D: bytes and its 3,145,728-byte partial prefix.
Recorded free-space samples during that phase stayed above C: 82.3 GB and
D: 75.1 GB; they are sampled observations, not continuous minima. Cleanup removed
only those proved working copies. Original-source recovery remains zero.
Local `measurements-final.json` supersedes the preliminary 6,927,992,912-byte
allocation-only estimate with a **5,701,554,176-byte conditional net projection**
across both volumes. It credits 8,077,164,544 bytes of large archived source-file
allocation, charges 852,303,872 bytes on D: (the greater of observed window loss
and 741,965,584 bytes of retained task file allocation), charges the entire
986,435,584-byte observed C: window loss, and reserves another 536,870,912 bytes.
Those whole-volume losses include unrelated/filesystem effects; they are not
claimed as causally measured task allocation. The reserve includes the exact
97,994,299-byte future journal, 338,411-byte baseline, metadata and final review.
Nine holds receive no retirement credit. Resident/small files and directory/MFT
recovery also receive zero credit. This is a conservative projection conditional
on approved retirement, not observed recovered space.

At that final checkpoint C: had 91,063,324,672 bytes free and D: 81,463,156,736,
against initial 92,049,760,256 and 82,315,460,608. Physical original-retirement
recovery is still zero. Future free-space movement must be measured independently
at GO/postflight; compression ratio alone cannot establish it.

The final read-only real-profile test locked 4,737 directories and all 969
excluded-file metadata handles, confirmed 134,140 eligible originals still
present, and read zero saved-payload bytes (259.932 seconds). It exercised the
real locking/census scale without a deletion INTENT. Fault qualification covers
metadata-only source changes, wrong owners, control-cap limits, tampering,
identity races, interrupted journals/selection, cleanup boundaries, C: headroom
and partial reconciliation. Twenty focused cases pass; the changed generic
executor also passed all 35 Cargo regression cases and the original save policy
all 14 cases. The existing committed Cargo routine still verifies independently
of the proposed resource selection. Exact source snapshots and outputs identify
which tests cover each implementation revision.
Final manual reading corrected four source documentation/comment contracts;
their non-docstring ASTs are unchanged. `documentation-delta.json` preserves the
before/after hashes. The focused suite was rerun on the final source; the prior
35-case Cargo and 14-case save-policy results retain their exact source snapshots
and this documented equivalence limit.

Two diagnostic failures remain visible: one C: low-space fixture initially
constructed its mock incorrectly (TypeError before testing the guard), then was
fixed; an independent restore review initially compared row-list order, then
corrected the oracle to complete path-to-row equality before reading payloads.
Neither is hidden or counted as a successful original run.

Execution used installed CPython 3.14.3 / Windows NTFS, executable SHA-256
`cce21c0e8710e304273e98ac4b2b0f5aceb639acbcd2343cbaa5c4e81619c45b`.
Some early method versions were reconstructed after code edits made while
already-loaded build/restore workers ran; `execution-provenance.json` explicitly
marks that limitation. They are not contemporaneous source snapshots. C:
restoration likewise preceded a change confined to its unused partial-sealing
function. Independent full archive and physical-file hashes establish the actual
preserved bytes separately. Final execution methods are frozen before GO.

## Acceptance and limits

| AC | Preparation evidence | Remaining operational result |
|---|---|---|
| AC1 | Exact scope, owners, exclusions and separate authority | GO still required; no live or Git mutation authority |
| AC2 | Current roster, dependency ledger, holds, exact historical overlap | Revalidate identities immediately before authorized retirement |
| AC3 | Real authenticated archive and independent complete physical equality | Maintain the verified archive as recovery root |
| AC4 | Both maintained protection readers, complete real corpus replay, shared locators | No universal historical-script claim; postflight replay required |
| AC5 | Exact inactive before/after accounting and scoped sample | Actual reduction/full routine timing NOT TESTED |
| AC6 | Complete exact allowlist, recovery proof and projected positive majority retirement | Physical retirement/COMMITTED activation NOT TESTED; awaiting GO |
| AC7 | Durable receipts, guards, faults, methods, editorial and exact patch delivery | Final package hashes/review govern the submitted snapshot |
| AC8 | Independent technical/archive/physical reviews and final package procedure | Final preparation verdict in review record; narrow post-GO review still required |

The archive may become the only local copy after authorized retirement. Its
byte integrity has been tested; this does not provide off-device redundancy or
protect against loss of D:. Cloud backup is a future decision. No game launch,
debugger, save modification, native-analysis edit, scientific predictor change,
new third-party dependency, contact, upload, staging, commit, push or publication
was performed. Raw archives, members, controls and restores are **LOCAL-ONLY**;
authored methods/reports are **REVIEW-REQUIRED**, and publication/B6 remains on
hold. Project-owned Stage A/B, Cargo and historical-reader reuse is credited
under SOR-P-0002 in [sources](../../SOURCES.md) and [credits](../../../CREDITS.md).
