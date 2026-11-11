# Q030: eighteen chains and the next bounded E step

2026-10-12 Australia/Sydney. Offline analysis under the
[recorded user scope](../../implementation-briefs/README.md#archive-lookup) (`implementation-briefs.zip :: docs/implementation-briefs/CODEX_BRIEF_SOR_Q030_captured_chains_offline.md`).
Continuation of SOR-EXP-0031 / SOR-EV-0039; no new experiment or live authority.

| Element | Scoped answer |
|---|---|
|Question|Why did these 18 Q calls bypass E, and which observed candidates offer the best next opportunity?|
|Best-supported answer|All 18 have different native A/B hierarchies, supporting the hierarchy-skip path. Invocations15/16 additionally have overlay bit 0 **set** in five samples each: useful positive leads for a matching-source follow-up.|
|Confidence|PROVEN / RUNTIME for captured private descriptor bytes, helper arguments and returns; STRONG / STATIC+RUNTIME for scoped skip reconstruction, pending maintainer review. No executed branch trace.|
|Coverage|144 records, 18 complete Q chains from the one approved unused Kreet landing in attempt 02; retail 1.16.244.0, unchanged 030/schema 3. No independent 18-site trial.|
|Evidence|Authenticated raw/journal, pinned native Q/caller/geometry exports; [per-chain matrix](captured-chain-matrix.csv), [source ledger](captured-chain-sources.csv), local analysis.json with all 11 comparisons per chain.|
|Limits|Sequential shared flag/settings/rectangle samples; no E/C/center/grid, runtime-to-saved identity join or full native equivalence.|
|Next step|One offline qualification of a matching-source scenario anchored to candidates 15/16, including source-key writer and natural Q trigger; choose at most one prospective live scenario only if that qualification succeeds. No run is authorized here.|

## What the eighteen chains establish

Raw session `session-28404-65495921` contains 2558592 bytes, SHA256
`43ac524c5172c98a696fdbda870dc6b29764ec4fcd8134184a4dc57815353b19`.
Journal SHA256 `9350ee7cd5099232ccafc07b5ca85474ce3841148cc601f2157ca53927a71cbe`.
Final seal SHA256 `411cb07163819f57d65ef33ef6604d3c7cb32b307e70eed1537671728cb317c9`
and all 93 members verified. All 310 qualified lock 05 pins verified unchanged.
[Attempt 02](live-attempt-02.md) retains acquisition conditions, procedural FAILs,
health/retirement/exit and protected-save evidence; this task performs no process checks.

Each invocation has kinds 7,13,15,16,17,18,19,8, thread 22636, parent 0, sequences 1–144.
Resolver and overlay complete normally/nonzero; A and B use the same landscape
argument. No fallback 14, E boundary 20, E10/11/12, C1/4/5, center 2, grid 6/3 or unwind 21.
Every final Q return and entry/exit latch is 1. These are direct observations, not
evidence of engine failure. The pinned caller AD93FA continues on 1; Q's final
geometry can return continuation after skipping E. Enumeration elsewhere remains possible.

At kind 17, all 44 bytes of private A/B descriptors are available, but Q compares
only these ordered `(offset,length)` fields, relative to each descriptor:
`(0,1),(4,4),(8,4),(10h,1),(Ch,4),(14h,4),(18h,4),(20h,1),(1Ch,4),(24h,4),(28h,4)`.
Padding is excluded. Q AD0992/AD099E and subsequent mismatch branches target
AD0ABA, beyond E AD0AB5. Static addresses here are **RVAs**; pinned preferred
image base 0x140000000. Captured runtime image base 0x00007ff7e96c0000 is session-only.

Geometry notation below is `(tag; coarseX,Y; subX,Y; fineX,Y)`, describing native
hierarchy fields, not FormIDs, map coordinates, metres or geographic distances.

| Invocations | Native candidate A geometry | First differing field | Count |
|---|---|---|---|
|1,13|0; 74,66; 8,8; 0,0|+4:74 versus 199|2|
|2–12,14–16,18|1; 54,110; 8,0; 0,0|+0:1 versus 0|15|
|17|0; 186,189; 0,0; 0,0|+4:186 versus 199|1|

Native B is identical across all 18: **0; 199,31; 8,8; 0,0**. Every pair also differs
at+4,+8,+C,+1C,+20. Fine fields+24/+28 agree at zero in all 18. Thus neither changing
only the tag nor matching only coarse coordinates would satisfy Q. Handle/table
fields participate, including byte fields+10/+20. Their numeric values are not
assigned object identities. All 198 ordered field comparisons are retained locally.

## Correction: two flag-positive candidates

The previous attempt report's sentence saying overlay bit 0 is clear in all 18 is
incorrect. Its unchanged branch-analysis JSON already reports true for 15/16;
the error was in prose summarization, not decoder or capture. Historical sealed
evidence and accepted submission remain untouched; an appended erratum links here.

| Invocations | Sample byte at overlay-relative+20 | Bit 0 | Supporting helper sequences |
|---|---|---|---|
|1–14|00|clear|kind 15–19 in each chain|
|15|01|set|115–119; kind17=117|
|16|01|set|123–127; kind17=125|
|17–18|02|clear|kind 15–19 in each chain|

Five samples per chain, 90 total, agree within each chain. Descriptor+20 is a
different field from **overlay+20**; confusing these offsets would be an error.
The actual TEST at Q AD0A12 happens only after all hierarchy comparisons pass.
It is therefore a later necessary gate, not the reconstructed executed blocker
in these 18 calls. Repeated samples do not prove its exact branch-time value or
the meaning/writer of bit 0. Set bit 0 does not prove collection population, ordinary
beacon membership or callback eligibility. Nonzero flag byte 02 does not pass bit 0.

Candidates 15/16 are identifiable for follow-up by exact captured angle bytes:

| Chain | Current candidate key | Longitude/latitude byte pair, LE binary64 | Prior 020 key |
|---|---|---|---|
|15|FF0176BF|3e7c5616334dccbf / 74c911eda75ce0bf|FF017655|
|16|FF01CC24|33fe6f484321ccbf / ac01c6cd5c5fe0bf|FF01CB2B|

All 18 angle pairs match the prior 020 ledger in order, while 17 dynamic keys change;
only candidate 1's static 00325868 key repeats. Thus a different unused landing
changed the source while revisiting the same angular candidate set. This supports
target selection by retained descriptors, not reuse of FF keys across sessions.
It does not prove stable logical object identity. Prior saved-correspondence
receipt finds these angle pairs at decompressed offsets 232427/232457 in Save27
global unit 6; those are **stream offsets**, not file offsets or runtime addresses.
The receipt explicitly leaves tagged-ID/load remapping unvalidated. Neither
candidate is declared SOR-002/SOR-003 or an ordinary beacon on these facts alone.

## Source inputs and what the old prediction now explains

Actual B R8 is packed key`0x02b20e7817a095a0`, identical in all 18 and agreeing with
sampled world+310. Its decoded fields are system 88327, body-index 15, tag 0,
encodedXY38304/6048. Landscape argument is runtime 0x000002e63d1908c0, with sampled
resolution 256 and body field0x0003F59F; block 10, merge 2 and scale bytes 0ad7233c.
These are actual arguments/output and adjacent sampled fields, not a proof of
all temporally atomic upstream component state. B's nonzero complete result
rules out an all-zero initialized-output explanation in these chains.

Prior 020 packed key`0x02b20e7843e090c0` instead encodedXY37056/17376, predicting
coarse 193/90 under old assumptions. Do not compare current candidates against
that obsolete source. Current A geometric fields agree with both earlier AVX/FMA
conditional predictions for all 18; this is scoped agreement on snapped geometry,
not exact trig equivalence, CPU dispatch selection or a full Workshop oracle.

Final geometry uses **context[4]'s angular source**, not B's packed argument.
Captured 24-byte source is
`ea0655ff711aefbf6f51bdb68070c63f63bead58671aefbf`, identical across chains.
Its final exact hierarchy is 0; 199,31; 7,8; 11,1, differing from snapped B.
Final candidate conversions also retain fine detail that A deliberately zeros.
The final native delta therefore cannot be substituted for the E-gating hierarchy.
It is[-23991,6725] for 1,[-23992,6734] for 13,[-2594,30242] for 17;
the other 15 range 21289–21328 /15068–15095 (individual rows in the matrix).
No exact rectangle replay is claimed: Q loads the rectangle into XMM6 before
the observed final helpers, while observer samples shared memory later.

## Recommended next bounded step — qualify one matching-source scenario offline

The best next step is **candidate 15/16 matching-source qualification**, keeping 030
unchanged. The positive flag samples make these more promising than candidates
with only clear samples; both share A geometry but still need a natural matching
source and Q dispatch. This is a research proposal, not permission to execute it.

Use retained Save27/28 correspondence, approved local copies, pinned retail static
state and these two angle descriptors. Limit the audit to source-key production
feeding world+310/AD92E0, overlay lookup/bit 0 lifecycle and the immediate existing
reference versus fallback decision. Trace only those paths needed to choose one
candidate. No broad engine survey, new observer, rebuild or live activity.

Deliverables and finite decision boundary:

1. Resolve at most these two angular candidates to a defensible saved site/reference
   association and ordinary-Workshop eligibility, or record the exact missing join.
   The existing receipt supplies an angle locator only; it cannot fill that join.
2. Trace natural packed-source production and test whether ordinary selection/travel
   can produce A-compatible geometry with matching table/handle fields. A derived
   **counterfactual test vector**, assuming the captured system/body and block sum 12,
   is tag 1/encodedXY10464,21120: packed`0x02b20e79528028e0`. It encodes
   coarse 54/110,sub8/0,fine 0/0. This is necessary geometric compatibility only,
   not a known selectable destination or proof that native B's handles would match.
   Never write this value into game memory or a save, or force a native call.
3. Establish how overlay bit 0 is set/retained and whether one proposed action reaches
   the **Q fallback** with this source/candidate. Inspect immediate 77FC20 existing
   search 77F900 versus 77E350 fallback: visiting an existing populated marker can
   bypass Q entirely. ACCAD0's4595C0→5DDB20 /461F10 /461EB0 lookup alone does not
   explain bit semantics. Retained exports establish these dependencies; this
   assignment has not completed their writer/lifecycle audit.
4. Stop after both candidates and those immediate dependency paths are adjudicated.
   Positive outcome: one source-grounded prospective operator action, exact protected
   save/candidate association, expected all 11 comparisons and flag/collection gates,
   plus a finite 030 run-card proposal. Negative outcome: no qualified scenario and
   a precise missing writer/identity/trigger, with rejected routes documented.
   Resource/input drift or required mutation ends the affected audit; no automatic
   widening, forced calls, save editing or extra landing. Static database inspection
   requires its separately stated read-only tool scope; no symbol/type/comment edits.

Any later live card needs separate review/approval, exact unchanged package locks,
one selected action, bounded health/capture/STOP/normal-exit cleanup and no implied
manual saves. E-boundary 20 would be the minimum reachability success; same-Q E/C/
center/grid and independent saved-frame identity are still required for full oracle
comparison. A healthy E0 result would be scoped negative evidence, not global absence.

| Alternative | Why lower priority now |
|---|---|
|Another arbitrary fresh landing|Two different source locations have revisited the same 18 angular candidates; no evidence it will align with either flag-positive candidate.|
|Return directly to a known outpost|May supply population but existing-reference search can skip Q; current evidence does not identify 15/16 as those outposts.|
|Change observer/force E|030 already records the discriminating gate outputs. Forced execution would change the question and requires new authority.|
|Independent center/grid component acquisition|Valid fallback if the selected full chain cannot be naturally qualified, but does not prove composed Workshop/native equivalence; separate acceptance/scope decision needed.|

## Qualification, preserved failures and review package

Original ignored utility `.local-work/q030-E-next-step/analyze.py` uses CPython 3.14
stdlib plus existing project `decode/raw` and disk/hash helpers. Reads sealed raw,
journal, decoded outputs, lock 05 and prior 020 ledgers; writes exclusive local
analysis.json and the authored 18-row CSV only. No process/save/config/database,
source/tool edits, dependency install or network. Full raw bytes remain LOCAL-ONLY;
small authored field summaries and report are REVIEW-REQUIRED, not publication-cleared.
Existing [source/rights ledger](sources.csv), [credits](../../../CREDITS.md) and
[Q/E provenance](../q-to-e/sources.csv) apply; no new external reuse/contact.

Two exploratory assertions failed and were corrected before outputs were written:
all sampled bits assumed clear (false for 15/16); full 24-byte candidate equality
across sessions assumed (17 dynamic keys differ despite exact 16-byte angles).
Original failed utility versions are retained as analyze-failed-01.py/-02.py.
The decoder was not changed. One shell attempt used an inaccessible WindowsApps
python alias before any baseline/script ran; installed CPython was then used.
These are analysis failures, distinct from preserved live transcription FAILs.
Initial independent review returned REWORK for an incorrect delta-X range and
mojibake from a Windows-default text read during attempted correction. The range
is corrected to 21289–21328 and UTF-8 text repaired; original submission is preserved
in submission-01/. Explicit encoding and mojibake checks were added to packaging.
Raw evidence, matrix, decoder and native files were unaffected.

| Mandatory criterion | Status | Actual check / limit |
|---|---|---|
|1: authenticate and tabulate 18 chains|PASS|144 journal extents/hashes/identifiers, raw decoder equality, 198 ordered fields, packed arguments, 90 flag samples and 18 deltas/returns; 93 seals/310 pins|
|2: reconcile evidence domains and unknowns|PASS|Flag erratum, all 18 prior angles/geometry versus 17 changed dynamic keys; packed versus angular source distinguished; rectangle/equivalence not claimed|
|3: finite next step and alternatives|PASS|Two-candidate offline qualification proposal above, one possible prospective scenario; missing joins/writers explicit; no execution authority|
|4: patches/checks/independent review|PASS|Independent ACCEPT; 30 text files/seven task paths, exact forward patches, 193 internal links, whitespace/encoding, 583-file baseline preservation, 310 pins/93 seals and HEAD/index verified|
|E reached / full native equivalence|NOT TESTED|No new live action; original capture E0, no linked C/center/grid|

Review artifacts are under `.local-work/q030-E-next-step/`; diffs at
`.local-work/diffs/q030-E-next-step-{complete,task-only}.diff`. Package records
exact hashes, status, exclusions, preservation, text/link/whitespace checks and
forward application to disposable plain .local-work/review-patches trees. No staging/commit/push,
deployment/launch/live capture or protected-input changes. No game is running or
absent is inferred by this offline task; prior postflight remains the source.

Independent disposition: **ACCEPT**, reviewed package SHA256
`97986a7a26537b40453764e03e8903677ba259bf1c92873a033366c0cd01d963`.
Actual return retained at `.local-work/q030-E-next-step/independent-decision.md`;
accepted bytes and patches in reviewed-submission/. Reviewer independently sliced
all 144 raw records with stdlib (without project decoder), checked 198 comparisons,
90 flags/18 deltas, primary CFG, 30 text hashes, 20 source members, 93 sealed members
and 310 pins. Exporter executed forward patch application; reviewer independently
checked resulting trees and patch identities. Initial REWORK and original bytes
remain in independent-rework-01.md/submission-01/. This final disposition-only
report/state refresh receives a separate consistency check; no scientific change
or new live/native-equivalence claim.
