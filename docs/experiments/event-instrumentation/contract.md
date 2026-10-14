# Verified sites, acquisition and evidence contracts

SOR-EXP-0025; STATIC/OBSERVED-INTERNAL, REVIEW-REQUIRED. Site hashes/file offsets
are independently obtained from the installed PE, after whole-file SHA-256
`7e9adb1414a8e1b325e5e1f097b9b17b78deb7eebeda37a333351a43a60f9d28`.
Retail 1.16.244.0 only; static VA = 140000000 + RVA, runtime VA = loaded base +
RVA. Offsets below are runtime member/stack offsets, never save-file offsets.
Existing instruction exports `workshop-origin-04.tsv` and `engine-oracle-01.tsv`
in ignored `.local-work/recon/` supply the ABI/control-flow evidence. The generated
`native-sites.json` records original PE file offsets and exact 32-byte hashes.

| Boundary / RVA | Verified first instruction / full length | Acquisition |
|---|---|---|
| Center entry F4AB80 | MOV [RSP+8],RBX / 5 | RCX reference, RDX caller-owned writable XYZ12, original SP and [SP] caller. |
| Center exit F4AC44 | MOV RBX,[RSP+40] / 5 | RBX actual reference, RDI output, original SP=current SP+38; [original SP] caller. Native XYZ12 is valid here on all traced normal branches. |
| Grid entry AD0B90 | MOV [RSP+18],RBX / 5 | RCX six-pointer context, RDX reference, original SP/caller. |
| Grid translated X AD0C93 | VMULSS XMM1,XMM0,XMM4 / 4 | Before multiplication, XMM0.low 32 is the actual translated X; XMM4.low 32 scale; RBX reference, RSI context. |
| Grid translated Y AD0C9C | VMULSS XMM2,XMM0,XMM4 / 4 | XMM0.low 32 is actual translated Y; XMM1.low 32 already scaled X; XMM4 scale. |
| Grid selected result AD0D3B | MOV RAX,[RSI+10] / 4 | RBX reference, RSI context, RBP-49 pretranslation center 12, RBP-9 hierarchy 44, RBP+6F floorXY8. |
| Grid common exit AD0E94 | LEA R11,[RSP+C0] / 8 | Original entry SP=current SP+C8, caller preserved; RAX return in Windows CONTEXT. Both qualified and early-return branches join this exit. |

## Correction to the earlier grid acquisition wording

The earlier EXP0021/24 documents called RBP-49 at AD0D3B “translated XYZ”.
Instruction evidence shows it is **the helper's pretranslation center** at that
boundary: AD0C88/AD0C97 add context X/Y into XMM0 and immediately multiply/floor,
without storing those translated values back. It is overwritten later by
projection at AD0DE5. The new two-axis boundaries preserve actual translated
values; observer-side addition is never labelled a native intermediate. Z is
not translated by this XY quantization segment. Frozen inputs/predictions,
validation protocol and historical captures remain untouched. Their old wording
is retained with linked correction, not silently reinterpreted as a live result.

## Acquisition choice and alternatives

SFSE entry/common-exit near bridges remain technically plausible, but require
dynamic unwind registration, nearby allocations, a proved multi-thread patch
installation phase and lifetime retirement. No approved detour/assembler library
is available. An original assembly bridge would introduce those new mechanisms
for exactly these sites. Return-address replacement would additionally change
unwinding/control-flow protection; it was rejected in favor of a common exit.
The existing DR0 failure history makes a hardware adapter less attractive for
this multi-site experiment, without banning hardware debugging generally.

The chosen adapter executes each complete instruction at its original address
under a qualified software-breakpoint protocol. No instruction relocation or
near-trampoline reachability assumption is needed. Windows debug events suspend
target threads while the adapter records evidence; see
[Microsoft's debugging-events documentation](https://learn.microsoft.com/en-us/windows/win32/debug/debugging-events).
That event stop alone is insufficient while replaying: the adapter explicitly
suspends other live threads, holds newly reported threads, restores the site's
original byte, rewinds owned RIP, sets TF, continues one instruction, verifies
the expected next RIP/owned thread and absence of hardware hits, clears only its
TF, rearms and resumes precisely its suspension increments. Windows CONTROL is
the only context portion written. GPR/vector/MXCSR values are read; target code
runs unchanged in place after replay. The unmodified native unwind metadata and
return stack remain in use. Native calls, saving and gameplay automation do not
exist in the adapter.

The actual all-stop debugger protocol is original code; OS documentation is a
contract source, not proof of qualification. See
[ContinueDebugEvent](https://learn.microsoft.com/en-us/windows/win32/api/debugapi/nf-debugapi-continuedebugevent).
Only owned break-in, site and replay events are handled; ordinary exceptions
are delivered to the target. A fault during replay stops acquisition and rolls
back rather than suppressing it. A pending replay is established before any
collector/writer operation so failure can restore original code and clear TF.
Kernel debug events serialize capture; invocations can nevertheless overlap or
nest, with separate per-TID stacks and monotonically assigned invocation IDs.

Center exit requires the same SP, caller, reference and output pointer as entry.
Skipped scopes, stack reuse/unwind, thread exit and retirement generate unpaired
classifications. A grid boundary must match its callback scope by original
SP=RBP+5F, context and actual reference. A helper invoked from that callback has
its grid invocation as parent. Equal XYZ and nearby timestamps never create a
join. Individual unreadable fields continue as partial evidence. Grid can be
disabled in configuration; failed grid preimages disable the entire grid branch
before patching, leaving verified center acquisition. Failed center preimages
prevent center installation.

## Identity, frames, health and retirement

Guarded copies preserve reference/base headers, XYZ, stored CELL/world, concrete
extra-bc identifier+98/compensation+60 and extra 0x81 where readable. At the same
stopped boundary the inherited terrain collector records manager/body/origin,
active-world/grid/settings roots. This is source-informed reuse of the existing
project collector, including its limited exterior-world support; it does not
call engine lookups or confer native ownership. Pairwise field equality is a
check, not complete lifetime or same-frame proof. Workshop identifier raw bytes
002=`f1517de43e171745`, 003=`0efca066ee4c7b9b` plus ordinary base 002C60E9 and
independent body/frame evidence select the comparison, never output numerics.

Grid additionally preserves source/candidate hierarchies, translation, bounds,
boolean and landscape/body/resolution, scale/one/margin bytes, actual translated
axis registers, native floor and hierarchy. Unknown/opaque handles remain raw.
Selected source world is evidenced by the actual context/source hierarchy and
reference/world roots; a definitive owning source-world object mapping and
saved-to-current-frame join remain live review questions, not inferred IDs.

No event/time/file quota exists. C:/D: caller-available disk queries fail closed
at 40,000,000,000 bytes. Genuine writer/integrity/control failure stops; optional
scientific reads do not. A STOP file induces an OS debugger break if no ordinary
event is pending, restores patched sites at a whole-process debug stop, verifies
original windows and detaches. In-flight native functions then continue with
original code; their absent exit record is partial. No generated bridge remains
to drain or unload. Complete raw files and journal prefixes are independently
flushed; scientific completeness, health and process survival remain separate.

Stopped-time acquisition and synchronous durable I/O can cause visible pauses.
No low-overhead or timing-neutral claim is made. Qualification measures this
cost; first live authorization must explicitly accept it or require a reviewed
asynchronous transport/in-process bridge before deployment.
