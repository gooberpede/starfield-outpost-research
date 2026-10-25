# D5B combined construction and consumer acquisition

Later separately authorized [Phase B](phase-b.md) records current Feynman V
consumer geometry. This report and its AC1–AC8 review describe the earlier Phase A.

2026-10-25, Australia/Sydney. [Authorized brief](../../implementation-briefs/CODEX_BRIEF_SOR_RG2_D5B_combined_construction_mask_consumer_acquisition.md), [native contract](native.md), [qualification and review](review.md), [proposed run card](run-card.md), [source pins](sources.csv).

**Phase A implements a combined Windows debugger controller. It captures the exact selected source's initial query and ordinary mask, and separately captures current Workshop consumption. Retail generation-to-consumption lifetime attribution remains UNKNOWN. No Starfield session was launched or attached.**

The selected case is the active second Feynman V outpost: saved Workshop identifier bytes `b0e207c2dee2c1b6`, saved beacon token `84e101`, owner/body FormID `0x0005e0de`, source `0:37536:20928:0029d20e`. These identifiers come from the committed [D5A identity records](../resource-construction-mask-selection/identity-context.csv), not screenshot labels. Source chart and descriptor are conditional on the qualified interior frame; current native pointers must be measured. A matching planet or resource list cannot satisfy the source selector.

## Supported result and coverage

The instrument observes actual target-owned source-shaped memory through Windows debugging APIs. The producer and consumer run in one disposable process, under one controller and durable SRO1/ACK transport. The synthetic population linkage test has an explicit fixture ownership contract: the generation writes the population; its stack-owned arrays remain alive through the synchronous consumer call; pinned fixture source establishes the sole writer and excludes reset/replacement on the positive path. The controller copies that population, its exact geometry and synthetic witness at both ends. Replacement and reset variants must refuse this link.

That qualification is **SYNTHETIC_ONLY_LINKED**. The synthetic witness is original fixture memory, not an engine field. It is compiled out of the retail controller. Retail reduction never supplies the fixture proof and cannot emit a synthetic link. An all-stop slot switch leaves a native lifetime observation gap, so equal pointers, bytes, geographic keys, geometry or timestamps do not establish a native population epoch. [C1's ownership limits](../resource-geometry-observation/native-contract.md) remain intact.

Construction-only is a useful canonical measurement even without a later consumer. Consumer-only establishes current accepted geometry and same-evaluation transfer membership, with historical construction unknown. A combined unlinked result retains both independent observations. Contradictory mask constructions remain separate by process, thread lifetime and invocation token. No observed contemporary query is called the historical Save52 query.

The fixed [D5A alternatives](../resource-construction-mask-selection/report.md) remain unchanged. Mask 0 predicts ordinary IL/Fluorine/Copper weights approximately (0.05, 0.2, 1); mask 3 predicts (1, 1, 1). Both alternatives can yield all three resource names. The comparator checks sampled mask, observed candidate order and weight bits, and exact ordered binary32 XYZW/bounds of consumed regions against both alternatives. It records disagreements rather than fitting a prediction. The frozen alternatives contain no historical first-query value, so that comparison remains explicitly unavailable.

## Controller and selection

The hardware schedule reserves generation entry and a rotating producer stage, plus provider entry/return. The fourth slot observes updater entry outside generation and the ordinary resource call inside generation. Updater entry switches all stopped threads to ACCEPT/REJECT/transfer sampling and invalidates incomplete construction state. Transfer retirement may restore producer sampling. A complete target construction can instead request consumer mode immediately after its durable ACK. No fifth hardware slot, INT3 patch, TF stepping, injection or detach/replay is used.

Every transition records its observation gap. A generation call during consumer sampling, or an updater entry during generation, can be missed. New threads receive the current schedule; nested evaluation ancestry is preserved in consumer stacks. Producer nesting that loses stages stays incomplete. Queued old-schedule traps that cannot satisfy the current ownership guard produce LOSS and disposal. No gap is converted into an epoch claim or a successful empty population.

Copy bounds are 65536 bytes per read, 1048576 bytes per sample, 4096 regions/points where the inherited parser applies, and 64 nested frames. These are memory-integrity limits, not arbitrary scientific quotas. The controller checks both drives for at least 40000000000 caller-available free bytes. It preserves program registers/floating state while changing owned debug registers and RF. Attachment, all-stop pauses and execution breakpoints can affect timing.

The wrapper fsyncs, closes, reopens and independently decodes each SRO1 sample before ACK. STOP intent is monotonic before termination; queued thread exits are drained without rearming. Complete receipts survive target failure. Engineering status, scientific result, evidence integrity and target exit are reported separately. Missing or refused ACK is not scientific success.

## Authored implementation and provenance

All code is original project adaptation under SOR-P-0002. No new dependency, outside code, licence acceptance or external contact was used. `sources.csv` records original paths, HEAD and SHA-256 pins, including primary native ledgers and frozen prediction bytes. Proprietary exports, saves, executable builds and raw receipts remain ignored and local. Publication eligibility remains independent of confidence.

The implementation lives in `research/resource-combined-acquisition/`:

- `controller.cpp`, `consumer.inc`, `operands.h`: combined external debugger and checked read paths; native provenance in [native.md](native.md).
- `producer.cpp`/`.asm`, `consumer.cpp`/`.asm`: original disposable fixtures adapted from D4 and D4A. They are source-shaped engineering targets, not retail geometry implementations.
- `reduce.py`, `consumer.py`, `compare.py`: exact-source selection, same-evaluation consumer ancestry and fixed-alternative comparison. The default reducer has no synthetic lifetime proof.
- `build.py`, `qualify.py`, `d5b_contract.py`: installed MSVC build, pinned real Windows execution and mandatory scenario roster.
- `collect.py`, `preflight.py`, `postflight.py`: future separately approved retail transport, strict offline admission and after-exit audit; no launch helper.
- `audit.py`, `regression.py`, `legacy_regression.py`, `inherited.py`, `package.py`: protected-input equality, actual inherited controls, logs and exact review exports.

Every script documents reads, writes, prerequisites and target effects. Build and test outputs refuse overwrite. No cleanup of prior evidence, staging, commit, push, integration, B6 or publication is authorized. The [review package](review.md) governs exact acceptance; this report does not approve Phase B.
