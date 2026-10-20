# Sources, controls, methods and limits

[Plan](plan.md), [sources](sources.csv), [review](review.md).

## Prior-work basis

| Prior record | Use here / retained limitation |
|---|---|
| [Workshop membership](../workshop-membership/report.md), [dependencies](../workshop-membership/dependencies.md) | Owner 054ba6, dummy 015804, DA grouping, replacement 191/foundation 192, construction versus generated-member distinction. |
| [Workshop population correction](../workshop-population/routes.md) | Extra 80 is quest/alias data; buffer override is not form type. Default/noninline/reverse reconstruction and ship counterexamples prevent an exhaustive population claim. |
| [L1](../limits/report.md), [L2](../build-budget/native.md), [L3](../spatial-placement/native.md) | Recipe admission, member accounting and spatial/collision/clearing are distinct from choosing a wall behavior entry. Their exact scopes and unknowns remain. |
| [DA1](../outpost-defense/integrity.md), [saved damage](../outpost-defense/persistence.md) | Health damage, destroyed flags, native repair on existing references and positive damaged-device controls. No historical wall attack/repair action is inferred. |
| [SD1](../containers-displays/native.md), [S1](../storage/report.md), [SD2](../shared-outpost-storage/consumers.md) | Inventory/display reference identity and ingredient provider/spending distinction. No decal or wall catalogue is inferred from a container label. |
| [C1](../cargo-links/configuration-ui/report.md), [C2 cycle](../cargo-links/transport/cycle.md), [C2 lifecycle](../cargo-links/transport/lifecycle.md) | Separate fixed cargo compartments, pairing, animation/state and OnLoad restoration. No freight transfer is inferred from an animation. |
| [Build Mode audit](../event-associated-position-oracle-and-build-mode.md), [position](../durable-outpost-center-and-object-transforms.md) | Transient preview/readiness and transform contexts remain separate from committed construction/configuration. No old runtime center is reused as this task's baseline. |

These are credited prior project findings, not fresh BM1 independent replications
of their entire subjects. Fresh executable/ESM hashes match the reused native
build pins. No older save's plugin state is silently equated to the current main
ESM or to a current rendered load.

## Census and inclusion/exclusion

The owned group-bounded reader freshly scans the main ESM. Header counts include
87 STBH, 655 STMP, 148 STND, 3009 COBJ and 12966 LMSW. Selected physical definition
types and full ordered fields are retained locally; CSVs export authored facts,
not game source dumps. Every STBH entry is retained in behavior-rules.csv,
including ship, debug, foundation, add/remove and ungrouped automatic entries.
No deleted/unused-looking editor ID is silently removed from a physical census.

The template walk selects 188 PackIns and 188 cells, yielding 2769 physical placed
references. Its selection contains hab/support/airlock/cargo and STBH target
PackIns; it is not every game template or an effective loaded construction
census. A second pass adds nested Outpost_OPK definitions. Missing indexed
template bases and selected TRNS/PTST definitions are physically reread in
extra-definitions01.json rather than guessed from nearby records.

Negative coverage: no grouped floor/ceiling selector is demonstrated in the
primary Four Wall Hab's template/behavior graph; other types of horizontal
adaptation remain present. Ordinary inspected hab wall candidates lack DEST;
cave breakable walls provide an independent positive damage mechanism. LMSW
collections provide positive material declarations; no storage-decal picker or
arbitrary dynamic save authority is inferred. All installed overrides, every
cosmetic asset and full ship construction are outside this main-ESM census.

## Tools and local outputs

All BM1 helpers below are original project code or explicit adaptations of owned
readers under SOR-P-0002. Hashes/paths are in sources.csv. They use CPython 3.14
stdlib and existing project modules; invoke with `-B` from the repository root.
No dependencies, binaries or scripts were downloaded. The existing Windows
python alias was inaccessible; the installed interpreter was used directly.

| Helper | Reads | Writes / prerequisites / effects |
|---|---|---|
| `.local-work/bm1-start.py` | Prior baseline, installed EXE/ESM/ZIP/BA2, existing database, HEAD/index, supplied brief/images | New ignored BM1 baseline/settings and copied owned readers; launches existing Ghidra 12.1.2/Temurin 21 with readOnly/noanalysis. No analysis/game mutation. |
| `.local-work/bm1-defs.py` | Installed main ESM, owned bounds/decompression reader | Exclusive definitions01/02 JSON; all physical selected-type fields local. The initial broad type selection hit the existing 16 MiB guard; relevant types succeeded without relaxing it. |
| `.local-work/bm1-templates.py` | Pinned main ESM and definition index | Exclusive templates01/02 JSON, original header/group checks; no extracted assets or input writes. |
| `.local-work/bm1-extra-defs.py` | Same ESM, selected missing base IDs and PTST records | Exclusive extra-definitions01 JSON. Header traversal is slow because it checks file size repeatedly; no safety bypass or source mutation. |
| `.local-work/bm1-saves.py` | Five immutable historical originals, frozen inventory, native-qualified prefix/extra grammar | Exclusive saved/saved2 JSON and local adapted-parser text; temporary decoded scratch context-cleaned. Unknown suffixes stop; no original writes. |
| E2ReadSession / Cr1Recon / TransitCalls | Existing imported program, named requests | Exclusive numbered native TSVs/done files under BM1; no analysis, symbols, comments, type or executable changes. Sentinel retires owned worker. |
| `.local-work/bm1-ledgers.py` | Local evidence and owned method hashes | New authored definition/rule/sample/function/source CSVs; no proprietary payload promoted. |
| [verify.py](../../../research/construction-variants/verify.py) | Ledgers, actual pinned ESM/saves/native exports, baseline | Exclusive verification JSON; physical rereads, saved envelope/queue and selected body-byte checks. DA/191/owner assertions use stored decoded extras; extra-level queue consumption is not independently rebuilt. |
| Local package.py | HEAD/index, current UTF-8 text, baseline | Ignored complete/task-only patches/manifests and disposable standalone replay trees under `.local-work/review-patches/`; no staging, workspace apply, ref or network writes. |
| `.local-work/bm1-prose-fix.py` | New BM1 Markdown only | Local prose correction pass, followed by manual review and explicit UTF-8/token audit. The plan's thousands-separator typo introduced by this pass was corrected; do not rerun it over the final prose. No evidence/input changes. |
| `.local-work/bm1-register.py` | Eight existing repository index/provenance files | Prepends one bounded BM1 cross-reference block to each after independent substantive acceptance, preserving prior bytes; no staging or target operation. |

New local source/script observations are generated using stdlib ZIP reads from
the hashed installed ContentResources.zip. Relevant Form/ObjectReference/cargo
members are hashed in scripts-source01.json. Their source declarations are
distinguished from the reused compiled C1–C3 execution evidence. Source text
itself is excluded from patches.

## Failures, integrity and review boundary

The inaccessible python alias, broad census resource-guard rejection, initial
size/bytes metadata mismatch, failed shell quotation and already-existing output
assertions are retained as investigation failures. None modified a protected
input. Failed/interior native function requests and decompiler/instruction caps
are enumerated in export-limits.csv; no missing decompilation is presented as a
successful execution trace. Full decompilation and bounded instruction coverage
are separate properties.

The verifier tests primary headers, envelopes, reference queues and selected
body bytes, plus assertions over stored decoded relationships. Extra-level queue
consumption is not independently rebuilt by it. Independent review separately
sampled the positive HIST-0210 doorway's DA source and 191/owner queue joins.
Preservation and scientific interpretation are separate. Reviewer instructions prohibit edits,
target operations and integration; its actual decision and reviewed snapshot
must be recorded in review.md. No maintainer integration or publication approval
is implied by passing mechanical checks or independent scientific acceptance.
