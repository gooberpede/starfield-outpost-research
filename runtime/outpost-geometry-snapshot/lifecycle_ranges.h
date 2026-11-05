// SPDX-License-Identifier: GPL-3.0-or-later
#pragma once
// Authored RVA facts from pinned original .pdata and recursively decoded FH4
// cleanup ownership: .local-work/d5ar/phase-unwind01.json. Missing-metadata
// actions are NOT treated as leaves; complete startup unwind refuses them.
#include <cstdint>
namespace d5ar {
struct LifecycleRange {uint64_t begin,end;};
inline constexpr LifecycleRange lifecycle_ranges[]={
{0x2b48b0,0x2b48dd},
{0x2b62d0,0x2b6314},
{0x2bc990,0x2bc9b2},
{0x2cc0f0,0x2cc12b},
{0x35e080,0x35e0c5},
{0x787830,0x788b59},
{0x788bc0,0x788e6f},
{0x788e70,0x789592},
{0x789ce0,0x78a119},
{0x79d910,0x79da7e},
{0x7b2240,0x7b2291},
{0x1881660,0x1882b3d},
{0x27d3f50,0x27d3f7a},
{0x28cb2c0,0x28cb2cf},
};
}
