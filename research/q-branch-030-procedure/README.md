# External Q030 procedure checks

Original GPL-3.0-or-later operational tooling for the [run card](../../docs/experiments/q-branch-030/live-run-card.md).
CPython3.14.3 standard library and existing project helpers only; no downloads.
The qualified runtime/native-oracle-030 tree is read/imported, never edited or rebuilt.

`prepare_lock.py` reads the existing build receipt, ZIP, executable CALL bytes,
protected inputs, previous evidence manifest and tool sources. It verifies identities
and exclusively writes the requested ignored release lock. No target execution.
`procedure.py audit --mode offline` hashes files/saves, inventories plugin files
and enumerates process **names** through Toolhelp; it never opens a process handle.
All audit modes require 40,000,000,000 caller-available bytes on C and D (failed
queries fail), required directories and exact protected/source identities.

**2026-10-12 external inventory repair:** [qualification and prospective amendment](../../docs/experiments/q-branch-030/module-inventory-fix.md).
Original lock02/previous tool qualification are historical. The revised modules
command requires a new lock explicitly pinning cooperative acquisition; no live
retry follows. The030 DLL and runtime sources remain unchanged.

`environment.py files` reads explicit local load-order/INI contents and hashes,
game-root/Data file metadata, distinguishing ABSENT from unreadable (failure).
Its revised future-only modules command reads the unchanged worker's latest complete
numbered module inventory, requests fresh nonce/ACK within15 seconds, validates health
and limited creation metadata, rehashes module files and rejects unstable/invalid
receipts. It does not perform a cross-process module snapshot or read target memory.
A30-second parent timeout stops only the inventory helper, never the target. Failed
queries/hashes/timeouts block cues; caller requests STOP. ACK is worker progress,
not an inventory digest binding; separate native scans can race A→B→A, so this is
last emitted cooperative inventory, not exact current-loader equality. Existing
Toolhelp function remains for the own-interpreter regression only. Tests use
synthetic receipts and a real reader child against the Python test interpreter.
CPython/Windows APIs only; no external code reused or elevation attempted.

Only a separately approved future run may use deployed audit, admit, monitor,
checkpoint, postflight or existing runtime control commands. Monitor reads receipts
and limited process creation metadata through the unchanged health helper; it
publishes flushed ACK/STOP files and exclusive ignored reports. No target memory,
debugger, game launch, installation, native calls or save/configuration edits.
Checkpoint copies only an operator-identified **new** manual save into an exclusive
ignored directory; it never writes the source. Postflight hashes original and copied
checkpoints, inventories save rotation, imports the unchanged inspector/branch
analyzer and writes new reports. It does not parse saves or infer menu identity.

Outputs are local-only `.local-work/q-branch-030-procedure/`; native session output
uses the unchanged config's `.local-work/native-oracle-live/session-*` root.
Use new output names; exclusive creation rejects overwrites. Admission receipts
are plugin self-attestation, not an independent read of live patched memory.
Monitor targets3 seconds, rejects measured gaps over10 seconds, retains the native
15-second gate, and attempts STOP on failure after establishing new-session ownership.
The512MiB observed output threshold and20-minute monitor bound initiate STOP;
sampling/drain latency means they are not exact byte/time caps. STOP is resident
retirement, never hot unloading. Terminal-file presence is preliminary; final
inspector determines completeness. Hardware/storage inability to write STOP requires
normal operator exit and an incident record, never forced recovery.

Offline qualification (synthetic directories only; live process metadata stubbed
to raise if accidentally accessed):

```powershell
& 'C:/Users/User/AppData/Local/Python/pythoncore-3.14-64/python.exe' -B research/q-branch-030-procedure/test_procedure.py -v
```

Tests retain their fixtures and never alter protected evidence. See the
[qualification record](../../docs/experiments/q-branch-030/procedure-qualification.md)
for actual results and limitations.
