# SPDX-License-Identifier: GPL-3.0-or-later
"""Disposable AppContainer access attacks; writes only output/probe.json.

Reads provisioned input/probes.json and attempts named custodian reads/listings,
parent traversal, sidecars, reparse escapes, and a write to the read-only input.
No socket connection, game operation or save write. The parent creates synthetic
sentinels; actual protected paths are tested by denied open/enumeration only.
"""
import json
import os


def main():
    with open('../input/probes.json', encoding='utf8') as stream:
        probes = json.load(stream)
    rows = []
    for row in probes:
        try:
            if row['operation'] == 'list':
                os.listdir(row['path'])
            elif row['operation'] == 'write':
                with open(row['path'], 'ab'):
                    pass
            elif row['operation'] == 'symlink':
                os.symlink(row['path'], 'escape-link')
                with open('escape-link', 'rb') as stream:
                    stream.read(1)
            else:
                with open(row['path'], 'rb') as stream:
                    stream.read(1)
        except PermissionError as error:
            rows.append(dict(**row, result='DENIED', winerror=error.winerror, errno=error.errno))
        except OSError as error:
            result = 'DENIED_CREATION_PRIVILEGE' if row['operation'] == 'symlink' and error.winerror == 1314 else 'OTHER_ERROR'
            rows.append(dict(**row, result=result, winerror=error.winerror))
        else:
            rows.append(dict(**row, result='ACCESSIBLE'))
    with open('probe.json', 'x', encoding='utf8') as stream:
        json.dump(dict(schema='sor-blind-probes/1', rows=rows), stream, indent=2)


if __name__ == '__main__':
    main()
