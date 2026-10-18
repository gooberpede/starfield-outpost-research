# Codex rework brief — CR1 current crew assignments and saved destination correspondence

**Project:** `starfield-outpost-research`  
**Type:** Focused corrective continuation of CR1 (not CR2/CR3 or a new general save-decoder project)  
**Status:** CR1 uncommitted; maintainer review requires REWORK on saved *current* crew membership and assignment identity  
**Authority:** Read-only offline native, script, definition and protected-save analysis; scoped research aids, tests, documentation and independent review. **No** game launch, live attachment, new gameplay/save generation, save mutation, observer deployment, staging, commit or push. Preserve all original CR1 work and earlier failures.

## 1. The critical distinction and question

The maintainer does **not** request historical assignment changes or a timeline of where crew previously served. The CR1 gap is more basic:

> Can the game's **current assignment state** be recovered from a save: which recruitable actor is assigned versus unassigned, and, if assigned, which particular outpost or ship is their destination?

This state is available to the running game's Crew screen and must have some persistence/reconstruction explanation. Establish the authoritative saved representation and join to actor and location identities where the evidence permits, rather than merely naming a native serializer. Distinguish **available/recruited**, **assigned**, **travelling**, **physically present**, and **contributing effective bonuses**; these are not interchangeable. The mandatory target is current assignment and destination, not current effective bonuses or exact actor position.

### Required answer-first summary

Report plainly whether each of these is **demonstrated from real saves**, **native-only mapped**, or **not yet established**: (1) individual crew identity; (2) unassigned versus assigned status; (3) outpost versus ship destination; (4) destination's unique identity; (5) whether saved relationships are fully authoritative or reconstructed using definitions/VM data. Include positive examples and exact counterexamples; a missing decoded field is **unknown**, not unassigned.

## 2. Sources and corpus strategy

Read the currently **uncommitted** CR1 package (`docs/experiments/crew/report.md`, `saves.md`, `lifecycle.md`, `screen.md`, `coverage.md`, `review.md`, native/function/source registers and research aids), its governing brief and user-added Crew-screen scope, `WORKFLOW.md`, `docs/EVIDENCE_STANDARD.md`, `docs/RESEARCH_EXECUTION_PROTOCOL.md`, and the compact completion contract. Reuse accepted Workshop ownership/identity, save framing, reference queues, Extra4C and native actor/VM evidence as appropriate. Verify installed build/source and protected hashes, not remembered paths.

**Do not make Save52 the principal positive-assignment sample.** Search the project's **earlier mature saves** systematically, prioritizing ones likely to contain currently assigned named or generic crew. Identify candidate saves from existing corpus metadata, chronology and available gameplay/context evidence before reading; record why each was selected and keep their original names/hashes. Save52 is valuable as a **potential negative comparison**, but neither its apparently vacant outposts nor the absence of `ExtraE2` on sampled beacons establishes that no crew were assigned. Qualify any negative control independently; never select or label controls by assuming the desired result.

The prior CR1 scan of Save52, HIST-0036 and HIST-0077 found no `ExtraE2` on 54 sampled ordinary beacon records and no qualified queued `CrewAssignment` link. That result is retained, not reinterpreted as a global absence proof. Earlier mature originals must not be dismissed simply because this narrow scanner returned zero.

## 3. Native persistence and reconstruction chain

Trace the actual assignment **writer, save serializer, loader, post-load fixup and Crew-screen reader** at the representation grain needed for reconstruction. Existing leads include destination crew lists (`ExtraE2`), actor `CrewAssignment` linked-reference (`Extra4C`, keyword `0026beac`), crew registry/availability data, VM/script properties, change records and default/base relationships. Treat these as hypotheses to verify, not an exclusive schema.

Specifically establish:

- Which reference owns each side of the relationship (actor, Workshop/beacon, ship, manager/quest/VM); which side is authoritative for a save import and how disagreements are handled.
- Whether `ExtraE2` is saved on the Workshop, on a child/reference other than the beacon, or only in a conditional representation; distinguish absent, default, zero-count, queued and unresolved values.
- How generic recruited crew instances and named crew identities are serialized and resolved, including base NPC versus placed actor and dynamic saved FormID versus runtime handle.
- Whether script state, linked-reference data, actor change records, or restored registries carry assignments when no matching beacon extra is present. Account for compressed/alternate reference or extra representations before declaring an absence.
- How the Crew screen's actual source of assigned/unassigned/location rows maps back through restored runtime state to persistent inputs. The UI proves runtime availability of the data, not the particular save record that contains it.

Favor concrete producer→wire→loader→consumer evidence. Avoid unbounded reverse-engineering of unrelated actor/VM behavior or rebuilding a universal actor decoder. If a new scoped reader is needed as an *evidence aid*, it may be adapted/implemented under existing offline authority; **no production-grade importer** is authorized or requested.

## 4. Real-save demonstration and controls

Seek at least one **positive, independently identified** assigned-crew example in an earlier mature save, preferably with a known outpost/ship and a different member that is unassigned or assigned elsewhere. For each qualified row provide:

| Actor | Saved actor/base identity | Assignment status | Assigned destination (saved + resolved outpost/ship) | Exact saved fields/offsets and decoding | Independent corroboration | Limit |
|---|---|---|---|---|---|---|

A successful claim requires a noncircular actor→destination join. Do not infer assignment solely from standing near an outpost, crew skill eligibility, a generic script/default, a station count, or a player's recollection without a matching saved relationship. Establish negative controls by a *positive unassignment marker or qualified complete enumeration*, not only missing E2/4C on one record class.

Use a different save or a distinct control where practicable to cross-check the serialization grammar and interpretation. Distinguish a change over time from a static current assignment; historical transition reconstruction is out of scope.

**If no positive witness exists in the available mature corpus:** document the saves/representations tested, concrete reason why the corpus cannot answer, and the smallest *player-only* controlled-save pair that would discriminate the remaining models (for example, the same named actor unassigned and then assigned to a uniquely known outpost, with retained originals). Do **not** execute it. This is a specific user-input escalation, not scientific closure or a license to claim current assignments cannot be recovered. Complete all independent authorized native/wire work first.

## 5. Completion and evidentiary standard (frozen)

Apply reasonable engineering confidence and explanatory sufficiency, not exhaustive proof against imagined alternatives. But do not call a current-assignment save model complete based solely on a plausible native serializer with **no** identified saved instance. Explicitly separate *research task completed* from *the saved assignment question resolved*.

**Mandatory criteria:**

1. Explain current runtime assignment membership, destination resolution and unassigned distinction, using concrete native/UI consumer paths and current CR1 evidence.
2. Establish the actual save/load representation(s) and actor/location identity join under supported conditions; identify any concrete alternate or default branches that matter to the claim.
3. Examine and document a justified earlier-mature-save corpus, retaining Save52 as a qualified comparison rather than the presumed principal positive sample.
4. Demonstrate at least one independently grounded real saved current actor→outpost/ship assignment and an appropriate control **or**, on an evidence-backed corpus shortfall, leave that scientific result OPEN and provide the minimal discriminating controlled-save request. Do not label this fallback an affirmative assignment reconstruction.
5. Produce a compact runtime-to-save capability matrix clearly distinguishing assigned, unassigned, unknown, and destination-unresolved; preserve all previous CR1 conclusions and historical failures without retrospective changes.
6. Update the CR1 report/saves/lifecycle/screen/review and appropriate indexes only where warranted; retain provenance, byte locators, build pins, coverage and realistic limitations. CR2 skill contribution and CR3 remote participation remain separate.
7. Execute scoped offline validation and relevant existing regressions; prove protected inputs, analysis databases and Git HEAD/index remain untouched; audit authored text for encoding, links and whitespace.
8. Obtain independent review against **this correction and the original CR1 contract**, with a criterion-by-criterion PASS/FAIL/NOT TESTED matrix; deliver task-only and combined complete textual diffs including all untracked text, exclusion inventory, manifest/hash receipts, and exact forward/reverse reconstruction checks. Do not stage or commit.

**Continuation:** Diagnose in-scope failures and repair/retest without requiring a new brief. Do not stop at the first failed decoder assumption. **Escalation:** stop only the action requiring unavailable save evidence, new gameplay/live authority, or a real integrity/safety gate; preserve results and specify the minimal required user action and resume point. Maintain the existing C:/D: free-space, protected-save and source-permission safeguards. Avoid arbitrary time/event/evidence quotas. A genuine NO-WITNESS corpus result is acceptable as a bounded negative *search result*, not a positive demonstration of recovered assignments.

**Handoff:** First paragraph must answer whether CR1 current saved assignments can now be reconstructed and from which sampled saves. If still open, explain the specific missing discriminator and why, without treating assignment history as the problem. Do not automatically move to CR2, create a live observer, or claim commit readiness without maintainer review.
