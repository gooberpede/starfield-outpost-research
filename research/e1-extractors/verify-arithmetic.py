# SPDX-License-Identifier: GPL-3.0-or-later
"""Original offline E1 source-integrity and selected-operation verifier.
Reads pinned executable/ESM/script/interface inputs, protected Ghidra files,
baseline, local definition/native/UI evidence and the original local AVM2 reader.
Writes one exclusive ignored JSON receipt. Requires CPython stdlib, repository
cwd, prepared evidence and disk guard. No game/process/save/project/index or
network effects. Native text checks are locators, not semantic or runtime oracles;
worked float examples are derivations, not an independent production simulator.
"""
from pathlib import Path
import argparse
import difflib
import hashlib
import json
import runpy
import struct
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT/'.local-work/e1-arithmetic'
sys.path.insert(0, str(ROOT/'save-analysis/scripts'))
from inventory_historical_saves import guard


def pin(path):
    with path.open('rb') as stream:
        digest = hashlib.file_digest(stream, 'sha256').hexdigest()
    return dict(path=str(path), size=path.stat().st_size, sha256=digest)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--run', required=True)
    args = parser.parse_args()
    assert args.run.isalnum()
    guard()
    checks = []

    def check(condition, label):
        assert condition, label
        checks.append(label)

    protected = json.loads((BASE/'protected-before.json').read_text())
    for expected in protected:
        check(pin(Path(expected['path'])) == expected, 'protected '+expected['path'])
    baseline = json.loads((BASE/'baseline.json').read_text())
    check(pin(ROOT/'.git/index') == baseline['index'], 'pre-existing index bytes preserved')
    check(subprocess.check_output(['git', 'rev-parse', 'HEAD'], text=True).strip() == baseline['head'], 'HEAD preserved')
    prior = []
    for expected in baseline['files']:
        path = Path(expected['path'])
        before = BASE/'baseline-tree'/path.relative_to(ROOT)
        actual = path.read_bytes()
        removed = [line for line in difflib.ndiff(before.read_text().splitlines(), actual.decode('utf8').splitlines()) if line.startswith('- ')]
        check(not removed, 'prior authored lines preserved '+str(path.relative_to(ROOT)))
        prior.append(dict(path=str(path), identical=actual == before.read_bytes()))
    inventory = json.loads((BASE/'definitions03.json').read_text())
    check(pin(Path(inventory['source']['path'])) == inventory['source'], 'installed ESM unchanged')
    records = inventory['records']
    by_id = {record['formid']: record for record in records}
    with Path(inventory['source']['path']).open('rb') as stream:
        for formid in (0x5ef19, 0x6ac84, 0x27ab66, 0x8407, 0x5ef53, 0x5ed88, 0x5ef6e):
            record = by_id[formid]
            stream.seek(record['offset'])
            header = stream.read(24)
            check(header[:4].decode() == record['type'] and struct.unpack_from('<I', header, 12)[0] == formid, 'physical ESM header '+hex(formid))
    for formid in (0x5ef53, 0x5ed88, 0x5ef6e):
        fields = dict(by_id[formid]['fields'])
        check(fields['NNAM'] == '0100' and not any(tag == 'FVPA' for tag, _ in by_id[formid]['fields']), 'example recipe count and no ingredients '+hex(formid))
    check(dict(by_id[0x8407]['fields'])['NAM0'] == '0000803f', 'HarvesterRateMult definition default 1')
    check(dict(by_id[0x3a]['fields'])['FLTV'] == '0000a041', 'TimeScale ESM default 20; not current state')
    exe = Path(next(row['path'] for row in protected if row['path'].endswith('Starfield.exe')))
    blob = exe.read_bytes()
    pe = struct.unpack_from('<I', blob, 60)[0]
    section_count = struct.unpack_from('<H', blob, pe+6)[0]
    optional_size = struct.unpack_from('<H', blob, pe+20)[0]
    sections = [struct.unpack_from('<8sIIII', blob, pe+24+optional_size+i*40) for i in range(section_count)]

    def native_float(va):
        rva = va-0x140000000
        for _, _, section_rva, size, offset in sections:
            if section_rva <= rva < section_rva+size:
                return struct.unpack_from('<f', blob, offset+rva-section_rva)[0]
        raise ValueError('not file-backed')

    for va, value in ((0x144f04f78, 3600), (0x144f04c30, 60), (0x144f04b5c, 24), (0x144f03fd8, struct.unpack('<f', bytes.fromhex('abaa2a3d'))[0]), (0x144f03e40, struct.unpack('<f', bytes.fromhex('6f12833a'))[0]), (0x144f03d54, 2**-23)):
        check(native_float(va) == value, 'file-backed float '+hex(va))
    f32 = lambda value: struct.unpack('<f', struct.pack('<f', value))[0]
    hours = struct.unpack('<f', bytes.fromhex(dict(by_id[0x5ed87]['fields'])['FLTV']))[0]
    nominal = f32(hours*native_float(0x144f04f78))
    check(nominal == 36, 'definition-derived common interval binary32 36')
    rate = f32(native_float(0x144f04c30)/nominal)
    check(struct.pack('<f', rate).hex() == '5555d53f', 'definition-derived baseline nominal rate bits')
    ui = json.loads((BASE/'ui-verification.json').read_text())
    check(pin(Path(ui['archive']))['sha256'] == ui['archive_sha256'], 'installed interface archive unchanged')
    scripts = json.loads((BASE/'quantity-script-locators01.json').read_text())
    check(pin(Path(scripts['source']))['sha256'] == scripts['sha256'], 'installed script archive unchanged')
    decode = runpy.run_path(str(BASE/'ui-disasm.py'))['decode']
    for asset in ui['assets']:
        stem = asset['asset']
        blocks = json.loads((BASE/'ui-assets'/(stem+'.uncompressed.abc.json')).read_text())
        check(len(blocks) == 1, 'single selected ABC '+stem)
        block = blocks[0]
        for body in block['bodies']:
            decode(block, body)
        check(len(block['bodies']) == asset['parsed_methods'], 'all selected method boundaries '+stem)
        swf = (BASE/'ui-assets'/(stem+'.uncompressed.swf')).read_bytes()
        for detail in asset['details']:
            raw = swf[detail['swf_code_offset']:detail['swf_code_offset']+detail['code_bytes']]
            check(hashlib.sha256(raw).hexdigest() == detail['code_sha256'], 'original SWF method slice '+stem+' '+detail['alias'])
        if stem.startswith('workshop'):
            precision = next(item for item in block['constants'] if item['owner'] == 'FooterContainer' and item['name'] == 'PRECISION')
            check(precision['value_kind'] == 3 and block['ints'][precision['value_index']] == 2, 'footer precision 2 '+stem)
            body = next(body for body in block['bodies'] if 'GlobalFunc[static].FormatNumberToString' in body['aliases'])
            check(block['methods'][body['method']]['optional'][-1] == [10, 10], 'footer default false '+stem)
            check([544, 'callproperty', 'substring', 2] in decode(block, body), 'footer substring branch '+stem)
        else:
            body = next(body for body in block['bodies'] if 'GlobalFunc[static].RoundDecimal' in body['aliases'])
            check([20, 'callproperty', 'round', 1] in decode(block, body), 'LOCATIONS Math.round '+stem)
            body = next(body for body in block['bodies'] if 'GlobalFunc[static].RoundDecimalToFixedString' in body['aliases'])
            check([15, 'callproperty', 'toFixed', 1] in decode(block, body), 'LOCATIONS fixed digits '+stem)
    for number, needles in {
        '01': ['140f7e1e1\tVROUNDSS', '140f7f2c3\tVMOVSS', '140f7f674\tVMULSS'],
        '16': ['1422cce66\tMOV ECX,0xa6', '1422cd077\tVMOVSS', 'DAT_1458d58f4'],
        '18': ['FUNCTION\t1421f2cb0', 'FUNCTION\t1404bcc80'],
        '19': ['FUNCTION\t1421f36b0', 'FUNCTION\t140839900'],
        '24': ['FUNCTION\t1421f2ac0', 'piVar7[1] = piVar7[1] | uVar9'],
    }.items():
        text = (ROOT/'.local-work/recon'/('e1-arithmetic-'+number+'.tsv')).read_text()
        for needle in needles:
            check(needle in text, 'native locator '+number+' '+needle)
    guard()
    result = dict(count=len(checks), checks=checks, prior_files=prior,
                  sample=dict(nominal_seconds=nominal, nominal_rate=rate),
                  scope='Static source/byte/locator checks and numerical derivations; no retail execution, independent timing or realized-output oracle.')
    with (BASE/('verification'+args.run+'.json')).open('x', encoding='utf8', newline='\n') as stream:
        json.dump(result, stream, indent=2)
        stream.write('\n')
    print('PASS', len(checks), 'offline checks; no runtime oracle')


if __name__ == '__main__':
    main()
