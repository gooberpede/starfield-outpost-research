# R1 prose spacing correction

2026-10-18. The maintainer requested an occurrence-by-occurrence review of the
uncommitted documentation after finding missing spaces between prose words and
numbers or identifiers. This is an editorial correction; the research scope,
evidence, numerical values and scientific conclusions remain unchanged.

The review covers all newly authored R1 Markdown, the R1 additions to existing
documentation, and the human-readable descriptions in the native function CSV.
The supplied frozen brief, previously committed historical prose, exact editor
IDs, code, source paths, hashes and evidence records retain their original text.
No game, analysis project or save was opened or changed for this correction.

Each replacement was selected after reading its context. An explicit literal
edit list records every affected occurrence and reason in the ignored local
directory `.local-work/r1-prose-spacing/`; no regex or general spacing rule was
used to modify the documents. The initial uncommitted tree was snapshotted there
before edits, so the correction can be reviewed separately from the R1 research.

| Case | Editorial determination |
|---|---|
| ModelA01, ModelA03, ModelS01 and related prose labels | Use Model A01, Model A03 and Model S01 for readability. These are prose labels, not renamed game records. Exact editor IDs such as `OutpostRobotModelS01` remain intact in the catalogue. |
| ModelS011d8ee5 | The instance/base CSVs identify Model S01 with base `1d8ee5`. Write Model S01 (`1d8ee5`). |
| ModelA04337eab | The instance/base CSVs identify Model A04 with base `337eab`. Write Model A04 (`337eab`). |
| actorff07258a / ownerff062012 | Separate the prose label from its exact saved ID: actor `ff07258a` / owner `ff062012`. |
| threshold3, rank2, operation3 and similar prose | Separate the word from the value after examining the sentence. Native addresses and numeric values are preserved. |
| virtual40 / virtualA0 | Express these as virtual methods at byte offsets +40 / +A0, consistent with the existing hexadecimal offset domain. They are not decimal slot indices. |
| Save52 | Retain the established sample identifier. The unchanged supplied brief contains this example. |
| ExtraBC, Extra2B, ExtraE2, Extra4C and Extra9C | Retain the established extra-data tag notation. The suffix belongs to the technical label. Prose such as “beacon E2” has a separate word boundary. |
| A1, DB, CR1–CR3, E1–E3, P1, S2, R8, 3D, binary32 and SHA256 | Retain valid dispatch codes, project IDs, register names and technical notation. |
| Opaque Actor15 tail | Use “opaque actor extra `15` tail” to distinguish an extra-data tag from an actor identity. Retained parsing locates tag `15` after the first 4C/1F. Its contents and grammar remain unclosed. |

Validation is limited to the editorial change: exact literal edit accounting,
manual rereading, CSV identity/locator preservation, current source-ledger pin
maintenance, UTF-8/newline/whitespace and internal links, unchanged Git HEAD/index,
and complete/task-only patch coverage with exact forward/reverse reconstruction.
Research acquisition and gameplay regressions need no rerun for prose changes.
The earlier R1 verification and independent decisions remain historical records.

Independent review and final package identities are retained locally in
`.local-work/r1-prose-spacing/`. Their actual verdict controls acceptance of this
correction; the earlier R1 ACCEPT does not automatically cover these edits.
No staging, commit, push, integration or publication is authorized.
