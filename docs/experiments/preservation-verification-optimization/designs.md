# Designs examined and selection

[Threat model](threat-model.md), [measured report](report.md). All alternatives
are prospective. No archive, ACL, snapshot or external store was installed over
existing research data.

| Architecture | Integrity and trust | Routine cost | Main failure / migration issue | Decision |
|---|---|---|---|---|
| A: Fresh task/critical manifests plus NTFS change journal and indexed historical IDs | Exact selected-byte hashes; trusted OS, anchored manifest and continuous visible journal | Small manifest hash, changed-record queries, selected inputs; no historical payload reread when quiet | Cannot attest unread historical bytes without a filesystem event; gap/reset forces full fallback; snapshot races need explicit scope | Implemented as conditional disposable prototype; no AC4 PASS |
| B: Immutable evidence store with authenticated Merkle index and selected leaf proofs | Trusted immutable store/version plus out-of-tree authentic root; selected leaf hashes/proofs | Root/proof validation and selected leaves; namespace identity bound to version | Ordinary mutable local files do not become immutable because their expected hashes are in a Merkle tree. Storage corruption and malicious roots require independent controls | Viable with a real storage trust boundary, not established here; proposal only |
| C: Single-pass union verification and a full post pass | Fresh current-readable-byte comparison, original expected hashes, explicit namespace checks | Two whole-payload passes rather than redundant inherited rehash plus union and post | Unique historical files still all read; namespace duties can add enumeration | Implemented full-byte fallback; measured 33.33% byte saving, below threshold |

These are different mechanisms: A trusts a change history to avoid rereads;
B changes the authoritative storage/version boundary; C retains whole-corpus
byte observation while removing redundant work. An ordinary size/mtime cache is
not a viable fourth design: the timestamp-preserving same-size mutation test
contradicts that proposed guarantee.

## What the prototype actually implements

The small stdlib implementation stores path/hash/size/file-reference/category
records in an indexed SQLite manifest. It reads that manifest into memory,
checks its externally supplied SHA-256, and deserializes those exact bytes.
Historical activity checks query file and parent IDs from USN records rather
than walking the entire table. Full mode enumerates namespaces and verifies
every leaf and file identity twice. Only `baseline()` writes a new manifest;
neither verification mode repairs data, refreshes expected hashes or advances
a checkpoint.

Windows SDK interface facts and Microsoft documentation informed the original
ctypes adapter; no SDK implementation or third-party snippet was copied. The
actual usable interface here is a root-directory handle with
`FSCTL_READ_UNPRIVILEGED_USN_JOURNAL`. Privileged volume reads failed and were
not escalated. Version-2 records are supported; unsupported record versions fail
closed. The entire drive's visible journal metadata may be read, so raw
diagnostics stay local. The timing charges this control-plane work.

## Why the promising alternatives do not yet meet AC4

A removes repeated payload reads in the tested quiet case and detects all the
tested ordinary filesystem mutations. It fails the stronger changed-readable-byte
duty without an event. B can offer stable logical version identity, but a root
hash alone does not make the current mutable corpus match it. ACL/read-only
controls reduce accidental mutation; a copied baseline, Git object name, signed
manifest or cached prior PASS cannot independently prove unread ignored bytes.
Trusted Git object identity is useful for authored tracked inputs read from the
object itself, but does not cover ignored raw files, mutable worktree bytes or
object-store corruption without reading/verifying those objects.

Filesystem snapshots preserve a coherent logical view and could address races;
they would still need a verified storage-integrity model and a separately approved
migration over original evidence. None exists in this assignment. No installation,
hardware assumption, compression/repacking or historical-evidence rewrite was
used to manufacture an efficiency result. C addresses the concrete redundant
pass without making new storage assumptions, but its unique-file saving is zero
and it is insufficient for the frozen 80% target.

The tested routes therefore support a narrow negative engineering result, not
universal infeasibility. A maintainer-approved storage guarantee or explicit
decision about delayed historical corruption detection could make a future
version of A or B useful. Such a decision would amend the contract rather than
turn the present AC4 into PASS. The inactive policy diff makes that choice
reviewable without activating it.
