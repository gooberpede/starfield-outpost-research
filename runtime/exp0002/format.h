// SPDX-License-Identifier: GPL-3.0-or-later
#pragma once
#include "win_support.h"
namespace sor {
inline std::string form(Reader& r,std::uint64_t pointer) {
    if(!pointer)return "{\"status\":\"NULL_RESULT\",\"pointer\":null}";
    std::uint32_t id{},candidate{};std::uint8_t type{};
    if(!r.get(pointer+0x28,id)||!r.get(pointer+0x24,candidate)||!r.get(pointer+0x2e,type))return "{\"status\":\"READ_FAILED\",\"pointer\":"+quote(hex(pointer))+"}";
    return "{\"status\":\"OBSERVED\",\"pointer\":"+quote(hex(pointer))+",\"form_id\":"+quote(hex(id,8))+
        ",\"type\":"+std::to_string(type)+",\"native_handle_candidate\":"+quote(hex(candidate,8))+",\"resolved_handle\":null}";
}
inline std::string vector(const std::array<float,3>& v) {
    std::ostringstream s;s<<std::setprecision(9)<<'['<<v[0]<<','<<v[1]<<','<<v[2]<<']';return s.str();
}
inline std::string identity_json(Reader& r,const Identity& item) {
    return "{\"identity\":"+form(r,item.pointer)+",\"stored_base\":"+form(r,item.base)+",\"stored_parent_cell\":"+form(r,item.cell)+
        ",\"extra_data_pointer\":"+quote(hex(item.extra))+",\"coordinates\":{\"reference_xyz\":{\"value\":"+vector(item.position)+
        ",\"source\":\"native_position_operands\",\"units\":\"UNKNOWN\",\"frame\":\"REFERENCE_QUERY_FRAME_UNQUALIFIED\"},\"rotation_raw\":{\"value\":"+vector(item.rotation_raw)+
        ",\"source\":\"native_angle_input_operands\",\"units\":\"UNKNOWN\"},\"cell_local_xyz\":null,\"worldspace_xyz\":null,\"body_relative_xyz\":null,\"surface_map\":null,\"latitude_longitude\":null},\"loaded_3d\":null}";
}
}
