# Cargo exact retirement transaction

Use installed CPython 3.14 on Windows NTFS from the repository root. Existing
project-owned Stage A/B and access components supply the decoder, archive/index
authentication, path checks, Windows handles and both-drive space guard. No
package installation, target process or network access is needed.

| Method | Reads | Writes and effects |
|---|---|---|
| `executor.py` | Externally pinned proposal, recovery, shadow and separate approval; exact Cargo sources, archive and index | Exact approved file disposition only in explicit `execute`; durable journal and Cargo baseline in a named transaction folder. No recursive deletion or implicit activation. |
| `qualify_executor.py` | Own generated synthetic files and archives; current code/tool identities | Fresh disposable synthetic fixtures, negative cases, journals and receipts. Deletes only its synthetic allowlist payloads. |
| `replica_executor.py` | Accepted real Cargo archive/index and 1,054 originals, maintained SWF/PEX readers | Fresh archival replicas and restored loose replicas, replica-only retirement, consumer outputs and audit receipts. Removes the authenticated consumer lease after replay. |

Run `python -B research/evidence-access/qualify_executor.py` for focused faults,
then `python -B research/evidence-access/replica_executor.py` for the full replica.
Both preserve earlier runs. Failed and interrupted outputs remain quarantined;
unknown file types are never recursively removed. Real originals and the real
baseline are outside these tests' write scope.

The existing preparer supplies a read-only real preflight. The executor's CLI
requires exact proposal/recovery/shadow paths and hashes, the source root and a
fresh transaction folder under `.local-work/cargo-retirement/`. Explicit execution
also requires a separately authorized approval path/hash. Neither a dry run nor
an ACCEPT record creates that approval. See the
[qualification report](../../docs/experiments/cargo-evidence-cutover/executor.md)
and [future card](../../docs/experiments/cargo-evidence-cutover/execution-card.md).

Provenance: project-owned resolver/preparer and Stage A/B are reused under
SOR-P-0002. Exact versions are recorded in local source ledgers and executed
method snapshots. No outside implementation or new permission basis is used.
Bethesda-derived archive/restore bytes stay local-only and untracked. Authored
code and reports remain REVIEW-REQUIRED; publication is not cleared.
