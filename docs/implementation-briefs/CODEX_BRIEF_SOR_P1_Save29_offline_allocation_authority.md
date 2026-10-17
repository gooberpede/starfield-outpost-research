# Codex research brief — P1 Save29: offline determination of allocation authority

**Project:** `starfield-outpost-research`  
**Type:** Bounded native-static/save analysis, hypothesis adjudication, documentation and independent review  
**Authority:** Offline, read-only examination of existing project-owned evidence and approved static tooling; authored documentation and local review artifacts only. **No** game launch, live observer design/build/deployment, debugger attachment, save modification/writing, new gameplay, staging, commit or push.

## 1. Question and agreed evidentiary policy

We have **accepted** the Kreet Save29 repeated-load result as a **PASS for project purposes**: after three independent desktop-exit/restarts, the same extractor (#1) was powered and #2 unpowered in an outpost with 6 available power and 10 required. This result is **not reopened**, subjected to retrospective test thresholds or discounted for lack of universal proof.

Determine which native mechanism best explains the settled state in this ordinary case:

- **R — State-preserving restoration:** saved `Extra9C` powered bits are restored and remain effective in this ordinary load; potential load-related allocator activity does not independently displace this already feasible pair.
- **C — Deterministic reconstruction:** load/attach processing invokes allocation which independently constructs the winning consumer set from a repeatable ordering/graph and supersedes, or effectively determines, the saved pair.
- **H — Hybrid/conditional:** native logic explicitly retains satisfactory prior assignments but recomputes when specified conditions arise, or separate load paths yield distinguishable outcomes.

The core distinction is **the authority for the resulting consumer selection**, not merely whether an allocator *can be called*, nor whether a setter is invoked with an unchanged value. Restoration and some recalculation can coexist.

**Agreed standard: reasonable engineering confidence and explanatory sufficiency.** Identify native causality with a bounded, relevant call-path analysis and corroborate against Save29. Do **not** require exhaustive elimination of conceivable callbacks or proof of every historical instruction. When an established restoration mechanism sufficiently explains the observation and targeted tracing finds no positive evidence of an allocation that supersedes it, accept **R as the best-supported working explanation**, where warranted, rather than maintaining an equally weighted speculative C (the agreed Russell's Teapot/burden-of-proof principle). Conversely, accept C if the actual reachable allocation path, ordering and result derivation are adequately demonstrated. A concrete contradictory path can defeat an explanation; mere unexamined possibilities cannot. This does **not** authorize false claims of proven nonexecution: distinguish **“not found in examined paths”** from **“cannot execute.”** Existing project `PROVEN / STRONG / PROVISIONAL / OPEN` confidence terminology remains authoritative; a `STRONG` result is useful, acceptable working knowledge.

## 2. Starting facts and research boundary

Read `AGENTS.md`, `WORKFLOW.md`, `docs/EVIDENCE_STANDARD.md`, `docs/RESEARCH_EXECUTION_PROTOCOL.md`, `docs/templates/completion-contract.md`, `docs/experiments/power/load-determinism.md`, `followup.md`, `native.md`, `saved.md`, `save29-test-plan.md`, `save29-derivatives.md`, relevant reviews and the existing function register. Reuse the pinned 1.16.244.0 image/ESM and verified local native exports where valid; check actual versions/hashes before relying on them. Treat historical native interpretations as starting evidence subject to correction, not assumptions.

Known positive anchors:

- Save29 solar array `ff022841`, extractor #1 `ff022917` (saved `0x40` set, position ~105.26/282.59/16.82), extractor #2 `ff02294d` (saved `0x40` clear, ~87.36/269.61/14.89). User console XYZ independently connected them to the visually observed objects. Runtime RefIDs can change.
- `Extra9C` loader retains the powered flag; native getter and difference-application paths are already mapped.
- `TESObjectLoadedEvent` / Workshop sink provides a real, load-reachable route capable of scheduling allocation from a notified reference. **Do not disregard this positive evidence merely because restoration is simpler.** Its invocation and effects for Save29 still need causal assessment.
- Some ordering arises from saved links, ordered notification lists, record layout or reconstructed owner indices; mere correlation between smaller saved FormID, earlier serialized offset and winner #1 does **not** prove any one orders allocation.
- Earlier owner-refresh analysis indicated that permuting eligible generator-root iteration alone does not change its union of contributions under fixed inputs. Distinguish that mechanism from per-reference allocation and later updates.
- Save writing was assessed **NO-GO** owing to unqualified BCPS header preservation. Do not reopen writer work or propose edited saves as a prerequisite.

## 3. Work plan (finite, hypothesis-led)

### A. Trace the load-to-effective-power paths

Start with the **known** restoration, finalization notification, Workshop event handler, queued/immediate worker, allocator and difference-set application. Follow only relevant branches into owner membership, activation/eligibility and callback scheduling. Produce a compact **reachable-path table**: entry and trigger, gates, candidate root, relevant object coverage, old/new powered-set operands, whether it computes or applies a materially new assignment, and evidence/unknowns. Distinguish a path's existence from its necessary execution during this Save29 load. Do not search all executable callbacks or infer absence from a truncated decompilation.

### B. Establish whether ordered reconstruction is actually used

For a relevant load-reachable allocation, identify the *actual* enumeration/priority mechanism and its provenance: ordered serialized references, FormIDs, `ExtraCB` connections, restored `Extra4C`, rebuilt `Extra4D`, notified-reference root, generator list, or other native container. State explicitly which candidates are **used**, merely **available**, or **not implicated**. Analyze whether the consumer calculation uses the **old powered bits** in selecting winners or uses those bits only to decide which differences to write. A bounded Save29 two-consumer walkthrough is useful only if its root, connections and gates are grounded, not assumed. If exact runnable inputs cannot be established, say which specific input is missing.

### C. Compare causal explanations

For R, C and H, tabulate supporting evidence, concrete conflicts, essential missing links and explanatory burden. Do not simply report “both possible.” Address directly:

1. Do restored `0x40` bits alone suffice to explain accepted Save29 observations, given the known native restoration mechanism?
2. Is an independently ordering-and-selecting allocation demonstrated on a relevant load path, or only potentially invoked?
3. If an applicable allocator runs and calculates the same one-on/one-off pair, does it independently determine that pair, or leave restored authority observationally indistinguishable? Distinguish calculation, old/new comparison, and actual mutation.
4. Can the available saved ordering/graph and proven native traversal make Save29's winner predictable, without hand-picking a favourable root after seeing the result?
5. What result best fits the evidence **now**, and what concrete observed/native counterexample would overturn it?

## 4. Frozen acceptance and stopping rules

**Complete the finite offline assignment when** the known positive load/restoration/allocator/result paths and plausible relevant ordering sources have been examined to a defensible boundary; a ranked best-supported explanation has been selected; and concrete contrary evidence and material unknowns are recorded. Do not pursue conjectural functions or expand into general reference-load reverse engineering solely to avoid a `STRONG` rather than `PROVEN` conclusion.

**Permissible verdicts:**

- **R established/strongly supported within ordinary Save29 conditions:** saved powered state is demonstrably restored, sufficient for observed allocation; bounded native evidence supplies no supported superseding winner selection in that scenario. Say exactly which positive load-related allocator paths remain, if any, and why they do not defeat this judgment.
- **C established/strongly supported:** specific load-reachable recomputation, reproducible ordering and independent winner selection adequately explain Save29; articulate how saved flags are superseded or made nondecisive.
- **H established/strongly supported:** identify a concrete native conditional rule/path distinguishing preservation and reassignment.
- **OPEN:** permitted **only** where a specific, materially relevant missing causal edge leaves competing explanations comparably supported. Name the missing edge and why it prevents selection; do not use generic “other callbacks might exist” as an OPEN justification.

If R is best supported without identifying a required recomputation, **do not demand a live observer to disprove an invisible alternative**. If C is best supported, do not demand proof that restoration never matters elsewhere. A completed research assignment may have an OPEN finding, but not from arbitrary escalation of proof requirements. Stop after this scoped analysis: no automatic observer or tool-building follow-up. Recommend such work only if there is a **specific contradiction, material application need or genuinely decisive observable** worth its independently justified engineering cost; otherwise close/defer P1 mechanism research.

## 5. Deliverables and controls

1. **Answer-first, plain-English conclusion** (one page maximum before technical appendix): choose R/C/H/OPEN, state confidence and scope, explain the Save29 consequence, and state what would change the conclusion. Prefer statements a maintainer can act on over “conditionally reconstructable.”
2. Evidence-linked native trace and ordering-provenance table with exact pinned RVAs/functions, operands and grounded Save29 identities; negative search/coverage claims must name the examined boundaries. Explicitly label illustrative models and unsupported assumptions.
3. Hypothesis assessment matrix, decisive versus compatible evidence, clearly separated **scientific confidence** and **assignment-completion disposition**; preserve the previously accepted Save29 reload PASS and writer NO-GO.
4. Update existing P1 durable docs, `RESEARCH_STATE.md`, relevant `DECISIONS.md`/`BACKLOG.md`, function register **only as findings warrant**, with links and transparent supersessions. Retain primary raw evidence locally and publication/permission distinctions; don't rewrite historical claims silently.
5. Independent reviewer per `WORKFLOW.md` and `docs/RESEARCH_EXECUTION_PROTOCOL.md`, assessing especially overqualified absence claims, ignored positive event paths, circular ordering inference and unjustified observer escalation. Report mandatory-criterion PASS/FAIL/NOT TESTED, independent observations, regressions, protected-input hashes, and deviation ledger.
6. Audit authored UTF-8/LF text, links, encoding corruption, RVA/version notation and formatting. Produce `*-task-only.diff`, `*-complete.diff`, status/path/exclusion manifests and **forward/reverse exact patch reconstruction** under established ignored `.local-work/` practices. No binary/save/native payloads in diffs. Suggest one combined Conventional Commit subject. No staging, commit or push.

### Compact completion contract

- **Task type:** bounded native research hypothesis adjudication and documentation.
- **Question/deliverable:** select the best-supported load-time power-allocation authority mechanism for Save29 using available offline native/save evidence.
- **Scope/bounds:** read-only static analysis and locally produced authored reports/receipts; protected source saves, executables and databases unchanged; no live, save writer, observer or Git integration actions. Preserve applicable C:/D: free-space and integrity guards.
- **Mandatory acceptance:** deliverables 1–6; anchored positive call-path examination; burden-of-proof/hypothesis matrix; explicit usable confidence and stop decision; independent review.
- **Optional:** a minimal illustrative two-consumer model, if independently grounded. Not necessary for completion.
- **Negative-result closure:** finite path coverage plus a specific material unresolved causal edge permits OPEN; failure to find a speculative mechanism without such an edge supports explanatory sufficiency rather than an endless search.
- **Continuation authority:** investigate/correct/retest within these offline limits without a new brief; fix failures within the same assignment.
- **Exit/escalation:** halt on identity/hash, rights, resource or protected-input guard failure; record blockers and request narrow approval. No new live/deployment/save-modification permissions. No arbitrary elapsed-time or evidence-volume stop conditions for otherwise healthy work.
- **Review/disposition:** separate science from execution completeness; independent ACCEPT/REWORK/ESCALATE, preserved failures, verified complete/task-only review artifacts. Material acceptance changes require explicit maintainer approval.
