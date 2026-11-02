# D5AI owner-context rework

The positive geometry frame is the actual consumed Descriptor joined through
Generating's output address and successful Generated to the resident holder.
Current manager double reads cannot replace that join: equal values permit ABA.
An empty completed scan may retain the *owner/proc context* of an earlier
positive generation only across a complete observed history with no reason
0, 1, 5 or 6 invalidation. Source retirement, Grid clear and source-key erase
(4, 3 and 2) do not by themselves discard that owner-only context. This is not
permission to retain old geometry after those events.

The owner graph needs two enclosing scopes: entire owner installer
`0x140789ce0` (reason 5) and entire true manager reset `0x140788e70` (reason 6).
Existing ProcGen clear reason 0 ends before the true reset's later manager-owner
zero at `0x14078936d`. A hypothetical generation in that interval could otherwise
become an apparently clean anchor for an owner subsequently cleared without
another inner reason 0. An anchor inside *any* active invalidator is rejected.
Whole-scope hazards and sequence/loss history must be joined to the actual scan;
equal raw owner values do not repair invalidation. A fresh empty process with no
positive owner certificate remains INCONCLUSIVE.

## Native writer and alias graph

All addresses are preferred static VAs in pinned build 1.16.244.0, executable
SHA256 `7e9adb1414a8e1b325e5e1f097b9b17b78deb7eebeda37a333351a43a60f9d28`.
The local source rows are listed in `d5ai-owner-context-sources.csv`.

| Receiver and operation | Native evidence | Consequence |
| --- | --- | --- |
| Manager constructor | `0x1407878ef` stores zero qword at manager+0x80 | Initialization cannot have an earlier certificate for this lifetime; replacement requires the existing ProcGen destructor reason 1 boundary. |
| True manager reset | `0x14078936d` stores zero dword at manager+0x80 | Reason 6 spans this late store and nested module resets. |
| Owner setter `0x14078a120` | `0x14078a144` stores incoming EDX; zero-input branch `0x14078a568` stores zero | Both existing direct callers, `0x14078a01c` and `0x14078a0d3`, are inside installer reason 5. |
| Installer comparison | `0x140789d6b..0x140789d76` forms manager+0x80 by +0x84 minus 4 | Comparison read, not an additional field writer. |
| Installer helper alias | `0x14078a06e..0x14078a075` passes manager+0x80 to `0x140478820` | Explicit read/escape inspection below closes this alias; synchronous bracketing alone would not prove absence of asynchronous retention. |
| Other manager aliases | `0x14078acfc`, `0x14078bcad`, `0x14078cf24` form +0x84 then subtract 4 | Owner comparison/read operands. `0x14078bf70` stores through the retained +0x84 pointer, a separate mirror field. |
| Save/load wrapper | `0x1407896d0` reads compatibility inputs and calls `0x1407895a0` at `0x140789837` | No direct deserialization into manager+0x80 in this function. |

The changed nonzero-owner branch calls true reset before the setter
(`0x14078a012`, then `0x14078a01c`). Initial zero owner may install without
reset; full installer still invalidates an older certificate. Same owner and
same component takes false reset `0x140789850` at `0x140789e10`. Changed
component takes true reset before recursive installation. Incoming zero also
resets. Consequently a body A→B→A transition cannot preserve an owner
certificate merely because the final number again equals A.

The helper closure is positive address-use evidence. `0x140478820` saves the
incoming field address in RSI and passes it to `0x140478350`. That function
holds it in RBX (`0x140478373`) and only loads its dword at
`0x14047838b` and `0x1404783ef`. Subsequent calls receive scalar FormID values,
independent stack outputs or resolved objects; the field address is not stored
into any object or supplied to a retaining call. RBX is replaced on every
continuing path by `0x140478445`, `0x14047844a` or `0x140478450`. The guarded
initializer `0x140477bd0` overwrites incoming RCX at `0x140477c03` before any
read or call; its preceding instructions use only stack, globals and independent
registers. It cannot consume the incidental owner-field argument.
Back in `0x140478820`, `0x14047888d` reads `[RSI]` into R8D; the subsequent
`0x140478030` receives that scalar, a stack temporary and an independently
resolved output. The owner-field address neither mutates nor escapes through
this helper chain. This is a statement about this address, not about all helper
side effects or global initialization.

The census starts from the manager method interval and existing direct
references to singleton `0x145fd9c30`, preserving 760 root references and 469
existing function bodies, including 82 in the method interval. The 387 bodies
outside the interval are consumers located by actual singleton references;
unrelated +0x80 stores in them are not classified as manager writers merely by
offset. Allocated task/list/UI/reference objects have distinct receiver origins.
The export also retains root references outside existing function bodies;
it is a census of existing analysis, not proof that the database defines every
possible code path or arbitrary computed reference. These coverage limits must
remain attached to the scoped native writer interpretation.

## Owned controls and limits

`d5ai_owner_native.py` executes the original installer decision/store slices
on owned objects. Eight controls cover changed owner, initial zero owner,
same owner/component, changed component, incoming zero, both legs of owner ABA,
and actual setter zero input. Owned callbacks model the independently traced
reset consequence; nonzero setter services and post-reset continuation are
explicitly skipped. Final-source receipts `owner-native02.json` and
`owner-native03.json` repeat all eight rows. They are not whole-manager or retail
execution and do not prove scheduling or hook correctness.

`d5ai_owner_continuity.py` is a separate owned contract model. Its 13 controls
include the late-zero adverse schedule admitted by inner-clear-only fencing,
rejection with whole-reset fencing, the four context invalidators, three
owner-only retaining retirements, ABA, lost history, unanchored empty state,
and rejection of an anchor inside retirement. The adverse schedule is permitted
by instruction order; this does not claim it was observed in a game process.

Raw native exports remain local and untracked. Export methods independently
rehash the already verified disposable analysis copy before and after each
read-only/no-analysis invocation; no original Ghidra project is opened.

## Do the enclosing scopes poison ordinary new source births?

The ordinary new Landscape construction has a positive path **after** the
installer returns; the new reason 5 does not cover that path. In
`0x14078b030`, installer call `0x14078b3f4` completes before Landscape/Grid
construction call `0x14078b936 → 0x1407847b0`. Those are synchronous calls in
one protected initialization function, not timestamps inferred from different
threads. Initial mode 1 and manager exclusive admission are set earlier at
`0x14078b080..0x14078b091`.

Installer success does invoke module+0x08 at `0x14078a0bc` before its return.
The concrete Landscape table is installed by constructor `0x140787f05`:
`0x144b3df48`, whose +0x08 slot is `0x140784680` (xref
`0x144b3df50`). This target acquires Landscape+0x08 at `0x140784699`, reads
manager owner at `0x1407846a9`, resolves that scalar through `0x14096b8e0`
and stores the resolved owner object at Landscape+0x58 at `0x1407846b4`,
then releases at `0x1407846c0`. It does not allocate or populate a Grid,
directly invoke a source-creation callback, or retain an owner-field address.
ProcGen's +0x08 is the existing no-op `0x1402b56d0`.

Resolver `0x14096b8e0` needs a branch qualification: when the record already
has +0x38, `0x14096b908..0x14096b90f` returns that body directly. Its lazy
branch instead allocates type 0xb6 and invokes virtual+0x1a0 plus
`0x14096e060`; this investigation does not claim those initializers have no
source-related side effects. The normal `0x14078b030` calls this same resolver
with the same owner and create=true at `0x14078b0d3`, before installer call
`0x14078b3f4`. Successful prior body resolution supplies the concrete cached
body fast-path premise for Landscape+0x08. If that earlier resolution fails
and later resolution succeeds inside an enclosing scope, births inside that
scope retain the ordinary hazard refusal. This exceptional branch is not
silently treated as a repairable qualified birth.

The actual Landscape source-preparation module is +0x40, bound by
`0x144b3df88` to thunk `0x140784c30 → 0x140785190`. Completion
`0x14078bc30` dispatches +0x40 at `0x14078bee1` before +0x48 at
`0x14078bf12`; this completion follows ordinary context initialization in
the retained `0x14078af30` call graph: its `0x14078afb3` calls
`0x14078b030`, and its later `0x14078afe0` calls `0x14078bc30`.
`0x140785190` calls synchronous
preparation `0x140784c40` at `0x140785303`; P1's closed capture/creation
graph binds its source constructor callback `0x140785490` and constructor
`0x140982d90`. P1's other two constructor callers are `0x1407862a0`
and `0x140849670`; these are distinct source-preparation/file paths, not
the Landscape owner-resolution +0x08 operation.

This establishes a concrete ordinary source-family birth/publication path
outside the whole installer fence. It does not assert that no unrelated
thread can create any source while the global hazard is active. Such an
overlapping birth remains conservatively unqualified. Likewise a reset drain
may finish earlier queued work while reason 6 is active; it does not make that
old allocation a post-reset certificate. The true-reset release/clear graph
and subsequent fresh initialization remain separate. No newly valid source
birth is assumed to survive a reset merely because its constructor ran.

No source-lifetime rule is relaxed to admit a birth inside reasons 5/6.
If an actual capture has only such births, later selections of those same
allocations remain INCONCLUSIVE; future queries alone cannot repair their
births. A fresh qualifying allocation outside the enclosing scopes is required.
The static path above makes that a supported ordinary initialization path,
not a guarantee for every gameplay schedule or an instruction to force travel.
