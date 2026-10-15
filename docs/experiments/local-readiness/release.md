# Concrete pre-live release identity

**UNADOPTED HISTORICAL CANDIDATE — NO-GO.** Exact artifact hashes below are preserved, not reissued. [Scientific reassessment](scientific-value-reassessment.md) rejects the proposed live experiment; the plugin and run card remain unapproved. Documentation corrections do not update historical build-source pins.

Version **0.8.0**, session/event schema 8, retail 1.16.244.0; **not deployed**.
This was the candidate for [the proposed operator card](run-card.md). The
scientific-value recommendation is now NO-GO. No new live findings are available.

| Artifact | SHA256 |
|---|---|
| Starfield.exe | `7e9adb1414a8e1b325e5e1f097b9b17b78deb7eebeda37a333351a43a60f9d28` |
| SFSE runtime 0.2.21 (Windows file version 0,0,2,21) | `28c5bda41d9959c885efcb6e889de69e92767c80a1a66842d711d215f722f82b` |
| SorNativePositionOracle.dll | `72832b1787f4c25cc41ef32d49c69a0194db6a046e8d653cbf393ccf43fc70e8` |
| SorNativePositionOracle-0.8.0.zip | `eb97cd993dcad87bbaef468a9985a798485538fe8116b1d7d041037a907f3fe6` |
| build.json | `9dd33c88b906621953c3d0609af9c212e034710e1ffe6356a37395473bd4e242` |
| private future plan.json | `c7f3a14dc2fb92514b7caa02c615e135cfcbc7125a27e42db0b565e3685cb7ed` |
| sfse_loader.exe | `16916c2ec47e31774e3d550609a1844fcb368b03060c03511891564b7f5f7526` |

Local build directory:
`.local-work/local-readiness/builds/qualification-03/`.
Vortex ZIP is in that directory. Private future plan is
`.local-work/local-readiness/plan.json`; `deployed:true` means future prelaunch
requires an actual effective deployment, not that deployment has occurred.
No actual prelaunch/live command has been executed with that plan.

Exact ZIP members (all decompressed bytes compared with package source during build):

| Member | Bytes | SHA256 |
|---|---:|---|
| `Data/SFSE/Plugins/SorNativePositionOracle.dll` | 13855744 | `72832b1787f4c25cc41ef32d49c69a0194db6a046e8d653cbf393ccf43fc70e8` |
| `ResearchNotices/PROJECT-LICENSE.txt` | 35149 | `3972dc9744f6499f0f9b2dbf76696f2ae7ad8af9b23dde66d6af86c9dfb36986` |
| `ResearchNotices/README.txt` | 64 | `9e1048935d6bb6bbdbca170f93bf8f6b5854004e02e5169f519f8024e545c061` |
| `ResearchNotices/SFSE-PluginAPI-LICENSE.txt` | 1172 | `7795510c3ee9970b5843639d79b7ab6d87d1a14a1e110e92fd0b09ff0e7628da` |

Only the DLL is runtime-essential in Data/SFSE/Plugins. ResearchNotices contains
the approved SFSE interface notice, project licence and package review label;
these are package notices, not files required beside the deployed DLL. No raw
evidence, research documents, source, fixtures, PDB/object or build trees are in
the ZIP. Existing installed Microsoft runtime dependencies are required, not
bundled or downloaded. Exact imports:

`bcrypt.dll`, `MSVCP140.dll`, `KERNEL32.dll`, `VCRUNTIME140.dll`, `VCRUNTIME140_1.dll`, `api-ms-win-crt-string-l1-1-0.dll`, `api-ms-win-crt-heap-l1-1-0.dll`, `api-ms-win-crt-stdio-l1-1-0.dll`, `api-ms-win-crt-filesystem-l1-1-0.dll`, `api-ms-win-crt-locale-l1-1-0.dll`, `api-ms-win-crt-runtime-l1-1-0.dll`.

External runtime pins in build.json include the actually installed System32
MSVCP140/VCRUNTIME140/VCRUNTIME140_1/ucrtbase files. Exact compiler/MASM/linker/
dumpbin and vcvars hashes, 13 guarded CALL preimages/windows, target hashes and
source hashes are retained there. Compiler report: MSVC 19.51.36256.0, x64;
SFSE runtime file version was read locally as 0,0,2,21, separately from its hash.

Protected input pins: **6847**, checked before/after the build.
Final build caller-available bytes: C:/=94036426752, D:/=117667311616.

The one compiler warning is expected alignment padding in Environment (C4324);
no compile/test error is waived. No retail timing/ABI guarantee follows from
these fixtures. Shared wrapper/plan hashes and the historical review manifests
identify the earlier reviewed source revision, which was never user-approved.
They do not qualify later documentation edits or authorize a rebuild.

The prose-only correction changes README documentation bytes, including a README
listed in the historical source manifest. That manifest is preserved unchanged
and must not be presented as a full pin of the corrected working tree. The old
README bytes and task snapshot are retained under
`.local-work/local-readiness-reassessment/before/`; code, DLL and ZIP bytes remain
unchanged. No pins were replaced, and no rebuild or renewed qualification occurred.
