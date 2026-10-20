# Source and reproducibility closure

**Tracked readers and observer source exist, but fresh-checkout method closure
is incomplete for recent acquisition workflows.** Protected original evidence
can stay private; owned method source/configuration and useful synthetic
examples can be assessed separately for a selected publication scope.

The [source metadata inventory](source-inventory.csv) covers 510 tracked and
15,008 ignored source/configuration candidates at the initial scan. It includes
JSON and archived snapshots, so it is not 15,008 unique missing programs. The
baseline supplied brief is the only nonignored untracked file before RR1.
The [CSV pin inventory](source-pin-inventory.csv) checks 9,258 recognized path
occurrences: 593 tracked, 8,661 locally present only and four receipt-field
locators initially unresolved by literal filesystem lookup. Source-code paths
account for 545 tracked and 475 local-only occurrences, with repeated pins.

Those four apparent misses are `outpost-defense/sources.csv:105-108`,
`saved-HIST-....json:source` locators. The suffix names a JSON source field,
not a physical filename. They require container/field resolution, not an
assertion that four essential files were lost. The local follow-up receipt
records container existence. CSV values not shaped like full repository or
Windows paths (for example short numbered export names) are not covered by
this path resolver; their enclosing report defines the namespace.

Selected source/image hash comparisons also find **26 historical-pin mismatch
occurrences at 23 literal path strings** (some absolute/relative aliases name
the same file). Exact declared/current hashes are in the pin CSV and local
`pin-mismatches.json`. Examples are build-budget sources rows 3/94 (local
packagers), exact-beacon changed-files row 21 (OutpostRecon.java), and resource
availability sources rows 143/153 (packager and resource_availability.py).
These differ from the RR1 starting snapshot, whose hashes remain unchanged:
they are historical references to earlier source versions, not demonstrated
RR1 damage. The housekeeping brief explicitly changed maintained exporters
while preserving frozen receipts. Do not repin history to today's bytes.
For B3, resolve each selected claim to its historical Git/source snapshot or
an independently qualified current method; availability of an old hash is
not established solely by today's pathname existing. No claim that all 26
differences are housekeeping-only or semantically harmless is made.

## Tool families and required inputs

| Family / representative source | Classification / source availability | Reproduction prerequisites and practical limit |
|---|---|---|
| save-analysis/scripts readers, stream_save and tests | Maintained research source and synthetic framing fixtures tracked. | CPython stdlib, documented format/version gates, lawful input saves for actual evidence. Synthetic behavior can be retried without originals; saved semantics still need claim-specific controls. |
| research E1–E3, P1, cargo, crew and storage readers | Tracked bounded research helpers and some verifiers/tests; original evidence in ignored roots. | Installed ESM/PE/context and exact corpus receipts; many checks intentionally fail if the local pinned evidence is absent. A verifier is not an acquisition pipeline. |
| research/locations-outpost/verify.py and build-catalogue verifier | Tracked verification; acquisition and packaging source also named in local ledgers. | LO1 methods lists lo1-start/defs/controls/assets and E2ReadSession/Cr1Recon/TransitCalls local sources. No fresh clone supplies these merely by containing the verifier. |
| Coordinate sufficiency | Durable methods/inputs/numerical ledgers and reusable save/position readers tracked; orchestration cs-*.py and local worker scripts ignored. | `coordinate-sufficiency/evidence.md` Offline commands explicitly calls local helpers. Promote reviewed source or describe independently repeatable alternatives for the chosen claims. |
| runtime/exp0002 and native-oracle 010–080 families | Archival experimental observer/fixture/decoder/operator source and build scripts tracked in versioned families. | Windows MSVC/MASM/SDK, approved exact SFSE header, separately installed runtime/game, version/guard/protected-save checks. No rerun/deployment authority follows; compiled historical packages need not be published. |
| runtime/session-tools | Reusable orchestration/source/tests tracked, version-specific adapters retained. | Explicit approved run card, input hashes, phase-aware lifecycle and caller space checks; historical operational output remains private. Source testability does not establish observer safety in retail. |
| debugger families | Archival failed and qualified instrumentation source, tests and fixtures tracked. | Windows APIs/toolchain and controlled fixture setup; live game/debugger runs separately gated. Retain abandonment and failure reasons. |
| ghidra/scripts; xedit/*.pas | Tracked owned exporters; two installed Pascal copies match exactly. | Ghidra 12.1.2/Temurin 21.0.12 and xEdit 4.1.5p are historical cited tool versions. Existing analysis/import state affects exports; legally obtained binary/database recreation needed, not database distribution. |
| .local-work acquisition readers/worker helpers | Local-only method source; many are duplicated in frozen snapshots/review trees. | Select authoritative source version per claim before promotion. Review embedded constants/excerpts/lineage and build configuration; a `.py` extension alone does not make a file publishable. |
| JSON schemas/configuration/manifests | Mix of tracked reusable definitions, generated run locks and private pinned inputs. | Synthetic minimal configuration can be public after review; live paths/session nonces/save identifiers remain separate. Do not publish private run locks wholesale. |
| docs/experiments CSV/Markdown and selected evidence | Authored analysis, derived tables, small verification fixtures and selected exact evidence. | Public readers can understand many claims without raw inputs. Hash availability is not a semantic oracle or legal clearance. Rights and evidence availability must be mapped per claim. |
| .local-work packages/build directories; installed game/CK/SFSE/tools; Ghidra DB | Generated or proprietary/local-only artifacts, not maintained source merely because consumed by a test. | Keep outside Git. Release source/build recipe can exist without distributing binaries or copyrighted inputs. |

## Policy/configuration audit

`.gitignore` excludes local work, raw saves, executable/plugin/archive/game
formats, databases, dumps and build outputs; it deliberately does not blanket
ignore Markdown/CSV/JSON/evidence. A changed suffix or an ignore match is not
permission to publish. `.gitattributes` normalizes authored text while keeping
selected evidence exact-byte, with authored evidence READMEs excepted.

No workflow/CI path was introduced or run by RR1. Builds and project tests were
not executed: this task changes only audit documents, and rerunning historical
target-aware suites would not close an evidence or rights gap. Existing source
contains process/memory/configuration writes by design in instrumentation
tools; these are archival/experimental entrypoints, not safe generic public
quick-start commands. Machine-specific roots and dangerous writes need explicit
effects and preconditions in any future public reproduction guide.

## Closure proposal

For every claim selected by B0, record: readable current report; semantic scope
and actual independent review; exact method source version; build/configuration
inputs and permitted dependencies; lawful private-input acquisition route;
minimal synthetic example; decisive evidence tier and absent-original impact.
Use one of **method reproducible without original evidence**, **method requires
lawful external inputs**, **method source incomplete**, or **historical evidence
only**. Do not equate all local-only paths with defects or require reproducing
every abandoned experiment. Claim-specific closure, rather than wholesale
promotion of `.local-work`, is batch B3's proposed acceptance criterion.
