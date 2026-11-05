// SPDX-License-Identifier: GPL-3.0-or-later
#pragma once
#include "capture.h"
#include <filesystem>
#include <string>
#include <cstdint>

namespace d5ar {
// Identity strings are independently checked by the plugin/fixture caller.
// This writer never certifies native lifetime, outpost membership or a frame.
struct Metadata {
    std::string session_id, capture_id, utc;
    std::uint32_t pid{};
    std::uint64_t creation_filetime{};
    std::string game_exe_sha256, sfse_sha256, plugin_sha256, source_lock_sha256;
    std::string evidence_basis{"UNQUALIFIED_NATIVE"};
};
struct Publication {
    bool success{};
    std::string status;
    std::filesystem::path path;
};
std::string random_uuid();
std::string precise_utc();
std::string sha_bytes(const void*, std::size_t);
std::string sha_file(const std::filesystem::path&);
bool disk_floors();
std::string snapshot_json(const Capture&, const Metadata&);
using PublicationCheck = const char*(*)(bool before_rename);
Publication publish_snapshot(const Capture&, const Metadata&, const std::filesystem::path&, PublicationCheck = nullptr);
}
