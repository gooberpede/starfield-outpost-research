# SPDX-License-Identifier: GPL-3.0-or-later
"""Resumable observation at the original ContentManager receiver return.

SOR-P-0002 lineage: D5S export38 and the older D5BJ private pump boundary.
The observer changes scheduling inside an owned disposable host. It calls
the original receiver, retains its return value and lets the original pump
continue after the hold. A failed callback stops that host through the
PoolRuntime callback guard. The caller owns the exact execution decision.
"""
import ctypes as C
import struct
import threading

import d5bj_sampler as host

PUMP_CALL = 0x1428d8a49
RECEIVER_ENTRY = 0x1428d8060
CODE = (0x1428d8000,)
SHIM_PAGE = 0x16d5b0000


def relative_call(site, destination):
    displacement = destination - (site + 5)
    host.require(-(1 << 31) <= displacement < 1 << 31, 'Pump observer is outside relative call range')
    return b'\xe8' + struct.pack('<i', displacement)


def observer_code(callback):
    # This is a CALL target with incoming RSP congruent to 8 modulo 16.
    # Reserve 0x20 bytes of Win64 shadow space and two 8-byte locals.
    # Save the original receiver argument and its full RAX result.
    return (
        b'\x48\x83\xec\x38'                         # sub rsp, 0x38
        b'\x48\x89\x4c\x24\x20'                     # mov [rsp+0x20], rcx
        b'\x48\xb8' + struct.pack('<Q', RECEIVER_ENTRY)  # mov rax, original receiver
        + b'\xff\xd0'                                 # call rax
        b'\x48\x89\x44\x24\x28'                     # mov [rsp+0x28], rax
        b'\x48\x8b\x4c\x24\x20'                     # mov rcx, [rsp+0x20]
        b'\x0f\xb6\xd0'                             # movzx edx, al
        b'\x48\xb8' + struct.pack('<Q', callback)        # mov rax, observer
        + b'\xff\xd0'                                 # call rax
        b'\x48\x8b\x44\x24\x28'                     # mov rax, [rsp+0x28]
        b'\x48\x83\xc4\x38'                         # add rsp, 0x38
        b'\xc3'                                      # ret to original 0x1428d8a4e
    )


class PumpGate:
    """One explicitly armed hold on a caller-owned ContentManager JobSite.

    Install on writable private image pages before any worker is admitted.
    Arm after the pool has started and before rectangle service. After the
    run, release any hold before stopping the pool, then close before freeing
    the private image pages.
    """

    def __init__(self, runtime, site):
        host.require(isinstance(site, int) and site > 0 and not site & 7,
                     'Invalid owned ContentManager JobSite address')
        self.runtime = runtime
        self.kernel = runtime.kernel
        self.site = site
        self.receiver = site + 0x40
        self.controller = self.kernel.GetCurrentThreadId()
        self.allow_return = threading.Event()
        self.state = 'idle'
        self.installed = False
        self.events = {}
        self.original = relative_call(PUMP_CALL, RECEIVER_ENTRY)
        self.instrumented = relative_call(PUMP_CALL, SHIM_PAGE)

    def install(self):
        host.require(not self.installed and not self.runtime.started,
                     'Install pump observation before native worker startup')
        host.require(C.string_at(PUMP_CALL, 5) == self.original, 'Original receiver CALL operand differs')
        self.observer = self.runtime.callback(None, (C.c_void_p, C.c_uint32), self._observe)
        target = C.cast(self.observer, C.c_void_p).value
        code = observer_code(target)
        address = self.kernel.VirtualAlloc(SHIM_PAGE, host.PAGE, 0x3000, 4)
        host.require(address == SHIM_PAGE, 'Private pump observer page unavailable')
        try:
            C.memmove(address, code, len(code))
            host.protect(self.kernel, address, 0x20)
            C.memmove(PUMP_CALL, self.instrumented, len(self.instrumented))
        except BaseException:
            host.require(self.kernel.VirtualFree(address, 0, 0x8000), 'Cannot release failed observer setup')
            raise
        self.installed = True

    def arm(self):
        with self.runtime.condition:
            self._require_controller()
            host.require(self.installed and self.runtime.started and self.state == 'idle',
                         'Pump gate can be armed once on a started pool')
            self.state = 'armed'

    def _require_controller(self):
        host.require(self.kernel.GetCurrentThreadId() == self.controller,
                     'Only the owning controller may change the pump hold')

    def _snapshot(self, result, states):
        mask = tuple((C.c_uint16 * 6).from_address(self.site + 0x28a))
        state = C.c_uint16.from_address(self.site + 0x296).value
        lock = tuple((C.c_uint32 * 2).from_address(self.receiver))
        member = self.runtime.membership()
        host.require(mask == (1, 2, 4, 8, 16, 32) and state in states
                     and lock == (0, 0) and result == 1,
                     'ContentManager return lacks the selected unlocked/running state')
        host.require(member and member['pool'] == self.runtime.pool
                     and C.c_uint32.from_address(self.site + 0x284).value == member['thread_id'],
                     'ContentManager receiver returned outside its native pump worker')
        return {'site': self.site, 'receiver': self.receiver, 'return': result, 'state': state,
                'receiver_lock_words': lock, **member}

    def _observe(self, receiver, result):
        if receiver != self.receiver:
            return
        with self.runtime.condition:
            if self.state != 'armed':
                return
            self.events['held'] = self._snapshot(result, (9,))
            self.state = 'held'
            self.runtime.condition.notify_all()
        self.allow_return.wait()
        with self.runtime.condition:
            host.require(self.state in ('released', 'cancelled'), 'Pump woke without controller disposition')
            positive = self.state == 'released'
            resumed = self._snapshot(result, (25,) if positive else (9, 25))
            held = self.events['held']
            host.require(all(resumed[key] == held[key] for key in held if key != 'state'),
                         'Pump resumption changed its receiver or native worker identity')
            self.events['resumed' if positive else 'cancelled_return'] = resumed
            self.state = 'returned'
            self.runtime.condition.notify_all()

    def wait_until_held(self):
        host.require(self.installed and self.runtime.started, 'Pump gate is not available')
        self.runtime.wait_for_progress(lambda: 'held' in self.events, self.runtime.idle,
                                       'selected ContentManager receiver hold')
        return self.events['held'].copy()

    @property
    def held(self):
        with self.runtime.condition:
            return self.state == 'held'

    def frontier(self):
        with self.runtime.condition:
            self._require_controller()
            host.require(self.state == 'held', 'ContentManager is outside the held frontier')
            state = C.c_uint16.from_address(self.site + 0x296).value
            lock = tuple((C.c_uint32 * 2).from_address(self.receiver))
            worker = C.c_uint32.from_address(self.site + 0x284).value
            host.require(state == 25 and lock == (0, 0) and worker == self.events['held']['thread_id'],
                         'Held frontier lost pending state, receiver unlock or worker identity')
            return {'state': state, 'receiver_lock_words': lock, 'thread_id': worker}

    def release(self):
        with self.runtime.condition:
            self.events['release'] = self.frontier()
            self.state = 'released'
            self.allow_return.set()
            self.runtime.condition.notify_all()

    def cancel(self, reason):
        with self.runtime.condition:
            self._require_controller()
            if self.state in ('armed', 'held'):
                self.events['cancel'] = {'from': self.state, 'reason': reason}
                self.state = 'cancelled'
                self.allow_return.set()
                self.runtime.condition.notify_all()

    def wait_until_resumed(self):
        host.require('release' in self.events, 'Release the pump before waiting for positive progression')
        self.runtime.wait_for_progress(lambda: 'resumed' in self.events, self.runtime.idle,
                                       'selected ContentManager receiver resumption')
        return self.events['resumed'].copy()

    def close(self):
        host.require(self.installed and self.runtime.closed and self.state in ('idle', 'cancelled', 'returned')
                     and set(self.runtime.threads) == self.runtime.joined,
                     'Stop the owned pool before removing the pump observation')
        host.require(C.string_at(PUMP_CALL, 5) == self.instrumented, 'Private pump CALL changed unexpectedly')
        page = PUMP_CALL & ~(host.PAGE - 1)
        host.protect(self.kernel, page, 4)
        C.memmove(PUMP_CALL, self.original, len(self.original))
        host.protect(self.kernel, page, 0x20)
        host.flush(self.kernel)
        host.require(self.kernel.VirtualFree(SHIM_PAGE, 0, 0x8000), 'Cannot release private pump observer page')
        self.installed = False
