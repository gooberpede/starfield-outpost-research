# Natural grid callback and CALL-boundary observation

SOR-EXP-0031. STATIC / PROPOSED-INTEGRATION, not a supported game interface.
The installed retail1.16.244.0 executable was independently rehashed to
`7e9adb1414a8e1b325e5e1f097b9b17b78deb7eebeda37a333351a43a60f9d28`.
Static VA=140000000+RVA; runtime VA=actual loaded base+RVA. PE file offsets below
are a different domain. Existing SOR-S-0127/0132 native/project provenance applies.

| Boundary | Exact contract and evidence |
|---|---|
| Callback vtable RVA4B916F0/4B916F8 | Two aligned pointer slots originally target AD8EC0; constructor/destructor slot4B916E8 targets31A630. Thunk dereferences RDX reference slot and RCX+8 context then tail-jumps AD0B90. Existing engine-oracle-02.tsv lines6–16/44–46. |
| Center CALL RVAAD0C36, fileAD0236 | Complete E8 rel32 to F4AB80; RCX actual reference, RDX writable caller-owned XYZ12. Capture after natural call. Existing engine-oracle-01.tsv lines32–43; workshop-origin-04 helper instructions. |
| Grid CALL RVAAD0D36, fileAD0336 | Complete E8 rel32 to96F5C0; RCX landscape, RDX writable native hierarchy44, R8 signed floorXY8; no consumed stack arguments. Capture input before and result after natural call. engine-oracle-01.tsv lines92–104 and selector instructions323–594. |

The independent specialist rechecked both installed PE call targets/bytes and
static contracts. Postcallback sampling alone fails: center RBP-49 is overwritten
by projection atAD0DE5; floors RBP+6F are overwritten by96F940 atAD0E20. Selected
hierarchy RBP-9 expires with the callback. Context+08 candidate and+18 source are
inputs, not a substitute for selected native output. This is the decisive reason
for two CALL wrappers in addition to the callback scope.

Alternatives considered: passive shared output cannot establish freshness;
vtable-only observation cannot expose the private selected result; arbitrary
entry/internal jumps require stolen-instruction relocation/unwind engineering;
return-address rewriting changes return/unwind protection; the external debugger
remains abandoned and was not executed or adapted. No assembler/detour dependency
was incorporated. Original project readers/Win32 hash utilities are reused with
their prior maintainer-informed provenance.

The two near islands contain only FF25 indirect tail jumps to compiled wrappers.
The CALL's complete five bytes are replaced with another CALL; no game instruction
is stolen or replayed, and no RIP-relative operand is relocated. RAX is forwarded;
known native consumers overwrite unused volatile return/flag/vector state.
Integer/pointer arguments and all nonvolatile GPR/XMM state follow the
[Windows x64 ABI](https://learn.microsoft.com/en-us/cpp/build/x64-calling-convention?view=msvc-170).
Compiler-generated unwind information covers wrappers; the relay is a stack-neutral
leaf. Native C++ and SEH faults propagate. A `__finally` reports abnormal completion
and releases the scope even for SEH. No native fault is suppressed. FP state and
LastError are saved around observer work; volatile registers, flags and upper
YMM lanes are not promised unchanged across a complete native CALL.

## Installation and lifetime boundary

Patch only synchronously during SFSE Load, before starting the observer worker,
after all file/code/signature guards and an actual sole-process-thread gate.
Pinned [SFSE source](https://github.com/ianpatt/sfse/blob/48535cc4306ab345252bf740c20a1c6194929b0e/sfse/sfse.cpp)
places normal Load in the CRT command-line hook before WinMain. This source report
is not proof of installed-binary semantics or a guarantee about other plugins.
The separate sole-thread test is mandatory. Startup can wait up to120 seconds
for background startup threads to retire, with disk checks; it then refuses all
edits if another thread remains. This is a bounded startup admission wait, not an
event collection quota or a patch retry. Disposable workers retired after about
30 seconds; Starfield applicability is NOT TESTED. No thread suspension, exception
replay, retry under a weaker gate or concurrent code patch is permitted.

The approved profile must exclude other SFSE plugins/injectors and concurrent
external thread creation. Snapshot checks alone are not an unconditional all-CPU
synchronization proof. An unexpected persistent startup thread means NOT_READY,
not permission to suspend it. Preimages are all checked before writing. Each write
restores page protection and flushes instruction cache, under the
[VirtualProtect contract](https://learn.microsoft.com/en-us/windows/win32/api/memoryapi/nf-memoryapi-virtualprotect).
Failure attempts rollback only in this same quiescent startup phase. Any potentially
remaining edit forces DLL residency and NOT_READY; no live recovery is promised.
ASLR vtable guards compare actual pointers to loaded-base-relative targets rather
than incorrectly hashing relocated pointer bytes against disk.

STOP atomically closes admission; existing scopes finish and the queue drains.
Rejected nested scopes suppress observation so they cannot inherit an outer ID.
No runtime unpatch or DLL unload occurs. Code/islands/buffers remain resident and
inert until normal process exit. Removal is user-managed Vortex work after exit.
An original call that never returns can prevent a drained marker; do not force
unhook, terminate the game or promise recovery. This differs from clean capture
retirement and is reported separately.

## Capture and reachability

Callback entry owns a TLS invocation and actual reference/context; each native
center and grid event carries that invocation, parent, thread and raw source fields.
Unknown identity remains unknown. Reads use bounded ReadProcessMemory without
engine lookup/census calls. Extra chains have a64-node safety bound and cycle flags;
incomplete identity prevents comparison, not native execution. Repeated reference
headers detect some races without claiming ownership, atomicity or source-world
authority. The queue has4096 preallocated17,768-byte slots (about69.4 MiB), plus
per-thread fixed scope/grid scratch. Saturation/lost records stop capture and are
explicit health failures. No explicit allocation, file I/O or locks in hooks;
OS/CRT TLS initialization and Win32 reads still affect timing.

Grid and center collection are independently selectable at reviewed startup,
with both enabled in the proposed package/card. A center-only configuration
cannot fulfill the grid objective. Derived translated XY is computed only offline
and is labelled DERIVED; there is no captured translated-register claim.

Static chain77E350→AD92E0→AD08D0→B1E190→AD8EC0→AD0B90 supports terrain/site
candidate processing as a plausible opportunity. Matching hierarchy/overlay and
landscape gates precede reference enumeration; ordinary activator/Workshop-keyword
gates precede center/grid. Existing `static-exhaustion-04.tsv`1115 onward and
`engine-oracle-02.tsv`/04 xrefs document these edges. Arrival/terrain processing
is plausible; opening build mode alone is unproven. Distinguish no callback,
early callback, center-only invocation, grid input without return, complete grid,
unreadable identity and qualified comparison. A no-hit run cannot falsify arithmetic.
