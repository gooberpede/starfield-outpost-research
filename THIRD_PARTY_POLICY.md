# Third-Party Research, Code, and Contribution Policy

## Principle

Respect other people's work in both letter and spirit. Public availability, a convenient implementation, attribution, or technical compatibility is not automatic project approval. Credit is required by project policy whenever substantive third-party work is used, whether or not the source's terms require it.

This policy governs this project's maintainers and agents. It is not an additional restriction on recipients of GPL-covered material. Downstream rights are governed by [LICENSE](LICENSE), not a requirement to ask this project before exercising those rights. See [LICENSING.md](LICENSING.md).

## Four distinct activities

| Activity | Requirement |
|---|---|
| Consult a source | Read-only inspection; record meaningful sources and exact versions. This does not authorize copying, execution, or publication. |
| Use research | Cite the specific finding, method, explanation, or design at the point of use and in credits. Independently validate claims before promoting them to project findings. |
| Use a separate tool | Discuss/authorize execution as appropriate; record tool version, purpose, terms, inputs, outputs, and output-rights issues. Running a tool does not clear its implementation or outputs for redistribution. |
| Incorporate material | Complete the relevant permission, licence, credit, and user-approval review before copying/adapting code, text, diagrams, data, fixtures, or other material into deliverables. |

Do not assume a repository's root licence covers all its files. Check file-specific notices and included third-party material. A mirror of game scripts does not establish that its maintainer can authorize redistribution of the underlying scripts.

## Code reuse requires two separate gates

1. **Documented rights-holder permission** for the actual proposed use, including modification and distribution when relevant.
2. **Explicit user authorization** of that specific use after discussing the source, material/version, permission basis, obligations, publication implications, and alternatives.

A licence may grant legal permission. An agent must present the exact terms rather than unilaterally deem them sufficient for this project's permission requirement. Record whether the user accepts that licence grant as the permission basis or requires separate rights-holder permission. If separate permission is required, obtain it before reuse. Silence is not consent. Contacting an author itself needs approval.

User approval cannot supply rights the user does not hold; author permission does not supply user approval. Permission limited to private use does not authorize a public release. Approval is not open-ended permission for other files, versions, purposes, or recipients.

This includes snippets, copied tests/comments, templates, ports, translations, generated bindings, build scripts, vendoring, dependencies, and AI-assisted adaptations. Renaming symbols, switching languages, rephrasing code, or having an AI rewrite it does not erase provenance. Describe source-informed work honestly; do not claim clean-room development without a documented process that supports that claim.

Do not evade review through submodules, package installation, build-time downloads, copied release assets, or a wholesale local mirror. No third-party implementation or dependency is included or approved by this scaffold.

## Forks, pull requests, and communication

Before creating a fork, discuss the repository, purpose, visibility, rights/disclosure implications, and maintenance commitment; record explicit approval. Do not replace a fork with a copied new repository to avoid discussion.

A pull request needs its own prior discussion and explicit approval, including draft PRs and PRs in this project's repository. Fork approval, investigation approval, or permission to reuse code does not authorize one. These gates apply equally to the web UI, APIs, command-line tools, and automation.

No unsolicited upstream issue, comment, permission request, publication of findings, or evidence upload on the user's behalf. Permission correspondence and personal contact details stay local unless disclosure is separately approved. Read-only source lookup is not an external contribution. Local inspection copies, when approved, remain outside tracked deliverables with origin intact.

## Credit and scientific provenance

Name the person/project and identify the actual contribution, precise source/version, and where it was used. Preserve required notices; add explanatory credit even when not required. Do not imply endorsement, collaboration, co-authorship, or approval that did not occur.

Distinguish **reported by another source**, **independently reproduced here**, and **newly established here**. Replication does not erase an earlier contribution. Credit and permission are separate obligations.

Use [SOURCES.md](docs/SOURCES.md) for discovery/use records, [PERMISSIONS.md](docs/PERMISSIONS.md) for scoped decisions, [CREDITS.md](CREDITS.md) for readable acknowledgment, and [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md) for rights boundaries and required notices. Cite sources beside affected findings, not only in a central list.

## Ambiguity, conflicts, and remediation

If ownership, permission, compatibility, or scope is uncertain, stop the affected reuse or external action and report the precise issue. Do not invent consent, remove notices, or quietly choose another unreviewed source. A GPL conflict requires discussion before integration, not silent relicensing of the project.

If unapproved material is discovered, identify its origin and locations, prevent further integration/disclosure, and report it. Do not silently destroy provenance or rewrite history. Agree the remediation, including any already published copies, before taking action.

## Policy examples

| Situation | Required outcome |
|---|---|
| Public repository with no licence | Consultation is not reuse permission; copying stays blocked. |
| Permissively licensed snippet, no user decision | Present the grant and proposed use; do not incorporate yet. |
| AI-generated port of upstream code | Treat as source-derived work and apply both gates. |
| Private-use-only author permission | Do not redistribute; record the publication blocker. |
| Approved fork, proposed draft PR | Obtain separate PR approval first. |
| Independently reproduced published finding | Preserve attribution and distinguish the new validation. |
| Incompatible or ambiguous terms | Stop the affected integration; discuss alternatives. |
| Cleared HEAD, private material in reachable history | Publication remains blocked pending reviewed remediation. |
| Software generates decompiled game code | Tool licence does not establish rights to publish the game-derived output. |
