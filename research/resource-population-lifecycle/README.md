# D5C offline verification helpers

[Research result and boundaries](../../docs/experiments/resource-population-lifecycle/report.md).
Prerequisites: installed CPython 3.14, Git, existing local input inventories and
the explicitly invoked offline D5C brief. Python stdlib and project-owned methods
only; no downloads or new dependency incorporation. All receipt output is exclusive
and ignored under `.local-work/resource-population-lifecycle/`. Original inputs
are never overwritten. Run commands from the repository root.

- `audit.py before|after` reads the inherited D5B evidence/Phase A inventories,
  all existing D5B artifacts, prior recon exports, protected saves/backups,
  installed inputs and HEAD/index. It requires game absence and both-drive free
  space of at least 40,000,000,000 bytes. The before run verifies historical
  expected hashes before recording a new inventory; after compares the exact
  before set. It calls the unchanged D4A protected-save policy, including its
  qualified transient exclusions. It writes audit/protection/time receipts only.
- `checks.py [--label checks02]` verifies source pins, historical register
  crosschecks, build/address domains, new export completion/error status, frozen
  alternatives and the ten-control historical result ledger. This checks
  integrity and transcription, not geometry by regeneration or native semantics.
- `package.py --label review01` adapts the owned D5B live exporter. It reads the
  actual tracked/untracked text and baseline, writes exact complete/task-only
  patches, separate manifests, status, exclusions and check receipts, and applies
  both directions only in disposable `.local-work/review-patches/` trees. It
  imports the unchanged session exporter with parent Git discovery stopped at
  `.local-work/`. It does not stage files or write repository refs/index.

The existing `research/workshop-population/export.ps1` and `ReadSpecialist.java`
export existing functions/xrefs/table entries under `-readOnly -noanalysis`.
Exact selectors and tool/source hashes are in local `commands.json`, the three
`d5c-*` logs and the [source ledger](../../docs/experiments/resource-population-lifecycle/sources.csv).
They write fresh local TSV/logs and tool cache/settings; no code, symbol, type or
comment changes are requested. The complete 15-file analysis-project inventory
is independently hashed before and after those exports. A read-only tool can
still affect transient cache/sidecar metadata; byte equality is checked, not
assumed from the command-line flag.

The helpers do not launch/attach a target, load saves, regenerate resources,
change game/configuration/save/analysis content, contact a service or publish
anything. Checksums establish bytes, not lawful redistribution or semantic truth.
The report and independent primary-evidence review supply scientific assessment.
