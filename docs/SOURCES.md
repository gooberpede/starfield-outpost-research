# Source Register

Record meaningful sources when they influence the work. A source entry is not a reuse permission, a compatibility finding, or proof of the source's claims. See [THIRD_PARTY_POLICY.md](../THIRD_PARTY_POLICY.md) and [PERMISSIONS.md](PERMISSIONS.md).

## Sources used for scaffold preparation

### SOR-S-0001 — User-supplied reference scaffold

- Source: `starfield-reference-handles-scaffold(1).zip`, attached to the setup request; no public URL supplied.
- Supplier: project maintainer. Original per-file authorship/rights not independently established from an upstream repository.
- Version: attached artifact identified by SHA-256 in [PROVENANCE.md](PROVENANCE.md); inspected 2026-10-01.
- Used contribution: structural pattern and research-document responsibilities, at the user's explicit request.
- Scope: adapted organizational guidance; no scripts, engine findings, existing environment baseline, or complete old archive redistributed.
- Permission/user decision: use as the structural reference explicitly requested; not a blanket grant for third-party content it might identify. Decision `SOR-D-0006`.
- Credit: [CREDITS.md](../CREDITS.md). No claim of independent validation of the reference-handle research.

### SOR-S-0002 — GNU GPLv3 text and SPDX version-choice reference

- Author of licence text: Free Software Foundation, Inc.; licence dated 29 June 2007.
- Public reference: <https://spdx.org/licenses/GPL-3.0-or-later.html>; inspected 2026-10-01.
- Canonical text location: <https://www.gnu.org/licenses/gpl-3.0.txt>; direct retrieval unsuccessful during this preparation.
- Included bytes: verbatim installed GPLv3 licence document, source/hash in [PROVENANCE.md](PROVENANCE.md).
- Contribution: required [LICENSE](../LICENSE), [licence grant/boundary](../LICENSING.md), and distinction between internal conduct rules and GPL recipient rights.
- Permission: the licence document expressly permits verbatim copying/distribution; its notice is retained. This legal-text inclusion implements the user's chosen GPL licence, not approval to reuse any software implementation.
- Credit: [CREDITS.md](../CREDITS.md) and [THIRD_PARTY_NOTICES.md](../THIRD_PARTY_NOTICES.md).

### SOR-S-0003 — Git attributes and ignore documentation

- Author/project: Git documentation contributors.
- Sources: <https://git-scm.com/docs/gitattributes> and <https://git-scm.com/docs/gitignore>; inspected 2026-10-01, online documentation rather than a pinned source checkout.
- Contribution: consulted behaviour of line-ending attributes and ignore rules for this scaffold's newly authored configuration and evidence handling.
- Scope: reference use, not copied Git implementation code; no dependency/binary bundled.
- Affected files: `.gitattributes`, `.gitignore`, `WORKFLOW.md`, and evidence instructions. Credit: [CREDITS.md](../CREDITS.md).

### SOR-S-0004 — GitHub local-repository and remote instructions

- Author/project: GitHub documentation contributors.
- Sources: <https://docs.github.com/en/migrations/importing-source-code/using-the-command-line-to-import-source-code/adding-locally-hosted-code-to-github> and <https://docs.github.com/en/get-started/git-basics/managing-remote-repositories>; inspected 2026-10-01.
- Contribution: reference for the owner-operated initial push and remote setup in [GIT_SETUP.md](GIT_SETUP.md).
- Scope: standard command usage tailored to the user's paths, not copied GitHub implementation; no dependency bundled. Credit: [CREDITS.md](../CREDITS.md).

## Candidate outpost-research leads — not validated or approved

These names came from the earlier discussion, not a completed prior-work audit in this project. They are listed to preserve leads, not to assert functionality, licence coverage, or release compatibility.

| Source ID | Candidate | Purpose of possible review | Current status |
|---|---|---|---|
| SOR-S-0101 | `Nexus-Mods/StarfieldSaveTool` — <https://github.com/Nexus-Mods/StarfieldSaveTool> | Check exact container/metadata capability, supported versions, documentation and reuse terms | NOT RECHECKED; no implementation adopted |
| SOR-S-0102 | `rux616/modding-sf1-scripts-vanilla` — <https://github.com/rux616/modding-sf1-scripts-vanilla> | Locate possible script declarations/behaviour leads; verify origin and rights separately | NOT RECHECKED; no scripts copied; a mirror is not rights-holder permission |

No third-party outpost claim has been promoted to a finding and no code reuse approval exists. Prior conversation citations and summaries must be checked before use. Add other sources only when actually consulted or deliberately registered as a lead; do not populate a ceremonial list of tools never used.

## New records

Use [templates/source.md](templates/source.md). Record author/owner, exact title/location and commit/version, access date, contribution, inspection status, original rights-holder/licence evidence, affected findings/files, permission decisions, credits, and public/private evidence locations. Preserve original attribution when later independently reproducing a result.
