# NOT AUTHORIZED: proposed system cutover and cleanup

This is an approval-ready design, not execution authority. The only current
decision requested is approval/amendment of archive boundaries and retention.
The [save-file amendment](scope-amendment.md) holds saves and raw representations
separately. No cloud upload, policy amendment or real deletion follows from Stage A.

## First candidate system

Propose the complete **cargo transport/fuel** system, covering C1/C2/C3 rather
than one archive per brief. Local `cargo-pilot-scoped04.json` names all 1,054
candidate files, 34,598,790 bytes, original relative paths, fresh hashes, roles
and provenance. Two Stage A passes agree; 510 current identities match earlier
source-ledger expectations. Missing older identities remain UNKNOWN.

Three packager paths under `c2-transit`, `c2-transport` and `c3-fuel` carry
historical method-version holds. Their current hashes match B5's later creator
inventory, while earlier execution ledgers name different bytes. The B5/scratch
lifecycle documents explain prospective exporter repair/retirement; they do not
turn old/new hashes into the same source version. Preserve every expectation.
Resolve original executed-method availability or retain those three paths loose;
do not delete them under a blanket cargo cleanup. No source is repaired here.

## Future batch contract

1. **Approve exact scope and recovery terms.** Choose the system boundary,
   canonical membership/index version, retention/loose holds and exact candidate
   original hashes. Reconcile unknown and conflicting provenance. Inspect rights
   and private paths for the intended destination. Freeze a separate Stage B brief
   with permitted writes, source protection, recovery, STOP and cleanup conditions.
2. **Preflight.** Verify original HEAD/index, relevant scientific inputs and
   protected content under current rules. Keep active saves, installed files and
   analysis databases outside this batch. Require a quiescent/controlled writer
   boundary; compare full expected names/hashes before packaging. Query both
   free-space guards and reserve the next phase's worst permitted writes.
3. **Create a new partial archive and candidate index transaction.** Stream exact
   original relative paths losslessly; hash every source while encoding. Record
   member/source equality, sizes, roles, ownership, original paths and version.
   Do not alter an old archive/index or normalize evidence. No per-experiment
   sidecars or duplicate cross-system payloads.
4. **Authenticate and qualify.** Hash complete archive bytes and stream every
   member against expected original hashes. Use a separately initiated reviewer
   to compare membership/identity and inspect primary logs. Flush archive/index
   data with a qualified durability protocol, including partial/archive-final/
   index-unregistered crash recovery. The Stage A prototype alone does not supply
   that power-loss guarantee.
5. **Restore to a fresh disposable tree.** Match every member to its original
   bytes, lengths and paths; independently reread outputs. Test corruption,
   interrupted/failed restore and source-version lookup. Keep originals throughout.
   Test required real consumers through an explicit adapter or controlled
   extraction. A literal absolute-path reader must not be assumed archive-aware.
6. **Make the backup/risk decision.** No off-device copy is confirmed. Decide exact
   recoverability, independent verification, replica placement and device-failure
   exposure. Two local replicas are an option, not off-device protection or proof
   of physical independence. No upload or connection is automatic. If existing
   protection requirements cannot be met, stop before source deletion.
7. **Present a separate deletion approval.** Supply the independently reviewed
   exact original path/hash allowlist, exclusions, archived owner/member/version,
   successful restore and consumer receipts, backup/risk disposition, expected
   reclaimed bytes/file count and rollback commands. Ask for authorization for
   that exact batch only. Boundary approval is not deletion approval.
8. **Approved future cleanup is mandatory for success.** After that separate
   approval and final equality/admission check, remove only the exact eligible
   loose copies. Keep held/unknown/version-sensitive files. Record each successful
   removal and actual before/after free space/file count; distinguish logical,
   allocation estimate and actual reclaimed storage. Keeping every loose source
   indefinitely does not complete a migration batch.
9. **Postflight and rollback.** Reverify archive/index roots, selected scientific
   members, protected inputs and namespace exclusions. Test reads through final
   locators. On failure halt the batch; do not broaden deletion, refresh expected
   hashes or overwrite a surviving original. Restore approved missing paths only
   from independently verified archive/replica into controlled locations, then
   verify exact bytes and consumers. Record incidents and preserve partial evidence.

## Space scheduling and verification acceptance

Use phase-aware admission. Before creation, reserve a conservative encoded-output
bound plus member/index/journal overhead. Once the actual verified archive size
is known, reserve restoration bytes and any exact-size replica copy separately.
The largest system may not fit a simultaneous worst-case all-phases reservation;
that does not authorize deleting originals to make room. If a later phase cannot
fit above either guard, stop with sources intact and obtain an approved storage
or genuine research-boundary change. A source-safe failed attempt is not cutover.

Explicitly authorize the lifecycle of newly generated test restores/partial
outputs in the future brief; do not treat that as permission to clean genuine
evidence. The cargo pilot is small enough to expose this process without first
requiring a multi-gigabyte cutover.

Freeze a future comparable loose/archived baseline before claiming the eventual
80% reduction. Measure namespace enumeration, unique opens, actual payload/archive/
index hash bytes and invocations, wall time, setup/migration amortization, backup,
restoration and repeated operations. Preserve fresh actual-input identity checks
and high-risk controls. Initial authenticated member-to-original comparison is
mandatory; a previous archive PASS or journal quietness never substitutes for it.

Stage A leaves this plan **NOT AUTHORIZED**. No current script automatically
rewrites consumers, activates an archive workflow or deletes original evidence.
