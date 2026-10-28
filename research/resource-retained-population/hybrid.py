# SPDX-License-Identifier: GPL-3.0-or-later
"""D5N source adapter for the owned D5M controller and native reducer.

Reads the existing project sources and returns generated source in memory.
Performs reads only; no process calls, new dependencies or retail deployment. Exact
single-use anchors fail closed when the inherited implementation changes.
Grid-clear uses DR0; the other thirteen boundaries retain software traps.
"""
from pathlib import Path
import types

SRC = Path(__file__).resolve().parent


def replace(text, old, new):
    if text.count(old) != 1:
        raise ValueError('D5N adaptation anchor changed: '+old[:100])
    return text.replace(old, new)


def controller(text):
    text = replace(text, 'int wmain(int argc,wchar_t** argv){', '''
static bool hardware_context(const CONTEXT& c,uint64_t address){
    return c.Dr0==address&&!(c.Dr1||c.Dr2||c.Dr3)&&(c.Dr7&0xffff20ffULL)==1;
}
static void arm_hardware(HANDLE h,uint64_t address,bool initial){
    CONTEXT c{};c.ContextFlags=CONTEXT_ALL;require(GetThreadContext(h,&c),"hardware context");
    require(!(c.EFlags&0x100),"foreign TF at hardware admission");
    require(initial?(!(c.Dr7&0xffff20ffULL)&&!(c.Dr6&15)):hardware_context(c,address),"foreign hardware slots");
    c.ContextFlags=CONTEXT_DEBUG_REGISTERS;c.Dr0=address;c.Dr1=c.Dr2=c.Dr3=c.Dr6=0;
    c.Dr7=(c.Dr7&~0xffff20ffULL)|1;
    require(SetThreadContext(h,&c),"arm DR0");
    CONTEXT v{};v.ContextFlags=CONTEXT_DEBUG_REGISTERS;
    require(GetThreadContext(h,&v)&&hardware_context(v,address)&&!(v.Dr6&15),"DR0 readback");
    diagnostic("HARDWARE_ARMED",",\\"address\\":"+std::to_string(address));
}
int wmain(int argc,wchar_t** argv){''')
    text = replace(text, 'auto patch=[&](int site,unsigned char byte){',
                   'auto patch=[&](int site,unsigned char byte){require(site!=10,"Grid-clear patch prohibited");')
    text = replace(text, '&&site==10&&!queued_test_requested)',
                   '&&site==(mode==L"queued-hardware"?10:11)&&serial>=3&&!queued_test_requested)')
    text = replace(text, 'if((mode==L"queued-same"||mode==L"queued-different")',
                   'if((mode==L"queued-same"||mode==L"queued-different"||mode==L"queued-hardware")')
    text = replace(text, 'if(stepping)require(suspend(stepping),"cannot fence new thread during rearm");',
                   'if(started)arm_hardware(threads.at(ev.dwThreadId).handle,base+sites[10],true);\n'
                   '                if(stepping)require(suspend(stepping),"cannot fence new thread during rearm");')
    text = replace(text, 'for(int j=0;j<SiteCount;++j)patch(j,0xcc);started=true;',
                   'if(mode==L"slot-pressure"){auto h=threads.begin()->second.handle;CONTEXT c{};c.ContextFlags=CONTEXT_DEBUG_REGISTERS;require(GetThreadContext(h,&c),"pressure context");c.Dr0=base+sites[10]+1;c.Dr7=1;require(SetThreadContext(h,&c),"fixture foreign DR0");}\n'
                   '                    for(int j=0;j<SiteCount;++j)if(j!=10)patch(j,0xcc);\n'
                   '                    for(auto& [tid,t]:threads)arm_hardware(t.handle,base+sites[10],true);started=true;')
    text = replace(text, '&&!(c.Dr7&0xff),"barrier foreign control state"',
                   '&&hardware_context(c,base+sites[10]),"barrier foreign control state"')
    text = replace(text, 'sor-d5l-native/2', 'sor-d5n-hybrid/1')
    text = replace(text, '}else if(code==EXCEPTION_BREAKPOINT&&started){',
                   '}else if((code==EXCEPTION_BREAKPOINT||code==EXCEPTION_SINGLE_STEP)&&started){')
    text = replace(text, 'for(int j=0;j<SiteCount;++j)if(c.Rip==base+sites[j]+1)site=j;', '''
                    bool hardware=code==EXCEPTION_SINGLE_STEP;
                    if(hardware){require(hardware_context(c,base+sites[10])&&(c.Dr6&15)==1&&!(c.Dr6&0x6000)&&c.Rip==base+sites[10],"hardware trap identity");site=10;}
                    else for(int j=0;j<SiteCount;++j)if(j!=10&&c.Rip==base+sites[j]+1)site=j;''')
    text = replace(text, 'auto expected_trap=stepping&&step_site==site?originals[site]:0xcc;',
                   'auto expected_trap=hardware||(stepping&&step_site==site)?originals[site]:0xcc;')
    text = replace(text, '"queued peer must remain fenced");c.Rip--;',
                   '"queued peer must remain fenced");if(!hardware)c.Rip--;else{c.Dr6=0;c.EFlags&=~0x10000UL;}')
    text = replace(text, 'set_owned_control(t.handle,c),"queued peer rewind"',
                   'set_owned_control(t.handle,c,hardware),"queued peer rewind"')
    text = replace(text, 'require(!(c.EFlags&0x100)&&!(c.Dr7&0xff),"foreign TF or hardware slots");',
                   'require(!(c.EFlags&0x100)&&hardware_context(c,base+sites[10]),"foreign TF or hardware slots");')
    text = replace(text, 'c.Rip--;require(set_owned_control(t.handle,c),"deferred trap rewind");resume();',
                   'if(!hardware)c.Rip--;else{c.Dr6=0;c.EFlags&=~0x10000UL;}require(set_owned_control(t.handle,c,hardware),"deferred trap rewind");resume();')
    text = replace(text, 'if(sites[j]+k==sites[m])expected_byte=0xcc;',
                   'if(m!=10&&sites[j]+k==sites[m])expected_byte=0xcc;')
    text = replace(text, 'diagnostic("SITES_VERIFIED",', '''
                        for(auto& [tid,peer]:threads){CONTEXT v{};v.ContextFlags=CONTEXT_DEBUG_REGISTERS;
                            require(GetThreadContext(peer.handle,&v)&&hardware_context(v,base+sites[10]),"continuous hardware coverage");}
                        diagnostic("SITES_VERIFIED",''')
    text = replace(text, 'else{\n                            if(mode==L"guard-loss"', '''else if(hardware){
                            c.Dr6=0;c.EFlags|=0x10000UL;
                            require(set_owned_control(t.handle,c,true),"hardware RF resume");
                            CONTEXT v{};v.ContextFlags=CONTEXT_ALL;require(GetThreadContext(t.handle,&v),"hardware resume readback");
                            require(hardware_context(v,base+sites[10])&&!(v.Dr6&15)&&(v.EFlags&0x10000)&&v.Rip==c.Rip&&
                                !memcmp(&v.Rax,&c.Rax,17*sizeof(DWORD64))&&!memcmp(&v.FltSave,&c.FltSave,sizeof c.FltSave)&&
                                v.MxCsr==c.MxCsr&&(v.EFlags&~0x10002UL)==(c.EFlags&~0x10002UL),"hardware CPU preservation");
                            diagnostic("HARDWARE_RESUMED",",\\"rip\\":"+std::to_string(v.Rip));resume();
                        }else{
                            if(mode==L"guard-loss"''')
    text = replace(text, 'if(mode==L"step-stop"){', '''
                            if(mode==L"hardware-loss"&&serial==1){v.ContextFlags=CONTEXT_DEBUG_REGISTERS;v.Dr0+=1;require(SetThreadContext(t.handle,&v),"fixture lost DR0");}
                            if(mode==L"step-stop"){''')
    return text


def fixture(text):
    """Retain software queue controls and add a hardware/software queue control.

    Grid-stress continues to exercise real concurrent hardware Grid-clear traps.
    An extra crash happens before construction; the inherited crash is afterward.
    """
    start = text.index('    if(mode==L"queued-same"||mode==L"queued-different"){')
    end = text.index('    if(mode==L"foreign-first")', start)
    block = text[start:end].replace('native_grid_clear(p.grid);',
                                   'fixture_source_init(p.source,p.grid,state.definition.b.data());')
    block = replace(block, 'else fixture_source_init(p.source,p.grid,state.definition.b.data());',
                    'else if(mode==L"queued-hardware")fixture_source_init(p.source,p.grid,state.definition.b.data());\n            else fixture_grid_init(p.grid);')
    block = replace(block, 'if(mode==L"queued-same"||mode==L"queued-different"){',
                    'if(mode==L"queued-same"||mode==L"queued-different"||mode==L"queued-hardware"){')
    block = replace(block, 'std::thread first([&]{fixture_source_init(p.source,p.grid,state.definition.b.data());});',
                    'std::thread first([&]{if(mode==L"queued-hardware")native_grid_clear(p.grid);else fixture_source_init(p.source,p.grid,state.definition.b.data());});')
    text = text[:start]+block+text[end:]
    return replace(text, '    if(mode==L"foreign-first")',
                   '    if(mode==L"early-crash")RaiseException(0xe0d51002,0,0,nullptr);\n    if(mode==L"foreign-first")')


def reducer():
    """Generate the same scientific reducer with exact hybrid RIP validation.

    Raw CONTEXT bytes and event addresses stay unmodified. Only Grid-clear's
    execution breakpoint expects RIP at the instruction instead of INT3+1.
    """
    text = (SRC/'native_reduce.py').read_text(encoding='utf8')
    text = replace(text, 'sor-d5l-native/2', 'sor-d5n-hybrid/1')
    text = replace(text, "session['sites'][r['site']]+1:",
                   "session['sites'][r['site']]+(0 if r['site']==10 else 1):")
    text = replace(text, "if not context_consistent(r):", "if not hybrid_context(r,session) or not context_consistent(r):")
    module = types.ModuleType('d5n_native_reduce')
    module.hybrid_context = hybrid_context
    exec(compile(text, str(SRC/'native_reduce.py')+'[D5N adapted]', 'exec'), module.__dict__)
    return module


def hybrid_context(row, session):
    """Check actual register ownership, without changing captured bytes."""
    import struct
    raw = bytes.fromhex(row['raw_context'])
    if len(raw) < 0x100:
        return False
    dr0, dr1, dr2, dr3, dr6, dr7 = struct.unpack_from('<6Q', raw, 0x48)
    return (dr0 == session['sites'][10] and not (dr1 or dr2 or dr3)
            and dr7 & 0xffff20ff == 1
            and dr6 & 15 == (1 if row['site'] == 10 else 0))
