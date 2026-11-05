// SPDX-License-Identifier: GPL-3.0-or-later
// Owned native writer fixture; never loads a plugin or touches a game process.
#include "writer.h"
#include "capture_fixture.h"
#include "startup_fixture.h"
#include "binding_fixture.h"
#include <cstring>
#include <iostream>

int wmain(int argc,wchar_t** argv) {
    using namespace d5ar;
    if(argc!=3)return 2;
    std::filesystem::path output=argv[1];std::wstring mode=argv[2];
    try {
        if(mode==L"capture-core")return d5ar::fixture::execute();
        if(mode==L"startup-core") {std::cout<<"PASS startup controls "<<d5ar::fixture::startup_controls()<<'\n';return 0;}
        if(mode==L"binding-core") {std::cout<<"PASS binding controls "<<d5ar::fixture::binding_controls()<<'\n';return 0;}
        Metadata meta;meta.session_id=random_uuid();meta.capture_id=random_uuid();meta.utc=precise_utc();
        meta.pid=777;meta.creation_filetime=12345;meta.evidence_basis="SYNTHETIC";
        meta.game_exe_sha256=std::string(64,'0');meta.sfse_sha256=std::string(64,'1');
        meta.plugin_sha256=std::string(64,'2');meta.source_lock_sha256=std::string(64,'3');
        Capture capture;capture.status="COPIED_UNQUALIFIED";capture.epoch_begin=capture.epoch_end=3;
        capture.lock_state=1;capture.required_bytes=500;capture.proc=0x10000;
        Holder holder;holder.source=0x20000;holder.holder=0x30000;holder.map_index=4;holder.complete=true;
        Resource resource;resource.form=7;Region region;region.count=2;
        float header[4]{1,2,3,4},points[8]{1,2,3,4,5,6,7,8};
        std::memcpy(region.header.data(),header,16);std::memcpy(region.header.data()+16,&resource.form,4);
        region.header[20]=1;region.header[21]=0xab;region.header[22]=0xcd;region.header[23]=0xef;
        region.points.resize(sizeof points);std::memcpy(region.points.data(),points,sizeof points);
        resource.regions.push_back(region);holder.resources.push_back(resource);capture.holders.push_back(holder);
        Holder unknown;unknown.source=0x40000;unknown.map_index=8;capture.holders.push_back(unknown);
        if(mode==L"bad-hash")meta.plugin_sha256="bad";
        if(mode==L"bad-date")meta.utc="2026-99-99T00:00:00.000000Z";
        if(mode==L"bad-path-date")meta.utc="../../../.T../..:...000000Z";
        if(mode==L"bad-point")capture.holders[0].resources[0].regions[0].count=3;
        if(mode==L"duplicate")capture.holders.push_back(capture.holders[0]);
        if(mode==L"refused")capture.status="LIFETIME_OVERLAP";
        if(mode==L"missing-dir")output/=L"absent";
        auto result=publish_snapshot(capture,meta,output);
        if(mode==L"normal") {
            if(!result.success)return 3;
            auto repeated=publish_snapshot(capture,meta,output);
            if(repeated.success||repeated.status!="FINAL_ALREADY_EXISTS")return 4;
            std::cout<<"PASS normal no-replace\n";return 0;
        }
        if(mode==L"refused") {
            if(!result.success||result.status!="REFUSED")return 5;
            std::cout<<"PASS refused retained\n";return 0;
        }
        if(result.success)return 6;
        std::cout<<"PASS refusal "<<result.status<<"\n";
        return 0;
    }catch(const std::exception& error){std::cerr<<error.what()<<'\n';return 7;}
}
