# Reproduction, effects and provenance

2026-10-22 Australia/Sydney. [Report](report.md), [matrix](qualification.md).
Use repository root and existing Python3.14.3, MSVC19.51.36256.0/link14.51.36256.0,
Visual Studio18 Community and installed Windows SDK10.0.26100.0. No package,
dependency, compiler or SDK installation/download is needed or performed.

```powershell
& 'C:/Users/User/AppData/Local/Python/pythoncore-3.14-64/python.exe' -B research/resource-oracle-collector/build.py --name build08
& 'C:/Users/User/AppData/Local/Python/pythoncore-3.14-64/python.exe' -B research/resource-oracle-collector/qualify.py --build .local-work/resource-oracle-collector/build08 --output .local-work/resource-oracle-collector/qualification04
& 'C:/Users/User/AppData/Local/Python/pythoncore-3.14-64/python.exe' -B research/resource-oracle-collector/collect.py --synthetic-only --build .local-work/resource-oracle-collector/build08 --target .local-work/resource-oracle-collector/build08/sor-c1c-target.exe --output .local-work/resource-oracle-collector/manual01 --mode threads --stop-after 256
& 'C:/Users/User/AppData/Local/Python/pythoncore-3.14-64/python.exe' -B research/resource-oracle-collector/preserve.py --output .local-work/resource-oracle-collector/postflight01.json
```

First two commands were executed with those exact build/run names. The third is
an optional single-run example, not an executed manual01 claim. Fresh directories
are required; reproduce using new --name/--output suffixes. Never overwrite an
earlier test. collect exits0 for complete scoped acquisition,1 for failed
acquisition; controller errors exit2. Qualification exit0 means all positive and
negative expectations passed. STOP is available through --stop-after or the
controller's numbered ACK/STOP input; EOF also disposes the synthetic target.

build08/build.cmd and build.log retain exact cl /Bv /std:c++20 /EHsc /W4 /Od /MT
commands, tool output and exit0. build.json pins vcvars64, cl/link binaries,
installed SDK headers, source and output identities. qualification04 contains
each exact command, return/exception status, observed raw bytes, ACK hashes and
independent oracle test outcome. config.json pins wrapper/qualifier/preservation
source and inherited receipt transport separately from compiled source pins.

| Script/component | Reads, writes, dependencies, prerequisites and target effects |
|---|---|
| [build.py](../../../research/resource-oracle-collector/build.py) | Reads owned C++/header, installed toolchain/SDK; creates only fresh local build dir, command/log/manifest, objects and executables. Original command construction follows owned research/internal-observation-qualification/build.py conceptually, not copied assembly/observer. Existing cmd/MSVC/SDK run only for this fixture. |
| [target.cpp](../../../research/resource-oracle-collector/target.cpp) / fixture.h | Own resource arrays, stack Evaluation, membership computation, exported natural sampling boundaries, thread create/join/yield and optional allocated PAGE_NOACCESS boundaries or declared exception. No file/network/game API or shared data cooperation channel. |
| [controller.cpp](../../../research/resource-oracle-collector/controller.cpp) | Reads own sibling PE, actual created-process identity and stopped foreign memory/contexts; creates that fixture only, changes DR0–DR2/DR6/DR7/RF, continues owned events and disposes fixture on STOP/error. Writes JSON stdout and diagnostic stderr only. Installed Windows APIs/BCrypt, no outside implementation or old debugger source reused. |
| [collect.py](../../../research/resource-oracle-collector/collect.py) | Reads build pins/controller stream; executes guarded controller; creates fresh ignored config, per-stop frame/ACK files and final logs/results. Imports unchanged owned C1B transport; no third-party module/dependency. Bounded watchdog kills controller, whose explicit kill-on-exit policy applies to its disposable child. |
| [qualify.py](../../../research/resource-oracle-collector/qualify.py) | Executes guarded synthetic runs and inherited pure synthetic transport tests, independently compares raw bytes/identities/order/filter results; writes fresh case/test receipts. Oracle tables are not collector input. |
| [preserve.py](../../../research/resource-oracle-collector/preserve.py) | Reads start, named protected files, tracked bytes/Git metadata, disk space and disposable process names. Writes one new ignored audit receipt. No saves/config/index/process state changed. |
| [review_package.py](../../../research/review_package.py) | Unchanged owned exporter: reads actual tracked/untracked text, HEAD/index; writes ignored patches/manifests and standalone scratch application trees under .local-work/review-patches. No staging or real-tree application. |

New consultation RG2C1C-W01–W04: Microsoft [debug main loop](https://learn.microsoft.com/en-us/windows/win32/debug/writing-the-debugger-s-main-loop),
[x64 CONTEXT](https://learn.microsoft.com/en-us/windows/win32/api/winnt/ns-winnt-context),
[ContinueDebugEvent](https://learn.microsoft.com/en-us/windows/win32/api/debugapi/nf-debugapi-continuedebugevent),
[SetThreadContext](https://learn.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-setthreadcontext),
read2026-10-22. Used as API contracts for all-stop, fields, exception continuation
and OS-sanitized context state; no examples/snippets vendored or adapted.
C1B's cited ReadProcessMemory contract is inherited. SOR-P-0002 covers owned
framing/build/export methods. C++/Python implementation is original, using only
installed system headers/tools and stdlib; executable outputs remain local.

Preflight start.json records branch/HEAD/index/worktree, all tracked-byte pins,
inherited protected identities and both-drive free space. protected-preflight.json
freshly verifies229 inherited pins, including installed EXE, Save51/52 masters,
controlled copies and frozen predictions. Final preserve receipt rehashes them,
all unchanged tracked bytes and permitted navigation edits; inventory hashes all
task-local outputs. It queries zero surviving sor-c1c processes. Application
output placement is checked by source/build-command audit and local inventories;
no system-wide I/O tracing or assertion that Windows crash bookkeeping writes
only here is made. No code path opens a game/save for writing or chooses another
process. Local diff/link/newline/whitespace/application checks are in [review](review.md).
