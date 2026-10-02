# Publication Plan and Release Gate

**Status: NOT READY.** No research has been completed in this project and no public-release action is authorized.

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
- [ ] Proprietary binaries/assets, raw saves, decompressed saves, memory dumps, imported analysis databases, private correspondence, credentials, and unreviewed bulk traces are excluded.
- [ ] Samples, paths, filenames, screenshots, logs, and metadata are inspected for personal data; redactions and reproducibility impacts are recorded.
- [ ] Credits cover useful research and tools as well as code, without implying endorsement.
- [ ] Internal approval rules do not add conditions to downstream GPL rights.

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
