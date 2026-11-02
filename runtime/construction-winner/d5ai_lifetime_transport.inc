// SPDX-License-Identifier: GPL-3.0-or-later
// Worker-only I/O. Producer callbacks never allocate, flush or touch files.
namespace winner::lifetime {
inline HANDLE raw=INVALID_HANDLE_VALUE,ledger=INVALID_HANDLE_VALUE;
inline U written{},flushed{},acknowledged{},bytes{},qualified_through{};
inline uint32_t prefix_crc{};inline Mark coverage{};
inline std::string marker_json(const Mark& m){
 return "{\"cursor\":"+std::to_string(m.cursor)+",\"ticks\":"+std::to_string(m.ticks)+",\"generation_before\":"+std::to_string(m.generation_before)+",\"generation_after\":"+std::to_string(m.generation_after)+",\"active_before\":"+std::to_string(m.active_before)+",\"active_after\":"+std::to_string(m.active_after)+",\"loss\":"+std::to_string(m.loss)+",\"failed\":"+std::to_string(m.failed)+"}";
}
bool begin(){
 if(!configured)return true;
 if(enabled.load()||!guards()||identity_hash.size()!=64)return false;
 for(U i=0;i<capacity;++i)queue[i].ticket=i;
 for(unsigned i=0;i<32;++i){unsigned value=0;for(unsigned j=0;j<2;++j){char c=identity_hash[i*2+j];unsigned nibble=c>='0'&&c<='9'?c-'0':c>='a'&&c<='f'?c-'a'+10:255;if(nibble>15)return false;value=value*16+nibble;}file_header.identity_sha256[i]=(unsigned char)value;}
 file_header.armed_thread=GetCurrentThreadId();file_header.epoch_at_arm=winner::epoch.load();file_header.armed_ticks=tick();
 raw=CreateFileW((session/L"lifetimes.bin").c_str(),GENERIC_WRITE,FILE_SHARE_READ,nullptr,CREATE_NEW,FILE_ATTRIBUTE_NORMAL,nullptr);
 ledger=CreateFileW((session/L"lifetimes-flush.jsonl").c_str(),GENERIC_WRITE,FILE_SHARE_READ,nullptr,CREATE_NEW,FILE_ATTRIBUTE_NORMAL,nullptr);
 if(raw==INVALID_HANDLE_VALUE||ledger==INVALID_HANDLE_VALUE)return false;
 if(!winner::append(raw,&file_header,sizeof file_header)||!winner::flush(raw,false))return false;
 bytes=sizeof file_header;prefix_crc=winner::crc(&file_header,sizeof file_header);return true;
}
bool drain(){
 if(!configured)return true;if(fixture_hold.load())return true;
 U limit=enqueue.load();Event e{};bool changed=false;
 if(!disk((limit-dequeue.load())*112+65536))return false;
 while(dequeue.load()<limit&&pop(e)){
  unsigned char row[112]{};uint32_t frame[]{0x314a4c53,96,uint32_t(e.sequence),winner::crc(&e,sizeof e)};
  memcpy(row,frame,16);memcpy(row+16,&e,96);
  if(!winner::append(raw,row,sizeof row)){failed=true;return false;}prefix_crc=winner::crc(row,sizeof row,prefix_crc);bytes+=sizeof row;++written;changed=true;
 }
 if(changed&&!winner::flush(raw,false)){failed=true;return false;}flushed=written;
 auto sampled=mark();U cutoff=unlogged_cutoff.load();bool advances=(!cutoff||sampled.ticks<cutoff)&&coherent(sampled)&&sampled.cursor<=flushed&&sampled.ticks>qualified_through;
 if(advances){coverage=sampled;qualified_through=sampled.ticks;}
 // A fresh coherent empty-queue marker also advances an authenticated prefix.
 // An active or reserved-but-unpublished producer can never advance coverage.
 if(changed||advances){
  auto line="{\"schema\":\"sor-d5ai-lifetime-ack/1\",\"identity_sha256\":"+sor::quote(identity_hash)+",\"records\":"+std::to_string(flushed)+",\"bytes\":"+std::to_string(bytes)+",\"prefix_crc32\":"+std::to_string(prefix_crc)+",\"qualified_from_ticks\":"+std::to_string(file_header.armed_ticks)+",\"qualified_through_ticks\":"+std::to_string(qualified_through)+",\"coverage_mark\":"+marker_json(coverage)+",\"drops\":"+std::to_string(drops.load())+",\"failed\":"+(failed.load()?"true":"false")+"}\n";
  if(!winner::append(ledger,line.data(),DWORD(line.size()))||!winner::flush(ledger,true)){failed=true;return false;}acknowledged=flushed;
 }
 return !failed.load();
}
std::string metrics(){return ",\"lifetime_counter_overflow\":"+std::string(counter_overflow.load()?"true":"false")+",\"lifetime_unlogged_cutoff_ticks\":"+std::to_string(unlogged_cutoff.load())+",\"lifetime_enqueued\":"+std::to_string(enqueue.load())+",\"lifetime_written\":"+std::to_string(written)+",\"lifetime_flushed\":"+std::to_string(flushed)+",\"lifetime_acknowledged\":"+std::to_string(acknowledged)+",\"lifetime_bytes\":"+std::to_string(bytes)+",\"lifetime_prefix_crc32\":"+std::to_string(prefix_crc)+",\"lifetime_drops\":"+std::to_string(drops.load())+",\"lifetime_active\":"+std::to_string(active.load())+",\"lifetime_generation\":"+std::to_string(generation.load())+",\"lifetime_failed\":"+(failed.load()?"true":"false")+",\"lifetime_qualified_from_ticks\":"+std::to_string(file_header.armed_ticks)+",\"lifetime_qualified_through_ticks\":"+std::to_string(qualified_through);}
void close(){if(raw!=INVALID_HANDLE_VALUE)CloseHandle(raw);if(ledger!=INVALID_HANDLE_VALUE)CloseHandle(ledger);}
}
