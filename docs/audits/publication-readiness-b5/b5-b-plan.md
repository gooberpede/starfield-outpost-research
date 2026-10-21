# B5-B proposal: exact approval and preservation before cleanup

**DEFERRED UNTIL AFTER RELEASE; NOT AUTHORIZED.** B5-A deletes or moves no pre-existing artifact;
limited current-source repairs are authorized, and original evidence is never
overwritten. New synthetic workspaces clean only their own allocated fixtures.
The [original brief](../../implementation-briefs/CODEX_BRIEF_SOR_B5_A_local_work_inventory_scratch_lifecycle.md)
requires a new explicit maintainer decision for B5-B, even after independent
ACCEPT. Publication remains NOT CLEARED.

The historical detailed proposal remains local-only at
`.local-work/b5/deletion-candidates.json`; its hash and availability boundary are
recorded in the [tracked summary](report.md). B5-B is deferred until after release.
A future action needs a freshly reviewed manifest and explicit approved IDs; the
old working file is not a current execution list. Release supplies no deletion
authority. No prefix, age, extension or ignored-status
selection is permitted. HOLD entries cannot be included without resolving the
recorded reason and affected review, or explicit approval of a documented
reference exception. A proposed candidate is never implicit deletion authority.

1. Freeze approved IDs, actions, exact paths, tree membership and manifest hash.
   Recheck HEAD/index and before hashes of originals, B3 historical locators,
   B4-F1 core/addendum and their constituents. Preserve all original captures,
   WALs, failed runs, screenshots/saves, source/configuration versions and
   significant analysis state. Leave all four designated roots intact.
2. Query caller-available free space on **both C: and D:**; fail closed below
   40,000,000,000 bytes on either, or on query failure. Reserve space for any
   separately approved recovery copy and receipts. Logical candidate lengths
   do not predict volume-free deltas, NTFS allocation, compression or hardlinks.
3. Resolve each literal target again. Inspect target, every ancestor up to the
   approved owning root, and every enumerated descendant with `lstat`/Windows
   attributes. Reject links, junctions, reparse points, ADS, traversal, changed
   owner boundaries or a resolved path outside the approved root. A C: Temp
   entry is bounded to its one enumerated tree, never the Temp parent. Neither
   installed tools/game nor `D:/ReverseEngineering` is eligible.
4. Re-enumerate the complete file/directory set. Compare path, kind, size,
   SHA-256, file ID/device, timestamps and link count with the manifest; reject
   additions, changed bytes/identities or inaccessible paths. Re-hash every
   retained duplicate independently and confirm it is outside the deletion set.
   No candidate may be another candidate's only recovery source. Empty trees
   need a fresh recursive zero-file check; do not infer emptiness from age.
5. Re-run reference closure against current tracked documents/code and relevant
   local receipts/helpers. Historical provenance may remain with an explicit
   retirement/recovery wrapper, but operational prerequisites and reader links
   must resolve. Any new ambiguous consumer, unique/protected descendant,
   invalid reconstruction direction or changed protection pin stops that ID.
6. Persist and flush before receipts **outside** every target, including approved
   identity lists, retained duplicate bytes/hashes, protected state and actual
   free space. Agree recoverability/backup before destruction; B5-A makes no
   new recovery archive and offers no undelete guarantee. A duplicate can be
   copied back from the retained verified copy under later recovery authority;
   historical filesystem timestamps/IDs would not be restored by that alone.
7. Execute only specifically approved literal paths using native PowerShell
   `-LiteralPath` or a separately reviewed single-runtime equivalent. Do not
   enumerate in one shell then interpolate another deletion command. No broad
   globs, `git clean`, tree pruning, Git GC, staging, index/ref edits, network or
   external upload. Preserve the four roots even if their contents change.
8. Flush per-ID action/result logs. Recheck protected hashes, HEAD/index, retained
   recovery copies, reference availability, exact removed/remaining paths and
   free space. Report successful file bytes and observed volume deltas separately;
   report partial failures honestly. Stop on unexpected corruption and retain
   evidence; do not overwrite an original from a backup to hide a failure.

B5-B must define its own bounded execution and recovery authority and provide
before/after preservation receipts. No cleanup implementation is supplied here.
The ten historical Git temporary objects remain outside this filesystem proposal
and need a separate repository-maintenance decision.
