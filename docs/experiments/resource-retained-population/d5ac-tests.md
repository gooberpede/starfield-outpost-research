# D5AC test and counterexample ledger

2026-11-01. Tests use owned offline Python and immutable local captures only.
[Report](d5ac-report.md), [source locator](d5ac-sources.md).

| Test family | Actual result | Oracle and limits |
|---|---|---|
| Raw B2 authentication | 32,141 / 32,141 frames pass SHA, header, size, sequence and CRC; reader result equals original. | Independent explicit-offset decoder agrees on every field with existing decoder. Existing reader authenticates cumulative prefixes/ACK/terminal. Neither proves native coverage. |
| Epoch accounting | 224 / 224 increments consecutive; two reset and 111 matched Grid-call pairs. | Source increment sites, observed reason and QPC; all increment-causing records have strictly increasing QPC. No counter wrap, reentrancy hazard or reported loss observed. |
| Damaged raw inputs | 3 / 3 reject. | Truncation, changed byte and missing first frame fail the pinned-byte guard before derivation. This is identity refusal, not a separate successful CRC-damage exercise. |
| Unchanged predicate | 16 / 16 expected outcomes. | Disposable event copies of the retained P3 normal capture, not B2 substitutions. Valid triad yields one chain. Fifteen adverse cases yield none. |
| Independent state schedules | 4 / 4 expected outcomes. | Finite pointer-key state oracle permits miss/insert/store/hit, rejects hit without insert, insertion for another pointer and erase before hit. Lock scope is independently grounded in native code; this small oracle does not model OS scheduling. |
| Carried native emptiness | Interval 883 to 1731 to 2470 matches stated premises. | Separate native-graph inference; no production reducer modification or historical certificate fabrication. |
| Fresh-output repetition | Final reconstruction04/05 and controls03/04 byte-identical within each pair. | Input/method/output hashes retained in local verification manifest. First reconstruction01 predates the extra oracle and is retained separately. |

The sixteen predicate cases are valid triad; wrong reset owner; missing Cold;
missing reset end; unmatched epoch; constructor-only evidence; reset end after
Entry in native time; cross-thread reset end; cross-thread store; changed owner
at store; missing publication; loss through store; earlier eligible decision;
earlier map access; content/token collision; and retirement with delayed
admission. Full modified event dictionaries, expected chain counts and actual
diagnostics are in `.local-work/d5ac/controls04/controls.json`. The unchanged
normal P3 input SHA-256 is
`35dfc013c059f98602549fdfe92b3e43df45352b69e09100eb37c4b5a37ccc4c`.

The earlier-decision adverse control specifically reports
`PRIOR_OR_UNORDERED_NATIVE_DECISION`; the content/token collision reports
`TOKEN_COLLISION_OR_ALLOCATION_REUSE`; the reset-end timing control reports
`EMPTY_RESET_CERTIFICATE_NATIVE_ORDER_INVALID`. Thus these are not only
refusals caused by an unrelated missing reset premise. The retirement control
retains a refusal at the invalid lifetime prefix, rather than pretending to
execute a native retirement or record a new engine outcome.

## Preserved contrary evidence and failures

The first B2 main-menu attempt remains a failed admission, with no target
evidence or terminal. The B1 losses, D5AA historical non-identifiability and P1/P3
development failures retain their historical reports. The earlier target check
8006 is a direct counterexample to treating the constructing check 8020 as the
first eligible target decision. The stream's 97 adjacent QPC inversions refute
using admission order as a global causal oracle. Empty Grid clears refute
counting observer epochs as physical reset generations.

No failed experiment is rewritten as a pass. Initial read-only wildcard searches
using an unsupported Windows glob failed and were replaced with explicit paths;
they are not absence evidence. The specialist interrupted two overly broad
read-only searches and uses positive native bodies rather than those searches.
No native execution, Ghidra database action, third-party download or protected-save
test occurs. Historical native-host tests are context, not newly repeated tests.
