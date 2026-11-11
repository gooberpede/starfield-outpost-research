# Cargo real-execution authorization card

**NOT AUTHORIZED — FUTURE PLAN ONLY.** This card does not grant execution GO.
The [implementation brief](../../implementation-briefs/README.md#archive-lookup) (`implementation-briefs.zip :: docs/implementation-briefs/CODEX_BRIEF_SOR_cargo_evidence_retirement_baseline_activation.md`)
authorizes code, inspection and disposable qualification. Independent review and
maintainer integration are separate from this destructive-operation decision.

## Exact proposed boundary

Repository/source root: `D:/Projects/starfield-outpost-research`.
Future transaction directory: `.local-work/cargo-retirement/real01/` below that
root; it must not already contain an unrelated transaction. Delete **only the
1,051 regular files** in the following unchanged allowlist, totaling **34,579,565
logical bytes**. No directory, wildcard, excluded hold, save, installed asset or
analysis project is an approved deletion target.

| Object, relative to repository root | Required SHA-256 |
|---|---|
| `.local-work/research-archives/cargo-transport-fuel-b02/cargo-transport-fuel.tar.zst` | `ebda740f0092b93f1dc9f32120db365223f465a6d374ce8e98933e8041eb1da7` |
| `.local-work/research-archives/index.json` | `5500892dbc247c642b83336ee619ca34d40fae8967ccfda95c5394e7ceff7e3b` |
| `ARCHIVE-MEMBERS.json`, embedded in that archive | `f46605615abca2ff026f46aad6f51162a554c4383e89b79048899e4fb6e39a7a` |
| `.local-work/cargo-evidence-cutover/real04/deletion-allowlist.json` | `b809a65f25560bec838873bfbb50c1e945a478a627129c24f837ec437b88e75d` |
| `.local-work/cargo-evidence-cutover/real04/recovery.json` | `7d1ddeb5d169b35178d2632d3cdc54843e426c8a4ad159d0520967c12c194b63` |
| `.local-work/cargo-evidence-cutover/real04/shadow-baseline.json` | `66f7c05b521a64008c6b419509bea5a5ecbcb71169681ae41271b6eab0e62169` |

The three excluded loose holds remain unchanged:

| Path | SHA-256 |
|---|---|
| `.local-work/c2-transit/package.py` | `21f6754b994523eebfa3dc0709e79a65876758d285fc7bc312ef9a96b0e141a5` |
| `.local-work/c2-transport/package.py` | `0ecbdfc0d26402c52d3335dc0f7de9d0741f66b7752f09292a4aa09f2b10998c` |
| `.local-work/c3-fuel/package.py` | `019ed90d3c12596b3fd7023e9d0215fd959e568947532aab389edb31e4e4ebae` |

Six empty historical directories are explicitly retained: the `scratch/` folders
in C1 Cargo, C2 transport and C3 fuel, and `ghidra-cache/User-ghidra/fscache2/new/`
in C2 transit, C2 transport and C3 fuel. The exact paths are bound by
`executor.EMPTY_DIRECTORIES`; unknown files or directories fail admission. Empty
directories are not retired or counted as recovered capacity.

## Baseline, method and storage identities

The canonical prior Cargo row list hashes to
`378e3d2a1a5a6a86dcbfd4da661d0e4a40b908ce9f25af6454130f91934ccf38`.
The canonical five-object replacement row list hashes to
`a815c8d5bc99e0c5a93894abfa47b23d9f4a5f032dd5b8f1d2a7a25d251ecaea`.
The active document additionally binds the transaction and journal prefix. Its
deterministically predicted SHA-256 is
`72e89e4bc3c905eeff2a163542b514b77929c4208ee34755412d22da2d6be148`,
with pre-commit journal prefix
`a64932744138a378e05af0c41213f906aa54a0f2e79b4fa8d938d0978bca6af1`.
Local `execution-identities.json` preserves the pure event-replay derivation.
There is no real active baseline document from this assignment.

Task HEAD is `6c22cc3c4e57838583e594e9db1c925bf139ced9`; repository index SHA-256 is
`b8d3bc5ae135235f6c8fca96e87da0b208657aecfcd8a292fca14e807719d38a`.
The local `.local-work/cargo-retirement/approval-template.json` binds exact
executor/resolver/preparer/Stage A/B method hashes, source/root/control identities
and transaction placement. It deliberately says `NOT AUTHORIZED`, has no expiry,
and fails authorization. A later changed HEAD/index, tool, manifest or source
version requires re-pinning and review; it is never silently accepted as this GO.

The [qualification report](executor.md) and local storage ledger give the final
retained-cost projection, free-space readings and distinctions between measured
cost and projected recovery. The conservative final projected net is **593,920
bytes**, after a 13,000,704-byte envelope for this assignment and separate 1 MiB
future-transaction and 1 MiB final-ledger/review/export reserves. Real preflight
must preserve those bounds or obtain a revised reviewed projection. Actual
recovered original bytes remain **zero**.
Immediately before future execution, query actual caller-available space again:
C: must have at least 40,000,000,000 bytes; D: must retain that floor plus the
executor's 8 MiB sensitive-stage reserve. Stored old free-space numbers do not
authorize a new run. No C: enduring authority or cross-drive atomicity is used.

## Future operator sequence and inert command

1. Re-pin the unchanged source/tool/control identities; confirm the actual
   independent final-snapshot ACCEPT and the maintainer's separate approval of
   this exact transaction. Preserve that approval locally and retain its digest
   independently. Set an explicit timezone-aware expiry and exclusive-ownership
   declaration only after the maintainer supplies GO. Never use a synthetic
   approval or the inactive template as human authorization.
2. Confirm no other writer owns Cargo namespaces or transaction controls; check
   NTFS placement, both-drive free space, all originals and three holds, archive
   deep integrity, and the current preparer's exact real preflight. No target
   process needs to be launched or attached.
3. Run the following command only after that separately approved receipt exists.
   The placeholder approval/hash is intentionally unusable now.

```powershell
$cargoPython = 'C:/Users/User/AppData/Local/Python/pythoncore-3.14-64/python.exe'
& $cargoPython -B research/evidence-access/executor.py execute `
  --root 'D:/Projects/starfield-outpost-research' `
  --plan '.local-work/cargo-evidence-cutover/real04/deletion-allowlist.json' `
  --plan-sha256 b809a65f25560bec838873bfbb50c1e945a478a627129c24f837ec437b88e75d `
  --recovery '.local-work/cargo-evidence-cutover/real04/recovery.json' `
  --recovery-sha256 7d1ddeb5d169b35178d2632d3cdc54843e426c8a4ad159d0520967c12c194b63 `
  --shadow '.local-work/cargo-evidence-cutover/real04/shadow-baseline.json' `
  --shadow-sha256 66f7c05b521a64008c6b419509bea5a5ecbcb71169681ae41271b6eab0e62169 `
  --folder '.local-work/cargo-retirement/real01' `
  --approval 'SEPARATELY_AUTHORIZED_RECEIPT.json' `
  --approval-sha256 'EXTERNALLY_RETAINED_APPROVAL_SHA256'
```

4. Preserve stdout, journal hash and returned baseline digest. Require the returned
   baseline digest to equal the prediction above; any mismatch blocks acceptance.
   Routine verification
   uses the same source/control/folder arguments with `verify` and
   `--baseline-sha256` set to that independently retained digest. COMMITTED must
   agree with the baseline and exact absent-source population. A baseline file
   by itself is not a commit. Routine archive/index and hold verification does
   not hash retired member payloads; scientific restoration still verifies them.
5. Perform authenticated archive/member restoration smoke checks and the two
   maintained consumer replays using fresh leases. Verify lease cleanup, three
   loose holds and scoped protected-file equality. Preserve original source and
   failure provenance; no whole 90K-pin rehash is implied by this Cargo boundary.
6. Measure actual file allocation/free-space change separately from unrelated OS
   activity, count exact removed files, record durable closure and the new Cargo
   routine entrypoint. No global preservation policy is automatically changed.

## STOP and recovery

STOP on any identity mismatch, missing hold, unexpected Cargo node, unsupported
filesystem/reparse/hardlink, lost lock, expired/substituted approval, failed
free-space query/floor/reserve, source mutation, IO/permission failure, corrupt
journal, baseline conflict or operator STOP. Preserve all surviving evidence;
never skip an uncertain member and declare completion.

With an intact journal and authentic archive, re-run the same approved transaction
within its conditions: completed missing sources are checked against the exact
prefix; only an INTENT permits reconciliation of an absent pending member.
A baseline published before the final COMMITTED event remains inactive until
the same authenticated transaction safely completes. A torn journal tail or
`baseline.writing` requires explicit reconciliation and re-reviewed recovery;
the executor neither truncates nor cleans it automatically.

To restore loose preservation after partial/full retirement, use authenticated
restore into a fresh lease, verify every needed member and the held versions,
then obtain separate approval for copying to original locations without
overwriting survivors. Only afterward can the prior row list become effective.
The old shadow rollback function returns metadata; it does not recreate files.
Loss of the sole authoritative local archive after removal can be irrecoverable;
there is no promised off-device recovery or physical backup.

## Specific future approval request

> Do you authorize the exact 1,051-file retirement and Cargo archive-baseline
> transaction at `D:/Projects/starfield-outpost-research/.local-work/cargo-retirement/real01`,
> using allowlist SHA-256 `b809a65f25560bec838873bfbb50c1e945a478a627129c24f837ec437b88e75d`,
> the archive/index/inventory/recovery/shadow identities and three exclusions in
> this card, and the exact independently reviewed implementation snapshot? This
> authorizes journaled exact-file deletion and Cargo-specific baseline commit
> only, subject to fresh identity/space/exclusive-ownership checks and an agreed
> approval expiry. It accepts the stated risk of irrecoverable single-drive
> archive loss. It does not authorize staging, commit, push, publication, live
> activity, other-system cleanup or a changed deletion set.

No such approval is requested or presumed as part of the current implementation
delivery. Expected postflight evidence is the authenticated COMMITTED journal,
externally retained active-baseline hash, zero remaining allowlist sources,
unchanged three holds, archive/member smoke and consumer receipts, temporary
lease absence, source/tool/Git pins, both-drive space and actual recovery ledger.
