# SPDX-License-Identifier: GPL-3.0-or-later
"""Create the owned D4D controller derivative; development helper, not a target tool.

Reads pinned project sources; writes only the named D4D source files. No target,
network, save, analysis database or Git effects. Requires Python stdlib.
"""
from pathlib import Path

HERE = Path(__file__).resolve().parent
OLD = HERE.parent / 'resource-tungsten-acquisition'


def main():
    text = (OLD / 'controller.cpp').read_text()
    text = text.replace('#include "ancestry.h"', '#include "../resource-tungsten-acquisition/ancestry.h"\n#include "capture.h"')
    for name in ('context.h', 'sourcefiles.h', 'sample.inc'):
        text = text.replace('"' + name + '"', '"../resource-tungsten-acquisition/' + name + '"')
    text = text.replace('sor-d4a-', 'sor-d4d-')
    text = text.replace('uint64_t gen_entry=0,gen_token=0,gen_serial=0;', 'uint64_t gen_entry=0,gen_token=0,gen_serial=0; uint32_t sites[4]{}; std::vector<owner_capture::Frame> frames;')
    text = text.replace('exported(image,"diagnostic_call"),exported(image,"diagnostic_return")', 'exported(image,"map_loop"),exported(image,"map_cleanup")')
    text = text.replace('uint32_t rvas[4];std::copy(diagnostic,diagnostic+4,rvas);', 'uint32_t rvas[4];std::copy(diagnostic,diagnostic+4,rvas);\n        uint32_t extra[]={exported(image,"map_return"),exported(image,"diagnostic_call"),exported(image,"diagnostic_return")};', 1)
    text = text.replace('0x79b520,0x79be20,0x79ff1d', '0x79b520,0x7bc470,0x7bc745')
    point = 'uint32_t rvas[4];std::copy(diagnostic,diagnostic+4,rvas);\n        std::wstring command'
    text = text.replace(point, 'uint32_t rvas[4];std::copy(diagnostic,diagnostic+4,rvas);\n        uint32_t extra[]={0x79b925,0x79be20,0x79ff1d};\n        std::wstring command')
    text = text.replace('exported(image,"diagnostic_return")};', 'exported(image,"diagnostic_return"),exported(image,"candidate_ready")};')
    text = text.replace('0x79ff1d};', '0x79ff1d,0x79bd71};')
    text = text.replace('guards[7][16]', 'guards[11][16]').replace('allsites[7]', 'allsites[11]')
    text = text.replace('std::copy(diagnostic+1,diagnostic+4,allsites+4);', 'std::copy(diagnostic+1,diagnostic+4,allsites+4);std::copy(extra,extra+4,allsites+7);')
    text = text.replace('i<7;', 'i<11;')
    text = text.replace('if(t.gen_entry){++invalidated;t.gen_entry=0;}', 'if(t.gen_entry){++invalidated;t.gen_entry=0;t.frames.clear();} std::copy(rvas,rvas+4,t.sites);')
    text = text.replace('std::any_of(rvas,rvas+4,', 'std::any_of(allsites,allsites+11,')
    text = text.replace('threads.emplace(ev.dwThreadId,Thread{thread,lifetimes});', 'threads.emplace(ev.dwThreadId,Thread{thread,lifetimes});std::copy(rvas,rvas+4,threads.at(ev.dwThreadId).sites);')
    text = text.replace('CONTEXT c{}; c.ContextFlags=CONTEXT_ALL; require(GetThreadContext(t.handle,&c),"trap context");', 'CONTEXT c{}; c.ContextFlags=CONTEXT_ALL; require(GetThreadContext(t.handle,&c),"trap context");\n                    auto& rvas=t.sites;')
    text = text.replace('int guard_index=consumer_mode||slot==0?slot:slot+3;', 'int guard_index=-1;for(int k=0;k<11;++k)if(base+allsites[k]==c.Rip)guard_index=k;require(guard_index>=0,"known site");')
    text = text.replace('(slot==1?"generation_entry":slot==2?"ordinary_resource_call":"generation_return")', '(c.Rip==base+diagnostic[1]?"generation_entry":c.Rip==base+diagnostic[2]?"component_loop":c.Rip==base+diagnostic[3]?"map_cleanup":c.Rip==base+extra[0]?"map_return":c.Rip==base+extra[1]?"ordinary_resource_call":c.Rip==base+extra[3]?"candidate_ready":"generation_return")')
    text = text.replace('c.Dr6&=~15ULL; c.EFlags|=0x10000;', 'c.Dr0=base+rvas[0];c.Dr1=base+rvas[1];c.Dr2=base+rvas[2];c.Dr3=base+rvas[3];\n                        c.Dr6&=~15ULL; c.EFlags|=0x10000;')
    text = text.replace('bad.gen_entry=0;', 'bad.gen_entry=0;bad.frames.clear();')
    text = text.replace('// C2B adaptation of owned C1E controller; exact lineage in sources.csv.', '// D4D derivative of repaired D4B/D4A controller; provenance in sources.csv.')
    (HERE / 'controller.cpp').write_text(text, encoding='utf8', newline='\n')


if __name__ == '__main__':
    main()
