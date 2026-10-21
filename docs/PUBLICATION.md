# Publication Plan and Release Gate

**Status: NOT READY / NOT CLEARED.** Independently reviewed bounded research exists; see the [current roadmap](research-roadmap.md). No public-release action is authorized. The [proposed claim/build scope](audits/publication-readiness-b1/claim-build-matrix.md) still requires maintainer agreement and all release gates below.

The project begins privately and must publish completed, reviewed research under `GPL-3.0-or-later`. The first publication scope/build matrix must be explicitly agreed and contain runtime and persistence objectives. The continuing programme may remain broader, but unresolved required topics cannot be silently dropped to declare completion.

## Scientific review

- [ ] Agreed scope/build matrix is recorded, with required questions, exclusions, and acceptance criteria.
- [ ] Required runtime mechanisms, lifecycle behaviour, saved representations, and their relationships are documented and validated, or a scope revision is explicitly agreed.
- [ ] Persisted/default/derived/transient state and external game-data dependencies are distinguished.
- [ ] Findings link decisive evidence; outside reports, original observations, interpretations, and counterexamples remain distinguishable.
- [ ] Validation extends beyond discovery examples; actual coverage and untested versions/conditions are clear.
- [ ] Proposed mod integrations are not presented as tested/safe without their own evidence.
- [ ] Reproduction instructions work from a clean checkout with authorized prerequisites; unavailable private evidence and consequent limits are disclosed.
- [ ] Research helpers have source, usage, tests appropriate to their role, and explicit side effects; no unreviewed production promises are implied.

## Rights, attribution, and privacy review

- [ ] All included outside material has exact provenance, rights-holder permission, scoped user approval, required notices, and credit.
- [ ] Publication permission is distinguished from private-use approval; no unresolved compatibility conflict remains.
- [ ] Project licence scope is consistent across documentation and future source/package metadata; GPLv3 text is complete and unmodified; the `or later` choice is explicit.
- [ ] Desired public copyright/author-credit wording and actual contributor rights have been confirmed, without invented ownership or names.
- [ ] Game-derived evidence is reviewed separately; no blanket project ownership/relicensing is claimed.
- [ ] Proprietary binaries/assets, decompressed saves, memory dumps, imported analysis databases, private correspondence, credentials, and unreviewed bulk traces are excluded. Raw saves remain outside Git; only individually selected unchanged first-party originals may be proposed as supplementary Release assets under the conditions below. Third-party donor originals remain excluded without affirmative scoped redistribution permission and user approval.
- [ ] Samples, paths, filenames, screenshots, logs, and metadata are inspected for personal data; redactions and reproducibility impacts are recorded.
- [ ] Credits cover useful research and tools as well as code, without implying endorsement.
- [ ] Internal approval rules do not add conditions to downstream GPL rights.

## Conditional first-party original-save evidence

**B4-F1 settled policy, 2026-10-21:** the
[invoked addendum brief](implementation-briefs/CODEX_BRIEF_SOR_B4_F1_evidence_selection_addendum_packaging.md)
accepts first-party saves/screenshots as eligible research evidence, informed by
community practice. This is a maintainer policy decision, not an express
Bethesda/ZeniMax licence or a claim that legal risk is eliminated. Generic absence
of individual written permission alone does not hold first-party evidence.
File-specific provenance, practical privacy, scientific utility and immutable-byte
checks still apply; actual sensitive material or distinct restrictions hold the
affected file. Character names and historical `C:\Users\User` provenance are
acceptable; public reproduction instructions must remain portable. HIST-0255 is
accepted as first-party from the authorized local Saves inventory and is distinct
from Save52/HIST-0267. Bounded local provisional assembly is authorized by F1;
exact CORE/ADDENDUM membership and distribution remain pending maintainer/B6
approval. See the [provisional evidence index](audits/publication-readiness-b4/f1/README.md).
This prospectively qualifies the B4 eligibility/assembly wording below; no donor,
game-install, raw-save-in-Git, licence-grant or publication restriction is relaxed.

B4 policy-text integration, 2026-10-21, under the explicitly invoked
[brief](implementation-briefs/CODEX_BRIEF_SOR_B4_evidence_selection_rights_privacy_archives.md).
This resolves the former blanket raw-save exclusion only for individually
reviewed first-party supplementary assets; publication remains **NOT CLEARED**.

Selected first-party control or unusually useful mature saves may be proposed
after file-specific producer/provenance, exact size/SHA-256, necessity,
practical privacy and underlying-content rights assessment, and explicit
maintainer selection approval. Character names alone are acceptable. Examine
concrete account/platform/user/path data and unrelated state without assuming
that first-party capture licenses underlying game content. Technical/privacy
pass, rights assessment, selection approval and actual publication authorization
are separate decisions. Unknown material rights or disclosure decisions hold
the affected file; select the exact original or exclude it.

**Save bytes must never be sanitized, redacted, rewritten, patched, resaved or
otherwise transformed for publication.** Preserve original names and full
SHA-256. Lossless enclosing archive compression is permitted after specific
provisional-packaging review/approval; verify extracted saves byte-for-byte
against protected originals. Archives remain local until separate authorization.
Prefer GitHub Release assets with a durable repository evidence index; raw saves
remain untracked. Screenshots likewise require actual pixel/metadata and rights
review; they do not establish a same-time save join automatically.

No donor original or substantial donor payload may be distributed under existing
local-inspection permissions. EXE/ESM/BA2, extracted assets, game-install
INIs/libraries, decompiled native source, bulk disassembly, analysis databases,
installed tools and built observers remain excluded. Bounded authored analysis,
pseudocode and illustrative native excerpts require content-specific review;
a suffix or small size is not clearance. No history rewrite or public disclosure
is authorized by this policy text. See the [B4 dispositions](audits/publication-readiness-b4/report.md).

## Repository and release-content review

- [ ] Inspect the proposed tree **and all Git history/refs that would become public** for secrets, private/proprietary data, unapproved code, large artifacts, and obsolete disclosures.
- [ ] Inspect proposed tags/releases/assets and any other publication surfaces, not only tracked HEAD.
- [ ] Any history rewrite, purge, branch deletion, or replacement release strategy has separate owner approval; no silent remediation.
- [ ] Internal links, UTF-8, line endings, evidence hashes, and clean-checkout instructions are checked.
- [ ] Historical briefs/findings are labelled and point to current authority; removed artifacts are not falsely described as downloadable.
- [ ] Source and permission evidence remains verifiable without publishing unapproved private correspondence.
- [ ] No automated workflow uploads private inputs or unreviewed artifacts.
- [ ] User explicitly approves the exact release contents, refs/history boundary, visibility change, and timing.

## Handoff

Record the review, remaining blockers, approved contents/ref, and user decision in [audits/](audits/README.md) and [DECISIONS.md](DECISIONS.md). A `CLEARED-FOR-PUBLICATION` item label is not permission to publish the whole repository. A private first push is not the public release.

Only after the completed research is published should the project choose among tracker import, a supported generic dump tool, or downstream mods. No release tag, GitHub Release, package publication, fork, PR, or visibility change is created by these instructions.
