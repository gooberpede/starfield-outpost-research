// SPDX-License-Identifier: GPL-3.0-or-later
// Partial D4 diagnostics only. Never a Workshop join or success certificate.
bool ok=true;
auto copy=[&](const char* name,uint64_t at,size_t n){
    std::vector<unsigned char> b(n);bool got=reader(at,b.data(),n);ok=ok&&got;
    row<<",\""<<name<<"\":{\"status\":\""<<(got?"COMPLETE":"INCOMPLETE")<<"\",\"address\":"<<at<<",\"raw\":";
    if(got)row<<'"'<<hex(b.data(),n)<<'"';else row<<"null";row<<'}';return b;
};
if(slot==1){
    row<<",\"abandoned_generation\":"<<(t.gen_entry?"true":"false");
    t.gen_entry=c.Rsp;t.gen_token=++t.gen_serial;
    copy("source",c.Rcx,0x70);copy("origin",c.Rdx,8);copy("source_descriptor",c.R8,0x18);
    copy("entry_biom_pointer",c.Rsp+0x28,8);copy("entry_output_pointer",c.Rsp+0x30,8);
    row<<",\"owner_key_u32\":"<<uint32_t(c.R9);
}else if(slot==2){
    copy("ires",c.Rdx,0x118);copy("selected_dnam",c.R8,560);
    copy("generation_context",c.Rcx,0x28);copy("ordinary_mask_stack",c.Rsp+0x30,1);
    copy("component_selected_rsgd_pointer",c.Rsp+0x80,8);copy("family_root_formid",c.Rsp+0x58,4);
    copy("per_biome_data",c.Rsp+0xe0,0x68);
    row<<",\"mask_register_raw\":"<<unsigned(uint8_t(c.Rdi))<<",\"effective_weight_bits\":"<<uint32_t(c.Xmm3.Low);
}
bool frame=t.gen_entry&&(slot==1||(slot==2&&c.Rsp+0x2d8==t.gen_entry)||(slot==3&&c.Rsp==t.gen_entry+8));
row<<",\"invocation_token\":"<<t.gen_token<<",\"frame_matches\":"<<(frame?"true":"false")
   <<",\"required_reads_complete\":"<<(ok?"true":"false")
   <<",\"diagnostic_scope\":\"PARTIAL_GENERATION_OPERANDS\",\"initial_construction_query\":null,\"component_selection_history\":null"
   <<",\"consumer_join\":null,\"generation_epoch\":null,\"useful_success\":false";
if(slot==3)t.gen_entry=0;
