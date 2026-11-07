# Proposed publication preparation sequence v2

2026-11-07, Australia/Sydney. This amendment is proposed for maintainer
decision. [Publication policy](../../PUBLICATION.md) and the
[B0 gate matrix](../publication-readiness-b0/release-gates.md) remain controlling.
The first release must explain runtime and persistence together within its agreed
scope. Publication status is **NOT READY / NOT CLEARED**.

Version 2 incorporates the binding
[maintainer retention amendment](../../DECISIONS.md#d5aw-local-working-evidence-and-publication-independence--2026-11-07).
The earlier [D5AW review](review.md) records its original snapshot and verdict.

| Order | Workstream and dependency | Reviewable output and exit condition |
| --- | --- | --- |
| 0 | D5AW reconciliation and maintainer scope decision (B0/B1) | Review this register, agree exact first claims, native build, exclusions and advertised access tiers. Decide whether later resource work is included. Record changed claims and required evidence explicitly. |
| 1 | Tracked tree and publication architecture inventory (B1/B2/B3/B4, B6 planning) | Freeze tracked path/blob inventory and trace selected claims and tracked references to their consequential original inputs. Deliver a claim dependency ledger, proposed evidence routes and blockers with the link census, candidate exposure map and proposed layout/migration rules. Use B1 journeys and B2/RR1 ledgers as seeds. |
| 2 | Reader guides and technical references (B1/B2/B3) | Under a separate brief, author alongside the historic records. Independently review evidence qualifiers, conflicts, links, terminology, source versions and the scope retained before considering migration. |
| 3 | Evidence access, link and archival preparation (B2/B3/B4, B5 if applicable) | Establish an approved durable route for each indispensable artifact and its transitive dependencies. Reuse B4-F1 and assess only material deltas. Obtain separate authorization for any archive construction, path changes and evidence asset preparation. Resolve exact rights, privacy, credit and licence decisions and applicable method/scratch defects. |
| 4 | Exact candidate assessment (B6) | Freeze proposed tree, reachable history and refs, baseline, methods and selected assets. Independently audit that surface and verify candidate package/hash/member identities. Test reproduction and evidence access in a clean checkout without access to the existing `.local-work/`. Resolve missing indispensable routes or agree a scope change before accepting the candidate. |
| 5 | Maintainer release decision and authorized execution | Obtain explicit approval of exact contents, refs/history, release ID, visibility, timing and any upload. Once an approved hosted asset exists, validate downloads and URLs, and verify the changed index and surface within the approved sequence. Changed bytes or refs require affected re-review. |

### Carry forward the accepted work

- B0 supplies the policy, gate ownership, 21 RR1 dispositions and version update
  rules. Preserve `GPL-3.0-or-later`, narrow third-party grants and local-only
  comparators. A future build needs an independently reviewed per-finding update
  disposition if selected. [B0 policy and gates](../publication-readiness-b0/report.md).
- B1 delivered navigation and proposed claims. B2 corrected contextual notation,
  prose and native locator problems. Seed inventory and delta checks with those
  receipts, including the later RG1 notation lead. Never normalize archived logs,
  addresses or mask/bit identities as a bulk prose operation.
  [B1](../publication-readiness-b1/review.md) · [B2](../publication-readiness-b2/focused-rework.md).
- B3 supplies one pinned 1.16.244.0 native/definition baseline, authored method
  access contracts and disposition of historical mismatches. H? preserves
  unknown historical save origin. Verify relevant portable clean-checkout
  examples with lawful prerequisites, stated effects and accessible pins.
  Keep missing historical replay explicit. [B3](../publication-readiness-b3/report.md).
- B4/F1 supplies reviewed local preparation and practical privacy policy.
  Decide exact membership and unresolved author/contributor/excerpt choices and
  examine actual public paths/history. Keep donor evidence restricted.
  [B4](../publication-readiness-b4/report.md) · [F1](../publication-readiness-b4/f1/README.md).
- B5-A creator checks, legitimate auto-cleanup and retention records are reusable.
  Cosmetic scratch or Git temporary-object housekeeping is optional. Requalify
  only a selected method's actual creator, external dependency or safety issue.
  The historical B5-B named-manifest procedure governs any separately approved
  agent cleanup that uses it. The maintainer may discard the entire
  `.local-work/` directory after publication without a retention obligation.
  [B5-A](../publication-readiness-b5/report.md) · [B5-B](../publication-readiness-b5/b5-b-plan.md).

### Tree and reader architecture

Inventory tracked files at a frozen tree, with role, source/current authority,
target audience, proposed destination and disposition. Find Markdown links and
anchors, CSV/manifest paths, code examples and plain-text evidence paths.
Distinguish actual broken public links, unavailable targets, explicit private
provenance, superseded future instructions and administrative material. Record
inbound references and reader consequences for each proposed move or stub.
Identify candidate ref/history exposures at design level. Exact scope, destructive
remediation and full final history audit are later decisions.

Use the current roadmap as the reader entry point. For each subsystem propose an
entry guide covering the player-facing question, observed mechanism, runtime
conditions, saved representation, restoration/authority and qualified limits.
Link separate technical references for native/definition/script locations,
identifier domains, state contracts and evidence. Retain exact experiment and
review paths or historic lookup entries, including negative cases and former
interpretations. A guide should link a synthesis to the old result and explain
where it was superseded. Verify three reader journeys (understand, reproduce
within the advertised tier, challenge or recover history) and reconcile every
selected claim with its original evidence and review before moving records.

### Evidence tiers and private locators

| Tier | Tracked treatment and eventual verification |
| --- | --- |
| Available | Relative, case-correct link to the tracked report, method or evidence. An independent reproduction route identifies publicly available, lawful inputs and exact documented steps. Test the declared route from an isolated clean checkout. |
| Release asset candidate | Stable evidence ID, candidate archive/member, original-byte SHA-256, producer, scope and access state. Use `PENDING RELEASE` until an authorized asset exists. Then use an actual versioned download URL and verify the downloaded container and extracted members. |
| LOCAL-ONLY | Cite a historical locator as private provenance for nonessential support where useful. Describe access limits. The locator and any retained hash cannot close an indispensable dependency. |
| Stale/obsolete | Record the original target and its replacement or why no equivalent exists. Repair public routes only after separate approval. |

`.local-work/` is disposable working storage. Active investigations still
apply protected-save and experiment-integrity rules to their inputs and evidence.
The future inventory starts with selected claims and tracked references, including
plain text. Trace consequential dependency edges to original inputs. Inspect
particular indexed members only when a file-specific need warrants it within
the authorized read-only scope. The roughly 70 GB footprint does not define
the inventory denominator. Keep raw saves, game inputs,
decompressed payloads, memory, bulk native exports and proprietary files out of
the public Git tree. B4-F1 already covers 71 identities: 25 proposed CORE saves,
27 proposed ADDENDUM originals (14 saves, 13 screenshots), 15 LOCAL-ONLY, four
EXCLUDE and zero SPECIFIC HOLD. Save52 is HIST-0267. HIST-0255 is a separate
first-party save. Preserve file-specific rights and immutable original bytes.
Reuse the existing local provisional packages and indexes. Limit delta review to
an approved B1 claim change, genuinely needed evidence since 2026-10-21 or an
actual file-level defect. Compare the evidence benefit with documenting an
honestly narrower tier. A screenshot or save cannot supply a missing historical
runtime epoch. [F1 coverage](../publication-readiness-b4/f1/coverage.md) ·
[Assets](../publication-readiness-b4/f1/assets.csv) ·
[Members](../publication-readiness-b4/f1/members.csv).

For each dependency, record the claim ID, source reference, artifact identity
and version, provenance, upstream inputs and method/tool requirements. Record
whether it is indispensable, supporting but nonessential or disposable, and
whether it is independently reproducible. Reproducibility can apply to an
indispensable artifact. Record the proposed durable route, verification method,
rights/privacy decision state and any open dependency edge. A private historical
locator can explain provenance while readers use a separate durable route.

Every indispensable artifact must be in the tracked public tree, in an approved
GitHub Release asset, or independently reproducible using publicly available
inputs and documented methods. If a route is unavailable, flag the specific
claim as a publication blocker. The maintainer must resolve it explicitly,
including by narrowing or excluding the claim. B4-F1's 25 CORE and 27 ADDENDUM
selections stay provisional. Any subsequent evidence review is claim-led and
subject to the same rights, privacy, provenance, immutable-byte and exact
approval requirements.

### Historical brief and audit archives

Prefer compressed historical groups retained inside their brief/audit directory
structures, with a directory-local `README.md` and adjacent machine manifest.
The inventory assignment proposes exact groups, membership, names, codec and
which significant briefs should stay loose. For each group declare the baseline
tree and as-of date, paths in scope and exact inclusion/exclusion tests.

| Category | Accounting rule |
| --- | --- |
| `ARCHIVED_SOURCE_DOCUMENTS` | One row per eligible source in the proposed archive. |
| `REMAINING_LOOSE_SOURCE_DOCUMENTS` | One row per eligible source intentionally left loose, with reason. |
| `GUIDING_READMES_AND_INDEXES` | Enumerate separately. Prefer directory guidance outside the eligible source count. |
| `MANIFESTS_OR_OTHER_GENERATED_METADATA` | Enumerate separately, including generated indexes, receipts and archive containers where appropriate. |
| `EXCLUDED_NON_SOURCE_FILES` | Explicitly classify administrative material, zero-length placeholders and governing instructions. Decide whether each controlling brief qualifies as a source under the frozen rule. |

Require `TOTAL_ELIGIBLE_SOURCE_DOCUMENTS = ARCHIVED_SOURCE_DOCUMENTS + REMAINING_LOOSE_SOURCE_DOCUMENTS`.
Also reconcile the full inventory universe to the five disjoint categories.
For each archive record the original path, normalized member path, byte length
and SHA-256. Reject duplicate members, case-folded collisions, traversal,
absolute paths and links. Verify safe extraction in a disposable directory,
exact original-byte equality, no eligible omissions and no duplication between
archive and loose sets. Explain scope, historic paths, counts, exceptions and
how readers locate and search the members. State the README's counting treatment.

Inventory existing inbound Markdown links before a future move. Preserve
historical names and context with a real index/member lookup or justified stub,
and test all current-facing links from a fresh checkout. A ZIP is not browsable
or searchable like loose Markdown on GitHub. Do not invent clickable member
links. Removing a path at a future HEAD leaves its older blob reachable through
history unless the approved history/ref boundary excludes it. Any rewrite or
deletion needs its own authorization.

### Final public-surface checks

Review the actual candidate tree, history reachable from all refs proposed for
disclosure and associated tags/releases/assets. Audit credential/personal data,
licensing and excerpts, historical/private payloads, misleading old authorities,
oversize artifacts, and upload-enabled automation. Verify candidate member and
download SHA-256, portability, link/anchor/case behavior, source closure and
documented reproduction procedures and supplementary-asset dependencies within
the claims' stated scope. Run this future gate in a clean checkout with no access
to the existing `.local-work/` or fallbacks to it. Exercise candidate assets
through the approved release verification sequence and check actual versioned
downloads when available. Distinguish reproducible calculations and methods
from historical runtime observations that cannot be replayed. Verify the
approved durable route for indispensable historical evidence and disclose limits
on replay and nonessential private evidence. Keep actual final
ref choice, remediation, hosting and visibility decisions with the maintainer.
This amendment authorizes the gate design only.
