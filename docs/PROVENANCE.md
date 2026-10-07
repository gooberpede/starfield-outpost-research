# Provenance and Environment Baseline

## SOR-SAMPLE-0023–0028 — Output-link validation, 2026-10-07

L0C=0023, L1=0024, L1C=0025, L2=0026, L2C=0027, incidental exit=0028. L0 reuses S4C/SOR-SAMPLE-0015, not a new sample. Six new copies and the historical archive match their originals by SHA-256/size before analysis and at final verification. Exact private source/copy locators and filesystem metadata: `.local-work/output-link-L0-L2C/manifest.json`; [selected manifest](experiments/output-link-validation/manifest.csv). New archive `.local-work/savegames/output-link-L0-L2C/`. Original contents/mtime preserved, access-time behavior uncontrolled. Supplied brief's personal filenames remain an unresolved publication review item.

SOR-EXP-0004 / SOR-EV-0010 [report](experiments/output-link-validation-L0-L2C.md): reported reload between L0/L0C, then unlink/no-action/relink/no-action; no runtime observation by this task. All decoded headers report 1.16.244.0, not a measured originating executable/profile. Installed CPython3.14.3/zlib1.3.1.zlib-ng (SOR-S-0113); unchanged project decoder/diff reused from repository HEAD `268d4e1dfe67fa1cc5abe522a09bc6fe187d4a78`, exact file hashes in preregistration. New wrappers/probes are project-authored, no third-party parser source. Initial literal-signature failure preserved; exploratory token/framing correspondence recorded separately. Seven verified transforms/154 chunks; selected outputs REVIEW-REQUIRED, raw/bulk derivatives LOCAL-ONLY.

## SOR-SAMPLE-0006–0022 — Manual S0–S7C corpus, 2026-10-07

Sequential assignment: S0=0006, S0C=0007, S1=0008, S1C=0009, S2=0010, S2C=0011, S3=0012, S3C=0013, S4=0014, S4C=0015, S5=0016, S5C=0017, S6=0018, S6C=0019, S7=0020, S7C=0021, incidental exit=0022. User supplied exact filenames/actions and authorized copying plus offline analysis. All source/copy/source SHA-256 checks passed. [Selected manifest](experiments/manual-save-corpus/manifest.csv) retains sizes, times and original/decoded hashes; exact private locators are in ignored `.local-work/manual-S0-S7C/manifest.json`. Source files untouched; prior local copies preserved; fresh archive `.local-work/savegames/manual-S0-S7C/`.

SOR-EV-0009 / [experiment](experiments/manual-save-corpus-S0-S7C.md) records a single continuous session, nearly stationary actor, S5 actor movement, non-atomic S3 construction, uncertain S3/S3C combat and S7 cleanup confounds. Decoded version strings report 1.16.244.0; originating executable hash and actual loaded module profile were not independently acquired for this corpus. CPython3.14.3 with installed standard-library zlib runtime1.3.1.zlib-ng, SOR-S-0113; exact tool/script/transform hashes and chunk metadata local. Raw/decoded data LOCAL-ONLY, authored summaries REVIEW-REQUIRED. This sample set does not inherit old protected-parent semantics or establish reload behavior.

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

## SOR-ENV-0002 — EXP0002 offline preparation, 2026-10-06

Codex under SOR-D-0010 rehashed installed/pinned Starfield.exe and CreationKit.exe, installed SFSE loader/DLL and ContentResources.zip. All seven size/hash checks match SOR-ENV-0001; file versions are inherited only because byte identity was re-established. Actual runtime module base, plugin profile and ABI remain UNKNOWN. No game, CK UI, SFSE loader or debugger was executed. Existing Ghidra 12.1.2 read-only/no-analysis exports inspected only coordinate-related xrefs/two functions; database preservation in [SOR-EV-0002](experiments/evidence/exp0002-preparation/README.md).

Installed CPython 3.14.3 and standard library ran original offline metadata/hash/PE/ZIP/string and synthetic-contract checks (SOR-S-0113). Exact Python executable locator/hash and input locators remain in local evidence. No dependency install, build download or third-party implementation incorporated. No native plugin build/package exists; Python execution is not native observer validation. Current Ghidra import hashes still match both pinned executable hashes.

## SOR-ENV-0003 — EXP0002A mapping and debugger setup, 2026-10-07

Seven installed/pinned game/CK/SFSE/archive identities and protected Save3 original/backup match the historical baseline. Starfield1.16.244.0 SHA-256 remains `7e9adb1414a8e1b325e5e1f097b9b17b78deb7eebeda37a333351a43a60f9d28`. Ghidra12.1.2 read-only/noanalysis exports; existing Starfield project15-file preservation checked separately. No CK database accessed. CPython3.14.3 and installed MSVC/Windows SDK built/executed the original synthetic fixture; no new package/dependency installation.

Installed x64dbg headless source revision label `9c8ca1cae0b6d56cc44f31fddcb10e3b02ffbb87`; headless.exe SHA-256 `44ece2d8f81c1acbf4c85b45fe89e11875f0e1a0d2ba0c8c8c1a56bf85164268`, x64dbg.dll `dc9d5ff18d6e5fc9d667a2c2bc8fa9cce15fa5e0da9728222259a4525d542c0f`, x64bridge.dll `39730aea3509e275bc2d69d8d27f22695821b7caffa30943fa0dcf36f9f558cd`. This is installed-tool identity, not source/binary reproducibility. No debugger plugin autoload found. Each run uses isolated settings and local databases.

User ready at ordinary New Save after requested SFSE-profile/parent workflow. Live PID20804; observed image base `0x00007ff60a5b0000` in manual-002. No SFSE research observer deployed; plugin directory contained only Vortex's folder marker. Actual loaded SFSE module and four32-byte code sites were checked in manual-002. Restricted attach failed; elevated-context attempts attached, then detached. Default TLS breakpoint side effects and subsequent no-pause failure are retained, not successful save traces. Final live status/parent preservation and local hashes: [SOR-EV-0005](experiments/evidence/exp0002a-static/README.md), [report](experiments/SOR-EXP-0002A-native-save-thread-mapping.md). No live save-call ABI/thread or safe query context established.

## SOR-SAMPLE-0001 — Immutable pre-outpost parent

Owner-supplied Save3; original and existing backup independently compared byte-for-byte and hashed under the invoked brief. Both 2,096,496 bytes; SHA-256 `d06123ee32bd5b3e244650852fac9714697a19fd6243384966414d1d1f4ffbfe`. Exact filenames/paths/last-write timestamps remain in local `integrity-before.json` and `integrity-after.json`. Parent/backup last-write timestamps differ; bytes agree. Only hash/metadata/byte comparison performed, no save semantics inspected. Final preservation result is in SOR-EV-0002.

Planet/body Kreet, outpost none, buildable-site position and inventory are USER-REPORTED until live confirmation. Originating game build, save format and loaded profile UNKNOWN. Parent role: immutable pre-outpost baseline. Publication: LOCAL-ONLY. A0/A0C/A1/A1C/A2/A2R aliases in the plan do not identify already-created artifacts. No other save accessed in this preparation.

### SOR-ENV-0002 continuation — original native preparation

SOR-D-0011 corrects the premature initial stop. Original observer and diagnostic were built offline using installed VS 2026 Community 18.9.0, MSVC 14.51.36231 (compiler 19.51.36256), Windows SDK 10.0.26100.0 and CPython 3.14.3. Exact compiler/linker/source/DLL/EXE/package hashes and build logs remain in the ignored review build manifest. SFSE PluginAPI.h is the one approved MIT incorporation (SOR-P-0001); SFSE runtime external, no CommonLib/Address Library linking, sibling code copying or download. Additional read-only Ghidra exports independently checked callback/transform/cell operands; the earlier coordinate-only scope description is historical. Final 77-file project comparison and parent/build rechecks are in SOR-EV-0002. Runtime module base/profile/ABI still UNKNOWN. Native test DLL loaded only in its synthetic test process, never Starfield.

### SOR-ENV-0002 live extension — review14 primary controls

2026-10-06, SOR-D-0013 / SOR-EV-0004. The review14 DLL and configuration were independently matched to the approved ZIP after user-managed Vortex deployment. Protected parents, pinned game/SFSE and package/source identities passed preflight. Vortex profile Starfield - SFSE and SFSE-only additional mod are USER-REPORTED; file/config snapshots and 61-entry startup module snapshot are local evidence, not resolved runtime winning-definition proof. Loaded game base observed as 0x00007ff62bcf0000, observer hash `9a1636adacdcd0967e7873fcdbc161fed04876d3c368f9e37735f707e9e191ed`. A0/A0C capture IDs and SFSE logs show differing task execution threads; native query safety remains unqualified. No debugger attached.

### SOR-SAMPLE-0002 / SOR-SAMPLE-0003 — A0 and A0C controls

Owner-operated ordinary new manual saves during the review14 attempt. Logical aliases SOR-SAMPLE-EXP0002-A0 and SOR-SAMPLE-EXP0002-A0C. Parent lineage: immutable SOR-SAMPLE-0001 to A0, then no-deliberate-action A0C. User confirms Kreet, no construction and settled controls; captured raw player/cell/world values match within the non-atomic views. Raw saves are LOCAL-ONLY; no format/semantic analysis. A0: 2,082,992 bytes, SHA-256 `7d25e02cc0ac4bc81ab7d966a73c84ade0c6c795d154aa625d85b0aaf259fa66`. A0C: 2,066,048 bytes, SHA-256 `875f2e8460d3e5adfdfc15de860a57b991139195905ffff461c43fdf59409d0c`. Exact private filenames/timestamps and source/copy/source hash checks are in local post-exit.json; A0C/exit-save correlation and its initial ambiguity are retained. No save patched or overwritten by the researcher; protected parent/backup unchanged. See [run record](experiments/EXP0002-review14-run.md).

### EXP0002A disposable adapter qualification

SOR-D-0016 / SOR-S-0122: four fresh disposable attachments, no game/save access. Installed MSVC/SDK built the original fixture and maintainer-core adapter; source/binary hashes, command logs, raw JSONL and failed source snapshot remain under .local-work/exp0002a-adapter. [Audit](audits/exp0002a-adapter-qualification.md) distinguishes the handle-ownership failure, subsequent passing existing-thread/timeout controls, and failed new-thread retirement/health. No engine confidence upgrade or Stage-C authorization. Raw evidence/binaries remain local-only; authored summaries and code remain review-required.

### EXP0002A adapter0.1.1 qualification and prior-process closure

SOR-D-0017: USER-REPORTED manual termination of failed0.1.0 disposable PID16100 after review; no agent cleanup action or process lookup for that PID. The old evidence/source/build receipts remain byte-preserved and the dynamic-new-thread failure remains failed. New0.1.1 evidence lives separately under .local-work/exp0002a-adapter-0.1.1. Three focused controls passed: fixed-population capture, unarmed-new-thread NO_HIT, and explicit disposable-only post-flush retirement-fault recovery. Native data completeness, cleanup and target outcome are separate fields. [Identity, exact hashes, limitations and review](audits/exp0002a-adapter-0.1.1.md). No new engine finding or game/save access.

### SOR-SAMPLE-0004 — S0 no-debugger control

2026-10-07: PROJECT-VERIFIED RUNTIME control performed by the project operator, ordinary Steam without SFSE, Save3 parent, New Save confirmed once, automatic return to gameplay, normal exit and completed sync. Codex independently archived Save6: 2,082,128 bytes, SHA-256 c40fbd2d22c81edacdb7fde5a7f68658dc3b559f4ac0aec731660bf5dd6bc94c, last-write UTC 2026-10-07T02:12:02.871840Z. Incidental exit save: 2,082,432 bytes, SHA-256 57cd8388fa13237c4573e682eff550af18024282af361897ba12608bb9efd4df, last-write UTC 2026-10-07T02:12:15.713587Z. Source/copy/source hashes secured before exact experimental Save4/5/6 cleanup. Raw saves/private paths remain ignored. [S0 scope and limits](experiments/EXP0002A-S0-control.md); corrected local archive index excludes accidentally copied unrelated history. No save parsing/reload verification.

### SOR-SAMPLE-0005 — S1 debugger-only save control

PROJECT-VERIFIED RUNTIME S1 pass: new Save7 created during the active no-DR0 window; user returned to gameplay, confirmed delayed responsiveness, normal exit and completed sync. Archived2,079,808 bytes, SHA-25619b88ea38a1e13893b2dda53d0eb07a13288c161b864e0f1408a9e022adec6c6, filesystem last-write2026-10-07T04:27:58.404317Z. Exact paths/incidental exit save and source/copy/source receipts stay local in s1-live-01/outcome.json. S2 produced no newly visible save and no native request contract. [Control audit](audits/exp0002a-adapter-0.1.3.md).
