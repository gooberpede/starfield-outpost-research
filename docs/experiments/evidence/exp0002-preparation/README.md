# SOR-EV-0002 — EXP0002 offline preparation evidence

Date: 2026-10-06 Australia/Sydney. SOR-EXP-0002 / SOR-ENV-0002 / SOR-SAMPLE-0001. Authored index REVIEW-REQUIRED; all listed artifacts LOCAL-ONLY. No live/save semantic evidence, raw sources, native bytes or decompilation is incorporated here. Locators are relative to ignored `.local-work/`.

| Artifact | Bytes | SHA-256 |
|---|---:|---|
| exp0002/checkpoint-templates.json | 24300 | `bf3e4d56df7449b1c25d8723981a2a07957a4a9807e1948ded1cfc195b361035` |
| exp0002/coordinates-focused.json | 12582 | `8928f013de0c91203adbeed4beb38052668ab8c6f4a376b93bc1106a39eb22f8` |
| exp0002/coordinates.json | 41537 | `f47bae9352e671207a687a75ad73518cc1db80e64c14c547f591ea7153191b4f` |
| exp0002/ghidra-after.json | 16695 | `52e06b2eb9d2edba1b39ff33cdd9b48dca053c56a1e43e15c2cb7b2f7f63fd91` |
| exp0002/ghidra-before.json | 16695 | `52e06b2eb9d2edba1b39ff33cdd9b48dca053c56a1e43e15c2cb7b2f7f63fd91` |
| exp0002/integrity-after.json | 3864 | `6840e4194104a7b7f6549154ea763779d55da84d779956faa7269594be2b8baa` |
| exp0002/integrity-before.json | 3864 | `fc7fbec57c1eb1e399c96914877b90ce2242692ee5ea5916b895914cc111c39b` |
| exp0002/pe-targets.json | 728 | `17f03f4089790c37b53ee0e49ffae2d1544fbe7862e4c87b0c394aca2c603f16` |
| exp0002/sample-manifest-template.json | 3894 | `7251b2c0fa3803e97081f7fca6041bae394a7b7636e0ae26436ca92a7142b783` |
| recon/exp0002-ck-coordinate-refs.tsv | 493 | `04152d62c5d5aec2329c896d85e4b8c363024bc25601efe4d61c7f7ae2e6a146` |
| recon/exp0002-coordinate-functions.tsv | 18328 | `67cd51046bf4e749fa140333116de5e2b821ca3591f83c9157d092a6b504f757` |
| recon/exp0002-coordinate-refs.tsv | 359 | `f334f5b545bf875936afd7e977b3fd7f1deba96a625adddbee69e94e8a305f4f` |

## Anchors and limitations

- `exp0002/integrity-before.json` and `integrity-after.json`: original/backup exact local locators, metadata, SHA-256, byte equality, seven executable/tool/archive baseline comparisons. Both original and backup size/hash/mtime remained unchanged across preparation. Metadata reads do not establish save format or originating build. Timestamps explicitly UTC.
- `exp0002/pe-targets.json`: independently hashed PE; callback RVA 0x02073cf0 at file offset 0x020732f0, tail RVA 0x00517d60 at file offset 0x00517360; 24-byte code ranges and relative-displacement results. Key global RVA 0x05f0b3d8 requires a runtime value, not disk-byte semantics. Initial rejected file-backed read corrected before successful output; no source mutation.
- `exp0002/coordinates.json` and `coordinates-focused.json`: exact input hashes, bounded raw ASCII/UTF-16LE matches, static VAs/file offsets and six script-entry hashes/line anchors. Broad scan can cap at 80 per encoding; focused scan records its own pattern. No complete absence claims.
- `recon/exp0002-coordinate-refs.tsv`: retail coordinate literal xrefs to functions 0x14167f7e0 and 0x14341c0a0; `coordinate-functions` has both instruction bodies and successful decompilations, no truncation markers. Decisive instructions 0x14167f82f–854 pass +0x68/+0x88 addresses and coordinate names. Units/types/authority unverified.
- `recon/exp0002-ck-coordinate-refs.tsv`: Location latitude/longitude label xrefs in 0x142b96190 and spinbox name xrefs in 0x1432018b0. CK function bodies not examined; no UI executed.
- Ghidra manifests: all 77 enumerated pre/post project files across the two existing project roots agree in path, size and SHA-256. This run's inventory scope differs from the earlier 37-file record; do not equate the counts. No project files were excluded by extension. Read-only exports do not prove pre-existing analysis correctness.
- Checkpoint and sample-manifest templates are PLANNED with no created saves or runtime observations. Local `tooling.json`, `tests.txt`, `validation.json`, `review.diff` and `status.txt` supply tool/script identities, offline checks and the complete review package; review exports are not evidence of semantics.

Reproduction: [offline tools](../../../../research/exp0002/README.md) and [experiment](../../SOR-EXP-0002-outpost-membership-reload-location.md). Ghidra used the existing reader and launcher unchanged: one Starfield reference query for each literal, one two-function export, one CK four-reference query; read-only/no-analysis. Proprietary outputs remain outside tracked evidence. Sources SOR-S-0103/0104/0105/0112/0113; no new code-reuse clearance.

## Continued native preparation — SOR-D-0011 / SOR-P-0001

This continuation supersedes the initial no-native-build/no-code-reuse statements above, while preserving their historical scope. Original observer and debugger built offline; sole incorporated code is the approved MIT SFSE header. Ghidra reader gained bounded windows/API mode; no analysis edits. The partial callback export is retained as PARTIAL, with corrected selection/final-contract exports used for missing sites. Exact contracts/limits in runtime/exp0002/STATIC-CONTRACT.md and the current audit. No runtime or persistence evidence.

All artifacts below remain LOCAL-ONLY, including compiled original tools and historical reports. REVIEW-REQUIRED authored index is not approval to publish these outputs.

| Artifact under .local-work | Bytes | SHA-256 |
|---|---:|---|
| exp0002/tooling-resumed.json | 591 | `9bc6b0eb85136d9904ec35f6e7ac6b770b58c99f22296840aa2f2ad16453610f` |
| exp0002/guard-smoke.txt | 383 | `ccdd69bc09444ef61cf7ed430edc8c95de50d0af4ac6d706bbe46ee759428570` |
| exp0002/integrity-resumed-final.json | 3864 | `5c6ac006677d2a1b548e4447ae0e19470ce7a91bf48fc7d13d6ec5ab7315bd5e` |
| exp0002/ghidra-resumed-final.json | 16697 | `7e973f2b6b17818849bcb1ef399fa39659e4cb7e34dd19158084bbae52ba1b5d` |
| exp0002/pre-continuation-report.md | 21245 | `0d449ff31c5d8a3cb55608d5e895f12e9af59c86675139f2fbfc8716caea7e31` |
| exp0002/pre-continuation-audit.md | 6064 | `2fc4caad23a8a58f8d5b5bc1e537a7a9233e34387bffb3b0568848d7f3014ef9` |
| recon/exp0002-observer-interfaces.tsv | 1509 | `f283fcb149cbe77d42c79365f003aae6807953dd980e361905912cb8db971bfd` |
| recon/exp0002-registration-windows.tsv | 17922 | `bda9fcc49aa5adde6fd1f9c1a58a709283a1049409e9703f93a253d79d3c004a` |
| recon/exp0002-observer-callbacks.tsv | 6551 | `a934266fc895b21c337d2a323d307c51ecd5bd3762a7f70415a7b27e91bcbc66` |
| recon/exp0002-selection-sites.tsv | 47848 | `1f2d830b761dcd72ce719f22509f3670e1acb41b3106b9c74347675e833225f9` |
| recon/exp0002-final-native-contract.tsv | 11138 | `9c915f24f6df1cfaa12c34385e3bfdf59b9fe605a7d410c4b5f370ac5b126d93` |
| exp0002-builds/review08/build.json | 7262 | `c9e2e04ee1506afbdeac8ca28860d376f7dd5ec9643d1ce3b0a9660c6e39628c` |
| exp0002-builds/review08/site-guards.json | 3423 | `19a5179830331e1c05730dd1363c64bcc0faf2fb7f02e92cceacc0ebf9f2ee37` |
| exp0002-builds/review08/observer-build.txt | 1716 | `1dab7cf45e387afdee8e13d52f97d201bcb4fc828578b38a377c2077db1855ba` |
| exp0002-builds/review08/trace-build.txt | 1651 | `737783c37f4a04abd6ad4b5b567e3091e19d7d24a4ed628979586b5545feed96` |
| exp0002-builds/review08/tests-build.txt | 1651 | `9c31e18df43c09a1c7e850649a3d3464a8e5d8e3ec485b639bd513adcbde9682` |
| exp0002-builds/review08/tests.txt | 62 | `7e0a5897fde9696e9fac979d14ea0a6fe99a0fa7663ee42ffb2b06001f5a5369` |
| exp0002-builds/review08/output-tests.txt | 74 | `13e7f304c97e7a6992e2ab03794a49e5eb33559882f1fc86e81d93f44c13edb6` |
| exp0002-builds/review08/SorExp0002.dll | 141824 | `af56282184fdbdb89df1f7c3cbfcc960136758dfb7ee53d6f137daf0618047de` |
| exp0002-builds/review08/workshop-trace.exe | 98816 | `7e6936caa7a943130604eb04d96d48e438cd768277b3b83b8e6bf9aa20f6acdd` |
| exp0002-builds/review08/SorExp0002-local-test.zip | 75700 | `0be4ee9aa3b3ceb61a0e27b40477f0adaf6beb20005fddc615aae6be62a6f81e` |

## READY correction review build — 2026-10-06

User-scoped initialization/publication fix and offline tests only; no new game/save/static research. This build supersedes review 08 for future package review; earlier artifacts remain historical, not deleted. Its temporary manual deployment proposal was never executed and is now superseded by exclusive user-managed Vortex deployment; nothing deployed. All artifacts below LOCAL-ONLY. See the updated audit for scope and limits.

| Artifact under .local-work | Bytes | SHA-256 |
|---|---:|---|
| exp0002-builds/review09-ready-fix/build.json | 7572 | `d553962ff921b56ca6df5527adfa33fb87d4525a7981baaf26cdbbcc8a9c96b2` |
| exp0002-builds/review09-ready-fix/observer-build.txt | 1716 | `1dab7cf45e387afdee8e13d52f97d201bcb4fc828578b38a377c2077db1855ba` |
| exp0002-builds/review09-ready-fix/tests.txt | 62 | `5fa1012e22eb94866a3c20e33710a4c3c927495aa6662f8ad29ea42574c2c6bb` |
| exp0002-builds/review09-ready-fix/output-tests.txt | 74 | `13e7f304c97e7a6992e2ab03794a49e5eb33559882f1fc86e81d93f44c13edb6` |
| exp0002-builds/review09-ready-fix/SorExp0002.dll | 144384 | `cdda0fe400696c3761a0e19a6659ae3d3b582645d569c0806412fdad729b1d39` |
| exp0002-builds/review09-ready-fix/workshop-trace.exe | 98816 | `a7d265c60cd9abe3a0fba87689e0d53f6909b658a90a46b0e9ae0c2e836eeb82` |
| exp0002-builds/review09-ready-fix/SorExp0002-local-test.zip | 76713 | `e7f198591865e44c9c96c4c116530299203c7b6152d66d8c79962b475772bada` |


## Scientific anomaly / Vortex review build — 2026-10-06

Current review 12-anomalies supersedes prior build selection. User-scoped observer anomaly/safety policy, offline tests and exclusive Vortex deployment documentation only; no new scientific result or game/save/static research. 125 native and 26 output checks pass. Prior artifacts, including the review 11 fixture failure, are retained. See the audit and runtime README for limitations. These files and the complete review patch remain LOCAL-ONLY. No deployment or live execution occurred.

| Artifact under .local-work | Bytes | SHA-256 |
|---|---:|---|
| exp0002-builds/review12-anomalies/build.json | 7883 | `a1df627116c4ab3b6de60dcdf7258f35ea77224366430a0cccbd8738106a4b13` |
| exp0002-builds/review12-anomalies/observer-build.txt | 1716 | `1dab7cf45e387afdee8e13d52f97d201bcb4fc828578b38a377c2077db1855ba` |
| exp0002-builds/review12-anomalies/tests-build.txt | 1651 | `9c31e18df43c09a1c7e850649a3d3464a8e5d8e3ec485b639bd513adcbde9682` |
| exp0002-builds/review12-anomalies/trace-build.txt | 1651 | `737783c37f4a04abd6ad4b5b567e3091e19d7d24a4ed628979586b5545feed96` |
| exp0002-builds/review12-anomalies/tests.txt | 63 | `e0f3ed2407e417fab248f3025fd1914b8ab14787bf072bb625fa06e7f6b2e6bf` |
| exp0002-builds/review12-anomalies/output-tests.txt | 74 | `97e22c4d662b86c9f251b94d4baa14bbea194645d5baa2e9f004e9978796177b` |
| exp0002-builds/review12-anomalies/SorExp0002.dll | 176640 | `ca167cb5e47ea90739729ee686ce1691766461238847d6a778f98530bf6ce94e` |
| exp0002-builds/review12-anomalies/workshop-trace.exe | 99840 | `701033d459c11e54bbda5c4896a57f98940759f95e1a83034cbda2601295e36a` |
| exp0002-builds/review12-anomalies/SorExp0002-local-test.zip | 89338 | `84bc87c0f7ba8f58c843f70d170bb6d31ea1e72a47a339c0e47e57f0b41a9ae1` |
