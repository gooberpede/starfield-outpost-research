# SPDX-License-Identifier: GPL-3.0-or-later
"""Stopped N2 accounting without eager all-pairs witness materialization.

Owned SOR-P-0002 adaptation of d5ao_n2_operations. Reads the unchanged pinned
sources, closed session and protected inputs; writes a fresh local postflight.
No target, save, deployment or network writes. Original causal readers retain
every validation and history-issue predicate. Only the pure registration_windows
enrichment is omitted, explicitly marked UNCOMPUTED. Separate focused review
must establish relevant causal witnesses. This is a new offline method, not the
frozen live method or a certificate of scientific completeness.
"""
import os
import sys
if not __debug__ or sys.flags.optimize or os.environ.get('PYTHONOPTIMIZE', '') not in ('', '0'):
    raise RuntimeError('Use pinned Python -E -B without optimization')

import argparse
from pathlib import Path
import d5ao_n2_operations as operations

OMISSION = 'ALL_HISTORY_REGISTRATION_WINDOWS_OMITTED_UNCOMPUTED'


def omit_windows(rows, issues):
    """No input mutation, no inferred absence, no scientific qualification."""
    return []


def install_omission():
    import d5an_read_causal
    import d5am_read_causal
    import d5am_join_causal
    d5an_read_causal.registration_windows = omit_windows
    d5am_read_causal.registration_windows = omit_windows
    original_load = d5am_join_causal.load

    def load(name):
        module = original_load(name)
        if name == 'd5am_read_causal':
            module.registration_windows = omit_windows
        return module

    d5am_join_causal.load = load


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ('plan', 'preflight', 'approval'):
        parser.add_argument('--' + name, type=Path, required=True)
        parser.add_argument('--' + name + '-sha256', required=True)
    parser.add_argument('--session', type=Path, required=True)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    operations.guard()
    plan = operations.original.pinned_json(args.plan, args.plan_sha256)
    plan['plan_sha256'] = args.plan_sha256
    operations.source_pins(plan)
    before = operations.original.pinned_json(args.preflight, args.preflight_sha256)
    before['receipt_sha256'] = args.preflight_sha256
    operations.require(before['plan_sha256'] == args.plan_sha256, 'Preflight plan mismatch')
    approval = operations.original.pinned_json(args.approval, args.approval_sha256)
    out = args.out.resolve()
    operations.require(out.is_relative_to(operations.ROOT / '.local-work/d5ao'), 'Local output required')
    operations.regular(out.parent)
    operations.require(not any(p.is_symlink() or p.is_junction() for p in (out, *out.parents)), 'No reparse output')
    out.mkdir(exist_ok=False)
    install_omission()
    try:
        result = operations.postflight(plan, before, args.session, approval, out)
        result['offline_analysis_adapter'] = dict(
            method_sha256=operations.sha(__file__), omission=OMISSION,
            original_operations_sha256=operations.sha(operations.__file__),
            original_readers=result['reader_sources'],
            validation='Original validation/accounting/history predicates unchanged; enrichment only omitted',
            scientific_coverage='REQUIRES_SEPARATE_FOCUSED_ADJUDICATION')
        for key in ('causal', 'joins'):
            if isinstance(result.get(key), dict):
                result[key]['registration_windows_disposition'] = OMISSION
        operations.fresh(out / 'receipt.json', result)
    except BaseException as error:
        operations.fresh(out / 'error.json', dict(state='CHECK_ERROR', error=repr(error), omission=OMISSION))
        raise
    print(result['status'])


if __name__ == '__main__':
    main()
