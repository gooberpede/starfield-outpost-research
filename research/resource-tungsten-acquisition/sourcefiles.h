// SPDX-License-Identifier: GPL-3.0-or-later
#pragma once
#include "decode.h"
// Independently reconstructed from pinned retail native exports 003/007/010.
// This is NOT a full plugin census or an assumed Skyrim/CommonLib layout.
namespace retail {
struct SourceFile {uint64_t pointer{};unsigned char prefix[0x370]{};std::string name;};
struct Provenance {
    uint16_t index=0xffff;uint32_t table_count{};uint64_t table{},entry{},begin{};int32_t count{};
    bool complete=false,main_identity=false;std::string reason;std::vector<SourceFile> files;
    std::string json()const{
        std::ostringstream s;s<<"{\"status\":\""<<(complete?"COMPLETE":"INCOMPLETE")<<"\",\"reason\":\""<<reason
          <<"\",\"source_vector_index\":"<<index<<",\"table_count\":"<<table_count<<",\"table\":"<<table
          <<",\"entry\":"<<entry<<",\"begin\":"<<begin<<",\"count\":"<<count
          <<",\"main_file_identity\":"<<(main_identity?"true":"false")<<",\"files\":[";
        for(size_t i=0;i<files.size();++i){if(i)s<<',';auto& f=files[i];s<<"{\"pointer\":"<<f.pointer<<",\"name\":\""<<f.name
            <<"\",\"flags\":"<<field<uint32_t>(f.prefix,0x1b8)<<",\"full_index\":"<<unsigned(f.prefix[0x218])
            <<",\"raw_prefix\":\""<<hex(f.prefix,sizeof f.prefix)<<"\"}";}
        s<<"]}";return s.str();
    }
};
template<class Reader>Provenance provenance(Reader& read,uint64_t resource,uint64_t module,uint32_t formid){
    Provenance p;auto fail=[&](const char* why){p.reason=why;p.files.clear();p.complete=false;p.main_identity=false;return p;};
    if(!range(resource,0x32)||!read(resource+0x30,&p.index,2))return fail("source-index-read");
    if(p.index==0xffff)return fail("source-index-unavailable");
    if(!read(module+0x5e881e8,&p.table_count,4)||!read(module+0x5e881f0,&p.table,8))return fail("source-table-read");
    if(p.table_count>65536||p.index>=p.table_count||!range(p.table,8ULL*(p.index+1)))return fail("source-table-range");
    if(!read(p.table+8ULL*p.index,&p.entry,8)||!range(p.entry,16))return fail("source-entry-pointer");
    unsigned char entry[16]{};if(!read(p.entry,entry,16))return fail("source-entry-read");
    p.begin=field<uint64_t>(entry,0);p.count=field<int32_t>(entry,8);
    if(p.count<=0||p.count>128||!range(p.begin,8ULL*p.count))return fail("source-list-range-budget");
    std::vector<uint64_t> files(static_cast<size_t>(p.count));
    if(!read(p.begin,files.data(),files.size()*8))return fail("source-list-read");
    for(auto pointer:files){SourceFile f;f.pointer=pointer;
        if(!range(pointer,sizeof f.prefix)||!read(pointer,f.prefix,sizeof f.prefix))return fail("file-read");
        auto vt=field<uint64_t>(f.prefix,0);
        if(vt!=module+0x4b29a70 && vt!=module+0x4b29b80)return fail("file-vtable");
        // Static VAs 0x1405b99f6 through 0x1405b9a05 copy the filename
        // to object offset 0x38 with a 0x104-byte bound.
        bool ended=false;for(size_t i=0;i<0x104;++i){auto ch=f.prefix[0x38+i];if(!ch){ended=true;break;}
            if(!((ch>='a'&&ch<='z')||(ch>='A'&&ch<='Z')||(ch>='0'&&ch<='9')||ch=='.'||ch=='_'||ch=='-'||ch==' '))return fail("file-name-domain");
            f.name.push_back(char(ch));}
        if(!ended||f.name.empty())return fail("file-name-extent");
        auto flags=field<uint32_t>(f.prefix,0x1b8);
        // Narrow main-file mapping only. FD/FE/redirect paths remain unqualified.
        if(p.count==1 && f.name=="Starfield.esm" && !(flags&0x700) && f.prefix[0x218]==0 && (formid>>24)==0)p.main_identity=true;
        p.files.push_back(f);
    }
    unsigned char again[16]{};uint32_t count2{};uint64_t table2{},entry2{};uint16_t index2{};
    std::vector<uint64_t> files2(files.size());
    if(!read(p.entry,again,16)||memcmp(again,entry,16)||!read(resource+0x30,&index2,2)||index2!=p.index||
       !read(module+0x5e881e8,&count2,4)||count2!=p.table_count||!read(module+0x5e881f0,&table2,8)||table2!=p.table||
       !read(p.table+8ULL*p.index,&entry2,8)||entry2!=p.entry||!read(p.begin,files2.data(),files2.size()*8)||files2!=files)return fail("source-alias-change");
    p.complete=true;return p;
}
}
