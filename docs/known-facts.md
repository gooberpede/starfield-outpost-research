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
