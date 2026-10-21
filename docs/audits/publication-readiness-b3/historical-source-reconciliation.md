# Historical source identity reconciliation

**26/26 RR1-021 occurrences: EXACT RECOVERED.** All 23 literal source paths retain
their original citations and SHA-256 pins. Each current file is a
**CHANGED/CURRENT DISTINCT** version. A recovered hash establishes byte identity,
not semantic equivalence or permission to execute an old helper.

The [occurrence ledger](historical-source-reconciliation.csv) records original
CSV/line/column, expected hash, RR1 observed hash, freshly observed current hash,
historical size, exact recovered locator, matching candidate count, affected
claim, reproduction impact and public-access limit. Repeated c3-fuel,
e1-intervals and r1-robots references are separate occurrences; absolute/relative
aliases remain separate literal paths. No old source ledger is edited.

The bounded search used RR1's 15,518-row tracked/local source metadata inventory,
restricted to actual files with the mismatched source basenames, and real Git
history of the three tracked paths. Candidate bytes were independently hashed;
matching copies were reopened and rehashed. This did not infer source identity
from receipt text, filename similarity, timestamps or a current script passing.
Full candidate identities/search results remain in local
`.local-work/b3/historical-candidates.json`; no snapshot or repository was deleted.

Twenty-three occurrence decisions select byte-identical local source snapshots.
The protected pre-housekeeping tree under
`.local-work/review-scratch-housekeeping/before/` recovers the changed packagers;
other exact copies also exist. OutpostRecon, resource_availability and its review
exporter are recovered from actual Git commits recorded in the CSV; their local
snapshot matches are also retained in the search receipt. No uncommitted source
is assumed to have entered Git history.

Package/exporter revisions mostly control review packaging and output locations.
Their exact source is retained locally and is not necessary to rerun a scientific
parser, so it is not promoted merely to publish every historical artifact.
OutpostRecon and resource_availability are scientific exporter/reader revisions:
the ledger explicitly distinguishes their historical bytes from today's source.
Use the exact historical locator for inspection; do not silently substitute the
current implementation. Local-only historical source access remains a release
limitation even though acquisition of those identities is closed.

Every selected promoted candidate with a recognized historical SHA-256 in the
claim-led census matched that citation at selection time. This bounded related
check found no additional selected-source mismatch to substitute or conceal.
Unselected source leads retain their declared/current identities in
[source-selection.csv](source-selection.csv); this is not an all-repository
historical-source closure claim.

Historical evidence integrity is unchanged: original source pins, raw outputs,
saved observations, prior failures and interpretations are untouched. Recovery
removes an identity uncertainty; it neither reruns those experiments nor upgrades
confidence, corpus completeness or publication eligibility. B6 must separately
assess which history/source versions are actually included in a release.
