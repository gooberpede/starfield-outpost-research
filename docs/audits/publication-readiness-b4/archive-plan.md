# Provisional supplementary evidence index and archive plan

2026-10-21. **PROPOSED / HOLD; no assets exist or have been uploaded.**
[Group/member ID inventory](archive-groups.csv), [file identities](file-dispositions.csv)
and [claim consequences](claim-evidence.md). Exact local source paths and original
member names are in ignored `.local-work/b4/proposed-members.csv`; they are not
promised checkout inputs. Group totals are exact uncompressed candidate bytes,
not estimated compressed lengths. Excluded/archival groups are not assets.

## Concrete packaging contract

Choose ZIP with DEFLATE level 9, stdlib zipfile in existing CPython 3.14.3,
zlib runtime 1.3.1.zlib-ng, using stored original `.sfs`/JPEG file bytes.
Compression is optional for roughly 2 MB controls; grouping supplies navigation,
not meaningful compression of already compressed saves. Prefer compression for
the 16.4 MB Save52 and 24.9 MB HIST-0255. There is no unsupported promise of a
compression ratio. JPEGs are also already compressed. No installed 7-Zip tool
execution or new dependency is needed by the proposed method.

Before copying, require individual privacy/rights and maintainer selection
decisions plus explicit local provisional packaging approval. R1 remains pending
for every shortlisted raw file, so there are **no approved-to-package candidates**.
Do not use the GPL grant, first-party provenance or the optional packaging clause
as an embedded-content redistribution grant. Keep a manifest instead; no archive
was constructed and no extraction check was applicable. There is no archive hash,
size or producing-tool invocation to report. Those fields say NOT BUILT.

For any later approved operation, use exclusive output under ignored
`.local-work/b4/`, check 40,000,000,000-byte caller-available reserve on C: and D:
before and between writes with sufficient archive/extraction allowance, and stop
the affected group on missing source, changed identity, permission or space.
Validate relative single-file member paths, collisions, traversal/ADS/device
names and no encryption/links. Use the exact original filename from the private
identity registry, never an invented HIST alias; resolve any unsafe/conflicting
name with the maintainer, never silently rename a save. Save bytes may not be
sanitized, redacted, rewritten, patched, resaved or replaced by a derivative.

Hash the archive, record actual length and actual producing tool/codec versions,
list **every member** with length/SHA-256 and claim/experiment/source identity.
Reopen with an independent extraction route and stream-compare every reconstructed
save/JPEG against its protected original. Record total lengths, full member-set
equality and pre/post source hashes. A CRC/test command alone is insufficient.
Keep failed receipts, originals and local outputs; no deletion follows here.
Do not claim independent codec validation merely by calling the same library twice.

L0/S4C are one byte identity; do not duplicate across groups. Mature diversity
snapshots and exit saves are excluded from the proposed minimum; the two Save26
byte identities stay distinct. Each manifest member has exactly one group.
No manual-network JSON, WAL/memory, decompressed saves, extracted map/art/script,
EXE/ESM/BA2, database, install INI/library, compiled observer or bulk native source
is included. Raw inputs remain outside Git and existing evidence labels persist.

## Future GitHub link route

The durable route is versioned repository → this evidence index → approved
GitHub Release asset. The following is a **future template, not an active URL**:

```text
https://github.com/OWNER/REPOSITORY/releases/download/RESEARCH_TAG/ASSET_NAME.zip
```

OWNER/REPOSITORY/tag/asset names await the exact release decision; game version
1.16.244.0 is not automatically the research tag. No Markdown download link to
a nonexistent object is fabricated. B6 verifies exact uploaded bytes, member
manifest, public access and versioned links under separate publication authority.
No unrelated file-hosting dependency or automatic uploader is introduced.
