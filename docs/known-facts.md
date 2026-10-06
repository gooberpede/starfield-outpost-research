# Established Findings

**Only scoped STATIC findings are established. No runtime or saved-state finding.** Policy decisions in [DECISIONS.md](DECISIONS.md) are separate from engine evidence.

Add decisive, scoped findings with `SOR-F-` IDs using [the finding template](templates/finding.md). State confidence and basis (`STATIC`, `RUNTIME`, `SAVE`, or `CROSS-VALIDATED`), exact build/sample scope, supporting evidence, source credit, limitations, and counterexamples. Keep unconfirmed explanations in [hypotheses.md](hypotheses.md).

No version, address, object relationship, API capability, or binary layout from the prior conversation or reference-handle scaffold is adopted as fact here. Preserve superseded entries with their replacement links and reasons.

## SOR-F-0001 — Installed source exposes workshop membership and lifecycle interfaces

PROVEN / STATIC / current, scoped to SOR-ENV-0001's hashed ContentResources.zip. `Scripts/Source/ObjectReference.psc` lines 568–575, 636, 1766–1782 explicitly declare membership/resource queries and placement/removal/output-link events. This proves declaration presence, not executable support, exhaustive membership enumeration or runtime event order. Supporting evidence SOR-EV-0001; original source SOR-S-0104. Unchecked compiled PEX equivalence and attachments limit applicability. Persistence UNKNOWN; EXPOSED-INTERFACE, not VALIDATED-INTEGRATION. Publication REVIEW-REQUIRED, no clearance.

## SOR-F-0002 — Cargo and storage orchestration exists in installed Papyrus source

PROVEN / STATIC / current, same archive scope. `SQ_OutpostCargoLinkScript.psc:110–183` contains transfer orchestration with native inventory/redistribution calls; `OutpostContainerScript.psc:4–78` handles event registration and ready/busy state. Marker `OutpostCargoLinkMarkerScript.psc:47–51,84–88` reads/writes an animation ActorValue and applies animation on load. These source-level facts falsify a description of this source layer as declarations only. They do not prove the paths run, that animation state is saved, or that all cargo movement uses them. SOR-EV-0001, SOR-S-0104; REVIEW-REQUIRED.

## SOR-F-0003 — Native registration binds GetWorkshop to a keyed lookup callback

PROVEN / STATIC / current, pinned Starfield.exe SHA-256 in SOR-ENV-0001 only. At static `0x14209be33` the registration uses the GetWorkshop name; `0x14209be4a–0x14209be51` associates callback `0x142073cf0`. Its four instructions read `[R8+0xc8]`, zero R8D, load RDX from global `0x145f0b3d8`, and tail-jump to `0x140517d60`. Independent PE reads confirm callback bytes and registration RIP-relative targets (SOR-EV-0001). This establishes the instruction-level path; R8's live provenance, the global's resolved form, full container semantics and sole ownership authority are not proven. No function/symbol was created at the callback (Ghidra had a label, not a function). `+0xc8` is an operand offset in this callback's source object, not a saved offset or universally validated TESObjectREFR layout. Persistence UNKNOWN; OBSERVED-INTERNAL, proposed observation only. REVIEW-REQUIRED.

## SOR-F-0004 — Beacon, storage recipe and selected attachments map in the inspected ESM

PROVEN / STATIC / current, scoped to the hashed Starfield.esm interpreted by xEdit 4.1.5p. Focused output keys: ACTI 002C60E9 VMAD ScriptName `outpostbeaconscript`, KWDA includes WorkshopKeyword 00054BA7; COBJ 00299547 CNAM points to CONT 0023AED9; that CONT's PRPS CarryWeight is 75 and ONAM points to FLST 0029954D. CONT 002CE194 has VMAD OutpostContainerScript, while the inspected 0023AED9 record has no VMAD row. This last observation must not be broadened to all storage, pack-in children or runtime script instances. SOR-EV-0001 contains precise output locators; SOR-S-0103/0104 credited. These are xEdit-interpreted definition relationships/defaults, not independently decoded bytes, live capacity, persistence proof or current runtime override resolution. REVIEW-REQUIRED.

## SOR-F-0005 — Static position APIs and latitude/longitude naming sites

PROVEN / STATIC / current, scoped to byte-revalidated SOR-ENV-0002 inputs; [SOR-EV-0002](experiments/evidence/exp0002-preparation/README.md). Bethesda ObjectReference.psc declares position XYZ at lines 523/526/529, angles at 372/375/378, current location/parent cell/worldspace at 405/517/640. Raw CK strings include Location: Longitude/Latitude at static VA 0x148aa1b60/178, with existing Ghidra xrefs in function 0x142b96190. Retail strings latitude/longitude at 0x144c92618/0x144c92948 have xrefs in 0x14167f7e0 and 0x14341c0a0. Instructions 0x14167f82f–854 pass object-relative addresses +0x68/+0x88 with these names through an indirect call. No raw float layout, units, coordinate frame, body association, selected-outpost connection, runtime value or persistence is established. UI/property-binding interpretation is provisional. Sources SOR-S-0104/0105, not external implementation reuse. REVIEW-REQUIRED.

## SOR-F-0006 — Native operand checks supporting the observer contract

PROVEN / STATIC for the enumerated instruction operands only, SOR-ENV-0002 / SOR-EV-0002. Position callbacks 0x142072580/590/5a0 read R8+8c/+90/+94; angle callbacks 0x1420702e0/300/320 read +80/+84/+88 before multiplication; parent-cell callback 0x14208b990 reads +b0. Worldspace callback 0x14208b9e0 uses cell flags +48 and worldspace +110. GetFormID 0x14204d600 reads +28. Cell array windows at 0x140b1e22e/23f/2c8/2d9 support count +80, data +88 and pointer stride 8; 0x140bbdf70 accesses worldspace +d8. [Detailed contract](../runtime/exp0002/STATIC-CONTRACT.md) separates native checks from consulted type/candidate-ID leads, wrappers, stateful calls and rejected CommonLib cell offsets. Sources SOR-S-0104/0105/0115/0116; no copied library layout or live structure/coordinate/persistence validation. Unit/frame/lifetime/authority UNKNOWN; OBSERVED-INTERNAL, not safe mod integration. REVIEW-REQUIRED.
