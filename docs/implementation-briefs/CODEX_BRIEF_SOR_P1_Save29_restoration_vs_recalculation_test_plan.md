# Codex research brief — P1 Save29 validation and decisive mechanism test plan

**Project:** `D:\Projects\starfield-outpost-research`  
**Task:** Record completed player test; design a discriminating follow-up (planning only)  
**Authority:** Documentation and bounded read-only analysis. Do not launch Starfield, modify or generate saves, install/inject instrumentation, stage, commit or push. The prior P1 package has now been committed and synced.

## 1. Context and established conclusion

Record the **user's actual completed live test** as a positive, bounded result; do not retrospectively raise its acceptance threshold.

- Baseline: Kreet Save3; new manual **Save29**: `Save29_D6036588M417474696C61204B6972616C79_000216_20261017043132_3_0_4.sfs`, under `Documents/My Games/Starfield/Saves/`.
- One solar array supplies **6 power**; two small Iron extractors demand **5 each** (**10 total**, deficit **4**). UI reports the deficit.
- The foreground extractor in the second user screenshot is **#1**, with normal/non-red operating-cost display; the other, shown with red operating-cost display in the first screenshot, is **#2**.
- Before the trials: **#1 powered, #2 unpowered**. Three separate runs, each exiting Starfield to desktop before loading the **same Save29**, yielded **#1 powered and #2 unpowered**. The user inspected each extractor immediately after loading, waited several seconds, and inspected again; no differences were reported.
- **Disposition for the agreed empirical question: PASS — repeated-load allocation is consistent in this controlled configuration.** It is settled for project purposes. This is not a claim that every possible outpost has been exhaustively tested, and that disclaimer should not displace or undermine the accepted finding.

The screenshots were supplied in the conversation, not necessarily present in Codex's workspace. Do not claim to have independently inspected them unless provided. Confirm the actual Save29 file and checksum only if available locally, read-only; distinguish user-reported observations from independently examined save bytes. Never alter original Save3 or Save29. Save29 should be backed-up and hashed as evidence.

## 2. Remaining causal alternatives

The accepted repeatability result does **not** distinguish the mechanisms that yield it. Design a plan capable of proving or falsifying, under specified assumptions, these two primary alternatives:

- **R — Saved-state restoration governs the settled outcome:** power bits persisted in Save29 are restored and survive to the observed settled state without an allocation computation superseding them.
- **C — Load-time recomputation governs the settled outcome:** saved bits may be restored temporarily, but load/activation callbacks recompute the powered set, and that computed set supersedes saved bits before the observed settled state.

Do not force a false dichotomy. A **hybrid/conditional** model (different outcomes for different attach paths, delayed updates, or selective consumers), and cases where R and C produce the same outputs, must be described. A callback's mere reachability does not prove it actually overwrote the two extractor states on these three loads.

**Goal:** Return a practical, scientifically discriminating **test plan**, not another broad native-mapping exercise and not another test whose identical outcome is compatible with both explanations. Prefer a plan that can decisively settle R versus C for this Save29 setup; if this is impossible with allowable observations, identify the exact obstacle and the least invasive additional evidence needed. Do not promise an unconditional proof that the tools cannot deliver.

## 3. Design requirements

1. Review `WORKFLOW.md`, `AGENTS.md`, `docs/experiments/power/` (`report.md`, `saved.md`, `native.md`, `followup.md`, `load-determinism.md`, `review.md`, and any relevant registers), plus existing experimental/provenance standards. Use actual pinned forms/fields and established reader utilities rather than guessing values.
2. **First decide if Save29 is actually discriminating.** From a read-only Save29 inspection (if available), establish saved `ExtraFlags` powered-mask values for both identified extractors and relate those to the observed live #1/#2 states. If the specific references cannot be identified unambiguously, state exactly what mapping evidence is missing. A saved/loaded match *alone* does not distinguish R and C.
3. Investigate minimal controlled intervention(s) that could **make restoration and recomputation predict different outcomes**. Examples to assess, **not preapproved actions**: a legitimately generated contrasting save with allocation reversed; a reversible, in-game power-network change before save/load; a controlled load-triggered refresh after a saved state is observed; or a *protected-copy-only* saved-state perturbation if it is scientifically necessary and can be separately authorized and validated. Do not assume a reversible gameplay change actually controls the saved flags independently of the graph. State how to keep generator output, demand, graph, fuel and identity fixed where needed.
4. If R/C predictions still coincide, propose a **temporal read-only observation** that captures restored bits **before** any recalculation, identifies actual allocation callback/writer execution, and compares bits **after** the final effective update. Evaluate whether an already-qualified getter/observer can supply this; otherwise specify minimum additional instrumentation and separate review/safety prerequisites. Ordinary UI may only show the final state: do not claim it sees pre-recalculation memory.
5. For each proposed experiment give: **setup; saved baseline and protected copy rules; intentional variable changed; controls; observations including reference identity, time/settling criterion, and game restart protocol; mutually contrasting R/C predictions; what would falsify each hypothesis; potential confounders; stopping rule; risk/approval boundary.** Explain what negative or matching outcomes would leave unresolved. Distinguish testing **whether** recalculation writes final bits from explaining **why** a particular root/ordering was chosen.
6. Rank the experiments by **ability to discriminate**, practical effort, and invasiveness. Supply one recommended smallest decisive protocol suitable for the player to execute, and a clear escalation path **only if** that protocol is inconclusive. Avoid redundant reload repetitions of the unchanged Save29 unless needed as controls.
7. Where feasible, trace only narrowly necessary native/save writers to determine whether a proposed intervention truly separates R and C. Cite build pin, RVA/field, prior evidence, and what the new examination contributes. No unconstrained instrumentation or cross-subsystem research.

## 4. Reporting and deliverables

Create a concise durable planning report alongside the P1 documents, with the following **at the top**:

| Item | Required response |
|---|---|
| Agreed Save29 test | **PASS**, with the observations and scope stated plainly |
| R vs C | What is known; what is still observationally equivalent |
| Recommended decisive next experiment | Actionable one-paragraph summary |
| Predicted outcomes | A table showing what result supports/falsifies R, C, or neither |
| Permissions | What may be performed by the user now, and what requires a new approved brief |

Then include the detailed test matrix, technical basis, failure modes and an explicit **ex ante acceptance criterion**: define what outcome counts as a decisive answer or falsification *before* testing, and do not alter that criterion after results arrive. If no viable experiment can deliver a definite discrimination, say so explicitly and recommend the closest test with precisely bounded inferential value.

Update the P1 research state/uncertainty/backlog or experiment log minimally to record the accepted Save29 live result and link the proposed tests. Preserve distinctions between user-observed UI evidence and independently instrumented internal state. Preserve previous reviewed findings; make no unapproved correction by implication.

Use established independent review/audit and patch packaging conventions: reviewer checks discriminating predictions, controls, ex ante acceptance, user-evidence provenance, and action limits; provide task-only and complete diffs as warranted, forward/reverse reconstruction checks, protected-input integrity checks, and a Conventional Commit subject. Do not claim to have run unavailable live tests or verified unavailable screenshots. Do not stage, commit or push.

**Success criterion:** We obtain a trustworthy durable record that the originally agreed repeated-load test **passed**, and a genuinely falsifiable, pre-registered strategy to distinguish whether **saved powered state** or **load-time recomputation** controls the settled result—without moving the goalposts or overstating what the proposed observations can prove.
