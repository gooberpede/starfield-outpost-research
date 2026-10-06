# Provenance and Environment Baseline

## Scaffold provenance

Prepared on **2026-10-01** at the user's request, using the supplied reference-handle scaffold as an organizational reference and the agreed broader outpost-systems remit.

| Input / material | Provenance |
|---|---|
| Reference archive | `starfield-reference-handles-scaffold(1).zip`, supplied by the user |
| Reference archive SHA-256 | `9999f2efb4a0f7c0ca6011c3c9317777dc347ac850e0bee972e3b9909637031f` |
| Applied contribution | Directory pattern; durable research/agent records; local-only analysis artifacts |
| Not adopted | Reference-handle findings/hypotheses, executable/tool hashes and versions, machine paths, debugger success claims |
| Earlier save-only brief | Superseded by the runtime-and-persistence scope and direct-scaffold request; not an active repository brief |
| Included `LICENSE` | Verbatim `/usr/share/common-licenses/GPL-3` from the preparation environment; 35,149 bytes, 674 lines |
| `LICENSE` SHA-256 | `3972dc9744f6499f0f9b2dbf76696f2ae7ad8af9b23dde66d6af86c9dfb36986` |

The licence file is the complete GNU GPL version 3 text, carrying the Free Software Foundation's notice. Its title, permission notice, sections, and version-choice meaning were checked against the [SPDX entry](https://spdx.org/licenses/GPL-3.0-or-later.html). Direct GNU retrieval failed during preparation; do not claim those bytes were freshly downloaded from GNU. See [LICENSING.md](../LICENSING.md) and source `SOR-S-0002`.

Read-only GitHub checks during preparation identified `gooberpede/starfield-outpost-research`, private visibility, `main` as default branch, and no branches. This is a setup observation, not a guarantee of future state. No remote changes were made.

## Historical scaffold baseline: not yet established at 2026-10-01

Do not fill these fields from the example project. Use a new `SOR-ENV-` record when the actual environment is inspected. `UNKNOWN` is deliberate, not an invitation to guess.

| Field | Current value |
|---|---|
| Game edition/distribution | UNKNOWN |
| Executable product/file version, size, SHA-256 | UNKNOWN |
| Installed/working-copy equality | NOT CHECKED |
| Save format/container versions | UNKNOWN |
| DLC, plugins, load order, mod-manager profile | UNKNOWN |
| Operating system / architecture | UNKNOWN |
| Ghidra version, analysis options, language/compiler ID | UNKNOWN |
| Actual static image base / executable module | UNKNOWN |
| Debugger/backend versions and attach qualification | UNKNOWN |
| Python or other analysis runtime | NOT SELECTED |
| SFSE/native instrumentation/version/hashes | NOT SELECTED |
| Save samples and independent ground truth | NOT REGISTERED |

Record exact paths locally where needed. In durable/public records use portable placeholders such as `<starfield_executable_path>`, `<analysis_project_path>`, `<local_evidence_root>`, and `<sample_path>`. The scaffold referenced operational setup instructions in `GIT_SETUP.md`; that file is absent from this checkout. Current local helper paths are operational inputs, not release clearance.

## Baseline and sample records

For each baseline record observation time/timezone, observer, executable/module names and hashes, versions, distribution, load order, tool/script versions or commits, analysis options, read/write effects, source/permission IDs, and uncertainties. Distinguish reported values from independently read/hashed ones.

For each `SOR-SAMPLE-` record the original byte hash and size, origin and owner consent, game/build/save versions, plugin set, controlled actions, parent/control sample, time/loading conditions, local locator, and publication classification. Raw save filenames can reveal personal information; prefer neutral sample IDs in Git.

Keep immutable originals local. For decompression, normalization, redaction, or extraction, record each transformation and input/output hashes separately. Cross-link [experiments](experiments/README.md), [evidence](experiments/evidence/README.md), and [the evidence standard](EVIDENCE_STANDARD.md).

## SOR-ENV-0001 — Initial static reconnaissance, 2026-10-06

Observer: Codex, authorized by SOR-D-0009. Dates use Australia/Sydney; shell/tool logs may use UTC and must not be interpreted as local without conversion. Evidence root `<local_evidence_root>` is the ignored `.local-work/recon/` directory. `baseline.json` retains exact local locators. Independently read version resources, lengths, SHA-256 and PE32+ preferred image bases without executing game/CK. The directory is a Steam installation; actual running distribution/module state is NOT CHECKED. No save samples registered or opened.

| Input | Version / bytes | SHA-256 | Status |
|---|---|---|---|
| Installed and pinned Starfield.exe | 1.16.244.0 / 102476200 | `7e9adb1414a8e1b325e5e1f097b9b17b78deb7eebeda37a333351a43a60f9d28` | Independently hashed equal |
| Installed and pinned CreationKit.exe | 1.16.244.0 / 239885664 | `ed54e4906bc13b0fbc43ec7624fec4af2389a9a1e12b2789d73c5617f5a14020` | Independently hashed equal |
| ContentResources.zip | 163283936 bytes; archive release version UNKNOWN | `b5f3f66d6041193c2db139c50a8a4a2da7a80c862a95ba5eec929c7a2c42983c` | Installed CK development archive; not presumed PEX-identical |
| Starfield.esm | 1457098709 bytes | `1dabed00c3f4282dd3bb54d2e9601e40b577d8742d078b7ccef203adbfef0da7` | Independently hashed; static definitions input |
| sfse_1_16_244.dll | PE resource 0.0.2.21 / 116216 | `28c5bda41d9959c885efcb6e889de69e92767c80a1a66842d711d215f722f82b` | File only, no load/attach qualification |
| sfse_loader.exe | PE resource 1.1.1 / 68600 | `16916c2ec47e31774e3d550609a1844fcb368b03060c03511891564b7f5f7526` | Not equated to runtime API or sibling bootstrap version |
| xSF1Edit64.exe | PE resource 4.1.5.0 / 37490176 | `dff26145431e06ad849532a5b01ebf60bc2fe1eb7e4986ba9c0c9ac43666163c` | Installed directory/log identify 4.1.5p |
| x64dbg.exe (x64) | PE resource 0.0.2.5 / 207776 | `68d6afc2cc5a5bfd74a1b4066c0651254661355a0e384524cd1a8772adb95092` | Snapshot date UNKNOWN; not executed |

Both game/CK preferred image bases are `0x140000000`; these are static PE values, never runtime ASLR bases. Ghidra import metadata independently reports the matching executable hashes and image bases. Programs: project `Starfield`, program `/Starfield.exe`; project `StarfieldCK`, program `/CreationKit.exe`. Language `x86:LE:64:default`, compiler spec `windows`. Prior analysis options/coverage UNKNOWN; no new analysis permitted.

Ghidra `application.properties`: 12.1.2 PUBLIC, build 2026-06-05, revision `c0f584bf229fffba61b36431f3ce30c0c3e4e682`. Host Windows build `10.0.19045`, X64. Existing JDK path identifies 21.0.12.8; exact JDK binary hash NOT CHECKED. Tool paths remain in local baseline/launcher. SFSE README reports 0.2.21 pre-alpha and 1.16.244 compatibility (SOR-S-0112); these are consistent with independently read game/DLL resources and sibling report, not a live compatibility test.

`plugin-inventory.json` inventories installed ESM/ESP/ESL names/sizes. Includes Starfield, ShatteredSpace, BlueprintShips and SFBGS/SFTA masters plus ResourceGenerationTest.esp. Local `Plugins.txt` lists starred SFTA/SFBGS content and an unstarred experimental ESP. This is a file observation, not a complete resolved runtime load order or a verified Vortex profile. Do not label this an unmodded live baseline. No configuration edited.

First Ghidra batch launch and a settings-override retry failed before program inspection because LaunchSupport could not write its existing user Java preference. Direct JVM launch using installed launcher VM settings, a private settings/cache root and `-readOnly -noanalysis` succeeded. No global settings edited. `ghidra-before.json` hashes 37 project/database files; preservation is reported in the audit. Original helper and bounded exports are described in [ghidra/scripts/README.md](../ghidra/scripts/README.md). Sibling environment documentation (SOR-S-0111) was a locator only; no sibling hashes or function semantics were accepted without direct checks.
