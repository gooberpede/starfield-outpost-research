# Implementation, qualification and reproduction

[Report](report.md), [native ledger](native.md), [source pins](sources.csv).
The six C1G controller/fixture/build sources and C2B operational wrappers at
HEAD `e684cd4d2ebab886fc9c1995f02ea421c2b4cec9` are adapted under SOR-P-0002.
C1D namespace/bounded-read helpers and SRO1 transport are reused unchanged.
No third-party implementation, dependency, download, contact or disclosure was
added. Installed Python 3.14.3, MSVC 19.51.36256.0, linker 14.51.36256.0 and
Windows SDK supply the local toolchain. Source/output pins and exact commands
are in the ignored build.json/build.log; compiler/assembler/linker hashes are
in sources.csv; no built binary belongs in Git.

## Controller and limits

`research/resource-selection-context/controller.cpp` retains the owned Windows
all-stop engine, thread lifetimes, DR0–DR3, DR6/RF ownership, instruction guards,
CPU-state readback, external ACK and kill-on-debugger-exit policy. Generation
entry and ordinary CALL stay fixed; DR2 rotates through BIOM return, query conversion, component return,
mask call/return and alternate candidate/resolution. DR3 watches provider entry
outside generation and the generator continuation during generation. Each thread
has its own stage and invocation stack. The controller checks all eleven relocated instruction
preimages against the hash-pinned disk PE, then checks the current preimage at
each hit. Native aliases are analyst labels, not exported engine APIs.

This is disclosed instrumentation: it pauses execution, changes owned debug
state/timing and may terminate or destabilize a disposable target. It uses no
software breakpoint, injection, single-step or target-memory write. General and
floating CPU state is read back after DR/RF changes; full AVX/XSTATE and all
scheduler interleavings remain unqualified.

Each foreign read is at most 65,536 bytes; each stop copies at most 1,048,576
bytes; each JSON frame is at most 1,048,576 bytes. Descriptor/RNAM/resource arrays
are bounded at 64 entries; native invocation stacks at 64, tracked threads and
external active invocation records at 4096. These are memory/integrity bounds,
not scientific event or session-duration quotas. Both-drive caller-free-space
guards remain 40,000,000,000 bytes. Bad pointers/counts or lost stages produce
INCOMPLETE/INVALID or explicit fatal LOSS, never a resource-negative conclusion.

The sample schema is `sor-d4-operands/1`. Preserve PID/TID/lifetime/sequence,
capture numbers, raw Windows CONTEXT, UTC FILETIME, addresses/lengths/status/raw
bytes, source/manager copies, upstream capture numbers, selected operands and
ordered candidate arrays. `required_reads_complete`, upstream binding, stage
bits/validity, resource-call qualification and scientific sufficiency are separate.
The raw ordinary sampler return is not a full raster-byte/Special observation.

Breakpoint rotation has a tested blind interval: a nested producer can begin
while DR2 watches a parent's later stage. Fixed generation entry still records
the nested invocation; missing upstream/component/mask stages remain explicit,
and neither nested nor parent completion is invented. Pointer reuse, source ABA,
all-writer lifetime, historical cache epoch and source-population census remain
unqualified. Workshop binding and generation-to-consumption continuity are
explicitly UNKNOWN at every producer sample.

## Actual tests and reproducible commands

Run from repository root with the installed interpreter, without `-O`. Choose
fresh output names when reproducing; existing receipts are never overwritten.

```powershell
$d4Python = 'C:/Users/User/AppData/Local/Python/pythoncore-3.14-64/python.exe'
& $d4Python -B research/resource-selection-context/build.py --name build12
& $d4Python -B research/resource-selection-context/qualify.py --build .local-work/resource-selection-context/build12 --output .local-work/resource-selection-context/qualification11
& $d4Python -B research/resource-selection-context/test_readiness.py
& $d4Python -B research/resource-selection-context/preflight.py --build .local-work/resource-selection-context/build12 --qualification .local-work/resource-selection-context/qualification11/qualification.json --name offline-preflight04
& $d4Python -B research/resource-selection-context/analyze.py --captures .local-work/resource-selection-context/qualification11/inactive --case D2-81a75b --output .local-work/resource-selection-context/synthetic-analysis04.json
```

Build reads owned sources and installed MSVC/SDK, writing a fresh ignored build;
it executes no target. Its manifest binds the transitive operational sources,
including oracle collect.py/saves.py, receipt_probe.py and C2B protection/policy.
Qualification admits only a hash-pinned, gated synthetic PE created with no
visible window. The controller obtains answers through ReadProcessMemory from
target-owned allocations; the fixture does not provide answer JSON or pointers
over a cooperative receipt channel. PE export RVAs identify synthetic stops only.

The final suite passes 34 debugger scenarios with 373 persisted SAMPLE receipts. It covers distinct descriptor bytes
and pointers, candidate reordering, first-success termination, effective RSGD
precedence, current BIOM RNAM precedence and final fallback. The test oracle
checks expected descriptor markers, complete 560-byte equality and pointer
membership in independently acquired candidate entries, plus actual visitation.
The original source-shaped selector is deliberately small; it is not a retail
engine implementation or proof that Save52 took those branches.

The nonuniform-mask fixture uses a target-owned position-indexed sampler:
initial query (101,−201) returns 1; later cell queries return 4. Acquired source
mask/weight retains the initial result while the provider-return output records
both sampled values. Other controls cover concurrent threads, nested calls,
wrong owner/source/Workshop association, incomplete descriptors, inaccessible
pages, bad counts/node/index, byte budget, guard/context faults, ACK rejection,
no hits and crashes before, during and after collection. The injected context
failure is a controller fault after GetThreadContext, not a real OS API failure.

Every SAMPLE is independently parsed for SRO1 sequence/length/digest/END and
external ACK/readback before acknowledging the target. Separate truncated and
digest-corrupted derivatives must be rejected. The completion case uses the real
candidate Tracker; evidence is durable before ACK STOP disposes the target.
Two additional pure selector tests reject wrong owner/upstream/frame/namespace,
exception and thread-loss cases. They do not prove universal event-loss freedom
or qualify every possible scheduler, allocation or Windows failure.

The unchanged D1 verifier ran against `.local-work/resource-standalone/build03`,
writing `seven-controls01`. All seven original region controls match full ordered
XYZW/bounds and callback decisions in both corpus representations (14 comparisons).
All 31 D1/D2/D3 pure regression tests pass. Exact commands, output and exit status
are in `regression-01..03` under the D4 local root. No retail-derived replay occurs.

## Preserved failures and reviewer corrections

Build01 succeeded with inherited unused-variable warnings; build02 removed them
and qualification01 passed 24 scenarios. Build03 failed a MASM jump to a BYTE
label; build04 uses a separate loop label. Qualification03 preserved the poisoned
index fixture's own invalid access, which prevented a resource-call witness.
The fixture now uses a separate bounded control counter while exposing the bad
iterator to the observer. Qualification04–06 passed the then-current 27 cases.

Initial independent review correctly found that two nominal alternate candidates
shared one descriptor and an unconditional fixture traversal did not test winner
precedence. It also found no spatially nonuniform first-query control and missing
transitive transport/save-helper pins. These were engineering gaps, not native
results. Build08 adds distinct descriptor/precedence cases, the position-indexed
sampler and full operational pins. Qualification07 preserved three outdated
visitation expectations after first-success/direct paths were introduced. Their
actual winner tests passed; qualification11 uses explicit route-specific
visitation oracles and full candidate-pointer/byte checks. No failed receipt or
historical prediction was rewritten to make it pass.

Preflight performs full offline hashes and a fresh scratch-only Save52 restoration
rehearsal. It never changes Cloud, saves, configuration or a game process. The
new wrappers use the revised C2B active-transient policy; archives and designated
saves remain strict. Fresh Cloud confirmation is still UNKNOWN during Phase A.
Postflight independently compares the fresh preflight, and preservation checks
rehash the task baseline and earlier frozen evidence. The final review record
names exact receipts and their coverage. Raw payloads, private receipts, source
exports, saves, builds and scratch trees stay ignored and excluded from patches.

Finalization found a cache-bypass lineage hazard: an unconsumed BIOM/query
pending record could survive a provider return and meet reused stack/pointer
values in a later operation. Build12 observes provider entry, gives it a fresh
thread-local token, clears pending state there and on exceptions, and requires
that token plus the full provider/generator frame relation. DR3 changes to the
generator continuation only during generation. Cache-only and same-frame
cache-then-generation controls test that the old capture cannot be inherited.
Earlier successful suites remain preserved but do not qualify this new case.

Qualification10 retained two test-oracle failures: the new cache modes were
accidentally included in the older no-hit expectation group. The distinct
provider-token/same-frame assertions passed. Qualification11 removes that
conflicting expectation and retains explicit cache-only and cache-then-generation
assertions. No acquisition output or native conclusion was changed by the test
correction.
