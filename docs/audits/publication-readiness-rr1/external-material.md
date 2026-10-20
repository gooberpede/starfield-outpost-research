# External material, scratch creators and path lifecycle

**Twenty-nine empty system-temp trees are confirmed.** Their prefix and
historical exporter receipts support attribution to position/native-oracle
packaging; this is not an OS-level process-creation trace. No directory was
deleted or moved. Installed tooling and protected evidence remain legitimate
external dependencies, not automatically cleanup targets.

The inventory covers explicitly named leads and closely related project-owned
source. `D:/tools` and `D:/ReverseEngineering` were listed at top level; named
Ghidra/database/source paths referenced by project ledgers were checked for
existence. Unrelated tool projects and user directories were not recursively
searched. Local `temp-creators.json` and `source-paths-and-effects.json` retain
exact code locations; these scans include archived source copies and must not
be read as counts of independent maintained tools.

| Location / category | Existence / direction and creator/consumer | Lifecycle and current versus historical use | Durable reference / portability / proposed disposition |
|---|---|---|---|
| C:/Users/User/AppData/Local/Temp/sor-position-patch-* — residual scratch | 29 directory trees, zero files and zero file bytes recursively at inspection; two packaging helpers allocate matching prefix. | Persistent empty directory skeletons, not evidence payload. No cleanup block in inspected helpers. Historical use; not rerun. | Position/native-oracle reviews retain original scratch receipts. Reverify named roots before B5 cleanup; never sweep all Temp. |
| .local-work/position-resumption/package_review.py:94 — residual scratch creator | Exists; reads repository/baseline, writes mkdtemp tree in default OS temp and patch/receipt locally. | No cleanup call in the inspected exporter; final scratch path is retained in receipt. | `docs/experiments/position-resumption/review.md`. Retire or replace prospectively; retain historical copy/hash. |
| .local-work/native-oracle/package_review.py:94 — residual scratch creator | Exists; same prefix/default system-temp allocation, reads repository and writes review application tree. | Historical related helper can recreate same residue; prefix alone cannot allocate each of 29 trees to one helper. | Native-oracle review lineage. B5 prospective rerun/retirement decision, no execution in RR1. |
| research/x87-preservation/package.py:88 — bounded cleaned temp | Tracked; TemporaryDirectory context writes a review tree and cleans it on ordinary exit/exception. | Bounded temporary use; abrupt process termination cleanup not guaranteed. No persistent residue demonstrated by source. | Historical review references. Future reuse should obey current WORKFLOW project scratch/discovery ceiling; B5, no historical rewriting. |
| research/internal-observation-qualification/package.py:70 — bounded cleaned temp | Tracked; context-managed TemporaryDirectory, same read/patch/verify lifecycle. | Same qualification; no automatic defect merely from using system temp. | Internal-observation report/review. Prospectively relocate if reused. |
| Thirteen tracked test files — bounded cleaned temp | Default OS temp via TemporaryDirectory; context manager, addCleanup or tearDown cleanup in inspected source. | Synthetic test inputs. Source inspection only; no suite run by RR1. | [All 22 tempfile-using test paths](temp-test-inventory.csv); nine other test files explicitly choose local BASE/BUILD. Bounded temp is accepted. |
| Nine other tracked tempfile-using tests — legitimate local scratch | mkdtemp with explicit BASE/BUILD under local work, not default OS temp. | Persistent synthetic fixtures may be deliberate. Their cleanup is not inferred from patch-object addCleanup. | Retain evidence lifecycle/retention classification; no broad assertion that all 22 leak OS temp. |
| .local-work/review-patches/ — residual scratch / governed output | Exists; 479 child directories before RR1 writes, later RR1 children separately named. | Current workflow-designated application trees; retained historical reviews, not source distribution. | WORKFLOW Durable state and text. Lifecycle/retention decision B5; no removal. |
| D:/tools/xEdit.4.1.5p/Edit Scripts/SOR_OutpostRecon.pas — legitimate installed copy | Exists; installed SHA-256 3c072b34316c3eca74a28ec5290302687f4e270225dcc6a81a3fcd9f7bb212a7 equals tracked xedit source. Installation is write destination; xEdit consumes it. | Installed reader, no execution in RR1. | Initial reconnaissance validation; maintain source in Git, installation outside. B3 document setup, no installation change. |
| D:/tools/xEdit.4.1.5p/Edit Scripts/SOR_OutpostFocus.pas — legitimate installed copy | Exists; SHA-256 6b21e33de6bf1d63b05de686077590bffeaf401497a45b3b87fb52f9e3696345 equals tracked source. | Same separation; source is not stranded only in installation. | Same disposition. |
| D:/ReverseEngineering/Starfield and StarfieldCK — legitimate external analysis | Top-level directories exist; exact named .gpr/.rep dependencies also appear as existing CSV pin targets. | Imported executable/analysis state; consumed read-only by historical analysis. No Ghidra opened or whole-database rehash in RR1. | Source/provenance ledgers. Keep private; document lawful input/import procedure and version, not publish DB. |
| D:/ReverseEngineering/BackupInstalled, CompletePlanetSurveyMod, StarfieldResourceProbe — historical provenance / unresolved internals | Top-level presence verified only; no recursive examination. | Relevant leads, ownership/content not inferred from names. | No blanket cleanup or publication proposal. Inspect only if a selected B0 claim depends on them. |
| D:/tools/ghidra_12.1.2_PUBLIC; named Temurin/JDK; xEdit; x64dbg — legitimate external tools | Ghidra/xEdit/x64dbg top-level presence; JDK path documented by wrapper, not executed. | Inputs/executors of past methods. Version strings are reported historical pins, not newly qualified executable baselines. | B3 explicit prerequisites and caller-selected paths; tool licence never clears output rights. |
| ghidra/scripts/Invoke-OutpostRecon.ps1 — legitimate dependency plus portability risk | Reads installed launch settings, hardcodes tool/JDK/project roots; writes .local-work/recon export/log/cache/settings. | Current tracked wrapper already uses repo-local output, readOnly/noanalysis flags. It is not an ungoverned D:/tools output creator in current HEAD. | Historical defaults must not be transferred to current source. B3 parameterization proposal, no execution or edits. |
| Older local package-failed01.py and frozen export-review-package.py copies — historical uncontrolled output | Source still contains mkdtemp(dir='D:/tools') in archived failed/frozen copies. | Can recreate external trees if incorrectly rerun; current tracked preview/resource packagers use review_scratch under local work. | Housekeeping brief and old receipts retain paths intentionally. B5 mark entrypoint retirement; preserve bytes. |
| .local-work/screengrabs and l3-placement/protected/screenshot — local-only evidence | Exact selected files exist; seven CS plus eleven L3 screenshot copies freshly hash-checked. | Protected screenshots are inputs; independent reports consume them. | Evidence candidate report, source ledgers. B4 item-specific review; never auto-copy to Git. |
| Installed game, Documents/My Games/Starfield and local save archives — legitimate protected input | Named path occurrences inventoried; selected ledger path existence checked, no save decoding or modification. | Original saves/game assets persist independently of tool source. | Local-only evidence until exact rights/privacy decisions. B3 methods can be documented without originals. |

The reported **thirteen OS-temp tests is confirmed**, after distinguishing
22 tracked files importing/using tempfile from the nine with explicit local
directory arguments. The CSV shows calls, not test case counts. X87 and internal
qualification packagers use context-managed cleanup; position/native-oracle
helpers use bare mkdtemp. These are materially different lifecycle cases.

Absolute paths occur 2,428 times in the initial tracked text discovery pass.
This is occurrence coverage, not 2,428 unique dependencies or defects. Historical
source receipts retain evidence paths; current replay instructions depending
on ignored helpers require source closure. Do not make an all-temp-is-defective
policy or infer filesystem-wide cleanliness from this inventory.
