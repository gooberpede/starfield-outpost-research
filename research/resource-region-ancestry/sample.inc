// SPDX-License-Identifier: GPL-3.0-or-later
// Included inside the inherited C1D stopped-event handler. No target writes.
bool required_reads=true;
auto u64=[&](uint64_t at){uint64_t v=0;if(!read(at,&v,8)){required_reads=false;return uint64_t(0);}return v;};
if(slot==0){
    auto bp=c.Rsp-0x38;
    auto before=t.ancestry.stack.size();
    auto i=t.ancestry.begin(bp);
    auto abandoned=before-t.ancestry.stack.size();
    i.reference=c.R14;i.closure=bp-0x48;
    i.frame=u64(c.Rsp)==base+updater_return && c.Rcx==base+0x5f5d800 && c.Rdx==base+0x5f5d618 && required_reads;
    t.ancestry.stack.push_back(i);
    row<<",\"updater_token\":"<<i.token<<",\"parent_token\":"<<i.parent
       <<",\"updater_bp\":"<<i.bp<<",\"abandoned_invocations\":"<<abandoned
       <<",\"frame_verified\":"<<(i.frame?"true":"false");
}
if(slot==1 || slot==2){
    auto i=t.ancestry.find(c.Rsi+0x48);
    auto updater_bp=u64(c.Rbp+0x1c0),caller=u64(c.Rbp+0x1c8),source=u64(c.Rbp-0x58);
    uint64_t procgen=u64(c.Rbp+0x190),source_ordinal=u64(c.Rbp+0x1b0);
    uint64_t slots=u64(procgen+0x20),capacity=u64(procgen+0x28);
    uint64_t source_slot=slots+source_ordinal*24+8,key=0,selected_source=0;uint32_t occupied=0xffffffffU;
    bool source_ok=capacity<=4096 && source_ordinal<capacity && retail::range(slots,capacity*24)
        && read(source_slot,&selected_source,8) && read(source_slot-8,&key,8)
        && read(source_slot+8,&occupied,4) && occupied!=0xffffffffU && selected_source==source;
    bool frame=i && i->bp==updater_bp && caller==base+callback_return && i->closure==c.Rsi && i->frame && source_ok
        && u64(updater_bp+0x18)==i->reference && required_reads;
    if(i){i->slot=source_slot;i->source=source;i->key=key;i->temporary=u64(c.Rsi+8);}
    auto binding=retail::identity(reader,i?i->reference:0,base);
    size_t point_budget=65536;
#ifdef RETAIL_FIXTURE
    if(std::wstring(argv[3])==L"byte-budget")point_budget=16;
#endif
    auto shape=ancestry::geometry(reader,c.Rbx,point_budget);
    unsigned char closure[24]{},descriptor[24]{},qb[12]{};
    bool closure_ok=read(c.Rsi,closure,24);
    bool descriptor_ok=closure_ok && read(retail::field<uint64_t>(closure,0),descriptor,24);
    bool qb_ok=read(c.Rbp+0x70,qb,12);
    unsigned char resource_raw[0x30]{};
    bool resource_ok=read(c.R13,resource_raw,sizeof resource_raw);
    auto resource_id=retail::field<uint32_t>(resource_raw,0x28);
    auto selected=ancestry::decision(reader,source,c.R12,c.R13,c.Rbx);
    row<<",\"decision\":\""<<(slot==1?"ACCEPT":"REJECT")<<"\",\"callback_token\":null"
       <<",\"updater_token\":"<<(i?i->updater_token:0)<<",\"parent_token\":"<<(i?i->parent:0)<<",\"updater_bp\":"<<updater_bp
       <<",\"callback_bp\":"<<c.Rbp<<",\"callback_caller\":"<<caller
       <<",\"ancestry\":\""<<(frame&&binding.bound?"BOUND_CALLBACK":"UNKNOWN")
       <<"\",\"source_key\":"<<key<<",\"source_slot\":"<<source_slot<<",\"source_ordinal\":"<<source_ordinal
       <<",\"procgen\":"<<procgen<<",\"temporary_set\":"<<(i?i->temporary:0)
       <<",\"binding_reference\":"<<(i?i->reference:0)<<",\"binding\":\""<<binding.reason
       <<"\",\"raw_binding_reference\":\""<<hex(binding.ref,sizeof binding.ref)
       <<"\",\"raw_binding_base\":\""<<hex(binding.base,sizeof binding.base)
       <<"\",\"raw_binding_extra\":\""<<hex(binding.extra,sizeof binding.extra)
       <<"\",\"resource_pointer\":"<<c.R13<<",\"selected\":"<<selected
       <<",\"geometry\":"<<shape.json()<<",\"closure_read\":"<<(closure_ok?"true":"false")
       <<",\"raw_closure\":\""<<hex(closure,24)<<"\",\"descriptor_read\":"<<(descriptor_ok?"true":"false")
       <<",\"raw_descriptor\":\""<<hex(descriptor,24)<<"\",\"qb_retained_read\":"<<(qb_ok?"true":"false")
       <<",\"qb_retained_bits\":\""<<hex(qb,12)<<"\",\"per_use_qc_qv_qe\":null"
       <<",\"file_provenance\":"<<retail::provenance(reader,c.R13,base,
            resource_ok?resource_id:0xffffffffU).json();
}
if(slot==3){
    auto i=t.ancestry.find(c.Rbp);
    auto payload=retail::population(reader,c.Rdx,true);
    auto ref=u64(c.Rbp+0x18);auto binding=retail::identity(reader,ref,base);
    bool frame=i && i->frame && i->reference==ref && u64(c.Rbp+0x38)==base+updater_return
         && c.R14==base+0x5f5d800 && c.R13==base+0x5f5d618 && i->temporary==c.Rsp+0x60 && required_reads;
    row<<",\"updater_bp\":"<<c.Rbp<<",\"callback_token\":"<<0<<",\"updater_token\":"<<(i?i->updater_token:0)
       <<",\"temporary_set\":"<<(i?i->temporary:0)<<",\"binding\":\""<<binding.reason
       <<"\",\"ancestry\":\""<<(frame&&binding.bound?"BOUND_TRANSFER":"UNKNOWN")
       <<"\",\"refresh_payload\":"<<payload.json();
    t.ancestry.finish(c.Rbp);
}
row<<",\"population_epoch\":null,\"generation_inputs\":null,\"census_complete\":false";
row<<",\"required_reads_complete\":"<<(required_reads?"true":"false")
   <<",\"loss\":"<<(required_reads?"null":"\"stack-source-read\"");
