# SOR Research Brief — Output-Link Remove/Recreate Validation (L0–L2C)

## Purpose

Validate the provisional output-link interpretation from the S0–S7C corpus using a controlled reversible relationship experiment.

The central prediction is:

```text
link present
    -> candidate relationship motif present

link removed
    -> candidate relationship motif absent or predictably changed

link recreated
    -> candidate relationship motif present again
```

This task is deliberately **offline analysis only**.

Do not launch Starfield, deploy SFSE, attach a debugger, modify live saves, stage, commit, or push under this brief.

The immediate goals are:

1. archive and verify the new link-validation saves;
2. distinguish cross-session/reload churn from within-session action/control churn;
3. test whether the previously identified S4 relationship motif follows the expected present → absent → present lifecycle;
4. determine whether the relationship appears to be represented as a property of one endpoint, both endpoints, or a separate edge/list/relationship structure;
5. strengthen or reject the current provisional output-link semantic assignment.

---

## 1. Source saves

The live originals are currently in:

```text
C:\Users\User\Documents\My Games\Starfield\Saves\
```

The user intends to leave them there temporarily because Starfield saves are Steam-cloud-managed and eventual cleanup should be performed through the game.

Create verified **copies only** under the ignored project-local research area, for example:

```text
.local-work/savegames/
```

Do not move, delete, rename, or alter the live originals.

The corpus is:

```text
L0 - historical linked baseline = prior S4C / Save13
Save13_D6036588M417474696C61204B6972616C79_000219_20261007082801_3_0_4.sfs

L0C - new-session linked no-action baseline/control
Save20_D6036588M417474696C61204B6972616C79_000219_20261007100746_3_0_4.sfs

L1 - unlink extractor/storage
Save21_D6036588M417474696C61204B6972616C79_000219_20261007100826_3_0_4.sfs

L1C - no-action control after unlink
Save22_D6036588M417474696C61204B6972616C79_000220_20261007100840_3_0_4.sfs

L2 - relink extractor -> storage
Save23_D6036588M417474696C61204B6972616C79_000220_20261007100900_3_0_4.sfs

L2C - no-action control after relink
Save24_D6036588M417474696C61204B6972616C79_000220_20261007100920_3_0_4.sfs

exit - incidental terminal sample
Exitsave0_D6036588M417474696C61204B6972616C79_000220_20261007100930_3_0_4.sfs
```

---

## 2. Important experimental interpretation

`L0` is **not** a normal same-session no-action control.

It is the earlier `S4C` save from the prior manual corpus and serves as a **historical linked-state anchor**.

`L0C` is the actual baseline/control for the new session.

Treat the comparisons as:

```text
L0 -> L0C
    cross-session / reload / elapsed-time churn
    while the extractor->storage link should remain present

L0C -> L1
    deliberate unlink action

L1 -> L1C
    no-action control in unlinked state

L1C -> L2
    deliberate relink action

L2 -> L2C
    no-action control in relinked state
```

Do not interpret `L0 -> L0C` as equivalent to the within-session no-action controls.

This distinction must be recorded durably.

---

## 3. Archive and manifest requirements

Before analysis, copy every new source save into the project-local ignored research area.

For each source/original and project-local copy, record:

- checkpoint label;
- semantic description;
- exact filename;
- source path;
- local-copy path;
- file size;
- relevant filesystem timestamps;
- SHA-256;
- copy-verification result;
- action/control/historical/incidental classification.

Verify:

```text
SHA256(live original) == SHA256(project-local copy)
```

before using the copy for analysis.

For `L0`, existing archived/verified S4C evidence may be reused if it already satisfies the project evidence standard. Do not duplicate raw evidence unnecessarily.

The exit save should be classified as:

```text
INCIDENTAL_TERMINAL_SAMPLE
```

Raw `.sfs` files must remain ignored/untracked.

---

## 4. Prior hypothesis under test

The previous S0–S7C analysis identified a provisional relationship motif associated with:

```text
S3C -> S4
extractor -> storage output-link creation
```

and observed that the motif later disappeared/changed when the extractor was deleted at S7.

That evidence is suggestive but not independently sufficient because S7 also removed one endpoint.

This experiment is intended to isolate **relationship state only**, while keeping the principal objects intact.

Consult the existing durable corpus analysis and exact prior candidate structure/offset/token definitions.

Do not redefine the S4 candidate after seeing the new data merely to make the result fit.

The prior candidate must be treated as a preregistered target where practical.

---

## 5. Primary predicted lifecycle

The strongest predicted outcome is:

```text
L0 / L0C
    link present
    candidate relationship motif present

L1 / L1C
    link absent
    candidate relationship motif absent or consistently changed

L2 / L2C
    link restored
    same candidate relationship motif restored
```

The most persuasive pattern would therefore be:

```text
PRESENT
PRESENT
ABSENT
ABSENT
PRESENT
PRESENT
```

for the same logical relationship representation.

Do not require byte-for-byte identical physical offsets if the save/container format causes layout movement.

Prefer logical structure/identity over absolute file offset where possible.

---

## 6. Core comparisons

Perform and document at least:

```text
L0 -> L0C
L0C -> L1
L1 -> L1C
L1C -> L2
L2 -> L2C
```

### A. Cross-session control: L0 -> L0C

Purpose:

- characterize reload/session churn;
- confirm the linked-state candidate survives across sessions if applicable;
- identify which differences are unrelated to unlink/relink semantics.

Do not count this as an action validation transition.

### B. Unlink: L0C -> L1

This is the first decisive transition.

Ask:

- does the prior S4 relationship motif disappear/change?
- do the candidate extractor/storage identities remain?
- do any relationship counts/list lengths change?
- does one endpoint record change more than the other?
- does a separate relationship/edge structure disappear?
- are there secondary production/resource changes?

### C. Unlinked control: L1 -> L1C

Ask:

- does the candidate unlinked state persist?
- which changes are ordinary no-action churn?
- does any transient unlink-related state settle?

### D. Relink: L1C -> L2

This is the second decisive transition.

Ask:

- does the same relationship motif return?
- does it return with the same endpoint/object identities?
- does the same list/count/edge representation reverse predictably?
- is the new state structurally comparable to L0C and/or historical L0?

### E. Relinked control: L2 -> L2C

Ask:

- does the restored state persist?
- are any differences merely transient post-link churn?

---

## 7. Endpoint identity must remain separate from relationship identity

The principal objects should remain present throughout the new experiment:

```text
beacon
storage
extractor
solar array
```

Use the strongest prior candidate identities from the S0–S7C corpus to verify this where possible.

The key scientific distinction is:

```text
object remains
+
relationship changes
```

rather than:

```text
object disappears
```

If endpoint candidate structures unexpectedly change/disappear, document the contradiction before interpreting the link candidate.

---

## 8. Relationship representation questions

If the motif validates, characterize its likely representation without overclaiming.

Possible models include:

```text
A. relationship stored on extractor only
B. relationship stored on storage only
C. mirrored relationship stored on both endpoints
D. separate edge/relationship record
E. list/array owned by workshop/outpost
F. count + entry pair
G. indirect/token/reference relationship
```

Do not choose among these solely from intuition.

Base the interpretation on which logical structures change across unlink/relink.

If endpoint identifiers or reference-like values appear inside the relationship candidate, document them exactly.

---

## 9. Production/resource-state confound

The extractor may be powered and producing iron.

Unlinking/relinking may therefore alter secondary state such as:

- extractor output buffer;
- storage contents;
- production timers;
- resource counts;
- transfer state.

Do not assume every changed byte in `L0C -> L1` or `L1C -> L2` is part of the relationship representation.

Use:

```text
L1 -> L1C
L2 -> L2C
```

to identify transient/background changes where possible.

If the previous S4 motif reverses cleanly while nearby production values continue changing, that is useful evidence in favor of the motif representing relationship state rather than production quantity.

---

## 10. Compare against historical S4 evidence

Where practical, compare the new relink transition:

```text
L1C -> L2
```

against the original creation transition:

```text
S3C -> S4
```

Ask whether the same logical structure appears in both.

Also compare the linked steady states:

```text
S4C / L0
L0C
L2
L2C
```

If the same motif persists across:

- original link creation;
- session reload;
- unlink removal;
- relink recreation;

that is very strong evidence.

---

## 11. Evidence classification

Use explicit evidence levels.

Examples:

```text
OBSERVED:
A specific token/record/motif is present in L0C, absent in L1/L1C, and present again in L2/L2C.

INFERRED:
The structure likely represents extractor->storage relationship state.

HYPOTHESIZED:
A contained identifier may be the extractor endpoint and another the storage endpoint.
```

Do not silently promote inference to fact.

If the predicted lifecycle fails, preserve the negative result.

---

## 12. Promotion criteria

A stronger semantic assignment may be justified if all or most of the following hold:

1. prior motif appears in linked baseline;
2. unlink removes/changes it;
3. unlinked control preserves the unlinked state;
4. relink restores the same logical motif;
5. relinked control preserves it;
6. endpoint object candidates remain present;
7. the behavior matches the original S4 link-creation transition;
8. ordinary no-action churn does not explain the pattern.

If supported, propose an appropriate promotion in the project findings/state registers.

Do not promote automatically; explain the evidence basis.

---

## 13. Failure/alternative outcomes

If the prior S4 motif does **not** behave as predicted, classify the result.

Possible interpretations include:

```text
- prior motif was not the output link
- motif represented transient link-creation state only
- link state is stored elsewhere after creation
- unlink operation does not fully remove serialized relationship state
- relink generates a new logical relationship identity
- physical offsets shifted and matching logic failed
- endpoint/production changes confound the candidate
```

Recommend the smallest next discriminating analysis rather than inventing a new broad parser.

---

## 14. Tooling

Reuse existing manual-corpus tooling and scripts where practical.

Small offline additions are acceptable if directly useful for:

- manifesting;
- hash verification;
- save decomposition;
- structured diffing;
- shift-tolerant candidate tracking;
- relationship lifecycle comparison;
- token/reference correlation.

Do not build unrelated general infrastructure.

No live debugger work is authorized.

No SFSE deployment is authorized.

---

## 15. Desired outputs

Produce at minimum:

### A. Link-validation manifest

Verified provenance for L0C–L2C and exit sample, with L0 linked to its existing historical evidence.

### B. Transition summary

Quantitative/descriptive summary for:

```text
L0 -> L0C
L0C -> L1
L1 -> L1C
L1C -> L2
L2 -> L2C
```

### C. Prior-motif lifecycle table

A compact table showing whether the exact prior S4 relationship candidate is:

```text
present / absent / changed / unresolved
```

at each checkpoint.

### D. Endpoint-persistence analysis

Confirm whether candidate extractor/storage structures remain present throughout.

### E. Relationship-structure interpretation

Describe whether the evidence best supports:

```text
endpoint-owned
mirrored
separate edge/list
unknown
```

### F. Cross-session persistence result

State whether the linked relationship candidate survives from historical S4C/L0 into new-session L0C.

### G. Semantic recommendation

Recommend:

```text
promote
retain provisional
reject
```

for the current output-link hypothesis, with reasons.

### H. Next-step recommendation

Recommend the smallest next experiment or analysis only if needed.

---

## 16. Success criteria

This experiment is successful if it materially discriminates the output-link hypothesis.

The strongest success case is:

```text
linked      -> motif present
unlinked    -> motif absent
relinked    -> motif present
```

with endpoint object candidates otherwise persistent.

A negative result is also scientifically useful if it clearly rejects or narrows the prior interpretation.

---

## 17. Live-save cleanup

Do not delete the live originals.

The user will clean up the Steam-managed save directory manually/in-game after archival and review.

---

## 18. Git and artifact policy

Do not:

- stage;
- commit;
- push;
- track raw `.sfs` files;
- modify live originals.

Generated summaries/manifests/scripts/documentation may be tracked if consistent with repository policy.

Raw save copies remain under ignored local-work/evidence paths.

---

## 19. Validation

Before returning:

- verify every new project-local save copy against its live original by SHA-256;
- verify L0 historical anchor provenance;
- verify originals remain unchanged;
- verify no raw `.sfs` became tracked;
- run `git diff --check`;
- validate internal Markdown links if documentation changed;
- inspect `git status --short`;
- record all new scripts/tool outputs and locations.

---

## 20. Return for review

Return:

1. exact manifest/copy-verification status;
2. L0 historical-anchor provenance;
3. transition metrics for all five comparisons;
4. prior S4 motif lifecycle across L0/L0C/L1/L1C/L2/L2C;
5. endpoint persistence result;
6. cross-session persistence result;
7. unlink result;
8. relink result;
9. no-action-control behavior;
10. relationship representation interpretation;
11. observed vs inferred vs hypothetical distinctions;
12. strongest current semantic conclusion;
13. alternative explanations;
14. recommendation to promote/retain/reject the output-link hypothesis;
15. next smallest experiment/analysis if needed;
16. files changed;
17. checks run/results;
18. `git diff`;
19. `git status --short`.

Do not commit or push.

Suggested commit message only if later approved:

```text
research: validate outpost output-link serialization
```
