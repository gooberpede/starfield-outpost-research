# Workshop projection v2

`sor-d5bx-workshop/2` is derived evidence from the three D5BW-pinned Workshop
contexts. The [crosswalk](crosswalk.json) specifies source selectors and domain
rules. The exact canonical ledger is an independent ZIP member. The
[builder](../../../save-analysis/scripts/build_d5bx_workshop.py) verifies the
original baseline and typed `source` objects agree before retaining only size
and SHA-256. Both raw originals and their custody metadata remain private.

## Selection and ordering

Keep every historical constructed root, member role and ordinary owner in
source order. Select the union of their root, member, role and owner identities.
Add unresolved baseline identities when the linked prefix reports `NOT_DECODED`,
the identity occurs as a group in the exact ledger, or a retained DA record
names any ledger group in its resolved identities. Keep every matching row in
both baseline arrays, including repeated identities if present. This preserves
the supplement's identity-multiplicity check. Replaying the baseline roles also
checks the foundation and replacement references that must be present to
reproduce the selected 657 roots. Retain matching typed records in source order,
after testing full typed identity uniqueness before reduction. Also retain the
typed frame for each canonical group that has a reference-family record and for
each of the 115 canonical DA source records. For the latter, keep the exact
typed case, base, end and extra operands when the fourth DA identity names one
of the 31 ledger groups and the saved 4C entries contain no WorkshopItem key.
Rejoin the raw counted extras in F040 and compare all 31 counts and recorded
group presence in R3. The ship mapping and both Hab assemblies remain outside
the ordinary root set. Root/member tuples use decoded logical-stream offsets,
native type-registry values and
separate per-record buffer overrides. Source saved tokens, resolved FormIDs and
definition file offsets remain distinct fields.

Keep all 2,643 ordered ALLA pairs from the historical census with plugin,
original ESM record offset, quest FormID, alias ID, raw keyword word, resolved
keyword and target alias ID. Exclude names, stat metadata, the original coverage
sentence and the private source context locator. Keep the per-plugin coverage
counts for all QUST variants, ordered alias blocks and all their ALLA pairs.
Recompute keyword multiplicity from the retained pairs. The reader walks QUST
records in the pinned main ESM, tracks alias boundaries and compares every main
ESM pair including duplicate multiplicity. The other 37 installed ESM inputs
remain an inherited historical coverage premise. The reader also excludes the
three exact main-namespace object IDs in the raw low 24 bits across all projected
pairs. Absence of the three keys applies to the pinned 38-ESM census and its
observed aliases. Arbitrary mod sets
and loaded defaults remain outside the claim.

## Encoding and safe access

The archive contains `manifest.json`, `workshop.json`, then
`canonical-candidates01.json`. The first two are ASCII-compatible UTF-8 JSON,
sorted object keys, compact separators and one final LF. Arrays retain source
order. The ledger retains its original 9,469 bytes. ZIP metadata uses DOS epoch
1980-01-01, regular Unix `0644` file mode, no comments or extra fields, and
DEFLATE level 9 under CPython 3.14.3 with zlib 1.3.1.zlib-ng. Two builds on
that runtime produced identical archive bytes. The external index pins the
container and every member, including the internal manifest. The internal
manifest pins the historical sources and its two data members.

Use the [reader](../../../save-analysis/scripts/verify_d5bx_workshop.py) to
check the exact outer length and SHA-256 before opening the archive. It
compares ordered member names, regular file metadata, bounded exact sizes and
hashes. It reads those bytes in memory without filesystem extraction. A
custodian needing a loose copy can copy a validated member to an exclusive
caller-chosen filename after verification and confirm its hash again. Every
archive-supplied path is treated as data. Unknown, duplicate, traversal and
non-regular members refuse.
