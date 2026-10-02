# Provenance and Environment Baseline

## Scaffold provenance

Prepared on **2026-10-01** at the user's request, using the supplied reference-handle scaffold as an organizational reference and the agreed broader outpost-systems remit.

| Input / material | Provenance |
|---|---|
| Reference archive | `starfield-reference-handles-scaffold(1).zip`, supplied by the user |
| Reference archive SHA-256 | `9999f2efb4a0f7c0ca6011c3c9317777dc347ac850e0bee972e3b9909637031f` |
| Applied contribution | Directory pattern; durable research/agent records; local-only analysis artifacts |
| Not adopted | Reference-handle findings/hypotheses, executable/tool hashes and versions, machine paths, debugger success claims |
| Earlier save-only brief | Superseded by the runtime-and-persistence scope and direct-scaffold request; not an active repository brief |
| Included `LICENSE` | Verbatim `/usr/share/common-licenses/GPL-3` from the preparation environment; 35,149 bytes, 674 lines |
| `LICENSE` SHA-256 | `3972dc9744f6499f0f9b2dbf76696f2ae7ad8af9b23dde66d6af86c9dfb36986` |

The licence file is the complete GNU GPL version 3 text, carrying the Free Software Foundation's notice. Its title, permission notice, sections, and version-choice meaning were checked against the [SPDX entry](https://spdx.org/licenses/GPL-3.0-or-later.html). Direct GNU retrieval failed during preparation; do not claim those bytes were freshly downloaded from GNU. See [LICENSING.md](../LICENSING.md) and source `SOR-S-0002`.

Read-only GitHub checks during preparation identified `gooberpede/starfield-outpost-research`, private visibility, `main` as default branch, and no branches. This is a setup observation, not a guarantee of future state. No remote changes were made.

## Experimental baseline: not yet established

Do not fill these fields from the example project. Use a new `SOR-ENV-` record when the actual environment is inspected. `UNKNOWN` is deliberate, not an invitation to guess.

| Field | Current value |
|---|---|
| Game edition/distribution | UNKNOWN |
| Executable product/file version, size, SHA-256 | UNKNOWN |
| Installed/working-copy equality | NOT CHECKED |
| Save format/container versions | UNKNOWN |
| DLC, plugins, load order, mod-manager profile | UNKNOWN |
| Operating system / architecture | UNKNOWN |
| Ghidra version, analysis options, language/compiler ID | UNKNOWN |
| Actual static image base / executable module | UNKNOWN |
| Debugger/backend versions and attach qualification | UNKNOWN |
| Python or other analysis runtime | NOT SELECTED |
| SFSE/native instrumentation/version/hashes | NOT SELECTED |
| Save samples and independent ground truth | NOT REGISTERED |

Record exact paths locally where needed. In durable/public records use portable placeholders such as `<starfield_executable_path>`, `<analysis_project_path>`, `<local_evidence_root>`, and `<sample_path>`. The user-requested workstation path is intentionally included in [GIT_SETUP.md](GIT_SETUP.md) only as an operational setup instruction.

## Baseline and sample records

For each baseline record observation time/timezone, observer, executable/module names and hashes, versions, distribution, load order, tool/script versions or commits, analysis options, read/write effects, source/permission IDs, and uncertainties. Distinguish reported values from independently read/hashed ones.

For each `SOR-SAMPLE-` record the original byte hash and size, origin and owner consent, game/build/save versions, plugin set, controlled actions, parent/control sample, time/loading conditions, local locator, and publication classification. Raw save filenames can reveal personal information; prefer neutral sample IDs in Git.

Keep immutable originals local. For decompression, normalization, redaction, or extraction, record each transformation and input/output hashes separately. Cross-link [experiments](experiments/README.md), [evidence](experiments/evidence/README.md), and [the evidence standard](EVIDENCE_STANDARD.md).
