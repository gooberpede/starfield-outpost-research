; SPDX-License-Identifier: GPL-3.0-or-later
; D5AM derivative. Snapshot before, native receiver gate after displaced operation.
; This catches a watch published while an initially unmatched operation is in flight.
; All paths preserve native state; unmatched receivers avoid the C++ callback.
; Acquired is reached only from successful CAS (equal subtraction flags).
EXTERN D5AM_capture:PROC
EXTERN D5AM_causal_core_active:QWORD
EXTERN D5AM_causal_enabled:QWORD
EXTERN D5AM_causal_fixture_before_operation:QWORD
EXTERN D5AM_causal_fixture_before_admission:QWORD
EXTERN D5AM_causal_bridge_active:QWORD
EXTERN D5AM_causal_counter_faults:QWORD
EXTERN D5AM_watched_lock:QWORD
EXTERN D5AM_watched_state:QWORD
EXTERN D5AM_generation:QWORD
EXTERN D5AM_registry_serial:QWORD
EXTERN D5AN_counter_next:PROC
EXTERN D5AN_counter_leave:PROC
.code
save_state MACRO frame_bytes
 push rbp
 .pushreg rbp
 pushfq
 .allocstack 8
 push rax
 .allocstack 8
 push rcx
 .allocstack 8
 push rdx
 .allocstack 8
 push r8
 .allocstack 8
 push r9
 .allocstack 8
 push r10
 .allocstack 8
 push r11
 .allocstack 8
 sub rsp,frame_bytes
 .allocstack frame_bytes
 mov rbp,rsp
 .setframe rbp,0
 .endprolog
 movdqu [rsp+48],xmm0
 movdqu [rsp+64],xmm1
 movdqu [rsp+80],xmm2
 movdqu [rsp+96],xmm3
 movdqu [rsp+112],xmm4
 movdqu [rsp+128],xmm5
ENDM
fixture_before MACRO frame_bytes,receiver,kind
 LOCAL no_fixture
 mov [rsp+152],r9
 mov rax,D5AM_causal_fixture_before_operation
 test rax,rax
 jz no_fixture
 mov rcx,receiver
 mov edx,kind
 call rax
no_fixture:
 mov r9,[rsp+152]
 mov rax,[rsp+frame_bytes+48]
 mov rcx,[rsp+frame_bytes+40]
 mov rdx,[rsp+frame_bytes+32]
ENDM
snapshot MACRO frame_bytes
 mov r10,D5AM_registry_serial
 mov r9,D5AM_generation
 mov [rsp+32],r10
 mov r10,[rsp+frame_bytes+72]
 lea r10,[r10-5]
 mov [rsp+40],r10
ENDM
save_flags MACRO frame_bytes
 pushfq
 pop QWORD PTR [rsp+frame_bytes+56]
ENDM
restore_state MACRO frame_bytes
 movdqu xmm0,[rsp+48]
 movdqu xmm1,[rsp+64]
 movdqu xmm2,[rsp+80]
 movdqu xmm3,[rsp+96]
 movdqu xmm4,[rsp+112]
 movdqu xmm5,[rsp+128]
 push QWORD PTR [rsp+frame_bytes+56]
 popfq
 mov r11,[rsp+frame_bytes]
 mov r10,[rsp+frame_bytes+8]
 mov r9,[rsp+frame_bytes+16]
 mov r8,[rsp+frame_bytes+24]
 mov rdx,[rsp+frame_bytes+32]
 mov rcx,[rsp+frame_bytes+40]
 mov rax,[rsp+frame_bytes+48]
 lea rsp,[rbp+frame_bytes+64]
 pop rbp
ENDM

enter_producer MACRO failed_label
 LOCAL core_held,bridge_held,rollback
 mov rcx,D5AM_causal_core_active
 mov edx,33
 mov r8d,5
 xor r9d,r9d
 call D5AN_counter_next
 test al,al
 jnz core_held
 jmp failed_label
core_held:
 lea rcx,D5AM_causal_bridge_active
 mov edx,42
 mov r8d,6
 xor r9d,r9d
 call D5AN_counter_next
 test al,al
 jnz bridge_held
 jmp rollback
bridge_held:
 mov rax,D5AM_causal_enabled
 cmp BYTE PTR [rax],0
 jne @F
 lea rcx,D5AM_causal_bridge_active
 mov edx,42
 mov r8d,16
 call D5AN_counter_leave
rollback:
 mov rcx,D5AM_causal_core_active
 mov edx,33
 mov r8d,17
 call D5AN_counter_leave
 jmp failed_label
@@:
ENDM
leave_producer MACRO
 lea rcx,D5AM_causal_bridge_active
 mov edx,42
 mov r8d,16
 call D5AN_counter_leave
 mov rcx,D5AM_causal_core_active
 mov edx,33
 mov r8d,17
 call D5AN_counter_leave
ENDM

PUBLIC D5AM_pending
D5AM_pending PROC FRAME
 save_state 160
 mov QWORD PTR [rsp+144],0
 mov rax,D5AM_causal_enabled
 cmp BYTE PTR [rax],0
 je pending_unadmitted
 mov rax,D5AM_causal_fixture_before_admission
 test rax,rax
 jz pending_enter_native
 mov rcx,r14
 mov edx,2
 call rax
pending_enter_native:
 enter_producer pending_unadmitted
 mov QWORD PTR [rsp+144],1
pending_unadmitted:
 mov rax,[rsp+208]
 mov rcx,[rsp+200]
 mov rdx,[rsp+192]
 snapshot 160
 fixture_before 160,r14,2
 lock xadd DWORD PTR [r14+4],eax
 mov [rsp+208],rax
 save_flags 160
 cmp QWORD PTR [rsp+144],0
 je pending_restore
 cmp r14,D5AM_watched_lock
 jne pending_restore
 mov rcx,r14
 mov edx,DWORD PTR [rsp+208]
 mov r8d,2
 call D5AM_capture
pending_restore:
 cmp QWORD PTR [rsp+144],0
 je pending_restore_state
 leave_producer
pending_restore_state:
 restore_state 160
 ret
D5AM_pending ENDP

PUBLIC D5AM_acquired
D5AM_acquired PROC FRAME
 cmp r14,r14
 save_state 160
 mov QWORD PTR [rsp+144],0
 mov rax,D5AM_causal_enabled
 cmp BYTE PTR [rax],0
 je acquired_unadmitted
 mov rax,D5AM_causal_fixture_before_admission
 test rax,rax
 jz acquired_enter_native
 mov rcx,r14
 mov edx,3
 call rax
acquired_enter_native:
 enter_producer acquired_unadmitted
 mov QWORD PTR [rsp+144],1
acquired_unadmitted:
 mov rax,[rsp+208]
 mov rcx,[rsp+200]
 mov rdx,[rsp+192]
 snapshot 160
 fixture_before 160,r14,3
 mov eax,DWORD PTR [rsp+224]
 mov DWORD PTR [r14],eax
 mfence
 cmp QWORD PTR [rsp+144],0
 je acquired_restore
 cmp r14,D5AM_watched_lock
 jne acquired_restore
 mov rcx,r14
 mov edx,DWORD PTR [rsp+208]
 mov r8d,3
 call D5AM_capture
acquired_restore:
 cmp QWORD PTR [rsp+144],0
 je acquired_restore_state
 leave_producer
acquired_restore_state:
 restore_state 160
 ret
D5AM_acquired ENDP

PUBLIC D5AM_recursive
D5AM_recursive PROC FRAME
 save_state 160
 mov QWORD PTR [rsp+144],0
 mov rax,D5AM_causal_enabled
 cmp BYTE PTR [rax],0
 je recursive_unadmitted
 mov rax,D5AM_causal_fixture_before_admission
 test rax,rax
 jz recursive_enter_native
 mov rcx,r14
 mov edx,4
 call rax
recursive_enter_native:
 enter_producer recursive_unadmitted
 mov QWORD PTR [rsp+144],1
recursive_unadmitted:
 mov rax,[rsp+208]
 mov rcx,[rsp+200]
 mov rdx,[rsp+192]
 snapshot 160
 fixture_before 160,r14,4
 lock xadd DWORD PTR [r14+4],esi
 save_flags 160
 cmp QWORD PTR [rsp+144],0
 je recursive_restore
 cmp r14,D5AM_watched_lock
 jne recursive_restore
 mov rcx,r14
 mov edx,esi
 mov r8d,4
 call D5AM_capture
recursive_restore:
 cmp QWORD PTR [rsp+144],0
 je recursive_restore_state
 leave_producer
recursive_restore_state:
 restore_state 160
 ret
D5AM_recursive ENDP

PUBLIC D5AM_reader
D5AM_reader PROC FRAME
 save_state 160
 mov QWORD PTR [rsp+144],0
 mov rax,D5AM_causal_enabled
 cmp BYTE PTR [rax],0
 je reader_unadmitted
 mov rax,D5AM_causal_fixture_before_admission
 test rax,rax
 jz reader_enter_native
 mov rcx,rdi
 mov edx,5
 call rax
reader_enter_native:
 enter_producer reader_unadmitted
 mov QWORD PTR [rsp+144],1
reader_unadmitted:
 mov rax,[rsp+208]
 mov rcx,[rsp+200]
 mov rdx,[rsp+192]
 snapshot 160
 fixture_before 160,rdi,5
 lock xadd DWORD PTR [rdi],eax
 test eax,0ffc00000h
 mov [rsp+208],rax
 save_flags 160
 cmp QWORD PTR [rsp+144],0
 je reader_restore
 cmp rdi,D5AM_watched_state
 jne reader_restore
 lea rcx,[rdi-4]
 mov edx,DWORD PTR [rsp+208]
 mov r8d,5
 call D5AM_capture
reader_restore:
 cmp QWORD PTR [rsp+144],0
 je reader_restore_state
 leave_producer
reader_restore_state:
 restore_state 160
 ret
D5AM_reader ENDP

PUBLIC D5AM_reader_release
D5AM_reader_release PROC FRAME
 save_state 160
 mov QWORD PTR [rsp+144],0
 mov rax,D5AM_causal_enabled
 cmp BYTE PTR [rax],0
 je reader_release_unadmitted
 mov rax,D5AM_causal_fixture_before_admission
 test rax,rax
 jz reader_release_enter_native
 mov rcx,rcx
 mov edx,6
 call rax
reader_release_enter_native:
 enter_producer reader_release_unadmitted
 mov QWORD PTR [rsp+144],1
reader_release_unadmitted:
 mov rax,[rsp+208]
 mov rcx,[rsp+200]
 mov rdx,[rsp+192]
 snapshot 160
 fixture_before 160,rcx,6
 lock xadd DWORD PTR [rcx],edx
 mov eax,edx
 mov [rsp+208],rax
 mov [rsp+192],rdx
 save_flags 160
 cmp QWORD PTR [rsp+144],0
 je reader_release_restore
 cmp rcx,D5AM_watched_state
 jne reader_release_restore
 lea rcx,[rcx-4]
 mov edx,DWORD PTR [rsp+192]
 mov r8d,6
 call D5AM_capture
reader_release_restore:
 cmp QWORD PTR [rsp+144],0
 je reader_release_restore_state
 leave_producer
reader_release_restore_state:
 restore_state 160
 ret
D5AM_reader_release ENDP

PUBLIC D5AM_writer_release
D5AM_writer_release PROC FRAME
 ; The original release helper is a leaf entered with RSP modulo 16 == 8.
 ; An inserted CALL enters this bridge with RSP modulo 16 == 0.
 save_state 168
 mov QWORD PTR [rsp+144],0
 mov rax,D5AM_causal_enabled
 cmp BYTE PTR [rax],0
 je writer_release_unadmitted
 mov rax,D5AM_causal_fixture_before_admission
 test rax,rax
 jz writer_release_enter_native
 mov rcx,rcx
 mov edx,7
 call rax
writer_release_enter_native:
 enter_producer writer_release_unadmitted
 mov QWORD PTR [rsp+144],1
writer_release_unadmitted:
 mov rax,[rsp+216]
 mov rcx,[rsp+208]
 mov rdx,[rsp+200]
 snapshot 168
 fixture_before 168,rcx,7
 lock xadd DWORD PTR [rcx],eax
 test eax,0fffh
 mov [rsp+216],rax
 save_flags 168
 cmp QWORD PTR [rsp+144],0
 je writer_release_restore
 cmp rcx,D5AM_watched_state
 jne writer_release_restore
 lea rcx,[rcx-4]
 mov edx,DWORD PTR [rsp+216]
 mov r8d,7
 call D5AM_capture
writer_release_restore:
 cmp QWORD PTR [rsp+144],0
 je writer_release_restore_state
 leave_producer
writer_release_restore_state:
 restore_state 168
 ret
D5AM_writer_release ENDP

PUBLIC D5AM_recursive_release
D5AM_recursive_release PROC FRAME
 save_state 168
 mov QWORD PTR [rsp+144],0
 mov rax,D5AM_causal_enabled
 cmp BYTE PTR [rax],0
 je recursive_release_unadmitted
 mov rax,D5AM_causal_fixture_before_admission
 test rax,rax
 jz recursive_release_enter_native
 mov rcx,rcx
 mov edx,8
 call rax
recursive_release_enter_native:
 enter_producer recursive_release_unadmitted
 mov QWORD PTR [rsp+144],1
recursive_release_unadmitted:
 mov rax,[rsp+216]
 mov rcx,[rsp+208]
 mov rdx,[rsp+200]
 snapshot 168
 fixture_before 168,rcx,8
 mov eax,0ffc00000h
 lock xadd DWORD PTR [rcx],eax
 mov [rsp+216],rax
 save_flags 168
 cmp QWORD PTR [rsp+144],0
 je recursive_release_restore
 cmp rcx,D5AM_watched_state
 jne recursive_release_restore
 lea rcx,[rcx-4]
 mov edx,DWORD PTR [rsp+216]
 mov r8d,8
 call D5AM_capture
recursive_release_restore:
 cmp QWORD PTR [rsp+144],0
 je recursive_release_restore_state
 leave_producer
recursive_release_restore_state:
 restore_state 168
 ret
D5AM_recursive_release ENDP

PUBLIC D5AM_reader_ready
D5AM_reader_ready PROC FRAME
 save_state 160
 mov QWORD PTR [rsp+144],0
 mov rax,D5AM_causal_enabled
 cmp BYTE PTR [rax],0
 je reader_ready_unadmitted
 mov rax,D5AM_causal_fixture_before_admission
 test rax,rax
 jz reader_ready_enter_native
 mov rcx,rdi
 mov edx,15
 call rax
reader_ready_enter_native:
 enter_producer reader_ready_unadmitted
 mov QWORD PTR [rsp+144],1
reader_ready_unadmitted:
 mov rax,[rsp+208]
 mov rcx,[rsp+200]
 mov rdx,[rsp+192]
 snapshot 160
 fixture_before 160,rdi,15
 mov rbx,QWORD PTR [rbp+296]
 cmp QWORD PTR [rsp+144],0
 je reader_ready_restore
 cmp rdi,D5AM_watched_state
 jne reader_ready_restore
 lea rcx,[rdi-4]
 xor edx,edx
 mov r8d,15
 call D5AM_capture
reader_ready_restore:
 cmp QWORD PTR [rsp+144],0
 je reader_ready_restore_state
 leave_producer
reader_ready_restore_state:
 restore_state 160
 ret
D5AM_reader_ready ENDP

PUBLIC D5AM_inline_writer_release
D5AM_inline_writer_release PROC FRAME
 save_state 160
 mov QWORD PTR [rsp+144],0
 mov rax,D5AM_causal_enabled
 cmp BYTE PTR [rax],0
 je inline_writer_release_unadmitted
 mov rax,D5AM_causal_fixture_before_admission
 test rax,rax
 jz inline_writer_release_enter_native
 mov rcx,rdi
 mov edx,7
 call rax
inline_writer_release_enter_native:
 enter_producer inline_writer_release_unadmitted
 mov QWORD PTR [rsp+144],1
inline_writer_release_unadmitted:
 mov rax,[rsp+208]
 mov rcx,[rsp+200]
 mov rdx,[rsp+192]
 snapshot 160
 fixture_before 160,rdi,7
 mov DWORD PTR [rsp+152],ecx
 mov r10d,DWORD PTR [rdi]
 mov DWORD PTR [rsp+156],r10d
 lock xadd DWORD PTR [rdi+4],ecx
 mov [rsp+200],rcx
 save_flags 160
 cmp QWORD PTR [rsp+144],0
 je inline_writer_release_restore
 cmp rdi,D5AM_watched_lock
 jne inline_writer_release_restore
 mov rcx,rdi
 mov edx,DWORD PTR [rsp+200]
 mov r10d,DWORD PTR [rsp+156]
 shl r10,32
 or rdx,r10
 mov r8d,7
 mov r10d,DWORD PTR [rsp+152]
 shl r10,32
 or r8,r10
 call D5AM_capture
inline_writer_release_restore:
 cmp QWORD PTR [rsp+144],0
 je inline_writer_release_restore_state
 leave_producer
inline_writer_release_restore_state:
 restore_state 160
 ret
D5AM_inline_writer_release ENDP


PUBLIC D5AM_inline_recursive_release
D5AM_inline_recursive_release PROC FRAME
 save_state 160
 mov QWORD PTR [rsp+144],0
 mov rax,D5AM_causal_enabled
 cmp BYTE PTR [rax],0
 je inline_recursive_release_unadmitted
 mov rax,D5AM_causal_fixture_before_admission
 test rax,rax
 jz inline_recursive_release_enter_native
 mov rcx,rdi
 mov edx,8
 call rax
inline_recursive_release_enter_native:
 enter_producer inline_recursive_release_unadmitted
 mov QWORD PTR [rsp+144],1
inline_recursive_release_unadmitted:
 mov rax,[rsp+208]
 mov rcx,[rsp+200]
 mov rdx,[rsp+192]
 snapshot 160
 fixture_before 160,rdi,8
 mov DWORD PTR [rsp+152],ecx
 mov r10d,DWORD PTR [rdi]
 mov DWORD PTR [rsp+156],r10d
 lock xadd DWORD PTR [rdi+4],ecx
 mov [rsp+200],rcx
 save_flags 160
 cmp QWORD PTR [rsp+144],0
 je inline_recursive_release_restore
 cmp rdi,D5AM_watched_lock
 jne inline_recursive_release_restore
 mov rcx,rdi
 mov edx,DWORD PTR [rsp+200]
 mov r10d,DWORD PTR [rsp+156]
 shl r10,32
 or rdx,r10
 mov r8d,8
 mov r10d,DWORD PTR [rsp+152]
 shl r10,32
 or r8,r10
 call D5AM_capture
inline_recursive_release_restore:
 cmp QWORD PTR [rsp+144],0
 je inline_recursive_release_restore_state
 leave_producer
inline_recursive_release_restore_state:
 restore_state 160
 ret
D5AM_inline_recursive_release ENDP


END
