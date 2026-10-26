# SPDX-License-Identifier: GPL-3.0-or-later
"""Read tracked Python/read-site references; retain a local dependency ledger.

Literal references are candidates, not evidence of execution or complete dynamic
coverage. No referenced consumer is executed. Writes only a fresh local receipt.
"""
import ast
import json
from pathlib import Path
import subprocess

from cutover import ROOT, OUT, save, e


def run():
    roots = json.loads((OUT / 'intake.json').read_text())['system_directories']
    names = subprocess.check_output(['git', 'ls-files', '-z'], cwd=ROOT).decode().split('\0')[:-1]
    scripts = []
    for name in names:
        path = ROOT / name
        if path.suffix != '.py':
            continue
        text = path.read_text(encoding='utf8')
        hits = [root for root in roots if root in text]
        if not hits:
            continue
        calls = []
        for node in ast.walk(ast.parse(text)):
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) and node.func.attr in (
                    'open', 'read_text', 'read_bytes', 'glob', 'rglob'):
                calls.append(dict(line=node.lineno, expression=ast.get_source_segment(text, node)))
        treatment = ('Maintained preservation consumer: original manifest stays loose; committed archive substitution is explicit'
                     if name in ('research/resource-carinae-source-context/protection.py',
                                 'research/resource-tungsten-acquisition/protection.py')
                     else 'Historical corpus reader: explicit restored inputs and historical modules'
                     if name == 'research/resource-standalone/isolate.py'
                     else 'Historical or unqualified acquisition, analysis, admission or packaging candidate; no execution inferred; deliberate restoration and original prerequisites required')
        scripts.append(dict(path=name, sha256=e.pin(path), namespace_mentions=hits,
                            read_sites=calls, treatment=treatment))
    save(OUT / 'dependencies-final.json', dict(scripts=scripts,
         scope='Tracked Python literals and AST read/glob sites; no proof of execution and no exclusion of unknown external or dynamically assembled consumers',
         maintained_preservation_inputs=['.local-work/resource-carinae-source-context/protected-before.json',
                                        '.local-work/resource-carinae/sync-paths-preflight02.json'],
         historical_replay='research/resource-standalone/isolate.py with restored D4E corpus and five historical modules',
         protected_saved_inputs='Excluded from archive and retirement; existing prospective save policy unchanged'))
    print('Dependency candidates:', len(scripts), flush=True)


if __name__ == '__main__':
    run()
