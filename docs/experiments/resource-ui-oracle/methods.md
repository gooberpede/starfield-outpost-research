# Acquisition architecture and actual offline qualification

[Answer](report.md), [receipt](capture-contract.md). All native site addresses
use [dataflow's pinned static VA domain](dataflow.md). Proposed interventions
below are future actions, not actions performed by this assignment.

| Method | Decision, concrete mitigation and qualification |
|---|---|
| Existing 070 call observer | Actual historical producer/UI identity records prove this smaller boundary has information value. Its source `runtime/beacon-resource-070/capture.h` is inspected conceptually through the output contract; no binary/source is repurposed here. Would need a new version, established-Workshop identity, branch freshness, catalogue sites, preservation and copy qualification. No automatic deployment or expanded SFSE-header reuse permission. Alternative if debugger control fails, not ready as-is. |
| Old INT3 debugger | NO-GO as-is. Actual SuspendThread denial and queued traps surviving detach in [failure report](../event-latency/thread-control-final-report.md) are not repaired by renaming it. New design below removes software-byte replay, manual suspend loops and detach requirement. Must still independently test hardware trap ownership/continuation and thread lifecycle. |
| New disposable external hardware-stop controller | **Selected, CONDITIONAL-WITH-MITIGATION.** Synchronously stops at natural updater/catalogue instructions; copies small identity lists externally while stopped; stays debug-connected until process exit. No injected borrowed-pointer worker or game-native calls. More timing interference than ordinary observation; no claim of non-invasive capture. |
| New bounded native plugin | Can copy at updater/catalogue sites and keep instrumentation loaded until process exit, relaxing uninstall. Needs ABI/unwind/state preservation, source lifetime and all alias exclusion during copying; small identity copy avoids deep region geometry but not these obligations. Concrete alternative: 070-style synchronous numeric identity copy, preallocated transport, source-backed guard/qualification; no deferred pointer dereference. Larger target crash risk than external guarded reads; second choice. |
| Native one-shot invocation / asynchronous external snapshot | Forced native updater calls can mutate caches and have no qualified arbitrary-call context. Reject invocation; intercept natural calls instead. Uncorrelated snapshots lack call path/freshness; use only a stopped natural instruction and independently validated context, as below. |
| Manual list/video | Supports operator/site registration, cannot supply source-tagged populations. Auxiliary recording only. Repeating C1A's stable IL video cannot pass this brief's information criterion. |

## Selected controller: exact construction trajectory

Implement from original code against installed Windows SDK/Python stdlib ctypes
or installed MSVC/SDK only. No SDK/header implementation is vendored, new library,
download, CommonLib/SFSE dependency or old adapter incorporation is prescribed.
Controller and decoder live outside the game; all raw outputs ignored. First
build a self-owned multithreaded fixture with typed mock resources, the three
vectors, conditional retain/reset paths, node/category calls and selected overlap.
Compile it only under separately specified disposable fixture authority; this
assignment implements the nonnative transport subset instead.

Use the Windows debug-event loop, not a separate `SuspendThread` census. Windows
documents process-thread suspension while a debug event is being handled;
continuation resumes execution. [Microsoft main-loop contract](https://learn.microsoft.com/en-us/windows/win32/debug/writing-the-debugger-s-main-loop).
Use checked external reads with exact returned length;
[ReadProcessMemory](https://learn.microsoft.com/en-us/windows/win32/api/memoryapi/nf-memoryapi-readprocessmemory)
requires read access and fails on inaccessible ranges. These are consulted API
contracts, no Microsoft example code copied. They do not establish safe native
object identity or future debugger correctness.

Controller phases, with a separately built/tested breakpoint manifest:

1. Verify loaded image path/hash/base and exact instruction bytes against pinned
   EXE file sections. Enumerate thread creation/exit debug events from startup;
   assign thread lifetime tokens. Qualify permitted startup/attach handling on
   fixture before retail. Never guess process identity or bypass access denial.
2. Hardware execution break at updater `1421e07d0`; record RCX/RDX/XMM2/XMM3,
   caller return address and originating operation/Workshop witness. Route must
   include established caller `1421b26bc`, not assume preview context equals it.
   Trace that updater's own branch history to normal return, using owned hardware
   execution slots and TF steps; trace nested calls/returns without logging
   every instruction payload. Capture `1421e0bf4` spatial replacement,
   `1421e0d2f` atmosphere replacement and `1421e0e75..0ee3` biome replacement
   paths. At `1421e0bf4`, also copy the actual transfer input via RDX
   (stack-local header at RBP-78) before the helper; tag SPATIAL_REFRESH_PAYLOAD.
   This is newly scanned spatial membership for that descriptor, independently
   of later shared-vector consumers. At `1421e0d2f` RDX similarly identifies
   the atmosphere transfer input. Preserve these as distinct samples.
   A skipped trace or unwind yields UNKNOWN freshness. The qualification
   must cover external callees/exception events and loss; do not force refresh.
3. At updater pre-epilogue `1421e0f04` (R14=S, R13B refresh work), copy the three
   current vectors and resource headers; native branch trace distinguishes which
   replacements completed. Other threads can run between debug events: unless
   conflicting writer exclusion is proven, the return snapshot's ancestry is
   UNKNOWN even if this invocation performed a replacement. The transfer-input
   sample retains its directly witnessed scan provenance. After tracing to
   normal return, seal the event. A
   missing return makes it partial. These lists are the primary spatial probe,
   independently useful even if no catalogue event follows. No source geometry
   is copied and source-generation age remains UNKNOWN.
4. Catalogue phase: stop before call `1415796f7` (RCX category/RDX node), then
   trace that gate invocation. At `1421f6b58` RCX chosen shared header, R14
   resolved property object, frame `RBP-79/-71` produced range. Copy selected
   range plus all three tagged populations and produced identities immediately.
   Trace overlap comparison and return to `1415796fc` for AL; bypasses never
   reach b58 and must have their own path terminal. Preserve category/node→leaf
   mapping via actual `141579fc0` / `14157a740` arguments and return/append paths.
   Failed recipe/organic gates do not become displayed items. Capture category
   rebuild and final constructor events if asserting actual item census; otherwise
   catalogue outcome remains FILTER_RESULT_ONLY.
5. Optional area-UI phase: stop at `1415785c9` and `1415785e8` for actual union
   arguments RDX/R8 and follow selected Water append, constructors and return for
   typed rows. Phase slots are reused only at completed call boundaries. Four
   x64 hardware address slots are a scheduling constraint: use a phase table
   with no more than four active sites/thread and TF tracing within one admitted
   invocation. Missing events during a phase switch are declared UNOBSERVED;
   this is not complete global writer coverage. The required primary oracle does
   not depend on this optional typed-row phase.
6. Serialize into externally owned memory, append framed BEGIN/SAMPLE/END or
   LOSS, flush/close, decode/read back and emit ACK. No external file I/O takes
   a game lock in injected code; the game is nevertheless paused for the copy.
   Resume with documented breakpoint handling only after preserving that stop's
   owned bytes. No native query, cache reset or forced miss is called.
7. Close capture admission when the finite P1/P2 questions are sampled. Leave
   debugger attached through user normal exit, or the exact future-approved
   disposable crash/termination policy. Do not detach/replay/remove software
   traps mid-session. Unknown first-chance exceptions are passed to ordinary OS
   handling, not suppressed; owned TF/hardware exceptions need proven DR6/site/
   thread ownership. DR/TF/RF edits are explicit future register mutations.

The built controller must include initial debug-event ownership, DR state
save/restore policy, TF/RF re-execution handling, all existing/new thread coverage,
per-thread nested calls, unexpected exits and an out-of-process evidence writer
health channel. Sharing debugger slots with another debugger/instrument is FAIL.
There is **no implemented controller or retail ABI qualification** in this tree.

## Risk, test and objective disposition

| Issue | Required mitigation/test before pilot admission | Failure/fallback |
|---|---|---|
| Freed/changed native storage | All-stop event, no resume during copy; OS-guarded reads, exact lengths, type/load-map validation. Fixture races/reset/unmap/reuse and malformed headers must yield explicit INVALID/LOSS, never absence. Validate native owner/caller provenance at the stop; readable stale pages alone insufficient. | Refuse membership attribution; capture scalar failure/context only. For a valid actual per-use IRES observation, trace comparator operands instead of speculative deep walk. No arbitrary pointer chase or target AV. |
| Inter-event ABA/writer gaps | Separate each instant; do not promote digest/header equality to freshness. Test reset-with-same-header/ID, cross-thread updates and retained-cache branches; decoder must leave joins UNKNOWN. | Primary updater source-tagged result remains useful; fresh gate claim withheld. Full writer interval qualification only if later required. |
| Full enumeration too large/slow | Checked budgets and preallocated external buffers; fixture max/overflow/short-read/cold-page tests; qualify chosen limit and pause costs before retail. | LOSS, preserve positive validated subset separately. Increase budget only after offline qualification; no partial-as-empty. |
| Hardware/TF event handling | Multithread fixture: concurrent same-site traps, new/exiting threads, nested calls, unwind, STOP, controller/writer failure. Every admitted event needs one terminal or sticky LOSS. Verify native CPU state except declared debug state unchanged. | No retail admission. Build bounded persistent 070-derived call observer as alternative, with its own source/rights/ABI/copy tests. Not revive abandoned adapter. |
| Exit/retirement | Never detach before process exit; fixture normal exit, post-ACK crash, pre-ACK crash and debugger failure policy. Explicit future kill-on-controller-exit configuration and recovery permissions must be specified/tested, never rely on default. | Pre-ACK crash FAIL acquisition. Post-ACK crash may retain complete evidence. Need safe user-controlled recovery if controller/target stalls; no improvisation. |
| Identity/catalogue relation | Fixture foreign Workshop/node, category bypass, duplicate resource ID/pointer distinctions, failed recipe, unearned variant, delayed rebuild. Native copy must include current Workshop witness, source tags and actual gate branch. | SITE_ONLY/UNKNOWN, not complete native oracle; reconcile offline before another authorized run. |
| Protected saves/disk | Pilot's path/cloud/autosave checks, masters hash unchanged; both drives >=40,000,000,000 caller-available bytes, independent writer/readback ACK. | Abort affected admission, preserve logs. No arbitrary healthy-session time/event quota or operator-delay cutoff. |

Relaxed C1/C1A gates: clean detach/uninstall and post-capture playability are no
longer prerequisites for a separately approved disposable run. Deep region-owner
lease/copy of all points is unnecessary for this small external resource-list
probe. Neither relaxes object validity, correct identity/source attribution,
loss/flush integrity, bounded effects or save protection. Safe retirement still
matters if a design proposes reuse of a surviving process; this one does not.
Historical NO-GO/failures remain unchanged. Crash tolerance grants no present
launch/attach/register/deployment/termination authority.

## Prototype actually executed

[receipt_probe.py](../../../research/resource-ui-oracle/receipt_probe.py) is
original GPL-3.0-or-later stdlib code. It demonstrates bounded eight-byte-member
copying from synthetic ranges, source-tagged qualified fixture identities,
length/sequence/SHA256 framing, explicit terminals/loss rejection, OS fsync and
full readback before ACK, and conservative population interpretation. Eight test
methods include corruption/truncation, gap/duplicate terminal, missing terminal,
budget/short-read, retained and nonspatial cases and wrong context. Exact command,
versions/stdout/exit and result are in [verification](verification.md).

Reads only its own fixture files; exclusively writes a requested fresh directory
under repository `.local-work`, leaves outputs intact, no target/process/config/
save/DB/network access. Prerequisite existing Python stdlib only. This validates
transport/accounting and its own flush path, not retail lifetime/concurrency,
native serialization, OS debugger scheduling, actual outpost joins or UI ancestry.
