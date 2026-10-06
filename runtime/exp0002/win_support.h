// SPDX-License-Identifier: GPL-3.0-or-later
#pragma once
#define NOMINMAX
#include <Windows.h>
#include <bcrypt.h>
#include <filesystem>
#include <fstream>
#include <iomanip>
#include <limits>
#include <sstream>
#include <string>
#include <vector>
#include "core.h"
#pragma comment(lib,"bcrypt.lib")

namespace sor {
namespace fs=std::filesystem;
inline std::string hex(std::uint64_t n,int width=16) {
    std::ostringstream s;s<<"0x"<<std::hex<<std::setfill('0')<<std::setw(width)<<n;return s.str();
}
inline std::string quote(const std::string& in) {
    std::ostringstream s;s<<'"';for(unsigned char c:in) {
        if(c=='"'||c=='\\') s<<'\\'<<c;
        else if(c<32) s<<"\\u"<<std::hex<<std::setw(4)<<std::setfill('0')<<unsigned(c);
        else s<<c;
    }s<<'"';return s.str();
}
inline std::string utc() {
    SYSTEMTIME t{};GetSystemTime(&t);char out[40]{};
    sprintf_s(out,"%04u-%02u-%02uT%02u:%02u:%02u.%03uZ",t.wYear,t.wMonth,t.wDay,t.wHour,t.wMinute,t.wSecond,t.wMilliseconds);return out;
}
inline std::string sha_bytes(const void* bytes,std::size_t n) {
    BCRYPT_ALG_HANDLE alg{};BCRYPT_HASH_HANDLE hash{};UCHAR digest[32]{};
    if(n>std::numeric_limits<ULONG>::max() || BCryptOpenAlgorithmProvider(&alg,BCRYPT_SHA256_ALGORITHM,nullptr,0)<0) return {};
    bool ok=BCryptCreateHash(alg,&hash,nullptr,0,nullptr,0,0)>=0;
    if(ok) ok=BCryptHashData(hash,static_cast<PUCHAR>(const_cast<void*>(bytes)),static_cast<ULONG>(n),0)>=0;
    if(ok) ok=BCryptFinishHash(hash,digest,32,0)>=0;
    if(hash) BCryptDestroyHash(hash);BCryptCloseAlgorithmProvider(alg,0);
    if(!ok) return {};std::ostringstream out;for(auto c:digest) out<<std::hex<<std::setw(2)<<std::setfill('0')<<unsigned(c);return out.str();
}
inline std::string sha_file(const fs::path& path) {
    std::ifstream stream(path,std::ios::binary);if(!stream)return {};
    BCRYPT_ALG_HANDLE alg{};BCRYPT_HASH_HANDLE hash{};UCHAR digest[32]{};char block[65536];
    if(BCryptOpenAlgorithmProvider(&alg,BCRYPT_SHA256_ALGORITHM,nullptr,0)<0)return {};
    bool ok=BCryptCreateHash(alg,&hash,nullptr,0,nullptr,0,0)>=0;
    while(ok && stream) {stream.read(block,sizeof block);auto n=stream.gcount();if(n)ok=BCryptHashData(hash,reinterpret_cast<PUCHAR>(block),static_cast<ULONG>(n),0)>=0;}
    if(!stream.eof())ok=false;
    if(ok)ok=BCryptFinishHash(hash,digest,32,0)>=0;
    if(hash)BCryptDestroyHash(hash);BCryptCloseAlgorithmProvider(alg,0);
    if(!ok)return {};std::ostringstream out;for(auto c:digest)out<<std::hex<<std::setw(2)<<std::setfill('0')<<unsigned(c);return out.str();
}
struct ProcessReader:Reader {
    HANDLE process=GetCurrentProcess();
    bool bytes(std::uint64_t address,void* into,std::size_t size) override {
        SIZE_T got{};return address && ReadProcessMemory(process,reinterpret_cast<void*>(address),into,size,&got) && got==size;
    }
};
inline bool allowed_root(const fs::path& path) {
    if(!path.is_absolute() || path.lexically_normal()!=path || path.filename()!=L"exp0002-live" || path.parent_path().filename()!=L".local-work") return false;
    auto repo=path.parent_path().parent_path();
    if(!fs::is_regular_file(repo/L"docs"/L"implementation-briefs"/L"CODEX_RESEARCH_BRIEF_SOR-EXP-0002_outpost_membership_reload_location.md"))return false;
    for(auto cur=path;!cur.empty();) {
        auto attrs=GetFileAttributesW(cur.c_str());
        if(attrs!=INVALID_FILE_ATTRIBUTES && (attrs&FILE_ATTRIBUTE_REPARSE_POINT))return false;
        auto parent=cur.parent_path();if(parent==cur)break;cur=parent;
    }
    return true;
}
inline bool write_new(const fs::path& path,const std::string& data,std::size_t limit=32768) {
    if(data.size()>limit)return false;
    HANDLE f=CreateFileW(path.c_str(),GENERIC_WRITE,FILE_SHARE_READ,nullptr,CREATE_NEW,FILE_ATTRIBUTE_NORMAL|FILE_FLAG_WRITE_THROUGH,nullptr);
    if(f==INVALID_HANDLE_VALUE)return false;DWORD wrote{};
    bool ok=WriteFile(f,data.data(),static_cast<DWORD>(data.size()),&wrote,nullptr)&&wrote==data.size();
    if(ok)ok=FlushFileBuffers(f)!=0;CloseHandle(f);return ok;
}
inline bool read_small(const fs::path& path,std::string& out,std::size_t cap=1024) {
    std::error_code error;auto n=fs::file_size(path,error);if(error||n>cap)return false;
    std::ifstream f(path,std::ios::binary);out.assign(static_cast<std::size_t>(n),'\0');f.read(out.data(),static_cast<std::streamsize>(n));return bool(f)||n==0;
}
}
