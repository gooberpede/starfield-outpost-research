# Editorial and validation record

The complete changed-file inventory and per-file exact hashes are in
`.local-work/diffs/d5by-final-manifest.json`. The supplied brief belongs to
the complete patch only. The editorial checker and exact-file export use
the actual Git changed/untracked set. The validation outputs are retained
under ignored `.local-work/d5by-documentation/`.

| Changed prose inventory | Manual checks |
| --- | --- |
| Root README, documentation index, roadmap | Read all changed paragraphs and tables with their landing targets. Checked all three routes, naming and scoped baseline. Corrected the stale B3 current route. |
| Guide index, authoring standard, Cargo, Fabrication, Identity, Inorganic production, Organic production, Power, Resource generation and Storage/output links | Read the changed paragraphs and source contexts. Checked named gates, missing glossary terms and diagrams. Linked PackIn on first use. Corrected an obsolete roadmap fragment. |
| Technical index, access and framing, Cargo, Construction, Displays, Crew, Defense, Fabrication, Identity, Locations, Nominal biomes, Organic production, Position, Resource generation, Storage/output links and Stored Resources | Read each changed context, technical link and evidence boundary. Preserved exact original pins for the separate power, inorganic and shared-storage technical documents. |
| First-release scope, Evidence access, History index, Research IDs, save aliases and glossary | Read the complete additions and tables. Corrected the Feynman V site granularity, exact native host/effect recipe, time/identity domains and history coverage. |
| Claim and route lookup tables | Read the inherited and selected evidence wording in context with the original ledgers and the generated cells. Checked report/authority destinations, attribution and the native, tracked and historical wording. Removed duplicate punctuation and replaced bare administrative batch locators with actual method routes. |
| D5BY audit Markdown | Read the full new records including the authority/reading and dependency rationale, ledger, term record, reader outcomes and review dispositions. |
| Reader dependency and identifier CSVs | Read headers, labels and disposition text. Checked exact machine paths and source IDs separately from prose. Verified that the scripts regenerate the data. |
| Validator and census sources | Read explanatory comments, docstrings and diagnostics. Confirmed scope, exact-case path behavior, counts, citation classifications and effects. |

The changed-prose checker initially treated raw filenames as joined prose.
Readable study labels replaced bare filenames in links. The dependency CSV
now declares its two opaque locator fields as paths. The remaining warnings
from the earlier check are retained in the first snapshot record. A structural
parser covers the simple Mermaid flowchart grammar present in the guides and
references. Visual rendering remains a separate B6 check. Read the two new
plain-text diagrams against the power and cargo evidence.

The validators use the Python standard library and current Git file names.
They read authored documentation and metadata and write output only to
stdout. The census producer writes no files. The caller captured its CSV
output as tracked authored tables. No method runs a game, native fixture,
old acquisition program or original save decoder. These checks establish
navigation and consistency of the authored surface within the declared
patterns. Independent comprehension and scientific review are separate.
