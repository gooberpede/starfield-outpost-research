# SPDX-License-Identifier: GPL-3.0-or-later
"""Bounded, non-rewriting changed-authored-text screen; Python stdlib only.

Reads explicit repository files or Git's changed tracked/untracked text inventory.
For existing files scans added lines, leaving legacy prose outside the screen.
Python scanning covers comments/docstrings; opaque JSON/binary/raw data is skipped.
Prints JSON diagnostics with file, line, rule and severity. No file/index writes.
Manual semantic reading and independent review are mandatory after this screen.
"""
import argparse
import ast
import csv
import io
import json
from pathlib import Path
import re
import subprocess
import tokenize

ROOT = Path(__file__).resolve().parents[2]
SUFFIXES = {'.md', '.csv', '.py'}

def prose(line):
    line = re.sub(r'`[^`]*`', '', line)
    line = re.sub(r'https?://\S+', '', line)
    line = re.sub(r'\[[^\]]*\]\([^)]*\)', lambda m: m[0].split(']')[0][1:], line)
    return line

def line_rules(line):
    rules=[]
    plain=prose(line)
    if re.search(r'\b(?:[A-Za-z]+\d+[a-z]{2,}|[a-z]{2,}\d+(?:,\d+)?[a-z]{2,})\b',plain):
        rules.append(('JOINED_PROSE','WARN'))
    if re.search(r'\bcell\d+(?:,\d+)?\b',plain):rules.append(('JOINED_COORDINATE','WARN'))
    if re.search(r'[a-z][,;:!?][A-Za-z]|[a-z]\.[A-Z][a-z]',plain):rules.append(('PUNCTUATION_SPACE','WARN'))
    if any(c in line for c in ('\ufffd','\u00c3\u00a2','\u00c3\u2014','\u00c2\u00a0','\u00e2\u20ac')):
        rules.append(('ENCODING','ERROR'))
    if re.search(r'\b(?:VA|RVA|FormID|offset)\s+`?(?!0x)[0-9a-fA-F]{5,}\b',line):
        rules.append(('HEX_DOMAIN_PREFIX','WARN'))
    if re.search(r'\[[^\]]+\]\([^)]*$',line):rules.append(('MARKDOWN_LINK','ERROR'))
    return rules

def authored_python(text):
    lines=set()
    for tok in tokenize.generate_tokens(io.StringIO(text).readline):
        if tok.type==tokenize.COMMENT:lines.add(tok.start[0])
    tree=ast.parse(text)
    for node in ast.walk(tree):
        if isinstance(node,(ast.Module,ast.ClassDef,ast.FunctionDef,ast.AsyncFunctionDef)) and node.body:
            first=node.body[0]
            if isinstance(first,ast.Expr) and isinstance(first.value,ast.Constant) and isinstance(first.value.value,str):
                lines.update(range(first.lineno,first.end_lineno+1))
    return lines

def scan(path, text, selected=None):
    path=Path(path);diagnostics=[];fence=False
    if path.suffix=='.csv':
        reader=csv.reader(io.StringIO(text))
        headers=next(reader,[])
        opaque={'path','locator','sha256','source_id','bytes'}
        for n,fields in [(1,headers),*((reader.line_num,fields) for fields in reader)]:
            # CSV delimiters are structure, not prose punctuation. Pin/path
            # columns are identifiers; labels and explanatory fields are prose.
            for i,value in enumerate(fields):
                if fields is not headers and i<len(headers) and headers[i] in opaque:continue
                for rule,severity in line_rules(value):
                    if selected is None or n in selected:
                        diagnostics.append(dict(file=path.as_posix(),line=n,rule=rule,severity=severity))
        return diagnostics
    python_lines=authored_python(text) if path.suffix=='.py' else None
    for n,line in enumerate(text.splitlines(),1):
        if path.suffix=='.md' and re.match(r'^\s*```',line):
            fence=not fence;continue
        if selected is not None and n not in selected:continue
        if python_lines is not None and n not in python_lines:continue
        if fence:continue
        suppression=re.search(r'editorial: allow ([A-Z_,]+) -- (\S.*?)(?: -->|$)',line)
        allowed=set(suppression[1].split(',')) if suppression else set()
        for rule,severity in line_rules(line):
            if rule not in allowed:diagnostics.append(dict(file=path.as_posix(),line=n,rule=rule,severity=severity))
        if path.suffix=='.md':
            for target in re.findall(r'\[[^\]]*\]\(([^)]+)\)',line):
                link=target.split('#')[0].strip('<>')
                if link and not re.match(r'[A-Za-z]+:',link) and not (path.parent/link).exists():
                    diagnostics.append(dict(file=path.as_posix(),line=n,rule='LOCAL_LINK',severity='ERROR'))
    if fence:diagnostics.append(dict(file=path.as_posix(),line=len(text.splitlines()),rule='MARKDOWN_FENCE',severity='ERROR'))
    return diagnostics

def git(*args):
    return subprocess.check_output(['git',*args],cwd=ROOT).decode('utf8')

def changed():
    tracked=git('diff','HEAD','--name-only','-z').split('\0')[:-1]
    new=git('ls-files','--others','--exclude-standard','-z').split('\0')[:-1]
    out=[]
    for name in sorted(set(tracked+new)):
        p=ROOT/name
        if p.suffix not in SUFFIXES or not p.is_file():continue
        if name.startswith(('docs/experiments/evidence/','.local-work/')):continue
        selected=None
        if name not in new:
            selected=set();n=0
            for line in git('diff','--unified=0','HEAD','--',name).splitlines():
                h=re.match(r'@@ -\d+(?:,\d+)? \+(\d+)',line)
                if h:n=int(h[1]);continue
                if line.startswith(('+++','---')):continue
                if line.startswith('+'):selected.add(n);n+=1
                elif line.startswith(' '):n+=1
        out.append((p,selected))
    return out

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--changed',action='store_true')
    ap.add_argument('files',nargs='*',type=Path)
    a=ap.parse_args()
    if a.changed and a.files:ap.error('choose changed inventory or explicit files')
    paths=changed() if a.changed else [(p.resolve(),None) for p in a.files]
    diagnostics=[]
    for p,selected in paths:
        if not p.resolve().is_relative_to(ROOT) or p.suffix not in SUFFIXES or '.local-work' in p.parts:
            raise ValueError('only authored repository text is eligible')
        diagnostics.extend(scan(p,p.read_text(encoding='utf8'),selected))
    print(json.dumps(dict(files=[p.relative_to(ROOT).as_posix() for p,_ in paths],diagnostics=diagnostics,
                          limitation='Changed lines only for existing files; code fences and inline symbols excluded. No semantic or universal detection guarantee.'),indent=2))
    return bool(diagnostics)

if __name__=='__main__':raise SystemExit(main())
