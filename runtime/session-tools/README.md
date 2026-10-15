# Phase-aware session operations

This is offline-qualified infrastructure, with version-specific adapters for
observer 0.7.0 and the historical [0.8.0 candidate](../local-readiness-080/README.md).
The 0.8.0 live proposal is now **NO-GO** under its
[scientific reassessment](../../docs/experiments/local-readiness/scientific-value-reassessment.md);
its plugin and run card remain unapproved.
Select `adapter: "080"` only with its reviewed version 8 manifest and run card;
the historical example below remains for 0.7.0. Adapter selection is retained in the
hash-bound plan/receipt and mismatched receipt/plan versions are refused.
It grants no launch, deployment, instrumentation, save or configuration authority.
Use only after review and the next experiment's explicit authorization. Observer
0.5.0 and 0.6.0 remain historical implementations; their protocols are not
interchangeable with 0.7.0. A different observer needs a reviewed small adapter.

Use installed CPython 3.14, standard library only, with `-B` and without `-O`.
No downloads, packages, shell subprocesses or native builds are used by the
operational commands. Paths and JSON receipts are private and remain untracked.
All outputs are exclusive; choose a new filename for every observation. Pin each
input receipt's SHA256 when handing it to another command. Hashes bind content,
not scientific truth or an authorization decision.

See the [future card](../../docs/experiments/session-infrastructure/future-run-card.md)
for the exact phase sequence and the [audit/qualification](../../docs/experiments/session-infrastructure/report.md)
for tested coverage and measured costs.

## Session commands

`session.py prelaunch --input PLAN --sha256 PLAN_HASH --out RECEIPT` performs
the expensive audit before launch: actual reviewed build/DLL/package, game/SFSE,
external runtime, protected and research sources; explicit loader/tool pins;
complete save content/mtime inventory; both-drive free-space guard and process-name
inventory. With `deployed: true`, it verifies the effective game plugin bytes,
installed SFSE and competing SOR observer DLL names. Optional README/notices or
manifest files alongside the deployed DLL are never required. This checks
effective deployment, not Vortex's internal database or a UI claim of deployment.
Normal Steam/NVIDIA overlays are accepted; module/admission receipts remain the
observer's responsibility.

The pinned plan is a local JSON object:

```json
{
  "adapter": "070",
  "build": "D:/Projects/starfield-outpost-research/.local-work/continuous-beacon-preview/builds/qualification-06",
  "manifest_sha256": "20d82ecea1949265778ba2ee1af578baa9a9d2836bb82a23f48a131df7381b2a",
  "deployed": true,
  "saves": "C:/Users/User/Documents/My Games/Starfield/Saves",
  "extra_pins": {
    "C:/Program Files (x86)/Steam/steamapps/common/Starfield/sfse_loader.exe": "16916c2ec47e31774e3d550609a1844fcb368b03060c03511891564b7f5f7526"
  },
  "removal_paths": []
}
```

This is a known historical identity example, not approval to run that experiment
again. The new reviewed card supplies the appropriate pins and any alternate
effective DLL removal paths shown by Vortex. Add separately reviewed operational
tool/executable pins in `extra_pins` where needed. The prelaunch receipt retains
the entire checked manifest, plan, shared-tool hashes and save inventory.

`session.py reuse-full --input RECEIPT --sha256 RECEIPT_HASH --out RESULT`
checks that the same full protected inputs still match. Use offline. A failed
pin cannot be waived or replaced with the newly observed hash. Before a new run,
create a new prelaunch receipt so existing sessions cannot be selected again.
An expected ExitSave rotation is separately reported; any protected-manifest pin
still applies even if its name begins ExitSave.

The following commands consume the prelaunch receipt and additionally require
`--session EXACT_NEW_SESSION`:

| Command | Work and effects |
|---|---|
| `request` | Rechecks shared-tool/build-manifest pins, deployed DLL/SFSE, PID/creation and disk. Publishes one unique `control-NONCE.request`; the exclusive output receipt binds nonce, identity, session and prelaunch hash. |
| `live` | Same small identity checks, READY/admission/site preimage receipts, worker/failure/emergency/retirement state, bounded 64 KiB health suffix. With `--request REQUEST --request-sha256 HASH`, checks only that request's ACK and full identity. No protected/save/archive rescan or raw-event decode. |
| `stop` | Reuses existing own-session STOP protocol, including preallocated four-byte flag. Bypasses full/protected/deployed/disk checks so STOP remains available on those incidents. Still requires trusted tool/build receipt and session identity. No process modification or automatic termination. |
| `postflight` | Confirms original PID/creation gone, independently repeats full content audits, checks removal, save rotation/content/metadata, and runs the existing version-specific decoder offline. Saves compact summary rather than duplicating all decoded events into a giant receipt. |

Always supply `--out NEW_RECEIPT`. `live` without a request cannot return
`READY_ACK`. A response to a newly generated nonce is fresh for that request;
there is no arbitrary age timeout. Do not reuse an old successful request as a
new phase challenge. Request another nonce at meaningful phase boundaries and
compare health serial/durable progress between receipts. Receipt observation is
cooperative and non-atomic; it does not establish perpetual health or a new module
snapshot. The worker performs its own instruction/relay checks before ACKs.

`WAITING_READY`, `WAITING_ACK` and `WAITING_FRESH_ACK` require an operator update
and continuation as appropriate. Slow progress or missed routine polls alone do
not stop acquisition. `STOP_PENDING_RETIREMENT`, `RETIRED`, `RETIREMENT_ERROR`,
`WORKER_FAILURE`, `PARTIAL_POSTFLIGHT` and `CHECK_ERROR` stay distinct. Investigate
missing progress; confirmed integrity/identity/instruction/worker failures, disk
query/floor failures and explicit STOP remain hard stops. Commands never
automatically issue STOP or kill the game. Stop while safe, preserve evidence,
then follow the approved exit/recovery policy. A failed postflight returns 1;
partial archival preserves that failure rather than converting it to PASS.

Every non-STOP operation checks **40,000,000,000 caller-available bytes on both
C: and D:** using `GetDiskFreeSpaceExW`. An unavailable query fails closed.
The preallocated STOP can succeed when disk queries fail; if its audit output
cannot be written, terminal/flag state still matters. Use the existing 070 STOP
command with its reviewed manifest if an independently changed shared-tool pin
prevents this wrapper; do not alter pins to bypass a failure.

## Archival contract

Create a roots JSON mapping simple aliases to absolute source directories and
`kind`: `raw-capture`, `derivative`, `private-receipt`, or `publishable-report`.
For example, `raw` points at the original session and `receipts` at the finished
run receipts directory. Include operator/control/module/health/journal/terminal
files and all companion metadata needed to reproduce the run. Use `derivative`
for analysis outputs. These labels preserve provenance; they grant no publication
clearance. Companion receipts and embedded paths may be sensitive.

Put the seal, ZIP and archival verification receipts **outside all sealed roots**.
Finish all companion outputs first; seal quiescent roots after confirmed game
exit. Do not add an archive receipt back inside a sealed root. Nested/overlapping
roots should be avoided so a single source has one unambiguous relative name.

```text
archive.py seal --input ROOTS_JSON --sha256 ROOTS_HASH --postflight POSTFLIGHT_JSON --postflight-sha256 POSTFLIGHT_HASH --out SEAL_JSON
archive.py create --input SEAL_JSON --sha256 SEAL_HASH --archive NEW_ZIP --out NEW_ARCHIVE_RECEIPT
archive.py verify --input SEAL_JSON --sha256 SEAL_HASH --archive ZIP --archive-sha256 ZIP_HASH --out NEW_VERIFY_RECEIPT
```

`seal` requires a hash-bound completed offline postflight with the original
process confirmed gone, the actual raw session root, and the postflight file in
the companion inventory. Only `PASS_POSTFLIGHT` can yield `COMPLETE` automatically.
Use `--partial-reason REASON` with `PARTIAL_POSTFLIGHT` to preserve a crashed,
incomplete or failed capture. `PARTIAL` describes the capture; every byte in that
partial source set still must archive and verify exactly. No raw tail is repaired,
trimmed or reinterpreted. If process exit/source quiescence or the offline
postflight cannot be established, preserve raw bytes and resolve that blocker;
the utility does not invent a seal. There is no separate new live authority here.

The source seal records every file's relative path, byte length and SHA256,
source-root provenance, completion classification and postflight hash. It is an
immutable-content receipt, not an operating-system write lock. The archive
contains that complete manifest as `SOR-MANIFEST.json` and every inventoried
file, compressed with standard ZIP Deflate level 6 and ZIP64 support.

Creation reserves the uncompressed total plus 1%, per-member/manifest overhead
and 16 MiB on the destination drive **above** the floor, while checking both
drives. Only C:/D: destinations are supported. Verification streams all members,
requiring no whole-archive extraction or additional full-size scratch. Creation
checks the disk guard during streaming, checks source inventories before/after,
hashes the ZIP and checks all member inventories, decompressed sizes, CRCs and
SHA256s. Duplicate/case-colliding/escaping/Windows-reserved paths, symlinks,
encryption, missing members, corrupt/truncated bytes and writer failures are
rejected. Failure leaves a durable error receipt when writable; an incomplete ZIP
is an unverified artifact and is never reused as successful output.

For selective analysis, first run full `verify` with the retained seal and ZIP
hash. Then use Python `ZipFile.open('raw/records.jsonl')` or another exact member
as a read stream. For a path-based decoder, extract only its required members
using `ZipFile.open` and `shutil.copyfileobj` to **exclusive new files in an empty
disposable directory**, using the already verified names; recheck their seal
hashes before analysis. Do not call unrestricted `extractall` on unknown archives
or overwrite originals. Keep derived outputs outside the raw roots. This utility
does not provide a virtual filesystem or modify native decoders.

**Retention proposal for later authorization:** keep the original raw tree,
original seal, verified ZIP and its receipt through the first production adoption
and independent maintainer review. Later, if authorized, move a redundant raw
tree to a separately named local quarantine, verify analysis from selected ZIP
members, and retain the quarantine for an agreed recovery interval before any
separate deletion decision. No automatic retirement, moving or deletion exists.

## Qualification and effects

```powershell
$py = 'C:/Users/User/AppData/Local/Python/pythoncore-3.14-64/python.exe'
& $py -B -m unittest discover -s runtime/session-tools -p test_session_tools.py -v
& $py -B runtime/session-tools/qualify.py --out .local-work/session-tools/NEW_QUALIFICATION
```

The tests use disposable files and mocked process/deployment contacts.
`qualify.py` additionally reads the fixed reviewed 070 manifest, protected inputs,
historical seal/metadata and bounded historical evidence prefixes; it writes
exclusive ignored test logs, copied prefixes and ZIPs. It never calls live
process/deployment/control functions. The historical full checker is invoked
offline without its CLI, launch or build actions. Its selected pins must match;
this is a qualification recipe for this checkout, not a universal benchmark.
Old native fixture suites are outside the shared interface and were not rerun.
