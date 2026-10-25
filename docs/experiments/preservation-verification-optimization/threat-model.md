# Protection ledger and trust boundaries

[Baseline](baseline.md) distinguishes actual historical coverage from the
prospective duties below. The prototype is disposable-only. This ledger does
not amend [save protection](../../SAVE_PROTECTION.md).

| Class / operation | Required detection | Full prototype | Conditional journal prototype |
|---|---|---|---|
| Actual scientific input, including ignored/untracked raw input | Fresh SHA-256 at intake and applicable reuse, independent expected identity | Two fresh hash passes | Same two fresh passes |
| Designated/manual/quick original and independently verified backup | Names, identity, hashes, backup readiness and protected namespace | Simulated with paired stand-ins | Same stand-ins; never skipped |
| Installed EXE/ESM and native evidence used by task | Exact selected identity, not an old PASS | Critical hashes; native inputs belong in scientific manifest | Same |
| Historical byte edit or same-size/timestamp-preserving substitution | Detect changed readable bytes; timestamp equality is insufficient | Full hashes plus file identities | Detects journaled write; no byte oracle without an event |
| Deletion, rename, replacement or inserted path | Detect namespace/identity change | Enumeration and file IDs | Watches original file IDs and parent directory IDs; any matching event refuses admission |
| Manifest edits, corruption or maliciously changed expected hash | Reject against independently supplied digest | Exact manifest-byte hash | Same |
| Wrong baseline/root or journal checkpoint | Reject stale/mismatched identity | Root/path/volume identity; externally bound digest | Same plus journal ID and continuity bounds |
| I/O denial, malformed archive, scanner interruption | Explicit failure; no PASS or automatic baseline refresh | Exceptions propagate | Same; journal errors cannot become “no changes” |
| Benign task outputs and ordinary authorized Git edits | Allow only outside frozen protected roots; preserve HEAD/index | Demonstrated on fixtures and actual task output context | Same; no project wrapper is installed |
| Changes to HEAD/index or controlling policies | Task-specific authority check | Assignment wrapper rechecks exact original HEAD/index; policies are not edited | No conditional deployment wrapper exists |

The baseline is an in-memory SQLite database serialized to a new file. Each
verification loads and hashes those exact bytes before deserializing them; a
digest supplied by the caller is the trust anchor. Reading the same manifest
file to discover its own expected digest would defeat that boundary. The
fixture's anchor is retained outside the protected fixture tree in a task
receipt. That is separation for a test, **not** an externally immutable root.

NTFS volume serial and file reference numbers are filesystem identities, not
cryptographic identities. The journal design requires the same trustworthy OS,
volume, identity mapping, unprivileged record visibility and continuous journal
range since the frozen baseline. It refuses reset/gap/unsupported/corrupt records
and historical activity, rather than guessing that a timestamp-only change is
benign. Hardlink alias writes are included in actual qualification. Reparse roots,
ancestors and baseline-enumerated nodes are rejected. An external attacker able
to alter both the data and supplied anchor, kernel, reader or journal is outside
the demonstrated trust model.

The journal gate runs before and after fresh scientific/critical reads. It
checks the recorded historical file and directory IDs with indexed queries;
there is no repeated historical pin-table traversal. Namespace mutations and
matching hardlinked file IDs invalidate admission. The manifest load/hash cost
remains visible as control bytes. An inaccessible journal fails closed; callers
may explicitly perform a full verification without changing baseline bytes.

Neither mode is an atomic filesystem snapshot. A full scan can miss a write
after its final read of the affected file. That general finite-window limit is
reasoning, not a measured miss in the final suite. The supplementary concurrent
write control demonstrates the repaired global post-pass and the journal's final
gate: both detect the tested write during scientific-input hashing. A later
write after the last read or journal checkpoint remains outside the observation
interval. Immutable
snapshot acquisition or an enforced exclusive writer boundary is a separate
unimplemented requirement for a stronger transactional claim.

## The material unresolved distinction

The full scanner checks bytes returned by its read path; it does not prove that
cached bytes equal physical media or that either describes true game semantics.
The conditional scanner checks filesystem activity and selected input bytes.
Changed historical bytes returned by a later read, without a qualifying journal
event, can pass its activity gate. This is a concrete missing observation, not
an accusation that such corruption occurred in the research archive.

The modeled counterexample suppresses real mutation events to represent that
observation gap; it is not a real below-filesystem corruption experiment. Raw
volume writes were neither needed nor authorized. A Merkle root or signature
authenticates expected content but cannot establish that unread local payloads
still match it. Read-only attributes or ACLs restrict some writes; they do not
supply current-byte equality against storage faults or administrators.

No prototype PASS can replace fresh scientific-input hashes, silently exempt
ignored evidence, or weaken high-risk save/content protection. Full historical
re-audit triggers are proposed separately for migration, suspected corruption,
changed trust roots, incidents and release gates. Until an approved replacement
defines an acceptable guarantee, the current policies continue unchanged.
