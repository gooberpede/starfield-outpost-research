// SPDX-License-Identifier: GPL-3.0-or-later
#pragma once
#include <cstdint>
namespace d5ar {
// This export is accepted only in the exact hash-pinned owned fixture host.
// No retail process or SFSE-loaded process can enter the offline test path.
struct OfflineInput {uint64_t image_base{},proc{},holder{};const wchar_t* output_directory{};unsigned mode{};uint64_t operation_reference{},area_query{},operation_state{};};
using OfflineQualify=unsigned(*)(const OfflineInput*);
}
