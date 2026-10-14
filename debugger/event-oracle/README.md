# Event-associated oracle adapter 0.1.3

Original, narrowly scoped Windows x64 software-breakpoint adapter for
[the authorized implementation brief](../../docs/implementation-briefs/CODEX_IMPLEMENTATION_BRIEF_SOR_event_associated_oracle_instrumentation.md).
The [latency follow-up](../../docs/implementation-briefs/CODEX_BRIEF_SOR_event_adapter_latency.md)
governs0.1.3; [report and comparison](../../docs/experiments/event-latency/README.md).
**Review candidate; no Starfield execution in this task.** It is an external
debugger, independent of the unchanged SFSE observer 0.1.1. It never launches a
game or calls game-native functions. Runtime mode requires separate live review
and authorization. [Contract and prospective card](../../docs/experiments/event-instrumentation/README.md).

`adapter.cpp` attaches to an explicitly identified PID, verifies its on-disk
executable hash and loaded site preimages, installs scoped INT3 bytes at a debug
event stop, and copies producing invocation evidence. It temporarily restores
one instruction, rewinds its RIP and owns TF for one step while other known live
threads are explicitly suspended. Newly reported threads are held during replay.
It rearms before resuming those threads. Original instructions run in place;
there is no relocation, trampoline, stack injection or replaced return address.
This changes execution/scheduling and is intrusive. It writes target code bytes
and control context only for that protocol; no DR writes or engine calls.

Center entry/exit use thread, original SP/caller, reference and output pointer.
Grid callback entry, two translated-axis register boundaries, selected hierarchy
and common exit form a separate branch. No identity is selected by output values.
Missing exits are partial evidence; scopes are retired on stack reuse, thread
exit or session end. All raw records retain byte extents, origins and SHA-256;
event sequence, invocation/parent, QPC/frequency, UTC, TID, module/RVA and raw
Windows CONTEXT/stack permit review. The Windows CONTEXT blob uses a zero
address sentinel because it is register evidence, not a memory read. It contains
XMM0..15/MXCSR/GPRs; extended XSTATE is not acquired. Only CONTROL is written.

The adapter adapts this project's guarded reference/extra/cell/terrain reader
into `capture_epoch.h`, changing only its writer type and excluding unused census/
run collectors. Original source/hash is cited in that header. Shared
`runtime/beacon-observer/capture.h` and Windows helpers
from `runtime/exp0002`. Existing sources are unchanged. Sibling lifetime/scope
methods informed the design under SOR-P-0002; no sibling code, assembler library,
detour SDK or new third-party implementation is copied. Microsoft SDK/compiler,
Windows debug API and Python stdlib are prerequisites. No downloads occur.

`qualify.py` reads/hash-checks the pinned installed executable and creates one NEW
ignored build directory. It writes a generated header with site hashes, builds
the original adapter/fixtures using installed MSVC/ml64/SDK, and attaches only to
freshly built fixtures. It exercises full acquisition, center-only acquisition,
bad-grid-preimage isolation, zero hits, active-scope retirement and actual writer
failure. Source snapshots, compiler diagnostics, native guard receipt, raw
evidence and independent code-restoration/detach checks stay local. `health_tests`
tests exact disk boundaries/query failure, writer/reader evidence integrity and
raw-open failure; inspector tests cover incomplete/corrupt/cross-thread evidence.
Counts and the 1200-second runner wait are finite qualification safety bounds,
not acquisition quotas. Twelve local health assertions and eleven Python tests
include retained WAL prefixes, torn/corrupt/reordered frames and original controls.

```powershell
& 'C:/Users/User/AppData/Local/Python/pythoncore-3.14-64/python.exe' -B debugger/event-oracle/qualify.py --run NEW-NAME --vcvars 'C:/Program Files/Microsoft Visual Studio/18/Community/VC/Auxiliary/Build/vcvars64.bat'
```

`fixture.asm` reproduces stack/register ABI shapes with unwind metadata and
checks all eight integer nonvolatile registers, XMM6..15 and MXCSR around calls.
`fixture.cpp` supplies original zero/nonzero/nested/overlapping/throwing producers,
an independently literal grid hierarchy and exception handler. It never loads
game code or saves. Failed fixture crash receipts are retained; fixture-only
error dialogs are disabled. Normal cleanup is cooperative release. If a failed
fixture does not exit, the runner may terminate only its original Popen fixture
handle and records that failure; it never terminates a game. An attached debugger
cleanup failure remains a review blocker.

`epoch_writer.h` writes only `evidence/epochs.wal`. Each completed logical raw/
event operation has bytes, metadata and acquisition UTC in one ordered SHA-256
chained frame and calls FlushFileBuffers before returning. No memory-only queue,
background writer or target reads after continuation. This preserves completed-
field prefix durability; an entire boundary is deliberately not buffered for a
later single commit. A partial final frame is uncommitted/recoverable; a corrupt
complete frame is fatal. Hardware power-loss guarantees are not established.

`materialize_epochs.py SOURCE --output NEW_DIRECTORY` validates the WAL and
expands traditional raw/journal files **offline after detachment**. The WAL stays
authoritative and unchanged. Its independent derivative receipt records input
hash/chain/tail and output location. No terminal marker is invented for a partial
stream. Both the qualifier and prospective workflow materialize only after the
adapter exits/detaches. This moves per-field file creation/derived journal writing
out of the stopped interval while keeping required durable writes inside it.

`inspect_events.py` reads these materialized journals/raw files offline and writes only a NEW explicit
`--output`. It verifies extents/hashes/pairing, decodes center/workshop identity and
grid axis/frame fields, and leaves scientific equivalence/frame UNASSESSED.
Incomplete final lines are recoverable; corrupt completed raw sections are
fatal integrity errors. Unreadable optional target fields remain partial.

Acquisition has no arbitrary event/duration/size cap. Failed free-space queries
or caller-available space below 40,000,000,000 bytes on C: or D: stop acquisition.
Writer/integrity/instrument safety failures stop and attempt stopped-state
restoration/detach. STOP requests a debugger break when otherwise idle. Complete
flushed evidence remains readable without a final marker after failure/exit.
`profile.h` measures exclusive QPC buckets for memory APIs, writer path, control,
suspension, disk guard and other stopped handling. Replay delivery is an upper
bound including OS/scheduling/one instruction; unrelated wait includes native
execution. Auxiliary `timing.json` is written after detach, is not scientific
evidence and need not survive a debugger crash. Timing records grow with debug
events; allocation failure follows the same rollback path. Original 0.1.2 and
all six controls are preserved under ignored `.local-work/event-latency/baseline-012/`
with a full byte/hash manifest and sources/helpers to reproduce in a NEW scratch
tree; do not rebuild inside that immutable baseline.

Remaining stopped-time durable I/O imposes latency: review measured qualification
timing before approving the proposed live sequence. A disposable pass does not
establish live event frequency, lack of timing effects, frame equivalence or safe
integration with other tools/mods. No deployment owner changes: Vortex retains
exclusive ownership of any game plugin; this tool has no game-directory payload.
