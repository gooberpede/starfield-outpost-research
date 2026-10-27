// SPDX-License-Identifier: GPL-3.0-or-later
// Original external reader for the pinned D5L native boundary contract.
// Included after owned read/hex helpers. No target writes or native calls.
#pragma once
namespace d5l_native {
enum Site {Visited,Lookup,Query,Mask,Append,Complete,Init,Reset,Destroy,Erase,GridClear,SourceInit,GridInit,SourceRetire};
static constexpr unsigned site_count=14;
static const char* names[]={"native_visited","native_lookup","native_query","native_mask","native_append","native_complete","native_init","native_reset","native_destroy","native_erase","native_grid_clear","native_source_init","native_grid_init","native_source_retire"};
static const uint32_t rvas[]={0x79fca3,0x79fcd0,0x79feaf,0x79b8ed,0x79acf2,0x79ff1d,0x79d8b2,0x79de92,0x79d910,0x975030,0x9829b0,0x983140,0x9828d5,0x982b70};
// These authored lengths/flow targets must agree with the pinned existing
// instructions; qualification binds each mapped instruction to its PE backing.
struct Config {uint32_t singleton=0x5fd9c30,inner_return=0x79c4fc;
    uint32_t outer_returns[3]={0x79be25,0x79c047,0x79c11c};uint32_t complete=0x79ff1d;
    uint32_t grid_vtable=0x4b67f48,procgen_vtable=0x4b3f3a8;};
struct Reader {
    bool ok=true;
    bool get(uint64_t at,void* p,size_t n){bool good=read(at,p,n);ok&=good;return good;}
    uint64_t q(uint64_t at){uint64_t v=0;get(at,&v,8);return v;}
    uint32_t u(uint64_t at){uint32_t v=0;get(at,&v,4);return v;}
    std::string raw(uint64_t at,size_t n){if(!n)return {};std::vector<unsigned char>b(n);return get(at,b.data(),n)?hex(b.data(),n):std::string();}
};
static std::string region(Reader& r,uint64_t at){
    unsigned char header[48]{};bool good=r.get(at,header,48);
    uint32_t count=retail::field<uint32_t>(header,0x18),cap=retail::field<uint32_t>(header,0x1c);
    uint64_t data=retail::field<uint64_t>(header,0x20);
    good=good&&count<=cap&&cap<=4096;
    if(!good)r.ok=false;
    std::string points=good?r.raw(data,size_t(count)*16):std::string();
    if(count&&points.empty())good=false;
    std::ostringstream s;s<<"{\"address\":"<<at<<",\"read_complete\":"<<(good?"true":"false")
      <<",\"header\":\""<<hex(header,48)<<"\",\"points\":\""<<points<<"\"}";return s.str();
}
static std::string population(Reader& r,uint64_t procgen,uint64_t source){
    uint64_t slots=r.q(procgen+0x20),capacity=r.q(procgen+0x28),wrapper=0,index=capacity;
    bool good=capacity<=4096;
    if(good)for(uint64_t i=0;i<capacity;++i){unsigned char s[24]{};if(!r.get(slots+i*24,s,24)){good=false;break;}
        if(retail::field<uint32_t>(s,16)!=0xffffffffU&&retail::field<uint64_t>(s,0)==source){
            if(index!=capacity){good=false;break;}wrapper=retail::field<uint64_t>(s,8);index=i;}}
    auto slot_raw=index<capacity?r.raw(slots+index*24,24):std::string();
    std::ostringstream out;out<<"{\"source\":"<<source<<",\"wrapper\":"<<wrapper<<",\"slot_index\":"<<index<<",\"capacity\":"<<capacity<<",\"slot_raw\":\""<<slot_raw<<"\",\"resources\":[";
    bool comma=false;
    if(good&&wrapper){
        auto references=r.u(wrapper);good=references>0&&references!=0xffffffffU;
        uint64_t resource_slots=r.q(wrapper+0x20),resource_capacity=r.q(wrapper+0x28);
        good=good&&resource_capacity<=4096;
        if(good)for(uint64_t i=0;i<resource_capacity;++i){unsigned char s[24]{};if(!r.get(resource_slots+i*24,s,24)){good=false;break;}
            if(retail::field<uint32_t>(s,16)==0xffffffffU)continue;
            uint32_t resource=retail::field<uint32_t>(s,0);uint64_t collection=retail::field<uint64_t>(s,8);
            if(!collection){good=false;continue;}
            auto collection_references=r.u(collection);if(!collection_references||collection_references==0xffffffffU){good=false;continue;}
            auto count=r.u(collection+8),cap=r.u(collection+12);auto data=r.q(collection+16);
            if(count>cap||cap>4096){good=false;continue;}
            if(comma)out<<',';comma=true;out<<"{\"resource\":"<<resource<<",\"collection\":"<<collection<<",\"resource_slot_raw\":\""<<hex(s,24)<<"\",\"collection_header\":\""<<r.raw(collection,24)<<"\",\"regions\":[";
            for(uint32_t j=0;j<count;++j){if(j)out<<',';out<<region(r,data+uint64_t(j)*48);if(!r.ok)break;}
            out<<"]}";
        }
    }
    good&=r.ok;if(!good)r.ok=false;
    out<<"],\"read_complete\":"<<(good?"true":"false")<<"}";return out.str();
}
static void capture(unsigned site,const CONTEXT& c,uint64_t base,const Config& config){
    Reader r;auto manager=r.q(base+config.singleton);
    std::cout<<",\"native_abi\":true,\"event\":\""<<names[site]<<"\",\"manager\":"<<manager;
    if(site==Init||site==Reset||site==Destroy){
        auto procgen=site==Init?c.Rdi:site==Reset?c.Rsi:c.Rcx;
        std::cout<<",\"procgen\":"<<procgen;
        if(site==Init||site==Reset){
            auto slots=r.q(procgen+0x20),cap=r.q(procgen+0x28);bool empty=cap<=4096&&r.q(procgen)==base+config.procgen_vtable;
            if(empty)for(uint64_t i=0;i<cap;++i)empty&=r.u(slots+i*24+16)==0xffffffffU;
            std::cout<<",\"empty_source_map\":"<<(empty&&r.ok?"true":"false");
        }
        std::cout<<",\"read_complete\":"<<(r.ok?"true":"false");return;
    }
    if(site==GridClear){std::cout<<",\"grid\":"<<c.Rcx<<",\"read_complete\":"<<(r.ok?"true":"false");return;}
    if(site==SourceRetire){std::cout<<",\"source\":"<<c.Rcx<<",\"read_complete\":"<<(r.ok?"true":"false");return;}
    if(site==GridInit){std::cout<<",\"grid\":"<<c.R15<<",\"initialized_type\":"<<(r.q(c.R15)==base+config.grid_vtable?"true":"false")<<",\"read_complete\":"<<(r.ok?"true":"false");return;}
    if(site==SourceInit){
        std::cout<<",\"source\":"<<c.R14<<",\"grid\":"<<c.R12-0x10<<",\"definition\":"<<c.R13
          <<",\"source_raw\":\""<<r.raw(c.R14,0x70)<<"\",\"read_complete\":"<<(r.ok?"true":"false");return;
    }
    auto current_procgen=manager?r.q(manager+0x130):0;
    if(site==Erase){
        bool related=current_procgen&&c.Rcx==current_procgen+0x10;
        auto cap=related?r.q(current_procgen+0x28):0;
        auto slots=related?r.q(current_procgen+0x20):0;
        unsigned char raw[24]{};bool valid=related&&c.Rdx<cap&&cap<=4096&&r.get(slots+c.Rdx*24,raw,24);
        std::cout<<",\"procgen\":"<<current_procgen<<",\"related_map\":"<<(related?"true":"false")
          <<",\"source\":"<<(valid?retail::field<uint64_t>(raw,0):0)<<",\"slot\":\""<<(valid?hex(raw,24):std::string())
          <<"\",\"read_complete\":"<<(r.ok&&(!related||valid)?"true":"false");return;
    }
    uint64_t w=c.Rsp+(site==Mask?0x2e0:site==Append?0x560:0);
    auto source=r.q(w+0x38),procgen=r.q(w+0x3d0),query=r.q(w+0x3d8),grid=r.q(w+0x100);
    unsigned char owner[0x200]{},s[0x70]{},q[8]{},descriptor[0x2c]{};
    r.get(manager,owner,sizeof owner);r.get(source,s,sizeof s);r.get(query,q,8);
    auto desc=manager+(owner[0x20]==3?0x1c0:0xc8);r.get(desc,descriptor,sizeof descriptor);
    bool frame=procgen==current_procgen;
    if(site==Mask)frame&=r.q(c.Rsp+0x2d8)==base+config.complete;
    else if(site==Append){
        auto outer=r.q(c.Rsp+0x278);bool caller=false;for(auto at:config.outer_returns)caller|=outer==base+at;
        frame&=r.q(c.Rsp+0x208)==base+config.inner_return&&caller&&r.q(c.Rsp+0x558)==base+config.complete;
    }else frame&=c.Rbp==w+0x100&&c.R13==procgen;
    if(site==Query)frame&=c.R8==desc&&c.R9==query;
    // Provider retains this concrete grid throughout enumeration. Membership
    // confirms the source belongs to that owner, without using geographic names.
    auto count=r.u(grid+0x10),cap=r.u(grid+0x14);auto sources=r.q(grid+0x18);
    bool member=false;if(count<=cap&&cap<=4096){for(uint32_t i=0;i<count;++i)member|=r.q(sources+uint64_t(i)*8)==source;}else r.ok=false;
    frame&=member&&r.q(r.q(manager+0x120)+0x10)==grid&&r.q(grid)==base+config.grid_vtable&&r.q(procgen)==base+config.procgen_vtable;
    auto axis=[&](unsigned at,unsigned coarse,unsigned sub,unsigned residual){return int64_t(retail::field<int32_t>(s,at))+
        int64_t(retail::field<int32_t>(descriptor,coarse))*192+int64_t(retail::field<int32_t>(descriptor,sub))*12+retail::field<int32_t>(descriptor,residual);};
    bool selected=descriptor[0]==0&&retail::field<uint32_t>(s,0)==0x29d20e&&retail::field<uint32_t>(owner,0x80)==0x5e0de
        &&axis(0x10,4,0x14,0x24)==37536&&axis(0x14,8,0x18,0x28)==20928;
    std::cout<<",\"working_rsp\":"<<w<<",\"source\":"<<source<<",\"procgen\":"<<procgen<<",\"grid\":"<<grid
      <<",\"query_pointer\":"<<query<<",\"descriptor_pointer\":"<<desc
      <<",\"source_raw\":\""<<hex(s,sizeof s)<<"\",\"manager_raw\":\""<<hex(owner,sizeof owner)<<"\",\"query_raw\":\""<<hex(q,8)
      <<"\",\"descriptor_raw\":\""<<hex(descriptor,sizeof descriptor)<<"\",\"selected\":"<<(selected?"true":"false")<<",\"frame_valid\":"<<(frame?"true":"false");
    if(site==Visited)std::cout<<",\"operand\":"<<(c.Rsi&255)<<",\"visited_key\":"<<c.Rdi;
    if(site==Lookup){std::cout<<",\"operand\":"<<c.Rax<<",\"lookup_capacity\":"<<r.q(procgen+0x28);if(selected)std::cout<<",\"population\":"<<population(r,procgen,source);}
    if(selected&&(site==Query||site==Complete))std::cout<<",\"population\":"<<population(r,procgen,source);
    if(site==Mask)std::cout<<",\"operand\":"<<(c.Rax&255)<<",\"geographic_raw\":\""<<r.raw(r.q(c.Rsp+0x2f0),24)<<'"';
    if(site==Append&&selected){
        auto index=uint32_t(c.Rax);auto n=r.u(c.Rbx+8);auto data=r.q(c.Rbx+16);
        std::cout<<",\"append_index\":"<<index<<",\"collection\":"<<c.Rbx<<",\"resource\":"<<r.u(c.Rsp+0x230)
          <<",\"temporary\":"<<region(r,c.Rsp+0x50)<<",\"destination\":";
        if(index<n&&index!=0xffffffffU)std::cout<<region(r,data+uint64_t(index)*48);else std::cout<<"null";
    }
    unsigned char again_s[0x70]{},again_q[8]{},again_owner[0x200]{};
    bool same=r.get(source,again_s,sizeof s)&&!memcmp(s,again_s,sizeof s)&&r.get(query,again_q,8)&&!memcmp(q,again_q,8)
        &&r.q(base+config.singleton)==manager&&r.get(manager,again_owner,sizeof owner)&&!memcmp(owner,again_owner,sizeof owner);
    std::cout<<",\"read_complete\":"<<(r.ok&&same?"true":"false");
}
}
