// SPDX-License-Identifier: GPL-3.0-or-later
#pragma once
#include <Windows.h>
#include <cstdint>

namespace d5ar {
// Caller holds the owner lifetime lease from before pointer selection until
// after release. These operations change synchronization state only.
inline volatile LONG* direct_reader_word(std::uint64_t proc) noexcept {
    if (proc < 0x10000 || proc > UINT64_MAX - 0x48 || (proc & 3)) return nullptr;
    auto word = reinterpret_cast<volatile LONG*>(proc + 0x44);
    MEMORY_BASIC_INFORMATION page{};
    if (!VirtualQuery(reinterpret_cast<const void*>(proc + 0x44), &page, sizeof page) ||
        page.State != MEM_COMMIT || page.Protect != PAGE_READWRITE || page.RegionSize < sizeof(LONG) ||
        proc + 0x44 - reinterpret_cast<std::uint64_t>(page.BaseAddress) > page.RegionSize - sizeof(LONG)) return nullptr;
    return word;
}

inline bool try_direct_reader(volatile LONG* word) noexcept {
    return InterlockedCompareExchange(word, 1, 0) == 0;
}

inline bool release_direct_reader(volatile LONG* word) noexcept {
    // Original area reader tail at preferred VA 0x1421e0a82. The counted
    // reader prevents any exclusive owner from entering until this decrement.
    const auto before = static_cast<std::uint32_t>(InterlockedExchangeAdd(word, -1));
    if ((before & 0xffc00fff) == 1 && (before & 0x003ff000))
        WakeByAddressSingle(const_cast<LONG*>(word));
    return !(before & 0xffc00000) && (before & 0xfff);
}
}
