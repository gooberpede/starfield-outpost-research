# Evidence, corpus, tool effects and retained corrections

[Frozen plan](plan.md), [original brief](../../implementation-briefs/README.md#archive-lookup) (`implementation-briefs.zip :: docs/implementation-briefs/CODEX_BRIEF_SOR_BM2_build_catalogue_selection_production_aggregation.md`),
[sources](sources.csv), [functions](functions.csv), [review](review.md).

## Baseline and address domains

Fresh pre-analysis hashes match the preceding reviewed build: retail
Starfield.exe 1.16.244.0, 102,476,200 bytes, SHA256
`7e9adb1414a8e1b325e5e1f097b9b17b78deb7eebeda37a333351a43a60f9d28`;
Starfield.esm 1,457,098,709 bytes, SHA256
`1dabed00c3f4282dd3bb54d2e9601e40b577d8742d078b7ccef203adbfef0da7`.
The BM2 baseline freshly pins 19 installed/static-analysis inputs, original brief,
HEAD and index. The installed Interface.ba2 and SD2 add-on receive separate fresh
checks against their retained source identities. Raw/current source identities and
helper hashes are in sources.csv and ignored baseline/verification receipts.

Native locations are **preferred static VAs**, image base `140000000`; subtract
that base for module RVA. Function names are original analysis names; semantic
descriptions are research aliases, not qualified callable ABIs. Object-relative
offsets are hexadecimal. Physical ESM and uncompressed SWF offsets are decimal.
FormIDs are file-local identities under the specified file/master mapping;
UI selected form IDs, runtime reference handles and saved reference identities
are not interchangeable. No new runtime pointer or save offset is established.

## Prior work read and reused

| Reviewed project source | BM2 use / retained boundary |
|---|---|
| [Build Mode/Locations audit](../../audits/README.md#archive-lookup) (`audits.zip :: docs/audits/outpost-coverage-2026-10/build-mode-and-locations.md`) | Starting field gaps only; its pre-BM1 CHANGE status is historical. |
| [BM1](../construction-variants/report.md), methods/manual/automatic/review | Placed STBH variants, PackIn anchors and positive HIST-0210 relationships; not prospective grid siblings. |
| [SD2](../shared-outpost-storage/prerequisites.md), consumers/methods/review | Actual two-perk/location/add-on control; condition retry, ingredient sourcing and spending. Add-on source/selected records are freshly reread here. |
| [L1](../limits/native.md), report/review | Quota, player/environment gates and ordinary action admission, not a catalogue count ceiling. |
| [L2](../build-budget/report.md), native/UI/review | Cached scalar charge, persisted usage and footer meter. |
| [L3](../spatial-placement/report.md), native/review | Territory/collision/clearing boundaries; no new photo replay. |
| [E1](../inorganic-extractors/arithmetic-ui.md), arithmetic/stacking/resource-interval reports and reviews | Effective timers/AVs, per-minute binary32 sum, cache epochs and formatting; small gas/atmospheric factor 2 correction retained. |
| [E2](../organic-facilities/definitions.md), native/review | Organic capability/configuration, positive historical rows, inputs and shared scheduling. |
| [E3](../fabricators/definitions.md), native/review | Product presets, manufactured intervals and saved row schema; fresh native export distinguishes inline row construction from a direct call. |
| [P1](../power/report.md), fuel/native/review | Fueled-generator exclusion, power-state influence and body-conditioned variants. |
| [C1](../cargo-links/configuration-ui/native.md) | Target/active default-object identities and endpoint semantics; freshly rechecked constructors/consumers. |

These are credited prior project discoveries with original coverage/statuses
retained, not newly repeated live experiments. New BM2 scientific evidence is
STATIC. Prior SAVE evidence supports the relevant configuration/membership
contracts, not an observed BM2 menu or total. **Zero new save scans** were run.
No historical original was decompressed or modified. No old save's content/load
order is silently equated to the current installed files.

## Physical population and exclusions

The fresh group-bounded main-ESM walk visits every record header and selects
COBJ/FLST/KYWD/DFOB/FURN/GLOB/AVIF/IRES/PKIN/CONT/RSPJ ordered fields:
28,378 records, including all 3,009 COBJ. Payload and decoded resource guards
remain 16 MiB. The verifier physically rereads each selected header/field list.

First-FNAM/root-list qualification with clear deleted flag selects 204 physical
root recipes. The selected CNAM/FLST graph reaches 1,269 indexed records,
including 545 COBJ, with no cycle found in that graph. A separate header-only
terminal pass resolves all 273 out-of-payload IDs: 181 STAT, 42 ACTI, 41 NPC_,
seven MSTT, one AACT and one TERM. These are explicitly
unexpanded buildable/asset terminals, not missing recipes or a claimed exhaustive
model/template walk. Every COBJ and FLST in the main file is selected, so those
terminal exclusions do not hide a further ordinary COBJ/FLST recursion branch.
Leveled-list payload expansion and non-COBJ per-index condition maps are not
included in the six-index **direct COBJ** condition-vocabulary negative.

The initial BNAM comparison population (546 recipes) remains in survey.json.
Native `140a0239b` and `140f4d630` establish that the discovery test uses FNAM,
giving 204 roots instead. This is a substantive reconnaissance correction,
not a discrepancy to hide. The main-file population includes test/ship-context
definitions before conditions. It is not the menu's current eligible population,
all winning plugins, a list of successful constructions or an item-unlock census.

Mechanism-diverse controls are named in catalogue.md/eligibility.md; selected
definitions.csv has exact physical offsets and metadata. The two add-on primary
records retain SD2's sole-main-master mapping and physical offsets. No arbitrary
third-party plugin, xEdit, external decompiler, new dependency or downloaded
implementation is used. Game-derived payloads remain local and excluded.

## Helpers, reads, writes and target effects

All helpers use CPython 3.14 stdlib/project-owned methods under SOR-P-0002.
Immediate owned sources are BM1 setup, E2 UI equality reader, S1/ESM framing,
E1 AVM2 decoder, BM1/B1 review exporter and existing bounded Ghidra Java readers.
Existing Ghidra 12.1.2/Temurin 21 and Git are separately retained tools.

| Helper / local artifact | Reads and writes / effects |
|---|---|
| bm2-start.py / baseline.json | Hash installed inputs/analysis state/brief/index; launch owned hidden readOnly/noanalysis worker; isolated local logs/cache/settings. No target execution or analysis mutation. |
| bm2-defs.py / definitions.json | Full bounded installed ESM header/group walk and selected ordered fields; exclusive ignored JSON, pre/post identity. |
| bm2-inspect.py, bm2-read.py, bm2-exe.py | Console-only bounded locators over owned caches/native/UI and file-backed PE bytes; no output file/input mutation. |
| bm2-request.py / native/*.request | Exclusive numbered selectors for existing static state; reader writes local TSV/done receipts. No function invocation. |
| E2ReadSession/Cr1Recon/TransitCalls | Reused existing Ghidra read-only exporters. BM2 expands the condition-registration selector to actual sampled command IDs. No symbols/types/comments/bytes/analysis edits. |
| bm2-survey.py, bm2-graph.py, bm2-terminal-types.py | Local physical-definition summaries and terminal header qualification; authored categories/selected definitions metadata CSVs. No full game record payload enters Git. |
| bm2-regnames.py | Existing registration windows plus current file-backed executable strings -> exclusive local condition-name receipt. |
| bm2-ui.py / ui.json | Current BA2 member equality, owned derivative/method spans and bounded AVM2 instruction decoding; exclusive local receipt, no Flash execution or asset edits. |
| [verify.py](../../../research/build-catalogue/verify.py) | Protected identities, every selected physical record, graph/controls, actual PE constants/vtable pointer, native completion/pins, fresh BA2 reads/ABC spans, authored CSV identities and mixed float derivation. Writes exclusive ignored receipt; no save read or native execution. |
| Local ledger/package/retirement helpers | Hash/metadata registers; worker stop sentinel and process-presence query; exact UTF-8 patches/manifests and disposable standalone reconstruction. No workspace patch application, staging, refs or network. |

Exports use full-function selectors with finite decompiler/instruction limits.
functions.csv and export-limits.csv disclose actual completeness. A successful
decompiler return is not semantic proof; instructions control numeric operations.
Failed/interior addresses, capped symbols/xrefs and missing exports are not
absence evidence. The verifier's instruction-token checks locate selected
operations; they are not an independent disassembler or a universal native oracle.

## Failures and corrections retained

Early console attempts read a still-running export before its exclusive output
existed; later analysis waits for done receipts. Several guessed native entries
were interior/nonfunctions; export-limits.csv retains them and no conclusion
uses those failures. A symbol search reached its 256-symbol cap; required
consumers were found through exact data/string/xref paths instead. One console
render used Windows cp1252 and failed on a decompiler-generated character;
the UTF-8 source remained intact and subsequent readers explicitly select UTF-8.

The first graph CSV pass treated an unrelated FURN FNAM as recipe IDs, raising
a size/alignment error. Its already-written graph.json is retained; graph02.json
and final metadata limit FNAM interpretation to COBJ. No input was changed.
The first verifier caught an authored small-table count of 28; the exact list
has **27** entries. The assertion/report were corrected against physical bytes,
with the failed first run retained in review.md. No criterion was altered.

A second verifier run rejected an overly broad instruction assertion copied from
earlier shorthand: `1421f3839` is VADDSS, while `1421f383e` is its VMOVSS store.
The actual instructions were reread and the assertion/prose corrected. This does
not change the binary32 sum; the failed assertion is preserved rather than counted
as a pass.

The following run also rejected a locator expecting the full `04000000` mask
spelling; the actual consumer tests the corresponding byte/bit and decompiles
as `>> 0x1a & 1`. The locator was corrected to the exported operation, while
physical recipe flags remain checked independently. This was an evidence-check
representation error, not a failed game experiment.

Preconstruction AttemptBuild and Cancel callbacks were distinguished during
reconnaissance: `1421bb4a0` emits CancelEvent and is not the build request.
The final request trace uses `141719fb0/1421f4ed0/1421bb3d0` and CommitEvent.
Source-derived distinctions, including FNAM versus BNAM and nominal versus actual
production, take precedence over plausible labels or earlier shorthand.
