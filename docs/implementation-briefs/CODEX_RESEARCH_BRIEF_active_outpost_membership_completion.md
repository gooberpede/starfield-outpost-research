# SOR — Active Outpost Membership: Complete Beacon Identification and Ownership Validation

**Codex research/implementation brief — for critical review before commit**

## Objective

Finish the specific outstanding work toward determining, **from a Starfield save**, whether the reconstructed character has any active player-owned outposts. Focus on complete identification of outpost beacon references and the saved state establishing their membership/ownership. Do not start a general save-format investigation.

The known controlled contrast is **Save3/S0/S0C (no outpost)** versus **S1/S1C (one newly placed beacon/outpost)**. The mature **Save52** provides an independent complex positive: 17 player-recognized active outposts and two remembered removed outposts, reflected in 19 identified beacon records. Existing research framed 409 saves and found the inline type-5 beacon path, but its coverage is not complete; a historical alternate initial/base reconstruction case (notably `HIST-0016`) and the connection to workshop/ownership predicates remain open.

The intended output is a reproducible, evidence-based classifier or, if completeness cannot yet be established, the most advanced justified partial classifier **plus a precise demonstration of the remaining obstacle and what would resolve it**. Do not stop at reiterating earlier blockers: investigate them and test new hypotheses.

## Standing interpretation: disabled versus deleted

The current Save52 observations are:

- 17 beacons corresponding to known active outposts have the decoded **disabled** bit clear.
- Two beacon-like records corresponding to previously removed outposts (`Feynman VII-b U He3` and `Feynman II Ag U V`) have **disabled** set.
- None of those 19 examples has the decoded **deleted** bit set.

**Prioritize the observed disabled-state distinction.** The fact that players can delete an outpost through gameplay does **not** establish that the engine's `IsDeleted` flag must be used. Treat `IsDeleted`/the decoded deleted bit as **shelved for active-outpost classification**. It may be recorded incidentally when decoded, but do not make it a required predicate or spend effort exploring it solely because of its name. Reopen it only upon (a) a demonstrable outpost record with that bit set, or (b) a concrete outpost-specific path that sets/clears it. Interpret the two disabled historical beacons as consistent with gameplay removal, not as proof of a universal deletion representation.

Record this research-priority decision in appropriate durable state/decision documents, without overwriting the original observed flags.

## Ground truth and evidence discipline

Use the existing, hash-verified archived inputs and their manifests; locate exact paths from the repository rather than inventing them.

- **Negative:** pristine Save3, S0 and S0C (known no beacon/outpost).
- **Simple positive:** S1 and S1C (known one outpost).
- **Complex positive:** Save52 with the known 17-outpost network, corroborated by the manually maintained JSON and earlier mature-save validation; the JSON is comparison evidence, not an input to the classifier.
- **Adversarial/coverage:** S2–S7C, L0–L2C, historical saves (including `HIST-0016`), and launch-era third-party saves, subject to actual format support and third-party rules.

Maintain strict separation between (1) physical framing, (2) beacon-base/reference identification, (3) saved disabled state, (4) runtime workshop/player ownership and registration, and (5) the resulting *active-outpost* classification. An enabled beacon-like record is not automatically a proven player-owned outpost.

Avoid circular validation: derive candidate rules from the controlled contrast and structural/static evidence, run them against held-out saves **before consulting** those saves' previous heuristic labels, and report disagreements and false positives/negatives.

## Research authority and priorities

Codex has broad authority for **offline** hypothesis-driven investigation directly serving the objective. It may inspect or extend framing and record parsers, reference/base-form reconstruction, save tables, relevant xEdit/ESM forms, existing Ghidra static analysis, loader paths and the internal Almanac/UI outpost-enumeration path. The latter is a *candidate runtime validation path*, not an automatically authoritative registry. Use the exact source-backed semantics and addresses in durable records; do not assume a debugger-derived conclusion beyond what was observed.

Investigate, rather than merely restate, the following:

1. **Complete beacon representation coverage.** Trace alternative initial-data/base-form reconstruction paths, including the `HIST-0016` counterexample. Determine when a beacon can be encoded other than the previously decoded inline type-5 case. Enumerate actual alternate forms and provide tests covering them. Distinguish absent records from undecoded ones.
2. **Reference identity.** Where needed, bridge save-local reference encodings to the specific placed reference, its base FormID/type and any workshop-identifying metadata. Do not confuse base object identity with placed instance identity.
3. **Disabled-state semantics.** Confirm the decoded flag's encoding, applicability and reconstruction behavior on the relevant record paths. Preserve contradictory examples.
4. **Ownership/registration.** Identify which save-resident data, together with game/ESM definitions, establishes player-owned active-outpost membership. Relate it to outpost/workshop enumeration and `ExtraWorkshop`/keywords where supported. A runtime/UI filter may help but cannot replace proof that the offline predicate is complete.
5. **Completeness and negative proof.** Determine what must be exhaustively enumerated to conclude `NO_ACTIVE_OUTPOSTS` on a supported file. Show why no alternate representation can silently evade the parser within the claimed scope. Unsupported variants must remain `INDETERMINATE`.

Codex may revise earlier hypotheses and explore necessary general save machinery **only to the extent it directly supports these questions**. No mandatory method or predetermined implementation is imposed.

## Classifier contract

Design and test a narrow offline interface with at least:

- `OUTPOSTS_PRESENT`: one or more active player-owned outposts demonstrably identified;
- `NO_ACTIVE_OUTPOSTS`: validated complete enumeration establishes zero;
- `INDETERMINATE`: incomplete representation coverage, ambiguous semantics, unsupported variant or insufficient evidence.

Report outpost candidate counts, decisive supporting record references, relevant decoded states, exact parser coverage and reason codes for indeterminate cases. Do not transform an empty candidate set into `NO_ACTIVE_OUTPOSTS` without a completeness argument. Avoid hard-coding Save3, S1, Save52, names or expected counts into classification logic.

**Milestone A:** separate Save3/S0/S0C from S1/S1C, with at least one grounded active beacon identity and no false outpost positives on the known negatives.

**Milestone B:** justified absence for the supported representation, including an explicit completeness argument that confronts alternate paths.

**Milestone C:** adversarial cross-corpus validation, with failures and unsupported versions visible rather than concealed.

## Work and stop conditions

Do not terminate the investigation simply because one decoder or hypothesis fails, or because an existing report called the problem unresolved. Follow leads, test competing hypotheses and use the available corpus to falsify them.

A satisfactory outcome is either:

**(i)** a tested classifier with a clearly bounded completeness claim and credible negative detection; **or**

**(ii)** concrete material progress plus a **persuasive, evidence-backed account of the precise unresolved dependency**, the experiments/analyses performed to resolve it, why current authorized offline methods cannot decide it, and the *single smallest* new permission/data/live experiment needed next. “Needs more research” or “unknown save format” is not acceptable as a stopping explanation.

Do not fabricate conclusive absence merely to meet the milestone. If a decisive question truly requires a live controlled experiment, propose it for separate authorization; do not run it here. **Do not create a beacon deletion test** under this brief.

## Scope and preservation

- **Offline only.** No Starfield launch, save loading/resaving, SFSE deployment, live debugger attachment or direct editing of source saves.
- Read verified copies in ignored `.local-work/` paths. Preserve hashes and avoid duplicating large evidence unnecessarily.
- Keep raw `.sfs` saves, dumps and raw decoded payloads untracked. Retain the 40 GB free-space guard where relevant and cap diagnostic output.
- Continue source attribution, the `gooberpede` maintainer-reuse exception with provenance, and all third-party permission/publication constraints.
- Existing durable evidence must remain historically accurate. Update registers only with well-supported new observations, explicitly distinguishing `OBSERVED`, `INFERRED` and `HYPOTHESIZED`.
- Do not stage, commit or push.

## Validation and deliverables

Provide:

1. A precise comparison of known negative and positive saves at the decisive record/state level.
2. Coverage inventory of inline and alternative beacon/base reconstruction paths, including `HIST-0016`.
3. Decode and semantics of the disabled state; explicit shelved status for `IsDeleted`.
4. Evidence connecting save records to placed beacon identity and workshop/player ownership, including gaps.
5. Executable/reproducible classifier or bounded prototype, with documented outputs and reason codes.
6. Held-out corpus challenge: predicted states, independent ground truth where available, counterexamples and unknowns; avoid using prior heuristic classifications as ground truth.
7. Completeness argument **or** rigorous impossibility/authorization-boundary account as defined above.
8. Updated experiment report, findings/hypothesis/state/decision records as justified, with provenance and falsification cases retained.
9. Tests, exact input hashes, raw-artifact tracking checks, `git diff --check`, internal-link check, changed-file inventory, review diff and `git status --short`.
10. A recommended next step only if necessary, narrowly tied to the unresolved blocker.

If complete classification is achieved, propose an appropriately scoped evidence promotion for review; do not promote uncertain semantic assertions merely because the tests pass.

**Suggested commit message after separate review (not authorization to commit):**

`research: resolve active outpost beacon identity and membership evidence`
