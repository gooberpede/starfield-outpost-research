# D5V active investigation ledger

2026-10-30, Australia/Sydney. The maintainer invoked the
[original brief](../../implementation-briefs/CODEX_BRIEF_SOR_RG2_D5V_resource_population_stability_consumption_native_coordinates.md)
in chat. D5V-AC1–AC11 and the original generality of D5V-Q1–Q4 are frozen;
there are no approved amendments. This is an active checkpoint, not completion.

## Frozen controlling questions

- **D5V-Q1 — Population lifecycle:** When is construction executed, when is a previously constructed population reused, and which specific lifecycle operations can invalidate it or require regeneration during common arrival, departure, streaming, loading and Workshop activity?
- **D5V-Q2 — Gameplay consumption:** By what actual native data and control paths do generated resource regions become resource queries, outpost resource availability and extractor/Workshop decisions? Can a changed gameplay observation arise without a changed generated population, as a matter of native semantics? Do not assert that it does occur without evidence.
- **D5V-Q3 — Stability mechanisms:** Under documented ordinary action/state contracts, what determines stability of the player-visible population, including any constraints on query-winner selection, caching, lifetime, persisted state, or consumer behaviour? Distinguish guaranteed invariance, conditional stability, and possibilities that require unobserved timing.
- **D5V-Q4 — Native spatial provenance and visualization:** Establish and document the native coordinate domains, transforms and ownership of the geometry, outpost centre/beacon, 150-native-unit build radius, source frames, Workshop queries and consumer outputs. Produce scientifically traceable visual comparisons using the actual native coordinate systems.

## Initial checkpoint

Read the brief, standing orders, workflow, charter, evidence/completion/editorial
standards, reviewer instructions, save policy, current research-state opening,
D5Q dataflow and D5U-C1 coordinate work. Initial Git status contains only the
supplied untracked brief. No task-authored changes predate this ledger.

| Branch | Questions | Current evidence and alternatives | Disposition / next action |
|---|---|---|---|
| V01 Identity and authority | All | Prior pins are leads, not current verification. | OPEN: hash installed executable, definitions and existing analysis identity; preserve HEAD/index. |
| V02 Construction and lifetime | Q1,Q3 | D5Q distinguishes visited bypass, map hit/miss, wrapper and successful geometry. D5C/D5R contain lifetime leads. | OPEN: inspect original native windows and callers for clear/reset/retirement/manager changes. |
| V03 Consumers | Q2,Q3 | D5Q identifies resident scan `0x1421e07d0` and callback `0x1421e0f50`; this alone does not close dataflow. | OPEN: trace native spatial predicates, aggregation and extractor consumers. |
| V04 Coordinates | Q4 | C1 independently joins saved descriptor-frame centres; fixed research disk is explicitly not recovered saved hardware boundary. | OPEN: verify native radius and consumer frame contract before plotting. |
| V05 Ordinary stability | Q1,Q3 | D5S/T/U establish conditional alternatives, not observed population changes or bug causes. | OPEN: compose generation, ownership, ordering and consumer contracts; challenge persisted-state alternatives. |
| V06 Conditional save examination | Q3,AC8 | No indispensable missing serialized input identified yet. | NOT TRIGGERED: revisit only on a specific supported serialized producer. |
| V07 Independent review | All, AC10 | Brief requires separate scientific, engineering and editorial reviewers. | OPEN: provide original contract, primary windows and exact final snapshots to reviewers. |

## Experiment boundary

Read existing repository, installed binary/data and controlled historical
evidence; export existing analysis without database edits. Task-owned scripts
may write authored derivatives and ignored scratch. Disposable offline native
execution requires a recorded input/output/risk/control boundary before running.
No installed game execution, process attachment, gameplay, configuration/plugin
changes, save writes, external communication, staging, commit, push or publication.
Check caller-available free space separately on C: and D: before material writes;
stop affected experiments below 40,000,000,000 bytes or on identity/integrity
failure. Preserve raw originals. Scientific, evidence, editorial and authority
outcomes remain separate. Every question is currently **INCOMPLETE**.

## Native follow-up and consumer experiment checkpoint

Fresh identity receipt `.local-work/d5v/initial.json` verifies all three installed
pins and 15 existing analysis pins. HEAD is `d05d909dc14257e803e7ac2f04859c2e4596acab`;
index SHA-256 is `65aa1e62edcc1b0dd773ce7342d9fe6c40227bdb17f20160880ac0c701bc237b`.
Both caller-available free-space readings exceed 40,000,000,000 bytes.
Fresh read-only exports are under `.local-work/d5v/export01` and `export02`.
The latter completed, but its Python reader incorrectly used Windows cp1252;
`split.py` recovered the unchanged UTF-8 export. The failed reader is preserved.

Scientific interim review identifies two required leads: source retirement does
not clear visited state; and extractor placement calls a different query than
the area updater. These remain OPEN. Source construction `0x140982d90` sets
`S+0x68` from definition/geographic hashing plus filename hashing through
`0x1427d7580`, rather than a monotonically increasing allocation epoch.
Trace module reset callbacks before interpreting return-to-area regeneration.
Placement `0x140f3f9a0` calls `0x140f7c290`, which queries `0x14079df70` at the
candidate reference position and intersects results with produced resources.
The atmosphere branch and catalogue filters remain separate.

**Authorized disposable experiment:** execute the original area callback
`0x1421e0f50` and its arithmetic helpers only in a new offline Python process.
Read the pinned PE and existing analysis exports, supplied C1 geometry and
explicit synthetic controls. Supply fixture IRES resolution, successful temporary
quad allocation/free and one preallocated resource-set slot. Preserve original
predicate and insertion instructions. Compare native accepted-set membership
with the existing owned spatial transcription; vary query/translation/radius/
height while holding region bytes fixed. Outputs are ignored exact receipts;
authored aggregate results may enter the task report. Risks are fixture-process
faults or allocation pressure, not target intervention. Stop on native fault,
identity mismatch, malformed geometry or either free-space floor failure.
No exception suppression, live attachment, installed patch, save or database
write is permitted. Cleanup is ordinary fixture-process exit; retain evidence.

## Mechanism and validation checkpoint

Nine completed fresh read-only exports follow the material lifecycle, consumer,
coordinate and produced-property branches. `d5v-sources.csv` records their exact
hashes and function line windows. All exports retain their original bytes.
The final native fixture extends the declared experiment to the actual point
predicate `0x142346b30` and its original math helpers; the existing installed CRT
supplies its imported `atan2f`. It runs in the same disposable offline boundary.
No game process or installed code is patched; fixture-only resolution/allocation
substitutions are documented in the method.

Interim independent scientific and engineering reviews returned REWORK checkpoints.
Engineering identified missing 3D-edge and narrowphase controls and dependency
hashes. `native02` adds those controls; `native03/04` add the point path and explicit
area-versus-point discriminator; `native05` adds 605 positive first-point and
changed-Z pairs. Final receipts retain 606 area comparisons, 606 centre/control
point evaluations and those additional point controls. Earlier receipts remain
preserved. The first 599-case result was never treated as full predicate coverage.

| Branch | Checked paths and decisive result | Disposition / next action |
|---|---|---|
| V01 Identity/authority | Three installed pins and 15 analysis pins match; exports use isolated read-only/noanalysis state; definitions reread at exact ESM record offsets. | RESOLVED within offline scope; final preservation recheck remains. |
| V02 Construction/lifetime | D5Q/D5S primary paths plus fresh constructor module registration, manager reset, shift, retirement, Grid clear and destructor windows. | RESOLVED conditionally: broad reset clears both stores; retirement alone does not. No blanket regeneration or lifetime guarantee. |
| V03 Area/candidate/catalogue | Actual point leaf `0x142346b30`; produced selector `0x1409e8700 → 0x1409ea530 → 0x1409e8950`; original predicate executions; static catalogue/UI paths. | RESOLVED for requested consumer distinctions; no placement collision/production-rate claim. |
| V04 Coordinates | Independent saved-frame/projection byte joins, native indexed translation, raw candidate operand copy, radius definition reread and exact SVG inverse/replay controls. | RESOLVED for plotted conditional historical domain; unobserved loaded/candidate frames not joined or plotted. |
| V05 Stability/action forks | Owner/component install `0x140789ce0`, world release `0x14078cf00`, loading drain/phase reset, shift slots, preserved D5S/T/U alternatives and Feynman area/point results. | RESOLVED as conditional contracts; frequency/history not inferred. |
| V06 Save gate | No indispensable missing input with an evidenced serialized producer required for the mechanism contracts. Existing authored saved-centre derivatives suffice. | NOT TRIGGERED; no raw-save access. Geometry serialization remains a separately bounded unknown, not a whole-save absence claim. |
| V07 Reviews/delivery | Reports, source/consumer tables, four SVGs and reversible numerical controls are prepared. | OPEN: exact-snapshot scientific, engineering and editorial review and final packaging. |

Primary comparison data hold region geometry fixed and execute different native
consumers. Equal area resource sets under the two U25 alternatives contradict
the hypothesis that different generated populations necessarily change outpost
resource identities. Area-versus-point controls contradict equating an area list
with admission at the candidate point. Visited survival contradicts treating
source-pointer retirement alone as proof of a fresh generator call.
None of these counterexamples diagnoses the operator's reported bug.

All four scientific question answers are proposed COMPLETE under their original
conditional mechanism generality; independent review remains mandatory. No
terminal blocker or live request is proposed. Remaining historical epoch,
frequency, effective override and exceptional-frame unknowns are explicitly
outside the plotted/model claims, not secretly answered by fixture execution.

## Review closure checkpoint

Independent scientific/completeness, engineering/evidence and editorial reviewers
each returned ACCEPT for review01. Their complete returns are retained locally
as `scientific-review01.md`, `engineering-review01.md` and `editorial-review01.md`
under `.local-work/d5v/`. The scientific reviewer found Q1–Q4 COMPLETE at the
frozen conditional-mechanism generality and no remaining material omitted
authorized lead. The engineering reviewer independently checked receipt/patch
contents and centre arithmetic; it did not rerun native experiments. Editorial
review covered all 23 task-authored files and four rendered previews.

Final preservation verified all three installed inputs, 15 analysis pins and
166 source rows, with both drives above the required floor and unchanged
HEAD/index. `.local-work/d5v/postflight.json` and `excluded-inventory.json`
retain actual checks and the 405 task-local excluded files present at that
inventory checkpoint. Native evidence stays local. V01 and V07 are RESOLVED
subject to the final package's narrow closure review; no scientific branch is
left open or terminally blocked. Full final outcomes and patch paths are in
[the review record](d5v-review.md). No next experiment is started.

## Maintainer correction — native plotted axes

The invoked [D5V-C1 brief](../../implementation-briefs/CODEX_BRIEF_SOR_RG2_D5V_C1_native_coordinate_plot_correction.md)
reopens AC6/AC7 presentation only. Prior reviewer acceptance of a reversible
relative grid did not satisfy the requested native descriptor-frame axes.
[The active correction ledger](d5v-c1-report.md) freezes C1-Q1/AC1–AC9 and records
the corrected renderer, unchanged scientific fields and independent visual review.
Earlier ledger/review statements remain historical; the C1 record controls the
current presentation disposition. No native-consumer or lifecycle finding changes.
