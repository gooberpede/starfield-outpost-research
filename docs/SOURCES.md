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

No third-party outpost claim has been promoted to a finding and no code reuse approval exists. Prior conversation citations and summaries must be checked before use. Add other sources only when actually consulted or deliberately registered as a lead; do not populate a ceremonial list of tools never used.

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
