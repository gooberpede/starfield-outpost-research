# Local availability observer 0.8.0

**UNADOPTED HISTORICAL CANDIDATE — NO-GO.** The [scientific reassessment](../../docs/experiments/local-readiness/scientific-value-reassessment.md) rejects the proposed first live session. Plugin and run card remain unapproved. Build instructions below are retained documentation; no rebuild, observer execution or deployment is authorized for this correction.

Offline candidate for [SOR-EXP-0036](../../docs/experiments/local-readiness/contract.md).
No deployment or live authority. [Review](../../docs/experiments/local-readiness/review.md)
and [run card](../../docs/experiments/local-readiness/run-card.md) govern use.

Adapted from owned 0.7.0 capture/build/worker/decoder and 0.6.0 patch/module support;
exact original hashes and HEAD are in lineage.json. Third-party incorporation is
limited to the existing approved unmodified SFSE PluginAPI.h and its MIT notice
(SOR-P-0001); existing Microsoft runtime is a prerequisite, not bundled code.

Build with installed CPython 3.14 and MSVC/MASM/SDK, no downloads:

```powershell
& 'C:/Users/User/AppData/Local/Python/pythoncore-3.14-64/python.exe' -B runtime/local-readiness-080/build.py --name FRESH-BUILD-NAME
```

Reads exact installed executable/SFSE, inherited protected baseline, prior owned
toolchain receipt and own sources. Writes exclusive ignored build under
`.local-work/local-readiness/builds/`; compiles/runs disposable original fixtures
only, never executes retail functions or loads SFSE. Build checks both-drive
caller-available 40,000,000,000-byte floor and original protected hashes before
and after. No target, save/configuration, analysis DB, Git or network changes.
Large inherited protected audits can take minutes, entirely offline.

0.8.0 preserves event byte size 3328 but uses session schema 8 and a new report
schema. Source/provider tags are additions; the 0.7.0 adapter must not operate it.
Producer callbacks publish owned records through preallocated Windows lock-free
SLISTs. The worker alone hashes, writes and flushes. Overflow is sticky failure;
no producer waits for the worker. No invocation-wide locks or native lock-taking
by the observer. Fixed snapshot work uses ReadProcessMemory: OS execution and
timing perturbation remain, so this is bounded observation instrumentation, not
a promise of hard real-time latency or zero interference.

Queue capacity is 4096 owned records (about 13.7 MB plus links); vector/row capture
limit is 256 per collection. These protect callback work and memory. Exceeding
them stops admission and reports failure, never a sampled complete population.
They impose no total event, evidence-volume, elapsed-time or ACK-response quota.
Future integrated approval must include these concrete engineering bounds.

STOP closes admission, drains admitted invocations/records, and retains inert
resident wrappers until normal process exit. No hot unload/unpatch. Failed writes
preserve a verified durable prefix and explicit queued/loss/failure counters;
no repair or retry claims missing detached records were persisted.

Only `Data/SFSE/Plugins/SorNativePositionOracle.dll` belongs in the installed
plugin directory. ResearchNotices stay package notices. Keep raw/build/native
exports local; actual in-game reachability, timing and scientific results remain
NOT TESTED.
