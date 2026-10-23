# SPDX-License-Identifier: GPL-3.0-or-later
"""Pure prospective protected-save gate and unchanged scientific transfer test."""
from save_policy import admission as save_admission


def admit(live, backup, historical, policy):
    result = save_admission(live, backup, historical, policy)
    assert result['ok'], result
    return result


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
