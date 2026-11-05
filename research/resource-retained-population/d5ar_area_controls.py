# SPDX-License-Identifier: GPL-3.0-or-later
"""Repeat original native area predicates on fixed owned consumer operands.

SOR-P-0002 adaptation of the owned pinned D5V fixture setup/test function.
Reads installed PE, retained function metadata and independent planar predicate;
executes only private original instructions with declared resolver/quad allocator
substitutions. Writes exclusive ignored derivative and receipts in a disposable
child. Every inherited assert is explicitly converted to a normal fail-closed
conditional, including side-effect checks. No game, save, database or Git writes.
"""
import os
import sys
if not __debug__ or sys.flags.optimize or os.environ.get('PYTHONOPTIMIZE','') not in ('','0'):
    raise RuntimeError('Use pinned Python -E -B without optimization')

import ast
import json
from pathlib import Path
import subprocess
from d5ad_baseline import ROOT, guard, sha


class ExplicitChecks(ast.NodeTransformer):
    def __init__(self):
        self.changed=0
    def visit_Assert(self,node):
        self.changed+=1
        message=node.msg or ast.Constant('Inherited native area check failed')
        return ast.copy_location(ast.If(test=ast.UnaryOp(op=ast.Not(),operand=node.test),
            body=[ast.Raise(exc=ast.Call(func=ast.Name(id='RuntimeError',ctx=ast.Load()),args=[message],keywords=[]),cause=None)],orelse=[]),node)


def owned_host(destination):
    guard()
    original=Path(__file__).with_name('d5v_native.py')
    prior=ROOT / '.local-work/d5v/native05.json'
    old=json.loads(prior.read_bytes())
    if sha(original)!=old['code_sha256']:
        raise ValueError('Owned D5V fixture source changed')
    for name,digest in old['functions'].items():
        if sha(ROOT / '.local-work/d5v/functions' / (name+'.txt'))!=digest:
            raise ValueError('Native function metadata changed')
    source=original.read_text(encoding='utf8').split("    for case in ('D2-83388f','D2-84e101'):",1)[0]
    if '    def test(' not in source:
        raise ValueError('Owned native setup/test anchor absent')
    source=source.replace('destination = LOCAL/sys.argv[1]','destination = Path(sys.argv[1]).resolve()')
    source=source.replace('assert destination.parent == LOCAL and not destination.exists()',
                          "assert destination.is_relative_to(ROOT/'.local-work/d5ar') and not destination.exists()")
    tail='''
    cases=[
        ('context-A-overlap',[0,0,0],5,100,[0,0,0,2],[[0,0,0,2]],None),
        ('context-A-nonintersection',[100,0,0],5,100,[0,0,0,2],[[0,0,0,2]],None),
        ('context-B-indexed-overlap',[100,200,0],5,100,[0,0,0,2],[[0,0,0,2]],[-100,-200,0]),
        ('context-B-indexed-nonintersection',[100,200,0],5,100,[50,0,0,2],[[50,0,0,2]],[-100,-200,0]),
        ('same-count-moved-region',[100,200,0],5,100,[20,20,0,2],[[20,20,0,2]],[-100,-200,0]),
        ('no-points',[0,0,0],150,100,[0,0,0,2],[],None),
        ('inclusive-tangency',[2,0,0],0,100,[0,0,0,2],[[0,0,0,2]],None),
        ('one-point-height-independent',[0,0,1000],0,-1000,[0,0,0,2],[[0,0,0,2]],None),
        ('strip-interior',[0,0,1000],0,-1000,[0,0,0,20],[[-10,0,0,2],[10,0,0,2]],None),
        ('strip-broadphase-only-counterexample',[0,8,0],0,100,[0,0,0,20],[[-10,0,0,2],[10,0,0,2]],None),
        ('strip-edge-3d-accept',[0,2.5,0],1,-10,[0,0,0,20],[[-10,0,0,2],[10,0,0,2]],None),
        ('strip-edge-3d-reject',[0,2.5,3],1,-10,[0,0,0,20],[[-10,0,0,2],[10,0,0,2]],None),
        ('strip-vertex-height-accept',[10,2.5,-100],1,0,[0,0,0,20],[[-10,0,0,2],[10,0,0,2]],None),
        ('strip-vertex-height-reject',[10,2.5,-100],1,-1,[0,0,0,20],[[-10,0,0,2],[10,0,0,2]],None)]
    for arguments in cases:test(*arguments)
    verdicts={r['label']:r['native_accepted'] for r in rows}
    if not verdicts['context-A-overlap'] or verdicts['context-A-nonintersection'] or not verdicts['context-B-indexed-overlap'] or verdicts['context-B-indexed-nonintersection']:
        raise RuntimeError('Distinct owned consumer context relation differs')
    destination.write_text(json.dumps(dict(schema='sor-d5ar-native-area/1',status='PASS',rows=rows,
        point_rows=point_rows,functions=functions,executable_sha256=initial['installed'][exe],
        inherited_method_sha256=sha(ROOT/'research/resource-retained-population/d5v_native.py'),
        scope='Original area predicate on supplied owned frozen operands; not an actual retail outpost/frame certificate'),indent=2)+'\\n',encoding='utf8',newline='\\n')
'''
    tree=ast.parse(source+tail)
    checks=ExplicitChecks();tree=checks.visit(tree);ast.fix_missing_locations(tree)
    if any(isinstance(node,ast.Assert) for node in ast.walk(tree)):
        raise ValueError('Inherited assertion survived explicit conversion')
    derived=destination.with_suffix('.method.py')
    with derived.open('x',encoding='utf8',newline='\n') as stream:stream.write(ast.unparse(tree)+'\n')
    namespace={'__file__':str(original),'__name__':'d5ar_owned_area_fixture'}
    prior_argv=sys.argv
    try:
        sys.argv=[str(original),str(destination)]
        exec(compile(tree,str(derived),'exec'),namespace)
        namespace['main']()
    finally:sys.argv=prior_argv
    value=json.loads(destination.read_bytes())
    if len(value['rows'])!=14 or value['status']!='PASS':
        raise ValueError('Native area output differs')
    receipt=dict(status='PASS',controls=14,original_native_predicate=True,game_process=False,
        result_sha256=sha(destination),derived_method_sha256=sha(derived),explicit_assert_conversions=checks.changed,
        wrapper_sha256=sha(__file__),inherited_method_sha256=sha(original),prior_receipt_sha256=sha(prior),floors=guard())
    with destination.with_suffix('.qualification.json').open('x',encoding='utf8',newline='\n') as stream:
        stream.write(json.dumps(receipt,indent=2)+'\n')


def main():
    destination=Path(sys.argv[-1]).resolve()
    if not destination.is_relative_to(ROOT / '.local-work/d5ar') or destination.exists():
        raise ValueError('Fresh ignored D5AR output required')
    if any(p.is_symlink() or p.is_junction() for p in (destination,*destination.parents)):
        raise ValueError('No reparse outputs')
    guard()
    if sys.argv[1:2]==['--owned-host']:return owned_host(destination)
    try:
        result=subprocess.run([sys.executable,'-E','-B',str(Path(__file__).resolve()),'--owned-host',str(destination)],
            capture_output=True,timeout=30,creationflags=subprocess.CREATE_NO_WINDOW)
    except subprocess.TimeoutExpired as failure:
        with destination.with_suffix('.failure.json').open('x',encoding='utf8',newline='\n') as stream:
            stream.write(json.dumps(dict(status='OWNED_HOST_TIMEOUT',seconds=30,
                stdout=(failure.stdout or b'').decode(errors='replace'),
                stderr=(failure.stderr or b'').decode(errors='replace')),indent=2)+'\n')
        raise RuntimeError('Owned native area host timed out; failure receipt retained') from failure
    if result.returncode:
        with destination.with_suffix('.failure.json').open('x',encoding='utf8',newline='\n') as stream:
            stream.write(json.dumps(dict(exit=result.returncode,stdout=result.stdout.decode(errors='replace'),
                stderr=result.stderr.decode(errors='replace')),indent=2)+'\n')
        raise RuntimeError('Owned native area host failed; failure receipt retained')
    print(json.dumps(dict(status='PASS',controls=14,path=str(destination))))


if __name__=='__main__':main()
