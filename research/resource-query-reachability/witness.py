# SPDX-License-Identifier: GPL-3.0-or-later
"""Replay the selected two candidate demand prefixes, without claiming admission.

Reads the authenticated corpus, BA2 and pinned arithmetic receipt. Executes only
existing host CRT math on owned numbers. Writes one fresh ignored receipt; no
game, generator, analysis-project, original evidence or classification writes.
Uses owned D5H domain/occupancy methods (SOR-P-0002). Native feasibility must be
reviewed separately; numerical agreement cannot establish a first miss.
"""
import ctypes
import json
from pathlib import Path
import sys
from domains import ROOT, load, maps, pin
from roundtrip import projected
from occupancy import contributors
from audit import write, LOCAL


def main():
    output=Path(sys.argv[1]).resolve()
    assert output.is_relative_to(LOCAL) and not output.exists()
    corpus=load('.local-work/resource-feynman-d5/build04/normalized.json',
                '97aa50e0eb6bc7a2d5157bffbb311942fd84e7c01e6bd2ef3ea28a4e9bd9e0f9')
    manifest=load('.local-work/resource-save52/build-v1/manifest.json',
                  '9d2ff9012a573595227c8feda5345de35286b807103665486239ddbe8cbfa9de')
    raster=maps(manifest,{'0005e0de'})['0005e0de']
    arithmetic=json.loads((LOCAL/'native-bytes09.json').read_text())
    host=Path('C:/Windows/System32/ucrtbase.dll')
    assert pin(host)=='3c60056371f82e4744185b6f2fa0c69042b1e78804685944132974dd13f3b6d9'
    crt=ctypes.CDLL(str(host))
    for name in ('cos','atan2'):
        function=getattr(crt,name)
        function.argtypes=[ctypes.c_double]*(2 if name=='atan2' else 1)
        function.restype=ctypes.c_double
    crt._controlfp_s.argtypes=[ctypes.POINTER(ctypes.c_uint32),ctypes.c_uint32,ctypes.c_uint32]
    crt._controlfp_s.restype=ctypes.c_int
    control=ctypes.c_uint32()
    assert crt._controlfp_s(ctypes.byref(control),0,0)==0 and control.value&0x300==0
    resources=[r for r in corpus['bodies']['0005e0de']['biomes']['00145440']['resources']
               if r.get('branch')!='special']
    assert [r['id'] for r in resources]==['000057d4','000057d0','000057cf']
    rows=[]
    for label,root,expected in [('L',(5,-2),0),('H',(5,0),3)]:
        queries=[]
        for dx,dy in [(-1,1),(-1,0),(0,1),(1,1)]:
            x,y=37536+root[0]+dx,20928+root[1]+dy
            branches=[]
            for fused in (False,True):
                tag,column,row,error=projected(0,x,y,constants=arithmetic['sine_constants'],
                                              fused=fused,scalar_math=crt)
                mask=raster['faces'][tag]['mask'][row*256+column]&15
                assert mask==expected
                vector=[(0.0 if r['rarity']==6 else corpus['settings'][r['rarity']])
                        if mask==8 or mask<r['rarity'] else 1.0 for r in resources]
                branches.append(dict(fused=fused,chart=tag,column=column,row=row,
                                     error_fine_cells=error,mask=mask,vector=vector))
            queries.append(dict(geographic_query=[x,y],branches=branches))
        occupancy=contributors(corpus,queries[0]['geographic_query'])
        assert occupancy['permutation_outcomes'] and all(
            result['emitted'][0]=='0:37536:20928:0029d20e'
            for result in occupancy['permutation_outcomes'])
        rows.append(dict(continuation=label,root=list(root),density_queries=queries,
                         first_query_occupancy=occupancy))
    write(output,dict(rows=rows,scalar_host_sha256=pin(host),control_word=hex(control.value),
        arithmetic_receipt_sha256=pin(LOCAL/'native-bytes09.json'),helper_sha256=pin(Path(__file__)),
        qualification='Finite candidate arithmetic/occupancy only; native first-miss feasibility requires independent review'))
    print('Two candidate prefixes; eight queries; sixteen SIMD evaluations; masks 0/3')


if __name__=='__main__':main()
