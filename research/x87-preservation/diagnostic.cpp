// SPDX-License-Identifier: GPL-3.0-or-later
#include <windows.h>
#include <intrin.h>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <mutex>
#include "diagnostic.h"
unsigned diagnostic_condition{}, diagnostic_requested{};
static FILE* output{};
static std::mutex output_mutex;
static unsigned sequence{};
void diagnostic_open(int argc, char** argv) {
    if(argc!=2) std::abort();
    diagnostic_requested=std::strcmp(argv[1],"minimal")==0 ? 1 :
                         std::strcmp(argv[1],"adversarial")==0 ? 2 : 0;
    if(!diagnostic_requested || fopen_s(&output,"states.bin","wb") || !output) std::abort();
    int cpu[4]{}; __cpuid(cpu,0);
    char vendor[13]{};
    std::memcpy(vendor,cpu+1,4); std::memcpy(vendor+4,cpu+3,4); std::memcpy(vendor+8,cpu+2,4);
    __cpuid(cpu,1);
    std::printf("CPU vendor=%s signature=%08x XCR0=%llx GetVersion_packed=%08lx\n",vendor,cpu[0],_xgetbv(0),GetVersion());
}
void diagnostic_write(const unsigned char* state, unsigned mode, unsigned child) {
    std::lock_guard<std::mutex> guard(output_mutex);
    // Version 1 has 5184 snapshot bytes; version 2 also owns the restore image.
    constexpr unsigned version=DIAGNOSTIC_CORRECTED ? 2 : 1;
    constexpr unsigned bytes=DIAGNOSTIC_CORRECTED ? 5696 : 5184;
    unsigned header[]{0x37385853,version,++sequence,diagnostic_condition,mode,
                      (child<<24)|(GetCurrentThreadId()&0xffffff)};
    unsigned trailer=0x454e4421;
    if(std::fwrite(header,sizeof(header),1,output)!=1 ||
       std::fwrite(state,bytes,1,output)!=1 || std::fwrite(&trailer,4,1,output)!=1 ||
       std::fflush(output)) std::abort();
}
void diagnostic_close() {
    if(std::fclose(output)) std::abort();
    std::printf("diagnostic_records=%u\n",sequence);
}
