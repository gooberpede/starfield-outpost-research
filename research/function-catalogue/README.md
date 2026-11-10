# Reproduce a native function catalogue edition

Use a checkout of the modernized tooling with local Git objects for the edition
you select. The verifier uses Git with lazy fetching and replacement objects
disabled and uses the Python standard library. D5BS tested Git 2.53.0.windows.1
and CPython 3.14.3. The exact build requires only Git, Python, the scripts and
manifests in this directory, and the selected local Git objects.

## Accepted D5BD edition

From the repository root:

```text
python -B research/function-catalogue/verify.py
```

This verifies the [D5BD manifest](editions/d5bd.json) and regenerates all 16
outputs in memory. It compares the output bytes with both the manifest and the
accepted Git blobs, then prints the SHA-256 of each result. It reads source
bytes from commit `6e799a428a765aa196a24d3c1de8ae133260aa08`, tree
`7a1f6fdd6728a8f98bc92ef7ee6c9b24a62f0e0e`. The same command in a checkout
of that commit runs the original verifier against the original checkout.
The modern verifier can run from a later checkout and compares against the
accepted Git blobs. The installed working-tree copies are separate from that
comparison. The [public catalogue](../../docs/functions/README.md) and
[D5BD audit](../../docs/audits/native-function-catalogue-d5bd/README.md) retain
their original paths. The modern verifier refuses historical writes.

If a shallow clone or archive lacks the pinned objects, obtain the exact
objects from a separately approved source before running the verifier.
Availability of this history in a future release depends on the approved
exposure and the [publication run card](../../docs/PUBLICATION_RUN_CARD.md).
The tool fails with a Git error when the required local objects are unavailable.

## Technical edition

The [test manifest](editions/test-d5bs-v1.json) explicitly admits the source
set at D5BR HEAD, `57e89d1ec2bcfdca4a22594b8eed081153c724cf`.

```text
python -B research/function-catalogue/verify.py --edition test-d5bs-v1
python -B research/function-catalogue/verify.py --edition test-d5bs-v1 --write
python -B research/function-catalogue/test_editions.py
```

The first command checks the in-memory output. The second repeats verification
before creating a fresh receipt under
`.local-work/function-catalogue/test-d5bs-v1/run-*/files/`. It assembles the
16 files in a temporary sibling directory before moving the complete output
tree into the receipt. Each run has a distinct path. The test script uses
disposable work directories and reads the repository's local Git objects.
It removes its own temporary directories after testing. Keep project scratch
and receipts local and apply the [project safeguards](../../WORKFLOW.md#scientific-experiment-continuation-and-health)
when running project validation.

This is an engineering demonstration with the same 2,095 entries. Later
documents change the coverage and locator tables. The receipt contains
generated files only. Its relative links and source-line coordinates are
verified against the pinned source tree plus the generated files. To follow
these links offline, use that tree as the source and overlay the generated
files in a disposable copy. The receipt namespace identifies the technical
edition. Its contents carry the historical scientific and external-invocation
qualifications and have no release approval.

## Source selection and drift

The manifest pins the Git commit and tree, executable identity, output
namespace, path and SHA-256 of each input and expected output. Source entries
use repository-relative paths in lexical order. `scan` inputs feed the
inventory. `support` inputs supply curated joins, reference pairs, and
navigation text. Generation fails on an absent, changed, unused or duplicate
input. A separate manifest for a new technical edition must explicitly name
each admitted source. Use a new `test-<name>-v<number>` identifier and
the corresponding ignored namespace. Review its source selections and line
references against that revision before pinning the output hashes. Developers
can derive draft hashes in memory using `outputs(SourceSet(repo, manifest))`
from the local modules. The command-line verifier still requires all
expected hashes to match before any write.

The schema carries executable hash, module, version and preferred base.
This generator accepts only the established 1.16.244.0 image. Supporting
a different image requires its own reviewed address rules and sources. The
canonical key remains the executable hash, module and entry RVA.

```text
python -B research/function-catalogue/verify.py --drift
```

Drift reports eligible tracked and nonignored untracked working-tree paths
outside the selected scan set, with their current byte hashes. Use
`--edition test-d5bs-v1 --drift` for the technical selection. The listing is
informational. Even a file with zero address mentions can affect old scanner
coverage. Address-like text may refer to globals, sites or unrelated prose.
The report neither admits inputs nor changes the manifest. Working-tree edits
to an already selected path are outside the drift listing because the build
reads its pinned Git version.

The historical pages keep their original relative links to authored sources.
They resolve against the reader's checkout. If a linked file has changed
since D5BD, use the historical commit for the printed physical line or CSV
row. For example:

```text
git show 6e799a428a765aa196a24d3c1de8ae133260aa08:docs/function-register.md
```

Raw export references remain provenance metadata. Build and link checks use
authored files and curated boundary receipts. Original export replay and
external invocation have separate evidentiary and authorization requirements.
See the [D5BS checks](../../docs/audits/native-function-catalogue-d5bs/README.md).
