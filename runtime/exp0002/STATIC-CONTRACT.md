# EXP0002 native contract and provenance

All addresses below are **static VAs** in SOR-ENV-0002 Starfield.exe, preferred base `0x140000000`, SHA-256 `7e9adb1414a8e1b325e5e1f097b9b17b78deb7eebeda37a333351a43a60f9d28`. Actual runtime addresses use the loaded module base plus RVA. Local instruction exports and build-generated 32-byte SHA-256 guards support this table; no proprietary instruction bytes are included here. This is a STATIC operand contract, not a validated integration interface, complete engine layout, ownership contract or saved representation.

| Use | Independent native anchor | Implemented interpretation and limit |
|---|---|---|
| Main-thread task | Approved SFSE PluginAPI.h, SFSETaskInterface | Header explicitly describes AddTask as one execution on Main thread then deletion. Runtime compatibility not exercised. |
| Player | GetPlayer callback `0x14177a1f0` | Reads global `0x145f43230`; require candidate reference FormID 14. |
| Identity | GetFormID `0x14204d600`; selection sites | FormID operand +28; +2e form-type and +24 candidate identifier are reference-derived gates/leads. The latter is never called a resolved handle. |
| Stored base | GetBaseObject branch `0x1420706b7` | Reference +98. Native GetBaseObject also handles altered-base extras; stored_base is intentionally distinct from its resolved result. |
| Transform | Position callbacks `0x142072580/590/5a0`; angles `0x1420702e0/300/320` | Reference +8c/+90/+94 and +80/+84/+88. Raw angle inputs precede an engine multiplier; units UNKNOWN. No coordinate conversion. |
| Stored parent cell | `0x14208b990` | Reference +b0, not proof of loaded 3D. |
| Exterior worldspace | `0x14208b9e0` | Cell +48 bit 0 controls exterior/null branch, worldspace +110; native fallback uses extras when stored parent missing. Selection requires a stored exterior parent; query result is logged separately. |
| Candidate persistent cell | `0x140bbdf70`, operands at `0x140bbdff4/0x140bbe019` | Worldspace +d8; setter-like code also accesses cell +110. The function is inspected, never called. No universal membership inference. |
| Cell reference view | windows at `0x140b1e22e/23f/2c8/2d9` | Count +80, array pointer +88, stride 8. +84 captured only for before/after equality, without capacity semantics. Type constants 49/4a/4b/56 are consulted header leads, not independently proved enumerations. |
| GetWorkshop | callback `0x142073cf0`, tail `0x140517d60` | Entry R8 source; reads +c8; RDX from `0x145f0b3d8`; R8 zeroed; tail jump. Return pointer is a candidate form, validated by bounded reads. Tail code uses locking/resolution; invocation may change caches. |
| Current location | `0x14208b8f0` to `0x140b4e650` | R8 moved to RCX before tail jump. Helper has state/cache behavior; query is an intervention. |

## Source boundaries

Bethesda native inputs (SOR-S-0104), Ghidra rendering (SOR-S-0105), sibling research locators (SOR-S-0115) and CommonLibSF field/type leads (SOR-S-0116) are credited. We checked the operand sites independently against this project's pinned executable. No sibling observer implementation, CommonLib class/layout definition, binding or build script was copied/adapted. This is source-informed research, **not clean-room work**. CommonLib's consulted cell layout disagrees with this build's +110 worldspace / +48 flags; its +118 / +40 offsets were rejected. The incomplete callback export is preserved and corrected by later exports, not silently presented as a successful run.

The sole incorporated third-party code is the exact approved SFSE public interface header (SOR-P-0001 / SOR-S-0114). Its scope and notice are in [the permission register](../../docs/PERMISSIONS.md) and [LICENSE.txt](third_party/sfse/LICENSE.txt). Windows SDK declarations and MSVC/Windows system facilities are used through the installed compiler; no SDK/runtime binaries are bundled. No Address Library database is read or packaged, and no CommonLib dependency is linked/downloaded.

## Remaining assumptions

Selection scans at most two cells and 4096 entries per cell, recording a bounded anomaly and suppressing target queries for missing/ambiguous role counts; the observer remains available for later explicit checkpoints. It does not discover all outpost members or prove absence elsewhere. Repeated byte views detect some changes but neither lock the arrays nor retain engine ownership. The task is synchronous on the documented SFSE main thread; other threads can still mutate state. Direct callback invocation with unused registers zeroed is grounded in these entry operands but **has not been executed**; engine lifetime, query safety and current profile compatibility remain live assumptions under brief section 21. No safe mod integration point is claimed.

GetBaseObject and Is3DLoaded use wrapper conventions distinct from the chosen direct R8 callbacks. They are not invoked. loaded_3d, resolved handles, game time, body/map/lat-long conversion and saved authority remain unavailable. Static byte guards do not prove semantics or stop a call that blocks inside the engine.

## Local evidence anchors

SOR-EV-0002 indexes `.local-work/recon/exp0002-observer-interfaces.tsv`, `registration-windows.tsv`, `observer-callbacks.tsv` (PARTIAL), `selection-sites.tsv` and `final-native-contract.tsv` (each filename prefixed `exp0002-`). Read-only/no-analysis Ghidra queries did not change project state. Build manifests list each file-backed RVA, file offset, hash and exact source identities. Native bytes, exports, PDB/build outputs and runtime records remain LOCAL-ONLY.


Synchronization revision: operator-settled requests gate fresh per-task acquisition. Optional SFSE save/load messages are telemetry only. Repeated global-player, cell/world, collection-header and selected-identity reads use the existing operand sites above; no new native address/layout or hook is introduced. A2R retains no A2 acquisition state. These consistency checks remain non-atomic and do not confer ownership; see the current runtime README and correction review before any fresh run.
