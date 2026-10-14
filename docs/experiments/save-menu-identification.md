# Save-menu identification utility — 2026-10-14

**COMPLETE — PASS for the brief's practical sufficiency contract; maintainer/ChatGPT review pending.** Single primary agent, no independent reviewer or sub-agents, as explicitly required by the [authorized brief](../implementation-briefs/CODEX_BRIEF_SOR_save_menu_identification_utility.md). This operational result does not promote outpost findings or authorize integration, live work or publication.

|Element|Supported result|
|---|---|
|Question|Can the current research saves be identified before gameplay without guessing menu order?|
|Answer|Yes. Five controlled Save3/25/26/27/28 character/timestamp pairs are distinct and match the supplied menu. Mature Save52 is separately identified from its own header and original last-write timestamp, with screenshot validation explicitly absent.|
|Confidence|PROVEN observed equality for 12 screenshot timestamps/locations/levels/playtimes; STRONG scoped original-last-write/current-offset display model, proposed for review. This is not a native menu implementation proof.|
|Coverage|Five controlled entries plus seven independent mature-character auto/exit controls, two character names, BCPS1/header word 27, English text. Sampled adjacent header strings report 1.16.244.0; they are not independently measured originating builds.|
|Evidence|Ignored `.local-work/save-menu/run-04/` inventories, validation/preservation and controls; manual inspection of the two supplied screenshots; prior [Attila transcription](ship-relocation-050/run-card.md#save-selection-supplied-in-advance).|
|Limits|Save52 itself is not visible in the screenshots. Copies may have unrelated timestamps. General locale, timezone-setting changes, arbitrary header layouts and full save-kind semantics are untested. No completeness claim for all saves or characters.|
|Next step|Maintainer/ChatGPT diff review; then return to separately authorized inorganic-resource availability research with the unplaced-beacon Available Resources panel as independent gameplay oracle. No extended menu reverse engineering is needed.|

## Recovered fields and independent controls

The [utility](../../save-analysis/scripts/save_menu.py) reuses project `inventory_historical_saves.metadata` and `stream_save.header`. Character is the length-prefixed string at decompressed-stream offset 25; level follows it as little-endian uint32; location, playtime and race are subsequent uint16-byte-length-prefixed strings. Exact offsets, raw values and first-stream digest are retained per input. Optional English playtime abbreviations come from the saved text, without calculating elapsed time. Filename save-kind prefixes are inexpensive **inferences**, separately labelled and excluded from human instructions. No menu ordinal or Creation Club flag is generated.

The displayed timestamp matches **original last-write time**, truncated to whole seconds, with the screenshot's **fixed UTC+11:00 offset applied to every date**. Five Attila entries and all seven second-screenshot entries match exactly. Attila character identity also has prior maintainer testimony; neither screenshot displays a character name. The second screenshot's character name comes from its matching files' decoded headers, not pixels.

Historical Australia/Sydney date-specific conversion is a counterexample: September 28's UTC+10 gives times one hour earlier than screenshot 1. The successful UTC+11 model instead matches September and October rows alike. This supports a current-offset display model within these controls; it does not establish the game's timezone API. The CLI requires an explicit offset and never consults the machine's current timezone. If the player's menu offset changes, regenerate instructions with that offset. Do not assume an old screenshot remains an exact time control after such a change.

Header FILETIME-like words at ten bytes after the race field, and filename times, disagree with these menu seconds. For example controlled Save25 has original mtime 2026-10-09T10:22:22Z, candidate header time 10:22:24.420244Z, and filename time 10:22:24. Save27 header time precedes its displayed second. No blanket subtraction can fix both. Those candidates are retained as diagnostics, never used as menu timestamps.

Copies are an independent negative control: original Save3 mtime is 01:34:27Z, while its archived copy is 01:34:28.678096Z; the Save25 archive mtime is 11:48:59.333891Z rather than 10:22:22Z. The mapping binds original metadata to the archive's SHA-256. Missing source timestamps remain UNKNOWN; the utility does not fall back to a copy timestamp or the header candidate.

Actually generated controlled timestamps, all using UTC+11 and M/D/YY:

|Research ID|Header location|Level|Generated menu timestamp|Control|
|---|---|---|---|---|
|Save3|Kreet - Kreet|3|10/6/26, 12:34:27 PM|Screenshot 2 / prior transcription|
|Save25|Kreet - Outpost|4|10/9/26, 9:22:22 PM|Screenshot 2 / prior transcription|
|Save26|Kreet - Outpost|4|10/10/26, 12:24:53 PM|Screenshot 2 / prior transcription|
|Save27|Kreet - Outpost|4|10/12/26, 12:11:19 PM|Screenshot 2 / prior transcription|
|Save28|Kreet - Landing Area|4|10/12/26, 12:18:28 PM|Screenshot 2 / prior transcription|
|Save52|Jemison - The Lodge|319|8/18/26, 5:45:40 PM|Original-mtime model; NOT screenshot-verified|

Names, exact paths, hashes, raw fields, source/copy identities and complete generated instructions remain in the LOCAL-ONLY JSON and `controlled-labels.txt`. The two lineages are not conflated by save number. No collisions occur in either actual inventory. Different hashes sharing character/timestamp are conservatively flagged even when optional clues differ; identical-byte copies are duplicate inputs, not distinct-save collisions. Collision analysis covers only supplied inputs, not unseen menu entries. Filename/hash are offline clues, never claimed to appear in the menu.

## Invocation and operator use

From the repository root, with installed CPython (no packages/downloads):

```powershell
$menuPython = 'C:/Users/User/AppData/Local/Python/pythoncore-3.14-64/python.exe'
& $menuPython -B save-analysis/scripts/save_menu.py --mapping .local-work/save-menu/run-04/controlled-mapping.json --utc-offset '+11:00' --json .local-work/save-menu/new-inventory.json
& $menuPython -B save-analysis/scripts/save_menu.py 'C:/absolute/original/Save25_example.sfs' --utc-offset '+11:00'
& $menuPython -B -m unittest discover -s save-analysis/scripts -p test_save_menu.py -v
```

The first command uses actual retained inputs; choose a **new** JSON output name. The second is a syntax example, not a claimed existing file. Positional paths may be repeated. Mapping input accepts a label-to-path/record object, a record list, or an existing `{samples:[...]}` manifest with `label`, `source_before`/`source`, and `copy`. Hash-bound source identities must include original `mtime_ns`; direct paths use their own mtime with a copy/retiming warning. Optional `utc_offset` overrides are explicit per row. Optional `control` contains an exact local evidence path, its SHA-256 and manually transcribed `fields`; the tool verifies evidence bytes and field equality, **not screenshot interpretation or testimony**. A hash does not prove those assertions. Future controls must state their method and name provenance.

Before gameplay, use the generated character filter and unique date/time instruction. In this corpus the Save25 instruction is `Load Attila Kiraly Save25 — Kreet - Outpost — Level 4 — 10/9/26, 9:22:22 PM`. Give it once before loading; do not repeat routine after-the-fact confirmation. A missing entry, materially different label or ambiguity warrants one targeted check. Never choose by permanent ordinal. A research ID in the instruction is an offline designation, not displayed menu text.

The tool reads saves twice for hashes and validates physical framing, then decompresses only the first stream, bounded to 262144 decoded bytes and at most 263168 compressed bytes. It never decompresses the whole save, creates scratch, or writes saves. Later compressed-stream checksums are not tested; the SHA-256 identifies the complete source bytes. JSON uses exclusive creation and may contain private metadata; keep it ignored/local. CLI returns 0 for identified inputs, 1 for errors/incomplete fields/collisions, 2 for invocation/output errors. An error emits no load instruction. Stdlib/project imports only; no game/tool/database/network effects.

## Acceptance and review package

|Mandatory criterion|Result / evidence|
|---|---|
|Character and menu-matching controlled timestamps|PASS: five distinct pairs, screenshot 2 and prior testimony/transcription.|
|Save3/25/26/27/28 plus mature Save52 and separate lineages|PASS: six hash-bound inputs; archived bytes used where accessible, original source metadata retained. Save52 screenshot comparison NOT TESTED.|
|Independent controls, timezone/source discrimination|PASS: 12 exact screenshot matches; historical-offset/header/filename/archive-mtime counterexamples preserved.|
|Single/multiple paths or research mapping; human and structured outputs|PASS: actual CLI mapping outputs, synthetic CLI/output refusal test; exact paths and per-field provenance/unknowns retained.|
|Collisions and safe extra clues|PASS: synthetic two-character/different-byte collisions and duplicate-content controls; actual inventories have zero collisions. Unseen saves remain outside coverage.|
|Focused parsing/time/absent-field/malformed-save tests|PASS: 13 focused tests; preservation and existing stream-reader regression tests recorded locally.|
|Read-only safety and preservation|PASS: before/after hashes and mtimes for selected originals, archives and screenshots; no save/config/database changes. C/D free space above 40,000,000,000 bytes. No full decode or substantial processing.|
|Review patches/status/manifest/exclusions/forward and reverse checks|PASS: `.local-work/diffs/save-menu-identification-{complete,task-only}.diff` and package receipts. Supplied previously untracked brief is included only in complete patch.|
|Single-agent handoff and no Git/external mutations|PASS: no sub-agents, game launch, instrumentation, staging, commit, push or disclosure. Maintainer/ChatGPT critical review pending by explicit brief exception.|

Initial exploratory console output failed on a non-English historical string because of the console encoding; the probe switched to UTF-8 and narrowed to required inputs. The first supplemental timestamp check incorrectly used historical September UTC+10 and failed; it was corrected using all seven screenshot controls. Initial artifacts remain under `.local-work/save-menu/`; final qualification is run-04. No mandatory engineering failures remain.

Exact source/tool/output hashes, test logs, exclusions, diff path/content checks and internal-link checks accompany the ignored review package. Raw saves, screenshots, header inventories and exact personal locators are excluded from review patches. New authored code/report is REVIEW-REQUIRED; no material is cleared for publication. No new third-party code or permission issue was found. Existing Bethesda save/menu representations, maintainer screenshots/testimony, owned project readers at HEAD `b225cb61bbafeefd2496f62fa4ba5a0437ded09a`, and installed CPython/zlib retain provenance in [sources](../SOURCES.md) and [credits](../../CREDITS.md).
