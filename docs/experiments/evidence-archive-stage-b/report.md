# Stage B cargo archive qualification and retirement proposal

2026-10-26, Australia/Sydney. Under the
[frozen AC1–AC8 contract](../../implementation-briefs/CODEX_BRIEF_SOR_consolidated_evidence_archival_stage_b_pilot.md),
the real cargo archive and complete disposable restore pass byte verification.
**No original has been deleted or changed. Storage recovery is not complete.**
The safe conditional retirement set contains only 37 historical editorial-package
files; active cargo-tool dependencies and three disputed packager versions remain
loose. Retiring that set would still leave a net storage cost. Recommend deferring
cleanup until separately scoped consumer work makes a useful larger cutover safe.

## Exact identities and preservation

All local paths below are repository-relative. They are LOCAL-ONLY, excluded from
Git and publication. The [continuation card](continuation.md) is the decision
package; [method documentation](../../../research/evidence-archive-stage-b/README.md)
describes reads, writes, prerequisites and limitations.

| Artifact | Local path | SHA-256 |
|---|---|---|
| Final archive | `.local-work/research-archives/cargo-transport-fuel-b02/cargo-transport-fuel.tar.zst` | `ebda740f0092b93f1dc9f32120db365223f465a6d374ce8e98933e8041eb1da7` |
| Sole active central index | `.local-work/research-archives/index.json` | `5500892dbc247c642b83336ee619ca34d40fae8967ccfda95c5394e7ceff7e3b` |
| Embedded member inventory | `ARCHIVE-MEMBERS.json` inside that archive | `f46605615abca2ff026f46aad6f51162a554c4383e89b79048899e4fb6e39a7a` |
| Exact conditional deletion manifest | `.local-work/evidence-archive-stage-b/deletion-manifest02.json` | `c80ac405e2f3af32fb715df6dc053865cc53756975fbae550e4a7ff40aed7eb7` |
| Retain-loose inventory | `.local-work/evidence-archive-stage-b/retain-loose02.json` | `42408ecbff27945e741a0a4c3675d0398f4bb0ab4de821ffe89ade1c9428c028` |

Stage A's exact 1,054-file set reconciles to 34,598,790 logical bytes. Fresh
source hashes match every Stage A expected current identity. Seven historical
CSV ledgers are separately authenticated; 510 members match that resolver's
historical expectations. Its other 544 members have UNKNOWN historical identity
within that resolver's coverage, rather than proof that no older pins exist.
Four additional editorial receipt identities match the existing final seal.
Current readable equality establishes bytes, not scientific semantics.

The three version holds are `.local-work/c2-transit/package.py`,
`.local-work/c2-transport/package.py` and `.local-work/c3-fuel/package.py`.
Their current bytes match B5's creator inventory but not earlier execution pins.
`version-holds02.json` preserves every exact expected hash and ledger origin.
They are excluded from the archive and deletion set, retained loose unchanged.
Synthetic copied-method controls reject each old expectation against its current
bytes. No newest-version rule or overwrite resolves that historical difference.

The archive contains 1,051 original files, 34,579,565 logical bytes, plus one
embedded inventory. Full restoration creates 1,052 regular files containing
35,379,174 bytes. Every restored member is hashed again after writing.
`real-restoration02/` retains the complete proof. `source-postflight02.json`
records all 1,054 originals still equal their frozen sizes, hashes and reported
allocations. An independent reviewer also reread all originals and restored
payloads, and used stdlib tarfile separately from the project decoder to verify
all 1,052 members. This is recoverability of these bytes, not a new cargo finding.

## Consumers and ownership

`freeze02.json` records every origin, expected/current hash, owner, historical
expectation and consumer disposition. `membership02.json` contains the admitted
subset. `consumers02.json` records the fresh authored-reference scan with exact
source hashes and line numbers. Literal references do not prove execution and
cannot exclude unknown external or dynamically assembled consumers.

The fixed `.local-work/c1-cargo/`, `c2-transit/`, `c2-transport/` and `c3-fuel/`
namespaces remain loose in their entirety. Their current verification, native
inspection and acquisition tools therefore retain their exact inputs. No game,
save reader, installed-content audit or Ghidra session was run to claim consumer
compatibility. The retain list has 1,017 members, including the three holds.

Only `.local-work/c2-prose-spacing/` enters the 37-file conditional allowlist.
It is the completed historical editorial correction package, already assigned
to cargo by Stage A. B5 explicitly retires its task-bound packager in favor of
`research/review_package.py`. Current references are historical locators and
inventories. The full restored package preserves before copies, failed/accepted
edit records, the independent review, seal and all scripts at their original
relative paths. Its scripts are retained as evidence and must not be executed.
Controlled extraction and fresh member hashing support historical inspection;
regeneration is neither needed nor claimed. No active cargo input is retired.

Schema 2 has one owner entry for cargo, and 37 governance cross-references to
that owner. All original paths across owners undergo the same case/Unicode/path
collision checks. There is no duplicated physical ownership or per-brief archive.
The earlier b01 archive/index are inactive failed-attempt diagnostics, never a
second authority. Other task-created restores and fixtures remain temporary review
material, not archive owners. Existing loose saves, protected backups, raw save
streams, installations, analysis projects and unrelated evidence are excluded
universally; their payloads were not read or their namespaces modified.

## Measured costs and recovery

Primary receipts are `build02.json`, `restore02.json`, `measurements02.json`,
`allocation02.json` and `audit02/audit.json` under
`.local-work/evidence-archive-stage-b/`. Initial measurement failures remain
separate. Decimal MB and GB are used here.

| Quantity | Observed value and meaning |
|---|---|
| Encoded archive | 4,658,286 bytes; 13.47% of admitted original logical bytes, including container/inventory overhead |
| Central index | 914,164 logical bytes |
| Archive creation / initial verification | 1.490 / 0.312 seconds |
| Full restoration with flushed writes and independent reread | 53.165 seconds |
| Whole successful pilot operation | 72.363 seconds |
| Original reported allocation | 35,930,416 bytes across 1,054 originals |
| Final archive + index reported allocation | 5,578,752 bytes |
| 37-file gross conditional retirement estimate | 747,224 bytes of file-reported allocation |
| Conditional persistent net recovery | **−4,831,528 bytes**, even before journals, other controls and retained temporary proof |
| Actual original files/bytes removed | **0 / 0** |
| Retained task file allocation at audit02 | 94,345,752 bytes; includes initial attempt, both restores, diagnostics and fixtures, deduplicating synthetic hardlinks |
| Temporary file-allocation peak bound at audit02 | 102,734,360 bytes including an 8 MiB transient-control allowance; directory/MFT allocation, later review exports and OS activity are separate |

NTFS `FileStandardInfo.AllocationSize` is measured, but resident small files may
report their logical length. These figures are file-allocation estimates, not a
guarantee that deletion frees equivalent clusters or MFT capacity. Exact physical
temporary peak and eventual physical recovery remain unmeasured. No real cleanup
occurred. Free-space changes include OS/other-process activity and are not treated
as causal recovery measurements. All large temporary artifacts remain retained
for review; only task-created, verified temporary objects may later be cleaned.

Both-drive guards precede disk-intensive phases and reserve worst-case writes.
Build reservation covers four times source bytes, 32,768 bytes per member and
32 MiB control margin. Restore separately reserves payload, member/directory
allowance and 32 MiB. This small pilot requires no C: staging.

| Boundary | C: caller-available bytes | D: caller-available bytes |
|---|---:|---:|
| Task baseline | 92,475,932,672 | 82,421,600,256 |
| Final build before / after | 92,488,671,232 / 92,488,671,232 | 82,368,573,440 / 82,362,994,688 |
| Final restore before / after | 92,488,671,232 / 92,481,835,008 | 82,362,994,688 / 82,324,291,584 |
| Audit02 after | 92,488,896,512 | 82,320,367,616 |

All remain above 40,000,000,000 bytes. These are dated receipts, never future
admission authority; the continuation must query both drives again.

For equal admitted original membership, audit02 reads/hashes 34,579,565 source
bytes through 1,051 payload hash calls in 2.234 seconds, with no enumeration.
Full archive verification hashes 914,164 index bytes and 4,658,286 archive bytes,
then reads the archive again to decode/hash 35,379,174 member bytes through
1,052 member hashes in 0.254 seconds, also without enumeration. These are API-level
reads and warm local elapsed times; device I/O, cache state and routine per-task
consumer workload are not controlled. Retirement intentionally repeats integrity
checks per file. **The future ≥80% routine-verification objective is NOT TESTED.**
No journal shortcut replaces scientific-input verification.

## Qualification, failures and durability limits

Final own qualification is `qualification-c28faf32e3a546d78b59015aa5d3c1ca/`:
51/51 PASS. Independent execution is
`qualification-62ae0c92c68b463189d1d282d18f5bb3/`: 51/51 PASS. Controls cover
full equivalence, empty files, interrupted creation/publication/restoration,
abrupt process exit without finally blocks, fresh retry, corrupt/missing/truncated
archives, external-root substitution, invalid schemas/manifests, nonmember
allowlists, malicious tar paths/links, case/Unicode aliases, Windows junctions,
hardlinks, alternate streams, source changes/missing inputs, disk failure, three
wrong historical versions and partial retirement/rollback. Real deletion remains
unexercised. The independent reviewer also checked byte preservation and decoding.

Preserved earlier failures include fsync on a read-only Windows handle, corrected
by flushing output handles before closing; a substitution fixture that initially
constructed an identical deterministic pair, corrected to alter its payload; and
the first real attempt's allocation scan entering its synthetic junction, corrected
by bounded measurement traversal. That initial archive, full restore and original
postflight passed; initial timings were lost before receipt persistence and remain
UNKNOWN. Exact executed versions are retained in `initial-methods/` and
`executed-b02/`. The final engine's cross-owner NFC correction is covered by final
qualification and actual archive verification; it does not change archive bytes.
The reviewer-discovered disappeared-source race now stops before completion and
has an explicit after-preflight regression control. A second reviewer finding
added reserved space for journal/temp writes above the bare 40 GB floor; its
near-threshold control proves failure before the first journal write or removal.
`audit03/` rechecks the real archive, source set and deterministic dry run with
the final engine, preserving audit02's earlier measured costs separately.

File data is fsynced, then Windows namespace publication requests write-through
on the same volume. PREPARED, VERIFIED, RESTORED-TESTED, AWAITING-APPROVAL,
RETIRING and COMPLETED distinguish progress; neither a journal nor rename alone
authenticates evidence. Interrupted outputs without an independently expected
index digest stay quarantined. Tests establish process-interruption behavior,
not actual power-loss survival, universal media integrity or multi-file atomicity.
Directory ancestry requires exclusive operator ownership. Hostile OS/kernel or
trust-root replacement is outside the guarantee. A single local copy can be lost
to drive failure or corruption; no off-device copy is required or claimed here.

## Later systems and backup planning

The nine provisionally accepted groups remain accounted for below, using
[Stage A's frozen totals](../evidence-archive-discovery/archive-options.csv).
They are future planning, not new migration or payload verification.

| System | Files | Logical bytes |
|---|---:|---:|
| Identity, location and lifecycle | 21,229 | 17,572,484,550 |
| Resources, production and power | 134,140 | 8,002,753,894 |
| Crew and robots | 1,399 | 2,188,017,257 |
| Shared native observation and methods | 40,353 | 1,756,696,474 |
| Governance, review and publication | 42,074 | 1,490,547,629 |
| Construction, limits and defense | 903 | 1,098,393,313 |
| Storage and local links | 1,540 | 705,057,626 |
| Shared corpus indexes/receipts, excluding saved payloads | 303 | 82,232,896 |
| Cargo transport and fuel | 1,054 | 34,598,790 |

The bounded workshop assessment reads Stage A metadata and checks current names
and lengths: 739 files / 12,312,513,157 bytes, zero metadata discrepancies. It does
not hash or reclassify their payloads. Recommend considering one separate workshop
identity/population archive, leaving lifecycle/location in the remaining identity
group and recording cross-references. That yields ten owners, below the hard
ceiling of 30. No split, extra archive or classification is activated now.

For subsequent separately briefed work, prioritize workshop inventory, then the
remaining identity/lifecycle pool and resources/production for storage relief.
Qualify shared native/corpus dependencies before dependent cutovers; treat active
resources/live work conservatively. Crew, construction and storage follow their
dependency assessments; governance/shared-method consolidation can reduce file
count after their consumers are ready. Cargo's remaining active roots need explicit
consumer adaptation before broader retirement. This order grants no deletion.

Complete non-save logical scope remains 32,930,782,429 bytes; essential scope is
32,892,968,157. Stage A's 2.87–14.66 GB encoded-plus-index scenarios remain
uncertain, purposive transfers rather than confidence intervals. This small pilot's
13.47% ratio cannot be extrapolated to the entire corpus. A 10 GB backup target
remains plausible but unproved for complete or essential evidence. No upload,
external copy, backup entitlement or publication clearance is implied.

## Frozen acceptance and review delivery

The evidence below supports the implementer's criterion matrix. Independent
ACCEPT is separately recorded against exact final source/prose/patch hashes in
the local delivery package; this table cannot issue its own acceptance.

| Criterion | Implementer result | Primary evidence and scope |
|---|---|---|
| AC1 | PASS | Baseline HEAD/index unchanged, exact 1,054-source postflight, no original/target/save/Git integration actions. |
| AC2 | PASS | Nine-group accounting, bounded workshop recommendation, one cargo owner plus 37 cross-references, ≤30 owners. |
| AC3 | PASS | Exact Stage A/hash reconciliation, historical pins retained, authenticated central index and all members, three held versions. |
| AC4 | PASS | Full real restoration and independent reread/decoder; active cargo namespaces retained and historical package accessible by extraction. |
| AC5 | PASS | Final own and independent 51-control runs, Windows handle retirement on disposable files, process-crash and fail-closed recovery; physical power-loss limits explicit. |
| AC6 | PASS | Exact 37-file manifest, 1,017 retains, deterministic dry run, separate approval gate, rollback/card; no cleanup completion claim. |
| AC7 | PASS | Actual compression, timings, allocation/free-space receipts and bounds, source provenance, retained failures and complete manual editorial pass. |
| AC8 | Independent disposition required | Exact reviewed snapshot, screen/manual record, verified complete/task-only patches and independent closure disposition are retained locally. |

Scientific outcome is preserved historical evidence, with no stronger cargo or
save claim. Engineering outcome is qualified bounded packaging/recovery and a
conditional cleanup proposal. Target survival is not applicable: no game or native
analysis process was operated. Storage migration remains unfinished. Publication,
integration and real retirement remain distinct permissions. The earlier
preservation-optimization AC4 remains FAIL / REWORK.

Baseline HEAD is `87a5832a9ee62008e8574f7c4c9f65ff7a855971`; index SHA-256 is
`83375252488646e00e3a70fb123507e04780b34f2f387e0d6f4c6fc7c69720fa`.
Only the supplied Stage B brief was initially untracked. It remains unchanged
and is included separately in the complete patch. Task changes comprise the four
methods and their README, this report/card, and navigation/source/credit updates.
All raw evidence, manifests, fixtures, archives and restores remain excluded.
No staging, commit, push, contact or new third-party permission basis was used.

The final local source ledger is `audit03/sources.json`; it pins the owned Stage A
decoder, current review exporter, policies, invoked brief, methods and primary
receipts. Reuse is under SOR-P-0002, with CPython 3.14.3 stdlib Zstandard and
Windows APIs as existing execution tools. Review receipts, screen/manual coverage,
exclusions, exact status, source hashes and final diff hashes are bound by the
detached delivery record. Their local-only status prevents recursive changes to
the reviewed authored snapshot. Reviewer acceptance grants no integration or
retirement authority.
