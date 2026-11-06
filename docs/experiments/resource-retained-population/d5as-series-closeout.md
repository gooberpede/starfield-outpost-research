# D5AS Feynman series closeout

2026-11-06, Australia/Sydney. **Two of 30 qualified fresh-process observations
matched the complete fixed mask-0 reference. The other 28 matched the complete
fixed mask-3 reference.** Both geometry classes occurred at the established
Feynman V source under the series protocol. No qualified observation differed
from both references.

This is runtime evidence of full canonical geometry equivalence at geographic
source `0:37536:20928:0029d20e`, owner body FormID `0x0005e0de`, and source-planar
origin `(-200,-200)`. Reference equality supplies the prespecified mask-class
proxy. The capture contains no direct observation of the generating mask.
Effective generation-input equivalence, physical outpost membership and
ordinary construction-winner causality remain open. GC-10, GC-31 and D5R
remain OPEN. Raw series evidence is LOCAL-ONLY.

## Frozen roster and comparisons

| Qualified class | Count | Fraction | Exact marginal 95% interval under IID |
| --- | ---: | ---: | ---: |
| `MATCH_MASK0_REFERENCE` | 2 | 6.67% | 0.82% to 22.07% |
| `MATCH_MASK3_REFERENCE` | 28 | 93.33% | 77.93% to 99.18% |
| `OTHER_QUALIFIED_GEOMETRY` | 0 | 0% | 0% to 11.57% |

Qualified roster positions 7 and 13 are the mask-0-reference matches. Their
capture UUIDs are `359325f8-3088-4997-a348-a559dbd403c3` and
`adb8bb75-84e1-4b7e-87f9-1a150741f6b4`. Both complete 4,966-byte canonical
bodies have SHA-256
`bba4c877bc14d8abd3cfe36313e4cd62fd98e510dbf18441b250eacb57b942c4`.
The other 28 complete 4,858-byte bodies have SHA-256
`7b66c2cce4b0c4c2d52a91a41d02997f12632d0c197681fcf4f21cb87bdbf653`.
The comparison uses all canonical body bytes. The body and historical
envelope-inclusive A0 representation are separate byte domains.
[Producer profile and reference basis](d5as-producer-profile.md).

Under the prespecified binary proxy model and the hypothetical IID binomial
null with 30 trials and mask-0-reference probability 1/7, the observed count
is K = 2. The inclusive lower tail is 0.177368, the inclusive upper tail is
0.941150, and the probability-ordered exact two-sided p-value is 0.303654.
The preregistered probability of 30 mask-3-reference matches is 0.00980836
under the same null. The intervals are marginal. Neither they nor the tail
probabilities account for dependence or selection from acquisition failures.
Fresh process identities establish separate starts. They supply no proof of
IID, and the conditional request-coordinate census does not measure a game
winner probability.
[Prespecified analysis](d5as-analysis-protocol.md).

## Acquisition and exclusions

The maintainer authorized the selected 0.2.0 package and five-action card after
the startup-only smoke test. The maintainer reported following that procedure,
collecting one replacement the same way, and disabling the plugin after
eligibility was confirmed. These are operator observations. The startup and
capture records independently bind the reported producer and process fields
within their evidence scope. Effective deployment, loaded save and route
were not independently observed on each run.

| Evidence class | Observed | Disposition |
| --- | ---: | --- |
| Published snapshot files | 31 | 30 qualified, one excluded |
| Startup receipt files | 99 | Three stages for each of 33 process sessions |
| Startup-only sessions | 2 | Consistent with the reported smoke test and failed background launch. No capture artifact for either session. |
| Partial files | 0 | None inventoried |
| Pilot04 | Historical | Excluded from the series by design |

Capture attempt 6, UUID `7edfc207-4f95-4cdc-9617-ce847107c49c`, is the sole
invalid or inconclusive capture. The producer reported
`SOURCE_LIFETIME_RETIRED` for `map-entry-56`. The missing geographic identity
could conceal a second target. The prespecified eligibility rule excluded it
before any outcome classification. The first pass therefore returned
29 qualified from 30. The replacement added one eligible capture and three
startup receipts, and all 126 prior artifacts remained byte-identical. The
second pass found 30 eligible and required no further replacement. The
chronological roster uses process creation FILETIME, then invocation UTC and
the two UUID ties. The evidence cannot enumerate launches that left no artifact.

## Protection and archive

The protected content postflight passed against the pinned D5AS baseline.
It verified 98 protected originals and backup sets, 95 protected remote files,
39 definitions, 23 configuration files, and two archive/index inputs. Save52,
its loose backup and the isolated restoration rehearsal each matched
16,411,136 bytes and SHA-256
`6b4a10084c7e752c31fd2de121a00850aaa2bf1decd700b437d7dccfcdbc82e8`.
`Plugins.txt` and `StarfieldCustom.ini` had timestamp changes with equal
content. Caller-available space at the end of postflight was
77,332,410,368 bytes on C: and 82,111,463,424 bytes on D:. Both exceeded the
40,000,000,000-byte floor. The audit left original saves and backup inputs
untouched. Its inherited diagnostic still reports the separate historical
strict removed-ZIP failure. That historical verdict remains intact.

The independent pre-freeze review accepted the exact authorization, ledger,
capture archive, and before and after protection receipts. It reproduced
the same candidate roster without classifying outcomes. All 130 capture
archive members matched the loose evidence and ledger hashes. The locked
analyzer then published the exclusive frozen manifest containing the roster,
canonical bodies and statistics. The closeout bundle seals that result and its
supporting receipts with a stream-verified internal manifest. Loose capture
evidence and protection receipts remain in place.

| Local artifact | SHA-256 |
| --- | --- |
| [Final eligibility ledger](../../../.local-work/d5as/attempts-02.json) | `f248c86e940accf2643f3f9d4a1778e0d9f84bc03a9d93ec8131e6cebd34eefa` |
| [Protected postflight](../../../.local-work/d5as/protection-after01/protection.json) | `0df32300a3564d21e7bea2b05f884ddcdc02f5798daaf4941a8f7e913b02c2f4` |
| [Capture archive](../../../.local-work/d5as/corpus.zip) | `4d0dc101ed7bc8204ae29273bf1eb87feeb8cf0b9ac291988da177511f81966b` |
| [Frozen corpus and statistics](../../../.local-work/d5as/frozen-corpus.json) | `16784d4c772895ccad62415011014e2c6165906231498d203ed833f5a30dc598` |
| [Sealed closeout bundle](../../../.local-work/d5as/d5as-closeout-evidence.zip) | `f0660067971738ba341562677efb0a3f0ca198f25478e09fea10880d0de90874` |

[Independent pre-freeze review](../../../.local-work/d5as/pre-freeze-review.md) ·
[Seal receipt](../../../.local-work/d5as/d5as-closeout-seal.json) ·
[Preparation and authority boundary](d5as-handoff.md).
