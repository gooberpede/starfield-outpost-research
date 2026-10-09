# Agent Standing Orders

These orders apply to all agents working on this repository. Narrower instructions may tighten them. A conflict or proposed exception must be raised explicitly; do not silently weaken a standing rule.

## Required reading

Before substantive work read [README.md](README.md), [WORKFLOW.md](WORKFLOW.md), [THIRD_PARTY_POLICY.md](THIRD_PARTY_POLICY.md), [the charter](docs/CHARTER.md), [research state](docs/RESEARCH_STATE.md), [evidence standard](docs/EVIDENCE_STANDARD.md), the active authorized brief, and relevant subsystem/source/evidence records.

## Purpose and scope

Research the live outpost system and its persistence as connected, equally valuable subjects. Follow bounded questions across static data, scripts, native code, runtime observations, and save files. Keep findings organized by subsystem. Do not start a tracker importer, production dump tool, or gameplay mod without a separate decision and brief.

The scaffold establishes documentation only. No game build, tool version, executable hash, address, save format, native structure, or community claim is a verified baseline merely because it appeared in another project or an earlier conversation.

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
