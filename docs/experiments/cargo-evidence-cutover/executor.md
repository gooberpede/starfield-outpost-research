# Cargo retirement executor qualification

2026-10-26, Australia/Sydney. Governing authority is the
[retirement and activation brief](../../implementation-briefs/README.md#archive-lookup) (`implementation-briefs.zip :: docs/implementation-briefs/CODEX_BRIEF_SOR_cargo_evidence_retirement_baseline_activation.md`).
**Real deletion and baseline activation are NOT AUTHORIZED.** This work implements
and tests a separate transaction on disposable Cargo replicas. The accepted
[consumer cutover](report.md) remains the scientific baseline; no gameplay or
persistence conclusion is changed.

## Scope and chosen method

Reuse the existing [resolver](../../../research/evidence-access/access.py),
[preparer](../../../research/evidence-access/retirement.py), Stage B locked-handle
and index checks, and Stage A strict decoder. A quarantine move would retain the
loose population and would not demonstrate retirement. Replacing the archive
format would enlarge scope without improving this bounded question. The chosen
method adds exact-file handle disposition, a durable transaction journal and a
Cargo-specific verification baseline. It does not modify project-wide protection
utilities or the historical 93,334-pin inventory, which contains no Cargo members.

Reads are limited to repository guidance, current source/tools, accepted Cargo
artifacts and all 1,054 Cargo originals. Writes affect authored code/documents and
ignored disposable fixture, control and review directories. No save, installed
game asset, analysis project, historical archive or original evidence is a write
target. No staging, commit, push, live operation, dependency installation, network
operation or publication is part of this assignment.

## Transaction and baseline schema

`sor-cargo-retirement/1` remains an inactive proposal. External authorization
names its exact hash, the recovery/shadow hashes, source root, archive/index and
embedded inventory roots, transaction directory, tool identities, HEAD/index,
expiry and exclusive directory ownership. An externally supplied approval digest
is the operator's trust boundary. JSON cannot prove that its author is the human
maintainer: an implementer-generated approval is never authority for real data.
Fixture approvals name only disposable roots.

| Durable state | Meaning and allowed continuation |
|---|---|
| PREPARED | All present source identities, three holds, complete archive and controls verified before removal. |
| RETIRING | Each exact path has a flushed INTENT before disposition and a flushed DONE afterward. Only the exact approved prefix may be replayed. |
| RETIRED_PENDING_BASELINE | Every approved source is absent; holds survive; the archive remains authenticated. Routine verification still blocks. |
| COMMITTED | Same-volume baseline publication and a final flushed journal event agree. Routine Cargo checks use archive/index and three holds. |
| RECOVERY_REQUIRED | A derived blocking disposition for a torn/invalid journal, unexplained absence/presence, unknown artifact, unavailable archive or conflicting baseline. No automatic truncation, wildcard cleanup or declaration of success. |

The journal uses ordered, hash-chained, flushed JSON records. Hashes establish
continuity, not protection against an administrator rewriting all trusted inputs.
The baseline has schema `sor-cargo-active/1`; it binds the controls, prior baseline
hash, exact five replacement rows, retired count and pre-commit journal prefix.
An unpublished baseline never changes routine authority. The original full
baseline remains in the authenticated shadow document for recovery planning.

Retirement cannot be rolled back by merely switching a policy pointer: removed
files must first be restored and independently verified. An INTENT with an absent
source may be reconciled only from the authentic journal prefix and complete
archive. Missing sources without an INTENT block. A torn tail or uncertain
temporary baseline stays preserved for explicit recovery. A failed commit is not
reported as complete retirement, even when every source was already removed.

## Safety and limits

Sources are opened with Windows handles denying writes and deletion sharing;
directory handles prevent ancestor rename/delete. The file hash and identity
are checked through the same handle used for disposition. The full archive,
index and immutable controls stay locked through the transaction. Both C: and
D: must retain at least 40,000,000,000 caller-available bytes; sensitive writes
also reserve workspace/journal capacity on D:. No C: authority or cross-drive
atomicity is assumed.

Windows source sharing alone does not prevent hardlink creation. Qualification
reproduced that race. The corrected executor queries live link state before
disposition and again while the original is delete-pending. On qualified NTFS,
the pending original no longer contributes a link and new links through its
path are denied. A surviving alias yields a nonzero link count; the executor
cancels disposition, preserves the original and blocks. Actual alias-race,
pending-link and cancellation tests support this specific filesystem behavior.
The journal retains its own writable handle denying concurrent write/delete;
each append is flushed and reread through that handle. RUNNING serializes
cooperating executors; it is not relied on to protect journal bytes.

Six historical empty directories discovered by real preflight are explicitly
listed in `EMPTY_DIRECTORIES` and the approval binding. They survive unchanged;
unknown directories still fail. That reconciliation changes no allowlist member,
original file hash, held version or archive identity. Routine checks authenticate
archive/index and three held payloads, plus the pinned controls and journal;
the five-object payload count excludes those additional metadata reads.

Qualification covers process interruption and software faults, not physical
power loss, hostile kernel behavior or an administrator bypassing the declared
exclusive namespace ownership. The real archive is a single authoritative local
copy. Losing it after retirement can make removed evidence irrecoverable. No
off-device copy, independent physical backup or cloud upload is required or
claimed. Temporary archival replicas are test inputs, not enduring authorities.

The [execution card](execution-card.md) is a separate future decision package.
Approval of this implementation or reviewer acceptance never supplies its GO.

## Qualification and preserved counterexamples

The complete [35-case matrix](executor-faults.csv) corresponds to own run
`.local-work/cargo-retirement/qualification-8c1ad45b29c24fcfa268a29226254d01/`
and independent rerun `qualification-95813c33a6e34acd98d23fa564d0671c/` under
the same root: **35/35 PASS in each**. Each `results.json` records actual rejected
exceptions and case outcomes. `executed-methods.json` pins seven methods and
their exact copied bytes, Python 3.14.3, its executable hash and Git state;
the harness verifies those method bytes remain unchanged through the run.

Controls include normal exact retirement; corrupt source/archive/index/inventory/
allowlist/recovery/shadow; replaced inode; extra/missing source and hold;
read-only deletion failure; unsupported paths, junctions, hardlinks and unknown
cleanup outputs; both-drive guard failure; real concurrent source writes/deletes,
ancestor rename and journal mutation; actual hardlink admission and cancellation;
torn journal tail; stop after INTENT, deletion, or baseline publication; restart,
double activation, stale/bogus approval and transitive-method substitution.
Before/mid-transaction routine probes supply an actual baseline hash when one
exists: a published baseline without COMMITTED still blocks. A separate control
shows committed verification survives unrelated later HEAD/index changes while
using its externally retained baseline hash.

The archive-loss negative case removes one synthetic source, then destroys its
only synthetic archive. Restart and routine verification block; restoration of
that removed payload is impossible from surviving inputs. The torn-tail and
unpublished `baseline.writing` cases also deliberately remain blocked. These
are correctly preserved failures/recovery dispositions, not successful retries.
Process-exit qualification uses a child exiting with code 73 immediately after
deletion, then a fresh manager replays its persisted INTENT safely.

Earlier trials remain distinct. The first 27-case run failed at fixture manager
construction because archive-index and repository-index keys collided; no
retirement occurred. An initial corrected suite passed 27 cases, but independent
review reproduced hardlink admission during a locked deletion and journal
overwrite followed by a false COMMITTED return. It also found late missing-hold
detection and incomplete transitive tool binding. Corrections added live
post-disposition alias checks/cancellation, a persistent journal handle, early
hold presence and method pins. Review then strengthened two test oracles: missing
holds must leave every source unchanged, and partial-baseline verification must
reach the authenticated journal-state check rather than reject a missing argument.
These defects and their original receipts were not relabelled as passing tests.

The first complete 1,051-file disposable replay passed before those corrections;
it is historical corroboration, not final-code proof. A later real preflight
stopped on the six existing empty directories before replica construction.
Explicit directory reconciliation was followed by final qualification and a new
full replica. Early pre-snapshot runs lack the final harness's executed-source
freeze; their narrower provenance is not substituted for final evidence.

## Full replica reproduction and real preservation

The exact final full run is
`.local-work/cargo-retirement/replica-68afcce634134a859eb090ba7da2cdb0/`.
Its `summary.json`, `retirement.json`, `routine.json`, `consumers.json` and
`lease-cleanup.json` establish removal of all **1,051 disposable originals**,
COMMITTED replica baseline, zero routine retired-member payload hashes, two
complete consumer reproductions and absence of the temporary consumption lease.
The replica archive/index are copies authenticated against the real external
trust roots, and its three held packagers use copies of the current real holds.

| Complete workflow output | Frozen and replay SHA-256 |
|---|---|
| C1 `menu_abc.py` JSON | `0ecf10ee374dc3e8994b21ba6f75d6bc6fb13b674a5b488a9296292e9926ab70` |
| C2 `pex.py` JSON | `22b5169577439d2372c17d7df45d2b39b603dc1f46b0b791794cf67cdea0d4e6` |

The full parsed JSON objects and complete output bytes agree; these are payload
reader workflows, not replay of historical acquisition environments. Frozen
scientific claims are unchanged. `real-before.json` and `real-after.json` contain
all 1,054 exact identities, including three excluded holds, with equal ledger
SHA-256 `d9e097f69025d59e4bd1b5119b7ad89a0b5556dec551211e32399abe66db4de1`.
The independent reviewer separately read/hashed the same real population and
archive. Final scoped postflight rechecks this ledger and HEAD/index.

Task HEAD is `6c22cc3c4e57838583e594e9db1c925bf139ced9`; repository index SHA-256 is
`b8d3bc5ae135235f6c8fca96e87da0b208657aecfcd8a292fca14e807719d38a`.
The supplied brief was the sole initial untracked file. It is preserved unchanged
and appears separately in the complete patch. No unrelated starting work existed.
No real source deletion or baseline activation occurred; no protected save,
installation or analysis database was an experimental write target. Scoped
preservation is not a new whole-estate or 90K-pin audit.

## Retained costs and disposable lifecycle

The source allocation credit remains the earlier conservative **34,758,656 bytes**,
with **19,066,880 bytes** of already retained archive/index, prior run/audit and
executed-method costs. The previous task's unspent 2 MiB reserve is replaced by
actual costs for this assignment and explicit new reserves; it is not charged
twice or treated as recovered capacity. Local `storage.json` itemizes the final
retained population, deduplicates hardlink identities, skips junction traversal
and rounds persistent costs upward using 4,096-byte D: allocation units.

Fresh disposable fixture payloads, archive/index copies and stale metadata leases
were disposed of after qualification using exact file/identity/hash manifests.
`fixture-disposal-plan.json` and `fixture-disposal-result.json` record 2,476 files /
14,417,518 logical bytes removed from test directories only. This includes the
synthetic Stage B builder's indexes/journals, not executor transaction journals
or any preexisting historical receipt. Unknown types, aliases, read-only and
reparse fixtures were held rather than broadly cleaned.

`synthetic-input-disposal-plan.json` and its result separately record removal of
745 earlier synthesized plan/recovery/shadow/approval input documents, totaling
1,425,132 logical bytes. Their generating methods and result histories survive.
Every executor transaction journal/baseline, primary result, failure/reviewer
receipt, executed-method snapshot, complete consumer output and actual replica
control remains. Final own and independent synthetic inputs also remain. Neither
disposal affects the real archive/index, original 1,054 sources, accepted real04
controls or historical review packages. Temporary replica stores are no longer
available after this deliberate test lifecycle; their earlier routine PASS is
an observation at the tested boundary, not a claim they remain active authorities.

The final storage table and local closure record bind the exact projection.
An independent current read remeasured 338 eligible source streams contributing
the same 34,758,656-byte conservative allocation credit. At accounting, current
task artifacts cost 12,791,808 bytes. The table charges a larger fixed envelope
of 13,000,704 bytes; closure checks require actual retained task costs to fit it.

| Projected cost or recovery | Bytes |
|---|---:|
| Conservative original-source allocation credit | 34,758,656 |
| Prior retained archive/index, run and audit costs | −19,066,880 |
| This assignment's retained artifact allocation envelope | −13,000,704 |
| Future exact transaction reserve | −1,048,576 |
| Final ledger, review and complete/task-only export reserve | −1,048,576 |
| Conservative projected net after all listed retained costs | **593,920** |
| Actual original-source recovery | **0** |

This supersedes the earlier 13,594,624-byte projection for the final execution
card. The smaller positive margin includes failed/repeated tests and independent
review fixtures. It is a file-allocation projection with explicit reserve limits,
not observed physical capacity recovery. If either retained-cost envelope is
exceeded, recompute and re-review rather than silently assuming positivity.

One MiB is reserved for the future transaction; its deterministic journal is
696,843 logical bytes and baseline 3,080 bytes before allocation rounding and
approval overhead. Final review/export/ledger costs have a separate allowance.
Directory/MFT recovery and physical free-space causality remain unmeasured.
All removal measurements in this assignment refer to disposable test artifacts;
**actual recovered original bytes and real retired files remain 0 / 0**.

The final replica's observed free space was C: 92,070,993,920 and D: 82,276,528,128
bytes before, C: 92,056,887,296 and D: 82,264,363,008 afterward. All exceed the
40,000,000,000-byte floor. These dated observations include unrelated system
activity and never substitute for a future preflight or actual recovery measure.

## Frozen acceptance and review

The original brief's AC1–AC8 wording remains authoritative. The table below is
an evidence index, not a change to mandatory criteria or self-issued acceptance.

| Criterion | Implementer result | Primary evidence and limits |
|---|---|---|
| AC1 | PASS | Baseline/final Git pins and 1,054-source ledger equality; operation log and exact disposable-only cleanup; no real retirement/activation/target/Git writes. |
| AC2 | PASS | Real before/after ledgers, independently checked archive/index/inventory/plan roots, 1,051 exact members and three held exclusions. |
| AC3 | PASS | Reviewed state machine, authorization/tool binding, same-handle disposition, locked/readback journal, restart and baseline handover; qualified NTFS/process-interruption scope. |
| AC4 | PASS | Own and independent 35-case matrices, original defect receipts, stronger regression oracles and explicit unrecoverable negative case. |
| AC5 | PASS | Final full disposable retirement precedes authenticated consumer restoration; complete C1/C2 byte equality and lease absence. |
| AC6 | PASS | Routine committed protection uses archive/index plus three holds, with control overhead disclosed; partial state blocks; final reserved projection is 593,920 bytes. No real/global policy activation or D5G pin savings. |
| AC7 | PASS | Source/helper inventory, original failures, exact card and postflight checks; full changed prose screen/manual reading and independent editorial ACCEPT. |
| AC8 | PASS | Independent substantive ACCEPT covers all eight criteria; final closure delta, exact snapshot, complete/task-only patches and manifests are bound by the detached delivery record. |

The original real allowlist, archive/index and embedded inventory hashes remain
unchanged. Local `approval-template.json` is deliberately inert;
`execution-identities.json` independently derives the proposed baseline hash
without creating a real transaction. No permission issue blocks the performed
offline scope. Real execution still requires the [card's separate approval](execution-card.md).

Independent substantive review accepted all eight mandatory criteria at snapshot
`0cb10b452bc99ef7071c57d2d16c78f23bc97fea6af43602161ec2a304371438`.
Its verbatim return is local `independent-substantive-review.md`. The final
closure text, refreshed exports and retained-cost bounds receive a separate
narrow delta review, retained alongside the final delivery manifest. The reviewer
independently reran the 35-case suite and authenticated real identities/allocation;
it inspected the complete replica and scratch-application receipts rather than
independently rerunning those two operations. No broader coverage is claimed.

Scientific outcome is preservation/reproduction of the accepted Cargo evidence
version, with no new game/save inference. Engineering outcome is bounded NTFS
retirement/recovery qualification; hardware power-loss survival is unknown.
Target survival is not applicable. Publication remains NOT CLEARED. The detached
independent review governs accepted completion; any REWORK remains this assignment.
