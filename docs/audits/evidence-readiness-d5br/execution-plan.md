# Verification plan for separate authorization

Roadmap item 5B remains **OPEN**. These stages define test inputs and
evidence, with a separate authorization for each operation. The
[crosswalk](readiness.json) binds selectors, assertions, negative cases and
reader hashes. An audit outcome, a qualified method and a B6 acceptance are
separate.

## Stage 0 — bind inputs and establish safe staging

1. Confirm the exact tier and asset/member choices for the run. Use the
   [D5BF ledger](../release-assets-d5bf/release-assets.json) and exact later
   derivative ledgers, with an explicit staged input list. Verify basenames,
   container/member identity and versions. Reuse one receipt across all
   consumers of the same immutable staged input. A manifest entry is a
   locator and expected digest. Require an actual matching file.
2. Use a caller-owned isolated workspace, excluding the active save
   directory, original historical output paths and existing `.local-work/`
   except separately authorized retrieval of named inputs. Verify immutable
   originals and protected receipts before and after. Preserve the C: and D:
   floor of **40,000,000,000 caller-available bytes each** before substantive
   writes and through work as applicable. Account for peak decoded copies,
   intermediates and outputs per [B5](../publication-readiness-b5/report.md).
   Use fresh exclusive output names and never write original saves, receipts
   or game inputs. Keep decoded streams, maps, exact installed bytes and
   detailed diagnostic outputs local. Account for ownership and retention
   before authorizing cleanup. Preserve a failure before any retry.
3. Pin the exact reader source, transitive imports, Python/environment, output
   paths and expected effects. Check [B3 contracts](../publication-readiness-b3/method-reproduction.md)
   and [input pins](../publication-readiness-b3/baseline-manifest.md) before
   constructing any historical layout. Treat a pinned legacy helper as code
   to inspect before invocation. Reject hard-coded active-save inputs,
   whole-corpus modes, pre-existing output paths, private receipt dependencies
   with no authorized supply and unsafe archive paths.
4. Bind a receipt to container/member digests, source/reader/build pins,
   invocation, supplied input paths privately, actual supported header/branch,
   positive and control outputs with coordinate or byte domain, failure cause,
   exit status, pre/post protection and allowed outputs. Require a second
   independent framing walk or separately derived oracle for the decisive
   field comparisons. Send authored summaries and exact private receipt
   identities to the authorized reviewer. Absent input or incompatible header
   means a refusal and a held claim route.

## Stage A — selected originals

Stage CORE and ADDENDUM once, process selected members in explicit input order,
and keep one immutable decoded buffer per member and compatible framing domain
where downstream adapters can use it. Reuse original and decoded identities
across branches. Methods with different qualified decode contracts receive
separate receipts. Run the portable framing control first. It covers record
closure and failure cases, with semantic comparisons in the subsequent steps.

Synthetic entry point (only under the later batch authorization): use the
[B3 isolated recipe](../publication-readiness-b3/method-reproduction.md#runnable-representative-synthetic-record-framing)
with exact `test_outpost_record_framing.py`, `outpost_record_framing.py` and
`stream_save.py` copied to an empty caller-owned directory. With existing
CPython 3.14.3, run:

```text
<python> -I -B -c "import sys,runpy;sys.path.insert(0,'.');sys.argv=['test_outpost_record_framing.py'];runpy.run_path('test_outpost_record_framing.py',run_name='__main__')"
```

Expect six methods, with independent walk agreement, count-width, truncation,
exact closure and prefix/decoy controls. Stop on output drift or a failing
control. No original input is provided to this command.

| Batch | Required test and review checkpoint |
| --- | --- |
| A1 · Coordinates and nominal biomes | Use CORE F001/F002/F003/F047/F053, F040 and ADDENDUM F049. Resolve exact Save26 identity and fixed anchors. Compare player, beacon, descriptor, typed world joins and frame arithmetic, including fixed centre after compensated shift and negative-X direction. Then match lawful pinned v5 map members and positive-area cell checks. Save39 is the held-out Kreet case. Keep the HIST-0035 nonunique descriptor and the separate Save25 unrelated type-6 failure visible. Supply the source/definition/body context explicitly. [Position](../../experiments/coordinate-sufficiency/report.md) · [Biomes](../../experiments/outpost-biomes/saves.md) |
| A2 · Mature witnesses | Stage F064, F051 and F040 once, plus F042/F043 for root controls. Verify F064's 17 fabricators/14 groups and BF/base/producer fields, 24 local paths and boundary cases using only the selected E3 scope. Separately derive the 17 SD2 fixture-to-beacon joins and recount the F051/F040 controls at 16/17. For F040 also compare C1 pair roles, C2 shared hold and recognized/unknown inventories, C3 four fuel-source rows and branch controls, and the population route's 657+191 root identities. Preserve the named owner, type and offset domains. Retrieve C3's named archive members only after approval, and independently establish or stage the roots context per schema. [E3](../../../research/e3-fabricators/README.md) · [SD2](../../experiments/shared-outpost-storage/methods.md) · [C2](../../experiments/cargo-links/transport/saves.md) · [C3](../../experiments/cargo-links/fuel/saves.md) · [Roots](../../experiments/workshop-population/schema.md) |
| A3 · Save29 | Hold the exact route until a finite adapter is independently qualified or the historical helper is recovered and staged. Start from the tracked workshop_inventory.linked_prefix ExtraBC grammar and compare it with the strict saved_instances.extra_view adaptation, including counted-extra end and reference cursor. Then use F054 and selected definitions to check four REFR, four ordered CB and four Extra9C spans, and the swapped demand control. Keep the old flag contrast separate from allocation. No replay of the three historical loads. [Authority and controls](../../experiments/power/save29-authority.md) |
| A4 · Local links | Use F032 and F055–F059. Compare exact four role windows, failed original literal and failed token-only substitution, length/discriminator changes and same-session pair equality. Historical main has an active-save copy mode and older fixed dependencies. Qualify an explicit six-save adapter around the owned pure window logic. No incidental exit-save input. [Original sequence](../../experiments/output-link-validation-L0-L2C.md) |
| A5 · Display slot | Stop at the missing portable type-6 reader route. Review the two known local sources and exact pending-dialogue branch for approved supply or qualify a bounded equivalent. Check F067 closed component sections, zero fixture stock, helmet slot and reverse links, independent backpack case and unsupported extras. Report exact decoded offsets and provenance. [SD1 methods](../../experiments/containers-displays/methods.md) |
| A6 · Construction, placement and visual context | Reuse eligible CORE controlled buffers and F051, and stage the six F011–F016 originals. Compare typed roots, disabled/deleted state, budget/registration and the two 0→1→3 sequences with their distinct bulldoze counts. Review the listed supporting JPEGs separately against the recorded restriction, intersection and permissive previews. Absence of a rejected XYZ, paired variant action or synchronized image/save join remains a scope boundary. [Placement](../../experiments/spatial-placement/report.md) · [Variants](../../experiments/construction-variants/report.md) |

For A1, A2, A4 and A6, a finite safe source route is identified, with some
staging or adapter qualification still required. In particular, E3's saved
entry point scans the historical corpus, SD2's join main hardcodes the fresh
trio, and the L-series validation main can copy active saves. A selected
reproduction authorizes only its input list and owned scratch. The necessary
reviewable output is one receipt per route and one shared identity receipt per
immutable input. If the finite selector fails or prerequisite is unavailable,
hold the affected exact claim and report the supported authored or attributed
tier for a maintainer decision. A compatible unrelated save is never a
replacement oracle.

## Stage B — standalone derivatives

These are read-only scientific comparisons on explicitly supplied candidates,
with control mutations performed in memory. Their prior local and isolated
passes suffice at the selected method tier. Avoid an additional real-data pass
before B6 unless the exact candidate, method or qualification changes. No
builder, archived source data or game installation is required for these checks.

| Batch | Exact reader instructions and expected result |
| --- | --- |
| B1 · D5AS | Use D5BF's shared integrity verifier then the standalone `d5as_verify.py` with exact SHA and `--negative-controls`. Check all 30 complete canonical bodies against both references, exclusion and replacement, and six refusals. [D5AS contract](../evidence-access-d5be/d5as.md) |
| B2 · C19 | Use `c19-verify.py` with exact SHA and `--negative-controls`. Check all 346 ordered comparisons and six refusals. Keep `--self-test` as a separate synthetic result. [C19 contract](../evidence-access-d5be/c19.md) |
| B3 · Episode | Supply the exact ZIP with all 27 preflight members and use `d5bh_verify.py` and `d5bh_controls.py` with `-E -B` and the pinned SHA. Use the qualified Windows CPython host. Check A0, lifecycle, process and forecast comparisons, including equal-but-wrong A0. [Episode contract](../evidence-derivative-d5bh/README.md) |
| B4 · N2 | Supply the six-member ZIP to `d5bi_verify.py` and `d5bi_controls.py` with `-E -B` and no optimization. Use Windows CPython 3.14.3 because the authored import chain resolves Windows modules. The D5BH verifier source is imported, with no D5BH ZIP dependency. Check constructor/competition and all 24 controls. [N2 contract](../evidence-derivative-d5bi/README.md) |
| B5 · B2 | Use `d5bo_verify.py` with `-I -B` and `d5bo_controls.py` with `-E -B` and exact SHA. Check 32,141 projected frames, decision inversion and all 24 controls. Retain unqualified decisions and earlier same-geography births. [B2 contract](../public-evidence-d5bo/b2-asset.md) |

For each, stage only after applicable rights and transfer decisions. Keep
stdout/exit and the exact method, manifest, asset and member pins. Fail the
dependent route if the isolated run reads a private path, relies on hidden
environment state, loses a negative case or reports different science. The
hosted checks later confirm actual download bytes separately.

## Stage C — conditional D5AG native reader

Require explicit native-execution authority and a supported separate fixture
process. Recheck lawful N244 EXE, main ESM, PlanetData BA2 and its exact Feynman
raster, D5AS ZIP and Windows AMD64/Python/UCRT/CPU/OS/page compatibility. Verify the complete 33-member D5AS ZIP first. The two reference bodies
are the native comparison operands. Use the
[unchanged geometry command](../public-evidence-d5bo/d5ag-reader.md) and
[dependency inventory](../evidence-reproduction-d5bj/dependencies.md).
The private process maps selected game code pages, runs the original sampler
and geometry paths, allocates private buffers and releases them on exit.
Process isolation bounds memory lifetime. Use the approved host and execution
boundary. The shared-host STOP for the deferred continuation remains in force.

Collect separate receipts for refusal before mapping incompatible bytes, both
sampler branches, all packed keys, three complete populations, full
same-mask equality and independent planar checks. A fault, incomplete
allocation/append, missing atlas, changed ZIP or preflight refusal holds the
native route. Preserve exact stdout/exit and protections. Readers without
lawful compatible inputs can still check the D5AS precomputed body tier.

## Stage D — freeze and reader preflight

Perform normal tracked arithmetic and source review in the candidate, including
D5AT's 17 sites, relation partition, 65 exclusions, rank totals and fixed
historical attribution. The authored scopes for inventory, crew, placement,
position, power, production, static interfaces and resource generation stay
within their exact source/version records. A source-level explanation may be
inspectable with no external data, while independent byte-level rereads of
installed definitions, PEX/VMAD, SWF, rasters or native instructions need lawful
pinned inputs. Use the crosswalk to distinguish those claims.

After the separately authorized archive and clearance decisions, freeze the
exact commit/tree, refs/reachable history, assets, notices, reader methods and
release wording. Isolate B6 from existing private work and independently
verify selected evidence, complete reader navigation, all applicable build and
side-effect contracts, actual rendered examples and exclusions. Bind B6 to that
candidate. Release draft/upload and visibility/timing each need their own
authority. Verify authorized draft and public downloads against the same
container/member ledger. See the [publication run card](../../PUBLICATION_RUN_CARD.md).
