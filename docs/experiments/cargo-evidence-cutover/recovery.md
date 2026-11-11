# Cargo recovery and proposed retirement decision card

**DELETION NOT AUTHORIZED. Policy activation is not authorized.**
Use the [report](report.md), [method instructions](../../../research/evidence-access/README.md)
and frozen [brief](../../implementation-briefs/README.md#archive-lookup) (`implementation-briefs.zip :: docs/implementation-briefs/CODEX_BRIEF_SOR_archived_evidence_resolution_cargo_cutover.md`).
The proposal covers 1,051 exact archived originals, not a directory wildcard.
Three unarchived `package.py` versions remain held unchanged.
The final conservative projection is 13,594,624 bytes of net file-data allocation
recovery after retained failed/repeated-audit artifacts, compared with 23,805,952
bytes for the steady-state archival proposal alone. Actual recovery is unmeasured.

## Decision identity

The proposed allowlist is local-only:
`.local-work/cargo-evidence-cutover/real04/deletion-allowlist.json`.
Its SHA-256 is
`b809a65f25560bec838873bfbb50c1e945a478a627129c24f837ec437b88e75d`.
Each row records original normalized path, SHA-256, length, file/device identity,
owner/member, index digest and dependency disposition. Independent review binds
these immutable bytes; a changed row needs a fresh decision and review.

The archive is
`.local-work/research-archives/cargo-transport-fuel-b02/cargo-transport-fuel.tar.zst`,
SHA-256 `ebda740f0092b93f1dc9f32120db365223f465a6d374ce8e98933e8041eb1da7`.
The central index is `.local-work/research-archives/index.json`, SHA-256
`5500892dbc247c642b83336ee619ca34d40fae8967ccfda95c5394e7ceff7e3b`.
Embedded `ARCHIVE-MEMBERS.json` has SHA-256
`f46605615abca2ff026f46aad6f51162a554c4383e89b79048899e4fb6e39a7a`.
The exact recovery receipt and its independent hash are in real04's
`recovery.json` and `measurements.json`. No Stage B 37-file manifest grants
authority for this replacement set.

## Read or restore now

1. Check both C: and D: caller-available free space against 40,000,000,000 bytes,
   plus the next phase's write reservation. Stop on a failed query or guard.
2. Run `access.py verify` from the repository root. Compare the printed external
   archive/index/inventory identities with this card. Stop on any mismatch.
3. Locate one exact original with `locate --member ORIGINAL`. A changed surviving
   loose file stops; it is not silently ignored in favor of the archive.
4. Restore selected members or one complete experiment with `restore` into a
   fresh named directory beneath `.local-work/cargo-evidence-cutover/`. Preserve
   the returned lease digest independently. Hashes are checked while streaming
   and after writing. Never overwrite a surviving original or destination.
5. For the qualified SWF/PEX readers, pass the explicit lease and fresh separate
   output directory. Compare operation-specific results. Other historical tools
   retain their prerequisites and require deliberate review before execution.
6. Retain the receipt, then clean the exact disposable lease using its external
   digest. On unknown files or interruption, quarantine and reconcile explicitly.

## Before any later retirement

Separate maintainer approval must identify this exact allowlist and the proposed
baseline version after independent acceptance and inspection of recovery costs.
This assignment supplies a dry-run preparer, not an activated deletion executor.
Any future executor must be independently qualified before real use. The older
Stage B executor must not be invoked on this new schema.

Require exclusive source/ancestor ownership; fresh archive/index/member and source
identity verification; qualified filesystem/allocation/free-space queries; exact
recovery-receipt authentication; unchanged allowlist and source bytes; no unsafe
paths, alternate streams, hardlinks or reparse targets. Refuse unsupported states.
Keep saves, raw save streams, installed content, databases, active scratch and all
paths outside the allowlist excluded. No original directories enter the allowlist.

A future write-ahead journal must bind the externally approved plan, baseline,
archive and recovery receipts. Flush PREPARED and each pending intent before the
corresponding exact locked-handle deletion; flush completion afterward. Recheck
space with a journal/control write reserve. Stop on disappeared sources or changed
identities. A pending intent without durable completion is ambiguous after a crash,
not proof of deletion. Reconcile every source/archive/journal row and obtain an
explicit recovery disposition before resuming; never infer permission from a log.
The preparer rejects all nonempty pending/completed or RETIRING/COMPLETED journals.

## Rollback and post-retirement recovery

Before retirement, authenticate `shadow-baseline.json` against the reviewed
delivery manifest, call `rollback` with its independently retained prior-baseline
digest, and verify all 1,054 loose sources against those original rows. The
demonstration returns identical rows without changing the current baseline.

After any approved retirement, the old baseline is not independently available
on disk. First deep-verify the archive/index, restore the missing exact members
into a fresh disposable lease and verify every byte. Reinstating original paths
or changing active preservation policy needs the incident's explicit authority;
never overwrite existing sources. If the archive is corrupt or unavailable,
quarantine it and use a separately authenticated authorized replica if one exists.
No second permanent replica or automatic repair is provided here. Actual target
survival is not applicable; no Starfield operation took place.
