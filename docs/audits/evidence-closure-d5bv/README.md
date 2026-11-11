# First-release evidence verification and publication handoff

**Publication is NOT READY / NOT CLEARED.** Prior accepted work qualifies
the 68 selected evidence routes at their specific local tiers. No new
scientific execution took place in D5BV. The frozen release candidate,
durable reader access, independent B6 and release authorization remain open.

| Frozen question | Result submitted for independent review |
| --- | --- |
| D5BV-Q1 | The current view maps all 126 selected claim-to-route relationships to 68 distinct routes. D5BU review06 accepted all 14 original-witness and method routes, including both D5BT reader integrations. |
| D5BV-Q2 | The overlay preserves all 71 claims, 31 actions and 110 edges and their inherited dispositions. Read it alongside the original D5BG proposal for today's local verification and release status. |
| D5BV-Q3 | Static planetary data, coordinates and resource definitions alone do not determine the next construction episode's geometry. The prospective scope decision preserves D5AG's historical blocked questions and keeps its fixed-stage method conditional. |
| D5BV-Q4 | The handoff lists the seven candidate assets, conditional and source-only routes, and the decisions and observable checks required from item 7 through release. |

[Frozen brief](../../implementation-briefs/CODEX_BRIEF_SOR_RG2_D5BV_First_Release_Evidence_Verification_Closure_and_Publication_Handoff.md) ·
[Current routes](routes.json) · [Item 7 handoff](item7-handoff.md) ·
[Investigation ledger](investigation-ledger.md) · [Independent review](review.md)

## Reading the current view

`routes.json` extends the proposal as a separate, versioned document.
Existing D5BG files and their consumers retain the original schema. Route
keys use the exact D5BR IDs. `prior_evidence_record` and
`d5bu_evidence_record` are JSON Pointers into the pinned D5BR and D5BU
files in `sources`. Use the D5BR pointer for the assertion, qualification,
negative controls, original source pins and scope. Use the D5BU pointer
for the executed reader, selected members, scope, controls and receipt
locators with SHA-256. The receipt index and source manifest bind the prior
read, preservation and method evidence. D5BT and D5BS review flags identify
additional accepted records. `members_by_asset` uses the original selector
domain. Resolve each ID or name through the controlling member index.

Read `claims` for the selected tier, original claim status and inherited
actions across all 71 claims. Its `selection_record` points to the exact
wording in D5BR. Each route's claim `relation` distinguishes an inherited
root, selected prerequisite and replacement root. The 31 `actions` rows
show each affected claim's selected and locally verified routes alongside
the inherited action kind and edge states. An inherited edge can be
selected by another claim while remaining deferred or supporting for the
claim at hand. For example, the selected N2 comparison supplies no
release or verification pass for D5AQ's deferred Option C route. The
D5BG action ledger retains the original options and acceptance evidence.
Direct and transitive edge dependencies are explicit.

The 54 previously qualified routes comprise 53 prior selected-tier
qualifications and one conditional native host qualification. The 12
previously awaiting verification and two previously blocked are now the
14 accepted D5BU routes. Zero selected original reader barriers remain.
Zero release routes are cleared. Forty-two inherited edges are outside
the selected inventory. The D5BG totals of 3 READY, 38 READY — QUALIFIED,
12 ACTION REQUIRED, 14 MAINTAINER DECISION and four HISTORICAL ONLY
describe the inherited proposal. [D5BR](../evidence-readiness-d5br/review.md) ·
[D5BT](../reader-qualification-d5bt/review.md) ·
[D5BU](../original-save-verification-d5bu/review.md)

D5BU qualifies the named position and nominal-biome checks, the representative
fabricator and SD2 witnesses, scoped cargo and Workshop root observations,
Save29's ordered power calculation, L-series saved windows, the displayed-item
join and selected variants and placement controls. The first historical helper
intake lacks a full pin. Later source-only runs have a complete protection bracket
for those runs. The original missing measurement remains absent.
[Accepted batches and limits](../original-save-verification-d5bu/README.md)

## Selected tiers and scope

D5AT Option A uses the tracked tables and attributed historical fixed-input
comparisons. E3's 105 positive saves and 1,190 producer-row observations and
SD2's 124 positive saves and 1,499 inline-base records retain their historical
census scopes. Their narrower original checks cover the selected witnesses.
D1 retains the attributed saved-state tier and independent transcribed
comparison. The Save29 trial loads, private cargo comparator, reported D1
incident and larger C19 upstream preview remain historical only. Stronger
full-corpus, exact D5AT, D1, three-load, full C18 and extra SD2 trio replays
retain their individual held or excluded tiers.
[D5BP](../publication-decisions-d5bp/README.md) ·
[D5BQ](../publication-decisions-d5bq/README.md)

The [prospective resource-generation decision](../../DECISIONS.md#d5bv-practical-resource-generation-predictability--2026-11-11)
controls current scope. The fixed-stage D5AG method depends on D5AS and the
documented host and lawful game inputs. D5BJ and D5BM remain stopped or deferred
under their original decisions. D5AQ Option C remains a stronger unfinished
route. [D5BO method](../public-evidence-d5bo/d5ag-reader.md) ·
[D5BN deferral](../d5bm-deferred-d5bn/README.md)

## Metadata checks

From the checkout root, run these standard-library commands with the local
Python executable. Both read tracked text and metadata and write only to
stdout. Neither command opens an evidence asset or invokes a reader.

```text
python -I -B docs/audits/publication-claims-d5bg/verify.py --negative-controls
python -I -B docs/audits/evidence-closure-d5bv/verify.py --negative-controls
```

The new checker compares the overlay with the actual D5BG graph and the
selected D5BR/D5BU inputs. Its negative controls reject missing routes,
incorrect claim joins, hosted or cleared status, historical replay promotion,
wrong asset assignment, dropped transitive prerequisites and a shared edge
incorrectly selected for a different claim. It rejects type changes that
Python would otherwise compare as equal. The linked reviews supply the
evidence of actual method execution and findings.
