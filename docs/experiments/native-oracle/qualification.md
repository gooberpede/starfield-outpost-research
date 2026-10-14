# Disposable qualification — SOR-EXP-0031 / SOR-EV-0039

2026-10-11. Engineering evidence only; no fresh Starfield observation. The
[contract](contract.md), [architecture](architecture.md), [schema](schema.md),
[review ledger](review.md) and [executable run card](run-card.md) form one package.

## What was exercised

The original MSVC/MASM fixture has two real five-byte CALL instructions, two
callback table slots and native output buffers. Production patch/relay, callback,
channel, admission, queue and append/flush routines execute inside this disposable
process. No Starfield/SFSE executable is run. Assembly is original project work;
it models the observed ABI, not the entire game function or its scheduling.

The final build's `qualification.txt` records 477 passing assertions. These
include signature refusal before mutation; nonquiescent refusal; thread inventory;
actual rel32 CALL and indirect island execution; expected native returns/output;
all eight nonvolatile GPRs and ten XMM registers; floating-point control and
LastError; unreadable/null identity; C++ and structured exception propagation;
nested and rejected nested callbacks; four concurrent callback producers;
independent channels; stop during an in-flight native call; inert post-stop native
execution; queue exhaustion; concurrent transport without torn records; recursion
overflow; invalid writer handle; disk refusal; actual append/flush/hash equality;
and disposable quiescent original-byte restoration. Zero-capture/rejected scopes
do not become native comparison evidence. Repeated hits have separate invocations.

Seventeen Python inspector tests exercise actual fixture bytes, complete normal
pairing, missing exits/centers, duplicate sequence refusal, corrupt bytes,
truncated records, a partial journal tail, orphan raw bytes, unreadable-vs-zero
identity, exact conditional input replay and a deliberately mismatching native
result. Qualified identity controls directly exercise non-nearest rounding,
subnormal input/product and binary32 overflow. Missing grid-before, abnormal exit
and center-after-grid-before order cannot qualify pairing. Synthetic
READY always labels these outputs SYNTHETIC_QUALIFICATION_ONLY.

The build validates game/SFSE file hashes, generated static guards, protected
inputs before/after, source stability, ZIP CRC/member uniqueness and exact member
bytes. Compiler, assembler, linker and source hashes are retained in build.json;
command files and complete diagnostics are retained beside it. Operational
preflight is separately run against staged inputs, never described as deployed
or live admission. Final review records the actual result.

## Failed iterations retained

Ignored builds qualification-01 through 09 remain intact. Initial failures exposed
a C++ name/header conflict, erroneous object-output syntax, then an actual
non-sole-thread fixture startup. The fixture now waits for transient OS startup
threads to retire and still refuses unless exactly one remains. A later stack
overflow from a large local test queue was corrected by preallocation on the heap.
The expanded ABI probe initially had MASM operand/literal errors. A concurrency
test initially invoked an unpatched fixture callback slot; correcting that
fixture exposed the real wrapper to the concurrent test. No failure was removed
or reclassified as successful evidence. qualification-05's ZIP is unsealed
development output because sources changed during that build; it is not a
deployment candidate. Source-before/source-after equality is now mandatory.

The preliminary independent review required repairs to rejected nested admission,
an inspector unpacking error, grid-before/center/normal-exit association,
subnormal/overflow arithmetic and ASLR-aware vtable guards. These were corrected
and requalified. Original page protection is retained across rollback attempts,
including a failed protection restoration; successful byte restoration alone
does not justify a claim of live teardown.

Final-review-02 was independently rerun (463 assertions/11 tests), but review
found that a perpetually nonempty drain could starve STOP/integrity polling and
that the FP-negative test returned before its advertised branch. Final-review-03
uses a shared production drain/control routine checking disk, STOP and exact
patch integrity before every record. A disposable producer maintains nonempty
backlog while an operator STOP file is created; admission closes before queue
empty and the remaining two events drain. A patch mismatch throws the production
control failure. The expanded inspector tests reach the actual FP/order branches.
Both earlier candidates/logs remain retained, superseded for deployment.

Final-review-04 repeats477/17 with unchanged executable source and corrected
UTF8 documentation/source-pinned README. The independent reviewer also reran
477/17 against final04. Its original disposable artifacts remain in
`.local-work/native-oracle/reviewer-fixture-02/`, including fixture-events.bin,
writer.bin, backlog-control/STOP and synthetic evidence sessions. Independent
stdout/stderr were observed in tool results (native chunk e4a692, inspector
c1a1e8), not saved as separate independent log files. Independent hash and
post-test unchanged-tree/index checks were observed in 82b345/f0cc3f. The
implementer's full build logs remain separately preserved; these are not
mislabelled as reviewer-generated logs. Final artifact ledger pins both sets.

## What remains untested

This cannot prove that installed SFSE reaches sole-thread pre-main Load, that no
other plugin/injector can create a racing thread, that game object lifetime is
stable during reads, that a gameplay action triggers the boundary, or that any
captured object is an ordinary outpost. The startup precondition is deliberately
conditional and fail-closed; a thread snapshot is not a general all-CPU barrier.
Game CFG/CET, SEH propagation under game faults, exact live timing/performance,
real disk exhaustion, failed VirtualProtect rollback and process crashes remain
unexercised in Starfield. No dynamic unhook is implemented or authorized.

Captures may be partial, lossy after a health stop, or never occur. Each accepted
raw/journal pair is independently flushed; a failure can leave a raw tail or
incomplete invocation. A terminal marker is not guaranteed after storage failure.
Queue/depth/IO failure stops admission and retains inert instrumentation until
process exit. Neither target survival nor a complete drain is guaranteed.

Conditional native-input replay tests only the supplied native inputs through
floor and hierarchy selection. Saved-to-loaded frame reconciliation, native
projection intermediates, blinded holdouts, seam/angular/CPU-selected branches
and full durable-position equivalence remain NOT TESTED. The 23 frozen
predictions are unchanged. Safe activation, useful events and scientific
sufficiency are three separate gates.
