// SPDX-License-Identifier: GPL-3.0-or-later
// D5E read-only native adapter. The four sites never rotate.
// Lifetime witnesses are deliberately absent; native reduction cannot emit A/B.
auto working=slot==2?c.Rsp+0x2e0:c.Rsp;
bool complete=true;
auto copy=[&](const char* label,uint64_t address,size_t size){
    std::vector<unsigned char> b(size);bool ok=read(address,b.data(),size);
    std::cout<<",\""<<label<<"\":{\"address\":"<<address<<",\"complete\":"<<(ok?"true":"false")<<",\"raw\":\""<<(ok?hex(b.data(),size):std::string())<<"\"}";
    if(!ok){complete=false;b.clear();}return b;
};
auto word=[&](const char* label,uint64_t address){auto b=copy(label,address,8);return b.empty()?uint64_t(0):retail::field<uint64_t>(b.data(),0);};
std::cout<<",\"native\":true,\"provider_working_rsp\":"<<working;
auto source=word("source_pointer",working+0x38);
auto procgen=word("procgen_pointer",working+0x3d0);
auto query=word("query_pointer",working+0x3d8);
auto owner=word("manager_pointer",base+0x5fd9c30);
auto manager=copy("manager",owner,0x200);
copy("source",source,0x70);copy("original_query",query,8);
auto capacity=word("capacity",procgen+0x28);
auto slots=word("slots",procgen+0x20);
bool frame=(slot==2?word("generation_return",c.Rsp+0x2d8)==base+0x79ff1d:c.Rbp==working+0x100);
frame=frame&&!manager.empty()&&retail::field<uint64_t>(manager.data(),0x130)==procgen;
if(slot!=2)frame=frame&&c.R13==procgen;
std::cout<<",\"frame_valid\":"<<(frame?"true":"false")<<",\"decision_operand\":"<<(slot==0?(c.Rsi&255):slot==1?c.Rax:slot==2?(c.Rax&255):0);
if(slot==0)std::cout<<",\"visited_key_operand\":"<<c.Rdi;
if(slot==1&&c.Rax<capacity&&capacity<=4096)copy("lookup_slot",slots+c.Rax*24,24);
if(slot==2){auto at=word("geographic_pointer",c.Rsp+0x2f0);copy("geographic_query",at,0x18);}
if(slot==3){
    if(capacity<=4096&&capacity>0)copy("retained_slots",slots,size_t(capacity)*24);
    else if(capacity>4096)complete=false;
    copy("conversion_descriptor",c.R8,0x2c);
    copy("conversion_original_query",c.R9,8);
    std::cout<<",\"conversion_query_pointer\":"<<c.R9;
}
// Equal copies validate this stop only; they cannot detect between-stop ABA.
copy("source_again",source,0x70);copy("original_query_again",query,8);
auto owner_again=word("manager_pointer_again",base+0x5fd9c30);
copy("manager_again",owner_again,0x200);
std::cout<<",\"native_read_complete\":"<<(complete?"true":"false")<<",\"lifetime\":null";
