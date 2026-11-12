# Intake and proposed exposure

The ordinary public-ref proposal is `refs/heads/main` at
`e29b7507def041e25884e87222deea32b30d964d`. That commit is D5BZ's sealed
delivery. The previous tip, D5BY `d5ab299a5103b6d8d9f00c536f7cef455648cddb`,
has tree `1d0fa968c4e606fda7b3ba33636dda3d0f66c6b5` and 4,141 paths.
D5CA checked 3,615 tracked paths in tree
`f75eca587b5ce2efe46c50aeabcbdb332897f619`. The index has 3,615 entries and
matches HEAD in the staged diff. The supplied D5CA brief was the sole
untracked path at intake. [Machine inventory](tree-and-refs.json)

The candidate has 9,478 reachable objects: 252 commits, 2,298 trees and
6,928 blobs. The current tree uses 3,565 distinct blobs. The local ref union
adds 45 objects outside the proposal, and the local reflog walk adds zero
to that union. The local object-store census found another 892 object IDs
outside those sets. Eight temporary object-store files reported by Git are
housekeeping and sit outside the census. The local ref inventory includes
`main`, its remote-tracking copy, the remote-tracking symbolic HEAD and
Codex checkpoint tree refs. No local tag or stash ref was enumerated.
The fetch refspec covers remote branches and the repository is non-shallow.
Object set membership is independent of working-tree status.

The GitHub connector confirmed private visibility, default branch `main`
and the same hosted tip. Branch pagination returned no other branch. Sandboxed HTTPS failed.
The authorized authenticated retry advertised only symbolic HEAD and
`refs/heads/main`. The GitHub API returned HTTP 200, zero items and no
next page for releases, tags and pull requests in all states. The API
release inventory therefore lists no associated assets. Provider-internal
refs, cached objects and arbitrary issue/comment attachments fall outside
these account-visible endpoints. Refresh the inventories at exact freeze.

## Archive and tree census

Each archive root at HEAD contains three loose files: README, index and
ZIP. Both containers, the READMEs and indexes match D5BZ's external manifest.
Both indexes match the actual case-sensitive member inventories, file sizes
and digests. Independent in-memory ZIP reads and the tracked verifier's
disposable extraction covered all 594 members. The audits ZIP has 291
`ARCHIVE_SOURCE` and 44 `ACTIVE_RELOCATED_COPY` entries. The briefs ZIP has
259 `ARCHIVE_SOURCE` entries. The governing D5BZ brief and six pre-seal audit
records resolve through the indexes. Of 594 rows, 587 name a prior Git blob
and all 587 match the old tree path. Ten of their archived worktree payloads
have documented line-ending-only differences from the Git blob. The
supplied D5BZ brief and six pre-seal records have no prior Git blob.
The external post-seal attestation
binds the container manifest without inserting itself into either ZIP.
[Archive verification](../archive-verification.md)

The largest reachable blob is the historical D5AX text reference
inventory, 13,111,795 bytes. The largest other examples are D5AT
supplemental masks at 5,133,227 bytes and the audits ZIP at 3,875,869 bytes.
The inventories retain the archive/loose distinction. A member stored in a
ZIP can disclose the same material as a historical loose blob.

All 44 active relocation rows agree across the archive index, relocation
map, verification CSV and pinned current-source edition. Thirty-two keep
the original byte identity. The other twelve have the current hashes
recorded in the crosswalk. The old loose paths are absent at HEAD.

## Machine inventory semantics

`tree-and-refs.json` records exact tree entries, local ref targets and
overlap counts. A historical object path is Git's representative locator.
Use the OID for identity and `git log --find-object=<oid> main` for
introductions and removals. Excluded object records carry reachability
class without an exposure finding. `exposure-inventory.csv` records one
row per unique candidate blob, each commit metadata record and each
sealed ZIP member, with SHA-256 and screening counts. A current blob
may also be present in history. The path count and unique blob count
measure different things.
