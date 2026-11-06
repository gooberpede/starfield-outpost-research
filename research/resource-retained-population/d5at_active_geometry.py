# SPDX-License-Identifier: GPL-3.0-or-later
"""Compare full ordinary geometry for the newly ranked VII-b density lead.

Adapts the owned D5U geometry driver under SOR-P-0002. Reads pinned installed
definitions and copies the existing native fixture to a new ignored directory.
Runs native generation only inside a disposable private child.
"""
import os
import sys

if sys.flags.optimize or os.environ.get('PYTHONOPTIMIZE', '') not in ('', '0'):
    raise RuntimeError('Use pinned Python -E -B without optimization')

from pathlib import Path
import shutil
import subprocess

from d5at_active import LOCK, LOCK_SHA, ROOT
import d5at_survey as s
from d5u_census import resources, weights

sys.path.insert(0, str(ROOT / 'research/resource-geometry'))
from context import packed_seed_key
from geometry import populate_source


def run(output):
    s.guard()
    s.require(s.sha(LOCK) == LOCK_SHA, 'Reviewed lock changed')
    s.require(s.sha(sys.executable) == s.PINNED[Path(sys.executable)], 'Interpreter identity')
    s.require(s.sha(s.D5) == s.PINNED[s.D5], 'Installed definitions identity')
    corpus = s.load(s.D5)['payload']
    body_id, chart, x, y, block = '0005e0e7', 1, 32124, 15168, '00298a3d'
    body = corpus['bodies'][body_id]
    sfpt, orientation, biome, _ = body['tiles'][f'{chart}:{x // 192}:{y // 192}']
    index = (x % 192 // 12) * 16 + y % 192 // 12
    selected, flags = corpus['patterns'][sfpt][index]
    s.require(orientation == 8 and flags & 8 and selected == block, 'VII-b source identity differs')
    w, h = (value - 4 for value in corpus['source_blocks'][block])
    origin = [-200, -200]
    keys = {f'{i},{j}': packed_seed_key(chart, [x, y], origin, [i, j], body['system'], body['index'])
            for i in range(1, w + 3) for j in range(1, h + 3)}
    definitions = resources(corpus, body_id, biome)
    constants = {int(key, 16): value for key, value in corpus['constants'].items()}
    models = []
    for mask in (0, 2):
        ordered = [dict(resource=r['id'], rarity=r['rarity'],
                        block=corpus['generation_blocks'][r['block']] + [0, 0], weight=weight)
                   for r, weight in zip(definitions, weights(corpus, definitions, mask))]
        request = dict(source=f'{chart}:{x}:{y}:{block}', provenance='D5AT VII-b fixed ordinary source-relative',
                       origin=origin, owner_key=int(body_id, 16), clip_center=[-200 + w // 2 * 100, -200 + h // 2 * 100, 0],
                       clip_half=[w // 2 * 100 + 200, h // 2 * 100 + 200, 0], context_qualified=True,
                       order_qualified=True, cell_bounds=[1, w + 3, 1, h + 3], ordered_resources=ordered, packed_keys=keys)
        full = populate_source(request, constants)
        s.require(full['status'] == 'CONDITIONAL_PLANAR_SOURCE', 'VII-b geometry model did not qualify')
        models.append(dict(label=f'M{mask}', mask=mask, request=request, full=full))
    tool = Path(__file__).with_name('d5u_native.py')
    pins = {r['path']: r['sha256'] for r in s.read_csv(s.DOC / 'd5u-sources.csv')}
    s.require(s.sha(tool) == pins[tool.relative_to(ROOT).as_posix()], 'D5U native source identity')
    prior = ROOT / '.local-work/d5u/native05'
    output.mkdir()
    for name in ('start.py', 'native_probe.py', 'geometry.json', 'initial.json'):
        shutil.copyfile(prior / name, output / name)
    shutil.copytree(prior / 'functions', output / 'functions')
    model = output / 'model.json'
    s.write(model, dict(results=[*models, dict(models[-1], label='M2-repeat')]))
    wrapper = ("import os,runpy,sys\n"
               "if sys.flags.optimize or os.environ.get('PYTHONOPTIMIZE','') not in ('','0'): raise RuntimeError('Optimization refused')\n"
               "sys.argv=sys.argv[1:]\nrunpy.run_path(sys.argv[0],run_name='__main__')")
    process = subprocess.run([sys.executable, '-E', '-B', '-c', wrapper, str(tool), 'native.json', str(model)],
                             env=dict(os.environ, D5S_OUTPUT=str(output)), capture_output=True)
    (output / 'stdout.log').write_bytes(process.stdout)
    (output / 'stderr.log').write_bytes(process.stderr)
    s.require(process.returncode == 0 and not process.stderr, 'VII-b native comparison failed')
    native = s.load(output / 'native.json')
    runs = native['runs']
    s.require(len(runs) == 3 and runs[0]['regions'] != runs[1]['regions']
              and runs[1]['regions'] == runs[2]['regions'], 'VII-b geometry or repeat comparison failed')
    result = [dict(mask=r['mask'], regions=len(r['full']['regions']),
                   points=sum(len(p['points']) for p in r['full']['regions'])) for r in models]
    s.write(output / 'comparison.json', dict(source=models[0]['request']['source'], body=body_id, biome=biome,
                                              comparison=result, model_sha256=s.sha(model),
                                              native_sha256=s.sha(output / 'native.json'), after=s.guard()))
    print(result)


if __name__ == '__main__':
    path = Path(sys.argv[1]).absolute()
    s.require(path.is_relative_to(ROOT / '.local-work') and path == path.resolve() and not path.exists(),
              'Fresh ignored output required')
    run(path)
