# Credits

For [L0–L2C output-link validation](docs/experiments/output-link-validation-L0-L2C.md), **Python Software Foundation/CPython contributors and zlib/zlib-ng contributors** supplied the separately installed runtime/compression facilities (SOR-S-0113). **Bethesda Game Studios** supplied the locally owned save inputs. Existing project-authored manual-corpus methods and prior candidate discovery are identified at use. No third-party parser code was incorporated; evidence and publication boundaries remain separate.

For [manual S0–S7C save analysis](docs/experiments/manual-save-corpus-S0-S7C.md), **Python Software Foundation/CPython contributors and zlib/zlib-ng contributors** supplied the installed separate runtime and compression facilities (SOR-S-0113 extension). **Bethesda Game Studios** supplied the locally owned game/save inputs; prior xEdit/script research (SOR-S-0103/0104) supplied labelled definition/vocabulary comparisons. No third-party parser implementation was incorporated. Raw saves and decoded content remain local, with independent publication review required for selected research summaries.

For SOR-EXP-0002A, **Ian Patterson and SFSE contributors** supplied the serialization-address/source lead, independently rejected for the current retail locations (SOR-S-0120). **x64dbg contributors and documentation authors** supplied the installed headless debugger and its command/default-behavior documentation; **Microsoft Learn authors** supplied process/debugger verification references (SOR-S-0121). **Bethesda**, **Ghidra**, **CPython**, and **Microsoft MSVC/Windows SDK** supplied the separately installed research/build/runtime tools and inputs already credited below. Original experiment controllers are source-informed work, not a clean-room claim. No additional third-party implementation was incorporated; none of these authors endorses the research.

Credit identifies contributions actually used. It is neither a permission record nor a claim of endorsement. Add source-specific acknowledgments here and citations beside affected research; retain credit when independently reproducing an earlier finding.

## Scaffold preparation

- **The project maintainer's supplied `starfield-reference-handles-scaffold(1).zip`:** reference for the directory pattern, agent guidance, separate facts/hypotheses/function register, and local-only handling of bulky analysis material. Adapted at the user's explicit request. No engine finding or pinned environment from that project is adopted as verified here. See `SOR-S-0001` in [SOURCES.md](docs/SOURCES.md).
- **Free Software Foundation:** authorship of the GNU GPLv3 licence text included verbatim in [LICENSE](LICENSE). **SPDX** provided the public reference used to check the `GPL-3.0-or-later` identifier and licence terms. See `SOR-S-0002`.
- **Git project and GitHub documentation authors:** references consulted for text/ignore behaviour and first-push/remote instructions. The commands and project configuration were prepared for this scaffold; no Git/GitHub implementation source was copied. See `SOR-S-0003` and `SOR-S-0004`.

This scaffold was drafted with ChatGPT assistance at the maintainer's direction. That assistance is not experimental evidence or an independent reviewer. Public author/copyright-credit wording remains for maintainer confirmation.

## Outpost research

- **Bethesda Game Studios:** installed development script declarations and control flow, plus game/CK data and native terminology, supply the static research inputs (SOR-S-0104). No game source is redistributed or relicensed.
- **TES5Edit/xEdit contributors and documentation authors:** record interpretation and documented scripting APIs for the project-authored bounded readers (SOR-S-0103).
- **NSA/Ghidra contributors:** existing-program static inspection, references, instruction rendering and decompilation; documentation for read-only headless operation (SOR-S-0105).
- **Nexus Mods / StarfieldSaveTool contributors**, with the README's acknowledgment of **Mod Organizer 2 and Silarn**: clarification that its documented scope is save metadata, a useful limit on the initial persistence lead (SOR-S-0101).
- **rux616:** version/provenance discovery through vanilla-script mirror documentation; actual script inspection used the independent installed archive (SOR-S-0102).
- **SKKmods:** documented storage, unloading and removal behavior supplies test leads (SOR-S-0106). **Constellation-VASCO / Starfield Community Patch issue 155:** cargo return-flow/loading-condition report (SOR-S-0107). Neither has been reproduced here.
- **libxse/CommonLibSF contributors:** native-library scope/coverage discovery (SOR-S-0108). **SenterPat** (OUT) and **Sgtsplat/iamsgtsplat** (Unique-Resource Containers): build/assignment and single-resource storage investigation leads (SOR-S-0109/0110).
- **Ian Patterson, Stephen Abel and Expired:** SFSE installed documentation used for tool identity (SOR-S-0112). No SFSE run in this phase.
- **Maintainer's reference-handle project:** environment/project-location guidance only (SOR-S-0111); no implementation or engine finding imported.

Exact sources, access dates, limitations and affected research are in [SOURCES.md](docs/SOURCES.md) and cited in [the report](docs/experiments/initial-outpost-system-reconnaissance.md). Credit grants no reuse permission, and no source-reported runtime claim has been promoted to project validation.

For [SOR-EXP-0002 preparation](docs/experiments/SOR-EXP-0002-outpost-membership-reload-location.md), Bethesda's installed inputs and Ghidra's static rendering supplied coordinate-name/API evidence (SOR-S-0104/0105); prior xEdit interpretation supplied the storage choice (SOR-S-0103). **Python Software Foundation and CPython contributors** supplied the installed separate runtime/standard library for original offline integrity, contract and synthetic-test tools (SOR-S-0113). SFSE loader/DLL identity was rechecked, not executed or incorporated (SOR-S-0112). That initial offline-only pass was followed by the scoped incorporation below.

For the continued EXP0002 implementation: **Ian Patterson** supplies the explicitly MIT-granted SFSE public interface header (SOR-S-0114 / SOR-P-0001); notice retained. **Maintainer/reference-handle project contributors** supplied architecture and native research locators (SOR-S-0115), and **libxse/CommonLibSF contributors** supplied field/type research leads (SOR-S-0116). Native operands were independently checked, including a layout discrepancy; no sibling observer code or CommonLib implementation was incorporated. **Microsoft Visual C++/Windows SDK and Microsoft Learn authors** supplied installed build facilities and debugger API documentation (SOR-S-0117). These are substantive source-informed research/tool credits, not claims of clean-room development or live validation.

For the first primary Gate B attempt, **Ian Patterson and SFSE contributors** supplied read-only implementation evidence explaining why declared save/load message enums do not guarantee active dispatch (SOR-S-0118). No hook implementation was copied or adapted. This diagnosis corrects our observer's integration assumption; it is not an outpost finding.

For the review14 primary run, **Ian Patterson and SFSE contributors** supplied read-only task-dispatch implementation context (SOR-S-0119) for the observed execution-thread discrepancy. No implementation was incorporated, and safe native-query thread affinity remains unresolved.

Microsoft's installed CDB/dbgeng and Windows SDK minidump/AMD64 CONTEXT format declarations support the [EXP0002A offline crash comparison](docs/audits/exp0002a-crash-dump-comparison.md) (SOR-S-0117 extension). Separate installed tools and format consultation only; no third-party implementation/header incorporated. No additional maintainer-owned code reuse occurred in this task.

Microsoft CDB/dbgeng and Ghidra debugger-agent documentation informed the [final EXP0002A software-breakpoint preparation](docs/audits/exp0002a-final-software-attempt.md). Separate installed tools/read-only consultation; no third-party implementation incorporated.

## Offline structural containment — 2026-10-08

SOR-EXP-0005 reuses the project's original SOR-EXP-0003/0004 decoder and candidate research, with installed CPython/standard-library zlib facilities credited in SOR-S-0113. Previous xEdit-interpreted Bethesda beacon/storage definition evidence (SOR-S-0103 / SOR-F-0004) informs explicitly limited base-token comparisons. No outside parser, implementation, new dependency or live tool run was introduced. [Results and limits](docs/experiments/outpost-save-structural-containment.md).

## Mature-save validation — 2026-10-08

SOR-EXP-0006 credits preserved project/maintainer-directed exploratory discovery and methods as prior unreviewed research (SOR-S-0124), rather than presenting replication as new discovery. Python Software Foundation/CPython contributors provide the installed separate runtime and standard-library zlib facilities (SOR-S-0113). Earlier Bethesda inputs and xEdit interpretation supply independently inventoried marker/keyword definition comparisons (SOR-S-0103/0104). No external save parser or new third-party implementation was incorporated. [Results, contradictions and provenance](docs/experiments/mature-save-outpost-validation.md).

## Historical save inventory — 2026-10-09

[Historical inventory and location triage](docs/experiments/historical-save-inventory-triage.md) builds on the project/maintainer-directed exploratory and validated save methods credited in SOR-S-0124 and SOR-EXP-0003/0005/0006. Python Software Foundation/CPython and zlib/zlib-ng contributors supply separately installed runtime/compression facilities (SOR-S-0113). Bethesda supplies the locally owned save inputs; prior xEdit interpretation and installed definition research retain SOR-S-0103/0104 attribution. No third-party parser implementation or new dependency is incorporated, and no publication permission is implied.

## Supplemental launch-era corpus — 2026-10-09

**TheDailyXPerience** supplied the save package published on [Nexus Mods, listing 1798](https://www.nexusmods.com/starfield/mods/1798), used as observational inputs for [SOR-EXP-0008](docs/experiments/launch-era-third-party-save-corpus.md), SOR-S-0125. No endorsement is implied; originals and substantial payload remain local and excluded from publication. **Igor Pavlov and 7-Zip contributors** supplied the separately installed listing/extraction tool, SOR-S-0126. **Python Software Foundation/CPython and zlib/zlib-ng contributors** supplied installed runtime/compression facilities, SOR-S-0113. Existing project/maintainer-directed methods retain SOR-S-0124 and prior Bethesda/xEdit definition-research credit SOR-S-0103/0104. No third-party parser implementation was incorporated.


## Active outpost identification research — 2026-10-09

[SOR-EXP-0009](docs/experiments/active-outpost-identification.md) credits **Bethesda Game Studios** for the locally installed engine/content/script research inputs (SOR-S-0127 / SOR-S-0103/0104), **Ghidra contributors** and the existing installed **Eclipse Adoptium/OpenJDK** runtime for separate read-only analysis tooling, and **Python Software Foundation/CPython and zlib/zlib-ng contributors** for installed offline tooling (SOR-S-0113). Existing project/maintainer-directed methods retain SOR-S-0124 provenance. **TheDailyXPerience** retains SOR-S-0125 credit for the launch-era observational corpus and unchanged raw redistribution restrictions. No outside parser implementation or new dependency was incorporated; proprietary exports remain local.
