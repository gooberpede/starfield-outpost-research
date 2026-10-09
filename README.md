# Starfield Outpost Systems Research

**Latest scoped result — SOR-EXP-0012 / SOR-EV-0018, 2026-10-09:** [capacity and planetary location](docs/experiments/save-capacity-and-planetary-location.md) validates all three formerly size-excluded saves through bounded disk-backed decoding. Beacon parents resolve to Kreet in S1/S1C/L2C; all 17 mature clear body/system associations match the manual JSON under disclosed correspondence. Separate double pairs are provisional surface anchors, not validated latitude/longitude. STRONG body interpretation proposed pending review; historical classifications and earlier findings retained. No live work, staging, commit, push or publication.

**Latest scoped result, 2026-10-09:** [ordinary beacon detection](docs/experiments/ordinary-outpost-beacon-detection.md) reproduces zero/one controls and Save52's 19 ordinary candidates split 17 disabled-clear/two disabled-set. All 17 clear records match the manual network; both set records fall outside it. Positive evidence is separate from unresolved authoritative ownership/completeness. Offline only; critical review pending, no staging/commit/push.

**Latest offline result, 2026-10-09:** [historical save inventory](docs/experiments/historical-save-inventory-triage.md) catalogs 278 saves across six first-header-version strata; 275 receive bounded fingerprints and three remain header-only at the 64 MiB limit. Ten mature absence candidates are provisional; no residual-state exclusion is claimed. Name-associated local XYZ candidates and body-name leads are recorded, without decoded planetary coordinates. Critical review pending; no live work, staging, commit or push.


**Latest offline result, 2026-10-08:** [mature-save validation](docs/experiments/mature-save-outpost-validation.md) independently consumes the bounded reference/relationship grammar and reconstructs 24 reciprocal cargo connections before JSON comparison. All 17 names and per-outpost pad types/counts agree; 53 associated pads are a subset of 61 marker windows. Small-corpus counterexamples block a universal active-index interpretation. Semantic promotions await critical review; no live work, staging, commit or push.

**Latest offline result, 2026-10-08:** [structural containment](docs/experiments/outpost-save-structural-containment.md) maps known outpost anchors to separate directory-backed relationship/object/string regions. A counted shared string collection and remappable beacon name/animation indices are observed; complete object record bounds and stable runtime identity remain unresolved. Model C is the best-supported structural interpretation, pending review. 22 labels / 21 unique archived saves verified; no live work, commit or push.

**Latest offline result, 2026-10-07:** [L0–L2C output-link validation](docs/experiments/output-link-validation-L0-L2C.md) observes reversible endpoint-pair removal/recreation with all four object candidates retained. The original literal fails across reload; token remapping and entry reordering explain structural correspondence. Semantic promotion to STRONG is proposed for critical review, not automatically applied. Six new saves verified, historical S4C archive reused; no live work, commit or push.

**New offline result, 2026-10-07:** [manual S0–S7C save-corpus analysis](docs/experiments/manual-save-corpus-S0-S7C.md) archives and verifies 17 saves, recovers the rename anchor and candidate object/link/movement/deletion lifecycles, and flags Kreet/Narion/location uncertainty. First pass complete; critical review pending. Raw data stays local. No commit/push; proposed next experiments are not authorized by this result. Earlier “next active task” wording below predates this pass.

**Current direction — SOR-D-0021:** native save automation is optional/unresolved, not a project dependency. Manual differential saves and live outpost observation are primary supported paths. The [final one-shot software-breakpoint attempt](docs/implementation-briefs/EXP0002A-final-software-attempt.md) ended with zero request captures: **DEFERRED_NO_MATERIAL_ADVANCE**. This phase of native-save investigation is closed/deferred. No further S1.5, backend or hardware retry for EXP-0002A native-save instrumentation. The next active project task is [resumed beacon research](docs/experiments/EXP0002-manual-beacon-resumption.md) using manual checkpoints. Native-save revisits require a specific new reason from central outpost evidence and separate review. Stage C is not authorized. No commit/push.

The dated EXP0002A holds/results below are preserved history; they do not block the overall outpost programme.

**Historical S1/S2 controls:** S0 no-debugger manual save passed and is archived; S1 debugger-without-DR0 save passed and is archived. S2 armed only the reviewed game-window thread, then the game exited after one click with no REQUEST_ENTRY evidence. A remaining pre-exit-notification cleanup defect is recorded; both processes are gone and sync completed. Crash dumps are secured locally. No widening/rerun or Stage C. The entire 0.1.2 evidence remains unchanged. [Full 0.1.3 audit](docs/audits/exp0002a-adapter-0.1.3.md).


**Historical result — adapter 0.1.2:** the authorized Stage-B attempt reached ARMED on 92 existing threads. The operator clicked New Save once, then Starfield exited before any REQUEST_ENTRY capture. Evidence is incomplete; the controller exit-event recovery defect is recorded separately. Both processes are gone, the user reports Steam sync finished, and protected Save3 hashes remain unchanged. No retry or substantive adapter fix before review. Stage C remains blocked. [Live audit](docs/audits/exp0002a-adapter-0.1.2.md).

**Repository:** `starfield-outpost-research`

**Historical review hold:** [EXP0002A adapter0.1.1 qualification](docs/audits/exp0002a-adapter-0.1.1.md) passed the focused fixed-population capture, unarmed-new-thread NO_HIT and capture-first destructive-recovery controls. The0.1.0 dynamic-new-thread retirement failure is preserved. Stage B remains ordinary Steam without SFSE; Starfield mode stays disabled pending review. No deployment or game launch. Static mapping is preserved; Stage C remains blocked.

**Current stage:** EXP-0002A native-save investigation is [deferred](docs/audits/exp0002a-final-software-attempt.md). EXP0002 outpost/beacon research is ready to resume using [manual controlled saves](docs/experiments/EXP0002-manual-beacon-resumption.md); native-save automation is not a prerequisite.

**Historical pre-pivot stage:** [SOR-EXP-0002A](docs/experiments/SOR-EXP-0002A-native-save-thread-mapping.md) mapped static manual-save candidates, but bounded debugger setup attempts acquired no manual-save trace. User exited normally; protected parents unchanged; incidental exit save archived without deletion. No native-save prototype or safe query thread established. EXP0002 was paused after [review14 A0/A0C](docs/experiments/EXP0002-review14-run.md), before construction/native queries. Review required; no commit/push.

**Development:** Private initially; completed, reviewed research must be published.

**Licence:** `GPL-3.0-or-later` for project-authored material within the rights boundary in [LICENSING.md](LICENSING.md).

> How does Starfield represent, operate, and persist player outposts, and how do those mechanisms interact throughout an outpost's lifecycle?

Runtime behaviour and save-file representation are equally important research subjects. A runtime finding is valuable even before its saved representation is understood; a persistence finding is valuable even while some runtime consequences remain open. Follow a bounded question between game definitions, scripts, static analysis, live observation, and saved data as the evidence requires.

Organize findings by outpost subsystem, not into disconnected runtime and save specifications. Explain which state is persisted, inherited, reconstructed, derived, transient, or still unclassified. Do not assume that any proposed field, relationship, or simulation mechanism exists until demonstrated.

## Start here

1. Read [AGENTS.md](AGENTS.md), [WORKFLOW.md](WORKFLOW.md), and [THIRD_PARTY_POLICY.md](THIRD_PARTY_POLICY.md).
2. Read the [charter](docs/CHARTER.md) and [current research state](docs/RESEARCH_STATE.md).
3. Use the [documentation index](docs/README.md) for records and templates.
4. Follow [WORKFLOW.md](WORKFLOW.md) for review/integration rules. The scaffold referenced `docs/GIT_SETUP.md`, but that file is absent from this checkout; no synchronization action is implied.

The [initial reconnaissance brief](docs/implementation-briefs/CODEX_RESEARCH_BRIEF_initial_outpost_system_reconnaissance.md) and [report](docs/experiments/initial-outpost-system-reconnaissance.md) are retained. Future briefs belong in [docs/implementation-briefs/](docs/implementation-briefs/README.md).

## Research boundary

The deliverable is a verified account of the outpost system, supported by reproducible evidence and validation within an agreed scope/build matrix. The initial brief authorized small xEdit/Ghidra readers; no save parser, runtime exporter, observer plugin, new dependencies, or build/CI setup was introduced.

The sequence remains **complete and validate the agreed research scope -> publish the research -> decide how to consume it**. An `Import from Save` feature in Starfield Outpost Network, a generic dump tool, and future mods are downstream possibilities, not current implementation commitments. Do not impose their data models on the research.

## Layout

```text
.
|-- AGENTS.md / WORKFLOW.md
|-- THIRD_PARTY_POLICY.md / THIRD_PARTY_NOTICES.md / CREDITS.md
|-- LICENSE / LICENSING.md
|-- .gitignore / .gitattributes / .editorconfig
|-- docs/
|   |-- CHARTER.md / RESEARCH_STATE.md / DECISIONS.md
|   |-- PROVENANCE.md / EVIDENCE_STANDARD.md
|   |-- SOURCES.md / PERMISSIONS.md / PUBLICATION.md / GIT_SETUP.md
|   |-- known-facts.md / hypotheses.md / function-register.md / state-register.md
|   |-- subsystems/        # Shared runtime/persistence research map
|   |-- experiments/
|   |   `-- evidence/      # Only explicitly reviewed, selected evidence
|   |-- templates/        # Experiment, finding, source, permission, evidence bundle
|   |-- audits/
|   `-- implementation-briefs/
|-- ghidra/scripts/        # Future project-authored static-analysis scripts
|-- debugger/scripts/      # Future project-authored debugger automation
|-- runtime/               # Reserved for explicitly authorized runtime research
|-- save-analysis/scripts/ # Future project-authored offline analysis
`-- exports/               # Generated work ignored except its README
```

Use an external workspace or ignored `.local-work/` for saves, raw/decompressed data, dumps, analysis databases, unreviewed exports, and private permission correspondence. Do not upload them merely because the repository is private. The static baseline was independently checked here; no sibling baseline was adopted without verification.

## Licence and third-party conduct

No fork or pull request without prior discussion and explicit user approval. No third-party code reuse without documented rights-holder permission and explicit user authorization of the specific use. Give explicit credit for all substantive work used, including research and tools, whether or not legally required. Honour licences in letter and spirit.

These are internal project operating rules, not additional restrictions on recipients exercising GPL rights. See [the detailed policy](THIRD_PARTY_POLICY.md), [credits](CREDITS.md), and [publication gate](docs/PUBLICATION.md).
