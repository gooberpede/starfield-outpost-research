# Publication run card — Starfield 1.16.244.0

**Starfield Outpost Research v1.0.0 (Starfield 1.16.244.0)**

**Release preparation approved and verified.** The maintainer confirmed
closure of A–D and B6 and approval of the remaining release operations on
2026-11-12. The four remaining operations are to create the tag, create the
GitHub Release draft, upload the nine approved assets, and make the release
public. Record the tag, draft, upload and public verification receipts as
each operation is performed.

Retain the exact candidate and operation receipts. The [publication policy](PUBLICATION.md),
[B0 gate matrix](audits/README.md#archive-lookup) (`audits.zip :: docs/audits/publication-readiness-b0/release-gates.md`) and
[D5AW preparation sequence](audits/README.md#archive-lookup) (`audits.zip :: docs/audits/deferred-work-d5aw/publication-plan-amendment.md`)
govern the checks and scope.

Use the [D5BG proposed claim and evidence reconciliation](audits/README.md#archive-lookup) (`audits.zip :: docs/audits/publication-claims-d5bg/README.md`)
for historical preparation. Use the [first-release scope](first-release-scope.md)
and [current route lookup](history/evidence-routes.md) for the selected claims,
indispensable dependencies and reader tiers.

| Checkpoint | Status | Basis |
| --- | --- | --- |
| A–D and B6. Candidate freeze, scope, evidence, rights, packaging and isolated preflight | PASS | Maintainer confirmation, 2026-11-12. See A–D and F for the underlying records. |
| E. Create the tag and draft, then upload the approved assets | APPROVED · TO DO | Maintainer confirmation, 2026-11-12. See E for the sequence. |
| F. Check served bytes and release identity during execution | TO DO | Capture draft and public receipts as part of upload and publication. |
| G. Make the release public | APPROVED · TO DO | Maintainer confirmation, 2026-11-12. Execute after draft verification. |

## A. Release identity and freeze

| Field | Value or receipt |
| --- | --- |
| Research release title | Starfield Outpost Research v1.0.0 — Starfield 1.16.244.0 |
| Native baseline | Starfield.exe **1.16.244.0**, preferred image base `0x140000000` |
| Executable SHA-256 | `7e9adb1414a8e1b325e5e1f097b9b17b78deb7eebeda37a333351a43a60f9d28` |
| Main Starfield.esm SHA-256 | `1dabed00c3f4282dd3bb54d2e9601e40b577d8742d078b7ccef203adbfef0da7` |
| Other pinned inputs and qualifiers | [B3 baseline and input manifest](reference/b3-baseline.md) |
| Selected claims, build and exclusions | [First-release scope](first-release-scope.md) and [selected route ledger](../research/evidence-data/evidence-closure-d5bv/routes.json) |
| Historical save creation and effective load/configuration qualifications | [First-release scope](first-release-scope.md) and the [evidence access contract](reference/evidence-access.md) |
| F0, approved committed intake | `main` commit `722d779568d56730e03c9585154d1c9a6ad93917`, tree `880ea503ee942b64f4cec2307a625a13db18f8b4` |
| D5CC independently reviewed F1 overlay tree | `9a837bec47ba7cc3c4cf868684be0f5368e118ab`. Historical pre-integration receipt in `.local-work/b6-preflight/handoff.md`. |
| Approved disclosure boundary | Ordinary ancestry of the sole `main` branch. The reserved release tag is uncreated. Additional refs and history changes require separate decisions. |
| Release candidate | `main` commit `dd426e8b1f2dbe647d5d996a16097a3b627a6fc2`, tree `17b2e131c2701917cacc09ecf653ba18c3556fd0`. Clean index and working tree at reconciliation. |
| Document, verifier, manifest and package identities | The candidate tree binds the tracked inputs. The ledgers in D bind the nine staged assets. |

Use the recorded release candidate as the tag target. Later run-card receipt
edits are operational records. A changed release target needs an explicit
candidate decision. The EXE and ESM pins identify the investigated baseline.
Qualify a later build separately under the
[version update policy](audits/README.md#archive-lookup) (`audits.zip :: docs/audits/publication-readiness-b0/versioned-baselines.md`)
and preserve historic address mappings.

## B. Scientific and evidence validation

| Gate | Status | Basis |
| --- | --- | --- |
| B0/B1. Scope, build, exclusions and evidence tiers | PASS | [First-release scope](first-release-scope.md) and the maintainer's scope decisions. |
| B2. Prose, notation and navigation | PASS | [Focused rework](audits/README.md#archive-lookup) (`audits.zip :: docs/audits/publication-readiness-b2/focused-rework.md`) and D5CC navigation and rendering checks. |
| B3. Method and source contracts | PASS | [Baseline and input manifest](reference/b3-baseline.md) and the [evidence access contract](reference/evidence-access.md). |
| B4. Evidence routes and exact file selection | PASS | [Selected route ledger](../research/evidence-data/evidence-closure-d5bv/routes.json) and the R4 decisions in C and D. |
| B5. Creator safety, output accounting and retention | PASS | [B5 report](audits/README.md#archive-lookup) (`audits.zip :: docs/audits/publication-readiness-b5/report.md`) and the maintainer's closure confirmation. |
| B6. Isolated verification of the release scope | PASS | D5CC independently accepted the tested overlay at the selected tiers. The maintainer confirmed final candidate approval and verification on 2026-11-12. |

Use the [selected route ledger](../research/evidence-data/evidence-closure-d5bv/routes.json)
for all 68 distinct routes and 126 claim-to-route joins and the
[inherited evidence graph](../research/evidence-data/publication-claims-d5bg/evidence-edges.json)
for their claim context. Keep each exact original-witness tier
separate from the corresponding authored mechanism or arithmetic tier. If a
selected claim needs an ADDENDUM member, identify that required reader download
in its verification instructions.

| Selected evidence | Verification disposition |
| --- | --- |
| CORE and ADDENDUM saved-state and screenshot witnesses | Verified at the [selected original-reader tiers](reference/evidence-access.md#selected-original-witnesses). |
| D5AS complete-body comparisons, D5BH episode witnesses, D5BI N2, D5BO B2 and C19 | Verified at the [selected derivative tiers](reference/evidence-access.md). |
| Workshop v2 and Cargo C3 supplements | Verified with the [selected original readers](reference/evidence-access.md#selected-original-witnesses) and exact supplements. |
| D5AG fixed native stage | Conditional reader route. D5CC checked the input and host pins and the non-native D5AS tier. Native execution was outside the completed preflight checks. [Method and prerequisites](reference/evidence-access.md#fixed-native-geometry). |
| D5AQ exact controlled fixture | Held outside the selected release scope. [D5BJ method and outcome](audits/README.md#archive-lookup) (`audits.zip :: docs/audits/evidence-reproduction-d5bj/README.md`). |

The Geography command needs CORE F001/F002/F003/F040/F047/F053, ADDENDUM
F049, the matching main ESM and PlanetData BA2, and an exclusive output
directory. L-series needs CORE F032 and ADDENDUM F055–F059 in the documented
flag order. Workshop v2 needs CORE F040/F042/F043, the exact supplement and the
matching main ESM. Cargo C3 needs CORE F040 and the exact C3 JSON. Use the
[current source edition](../research/evidence-data/README.md) for Fabricators,
Controls and the other selected methods. Shared Storage also requires the pinned
`SFBGS00D.esm` in the [B3 input manifest](reference/b3-baseline.md).
Native D5AG additionally needs the
exact host, lawful inputs and separate process authority.

The release uses the tracked tree, the nine versioned Release assets and
documented reproduction from reader-supplied inputs. The selected assets
were checked from staged bytes. Section F records the served-download checks
during execution.

## C. Rights, privacy and attribution

| Surface | Status | Basis |
| --- | --- | --- |
| Exact tree and reachable `main` history | PASS | Maintainer approval of the disclosure boundary in A and 2026-11-12 closure confirmation. |
| Authorship, licensing, attribution and notices | PASS | [R3 wording](DECISIONS.md#r3-author-and-contributor-wording), D5CC preflight and the maintainer's closure confirmation. |
| Original saves, screenshots and game-derived evidence | PASS | [R4 file-specific decisions](DECISIONS.md#r4-asset-and-excerpt-decisions) for the exact inventory in D. |

Retain the accepted B02 twelve historical paths and `ACTIVE` marker, and the
separate four historical C3 fields. Preserve the CyberDanz credit and exclude
third-party saves from the repository and Release assets.
[B02 and R4 decisions](DECISIONS.md#d5cb-pre-freeze-evidence-and-distribution) ·
[Credits](../CREDITS.md)

## D. Packaged assets and member manifest

The [current candidate inventory](reference/evidence-access.md#candidate-inventory)
identifies seven candidate assets and two supplements. The
[D5BF ledger](../research/evidence-data/release-assets-d5bf/release-assets.json)
pins CORE, ADDENDUM, D5AS and C19. The
[D5BW ledger](../research/evidence-data/evidence-distribution-d5bw/assets.json)
joins all seven assets to their original member indexes. The
[D5BX supplement index](../research/evidence-data/evidence-access-d5bx/assets.json)
pins Workshop v2 and Cargo C3. The approved upload inventory is exactly those
nine files in `.local-work/release-assets/1.16.244.0/`. The candidate inventory
and ledgers give the exact basenames, byte counts, hashes and member identities.
D5CC checked all nine files and 125 indexed member identities. The uploads
are still to do. Verified hosted downloads become the recovery route.

## E. Release operations

| Step | Approved operation | Status |
| --- | --- | --- |
| 1 | Create and verify `v1.0.0+sf1.16.244.0` at the exact commit in A. Check for local and hosted tag collisions before creation and verify the tag resolves to the approved commit. | TO DO |
| 2 | Create the GitHub Release draft using the title and tag in A and E. Record the draft identity and include the build, access limits and verification instructions from the selected scope and evidence access contract. | TO DO |
| 3 | Upload exactly the nine files in D to the draft. Verify the draft inventory and served bytes as described in F. | TO DO |
| 4 | Make the release public after the draft checks pass. Record the public release and verification receipts in F and G. | TO DO |

## F. Verification receipts

| When | Receipt | Status |
| --- | --- | --- |
| Isolated preflight | D5CC handoff records clean-checkout isolation, missing-input refusal, rendered diagrams, navigation, selected method checks and the nine-asset seal. The maintainer confirmed closure on 2026-11-12. | PASS |
| During draft upload | Verify the hosted tag and target commit. Download the nine draft assets and match the exact inventory, container or standalone hashes, and all 125 indexed member identities to D. Check the draft's disclosure surfaces against the approved boundary in A. | TO DO |
| During publication | Record the public Release URL and tag target. Verify public reachability and repeat the inventory, container and member checks at the versioned download URLs. Confirm the exposed refs and notices. | TO DO |

Asset URLs stay `PENDING RELEASE` until hosting is verified. A Git-side URL
update belongs in a reviewed follow-up so the release tag stays bound to A.

## G. Signoffs and incidents

The maintainer's 2026-11-12 confirmation closes preparation and records
approval of the tag, draft, asset upload and final visibility operations for
the scope above. Record the actual tag and target, draft and public URLs,
asset verification receipts, operator and execution timestamps when the
operations are performed.

On a gate failure, identity mismatch, omitted or unapproved asset, rights/privacy
finding or missing authorization, stop the dependent action and preserve the
receipt. Notify the maintainer with the affected scope and record the approved
remediation, re-review and restart point. Before exposure, keep any draft on hold
within its authorized access boundary. If exposure already occurred, record
what was exposed, when and where, and seek separate authority for any corrective
platform action. Removal cannot recover copies of public tags, history or assets
already obtained by others.

## D5BZ document archives and 7C handoff

Use the [current evidence access contract](reference/evidence-access.md) for
the seven candidate assets and the two supplementary inputs. The
[current source edition](../research/evidence-data/README.md) records their
machine operands and verifier commands. The [archive verification record](archive-verification.md)
binds the first-release documentation containers and their member indexes.
Use the approved candidate and custody records above when executing the
four release operations.
