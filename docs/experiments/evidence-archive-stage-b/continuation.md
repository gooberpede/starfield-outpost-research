# Conditional retirement card: exact 37-file cargo editorial package

**NOT AUTHORIZED.** This card proposes an operation only after separate explicit
maintainer approval of manifest SHA-256
`c80ac405e2f3af32fb715df6dc053865cc53756975fbae550e4a7ff40aed7eb7`.
The [pilot report](report.md) supplies measurements, exclusions and limitations.
No real retirement command was exercised in this assignment.

The proposal is 37 exact files under `.local-work/c2-prose-spacing/`, totaling
747,224 bytes of reported file allocation. Every source path, preexisting hash
and size is listed in `.local-work/evidence-archive-stage-b/deletion-manifest02.json`.
Its bytes are the approval identity; no wildcard or recursive deletion is permitted.
The remaining 1,017 candidate files stay loose, including all four active cargo
tool namespaces and the three historical packager holds. Every save, backup, raw
save stream, installed file, native analysis project and path outside that exact
manifest is excluded. No original directory is removed.

The archive is
`.local-work/research-archives/cargo-transport-fuel-b02/cargo-transport-fuel.tar.zst`,
SHA-256 `ebda740f0092b93f1dc9f32120db365223f465a6d374ce8e98933e8041eb1da7`.
The central index is `.local-work/research-archives/index.json`, SHA-256
`5500892dbc247c642b83336ee619ca34d40fae8967ccfda95c5394e7ceff7e3b`.
The embedded inventory digest is
`f46605615abca2ff026f46aad6f51162a554c4383e89b79048899e4fb6e39a7a`.
The independent full restoration proof is
`.local-work/evidence-archive-stage-b/real-restoration02/`, with exact original
relative paths underneath. The detached final review must independently ACCEPT
this exact package before the maintainer considers retirement.

There is **no net storage relief** in this narrow proposal. The archive/index
allocate 5,578,752 bytes versus the 747,224-byte gross estimate; conditional net
recovery is −4,831,528 bytes before other controls and retained scratch. Resident
files may free less physical capacity than their reported allocation. Actual
original recovery remains zero. Recommend deferring retirement while separately
scoping useful consumer adaptation. The only decision needed to execute this
card is explicit approval of the exact manifest above; silence is not approval.

## Admission and stop conditions

1. Retain the independent expected digests from this reviewed card/delivery.
   Check current implementation hashes against the accepted delivery. Stop if
   code, index, archive, manifest, source or review identity has changed.
2. Establish exclusive control of the source/archive ancestor directories and
   quiescent evidence writers. Keep all existing active cargo roots untouched.
   Do not rerun retired editorial/acquisition scripts. Any unknown active consumer
   blocks its affected path and requires a revised manifest and fresh approval.
3. Query caller-available space on **both C: and D:**, fail below 40,000,000,000
   bytes, and reserve full restoration plus controls before recovery writes.
   This executor uses D:; it does not move long-term storage to C:.
4. Reauthenticate the central index against its independent digest, encoded
   archive and every decoded member. Recheck all exact original hashes. Perform
   a fresh controlled full restore when qualification is stale or an incident
   affects evidence. The existing local proof is not perpetual admission.
5. Run the same command below with operation `dry-run` and without
   `--execute-retirement`, then inspect its exact 37-file/no-deletion result.
   This alone does not approve execution.
6. Only after explicit manifest approval, execute the following from repository
   root with installed CPython. Capture output, timestamps, before/after capacity
   and progress records locally. Stop on any mismatch, missing source, write or
   disk failure, reparse/stream/hardlink hazard, lost writer control or operator STOP.

```powershell
& 'C:/Users/User/AppData/Local/Python/pythoncore-3.14-64/python.exe' -B `
  research/evidence-archive-stage-b/engine.py retire `
  --index .local-work/research-archives/index.json `
  --index-sha256 5500892dbc247c642b83336ee619ca34d40fae8967ccfda95c5394e7ceff7e3b `
  --manifest .local-work/evidence-archive-stage-b/deletion-manifest02.json `
  --approved-manifest-sha256 c80ac405e2f3af32fb715df6dc053865cc53756975fbae550e4a7ff40aed7eb7 `
  --execute-retirement
```

This is an unexecuted proposal, not a request to run it automatically. The
executor rechecks index/archive and the locked source immediately before each
handle-bound removal. It writes retirement intent durably first. No multi-file
atomicity is promised; a failure may leave some files removed and others present.

## Partial retirement, rollback and postflight

On interruption, preserve `retirement.json`, console/error receipts and current
namespace. Do not trust the journal as proof of deleted bytes. A retry that finds
any missing source stops, including an interruption between deletion and its
completion checkpoint. Do not substitute a newly computed expected digest.

Reauthenticate the reviewed central index/archive, check both drive guards and
reserve a full restore. Extract into a **fresh** D: task directory using
`engine.py restore` with the reviewed index digest and an explicit destination.
Hash each required restored file against the approved member expectation. The
full original-relative hierarchy is preserved. Under separately explicit recovery
authority, recreate only the approved missing originals; never overwrite a
surviving changed file or any save. Preserve the failed transaction and seek a
fresh operator decision before retrying the full exact allowlist. Synthetic
tests demonstrate this reconstruction/retry pattern; it was not applied to real
originals. A changed survivor requires investigation and reapproval, not rollback
over its bytes.

After successful retirement, reauthenticate archive/index, confirm exact approved
source absence, verify every retained original unchanged, check both drives and
record actual file-count/logical/allocation recovery separately from free-space
churn. Only then report cleanup completion and publish a revised local state.
No staging, commit, push, cloud upload or release follows from retirement approval.

A single local archive can become the sole surviving copy of retired members.
Drive failure, corruption or loss of the trusted index can therefore lose evidence.
Process-crash tests and write-through requests do not prove physical power-loss
survival. For every later scientific use, hash the restored input against the
reviewed member expectation. Reaudit encoded identity and member readability
before reuse and after storage errors, interrupted writes, unexpected source
changes or OS/storage repair. A periodic monthly audit is recommended for future
retired archives; none is scheduled or authorized to upload anything here. If an
audit fails, quarantine the archive and stop dependent research; never repair it
from an unverified source or silently bless a new digest.
