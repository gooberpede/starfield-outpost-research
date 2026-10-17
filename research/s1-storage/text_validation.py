# SPDX-License-Identifier: GPL-3.0-or-later
"""Text-only UTF-8/mojibake validation for review exports. Standard library only.
Reads supplied bytes; never reads game/save/native inputs or writes files.
Call validate_text(bytes, label) from the exporter before constructing patches.
"""
import re
import difflib
import hashlib
import json
import subprocess
from pathlib import Path


def _byte_chars(low, high):
    chars = set()
    for value in range(low, high + 1):
        for encoding in ('cp1252', 'latin1'):
            try:
                chars.add(bytes([value]).decode(encoding))
            except UnicodeDecodeError:
                pass
    return '[' + re.escape(''.join(sorted(chars))) + ']'


# UTF-8 leads/continuations wrongly decoded as Windows-1252 or Latin-1.
# Includes the observed multiplication and minus corruptions. Escaped source
# keeps the validator's own examples from introducing literal corrupted text.
_CONT = _byte_chars(0x80, 0xbf)
_MOJIBAKE = re.compile(
    '[\u00c2\u00c3]' + _CONT
    + '|[\u00e2\u00ef]' + _CONT + '{2}'
    + '|\u00f0' + _CONT + '{3}'
)


def validate_text(data, label='<text>'):
    text = data.decode('utf-8', errors='strict')
    if text.startswith('\ufeff'):
        raise ValueError(f'{label}: UTF-8 BOM')
    for number, line in enumerate(text.split('\n'), 1):
        if '\ufffd' in line or re.search('[\u0080-\u009f]', line):
            raise ValueError(f'{label}:{number}: replacement character or C1 control')
        match = _MOJIBAKE.search(line)
        if match:
            points = ' '.join(f'U+{ord(c):04X}' for c in match[0])
            raise ValueError(f'{label}:{number}: suspected mojibake ({points})')
    return text


def validate_authored(data, label, prior=None):
    """Validate all new text or only additions to an existing tracked file."""
    text = data.decode('utf8', errors='strict')
    if prior is None:
        validate_text(data, label)
    else:
        added = '\n'.join(line[2:] for line in difflib.ndiff(
            prior.decode('utf8').split('\n'), text.split('\n')) if line.startswith('+ '))
        validate_text(added.encode('utf8'), label + ' (added text)')
    return text


def audit_authored_text(root, run):
    """Read Git's changed/untracked text inventory; scan new files and added
    tracked lines, excluding the unchanged user-supplied brief. Write one fresh
    ignored receipt. No protected scientific inputs or regression suites read.
    """
    if not run.isalnum():
        raise ValueError('run must be alphanumeric')
    root = Path(root)
    def git(*args):
        return subprocess.check_output(['git', *args], cwd=root)
    changed = git('diff', 'HEAD', '--name-only', '-z').decode('utf8').split('\0')[:-1]
    new = git('ls-files', '--others', '--exclude-standard', '-z').decode('utf8').split('\0')[:-1]
    brief = 'docs/implementation-briefs/CODEX_BRIEF_SOR_S1_capacity_inventory_state_completion.md'
    rows = []
    for name in sorted(set(changed + new) - {brief}):
        data = (root / name).read_bytes()
        text = data.decode('utf8', errors='strict')
        if name in new:
            validate_authored(data, name)
            scope = 'entire new authored file'
        else:
            validate_authored(data, name, git('show', 'HEAD:' + name))
            scope = 'newly added/changed lines; existing HEAD text excluded'
        rows.append(dict(path=name, sha256=hashlib.sha256(data).hexdigest(), scope=scope))
    out = root / '.local-work/s1-capacity' / (run + '.json')
    with out.open('x', encoding='utf8', newline='\n') as f:
        json.dump(dict(files=rows, excluded_supplied_brief=brief,
                       head=git('rev-parse', 'HEAD').decode().strip(),
                       index_sha256=hashlib.sha256((root / '.git/index').read_bytes()).hexdigest(),
                       result='PASS', limits='Text only; no scientific evidence or native/save analysis rerun'), f, indent=2)
        f.write('\n')
    print('PASS text validation', len(rows), 'authored files;', out)
