# SOR-EXP-0029 — Placed extractor/resource association

2026-10-11, Australia/Sydney. SOR-EV-0037 / SOR-F-0030 / SOR-ST-0028.
Authored research REVIEW-REQUIRED; raw inputs and inventories LOCAL-ONLY.
Governing [brief](../implementation-briefs/CODEX_BRIEF_SOR_extractor_resource_association_protocol_trial.md),
[original frozen contract](extractor-resource-contract.md),
[workflow trial and acceptance matrix](extractor-resource-trial-review.md).
**Outcome: COMPLETE — PASS.** Fresh independent reviewer ACCEPT; actual checks
and final package confirmation are retained in the trial review/local reviewer
ledger. No integration or publication authority follows.

| Element | Supported answer |
|---|---|
| Question | Can existing saves identify placed extractors and associate their produced resource deterministically? |
| Answer | Yes, for the tested dynamic case-5 inline-base representation: saved reference → qualified CONT base → positive PRPS resource actor value → IRES NAM1 → IRES NAM2 resource recipe → COBJ CNAM created item. Classification requires the extractor-category keyword, not an extractor-looking name. |
| Confidence | Exact sampled fields/framing are PROVEN / SAVE + STATIC. Produced-resource semantics are proposed STRONG / CROSS-VALIDATED within this scope, pending maintainer critical review. Actual production and load authority remain UNKNOWN. |
| Coverage | 25 labels, 24 unique save hashes: 17 manual labels, seven output-link labels including incidental exit, and mature Save52. Exhaustive R3 walks: 703,591 records across labels, including 205,557 in Save52. All embedded build strings are 1.16.244.0; these are saved metadata, not a newly measured executable baseline. |
| Result | Controlled creation/deletion and every no-action checkpoint agree. Save52: 63 recognized references, 37 distinct bases, 29 resources; all 63 resource/item associations resolved. |
| Limits | Conditional inherited reference type, unsupported noninline representations, incomplete authoritative ownership and historical content equivalence; no universal active-player count. Current installed definitions are a separately pinned input, not proof of save-era identical content. |
| Next domain | Resource operating state/deposit eligibility can be investigated separately; no live experiment or production reconstruction is authorized here. |

## Method and decisive evidence

Original project tools [extractor_resources.py](../../save-analysis/scripts/extractor_resources.py),
[runner](../../save-analysis/scripts/research_extractor_resources.py) and
[tests](../../save-analysis/scripts/test_extractor_resources.py) reuse established
project stream, record, reference and ESM readers. No outside parser or dependency.
ESM inspection walked all 38 installed `.esm` files, retaining 21,585 selected
TES4/CONT/COBJ/AVIF/IRES/MISC/LVLI/KYWD records locally. The static category
catalog contains 159 bases; every one has a unique resource association in these
installed definitions. Definition-only catalog entries are never placed instances.

Extractor identification requires a dynamic saved token, supported reference type
when explicit, inline case-5 base, successfully consumed initial prefix/repeated
self, CONT type and `Starfield.esm:008406` in KWDA. The property's actor value is
joined by identity to IRES NAM1, never by similarity of labels. A single positive
PRPS resource association is required for ASSOCIATED; zero/multiple remain
UNKNOWN. IRES NAM2 resolves a COBJ; its CNAM resolves the created item. Missing
recipe/item retains a resource result with an explicit item gap. This does not
read the placed object's output inventory or assert that it is currently producing.

Example: controlled S3's record token `822da9`, ordinal 10539, decoded logical
range **1299733–1300165**, body **1299791**, consumes base token `45ef19` and self
`822da9`. This resolves `Starfield.esm:05ef19`, whose PRPS entry 2 contains
`Starfield.esm:05ef18` with value 1. IRES `Starfield.esm:0057c7` NAM1 repeats that
actor value; NAM2 resolves COBJ `Starfield.esm:05ef53`, whose CNAM resolves item
`Starfield.esm:00556e` (iron). ESM physical record offsets are respectively
**5403487**, **1301610017**, **1300253652**. ESM physical offsets and decoded save
offsets are separate domains. Native pointers/runtime handles are not used.

The independent original action brief explicitly records **iron extractor + solar**
at S3 and **delete extractor** at S7; see
[manual corpus brief](../implementation-briefs/CODEX_RESEARCH_BRIEF_manual_save_corpus_S0-S7C.md).
This resource expectation was not inferred from this tool. Earlier candidate
bytes, independent arithmetic record-boundary walker, definition relationships
and action/no-action controls provide different checks. Initial-loot CNTO/LVLI
paths independently reach the associated item for all 155 ordinary static bases.
The four X-Tech definitions do not corroborate through that path; that counterexample
is preserved, rather than forcing the ordinary loot rule onto them. Loot itself
would be an inadequate production classifier.

## Controlled and mature results

| Corpus | Recognized extractor result | Independent expectation/check |
|---|---|---|
| S0/S0C, S1/S1C, S2/S2C | zero | No outpost, beacon only, then storage only; generic workshop vocabulary is insufficient. |
| S3/S3C through S6/S6C | one iron extractor each | Construction at S3; controls retain it; solar movement does not change its resource. |
| S7/S7C/manual exit | zero | Extractor deletion; beacon/storage/solar persist in earlier independently recorded lifecycles. No total residual-state absence claim. |
| L0/L0C/L1/L1C/L2/L2C/link exit | one iron extractor each | Reported reload/remapping and unlink/relink retain the instance class/resource. L0 is reused S4C, not an independent repetition. Exit labels are incidental. |
| Save52 | 63 recognized, all flags disabled/deleted clear | 37 bases / 29 resources; all have exactly one queued beacon-link lead, matching the 17 previously inventoried collection beacons. Names are context only, never resource-production oracles. |

Save52 resource counts are: helium-3 11; water/copper 5 each; aluminum 4;
beryllium/lithium/caesium 3 each; tungsten/antimony/gold/europium/tetrafluorides/
nickel/ionic liquids 2 each; neodymium/titanium/rothicite/iron/alkanes/vanadium/
uranium/palladium/cobalt/fluorine/silver/lead/aldumite/chlorosilanes/chlorine 1 each.
These counts describe recognized saved references, not guaranteed active output.

All 63 context leads are the queued `Starfield.esm:054ba6` keyword followed by a
saved beacon reference, corroborated against the prior mature extraction's 17
beacons. The tool deliberately retains `containing_outpost=UNRESOLVED`: queue
adjacency/context is not authoritative workshop ownership. There are **17 additional
Save52 records** with extractor bases outside the base slot. They are retained as
unresolved reference leads, not classified as extractors; controlled beacon/link
records likewise reference an extractor base without themselves being extractors.
Unsupported dynamic/noninline records are counted separately in coverage output.
Disabled/deleted/omitted states remain distinct; no inconvenient record is dropped
by those states. There are no disabled/deleted recognized instances in this sample.

## Plugin and identity boundaries

New observed modern-header reader consumes the size-delimited save plugin block:
u8 full, u16 small and u32 medium counts, metadata where present, and exact `0100`
trailer closure. All 25 tested labels close. It fails on an unqualified build or
unknown block shape. ESM MAST ordering plus TES4 small/medium flags resolve
file-relative identities; saved full/FD/FE slots resolve separately. Tag-00 form
array indices, tag-01 direct forms and tag-10 dynamic save tokens use established
project decoding. No bare DLC number is transferred between those domains.
Full/small/medium synthetic regressions cover equal local IDs in different plugins.
Selected records follow save table order; a general cross-class override/load-order
merger is not claimed. No observed extractor/resource chain has a conflicting
override in this installed corpus. Third-party/modded historical saves are untested.

## X-Tech exception and source claims

Static association is demonstrated for `SFBGS050.esm:01662c` and its FC/RI/UC
variants `07e613–07e615`: PRPS actor value `SFBGS00D.esm:05f4dc` →
IRES `SFBGS00D.esm:033e3f` → COBJ `SFBGS00D.esm:05f4db` →
created item `SFBGS00D.esm:033e3d`. This is a resource item, distinct from the
upgrade component or quest item with an X-Tech-like name. No name-only matching.
Installed record offsets: ordinary extractor **414999** in SFBGS050.esm;
resource **100652125** and recipe **100615988** in SFBGS00D.esm.

Ordinary X-Tech COBJ `SFBGS050.esm:01662b` points to that extractor in CNAM.
Its FVPA specifies resource forms iron/aluminum/tungsten at 5/4/2 plus one
`SFBGS050.esm:031e18` power core. This verifies the core requirement in the static
recipe, not all conditions for building it. Core XFLG byte `02` is observed;
its dismantle semantics were not independently established.

[Bethesda's overview](https://bethesda.net/en-US/news/starfield-free-lanes-terran-armada)
reports X-Tech introduced with Free Lanes. [INARA's extractor entry](https://inara.cz/starfield/outpost-module/4714/)
reports Terran Armada availability, the core cost and no core refund on dismantling;
[INARA's core entry](https://inara.cz/starfield/item/4719/) is a separate item lookup.
The nonrefund statement remains SOURCE-REPORTED, not reproduced engine behavior.
The suggested deposit-placement exception is UNKNOWN: neither these consulted
pages nor this offline trial proves its placement rules. No ordinary rarity or
deposit-family rule was applied to X-Tech. Consultation date 2026-10-11;
source/credit record SOR-S-0141. No source code/text incorporated.

**Placement: NOT_OBSERVED_IN_SAVE_CORPUS**, scoped to the implemented detector's
25 tested labels. Static availability is verified, placed-instance validation
remains a future coverage gap. No new live X-Tech outpost is requested or authorized.

## Reproduction, preserved failures and evidence

Use the installed CPython recorded in the local receipts; stdlib/project only:

```powershell
python save-analysis/scripts/research_extractor_resources.py --run fresh-run --data 'C:/Program Files (x86)/Steam/steamapps/common/Starfield/Data'
python save-analysis/scripts/test_extractor_resources.py --corpus-run .local-work/extractor-resource/fresh-run
```

Successful reference run `.local-work/extractor-resource/run05/` contains
`summary.json`, per-series/per-label JSON, `instances.tsv`, `inventory.txt`,
`inputs-before.json`, `inputs-after.json`, `contract-pin.json`, `corpus-tests.json`.
Static primary derivation is `run01/static-records.json`, pinned and rechecked
against every source when reused. Every save's archived hash matches its frozen
manifest or prior mature pin, before and after; scratch is cleaned by the decoder.
All scans are exhaustive within declared record regions; no arbitrary sample cap.
C:/D: space guards run before sizeable writes/decoding and at completion.

Preserved failures: run01 stopped on compact ESM identity handling (744 compact
records exposed the unsupported assumption); run02 stopped on duplicate incidental
exit filenames after valid controlled rows; first corpus test stopped because
`mmap` has no `count` method. These are engineering failures, not scientific
negative results. Compact table mapping, series-qualified filenames and mmap-find
counting corrected them within this assignment. run03 and run05 completed; 11
synthetic tests and all 25 primary-byte corpus tests pass. Each successful inventory
is repeated on the same bytes to check determinism. The 24 existing reader tests
also pass. Independent review replays all 25 saves and directly checks all 21,585
cached static records against ESM bytes; 343 chain identities have no duplicate
installed records. `static-crosschecks.json` and
`context-crosschecks.json` retain independent corroboration and X-Tech exceptions.

Publication remains gated separately. No raw saves, game payloads, bulk local
inventories or system data are in tracked deliverables/review patches. No original
input edits, game launch, debugger, deployment, staging, commit or push occurred.
