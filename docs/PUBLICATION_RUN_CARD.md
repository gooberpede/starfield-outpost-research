# Publication run card — Starfield 1.16.244.0

**Template for a separately authorized release. Status: NOT READY / NOT CLEARED.**
Complete a release-specific copy and retain its receipts. The [publication policy](PUBLICATION.md),
[B0 gate matrix](audits/publication-readiness-b0/release-gates.md) and
[D5AW preparation sequence](audits/deferred-work-d5aw/publication-plan-amendment.md)
govern the checks and scope.

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
| Other pinned inputs and qualifiers | [B3 baseline and input manifest](audits/publication-readiness-b3/baseline-manifest.md) |
| Approved claim/build matrix revision, selected claims, exclusions | TBD |
| Historical save creation and effective load/configuration qualifications, by claim | TBD |
| Repository, candidate branch, frozen commit and tree OIDs | TBD |
| Proposed public refs and reachable-history boundary | TBD |
| Clean index/working-tree and inventory receipts | TBD |
| Document, verifier, manifest and package versions/hashes | TBD |

Record exact candidate Git identities with `git rev-parse HEAD "HEAD^{tree}"`,
`git status --porcelain=v1 --untracked-files=all`, and an inventory of refs/OIDs
and reachable objects for the proposed exposure. The EXE and ESM pins identify
the investigated baseline. Historical save origin, loaded data and effective
overrides need claim-specific evidence. Qualify a later build separately under
the [version update policy](audits/publication-readiness-b0/versioned-baselines.md)
and preserve historic address mappings.

## B. Scientific and evidence validation

| Gate | Required result and receipt | Status | Reviewer / timestamp |
| --- | --- | --- | --- |
| B0/B1 | Maintainer agrees [runtime and persistence scope](audits/publication-readiness-b1/claim-build-matrix.md), mandatory questions, exclusions, and negative cases. Independent reviews confirm selected conclusions and limits. | PENDING | TBD |
| B2 | [Contextual prose, notation and source-locator checks](audits/publication-readiness-b2/focused-rework.md) and current reader routes pass. | PENDING | TBD |
| B3 | [Method/source/dependency contracts](audits/publication-readiness-b3/report.md), versioned inputs, prerequisites, effects, reproduction and lawful availability are verified for selected methods. | PENDING | TBD |
| B4 | Every indispensable claim dependency has an agreed durable route and exact file-specific decision under C and D. | PENDING | TBD |
| B5 | [Selected creator safety](audits/publication-readiness-b5/report.md), output accounting and retention pass. | PENDING | TBD |
| B6 | Independent review binds the exact tree, reachable history/refs, claims, methods and packages to the clean-checkout receipt in F. | PENDING | TBD |

Copy a row for every selected claim and its indispensable dependencies.

| Claim / agreed scope and limit | Primary evidence / review / required negative cases | Dependency and transitive dependencies | Durable route, exact manifest and verification receipt | Status / reviewer |
| --- | --- | --- | --- | --- |
| D5AS qualified body comparisons, if selected | [D5BE access index](audits/evidence-access-d5be/README.md) | Complete canonical reference and sample bodies, roster and provenance | TBD | PENDING |
| C19 native UI comparisons, if selected | [D5BE access index](audits/evidence-access-d5be/README.md) | Complete recorded callback operands, native outputs and provenance | TBD | PENDING |
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

Use the [B4-F1 provisional index](audits/publication-readiness-b4/f1/README.md),
[asset manifest](audits/publication-readiness-b4/f1/assets.csv) and
[member manifest](audits/publication-readiness-b4/f1/members.csv) for exact
existing candidate data. Copy only approved final identities into the release
ledger. Record an explicit inclusion or exclusion and the effect on claims for
each optional group, including large supplementary audits.

| Group / candidate contents | Required or optional / include or exclude | Purpose / claims / producer | Final basename / count / bytes / codec / SHA-256 | Exact member manifest / SHA-256 | Rights and privacy receipt / staging location | Tag / release | Upload status / hosted URL / download and extracted-member checks |
| --- | --- | --- | --- | --- | --- | --- | --- |
| B4-F1 CORE, 25 unchanged first-party saves | TBD | F1 control and mature witnesses / TBD | TBD | F1 candidate linked above / TBD final | TBD | TBD | PENDING RELEASE / TBD / TBD |
| B4-F1 ADDENDUM, 14 unchanged saves and 13 original JPEGs | Optional / TBD | F1 supplemental witnesses / TBD | TBD | F1 candidate linked above / TBD final | TBD | TBD | PENDING RELEASE / TBD / TBD |
| D5AS geometry derivative | TBD / specific approval required | Qualified sample/reference comparisons / TBD | TBD | TBD | TBD | TBD | PENDING RELEASE / TBD / TBD |
| C19 native UI derivative | TBD / specific approval required | Native UI row comparisons / TBD | TBD | TBD | TBD | TBD | PENDING RELEASE / TBD / TBD |
| Later package or supplementary audit | TBD | TBD | TBD | TBD | TBD | TBD | PENDING RELEASE / TBD / TBD |

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
| Before B6 preflight acceptance | Test explicitly supplied, approved candidate packages in isolation. Record hashes, extracted-member results, and the planned durable route. Hold if clearance, exact bytes or a viable route are missing. | PENDING | TBD |
| Before upload | Review release notes, build/version statement, access limits, and download/verification instructions against the approved candidate. | PENDING | TBD |
| After authorized draft upload | Verify authorized draft links, actual downloaded package bytes and safe extracted member set, sizes and SHA-256. Compare final draft asset names, tag/target commit, and all changed Git/history/asset/link surfaces to the approval receipts. | PENDING | TBD |
| After authorized visibility change | Verify public reachability at the actual versioned URLs and download again. Record full container and member checks, Release/tag/commit identity, final tree/refs/history exposure and index consistency. | PENDING | TBD |

Keep a proposed URL as `TBD` until verified hosting. If linking the hosted
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
