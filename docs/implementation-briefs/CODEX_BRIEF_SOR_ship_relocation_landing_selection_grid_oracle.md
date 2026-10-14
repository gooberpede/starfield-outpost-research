# Codex Research Brief — Ship Relocation, Natural Landing-Site Selection and Native Grid Oracle Assessment

**Project:** `D:\Projects\starfield-outpost-research`  
**Mode:** Offline research and analysis only  
**Starting point:** Current committed/synced repository, including the 0.4.0 native observer, its live evidence, the fallback-grid provenance investigation, and the established Research Execution and Completion Protocol.  
**Authority:** No Starfield launch/attachment; no new observer build or deployment; no save modifications, native call injection, debugger revival, staging, commit or push.

## 1. Purpose and scientific priority

Establish whether the **natural ship-relocation mechanism** during travel to an existing outpost offers an independently identifiable native terrain-grid calculation useful for validating the **durable outpost-position reconstruction**. Follow ship placement only as far as needed to establish the relevant shared coordinate transformation and a defensible future acquisition path. Do **not** expand this task into a general reconstruction of landing-site procedural generation.

Existing evidence includes a fresh 0.4.0 **fallback** grid component `[1, 10464, 21141]` agreeing exactly with the frozen offline component, with zero offsets and a `ShipLandingMarker_80m_Large` (`00007145`) base. That is **not** a selected SOR-003 Workshop identity or end-to-end durable-position validation. Preserve this distinction and the frozen predictions without adjustment.

## 2. New operator-supplied observations — treat as manual evidence, not native proof

Starting from **Save25** (SOR-003, no SFSE), the player initially finds the ship at **LZ1**, the original Save3 landing location near SOR-002, approximately 230 m from SOR-002 and over 2 km from SOR-003. The observations include:

- Local fast travel **SOR-002 ↔ SOR-003** often leaves the ship in its existing location (initially LZ1; after arriving via another location, potentially LZ3).
- Travel from a new Kreet landing area **LZ2** or **LZ4** to SOR-003 relocates the ship to a natural landing area **LZ3**, approximately 450 m from SOR-003.
- Travel from LZ2 or LZ4 to SOR-002 relocates the ship to **LZ1**.
- Travel to a separate POI with a conventional landing pad did not necessarily move the ship; its pad remained empty in the observed sequence.
- First arrival at a new landing area put the player in front of the ship ramp; repeat travel to that area placed the player elsewhere near its landing area.
- A restart and reload of original Save25 reproduced LZ4→SOR-003→LZ3 and LZ4→SOR-002→LZ1 behavior.

These are **two manually reported sequences**, not recorded native call traces. Distinguish player arrival, ship relocation, landing-marker generation/lookup/selection, and Workshop-center positioning. Do not infer that visible ship movement proves a newly generated marker; a pre-existing marker may have been selected.

Additional player experience, to treat as a hypothesis: natural ship landing areas partly overlapping an outpost's boundary may be excluded for that outpost when no suitable constructed landing pad exists. The ordinary workshop build radius identified in earlier static evidence is **150 native units**, but the value used by any landing-site exclusion test is unknown. The `80m` in `ShipLandingMarker_80m_Large` may indicate ship accommodation class rather than footprint radius; verify rather than assume. Constructed 40 m/80m pads and their familiar ship-follow behavior need **no new gameplay test** in this task.

## 3. Mandatory investigation

### A. Travel and ship-placement control flow

Trace relevant pinned `Starfield.exe` native functions and callers, using durable static evidence and the existing 0.4.0 raw records. Reconstruct as far as supported:

1. Origin and type of travel request; choice between local player-only relocation and travel that moves/repositions the ship.
2. Whether and how player arrival and ship placement are resolved separately.
3. The ship-placement invocation that looks up, selects, generates or instantiates a natural landing marker; distinguish those operations and prove any claimed ordering.
4. Existing-reference lookup versus fallback resolution, and the role of the observed `ShipLandingMarker_80m_Large` reference.
5. Native terrain-frame and grid transforms used in these paths; identify any operations shared with the saved durable-position model, including nonzero-offset/carry/rounding branches when supported.
6. Any native landing-area eligibility or outpost-exclusion predicate with recoverable operands. If no such predicate is found after a serious dependency search, report the searched scope and gap without asserting that exclusion does not exist.

Do not stop at a single failed call-chain lead. Follow relevant upstream/downstream dependencies and alternate routes within this task, while keeping the ultimate positioning question central.

### B. Reconcile existing evidence and establish identity limits

- Reinspect the genuine 0.4.0 fallback-grid capture, its nested invocation/route records and corrected decoder. Establish what is observed versus statically reconstructed versus hypothetical.
- Attempt to identify which request produced the ship landing-marker calculation and whether it can be attributed to an outpost destination, natural landing marker, saved reference or selected Workshop. Respect static FormID, dynamic token, handle, runtime pointer and base-form identity domains.
- Explain whether the manual contrast (SOR-002↔SOR-003 non-relocation vs LZ2/LZ4→SOR-003 relocation) is consistent with recovered control flow; enumerate alternative explanations not discriminated by the evidence.
- Determine whether the captured native grid transform is a useful oracle for a component shared with Workshop positioning. Do not promote ship-marker component agreement into full Workshop equivalence.
- Audit whether suitable nonzero-offset cases can be established from *existing* native or saved evidence. Synthetic cases may test reconstruction but do not count as independent native validation.

### C. Decision-ready acquisition assessment

Rank **concrete, source-supported** observation opportunities by scientific value and implementation intrusiveness, not by the ease of installing hooks. Contrast at minimum:

- Natural travel that visibly relocates the ship (e.g. LZ2/LZ4→SOR-003), versus local SOR-002↔SOR-003 travel where the ship stays put;
- Native ship landing-marker selection and generic grid calculations;
- A directly identity-bound Workshop positioning operation, if a credible path is found.

For the strongest opportunity, give the native call path, required input/output/identity observations, known branch prerequisites, the minimum proposed hook or passive observation set, a feasible Save25-based operator sequence, and what outcome would falsify or distinguish each competing explanation. State whether a new controlled save would materially improve the experiment; propose one only if justified and do not create it. In particular, do not assume that LZ2/LZ4 are durable selectable named destinations or that a fresh previously unvisited landing behaves identically.

## 4. Research tooling, integrity and scope

Read the actual repository conventions, prior native evidence, provenance ledger and relevant save references before modifying analysis code. Implement *offline-only* deterministic analysis/verification tools and tests as necessary to produce the evidence-backed conclusion. Keep raw local/proprietary data out of Git and review archives. Preserve source hashes, all frozen predictions and historical findings, including counterexamples. Honor the mandatory **40,000,000,000 bytes caller-available free** on both C: and D: for substantial evidence processing.

No arbitrary execution-time, monitoring, event-count or evidence-volume stopping thresholds. The `WORKFLOW.md` continuation policy remains in force. Genuine machine/instrumentation-integrity stops and explicit operator boundaries remain enforceable. No live Starfield access, new DLL, SFSE/Vortex deployment, debugger work, save changes or new manual gameplay under this brief.

## 5. Completion contract and acceptable outcomes

Apply the established Research Execution and Completion Protocol. In-scope obstacles require continuing investigation, corrections and rerun verification **within this assignment**, not a suggestion for another brief. Preserve failed hypotheses and counterexamples.

Return exactly one completed scientific disposition:

- **A — QUALIFIED ACQUISITION SCENARIO:** Evidence supports a specific natural ship-relocation/travel path to independently identified terrain-grid operations relevant to the durable-position model, and the minimal future acquisition design and discriminating controls are defined.
- **B — COMPLETE NEGATIVE ASSESSMENT:** A fully pursued dependency and evidence analysis demonstrates why the investigated ship-relocation routes do not currently give a qualifying identity-bound grid oracle, or demonstrates a better-supported alternative. Identify exact missing observations and the explored counterexamples; no generic “more investigation required” closure.

Neither outcome may claim exact native durable-Workshop equivalence without direct independent matching evidence. A legitimate **BLOCKED — AUTHORITY REQUIRED** is permitted only for an actually indispensable new permission/action, with a precisely specified request; offline unresolved leads are not automatically a blocker.

Deliver a standalone research report; native call/dependency and evidence ledger; manual-observation matrix with evidence grading; deterministic scripts/tests if needed; ranked acquisition design; acceptance matrix; changed-file inventory; `git status --short`; and complete and task-only patches in `.local-work/diffs/` including untracked task text. Apply internal link and patch-integrity checks. Do not stage, commit or push.

## 6. Agent use and what to assess

**At most two active sub-agents concurrently, excluding primary Codex.** The **independent reviewer remains mandatory** with a fresh context, original contract, code, direct evidence, test outputs and authority to issue ACCEPT/REWORK/ESCALATE; its established usefulness needs no further routine performance evaluation unless premature-handoff behavior recurs.

**Shift workflow assessment to the specialist researcher.** When a separable investigation warrants it, assign **one specialist** (for example, independently reconstruct native ship-relocation dispatch while the primary implementer reconciles live/save evidence). The specialist must deliver its own source-grounded result, rejected hypotheses and concrete evidence, not merely endorse the implementer's account. Primary Codex remains responsible for integration and correctness. Record briefly in the final report:

- What specific question the specialist owned and what independent evidence it produced;
- Which new findings, corrections or counterexamples were attributable to the specialist rather than the primary implementer;
- Whether the parallel work changed the scientific outcome, reduced uncertainty or saved material investigation effort;
- Cases where the specialist added little value, without manufacturing a contribution.

The reviewer must remain independent of the implementer's and specialist's claims. If both specialist and reviewer run concurrently, the two-sub-agent limit still applies. Do **not** turn this into an elaborate agent-effectiveness experiment or delay the science to evaluate staffing.

## 7. Handoff standard

Return a decision-ready recommendation: either a precise, qualified future integrated observer/live-test scenario or a definitive supported reason to prioritize another native oracle. Explicitly separate manual gameplay reports, directly captured native values, static native execution semantics, saved-state associations and inference. Report limitations by scope and confidence, not as a pretext for premature completion.

**Do not implement or launch the next observer under this authorization.**
