# SPDX-License-Identifier: GPL-3.0-or-later
"""Preparation-only SFPT FNAM/GNAM installation, pinned FUN_14096bae0.

Pure operation on 256 serialized FormID/flag pairs. The modern FNAM path
transposes pairs into the runtime X-major array without changing flag bits.
EFRM partial updates and legacy packed formats require different input handling.
"""


def install_fnam(entries):
    if len(entries) != 256:
        raise ValueError('SFPT_ENTRY_COUNT')
    return [entries[y*16+x] for x in range(16) for y in range(16)]
