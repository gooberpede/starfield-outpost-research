# First-release tiers for power, cargo, local links and historical observations

**Selected 2026-11-10 (Australia/Sydney). Publication NOT READY / NOT CLEARED.**
The [maintainer brief](../../implementation-briefs/CODEX_BRIEF_SOR_RG2_D5BQ_Power_Cargo_D1_Historical_Publication_Reconciliation.md)
selects the evidence tiers below. The original reports and reviews govern
scientific confidence. The [D5BG ledgers](../publication-claims-d5bg/README.md)
track each route and its prerequisites.

## Mechanisms and selected original witnesses

| Finding | Selected first-release tier and limits | Pending original-byte or release check |
| --- | --- | --- |
| Ordinary power and shortage allocation (`B4-C07`, `B4-C21`, `B4-C21-SAVE29-ORIGINAL`) | Retain the accepted traversal and cumulative-demand rule. Save29's ordered graph supports a conditional reconstruction with supply 6 and demands 5 then 5, so only extractor #1 fits. The saved powered bits also match the report. Historical effective inputs and the recalculation invocation remain untraced. [Allocation review](../../experiments/power/review.md) · [Save29 authority](../../experiments/power/save29-authority.md) · [review](../../experiments/power/save29-authority-review.md) | `S-P1-S29-ORIGINAL` remains CONDITIONAL. Verify CORE B4-F054 with a qualified read-only reader, including all four selected electrical connection rows, saved flags and decoded-stream selectors. The tracked calculation `S-P1-S29-CALC` has its separate route. |
| Freight, the return hold and inter-system fuel (`B4-C09`, `B4-C23`, `B4-C23-SAVE52-ORIGINAL`) | One shared hold can carry freight that did not fit on arrival back to the origin's **incoming** bay if the return completes and space allows. Either eligible inter-system endpoint can pass the readiness check. Separate timer queueing and Papyrus virtual machine (VM) dispatch from native path completion, producer elapsed time and delivery throughput. Five He-3 is the recipe per accepted fuel-production cycle. Constellation's Guide is a candidate 0.95 interval multiplier, changing 108 to 102.6 engine scheduler seconds when applicable. Shorter eligible intervals could raise He-3 use per scheduler time. Historical source and rank, delivery acceleration, shorter transit and universal rates remain unestablished. [Freight report](../../experiments/cargo-links/transport/report.md) · [Timing review](../../experiments/cargo-links/transport/transit-review.md) · [Fuel mechanism](../../experiments/cargo-links/fuel/native.md) · [Saved interval](../../experiments/cargo-links/fuel/saves.md) | `S-C23-SAVE52` remains CONDITIONAL. Verify CORE B4-F040 (Save52/HIST-0267), the selected pair, child roles, shared hold, decoded stock and explicit inventory unknowns, and the four selected fuel-source joins with a qualified offline reader. |
| Local output links across unlink and relink (`B4-C08`, `B4-C22`, `B4-C22-L-SERIES-ORIGINAL`) | L0 is the original linked baseline. The operator reported a linked baseline after reload (L0C), unlink and its same-session unlinked control (L1, L1C), then relink and its same-session linked control (L2, L2C). The selected relationship payload lengths are **19, 19, 12, 12, 19 and 19 bytes**. The tokens differ in corresponding saved windows across the reported reload and elapsed time. The original literal fails from L0C onward, and entry order defeats token-only substitution at L0C. The later bounded endpoint-pair association leaves the remapping mechanism, full grammar, general direction and load authority unresolved. [Controlled save sequence](../../experiments/output-link-validation-L0-L2C.md) · [Local links review](../../experiments/local-output-links/review.md) | Both `S-S2-L0` and `S-S2-L-CONTROLS` remain CONDITIONAL. Qualify CORE B4-F032 plus ADDENDUM B4-F055–F059 and the exact windows, failed literal and same-session controls. If any required member or reader control fails, narrow independent reproducibility to the supported authored inspection tier and preserve the recorded investigation. |
| Saved-site contrasts for reported disappearing deposits (`C19-D1-SAVED`, `C19-D1-SITE-TABLE`) | Select the attributed bounded saved-state tier. D1 identified three site correspondences with unchanged sampled fields across the tested pairs and 45 curated direct-owner extractor associations. The tracked site table separately supports arithmetic over transcribed fields. Save37/HIST-0249 is outside the qualified extractor decode. The saved evidence supplies no timed deposit or production change. [D1 report](../../experiments/disappearing-deposits/report.md) · [Review](../../experiments/disappearing-deposits/review.md) · [Site table](../../experiments/disappearing-deposits/sites.csv) | Keep `P-D1-SAMPLES` HELD for the stronger exact replay. Save52 alone cannot recreate the mature pairs. No additional historical-saved-state asset is selected. |
| Native callback comparisons in Kreet (`C19-CALLBACK`) | The proposed `c19-callbacks-v1.json` derivative checks all **346 complete recorded callbacks**, from ordered native inputs to final row associations. The prior local check includes repeated updates. The broader preview chronology is a separate historical tier. [Callback evidence and verification](../evidence-access-d5be/c19.md) | `P-CALLBACK-FOLD` remains CONDITIONAL. Verify the exact C19 asset, ordered comparisons and negative controls in isolation for B6, then check separately authorized hosted bytes. |

The exact [D5BF asset ledger](../release-assets-d5bf/release-assets.json) and
[original member index](../publication-readiness-b4/f1/members.csv) bind the
selectors. Assets remain **APPROVED FOR PROPOSED RELEASE / PENDING RELEASE**.
File-specific rights and privacy, authorized transfer and retention, exact
isolated frozen-candidate B6 preflight, separately approved distribution and
hosted container/member verification remain pending. The
[publication run card](../../PUBLICATION_RUN_CARD.md) also covers the tree,
reachable history and final visibility and timing.

## Historical observations

| Historical-only tier | Attribution and access boundary |
| --- | --- |
| Three fresh-process Save29 loads (`B4-C07-SAVE29-THREE-LOADS`) | The maintainer reported extractor #1 powered and #2 unpowered immediately and several seconds after each load. Two screenshots corroborate the setup and displayed contrast. They lack per-trial timing and synchronized native effective-state observations. The report retains its original historical disposition. Exact reconstruction of the three executions stays HELD under `S-P1-THREE-LOADS`. [Trial evidence](../../experiments/power/save29-test-plan.md) |
| Mature private cargo network and script context (`B4-C23-PRIVATE-COMPARATORS`) | Attribute the original topology agreement with the private manually maintained network. Parallel pair identities remain ambiguous, and the specific historical Save52 timer remains unknown. The comparator supplies neither a replayable voyage nor a measured flight clock. `S-C23-VM-NETWORK` stays HELD. [Network comparison](../../experiments/mature-save-outpost-validation.md) · [Saved freight state](../../experiments/cargo-links/transport/saves.md) |
| Reported loss or substitution of deposits (`C19-D1-INCIDENT`) | Preserve the source-reported incident and D1's original **PARTIALLY DISCRIMINATED** verdict. The [later research synthesis](../../experiments/disappearing-deposits/subsequent-research.md) explains how geometry can change. Actual cause of the reported incident and a matched change in affected-extractor operation remain unmeasured. `P-D1-INCIDENT` stays HELD. |
| Larger Kreet unplaced-beacon preview experiment (`C19-UPSTREAM`) | The operator reported **A** Iron + He-3, **B** Iron + Alkanes + He-3 and **C** Iron + He-3. The original study recorded **35,573 preview evaluations plus one initialization evaluation**, and **346 complete native user-interface callbacks**. The selected callback derivative carries run summaries as context. It cannot reconstruct every upstream evaluation, establish a unique asynchronous producer or timestamp actual screen rendering. The original observations and review retain their scope. `P-CALLBACK-UPSTREAM` stays HELD. [Original Kreet report](../../experiments/continuous-beacon-preview/live-scientific-report.md) · [Original review](../../experiments/continuous-beacon-preview/review.md) · [Callback access](../evidence-access-d5be/c19.md) |

## Separate research follow-up

The [Exotic inactive-resource setting gap](../../BACKLOG.md#exotic-inactive-resource-default-reachability)
remains OPEN and nonblocking. The accepted initializer and installed-setting
discrepancy motivates a separately scoped static reachability audit.
[C1H evidence and limits](../../experiments/resource-installed-settings/review.md)

The [D5BP selections](../publication-decisions-d5bp/README.md) and
[D5BO routes](../public-evidence-d5bo/README.md) retain their scope. The
[D5BN decision](../../DECISIONS.md#d5bn-d5bm-deferral--2026-11-10) retains
D5AQ Option C as preferred and D5BJ and D5BM as deferred.
[Reading, verification and review](review.md)
