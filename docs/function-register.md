# Function and Operation Register

No project function or operation is registered yet. Do not prefill addresses or semantic names from another project.

| ID | Build ID | Module / script | Static address or exact symbol | RVA / source version | Original name | Proposed semantic alias | Role and side effects | Confidence / basis | Evidence / source IDs |
|---|---|---|---|---|---|---|---|---|---|

Use `SOR-FN-` IDs. For native functions record actual static/image bases and instruction ranges in the linked detail. For script operations record the script, exact source/version, declaration or call site, and what was independently checked. Include Address Library IDs only with version/provenance.

Preserve original names and addresses; semantic aliases do not authorize Ghidra renaming. Record reads/writes, callers, parameters, ownership, lifecycle, failure/cleanup paths, and unresolved parts as supported. Call-site and instruction evidence take precedence over an unverified decompiler prototype.

Separate observed internal functions from exposed or validated integration points. See [EVIDENCE_STANDARD.md](EVIDENCE_STANDARD.md).
