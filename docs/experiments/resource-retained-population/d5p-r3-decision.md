# D5P-R3 pre-implementation Grid and membership decision

2026-10-29, Australia/Sydney. The [invoked brief](../../implementation-briefs/README.md#archive-lookup) (`implementation-briefs.zip :: docs/implementation-briefs/CODEX_BRIEF_SOR_RG2_D5P_R3_grid_membership_context_validation_repair.md`)
freezes R3-AC1–R3-AC9 unchanged. Written before any production validation edit.
The task starts at HEAD `513461a89a5e4958e9dc6f30f97f7e50be5141f0` with only
the supplied brief untracked. No retail, deployment or save action is authorized.

**Decision: qualify the existing validator and a disposable counterfactual before
choosing a production repair. Do not replace 256 with 512.** A dynamic native
array is supported; a universal 512-member representation is not. Safe acquisition
and complete membership are different claims. No production change is selected
until backing-storage and concurrent-publication guarantees can be justified.

## Native representation and ownership

All addresses here are preferred static VAs for installed Starfield 1.16.244.0,
image base `0x140000000`, executable SHA-256
`7e9adb1414a8e1b325e5e1f097b9b17b78deb7eebeda37a333351a43a60f9d28`.
The installed executable, ESM, PlanetData and SFSE pins were freshly matched.
Existing exports and R2 primary receipts were authenticated. Fresh Ghidra
`-readOnly -noanalysis` output is local at
`.local-work/d5p-r3/investigation01/native.tsv`; database files hashed before and
after are equal. The [source ledger](d5p-r3-sources.csv) binds exact identities.

| Property | Direct static evidence and remaining uncertainty |
|---|---|
| Ordinary Grid array | `0x140986824` loads u32 count at Grid+`0x10`; `0x14098682f` loads storage at +`0x18`; +`0x14` supplies the capacity operand at `0x14098315f`. Pointer elements have stride eight bytes. |
| Dynamic growth | `0x14098316c` calls `0x1422cc0d0` with stride eight. The helper increments count, possibly invoking allocator virtual methods; `0x14098317e` subsequently stores the source pointer. No universal 512 ceiling is established. |
| Native synchronization | Acquire/dedup locks Grid+`0x5c` at `0x140982dc1`, scans, may allocate a `0x1a0` source, appends and releases. A before/after zero lock sample is not yet a proved coherent snapshot protocol. |
| Retained Grid | Provider `0x14079f8fd` stores Grid at W+`0x100`; `0x14079f912` increments Grid+`0x8`. Object retention does not establish backing-array immutability. |
| Retirement | Clear `0x1409829b0` traverses sources, erases under ProcGen protection, frees sources and storage, then clears array metadata. Existing entry fences conservatively invalidate overlapping observations. |
| Allocation extent | Count/capacity are native array metadata. They are not independent allocator receipts. Readability of a virtual page does not establish that all its bytes belong to this array. A corrupted but readable alias remains a concrete adversarial case. |

## Competing routes

| Route | Decision before production coding |
|---|---|
| Native direct lookup | Do not add a CALL. Acquire/dedup mutates and locks; spatial lookup `0x140985870` returns a spatial cell, not a pointer-membership answer. The inspected virtual collector scans and appends to caller storage. ABI-correct invocation alone would not make these safe observers. |
| Traverse actual count | Test as a disposable counterfactual. It can cross 256, but O(n) work follows untrusted u32 metadata. Native capacity and page readability alone do not establish allocation ownership or consistency. No huge replacement ceiling is justified. |
| Header/lock rereads | Plausible refinement, not disproved. It needs lock-bit/acquire-release semantics, coverage of member-array writers and publication windows, an independent storage boundary, and an explicit incomplete result. Equal samples cannot generally exclude intervening ABA. |
| Consumer cursor witness | Provider obtains a spatial cell, materializes an iteration container through virtual +`0x10`, then selects source. This may support invocation-selected provenance with less scanning. It does not automatically prove complete ordinary-Grid membership; container representation, ownership and mutation must be validated and schema meaning changed explicitly. |
| Finite fallback | Keep the old bound as an explicit known limitation until a justified replacement exists. A new fixed bound needs a native envelope, not the observed capacity of one session. A time/read budget could yield incomplete acquisition; it cannot turn a truncated scan into absence. |

## Downstream order and recorder interaction

The production order remains type, count/capacity, count <= capacity, observer
coverage, member-pointer read, each member-slot read, membership, retained/current
Grid read/equality, then lifetime. Earlier read/type/manager predicates precede
this chain. Reason 24 makes all subsequent operands unavailable in R2. Reasons
21, 22, 25, 26 and 23 must be independently exercised rather than assumed good.
Manager reset, Grid clear, source retirement, destruction, map erase and recorder
loss conservatively advance the existing observer epoch; these are observer
tokens, not native allocator generations or complete writer coverage.

The qualification may generate an ignored header differing only by removal of
the count-256 predicate. It is an explicitly unsafe counterfactual, never a DLL
candidate or changed production contract. Preserve original schema-2 records,
eleven hooks, queue, losses and readers. Compare timing distributions and record
volume; mean or maximum observed time is not a universal latency guarantee.
No filesystem work is added inside hooks. Do not package a retail candidate if
allocation/consistency or downstream gates remain unqualified.
