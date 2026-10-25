# Prototype integrity, safety and qualification boundaries

[Methods](../../../research/evidence-archive-discovery/README.md),
[benchmark interpretation](benchmarks.md), [Stage B gate](stage-b-plan.md).

The authority boundary is marked disposable trees inside this task's ignored
workspace. Original inputs are read for authenticated replication only. Decoder,
index, archive and restore paths are guarded against reparse/root escape.
Restoration uses exclusive new files in a fresh partial tree and publishes the
new destination only after member hashes and an independent restored reread.
It never uses `extractall`, overwrites an existing destination, repairs an
original, or chooses a new expected digest after failure.

An independently supplied expected SHA-256 authenticates exact index bytes
before private in-memory SQLite deserialization. Archive hashes, member hashes,
sizes, grouping version, original locations and owner references are separate
fields. Corrupt/unknown schema, wrong index, missing owner and ambiguous locator
fail. Existing schema 0 benchmark indexes are read-only compatible; final schema
2 adds checked aliases. A co-replaced index/archive is rejected against the
original expected root even when its own new pair is internally self-consistent.
An attacker controlling the expected root, OS or reader is outside this guarantee;
there is no externally immutable/off-device trust root in Stage A.

Archive-byte verification establishes current readable encoded bytes against
authenticated expectations after initial source/member qualification. It is
different from decoding every member, and different again from fresh intake of
an actually used scientific member. Future routines must keep those dimensions
separate and freshly verify every actual scientific input. No NTFS journal path
is treated as equivalent to reading bytes.

Names reject absolute/drive/UNC forms, traversal, empty/dot components, backslash,
ADS/colon, Windows reserved device names, trailing dot/space, duplicate names,
case/Unicode aliases and file/ancestor collisions. Tar links, devices, FIFO,
sparse/global or unsupported metadata overrides are rejected. PAX accepts only
a bounded path record, preserving long canonical original relative paths.
Declared member lengths/counts and total expansion are tied to authenticated
expectations; ZIP metadata construction is bounded before member parsing.

One canonical payload can serve multiple authenticated original-path aliases
and consumer systems. Aliases require caller-verified byte identity, retain each
original location/provenance, and restore at that original relative path. The
synthetic alias test proves one stored payload and correct restored bytes;
it does not establish that any real evidence copies may be merged or deleted.

Final own archive qualification declares 58 outcomes, including actual corruption,
truncation, missing/extra/same-size substitution, malicious metadata, unsafe names,
links, reparse destination, external-index substitution, a genuinely self-consistent
co-substituted pair, interrupted packaging, write-failed restore, no-clobber,
space-guard failure, long paths, central resolution and 70,000-member streaming.
Windows console aliases and superscript device-name variants are rejected using
the installed Windows path API. Additional read-only admission controls refuse
metadata/benchmark/test entrypoints before work when reserved free space is absent.
Negative controls allow unchanged tar/ZIP. Failed packaging registers no success;
failed restore leaves no published destination. Failed partials are retained.
Empty members round-trip with an undefined compression ratio rather than a divide
by zero. Publication retries only Windows access/sharing refusal, at most five
attempts, never an existing destination; permanent refusal preserves the partial.
This addresses an observed disposable-directory publication denial without claiming
its unobserved cause or suppressing an underlying integrity failure.
Independent read-only controls and exact final disposition are in [review](review.md).

Software interruption is tested; power-loss durability is not. Rename plus SQL
commit without a qualified flush/fsync/recovery protocol is not a crash-durable
migration transaction. Unregistered final archives and partial trees must stay
quarantined on failure. Another process able to mutate the private output tree
concurrently is outside the exclusive-writer test assumption. No guarantee of an
atomic source snapshot, universal physical-media integrity or safe live operation
is claimed. Stage B must close those exact gaps before its cutover/deletion gate.
