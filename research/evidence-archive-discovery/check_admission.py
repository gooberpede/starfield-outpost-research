# SPDX-License-Identifier: GPL-3.0-or-later
"""Read-only negative entrypoint checks; synthetic free-space responses only.

No helper reaches source reads or writes when its admission gate rejects. Restore
the real disk query before writing one new local test receipt. No save access.
"""
import importlib

import archive as a
from inventory import LOCAL,write


def main():
    original=a.shutil.disk_usage;rows=[]
    try:
        a.shutil.disk_usage=lambda path:type('Usage',(),dict(free=40_500_000_000 if path=='D:/' else 90_000_000_000))()
        for name in ('inventory','discover','scope','model','retention','benchmark','qualify'):
            module=importlib.import_module(name)
            try:module.main()
            except a.ArchiveError as exc:
                if 'Free-space' not in str(exc):raise
                rows.append(dict(helper=name,expected='REFUSE before work',observed='REFUSE',passed=True))
            else:raise AssertionError('Entrypoint did not reject: '+name)
        a.shutil.disk_usage=lambda path:type('Usage',(),dict(free=39_000_000_000 if path=='C:/' else 90_000_000_000))()
        try:a.space()
        except a.ArchiveError:rows.append(dict(helper='C-drive guard',expected='REFUSE',observed='REFUSE',passed=True))
        else:raise AssertionError('C guard missing')
    finally:a.shutil.disk_usage=original
    write(LOCAL/'admission-tests.json',dict(results=rows,passed=len(rows),actual_disk_state_modified=False,
        source_payloads_read=False,no_helper_output_created=True))
    print('Admission controls passed',len(rows))


if __name__=='__main__':main()
