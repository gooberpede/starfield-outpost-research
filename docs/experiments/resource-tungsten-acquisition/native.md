# Consumer and diagnostic native contract

Scope is the pinned Starfield.exe 1.16.244.0. Preferred image base is `0x140000000`; table addresses are RVAs. Runtime VAs add the measured module base. Object offsets belong to the named native object. Saved tokens and Workshop identifier bytes are never runtime addresses.

| Site RVA | Native observation and guards |
|---|---|
| `0x021e07d0` | Permanent updater entry. Reference R14, entry RSP, saved return `0x021b6936`, indexed query RDX and spatial state RCX bind the outer invocation. Copy 24 query descriptor bytes and XMM2/XMM3 radius/upper bits. |
| `0x021e1772` / `0x021e174e` | Actual ACCEPT / REJECT, before region advance. RBX is the region, R13 the IRES, R12 resource-slot displacement, RSI closure. Require saved updater frame, callback return `0x021e0a4b`, source ordinal/procgen slot and reference checks. |
| `0x021e0bf4` | Pre-install transfer. Same updater frame/reference/temp-set lineage; copy the vector and each resource prefix before installation/disposal. |
| `0x0079b520` | Diagnostic generation entry: source RCX, origin RDX, converted descriptor R8, owner R9D, stack BIOM/output pointers. |
| `0x0079be20` | Diagnostic ordinary resource call: IRES RDX, DNAM R8, context RCX, mask register/stack, component/family payload and weight bits. |
| `0x0079ff1d` | Diagnostic provider continuation. Stack identity only; no completion certificate or consumer epoch join. |

Point-of-use evidence is the existing [C2B native map](../resource-carinae-source-context/native.md), [observation contract](../resource-geometry-observation/native-contract.md), and [D4 producer map](../resource-selection-context/native.md). The source ledger pins existing instruction exports. No analysis-project symbols/types/comments are changed.

Native identity reads require reference type `0x4a`, ordinary beacon base `0x002c60e9`/type `0x1e`, exterior stored CELL/type `0x49`, BC type/vtable and Workshop bytes `e07e10e02770599b`. These do not alone identify the planet: current manager owner `+0x80` must also equal Archimedes III `0x0005de4c`. Saved-parent equivalence remains UNKNOWN. Tungsten IRES `0x000057c4` requires the main Starfield.esm associated-file identity; Chlorine `0x000057d5` is secondary.

Source selection follows actual occupied procgen slot → source wrapper → resource slot → collection → region ordinal. Copy source key referent `0x70`, manager `0x200`, slot 24 bytes and stable re-reads. Region is `0x30` bytes, bounds XYZ/radius at `+0x0..+0xc`, count/capacity at `+0x18/+0x1c`, points pointer `+0x20`; points are ordered 16-byte XYZ/width values. Zero points, nonfinite values, negative radii/widths and malformed bounds fail useful admission. Maximum is 4096 points, 65536 bytes per read, 1048576 bytes per sample.

Entry descriptor bytes must equal the callback descriptor. Retained Qb is captured separately: indexed descriptor conversion at `0x021e1094..0x021e10fb` may change XYZ. Qb, area query, initial construction query and downstream placement query are distinct. The integrated three diagnostic sites do not witness the initial construction sampler, provider BIOM selection or complete alternate-component traversal. Those remain UNKNOWN; the unchanged full D4 observer retains its historical qualification.

DR0 stays on updater entry. Outside any active updater, DR1–DR3 observe generation diagnostics. While any tracked thread has an active updater, all threads use ACCEPT/REJECT/transfer slots. New threads inherit the current mode. All-stop phase changes set/read back only debugger registers; RF resumes the stopped instruction once. Program registers, floating state and instruction bytes are checked/preserved by the inherited engine. Entering consumer mode invalidates unfinished diagnostic generations and records a generation gap. Nested updater retirement cannot restore generation mode while an outer updater remains active.

Updater bypass/unobserved unwind is conservative: no terminal means no success, and consumer mode may remain armed until pruning/exit/exception. Exceptions invalidate pending chains. Near-simultaneous queued old-phase traps can fail the ownership check and produce fatal LOSS; this scheduling method makes no universal loss-free claim. Slot contention tests retain that outcome rather than guessing a missing edge.

Useful identity requires the same process, thread lifetime, updater token/frame, reference and temp set, ACCEPT geometry/source/binding, and identical resource pointer plus `0x30` prefix at transfer. Distinguishable pointer reuse fails. Identical-byte ABA and complete all-writer lifetime exclusion remain unqualified. No pointer/time/source-key correspondence establishes generation history. Current source/manager snapshots are useful discriminators with generation epoch UNKNOWN.
