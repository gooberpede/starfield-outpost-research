# SorNativePositionOracle0.1.0

Original SFSE research instrument; distinct from SorBeaconObserver0.1.1 and the
abandoned external debugger adapters0.1.2–0.1.4. Offline qualification only.
No deployment/live/integration authorization follows from this source or ZIP.

[Architecture](../../docs/experiments/native-oracle/architecture.md),
[schema](../../docs/experiments/native-oracle/schema.md),
[combined review](../../docs/experiments/native-oracle/review.md),
[complete conditional run card](../../docs/experiments/native-oracle/run-card.md).

| Source/tool | Reads / writes / effects |
|---|---|
| core.h/plugin.cpp/patch.h | Once deployed/authorized only: actual natural callback/ref/context/native outputs; startup sole-thread CALL/vtable edits and nearby relay allocation; worker writes new ignored raw evidence. STOP retains inert hooks until normal exit. No invented inputs, engine lookup calls, gameplay edits or dynamic unload. |
| build.py | Reads installed game, explicit SFSE, exact protected inputs, own/header sources, installed MSVC/SDK; writes exclusive ignored build; runs original tests, never game/SFSE; builds ZIP. No download/deployment/config edits. |
| fixture.asm/tests.cpp | Original disposable synthetic ABI functions/allocations/call sites, controlled thread and exception/queue/writer tests; writes private fixture evidence only; restores its own patches. No game code copied/executed. |
| inspect_events.py/test_inspect.py | Reads journal/raw/frozen expectations; new JSON or synthetic ignored derivatives. Preserves originals, partials and mismatches; no process access. |
| operate.py | Read-only module/save/source hashes and Toolhelp process-name/PID inventory; exclusive ignored preflight/postflight/operator/STOP receipts. No launch, memory access or installation. |

Build from repository root with existing tools:

```powershell
& 'C:/Users/User/AppData/Local/Python/pythoncore-3.14-64/python.exe' -B runtime/native-oracle/build.py --name final-review-04 --sfse 'C:/Users/User/AppData/Roaming/Vortex/starfield/mods/SFSE 106 0.2.21 2026-06-11T15-06Z F5ipYCCxI/sfse_1_16_244.dll' --vcvars 'C:/Program Files/Microsoft Visual Studio/18/Community/VC/Auxiliary/Build/vcvars64.bat'
```

Use a fresh name to replay; no existing artifact is replaced. The exact installed
game/SFSE/header hashes, compiler logs and protected-before/after checks are in
build.json. MSVC/Windows SDK, CPython standard library and system DLLs only.
Existing unmodified approved PluginAPI.h/SOR-P-0001 remains at its original path
with its MIT notice in the package. No CommonLib, Address Library or detour code.
All source is REVIEW-REQUIRED; game/raw/save/analysis inputs remain LOCAL-ONLY.
