// SPDX-License-Identifier: GPL-3.0-or-later
// Original D5AR schema/atomic writer. SHA routines adapt owned EXP0002
// win_support.h under SOR-P-0002; no outside JSON/hash implementation included.
// Reads owned capture buffers/metadata and caller-selected output directory.
// Normal file IO follows the original consumer's reader release. Exceptional
// completion writes only an owned failure tombstone; native release is UNKNOWN.
#define NOMINMAX
#include <Windows.h>
#include <bcrypt.h>
#include "writer.h"
#include <array>
#include <algorithm>
#include <fstream>
#include <map>
#include <set>
#include <limits>
#include <stdexcept>
#include <vector>
#include <cstdio>
#pragma comment(lib, "bcrypt.lib")

namespace d5ar {
namespace {
using Object = std::map<std::string, std::string>;
std::string bytes_hex(const void* data, std::size_t size) {
    static constexpr char digits[]="0123456789abcdef";
    const auto* bytes=static_cast<const unsigned char*>(data);
    if(size>std::numeric_limits<std::size_t>::max()/2) throw std::runtime_error("HEX_CAPACITY");
    std::string result(size*2, '0');
    for(std::size_t i=0;i<size;++i) {result[i*2]=digits[bytes[i]>>4];result[i*2+1]=digits[bytes[i]&15];}
    return result;
}
std::string quote(const std::string& value) {
    std::string result="\"";
    for(unsigned char c:value) {
        if(c>=128) throw std::runtime_error("NON_ASCII_METADATA");
        if(c=='"'||c=='\\') {result+='\\';result+=char(c);}
        else if(c<32) {result+="\\u00";result+=bytes_hex(&c,1);}
        else result+=char(c);
    }
    return result+'"';
}
std::string object(const Object& fields) {
    std::string result="{";
    for(const auto& [key,value]:fields) {if(result.size()>1)result+=',';result+=quote(key)+':'+value;}
    return result+'}';
}
std::string array(const std::vector<std::string>& values) {
    std::string result="[";
    for(const auto& value:values) {if(result.size()>1)result+=',';result+=value;}
    return result+']';
}
void require(bool test,const char* reason) {if(!test)throw std::runtime_error(reason);}
std::string hash(const std::string& data) {
    auto result=sha_bytes(data.data(),data.size());require(result.size()==64,"HASH_FAILED");return result;
}
bool hash_word(const std::string& text) {
    return text.size()==64&&text.find_first_not_of("0123456789abcdef")==std::string::npos;
}
bool uuid_word(const std::string& text) {
    if(text.size()!=36)return false;
    for(std::size_t i=0;i<text.size();++i) {
        if(i==8||i==13||i==18||i==23) {if(text[i]!='-')return false;}
        else if(std::string("0123456789abcdef").find(text[i])==std::string::npos)return false;
    }
    return true;
}
bool utc_word(const std::string& text) {
    if(text.size()!=27)return false;
    for(std::size_t i=0;i<text.size();++i) {
        char expected=0;
        if(i==4||i==7)expected='-';else if(i==10)expected='T';
        else if(i==13||i==16)expected=':';else if(i==19)expected='.';else if(i==26)expected='Z';
        if(expected?text[i]!=expected:text[i]<'0'||text[i]>'9')return false;
    }
    SYSTEMTIME time{};time.wYear=WORD(std::stoi(text.substr(0,4)));time.wMonth=WORD(std::stoi(text.substr(5,2)));
    time.wDay=WORD(std::stoi(text.substr(8,2)));time.wHour=WORD(std::stoi(text.substr(11,2)));
    time.wMinute=WORD(std::stoi(text.substr(14,2)));time.wSecond=WORD(std::stoi(text.substr(17,2)));
    FILETIME file{};SYSTEMTIME back{};
    return SystemTimeToFileTime(&time,&file)&&FileTimeToSystemTime(&file,&back)&&time.wYear==back.wYear&&
        time.wMonth==back.wMonth&&time.wDay==back.wDay&&time.wHour==back.wHour&&time.wMinute==back.wMinute&&time.wSecond==back.wSecond;
}
std::string token(const char* prefix,std::uint64_t value) {return quote(std::string(prefix)+std::to_string(value));}
struct Handle {
    HANDLE value{INVALID_HANDLE_VALUE};
    ~Handle(){if(value!=INVALID_HANDLE_VALUE)CloseHandle(value);}
};
bool plain_directory(const std::filesystem::path& path) {
    if(!path.is_absolute()||path.lexically_normal()!=path)return false;
    for(auto p=path;!p.empty();) {
        auto attributes=GetFileAttributesW(p.c_str());
        if(attributes==INVALID_FILE_ATTRIBUTES||(attributes&FILE_ATTRIBUTE_REPARSE_POINT))return false;
        auto parent=p.parent_path();if(parent==p)break;p=parent;
    }
    return std::filesystem::is_directory(path);
}
}

std::string sha_bytes(const void* data,std::size_t size) {
    BCRYPT_ALG_HANDLE algorithm{};BCRYPT_HASH_HANDLE state{};
    std::array<unsigned char,32> digest{};
    if(BCryptOpenAlgorithmProvider(&algorithm,BCRYPT_SHA256_ALGORITHM,nullptr,0)<0)return {};
    bool ok=BCryptCreateHash(algorithm,&state,nullptr,0,nullptr,0,0)>=0;
    const auto* at=static_cast<const unsigned char*>(data);
    while(ok&&size) {
        auto count=static_cast<ULONG>((std::min)(size,std::size_t(1024*1024)));
        ok=BCryptHashData(state,const_cast<PUCHAR>(at),count,0)>=0;at+=count;size-=count;
    }
    if(ok)ok=BCryptFinishHash(state,digest.data(),32,0)>=0;
    if(state)BCryptDestroyHash(state);BCryptCloseAlgorithmProvider(algorithm,0);
    return ok?bytes_hex(digest.data(),digest.size()):std::string{};
}
std::string sha_file(const std::filesystem::path& path) {
    std::ifstream input(path,std::ios::binary);if(!input)return {};
    BCRYPT_ALG_HANDLE algorithm{};BCRYPT_HASH_HANDLE state{};
    std::array<unsigned char,32> digest{};std::array<char,65536> buffer{};
    if(BCryptOpenAlgorithmProvider(&algorithm,BCRYPT_SHA256_ALGORITHM,nullptr,0)<0)return {};
    bool ok=BCryptCreateHash(algorithm,&state,nullptr,0,nullptr,0,0)>=0;
    while(ok&&input) {
        input.read(buffer.data(),buffer.size());auto count=input.gcount();
        if(count)ok=BCryptHashData(state,reinterpret_cast<PUCHAR>(buffer.data()),static_cast<ULONG>(count),0)>=0;
    }
    if(!input.eof())ok=false;
    if(ok)ok=BCryptFinishHash(state,digest.data(),32,0)>=0;
    if(state)BCryptDestroyHash(state);BCryptCloseAlgorithmProvider(algorithm,0);
    return ok?bytes_hex(digest.data(),digest.size()):std::string{};
}
bool disk_floors() {
    for(const wchar_t* drive:{L"C:/",L"D:/"}) {ULARGE_INTEGER available{};
        if(!GetDiskFreeSpaceExW(drive,&available,nullptr,nullptr)||available.QuadPart<40000000000ULL)return false;
    }
    return true;
}
std::string random_uuid() {
    std::array<unsigned char,16> bytes{};
    if(BCryptGenRandom(nullptr,bytes.data(),16,BCRYPT_USE_SYSTEM_PREFERRED_RNG)<0)throw std::runtime_error("UUID_FAILED");
    bytes[6]=(bytes[6]&15)|0x40;bytes[8]=(bytes[8]&63)|0x80;
    auto hex=bytes_hex(bytes.data(),16);
    return hex.substr(0,8)+'-'+hex.substr(8,4)+'-'+hex.substr(12,4)+'-'+hex.substr(16,4)+'-'+hex.substr(20,12);
}
std::string precise_utc() {
    FILETIME file{};SYSTEMTIME time{};GetSystemTimePreciseAsFileTime(&file);
    if(!FileTimeToSystemTime(&file,&time))throw std::runtime_error("UTC_FAILED");
    std::uint64_t ticks=(std::uint64_t(file.dwHighDateTime)<<32)|file.dwLowDateTime;
    char result[40]{};
    sprintf_s(result,"%04u-%02u-%02uT%02u:%02u:%02u.%06lluZ",time.wYear,time.wMonth,time.wDay,
              time.wHour,time.wMinute,time.wSecond,(ticks%10000000ULL)/10);
    return result;
}
std::string snapshot_json(const Capture& capture,const Metadata& meta) {
    require(uuid_word(meta.capture_id)&&uuid_word(meta.session_id),"UUID_INVALID");
    require(meta.pid&&meta.creation_filetime,"PROCESS_IDENTITY_INVALID");
    require(hash_word(meta.game_exe_sha256)&&hash_word(meta.sfse_sha256)&&hash_word(meta.plugin_sha256)&&hash_word(meta.source_lock_sha256),"BUILD_HASH_INVALID");
    require(meta.evidence_basis=="UNQUALIFIED_NATIVE"||meta.evidence_basis=="SYNTHETIC","EVIDENCE_BASIS_INVALID");
    require(utc_word(meta.utc),"UTC_INVALID");
    std::vector<std::string> sources;
    std::set<std::uint64_t> source_keys,map_indices;
    for(const auto& holder:capture.holders) {
        require(map_indices.insert(holder.map_index).second,"DUPLICATE_MAP_ENTRY");
        require(!holder.source||source_keys.insert(holder.source).second,"DUPLICATE_SOURCE_POINTER");
        std::string geometry="null",geometry_hash="null";
        auto disposition=holder.disposition;
        if(disposition=="ALLOCATION_UNKNOWN"&&holder.complete) {
            std::uint64_t region_total=0,point_total=0;
            std::vector<std::string> resources;
            std::set<std::uint32_t> forms;
            for(const auto& resource:holder.resources) {
                require(forms.insert(resource.form).second,"DUPLICATE_RESOURCE");
                char form[9]{};sprintf_s(form,"%08x",resource.form);
                std::vector<std::string> regions;
                for(const auto& region:resource.regions) {
                    std::uint32_t header_form{};std::memcpy(&header_form,region.header.data()+16,4);
                    require(header_form==resource.form,"REGION_FORM_INVALID");
                    require(region.points.size()==std::uint64_t(region.count)*16,"POINT_COUNT_INVALID");
                    regions.push_back(object({{"count",std::to_string(region.count)},
                        {"header",quote(bytes_hex(region.header.data(),24))},{"points",quote(bytes_hex(region.points.data(),region.points.size()))}}));
                    ++region_total;point_total+=region.count;
                }
                resources.push_back(object({{"regions",array(regions)},{"resource",quote(form)}}));
            }
            geometry=object({{"capture",object({{"complete","true"},{"point_total",std::to_string(point_total)},
                {"region_total",std::to_string(region_total)},{"resource_slots",std::to_string(holder.resources.size())},{"status",quote("OK")}})},
                {"frame","null"},{"generation_quality",quote("UNKNOWN")},{"loss","0"},{"population",array(resources)},
                {"schema",quote("sor-d5ai-geometry/1")},{"session_id",quote(meta.session_id)},
                {"snapshot_id",quote(meta.capture_id)},{"source","null"}});
            geometry_hash=quote(hash(geometry));
        }
        require(disposition=="ALLOCATION_UNKNOWN"||disposition=="EMPTY"||disposition=="COPY_FAILED"||disposition=="MALFORMED","SOURCE_DISPOSITION_INVALID");
        sources.push_back(object({{"allocation_id",holder.source?token("source-pointer-",holder.source):"null"},
            {"area_association",quote("UNKNOWN")},{"geometry",geometry},{"geometry_sha256",geometry_hash},
            {"holder_id",holder.holder?token("holder-pointer-",holder.holder):"null"},
            {"map_entry_id",token("map-entry-",holder.map_index)},{"owning_grid","null"},
            {"source_diagnostics",object({{"status",quote(holder.source_diagnostics.status)},
                {"descriptor_status",quote(holder.source_diagnostics.descriptor_status)},
                {"source_descriptor_bytes",holder.source_diagnostics.descriptor_complete?quote(bytes_hex(holder.source_diagnostics.descriptor_bytes.data(),44)):"null"},
                {"origin_status",quote(holder.source_diagnostics.origin_status)},
                {"origin_input_words",holder.source_diagnostics.origin_complete?quote(bytes_hex(holder.source_diagnostics.origin_words.data(),16)):"null"},
                {"semantic_bytes",holder.source_diagnostics.complete?quote(bytes_hex(holder.source_diagnostics.semantic.data(),29)):"null"},
                {"visited_token",holder.source_diagnostics.complete?std::to_string(holder.source_diagnostics.visited):"null"}})},
            {"source_disposition",quote(disposition)}}));
    }
    const auto& operation=capture.operation;
    const auto& selected=capture.selected_reference;
    auto selected_identity=object({{"status",quote(selected.status)},
        {"invocation",std::to_string(selected.invocation)},{"command",std::to_string(selected.command)},
        {"epoch",std::to_string(selected.epoch)},
        {"reference_pointer_token",selected.reference?token("runtime-pointer-",selected.reference):"null"},
        {"formid_word",selected.copied?quote(bytes_hex(&selected.formid,4)):"null"},
        {"type",std::to_string(selected.type)},{"observations",std::to_string(selected.observations)},
        {"active",selected.active?"true":"false"},{"copied",selected.copied?"true":"false"},
        {"ambiguous",selected.ambiguous?"true":"false"},{"linked",selected.linked?"true":"false"},
        {"identity_time",quote("NATIVE_RESOLVED_REFERENCE_LEASE_BEFORE_RELEASE")},
        {"post_release_allocation_continuity",quote("UNKNOWN")}});
    auto area=object({{"status",quote(operation.status)},
        {"qualification",quote("UNQUALIFIED_OPERATION_DIAGNOSTICS")},
        {"caller_return_token",token("runtime-pointer-",operation.caller_return)},
        {"reference_pointer_token",token("runtime-pointer-",operation.reference)},
        {"query_state_token",token("runtime-pointer-",operation.query_state)},
        {"domain_pointer_token",token("runtime-pointer-",operation.domain)},
        {"indexed_input_bytes",quote(bytes_hex(operation.indexed.data(),24))},
        {"radius_word",quote(bytes_hex(&operation.radius_word,4))},
        {"upper_word",quote(bytes_hex(&operation.upper_word,4))},
        {"translation_status",quote(operation.translation_status)},
        {"translation_index",std::to_string(operation.translation_index)},
        {"translation_count",std::to_string(operation.translation_count)},
        {"translation_pointer_token",token("runtime-pointer-",operation.translation_pointer)},
        {"translation_bytes","null"},{"translation_applied","null"},
        {"translation_application_status",quote("UNKNOWN_NOT_OBSERVED")},
        {"reference_formid","null"},{"reference_type","null"},
        {"base_pointer_token","null"},{"base_formid","null"},{"base_type","null"},
        {"cell_pointer_token","null"},{"cell_formid","null"},{"cell_type","null"},
        {"reference_identity_complete","false"},
        {"operation_complete",operation.complete?"true":"false"},
        {"selected_reference",selected_identity}});
    auto outpost=object({{"area_context",area},
        {"reference",operation.complete?token("observed-reference-pointer-",operation.reference):"null"},
        {"status",quote(operation.complete?"ACTIVE_ESTABLISHED_OPERATION_REFERENCE":"UNKNOWN")}});
    auto binding=[](const OwnedBinding& value){return object({{"status",quote(value.status)},
        {"complete",value.complete?"true":"false"},
        {"manager_pointer_token",value.complete?token("runtime-pointer-",value.manager):"null"},
        {"attached_proc_token",value.complete?token("proc-pointer-",value.attached_proc):"null"},
        {"owner_formid_word",value.complete?quote(bytes_hex(&value.owner_formid,4)):"null"},
        {"mode",value.complete?std::to_string(value.mode):"null"},
        {"current_descriptor_bytes",value.complete?quote(bytes_hex(value.descriptor.data(),44)):"null"}});};
    Object envelope{{"build",object({{"game_exe_sha256",quote(meta.game_exe_sha256)},{"game_version",quote("1.16.244.0")},
        {"plugin_sha256",quote(meta.plugin_sha256)},{"sfse_sha256",quote(meta.sfse_sha256)},{"source_lock_sha256",quote(meta.source_lock_sha256)}})},
        {"capture_id",quote(meta.capture_id)},{"evidence_basis",quote(meta.evidence_basis)},
        {"capture_diagnostics",object({{"copy_status",quote(capture.status)},
            {"copy_begin_filetime",std::to_string(capture.copy_begin_filetime)},
            {"copy_end_filetime",std::to_string(capture.copy_end_filetime)},
            {"epoch_begin",std::to_string(capture.epoch_begin)},{"epoch_end",std::to_string(capture.epoch_end)},
            {"lock_state",std::to_string(capture.lock_state)},{"required_bytes",std::to_string(capture.required_bytes)},
            {"proc_identity_token",capture.proc?token("proc-pointer-",capture.proc):"null"}})},
        {"method",quote("sor-d5ar-offline/0.1.0")},
        {"outpost",outpost},
        {"owner_context",object({{"before",binding(capture.binding_before)},{"after",binding(capture.binding_after)}})},
        {"process",object({{"creation_filetime",std::to_string(meta.creation_filetime)},{"pid",std::to_string(meta.pid)}})},
        {"schema",quote("sor-d5ar-resident-snapshot/1")},{"scope",quote("RESIDENT_MAP_CENSUS_AREA_ASSOCIATION_UNKNOWN")},
        {"session_id",quote(meta.session_id)},{"sources",array(sources)},
        {"status",quote(capture.status=="COPIED_UNQUALIFIED"?"COPIED_UNQUALIFIED":"REFUSED")},{"utc",quote(meta.utc)}};
    envelope["payload_sha256"]=quote(hash(object(envelope)));
    return object(envelope)+'\n';
}
Publication publish_snapshot(const Capture& capture,const Metadata& meta,const std::filesystem::path& root) {
    Publication result{false,"NOT_STARTED",{}};
    try {
        require(disk_floors(),"DISK_QUERY_OR_FLOOR_FAILED");
        require(plain_directory(root),"OUTPUT_DIRECTORY_INVALID");
        auto stamp=meta.utc;stamp.erase(std::remove(stamp.begin(),stamp.end(),'-'),stamp.end());
        stamp.erase(std::remove(stamp.begin(),stamp.end(),':'),stamp.end());
        auto stem=stamp+'_'+meta.session_id+'_'+meta.capture_id;
        auto partial=root/(stem+".partial"),final=root/(stem+".snapshot.json");
        require(!std::filesystem::exists(final),"FINAL_ALREADY_EXISTS");
        auto data=snapshot_json(capture,meta);
        Handle file;file.value=CreateFileW(partial.c_str(),GENERIC_WRITE,FILE_SHARE_READ,nullptr,CREATE_NEW,
                                         FILE_ATTRIBUTE_NORMAL|FILE_FLAG_WRITE_THROUGH,nullptr);
        require(file.value!=INVALID_HANDLE_VALUE,"PARTIAL_CREATE_FAILED");result.path=partial;
        std::size_t at=0;
        while(at<data.size()) {DWORD wrote{};auto count=static_cast<DWORD>((std::min)(data.size()-at,std::size_t(1024*1024)));
            require(WriteFile(file.value,data.data()+at,count,&wrote,nullptr)&&wrote==count,"WRITE_FAILED");at+=wrote;
        }
        require(FlushFileBuffers(file.value)!=0,"FLUSH_FAILED");
        require(CloseHandle(file.value)!=0,"CLOSE_FAILED");file.value=INVALID_HANDLE_VALUE;
        require(sha_file(partial)==hash(data),"VERIFY_FAILED");
        // Exact readback compares bytes as well as the integrity digest.
        std::ifstream check(partial,std::ios::binary);std::array<char,65536> buffer{};at=0;
        while(check) {check.read(buffer.data(),buffer.size());auto count=std::size_t(check.gcount());
            require(at+count<=data.size()&&data.compare(at,count,buffer.data(),count)==0,"READBACK_FAILED");at+=count;
        }
        require(check.eof()&&at==data.size(),"READBACK_LENGTH_FAILED");check.close();
        require(disk_floors(),"DISK_QUERY_OR_FLOOR_FAILED");
        require(MoveFileExW(partial.c_str(),final.c_str(),MOVEFILE_WRITE_THROUGH)!=0,"ATOMIC_PUBLICATION_FAILED");
        result={true,capture.status=="COPIED_UNQUALIFIED"?"COPIED_UNQUALIFIED":"REFUSED",final};
    } catch(const std::exception& error) {result.status=error.what();}
    return result;
}
}
