# C1G controller, receipt contract and actual qualification

[Answer](report.md), [native ledger](native.md), [sources](sources.csv).
Project-owned C1E controller/build/preflight/postflight/wrapper at initial
HEAD `43786e5e418f2a9a4c43476a5ba3cadeb8d12d3e` are adapted into
[research/resource-selection-operands](../../../research/resource-selection-operands/).
Original files and C1C/D/E receipts are unchanged. SOR-P-0002 covers owned methods;
native instructions remain evidence, not redistributed implementation. The MASM
fixture expresses original source-shaped frames and known data; it implements
neither the game's RNG nor geometry.

## Receipt and identity

Unchanged SRO1 SESSION/SAMPLE/END and digest/ACK transport; additive sample schema
`sor-c1g-operands/1`. SESSION supplies measured image base, hash/PID and exact
16-byte site guards. Samples retain raw Windows CONTEXT/MXCSR, UTC FILETIME ticks,
event/sample/thread sequence, TID/lifetime, read volume/calls and elapsed copy
time. Thread-local invocation tokens/parents join exact native stack frames;
tokens alone are not globally unique. Provider return is a witnessed terminal,
not a successful-population certificate. Exceptions invalidate invocation state;
unwitnessed terminal counts remain explicit at prune/thread/process exit.

Each read group supplies address, requested length, COMPLETE/INCOMPLETE and raw
bytes or null. Bounded zero-valued bytes are distinct from failed reads and
unobserved sites. Required-read completeness is separate from entry/namespace/
source binding and scientific sufficiency. Successful memcpy or checksum does
not establish semantics. No deferred worker dereferences target pointers.

Field coverage and instruction domains are in [native.md](native.md). The current
four-site acquisition does not copy complete predecessor/accepted geometry or
prove cache installation, source ABA exclusion, all-writer lifetime or historical
producer→consumer continuity. Full effective BIOM/component/alternate RSGD
interpretation is limited by captured raw selection evidence; a null selected
RSGD pointer does not certify no fallback descriptor. One current selection is
not the complete override winner map. No save persistence class is promoted.

## Operation, bounds and effects

Inherited Windows attachment/all-stop/DR0–DR3/DR6/RF engine uses no software trap,
stepping, injected code, forced game call or target-memory write. It does pause
and alter execution timing/debug/control state and can dispose the admitted
process. Context readback checks general/floating state and meaningful control
bits; complete AVX/XSTATE and all scheduler interleavings remain unqualified.
This is disclosed instrumentation, not a non-invasive observation claim.

Individual foreign reads are <=65,536 bytes, total <=1,048,576 bytes per stop,
JSON frame <=1,048,576 bytes, native invocation stack <=64 and external active
invocations <=4096. These bound memory/copy integrity, not scientific event
volume or healthy session duration. Capacity refusal records loss/incompleteness
or fatal LOSS and disposes the synthetic/admitted target. Both C:/D: caller-free
space guards remain 40,000,000,000 bytes. No installation or download.

The retail wrapper requires a fresh actual-human GO receipt, card/build/preflight
hashes, fresh Cloud confirmation, newly Steam-started PID/path/hash/start time,
save/backup READY checks and exclusive consumed marker before controller startup.
It does not launch the game. `readiness.Tracker` stops only after a complete
candidate source invocation returns with main-file IL cells (10,1) and (11,1)
and Copper (11,1) comparison receipts. Neither desired admission nor weight 0.05
is required to stop: contradictory operands are equally useful. Missing namespace,
failed reads, frame joins or a different owner cannot satisfy that predicate.
This selector tests a candidate source, not actual P3 Workshop ancestry.

## Commands and results

Commands below use the installed Python 3.14.3 executable at
`C:/Users/User/AppData/Local/Python/pythoncore-3.14-64/python.exe`; WindowsApps
`python` is not the interpreter. Run from repository root, without `-O` because
admission assertions are fail-closed checks. Reproduction must choose fresh names.

```powershell
$sorPython = 'C:/Users/User/AppData/Local/Python/pythoncore-3.14-64/python.exe'
& $sorPython -B research/resource-selection-operands/provenance.py --output .local-work/resource-selection-operands/provenance01.json
& $sorPython -B research/resource-selection-operands/replay.py --provenance .local-work/resource-selection-operands/provenance01.json --output .local-work/resource-selection-operands/replay01.json
& $sorPython -B research/resource-selection-operands/test_readiness.py
& $sorPython -B research/resource-selection-operands/build.py --name build05
& $sorPython -B research/resource-selection-operands/qualify.py --build .local-work/resource-selection-operands/build05 --output .local-work/resource-selection-operands/qualification04
& $sorPython -B research/resource-selection-operands/preflight.py --build .local-work/resource-selection-operands/build05 --qualification .local-work/resource-selection-operands/qualification04/qualification.json --name offline-preflight02
```

Actual MSVC19.51.36256.0/link14.51.36256.0, VS18.9.0 and installed SDK; build.cmd,
build.log and build.json preserve exact compiler paths/commands/hashes. Build05
controller SHA256 `dc210aaa688a07d4911ae4f20415f5962e051d3f1f4437fd54009b405c3ccbcf`.
Its source and wrapper pins are in build.json. No target ran during compilation.

27 native debug scenarios / 187 persisted samples passed in qualification04:
inactive, active, rarity-above-mask, inactive-out-of-switch, installed-setting,
paired, alternate, copper, rejected, nested, threads, wrong-workshop,
missing-namespace, stack-budget, injected-context-failure, wrong-owner,
wrong-source, partial-descriptor, partial-dnam, byte-budget, guard-mismatch,
ackfail, no-hit, crash-before, crash-after, crash-during, completion. Every saved sample was
closed, independently parsed/digest-checked with its ACK, before controller ACK.
Completion uses the real Tracker on the paired IL→Cu fixture and sends atomic
ACK8 STOP at provider return; target survival is deliberately not required.
The final crash-during case preserves one durable entry before the unhandled
exception, records one invalidated invocation and never invents a provider
terminal. Build05 adds this explicit loss field/test after the independently
checked build04. Installed-setting fixture admits IL (10,1), rejects IL (11,1); active admits both.
XMM3 is deliberately clobbered inside the cell wrapper; independently captured
XMM1/XMM7 still govern the correct branch. Cells/keys have known signed/raw words.

Partial DNAM test crosses a real NOACCESS page while the specific target block
stays readable. Source/descriptor failures use invalid target addresses.
Stack-budget refuses invocation65 after 64 durable entries; byte-budget induces
the actual bounded copy-reader refusal. Injected-context-failure is an explicitly
injected controller fault after real GetThreadContext, not an OS context failure.
No-hit has zero receipts and is not a validated absence finding. Wrong-workshop
puts matching identifier bytes in unrelated source memory; binding remains UNKNOWN.
There is no real OS allocation/queue exhaustion or universal event-loss proof.

Two pure selector tests additionally cover wrong owner/frame/lifetime, rejected
namespace/read/join, exception invalidation and nested completion. Inherited
C1C build08 qualification-c1g02 passes19; C1D build14 qualification-c1g01 passes13
and40 decoder assertions; C1E build06 qualification-c1g01 passes32. Those local
roots are their original subsystem folders. A C1C run against obsolete build03
failed; it is retained as qualification-c1g01 and is not the qualified regression.

Earlier C1G build01 failed MASM ambiguous memory operands; build02 fixed explicit
DWORD size and qualification01 passed18. Qualification02 preserved two incorrect
test expectations introduced when adding wrong-workshop/missing-namespace cases;
the expected distinction between complete reads and unknown binding was corrected.
Build03 and all earlier receipts remain local. Preliminary independent review
found missing exception TID in the new wrapper path; build05 fixes it and adds
real paired-resource stop selection plus rarity branch controls. No old failure
or frozen result was rewritten.

The offline preflight independently rehashed271 live/271 backup saves and39
definitions, configuration, EXE; rehearsed a Save52 copy and checked exact
instruction/callsite guards. Cloud remains UNKNOWN pending fresh operator
confirmation. Build, qualify and pure tests write only fresh ignored outputs;
preflight adds a scratch restoration copy, never a live restore. Provenance/replay
read only named inputs and write new ignored JSON. Postflight inventories/hashes
without restoring. The wrapper/controller live path has **not** been executed.
Fresh per-session qualification/preflight and explicit human approval are
required before any such operation; this Phase A test result supplies none.
