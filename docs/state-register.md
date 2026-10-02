# State, Relationship, and Representation Register

No state structure, field, saved record, or cross-domain identity mapping is established yet.

| ID | Subsystem / concept | Runtime representation | Saved representation / offset domain | Definition dependencies | Persistence class | Lifecycle / authority | Build and sample scope | Confidence / evidence |
|---|---|---|---|---|---|---|---|---|

Use `SOR-ST-` IDs. Unknown columns must say `UNKNOWN`, not be silently inferred. Record owning object, identity, lifetime, creation/update/consumption, relationships, and whether an interpretation is structural or semantic. Link detailed evidence rather than putting guessed layouts into this table.

Persistence classes and integration statuses are defined in [EVIDENCE_STANDARD.md](EVIDENCE_STANDARD.md). An in-memory field is not proof of a serialized field; a stored value may be replaced or recalculated during load. Record mappings between runtime pointers, handles, FormIDs, saved identifiers, and logical entities only once demonstrated.
