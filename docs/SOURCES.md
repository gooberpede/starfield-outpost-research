# Source Register

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
