# Codex research brief — SOR: Fallback-Grid Provenance, Selected-Reference Identity and Acquisition Assessment

**Assignment type:** Offline research, deterministic analysis, and standing-workflow correction  
**Starting state:** Continue from the **committed and synced** Starfield outpost research repository and completed SorNativePositionOracle 0.4.0 live attempt. Do not assume outstanding uncommitted changes; inventory the actual working tree first.  
**Authority:** No Starfield launch, attachment, native plugin change, Vortex deployment, new live capture, save editing, staging, commit, or push is authorized.  
**Working repository:** `D:\Projects\starfield-outpost-research`.

## 1. Context and objective

The 0.4.0 live attempt yielded **778 intact native records** and one fresh native **fallback-path generic grid** observation, with the grid component `[1, 10464, 21141]` exactly matching the corresponding **frozen offline prediction**. The calculation used **zero floor offsets**. The instrumented existing-reference search returned null, and the fallback resolver supplied a reference with sampled base `00007145`, not the ordinary outpost beacon base `002C60E9`. The experiment did **not** establish selected SOR-003 workshop identity, a nonzero-offset algorithm case, or complete native durable-position equivalence. Apparent Q-chain gaps were subsequently identified as inspector/decoder false negatives for legitimate Q → E nesting; preserve the original evidence and record of the correction.

**Primary scientific question:** Reconstruct the native provenance and identity chain of that *actual captured* fallback-grid invocation. Determine what the fallback reference represents, why the search/fallback route was selected, and whether its resulting grid descriptor can be joined independently to a saved site, terrain frame, selected location, or other established positional identity.

This is an evidence-led investigation, **not** an instruction to build another observer or a justification to stop at the first missing operand. Pursue substantive static and offline dependencies until a defensible result or genuinely demonstrated evidence boundary is reached.

## 2. Mandatory research work

### A. Reconstruct the observed native execution chain

Follow relevant code in the pinned Starfield.exe static analysis and retained raw 0.4.0 acquisition through:

1. Gameplay selection/travel request or other producing caller, where evidenced.
2. Native request structure, selection identity and active source/terrain context.
3. Existing-reference search: actual arguments, especially **null source and known-reference inputs**, return value, guards and alternate routes.
4. Fallback resolver: inputs, producing caller, selection rules, output reference and its lifetime/ownership.
5. Descriptor creation, source hierarchy and generic grid function (including in-place result semantics and the zero-offset path).
6. Downstream consumers and the interpretation of the observed result, insofar as required to determine what it positions.

Reconstruct concrete control-flow predicates and data dependencies, not merely function labels. For every link state whether it is **directly captured**, **recovered from static native code**, **independently corroborated**, **conditionally inferred**, or **unknown**. Absence of a recorded hook event is not proof that an operation never ran. If an available trace or static lead is insufficient, follow immediate producers/callers and alternative supported paths rather than stopping automatically.

### B. Resolve selected-reference and saved-site identity

Investigate the meaning and provenance of sampled base `00007145` and its relationship, if any, to SOR-003, SOR-002, site anchors, landing areas and terrain overlays. Examine relevant save-reference records, parent/relationship identifiers, qualified plugin/FormID domains, static record definitions, and save-load remapping/handle rules as needed. Existing project research and, where relevant, the separate `starfield-reference-handles` work can be consulted without treating similarly shaped IDs as interchangeable.

Discriminate explicitly between **runtime pointer**, **native handle**, **dynamic reference identifier**, **saved FormID**, **base-object FormID**, **persistent reference identity**, **terrain/site identity**, and **workshop/beacon identity**. A numerical coincidence, shared angle or matching grid tuple alone is insufficient proof of ownership. Report any unresolvable joins with the exact missing transformation/observation.

### C. Test the model and investigate nonzero-offset coverage

Preserve the **23 frozen predictions** exactly. Compare the captured native tuple `[1, 10464, 21141]` with the correct frozen component without altering expectations or retroactively assigning an unsupported workshop identity. Analyze the grid arithmetic and look for available offline/native/static/save cases addressing nonzero offsets, carry, snapping, reflected axes, or relevant alternate branches. Distinguish model-derived predictions and synthetic tests from independently generated native observations. Do not fabricate an oracle by reusing the algorithm under test to calculate its own expected outputs.

Implement focused **deterministic offline tools/tests** where they materially answer a hypothesis, including negative/counterexample cases. Reconcile the complete captured invocation and any causally relevant other records against raw evidence; retain original artifacts and provide hashes and provenance. Do not require an arbitrary minimum number of samples; use coverage of meaningful native branches.

### D. Decision-ready acquisition assessment

Finish by ranking **concrete, code-supported** next routes to independent durable-position validation. For each route describe (i) exact missing native value or identity, (ii) source-supported trigger, (iii) what a positive or negative observation would distinguish, (iv) whether additional controlled saves would help, (v) intervention/risks, and (vi) whether the route validates generic grid, selected site, compensated workshop center, or complete model equivalence.

Prefer using captured evidence or offline dependencies before suggesting further instrumentation. A proposal for a new observer or controlled-save experiment is **not itself authorization**. The abandoned external debugger remains closed. Avoid optimizing merely for easiest instrumentation or for reaching one historically selected function.

## 3. Required `WORKFLOW.md` standing-order correction

In the same assignment, update `WORKFLOW.md` (and any genuinely authoritative run-card template/standing instruction needed to avoid contradictory defaults) to establish:

> **Elapsed time, evidence volume, a delayed operator action, or a routine monitoring-cadence overrun alone must not terminate an otherwise healthy scientific experiment.** Do not invent hard session/admission deadlines, event counts, evidence-size quotas or arbitrary capture cutoffs. Our established protections—particularly the **40,000,000,000-byte caller-available free-space guard on both C: and D:**, verified target/plugin identities and instruction guards, protected inputs, instrumentation/evidence integrity, actual worker failure, and explicit operator STOP—remain in force. If an additional hard limit is essential for a demonstrable safety or engineering reason, justify it concretely and **obtain maintainer approval before the live run**. During an unexpected delay, warn and continue where safe; consult the operator before terminating solely for the delay. Do not retrospectively redefine a violated approved limit as a pass.

Distinguish legitimate health checks (including real failure conditions) from arbitrary wall-clock limits. This policy must apply to **future** run cards; do not rewrite historical experiment criteria or results. Do not silently remove mandatory safety controls to improve throughput. Review other relevant templates for conflicting defaults and either correct them or document why retained historical cards are immutable.

This documentation change is **mandatory**, not a discretionary backlog suggestion.

## 4. Completion contract and independent review

Follow the repository Research Execution and Completion Protocol. An interesting partial finding, an unresolved in-scope dependency, a failed test or a recommendation for a follow-up brief **is not completion**. Preserve failures and investigate/correct them within this assignment. Research can conclude negatively if the negative result is genuinely supported and bounded.

Acceptable final dispositions:

**A — Supported provenance/identity reconstruction:** A reproducible, evidence-backed account of the captured chain, including what the native grid result does and does not validate, the independently supported identity joins, counterexamples, and ranked acquisition options. Any remaining unknown must be explicitly bounded rather than concealed.

**B — Completed evidence-boundary investigation:** After pursuing the authorized static/save/trace dependencies, demonstrate **precisely** why a decisive link cannot be made from existing evidence; identify the missing operand, identity or producer observation and which concrete acquisition would discriminate the remaining alternatives. Show actual investigated leads and failed alternatives. Do not relabel unfinished analysis as B.

The reviewer must test scientific independence, provenance and coverage; reject unjustified SOR-003 equivalence or ambiguous runtime/saved identity joins; verify that negative or escalated findings are not premature; check regression tests and the `WORKFLOW.md` policy; and issue **ACCEPT**, **REWORK**, or a substantiated **ESCALATE**. Reviewer REWORK is performed under this same assignment. Codex may use **at most two concurrent sub-agents**, comprising an independent reviewer and, when useful, one specialist researcher. The primary agent owns integration and final quality.

## 5. Boundaries and preservation

- **Offline/read-only only** for proprietary game content and protected saves; analysis scripts may write new derivatives solely in ignored local work areas.
- No Starfield process launch/open/attachment, no SFSE modification/deployment, no debugger, no native call injection, no new save generation, no edits to protected evidence or frozen predictions.
- Preserve original 0.4.0 binary, observer sources, WAL/raw records, historical reports, source manifests and prior package hashes unchanged unless a separately explained non-proprietary analytical fix is explicitly in scope. Keep historical incorrect inspector outputs and their correction provenance rather than overwriting evidence.
- Apply the **40 GB** free-space rule to relevant disk-intensive operations. Unexpected scientific outcomes and unreadable optional fields are evidence, not automatic termination.
- Do not incorporate third-party code without authorization; project-owned code may be reused with source/revision provenance. Do not stage proprietary binaries, saves, raw dumps or local private receipts.
- **No stage, commit, push, publication or live activity**. User will review diffs and choose when to commit.

## 6. Deliverables and review package

1. A durable, answer-first **research report** under `docs/experiments/`, showing the captured invocation's provenance chain, branch/predicate/identity ledger, exact evidence citations to retained local records, resolved/unknown joins and scoped conclusions.
2. Reproducible read-only analysis tools and tests where needed, with run instructions, verified counts/hashes and failure/counterexample accounting.
3. An explicit validation matrix separating **generic grid-component agreement**, **selected-reference identity**, **saved-site linkage**, **nonzero-offset branch coverage**, **workshop-center equivalence** and **full durable-position equivalence**.
4. A ranked, decision-ready acquisition assessment with a clearly specified next action **only if justified**.
5. The `WORKFLOW.md` correction and any minimal supporting template/document changes, preserving earlier standing orders.
6. Independent reviewer record, including challenges, in-assignment rework and final acceptance matrix.
7. Review diffs in `.local-work/diffs/`: task-only and **complete working-tree** patches (including new untracked text), plus `git status --short`, manifest, excluded binary/ignored artifacts and exact patch/whitespace/links/test checks. The complete patch must reflect the **actual** working tree, not assume the last brief's state.

The final response must state **COMPLETE — PASS**, **COMPLETE — EVIDENCE-BOUND NEGATIVE**, or **ESCALATE — GENUINE NEW AUTHORITY REQUIRED**, with an evidence-backed justification. Do not announce complete native equivalence without a true independent, identity-bound native comparison. Do not request authorization for work already permitted by this brief.
