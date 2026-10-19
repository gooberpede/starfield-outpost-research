# Methods, provenance and local evidence

[Plan](plan.md), [answer](report.md), [source hashes](sources.csv).
All paths below are repository-relative unless absolute. Local artifacts are
ignored and excluded from publication. Existing CPython 3.14/stdlib and owned
project readers only; no new dependency, third-party implementation or network.

Native analysis uses existing Ghidra 12.1.2/Temurin 21.0.12 with readOnly/noanalysis
and an isolated local settings/cache/log directory. E2ReadSession, Cr1Recon and
TransitCalls are adapted project-owned DA1/L3/S1 readers under SOR-P-0002.
No symbols/types/comments or executable bytes are changed. The reader is an
offline file-analysis worker, never Starfield or a debugger.

## Local acquisition helpers

All helpers require repository cwd, Python assertions enabled and `-B`. They
read the explicitly named installed/archive/receipt inputs and exclusively write
new local derivatives unless a table-generation purpose is stated. Repeated
acquisition names fail instead of replacing original evidence. None executes
PEX, invokes native game functions, writes saves/configuration/database content,
installs dependencies, changes Git or contacts a service.

| Helper / source lineage | Reads | Writes / effects |
|---|---|---|
| .local-work/sd1-start.py; adapted owned da1-start.py | Existing protected baseline, HEAD/index, supplied brief, installed development ZIP | sd1-containers/baseline.json; starts hidden owned read-only Ghidra worker; isolated logs/cache; selected PSC source-census01.json |
| sd1-acquire.py; S1 physical rereads and DA1 PEX reader | Pinned E2 index/main ESM/Misc.ba2 | definitions01.json and scripts01.json; 458 physical record rereads; independent complete Mannequin/TestDisplayCase PEX parses |
| sd1-census.py; original recursive selector, S1 assembly walk | Main ESM and E2 index | census01.json: all main relevant-type physical records, matching recipe/list closure, four selected PKIN cells and children |
| sd1-addons.py and sd1-addon-census.py | All 37 installed non-main ESMs, master tables and main definition context | addons01.json/addon-census01.json; name reconnaissance then recursive Outpost recipe/capability check; unresolved master leaves retained |
| sd1-saves.py; typed Workshop prefixes, DA1 actor and S1 extras/inventory | Canonical historical inventory and matching immutable originals | saved-HIST receipts, strict typed/footer framing and explicit gaps; decoder scratch removed by context manager |
| sd1-components.py; owned research_workshop_components audit | Selected protected originals and native-qualified component context | components-HIST receipts; full 43-section closure and selected component/item records, raw bodies local |
| sd1-containers/components_sd1.py | Supplied decoded buffer only | No I/O. Owned workshop_components.py adaptation: pending-dialogue id/u16-index/u32 layout from fresh 140d4ae40; no semantic dialogue claim |
| sd1-containers/extras_sd1.py | Frozen selected record bytes/queues | No I/O. Owned crew_extras extension for 33 modification masks, zero 96 subset, 36/37 relationships, 2C u32 and 22 compact count; unsupported flags fail closed |
| sd1-instance-joins.py | Three full component receipts | instance-joins01/02.json; exact counted reference extras, modification identities and ownership/backlinks; failed partial cases retained |
| sd1-details.py; owned esm_records | Installed ESM, selected item/static fixture/filter identities | details01.json; fresh weapon/armor/static reference/component/filter evidence |
| sd1-tables.py | Local acquired receipts and hashes | Authored definitions.csv/sources.csv only; no raw fields, private original save bodies, PEX or decompilation copied into Git |
| sd1-read.py | One numbered native TSV | Console selection of decompilation for research; no writes |
| sd1-more.py | Numbered selector arguments / native TSV | Exclusive numbered requests or console-only function/call/window selections; no analysis-content changes |
| sd1-corpus-table.py | Completed survey selection/success/failure receipts | Authored corpus.csv with bounded successes/errors; no save inputs reopened |
| sd1-stock-joins.py | Frozen H256/H257 saved record bodies and queued identities | stock-joins01/02.json; native-qualified stack-extra and row-state subset; actor tail remains unparsed |
| sd1-details2.py | Same pinned ESM as sd1-details.py plus five selected item IDs | details02.json, fresh suit/backpack/helmet/ammunition identity corroboration |
| sd1-binding.py | Pinned EXE bytes/PE sections | binding01.json numeric absolute-pointer reconnaissance; no hit is not proof the global cannot be bound |
| sd1-accessor.py | Pinned original EXE/PE sections, exact vtable slot | accessor01.json, independent pointer and complete five-byte getter reread after worker retirement; no execution/disassembly dependency |
| sd1-registers.py | Completed native exports and existing registry text | Authored function locators; task additions to nine existing documentation registers, preserving other bytes |
| sd1-verify.py | Baseline, all attempted originals, add-ons, native/save receipts; fresh H256 decode | Exclusive verification receipt; original/source preservation, joins and literal count/state/sentinel reread; guarded scratch removed |
| sd1-retire.py | Protected baseline, completed requests, owned PID and accessor receipt | preservation01.json; post-worker hashes, normal retirement and late getter/request checks; no process signals |
| sd1-resume.py / sd1-retire02.py / sd1-retire03.py | Same protected baseline and completed reader state | Fresh hidden read-only worker/logs for reviewer-requested n070–076; preserved first stop receipt; normal final retirement/preservation03.json; earlier numeric receipt typo retained |
| sd1-rework-check.py | Pinned main ESM, late native windows and authored conclusion | rework-check02.json, nineteen actual source/branch checks for review01 defects, no gameplay oracle |
| sd1-prose.py | Seven authored Markdown files only | Explicit UTF-8 numeric-spacing repair/check outside inline code/link targets; prose-check02.json; CSV/identifiers retained |
| sd1-containers/package.py; owned L3/CR1 lineage | HEAD/index and all authored changed/untracked text | Exact complete/task-only patches, status/manifest and isolated forward/reverse application checks; no workspace/index patching |

The survey launcher invokes sd1-saves separately per eligible label and records
unsupported header/build/reader errors rather than ending the corpus search at
the first exception. Selection and failure receipts live beside successful ones.
Hash/identity or disk-guard failures must stop affected operations; these are not
eligible negative scientific results. Historical file labels do not define a
single chronology or universe. No third-party donor corpus is added here.

Protection: baseline.json pins current EXE, main ESM, archives, analysis database
and relevant prior inputs; each scanned original is independently checked against
its historical inventory hash and rehashed after decoding. Add-on files receive
pre/post pins. Both drives retain 40, 000, 000, 000 caller-available bytes. Final
preservation and reader-retirement receipts are separate from scientific evidence.

## Reproduction and verification limits

Raw evidence is deliberately not distributed. Given the retained authorized
local inputs and pinned helper versions, reproduce acquisition into a fresh
local directory, not over the historical receipts. Native request selectors and
source hashes allow exact retrieval from the existing matching static project.
The review package records actual checks, errors and task/complete coverage.

The new tables are authored metadata/interpretation requiring review. Hashes
establish byte identity, full parser closure establishes framing, and native/save
joins establish the scoped semantics described in the report. None independently
establishes ordinary player success, final loaded authority, safe integration or
publication rights. All code/method reuse is project-owned under SOR-P-0002;
Bethesda installed scripts/data/EXE and the maintainer's saves are credited in
SOURCES/CREDITS. Raw scripts, decompilation and private saves remain LOCAL-ONLY.
