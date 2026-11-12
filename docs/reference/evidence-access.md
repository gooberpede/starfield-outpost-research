# Evidence access and reproduction

[Technical index](README.md) · [First-release scope](../first-release-scope.md) ·
[Exact evidence-route lookup](../history/evidence-routes.md)

Local qualification checks a named method and input in a stated setting.
Independent readers need the exact lawful inputs that the method checks.
A public checkout can supply authored sources and selected tables. Proposed
candidate assets and their independent retrieval are **PENDING RELEASE**.
[Publication run card](../PUBLICATION_RUN_CARD.md) ·
[Publication policy](../PUBLICATION.md#publication-independence)

## Choose a verification tier

| Tier | What a reader checks | What remains attributed or conditional |
| --- | --- | --- |
| Tracked tables, arithmetic and synthetic examples | Recount a named cohort, compute a given allocation, or check record framing on invented bytes. | The original collection, historical event and effective live state require their own evidence. |
| Authored mechanism inspection | Inspect the cited report, function/field mapping and independent review. A game-dependent reread needs lawful matching files and its method-specific source and host. | A static path supplies a conditional account of execution. |
| Original saved witness | Decode the exact saved member with the qualified reader. Check the named fields and adverse controls in the method. | Save metadata and decoded state do not establish the native executable hash at creation or current effective state. |
| Recorded derivative | Compare only the recorded operands represented by the exact asset. | Original acquisition, producer fidelity and omitted fields remain attributed to their original investigation. |
| Fixed native stage | Execute the pinned private-process fixture under its exact host and input contract. Compare all admitted outputs and refusal cases. | A fixed-input repeat leaves historical inputs, retail scheduling, renderer state and actual winners unresolved. |
| Historical only | Inspect the attributed report, original review and qualifications. | Upstream C19, Save29 trial loads, private Cargo comparators and the reported D1 incident have no selected exact replay route. |

## Build and input identities

The principal executable is retail Starfield.exe **1.16.244.0**,
102,476,200 bytes, preferred image base `0x140000000`, SHA-256
`7e9adb1414a8e1b325e5e1f097b9b17b78deb7eebeda37a333351a43a60f9d28`.
Starfield.esm is 1,457,098,709 bytes, SHA-256
`1dabed00c3f4282dd3bb54d2e9601e40b577d8742d078b7ccef203adbfef0da7`.
The PlanetData BA2 for the fixed fixture is 22,468,821 bytes, SHA-256
`2fb1fff5d8fc074718bf05022c099f3c87ef70e00050229b368ae7d680fbe5d5`.
Historical origins and effective overrides remain claim-specific. The
[function catalogue](../functions/README.md) distinguishes current authored
editions and the historical exact-source edition. Consult the
[original provenance register](../PROVENANCE.md) and each method's own pins.
A future reader's ability to obtain the matching lawful legacy build is
unestablished.

## Candidate inventory

| Candidate | Members | Bytes | SHA-256 | Access |
| --- | ---: | ---: | --- | --- |
| `sor-1.16.244.0-b4-f1-core-stored-provisional.zip` | 25 | 104,046,934 | `b27bb842770d51499bec30042660789f1e539a3187d0d63f226fafcedd405105` | PENDING RELEASE |
| `sor-1.16.244.0-b4-f1-addendum-deflate-provisional.zip` | 27 | 80,827,444 | `d904b452fcfe1a82e6c4ceae5dfd1396b4fa088868587605ced7e2e57de278a3` | PENDING RELEASE |
| `d5as-feynman-geometry-v1.zip` | 33 | 176,733 | `d0d35ed2193527dd8215a647178614a5403e814bf14c3f9d1f0a448c53a1043c` | PENDING RELEASE |
| `c19-callbacks-v1.json` | 1 | 189,747 | `d37476dd5b33fca44423c1c0aaf239b43e8a98d8cf2ed97b15beaa4225906ada` | PENDING RELEASE |
| `d5bh-episode-witness-v1.zip` | 27 | 1,592,210 | `2febe19f9348b7c6b45ab60bb3adb0cc0f278d04b815481445fb91473e3fc209` | PENDING RELEASE |
| `SOR-D5BI-N2-projected-evidence-v1.zip` | 6 | 3,896,901 | `a47bbd302553755d0fe87d746234d0d6c527ee7297cfda2e38915072edb7c3d7` | PENDING RELEASE |
| `SOR-D5BO-B2-projected-evidence-v1.zip` | 2 | 394,869 | `098ddf7d67f6a23390932b3440faa489439235663bf315754697e40acf694224` | PENDING RELEASE |
| `sor-d5bx-workshop-roots-v2.zip` | 3 | 1,373,706 | `d1ae3965c40e08a002e638fb1e49d1e3a1d3b67edad1ce1e5e0be9d5d36882f8` | PENDING RELEASE |
| `sor-d5bx-cargo-c3-v1.json` | 1 | 3,598,255 | `557f6148a357cc0a354336637a939ae1c3736a63f7a5f7cea27c189cd5095920` | PENDING RELEASE |

CORE and ADDENDUM use the [historical member aliases](../history/save-identifiers.md).
The pinned machine ledger at `research/evidence-data/release-assets-d5bf/release-assets.json`
provides exact member identities and is an active reader operand. The
`research/evidence-data/evidence-access-d5bx/assets.json` machine ledger pins both
supplements. The release inventory requires member validation as well as the
whole-file digests above. See the [pre-freeze decision](../DECISIONS.md#d5cb-pre-freeze-evidence-and-distribution)
for file-specific dispositions, local custody and pending approvals.

## Verify D5BF containers and members

The [D5BF ledger verifier](../../research/evidence-access/verify_release_assets.py)
reads the relocated ledger and the four explicitly supplied files. Use each
file's approved basename. The verifier reads and streams member bytes and
reports comparisons to stdout.

```text
python -I -S -B research/evidence-access/verify_release_assets.py research/evidence-data/release-assets-d5bf/release-assets.json --asset B4-F1-CORE "<CORE-path>" --asset B4-F1-ADDENDUM "<ADDENDUM-path>" --asset D5AS "<D5AS-path>" --asset C19 "<C19-path>"
```

For the standalone scientific checks, follow the C19 callback and D5AS
complete-body methods below.

## Selected original witnesses

Use Windows CPython 3.14.3 with `-I -B` and assertions enabled for the
selected readers. Supply explicit immutable operands and an exclusive new
receipt or output directory under caller-owned scratch. These readers check
the exact originals before and after. Methods with streaming decode apply
the existing caller-available two-drive guard and read-only temporary
buffers. Reproduce only the advertised witness, using the selector numbers
from the pinned member ledger.

| Subject | Entry point and operands | Verified comparison boundary |
| --- | --- | --- |
| Position and biomes | [Geography](../../save-analysis/scripts/verify_d5bu_geography.py) with `--member ID PATH` for CORE IDs 1, 2, 3, 40, 47, 53 and ADDENDUM ID 49, plus lawful matching `--esm` and `--planet-data` and a new `--output-directory`. | Seven original reads and three named maps. Position and biome claims select their own comparisons. |
| Fabricators | [Fabrication](../../save-analysis/scripts/verify_d5bu_fabricators.py) with `--hist-0036`, `--esm`, `--receipt`. Tracked authored recipe tables are also read. | Selected F064 producer, extra and graph joins. |
| Shared storage | [Controls](../../save-analysis/scripts/verify_d5bu_controls.py) subcommand `sd2` with `--member ID PATH` for 40, 42, 51, 64, `--esm`, `--addon`, `--receipt`. | Fresh owner and inline-base joins and selected zero/version controls. |
| Workshop roots | [Projection reader](../../save-analysis/scripts/verify_d5bx_workshop.py) with `--member ID PATH` for 40, 42, 43, `--archive`, `--esm`, `--receipt`. Supply the exact Workshop supplement. | 657 baseline roots and 191 supplemental roots, with typed membership and the 31-group canonical ledger. Retained Hab origin and full population completeness remain unresolved. |
| Construction | [Controls](../../save-analysis/scripts/verify_d5bu_controls.py) subcommand `construction` with `--member ID PATH` for 11–16, 29–39, 41–45 and 51, plus `--receipt`. | Paired roots, budgets, placement, gap ledgers and named variant extras. |
| Cargo | [Cargo reader](../../save-analysis/scripts/verify_d5bu_cargo.py) with `--save52`, `--c3-context`, `--receipt`. Supply CORE F040 and the exact Cargo C3 supplement. | Saved C2/C3 relationships and inventory selections. |
| Local output links | [L-series reader](../../save-analysis/scripts/verify_d5bu_output_links.py) with `--l0` for CORE F032, `--l0c` for ADDENDUM F055, `--l1` for F056, `--l1c` for F057, `--l2` for F058, `--l2c` for F059, and a new `--receipt`. | Named relationship windows and their payload/entry-order controls. |
| Power and displays | [Save29 and HIST-0021 reader](../../save-analysis/scripts/d5bt_reader.py) subcommands `save29` or `hist-0021`, `--save`, `--output-directory`. | F054 ordered allocation and swap calculation, or F067 displayed reference and backpack control. |

Both combined commands require CORE and ADDENDUM. The Geography batch
adds CORE F040 and ADDENDUM F049 to the five selected coordinate originals
used by `C02-ORIGINALS` and `C18-FULL-CONTROLS`. Use the main ESM and
PlanetData BA2 pins under [Build and input identities](#build-and-input-identities).
For L-series, all six flags are required for the combined command.
`B4-C22-L-SERIES-ORIGINAL` identifies the relationship windows and controls
supported by the selected claim. See the [route lookup](../history/evidence-routes.md)
for the evidence behind each claim.

The historical Cargo B02 custody record uses the label `ACTIVE` for its
local preservation baseline. The selected Cargo reader takes CORE F040
and the exact D5BX C3 JSON as `--save52` and `--c3-context`. Its checks
require neither the private B02 archive nor the local paths embedded in
the comparator. See the [B02 disposition](../DECISIONS.md#d5cb-pre-freeze-evidence-and-distribution).

D5BU accepted 14 selected original-reader routes locally. D5BX locally
qualified both exact supplements. Its Workshop projection reader matched
the original result field for field, including retained unsupported cases.
The Cargo input reproduced the accepted original-witness receipt byte for
byte. The earliest historical Workshop helper intake still lacks a full pin.
Read the [Workshop primary report](../experiments/workshop-population/report.md)
and [review](../experiments/workshop-population/review.md), and the
[Cargo saved evidence](../experiments/cargo-links/fuel/saves.md) and
[review](../experiments/cargo-links/fuel/review.md).

## C19 callback comparison

From the repository root, the project-owned
[standalone verifier](../../research/evidence-access/d5be/c19-verify.py)
uses Python 3.10+ and the standard library and writes no files.

```text
python -I -S -B research/evidence-access/d5be/c19-verify.py --self-test
python -I -S -B research/evidence-access/d5be/c19-verify.py c19-callbacks-v1.json --sha256 d37476dd5b33fca44423c1c0aaf239b43e8a98d8cf2ed97b15beaa4225906ada --negative-controls
```

The first command prints `PASS synthetic fold only`. The second needs the
exact candidate file and should recover 346 ordered comparisons, comprising
339 three-row and seven two-row lists, with 340 unchanged redeliveries,
zero selected appends, and six rejected adverse cases. It keeps first
occurrence by non-null pointer across spatial then atmosphere operands,
and appends actual selected-water operands in observed order. The asset
covers the native callback rows. The upstream capture census and rendered
timing remain attributed or unknown as the original report specifies.
[Original report](../experiments/continuous-beacon-preview/live-scientific-report.md) ·
[Review](../experiments/continuous-beacon-preview/review.md)

## D5AS complete-body comparison

From the root, the [standalone verifier](../../research/evidence-access/d5be/d5as_verify.py)
reads the exact ZIP and checks the represented roster and geometry bodies.

```text
python -I -B research/evidence-access/d5be/d5as_verify.py d5as-feynman-geometry-v1.zip --sha256 d0d35ed2193527dd8215a647178614a5403e814bf14c3f9d1f0a448c53a1043c --negative-controls
```

Match all 33 members and the 30 qualified full bodies split 2/28, the
excluded attempt and replacement, and six rejected controls. The comparison
checks reference equality. Acquisition and per-start eligibility follow the
[original roster and exclusions](../experiments/resource-retained-population/d5as-series-closeout.md).
Generating mask and winning request remain unobserved.

## Fixed native geometry

The selected conditional route `P-AG-FIXTURE` uses the
[fixed geometry entry point](../../research/resource-retained-population/d5bj_geometry.py)
with `--exe`, `--esm`, `--planet-data` and `--d5as`. Supply the exact
D5AS ZIP and hash-compatible lawful files. The qualified host is Windows 10
build 19045, AMD64 CPython 3.14.3 with interpreter SHA-256
`cce21c0e8710e304273e98ac4b2b0f5aceb639acbcd2343cbaa5c4e81619c45b`
and system `ucrtbase.dll` SHA-256
`3c60056371f82e4744185b6f2fa0c69042b1e78804685944132974dd13f3b6d9`.
The preflight also requires AVX, FMA3, enabled SSE/YMM state, available preferred
image pages and 40,000,000,000 caller-available bytes per involved volume.
Use a fresh process from the checkout root. Each path names an exact input
from the qualified host and inventory above.

```text
python -I -B -X faulthandler research/resource-retained-population/d5bj_geometry.py --exe EXE --esm MAIN_ESM --planet-data PLANET_DATA_BA2 --d5as D5AS_ZIP
```

Execution requires separate authority for the native fixture. The geometry
entry point, [sampler](../../research/resource-retained-population/d5bj_sampler.py)
and their tracked planar, ESM and context readers supply the source closure.
The BA2's exact 655,414-byte Feynman V BIOM member has SHA-256
`bd06d24e8ca1788481f6a4388c0e262b863b8b376a521752cf3d286c69f23863`.
The preflight authenticates all 33 ZIP members before mapping. Only the
two fixed reference bodies serve as native comparison operands.

The fixture maps a bounded PE page set into a fresh private process with
the Windows x64 ABI. It checks image sections and page protections, invokes
the converter, sampler, packed keys and per-cell stage, and uses private
allocator and collection callbacks. Numeric data pages are read-only and
the fixture's RNG state is writable. It uses declared UCRT bindings and
does not load engine services. It reads supplied files, releases private
allocations at exit, and reports comparison counts and body hashes to
stdout. A native fault fails the run. Inspect the source's exact page,
import and callback recipes before execution.

The accepted fixed-stage route checks both sampler branches, 144 packed
keys, three complete populations, a same-input repeat, both full canonical
reference bodies, and the independent planar point and bound comparison.
Wrong or missing inputs and incompatible hosts refuse. Complete D5AQ Option C
remains deferred. This procedure supplies no measured retail scheduler order.
[Original controls](../experiments/resource-retained-population/d5ag-geometry-controls.md) ·
[Original review](../experiments/resource-retained-population/d5ag-review.md)

## Projected event evidence

The candidate Episode A/B projection preserves equal rebuild, independent
equality, typed endings and the prespecified forecast. N2 preserves a
joined protected miss, sampling and store, and a negative target-overtake
stratum. The B2 projection preserves a positive decision inversion and its
negative cold-first controls. Original-to-derivative fidelity and omitted
fields follow the original custody and review. These checks require the exact
supplied archive and the corresponding project-owned reader. Episode A/B
and N2 use the qualified Windows CPython 3.14.3 import closure.
[Episode A](../experiments/resource-retained-population/d5ak-a-review.md) ·
[Episode B](../experiments/resource-retained-population/d5al-b-review.md) ·
[N2](../experiments/resource-retained-population/d5ap-review.md) ·
[B2](../experiments/resource-retained-population/d5ac-review.md)

| Projection | Reader and qualification target |
| --- | --- |
| Episode A/B | [Episode verifier](../../research/resource-retained-population/d5bh_verify.py) and [adverse controls](../../research/resource-retained-population/d5bh_controls.py), each with Python `-E -B`, exact ZIP path and `--sha256` from the inventory. Expect three complete normalizations, 196 pairs, 390 increments, four typed endings and 14 refusals. |
| N2 | [N2 verifier](../../research/resource-retained-population/d5bi_verify.py) and [adverse controls](../../research/resource-retained-population/d5bi_controls.py), with Python `-E -B` and the exact ZIP path. Expect 238,272 projected frames and 24 refusals. |
| B2 | [B2 verifier](../../research/resource-retained-population/d5bo_verify.py) with Python `-I -B`, exact ZIP path and `--sha256` from the inventory. The [control runner](../../research/resource-retained-population/d5bo_controls.py) uses `-E -B` with the same arguments. Expect 32,141 frames, one bounded overtake and 24 refusals. |

## Synthetic record framing

From the repository root, use CPython 3.14.3 and the standard library.

```text
python -I -B -c "import sys,runpy;sys.path.insert(0,'save-analysis/scripts');runpy.run_path('save-analysis/scripts/test_outpost_record_framing.py',run_name='__main__')"
```

The [suite](../../save-analysis/scripts/test_outpost_record_framing.py)
expects six passing tests of the bounded record grammar. It constructs its
operands in memory, reads no original save and reports unittest results.
Framing success leaves payload meanings and live ownership to the original
scientific evidence.

## Current source and historical methods

The [D5BZ source crosswalk](../../research/evidence-data/README.md) identifies
the relocated machine operands and changed reader sources. Use those paths
with this checkout. Historical receipts remain bound to their original
source hashes and are available by exact revision or archive member.

The [active source manifest](../../research/evidence-data/current-edition.json)
binds the D5CB resource-generation page and records the exact D5BZ page
revision and digest under `previous_current_edition`.
