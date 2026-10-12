// SPDX-License-Identifier: GPL-3.0-or-later
#include "health.h"
#include <thread>
#include <vector>
#include <iostream>
#include <stdexcept>
using namespace oracle;
extern "C" uint64_t fixture_body(uint64_t,uint64_t,uint64_t);
extern "C" unsigned char fixture_center_call[],fixture_grid_call[];
extern "C" uint64_t abi_probe(Callback,uint64_t,uint64_t);
extern "C" uint32_t fixture_query_entry(uint64_t,uint64_t);
extern "C" uint32_t fixture_enum_entry(uint64_t,uint64_t,uint64_t);
extern "C" unsigned char fixture_query_call[],fixture_enum_call[];
unsigned checks{};
void require(bool v,const char* s){if(!v)throw std::runtime_error(s);++checks;std::cout<<"PASS "<<s<<'\n';}
std::atomic<int> mode{};std::atomic<bool> started{},release_native{};
uint64_t nested_object{},nested_slot{};
extern "C" __declspec(noinline) uint64_t fixture_center(uint64_t r,uint64_t out){memcpy(reinterpret_cast<void*>(out),reinterpret_cast<void*>(r+0x8c),12);return 0x11223344;}
extern "C" __declspec(noinline) uint64_t fixture_selector(uint64_t,uint64_t h,uint64_t xy){
    int m=mode.load();if(m==1)throw std::runtime_error("native_cpp_fault");
    if(m==2)RaiseException(0xe1234567,0,0,nullptr);
    if(m==3){started=true;while(!release_native.load())SwitchToThread();}
    if(m==4 && depth==1)callback_hook(nested_object,nested_slot,0);
    if(m==5 && depth==1&&!suppressed){gate.stop();callback_hook(nested_object,nested_slot,0);}
    memcpy(reinterpret_cast<void*>(h+4),reinterpret_cast<void*>(xy),8);return 0x88776655;
}
struct Fixture {
    alignas(8) uint64_t object[2]{},ctx[6]{},refslot{},landscape_slot{},table[2]{};
    unsigned char ref[0xd0]{},base[0x30]{},list[0x20]{},extra[0xa0]{},cell[0x118]{},world[0x390]{},landscape[0x58]{},hierarchy[44]{},candidate[44]{},translation[12]{};
    int xy[2]{-1,17};
    Fixture(){
        auto p=[](auto* v){return reinterpret_cast<uint64_t>(v);};
        object[1]=p(ctx);refslot=p(ref);landscape_slot=p(landscape);
        ctx[1]=p(candidate);ctx[2]=p(&landscape_slot);ctx[3]=p(hierarchy);ctx[4]=p(translation);ctx[5]=p(xy);
        uint64_t x=p(base);memcpy(ref+0x98,&x,8);x=p(list);memcpy(ref+0xc8,&x,8);x=p(extra);memcpy(list+8,&x,8);extra[0x12]=0xbc;
        x=0xf1517de43e171745;memcpy(extra+0x98,&x,8);x=p(cell);memcpy(ref+0xb0,&x,8);x=p(world);memcpy(cell+0x110,&x,8);
        uint32_t bid=0x2c60e9;memcpy(base+0x28,&bid,4);ref[0x2e]=0x4a;
        for(int i=0;i<12;++i)ref[0x8c+i]=static_cast<unsigned char>(i+1);
        table[0]=table[1]=p(&fixture_body);
    }
    uint64_t call(){return reinterpret_cast<Callback>(table[0])(reinterpret_cast<uint64_t>(object),reinterpret_cast<uint64_t>(&refslot),0xfeed);}
};
extern "C" uint32_t fixture_query_body(uint64_t a,uint64_t flag){if(flag==10)return 1;return fixture_enum_entry(a,flag,0);}
extern "C" uint32_t fixture_enum_body(uint64_t a,uint64_t flag,uint64_t option){
    if(option)throw std::runtime_error("option forwarding");if(flag==11)return 1;if(flag==13)throw std::runtime_error("query native unwind");if(flag==14)RaiseException(0xe1234567,0,0,nullptr);if(flag==15)return 0x87654321;
    return static_cast<uint32_t>(reinterpret_cast<Fixture*>(a)->call());
}
bool seh_query(Fixture* f){__try{fixture_query_entry(reinterpret_cast<uint64_t>(f),14);return false;}__except(GetExceptionCode()==0xe1234567?EXCEPTION_EXECUTE_HANDLER:EXCEPTION_CONTINUE_SEARCH){return true;}}
bool seh_call(Fixture* f){__try{f->call();return false;}__except(GetExceptionCode()==0xe1234567?EXCEPTION_EXECUTE_HANDLER:EXCEPTION_CONTINUE_SEARCH){return true;}}
uint64_t recursive_callback(uint64_t object,uint64_t slot,uint64_t arg){if(arg<40)return callback_hook(object,slot,arg+1);return 77;}
int main(int argc,char** argv){try{
    require(sizeof(Blob)==1040,"schema blob ABI size");require(sizeof(Event)==17768,"schema event ABI size");
    auto waiting=GetTickCount64();
    while(!sole_thread() && GetTickCount64()-waiting<120000){std::cout<<"STARTUP_WAIT "<<GetTickCount64()-waiting<<'\n'<<std::flush;Sleep(1000);}
    require(sole_thread(),"disposable installation sole-thread phase");
    queue=new Queue<4096>();original_callback=fixture_body;original_center=fixture_center;original_selector=fixture_selector;
    Fixture f;Edit e[6];original_query=fixture_query_body;original_enum=fixture_enum_body;
    auto relay_page=islands(reinterpret_cast<uint64_t>(fixture_center_call));require(relay_page!=nullptr,"relay_page allocation");
    island(relay_page,reinterpret_cast<uint64_t>(&center_hook));island(relay_page+16,reinterpret_cast<uint64_t>(&selector_hook));island(const_cast<unsigned char*>(relay_page)+32,reinterpret_cast<uint64_t>(&query_hook));
    island(const_cast<unsigned char*>(relay_page)+48,reinterpret_cast<uint64_t>(&enum_hook));
    DWORD old{};
    require(VirtualProtect(relay_page,4096,PAGE_EXECUTE_READ,&old)!=0,"island RW to RX");require(FlushInstructionCache(GetCurrentProcess(),relay_page,4096)!=0,"island instruction flush");
    require(relay_guard(relay_page,reinterpret_cast<uint64_t>(&center_hook)),"production relay guard validates RX bytes and target");require(!relay_guard(relay_page,reinterpret_cast<uint64_t>(&selector_hook)),"production relay guard rejects target drift");
    require(call_edit(e[0],reinterpret_cast<uint64_t>(fixture_center_call),reinterpret_cast<uint64_t>(relay_page)),"center CALL reachability");
    require(call_edit(e[1],reinterpret_cast<uint64_t>(fixture_grid_call),reinterpret_cast<uint64_t>(relay_page+16)),"grid CALL reachability");
    for(unsigned i=0;i<2;++i){require(e[i].address[0]==0xe8,"fixture full instruction E8");memcpy(e[i].before,e[i].address,5);}
    require(call_edit(e[2],reinterpret_cast<uint64_t>(fixture_query_call),reinterpret_cast<uint64_t>(relay_page+32)),"Q complete CALL reachability");
    require(call_edit(e[3],reinterpret_cast<uint64_t>(fixture_enum_call),reinterpret_cast<uint64_t>(relay_page+48)),"E complete CALL reachability");
    for(unsigned i=2;i<4;++i){require(e[i].address[0]==0xe8,"diagnostic full E8 instruction");memcpy(e[i].before,e[i].address,5);}
    for(unsigned i=4;i<6;++i){e[i].address=reinterpret_cast<unsigned char*>(&f.table[i-4]);e[i].size=8;memcpy(e[i].before,e[i].address,8);auto target=reinterpret_cast<uint64_t>(&callback_hook);memcpy(e[i].after,&target,8);}
    bool dirty{};require(!install(e,6,false,dirty)&&!dirty,"nonquiescent refusal without write");
    {
        auto mutable_page=static_cast<unsigned char*>(VirtualAlloc(nullptr,4096,MEM_RESERVE|MEM_COMMIT,PAGE_READWRITE));
        HANDLE mapping=CreateFileMappingW(INVALID_HANDLE_VALUE,nullptr,PAGE_READONLY,0,4096,nullptr);
        require(mutable_page&&mapping,"rollback fixture allocations");
        auto denied=static_cast<unsigned char*>(MapViewOfFile(mapping,FILE_MAP_READ,0,0,4096));require(denied!=nullptr,"rollback readonly view");
        Edit transaction[2];transaction[0].address=mutable_page;transaction[1].address=denied;
        for(auto& edit:transaction){edit.size=8;memcpy(edit.before,edit.address,8);memset(edit.after,0x51,8);}
        DWORD attempted{};require(!VirtualProtect(denied,8,PAGE_EXECUTE_READWRITE,&attempted),"actual readonly mapping denies patch protection");
        bool residue=false;require(!install(transaction,2,true,residue)&&residue,"mid-transaction protection failure conservatively retains residency");
        MEMORY_BASIC_INFORMATION restored{};require(VirtualQuery(mutable_page,&restored,sizeof restored)==sizeof restored&&restored.Protect==PAGE_READWRITE,"rollback restores earlier page protection");
        require(match(transaction[0],false)&&match(transaction[1],false),"rollback restores earlier bytes and leaves denied site unchanged");
        require(UnmapViewOfFile(denied)&&CloseHandle(mapping)&&VirtualFree(mutable_page,0,MEM_RELEASE),"rollback disposable allocation cleanup");
    }
    e[1].before[1]^=1;require(!install(e,6,true,dirty)&&!dirty&&match(e[0],false),"all preimages checked before mutation");e[1].before[1]^=1;
    require(install(e,6,true,dirty)&&dirty,"actual full CALL and callback installation");
    for(auto& edit:e)require(match(edit,true),"installed exact patch bytes");
    gate.state=0;SetLastError(0x1234);auto before_mxcsr=_mm_getcsr();require(f.call()==7,"native callback return preserved");
    require(GetLastError()==0x1234,"observer LastError preservation");require(_mm_getcsr()==before_mxcsr,"observer MXCSR preservation");
    std::vector<Event> events;Event event;while(queue->pop(event))events.push_back(event);
    require(events.size()==5,"begin center grid end complete pairing");
    require(events[0].kind==begin&&events[1].kind==center&&events[2].kind==grid_begin&&events[3].kind==grid&&events[4].kind==end,"native phase ordering");
    require(events[3].result.ok&&field<int32_t>(events[3].result,4)==-1&&field<int32_t>(events[3].result,8)==17,"actual native selected hierarchy output");
    require(events[2].floor_xy.ok&&field<int32_t>(events[2].floor_xy,0)==-1,"actual native floor input");
    require(events[1].center.ok&&!memcmp(events[1].center.bytes,f.ref+0x8c,12)&&!memcmp(events[2].center.bytes,events[1].center.bytes,12),"native center linked within invocation");
    require(field<uint64_t>(events[2].extra,0x98)==0xf1517de43e171745,"positive workshop identity bytes");
    require(events[0].invocation==events[4].invocation&&events[2].invocation==events[0].invocation,"same invocation identity chain");
    require(abi_probe(reinterpret_cast<Callback>(f.table[0]),reinterpret_cast<uint64_t>(f.object),reinterpret_cast<uint64_t>(&f.refslot))==0,"all eight GPR and ten XMM nonvolatile sentinels preserved");while(queue->pop(event)){}
    if(argc>1){fs::path output=argv[1];fs::create_directory(output);std::ofstream raw_file(output/L"fixture-events.bin",std::ios::binary);for(auto& r:events)raw_file.write(reinterpret_cast<const char*>(&r),sizeof r);raw_file.close();}
    f.refslot=0;require(f.call()==1,"null native early return unchanged");while(queue->pop(event))events.push_back(event);require(events.size()==7,"early return without invented center grid");f.refslot=reinterpret_cast<uint64_t>(f.ref);
    Blob bad;require(!copy(bad,1,12)&&!bad.ok,"invalid pointer explicit status");require(!copy(bad,0,12),"null pointer");require(!copy(bad,0x7fffffffffffULL,12),"overflowing pointer");
    mode=1;bool propagated=false;try{f.call();}catch(const std::runtime_error&){propagated=true;}require(propagated&&depth==0&&gate.state==0,"native C++ unwind propagates and scope drains");
    bool unwind_seen=false;while(queue->pop(event))unwind_seen|=event.kind==unwind;require(unwind_seen,"unwind event retained");
    mode=2;require(seh_call(&f)&&depth==0&&gate.state==0,"native SEH propagates and scope cleanup");bool seh_unwind=false;while(queue->pop(event))seh_unwind|=event.kind==unwind;require(seh_unwind,"SEH abnormal completion explicitly retained");
    mode=4;nested_object=reinterpret_cast<uint64_t>(f.object);nested_slot=reinterpret_cast<uint64_t>(&f.refslot);f.call();events.clear();while(queue->pop(event))events.push_back(event);require(events.size()==10,"nested original invocation captures independently");require(events[3].parent==events[0].invocation&&events[3].invocation!=events[0].invocation,"TLS parent linkage without value join");
    mode=5;f.call();events.clear();while(queue->pop(event))events.push_back(event);require(events.size()==5&&suppressed==0&&depth==0,"rejected nested admission cannot inherit outer identity");gate.state=0;
    mode=0;std::vector<std::thread> calls;for(int j=0;j<4;++j)calls.emplace_back([]{Fixture own;own.table[0]=reinterpret_cast<uint64_t>(&callback_hook);for(int k=0;k<20;++k)own.call();});for(auto& t:calls)t.join();events.clear();while(queue->pop(event))events.push_back(event);require(events.size()==400&&lost==0,"overlapping actual wrappers preserve all invocations");
    center_channel=false;f.call();bool missing_center=false;while(queue->pop(event))if(event.kind==grid)missing_center=(event.status&32)&&!event.center.ok;require(missing_center,"grid-only channel exposes missing native center");center_channel=true;
    grid_channel=false;f.call();unsigned center_only=0;while(queue->pop(event)){require(event.kind!=grid&&event.kind!=grid_begin,"center-only does not manufacture grid");++center_only;}require(center_only==3,"independent center channel");grid_channel=true;
    mode=0;std::atomic<bool> background_ready{},background_stop{};std::thread background([&]{background_ready=true;while(!background_stop)SwitchToThread();});while(!background_ready)SwitchToThread();require(!sole_thread(),"overlapping-thread install gate refuses");background_stop=true;background.join();
    mode=3;started=false;release_native=false;std::thread in_flight([&]{f.call();});while(!started)SwitchToThread();gate.stop();require(!gate.drained(),"stop while native invocation active waits");release_native=true;in_flight.join();require(gate.drained(),"in-flight native completion drains after stop");while(queue->pop(event)){}
    require(f.call()==7&&!queue->pop(event),"retained inert wrappers continue native call without capture");
    mode=0;gate.state=0;for(unsigned i=0;i<1100;++i)f.call();require(lost>0&&(gate.state&stop_bit),"backpressure closes admission and reports loss");while(queue->pop(event)){}
    auto transport=std::make_unique<Queue<64>>();std::atomic<unsigned> received{},successful{};std::atomic<bool> finish{};
    std::thread reader([&]{Event r;while(!finish||received<successful){if(transport->pop(r)){require(r.invocation==r.sequence,"concurrent publication untorn");++received;}else SwitchToThread();}});
    std::vector<std::thread> producers;for(unsigned j=0;j<4;++j)producers.emplace_back([&,j]{for(unsigned k=0;k<100;++k){Event r;r.sequence=j*100+k;r.invocation=r.sequence;while(!transport->push(r))SwitchToThread();++successful;}});
    for(auto& t:producers)t.join();finish=true;reader.join();require(received==400,"four producers and consumer exact delivery");
    original_callback=recursive_callback;gate.state=0;require(callback_hook(reinterpret_cast<uint64_t>(f.object),reinterpret_cast<uint64_t>(&f.refslot),0)==77&&depth==0&&suppressed==0,"depth overflow preserves native return and TLS cleanup");require(depth_errors==1&&gate.drained(),"depth overflow reports health stop");while(queue->pop(event)){}original_callback=fixture_body;
    require(!durable_append(INVALID_HANDLE_VALUE,"x",1,true),"actual invalid writer handle fails closed");
    if(argc>1){auto path=fs::path(argv[1])/L"writer.bin";HANDLE h=CreateFileW(path.c_str(),GENERIC_WRITE,FILE_SHARE_READ,nullptr,CREATE_NEW,FILE_FLAG_WRITE_THROUGH,nullptr);require(h!=INVALID_HANDLE_VALUE,"disposable writer open");require(!durable_append(h,"blocked",7,false)&&GetFileSize(h,nullptr)==0,"disk refusal prevents append");require(durable_append(h,"durable",7,true),"production append and flush");CloseHandle(h);require(sha_file(path)==sha_bytes("durable",7),"flushed evidence byte identity");}
    if(argc>1){
        auto control=fs::path(argv[1])/L"backlog-control";fs::create_directory(control);gate.state=0;
        require(queue->push(event)&&queue->push(event),"production drain starts with backlog");unsigned consumed=0,after_stop=0;
        drain_controlled(*queue,control,e,6,[&](const Event& r){++consumed;
            if(gate.state.load()&stop_bit)++after_stop;
            else require(queue->push(r),"sustained producer backlog");
            if(consumed==10)require(write_new(control/L"STOP","STOP\n"),"operator STOP while backlog nonempty");
            if(consumed>20)throw std::runtime_error("worker_control_starved");
        });
        require(gate.drained()&&consumed==12&&after_stop==2,"production drain observes STOP without empty queue");
        e[0].after[1]^=1;bool refused=false;try{worker_control(control,e,6);}catch(const std::runtime_error& error){refused=std::string(error.what())=="patch_integrity";}e[0].after[1]^=1;
        require(refused,"production control refuses patch mismatch");
    }
    mode=0;lost=0;depth_errors=0;gate.state=0;
    for(int scenario:{0,10,11,12}){
        f.refslot=scenario==12?0:reinterpret_cast<uint64_t>(f.ref);
        if(scenario!=0)fixture_query_entry(reinterpret_cast<uint64_t>(&f),scenario);
        std::vector<Event> chain;while(queue->pop(event))chain.push_back(event);
        require(chain.size()==static_cast<size_t>(scenario==0?0:scenario==10?2:scenario==11?4:6),"diagnostic stage negative exact events");
        if(argc>1){std::ofstream data(fs::path(argv[1])/("case-"+std::to_string(scenario)+".bin"),std::ios::binary);for(auto& r:chain)data.write(reinterpret_cast<const char*>(&r),sizeof r);}
    }
    f.refslot=reinterpret_cast<uint64_t>(f.ref);SetLastError(0x3456);auto chain_mxcsr=_mm_getcsr();
    require(fixture_query_entry(reinterpret_cast<uint64_t>(&f),0)==7,"Q E C exact native return");
    require(GetLastError()==0x3456&&_mm_getcsr()==chain_mxcsr,"Q E preserve FP LastError");
    std::vector<Event> chain;while(queue->pop(event))chain.push_back(event);
    require(chain.size()==9&&chain[0].kind==query_begin&&chain[1].kind==enum_begin&&chain[2].kind==begin&&chain[7].kind==enum_end&&chain[8].kind==query_end,"Q E C machine CALL trace");
    require(chain[1].parent==chain[0].invocation&&chain[2].parent==chain[1].invocation,"Q E C parent identity");
    require(field<uint32_t>(chain[8].result,0)==7,"Q native uint32 result recorded");require(field<uint64_t>(chain[6].result,0)==7,"C native uint64 return recorded");
    if(argc>1){std::ofstream data(fs::path(argv[1])/"case-positive.bin",std::ios::binary);for(auto& r:chain)data.write(reinterpret_cast<const char*>(&r),sizeof r);}
    require(abi_probe(reinterpret_cast<Callback>(&fixture_query_entry),reinterpret_cast<uint64_t>(&f),0)==0,"Q E chain nonvolatile ABI sentinels");while(queue->pop(event)){}
    require(fixture_query_entry(reinterpret_cast<uint64_t>(&f),15)==0x87654321,"Q E full EAX forwarding without bool truncation");while(queue->pop(event)){}
    bool query_fault=false;try{fixture_query_entry(reinterpret_cast<uint64_t>(&f),13);}catch(const std::runtime_error&){query_fault=true;}
    require(query_fault&&depth==0&&suppressed==0&&gate.state==0,"Q E native C++ unwind cleanup");
    std::vector<Event> failed;while(queue->pop(event))failed.push_back(event);require(failed.size()==4&&failed[2].kind==enum_unwind&&failed[3].kind==query_unwind,"Q E abnormal phases");
    require(seh_query(&f)&&depth==0&&gate.state==0,"Q E SEH propagates cleanup");while(queue->pop(event)){}
    for(auto& a:active_stages)require(a==0,"all diagnostic active scopes drained");
    if(argc>1){
        auto control=fs::path(argv[1])/"health-control";fs::create_directory(control);Health health;
        LARGE_INTEGER frequency{};require(QueryPerformanceFrequency(&frequency)!=0,"health fixture QPC frequency");
        health.open(control,"{\"component\":\"SorNativePositionOracle\",\"version\":\"0.2.0\",\"synthetic\":true,\"qpc_frequency\":"+std::to_string(frequency.QuadPart));
        auto nonce="control-0123456789abcdef0123456789abcdef.request";
        require(nonce_name(nonce)&&!nonce_name("control-bad.request"),"control nonce names exact");
        require(write_new(control/nonce,"ACK\n"),"control CREATE_NEW request");
        worker_tick=1;auto start=GetTickCount64();health.poll(control,e,6,true);auto elapsed=GetTickCount64()-start;
        require(health.serial==2&&health.acknowledged.count(nonce)==1&&elapsed<health_deadline_ms,"production no-event heartbeat and durable nonce ack within deadline");
        require(worker_tick.load()>=start,"production durable heartbeat refreshes admission tick");
        health.poll(control,e,6,true);require(health.serial==3,"nonce acknowledged once and heartbeat continues");health.close();
        std::cout<<"HEALTH_ACK_MS "<<elapsed<<'\n';
        worker_tick=1;bool write_failed=false;try{Health broken;broken.append_health("");}catch(const std::runtime_error&){write_failed=true;}require(write_failed&&worker_tick==1,"health writer failure surfaced without admission tick refresh");
    }
    worker_required=true;worker_tick=GetTickCount64()-15001;gate.state=0;require(!gate.enter()&&gate.drained()&&health_timeouts==1,"stale durable heartbeat closes producer admission");worker_required=false;health_timeouts=0;
    gate.stop();for(auto& edit:e)require(write(edit,false)&&match(edit,false),"disposable quiescent original restoration");
    std::cout<<"TOTAL "<<checks<<" PASS; no game/SFSE process executed\n";return 0;
}catch(const std::exception& e){std::cerr<<"FAIL "<<e.what()<<'\n';return 1;}}
