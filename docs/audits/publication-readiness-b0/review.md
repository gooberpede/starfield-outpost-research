# B0 frozen contract, verification and independent review

2026-10-21, Australia/Sydney. **Policy proposal; publication NOT CLEARED.**
The [invoked brief](../../implementation-briefs/CODEX_BRIEF_SOR_B0_publication_policy_release_scope.md)
governs this documentation assignment. The original mandatory text is copied
verbatim below; no acceptance criterion has been weakened or replaced.

## Frozen original criteria

| Criterion | Mandatory evidence for PASS |
|---|---|
| **AC1 — Inputs and preservation** | RR1 and governing policies explicitly identified; status/identity protection recorded; no protected input, HEAD or index mutation. |
| **AC2 — Accurate decisions and release character** | B0 decision record reflects every maintainer-settled choice including single coordinated research-archive release, version-bound baseline identity, legal/evidence limits and clear not-cleared status; open choices remain open. |
| **AC3 — Material inclusion and licensing boundaries** | Coherent inclusion/exclusion treatment of project source, game/tool files, decompiled material, bounded excerpts, first-/third-party saves, screenshots and GPL scope, cross-referenced to existing policies. |
| **AC4 — Reproducible method and evidence policy** | Source-first, historical hash fidelity, locally reproducible extraction without bulk game dumps by default; GitHub-hosted supplementary archive/index/hash model; explicit research-release/game-build distinction and proportionate new-build requalification policy with stable locator identities and version-scoped offsets; no premature evidence clearance. |
| **AC5 — Local-work retention** | Four-way material classification and manifest-first, separately approved deletion procedure with protections; external scratch creators/dependencies included without executing cleanup. |
| **AC6 — Release gates and RR1 reconciliation** | Verifiable B1–B6 gates (including a primary game-build baseline manifest and policy for later build updates) plus exact coverage of RR1-001–RR1-021, consistent severity/proposed owner/verification and explicit publication holds. |
| **AC7 — Documentation and scope quality** | Concise durable navigable B0 docs including `versioned-baselines.md`, resolvable published-document links, no new malformed prose or ambiguous native address/offset notation; historical/scientific reports not rewritten. |
| **AC8 — Independent verification and delivery** | Independent reviewer ACCEPT against original criteria; PASS/FAIL/NOT TESTED matrix and primary evidence receipts; full/task-only diffs exactly reconstructible forward/reverse; tracked/untracked status and exclusion manifest; permissions and remaining decisions stated. |

## Submission assessment and evidence

| Criterion | Implementer assessment | Primary evidence and limits |
|---|---|---|
| AC1 | PASS | Local baseline.json pins every starting Git-visible file, supplied brief, HEAD and index; package rechecks preservation with only two approved index edits exempted from byte equality. All other originals untouched. No installed-game/save/database rehash claimed. |
| AC2 | PASS | report.md distinguishes brief-settled decisions, recommendations, tensions and deferred choices; exact scientific release corpus and action approval remain open. |
| AC3 | PASS | scope-and-evidence-policy.md tests each material class and GPL/SFSE/game/third-party boundary; existing policies unchanged. |
| AC4 | PASS | Source-first method tiers and historical hash fidelity; prospective GitHub member/index contract and versioned-baselines.md schema, statuses and illustrative placeholder row only. |
| AC5 | PASS | local-work-retention.md four classes, named RR1 families, two-stage separately approved deletion, protections and post-action checks; no cleanup executed. |
| AC6 | PASS | release-gates.md observable B1–B6 evidence and required versus optional/exception distinctions; rr1-dispositions.md exact 21-row ID/severity/primary-owner reconciliation. |
| AC7 | PASS | Seven new B0 documents, two minimal index entries, local strict encoding/link/table/prose checks; historical scientific reports unchanged. |
| AC8 | NOT TESTED until independent return | Local package manifests verify complete/task-only patch inventories and byte-exact forward/reverse reconstruction; actual reviewer return must ACCEPT the exact snapshot before accepted completion. |

## Change inventory and input record

New B0 files: [report.md](report.md),
[scope-and-evidence-policy.md](scope-and-evidence-policy.md),
[local-work-retention.md](local-work-retention.md),
[release-gates.md](release-gates.md), [rr1-dispositions.md](rr1-dispositions.md),
[versioned-baselines.md](versioned-baselines.md) and this review.md.
Only existing-file changes are a B0 entry in [audit index](../README.md) and
[brief index](../../implementation-briefs/README.md). The supplied untracked brief
is preserved, included only in the complete patch, and is not task-authored text.

Required guidance read: README, WORKFLOW, THIRD_PARTY_POLICY, charter, research
state, evidence standard, invoked brief, execution/reviewer protocol, PUBLICATION,
PERMISSIONS, PROVENANCE, LICENSING and notices. RR1 report/findings, source,
evidence, temporary-material, navigation, prose, licensing/history/comparator and
review ledgers supply existing observations. Current function register and selected
native-availability/build-budget/LO1 registers/source pins inform the prospective
schema. References are existence-checked by bounded document checks; no repeat
whole-repository crawl or new-build investigation is claimed.

## Actual checks and limits

Local scripts under `.local-work/b0/` use installed CPython standard library and
Git only. They read Git-visible documents, existing named ledgers, HEAD/index and
baseline; write ignored JSON/patch/status receipts and isolated plain application
trees under `.local-work/review-patches/`. No target/analysis-project effects,
source extraction, dependency downloads or network operations. Both drives must
pass the existing 40,000,000,000-byte guard before packaging; Git discovery in
scratch stops at `.local-work/`. Scratch is retained, not silently cleaned.

Verification checks exact RR1 identifiers/severities, frozen criterion equality,
UTF-8 without BOM/LF for new authored text, whitespace, obvious mojibake and fused
prose patterns, Markdown table widths and local relative targets/heading anchors.
Manual contextual review complements these bounded parsers; they are not full GFM
rendering or proof of universal prose correctness. Existing index newline style
is preserved. Patch checks compare path inventories and exact contents against
tracked/untracked text; merely passing reverse application is insufficient.

Preserved execution limitations: initial combined reads exceeded console limits;
targeted reads recovered governing sections. A duplicate baseline invocation
refused to overwrite its already-created receipt; the original baseline remains
authoritative. Neither event changes evidence or supplies a scientific negative.

## Independent review and final delivery identity

The read-only fresh-context reviewer uses the original brief and protocol, checks
actual changes, baseline/pins, criteria, mappings, links, package manifests and
patches, and returns ACCEPT, REWORK or ESCALATE. It must not edit or accept its own
corrections. Any correction or reviewed-byte change requires renewed review.
The verbatim actual return is retained as `.local-work/b0/independent-review.md`;
the final reviewed revision is identified by the local package file hashes, avoiding
self-referential document hashes. Until that return exists, status is NOT REVIEWED;
this paragraph does not preassign a verdict. The external return controls AC8's
final PASS or failure without rewriting the frozen contract or accepted snapshot.

Package locations: `.local-work/b0/package-final.json`, `status-final.txt`,
checks/changed-file/exclusion manifests within the package, and
`.local-work/diffs/b0-final-complete.diff` plus `b0-final-task-only.diff`.
Complete covers all uncommitted tracked/untracked text since HEAD, including the
unchanged supplied brief. Task-only covers the seven new documents and two index
entries. Protected/ignored raw material, screenshots, saves, native exports,
databases, tools, game inputs, local diagnostics and scratch are disclosed
exclusions. No excluded payload is claimed cleared or silently bundled.

Separate outcomes: policy content proposed; implementation integrity limited to
documents/packaging; existing scientific evidence/confidence unchanged; target
survival NOT APPLICABLE; live behavior, source-method replay, new-build semantics,
privacy/rights clearance, asset publication and all B1–B6 execution NOT TESTED.
Authority is B0 documentation/review only. No stage/commit/push, tag, upload,
visibility/history mutation, game/tool execution, archive creation, save alteration
or cleanup. Maintainer critical integration review still required after ACCEPT.

Open choices and policy conflicts are enumerated in report.md. Completion of B0
does not approve individual evidence, historical paths, source revisions, baseline
manifest, tag, archive format or schedule. Stop after this handoff.
