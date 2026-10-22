# Executed synthetic qualification

[Commands](verification.md); authoritative receipt:
`.local-work/resource-oracle-collector/qualification04/qualification.json`.
**19/19 cases PASS**, with intentionally failed acquisitions distinguished below.
This is actual x64 Windows execution, not mocked Windows APIs. Build08 is pinned
in its build.json. Each case retains command/config, native events, individual
SRO1 files and ACKs, result, independent test verdict and hashes. Raw addresses
are runtime VAs, sites are runtime base+module RVA, and IDs are synthetic u32s.

| Case | Observed result and test meaning |
|---|---|
| good | 12 complete acknowledged samples, two visits, one sampled thread; refresh→nested decision→retained→three recursive decisions per visit. Ordered population identities/type/raw bytes and source-selected outcomes match independent table. |
| zero | 12 complete ACKs; actual initialized spatial list is empty, unlike unreadable/null-member failure groups. Nonspatial positives remain. |
| threads | 18 complete ACKs, three sampled worker lifetime tokens, CREATE/EXIT coverage and deliberately yielded interleaved scheduling. Every visit has exactly its own six samples; global native sequence set and per-thread sequence coverage are checked. |
| crash-after | 12 complete readback ACKs before target exception0xe043c1c1; acquisition PASS, target survival FAIL by design. Both exception chances passed, no suppression. |
| bad-pointer | Seven samples, final spatial read fails at aligned inaccessible address8; INCOMPLETE(pointer-read), members=null, session FAIL as expected. Earlier six groups remain valid. |
| bad-count / overflow / budget | Seven each; final count>capacity, wrapped u64 ordering, or4097-entry header refused before the unsafe copy. INCOMPLETE(range/range/budget), session FAIL as expected. |
| truncated | Actual valid pointer range crosses into PAGE_NOACCESS; exact pointer-array read fails, INCOMPLETE, session FAIL. |
| truncated-resource | Pointer array remains readable but an8-byte Resource straddles a PAGE_NOACCESS boundary; resource-read INCOMPLETE, session FAIL. |
| crash-before | Target exception0xe043c1c0 before any sample; zero captures/ACKs, acquisition FAIL as expected. |
| interrupt | Explicit collector fault stops a group before its population walk; one durable diagnostic ACK, acquisition FAIL. This is an injected interruption, not a claim of OS partial-read behavior. |
| drop | Explicit serialization loss on second native sample; only first accepted ACK, sticky failure and fixture STOP. Not a test of Windows silently dropping debug events. |
| malformed | Deliberately truncated first receipt fails decoding; no ACK, acquisition FAIL and STOP. |
| ackfail | Deliberate rejection at ACK validation boundary; valid data/ACK bytes can exist, but zero accepted ACKs and acquisition FAIL. This tests rejection policy, not an actual failing disk. |
| preack-stop | Actual disposable termination after partial first receipt and before terminal/fsync/readback ACK; no ACK, acquisition FAIL. |
| stop | Explicit bound2; both complete receipts acknowledged before disposable termination0xc1c0. Acquisition PASS for those two observations; no full-visit completion claim. |
| transport | All eight unchanged C1B framing/corruption/sequence/terminal/copy-budget/empty/readback methods PASS. |
| isolation | Requested different executable refused before launch/output creation; missing --synthetic-only refused by actual controller, exit2. Protected-byte and index verification are separate postflight checks. |

The original table in qualification01/02 had eighteen passing cases but weaker
discrimination: atmosphere/biome tests only rejected an absent resource. Independent
review requested positive nonspatial and cross-population-negative controls;
qualification03/04 add these and actual nested sampling/resource-record truncation.
Earlier evidence is retained and not relabelled as final coverage. Build01 produced
an argument-conversion compiler warning, corrected by checked ASCII conversion.
smoke02/03 failed an overstrict raw context comparison after one acknowledged
sample; diagnosed raw differences were EFLAGS bit1 and DR7 bit10. Corrected build04
passed; final build08 also checks meaningful CPU state on every resumed sample.

No kernel debug-event loss was observed in this finite fixture, but none of this
proves detection of every missing breakpoint or arbitrary scheduler interleaving.
The three workers own separate populations; this is thread/site/accounting
qualification, not a shared-writer race/lifetime lease. Actual nested-return
witnesses support the fixture call relationship, not a general native unwinder.
No retail guard/owner/load map, geometry copy, cold-page stress, unowned-trap
injection, XSTATE test or physical disk-failure experiment was executed.
