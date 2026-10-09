# Research methodology refinement — review package

2026-10-09 (Australia/Sydney). SOR-D-0027; documentation-only implementation complete for critical review, integration pending. Governing [brief](../implementation-briefs/CODEX_BRIEF_SOR_research_methodology_evidence_standards.md). No scientific evidence-state change or new research execution. Authored additions REVIEW-REQUIRED.

## Reviewed authority and reconciliation

| Files reviewed | Authoritative role / outcome |
|---|---|
| [AGENTS.md](../../AGENTS.md) | Standing safety, rights, evidence and handoff orders; concise methodology reference added, gates preserved. |
| [WORKFLOW.md](../../WORKFLOW.md) | Scope → brief → execution → critical review → user-approved integration; authorized offline choices remain within experiment scope. |
| [THIRD_PARTY_POLICY.md](../../THIRD_PARTY_POLICY.md) | Rights/permission/credit gates, including SOR-P-0002 maintainer-owned exception and embedded third-party exclusion; unchanged. |
| [README.md](../../README.md), [CHARTER.md](../CHARTER.md) | Research purpose, runtime/persistence parity and publication scope; unchanged. |
| [EVIDENCE_STANDARD.md](../EVIDENCE_STANDARD.md) | Normative confidence, basis, publication, evidence and identifier rules; primary home for the refinement. |
| [RESEARCH_STATE.md](../RESEARCH_STATE.md), [DECISIONS.md](../DECISIONS.md) | Current versus historical status, authorized boundaries and durable decisions; prospective methodology entry added. |
| [Known facts](../known-facts.md), [hypotheses](../hypotheses.md), [state register](../state-register.md), [function register](../function-register.md) | Existing scoped observations, provisional models, semantic proposals, persistence and integration limits; unchanged. |
| [PROVENANCE.md](../PROVENANCE.md), [SOURCES.md](../SOURCES.md), [subsystem index](../subsystems/README.md) | Recorded sample/build/source attribution and programme questions; relevant entries consulted, no new sources or permission basis introduced. |
| [Finding template](../templates/finding.md), [experiment template](../templates/experiment.md) | Prospective authoring guidance; coverage/completeness and answer-first references added. |
| [Implementation brief index](../implementation-briefs/README.md) and supplied brief | Durable task authority/discovery; index linked, supplied brief unchanged. |
| SOR-EXP-0003 coordinate correction, SOR-EXP-0004, SOR-EXP-0006, SOR-EXP-0009 and relevant SOR-EXP-0010 records | Documentary basis for worked examples and deferred-case boundary; no captures, corpus analysis or new scientific validation performed. |

No normative conflict required weakening a standing order. The pre-existing `PROVEN` definition already says “decisive evidence within an explicit scope”; `STRONG` still means substantial independent support with a material gap. The refinement makes coverage and completeness explicit without redefining either. [Workflow step 7](../../WORKFLOW.md#question-led-research-loop) still requires proposing the next bounded step rather than automatically beginning it; selecting among already authorized offline analyses is distinct from expanding scope.

The apparent tension between a positive beacon observation and historical `INDETERMINATE` membership output is resolved by distinguishing the property claimed. Historical output and scientific conclusions are preserved. The brief's informal enabled-beacon wording is qualified to the durable record's saved disabled-clear state under conditional loader preconditions. Output-link and cargo `STRONG` claims remain proposed pending review. Existing SOR-D-0026 quest deferral remains controlling. No historical reclassification or retrospective reporting-format rewrite occurred.

## Changes and decision rules

- `docs/EVIDENCE_STANDARD.md`: independent coverage/completeness dimensions; strongest scoped conclusion; concrete reopening criteria; claim/use-specific support; scientific autonomy within authorization; answer-first reporting; four linked worked examples.
- `AGENTS.md` and `WORKFLOW.md`: concise cross-references to those rules, preserving standing gates and review.
- `docs/templates/finding.md`: concise tested/inferred/unknown coverage and optional completeness justification, plus reporting reference.
- `docs/templates/experiment.md`: answer-first guidance for completed substantive reports without suggesting planned execution occurred.
- `docs/DECISIONS.md` and `docs/RESEARCH_STATE.md`: SOR-D-0027 rationale, prospective effect, scope and review status.
- `docs/implementation-briefs/README.md`: retained brief and review-package discovery.
- This new audit: authoritative roles, reconciliation, checks, limits and follow-up scope. The supplied brief was already untracked on arrival and is included unchanged in the full review diff.

Use confidence for support of the exact interpretation; coverage for tested/inferred/unknown applicability; completeness for justified coverage of every qualifying instance within the claimed scope. Accepted `STRONG` results may guide later analysis within scope, subject to revision. Reopen for in-scope contradiction, misstated provenance/coverage, analysis error or a materially better explanation. Outside-scope exceptions are tracked separately. Definitive counts/absence require completeness and a validated qualifying predicate; narrower positives and detection-only negatives remain useful. Production/save-editing guarantees retain stronger proof and separate authorization requirements. No rigid evidence-method hierarchy is introduced.

## Worked examples and evidence state

The [worked applications](../EVIDENCE_STANDARD.md#worked-applications--existing-status-preserved) cite the current durable sources:

1. Ordinary beacon diagnostics: zero before placement, one disabled-clear after placement; Save52 has 17 clear / two set. Sampled byte/framing observations `PROVEN / SAVE`, conditional mapping `STATIC`; active membership remains `PROVISIONAL`, not complete enumeration.
2. Output links: reversible relationship payload with retained endpoint candidates and within-session controls; byte observations `PROVEN / SAVE`, semantic association **proposed STRONG pending review**. Literal failure and cross-session churn preserved.
3. Cargo: 24 reciprocal pairs match the manual network multigraph; observations `PROVEN / SAVE`, semantic interpretation **proposed STRONG pending review**. Parallel physical-pad identity and transport semantics unresolved.
4. Location: numerical runtime/save compatibility and arithmetic are supported; same/related local-frame interpretation remains `PROVISIONAL`. Transform ownership, units/frame, planetary mapping and latitude/longitude remain unresolved.

This task independently checked documentary correspondence, not the original scientific experiments. Existing point-of-use source records/credits remain attached through the reports; no new external consultation, copied third-party implementation, rights acceptance or publication clearance was needed. Existing publication restrictions remain.

## Validation and complete diffs

Checks performed: `git diff --check` passed; internal inline Markdown file links and heading anchors checked across 113 tracked/new Markdown files with zero missing targets/anchors; original confidence/basis/publication definition paragraphs compared verbatim with HEAD and preserved. Manual governance review found no contradictory new gates or competing confidence hierarchy; normative rules reside in the evidence standard with short references elsewhere. Duplicate examples here summarize status for handoff rather than adding rules.

Git path checks confirm all eight modified tracked files are authorized Markdown, with no scientific scripts, existing experiments/evidence or historical registers modified. The index is empty. Only this audit and the supplied brief are untracked non-ignored files. A tracked-file scan for `.sfs`, `.dmp`, `.exe`, `.dll`, `.bin`, `.gpr` and `.zip` found none; no new binary/raw artifact is tracked or staged. Changed authored files are UTF-8 without BOM with LF endings. No staging, commit, push, launch, attachment, deployment or save analysis occurred.

Limits: the original experiments were not rerun; this verifies documentary consistency, links, definitions and Git paths, not engine semantics, scientific promotion or publication clearance. The link checker covers inline Markdown links/headings, not remote URL availability or arbitrary HTML/reference-link syntax. No new permission issue was identified. Full check details and the original validation helper are ignored local review artifacts under `.local-work/reviews/methodology/`: `validation.json` and `validate.py`; these are local review locators, excluded from publication.

Review exports under that same local directory: `task-only.diff` contains all nine authored changed/new documents; `full-current.diff` additionally includes the unchanged supplied brief, which was already untracked on arrival. Both include new documents explicitly and are ignored, never staged. Neither diff implies integration approval. Git generated the individual patches directly; the review helper concatenates their bytes without text reserialization.

Final `git status --short`:

```text
 M AGENTS.md
 M WORKFLOW.md
 M docs/DECISIONS.md
 M docs/EVIDENCE_STANDARD.md
 M docs/RESEARCH_STATE.md
 M docs/implementation-briefs/README.md
 M docs/templates/experiment.md
 M docs/templates/finding.md
?? docs/audits/research-methodology-evidence-standards.md
?? docs/implementation-briefs/CODEX_BRIEF_SOR_research_methodology_evidence_standards.md
```

## Proposed next separate brief

Ordinary-case beacon detector refinement only: define the reported property as an ordinary player-built inline case-5 beacon candidate with conditionally decoded saved disabled state; specify tested versions/representations, inferred applicability and excluded/unknown cases. Design an answer-first report separating positive identity/state evidence from unresolved active-player membership and exhaustive counts. A future authorized offline pass could challenge that scoped property against independently labelled controls/holdouts and preserve alternate/unhandled records explicitly. Do not require resolving deferred Terran Armada quest status, reinterpret promotion as membership, promise absence, or change current algorithms here. Draft and review a separate downloadable brief before any implementation; new live checkpoints would need their own explicit authority.

Suggested later commit message: `docs(research): distinguish evidence confidence from coverage`.
