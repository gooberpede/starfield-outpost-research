# Native position-write observer 0.6.0

Offline candidate for the [authorized history brief](../../docs/implementation-briefs/README.md#archive-lookup) (`implementation-briefs.zip :: docs/implementation-briefs/CODEX_BRIEF_SOR_workshop_position_write_history_Z_oracle.md`).
[Report](../../docs/experiments/position-write-history/report.md),
[static coverage](../../docs/experiments/position-write-history/static-audit.md),
[prospective card](../../docs/experiments/position-write-history/run-card.md),
[schema](schema.md). No deployment or live execution in this assignment.

The build generates wrappers for all 115 evidenced direct B4E410 CALLs, both
B73310 CALLs, seven F4AB80 CALLs, four producer/allocation/application CALLs,
and one independently traced ordinary-reference B734C0 virtual slot. There are
128 CALL edits and one pointer edit. Each complete CALL forwards the original
four integer/pointer registers and original pointer operands. No stolen prologue,
return-address replacement, synthetic native call, debugger or exception masking.
Native void-return RAX is raw unspecified output, never an established result.

Capture starts before SFSE Load returns and includes generic references before
Workshop identity is available. A group-flushed, serialized file spool replaces
the 050 saturation-drop queue. There is no event queue, record quota, timeout or
evidence-size cutoff. WriteFile and OS cache backpressure can delay engine calls;
group flush briefly holds the same spool lock. No observer lock spans a native
call. The worker does not require native engine locks to flush copied records.
Module inventory runs before edits and after retirement, outside acquisition.

The disk floor is caller-available 40,000,000,000 bytes on both C: and D:; each
raw/journal write reserves its actual pending D: bytes above that floor. Failed
queries stop capture. Captured and last-durable sequence are separate; crash
before group flush may lose a suffix. The current one-second flush/health interval
is telemetry, never a deadline or STOP. Pending calls retain completion records
after STOP. Resident patches remain inert until normal game exit; no live unload.

Runtime payload is only `Data/SFSE/Plugins/SorNativePositionOracle.dll`.
Installed Microsoft /MD and Windows runtimes are separately pinned, never bundled.
Package notices are distribution/review material, not admission dependencies.
Existing unmodified SFSE PluginAPI.h/notice uses SOR-P-0001. Owned 050 patch/module
helpers and ABI probe are adapted under SOR-P-0002; win_support/core are reused
verbatim. Build source hashes preserve exact lineage. New code/fixtures are
project-authored and informed by native analysis, not clean-room work.

| Tool | Reads, writes, prerequisites and effects |
|---|---|
| `build.py` | Reads pinned retail PE/SFSE, historical protected pins, native xref export and sources; uses installed MSVC/MASM/SDK and CPython; creates a fresh ignored build, runs original disposable processes, packages DLL/notices. No target execution/deployment/download. |
| `plugin.cpp`, headers, generated wrappers | Future separately approved in-process CALL/pointer edits; copies raw arguments/memory; serializes file writes and group flushes; may change timing. New session logs/control/emergency page only. No reference counts, gameplay fields or registers are intentionally mutated. |
| `tests.cpp`, `fixture.asm`, `lifecycle_tests.cpp` | Own disposable memory/instructions/processes only; exercises the actual spool, patches and worker; one own child exits intentionally after flush. No retail code executes. |
| `inspect_history.py` | Reads session bytes; verifies journal hashes and prefix; optional new JSON output. Streaming summary uses memory proportional to active invocation bookkeeping; two-pass Workshop mode retains only pointers later seen with selected IDs. Full decode retains selected event objects and should be used for small fixtures. Raw originals remain unchanged. |
| `operate.py` | Reads pinned build/protected inputs and process identity metadata; writes fresh audit/seal receipts and own session ACK/STOP controls only. STOP bypasses admission/protected checks and overwrites four preallocated control bytes even when disk queries fail. No game launch/attachment/deployment/save/configuration changes. |
| `test_inspect.py`, `test_operate.py` | Reads generated fixture/build outputs; writes new disposable corruption/control copies and result receipts only. Never rewrites originals to pass. |

Reproduce offline with installed CPython:

```powershell
& 'C:/Users/User/AppData/Local/Python/pythoncore-3.14-64/python.exe' -B runtime/native-oracle-060/build.py --name NEW-UNIQUE
```

Build requires retained baseline/xref receipts and prior 050 build provenance at
their documented local paths. This is a research repository reproducibility
contract, not a standalone public SDK. Binaries/generated native preimages stay
local. Fixture correctness does not establish all native writers, continuous
lifetimes, saved-to-loaded remapping, native reachability or XYZ equivalence.
