# Publication run card — Starfield 1.16.244.0

**Template for a separately authorized release. Status: NOT READY / NOT CLEARED.**
Complete a release-specific copy and retain its receipts. The [publication policy](PUBLICATION.md),
[B0 gate matrix](audits/README.md#archive-lookup) (`audits.zip :: docs/audits/publication-readiness-b0/release-gates.md`) and
[D5AW preparation sequence](audits/README.md#archive-lookup) (`audits.zip :: docs/audits/deferred-work-d5aw/publication-plan-amendment.md`)
govern the checks and scope.

Use the [D5BG proposed claim and evidence reconciliation](audits/README.md#archive-lookup) (`audits.zip :: docs/audits/publication-claims-d5bg/README.md`)
to review claim wording, indispensable routes and remaining decisions before
freezing a candidate. Resolve claim-specific holds and agree the evidence tiers,
then coordinate archival of implementation briefs and administrative audits.
Recheck affected links and the intended exposure before candidate freeze.

| Order | Checkpoint | Status | Receipt / reviewer or approver / timestamp |
| --- | --- | --- | --- |
| A | Freeze the research candidate and planned exposure | PENDING | TBD |
| B–D | Close the science, rights, creator and evidence-package gates | PENDING | TBD |
| B6 | Obtain maintainer preflight authority and independently verify the exact frozen candidate in isolation | PENDING | TBD |
| E | Obtain approval for the exact tag and draft/upload operations | PENDING | TBD |
| F | Verify hosted bytes and changed disclosure surfaces | PENDING | TBD |
| G | Obtain final visibility/timing approval, execute and record the outcome | PENDING | TBD |

Use `PENDING`, `PASS`, `FAIL` or `NOT APPLICABLE` for gates. Record who decided
and when, plus the receipt or rationale. A mandatory `PENDING` or `FAIL` holds
its dependent actions. A `NOT APPLICABLE` decision needs a reviewed rationale
consistent with approved scope. Asset availability stays `PENDING RELEASE` until
hosting and verification are evidenced.

## A. Release identity and freeze

| Field | Value or receipt |
| --- | --- |
| Research release ID/version, title and notes draft | TBD |
| Native baseline | Starfield.exe **1.16.244.0**, preferred image base `0x140000000` |
| Executable SHA-256 | `7e9adb1414a8e1b325e5e1f097b9b17b78deb7eebeda37a333351a43a60f9d28` |
| Main Starfield.esm SHA-256 | `1dabed00c3f4282dd3bb54d2e9601e40b577d8742d078b7ccef203adbfef0da7` |
| Other pinned inputs and qualifiers | [B3 baseline and input manifest](reference/b3-baseline.md) |
| Approved claim/build matrix revision, selected claims, exclusions | [D5BG proposal](../research/evidence-data/publication-claims-d5bg/claims.json); approval and freeze receipt TBD |
| Historical save creation and effective load/configuration qualifications, by claim | TBD |
| Repository, candidate branch, frozen commit and tree OIDs | TBD |
| Proposed public refs and reachable-history boundary | TBD |
| Clean index/working-tree and inventory receipts | TBD |
| Document, verifier, manifest and package versions/hashes | [D5BF local proposal](audits/README.md#archive-lookup) (`audits.zip :: docs/audits/release-assets-d5bf/README.md`); freeze receipt TBD |

Record exact candidate Git identities with `git rev-parse HEAD "HEAD^{tree}"`,
`git status --porcelain=v1 --untracked-files=all`, and an inventory of refs/OIDs
and reachable objects for the proposed exposure. The EXE and ESM pins identify
the investigated baseline. Historical save origin, loaded data and effective
overrides need claim-specific evidence. Qualify a later build separately under
the [version update policy](audits/README.md#archive-lookup) (`audits.zip :: docs/audits/publication-readiness-b0/versioned-baselines.md`)
and preserve historic address mappings.

## B. Scientific and evidence validation

| Gate | Required result and receipt | Status | Reviewer / timestamp |
| --- | --- | --- | --- |
| B0/B1 | Maintainer agrees [runtime and persistence scope](audits/README.md#archive-lookup) (`audits.zip :: docs/audits/publication-readiness-b1/claim-build-matrix.md`), mandatory questions, exclusions, and negative cases. Independent reviews confirm selected conclusions and limits. | PENDING | TBD |
| B2 | [Contextual prose, notation and source-locator checks](audits/README.md#archive-lookup) (`audits.zip :: docs/audits/publication-readiness-b2/focused-rework.md`) and current reader routes pass. | PENDING | TBD |
| B3 | [Method/source/dependency contracts](audits/README.md#archive-lookup) (`audits.zip :: docs/audits/publication-readiness-b3/report.md`), versioned inputs, prerequisites, effects, reproduction and lawful availability are verified for selected methods. | PENDING | TBD |
| B4 | Every indispensable claim dependency has an agreed durable route and exact file-specific decision under C and D. | PENDING | TBD |
| B5 | [Selected creator safety](audits/README.md#archive-lookup) (`audits.zip :: docs/audits/publication-readiness-b5/report.md`), output accounting and retention pass. | PENDING | TBD |
| B6 | Independent review binds the exact tree, reachable history/refs, claims, methods and packages to the clean-checkout receipt in F. | PENDING | TBD |

Copy a row for every selected claim and its indispensable dependencies.
Use the [proposed evidence graph](../research/evidence-data/publication-claims-d5bg/evidence-edges.json)
and [decision ledger](../research/evidence-data/publication-claims-d5bg/actions.json) to populate this
table after the maintainer agrees scope. Keep each exact original-witness tier
separate from the corresponding authored mechanism or arithmetic tier. If a
selected claim needs an ADDENDUM member, identify that required reader download
in its verification instructions.

| Claim / agreed scope and limit | Primary evidence / review / required negative cases | Dependency and transitive dependencies | Durable route, exact manifest and verification receipt | Status / reviewer |
| --- | --- | --- | --- | --- |
| F1 saved-state and screenshot witnesses, at the agreed evidence tier | [F1 coverage](audits/README.md#archive-lookup) (`audits.zip :: docs/audits/publication-readiness-b4/f1/coverage.md`) | Exact selected first-party originals and lawful readers or inputs for the selected methods | D5BF CORE and ADDENDUM proposal under D; scope, clearance and B6 receipts TBD | PENDING |
| D5AS qualified body comparisons, proposed tier selected at D5BH | [D5BE access index](audits/README.md#archive-lookup) (`audits.zip :: docs/audits/evidence-access-d5be/README.md`) | Complete canonical reference and sample bodies, roster and attributed original qualification | D5BF D5AS candidate under D. Exact clearance and B6 receipts TBD | PENDING |
| D5AK/D5AL episode comparison and lifecycle witnesses | [D5BH local candidate assessment](audits/README.md#archive-lookup) (`audits.zip :: docs/audits/evidence-derivative-d5bh/README.md`) | Bounded A0/A1/B0 original-data projection with distinct process and frozen prediction checks | Exact public route held pending file-specific clearance, selection, transfer and B6 | PENDING |
| D5AO/D5AP N2 original-event and competition witnesses | [D5BI local candidate assessment](audits/README.md#archive-lookup) (`audits.zip :: docs/audits/evidence-derivative-d5bi/README.md`) | Projected direct constructor and complete recorded cohort with owner and alternative-continuation checks | Exact public route held pending file-specific clearance, approved transfer, B6 and hosting | PENDING |
| D5AQ exact controlled fixture | [D5BJ method and outcome](audits/README.md#archive-lookup) (`audits.zip :: docs/audits/evidence-reproduction-d5bj/README.md`) | Reader-supplied compatible game inputs, D5AS reference bodies, D5BI typed N2 projection and qualified continuation proof | Local bounded execution. Full dependency qualification, asset clearance, transfer, B6 and hosting pending | HELD |
| D5AG selected fixed stage | [Current native method](reference/evidence-access.md#fixed-native-geometry) | Exact D5AS archive, lawful EXE/ESM/PlanetData and compatible host | Selected conditional P-AG-FIXTURE. Exact-file and host checks remain part of B6. | PENDING |
| C19 native UI comparisons, if selected | [D5BE access index](audits/README.md#archive-lookup) (`audits.zip :: docs/audits/evidence-access-d5be/README.md`) | Complete recorded callback operands, native outputs and provenance | D5BF C19 proposal under D; clearance and B6 receipts TBD | PENDING |
| TBD | TBD | TBD | TBD | PENDING |

A durable route uses the public tree, an approved versioned Release asset, or
documented independent reproduction from public inputs. For first-time hosting,
B6 preflight may accept the approved exact asset and planned durable route
after an isolated check with explicitly supplied staged bytes. Record the
file-specific clearance and exact selection under C and D. Actual availability
stays pending until F verifies hosting. Hold an unresolved indispensable
dependency unless the maintainer approves narrowing or exclusion. Local paths
and hashes serve provenance. Record historical replay and calculation coverage
separately.

## C. Rights, privacy and attribution

| Surface | Review and decision to record | Status | Receipt / reviewer / timestamp |
| --- | --- | --- | --- |
| Exact tree, linked text/examples, code, scripts and assets | File-specific origin, rights, allowed use, privacy, notices and credits | PENDING | TBD |
| All proposed reachable Git history and refs | Exact object/ref inventory, secrets/personal data, past proprietary or unapproved blobs, large content and upload automation | PENDING | TBD |
| Authorship and licensing | Confirm author/contributor wording and grants, third-party boundaries, and `GPL-3.0-or-later` consistency | PENDING | TBD |
| Original saves, screenshots and game-derived evidence | Apply file-specific B4-F1 policy and separately review new derivative bytes and metadata. Hold proprietary, donor or other uncleared content. | PENDING | TBD |

Bind each clearance to the affected bytes, disclosure surface and approval
receipt. A clean current tree leaves previously reachable content in scope.
Any proposed history remediation requires its own approval and a new freeze.

## D. Packaged assets and member manifest

The [current candidate inventory](reference/evidence-access.md#candidate-inventory)
identifies seven candidate assets and two supplements. The
[D5BF ledger](../research/evidence-data/release-assets-d5bf/release-assets.json)
pins CORE, ADDENDUM, D5AS and C19. The
[D5BW ledger](../research/evidence-data/evidence-distribution-d5bw/assets.json)
joins all seven assets to their original member indexes. The
[D5BX supplement index](../research/evidence-data/evidence-access-d5bx/assets.json)
pins Workshop v2 and Cargo C3. Freeze these exact ledger revisions with the
claim matrix and clearance records under A. Record the effect on selected
claims of any change to the proposed membership.

| Group / candidate contents | Required or optional / include or exclude | Purpose / claims / producer | Final basename / count / bytes / codec / SHA-256 | Exact member manifest / SHA-256 | Rights and privacy receipt / staging location | Tag / release | Upload status / hosted URL / download and extracted-member checks |
| --- | --- | --- | --- | --- | --- | --- | --- |
| B4-F1 CORE, 25 unchanged first-party saves | Core / proposed include | Controlled and mature first-party saves | Ledger B4-F1-CORE | Ledger B4-F1-CORE | F1 scoped review and D5BF local receipt; final approval pending | TBD | PENDING RELEASE / PENDING RELEASE / TBD |
| B4-F1 ADDENDUM, 14 unchanged saves and 13 original JPEGs | Optional reader download / proposed include | Supplemental first-party saves and screenshots | Ledger B4-F1-ADDENDUM | Ledger B4-F1-ADDENDUM | F1 scoped review and D5BF local receipt; final approval pending | TBD | PENDING RELEASE / PENDING RELEASE / TBD |
| D5AS geometry derivative | Required for exact comparisons if selected / proposed include | Qualified sample and fixed-reference comparisons | Ledger D5AS | Ledger D5AS | D5BF payload assessment and local receipt; final approval pending | TBD | PENDING RELEASE / PENDING RELEASE / TBD |
| C19 native UI derivative | Required for exact callback census if selected / proposed include | Ordered native callback input and row comparisons | Ledger C19 | Ledger C19 | D5BF payload assessment and local receipt; final approval pending | TBD | PENDING RELEASE / PENDING RELEASE / TBD |
| Episode A/B projection | Selected derivative | A0/A1/B0 scoped lifecycle and equality comparisons | Ledger D5BH | D5BW member crosswalk | Pending candidate freeze and clearance | TBD | PENDING RELEASE |
| N2 projection | Selected derivative | Joined constructor, competition and negative controls | Ledger D5BI | D5BW member crosswalk | Pending candidate freeze and clearance | TBD | PENDING RELEASE |
| B2 projection | Selected derivative | Bounded inversion and cold-first controls | Ledger D5BO | D5BW member crosswalk | Pending candidate freeze and clearance | TBD | PENDING RELEASE |
| Workshop v2 and Cargo C3 | Supplementary reader operands | Selected P-ROOT-COUNTS and S-C23-SAVE52 checks | D5BX supplement index | D5BX supplement index | Exact-file custody, freeze and clearance pending | TBD | PENDING RELEASE |

For each package, record each exact member path/name, bytes, SHA-256, original
or derivative identity, producer and clearance. Bind the member inventory to
the package digest. Reject unexpected, missing or duplicate members, unsafe
paths, and hash/size mismatches. Compare the entire authorized upload inventory
to the final draft asset inventory and hold on omissions or extra files.

## E. Tags and publication actions

| Action | Exact target, command or platform action receipt | Authorization / status |
| --- | --- | --- |
| Record research tag name, naming policy and annotated/signed choice | TBD | TBD / PENDING |
| Compare frozen commit/tree and proposed exposure with target; check existing local and authorized remote tag collisions | TBD | TBD / PENDING |
| Create and verify tag after B6 ACCEPT and exact tag approval | TBD | TBD / PENDING |
| Transfer approved ref/tag, create approved Release draft, attach only D inventory | TBD | TBD / PENDING |
| Verify draft identity, assets and changed surfaces in F before final visibility decision | TBD | TBD / PENDING |

Research tags identify frozen research commits. Bethesda build numbers identify
game inputs, and asset basenames identify files. Record intended command
arguments and outputs. Compare the candidate and intended target commit OIDs
and tree OIDs. Use an exact local ref check such as
`git show-ref --verify "refs/tags/<tag>"` and a separately authorized remote
collision check. After tag creation, use `git rev-parse "<tag>^{commit}"` and
compare both the local and hosted tag targets to the frozen commit. A name
collision or target mismatch holds execution for a separate decision. Any ref
transfer, draft upload or other disclosure requires explicit authority for
that operation and recipient.

## F. Final release validation and hosted verification

| When | Check and required receipt | Status | Reviewer / timestamp |
| --- | --- | --- | --- |
| Before B6 acceptance | Clean checkout of exact commit with no access to existing `.local-work/`. Check relative links, case, anchors, actual rendered Mermaid diagrams, examples and verifiers with lawful prerequisites. | PENDING | TBD |
| Before B6 preflight acceptance | Supply the exact approved staged inputs for the seven candidates and two supplements to their [selected evidence checks](reference/evidence-access.md). Use the [D5BF ledger verifier command](reference/evidence-access.md#verify-d5bf-containers-and-members) for the four groups it covers. Bind the container/member and comparison receipts to the proposed tree, exposure and clearance. Hold if clearance, exact bytes or a viable route are missing. | PENDING | TBD |
| Before upload | Review release notes, build/version statement, access limits, and download/verification instructions against the approved candidate. | PENDING | TBD |
| After authorized draft upload | Verify authorized draft URLs and run the ledger verifier on the downloaded bytes. Compare final draft asset names, tag/target commit, and all changed Git/history/asset/link surfaces to the approval receipts. | PENDING | TBD |
| After authorized visibility change | Verify public reachability at the actual versioned URLs and download again. Record full container and member checks, Release/tag/commit identity, final tree/refs/history exposure, index consistency and notice availability. | PENDING | TBD |

Keep a proposed asset URL as `PENDING RELEASE` until verified hosting. If linking the hosted
asset changes reviewed repository bytes, hold for affected review and approval.
Keep the frozen tag bound to its approved commit. Record an independently
reviewed follow-up or new candidate decision for any Git-side link update.
For a first-time asset, B6 preflight gates tag creation and draft upload.
Verify draft downloads within the authorized access boundary before requesting
final visibility and timing approval. Public reachability is checked again
after authorized exposure.
Changes to bytes, refs, URL, manifest, rights, disclosure surface or approval
invalidate affected receipts. Resume only after affected review and approval.

## G. Signoffs, holds and incidents

| Decision or operation | Responsible operator / independent reviewer / maintainer | Exact scope and receipt / timestamp | Status |
| --- | --- | --- | --- |
| Maintainer authorizes release-candidate preflight scope and allowed actions | TBD | TBD | PENDING |
| Independent B6 preflight accepts the frozen candidate and reviewed routes | TBD | TBD | PENDING |
| Maintainer authorizes exact Git actions, tag and target commit | TBD | TBD | PENDING |
| Maintainer authorizes exact draft/upload actions, assets and recipient | TBD | TBD | PENDING |
| Maintainer authorizes final visibility, exposed refs/history and timing | TBD | TBD | PENDING |
| Operator records public verification and any incident | TBD | TBD | PENDING |

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
At 7C, inspect the contents of both containers, the retained tree, all proposed
refs and reachable Git history, and each candidate or supplementary asset.
Review privacy, rights, notices and custody against the exact proposed
bytes. Record the custodian and transfer decision before B6 isolation.
