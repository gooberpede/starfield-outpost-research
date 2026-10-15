// SPDX-License-Identifier: GPL-3.0-or-later
// Original disposable synthetic targets only. No game/SFSE/target execution.
#define SOR_FIXTURE
#include "capture.h"
#include <cassert>
#include <thread>
using namespace preview;
uint64_t closure[3]{},source[15]{},slot=reinterpret_cast<uint64_t>(source),xy=0;
uint64_t original(uint64_t a,uint64_t b,uint64_t c,uint64_t d){assert(a==reinterpret_cast<uint64_t>(closure)&&b==17&&c==reinterpret_cast<uint64_t>(&slot)&&d==99);assert(GetLastError()==123);SetLastError(456);return 1;}
uint64_t natural_provider(uint64_t a,uint64_t b,uint64_t c,uint64_t d){assert(a==reinterpret_cast<uint64_t>(source)&&b==reinterpret_cast<uint64_t>(&xy)&&c==reinterpret_cast<uint64_t>(closure)&&d==19);return 0xabcdef;}
unsigned char cached(uint64_t,uint64_t,float,float){return 0;}
unsigned char refreshed(uint64_t,uint64_t,float,float){SetLastError(123);assert(integral(0x21e0a46,source_visit,original,reinterpret_cast<uint64_t>(closure),17,reinterpret_cast<uint64_t>(&slot),99)==1);assert(GetLastError()==456);return 1;}
int main(int argc,char**argv){assert(argc==2||argc==3);auto root=fs::path(argv[1]);fs::create_directories(root);assert(spool.open(root));
    if(argc==3){uint64_t members[257]{};Invocation s(123,region,0,0,0,0);s.e.phase=before;forms(s,0,reinterpret_cast<uint64_t>(members),reinterpret_cast<uint64_t>(members)+sizeof(members));s.send(before,0);s.finish(false,0);assert(spool.broken&&spool.stopping&&spool.failed>0&&spool.active==0);assert(spool.flush());assert(write_new(root/L"failure.json","{"+spool.counts()+",\"error\":\"snapshot_capacity\"}\n"));spool.close();puts("PASS snapshot capacity fails explicitly without member traversal");return 0;}
    uint64_t state[13]{},position[3]{};
    assert(produce(0x21b42e3,cached,reinterpret_cast<uint64_t>(state),reinterpret_cast<uint64_t>(position),150,23)==0);
    assert(produce(0x21b42e3,refreshed,reinterpret_cast<uint64_t>(state),reinterpret_cast<uint64_t>(position),150,23)==1);
    assert(integral(0x7b526a,provider,natural_provider,reinterpret_cast<uint64_t>(source),reinterpret_cast<uint64_t>(&xy),reinterpret_cast<uint64_t>(closure),19)==0xabcdef);
    assert(spool.flush());spool.stop();assert(write_new(root/L"retired.json","{"+spool.counts()+"}\n"));spool.close();
    auto reads=fixture_reads.load(),attempts=spool.attempted.load();
    assert(integral(0x7b526a,provider,natural_provider,reinterpret_cast<uint64_t>(source),reinterpret_cast<uint64_t>(&xy),reinterpret_cast<uint64_t>(closure),19)==0xabcdef);
    SetLastError(123);assert(integral(0x21e0a46,source_visit,original,reinterpret_cast<uint64_t>(closure),17,reinterpret_cast<uint64_t>(&slot),99)==1);
    assert(produce(0x21b42e3,cached,reinterpret_cast<uint64_t>(state),reinterpret_cast<uint64_t>(position),150,23)==0);
    assert(fixture_reads==reads&&spool.attempted==attempts&&spool.active==0);
    static Spool overflow;Event e;for(size_t i=0;i<Spool::capacity;++i)assert(overflow.emit(e));assert(!overflow.emit(e)&&overflow.broken&&overflow.failed==1&&overflow.losses==1&&overflow.stopping);
    static Spool parallel;auto pr=root/L"parallel";fs::create_directory(pr);assert(parallel.open(pr));
    auto run=[](){Event e;for(int i=0;i<500;++i)assert(parallel.emit(e));};std::thread a(run),b(run);assert(parallel.flush());a.join();b.join();assert(parallel.flush());assert(parallel.captured==1000&&parallel.durable==1000&&parallel.queued==0&&parallel.failed==0);parallel.close();
    puts("PASS source/provider forwarding, result/LastError, actual parent, bounded overflow and concurrent lock-free publication");
}
