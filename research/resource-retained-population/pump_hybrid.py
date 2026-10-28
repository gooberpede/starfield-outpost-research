# SPDX-License-Identifier: GPL-3.0-or-later
"""Exercise the inherited durable pump on disposable D5N targets only.

Reads an exact build; writes fresh ignored pump evidence. Inherits the four
normal/STOP/collector-loss/pipe-loss cases and target disposal effects described
in qualify_pump.py. No retail admission, installation, saves, network or Git writes.
"""
import hybrid
import qualify_pump
import operate_hybrid

qualify_pump.reduce = hybrid.reducer().reduce
qualify_pump.pump = operate_hybrid.module('collect_native')['pump']

if __name__ == '__main__':
    qualify_pump.main()
