// SPDX-License-Identifier: GPL-3.0-or-later
#pragma once
#include "../exp0002/win_support.h"
#include <set>
#include <deque>
#include <stdexcept>
#include <bit>
#include <algorithm>

namespace beacon {
using namespace sor;
constexpr uint64_t floor_bytes=40000000000ULL;
inline bool space_safe(uint64_t c,uint64_t d,bool queried=true){return queried&&c>=floor_bytes&&d>=floor_bytes;}
constexpr uint64_t user_end=0x00007fffffffffffULL;
inline bool range(uint64_t p,size_t n){return p>=0x10000 && n && p<=user_end && n-1<=user_end-p;}
template<class T> T at(const std::vector<unsigned char>& b,size_t o){
    if(o>b.size() || sizeof(T)>b.size()-o)throw std::runtime_error("field_extent");
    T v{};memcpy(&v,b.data()+o,sizeof v);return v;
}
inline std::string number(float v){if(!std::isfinite(v))return quote(std::isnan(v)?"NaN":v>0?"+Infinity":"-Infinity");std::ostringstream s;s<<std::setprecision(9)<<v;return s.str();}
inline bool associated(uint32_t h,uint32_t index,uint64_t metadata){return h && (h&0x1fffff)==index && !(metadata>>32) && !(metadata&0x1fffff) && (h&~0x1fffffu)==(uint32_t(metadata)&~0x1fffffu);}
inline bool label_ok(const std::string& s){return !s.empty() && s.size()<=96 && std::all_of(s.begin(),s.end(),[](unsigned char c){return (c>='a'&&c<='z')||(c>='A'&&c<='Z')||(c>='0'&&c<='9')||c=='-'||c=='_';});}
// Only filesystem operations use this abstraction. No target writes or calls.
struct Writer {
    fs::path dir; HANDLE log=INVALID_HANDLE_VALUE; uint64_t serial{},bytes{};
    std::function<bool()> guard;
    Writer(fs::path d,std::function<bool()> g):dir(std::move(d)),guard(std::move(g)){
        if(!guard())throw std::runtime_error("disk_guard");
        if(!fs::create_directory(dir))throw std::runtime_error("snapshot_collision");
        log=CreateFileW((dir/L"records.jsonl").c_str(),GENERIC_WRITE,FILE_SHARE_READ,nullptr,CREATE_NEW,FILE_FLAG_WRITE_THROUGH,nullptr);
        if(log==INVALID_HANDLE_VALUE)throw std::runtime_error("journal_open");
    }
    Writer(const Writer&)=delete;
    ~Writer(){if(log!=INVALID_HANDLE_VALUE)CloseHandle(log);}
    void write(HANDLE h,const void* p,size_t n){
        const auto* b=static_cast<const unsigned char*>(p);
        while(n){if(!guard())throw std::runtime_error("disk_guard");DWORD k=static_cast<DWORD>(std::min<size_t>(n,65536)),got{};
            if(!WriteFile(h,b,k,&got,nullptr)||got!=k)throw std::runtime_error("writer_integrity");b+=k;n-=k;bytes+=k;}
        if(!FlushFileBuffers(h))throw std::runtime_error("flush_failed");
    }
    void event(const std::string& s){auto line=s+"\n";write(log,line.data(),line.size());}
    void status(const std::string& root,const char* state,const std::string& why){event("{\"kind\":\"status\",\"root\":"+quote(root)+",\"state\":"+quote(state)+",\"reason\":"+quote(why)+",\"utc\":"+quote(utc())+"}");}
    void raw(const std::string& root,uint64_t p,const void* b,size_t n,const std::string& origin){
        auto name="raw-"+std::to_string(++serial)+".bin";
        HANDLE f=CreateFileW((dir/name).c_str(),GENERIC_WRITE,FILE_SHARE_READ,nullptr,CREATE_NEW,FILE_FLAG_WRITE_THROUGH,nullptr);
        if(f==INVALID_HANDLE_VALUE)throw std::runtime_error("raw_open");
        try{write(f,b,n);}catch(...){CloseHandle(f);throw;}CloseHandle(f);
        auto hash=sha_bytes(b,n);if(hash.empty())throw std::runtime_error("hash_failed");
        event("{\"kind\":\"raw\",\"root\":"+quote(root)+",\"address_domain\":\"runtime_VA\",\"address\":"+quote(hex(p))+",\"bytes\":"+std::to_string(n)+",\"file\":"+quote(name)+",\"sha256\":"+quote(hash)+",\"origin\":"+quote(origin)+",\"utc\":"+quote(utc())+"}");
    }
    void finish(const std::string& terminal){
        auto data="{\"terminal\":"+quote(terminal)+",\"bytes_written_before_marker\":"+std::to_string(bytes)+"}\n";
        if(!guard())throw std::runtime_error("disk_guard");
        // Marker is independent of journal; no replacement of earlier evidence.
        HANDLE f=CreateFileW((dir/L"complete.json").c_str(),GENERIC_WRITE,FILE_SHARE_READ,nullptr,CREATE_NEW,FILE_FLAG_WRITE_THROUGH,nullptr);
        if(f==INVALID_HANDLE_VALUE)throw std::runtime_error("marker_open");
        try{write(f,data.data(),data.size());}catch(...){CloseHandle(f);throw;}CloseHandle(f);
    }
};
struct Capture {
    Reader& r;Writer& w;uint64_t module;bool partial{};
    Capture(Reader& a,Writer& b,uint64_t m):r(a),w(b),module(m){}
    void issue(const std::string& name,const char* state,const std::string& reason){partial=true;w.status(name,state,reason);}
    bool read(uint64_t p,size_t n,std::vector<unsigned char>& b){b.assign(n,0);return range(p,n)&&r.bytes(p,b.data(),n);}
    bool blob(const std::string& name,uint64_t p,size_t n,const std::string& origin,std::vector<unsigned char>* result=nullptr){
        if(!p){issue(name,"NOT_OBSERVED","null_pointer");return false;}
        std::vector<unsigned char> b;
        if(!read(p,n,b)){issue(name,"UNREADABLE",hex(p));return false;}
        w.raw(name,p,b.data(),n,origin);if(result)*result=std::move(b);return true;
    }
    uint64_t pointer(const std::string& name,uint64_t p,const std::string& origin){std::vector<unsigned char> b;if(!blob(name,p,8,origin,&b))return 0;return at<uint64_t>(b,0);}
    void table(const std::string& name,uint64_t p,uint64_t count,uint64_t stride){
        if(!count)return;
        if(count>user_end/stride || !range(p,static_cast<size_t>(count*stride))){issue(name,"UNEXPECTED","table_extent_overflow");return;}
        uint64_t bytes=count*stride;
        for(uint64_t offset=0;offset<bytes;){
            auto n=static_cast<size_t>(std::min<uint64_t>(bytes-offset,65536));
            if(!blob(name,p+offset,n,"workshop+30 table/+38 capacity; 24-byte initialized entries; byte_offset="+std::to_string(offset)))break;
            offset+=n;
        }
    }
    void extras(const std::string& name,uint64_t p){
        std::vector<unsigned char> list;
        if(!blob(name,p,0x20,"reference+0xc8 -> list; head+8 from 140517d60",&list))return;
        uint64_t node=at<uint64_t>(list,8);std::set<uint64_t> visited;
        while(node){
            if(!visited.insert(node).second){issue(name,"UNEXPECTED","cyclic_extra_chain:"+hex(node));break;}
            std::vector<unsigned char> b;
            if(!blob(name+".node",node,0x18,"extra head/next+8/type+0x12",&b))break;
            auto type=b[0x12];uint64_t next=at<uint64_t>(b,8);
            // Schema extents, not a quota. Unknown extra nodes retain header only.
            if(type==0xbc){std::vector<unsigned char> workshop;
                if(blob(name+".workshop",node,0xa0,"14053ddbb allocation0xa0; 140f4ffc0 constructor",&workshop))
                    table(name+".workshop.table",at<uint64_t>(workshop,0x30),at<uint64_t>(workshop,0x38),24);
            }
            if(type==0x81)blob(name+".cached_planet",node,0x40,"140910690 cached angles+18/+20 body+28 associated+38");
            if(type==0x80)blob(name+".linked",node,0x20,"140517d60 linked-ref type; payload schema UNSUPPORTED");
            node=next;
        }
    }
    void cell(const std::string& name,uint64_t p){
        std::vector<unsigned char> b;if(!blob(name,p,0x118,"stored CELL +b0; identity+28/type+2e/exterior+48/world+110",&b))return;
        if(b[0x2e]!=0x49){issue(name,"UNEXPECTED","cell_type");return;}
        if(at<uint32_t>(b,0x48)&1){issue(name,"UNSUPPORTED","interior_world_branch");return;}
        auto world=at<uint64_t>(b,0x110);
        // Largest inspected world field+388 is evidence for this prefix extent.
        blob(name+".world",world,0x390,"CELL+110; world overlay gate+20/+388 at140ad3b20");
    }
    void reference(const std::string& name,uint64_t p,uint32_t index=0,uint64_t metadata=0){
        std::vector<unsigned char> b,z;
        if(!blob(name,p,0xd0,"TESObjectREFR scalar prefix through extra+c8",&b))return;
        uint32_t id=at<uint32_t>(b,0x28),h=at<uint32_t>(b,0x24);auto base=at<uint64_t>(b,0x98);uint32_t bid{};
        bool base_ok=range(base,0x30)&&r.get(base+0x28,bid);
        if((name=="player"&&(id!=0x14||b[0x2e]!=0x4b)) || (index&&(!base_ok||bid!=0x2c60e9||b[0x2e]!=0x4a))){
            issue(name,"CAPTURE_PARTIAL","trusted_root_identity_mismatch");return;
        }
        bool stable=read(p,0xd0,z)&&std::equal(b.begin()+0x24,b.begin()+0x30,z.begin()+0x24)&&at<uint64_t>(z,0x98)==base;
        std::array<uint64_t,2> slot{};
        bool slot_equal=!index || (r.get(module+0x62d1400+16ULL*index,slot)&&slot[0]==p&&slot[1]==metadata);
        stable=stable&&slot_equal;
        w.event("{\"kind\":\"reference\",\"root\":"+quote(name)+",\"pointer\":"+quote(hex(p))+",\"formid\":"+quote(hex(id,8))+",\"stored_base_formid\":"+(base_ok?quote(hex(bid,8)):"null")+",\"type\":"+std::to_string(b[0x2e])+",\"handle_candidate\":"+quote(hex(h,8))+",\"slot_index\":"+std::to_string(index)+",\"observational_handle_association\":"+(index&&slot_equal&&associated(h,index,metadata)?"true":"false")+",\"identity_repeated_equal\":"+(stable?"true":"false")+",\"xyz\":["+number(at<float>(b,0x8c))+","+number(at<float>(b,0x90))+","+number(at<float>(b,0x94))+"],\"rotation_raw\":["+number(at<float>(b,0x80))+","+number(at<float>(b,0x84))+","+number(at<float>(b,0x88))+"],\"snapshot_atomic\":false}");
        if(!stable){issue(name,"CAPTURE_PARTIAL","identity_changed");return;}
        cell(name+".cell",at<uint64_t>(b,0xb0));
        extras(name+".extra",at<uint64_t>(b,0xc8));
    }
    void terrain(){
        auto p=pointer("terrain.global",module+0x5fd9c30,"140910690 terrain singleton RVA5fd9c30");
        std::vector<unsigned char> b;if(!blob("terrain",p,0x200,"14078d1f0 mode+20 origins+c8/+1c0;140910690 body+80/state+78",&b))return;
        auto state=at<uint64_t>(b,0x78);
        auto active=pointer("terrain.active_indirect",state,"terrain+78 -> indirect active state");
        blob("terrain.active",active,0xa0,"140910690 state flags+14/current world+98");
        if(active){std::vector<unsigned char> a;if(read(active,0xa0,a))blob("terrain.active_world",at<uint64_t>(a,0x98),0x390,"active state+98 world candidate");}
        auto terrain_owner=at<uint64_t>(b,0x120); // outside b? +120 is within 0x200
        std::vector<unsigned char> owner;
        if(blob("terrain.owner",terrain_owner,0x60,"14078d2c0 manager+120 -> owner+58",&owner))
            blob("terrain.grid",at<uint64_t>(owner,0x58),0x100,"14096da90 grid resolution+50; manager+120/owner+58");
        blob("stitch.block",module+0x5ea66f0,4,"14008cb90 B default component");
        blob("stitch.merge",module+0x5ea6770,4,"14008cc50 B merge component");
    }
    void census(){
        // Adapted algorithm from maintainer census.cpp; exact binding is checked,
        // never a broad memory search or assumed transferable layout.
        uint64_t p=module+0x62d1380;std::vector<unsigned char> mgr;
        if(!blob("handles.manager",p,0x70,"gooberpede census binding reference",&mgr))return;
        if(at<uint64_t>(mgr,0)!=module+0x4cb2e98 || at<uint64_t>(mgr,0x50)!=module+0x62d1400 || at<uint32_t>(mgr,0x64)!=0x200000 || at<uint32_t>(mgr,0x68)!=0x1fffff){issue("handles","UNSUPPORTED","binding_mismatch");return;}
        auto published=pointer("handles.published",module+0x5e60380,"reference manager publication global");
        if(published!=p){issue("handles","UNEXPECTED","published_manager_mismatch");return;}
        uint64_t pool=at<uint64_t>(mgr,0x50);uint64_t found=0;
        for(uint32_t index=0;index<0x200000;index+=4096){
            std::vector<unsigned char> b,z;auto address=pool+16ULL*index;
            if(!blob("handles.pool",address,4096*16,"fixed validated pool; 16-byte slots; index="+std::to_string(index),&b))continue;
            if(!read(address,b.size(),z)){issue("handles.pool","UNREADABLE","repeat");continue;}
            for(uint32_t j=0;j<4096;++j){size_t o=j*16;uint64_t obj=at<uint64_t>(b,o),meta=at<uint64_t>(b,o+8);
                if(!index&&!j)continue;
                if(!obj || (meta>>32)||(meta&0x1fffff))continue;
                if(memcmp(b.data()+o,z.data()+o,16)){issue("handles.slot","CAPTURE_PARTIAL","slot_changed:"+std::to_string(index+j));continue;}
                std::vector<unsigned char> ref; if(!read(obj,0xa0,ref)){issue("handles.occupied","UNREADABLE",hex(obj));continue;}
                if(ref[0x2e]!=0x4a)continue;
                auto base=at<uint64_t>(ref,0x98);uint32_t bid{};
                if(!range(base,0x30)||!r.get(base+0x28,bid))continue;
                if(bid!=0x2c60e9)continue;
                ++found;reference("beacon-"+std::to_string(index+j),obj,index+j,meta);
            }
        }
        blob("handles.manager.after",p,0x70,"non-atomic scan end bracket");
        w.event("{\"kind\":\"census\",\"ordinary_candidates\":"+std::to_string(found)+",\"scope\":\"occupied reference pool; stored base2c60e9; completeness not claimed\"}");
        if(!found)issue("beacons","NOT_OBSERVED","no_ordinary_candidate_in_pool");
    }
    void run(){
        auto began=GetTickCount64();
        auto player=pointer("player.global",module+0x5f43230,"GetPlayer RVA177a1f0 -> singleton");
        if(player)reference("player",player);
        auto player_done=GetTickCount64();terrain();auto terrain_done=GetTickCount64();census();
        w.event("{\"kind\":\"collector_metrics\",\"player_ms\":"+std::to_string(player_done-began)+",\"terrain_ms\":"+std::to_string(terrain_done-player_done)+",\"census_ms\":"+std::to_string(GetTickCount64()-terrain_done)+"}");
        w.status("native_queries","UNSUPPORTED","No native calls; execution-context affinity not assumed");
        w.finish(partial?"CAPTURE_PARTIAL":"ACQUISITION_COMPLETE_SEMANTICS_UNASSESSED");
    }
};
}
