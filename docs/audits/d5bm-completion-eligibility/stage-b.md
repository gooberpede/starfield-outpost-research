# Stage B first-miss integration

**NOT EXECUTED.** Stage A is **INCOMPLETE**. Under the D5BM gate, execution of
either integrated first-miss continuation requires an independently qualified
positive Stage A.

| Original continuation | Retained evidence and missing integration |
| --- | --- |
| Owner-back `(10,11) → 0x3` | The historical conditional sequence selects registration index 845 after 58 non-target claims. It reaches face cell `(37546,20939)` and corner slot `+0x28`. D5BM supplies neither the joined eligibility edge nor the selected protected miss. |
| Peer-front `(-2,-2) → 0x0` | The historical conditional sequence selects registration index 874 after 28 non-target claims. It reaches face cell `(37534,20926)` and corner slot `+0x20`. D5BM supplies neither the joined eligibility edge nor the selected protected miss. |

The common historical prefix has 1,600 rectangle roots, 1,720 deduplicated
density keys and 196 target-capable requests. The `(-2,11)` layer can target
the source even though its four density neighbors cannot. This defeats a
density-only exclusion. The retained N2 projection verifies one recorded
constructor at that layer coordinate, with mask `0x3` and sample sequence
3962, at its own evidence tier. Neither proposed first-miss continuation
was observed in N2.

Any later qualified integration has to bind the selected source allocation
and owner through native provider selection, full-token visited check,
owner-wide exclusive `+0x40` protection and full-pointer miss through
generation. A warm aggregate, occupied target holder, earlier demand,
full-token alias, owner-wide contention, frame invalidation or retirement can
defeat the proposed witness. The manager reader released by rectangle
destruction does not pin the later source. Historical scope remains two
native-feasible continuations using original instructions and static
composition under specified preconditions. Measured frequency, individual
winner reachability across 196 coordinates and uninstrumented retail
outcomes remain outside that scope.
[D5AQ reachability](../../experiments/resource-retained-population/d5aq-reachability.md) ·
[D5AM owner census](../../experiments/resource-retained-population/d5am-owner-lock-census.md) ·
[D5BI crosswalk](../evidence-derivative-d5bi/d5aq-crosswalk.md)
