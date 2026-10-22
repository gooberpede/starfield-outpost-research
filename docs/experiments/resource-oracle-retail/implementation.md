# Retail adapter and source-to-code correspondence

2026-10-22 Australia/Sydney. [Authority/card](run-card.md), [outcome](report.md).
Original/owned code is GPL-3.0-or-later; Bethesda native material is evidence,
not licensed project implementation. No new dependency, third-party source,
installation, upstream communication or publication.

The separate [controller](../../../research/resource-oracle-retail/controller.cpp)
adapts C1C's Windows debug-event/DR/RF/ReadProcessMemory engine from repository
HEAD60ce35a26d7215b50f7671e1ee9ef06724d491f4. The original C1C controller,
fixture ABI and nineteen qualification cases remain unchanged. Retail code does
not decode the synthetic Evaluation magic or eight-byte Resource structure.
The separate fixture build cannot accept the retail launch argument.

| Native evidence (preferred static VAs, base140000000) | Implemented observation and scope |
|---|---|
| C1B ui15 1421b2592–26bc | RSI=operation, R14=resolved Workshop reference, RCX=O+520, RDX=O+338 descriptor. Require shared O=relocated145f5d2e0. This is BEFORE refresh; shared population site ancestry remains UNKNOWN. |
| ui15 updater prologue1421e07d0–0808, transfer1421e0bed–bf4 | R14=S, R13=descriptor; current native return at RBP+38 must equal relocated1421b6936 (actual alternate caller independently mapped in ui15). Saved caller R14 at RBP+18 supplies current resolved reference. Copy RDX's native24-byte transfer header. Only this payload receives BOUND_TRANSFER ancestry. |
| C1B ui10/bm0011421f6b58, filter prologue | Selected header RCX; produced native header RBP−79. Recover caller return at RBP+5f and original grid node from saved caller RDI at RBP+47. Require return1415796fc; match later event by lifetime, RSP=RBP+67 and node. No last-event/time pairing. |
| bm0011415796fc | Observe AL before MOVZX EBX,AL. This is resource-filter result only, before organic/recipe/append/placement. Gate site identity stays UNKNOWN. Bypass/other-caller events are not invented overlap observations. |
| [Output contract](../native-availability-map/output-contract.md) | Three24-byte begin/end/capacity headers at O+520/+538/+550;8-byte member pointers;0x30-byte native resource headers with FormID+28/type+2e=9f. All counts/reads checked; failed/truncated/budgeted groups have members=null, never empty. |
| [Workshop persistence](../workshop-origin-beacon-relocation-persistence.md), existing beacon-observer/native-oracle050 readers | Reference type4a, base002c60e9/type1e, reference+c8→extra head+8; next+8/type+12, concrete BC vtable relocated144c24e60, extenta0, saved identifier+98. P3 raw bytes c3a5866f4cfcf585 bind context independently of saved-token remapping. Cycle/64-node integrity bounds fail closed. |

BC binding is scoped modern saved/runtime correspondence, not universal UUID
uniqueness or complete active-player membership. Resource FormIDs alone remain numeric. The final per-resource associated-file decoder supplies the narrow IL/Cu qualification below; installed/configuration hashes alone do not prove a full runtime load map or effective overrides.

Windows attachment emits initial process/thread events; all returned thread
lifetimes receive four guarded execution sites. Existing DR state/TF is refused.
Traps must match exactly one owned DR6 slot, runtime RIP, programmed DR addresses
and DR7, and unchanged16-byte instructions. Owned resume clears DR6 and sets RF;
general/floating state and meaningful control bits are checked against readback.
This does not qualify full AVX/XSTATE preservation or every scheduler interleaving.

The [writer](../../../research/resource-oracle-retail/collect.py) adapts C1C
orchestration and reuses unchanged C1B SRO1 frame/decoder functions. Per-stop
SESSION/SAMPLE/END bytes are exclusively created, fsynced, closed, fully reread,
decoded and hashed before the numbered ACK. ACK JSON is itself flushed/reread.
Synthetic fixtures are explicitly labelled synthetic; retail ACKs say false.
Partial diagnostic groups retain complete=false and continue; intact payloads
are not discarded because an unrelated cache is unreadable.

Atomic `ACK n STOP` validates durable completion then disposes at that same stop.
ReadFile control lines prevent stdio-prefetch/PeekNamedPipe disagreement.
Unknown exceptions pass to Windows. No software traps, instruction replay,
injection, forcing, detach, target-memory edits or borrowed-pointer workers.
All-stop supports copied bytes at that stop, not pre-stop object lifetime,
generation history, cross-event coherence or immutable caches.

## Executed engineering checks

Local authoritative build14/qualification11 reside under
`.local-work/resource-oracle-retail/`. Forty decoder unit assertions and
thirteen actual Windows attachment fixture scenarios pass. Original MASM
fixture constructs source-shaped updater/gate prologues and caller frames with
real four-slot stops, native-shaped resource/reference/BC memory and independently
specified expected IL/Cu-like numeric IDs. These are synthetic memory, never game
observations. Three separate worker lifetimes, wrong Workshop, wrong grid return,
stale transfer caller, invalid payload, byte guard mismatch, rejected ACK,
crash-before/after, partial-prelude/unrelated-partial and completion-with-no-next-stop
are included. Existing C1C qualification-c1d01 freshly passes all19 cases.

Earlier build02 failed to locate MASM output due `/Fo:` syntax; build03 corrected
it. A guessed byte-sized MOV encoding failed offline preflight; actual bm001 and
EXE verify MOVZX EBX,AL bytes0fb6d8. No target launch followed either failure.
Earlier builds/receipts and independent REWORK findings remain local, unmodified.
Build09 additionally tests the user-requested Steam/attach lifecycle and disposal
only after pinned-process admission. Compiler/tool logs and exact hashes remain
in each immutable build.json/build.log.

## Commands and effects

From repository root, installed Python3.14.3 and MSVC19.51.36256.0/SDK only:

```powershell
& 'C:/Users/User/AppData/Local/Python/pythoncore-3.14-64/python.exe' -B research/resource-oracle-retail/build.py --name build14
& 'C:/Users/User/AppData/Local/Python/pythoncore-3.14-64/python.exe' -B research/resource-oracle-retail/qualify.py --build .local-work/resource-oracle-retail/build14 --output .local-work/resource-oracle-retail/qualification11
& 'C:/Users/User/AppData/Local/Python/pythoncore-3.14-64/python.exe' -B research/resource-oracle-retail/saves.py pre --name preflight-saves --cloud-disabled-confirmed
& 'C:/Users/User/AppData/Local/Python/pythoncore-3.14-64/python.exe' -B research/resource-oracle-retail/preflight.py --build .local-work/resource-oracle-retail/build14 --qualification .local-work/resource-oracle-retail/qualification11/qualification.json --name identity-preflight-third-final
```

These commands were executed; outputs require fresh names for reproduction.
build.py only reads owned sources/toolchain and writes a fresh ignored build.
qualify.py only executes its hash-pinned sibling fixture/controller and writes
fresh local synthetic receipts. saves.py inventories/backups/rehearses, never
automatically restores; post phase only reads/hashes. preflight.py hashes protected
inputs, installed definitions/config and source exports, and checks PE call targets
and instruction encodings; it does not start any process. collect.py additionally
requires a GO receipt, exact build pins, matching live/backup inventories and a
new Steam-launched PID before debugger attachment. The controller alters only
declared debug/control state and admitted experimental-process exit state.
All raw/native/save/binary artifacts stay ignored/local. No download/network/CI,
Git index/ref mutation, game configuration write or analysis-project mutation.

## Final associated-file mapping and qualification

The new [sourcefiles.h](../../../research/resource-oracle-retail/sourcefiles.h) reads the native IRES associated-file vector for requested IL/Cu members. Existing read-only Ghidra state was exported using owned E2ReadSession/Cr1Recon helpers with -readOnly -noanalysis; process command and001–010 native exports are local and source-ledger pinned. No import, analysis run, symbol/type/comment change or database save was requested. Stop sentinel ended the worker.

IRES vtable144b6f0b0 slots100/108 lead to1402b76f0: resource+30 is a ushort association-table index (ffff sentinel), not a compile index. Global count145e881e8 and pointer145e881f0 select an entry containing pointer-array begin+0 and signed count+8. The native getter returns the last associated file; the decoder preserves the entire ordered vector and makes no defining/winning-file claim. Bounds: table<=65536, associated count1..128, exact reads; resource index, global table/count, slot/entry and pointer array reread. This detects declared changes, not ABA or every inter-thread mutation.

Typed TESFile vtable144b29a70 / packed144b29b80, captured prefix0x370.1405b9950 copies separate inline strings at+38/+268, each0x104 bytes. Namespace remapper1402b6c70 uses flags+1b8 (100 light,200 master redirect,400 medium) and indices+218/+219/+21a. Only one ordinary associated file named Starfield.esm, flags&700==0, compile index0 and resource high byte0 qualifies the narrow main-file identity; special/multiple/incomplete cases stay UNKNOWN. Final native IL/Cu each satisfy this with flags85. All failure paths clear both completeness and main identity. This does not qualify a full load map or override winner.

Build10 exposed a synthetic entry allocation12 versus required16; fixed fixture. Build11/qualification08 had one good-scenario target exit0 with zero samples while the other12 passed. Its initiating cause remains unproven. Build12 adds initial-system-breakpoint DR reconciliation/readback; build13 adds fixture main-ready handshake before attach, matching actual Steam main-menu lifecycle. Build14 clears stale identity on failed source-file rereads. Final40 unit assertions and13 attached Windows cases all pass; earlier failed receipts remain local. No universal scheduling/event-completeness claim follows.

The offline [analyzer](../../../research/resource-oracle-retail/analyze.py) only reads closed local receipts and pinned source exports, verifies binary framing/length/hash/decoded rows and ACK/EXIT counts, and writes a fresh derivative JSON. It validates native-associated-file raw prefixes and source correspondence. It source-qualifies02's alternate caller while preserving raw UNKNOWN;03 is originally BOUND. It never operates the target.

Actual final controller: `.local-work/resource-oracle-retail/build14/sor-c1d-controller.exe`, SHA25674aef9e6d7f366cd698beb245df98b8d6b2c49a0f906276a14a5edf75d6b9d6c. Exact invocation, Steam dispatch, launch gate and build/source pins: `retail-attempt03/config.json`, `steam-launch03.json`, `launch-gate03.json`, `build14/build.json`, all beneath that local root. Controller invocation was `sor-c1d-controller.exe --retail-pilot 59532`; the wrapper command is retained in the engineering delivery metadata. Reproduction requires a newly admitted PID and fresh outputs; do not rerun a consumed gate or attach to an arbitrary session.

Additional executed commands from repository root:

```powershell
python -B research/resource-oracle-retail/analyze.py --attempt .local-work/resource-oracle-retail/retail-attempt02 --output .local-work/resource-oracle-retail/analysis-attempt02-final.json
python -B research/resource-oracle-retail/analyze.py --attempt .local-work/resource-oracle-retail/retail-attempt03 --output .local-work/resource-oracle-retail/analysis-attempt03-final.json
python -B research/resource-oracle-retail/saves.py post --name postflight-attempt03
python -B research/resource-oracle-retail/preflight.py --build .local-work/resource-oracle-retail/build14 --qualification .local-work/resource-oracle-retail/qualification11/qualification.json --name identity-postflight-final
```

Here python denotes the exact installed interpreter above. These are completed read/audit operations; the report records outcomes. No further live tests are part of delivery. The first native acquisition's three shared populations are pre-install diagnostics; only its payload receives BOUND_TRANSFER. Catalogue overlap/AL records remain site UNKNOWN. Do not infer current-generation freshness, placement, production, full regions or complete source membership from those records.
