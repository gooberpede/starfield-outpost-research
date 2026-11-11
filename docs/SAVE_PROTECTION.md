# Prospective save protection

2026-10-23, Australia/Sydney. Authorized by the
[C2B transient-save amendment](implementation-briefs/README.md#archive-lookup) (`implementation-briefs.zip :: docs/implementation-briefs/CODEX_AMENDMENT_SOR_C2B_transient_save_protection.md`).
This policy changes prospective operational gates. It does not authorize a live
run, game save creation/modification/restoration, or changes to historical evidence.

| Class | Treatment |
|---|---|
| Protected designated research and manual saves | Verify exact protected names/identities, byte lengths, hashes, independently verified backups and restoration readiness. Quicksaves are protected too; they are not automatically excluded. |
| Reliably identified transient exitsaves/autosaves | Exclude active files from preservation/equality/absence/addition gates. Creation, replacement, rotation or removal is diagnostic information, never a reason to restore a transient or refuse an otherwise valid admission. |
| Ambiguous or unclassified saves | Fail closed until qualified or explicitly classified/designated by the maintainer. A suggestive substring or a partially matching filename cannot justify exclusion. |
| Steam `remotecache.vdf` | Diagnostic synchronization metadata, not a protected scientific input. Record its observed hash or read/absence diagnostic without requiring identity at preflight, admission or postflight. Ordinary metadata changes do not block experiments. |

An explicit research designation takes precedence over nominal kind. A later
designation of an exitsave/autosave protects it prospectively, with exact pins
and an independently verified backup before admission. Missing backup readiness
still fails. The policy must not silently discard or reclassify historical
research evidence because its original basename resembles a transient save.

## Qualified naming model and explicit designations

The C2B implementation uses the complete native-generated filename grammar for
retail 1.16.244.0, not the older save-menu utility's prefix-only inference.
The existing native export `exp0002a-ui-thread-functions.tsv`, function
`FUN_14184eec0` (preferred static VA `0x14184eec0`, image base `0x140000000`),
selects Save/Autosave/Quicksave/Exitsave and formats the complete suffix. Quick
and Exit slots are zero. Profile hex, flags, encoded character name, elapsed
day/hour/minute digits, UTC timestamp, numeric fields and final format marker
are validated together. Unsupported or malformed names remain unclassified.
This is a bounded native naming model, not a decoded save-header kind field or
proof that arbitrary renamed files were produced by that route.

[The tracked policy](../research/resource-carinae-source-context/save_policy.json)
records exact names, byte lengths, SHA-256 and designation evidence. Save52 is
the primary input. The maintainer additionally answered **“Designate it as
protected (Recommended)”** for nonstandard `funclist.sfs` in this amendment's
chat. It is protected regardless of its unknown nominal kind; neither its
original bytes nor backup has been altered. Classification provenance and the
actual instruction are retained in the amendment review package.

## Namespace and evidence boundaries

Only active Documents/Saves and the known Steam remote save namespace receive
transient treatment. Historical archives, independent backup records, frozen
predictions, native evidence and raw captures remain strictly pinned, including
archived copies with transient basenames. The original broad manifest is read
through this prospective policy; its bytes, hashes and historical discrepancies
are never rewritten. Newly appearing protected or unclassified active saves are
detected by namespace enumeration; equal total file counts prove nothing.

Preflight, lightweight launch admission and postflight use the same policy.
Preflight binds its canonical policy hash and complete classifications in the
receipt. Launch/postflight refuse a policy change or an older receipt schema.
Protected full hashes are checked before launch and after exit; launch admission
uses the existing lightweight names/sizes checks. No full save scan is added
during gameplay. Reparse/root/ancestor guards remain strict.

Steam remote saves use the same classification. Steam Cloud state confirmation,
remote namespace identity, protected remote save content and other explicitly
protected inputs remain strict independent checks. `remotecache.vdf` is excluded
from preservation/equality gates; its absence or an ordinary read race is also
diagnostic. This exclusion does not cover remote saves, independently verified
backups, installed binaries/definitions, configuration or other protected inputs.
Transient file diagnostics are not compared as a whole sync snapshot.

Prospective amendment, 2026-10-28, Australia/Sydney: the maintainer requested this
classification for the accepted D5L implementation and proposed Phase B card.
[Amendment and verification](experiments/resource-retained-population/cloud-metadata-amendment.md)
record the exact scope. Historical `remotecache.vdf` discrepancies, original
receipts and failed old-gate verdicts remain unchanged. No exact metadata-hash
exception is required prospectively. A legacy helper which still gates on that
hash needs amendment/review before reuse; this policy does not rerun it or grant
live authority.

The earlier C2B missing-old/present-new exitsave discrepancy is preserved as an
accurate historical observation and failed old-gate result. Under this policy
it is ordinary transient rotation and needs no corpus-disposition permission,
supplemental transient backup or restoration. Any unrelated protected change
still blocks admission even when transient churn occurs simultaneously.
