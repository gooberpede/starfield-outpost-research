# D5BS native function catalogue generator audit

| Frozen question | Implementer result |
| --- | --- |
| D5BS-Q1 · Historical reproducibility | **COMPLETE.** The old and modern generators each reproduced the 16 accepted D5BD files from the original Git source set. The modern check also passed in a disposable tree without the original documents or private working receipts. |
| D5BS-Q2 · Explicit sources and editions | **COMPLETE.** Each manifest pins a Git commit, tree, build, ordered source paths and byte hashes, output paths and hashes, and a write namespace. |
| D5BS-Q3 · Safe generation and technical edition | **COMPLETE.** The historical verifier is read-only. Technical writes use an exclusive ignored receipt. Two isolated runs with different Python hash seeds matched for every output. Drift reporting detected an unselected audit without changing historical output. |
| D5BS-Q4 · Independent regression and documentation | **COMPLETE.** The independent reviewer reran both historical routes and the regression suite, verified source correspondence and navigation, and reconstructed both patches in both directions. |

[Original brief](../../implementation-briefs/CODEX_BRIEF_SOR_RG2_D5BS_Native_Function_Catalogue_Generator_Modernization.md) ·
[Investigation ledger](investigation-ledger.md) ·
[Developer commands](../../../research/function-catalogue/README.md) ·
[Independent review](review.md)

## Frozen inputs and comparison

The original source is commit `6e799a428a765aa196a24d3c1de8ae133260aa08`,
tree `7a1f6fdd6728a8f98bc92ef7ee6c9b24a62f0e0e`.
The [D5BD manifest](../../../research/function-catalogue/editions/d5bd.json)
pins 1,897 scan sources and 60 support sources. Its SHA-256 is
`cb2b6813335b8f8c444dbcb58530bd07701da59569a0257f848796a2ad5ea157`.
The historical checkout source selection was reconstructed independently of
the new generator using the old scan roots and exclusions against the
verified Git tree. The old generator ran in a disposable authored-text
export with the original sidecars and navigation dependencies. Its bytes
matched both the accepted Git blobs and the 16 working-tree originals.

The [technical manifest](../../../research/function-catalogue/editions/test-d5bs-v1.json)
pins D5BR HEAD `57e89d1ec2bcfdca4a22594b8eed081153c724cf`, with 1,977 scan
sources and 60 support sources. Its SHA-256 is
`d8cf607d9efe66677941d90b9019d3b3605baec237a1c0456f71e3931ac35094`.
All original manifest paths are present in this selection. Twelve common
paths have different Git bytes, of which one feeds the broad scan. The
technique keeps later source text out of the historical build even when
the paths coincide.

| Output | Historical to technical | Technical SHA-256 |
| --- | --- | --- |
| `coverage.csv` | 1,897 to 1,977 data rows. Adds 80 source paths. The existing disappearing-deposits report increases from 158 to 162 lines. | `f05822e7736630153e5744441c46bcff8941b23a7315f286691c35663bda00c2` |
| `locators.csv` | 8,336 to 8,543 data rows. Adds 207 lexical candidates and preserves all original rows. | `0fc45693d642b7a3cc45ee59d99dd855b2244a28332bc15ef0af311e705d6940` |
| Other 14 files | Byte-identical. Both retain 2,095 canonical entries with 18 A, 366 B and 1,711 C. | See the manifests. |

The two changed tables match the scope of the
[D5BG reproduction comparison](../publication-claims-d5bg/handoff.md#catalogue-reproduction).
The first technical regression run revealed a sort tie in the inherited
scanner. Seeds 1 and 4 produced locator SHA-256
`6f5fed4f8b7300a2de1aac3e636e0efe183fbedd5ec6dc24456d97ea62077fd1`,
whereas seeds 2 and 3 produced the hash shown above. Eight rows had both
`C19` and `c19` in their lexical mentions. Exact spelling now breaks the
case-folded sort tie. Both spellings survive and all D5BD bytes match.

## Original output inventory

Paths are repository-relative. These hashes match the original Git blobs,
the working-tree originals and the modern historical regeneration.

| Path | SHA-256 |
| --- | --- |
| `docs/audits/native-function-catalogue-d5bd/coverage.csv` | `a62c5b279b51f886b9350db2170501eb80267bce7187123e0d0c3b66761c8075` |
| `docs/audits/native-function-catalogue-d5bd/crosswalk.md` | `13194373ef539a6a6e22fdb70aec224b2e30191e952a8a4e51575af712d29ed1` |
| `docs/audits/native-function-catalogue-d5bd/locators.csv` | `556c94fe81774fde135b359f76ae3733be60663ef45b683ddfcb38a12b052d23` |
| `docs/audits/native-function-catalogue-d5bd/reference-addresses.csv` | `e5afa0b7be4fb6da3bfc966248524930c1cb048bd8c1936264de3f5f9cb40e79` |
| `docs/audits/native-function-catalogue-d5bd/repeated-aliases.csv` | `19197a8befd82eb61d55562668d3cc04a1ae0dec156501a9a60ff911a6b0ead8` |
| `docs/functions/aliases.csv` | `92321034b62aea3cfad7cbe909ad5c62b9df5c2afd2e6dfa7557c54a156d485c` |
| `docs/functions/catalogue.csv` | `b961222c961c44b8c4c0b773c98ab8eb868c433b8b575298769e29b5f093d2af` |
| `docs/functions/evidence.csv` | `bd06810c58f229c0709c124b894550aced91fd449d1594c633e297b86cddc848` |
| `docs/functions/geography.md` | `b17521355563d1671afb6d690a9c1d24ef314e2c682330c077e7b84eaad417ed` |
| `docs/functions/index.md` | `16619cc48b75b51b3a67a08dbf39f6add8cac3b4ed94a83cf4fd3fd6ce73d192` |
| `docs/functions/interfaces.md` | `a34074929595f4aba9281cc343e6c6cfd6c07713a2554c086fe615cff3d0ec0b` |
| `docs/functions/inventory.md` | `0a07c03f44b7e05f732bb15d2f0a9ed8e94a6f7a2db8a2c5bf96ac5e1c90af4a` |
| `docs/functions/population.md` | `fad3be9ca6fdc477eb5bd0e857ba7aea27de9ef48159ed8cd98420cd0f8b3935` |
| `docs/functions/power.md` | `546466aef48082edc1439c196a12d4fc6137c23c5c92fd5818c314adf1a91812` |
| `docs/functions/production.md` | `17bfcfba49e16259e3bf870aea4f6f39947011f698e5f18e3fe123ba077246db` |
| `docs/functions/workshop.md` | `e2c007a1c7a28397dc12cd2647d52205c2d8990f4af4485131f22e5f19a11f5c` |

## Controls and effects

The modern generator verified 325 historical and 326 technical link targets
against the respective pinned source sets. A separate comparison of
historical source references against current working-tree text found no
changed physical spans in the 193 cited rows whose underlying source file
had different bytes. The relative links remain checkout-relative. Exact
reproduction and source coordinates belong to the pinned tree.

The retained [D5BD closure](../native-function-catalogue-d5bd/closure.md),
[build baseline](../publication-readiness-b3/baseline-manifest.md), historical
[function register](../../function-register.md),
[crew function table](../../experiments/crew/functions.csv) and
[export namespace guide](../publication-readiness-b2/native-export-ids.md)
control the identity and alias checks. Existing generator guards still
exercise `SOR-FN-0062` through `SOR-FN-0064`, the organic heading, transit
shorthand, storage and extractor aliases, the power exception, excluded
sites and the 18 subsystem crosswalks. All catalogue, alias, evidence and
crosswalk bytes match. The lexical additions do not create canonical entries.

Run these commands with the installed CPython 3.14.3. Local receipts under
`.local-work/function-catalogue/d5bs-proof/` retain stdout, stderr and exits,
plus the oracle and comparison scripts.

```text
python -B research/function-catalogue/verify.py
python -B research/function-catalogue/verify.py --edition test-d5bs-v1
python -B research/function-catalogue/verify.py --drift
python -B research/function-catalogue/test_editions.py
python -B research/editorial/screen.py --changed
```

The test runner copies just the tooling and manifests to disposable
directories. A historical run works without checkout source text. A later
run adds an unselected audit with an interior site and historical alias,
and an altered checkout copy of a selected source. Output hashes stay
identical and the drift listing reports the new document with its digest.
Separate technical runs compare all bytes and preserve 16 historical-path
sentinels per run. Negative controls cover an absent Git path, an omitted
required manifest entry, a different source version with a matching
checkout decoy, a wrong edition, executable or tree, malformed JSON,
duplicate source, an output/source collision, a wrong output digest, a
historical namespace, default historical write and an occupied technical
namespace. Each refusal preserved the fixture's original bytes.

The proof used regular Git blobs of authored text and reviewed metadata.
The C: and D: free-space floors were checked around validation. Scratch
outputs, patches and test receipts remain local. The game, installed
inputs, original saves and raw exports were outside the read and write
sets. No protected content rehash or native replay was part of this test.
Git state and complete/task-only patch reconstruction are in the local
delivery manifest. The supplied untracked brief is included in the complete
patch and excluded from the task-only patch.

## Reading applied

| Required reading | Application |
| --- | --- |
| [Standing orders](../../../AGENTS.md), [workflow](../../../WORKFLOW.md), [third-party policy](../../../THIRD_PARTY_POLICY.md), [charter](../../CHARTER.md) and relevant [research state](../../RESEARCH_STATE.md) | Kept the task text-only and local, used the existing project-authored method and installed tools, and left native, save and deferred research outside the execution boundary. |
| [Evidence standard](../../EVIDENCE_STANDARD.md), [D5BD brief](../../implementation-briefs/CODEX_BRIEF_SOR_RG2_D5BD_Native_Function_Catalogue_and_Developer_Reference.md), [D5BD audit](../native-function-catalogue-d5bd/README.md), its closure and the [catalogue guide](../../functions/README.md) | Preserved source-local alias scope, build/module/RVA identity, evidence and locator domains, original output paths and external-use cautions. Compared the original authored source locations where historical IDs collide. |
| [Completion protocol](../../RESEARCH_EXECUTION_PROTOCOL.md), [contract template](../../templates/completion-contract.md), [editorial standard](../../EDITORIAL_STANDARD.md) and [reviewer procedure](../../reviewers/research-completion-reviewer.md) | Kept the original question IDs, an active ledger and failed seed controls. Screened and read changed prose and prepared an exact-snapshot review with forward and reverse patches. |
| [D5BG handoff](../publication-claims-d5bg/handoff.md), [D5BR report](../evidence-readiness-d5br/README.md), [execution plan](../evidence-readiness-d5br/execution-plan.md) and [publication run card](../../PUBLICATION_RUN_CARD.md) | Separated exact text reproduction from original evidence replay, item 5B and B6. Kept the test-edition bytes in a local engineering namespace and documented the local Git object dependency. |
| [Original scanner](../../../research/function-catalogue/inventory.py), [verifier](../../../research/function-catalogue/verify.py), curated sidecars and original namespace and build proofs | Traced all text, ledger, sidecar and link reads. Used Git bytes for the same physical line semantics and kept the old discovery predicate solely for drift. |

## Acceptance matrix

| Criterion | Implementer check | Evidence |
| --- | --- | --- |
| AC01 | PASS | Reading coverage and controls above. |
| AC02 | PASS | Pinned original tree, all 16 original hashes and two-file comparison. |
| AC03 | PASS | Old-generator export and modern byte comparisons. |
| AC04 | PASS | Ordered manifest, Git pins and source refusal controls. |
| AC05 | PASS | Injected checkout document and two independent technical invocations. |
| AC06 | PASS | Read-only drift output and unchanged historical hashes. |
| AC07 | PASS | Original bytes, address/alias guards and all 18 crosswalks. |
| AC08 | PASS | Negative controls and pre/post fixture snapshots. |
| AC09 | PASS | Developer commands, local Git object prerequisite and source-only fixtures. |
| AC10 | PASS | Accepted bytes, checkout inventory and local delivery manifest. |
| AC11 | PASS | Changed prose screen, manual reading, link and coordinate checks. |
| AC12 | PASS | Independent ACCEPT with exact source, file and patch verification. [Review return](review.md). |

Scientific and evidence classifications follow D5BD. The technical edition
qualifies a reproducible text-generation workflow. Its receipts have no
scientific or release approval. B6, item 5B and publication clearance remain
separate under the run card.
