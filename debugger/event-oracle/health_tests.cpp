// SPDX-License-Identifier: GPL-3.0-or-later
// Disposable local writer/guard controls, no process attachment.
#include "epoch_writer.h"
#include <iostream>
using namespace beacon;
int wmain(int argc,wchar_t**argv){
    if(argc!=2)return 2;fs::path root=argv[1];fs::create_directories(root);int checks=0;
    auto check=[&](bool value){if(!value)throw std::runtime_error("health_assertion");++checks;};
    check(space_safe(40000000000,40000000000));check(!space_safe(39999999999,40000000000));check(!space_safe(40000000000,39999999999));check(!space_safe(UINT64_MAX,UINT64_MAX,false));
    bool allowed=true;Writer w(root/L"guarded",[&]{return allowed;});w.event("{\"kind\":\"durable_before_guard\"}");allowed=false;
    bool caught=false;try{w.event("must_not_be_written");}catch(const std::exception&){caught=true;}check(caught);
    std::ifstream f(w.dir/L"records.jsonl");std::string line,second;std::getline(f,line);std::getline(f,second);check(line=="{\"kind\":\"durable_before_guard\"}"&&second.empty());
    {Writer broken(root/L"broken",[]{return true;});CloseHandle(broken.log);broken.log=INVALID_HANDLE_VALUE;caught=false;try{broken.event("failure");}catch(const std::exception&){caught=true;}check(caught);}
    {Writer raw(root/L"raw-open",[]{return true;});fs::create_directory(raw.dir/L"raw-1.bin");caught=false;try{int b=42;raw.raw("blocked",0,&b,4,"fixture");}catch(const std::exception&){caught=true;}check(caught);}
    allowed=false;caught=false;try{EpochWriter blocked(root/L"wal-denied",[&]{return allowed;});}catch(const std::exception&){caught=true;}check(caught&&!fs::exists(root/L"wal-denied"));
    allowed=true;EpochWriter wal(root/L"wal-guarded",[&]{return allowed;});wal.event("{\"kind\":\"durable_before_guard\"}");
    unsigned char retained[]={1,2,3};wal.raw("retained",0,retained,sizeof retained,"disposable_register_bytes");
    auto previous_size=fs::file_size(wal.dir/L"epochs.wal");auto previous_hash=sha_file(wal.dir/L"epochs.wal");allowed=false;
    caught=false;try{wal.event("must_not_be_written");}catch(const std::exception&){caught=true;}check(caught);check(fs::file_size(wal.dir/L"epochs.wal")==previous_size&&sha_file(wal.dir/L"epochs.wal")==previous_hash);
    {EpochWriter broken(root/L"wal-broken",[]{return true;});CloseHandle(broken.log);broken.log=INVALID_HANDLE_VALUE;caught=false;try{broken.event("{\"kind\":\"failure\"}");}catch(const std::exception&){caught=true;}check(caught);}
    std::cout<<"checks="<<checks<<" PASS\n";return 0;
}
