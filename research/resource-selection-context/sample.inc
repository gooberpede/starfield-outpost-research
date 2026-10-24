// SPDX-License-Identifier: GPL-3.0-or-later
// Included in the owned all-stop engine. No target-memory writes or borrowed pointers.
bool complete=true;
auto copy=[&](const char* name,uint64_t at,size_t n)->std::vector<unsigned char>{
    std::vector<unsigned char> b(n);
    bool ok=retail::range(at,n)&&reader(at,b.data(),n);
    row<<",\""<<name<<"\":{\"address\":"<<at<<",\"bytes\":"<<n
       <<",\"status\":\""<<(ok?"COMPLETE":"INCOMPLETE")<<"\",\"raw\":";
    if(ok)row<<'"'<<hex(b.data(),n)<<'"';else row<<"null";
    row<<'}';if(!ok){complete=false;b.clear();}return b;
};
auto word=[&](const char* name,uint64_t at)->uint64_t{
    auto b=copy(name,at,8);return b.empty()?0:retail::field<uint64_t>(b.data(),0);
};
auto xmm=[](const M128A& x){uint32_t v{};memcpy(&v,&x,4);return v;};
// Snapshot ordered definition arrays with explicit bounds. This records candidates,
// not an independently executed winner algorithm or an all-writer guarantee.
auto descriptors=[&](const char* label,uint64_t biom,uint64_t effective){
    row<<",\""<<label<<"\":{\"biom_pointer\":"<<biom<<",\"rsgds\":[";
    auto emit=[&](uint64_t ptr){
        row<<"{\"pointer\":"<<ptr;
        auto header=copy("header",ptr,0x48);
        if(!header.empty()){
            row<<",\"file_provenance\":"<<retail::provenance(reader,ptr,base,retail::field<uint32_t>(header.data(),0x28)).json();
            auto n=retail::field<uint32_t>(header.data(),0x38);
            auto begin=retail::field<uint64_t>(header.data(),0x40);
            row<<",\"count\":"<<n;
            if(n>64){complete=false;row<<",\"loss\":\"DESCRIPTOR_COUNT_BOUND\"";}
            else if(n)copy("ordered_entries",begin,size_t(n)*0x238);
        }row<<'}';
    };
    if(effective)emit(effective);
    // BIOM prefix through ordered RNAM storage; no dereference from deferred work.
    std::vector<unsigned char> h(0x318);
    bool ok=reader(biom,h.data(),h.size());
    row<<"],\"biom_header_status\":\""<<(ok?"COMPLETE":"INCOMPLETE")<<"\",\"biom_header_raw\":";
    if(ok)row<<'"'<<hex(h.data(),h.size())<<'"';else{row<<"null";complete=false;}
    row<<",\"ordered_rnam\":[";
    if(ok){
        auto n=retail::field<uint32_t>(h.data(),0x308);
        auto begin=retail::field<uint64_t>(h.data(),0x310);
        if(n>64){complete=false;row<<"{\"loss\":\"RNAM_COUNT_BOUND\"}";}
        else if(n){
            std::vector<unsigned char> refs(size_t(n)*8);
            if(!reader(begin,refs.data(),refs.size())){complete=false;row<<"{\"loss\":\"RNAM_READ\"}";}
            else for(unsigned i=0;i<n;++i){if(i)row<<',';emit(retail::field<uint64_t>(refs.data(),i*8));}
        }
    }row<<"]}";
};
auto& state=t.ancestry;
if(slot==3&&!observed_return){
    state.pending={};t.provider_rsp=c.Rsp;t.provider_token=++t.next_provider;t.stage=0;
    row<<",\"provider_token\":"<<t.provider_token<<",\"provider_entry_rsp\":"<<c.Rsp;
    copy("provider_entry_query_xy_i32",c.Rdx,8);
    row<<",\"required_reads_complete\":"<<(complete?"true":"false")<<",\"workshop_binding\":\"UNKNOWN_NO_WORKSHOP_OPERAND_AT_THESE_SITES\"";
}else{
unsigned observed_stage=t.stage;
if(slot==2){
    row<<",\"selection_stage\":"<<observed_stage;
    if(observed_stage==0){
        state.pending={};state.pending.rsp=c.Rsp;state.pending.biom_capture=samples;state.pending.provider_token=t.provider_token;
        state.pending.source=word("provider_source_pointer",c.Rsp+0x38);
        state.pending.biom=c.Rax;
        state.pending.query=word("provider_query_pointer",c.Rbp+0x2d8);
        copy("source_at_biom_selection",state.pending.source,0x70);
        auto bh=copy("selected_source_biom",c.Rax,0x30);
        if(!bh.empty())row<<",\"biom_file_provenance\":"<<retail::provenance(reader,c.Rax,base,retail::field<uint32_t>(bh.data(),0x28)).json();
        copy("initial_query_xy_i32",state.pending.query,8);
        row<<",\"provider_rsp\":"<<c.Rsp;
        state.pending.complete=complete&&t.provider_token&&c.Rsp+0x3c8==t.provider_rsp;t.stage=1;
    }else if(observed_stage==1){
        bool joined=state.pending.rsp==c.Rsp&&state.pending.query==c.R9;
        copy("initial_query_xy_i32",c.R9,8);
        copy("manager_frame_descriptor",c.R8,0x2c);
        row<<",\"query_producer_join\":"<<(joined?"true":"false");
        state.pending.complete=state.pending.complete&&complete&&joined;state.pending.query_seen=joined;state.pending.query_capture=samples;
        if(!joined)complete=false;
        t.stage=0;
    }else if(state.stack.empty()){
        complete=false;row<<",\"loss\":\"UNOBSERVED_GENERATION_ENTRY\"";t.stage=0;
    }else{
        auto& inv=state.stack.back();auto f=inv.entry-0x2d8;
        bool frame=(observed_stage<=4)?c.Rsp==f:c.Rsp+0x70==f;
        row<<",\"selection_frame_matches\":"<<(frame?"true":"false");
        if(!frame)complete=false;
        inv.stages|=1u<<observed_stage;
        if(observed_stage==2){
            row<<",\"component_lookup_success_al\":"<<(c.Rax&255);
            copy("component_payload",f+0xe0,0x68);t.stage=3;
        }else if(observed_stage==3){
            copy("construction_mask_position",c.Rdx,0x18);
            row<<",\"mask_sampler_pointer\":"<<c.Rcx;t.stage=4;
        }else if(observed_stage==4){
            row<<",\"construction_mask_raw_u8\":"<<(c.Rax&255);t.stage=5;
        }else if(observed_stage==5){
            auto it=copy("alternate_iterator",c.Rbx,0x38);
            auto ctx=copy("alternate_context",c.Rdi,0x28);
            if(!it.empty()&&!ctx.empty()){
                auto node=retail::field<uint64_t>(it.data(),0x18);
                auto index=retail::field<uint64_t>(it.data(),0x20);
                row<<",\"iterator_node\":"<<node<<",\"iterator_index\":"<<index;
                if(index>=0xfe0||!retail::range(node,0x4000)){complete=false;row<<",\"loss\":\"ITERATOR_INDEX_BOUND\"";}
                else{
                    auto offset=copy("candidate_node_offset_u16",node+index*4+0x12,2);
                    if(!offset.empty()){
                        auto candidate=node+retail::field<uint16_t>(offset.data(),0);
                        auto record=copy("candidate_record",candidate,0x78);
                        if(!record.empty()){
                            auto current=copy("candidate_current_biom",retail::field<uint64_t>(ctx.data(),0),0x30);
                            bool eligible=!current.empty()&&retail::field<uint32_t>(record.data(),0x60)!=retail::field<uint32_t>(current.data(),0x28)&&
                                retail::field<uint32_t>(record.data(),0x70)==retail::field<uint32_t>(ctx.data(),0x18);
                            row<<",\"candidate_eligible_static_predicate\":"<<(eligible?"true":"false");
                            if(eligible)t.stage=6;
                        }
                    }
                }
            }
        }else if(observed_stage==6){
            auto ctx=copy("resolved_context",c.Rdi,0x28);
            uint64_t effective=ctx.empty()?0:word("effective_rsgd_pointer",retail::field<uint64_t>(ctx.data(),8));
            descriptors("alternate_biom",c.Rax,effective);t.stage=5;
        }
        inv.selection_valid=inv.selection_valid&&complete;
    }
}
// At b520, E is entry RSP; the native prologue consumes 0x2d8.
#ifdef RETAIL_FIXTURE
if(std::wstring(argv[3])==L"byte-budget")bytes=1048560;
#endif
if(slot==0){
    // Prune only frames whose stack has demonstrably unwound. Missing terminal
    // remains loss, never a successful generation result.
    unsigned pruned=0;
    while(!state.stack.empty()&&c.Rsp>=state.stack.back().entry){state.stack.pop_back();++pruned;}
    row<<",\"unwitnessed_terminals\":"<<pruned;
    require(state.stack.size()<64,"invocation stack budget");
    operands::Invocation inv{};inv.token=++state.next;inv.entry=c.Rsp;
    inv.parent=state.stack.empty()?0:state.stack.back().token;
    inv.source=c.Rcx;inv.descriptor=c.R8;
    auto ret=word("entry_return",c.Rsp);
    inv.biom=word("entry_biom_pointer",c.Rsp+0x28);
    inv.output=word("entry_output_pointer",c.Rsp+0x30);
    copy("source",inv.source,0x70);copy("origin",c.Rdx,8);
    copy("source_descriptor",inv.descriptor,0x18);copy("biom",inv.biom,0x30);
    auto manager=word("manager_pointer",base+0x5fd9c30);
    auto mgr=copy("manager",manager,0x200);
    row<<",\"owner_key_u32\":"<<uint32_t(c.R9);
    row<<",\"owner_matches_manager\":"<<(mgr.empty()?"null":
        retail::field<uint32_t>(mgr.data(),0x80)==uint32_t(c.R9)?"true":"false");
    inv.provider_rsp=c.Rsp+8;
    t.generation_watch=true;
    inv.upstream=state.pending.provider_token==t.provider_token&&t.provider_token&&c.Rsp+0x3d0==t.provider_rsp&&state.pending.complete&&state.pending.query_seen&&state.pending.rsp==inv.provider_rsp&&
        state.pending.source==inv.source&&state.pending.biom==inv.biom;
    row<<",\"provider_token\":"<<t.provider_token<<",\"upstream_provider_token\":"<<state.pending.provider_token;
    row<<",\"upstream_biom_capture\":"<<state.pending.biom_capture
       <<",\"upstream_query_capture\":"<<state.pending.query_capture;
    state.pending={};t.stage=2;
    row<<",\"upstream_join\":"<<(inv.upstream?"true":"false");
    inv.entry_ok=complete&&ret==base+provider_return&&!mgr.empty()&&
        retail::field<uint32_t>(mgr.data(),0x80)==uint32_t(c.R9);
    state.stack.push_back(inv);
}else if(slot!=2&&state.stack.empty()){
    complete=false;row<<",\"loss\":\"UNOBSERVED_ENTRY\"";
}
if(!state.stack.empty()){
    auto& inv=state.stack.back();
    bool frame=slot==0||slot==2|| (slot==1&&c.Rsp+0x2d8==inv.entry)||
        (slot==3&&c.Rsp==inv.entry+8);
    row<<",\"invocation_token\":"<<inv.token<<",\"parent_token\":"<<inv.parent
       <<",\"upstream_bound\":"<<(inv.upstream?"true":"false")
       <<",\"entry_rsp\":"<<inv.entry<<",\"frame_matches\":"<<(frame?"true":"false")
       <<",\"entry_bound\":"<<(inv.entry_ok?"true":"false");
    if(!frame)complete=false;
    if(slot==1){
        row<<",\"selection_stage_bits\":"<<inv.stages
           <<",\"selection_reads_valid\":"<<(inv.selection_valid?"true":"false")
           <<",\"selection_chain_complete\":"<<((inv.stages&28)==28&&inv.selection_valid&&inv.upstream?"true":"false");
        t.stage=0;
        inv.resource=c.Rdx;inv.selection=c.R8;inv.call_ok=false;++inv.order;
        auto res=copy("ires",c.Rdx,0x118);
        copy("generation_context",c.Rcx,0x28);
        auto desc=copy("selected_dnam",c.R8,560);
        auto mask=copy("ordinary_mask_stack",c.Rsp+0x30,1);
        auto rsgd=word("component_selected_rsgd_pointer",c.Rsp+0x80);
        // Optional typed record evidence: null is a genuine unresolved selection,
        // not an invented zero FormID or the selected descriptor's owner.
        if(rsgd)copy("rsgd_record_prefix",rsgd,0x30);
        copy("family_root_formid",c.Rsp+0x58,4);
        copy("per_biome_data",c.Rsp+0xe0,0x68);
        descriptors("current_biom",inv.biom,rsgd);
        auto begin=word("resource_order_begin",c.Rsp+0x50);
        auto count=copy("resource_order_count",c.Rsp+0x40,8);
        if(!count.empty()){
            auto n=retail::field<uint32_t>(count.data(),0);
            if(n>64){complete=false;row<<",\"order_loss\":\"COUNT_BOUND\"";}
            else if(n){
                auto list=copy("ordered_resource_pointers",begin,size_t(n)*8);
                row<<",\"ordered_resources\":[";
                if(!list.empty())for(unsigned i=0;i<n;++i){
                    if(i)row<<',';row<<"{\"ordinal\":"<<i;
                    auto at=retail::field<uint64_t>(list.data(),i*8);
                    if(at){auto h=copy("ires",at,0x118);
                        if(!h.empty())row<<",\"file_provenance\":"<<retail::provenance(reader,at,base,retail::field<uint32_t>(h.data(),0x28)).json();
                    }else row<<",\"null_slot\":true";
                    row<<'}';
                }row<<']';
            }
        }
        // Current slot/index identifies actual order; no sorting in collector.
        row<<",\"order_slot\":"<<c.Rbx<<",\"order_begin\":"<<begin
           <<",\"observed_resource_call_ordinal\":"<<inv.order;
        auto rarity=res.empty()?255:res[0x110];
        if(!res.empty())row<<",\"file_provenance\":"<<retail::provenance(reader,c.Rdx,base,
            retail::field<uint32_t>(res.data(),0x28)).json();
        uint8_t m=uint8_t(c.Rdi);
        bool inactive=m==8||rarity>m;
        row<<",\"rarity_raw\":"<<unsigned(rarity)<<",\"mask_register_raw\":"<<unsigned(m)
           <<",\"mask_branch_basis\":\"DERIVED_STATIC_PREDICATE_NOT_BRANCH_TRACE\""
           <<",\"mask_branch\":\""<<(inactive?"INACTIVE":"ACTIVE")<<"\""
           <<",\"effective_weight_bits\":"<<xmm(c.Xmm3);
        uint64_t setting=rarity<=5?base+0x5e901b8+0x20*rarity:0;
        if(inactive&&setting)copy("inactive_setting",setting,4);
        row<<",\"settings_at_use\":[";
        for(unsigned j=0;j<6;++j){if(j)row<<',';row<<"{\"rarity\":"<<j;copy("payload",base+0x5e901b8+0x20*j,4);row<<'}';}
        row<<']';
        if(rarity<=6&&!desc.empty()){
            auto offset=40*(rarity+7)+28;
            row<<",\"cell_chance_bits\":"<<retail::field<uint32_t>(desc.data(),offset);
        }else complete=false;
        if(mask.empty()||mask[0]!=m||res.empty()||res[0x2e]!=0x9f)complete=false;
        inv.call_ok=complete&&frame&&inv.entry_ok;
    }
    if(slot==3){
        copy("source_at_return",inv.source,0x70);
        copy("output_map_prefix_at_return",inv.output,0x30);
        row<<",\"terminal\":\"PROVIDER_RETURN_NOT_SUCCESS_CERTIFICATE\"";
        if(!inv.entry_ok)complete=false;
        state.stack.pop_back();t.stage=0;t.generation_watch=!state.stack.empty();
    }
}
row<<",\"status\":\""<<(complete?"COMPLETE":"INVALID")<<"\"";
row<<",\"required_reads_complete\":"<<(complete?"true":"false")
   <<",\"workshop_binding\":\"UNKNOWN_NO_WORKSHOP_OPERAND_AT_THESE_SITES\""
   <<",\"historical_c1e_epoch\":null,\"consumer_join\":null"
   <<",\"predecessor_geometry\":null,\"seed_before_first_draw\":null"
   <<",\"population_complete\":false";

}
