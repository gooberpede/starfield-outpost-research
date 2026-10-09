# Source Register

### SOR-S-0113 extension — Output-link validation, 2026-10-07

Installed CPython3.14.3 and standard-library zlib runtime1.3.1.zlib-ng supplied separate offline execution, hashing, BCPS decompression, structured comparisons and CSV/JSON generation for [SOR-EXP-0004](experiments/output-link-validation-L0-L2C.md). Python Software Foundation/CPython and zlib/zlib-ng contributors credited; no third-party implementation or dependency incorporated. Existing project-authored S0–S7C decoder/diff/candidate definitions reused with hashes/commit recorded in provenance and local preregistration. Bethesda locally owned saves supplied the evidence; no game data/raw save redistribution. No external source consultation or expanded code permission was needed.

### SOR-S-0113 extension — Manual corpus, 2026-10-07

Installed CPython3.14.3 standard-library hashing, filesystem, struct, JSON, CSV, difflib, unittest and zlib runtime `1.3.1.zlib-ng` executed original bounded offline scripts for [SOR-EXP-0003](experiments/manual-save-corpus-S0-S7C.md). Credit Python Software Foundation/CPython contributors and zlib/zlib-ng contributors for separate installed tooling. No implementation/example, redistributable runtime or new dependency was copied into this repository. The BCPS bounds/alignment and candidate motifs were derived from the authorized local corpus, not from a third-party parser. Exact runtime/script/input/decoded hashes are in local SOR-EV-0009 manifests. Tool/checksum success is not semantic validation.

Existing SOR-S-0103/0104 findings supplied the independently recorded beacon/storage definition numbers and script vocabulary used only as candidate comparisons. Bethesda's save bytes are local research inputs; no raw saves, decoded blobs or bulk string inventories are proposed for tracking. No new source implementation consultation, maintainer-code adaptation or permission expansion occurred in this pass.

### SOR-S-0122 — Maintainer debugger lifecycle research and scoped tooling reuse

2026-10-07, `gooberpede/starfield-reference-handles`, clean local checkout/origin verified at commit `6a77579a184c64e0c080c8f3b7883c34bd17e24b`. Consulted debugger/README.md, debugger/native/README.md, native Win32 hardware/RF core, startup/post-title/destructive adapters, probe_attach.py and lifecycle/capability reports. Exact per-file hashes and copied/adapted/conceptual uses: [provenance](../debugger/exp0002a/maintainer/PROVENANCE.md). SOR-P-0002 supplies the maintainer-authored rights/user grant, not a blanket grant for contained third-party work. Initial correction copied lifecycle_checks.py and adapted only offline read_rows/validate. SOR-D-0016 subsequently adapts the native RF core into the one-request adapter and runs bounded fresh disposable controls; [results](audits/exp0002a-adapter-qualification.md) include an unresolved new-thread retirement failure. No sibling disabled live adapter was enabled. Historical negative outcomes inform backend selection, not current-game findings. Raw sibling disposable evidence replay is explicitly historical. No self-credit/notice required; provenance retained at use.

### SOR-S-0123 — Installed Ghidra dbgeng capability assessment

Ghidra12.1.2 PUBLIC local `Ghidra/Debug/Debugger-agent-dbgeng/`: data/support/local-dbgeng-attach.py (attach/wait sequence), pypkg/src/ghidradbg/methods.py (attach_pid, break_hw_address, detach), commands.py (ghidra_trace_attach), pypkg/pyproject.toml (ghidratrace12.1/Pybag dependency). Read-only inspection2026-10-07; exact file hashes in correction backend-inventory.json. Confirms available implementation paths, not an executed Ghidra session or safe lifecycle. No source/dependency incorporation, install or debugger execution. Prior Ghidra credit SOR-S-0105 applies; [ordered assessment](audits/exp0002a-debugger-correction.md). Maintainer exception does not cover these third-party files.

### SOR-S-0120 — SFSE serialization addresses as a rejected current-build lead

Ian Patterson and SFSE contributors, read-only consultation2026-10-07; pin `48535cc4306ab345252bf740c20a1c6194929b0e`, [sfse/Hooks_Serialization.cpp](https://github.com/ianpatt/sfse/blob/48535cc4306ab345252bf740c20a1c6194929b0e/sfse/Hooks_Serialization.cpp). Exact declaration locators SaveGame_Call, SaveGame_Original, DeleteSaveGame_Original and Hooks_Serialization_Commit / disabled installation. Substantive influence: distinguishing save wrapper/serializer, choosing a high-layer search and testing old addresses before use. Retail checks reject address/signature transfer; [EXP0002A report](experiments/SOR-EXP-0002A-native-save-thread-mapping.md), SOR-F-0007. No hook code, binding, layout, comment or source fragment incorporated. SOR-P-0001 remains limited to the already approved PluginAPI.h. Consultation is neither broader reuse permission nor author endorsement.

### SOR-S-0121 — x64dbg headless command and breakpoint behavior

x64dbg contributors/documentation authors, consulted2026-10-07. Installed revision label `9c8ca1cae0b6d56cc44f31fddcb10e3b02ffbb87`; read-only [src/headless/headless.cpp](https://github.com/x64dbg/x64dbg/blob/9c8ca1cae0b6d56cc44f31fddcb10e3b02ffbb87/src/headless/headless.cpp), [src/dbg/x64dbg.cpp](https://github.com/x64dbg/x64dbg/blob/9c8ca1cae0b6d56cc44f31fddcb10e3b02ffbb87/src/dbg/x64dbg.cpp), [src/dbg/commands/cmd-debug-control.cpp](https://github.com/x64dbg/x64dbg/blob/9c8ca1cae0b6d56cc44f31fddcb10e3b02ffbb87/src/dbg/commands/cmd-debug-control.cpp) and [src/dbg/debugger.cpp](https://github.com/x64dbg/x64dbg/blob/9c8ca1cae0b6d56cc44f31fddcb10e3b02ffbb87/src/dbg/debugger.cpp). Locators: headless stdin command loop; -userdir/-cf parsing; cbDebugAttach's PROCESS_ALL_ACCESS and hexadecimal failure PID; cbDebugDetach breakpoint removal; Events/TlsCallbacks default true. Used to understand the installed interface, failed attach and unexpected TLS sites. No debugger implementation adapted/incorporated. Original Python command orchestration invokes the installed executable as a separate tool; no SDK linking, vendoring or new dependency.

Primary documentation: [conditional breakpoints](https://help.x64dbg.com/en/latest/introduction/ConditionalBreakpoint.html), [expressions](https://help.x64dbg.com/en/latest/introduction/Expression-functions.html), [formatting](https://help.x64dbg.com/en/latest/introduction/Formatting.html), [attach](https://help.x64dbg.com/en/latest/commands/debug-control/AttachDebugger.html), [detach](https://help.x64dbg.com/en/latest/commands/debug-control/DetachDebugger.html), [breakpoint commands](https://help.x64dbg.com/en/latest/commands/conditional-breakpoint-control/SetBreakpointCommand.html), [command line](https://help.x64dbg.com/en/latest/introduction/Commandline.html). Hardware breakpoint and script-command docs were considered, but selected acquisition uses software breakpoints. Installed -help/pinned source supplied newer headless options absent from older commandline documentation. Failed guessed documentation URLs supplied no evidence.

Microsoft Learn [CheckRemoteDebuggerPresent](https://learn.microsoft.com/en-us/windows/win32/api/debugapi/nf-debugapi-checkremotedebuggerpresent), plus SOR-S-0117/0119 debugger API references, informed independent read-only OS verification. Documentation and synthetic tests do not establish Starfield safety. Exact installed hashes, original fixture, unexpected defaults, corrections and actual results: SOR-ENV-0003 / SOR-EV-0005. Ghidra/Bethesda/CPython/MSVC inputs remain credited under SOR-S-0104/0105/0113/0117.

Record meaningful sources when they influence the work. A source entry is not a reuse permission, a compatibility finding, or proof of the source's claims. See [THIRD_PARTY_POLICY.md](../THIRD_PARTY_POLICY.md) and [PERMISSIONS.md](PERMISSIONS.md).

## Sources used for scaffold preparation

### SOR-S-0001 — User-supplied reference scaffold

- Source: `starfield-reference-handles-scaffold(1).zip`, attached to the setup request; no public URL supplied.
- Supplier: project maintainer. Original per-file authorship/rights not independently established from an upstream repository.
- Version: attached artifact identified by SHA-256 in [PROVENANCE.md](PROVENANCE.md); inspected 2026-10-01.
- Used contribution: structural pattern and research-document responsibilities, at the user's explicit request.
- Scope: adapted organizational guidance; no scripts, engine findings, existing environment baseline, or complete old archive redistributed.
- Permission/user decision: use as the structural reference explicitly requested; not a blanket grant for third-party content it might identify. Decision `SOR-D-0006`.
- Credit: [CREDITS.md](../CREDITS.md). No claim of independent validation of the reference-handle research.

### SOR-S-0002 — GNU GPLv3 text and SPDX version-choice reference

- Author of licence text: Free Software Foundation, Inc.; licence dated 29 June 2007.
- Public reference: <https://spdx.org/licenses/GPL-3.0-or-later.html>; inspected 2026-10-01.
- Canonical text location: <https://www.gnu.org/licenses/gpl-3.0.txt>; direct retrieval unsuccessful during this preparation.
- Included bytes: verbatim installed GPLv3 licence document, source/hash in [PROVENANCE.md](PROVENANCE.md).
- Contribution: required [LICENSE](../LICENSE), [licence grant/boundary](../LICENSING.md), and distinction between internal conduct rules and GPL recipient rights.
- Permission: the licence document expressly permits verbatim copying/distribution; its notice is retained. This legal-text inclusion implements the user's chosen GPL licence, not approval to reuse any software implementation.
- Credit: [CREDITS.md](../CREDITS.md) and [THIRD_PARTY_NOTICES.md](../THIRD_PARTY_NOTICES.md).

### SOR-S-0003 — Git attributes and ignore documentation

- Author/project: Git documentation contributors.
- Sources: <https://git-scm.com/docs/gitattributes> and <https://git-scm.com/docs/gitignore>; inspected 2026-10-01, online documentation rather than a pinned source checkout.
- Contribution: consulted behaviour of line-ending attributes and ignore rules for this scaffold's newly authored configuration and evidence handling.
- Scope: reference use, not copied Git implementation code; no dependency/binary bundled.
- Affected files: `.gitattributes`, `.gitignore`, `WORKFLOW.md`, and evidence instructions. Credit: [CREDITS.md](../CREDITS.md).

### SOR-S-0004 — GitHub local-repository and remote instructions

- Author/project: GitHub documentation contributors.
- Sources: <https://docs.github.com/en/migrations/importing-source-code/using-the-command-line-to-import-source-code/adding-locally-hosted-code-to-github> and <https://docs.github.com/en/get-started/git-basics/managing-remote-repositories>; inspected 2026-10-01.
- Contribution: historical reference for owner-operated initial push/remote instructions in `GIT_SETUP.md`, absent from the current checkout. Original provenance retained; no new setup instructions or Git action inferred.
- Scope: standard command usage tailored to the user's paths, not copied GitHub implementation; no dependency bundled. Credit: [CREDITS.md](../CREDITS.md).

## Candidate outpost-research leads — not validated or approved

These names came from the earlier discussion, not a completed prior-work audit in this project. They are listed to preserve leads, not to assert functionality, licence coverage, or release compatibility.

| Source ID | Candidate | Purpose of possible review | Current status |
|---|---|---|---|
| SOR-S-0101 | `Nexus-Mods/StarfieldSaveTool` — <https://github.com/Nexus-Mods/StarfieldSaveTool> | Container/metadata capability and limitations | README rechecked 2026-10-06; details below; no implementation adopted |
| SOR-S-0102 | `rux616/modding-sf1-scripts-vanilla` — <https://github.com/rux616/modding-sf1-scripts-vanilla> | Script provenance/version discovery | README rechecked 2026-10-06; local Bethesda archive used for code inspection |

At the initial lead-recording stage no third-party outpost claim was promoted to a finding and no reuse approval existed; later scoped SFSE header approval is recorded below. Prior conversation citations and summaries must be checked before use. Add other sources only when actually consulted or deliberately registered as a lead; do not populate a ceremonial list of tools never used.

## New records

Use [templates/source.md](templates/source.md). Record author/owner, exact title/location and commit/version, access date, contribution, inspection status, original rights-holder/licence evidence, affected findings/files, permission decisions, credits, and public/private evidence locations. Preserve original attribution when later independently reproducing a result.

## Initial reconnaissance consultation — 2026-10-06

Inspector: Codex at maintainer direction; all entries affect [SOR-EXP-0001](experiments/initial-outpost-system-reconnaissance.md). Public pages are read-only consultations, not tool downloads, execution, code reuse or permissions. Web snapshots may be stale; versions below identify returned pages, not verified latest releases. Commit hashes not exposed by the retrieved page remain UNKNOWN. Project notes are REVIEW-REQUIRED; raw local inputs/exports are LOCAL-ONLY. No publication clearance or author contact.

### SOR-S-0101 — StarfieldSaveTool recheck

Nexus Mods contributors; repository README on `master`, commit UNKNOWN. The description explicitly limits primary JSON work to metadata and excludes interpretation of main data blocks. This is a container/metadata lead, not an established outpost-state parser. README credits Mod Organizer 2 and Silarn for earlier format help. No implementation/templates inspected or adopted; no obvious licence file in retrieved root listing, rights basis UNKNOWN. Future execution/reuse requires its own review. SOURCE-REPORTED; no saves read here.

### SOR-S-0102 — Vanilla-script mirror recheck

rux616; `main` README, commit UNKNOWN. It reports CK/game 1.16.244.0 and version/build-labelled tags, and attributes underlying software rights to Bethesda. Useful as a version/provenance lead only. No mirror scripts/compiler imported. Locally installed `ContentResources.zip` was independently found and inspected (SOR-S-0104); mirror byte equivalence NOT CHECKED. Mirror accessibility grants no reuse rights.

### SOR-S-0103 — xEdit documentation/tool

TES5Edit/xEdit contributors; [overview](https://tes5edit.github.io/docs/2-overview.html) command-line section and [API reference](https://tes5edit.github.io/docs/13-Scripting-Functions.html) getters, traversal, loaded-file and output APIs. Online documentation version/commit UNKNOWN; local tool identified in SOR-ENV-0001. Consulted API contracts to author a small independent reader; no example script or implementation copied/adapted. View mode and cache flags are documentation-reported, not yet qualified by this project. Existing local log identifies MPL-2.0 for xEdit source; documentation-specific rights UNKNOWN. User authorizes separate-tool operation/helper placement through SOR-D-0009; no software redistribution. See [helper](../xedit/README.md).

### SOR-S-0104 — Bethesda installed development sources

Bethesda Game Studios; installed `Tools/ContentResources.zip`, exact hash/size in SOR-ENV-0001. Inspected selected `Scripts/Source/*.psc` entries locally, byte-identical extraction only into ignored private workspace. Original declarations/control flow support scoped STATIC findings; compiled PEX equivalence and actual VM execution remain unchecked. Underlying proprietary script rights remain Bethesda's, not the project GPL; no game code redistributed. The brief explicitly authorizes local inspection, not incorporation. Exact entry hashes and line anchors are recorded with SOR-EV-0001.

### SOR-S-0105 — Ghidra

NSA/Ghidra contributors; installed 12.1.2 PUBLIC, revision `c0f584bf229fffba61b36431f3ce30c0c3e4e682`. Local `support/analyzeHeadlessREADME.html`, launcher configuration and Java API used for bounded existing-program inspection. Headless documentation establishes `-readOnly -noanalysis` behavior; preservation is separately checked. Local launcher carries Apache-2.0 notice; no Ghidra source redistributed. Original `OutpostRecon.java` uses tool APIs, no sibling exporter code reused. Executed under brief Phase E; generated game-derived exports remain LOCAL-ONLY.

### SOR-S-0106 — SKK Universal Stash

SKKmods; [Nexus description/changelog](https://www.nexusmods.com/starfield/mods/5670?tab=description), returned version 009, updated 2024-06-23. SOURCE-REPORTED: distinguishes capped outpost production collectors from unlimited stash; reports workbench reconnection after unload and inventory consequences of removing transfer containers. These motivate capacity, unload and removal controls; none reproduced here. Page prohibits redistribution and requires permission for modification/assets; do not reuse scripts. Documentation only, no files downloaded. Affects storage/lifecycle/time questions.

### SOR-S-0107 — Cargo-link return-flow issue

Constellation-VASCO / Starfield Community Patch issue [#155](https://github.com/Starfield-Community-Patch/Starfield-Community-Patch/issues/155), issue page reports game version `1.0`, exact executable UNKNOWN, status Needs Vetting in returned page. SOURCE-REPORTED: outgoing material appears at its own incoming endpoint, with reported player-presence/sleep sensitivity. Used as a counterexample lead requiring loaded/unloaded controls, not proof of an engine defect in 1.16.244.0. Text rights UNKNOWN; short factual paraphrase only; no issue interaction or code consulted.

### SOR-S-0108 — CommonLibSF scope and coverage

libxse contributors; [README](https://github.com/libxse/commonlibsf), `main`, commit UNKNOWN; [include/RE/W listing](https://github.com/libxse/commonlibsf/tree/main/include/RE/W). Reports reverse-engineered library and GPL-3.0-or-later with Modding and Linking exceptions. Full file-specific terms not audited; no reuse decision. Returned W directory did not expose a Workshop header; this narrow negative search does not establish absence elsewhere. No offsets/layouts adopted. Useful future native-interface lead, presently LEAD/CONSULTED rather than validation.

### SOR-S-0109 — OUT: Outpost Ultimate Tweaks and add-ons

SenterPat; [Nexus description](https://www.nexusmods.com/starfield/mods/7013?tab=description) and [documentation search result](https://www.nexusmods.com/starfield/mods/7013?tab=docs). Returned description version 1.57, updated 2024-06-08; cached snapshot, current status UNKNOWN. SOURCE-REPORTED: outpost build/content expansion; documentation search snippet raises robot crew assignment/bonus constraints. Snippet-level robot claim is a provisional discovery lead only; full supporting implementation not inspected. Rights not established for incorporation; no mod/code downloaded. Affects construction and assignment questions.

### SOR-S-0110 — Unique-Resource Containers

Sgtsplat / iamsgtsplat; [Nexus description](https://www.nexusmods.com/starfield/mods/13016?tab=description), returned version 1.1, updated 2025-02-09. SOURCE-REPORTED: resource-specific small containers and transfer-container links. A useful single-resource control idea; not a validation of capacity/link semantics. Retrieved permissions prohibit reupload and require modification permission. No implementation downloaded or used; local vanilla container code was inspected independently. Affects storage/local-link test design.

### SOR-S-0111 — Sibling environment lead

Maintainer's local `starfield-reference-handles`, `docs/PROVENANCE.md` and `ghidra/README.md`, inspected 2026-10-06. Used only to locate external Ghidra project and documented headless entry point and compare reported SFSE/game versions. No exporter source or engine findings adopted. Commit not pinned; claims remain SOURCE-REPORTED until the independent local checks in SOR-ENV-0001. Rights basis for implementation reuse not reviewed; none authorized.

### SOR-S-0112 — SFSE installed documentation

Ian Patterson, Stephen Abel and Expired; local `sfse_readme.txt` identifies 0.2.21 pre-alpha and game compatibility 1.16.244. Read-only identity check; DLL/loader hashes and PE version resources independently recorded. No loader/DLL execution or source incorporation. Documentation/software rights not reviewed for redistribution; no redistribution proposed.

### SOR-EXP-0002 initial offline pass: reuse of existing research sources — 2026-10-06

SOR-S-0104 supplied installed position/location declarations and proprietary CK/retail string/code inputs; SOR-S-0105 supplied Ghidra's existing xrefs/instruction/decompiler rendering through the unchanged original reader; SOR-S-0112 installed loader/DLL identities were rehashed only. Exact hashes/anchors and limitations in SOR-EV-0002. No Bethesda source/native bytes or Ghidra exports promoted into Git; no SFSE/CommonLib/sibling implementation inspected for adaptation or incorporated. Prior xEdit relationship/display-name observations (SOR-S-0103, SOR-EV-0001) informed the planned small solid-storage choice. These uses are research/tool attribution, not new code-reuse approval.

### SOR-S-0113 — Installed CPython separate-tool execution

Python Software Foundation and CPython contributors; installed Python 3.14.3. Used under SOR-D-0010 for original offline scripts with standard-library hashing, JSON, PE byte reads, ZIP reads, timestamps, file flushing and synthetic unittest fixtures. Exact executable hash/locator in SOR-EV-0002 local tooling manifest. No CPython implementation, examples, package, bindings or redistributable runtime copied into the repository; no dependency download. Separate-tool operation only, not approval to vendor Python or other libraries. Affects research/exp0002 helpers and their offline validation. Tool success does not validate engine semantics.

### SOR-S-0114 — SFSE public interface header

Ian Patterson; [PluginAPI.h](https://github.com/ianpatt/sfse/blob/48535cc4306ab345252bf740c20a1c6194929b0e/sfse/PluginAPI.h) and [LICENSE](https://github.com/ianpatt/sfse/blob/48535cc4306ab345252bf740c20a1c6194929b0e/LICENSE), commit `48535cc4306ab345252bf740c20a1c6194929b0e`, fetched 2026-10-06 through read-only GitHub connector after exact user approval. MIT applies explicitly to this header only; preserved at runtime/exp0002/third_party/sfse. SOR-P-0001 documents the user's licence acceptance and exact use. The header supplies version/interface/task/messaging declarations. Runtime remains external; no other SFSE source incorporated. Source text preserved with LF normalization; build manifest hashes local files. REVIEW-REQUIRED package, no publication approval.

### SOR-S-0115 — Sibling observer architecture and research locators

Maintainer's [starfield-reference-handles](https://github.com/gooberpede/starfield-reference-handles), local HEAD `6a77579a184c64e0c080c8f3b7883c34bd17e24b`. Read-only README, plugin README, provenance/SFSE licensing and engine-layout/function research records on 2026-10-06. Supplied build feasibility, external-dependency boundaries and cell/reference instruction locators. No sibling observer source/build scripts copied or adapted. Native operand locators were independently checked in this project's pinned existing Ghidra program. This expands SOR-S-0111's earlier environment-only consultation for this continuation, not retroactively for EXP0001. Source-informed research is credited; sibling findings are not live validation here.

### SOR-S-0116 — CommonLibSF layout/type research leads

libxse/CommonLibSF contributors; local dependency pin `e0dbccd3a3716363f6b99194c98b7d2cccf2e7e6`, [repository](https://github.com/libxse/commonlibsf). Consulted TESObjectCELL, TESObjectREFR, TESForm, PlayerCharacter, BSTArray and IDs headers as research references on 2026-10-06 under user's clarification. Field/type leads only; no source, bindings, class declarations, dependencies or tests incorporated/linked. No library build was performed. Native cell flags/worldspace operands disagreed with the consulted layout and take precedence (STATIC-CONTRACT.md). No licence accepted for code reuse; any later incorporation needs a separate exact approval.

### SOR-S-0117 — Microsoft native build/debugger facilities

Existing PowerShell 7.6.5 is used for the original request helper without changing execution policy; Windows PowerShell 5.1 refused scripts under its existing policy. Installed Visual Studio 2026 Community 18.9.0, MSVC toolset 14.51.36231/compiler 19.51.36256, Windows SDK 10.0.26100.0. Separate installed tooling compiled original C++20 code; no package download, copied Microsoft example implementation or redistributed SDK/runtime. Exact paths/hashes/compiler-pass output in local build/tool manifests. Windows SDK declarations and system libraries support process reads, hashing, flushing, task worker and future debugger control.

### SOR-S-0118 — SFSE save/load notification implementation, read-only diagnosis

Ian Patterson and SFSE contributors; consulted 2026-10-06 at the same pinned commit `48535cc4306ab345252bf740c20a1c6194929b0e`: [sfse.cpp](https://github.com/ianpatt/sfse/blob/48535cc4306ab345252bf740c20a1c6194929b0e/sfse/sfse.cpp), [Hooks_Serialization.cpp](https://github.com/ianpatt/sfse/blob/48535cc4306ab345252bf740c20a1c6194929b0e/sfse/Hooks_Serialization.cpp), and [Hooks_Data.cpp](https://github.com/ianpatt/sfse/blob/48535cc4306ab345252bf740c20a1c6194929b0e/sfse/Hooks_Data.cpp). Read-only source inspection after the primary A0 attempt returned loading_before_task with load generation zero. Serialization hook installation is compiled out at lines 81–98; the save-load wrapper contains the PreLoadGame/PostLoadGame dispatch. Interface enum availability therefore does not establish operational notification delivery. Data-load notifications concern game data, not a demonstrated substitute for save-load safety. This is source evidence explaining an observed integration failure, not proof of the installed DLL's complete control flow. No source implementation, hook, address or adaptation was incorporated; only the previously approved interface header remains reused. See the [Gate B run record](experiments/EXP0002-gate-b-run.md).

### SOR-S-0119 — SFSE task dispatch implementation, read-only diagnosis

Ian Patterson and SFSE contributors; consulted 2026-10-06 at pin `48535cc4306ab345252bf740c20a1c6194929b0e`: [PluginManager.cpp](https://github.com/ianpatt/sfse/blob/48535cc4306ab345252bf740c20a1c6194929b0e/sfse/PluginManager.cpp#L51-L56) routes the interface to TaskInterface; [Hooks_Command.cpp](https://github.com/ianpatt/sfse/blob/48535cc4306ab345252bf740c20a1c6194929b0e/sfse/Hooks_Command.cpp#L21-L46) drains the queue in the command-processing hook, with no thread-ID check there. The approved header's main-thread description was contrasted with actual A0/A0C thread IDs and the loader's main-thread ID. No source code, hook or address was copied/adapted. This supports recording a discrepancy, not asserting complete installed-binary scheduler semantics. See [review14 run](experiments/EXP0002-review14-run.md). An attempted Hooks_Threads.cpp URL returned no source and supplied no evidence.

Microsoft Learn references consulted 2026-10-06: [DebugActiveProcess](https://learn.microsoft.com/en-us/windows/win32/api/debugapi/nf-debugapi-debugactiveprocess), [SetThreadContext](https://learn.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-setthreadcontext), [DebugSetProcessKillOnExit](https://learn.microsoft.com/en-us/windows/win32/api/winbase/nf-winbase-debugsetprocesskillonexit), [WaitForDebugEventEx](https://learn.microsoft.com/en-us/windows/win32/api/debugapi/nf-debugapi-waitfordebugeventex). Used to document debugger suspension/context, attach breakpoint, no-kill policy and timeout behavior. Documentation is not proof of target behavior; live attach was not tested.

SOR-S-0117 extension, 2026-10-07: Microsoft Learn [WaitForDebugEvent](https://learn.microsoft.com/en-us/windows/win32/api/debugapi/nf-debugapi-waitfordebugevent) and [ContinueDebugEvent](https://learn.microsoft.com/windows/win32/api/debugapi/nf-debugapi-continuedebugevent) handle ownership/cleanup documentation informed correction of premature event-handle closure in the disposable adapter. Read-only API documentation; no example implementation copied. Fresh C++17 builds use installed MSVC/SDK and system bcrypt; exact manifests and limits in the [adapter audit](audits/exp0002a-adapter-qualification.md).

SOR-S-0122 / SOR-S-0117 extension for SOR-D-0017: project0.1.1 changes the adapted maintainer core to freeze ownership at ARMED and leave later threads unarmed/untouched by debug-register retirement writes. Project-authored evidence latching and exact-handle recovery are documented in [the0.1.1 audit](audits/exp0002a-adapter-0.1.1.md). Microsoft Learn [TerminateProcess](https://learn.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-terminateprocess) and [GetProcessTimes](https://learn.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-getprocesstimes), consulted2026-10-07, inform asynchronous completion and creation-time verification. API documentation only; no example source or new dependency incorporated. Sibling commit/source hashes and SFSE permission boundaries are unchanged.

SOR-S-0117 extension,2026-10-07 / SOR-EV-0007: installed Microsoft CDB/dbgeng10.0.19041.5609 used separately for offline minidumps, with local-only symbol/image paths. Windows SDK10.0.26100.0 `um/minidumpapiset.h` (MINIDUMP_HEADER, exception/thread/module/memory/misc streams) and `um/winnt.h` (AMD64 CONTEXT) consulted as format declarations for the independently authored bounded Python reader. This is source-informed format research, not clean-room work; no Microsoft example/header/implementation was incorporated or redistributed. No new sibling tooling reuse or third-party dependency. Exact installed tool/header hashes, raw output and dump offsets remain in the ignored comparison bundle. [Analysis](audits/exp0002a-crash-dump-comparison.md).

SOR-S-0117 / SOR-S-0123 extension,2026-10-07: final EXP0002A uses installed CDB/dbgeng10.0.19041.5609 and Microsoft documentation for bp /1, qd and -pd. Ghidra12.1.2 local-dbgeng-attach.py and ghidradbg/methods.py were inspected as capability references only; no implementation copied. The direct engine console avoids a new Trace RMI/agent integration for this single test. Project-authored deadline guard0.1.4 uses installed OS APIs and Python standard library; no new dependency or sibling reuse. [Backend rationale and exact references](audits/exp0002a-final-software-attempt.md).

### SOR-S-0113 extension — Structural containment, 2026-10-08

Installed CPython 3.14.3 and standard-library zlib `1.3.1.zlib-ng` used separately for SOR-EXP-0005's hash verification, existing bounded BCPS transform, pointer/count/length probes and numeric summaries. Original project-authored code only; no implementation/examples/dependency copied or downloaded. Prior SOR-S-0103 / SOR-F-0004 supply independently inspected beacon/storage definition comparisons, not save-tag authority; no xEdit execution or new ESM inspection in this pass. [Report](experiments/outpost-save-structural-containment.md). No external source consultation/contact or additional permission basis was needed.

### SOR-S-0124 — Prior unreviewed mature-save exploratory research

Project/maintainer-directed Codex exploration, `.local-work/mature-save-offbook/`, preserved unchanged on 2026-10-08. Supplies prior discovery of the mature envelope/count grammar, base/prefix windows, name-index subunits, beacon-association pattern and cargo-reference methods. These are hypotheses and source-informed methods; the previous chat summary is not validation. The entire original workspace is hashed in `.local-work/mature-save-validation/before.json`; every exploratory script hash is in final inputs-before/after manifests. Only `local_decode.py` is imported/executed; no exploratory driver is rerun. The new validator conceptually reimplements count/window/name/graph methods and independently challenges them, with a separate physical-stream/count audit. No third-party material/dependency was incorporated or outside service consulted. [Exact provenance and results](experiments/mature-save-outpost-validation.md); SOR-P-0002 maintainer-owned exception remains distinct from execution/publication scope.

SOR-S-0113 extension — SOR-EXP-0006: installed CPython 3.14.3 and standard-library zlib facilities perform bounded offline transforms, hashing, synthetic tests and local review exports. No runtime implementation, example code or dependency was copied/downloaded. Prior SOR-S-0103/0104 static marker/keyword definitions inform arithmetic/type comparisons, not a universal save-tag schema. Existing separate-tool credit applies.

### SOR-S-0113 / SOR-S-0124 extension — Historical inventory, 2026-10-09

[SOR-EXP-0007](experiments/historical-save-inventory-triage.md) uses installed CPython 3.14.3/stdlib zlib separately, project-owned SOR-EXP-0003/0005/0006 directory/grammar/string/window methods and preserved prior exploration as credited source-informed research. Exact imported-script/tool hashes are in the local scan provenance. No outside parser, copied example, new dependency, tool download or external consultation. Prior Bethesda save inputs and xEdit-interpreted definitions retain SOR-S-0103/0104 attribution; header metadata is observed save content, not a measured originating executable. The local offbook decoder was consulted, not imported/executed by this inventory. Separate post-freeze location fallback and float probes remain hypotheses.

### SOR-S-0125 — TheDailyXPerience launch-era save package

2026-10-09: [Nexus listing 1798](https://www.nexusmods.com/starfield/mods/1798), author/uploader TheDailyXPerience; [files tab](https://www.nexusmods.com/starfield/mods/1798?tab=files), large first-playthrough package. Operator-supplied `Over 110 saves-1798-1-1694378623.7z`, SHA-256 `9b8bd55553c8e21f97a88d201a06aa870dd77a476f76cef69041176cf71b9093`, 867,429,978 bytes. Supplies observational inputs for [SOR-EXP-0008](experiments/launch-era-third-party-save-corpus.md), not source code, controlled causality or author endorsement. SOR-P-0003 records local examination authority, restrictive panel/broad prose ambiguity and raw redistribution exclusion. Cached web description/file sections and retrieval limitations are indexed in ignored `permission-reference.json`; a live-current permission snapshot remains required before publication. All source saves, archive and substantial extracted payload remain LOCAL-ONLY; independent summaries REVIEW-REQUIRED.

### SOR-S-0126 — Installed 7-Zip separate extraction tool

Igor Pavlov and 7-Zip contributors; installed 7-Zip 22.01 x64 (2022-07-15 build banner), executable hash/size and complete technical listing retained in SOR-EXP-0008 local provenance. Used solely to list and extract the operator-specified archive under the invoked brief's execution authority; no install/download, implementation copying, dependency incorporation or tool redistribution. Archive member CRCs/sizes checked independently after extraction. This tool's availability or terms do not clear source-save redistribution.

SOR-S-0113 / SOR-S-0124 extension — SOR-EXP-0008 reuses project-owned historical/mature framing, directory, string, reference and window methods unchanged, with exact script hashes in scan-03 provenance (repository starting HEAD `231786cc8c4c39b2defe706d2b9fe1c5344821f5`). CPython 3.14.3/stdlib zlib supplies separate installed runtime/compression facilities. SOR-S-0103/0104 retain prior definition-comparison credit. New intake/independent audit helpers are project-authored; no third-party parser code incorporated.


### SOR-S-0127 — Installed retail save loader and workshop/Almanac native evidence

Bethesda Game Studios; existing SOR-ENV-0001 pinned Starfield1.16.244.0 executable, SHA-256 `7e9adb1414a8e1b325e5e1f097b9b17b78deb7eebeda37a333351a43a60f9d28`. Source-informed local read-only static inspection for [SOR-EXP-0009](experiments/active-outpost-identification.md): record/count readers, initial-data selector, reference/string queues, named form-state callbacks, ExtraWorkshop load dispatch, registry insertion/removal and Almanac consumer. Exact addresses/local export hashes are retained in the evidence package. Proprietary code/decompilation remains ignored and LOCAL-ONLY; no implementation text was copied into project code. Original parser logic expresses observed framing/field semantics and preserves provenance. Existing Ghidra/JDK separate-tool credit applies; no new tool/dependency installed. Prior SOR-S-0103/0104 definition/script evidence, SOR-S-0124 project methods and SOR-S-0113 installed Python/stdlib remain credited. Donor inputs retain SOR-S-0125 / SOR-P-0003 limits. No external consultation/contact, fork or PR.


### SOR-S-0128 — Installed faction beacon definitions and quest/script leads

Bethesda Game Studios, locally installed Starfield.esm, SFBGS050.esm and SFBGS050 - Main.ba2, inspected read-only for [SOR-EXP-0010](experiments/active-outpost-membership-completion.md). Original bounded ESM/group/subrecord reader observes beacon ACTI/REFR definitions and exact source hashes; focused QUST/VMAD and BA2/PEX probes preserve quest FormID, alias and activation-blocking leads. Complete proprietary payload/native decompilation stays ignored LOCAL-ONLY; no implementation text/example/third-party parser/dependency is copied or redistributed. Installed content is not a historical save-era snapshot or complete override merger. Maintainer's Terran Armada quest hand-in explanation and edge-case deferral are SOURCE-REPORTED evidence, durably retained in SOR-D-0026, not independently validated gameplay. Prior native reader evidence SOR-S-0127, project methods SOR-S-0124, Python/stdlib SOR-S-0113, installed Ghidra/JDK and donor SOR-S-0125 / SOR-P-0003 retain credit and restrictions. No outside lookup/contact or changed permission basis. [Exact identities and review](experiments/active-outpost-membership-completion/validation.md).
