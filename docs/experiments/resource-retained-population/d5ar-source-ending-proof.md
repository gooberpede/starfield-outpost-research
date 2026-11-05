# D5AR source-ending history and diagnostic admission

2026-11-05, Australia/Sydney. Static design proof with historical acceptance
requirements. The [final implementation and controls](d5ar-lifetime-admission.md)
qualify its stated scope. Preferred static VAs refer only to EXE
SHA-256 `7e9adb1414a8e1b325e5e1f097b9b17b78deb7eebeda37a333351a43a60f9d28`,
image base `0x140000000`. This record authorizes no live operation.

**A current ProcGen map reader alone does not establish source allocation
validity.** The geometry reader protects the represented map and nested geometry.
Source operands require a separate source-ending history and copy exclusion.
The proposed repair observes existing pre-free operands, retains permanent
retired-address tombstones and serializes diagnostics with that marking.
It does not acquire an engine source lease or observe generation/birth.

## Actual source endings

The completed [P1 source-rooted closure](d5ab-p1-source-identity-lifetime.md),
L01–L21, supplies the bounded ordinary allocation/alias/destruction graph.
Constructor `0x140982d90` deduplicates or allocates a new `0x1a0` source,
initializes its fields and publishes it into the Grid source vector. The three
ordinary constructor callers and all cell/cursor/file/auxiliary getter escapes
are accounted for. Cells and GridFillFile objects hold raw source pointers;
their destructors free separately identified receivers, not the source base.
Constructor EH and the ten separately parent-bound free funclets do not add a
source-free path (P1 L04/L17). This is receiver-rooted coverage, not a claim that
every `0x1a0` allocation in the executable has this type.

| Ending | Exact original pre-free operands | Existing primary evidence |
| --- | --- | --- |
| Grid clear `0x1409829b0` | `0x140982af0` sets EDX=`0x1a0`; `0x140982af5` sets RCX=RBP; CALL `0x140982af8` targets `0x14365cdb0`. | `.local-work/d5ab/p1-export01/native.tsv`, lines 856–970; P1 L07. |
| Standalone retirement `0x140982b70` | `0x140982c2a` sets EDX=`0x1a0`; `0x140982c2f` sets RCX=RSI; CALL `0x140982c32` targets `0x14365cdb0`. | Same export, lines 763–814; P1 L08. |

Both bodies erase the source's pointer-map entry under current ProcGen exclusive
protection and release that protection before this free. The existing source
lifetime controls execute actual erase/release/free ordering against owned
objects, with logging frees retaining Python backing; they are not retail runs.
New relays must preserve each original CALL return address, all live operands,
flags/SIMD and exception behavior, and tail-forward the unchanged native target.
The observer reads only the existing RCX address operand at these sites.

## Why the earlier simpler argument was withdrawn

Provider `0x14079f860` retains a Grid, obtains a cell and enumerates raw source
pointers before its ProcGen reader/writer admission. P1 demonstrates that Grid
retention is not a source lease. A completed retirement can therefore precede
a later reader; exclusion of future erasure does not establish an earlier
selection-to-publication interval. No actual unsafe retail schedule is asserted
solely from this partial order.

An initially promising universal pre-shift drain was rejected by exact interface
binding. Original `0x14078c190` completes all module `+0x50` callbacks before any
module `+0x58` callback. But actual ContentManager constructor
`0x1407b1ff0` puts table `0x144b404f8` at base `+0xa0`
(`0x1407b2079/0x1407b2080`), and manager constructor appends that adjusted pointer
to its module vector (`0x14078880a..0x14078881d`). Its `+0x50` is a no-op;
`+0x58` reaches ordinary demand via `0x1407b1fe0`. The real site wait
`0x1407b2340` is `+0x10`, the reset callback, not the shift callback. The
provisional use of table `0x144b404b8`, which belongs to another subobject at
base`+0x38`, was a wrong-table-base interpretation and is withdrawn.

Landscape `+0x50` (`0x140785610`) only updates file-origin fields;
actual Grid shift/retirement occurs at `+0x58` (`0x1407856b0`). Other registered
candidate `0x140797dc0` tails to `0x140797e90`; its valid zero-count branch
`0x140797eba -> 0x140797ebc -> 0x140797fd8` performs no generation-site wait.
Thus that callback cannot supply a universal drain. Exact constructor, reset
and tail bodies are in fresh read-only/no-analysis exports
`content-module-ctor01`, `content-shift-drain01` and `module-shift-clear01`
under `.local-work/d5ar`. Existing pinned manager census and D5V exports bind
the module registration and direct reset wait. Successful reset-site draining
remains a positive result; it is not transferred to shift by callback name.

## Positive reset/body ordering

The rejected shift-table inference must not obscure the real reset drain. True
reset `0x140788e70` acquires manager exclusive protection at `0x140788e95`, then
iterates every registered module's `+0x10` callback at `0x140788f1d`. The actual
ContentManager callback is therefore `0x1407b2340`, which waits the same site as
Density and its registered continuation nodes. This occurs before descriptor
zeroing at `0x140788ff0` and the late body-zero write `0x14078936d`. False reset
`0x140789850` likewise acquires exclusive protection at `0x140789875`, calls all
module `+0x10` callbacks at `0x1407898fd`, then clears descriptors at
`0x140789954`.

B030 holds its outer manager exclusive admission (`0x14078b080`) before invoking
installer `0x140789ce0` at `0x14078b3f4`. A changed existing nonzero body takes
true reset at `0x14078a012` before body setter `0x14078a01c`; a same-body changed
component takes true reset at `0x140789feb` and recursively installs; the
same-body/same-component route takes false reset at `0x140789e10`. Thus an already
registered Density job admitted in the earlier pre-drain/acquisition gap is
caught by the inner reset drain while the manager remains exclusively held.
This is stronger than relying only on B030's earlier `0x14078f0b0` call.

The zero-old-body branch at `0x14078a009/0x14078a00b` does not itself reset. Its
valid initial/previously drained zero-body invariant and refusal of failed
installation state remain necessary; the two actual nonzero body-setter calls
are within this installer. Independent review must join site-count lifetime,
late continuation registration and ordinary ingress admission before promoting
this into a complete historical body/descriptor certificate. A claim about the
normal successful path does not give a failed/exceptional installation a new
qualified population. Source-ending history remains separately necessary for
ordinary shifts and permanently recycled addresses.

## Proposed observer-owned exclusion

The proof needs all of the following concrete properties of the final method:

1. Start the history before any ordinary source allocation reachable by the
   supported fresh-process manager. Pin the complete installation transaction
   and strict pre-owner/startup admission. Singleton-null equality by itself
   must not be used as proof that an earlier manager/source history never
   existed. A hot load or inherited pre-instrumentation source is unqualified.
   The subsequent [pinned SFSE preload proof](d5ar-preload-history.md) supplies
   actual installed-binary phase-0 invocation before the original EXE
   `_initterm_e`. Its supported fresh-process profile, earlier-plugin exclusions
   and strict native admission remain part of this premise.
2. Before forwarding either source-free CALL, acquire an observer-owned
   exclusive gate, permanently mark its RCX address, then release the gate.
   Do not dereference the source, call an engine function or hold the gate
   across the native free. No tombstone is ever cleared on address reuse.
3. Acquire that same gate in shared mode before checking the history or reading
   any source diagnostic. Refuse a retired address or sticky history failure.
   Keep shared exclusion through all selected geography, origin, descriptor and
   visited-token reads, then release it on every normal/exceptional exit.
4. Any failed mark, missing admission, recursion/overflow, lost ending or
   capacity/recorder failure permanently disables source qualification. Preserve
   explicit failure/unknown diagnostic statuses and healthy owned geometry.
   Never manufacture zeros or treat an unrecorded ending as a live allocation.
5. Bind admission to the exact independently reviewed producer/source lock and
   actual gate result. A caller-provided boolean or unchanged before/after
   manager pointer cannot replace this method proof.

If diagnostics obtain the shared gate first, an ending cannot mark or forward
free until copying finishes. If the ending obtains the exclusive gate first,
the reader sees the permanent mark and refuses before dereference. An ending
that has already released the gate but not yet forwarded free is also refused.
An address reused after actual free remains refused permanently. These cases
do not rely on numeric pointer equality as an allocation-generation token.
The source's reviewed immutable fields then support copying during the admitted
interval; mutable visited-token bytes remain diagnostic and not a source key.

The observer gate never waits for an engine lock while held. The ending path
marks and releases before any native free/cleanup continuation. The diagnostic
path performs only bounded checked reads into preallocated owned memory while
holding its shared gate. In particular it must not release a native object,
dispatch a task, generate/query resources or perform disk I/O inside this gate.
There is therefore no new observer-gate-to-engine-lock edge to close a cycle
with a native caller's pre-existing engine locks. Recursion and exceptional
exit were separate implementation controls, covered in the final record.

Permanent address refusal is deliberately conservative. Reused allocations can
lose source qualification even when their new geometry is healthy. Exhaustion
cannot be hidden by eviction or a guessed fresh birth. This is a coverage limit
to disclose in the pilot/study cards, not permission to stop at a timer or to
count an inconclusive record toward a scientifically qualified healthy quota.

## Acceptance boundary

The owner/ProcGen phase repair and actual reader still govern body and geometry.
This source-ending repair supplies only the additional allocation/copy premise;
the native planar writer theorem, ordinary zero-rebase scope and effective-input
equivalence remain separately reviewable. Required adverse controls include both
actual ending sites, foreign free blocked by an active copy, mark-before-free,
late publication of a marked key, same-address reuse, nested/exceptional cleanup,
history failure/exhaustion and unchanged geometry fallback. The final exact
source lock, controls and scoped admission are in the
[lifetime record](d5ar-lifetime-admission.md). Source diagnostic admission does
not close the original effective-input gate or AC05.
