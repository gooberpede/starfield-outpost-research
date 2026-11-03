# SPDX-License-Identifier: GPL-3.0-or-later
"""Offline-only proposed gate decisions, not a live controller or authorization.

Pure owned policy oracle for the D5AJ gate audit. Reads supplied gate states in
memory, returns operator-facing proposed responses, writes nothing and contacts
no process. Existing approved cards/controllers remain unchanged.
"""
GATES = {
    'operator_stop': ('SAFETY', 'STOP'),
    'protected_contents': ('SAFETY', 'STOP'),
    'backup_readiness': ('SAFETY', 'HOLD_ADMISSION'),
    'disk_C': ('SAFETY', 'STOP'),
    'disk_D': ('SAFETY', 'STOP'),
    'identity_guards': ('INTEGRITY', 'STOP'),
    'controller_worker': ('INTEGRITY', 'STOP'),
    'core_recorder': ('INTEGRITY', 'STOP'),
    'lifetime_recorder': ('INTEGRITY', 'STOP'),
    'output_transport': ('INTEGRITY', 'STOP'),
    'geometry_arm_ack': ('SCIENTIFIC PREREQUISITE', 'HOLD_QUERY'),
    'baseline_prefix_qualified': ('SCIENTIFIC PREREQUISITE', 'HOLD_DEPARTURE'),
    'consumer_frame': ('SCIENTIFIC PREREQUISITE', 'HOLD_DEPARTURE'),
    'complete_A0': ('SCIENTIFIC PREREQUISITE', 'HOLD_DEPARTURE'),
    'source_attribution': ('RECOVERABLE SCIENTIFIC UNCERTAINTY', 'HOLD_DEPARTURE'),
    'snapshot_native_quality': ('RECOVERABLE SCIENTIFIC UNCERTAINTY', 'RETAIN_UNKNOWN'),
    'global_epoch_changed': ('RECOVERABLE SCIENTIFIC UNCERTAINTY', 'QUALIFY_SOURCE_SCOPE'),
    'healthy_poll_delay': ('RECOVERABLE SCIENTIFIC UNCERTAINTY', 'CONTINUE'),
    'timestamp_only': ('RECOVERABLE SCIENTIFIC UNCERTAINTY', 'REHASH_CHANGED_GUARD'),
}


def assess(gate, state):
    """Classify a known observation; no elapsed time becomes an inferred failure."""
    if gate not in GATES or state not in ('PASS', 'FAIL', 'PENDING'):
        raise ValueError('Explicit known gate and observation required')
    category, failure = GATES[gate]
    if state == 'PASS':
        response = 'CONTINUE_WITHIN_APPROVED_ACTIONS'
    elif state == 'PENDING':
        response = 'WAIT_FOR_EVIDENCE'
    else:
        response = failure
    return dict(gate=gate, category=category, state=state, proposed_response=response,
                permission_to_act=False, preserve_evidence=True,
                exclusive_operator_stop=True)
