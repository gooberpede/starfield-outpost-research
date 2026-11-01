# P1 provenance and reproducibility ledger

2026-11-01, Australia/Sydney. [Report](d5ab-p1-report.md),
[native matrix](d5ab-p1-source-identity-lifetime.md),
[function/source ledger](d5ab-p1-sources.csv),
[selected test metadata](d5ab-p1-test-results.json), [review](d5ab-p1-review.md).
All raw native exports, exception bytes, captures, DLLs, caches and bulk receipts
remain LOCAL-ONLY. Authored code, this synthesis and selected metadata remain
REVIEW-REQUIRED; no publication clearance follows.

## Baseline and protected inputs

Admission HEAD is `4dea310b46c59da06f61cecc38b8198afe187279`. The only
pre-existing working-tree input was the supplied untracked P1 brief. The P1
ledger was created before acquisition/engineering. The later recorded baseline
`.local-work/d5ab/p1/baseline.json` pins HEAD/index, runtime sources, brief and
both-drive available space; its status correctly includes that new ledger.
It does not claim the ledger predated the user's instruction.

Installed executable/content/SFSE identities match `identity05/identity.json`.
All fifteen Ghidra project/database pins match before/after every export and in
Provenance05. Original historical P2 preservation records, including absences,
all 826 match. These are offline preservation checks, not active-save preflight.
No save is read, changed, restored, loaded or created. Both C: and D: satisfy
the 40,000,000,000-byte caller-available guard. No analysis symbol, type, comment
or database content is changed.

The pinned native baseline is Starfield 1.16.244.0, image base `0x140000000`.
Static VA and RVA remain separate; production sites are unchanged from D5AB.
Installed MSVC/MASM 14.51.36231, compiler 19.51.36256.0, Windows SDK, Ghidra
12.1.2, JDK 21.0.12+8 and explicit CPython 3.14 are existing tools. Actual
commands/compiler output, source snapshots and binary hashes are retained by
the build/export receipts. No dependency is downloaded and no third-party
implementation is added.

## Source and ABI lineage

The new native producer is version 0.4.0/schema `sor-d5x/4`; payload remains
312 bytes and framing remains 16 bytes. All eighteen production instruction
sites, their lengths/guards, and production `bridges.asm` remain unchanged.
The exact final producer/consumer combination is Native03, Reader Final03 and
Regressions01. Same-input Repro01 emits an identical DLL. Production transport,
queue stress, patch installer, controller and schema-3 reducer are byte-identical
to admission. The worker lease now accepts schema 4 while authenticating the
same exact identity keys. The lookup observer removes a memory read; it adds no
native boundary, engine lock or ABI convention.

The source ledger indexes seventeen new complete exports and ninety-three function
records, plus one bounded receiver-census record, with original one-based lines.
Existing E1/E2/E4/P and D5S/V/Z records
retain the locators/pins in the C2 matrix and their original source ledgers.
The incomplete E3 is preserved, not completed retroactively. The metadata CSV's
LOCAL-ONLY column classifies its referenced raw evidence, not publication
clearance of the authored locator table.

Owned D5AB/P2/D5S export, PE-reader, fixture, reducer and packaging methods are
adapted under SOR-P-0002. New scripts identify source lineage in docstrings and
receipt hashes. Microsoft's installed
`C:/Program Files/Microsoft Visual Studio/18/Community/VC/Tools/MSVC/14.51.36231/include/ehdata4_export.h`,
SHA-256 `b997c3f00192bb8c138532795d24b64c9b0f2ae4c4ee46af214b22bc7d88f447`,
is read-only factual-format consultation for FH4 metadata. No header text,
decoder implementation or new dependency is incorporated. The original stdlib
metadata interpreter preserves that provenance; it is not described as clean-room
work. Existing approved SFSE PluginAPI header and MIT notice remain unchanged.
No other third-party implementation, licence basis or disclosure is introduced.

## Reproduction commands and final receipts

Use `C:/Users/User/AppData/Local/Python/pythoncore-3.14-64/python.exe -B` followed
by a script/arguments below. Every output needs a fresh name. Historical labels
identify retained receipts, not permission to overwrite them.

| Operation | Script and retained arguments | Local final receipt / result |
|---|---|---|
| Full native build | `runtime/construction-winner/build.py p1-native03` | `.local-work/d5x/p1-native03/build.json`; 66 expected exits. |
| Same-input reproduction | `runtime/construction-winner/build.py p1-repro01 normal later-bypass p1-noaccess-lookup` | `.local-work/d5x/p1-repro01/build.json`; three controls, identical DLL. |
| Consumer/adverse/compatibility | `research/resource-retained-population/d5ab_p1_qualify.py .local-work/d5x/p1-native03 .local-work/d5ab/p1-reader-final03` | 316 passing checks; exact packaged consumer equality. |
| P2 regression batch | `research/resource-retained-population/d5ab_p1_regressions.py .local-work/d5x/p1-native03 p1-regressions01` | Wrapper pins all runtime sources and original P2 drivers before/after; controller 26, sharing one and queue nine pass. |
| Original-instruction controls | `research/resource-retained-population/d5ab_p1_native_controls.py .local-work/d5ab/p1-native-instructions04` | Eleven controls; substitutions and original range hashes explicit. |
| Original semantic oracles | `research/resource-retained-population/d5ab_p1_legacy_semantics.py .local-work/d5x/p2-native06 .local-work/d5ab/p1-legacy-semantics01` | Unchanged AST lines 105–230, 54 explicit oracles; final compatibility consumers on old schema-3 sessions. |
| Legacy worker-lease controls | `runtime/construction-winner/worker_health.py --qualify .local-work/d5ab/p1-worker-legacy01` | Nine own-thread controls. |
| Exceptional parents | `research/resource-retained-population/d5ab_p1_exception_parents.py .local-work/d5ab/p1/funclet-parents-final01.json` | Twelve parent/action records; all ten target actions; zero decode errors/unmapped `.rdata` references. |
| Combined verification | `research/resource-retained-population/d5ab_p1_provenance.py .local-work/d5ab/p1-provenance05` | Final sources/build outputs/test pins, seventeen exports, database/installed identities and 826 historical records. |

Read-only Ghidra acquisition uses the existing owned
`research/resource-retained-population/d5ab_lifetime_export.py`. Exact selected
functions/vtables/ranges are in each new export's `command.json`; every command
uses `-readOnly -noanalysis` and fresh local caches. No speculative executable
instruction census is performed. The inverse-action scan covers PE exception
metadata and the ten named `.rdata` action literals because L17 required exact
parent discrimination; it is not an allocation-size ownership heuristic.
The executed owned getter-census exporter is retained byte-for-byte as
`research/resource-retained-population/d5ab_p1_cell_access.py`, SHA-256
`d641bf9a9187324a8ecfa8ef96cf2df73f40f51675b54d45521f1ee8915c146c`.
Its selected command is `FRESH-LABEL %gridcells 1409831f0`; exact installed-tool,
generated Java, command and output pins remain in specialist Export15.
Other optional exporter modes are not additional experiment authority.

The final DLL SHA-256 is
`f12dfa2714ad97152c6130ef07e3139630382c00dce2d1ff0819a9469a9e361f`.
The selected JSON records every runtime component and receipt hash. Native03's
representative host retains 21,061 admitted/written/flushed/acknowledged records,
zero drops/output faults, 320-byte cells at capacity 32,768, and sampled
high-water lower bound 10,744. No universal zero-loss or maximum service-rate
claim is inferred from those finite workloads.

## Preserved failures and integration boundary

Development Native01/02, failed Original Instructions01 mapper admission,
Reader Final02's incorrect partial-evidence oracle and Provenance01's receipt
field error remain local. Corrected runs use separate names. The original
mapper traceback is retained as a transcribed tool return; an initial mapper
source snapshot/hash was not captured. The corrected final native script has an
exact source snapshot and hash. Do not invent an earlier source pin.

No native site/bridge relocation occurred. General asynchronous unwind through
generated trampolines and complete retail allocator/scheduling behavior remain
unqualified P3 concerns; no test silently converts those limits into runtime
safety. The final consumers deliberately keep combined native-source-lifetime
and scientific-firstness qualification false pending native integration. P1's
static contract/finite host qualification is a separate result.

Review patches, manifests, exclusions, editorial diagnostics and exact-final
independent returns are retained locally as described in the review record.
No staging, commit, push, publication, deployment or new live episode occurs.
