// SPDX-License-Identifier: GPL-3.0-or-later
// Original append-only durable evidence transport. No target reads or writes.
#pragma once
#include "profile.h"
#include "../../runtime/beacon-observer/capture.h"
namespace beacon {
struct EpochWriter {
    fs::path dir;HANDLE log=INVALID_HANDLE_VALUE;uint64_t serial{},bytes{};
    std::string previous=std::string(32,'\0');std::function<bool()> guard;
    EpochWriter(fs::path d,std::function<bool()> g):dir(std::move(d)),guard(std::move(g)){
        if(!guard())throw std::runtime_error("disk_guard");
        if(!fs::create_directory(dir))throw std::runtime_error("snapshot_collision");
        log=CreateFileW((dir/L"epochs.wal").c_str(),GENERIC_WRITE,FILE_SHARE_READ,nullptr,CREATE_NEW,FILE_ATTRIBUTE_NORMAL,nullptr);
        if(log==INVALID_HANDLE_VALUE)throw std::runtime_error("wal_open");
    }
    EpochWriter(const EpochWriter&)=delete;
    ~EpochWriter(){if(log!=INVALID_HANDLE_VALUE)CloseHandle(log);}
    static void u64(std::string& s,uint64_t n){for(int i=0;i<8;++i)s.push_back(char(n>>(i*8)));}
    static std::string unhex(const std::string& h){std::string b;for(size_t i=0;i<h.size();i+=2)b.push_back(char(std::stoul(h.substr(i,2),nullptr,16)));return b;}
    void event(const std::string& payload){
        latency::Phase timing(latency::writer);
        if(!guard())throw std::runtime_error("disk_guard");
        std::string identity;u64(identity,serial+1);identity+=previous;identity+=payload;
        auto hash=sha_bytes(identity.data(),identity.size());if(hash.size()!=64)throw std::runtime_error("wal_hash");
        std::string record="SOREP013";u64(record,payload.size());u64(record,serial+1);record+=previous;record+=unhex(hash);record+=payload;
        const char* p=record.data();size_t remaining=record.size();
        while(remaining){if(!guard())throw std::runtime_error("disk_guard");DWORD n=DWORD(std::min<size_t>(remaining,65536)),got{};
            if(!WriteFile(log,p,n,&got,nullptr)||got!=n)throw std::runtime_error("wal_write_integrity");remaining-=n;p+=n;
        }
        if(!FlushFileBuffers(log))throw std::runtime_error("wal_flush");
        // A completed event/raw call means durable bytes AND metadata, just as
        // in 0.1.2. No memory queue, background lag or boundary-wide durability gap.
        ++serial;bytes+=record.size();previous=unhex(hash);
    }
    void status(const std::string& root,const char* state,const std::string& why){event("{\"kind\":\"status\",\"root\":"+quote(root)+",\"state\":"+quote(state)+",\"reason\":"+quote(why)+",\"utc\":"+quote(utc())+"}");}
    void raw(const std::string& root,uint64_t address,const void* data,size_t n,const std::string& origin){
        latency::Phase timing(latency::writer);
        const auto* b=static_cast<const unsigned char*>(data);const char digits[]="0123456789abcdef";std::string encoded;encoded.reserve(n*2);
        for(size_t i=0;i<n;++i){encoded.push_back(digits[b[i]>>4]);encoded.push_back(digits[b[i]&15]);}
        auto hash=sha_bytes(data,n);if(hash.size()!=64)throw std::runtime_error("raw_hash");
        event("{\"kind\":\"raw\",\"root\":"+quote(root)+",\"address_domain\":\"runtime_VA\",\"address\":"+quote(hex(address))+",\"bytes\":"+std::to_string(n)+",\"sha256\":"+quote(hash)+",\"origin\":"+quote(origin)+",\"utc\":"+quote(utc())+",\"data_hex\":"+quote(encoded)+"}");
    }
    void finish(const std::string& terminal){event("{\"kind\":\"terminal\",\"terminal\":"+quote(terminal)+",\"bytes_written_before_marker\":"+std::to_string(bytes)+"}");}
};
}
