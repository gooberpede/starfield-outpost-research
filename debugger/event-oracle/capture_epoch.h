// SPDX-License-Identifier: GPL-3.0-or-later
// Adapted from this project runtime/beacon-observer/capture.h SHA256
// eec78be8e1f73e70c5c3b3a23b8f0870da16ec081bc4f47b94debe8905aae1f8.
// Only the sink type changes; census/run collectors are excluded.
#pragma once
#include "epoch_writer.h"
namespace beacon {
struct EpochCapture {
    Reader& r;EpochWriter& w;uint64_t module;bool partial{};
    EpochCapture(Reader& a,EpochWriter& b,uint64_t m):r(a),w(b),module(m){}
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
        workshop_output("before",p);
    }
    void workshop_output(const std::string& phase,uint64_t terrain){
        // Native producer1421b29ac/29b1 copies center+radius into this object.
        // Capture the engine's stored result; never recompute it here.
        auto output=pointer("terrain.workshop_output."+phase+".pointer",terrain+0x130,"1421b294d/2954 terrain+130 owner; lifetime unpinned");
        blob("terrain.workshop_output."+phase,output,0x100,"native output+90 XYZ/+9c radius; flags+e8/+e9/+ea; non-atomic, freshness unproven");
        blob("workshop.context."+phase,module+0x61dd460,8,"1418843c9 current workshop context global; pointer only");
    }
};
}
