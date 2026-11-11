# P1 offline power research contract

2026-10-17, Australia/Sydney. SOR-EXP-0041 / SOR-EV-0049.
[Original authorized brief](../../implementation-briefs/README.md#archive-lookup) (`implementation-briefs.zip :: docs/implementation-briefs/CODEX_BRIEF_SOR_P1_power_generation_distribution_native_mapping.md`).
The brief's mandatory questions and deliverables are frozen; this document
organizes their verification and does not reduce them.

| Mandatory criterion | Required evidence |
|---|---|
| Source review | E1–E3, prior saved links, maintainer network source and supplied version-4 exporter; actual paths/revisions and limitations |
| Generation | Constructible variants, ratings, planet selection, modifiers, fuel recipe/interval/amount and temporal checks/callers |
| Distribution | Registration, supply/demand, powered state, recalculation and deficit rule |
| Wiring | Authoritative endpoint admission, limits, graph mutations/traversal, switches, cycles, mixed wired/unwired deficit |
| Persistence | Qualified serializers/readers, more than Save52, exact identities/offsets, current-state versus historical data |
| Reference package | Report, catalogue, native register/dataflow, contract matrix, uncertainties/falsifiers, indexes/source credits |
| Verification and review | Executed checks, protected-input preservation, prose/links, task-only/complete textual patches with untracked text and exclusions, independent review and rework |

Allowed inputs are existing pinned game definitions/executable/static-analysis
state, protected original saves and prior local research. Allowed actions are
read-only offline inspection/export, original bounded research utilities,
documentation and local review packaging. Ghidra exports must use readOnly and
noanalysis; database bytes, symbols, types and comments must remain unchanged.
No native invocation, game launch, attachment, observer, deployment, save/game
changes, installation/download, Git mutation or external disclosure is authorized.

Outputs are authored research under this directory and `research/p1-power/`,
index/register additions and ignored local receipts/diffs. Raw definitions,
decompilations, saves and decoded bytes remain LOCAL-ONLY. Authored interpretation
is REVIEW-REQUIRED; independent scientific review does not authorize integration
or publication. Confidence, coverage and completeness are separate.

Risks are misidentified layouts/domains, stale caches, unqualified negative
claims, accidental input mutation and disclosure in diffs. Hash inputs and
analysis databases before/after, qualify byte framing, inspect numerical examples,
keep raw artifacts ignored and verify patch inventory/content. Stop the affected
operation for identity mismatch, unsupported framing, unexpected mutation or
insufficient space; diagnose within authority rather than inventing a negative
result. Remove only task-created disposable decoded scratch after preserving
receipts; retain failures and original inputs.

COMPLETE requires adequate answers to essential offline mapping objectives;
INCOMPLETE retains an important answer still addressable by authorized tracing;
BLOCKED requires an actual access/evidence barrier. Excluded live measurement
alone does not cause incompleteness. Review uses the original brief and primary
evidence and returns ACCEPT, REWORK or ESCALATE. No self-acceptance.
