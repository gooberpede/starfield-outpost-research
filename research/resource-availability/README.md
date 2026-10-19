# Offline resource research helpers

These original GPL-3.0-or-later helpers implement the [bounded brief](../../docs/implementation-briefs/CODEX_BRIEF_SOR_inorganic_resource_availability_runtime_serialization.md).
Read the [report](../../docs/experiments/resource-availability/report.md),
[contracts/commands](../../docs/experiments/resource-availability/schema.md) and
[native execution ledger](../../docs/experiments/resource-availability/native.md).

The Python probes use only installed CPython standard library and existing
project readers. They read pinned installed ESMs or archived local evidence,
enforce the C:/D: space guard and exclusively create ignored JSON receipts.
They never execute the game, modify saves/configuration or access the network.

ResourceGlobalRefs.java reads existing address references; ResourceFields.java
reads existing instructions in an explicit range; ResourceCellFields.java reads
existing instructions and selected field offsets. The last historical filename
does not assert CELL semantics: the traced source is BIOM. All use existing
Ghidra APIs with read-only/no-analysis invocation through the owned wrapper,
writing only exclusive TSV derivatives. They do not change symbols, types,
comments or analysis. Retained copies add SPDX and normalize line endings to LF;
the executed originals and their hashes remain in the specialist source ledger.
Tool transient side effects and actual failed exports are recorded separately.

export-review-package.py reads HEAD/index, baseline and authored text, creates
exclusive ignored complete/task-only patches and disposable .local-work/review-patches application
trees. It checks exact forward/reverse bytes, links and whitespace. It changes no
workspace content, Git index/ref, staging, commit, push or remote. The algorithm
is adapted from this project's owned workshop-population package helper; its
source and revision provenance are retained with the package.
