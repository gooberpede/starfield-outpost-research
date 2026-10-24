// SPDX-License-Identifier: GPL-3.0-or-later
// Native ABI stops; target bytes are observations, transitions are reconstructed
// separately; agreement and disagreement with the next snapshot are retained.
bool ok=true;
auto copy=[&](const char* name,uint64_t at,size_t n){
    std::vector<unsigned char> b(n),verify(n);bool got=reader(at,b.data(),n)&&reader(at,verify.data(),n)&&b==verify;ok=ok&&got;
    row<<",\""<<name<<"\":{\"status\":\""<<(got?"COMPLETE":"INCOMPLETE")<<"\",\"address\":"<<at<<",\"raw\":";
    if(got)row<<'"'<<hex(b.data(),n)<<'"';else row<<"null";row<<'}';return b;
};
if(c.Rip==base+diagnostic[1]){
    // Remove observed stack reuse/unwind before admitting another invocation.
    while(!t.frames.empty()&&t.frames.back().entry<=c.Rsp)t.frames.pop_back();
    require(t.frames.size()<64,"generation nesting budget");
    owner_capture::Frame f;f.entry=c.Rsp;f.token=++t.gen_serial;f.source=c.Rcx;f.owner=uint32_t(c.R9);
    t.frames.push_back(f);t.gen_entry=f.entry;
    copy("source",c.Rcx,0x70);copy("origin",c.Rdx,8);copy("source_descriptor",c.R8,0x18);
    auto caller=copy("generation_caller",c.Rsp,8);
    ok=ok&&retail::field<uint64_t>(caller.data(),0)==base+extra[2];
    row<<",\"owner_key_u32\":"<<f.owner;
    rvas[2]=diagnostic[2];rvas[3]=diagnostic[3];
}
bool frame=!t.frames.empty();
if(frame){
    auto& f=t.frames.back();auto F=f.entry-0x2d8;
    copy("source_retained",f.source,0x70);
    uint64_t manager=0;
    if(reader(base+0x5fd9c30,&manager,8))copy("current_manager",manager,0x200);else ok=false;
    row<<",\"invocation_token\":"<<f.token<<",\"parent_token\":"<<(t.frames.size()>1?t.frames[t.frames.size()-2].token:0)
       <<",\"generation_entry_rsp\":"<<f.entry<<",\"source_pointer\":"<<f.source;
    if(c.Rip==base+diagnostic[2]||c.Rip==base+diagnostic[3]){
        frame=c.Rsp==F-0x160&&f.phase==0;
        uint64_t ret=0,outer=0;
        frame=frame&&reader(c.Rsp+0x108,&ret,8)&&ret==base+0x7bc374
                   &&reader(F-8,&outer,8)&&outer==base+extra[0];
#ifdef RETAIL_FIXTURE
        // The fixture exports its two true return instructions. No caller
        // identity is inferred from the packet or from temporal adjacency.
        frame=c.Rsp==F-0x160&&f.phase==0&&reader(c.Rsp+0x108,&ret,8)&&ret==base+exported(image,"map_wrapper_return")
                   &&reader(F-8,&outer,8)&&outer==base+extra[0];
#endif
        if(!f.map)f.map=c.R15;
        frame=frame&&f.map==c.R15;
        auto mapping=owner_capture::map(reader,c.R15),staging=owner_capture::array(reader,c.Rsp+0x20);
        ok=ok&&mapping.find("INCOMPLETE")==std::string::npos&&staging.find("INCOMPLETE")==std::string::npos;
        row<<",\"map\":"<<mapping<<",\"staging\":"<<staging;
        if(c.Rip==base+diagnostic[2]){
            copy("registered_component_type",base+0x61dfa4c,2);
            auto it=copy("iterator",c.Rbx,0x38);
            uint64_t page=retail::field<uint64_t>(it.data(),0x18),ordinal=retail::field<uint64_t>(it.data(),0x20);
            uint16_t displacement=0;
            bool node_ok=ordinal<0xfe0&&reader(page+0x12+ordinal*4,&displacement,2);
            uint64_t node=page+displacement;
            if(node_ok)copy("component",node,0x8c);else ok=false;
            row<<",\"component_ordinal\":"<<f.loops++<<",\"page\":"<<page<<",\"page_ordinal\":"<<ordinal<<",\"node_displacement\":"<<displacement;
        }else{
            f.phase=1;rvas[2]=extra[0];rvas[3]=extra[2];
            row<<",\"visited_count\":"<<f.loops<<",\"construction_boundary\":\"CLEANUP_BEFORE_STAGING_FREE\"";
        }
    }else if(c.Rip==base+extra[0]){
        frame=c.Rsp==F&&f.phase==1&&f.map==F+0x210;
        auto mapping=owner_capture::map(reader,F+0x210);ok=ok&&mapping.find("INCOMPLETE")==std::string::npos;
        row<<",\"map\":"<<mapping;
        copy("selected_root",F+0x130,4);f.phase=2;rvas[2]=extra[3];
    }else if(c.Rip==base+extra[3]){
        frame=c.Rsp==F&&f.phase==2;
        auto candidates=owner_capture::array(reader,F+0x40,8,16);ok=ok&&candidates.find("INCOMPLETE")==std::string::npos;
        row<<",\"candidate_array\":"<<candidates;
        f.phase=3;rvas[2]=extra[1];
    }else if(c.Rip==base+extra[1]){
        frame=c.Rsp==F&&f.phase==3;
        auto ires=copy("ires",c.Rdx,0x118);copy("selected_dnam",c.R8,560);
        row<<",\"file_provenance\":"<<retail::provenance(reader,c.Rdx,base,retail::field<uint32_t>(ires.data(),0x28)).json();
        copy("family_root_formid",F+0x58,4);copy("per_biome_data",F+0xe0,0x6c);
        auto candidates=owner_capture::array(reader,F+0x40,8,16);ok=ok&&candidates.find("INCOMPLETE")==std::string::npos;
        row<<",\"candidate_array\":"<<candidates
           <<",\"effective_weight_bits\":"<<uint32_t(c.Xmm3.Low);
    }else if(c.Rip==base+extra[2]){
        frame=c.Rsp==f.entry+8;
        row<<",\"construction_completed\":"<<(f.phase>=2?"true":"false");
        t.frames.pop_back();t.gen_entry=t.frames.empty()?0:t.frames.back().entry;
        if(t.frames.empty()){rvas[2]=diagnostic[2];rvas[3]=diagnostic[3];}
        else{auto outer_phase=t.frames.back().phase;rvas[2]=outer_phase==0?diagnostic[2]:outer_phase==1?extra[0]:outer_phase==2?extra[3]:extra[1];rvas[3]=outer_phase==0?diagnostic[3]:extra[2];}
    }
}
row<<",\"frame_matches\":"<<(frame?"true":"false")<<",\"required_reads_complete\":"<<(ok?"true":"false")
   <<",\"diagnostic_scope\":\"ORDERED_OWNER_CONSTRUCTION\",\"generation_epoch\":null,\"consumer_join\":null,\"useful_success\":false";
