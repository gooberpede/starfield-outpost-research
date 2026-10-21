# Evidence, provenance and reproducible methods

2026-10-20. SOR-EXP-0058 / SOR-EV-0066. [Plan](plan.md), [answer](report.md), [review](review.md).

## Primary and authored registers

- [inputs.csv](inputs.csv): three exact named local saves, seven original JPEGs and prior Save25 archive; sizes/SHA-256, sealed-copy equality and preservation scope. Uploaded save copies were not accessible inputs and no equality to uploads is inferred.
- [positions.csv](positions.csv): seven player/beacon rows with decoded offsets, XYZ bits, parent/frame, angular association and descriptor/Workshop operands. Pair offsets are decoded-stream offsets; null model results in player rows do not mean missing geography.
- [fixed-controls.csv](fixed-controls.csv): fresh installed Jemison/Akila/Mars anchor rereads, same projection constants, both diagnostic dispatch candidates; fixed-anchor coverage only.
- [sources.csv](sources.csv): installed/existing-analysis hashes, method versions, script-member hashes, primary receipt/export paths and SHA-256. Full paths are private local reproducibility locators, not authority to publish the underlying files.

Local primary root is `D:/Projects/starfield-outpost-research/.local-work/coordinate-sufficiency/`. `baseline.json` records pre-analysis protected hashes, original/copy identities, read-only archive flags, starting HEAD/index and initial untracked inventory. `protected/inputs/` and `protected/screenshots/` contain byte-identical read-only copies. The original files were only opened for reading. Read-only attributes protect against accidental writes; they are not tamper-proof storage. Postflight rereads check both source and archive hashes.

`Save37.json`, `Save38.json`, `Save39.json`, `Save25.json` retain decode metrics, independent R3 framing, player/ordinary prefixes and construction ownership projections. The three new saves have complete qualified type6 component tables. Save25 retains `PAYLOAD_UNQUALIFIED` at unrelated component 140d4ae40/count 7/offset 293379; its separately qualified world-component run and descriptors still close and support the coordinate joins. A first verifier incorrectly required complete type6 closure in that old control and failed; the corrected check requires the actual scoped world grammar and preserves the unrelated gap. `Save*-descriptors.json` and `Save*-worlds.json` carry typed world joins; `numbers.json` contains calculations, including the unfavorable scanner comparison. `fixed.json` records the independently checked compressed Kreet PNDT record and WRLD/LCTN fields. `fixed-controls.json` retains the three additional fixed controls. `papyrus-sources.json` contains local-only source-member text and hashes; authored reports contain only signatures and analysis.

## Tool and build qualification

Installed executable resource version 1.16.244.0; fresh SHA-256 `7e9adb1414a8e1b325e5e1f097b9b17b78deb7eebeda37a333351a43a60f9d28`. ESM SHA-256 `1dabed00c3f4282dd3bb54d2e9601e40b577d8742d078b7ccef203adbfef0da7`. The new saves carry supported format 27/buffer 153 and the 1.16.244.0 build string; this does not prove every historical module/configuration. Exact decoded hashes and framing metrics are in each save receipt.

Tools actually used: CPython 3.14.3 and stdlib/project readers, Ghidra 12.1.2 PUBLIC existing analysis, Temurin 21.0.12+8, Git 2.53.0.windows.1 and PowerShell. `tools.json` and `sources.csv` pin versions/binaries. The shell's `python` alias initially failed to launch; subsequent commands use `C:/Users/User/AppData/Local/Python/pythoncore-3.14-64/python.exe`. No install or download occurred.

The existing Ghidra project at `D:/ReverseEngineering/Starfield/GhidraProject` was opened `-readOnly -noanalysis`. Database content pins were checked before the session and after retirement. `process.json`/`process02.json` contain exact commands; isolated settings/cache/logs stay under the local root. No analysis types, symbols, comments or bytes were altered. No target game process was opened or executed.

## Native export coverage and failures

| Receipt | Decisive content |
|---|---|
| native/001.request.tsv | Defined-string registration xrefs for GetPlayer and GetCurrentLocation |
| 002 | Complete decompilation of both registration functions, fixed-overlay ingestion and pattern lookup; instruction display has600-row caps |
| 003 | Typed binding constructors, player getter and location thunk; **failed** at invalid `window:` selector after four useful exports |
| 004 | Complete GetCurrentLocation underlying getter; guessed nearby terrain entries are explicitly NO_FUNCTION, not absence evidence |
| 005 | Corrected `win:` registration instruction windows and complete orientation-table helper |
| 006 | Shared angular/index projection, pattern lookup and dynamic overlay retrieval/selection |
| 007 | Terrain-table construction, initialization/resolution and general-reference containment branches |
| 008 | Deterministic hash, existing xrefs, ExtraLocation/cell/world getter paths |
| 009 | Terrain-instance construction and surface-table initialization callers; unrelated guessed function entries from earlier requests were replaced with actual xref entries |
| 010–011 | Body component resolution helpers; one guessed 142332b80 entry has no function and supplies no evidence |
| 012 | Existing defined-string census including terrain/content-manager seed setting names, uncancelled; individual xref display caps are not exhaustive callers |
| 013 | Surface seed default, independent PCM random seed initialization and body component lookup |
| native-followup/014–016 | Independent-review correction: exact candidate filter, registered form-table population, typed factory metadata and pure append helper; separate third read-only worker |

Request 003's script error ended the first offline worker. Its partial output and log remain unchanged; an explicit failure marker was written and a new worker resumed 004 onward. Request 005 re-exported the needed windows successfully. No failed output is called PASS. Normal second-worker stop/sentinel retirement is recorded in `retirement01.json`; the bounded candidate-filter follow-up has a separate command and retirement receipt. Complete decompilation and targeted windows support claims despite capped instruction displays; no claim depends on omitted instruction tails. BSS zero bytes in a database data window are not runtime setting measurements.

## Offline commands and effects

From the repository root, invoke the explicit Python path above with:

```text
.local-work/cs-start.py
.local-work/cs-saves.py
.local-work/cs-more.py
.local-work/cs-numbers.py
.local-work/cs-ledgers.py
.local-work/cs-retire.py
.local-work/cs-verify.py <new-receipt-suffix>
.local-work/coordinate-sufficiency/package.py --run <new-run-name>
```

These are reproducibility locators, not a replay-in-place instruction: helpers create exclusive outputs and require fresh output roots; never overwrite protected evidence. Native numbered requests/actual commands are preserved locally. The initial launcher uses previous project-owned SD3/L3 integrity/orchestration methods under SOR-P-0002; save analysis uses existing project readers listed by hash. This is source-informed owned-method adaptation, not clean-room work or outside code incorporation.

Reads: protected copies, installed ESM/source archive, existing analysis, project records/receipts and read-only Git state. Writes: ignored copies, decoder scratch, local JSON/TSV/logs, authored selected CSV/Markdown and isolated review scratch/diffs. Decoder cleans only its own temporary derivative. No network, target, original-save, configuration, analysis-database, index or ref mutation. Both-drive 40,000,000,000-byte guards remain fail-closed.

Existing tests actually run: 5 projection tests, 4 native-order diagnostic tests, 8 durable-v2 tests; all 17 passed. These are numerical/synthetic/regression checks, not new native execution or fresh-character validation. Actual save controls additionally use independent record walks, qualified component closure, typed joins and numerical comparisons. Package verification covers text, links, exact patch reconstruction and preservation, not scientific semantics by checksum.

## Credit and rights

Bethesda's installed executable, data and development-script archive are primary STATIC sources. The maintainer supplies the saves, screenshots and movement/placement testimony. Prior project position/Workshop/source-frame/native-availability discoveries and their owned readers supply the baseline methods, with original limitations retained. Ghidra/Temurin, CPython/stdlib and Git supply tools. Existing source records SOR-S-0124/0127/0128 and the position model remain the lineage; no outside source consultation, incorporation, contact, fork, PR or disclosure was needed. Credits and source index are updated. All authored metadata remains REVIEW-REQUIRED; primary extracts remain LOCAL-ONLY.
