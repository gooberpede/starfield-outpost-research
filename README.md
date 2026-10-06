# Starfield Outpost Systems Research

**Repository:** `starfield-outpost-research`

**Stage:** Initial static reconnaissance executed; critical review pending. No live/save experiment executed.

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
