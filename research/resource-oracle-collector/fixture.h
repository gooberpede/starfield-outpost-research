// SPDX-License-Identifier: GPL-3.0-or-later
// Synthetic ABI only. No retail layout is asserted.
#pragma once
#include <windows.h>
#include <cstdint>
struct Resource { uint32_t id, type; };
struct Population { uint64_t begin, end, capacity; };
struct Evaluation {
    uint64_t magic, sequence, visit, depth;
    Population populations[3];
    uint64_t selector, produced, result, branch;
};
static_assert(sizeof(Evaluation) == 136, "synthetic ABI");
constexpr uint64_t MAGIC = 0x433143534f525359;
