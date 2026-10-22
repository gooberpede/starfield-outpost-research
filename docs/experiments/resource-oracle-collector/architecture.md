# Architecture and native-to-synthetic boundary

[Report](report.md), [owned source](../../../research/resource-oracle-collector/fixture.h).
This is an independently implemented controller using installed Windows APIs.
The existing [C1B contract](../resource-ui-oracle/capture-contract.md) and unchanged
[receipt prototype](../../../research/resource-ui-oracle/receipt_probe.py) supply
the conceptual copy/transport method and actual framing/fsync/readback functions
under SOR-P-0002, source HEAD `fd673b5dd9a940f60136eb1a667bd191086d75a4`.
[Exact input pins](sources.csv) distinguish inherited research from new code.

| Retail motivation, inherited STATIC only | Implemented synthetic analogue |
|---|---|
| Three operation vector headers, spatial/ATMO/raw BIOM | Evaluation has three begin/end/capacity u64 headers; target-local ordered resource pointers. Source tags come from fixed synthetic ABI positions. |
| Resource identity/type read | Own Resource has u32 id/type at offsets0/4, size8. These are fixture IDs, never game FormIDs or retail +28/+2e headers. |
| Spatial replacement versus retention path | Separate naturally executed exported refresh/retained instructions; branch operand copied independently. Refresh initializes the fixture lists; retained copies unchanged storage again. No claim of retail branch-trace implementation. |
| Catalogue builder `FUN_1415795f0` to gate `FUN_1421f68f0` | Own filter computes membership in selected population and stores selector/produced/result before a natural decision boundary. Distinguishing spatial/ATMO/BIOM positives and cross-population negative. No row construction or placement analogue claimed. |
| Nested/repeated callbacks and workers | Decision called inside refresh frame, with stack-return witness in refresh's RVA range; further recursive decisions and repeated visits, three independently instrumented workers. No generic unwinder or retail invocation stack supplied. |
| Native identity/freshness/geometry | Only synthetic magic/visit/thread lifetime and witnessed synthetic site are bound. Cross-event epoch ancestry, native geometry and retail identities remain UNKNOWN. |

Hardware execution breakpoints were selected over software byte patches, a new
injected plugin, forced native calls or asynchronous snapshots. They give a small
implementation and inspectable stop ownership without instruction modification
or borrowed-pointer workers. Three sites fit three slots; retail phase scheduling
and all relevant writers do not yet fit this demonstrated model. No fallback
architecture was required. Debugging pauses execution and changes declared debug
register/control state; this is an intervention.

## Process and breakpoint lifecycle

The launcher checks its requested target against the build manifest's exact
sibling `sor-c1c-target.exe`, with no attach/PID option. The controller separately
hashes that sibling, parses its export RVAs, and creates it with
DEBUG_ONLY_THIS_PROCESS. At CREATE_PROCESS it verifies actual image path/hash,
measures the runtime module base and compares 16 instruction bytes at every site
against a nonexecuting LOAD_LIBRARY_AS_IMAGE_RESOURCE mapping of that exact PE.
Nothing is injected or called in the target. File resource mapping is local to
the controller and does not execute the target entry point.

CREATE_PROCESS/CREATE_THREAD debug events install DR0–DR2 execution sites before
continuation. Enabled pre-existing slots or TF are refused. Thread IDs have
monotonic lifetime tokens and per-thread capture sequences; exits retire tokens.
No separate SuspendThread census or manual resume count is used. Windows debug
events hold target threads while each foreign copy and external ACK completes.
The initial system breakpoint is consumed once; subsequent unrelated exceptions
are passed as DBG_EXCEPTION_NOT_HANDLED, including both chances of the deliberate
target exception. A hardware trap must match PID, known lifetime, RIP, exactly
one owned DR6 bit, programmed DR addresses/DR7 and instruction bytes.

After verified ACK, clear owned DR6 status and set RF for one instruction's
execution while keeping slots armed. No TF stepping or instruction replay occurs.
GetThreadContext immediately verifies general registers, RSP/RIP, floating-point
save data and MXCSR unchanged. Meaningful EFLAGS and DR7 bits must match too.
Raw context and raw requested/readback control values remain inspectable.
Observed Windows context sanitization changes fixed EFLAGS bit1 and DR7 bit10;
these two bits and declared RF are excluded from semantic state comparison.
Earlier overstrict comparison failures are preserved in smoke02/03. This is not
an AVX/XSTATE-preservation qualification or permission to edit game registers.

The controller stays connected through process exit, calls
DebugSetProcessKillOnExit(TRUE), and never detaches. STOP, rejected ACK, EOF or
event bound disposes only its own created fixture. Fatal controller errors also
terminate that fixture; earlier ACKs remain independently usable but missing
terminal accounting fails the session. Other processes are never selected.

## Copy bounds and durability

At each stop RCX supplies an actual foreign Evaluation pointer; exact
ReadProcessMemory reads copy its136 bytes and the real stack return address.
Each list validates u64 ordering, alignment, nonnull nonempty range, count and
capacity before reading. Limits: 4096 pointers/capacity per list, 65536 bytes per
individual read, 262144 bytes per stop, 1MiB serialized frame, 256 fixture captures.
The stopped-copy budget is 2000ms measured with GetTickCount64 (coarse, not a
microbenchmark); the writer's fixture-only 30s no-output watchdog catches a stuck
deterministic worker. These synthetic engineering bounds grant no retail time,
event or operator-delay cutoff. Both drives retain the 40,000,000,000-byte guard.

Exact reads copy pointer-array bytes and pointed-to Resource records while
stopped. A partial/unreadable record, invalid type/header or exceeded budget is
INCOMPLETE, with members=null and a reason. Only a complete zero-count initialized
header produces members=[]. No clamp, positive-prefix-as-complete or failed-as-empty
path exists. All copied values are independent bytes before resumption. All-stop
quiescence supports that instant, not object validity across retail writers/ABA.

`collect.py` computes each complete list's payload SHA256 over raw pointer bytes
followed by ordered raw resource records. It extends `sor-resource-oracle/1` as
`sor-resource-oracle/1+c1c-synthetic-1`; unimplemented retail fields are not
fabricated. The unchanged C1B SRO1 frame/sequence/length/SHA256 format persists a
SESSION, SAMPLE and END for each stop with exclusive create, flush, os.fsync,
close, full readback and digest validation. The ACK file is fsynced and reread;
only then does the wrapper send numbered ACK to the stopped controller. Per-stop
files preserve usable earlier groups even if a later group fails. Session result
requires consistent final capture/ACK accounting and no sticky loss. An ACK of
INCOMPLETE data confirms durable diagnostics, not acquisition success.

Native records, oracle expectations and interpretations stay separate: only
qualify.py knows the independent expected table. It never passes that table to
the collector. A failed durability acknowledgement can leave intact bytes on
disk; it still fails acquisition until independently recovered/reviewed. OS-flush
and readback do not prove power-loss immunity or storage-controller durability.
