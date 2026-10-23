// SPDX-License-Identifier: GPL-3.0-or-later
// Included in C1E's all-stop engine. No target writes or borrowed pointers.
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
// At b520: E=entry RSP; native prologue consumes 0x2d8. At a59e:
// S=cell RSP; c470 return=S+208; b520 frame=S+280.
auto& state=t.ancestry;
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
    inv.entry_ok=complete&&ret==base+provider_return&&!mgr.empty()&&
        retail::field<uint32_t>(mgr.data(),0x80)==uint32_t(c.R9);
    state.stack.push_back(inv);
}else if(state.stack.empty()){
    complete=false;row<<",\"loss\":\"UNOBSERVED_ENTRY\"";
}
if(!state.stack.empty()){
    auto& inv=state.stack.back();
    bool frame=slot==0|| (slot==1&&c.Rsp+0x2d8==inv.entry)||
        (slot==2&&c.Rsp+0x558==inv.entry)|| (slot==3&&c.Rsp==inv.entry+8);
    row<<",\"invocation_token\":"<<inv.token<<",\"parent_token\":"<<inv.parent
       <<",\"entry_rsp\":"<<inv.entry<<",\"frame_matches\":"<<(frame?"true":"false")
       <<",\"entry_bound\":"<<(inv.entry_ok?"true":"false");
    if(!frame)complete=false;
    if(slot==1){
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
        auto begin=word("resource_order_begin",c.Rsp+0x50);
        copy("resource_order_count",c.Rsp+0x40,8);
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
        if(rarity<=6&&!desc.empty()){
            auto offset=40*(rarity+7)+28;
            row<<",\"cell_chance_bits\":"<<retail::field<uint32_t>(desc.data(),offset);
        }else complete=false;
        if(mask.empty()||mask[0]!=m||res.empty()||res[0x2e]!=0x9f)complete=false;
        inv.call_ok=complete&&frame&&inv.entry_ok;
    }
    if(slot==2){
        auto ret=word("cell_return",c.Rsp+0x208);
        auto outer=word("resource_return",c.Rsp+0x278);
        auto xy=word("cell_pointer",c.Rsp+0x218);
        auto origin=word("cell_origin_pointer",c.Rsp+0x220);
        copy("cell_xy_i32",xy,8);copy("cell_origin_i32",origin,8);
        copy("packed_key_u64",c.Rsp+0xa0,8);
        copy("chance_block",c.R14,40);
        auto dnam=word("cell_dnam_pointer",c.Rsp+0x230);
        copy("seed_state_after_first_draw",base+0x5920b00,8);
        row<<",\"draw_times_100_bits\":"<<xmm(c.Xmm1)
           <<",\"threshold_bits\":"<<xmm(c.Xmm7)
           <<",\"eflags_after_vcomiss\":"<<c.EFlags
           <<",\"chance_edge\":\""<<((c.EFlags&1)?"ADMIT":"REJECT")<<"\""
           <<",\"observed_cell_ordinal\":"<<++inv.cells;
        bool joined=frame&&inv.call_ok&&c.Rsi==inv.resource&&dnam==inv.selection&&
            ret==base+cell_return&&outer==base+resource_return;
        row<<",\"resource_call_join\":"<<(joined?"true":"false");
        if(!joined)complete=false;
    }
    if(slot==3){
        copy("source_at_return",inv.source,0x70);
        copy("output_map_prefix_at_return",inv.output,0x30);
        row<<",\"terminal\":\"PROVIDER_RETURN_NOT_SUCCESS_CERTIFICATE\"";
        if(!inv.entry_ok)complete=false;
        state.stack.pop_back();
    }
}
row<<",\"required_reads_complete\":"<<(complete?"true":"false")
   <<",\"workshop_binding\":\"UNKNOWN_NO_WORKSHOP_OPERAND_AT_THESE_SITES\""
   <<",\"historical_c1e_epoch\":null,\"consumer_join\":null"
   <<",\"predecessor_geometry\":null,\"seed_before_first_draw\":null"
   <<",\"population_complete\":false";
