# SPDX-License-Identifier: GPL-3.0-or-later
"""Disposable original Jobs2Adaptor startup, worker and shutdown component.

SOR-P-0002 lineage: D5H-N230/N231/N257–N273, D5S exports 20, 30, 41
and 43, D5BJ worker and page-host methods. Uses the pinned reader EXE and
Windows x64 host. No game process or DLL is loaded. The caller owns the
disposable process, all data bindings and the controlled execution decision.
"""
import argparse
import ctypes as C
import json
import os
from pathlib import Path
import struct
import sys
import threading

sys.path.insert(0, str(Path(__file__).resolve().parent))
import d5bj_sampler as host
import d5bj_workers as prior

CODE = (
    0x1402b7000, 0x1402b5000, 0x140306000, 0x14030b000, 0x140315000,
    0x140318000, 0x140323000, 0x1405b4000, 0x140a04000,
    0x1422c7000, 0x1422c8000, 0x1422ce000, 0x1422cf000,
    0x1428d1000, 0x1428d2000, 0x1428d3000, 0x1428d4000, 0x1428d7000,
    0x14365c000,
)
DATA = (
    0x143a3f000, 0x143a40000, 0x144ca1000, 0x144d59000, 0x144da7000,
    0x144f04000, 0x1458d5000, 0x145e60000, 0x145e76000, 0x145e91000,
    0x145e9b000, 0x1461f9000, 0x1461fa000, 0x1482df000, 0x1484ff000,
    0x148500000,
)
RW_DATA = (0x145e60000, 0x1461fa000, 0x1484ff000, 0x148500000)

PRIMARY, SECONDARY = 2, 4
ADAPTOR = 0x1484ffdc0
ADAPTOR_SLOT = 0x1461fabe8
WORKER_SLOT = 0x145e9b174
MEMORY_SLOT = 0x1482dfa10
ARENA = 0x145e603c0
ARENA_STATE = 0x145e60398
BLOCK_BYTES = 0x10000
PTR, U32, U64 = C.c_void_p, C.c_uint32, C.c_uint64
require = host.require


def read_ptr(at):
    return PTR.from_address(at).value


def put_ptr(at, value):
    PTR.from_address(at).value = value


def pointer(function):
    return C.cast(function, PTR).value


def ncall(address, result, *types):
    return C.WINFUNCTYPE(result, *types)(address)


def available_bytes(kernel, drive):
    available = U64()
    kernel.GetDiskFreeSpaceExW.argtypes = (C.c_wchar_p, C.POINTER(U64), PTR, PTR)
    require(kernel.GetDiskFreeSpaceExW(drive, C.byref(available), None, None),
            f'Cannot query caller-available space for {drive}')
    return available.value


class PoolRuntime:
    """Bindings for already allocated private pages.

    Call bind while pages are writable and initialize only after final page
    protection. Keep this object alive until stop has joined owned workers.
    A caller using the integrated path must quiesce all published work and
    release its own holds before entering stop.
    """

    def __init__(self, kernel):
        self.kernel = kernel
        self.callbacks = []
        self.heap = {}
        self.blocks = set()
        self.context_storage = {}
        self.threads = {}
        self.semaphores = set()
        self.critical_sections = set()
        self.entered = {}
        self.departed = set()
        self.waiting = set()
        self.joined = set()
        self.condition = threading.Condition()
        self.adaptor = None
        self.started = False
        self.closed = False
        self.memory_owner = C.create_string_buffer(0x488)
        self.crt_tls = C.create_string_buffer(0x2c70)
        self.crt_tls[0xbc] = b'\x01'

        kernel.TlsAlloc.restype = U32
        kernel.TlsFree.argtypes = (U32,)
        kernel.TlsSetValue.argtypes = (U32, PTR)
        kernel.TlsGetValue.argtypes = (U32,)
        kernel.TlsGetValue.restype = PTR
        kernel.GetCurrentThread.restype = PTR
        kernel.GetCurrentThreadId.restype = U32
        kernel.CreateThread.argtypes = (PTR, C.c_size_t, PTR, PTR, U32, C.POINTER(U32))
        kernel.CreateThread.restype = PTR
        kernel.CreateSemaphoreExW.argtypes = (PTR, C.c_long, C.c_long, PTR, U32, U32)
        kernel.CreateSemaphoreExW.restype = PTR
        kernel.ResumeThread.argtypes = (PTR,)
        kernel.ResumeThread.restype = U32
        kernel.WaitForSingleObject.argtypes = (PTR, U32)
        kernel.WaitForSingleObject.restype = U32
        kernel.CloseHandle.argtypes = (PTR,)
        kernel.ReleaseSemaphore.argtypes = (PTR, C.c_long, PTR)
        kernel.InitializeCriticalSectionAndSpinCount.argtypes = (PTR, U32)
        kernel.DeleteCriticalSection.argtypes = (PTR,)
        kernel.EnterCriticalSection.argtypes = (PTR,)
        kernel.LeaveCriticalSection.argtypes = (PTR,)

    @staticmethod
    def refuse(error):
        # ctypes ignores exceptions raised by callbacks. Fail the owned child
        # rather than returning a placeholder pointer to native code.
        print(f'D5BM pool callback STOP: {error}', file=sys.stderr, flush=True)
        os._exit(70)

    def callback(self, result, types, operation):
        def checked(*args):
            try:
                return operation(*args)
            except Exception as error:
                self.refuse(error)

        fn = C.WINFUNCTYPE(result, *types)(checked)
        self.callbacks.append(fn)
        return fn

    def hook(self, address, result, types, operation):
        fn = self.callback(result, types, operation)
        # An absolute jump in a private copy keeps the Win64 arguments and
        # return address intact.
        C.memmove(address, b'\x48\xb8' + struct.pack('<Q', pointer(fn)) + b'\xff\xe0', 12)

    def import_hook(self, address, result, types, operation):
        put_ptr(address, pointer(self.callback(result, types, operation)))

    def arena_allocate(self, owner, length, alignment, aligned):
        require(owner == ARENA and 0 < length <= 0x800000
                and alignment in (0, 8, 0x40) and aligned in (0, 1),
                'Unqualified Jobs2 arena request')
        storage = C.create_string_buffer(length + 0x3f)
        address = (C.addressof(storage) + 0x3f) & ~0x3f
        self.heap[address] = storage
        return address

    def arena_free(self, address):
        if address:
            require(address in self.heap, 'Jobs2 attempted to free foreign storage')
            del self.heap[address]

    def array_construct(self, address, stride, count, constructor, destructor):
        require((stride, constructor, destructor) == (0x70, 0x1428d33f0, 0x1428d34d0)
                and count in (PRIMARY, SECONDARY) and address - 8 in self.heap,
                'Unexpected native GroupThread construction')
        create = ncall(constructor, PTR, PTR)
        for index in range(count):
            item = address + stride * index
            require(create(item) == item, 'Original GroupThread constructor failed')

    def array_destroy(self, address, stride, count, destructor):
        require((stride, destructor) == (0x70, 0x1428d34d0)
                and count in (PRIMARY, SECONDARY) and address - 8 in self.heap,
                'Unexpected native GroupThread destruction')
        destroy = ncall(destructor, None, PTR)
        for index in reversed(range(count)):
            destroy(address + stride * index)

    def format_thread(self, out, capacity, fmt, name, index):
        require(capacity == 0x103 and fmt == b'%s %u'
                and name in (b'BSJobs', b'BSJobs-Background', b'BSJobs-Secondary')
                and index < SECONDARY, 'Unexpected native worker name operands')
        value = name + b' ' + str(index).encode('ascii')
        C.memmove(out, value + b'\0', len(value) + 1)
        return len(value)

    def create_semaphore(self, attributes, initial, maximum, name, flags, access):
        require((attributes, initial, maximum, name, flags, access)
                == (None, 0, 0x10000, None, 0, 0x1f0002), 'Unexpected pool semaphore operands')
        handle = self.kernel.CreateSemaphoreExW(attributes, initial, maximum, name, flags, access)
        require(handle and handle not in self.semaphores, 'Could not create private pool semaphore')
        self.semaphores.add(handle)
        return handle

    def worker_records(self, pool):
        count = U32.from_address(pool + 0xe0).value
        require(count in (PRIMARY, SECONDARY), 'Unexpected worker population')
        start = read_ptr(pool + 0xc0)
        require(start and start - 8 in self.heap, 'Missing native GroupThread record array')
        return range(start, start + count * 0x70, 0x70)

    def create_thread(self, attributes, stack, entry, record, flags, identifier):
        valid = [pool for pool in (ADAPTOR + 0x40, ADAPTOR + 0x140)
                 if record in self.worker_records(pool)]
        require((attributes, stack, entry, flags, identifier)
                == (None, 0x80000, 0x1422cf120, 4, record + 0x40) and len(valid) == 1,
                'Unexpected owned CreateThread operands')
        require(read_ptr(record) == 0x144da7d58 and record + 0x50 == read_ptr(record + 0x68)
                and read_ptr(record + 0x50) == 0x144da7d08
                and read_ptr(record + 0x58) == valid[0], 'Native worker capture differs')
        index = U32.from_address(record + 0x60).value
        require(self.worker_records(valid[0])[index] == record, 'Native capture index differs')
        handle = self.kernel.CreateThread(None, stack, entry, record, flags,
                                          C.cast(identifier, C.POINTER(U32)))
        require(handle and handle not in self.threads, 'Native CreateThread failed')
        thread_id = U32.from_address(identifier).value
        require(thread_id and thread_id not in {row[2] for row in self.threads.values()},
                'Missing or duplicate owned thread ID')
        self.threads[handle] = (valid[0], index, thread_id)
        return handle

    def resume_thread(self, handle):
        require(handle in self.threads and self.kernel.ResumeThread(handle) == 1,
                'Could not start owned suspended worker')
        return 1

    def wait(self, handle, duration):
        require(handle in self.threads or handle in self.semaphores, 'Foreign wait handle')
        require(duration == 0xffffffff, 'Unexpected native wait bound')
        if handle in self.threads:
            status = self.kernel.WaitForSingleObject(handle, duration)
            require(status == 0, 'Native worker join failed')
            self.joined.add(handle)
            return status
        member = self.membership()
        require(member and read_ptr(member['pool'] + 0xb8) == handle,
                'Worker waited on a different pool semaphore')
        ident = member['thread_id']
        with self.condition:
            self.waiting.add(ident)
            self.condition.notify_all()
        try:
            status = self.kernel.WaitForSingleObject(handle, duration)
            require(status == 0, 'Native pool semaphore wait failed')
        finally:
            with self.condition:
                self.waiting.remove(ident)
                self.condition.notify_all()
        return status

    def close_handle(self, handle):
        require(handle in self.semaphores or handle in self.joined, 'Foreign or unjoined close handle')
        require(self.kernel.CloseHandle(handle), 'Native CloseHandle failed')
        self.semaphores.discard(handle)
        return 1

    def release_semaphore(self, handle, count, previous):
        require(handle in self.semaphores and 0 < count <= SECONDARY,
                'Native wake referenced a foreign semaphore or invalid count')
        require(self.kernel.ReleaseSemaphore(handle, count, previous), 'Native semaphore release failed')
        return 1

    def initialize_critical_section(self, address, spin):
        require(spin == 1000 and address not in self.critical_sections,
                'Unexpected worker critical-section initialization')
        require(self.kernel.InitializeCriticalSectionAndSpinCount(address, spin),
                'Native worker critical-section initialization failed')
        self.critical_sections.add(address)
        return 1

    def delete_critical_section(self, address):
        require(address in self.critical_sections, 'Foreign worker critical section')
        self.kernel.DeleteCriticalSection(address)
        self.critical_sections.remove(address)

    def allocate_block(self, _owner):
        address = self.kernel.VirtualAlloc(None, BLOCK_BYTES, 0x3000, 4)
        require(address and address % BLOCK_BYTES == 0 and address not in self.blocks,
                'Cannot allocate aligned private callback block')
        self.blocks.add(address)
        return address

    def release_block(self, _owner, block):
        require(block in self.blocks, 'Native callback release used a foreign block')
        require(self.kernel.VirtualFree(block, 0, 0x8000), 'Cannot free private callback block')
        self.blocks.remove(block)

    def memory_context(self, owner):
        require(owner in (C.addressof(self.memory_owner) + 0x460, 0x145e60820),
                'Unexpected worker memory-context owner')
        ident = self.kernel.GetCurrentThreadId()
        require(ident not in self.context_storage, 'Repeated thread-memory allocation')
        storage = C.create_string_buffer(0x4c0)
        self.context_storage[ident] = storage
        base = C.addressof(storage)
        allocator = base + 0x418
        put_ptr(allocator + 0x20, C.addressof(self.block_acquire))
        put_ptr(allocator + 0x48, C.addressof(self.block_release))
        U64.from_address(allocator + 0x50).value = BLOCK_BYTES
        U64.from_address(allocator + 0x58).value = 2
        put_ptr(allocator + 0x80, allocator + 0x78)
        acquire = ncall(0x1422ce960, PTR, PTR)
        block = acquire(allocator)
        require(block in self.blocks and read_ptr(block) == allocator, 'Native callback block init failed')
        put_ptr(allocator + 0x68, block + BLOCK_BYTES)
        put_ptr(allocator + 0x70, block)
        return base

    def tls_set(self, slot, value):
        require(self.kernel.TlsSetValue(slot, value), 'Native TLS store failed')
        if slot == self.worker_slot:
            ident = self.kernel.GetCurrentThreadId()
            with self.condition:
                if value:
                    require(ident not in self.entered, 'Duplicate worker TLS admission')
                    member = self.membership()
                    require(member is not None and member['thread_id'] == ident,
                            'Worker TLS differs from captured pool/index')
                    self.entered[ident] = member
                else:
                    require(ident in self.entered, 'Worker cleared TLS without native admission')
                    self.departed.add(ident)
                self.condition.notify_all()
        return 1

    def membership(self):
        context = self.kernel.TlsGetValue(self.worker_slot)
        ident = self.kernel.GetCurrentThreadId()
        for pool, index, thread_id in self.threads.values():
            if thread_id != ident:
                continue
            expected = read_ptr(pool + 0xc8) + 0xc0 * index
            if (context == expected and read_ptr(context + 0x88) == pool
                    and U32.from_address(context + 0x90).value == index):
                return {'pool': pool, 'context': context, 'index': index, 'thread_id': ident}
        return None

    def bind(self):
        k = self.kernel
        synchronization = C.WinDLL('kernelbase', winmode=0x800)
        self.memory_slot, self.worker_slot = k.TlsAlloc(), k.TlsAlloc()
        require(0xffffffff not in (self.memory_slot, self.worker_slot), 'Cannot allocate private TLS slots')
        U32.from_address(MEMORY_SLOT).value = self.memory_slot
        U32.from_address(WORKER_SLOT).value = self.worker_slot
        U32.from_address(ARENA_STATE).value = 2
        put_ptr(0x145e60840, None)
        put_ptr(0x1461f9c68, None)
        put_ptr(0x145e762b0, None)

        direct = {
            0x143a3f1f0: k.SetThreadPriority,
            0x143a3f2a0: k.SetThreadPriorityBoost,
            0x143a3f2a8: k.GetCurrentThread,
            0x143a3f2f8: k.Sleep,
            0x143a3f310: k.SetThreadDescription,
            0x143a3f360: k.MultiByteToWideChar,
            0x143a3f390: k.TlsGetValue,
            0x143a3f3f0: k.EnterCriticalSection,
            0x143a3f410: k.LeaveCriticalSection,
            0x143a3f418: k.GetCurrentThreadId,
            0x143a40258: k.QueryPerformanceCounter,
            0x143a402c8: synchronization.WakeByAddressSingle,
            0x143a402d0: synchronization.WaitOnAddress,
        }
        for address, fn in direct.items():
            put_ptr(address, pointer(fn))
        self.import_hook(0x143a3f1c8, U32, (PTR, U32), self.wait)
        self.import_hook(0x143a3f1f8, PTR, (PTR, C.c_long, C.c_long, PTR, U32, U32),
                         self.create_semaphore)
        self.import_hook(0x143a3f2c0, None, (PTR,), self.delete_critical_section)
        self.import_hook(0x143a3f2c8, C.c_int, (PTR, U32), self.initialize_critical_section)
        self.import_hook(0x143a3f398, C.c_int, (U32, PTR), self.tls_set)
        self.import_hook(0x143a3f440, C.c_int, (PTR,), self.close_handle)
        self.import_hook(0x143a40220, PTR, (PTR, C.c_size_t, PTR, PTR, U32, PTR), self.create_thread)
        self.import_hook(0x143a40230, U32, (PTR,), self.resume_thread)
        self.import_hook(0x143a402a8, C.c_int, (PTR, C.c_long, PTR), self.release_semaphore)

        self.hook(0x1402b7e60, PTR, (), lambda: C.addressof(self.memory_owner))
        self.hook(0x14030b3a0, C.c_int, (PTR, U64, C.c_char_p, C.c_char_p, U32), self.format_thread)
        self.hook(0x1422c7ad0, PTR, (PTR, U64, U32, C.c_uint8), self.arena_allocate)
        for address in (0x1402b7910, 0x1422c7560):
            self.hook(address, None, (PTR,), self.arena_free)
        self.hook(0x1422c8910, PTR, (PTR,), self.memory_context)
        self.hook(0x14365ceb4, None, (PTR, U64, U64, PTR, PTR), self.array_construct)
        self.hook(0x14365cdb8, None, (PTR, U64, U64, PTR), self.array_destroy)
        self._bind_allocator_vtables()
        self._bind_private_crt_tls()

    def _bind_allocator_vtables(self):
        acquire = self.callback(PTR, (PTR,), self.allocate_block)
        release = self.callback(None, (PTR, PTR), self.release_block)
        self.block_acquire_vtable = (PTR * 3)(None, None, pointer(acquire))
        self.block_release_vtable = (PTR * 3)(None, None, pointer(release))
        self.block_acquire = (PTR * 1)(C.addressof(self.block_acquire_vtable))
        self.block_release = (PTR * 1)(C.addressof(self.block_release_vtable))

    def _bind_private_crt_tls(self):
        # Native startup touches game-specific static CRT TLS on the calling
        # thread. Redirect only the GS:[0x58] loads to a fixture-local pointer
        # cell. The worker's allocator state is already initialized and its
        # game-private CRT fields are unreachable on the selected path.
        cell = 0x148500080
        put_ptr(cell, C.addressof(self.crt_tls))
        for entry in (0x1422cf24f, 0x1428d3c8b):
            require(C.string_at(entry, 9) == b'\x65\x48\x8b\x04\x25\x58\x00\x00\x00',
                    'Original static TLS operand differs')
            C.memmove(entry, b'\x48\x8d\x05' + struct.pack('<i', cell - entry - 7) + b'\x90\x90', 9)

    @property
    def pool(self):
        require(self.adaptor == ADAPTOR and not self.closed, 'Pool is outside its owned lifetime')
        return self.adaptor + 0x140

    def initialize(self):
        require(self.adaptor is None and not read_ptr(ADAPTOR_SLOT), 'Pool singleton already installed')
        init = ncall(0x1428d1420, None, U32, U32)
        init(PRIMARY, SECONDARY)
        require(read_ptr(ADAPTOR_SLOT) == ADAPTOR, 'Original initializer did not install its singleton')
        self.adaptor = ADAPTOR
        require(ncall(0x1428d1880, PTR)() == self.pool, 'Original common getter returned wrong pool')
        for pool, count in ((ADAPTOR + 0x40, PRIMARY), (self.pool, SECONDARY)):
            require(U32.from_address(pool + 0xe0).value == count
                    and U32.from_address(pool + 0xe8).value == 0
                    and read_ptr(pool + 0xb8) in self.semaphores, 'Native initial pool state differs')
            self.worker_records(pool)
            for index in range(count):
                context = read_ptr(pool + 0xc8) + 0xc0 * index
                require(read_ptr(context + 0x88) == pool
                        and U32.from_address(context + 0x90).value == index
                        and read_ptr(context + 0x48) in self.heap, 'Invalid native worker context')

    def verify_site_getters(self, *getters):
        require(self.started and not self.closed and len(getters) == 2
                and getters == (0x1428d1880, 0x1428d1880), 'Unexpected or unstarted site pool')
        require(all(ncall(entry, PTR)() == self.pool for entry in getters), 'Sites differ in native pool identity')
        return self.pool

    def wait_for_progress(self, ready, missing, label):
        # Nonblocking waits observe owned-worker liveness. The polling
        # interval supplies no elapsed-time cutoff for healthy workers.
        with self.condition:
            while not ready():
                for handle, (_, _, ident) in self.threads.items():
                    require(self.kernel.WaitForSingleObject(handle, 0) == 0x102,
                            f'Worker {ident} exited or could not be inspected before {label}')
                require(not missing(), f'Original workers reached idle without {label}')
                self.condition.wait(0.1)

    def queues_empty(self):
        for pool in (ADAPTOR + 0x40, self.pool):
            count = U32.from_address(pool + 0xe0).value
            contexts = read_ptr(pool + 0xc8)
            queues = (pool, *(contexts + 0xc0 * index for index in range(count)))
            if any(U64.from_address(queue).value != U64.from_address(queue + 0x40).value
                   for queue in queues):
                return False
        return True

    def idle(self):
        return len(self.waiting) == PRIMARY + SECONDARY and self.queues_empty()

    def start(self):
        require(self.adaptor == ADAPTOR and not self.started, 'Pool is uninitialized or already started')
        ncall(0x1428d1450, None)()
        require(len(self.threads) == PRIMARY + SECONDARY, 'Original start did not create all owned workers')
        # The worker entry has no queued work or external dependencies here.
        # Wait for actual TLS admissions, without stopping healthy progress
        # based on a fixed iteration count.
        self.wait_for_progress(lambda: len(self.entered) == PRIMARY + SECONDARY,
                               lambda: False, 'scheduler TLS admission')
        require(all(U32.from_address(pool + 0xe8).value == count for pool, count in
                    ((ADAPTOR + 0x40, PRIMARY), (self.pool, SECONDARY))), 'Native started counts differ')
        self.started = True

    def stop(self):
        require(self.adaptor == ADAPTOR and not self.closed, 'No owned pool to stop')
        require(self.queues_empty(), 'Pool stop requires drained native queues')
        if self.started:
            self.wait_for_progress(self.idle, lambda: False, 'native queue drain and worker idle')
        ncall(0x1428d1890, PTR, PTR, U32)(ADAPTOR, 0)
        require(not read_ptr(ADAPTOR_SLOT) and not self.semaphores
                and set(self.threads) == self.joined and set(self.entered) == self.departed,
                'Original pool shutdown did not join every owned worker')
        require(not self.critical_sections and not self.heap, 'Native backing ownership did not drain')
        for storage in self.context_storage.values():
            require(U32.from_buffer(storage, 0x410).value == 0, 'Native thread memory counter leaked')
        for block in tuple(self.blocks):
            released = U64.from_address(block + 0x10).value
            published = U64.from_address(block + 0x18).value
            require(released in (published, published + 1), 'Native callback references remain outstanding')
            require(self.kernel.VirtualFree(block, 0, 0x8000), 'Cannot release terminal fixture backing block')
            self.blocks.remove(block)
        require(self.kernel.TlsSetValue(self.memory_slot, None)
                and self.kernel.TlsFree(self.memory_slot) and self.kernel.TlsFree(self.worker_slot),
                'Cannot release private TLS slots')
        self.closed = True


def native_component(kernel, pages):
    runtime = PoolRuntime(kernel)
    host.allocate_pages(kernel, pages)
    runtime.bind()
    for page in pages:
        host.protect(kernel, page, 0x20 if page in CODE else 4 if page in RW_DATA else 2)
    host.flush(kernel)
    runtime.initialize()
    try:
        runtime.verify_site_getters(0x1428d1880, 0x1428d1880)
    except ValueError:
        require(not runtime.threads, 'Unexpected worker before original start')
    else:
        raise ValueError('Initialized but unstarted pool passed membership admission')
    runtime.start()
    runtime.verify_site_getters(0x1428d1880, 0x1428d1880)
    trace = []
    def command(payload):
        member = runtime.membership()
        require(member is not None, 'Original claim callback ran outside its captured worker')
        tag = U64.from_address(payload + 0x10).value
        with runtime.condition:
            trace.append((tag, member))
            runtime.condition.notify_all()

    callback = runtime.callback(None, (PTR,), command)
    # Give the single outside producer its private memory context. Native
    # allocation and worker callback release exercise the untagged route.
    memory = runtime.memory_context(0x145e60820)
    allocate = ncall(0x1422ce9f0, PTR, PTR, U64, U64)
    push = ncall(0x1428d2b80, U64, PTR, PTR)
    for tag, pool in ((1, runtime.pool), (2, ADAPTOR + 0x40)):
        payload = allocate(memory + 0x418, 32, 8)
        require(payload and payload & -BLOCK_BYTES in runtime.blocks,
                'Original callback allocation did not use a private native block')
        C.memmove(payload, struct.pack('<4Q', 0, pointer(callback), tag, 0), 32)
        push(pool, C.byref(U64(payload)))
        runtime.release_semaphore(read_ptr(pool + 0xb8), 1, None)
    runtime.wait_for_progress(lambda: len(trace) == 2, runtime.idle, 'two original worker claims')
    require(sorted((tag, member['pool']) for tag, member in trace)
            == [(1, runtime.pool), (2, ADAPTOR + 0x40)], 'Wrong or foreign worker claim')
    runtime.stop()
    for base in sorted({page & ~0xffff for page in pages}, reverse=True):
        require(kernel.VirtualFree(base, 0, 0x8000), 'Private pool page release failed')
    return {
        'constructor_getter_operands': 2,
        'unstarted_refused': True,
        'wrong_pool_distinguished': True,
        'worker_entries': list(runtime.entered.values()),
        'claims': trace,
        'native_joins': len(runtime.joined),
        'native_shutdown_complete': runtime.closed,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--exe', required=True, type=Path)
    parser.add_argument('--run-owned-pool', action='store_true')
    args = parser.parse_args()
    try:
        kernel, _ = host.host_preflight()
        exe = host.regular(args.exe)
        drives = {exe.anchor, Path.cwd().anchor, Path(sys.executable).anchor}
        drives.update(drive for drive in ('C:\\', 'D:\\') if Path(drive).is_dir())
        require(all(available_bytes(kernel, drive) >= 40_000_000_000 for drive in drives),
                'Insufficient caller-available disk floor')
        image = host.read_pinned(exe, host.EXE, 'Starfield EXE', keep=True)
        prior.original_getter_sites(image)
        pages = host.pe_pages(image, CODE, DATA)
        outcome = {'exe_sha256': host.EXE, 'code_pages': len(CODE), 'data_pages': len(DATA)}
        if args.run_owned_pool:
            host.cpu_check(kernel)
            outcome['scope'] = 'Original native Jobs2Adaptor and worker component with private backing'
            outcome['result'] = native_component(kernel, pages)
            host.read_pinned(exe, host.EXE, 'Starfield EXE after original pool component')
        else:
            outcome['scope'] = 'Static original pool preflight only'
    except (OSError, ValueError, struct.error) as error:
        parser.exit(1, f'D5BM pool refused: {error}\n')
    print(json.dumps(outcome, sort_keys=True))


if __name__ == '__main__':
    main()
