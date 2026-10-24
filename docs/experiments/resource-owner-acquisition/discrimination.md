# D4D comparison and discrimination matrix

Every example below is an authored synthetic target history. Resource-number
constants deliberately resemble the question's inputs; none is a new observed
Archimedes component. `W`, `T` and `C` denote fixture words `0x000083ec`,
`0x000057c4` and `0x000057d5`. Root `0x00000123` is an arbitrary test key.
Raw component prefixes, every map/staging boundary and candidate/CALL order are
retained in the local qualification receipts. [Native interpretation](native.md)
and [executed checks](qualification.md) provide the evidence boundary.

| Fixture or adversary | Discriminating observation | Expected result |
|---|---|---|
| Direct supply | Zero-root row has W in slots 0 and 2; C-root row has T in slot 1. | C map is `[W,W,T]`; ordered calls are `[W,W,T,C]`. Both W occurrences have separate native slot locations. |
| Exchange displacement | Zero-root W row; root `0x00000123` receives T; its repeated empty row displaces `[W,W,T]`; C receives the displaced staging array. | Same final C map and calls as direct supply, with a different ordered component/operation history. A final multiset cannot distinguish these fixtures. |
| Distinct visitation order | T/C row precedes zero-root W; another root later receives W. | C map is `[T]`; calls are `[T,C]`. The earliest component-order difference precedes geometry. |
| Null slots | All six words in each row are zero. | Empty supplemental map arrays; ordinary C root remains. Nulls are retained, not omitted fields. |
| Empty repeated root | C's later empty row exchanges with its populated entry. | C becomes empty; displaced `[W,W,T]` remains staging and is discarded. Calls contain only C. |
| Multiple roots | The direct fixture also installs `0x00001234` under root `0x00000099`. | Both map entries are copied; only the selected C entry feeds these calls. |
| Malformed/incomplete slot source | Invalid page pointer prevents a complete `0x8c`-byte node prefix. | No complete chain or positive STOP; unknown slots are never replaced with zero. |
| Source/wrapper reuse | Changed retained source bytes reject the chain; repeated same wrapper receives distinct invocation tokens. | No history is joined by pointer or token number alone. Identical-byte ABA remains outside qualification. |
| Wrong owner/type/range | Ascending keys have the wrong owner/type word or exceed the second-key bound. | Rejected at the first invalid node, even with plausible resource names. |
| Unrelated source/Workshop | Same-planet source or wrong Workshop can otherwise look coherent. | A construction may remain useful diagnostic evidence, but positive scientific STOP is false. |
| Cache only | Workshop-bound consumer executes without construction. | Retain cached context; construction is NO_HIT, not reconstructed lineage. |
| Descriptor bypass | Complete map returns without candidate-ready or CALL execution. | Construction completion retained; candidate/CALL coverage UNKNOWN and positive STOP false. |
| Missing ready/CALL receipts | Omit every CALL, or both ready and CALL rows, from an otherwise normal receipt stream. | Sequence/array-count checks reject complete call coverage. |
| Map contradicts model | Observed later C arrays differ from the D4C operation prediction. | Preserve the coherent observed chain and first expected/observed boundary. Allocation or mutation cause remains UNKNOWN. |
| Combined discrepancies | Model slot disagreement at component 0 plus a later observed operation discrepancy. | Report the earlier component mismatch first; retain the later discrepancy separately. |
| Nested/overlapping threads | Separate entry/parent/lifetime tokens; barriers force both entries and map returns before either concurrent call sequence. | No per-thread schedule is borrowed; complete ordered histories remain separate. |
| ACK/crash/corruption | Genuine refused/partial/missing ACK, crash before/after evidence, and modified copied SRO1 payload. | Persisted evidence, useful science, target exit and controller error remain independent outcomes. Corrupt receipt is rejected. |

The comparator accepts either decoded event JSON (`--events`) or a capture
directory (`--captures`). Capture mode independently reopens every SRO1/ACK pair,
checks its digest/framing and exact agreement with the event row, then applies
sequence, native-frame, key, map and candidate checks. An events-only result is
labelled supplied decoded events; it is not a verified raw receipt result.

The existing D4C `inputs-v1.json` can be supplied as `--model`. Its BIOM labels
remain conditional projected identities rather than manufactured native keys.
Root/slot/population comparisons precede selected-array/CALL comparison. Existing
frozen D4C inputs were not changed after seeing answers, and no new installed-data
reconstruction is claimed. The demonstrated first-order mismatch against the
synthetic fixture is a tool qualification, not an Archimedes result.
