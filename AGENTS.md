# Agent Standing Orders

These orders apply to all agents working on this repository. Narrower instructions may tighten them. A conflict or proposed exception must be raised explicitly; do not silently weaken a standing rule.

## Required reading

Read [README.md](README.md), [WORKFLOW.md](WORKFLOW.md), [THIRD_PARTY_POLICY.md](THIRD_PARTY_POLICY.md), [the charter](docs/CHARTER.md), [research state](docs/RESEARCH_STATE.md), [evidence standard](docs/EVIDENCE_STANDARD.md), the active authorized brief, and relevant subsystem/source/evidence records.

For D5AL and future newly issued briefs, complete relevant required reading must
be recovered and understood by final substantive acceptance. Continue truncated
outputs, record coverage and its concrete influence on implementation and
safeguards, and have an independent reviewer verify applied understanding.
Prefer early reading; its chronological order is not a pass/fail criterion.
Missing critical content, material misunderstanding or unverifiable coverage
still fails AC01. The maintainer explicitly authorizes this prospective amendment
in [D5AL section 3](docs/implementation-briefs/README.md#archive-lookup) (`implementation-briefs.zip :: docs/implementation-briefs/CODEX_BRIEF_SOR_RG2_D5AL_episode_B_operational_adaptation.md`).
Earlier frozen contracts, reading-order breaches and verdicts remain unchanged.

For D5AT and future briefs, at most one sub-agent may be active at a time. An
authorized specialist and an independent reviewer may serve sequentially after
the preceding session is confirmed terminated. Disclose breaches with duration,
operations and effects. A minor promptly corrected breach without material
consequences does not automatically fail a criterion. Evaluate material effects
on evidence, independence, safety, authorization and budget. See [the D5AT
amendment](docs/implementation-briefs/README.md#archive-lookup) (`implementation-briefs.zip :: docs/implementation-briefs/CODEX_BRIEF_SOR_RG2_D5AT_Save52_outpost_mask_inventory_distribution_survey.md#1-authority-and-governance`).

## Purpose and scope

Research the live outpost system and its persistence as connected, equally valuable subjects. Follow bounded questions across static data, scripts, native code, runtime observations, and save files. Keep findings organized by subsystem. Do not start a tracker importer, production dump tool, or gameplay mod without a separate decision and brief.

The scaffold establishes documentation only. No game build, tool version, executable hash, address, save format, native structure, or community claim is a verified baseline merely because it appeared in another project or an earlier conversation.

**Research purpose and responsible reverse engineering.** This project is a
good-faith technical investigation into the operation and persistence of outpost
systems in Bethesda Game Studios' *Starfield*. Reverse engineering is used to
understand software behaviour, test hypotheses and develop reproducible research
methods. The project does not seek to circumvent copyright protections,
misappropriate proprietary material, introduce malware, compromise systems or
distribute modified game executables. Proprietary files remain subject to their
rights holders' restrictions, and native-code analysis or controlled execution
requires the project's explicit authorization and safeguards. This statement does
not override platform security controls or authorize otherwise restricted operations.

## Third-party work: mandatory gates

Maintainer-authored material in `gooberpede` repositories, including `starfield-reference-handles`, follows the standing [maintainer-owned exception](THIRD_PARTY_POLICY.md#maintainer-owned-material) (SOR-P-0002). Inspection, copying, adaptation, porting and reuse are authorized without another permission discussion; provenance remains mandatory, self-credit is optional. Third-party material inside those repositories is excluded and retains all gates below.

- **No fork without prior explicit discussion and scoped user approval.** No mirror or copied repository used to evade that gate.
- **No pull request, including a draft PR, without separate prior discussion and scoped user approval.** Investigation or fork permission is not PR permission. This also applies to PRs created in this project.
- **No reuse of third-party code without documented rights-holder permission and explicit user authorization of that exact use.** Cover snippets, ports, translations, tests, comments, binary templates, bindings, build scripts, vendored code, dependencies, and AI-assisted adaptations. Attribution alone is not permission.
- A licence may supply permission, but the agent must not unilaterally treat it as satisfying the user's approval requirement. Present its scope and obligations; record the user's acceptance of that basis or their requirement for separate author permission. Missing or ambiguous permission blocks the affected action.
- Do not strip notices, disguise provenance, or call source-informed adaptations clean-room work. Honour the licence in both letter and spirit. Do not use a dependency, build-time download, submodule, or tool-generated output to bypass review.
- Credit substantive research, discoveries, explanations, methods, data, and tools used, even when attribution is not required. Cite at the point of use and update [CREDITS.md](CREDITS.md) and [SOURCES.md](docs/SOURCES.md).
- No upstream contact, issues/comments, permission requests, evidence uploads, or other external disclosure without authorization. Read-only consultation is not permission to incorporate or distribute.
- Preserve origin and report unapproved material; do not silently delete provenance or rewrite history. Keep sensitive correspondence local. Follow [THIRD_PARTY_POLICY.md](THIRD_PARTY_POLICY.md).

These orders govern agents acting for the maintainer. They do not add conditions to the GPL licence or restrict downstream recipients. Do not modify the GPL text.

## Evidence discipline

Use [EVIDENCE_STANDARD.md](docs/EVIDENCE_STANDARD.md). Separate source reports, direct observations, interpretations, hypotheses, predictions, and validated findings. Preserve superseded interpretations and counterexamples. Do not treat a plausible output, passing integrity check, or an agent's summary as proof of semantics.

Apply its scoped-conclusion and answer-first reporting rules: distinguish confidence, coverage and claimed completeness; use the strongest supported scoped result while preserving review and authorization gates.

Record build/sample/tool provenance; stable record identifiers; exact supporting evidence; and the relevant address or offset domain. Runtime pointers, handles, FormIDs, serialized IDs, and file offsets are not interchangeable. Do not transfer an address or layout between builds without validation.

Track publication eligibility independently of scientific confidence. A runtime field is not automatically persisted. A saved value is not automatically authoritative after load. A discovered function or field is not automatically a safe mod integration point.

## Research completion

Follow the [completion protocol](docs/RESEARCH_EXECUTION_PROTOCOL.md#controlling-question-and-outcome-gate).
Keep the frozen controlling question visible, pursue material authorized
dependencies across subsystem boundaries, and maintain an active investigation
ledger. Report COMPLETE, BLOCKED or INCOMPLETE for each controlling question;
a bounded subtask or abandoned method leaves its parent question explicitly open.
Independent review must challenge unresolved branches against the original
contract. Accurate partial findings and polished deliverables cannot close an
unanswered mandatory question. Safety STOP and permission gates always prevail.

## Tooling and experimental safety

No game launch, debugger attachment, deployment, third-party tool execution, or save modification follows automatically from setup. Each experiment must state the allowed actions, inputs, outputs, risks, stop conditions, and cleanup.

Prefer observation-only analysis. Attaching, pausing, stepping, execution breakpoints, hooks, and injected observers may affect execution and must be disclosed. Do not call a hooked or breakpoint-based experiment non-invasive simply because it does not intentionally change gameplay.

Do not patch bytes, alter registers/memory, suppress exceptions, terminate the game, change game/plugin configuration, install instrumentation, or alter Ghidra symbols/types/comments under a read-only task. These require explicit authorization. Use controlled copies of saves; never overwrite an original or a user's active playthrough. Record instrumentation and loaded/unloaded/time-state conditions.

Read/export existing static-analysis state by default. Keep imported executables and analysis databases outside Git. Document every script's reads, writes, dependencies, prerequisites, and effect on the target or analysis project.

Future explicitly approved live captures may be intentionally crash-tolerant: a post-capture exit does not invalidate complete evidence already persisted. Evidence completeness, scientific result, and target survival are separate outcomes. This grants no live execution authority. The live brief must specify build/sample, breakpoint/hook/trace scope, expected information, finite bounds, any mutations, source-save protection, evidence flushing, and exit/recovery policy. Preserve protected saves; a pre-evidence crash is not success; disclose debugger-induced failures and stop on unexpected corruption outside the declared boundary. See decision `SOR-D-0008`.

## Repository and publication safety

Keep proprietary binaries/assets, raw saves, decompressed saves, memory dumps, analysis/debugger databases, credentials, and unreviewed bulk data local and untracked. A private remote is still a disclosure boundary. Ignore rules do not clear material or remove already tracked content.

No staging, commit, push, remote change, branch publication, release/tag, history rewrite, or visibility change unless explicitly requested for the current task. Do not touch unrelated local changes. No network-enabled CI, auto-update/download step, or automatic artifact upload is authorized by this scaffold.

Development starts private; completed research must be published under `GPL-3.0-or-later` after the agreed research scope and [publication gate](docs/PUBLICATION.md) are satisfied. Do not silently switch to GPLv3-only or add downstream permission requirements.

## Handoff

Implementation/audit briefs are downloadable Markdown files retained in the repository. Short corrections may be given in chat but must be durably recorded when adopted. Return a complete review package including new files, actual checks and their limits, remaining unknowns, changes to the evidence state, and any permission issues. Await critical review; do not treat your own completion summary as approval to integrate or expand scope.
