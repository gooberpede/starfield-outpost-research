# SPDX-License-Identifier: GPL-3.0-or-later
"""Pure prospective save-corpus gate; never writes, restores or operates a target.

A missing historical save needs a separate explicit, hash-bound maintainer
disposition. This predicate cannot confer that authority itself.
"""


def admit(live, backup, historical, disposition=None, card_hash=None):
    assert backup == historical, 'Independent historical backup changed'
    missing = sorted(set(historical) - set(live))
    added = sorted(set(live) - set(historical))
    assert all(live[n] == historical[n] for n in set(live) & set(historical)), 'Existing save changed'
    if missing or added:
        assert disposition is not None, 'Missing historical saves require explicit disposition'
        assert disposition['status'] == 'ACCEPT_CURRENT_CORPUS_PRESERVE_BACKUP'
        assert disposition['human_instruction'].strip() and card_hash is not None
        assert disposition['card_sha256'] == card_hash
        assert disposition['missing'] == {n: historical[n] for n in missing}
        assert disposition['added'] == {n: live[n] for n in added}
        assert disposition['restore_authorized'] is False
    return missing, added


def useful_transfer(row, accepted):
    """Require three qualified resource identities in the same transfer.

    The caller's map is scoped by thread lifetime and updater token and contains
    only complete, Workshop-bound, main-file-qualified context decisions.
    """
    payload = row.get('refresh_payload', {})
    return (row.get('ancestry') == 'BOUND_TRANSFER' and
            row.get('required_reads_complete') is True and
            payload.get('status') == 'COMPLETE' and
            {accepted.get(m['pointer']) for m in payload.get('members') or []}
            >= {0x57c7, 0x57c9, 0x5df1})
