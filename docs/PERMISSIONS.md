# Permission and Reuse Register

**One scoped third-party header reuse is approved (SOR-P-0001 below).** No broader SDK/library/runtime reuse follows from it.

## SOR-P-0002 — Standing maintainer-owned material grant

APPROVED-FOR-STATED-SCOPE, 2026-10-07. The maintainer explicitly grants the [standing exception](../THIRD_PARTY_POLICY.md#maintainer-owned-material) for maintainer-authored material in any `gooberpede` GitHub/local repository. This supplies authorial permission and user authorization for inspection/copy/adaptation/port/reuse here without another permission discussion. Mandatory per-use provenance, optional self-credit, third-party exclusions and separate execution/publication gates are defined once in that policy. It supersedes earlier sibling-copy restrictions only for covered maintainer-authored material; historical records retain their original scope. SFSE SOR-P-0001 remains unchanged. Current use: SOR-S-0122 and [correction provenance](../debugger/exp0002a/maintainer/PROVENANCE.md). Whole-project publication remains REVIEW-REQUIRED.

Scaffold-specific use of the supplied organizational reference and verbatim GPL legal text is recorded transparently in [SOURCES.md](SOURCES.md). Neither is a blanket permission to copy implementations, research datasets, or game scripts.

| ID | Source / exact material and version | Proposed use | Rights-holder permission | User decision | Conditions / notices | Affected files / credit | Publication eligibility |
|---|---|---|---|---|---|---|---|
| SOR-P-0001 | Ian Patterson / SFSE `sfse/PluginAPI.h`, commit `48535cc4306ab345252bf740c20a1c6194929b0e` | Use the unmodified public plugin interface header to compile the original EXP0002 observer; retain it with the exact licence scope/notice | Upstream LICENSE explicitly grants MIT for this header only, copyright 2023 Ian Patterson | 2026-10-06 user answered: “Yes—accept MIT for this header” to the exact pinned use and notice requirements | Preserve copyright/permission/disclaimer; SFSE runtime and other source excluded; no sibling observer copying | `runtime/exp0002/third_party/sfse/`; SOR-S-0114; CREDITS/THIRD_PARTY_NOTICES | Header rights basis documented; complete package remains REVIEW-REQUIRED, not publication-authorized |

The header and licence were fetched through the read-only GitHub connector at the exact commit after approval. Text content is unmodified; repository LF normalization is recorded rather than claiming upstream byte identity. SOR-P-0001 is APPROVED-FOR-STATED-SCOPE. User's preceding clarification permits external Address Library mod use with code boundaries respected and CommonLibSF reference consultation with attribution; it does not approve arbitrary library source incorporation. No Address Library installation/deployment is authorized by Gate A.

Create records with `SOR-P-` IDs using [templates/permission.md](templates/permission.md).

## States and gates

### Initial reconnaissance boundary — 2026-10-06

SOR-D-0009 records authority to run separate installed static tools and inspect local development inputs, plus install/run original bounded xEdit readers. This is execution/inspection authorization, not acceptance of any third-party code licence for incorporation. No new `SOR-P-` code-reuse entry is appropriate: none was requested or performed. xEdit/Ghidra licences do not clear Bethesda-derived outputs. Raw sources and exports remain LOCAL-ONLY; mod/source rights remain as recorded in SOR-S-0101–0112. Further tool/dependency incorporation or disclosure requires a scoped review.

Use `PROPOSED`, `PENDING-PERMISSION`, `PENDING-USER-APPROVAL`, `APPROVED-FOR-STATED-SCOPE`, `DECLINED`, or `SUPERSEDED`. The two authorization dimensions must remain visible even when a short state is shown.

Record the rights holder and how identified, actual permission evidence, whether the user accepts a licence grant or requires separate permission, the user's explicit decision/date, the precise actions/versions/files allowed, and conditions covering modification and redistribution where relevant. Private evaluation permission is not public-release permission.

Store correspondence locally using neutral private evidence IDs. Do not publish private email addresses, signatures, or communications without separate disclosure approval. Cite enough non-sensitive metadata to find the evidence during review.

Fork and PR approvals are separate action decisions in [DECISIONS.md](DECISIONS.md), linked here where related. A permission for one action is not automatically permission for any other. Ambiguity blocks the affected reuse/action; see [THIRD_PARTY_POLICY.md](../THIRD_PARTY_POLICY.md).

## SOR-P-0003 — Local examination of TheDailyXPerience package

2026-10-09, APPROVED-FOR-STATED-SCOPE for the invoked brief's bounded local examination and independently authored research; publication basis PENDING-PERMISSION-REVIEW. Rights holder/uploader identified as TheDailyXPerience by [listing 1798](https://www.nexusmods.com/starfield/mods/1798), SOR-S-0125. Exact archive identity and permitted/prohibited actions: [SOR-EXP-0008](experiments/launch-era-third-party-save-corpus.md). User explicitly requested execution of the retained brief; no new code/assets reuse is authorized.

The listing panel prohibits other-site upload and conversion to other games, requires author permission for improvement modifications and asset use, and restricts sale/Donation Points uses. Description prose offers broad resource/testing use. Preserve that ambiguity; do not silently construe it as a distribution grant. Local `permission-reference.json` identifies sections, URLs, retrieval date and cache limitations. An exact independently preserved live-current permission snapshot was not acquired. This remains a publication-review condition, not a claim that author contact/consent occurred. No upstream contact is authorized.

Original archive/saves and substantial original extracted payload must never be re-uploaded or included in this project's publication under this authorization. Only independent scripts, minimal non-sensitive numeric manifests and authored research are candidates for review; they are not yet publication-cleared. Bethesda/game-content rights remain separate. SOR-P-0001/0002 and GPL text unchanged.
